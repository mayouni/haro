"""Judges rung 20, refinement over the program graph of rung 18, for the Ring++ face:
   python haro/spike/v20/refine_check.py [--plant] [--quick] [--wide]      (exit 1 on any failure)

  F  the fixtures (v20/fixtures.txt, composed before the code): programs, proposals, and the verdict each must get -- the stage that refuses it,
     the words the refusal says, the RCP primitives a sentence lowers to, the canonical text that is left. For EVERY fixture, whatever it says:
     a refused proposal changes nothing; an admitted one changes exactly one line of text and no id; the inverses captured before each change land
     put back the original text, byte for byte, with its ids; the log replayed from the base text through the gate gives the same verdicts and the
     same text, and the transactions alone (no gate) the same text; the refined text is its own canonical form on the OTHER printer, rnxc fmt
  T  the twelve primitives, one fixture each or more, and a transaction that fails halfway undoes what it did
  L  declarations that do not lift: the gate fails closed
  C  commutation: RCP's predicate over two sentences' footprints is sound (applied in both orders, what it calls commuting gives one result),
     and the rows that do not commute are shown to differ
  A  a text edit read back as the refinements it amounts to, each judged by the gate on the old program
  S  the live gate: the same proposals -- the fixtures' and a sweep of points x values x actors x postures -- put to Softanza's own
     stzRefinableCode on the Ring++ package; the two gates must agree on admitted-or-not and on the stage that refuses. What this gate checks and
     that one does not (the value parses, the sentence is well formed, the id is current) is counted apart, never folded in
  D  controls that must FAIL: a gate without its trust stage, its constraint stage, its governance stage, its derivation stage; one that edits the
     live program before it has judged; a cascade that sees nothing; an inverse that loses the ids; a revert that does not check what it restores
  H  Haro's own history: a refinement drafted against a literal of one revision -- does it still land after the next human edit? Landed, refused as
     stale (the value changed), or aimed at a different variable (the hazard a name-checking gate catches): counted
  K  a corpus: a literal of each of many real Ring files made a point, refined, and judged by a second route (the line spliced by hand), by the
     other printer (rnxc fmt), by the compiler (rnxc dis: the same code shape) and by locality (one line out, one line in)
The engine is v20/refine.py; the graph is rung 18's, the ids rung 19's.
"""
import contextlib, copy, glob, json, os, re, subprocess, sys, tempfile, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'v19'))
sys.path.insert(0, os.path.join(HERE, '..'))
if os.environ.get('REFINE_SRC'):                     # probes/mutate.py judges the court by putting a defect into the engine and loading it here
    import importlib.util
    _spec = importlib.util.spec_from_file_location('refine', os.environ['REFINE_SRC'])
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules['refine'] = _mod
    _spec.loader.exec_module(_mod)
import refine, scoped, ids, l1, random
import ids_check
from haro_forge import Gbnf

PLANT = '--plant' in sys.argv
QUICK = '--quick' in sys.argv
WIDE = '--wide' in sys.argv
ONLY_FX = '--fx' in sys.argv
SCRATCH = os.path.join(HERE, 'scratch')
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
ORACLE = os.environ.get('RING') or os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
PACKAGE = os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
FIXTURE_FLOOR, STEP_FLOOR = 55, 150
SWEEP_FLOOR = 300
CORPUS_FILES_FLOOR, CORPUS_CANDIDATES_FLOOR = 25, 100
LAND_FLOOR = 0.95
fails = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def write(name, data):
    os.makedirs(SCRATCH, exist_ok=True)
    p = os.path.join(SCRATCH, name)
    open(p, 'wb').write(data if isinstance(data, bytes) else data.encode('latin-1'))
    return p


def run(cmd, timeout=300, cwd=None):
    p = subprocess.run(cmd, capture_output=True, timeout=timeout, cwd=cwd)
    return p.returncode, p.stdout.decode('latin-1').replace('\r\n', '\n'), p.stderr.decode('latin-1').replace('\r\n', '\n')


# ---- the fixtures ---------------------------------------------------------------------------------------------------------------------------

SECTIONS = ('program', 'context', 'edited', 'do', 'text', 'run', 'lift', 'cascade', 'tx', 'error', 'ids', 'commute', 'audit')


def read_fixtures(path):
    fx, cur, sec = [], None, None
    raw = open(path, 'rb').read().decode('latin-1').replace('\r\n', '\n')
    for line in raw.split('\n'):
        if line.startswith('=== '):
            fid, _, name = line[4:].partition(' ')
            cur = {'id': fid, 'name': name}
            for s in SECTIONS:
                cur[s] = None
            fx.append(cur)
            sec = None
        elif cur is None or line.startswith('~~~'):
            continue
        elif line.startswith('--- ') and line[4:] in SECTIONS:
            sec = line[4:]
            cur[sec] = []
        elif sec is not None:
            cur[sec].append(line)
    for f in fx:
        for s in SECTIONS:
            lines = f[s]
            if lines is None:
                continue
            while lines and lines[-1] == '':
                lines.pop()
        for s in ('program', 'edited', 'text'):
            if f[s] is not None:
                f[s] = '\n'.join(f[s]) + '\n'
        if f['context'] is not None:
            f['context'] = refine.parse_context('\n'.join(f['context']))
    return fx


def parse_verdict(v):
    """`admitted`, `flagged words`, `rejected STAGE words`, each optionally followed by ` tx=a,b` -> dict."""
    tx = None
    m = re.search(r'\s+tx=([\w.,]+)$', v)
    if m:
        tx, v = m.group(1).split(','), v[:m.start()]
    parts = v.split(None, 2)
    d = {'status': parts[0], 'tx': tx, 'stage': None, 'words': ''}
    if parts[0] == 'rejected':
        d['stage'] = parts[1]
        d['words'] = parts[2] if len(parts) > 2 else ''
    elif parts[0] == 'flagged':
        d['words'] = ' '.join(parts[1:])
    return d


def judge_outcome(out, exp):
    bad = []
    if out.status != exp['status']:
        bad.append('verdict %s (%s: %s), want %s' % (out.status, out.stage, out.why[:100], exp['status']))
        return bad
    if exp['status'] == 'rejected':
        if out.stage != exp['stage']:
            bad.append('refused at %s (%s), want %s' % (out.stage, out.why[:100], exp['stage']))
        elif exp['words'].lower() not in out.why.lower():
            bad.append("refusal says '%s', want it to hold '%s'" % (out.why[:120], exp['words']))
    if exp['status'] == 'flagged' and exp['words'].lower() not in ' | '.join(out.warnings).lower():
        bad.append("warnings %s, want one holding '%s'" % (out.warnings, exp['words']))
    if exp['tx'] is not None and [p['op'] for p in out.tx] != exp['tx']:
        bad.append('lowered to %s, want %s' % ([p['op'] for p in out.tx], exp['tx']))
    return bad


def changed_lines(diff):
    return [x for x in diff if x[:1] in '+-' and not x.startswith(('+++', '---'))]


def rnxc_fmt_ok(text, name):
    p = write(name, text)
    rc, out, err = run([RNXC, 'fmt', '--check', p])
    return rc == 0


def run_program(exe, text, name):
    p = write(name, text)
    rc, out, err = run([exe, p], timeout=60)
    return out.strip()


def run_steps(f, stats):
    """The steps of a refinement fixture through the gate: -> (list of failures, the model)."""
    bad = []
    m = refine.Model(f['program'], f['context'] or {})
    if m.text() != f['program']:
        return ['the program is not its own canonical text (the diff a refinement shows is the printer\'s)'], m
    start_ids = ids.ids_of(m.g)
    start_text = m.text()
    for n, line in enumerate(f['do'] or [], 1):
        if line.strip() == 'EDIT':
            m.edit(f['edited'])
            start_text, start_ids = None, None
            continue
        sent, _, verdict = line.rpartition(' => ')
        exp = parse_verdict(verdict)
        before_text, before_hash = m.text(), m.hash()
        before_ids = ids.ids_of(m.g)
        out = m.refine(sent)
        stats['steps'] += 1
        stats[out.status] = stats.get(out.status, 0) + 1
        if out.stage:
            stats[out.stage] = stats.get(out.stage, 0) + 1
        for why in judge_outcome(out, exp):
            bad.append('step %d: %s' % (n, why))
        if not out.admitted:
            if m.text() != before_text or m.hash() != before_hash:
                bad.append('step %d: a refused proposal changed the program' % n)
            if ids.ids_of(m.g) != before_ids:
                bad.append('step %d: a refused proposal changed the ids' % n)
        else:
            ch = changed_lines(out.diff)
            if len([x for x in ch if x[0] == '-']) != 1 or len([x for x in ch if x[0] == '+']) != 1:
                bad.append('step %d: an admitted refinement changed %d line(s), not one out and one in' % (n, len(ch)))
            if ids.ids_of(m.g) != before_ids:
                bad.append('step %d: an admitted refinement moved an id' % n)
    return bad, m, start_text, start_ids


def check_fixture(f, stats):
    bad = []
    if f['do'] is None and f['lift'] is None:
        return ['has neither steps nor a lift']
    m0 = refine.Model(f['program'], f['context'] or {})
    if m0.text() != f['program']:
        return ["the program is not its own canonical text (the diff a refinement shows is the printer's)"]
    if f['lift'] is not None:
        got = refine.show_lift(m0.lift())
        want = f['lift']
        wants_err = [w[6:] for w in want if w.startswith('error ')]
        want_plain = [w for w in want if not w.startswith('error ')]
        got_plain = [g for g in got if not g.startswith('error ')]
        got_err = [g[6:] for g in got if g.startswith('error ')]
        if (want_plain or not wants_err) and got_plain != want_plain:
            bad.append('lift: %s, want %s' % (got_plain, want_plain))
        for w in wants_err:
            if not any(w.lower() in g.lower() for g in got_err):
                bad.append("lift: no error holds '%s' (errors: %s)" % (w, got_err))
        if not wants_err and got_err:
            bad.append('lift: unexpected errors %s' % got_err)
        stats['lifts'] += 1
    if f['cascade'] is not None:
        L = m0.lift()
        names = {w.split()[0] for w in f['cascade']}
        got = []
        for p in L['points']:
            if p['name'] in names:
                c = refine.cascade(m0.g, p)
                for what in ('reads', 'writes'):
                    rows = c[what]
                    got.append('%s %s%s' % (p['name'], what, (' ' + ' | '.join('@%d %s' % r for r in rows)) if rows else ''))
        if got != f['cascade']:
            bad.append('cascade: %s, want %s' % (got, f['cascade']))
    if f['do'] is None:
        return bad
    res = run_steps(f, stats)
    if len(res) == 2:
        bad += res[0]
        return bad
    steps_bad, m, start_text, start_ids = res
    bad += steps_bad
    want_text = f['text'] if f['text'] is not None else f['program']
    if m.text() != want_text:
        bad.append('final text:\n' + m.text() + 'want:\n' + want_text)
    # the inverses put the original back, byte for byte, with its ids -- unless a human edit stands between (the ids are carried then)
    if start_text is not None and not any(e['kind'] == 'edit' for e in m.log):
        g = copy.deepcopy(m.g)
        for ev in reversed(m.admitted()):
            g, _ = refine.apply_tx(g, ev['inverse'], inplace=False)
        if refine.text_of(g) != start_text:
            bad.append('the inverses did not restore the original text')
        if ids.ids_of(g) != start_ids:
            bad.append('the inverses did not restore the ids')
    # replay: the same verdicts and text through the gate; the same text from the transactions alone
    m2, diffs = refine.replay(f['program'], json.loads(json.dumps(m.log)), f['context'] or {})
    if diffs or m2.text() != m.text():
        bad.append('the log replayed from the base text through the gate differs: %s' % diffs[:2])
    if not any(e['kind'] == 'edit' for e in m.log):
        if refine.text_of(refine.replay_tx(f['program'], m.log)) != m.text():
            bad.append('the transactions applied without the gate give another text')
    # the other printer
    if m.text() != start_text and not rnxc_fmt_ok(m.text(), 'fmt_%s.ring' % f['id']):
        bad.append('rnxc fmt does not call the refined text canonical')
    stats['events'] += len(m.log)
    # the oracle
    if f['run'] is not None:
        want = [x.strip().replace('\\n', '\n') for x in f['run'][0].split(':', 1)[1].split(' | ')]
        before = run_program(ORACLE, f['program'], 'run_%s_a.ring' % f['id'])
        after = run_program(ORACLE, m.text(), 'run_%s_b.ring' % f['id'])
        if [before, after] != want:
            bad.append('on the oracle the program prints %s, want %s' % ([before, after], want))
        rb = run_program(RNXC, f['program'], 'run_%s_c.ring' % f['id'])
        ra = run_program(RNXC, m.text(), 'run_%s_d.ring' % f['id'])
        if [rb, ra] != want:
            bad.append('on rnxc the program prints %s, want %s' % ([rb, ra], want))
        stats['runs'] += 1
    return bad


def check_tx_fixture(f, stats):
    bad = []
    m = refine.Model(f['program'])
    if m.text() != f['program']:
        return ['the program is not its own canonical text']
    tx = [json.loads(x) for x in f['tx']]
    before_text, before_ids = m.text(), ids.ids_of(m.g)
    try:
        new, inv = refine.apply_tx(m.g, tx)
    except refine.TxError as e:
        if f['error'] is None:
            return ['the transaction failed: %s' % e]
        if f['error'][0].lower() not in str(e).lower():
            bad.append("the failure says '%s', want '%s'" % (e, f['error'][0]))
        if m.text() != before_text or ids.ids_of(m.g) != before_ids:
            bad.append('a transaction that failed left a change behind')
        stats['atomic'] += 1
        return bad
    if f['error'] is not None:
        return ['the transaction was meant to fail']
    stats['tx'] += 1
    for p in tx:
        stats['ops'][p['op']] = stats['ops'].get(p['op'], 0) + 1
    if refine.text_of(new) != f['text']:
        bad.append('text:\n' + refine.text_of(new) + 'want:\n' + f['text'])
    if f['ids'] is not None:
        want = [int(x) for x in ' '.join(f['ids']).split()]
        got = [it['_id'] for it in new['items']]
        if got != want:
            bad.append('top-level ids %s, want %s' % (got, want))
    back, inv2 = refine.apply_tx(new, inv)
    if refine.text_of(back) != before_text:
        bad.append('the inverse did not restore the text')
    if ids.ids_of(back) != before_ids:
        bad.append('the inverse did not restore the ids: %s, want %s' % (ids.ids_of(back), before_ids))
    again, _ = refine.apply_tx(back, tx)
    if refine.text_of(again) != refine.text_of(new):
        bad.append('the transaction applied again after its inverse gives another text')
    if not rnxc_fmt_ok(refine.text_of(new), 'fmt_%s.ring' % f['id']):
        bad.append('rnxc fmt does not call the result canonical')
    return bad


def try_orders(program, ctx, sa, sb):
    out = []
    for first, second in ((sa, sb), (sb, sa)):
        m = refine.Model(program, ctx)
        o1 = m.refine(first)
        o2 = m.refine(second)
        out.append((m.text(), (first == sa and (o1.status, o2.status) or (o2.status, o1.status))))
    return out


def check_commute_fixture(f, stats):
    bad = []
    for n, row in enumerate(f['commute'], 1):
        pair, _, verdict = row.rpartition(' => ')
        sa, sb = [x.strip() for x in pair.split(' ~ ')]
        (ta, va), (tb, vb) = try_orders(f['program'], f['context'] or {}, sa, sb)
        differs = (ta != tb) or (va != vb)
        m = refine.Model(f['program'], f['context'] or {})
        a, _ = refine.parse_sentence(sa)
        b, _ = refine.parse_sentence(sb)
        pred = refine.commutes(m, a, b)
        want = verdict.strip()
        got = 'commute' if pred and not differs else ('conflict differs' if (not pred and differs) else ('conflict same' if not pred else 'UNSOUND'))
        stats['pairs'][got] = stats['pairs'].get(got, 0) + 1
        if got != want:
            bad.append('row %d: %s, want %s' % (n, got, want))
    return bad


def check_audit_fixture(f, stats):
    bad = []
    m = refine.Model(f['program'], f['context'] or {})
    posture, author = 'trusted', 'text-edit'
    wants, raw = [], None
    for line in f['audit']:
        if line.startswith('as '):
            posture, _, by = line[3:].strip().partition(' by ')
            author = by or author
        elif line.startswith('raw '):
            raw = int(line[4:])
        elif line.startswith('refine '):
            lhs, _, v = line[7:].rpartition(' => ')
            t, a, b = lhs.split()
            wants.append((t, a, b, parse_verdict(v)))
    results, nraw, faults = refine.audit(m, f['edited'], posture, author)
    if faults:
        return ['the edit does not lift: %s' % faults]
    got = {(t, a, b): o for t, a, b, o in results}
    for t, a, b, exp in wants:
        o = got.get((t, a, b))
        if o is None:
            bad.append('the edit was not read back as refinement %s %s -> %s (got %s)' % (t, a, b, sorted(got)))
            continue
        bad += ['audit %s: %s' % (t, w) for w in judge_outcome(o, exp)]
    if len(got) != len(wants):
        bad.append('the edit amounts to %d refinements, want %d' % (len(got), len(wants)))
    if raw is not None and nraw != raw:
        bad.append('%d raw edit(s), want %d' % (nraw, raw))
    stats['audits'] += 1
    return bad


def judge_fixtures(fx, stats):
    results = []
    for f in fx:
        try:
            if f['tx'] is not None:
                bad = check_tx_fixture(f, stats)
            elif f['commute'] is not None:
                bad = check_commute_fixture(f, stats)
            elif f['audit'] is not None:
                bad = check_audit_fixture(f, stats)
            else:
                bad = check_fixture(f, stats)
        except Exception as e:      # a defect of the engine is a failed fixture, never a crashed court
            import traceback
            bad = ['EXCEPTION %s: %s' % (type(e).__name__, traceback.format_exc().strip().split('\n')[-3:])]
        results.append((f['id'], bad))
    return results


def new_stats():
    return {'steps': 0, 'events': 0, 'lifts': 0, 'runs': 0, 'tx': 0, 'atomic': 0, 'ops': {}, 'pairs': {}, 'audits': 0}


# ---- the live gate: stzRefinableCode on the Ring++ package ---------------------------------------------------------------------------------

LEVEL_SYMBOL = {'advisory': 'Advisory', 'delegated': 'Delegated', 'autonomous': 'Autonomous', 'emergencyoverride': 'EmergencyOverride'}

SWEEP_PROGRAMS = [
    ('governed', '''$nVat = 0.20  # <R:PARAM name="vat" min="0" max="0.9" risk="1" governed_by="ops">
$nFloor = 0.10  # <R:PARAM name="floor" min="0" max="0.5" risk="2" governed_by="ops" floor="external">
$cSort = "quick"  # <R:ALGO name="sort" options="quick|merge|heap" risk="3" governed_by="ops" floor="trusted">
# <R:RULE name="vat-above-floor" expr="vat >= floor" message="vat must not drop below floor">
# <R:RULE name="floor-cap" expr="floor <= 0.3" message="floor is capped at 0.3">
''', '''governance ops
	actor bot delegated may vat floor sort
	actor lead autonomous may vat floor sort
	actor intern advisory may vat
	actor boss emergencyoverride may vat floor sort
''', {'vat': ['0.20', '0.30', '0.9', '0.95', '0', '-0.1', '0.05', '0.15'],
      'floor': ['0.10', '0.15', '0.25', '0.35', '0.5', '0.6', '0.30'],
      'sort': ['quick', 'merge', 'heap', 'radix']},
     ['bot', 'lead', 'intern', 'boss', 'stranger'], ['trusted', 'external', 'sandboxed', 'llm']),
    ('floors only', '''$nRate = 5  # <R:PARAM name="rate" min="1" max="10" floor="sandboxed">
$cMode = "fast"  # <R:ALGO name="mode" options="fast|slow|auto" floor="external">
$nSize = 100  # <R:PARAM name="size" max="1000">
# <R:RULE name="size-over-rate" expr="size > rate" message="size must stay above rate">
''', '', {'rate': ['5', '1', '10', '0', '11', '2.5', '100'], 'mode': ['fast', 'slow', 'auto', 'warp'], 'size': ['100', '1000', '1001', '5', '4', '6']},
     ['any'], ['trusted', 'external', 'sandboxed', 'llm']),
]


def expressible(m, sent):
    """The live gate carries a value as `value="..."` in a tag, so a value that holds a double quote cannot be put to it."""
    s, _ = refine.parse_sentence(sent)
    return s is not None and '"' not in s['to'] and all('"' not in p['value'] for p in m.lift()['points'])


def stz_source(m):
    """The program's points as stzRefinableCode's own tag form: `x = <R:KIND name="" value="" min="" ...>`."""
    lines = []
    for p in m.lift()['points']:
        a = p['attrs']
        extra = ''.join(' %s="%s"' % (k, a[k]) for k in ('min', 'max', 'options') if k in a)
        lines.append("x = <R:%s name=\"%s\" value=\"%s\"%s>" % (p['kind'].upper(), p['name'], p['value'], extra))
    return '\n'.join(lines)


def ring_lambda(r, L):
    """The rule as a derivation of the live gate. A rule that names a point holding text (a string param, an algo) is compared as text, as this gate's
    rules_violated compares it; the first translation put ring_number() on both sides, and a string side then RAISED R41 in the live gate on every proposal
    (fixture 42's `label != a`), since the live gate evaluates every rule of the program each time."""
    def is_text(side):
        p = None if refine.NUM_RE.match(side) else refine.point_named(L, side)
        return p is not None and p['form'] not in ('num', 'neg')
    text = is_text(r['left']) or is_text(r['right'])

    def operand(side):
        if refine.NUM_RE.match(side):
            return ('"%s"' if text else 'ring_number("%s")') % side
        return ('oCode.ValueOf("%s")' if text else 'ring_number(oCode.ValueOf("%s"))') % side
    op = {'=': '=', '!=': '!='}.get(r['op'], r['op'])
    return 'func oCode { return %s %s %s }' % (operand(r['left']), op, operand(r['right']))


def stz_case(i, m, ctx, sent):
    """Ring source that builds the live gate for a model and puts one sentence to it: prints `V|i|admitted|why|value-after`."""
    L = m.lift()
    s, _ = refine.parse_sentence(sent)
    lines = ["o = new stzRefinableCode('" + stz_source(m).replace('\n', "' + nl + '") + "')"]
    govs = {p['attrs']['governed_by'] for p in L['points'] if p['attrs'].get('governed_by')}
    if govs:
        g = sorted(govs)[0].lower()
        lines.append('o.SetGovernedBy(new stzGovernance("%s"))' % g)
        lines.append('o.SetActor("%s")' % s['author'])
        for p in L['points']:
            if p['attrs'].get('risk'):
                lines.append('o.SetRiskFor("%s", %s)' % (p['name'], p['attrs']['risk']))
        who = ctx.get(g, {}).get(s['author'].lower())
        if who:
            for p in L['points']:
                if p['name'].lower() in who['may']:
                    lines.append('o.SetAllowRefine("%s")' % p['name'])
            lines.append('o.SetAuthorityLevel(:%s)' % LEVEL_SYMBOL[who['name']])
    for p in L['points']:
        if p['attrs'].get('floor'):
            lines.append('o.TrustFloor("%s", "%s")' % (p['name'], p['attrs']['floor']))
    for r in L['rules']:
        lines.append('o.DeclareDerivation("%s", %s, "%s")' % (r['name'], ring_lambda(r, L), r['message']))
    # both gates match a point's name exactly (D24, HF-88)
    pt = refine.point_named(L, s['base'])
    name = pt['name'] if pt else s['base']
    lines.append('r = o.Refine("%s").As("%s").To("%s")' % (name, s['posture'], s['to']))
    lines.append('? "V|%d|" + r[:admitted] + "|" + r[:why] + "|" + o.ValueOf("%s")' % (i, name))
    return 'try\n' + '\n'.join(lines) + '\ncatch\n? "V|%d|ERR|" + cCatchError + "|"\ndone' % i


def sweep_cases():
    cases = []
    for label, text, ctxtext, values, actors, postures in SWEEP_PROGRAMS:
        ctx = refine.parse_context(ctxtext) if ctxtext else {}
        m = refine.Model(text, ctx)
        L = m.lift()
        assert not L['errors'], L['errors']
        for p in L['points']:
            for v in values[p['name']]:
                for a in actors:
                    for po in postures:
                        sent = refine.sentence_text('s', p['name'], p['kind'], p['value'], v, a, po, 'sweep')
                        cases.append((label, text, ctx, sent))
    return cases


INCONSISTENT = []


def fixture_cases(fx):
    """The steps of the fixtures the live gate can judge: a value of a literal point, no id, no cascade, no revert, no human edit before it,
    a program whose points are all governed by one governance or none, and every governance it names configured."""
    cases = []
    for f in fx:
        if not f['do'] or f['edited'] is not None:
            continue
        try:
            m = refine.Model(f['program'], f['context'] or {})
        except Exception:
            continue
        L = m.lift()
        if L['errors'] and not all(e['own'] for e in L['errors']):
            continue
        if any(e['own'] for e in L['errors']) or refine.rules_violated(L):
            INCONSISTENT.append(f['id'])         # the live gate judges the whole program, so it refuses every proposal from a state that already breaks a rule
            continue
        if any(p['kind'] not in ('param', 'algo') or p['form'] == 'call' for p in L['points']):
            continue
        govs = [p['attrs'].get('governed_by') for p in L['points']]
        if any(govs) and not all(govs):
            continue
        if any(g and g.lower() not in (f['context'] or {}) for g in govs) or len({g for g in govs if g}) > 1:
            continue
        for line in f['do']:
            sent = line.rpartition(' => ')[0]
            s, _ = refine.parse_sentence(sent)
            if s is None or s['attr'] or 'at' in s or 'reverts' in s or 'cascade' in s:
                continue
            cases.append((f['id'], f['program'], f['context'] or {}, sent))
    return cases


def compilers_note():
    """The package carries a COPY of the compiler (bench/package.py): when it is older than the repository's, the live gate answers on a compiler without the fixes since,
    and the first thing a report must say."""
    if not (os.path.exists(PACKAGE) and os.path.exists(RNXC)):
        return None
    a, b = os.path.getmtime(PACKAGE), os.path.getmtime(RNXC)
    when = lambda t: time.strftime('%Y-%m-%d %H:%M', time.localtime(t))
    if a + 60 < b:
        return ('  --   THE PACKAGE\'S COMPILER (%s) IS OLDER THAN THE REPOSITORY\'S (%s): the live gate, the engine\'s decoder and the history below run Softanza on a compiler without the '
                'fixes since; `python bench/package.py` lays out a new one' % (when(a), when(b)))
    return '  --   the package\'s compiler (%s) is not older than the repository\'s (%s)' % (when(a), when(b))


def run_live_gate(cases):
    """-> {index: (admitted, stage, value)} read from stzRefinableCode, or None when the Ring++ package is not laid out."""
    if not os.path.exists(PACKAGE):
        return None
    got = {}
    for start in range(0, len(cases), 150):
        body = ['load "stzlib.ring"']
        for i in range(start, min(len(cases), start + 150)):
            label, text, ctx, sent = cases[i]
            mm = refine.Model(text, ctx)
            if not expressible(mm, sent) or is_stricter(mm.refine(sent)):
                continue
            body.append(stz_case(i, refine.Model(text, ctx), ctx, sent))
        path = write('live_gate.ring', '\n'.join(body) + '\n')
        rc, out, err = run([PACKAGE, path], timeout=900, cwd=ROOT)
        for line in out.split('\n'):
            if line.startswith('V|'):
                _, i, adm, rest = (line.split('|', 3) + [''])[:4]
                why, _, val = rest.rpartition('|')
                stage = why.split(':', 1)[0]
                got[int(i)] = (adm == '1', ('RAISED ' + why) if adm == 'ERR' else (stage if adm != '1' else 'all'), val)
    # a case that raised is put again, alone, and what it says then is what counts; how many needed it is printed. Once in 488 cases the live stack raised
    # R14 `nodesids` and passed alone: DIAGNOSED 2026-10-05 -- the package's compiler was a copy of 2026-09-28, which looked a lambda up by its byte offset across
    # every file of the unit, so a lambda of the script that started at byte 2557 ran stzSecurityRule's, which starts there too (CLAUDE.md, bench/exec/lambda_offset.ring).
    # The retry is kept for any other case the live stack raises on, and `compilers_note` says first whether the package is the repository's compiler
    again = [i for i in sorted(got) if str(got[i][1]).startswith('RAISED')]
    RETRIED.extend(again)
    for i in again:
        label, text, ctx, sent = cases[i]
        path = write('live_gate_one.ring', 'load "stzlib.ring"\n' + stz_case(i, refine.Model(text, ctx), ctx, sent) + '\n')
        rc, out, err = run([PACKAGE, path], timeout=300, cwd=ROOT)
        for line in out.split('\n'):
            if line.startswith('V|%d|' % i):
                _, j, adm, rest = (line.split('|', 3) + [''])[:4]
                why, _, val = rest.rpartition('|')
                stage = why.split(':', 1)[0]
                got[i] = (adm == '1', ('RAISED ' + why) if adm == 'ERR' else (stage if adm != '1' else 'all'), val)
    return got


RETRIED = []


def is_stricter(out):
    """Refused by the language itself at the structural stage, for something stzRefinableCode's structural stage never looks at."""
    return not out.admitted and out.stage == 'structural' and not out.why.startswith("no refinement point")


def judge_live(cases, got):
    """Per case: mine against theirs. -> (agree, stricter, [disagreements])."""
    agree, stricter, bad, unsayable = 0, 0, [], 0
    for i, (label, text, ctx, sent) in enumerate(cases):
        m = refine.Model(text, ctx)
        out = m.refine(sent)
        if is_stricter(out):
            stricter += 1
            continue
        theirs = got.get(i)
        if theirs is None and not expressible(refine.Model(text, ctx), sent):
            unsayable += 1
            continue
        if theirs is None:
            bad.append((label, sent, 'the live gate printed nothing for it'))
            continue
        mine = (out.admitted, out.stage if not out.admitted else 'all')
        if mine != theirs[:2]:
            bad.append((label, sent, 'mine %s, theirs %s' % (mine, theirs[:2])))
            continue
        pt = refine.point_named(m.lift(), refine.parse_sentence(sent)[0]['base'])
        same = refine.same_value(pt, pt['value'], theirs[2]) if pt else True
        if not same:
            bad.append((label, sent, 'the value after is %s here and %s there' % (pt['value'], theirs[2])))
            continue
        agree += 1
    return agree, stricter, bad, unsayable


# ---- the language as judge of a retargeted call ----------------------------------------------------------------------------------------------

FUNCS = """func F1(a)
	return a

func F2(a, b)
	return a

func F3()
	return 1

func F4(a)
	return a
"""


def graph_has_call(text):
    p = write('g_call.ring', text)
    rc_, out, err = run([RNXC, 'graph', p], timeout=60)
    return any(ln.startswith('CALL|<top>|') and ln.endswith('|static') for ln in out.split('\n'))


def calls_against_graph():
    """For a call passing 0, 1 and 2 arguments and every candidate callee -- a function of each arity, one that does not exist, a case variant --
    the gate's structural stage says the retarget stands exactly when `rnxc graph`, which reads what the compiler bound, shows a static call edge
    from the refined program. -> (checked, [disagreements])"""
    cands = ['F1', 'F2', 'F3', 'F4', 'NoSuch', 'f4', 'f2']
    bad, n = [], 0
    for nargs in (0, 1, 2):
        args = ', '.join(['aData'] * nargs)
        prog = 'aData = [3, 1, 2]\naOut = F1(%s)  # <R:ALGO name="f" options="%s">\n\n%s' % (args, '|'.join(cands), FUNCS)
        m = refine.Model(prog)
        if m.text() != prog:
            return n, ['the program is not canonical']
        p = refine.point_named(m.lift(), 'f')
        for cand in cands:
            sent = refine.sentence_text('g', 'f', 'algo', 'F1', cand, 'court', 'trusted', 'graph')
            s, _ = refine.parse_sentence(sent)
            out = refine.evaluate(m, s, {})
            mine = not (out.status == 'rejected' and out.stage == 'structural')
            if cand == 'F1':                      # the callee already there: a no-op, refused before the graph is asked (D25)
                if mine or 'nothing to refine' not in out.why:
                    bad.append('%d argument(s) to F1, the callee already there: the gate says %s, not "nothing to refine"' % (nargs, out.why[:60]))
                continue
            new, _ = refine.apply_tx(m.g, refine.lower(p, s), inplace=False)
            theirs = graph_has_call(refine.text_of(new))
            n += 1
            if cand.lower() in ('f2', 'f4') and cand not in ('F2', 'F4') and theirs:
                # a case variant: Ring would bind it, so the graph shows the edge; the gate refuses it and names the declared spelling (D24)
                if mine or 'names are exact' not in out.why:
                    bad.append('%d argument(s) to %s: a case variant, the gate says %s' % (nargs, cand, out.why[:60]))
                continue
            if mine != theirs:
                bad.append('%d argument(s) to %s: the gate says %s, rnxc graph says %s' % (nargs, cand, 'stands' if mine else 'refused', 'an edge' if theirs else 'no edge'))
    return n, bad


# ---- the write surface: the grammar scoped to a program ------------------------------------------------------------------------------------

GBNF_BATCH = os.path.join(HERE, 'probes', 'gbnf_batch.ring')
SHAPE_WORDS = ('malformed sentence', 'no refinement point', "kind '", 'stale:', 'no governance')
STRUCTURAL_OK_UNDER_GRAMMAR = ('no function', 'argument(s)', 'distinct options', 'nothing to refine')   # what no context-free grammar says
# ('nothing to refine', D25: a grammar would need a rule per point to say "any value but the one there"; 'is not governed' went with the branch D25 made dead)
UNSCOPED = (
    'root ::= "DEFINE REFINE " id " AS ( TARGET " str ", KIND " kind ", FROM " str ", TO " str ", AUTHOR " str ", POSTURE " post ", REASON " str " )"\n'
    'id ::= [a-z] [a-z0-9_]*\n'
    'str ::= "\\"" [^"\\n]* "\\""\n'
    'kind ::= "param" | "algo" | "pipeline"\n'
    'post ::= "trusted" | "external" | "sandboxed" | "llm"\n')


def shape_refusal(out):
    """A refusal of the SHAPE or the IDENTITY of a proposal -- the ones a grammar scoped to the program says in advance."""
    if out.admitted:
        return False
    w = out.why
    if out.stage == 'structural':
        if w.startswith(SHAPE_WORDS):
            return True
        return w.startswith("TO '") and any(x in w for x in ('is not a number', 'is not a risk tier', 'is not a posture', 'is not a governance name'))
    if out.stage == 'constraint':
        return 'not in options' in w
    return False


def canonical(s):
    return refine.sentence_text(s['id'], s['target'], s['kind'], s['from'], s['to'], s['author'], s['posture'], s['reason'],
                                at=s.get('at'), cascade=s.get('cascade'), reverts=s.get('reverts'))


def collect_steps(fx, grammar_fn):
    """Every sentence step of the fixtures: the grammar of the program as it stood before the step, the sentence written canonically, the gate's outcome."""
    jobs = []
    for f in fx:
        if not f['do']:
            continue
        m = refine.Model(f['program'], f['context'] or {})
        for n, line in enumerate(f['do'], 1):
            if line.strip() == 'EDIT':
                m.edit(f['edited'])
                continue
            sent = line.rpartition(' => ')[0]
            s, _ = refine.parse_sentence(sent)
            if s is not None:
                s = dict(s, _spelt=spelt_otherwise(m, s))
            g = grammar_fn(m)
            out = m.refine(sent)
            jobs.append((f['id'], n, g, canonical(s) if s else sent.strip(), out, s))
    return jobs


def spelt_otherwise(m, s):
    """Is the sentence outside its program's scoped grammar BY DESIGN? The grammar writes the program's own spellings -- the point's declared name, the
    text FROM finds there -- and strings without a double quote; the gate takes a number spelt another way (`"1.0"` for `1`) and a value that needs another
    quote. Names have one spelling (D24), so a name in another case is refused, not outside the grammar. It was two fixture ids, 07 and 09."""
    p = refine.point_named(m.lift(), s['base'])
    if p is None:
        return False
    cur = p['attrs'].get(s['attr'], '') if s['attr'] else p['value']
    return s['from'] != cur or '"' in s['to']


def run_gbnf_jobs(pairs):
    """pairs: [(grammar text, sentence)] -> [(the engine's refusal of the grammar, 1 when it accepts the sentence)], or None without the package."""
    if not os.path.exists(PACKAGE):
        return None
    d = os.path.join(SCRATCH, 'gb')
    os.makedirs(d, exist_ok=True)
    names, manifest = {}, []
    for i, (g, s) in enumerate(pairs):
        if g not in names:
            names[g] = 'g%d.gbnf' % len(names)
            open(os.path.join(d, names[g]), 'wb').write(g.encode('latin-1'))
        open(os.path.join(d, 's%d.txt' % i), 'wb').write(s.encode('latin-1'))
        manifest.append('%s|s%d.txt' % (names[g], i))
    mp = os.path.join(d, 'manifest.txt')
    open(mp, 'wb').write('\n'.join(manifest).encode('latin-1'))
    res = {}
    for start in range(0, len(manifest), 400):
        part = os.path.join(d, 'manifest_%d.txt' % start)
        lines = manifest[start:start + 400]
        open(part, 'wb').write('\n'.join(lines).encode('latin-1'))
        rc_, out, err = run([PACKAGE, GBNF_BATCH, part, d], timeout=900, cwd=ROOT)
        for ln in out.split('\n'):
            if ln.startswith('J|'):
                _, j, refusal, acc = (ln.split('|', 3) + ['', ''])[:4]
                res[start + int(j) - 1] = (refusal, acc.strip() == '1')
    return [res.get(i) for i in range(len(pairs))]


SAMPLE_PROGRAMS = [
    ('governed', SWEEP_PROGRAMS[0][1], SWEEP_PROGRAMS[0][2]),
    ('floors only', SWEEP_PROGRAMS[1][1], SWEEP_PROGRAMS[1][2]),
    ('pipeline and algo', 'aSteps = ["parse", "check", "emit"]  # <R:PIPELINE name="steps" options="parse|check|optimize|emit" risk="2" governed_by="ops">\n'
                          '$cSort = "quick"  # <R:ALGO name="sort" options="quick|merge|heap" floor="external">\n$nSize = -5  # <R:PARAM name="size" min="-20" max="50">\n',
     'governance ops\n\tactor lead autonomous may steps\n\tactor boss emergencyoverride may steps\n'),
    ('callees', 'aData = [3, 1, 2]\naSorted = QuickSort(aData)  # <R:ALGO name="sort" options="QuickSort|MergeSort|HeapSort|RadixSort">\n\nfunc QuickSort(aList)\n\treturn aList\n\n'
                'func MergeSort(aList)\n\treturn aList\n\nfunc HeapSort(aList, nDepth)\n\treturn aList\n', ''),
]


def write_surface(fx, grammar_fn, per_program):
    """The grammar scoped to a program, judged three ways. -> a dict of the counts and the failures."""
    r = {'bad': [], 'steps': 0, 'refused': 0, 'shape': 0, 'shape_ok': 0, 'admitted': 0, 'admitted_ok': 0, 'exceptions': 0, 'grammars': 0, 'sampled': 0,
         'sample_admit': {}, 'sample_stage': {}, 'structural': {}, 'engine': True}
    steps = collect_steps(fx, grammar_fn)
    rnd = random.Random(20201005)
    samples = []
    for label, text, ctxtext in SAMPLE_PROGRAMS:
        ctx = refine.parse_context(ctxtext) if ctxtext else {}
        m = refine.Model(text, ctx)
        actor = 'lead' if ctx else 'court'
        for variant, kw in (('', {}), (' under :llm', {'posture': 'llm', 'author': actor})):
            try:
                g = grammar_fn(m, **kw)
            except TypeError:
                g = grammar_fn(m)
            G = Gbnf(g)
            for _ in range(per_program // 2):
                samples.append((label + variant, text, ctx, g, G.sample(rnd)))
    pairs = [(g, s) for (_, _, g, s, _, _) in steps] + [(g, s) for (_, _, _, g, s) in samples]
    got = run_gbnf_jobs(pairs)
    if got is None:
        r['engine'] = False
        return r
    r['grammars'] = len({g for g, _ in pairs})
    for (g, s), res in zip(pairs, got):
        if res is None or res[0] != '':
            r['bad'].append('the engine does not hold a scoped grammar: %s' % (res[0] if res else 'no answer'))
            # nothing below can be judged then: the first version went on, unpacked the missing answer, and the court's thread died with no word
            # (2026-10-19, a grammar over the decoder's 128 rules: the batch stopped at that job and every later one had no answer)
            return r
    nsteps = len(steps)
    for k, (fid, n, g, sent, out, s) in enumerate(steps):
        refusal, accepts = got[k]
        r['steps'] += 1
        if out.admitted:
            r['admitted'] += 1
            if accepts:
                r['admitted_ok'] += 1
            elif s is not None and ('reverts' in s or s.get('_spelt')):
                r['exceptions'] += 1
            else:
                r['bad'].append('%s step %d was admitted by the gate but is not a sentence of its scoped grammar: %s' % (fid, n, sent[:140]))
        else:
            r['refused'] += 1
            if shape_refusal(out):
                r['shape'] += 1
                if not accepts:
                    r['shape_ok'] += 1
                else:
                    r['bad'].append('%s step %d was refused for its shape (%s) but its scoped grammar accepts it: %s' % (fid, n, out.why[:60], sent[:120]))
    for k, (label, text, ctx, g, sent) in enumerate(samples):
        refusal, accepts = got[nsteps + k]
        r['sampled'] += 1
        if not accepts:
            r['bad'].append('a sentence sampled from the scoped grammar of %s is not accepted by the engine: %s' % (label, sent[:140]))
        m = refine.Model(text, ctx)
        out = m.refine(sent)
        key = label
        r['sample_admit'][key] = r['sample_admit'].get(key, [0, 0])
        r['sample_admit'][key][0] += 1 if out.admitted else 0
        r['sample_admit'][key][1] += 1
        r['sample_stage'][out.stage] = r['sample_stage'].get(out.stage, 0) + 1
        if shape_refusal(out):
            r['bad'].append('a sentence written under the scoped grammar of %s was refused for its shape (%s): %s' % (label, out.why[:80], sent[:120]))
        elif out.stage == 'structural':
            if not any(x in out.why for x in STRUCTURAL_OK_UNDER_GRAMMAR):
                r['bad'].append('a sentence written under the scoped grammar of %s was refused structurally for a reason no grammar says: %s' % (label, out.why[:100]))
            else:
                key = next(x for x in STRUCTURAL_OK_UNDER_GRAMMAR if x in out.why)
                r['structural'][key] = r['structural'].get(key, 0) + 1
    return r


# ---- the controls -----------------------------------------------------------------------------------------------------------------------------

@contextlib.contextmanager
def patched(**kw):
    saved = {}
    for k, v in kw.items():
        saved[k] = getattr(refine, k)
        setattr(refine, k, v)
    try:
        yield
    finally:
        for k, v in saved.items():
            setattr(refine, k, v)


def n_failing(fx):
    return sum(1 for _, bad in judge_fixtures(fx, new_stats()) if bad)


_orig_apply_prim = refine.apply_prim


def apply_prim_losing_ids(work, p):
    inv = _orig_apply_prim(work, p)
    if inv.get('op') == 'node.create':
        inv = dict(inv)
        inv['node'] = ids.strip(inv['node'])
    return inv


def evaluate_loose_revert(model, s, ctx, readback=True):
    if s is not None and 'reverts' in s:
        s = dict(s)
        s['reverts'] = None
        s.pop('reverts')
    return _orig_evaluate(model, s, ctx, readback)


_orig_evaluate = refine.evaluate


# ---- history and corpus ------------------------------------------------------------------------------------------------------------------

def literal_assignments(g):
    """(item, lhs text, value, form) for each statement `x = <literal>` in a graph."""
    out = []
    for it, parent, bpath, lst, i, owner in refine.walk_items(g):
        if it['k'] == 'expr' and it['e']['k'] == 'assign' and it['e'].get('op') == '=' and it['e']['l']['k'] == 'id':
            lt = refine.literal_text(it['e']['r'])
            if lt is not None:
                out.append((it, it['e']['l']['text'].lower(), lt))
    return out


def landing(sources, n):
    """Old literal assignments as the targets of refinements drafted at one revision, over every consecutive pair: where does each land at the next?"""
    tot = {'pairs': 0, 'targets': 0, 'lands': 0, 'stale': 0, 'shape': 0, 'other': 0, 'lost': 0}
    for repo, path in sources:
        revs = ids_check.revisions(repo, path, n)
        gs = []
        for rv, pth in revs:
            try:
                gs.append(ids_check.graph_at(repo, rv, pth))
            except Exception:
                gs.append(None)
        for a, b in zip(gs, gs[1:]):
            if a is None or b is None:
                continue
            og, ng = copy.deepcopy(a), copy.deepcopy(b)
            ids.number(og)
            ids.carry(og, ng)
            tot['pairs'] += 1
            now = {it['_id']: it for it, *_ in refine.walk_items(ng)}
            for it, lhs, lt in literal_assignments(og):
                tot['targets'] += 1
                n2 = now.get(it['_id'])
                if n2 is None:
                    tot['lost'] += 1
                    continue
                if not (n2['k'] == 'expr' and n2['e']['k'] == 'assign' and n2['e'].get('op') == '=' and n2['e']['l']['k'] == 'id'
                        and refine.literal_text(n2['e']['r']) is not None):
                    tot['shape'] += 1
                elif n2['e']['l']['text'].lower() != lhs:
                    tot['other'] += 1
                elif refine.literal_text(n2['e']['r']) != lt:
                    tot['stale'] += 1
                else:
                    tot['lands'] += 1
    return tot


LINE_RE = re.compile(r'^(\t*)(\$?@?[A-Za-z_][A-Za-z0-9_]*) = (-?[0-9]+(?:\.[0-9]+)?|"[^"]*"|\'[^\']*\')$')


def candidates(text, k):
    """Up to k lines of canonical text that are a plain literal assignment with no comment, evenly spread."""
    lines = text.split('\n')
    cand = [i for i, ln in enumerate(lines) if LINE_RE.match(ln)]
    if len(cand) <= k:
        return cand
    step = len(cand) / k
    return [cand[int(j * step)] for j in range(k)]


def bump(lit):
    """A different literal of the same class: a number one larger in its whole part, a string with an x more."""
    if lit[:1] in ('"', "'"):
        body = lit[1:-1] + 'x'
        return refine.to_literal(body), body
    neg = lit.startswith('-')
    whole, dot, frac = lit.lstrip('-').partition('.')
    whole = str(int(whole) + 1)
    new = ('-' if neg else '') + whole + dot + frac
    return new, new


def corpus_files():
    files = []
    files += sorted(glob.glob(os.path.join(ROOT, 'haro', 'spike', '*.ring')))
    files += sorted(glob.glob(os.path.join(ROOT, 'bench', 'exec', '*.ring')))
    files += sorted(glob.glob(os.path.join(ROOT, 'bench', '*.ring')))
    if WIDE:
        files += sorted(glob.glob(os.path.join(r'D:\GitHub\stzlib\libraries\stzlib\base', 'refine', '*.ring')))
        files += sorted(glob.glob(os.path.join(r'D:\GitHub\stzlib\libraries\stzlib\base', 'governance', '*.ring')))
    keep = []
    for p in files:
        try:
            if b'GENERATED by forge.ring' in open(p, 'rb').read(400):
                continue
        except OSError:
            continue
        keep.append(p)
    return keep


def dis_shape(path):
    rc, out, err = run([RNXC, 'dis', path], timeout=120)
    if rc != 0:
        return None
    ops, on = [], False
    for ln in out.split('\n'):
        if ln.startswith('---- code'):
            on = True
        elif on and ln.strip():
            parts = ln.split()
            if len(parts) > 1:
                ops.append(parts[1])
    return ops


def corpus(max_files, per_file):
    stats = {'files': 0, 'candidates': 0, 'bad': [], 'dis': 0, 'dis_skipped': 0, 'bytes': 0, 'fmt': 0}
    t0 = time.time()
    for path in corpus_files():
        if stats['files'] >= max_files:
            break
        try:
            raw = open(path, 'rb').read().decode('latin-1')
            g = refine.new_graph(raw)
        except Exception:
            continue
        text = refine.text_of(g)
        if '<R:' in text:
            continue
        lines = text.split('\n')
        picks = candidates(text, per_file)
        if not picks:
            continue
        stats['files'] += 1
        stats['bytes'] += len(text)
        has_load = any(x['k'] == 'load' for x in g['items'])
        for li in picks:
            m_ = LINE_RE.match(lines[li])
            lit = m_.group(3)
            tagged = lines[:li] + [lines[li] + '  # <R:PARAM name="p">'] + lines[li + 1:]
            t1 = '\n'.join(tagged)
            try:
                m = refine.Model(t1)
            except Exception as e:
                continue
            if m.text() != t1:
                continue                # the tag moved the canonical form (a layout rule): not a candidate
            L = m.lift()
            if L['errors'] or len(L['points']) != 1 or L['points'][0]['carrier']['path'] != ['trail']:
                continue
            p = L['points'][0]
            newlit, newval = bump(lit)
            if newlit is None:
                continue
            stats['candidates'] += 1
            sent = refine.sentence_text('c', 'p', 'param', p['value'], newval, 'court', 'trusted', 'corpus')
            out = m.refine(sent)
            where = '%s:%d' % (os.path.basename(path), li + 1)
            if not out.admitted:
                stats['bad'].append((where, 'refused at %s: %s' % (out.stage, out.why[:80])))
                continue
            spliced = '\n'.join(tagged[:li] + [tagged[li].replace(' = ' + lit + '  #', ' = ' + newlit + '  #', 1)] + tagged[li + 1:])
            if m.text() != spliced:
                stats['bad'].append((where, 'the graph route and the splice route give different text'))
            ch = changed_lines(out.diff)
            if len(ch) != 2:
                stats['bad'].append((where, 'the diff holds %d changed lines' % len(ch)))
            if ids.ids_of(m.g) != ids.ids_of(refine.Model(t1).g):
                stats['bad'].append((where, 'an id moved'))
            if not rnxc_fmt_ok(m.text(), 'k_fmt.ring'):
                stats['bad'].append((where, 'rnxc fmt does not call the refined text canonical'))
            stats['fmt'] += 1
            back, _ = refine.apply_tx(m.g, out.inverse, inplace=False)
            if refine.text_of(back) != t1:
                stats['bad'].append((where, 'the inverse did not restore the text'))
            edge = lit[:1] not in ('"', "'") and '.' not in lit and abs(int(lit)) >= 2 ** 31 - 2
            if edge:
                stats['dis_edge'] = stats.get('dis_edge', 0) + 1
            elif not has_load:
                a = dis_shape(write('k_old.ring', t1))
                b = dis_shape(write('k_new.ring', m.text()))
                if a is None or b is None:
                    stats['bad'].append((where, 'rnxc dis could not read a version'))
                elif a != b:
                    stats['bad'].append((where, 'the compiled code changed shape (%d vs %d instructions)' % (len(a), len(b))))
                stats['dis'] += 1
            else:
                stats['dis_skipped'] += 1
    stats['secs'] = time.time() - t0
    return stats


# ---- the court ---------------------------------------------------------------------------------------------------------------------------------

def small_checks():
    # the inverse of an old change is refused when the state has moved on since: the primitive checks what it expects to find
    m = refine.Model('$nVat = 0.20  # <R:PARAM name="vat" min="0" max="0.9">\n$cSort = "quick"  # <R:ALGO name="sort" options="quick|merge">\n')
    sa = refine.sentence_text('a', 'vat', 'param', '0.20', '0.30', 'm', 'trusted', 'r')
    sb = refine.sentence_text('b', 'vat', 'param', '0.30', '0.40', 'm', 'trusted', 'r')
    sc = refine.sentence_text('c', 'sort', 'algo', 'quick', 'merge', 'm', 'trusted', 'r')
    ea, eb, ec = [m.refine(x) for x in (sa, sb, sc)]
    try:
        refine.apply_tx(m.g, ea.inverse)
        stale = False
    except refine.TxError as e:
        stale = 'conflict' in str(e)
    ok_b, _ = refine.apply_tx(m.g, eb.inverse)
    ok_c, _ = refine.apply_tx(m.g, ec.inverse)
    check(stale and refine.text_of(ok_b).startswith('$nVat = 0.30') and refine.text_of(ok_c).count('"quick"') == 1,
          'T the inverse of a change refuses to run over a state that has moved on since (the first change of a point whose second is still in place), and the inverse of the latest, or of an '
          'independent one, runs')
    # the command line
    d = os.path.join(SCRATCH, 'cli')
    os.makedirs(d, exist_ok=True)
    prog = '$nVat = 0.20  # <R:PARAM name="vat" min="0" max="0.9">\n? Gross(100)\n\nfunc Gross(nNet)\n\treturn nNet * (1 + $nVat)\n'
    open(os.path.join(d, 'p.ring'), 'wb').write(prog.encode('latin-1'))
    open(os.path.join(d, 'ok.rfn'), 'wb').write(('-- a refinement of the vat\nDEFINE REFINE up AS (\n  TARGET "vat", KIND param,\n  FROM "0.20", TO "0.30",\n  AUTHOR "mansour", POSTURE trusted,\n'
                                                   '  REASON "the rate went up"\n) RATIONALE "a rate is a parameter"\n').encode('latin-1'))
    open(os.path.join(d, 'bad.rfn'), 'wb').write(('DEFINE REFINE high AS ( TARGET "vat", KIND param, FROM "0.20", TO "0.95", AUTHOR "a", POSTURE trusted, REASON "r" )\n').encode('latin-1'))
    cli = [sys.executable, os.path.join(HERE, 'refine.py')]
    rc1, out1, _ = run(cli + [os.path.join(d, 'p.ring'), os.path.join(d, 'ok.rfn')])
    rc2, out2, _ = run(cli + [os.path.join(d, 'p.ring'), os.path.join(d, 'bad.rfn')])
    rc3, out3, _ = run(cli + [os.path.join(d, 'p.ring'), os.path.join(d, 'ok.rfn'), '--write'])
    after = open(os.path.join(d, 'p.ring'), 'rb').read().decode('latin-1')
    open(os.path.join(d, 'q.ring'), 'wb').write(prog.replace('  #', ' #').replace('0.20', '0.2000').encode('latin-1'))   # not its own canonical text
    rc4, out4, _ = run(cli + [os.path.join(d, 'q.ring'), os.path.join(d, 'ok.rfn'), '--write'])
    unchanged = open(os.path.join(d, 'q.ring'), 'rb').read().decode('latin-1') == prog.replace('  #', ' #').replace('0.20', '0.2000')
    check(rc1 == 0 and 'admitted' in out1 and '+$nVat = 0.30' in out1 and open(os.path.join(d, 'p.ring'), 'rb').read().decode('latin-1') != prog and 'wrote' in out3
          and rc2 == 1 and 'rejected constraint' in out2 and rc4 == 2 and unchanged and after == prog.replace('0.20', '0.30', 1),
          'F the command line: `refine.py program sentences` prints the verdict, the primitives and the diff (exit 0 admitted, 1 refused); `--write` replaces the program with the '
          'canonical text of the result, and refuses to on a program that is not already canonical (exit 2, the file untouched)')

    # a value no sentence can carry
    # and a line break: a refinement is one line out, one line in, so a value holding one is refused (a sentence file can carry it, a fixture line cannot)
    check(refine.to_literal('a"b\'c`d') is None and refine.to_literal('say "hi"') == "'say \"hi\"'" and refine.to_literal('it\'s "x"') == "`it's \"x\"`"
          and refine.to_literal('two\nlines') is None and refine.to_literal('a\rb') is None,
          'F a value that holds all three quotes cannot be written as a Ring string (F-55), one that holds two can; one holding a line break cannot either')


def main():
    t0 = time.time()
    print('refine_check -- refinement over the program graph, Ring++ face (rung 20)')
    fx = read_fixtures(os.path.join(HERE, 'fixtures.txt'))
    check(len(fx) >= FIXTURE_FLOOR, 'F the fixtures hold %d, at or above the pinned floor of %d' % (len(fx), FIXTURE_FLOOR))
    stats = new_stats()
    res = judge_fixtures(fx, stats)
    bad = [(i, b) for i, b in res if b]
    for fid, b in bad[:10]:
        for x in b[:3]:
            print('  FAIL %s: %s' % (fid, x[:400]))
    fails.extend('fixture %s' % fid for fid, _ in bad)
    check(not bad, 'F %d fixtures, %d steps through the gate (%s): each gets the verdict, the stage, the words and the lowering its fixture says, '
                   'and the properties every fixture must keep hold (%d fail)' % (len(fx), stats['steps'], ', '.join('%s %d' % (k, stats[k]) for k in ('admitted', 'flagged', 'rejected') if k in stats), len(bad)))
    check(stats['steps'] >= 90, 'F the steps are not shrinking: %d (floor 90)' % stats['steps'])
    stg = ', '.join('%s %d' % (k, stats.get(k, 0)) for k in refine.STAGES)
    print('  --   refusals by stage: %s; %d events in the logs, %d programs run on the oracle and on rnxc, %d primitives, %d atomic failure(s), pairs %s, %d audit(s)'
          % (stg, stats['events'], stats['runs'], stats['tx'], stats['atomic'], stats['pairs'], stats['audits']))
    seen = set(stats['ops'])
    twelve = {'node.create', 'node.delete', 'node.update_property', 'edge.create', 'edge.delete', 'edge.retarget', 'refinement.set_value',
              'refinement.add_option', 'refinement.remove_option', 'pipeline.insert_stage', 'pipeline.remove_stage', 'pipeline.reorder_stages'}
    check(seen >= twelve, 'T all twelve of RCP\'s primitives are applied, each with its inverse captured first and checked (missing: %s)' % sorted(twelve - seen))
    sentence_ops = set()
    for f in fx:
        if f['do']:
            m = refine.Model(f['program'], f['context'] or {})
            for line in f['do']:
                if line.strip() == 'EDIT':
                    m.edit(f['edited'])
                    continue
                o = m.refine(line.rpartition(' => ')[0])
                sentence_ops |= {p['op'] for p in o.tx}
    print('  --   %d of the twelve primitives are reached by a sentence; the others only as raw transactions: %s' % (len(sentence_ops & twelve), sorted(twelve - sentence_ops)))
    check(stats['pairs'].get('UNSOUND', 0) == 0, 'C the commutation predicate is sound on the fixtures: nothing it calls commuting gives two results')

    # the sweep for the predicate's soundness, on every pair of a pool of sentences over each sweep program
    pool_pairs, unsound, conservative, commuting = 0, 0, 0, 0
    for label, text, ctxtext, values, actors, postures in SWEEP_PROGRAMS[:1]:
        ctx = refine.parse_context(ctxtext) if ctxtext else {}
        m0 = refine.Model(text, ctx)
        sents = []
        for p in m0.lift()['points']:
            for v in values[p['name']][:5]:
                sents.append(refine.sentence_text('s', p['name'], p['kind'], p['value'], v, 'lead', 'trusted', 'pool'))
        sents.append(refine.sentence_text('s', 'vat.max', 'param', '0.9', '0.5', 'lead', 'trusted', 'pool'))
        sents.append(refine.sentence_text('s', 'sort.options', 'algo', 'quick|merge|heap', 'quick|merge', 'lead', 'trusted', 'pool'))
        if QUICK:
            sents = sents[::2]
        for i in range(len(sents)):
            for j in range(i + 1, len(sents)):
                a, _ = refine.parse_sentence(sents[i])
                b, _ = refine.parse_sentence(sents[j])
                pred = refine.commutes(m0, a, b)
                (ta, va), (tb, vb) = try_orders(text, ctx, sents[i], sents[j])
                differs = (ta != tb) or (va != vb)
                pool_pairs += 1
                if pred and differs:
                    unsound += 1
                elif pred:
                    commuting += 1
                elif not differs:
                    conservative += 1
    check(unsound == 0 and pool_pairs >= 100, 'C %d pairs of sentences over one program, each applied in both orders: %d the predicate calls commuting (and are), %d it calls conflicting and '
                                              'are order-dependent, %d it calls conflicting and are not (conservative), %d it calls commuting and are not (unsound)'
          % (pool_pairs, commuting, pool_pairs - commuting - conservative - unsound, conservative, unsound))

    if ONLY_FX:
        small_checks()
        print('refine_check: %s (%d failure(s), %.0f s) -- fixtures only' % ('FAIL' if fails else 'PASS', len(fails), time.time() - t0))
        return 1 if fails else 0
    # the live gate
    note = compilers_note()
    if note:
        print(note)
    cases = fixture_cases(fx)
    sweep = sweep_cases()
    if QUICK:
        sweep = sweep[::5]
    allc = cases + sweep
    got = run_live_gate(allc)
    if got is None:
        print('  SKIP S the Ring++ package is not at %s (python bench/package.py lays it out): the live gate was not asked' % PACKAGE)
        live_agree = None
    else:
        agree, stricter, lbad, unsayable = judge_live(allc, got)
        for label, sent, why in lbad[:8]:
            print('  FAIL S %s: %s -- %s' % (label, sent[:150], why))
        fails.extend('live gate: ' + w for _, _, w in lbad)
        check(not lbad and len(allc) >= SWEEP_FLOOR,
              'S %d proposals (%d from the fixtures, %d swept over %d programs x points x values x actors x postures) put to stzRefinableCode on the Ring++ package: '
              '%d agree on admitted-or-not, on the refusing stage and on the value left; %d are refused by the language itself at a stage the live gate does not have, %d carry a value its tag form cannot hold; '
              '%d disagree (floor %d proposals)' % (len(allc), len(cases), len(sweep), len(SWEEP_PROGRAMS), agree, stricter, unsayable, len(lbad), SWEEP_FLOOR))
        live_agree = (got, allc)
        if INCONSISTENT:
            print('  --   fixtures %s start from a program that already breaks a rule: this gate answers for the rules of the point a refinement touches, the live gate for the '
                  'whole program, so they are not put to it' % ', '.join(INCONSISTENT))
        if RETRIED:
            print('  --   %d proposal(s) raised in the live stack and were put again alone (cases %s)' % (len(RETRIED), RETRIED))

    n, gbad = calls_against_graph()
    for w in gbad[:6]:
        print('  FAIL G ' + w)
    fails.extend('graph: ' + w for w in gbad)
    check(not gbad and n >= 18, 'G %d retargeted calls (0, 1 and 2 arguments x a function of each arity, one that does not exist, a case variant): the structural stage says the retarget '
                                'stands exactly when `rnxc graph`, which reads what the compiler bound, shows a static call edge from the refined program -- but for a case '
                                'variant, which Ring binds and the gate refuses by name (D24); the callee already there is a no-op, refused (D25) (%d disagree)' % (n, len(gbad)))

    w = write_surface(fx, scoped.scoped_gbnf, 40 if QUICK else 150)
    if not w['engine']:
        print('  SKIP W the Ring++ package is not at %s: the engine\'s decoder was not asked' % PACKAGE)
    else:
        for b in w['bad'][:6]:
            print('  FAIL W ' + b)
        fails.extend('write surface: ' + b for b in w['bad'])
        adm = ', '.join('%s %d of %d' % (k, a, n) for k, (a, n) in sorted(w['sample_admit'].items()))
        stg = ', '.join('%s %d' % (k, v) for k, v in sorted(w['sample_stage'].items(), key=lambda kv: str(kv[0])) if k != 'all')
        check(not w['bad'] and w['sampled'] >= 100 and w['shape'] >= 8,
              'W the grammar scoped to each program (%d grammars, each held by the engine\'s decoder): all %d admitted proposals of the fixtures that its author could write '
              'are sentences of it (%d of %d; %d are outside it by design: a revert is written by the harness; a number spelt otherwise than the program writes it, or a value needing another quote); the decoder refuses every one of the '
              '%d proposals the gate refuses for their shape (%d of %d); and %d sentences SAMPLED from the grammars are all accepted by the decoder and none is refused '
              'for its shape: the gate admits %s, and refuses the rest at %s' % (w['grammars'], w['admitted'], w['admitted_ok'], w['admitted'] - w['exceptions'], w['exceptions'],
                                                                                 w['shape'], w['shape_ok'], w['shape'], w['sampled'], adm, stg))
        print('  --   the shapes no context-free grammar says, refused structurally under it: %s' % w['structural'])
        # D26: the write surface is what a TASK may change. A program of 15 points has no single grammar the decoder holds (HF-87); scoped to the three
        # points a task names it is held and writes their sentences, and a task naming a point the program does not declare is refused by name
        big = refine.Model(''.join('$nP%d = %d  # <R:PARAM name="p%d" min="0" max="100">\n' % (i, i, i) for i in range(15)), {})
        sent = refine.sentence_text('s', 'p7', 'param', '7', '8', 'court', 'trusted', 'a task')
        got = run_gbnf_jobs([(scoped.scoped_gbnf(big, points=['p0', 'p7', 'p14']), sent), (scoped.scoped_gbnf(big), sent)])
        try:
            scoped.scoped_gbnf(big, points=['p7', 'nowhere'])
            named = False
        except ValueError as e:
            named = 'nowhere' in str(e)
        ok = (got is not None and got[0] == ('', True) and got[1] is not None and 'GBNF-M2' in got[1][0] and named)
        check(ok, 'W a grammar scoped to the points a task names (D26): of a 15-point program the decoder refuses whole (%s), the grammar of 3 points is held and '
                  'writes their sentences, and a task naming a point the program does not declare is refused by name' % ((got[1][0][:40] if got and got[1] else 'no answer')))

    # controls
    for label, kw, floor in (
            ('a gate that never asks the trust floor', {'SKIP_STAGES': {'trust'}}, 3),
            ('a gate that never checks bounds or options', {'SKIP_STAGES': {'constraint'}}, 3),
            ('a gate that never consults governance', {'SKIP_STAGES': {'governance'}}, 3),
            ('a gate that never evaluates the derivation rules', {'SKIP_STAGES': {'derivation'}}, 2),
            ('a gate that edits the live program before it has judged it', {'INPLACE': True}, 2),
            ('a cascade that sees nothing', {'cascade': lambda g, p: {'reads': [], 'writes': []}}, 1),
            ('an apply whose inverse of a delete forgets the ids', {'apply_prim': apply_prim_losing_ids}, 1),
            ('a revert that does not check what it restores', {'evaluate': evaluate_loose_revert}, 1)):
        with patched(**kw):
            nbad = n_failing(fx)
        check(nbad >= floor, 'D the control, %s, fails %d fixture(s) (at least %d)' % (label, nbad, floor))
    if w['engine']:
        wc = write_surface(fx, lambda m, ctx=None, posture=None: UNSCOPED, 10)
        nbad = len([b for b in wc['bad'] if 'but its scoped grammar accepts it' in b])
        check(nbad >= 3, 'D the control, a grammar that does not name the program\'s points (any target, any kind, any value), accepts %d proposals the gate refuses for their shape (at least 3)' % nbad)
    if live_agree and not QUICK:
        with patched(SKIP_STAGES={'trust'}):
            agree2, stricter2, lbad2, _ = judge_live(live_agree[1], live_agree[0])
        check(len(lbad2) >= 10, 'D with the trust stage switched off the live gate disagrees on %d proposals: S is not agreeing by accident' % len(lbad2))

    # history
    srcs = ids_check.hand_written()
    tot = landing(srcs, 4 if QUICK else 7)
    lands = tot['lands'] / max(1, tot['targets'])
    resolve = (tot['lands'] + tot['stale'] + tot['other']) / max(1, tot['targets'])
    print('  --   %d pairs of consecutive revisions, %d literal assignments drafted against: %d land (%.1f%%), %d refused as stale (the value changed), %d no longer a literal '
          'assignment, %d now a different variable, %d gone' % (tot['pairs'], tot['targets'], tot['lands'], lands * 100, tot['stale'], tot['shape'], tot['other'], tot['lost']))
    check(tot['pairs'] >= ids_check.PAIRS_FLOOR and tot['targets'] >= 500,
          'H the sample is not shrinking: %d pairs, %d targets' % (tot['pairs'], tot['targets']))
    check(lands >= LAND_FLOOR, 'H %.1f%% of the literals a refinement could have been drafted against still land after the next human edit (floor %.0f%%): the rest are '
                               'refused as stale or gone, never applied elsewhere' % (lands * 100, LAND_FLOOR * 100))
    print('  --   of the %d that did not land, %d resolve to a different variable: a gate that checks TARGET against the id refuses them (AT does)' % (tot['targets'] - tot['lands'], tot['other']))

    if WIDE:
        wt = landing(ids_check.MEMO_SEVEN, 12)
        print("  --   the memo's seven files, up to 12 revisions: %d pairs, %d literal assignments, %.1f%% land, %d stale, %d no longer a literal, %d a different variable, %d gone"
              % (wt['pairs'], wt['targets'], wt['lands'] * 100 / max(1, wt['targets']), wt['stale'], wt['shape'], wt['other'], wt['lost']))

    # corpus
    nf, per = (30, 3) if QUICK else (80, 3) if not WIDE else (200, 4)
    cs = corpus(nf, per)
    for where, why in cs['bad'][:8]:
        print('  FAIL K %s: %s' % (where, why))
    fails.extend('corpus %s: %s' % w for w in cs['bad'])
    check(not cs['bad'] and cs['files'] >= CORPUS_FILES_FLOOR and cs['candidates'] >= CORPUS_CANDIDATES_FLOOR,
          'K %d literals of %d real Ring files (%d KB) made a point and refined: each admitted, equal to the line spliced by hand, canonical on rnxc fmt (%d), one line out and one '
          'in, no id moved, restored by its inverse, and %d compiled to the same code shape under rnxc dis (%d files with loads skipped it, %d literals at the 32-bit immediate, where the instruction itself changes): %d fail, %.0f s '
          '(floors: %d files, %d literals)' % (cs['candidates'], cs['files'], cs['bytes'] // 1024, cs['fmt'], cs['dis'], cs['dis_skipped'], cs.get('dis_edge', 0), len(cs['bad']), cs['secs'],
                                              CORPUS_FILES_FLOOR, CORPUS_CANDIDATES_FLOOR))

    small_checks()
    if PLANT:
        fails.append('PLANTED')
        print('  FAIL PLANTED')
    print('refine_check: %s (%d failure(s), %.0f s)' % ('FAIL' if fails else 'PASS', len(fails), time.time() - t0))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.setrecursionlimit(200_000)
    threading.stack_size(128 * 1024 * 1024)
    rc = []
    t = threading.Thread(target=lambda: rc.append(main()))
    t.start()
    t.join()
    sys.exit(rc[0] if rc else 1)
