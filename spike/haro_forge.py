"""haro_forge.py -- the guard of the Haro spike (charter section 10).

Born standalone; folded into bench/gate.py only when green. Every claim it
prints is a comparison against a pinned judge or an oracle:

  stage 1  the Haro meta-court (stzu v0.1's grammar, grown), ported to pure Ring (haro/spike/haro.ring),
           judged by stz/declarative/stzu/fixtures.json exactly as the Luau
           runner judges it, on rnxc AND on the oracle ring.exe -- and the two
           runtimes must print the same bytes for every fixture.

Later stages (the forge, the machine court against harb, the GBNF, the
refinement, the timing, the fleet court, W forged whole, Z forged whole)
are added below as they are built.

Usage: python haro/spike/haro_forge.py [--stage N] [--plant]
  --plant   plants a known-wrong verdict to prove the guard can fail.
"""
import json, os, re, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RNXC = os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
ORACLE = os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
STZU_FIXTURES = r'D:\GitHub\stz\declarative\stzu\fixtures.json'
STZU_RING = os.path.join(HERE, 'haro.ring')

PLANT = '--plant' in sys.argv


def run(exe, script, path):
    # cwd beside the script: Ring resolves a ROOT file's `load` from the
    # current directory (C-4), Ring++ beside the root; running both from
    # HERE asks the same question of each.
    env = dict(os.environ)
    env['RNXC_NOCACHE'] = '1'
    r = subprocess.run([exe, os.path.basename(script), path], capture_output=True,
                       env=env, timeout=120, cwd=os.path.dirname(script))
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def parse_verdict(out):
    """'ok' + fields, or a refusal line. Returns (accepted, fields|refusal)."""
    lines = [l for l in out.split('\n') if l != '']
    if not lines:
        return False, 'NO OUTPUT'
    if lines[0] != 'ok':
        return False, lines[0]
    fields = {}
    for l in lines[1:]:
        k, _, v = l.partition(' ')
        if k == 'count':                      # 'count SERVICE 3' -> fields['count SERVICE'] = '3'
            verb, _, n = v.partition(' ')
            fields['count ' + verb] = n
        else:
            fields[k] = v
    return True, fields


STZU2_FIXTURES = os.path.join(HERE, 'v02', 'fixtures.json')
STZU3_FIXTURES = os.path.join(HERE, 'v03', 'fixtures.json')
STZU4_FIXTURES = os.path.join(HERE, 'v04', 'fixtures.json')
STZU5_FIXTURES = os.path.join(HERE, 'v05', 'fixtures.json')
STZU6_FIXTURES = os.path.join(HERE, 'v06', 'fixtures.json')
STZU7_FIXTURES = os.path.join(HERE, 'v07', 'fixtures.json')
STZU8_FIXTURES = os.path.join(HERE, 'v08', 'fixtures.json')
STZU9_FIXTURES = os.path.join(HERE, 'v09', 'fixtures.json')
STZU10_FIXTURES = os.path.join(HERE, 'v10', 'fixtures.json')
STZU11_FIXTURES = os.path.join(HERE, 'v11', 'fixtures.json')
STZU12_FIXTURES = os.path.join(HERE, 'v12', 'fixtures.json')
STZU13_FIXTURES = os.path.join(HERE, 'v13', 'fixtures.json')
STZU16_FIXTURES = os.path.join(HERE, 'v16', 'fixtures.json')
STZU17_FIXTURES = os.path.join(HERE, 'v17', 'meta_fixtures.json')


def judge_stzu(exe, label, fixtures=STZU_FIXTURES):
    """Mirror experiment/run_stzu.luau: accepts carry structural
    expectations, rejects carry the fragment the refusal must contain.
    v0.2's fixtures add the keys menus/ranges/formats/constraints (under
    counts), world and points."""
    doc = json.load(open(fixtures, encoding='utf-8'))
    # the pinned v0.1 judge is stzu's; everything since is Haro's (D1)
    assert doc['grammar'] in ('stzu', 'haro') and doc['version'] in ('0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.10', '0.11', '0.12', '0.13', '0.16', '0.17')
    passed = failed = 0
    outputs = {}
    with tempfile.TemporaryDirectory() as td:
        for case in doc['accepts'] + doc['rejects']:
            # v0.4: a fixture may carry files written beside it (the languages
            # its SENTENCEs name); each case gets its own folder so nothing leaks
            cd = os.path.join(td, case['id'])
            os.makedirs(cd, exist_ok=True)
            for fname, text in case.get('files', {}).items():
                with open(os.path.join(cd, fname), 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
            # a Haro declaration is a .haro file (D1); the pinned v0.1 judge keeps .stzu
            p = os.path.join(cd, case['id'] + ('.haro' if doc['grammar'] == 'haro' else '.stzu'))
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(case['source'])
            out = run(exe, STZU_RING, p)
            outputs[case['id']] = out
            ok, got = parse_verdict(out)
            why = ''
            if 'expect' in case:
                verdict = ok
                if not ok:
                    why = ' -- refused: ' + got
                else:
                    e = case['expect']
                    for k, want in e.items():
                        if k == 'counts':
                            for ck, cv in want.items():
                                if int(got.get(ck, '-1')) != cv:
                                    verdict = False
                                    why = f' -- {ck}: expected {cv} got {got.get(ck)}'
                        elif k == 'verbs':
                            g = [v for v in got.get('verbs', '').split(',') if v]
                            if g != sorted(want):
                                verdict = False
                                why = f' -- verbs: expected {sorted(want)} got {g}'
                        elif got.get(k) != str(want):
                            verdict = False
                            why = f" -- {k}: expected '{want}' got '{got.get(k)}'"
                if PLANT and case['id'] == 'A1':
                    verdict = False
                    why = ' -- PLANTED'
                kind = 'accept'
            else:
                frag = case['refusal']
                if ok:
                    verdict, why = False, ' -- ACCEPTED, must refuse'
                elif frag not in got:
                    verdict, why = False, f" -- refused for the wrong reason: '{frag}' not in '{got}'"
                else:
                    verdict = True
                kind = 'reject'
            if verdict:
                passed += 1
            else:
                failed += 1
                print(f'  FAIL {case["id"]} ({kind}): {case["name"]}{why}')
    print(f'{doc["grammar"].upper()}-CONFORMANCE ({label}): {passed} passed, {failed} failed')
    return failed, outputs


def stage1():
    failures = 0
    for label, fixtures in (('v0.1, the pinned judge', STZU_FIXTURES), ('v0.2, the WORLD and REFINE seats', STZU2_FIXTURES),
                            ('v0.3, the UNION, MESSAGES and the relations', STZU3_FIXTURES),
                            ('v0.4, the SENTENCE, the VIEW and the paths', STZU4_FIXTURES),
                            ('v0.5, CONTEXTS on an EXPRESSION', STZU5_FIXTURES),
                            ('v0.6, pair lists, the expression semantics and WALK', STZU6_FIXTURES),
                            ('v0.7, ASK -- the Q letter -- and ABSENT missing', STZU7_FIXTURES),
                            ('v0.8, what F needs: NAMED refusals, keyed pairs, a UNION of declarations, deadlines, ENTRY, three relations', STZU8_FIXTURES),
                            ('v0.9, what A needs: RUN, the structured steps, and a list of a UNION of declarations', STZU9_FIXTURES),
                            ('v0.10, the WORLD as versioned data: SYMBOL and PUBLISH', STZU10_FIXTURES),
                            ('v0.11, the Diagnostic Contract: CODE, CODES, CITES', STZU11_FIXTURES),
                            ('v0.12, FORMS: the function-name grammar as data', STZU12_FIXTURES),
                            ('v0.13, NARRATE: the court\'s voice', STZU13_FIXTURES),
                            ('v0.16, NARRATE tells a run and a question', STZU16_FIXTURES),
                            ('v0.17, UNDERSTAND: what a human language reaches closed questions with', STZU17_FIXTURES)):
        print(f'stage 1 -- the Haro meta-court in pure Ring, judged by its fixtures ({label})')
        f1, o1 = judge_stzu(RNXC, 'rnxc', fixtures)
        f2, o2 = judge_stzu(ORACLE, 'oracle ring.exe', fixtures)
        diff = [k for k in o1 if o1[k] != o2.get(k)]
        if diff:
            print(f'  FAIL the two runtimes differ on {len(diff)} fixture(s): {diff}')
            for k in diff[:3]:
                print('    rnxc  :', o1[k].strip()[:200])
                print('    oracle:', o2[k].strip()[:200])
        else:
            print(f'  ok   rnxc and the oracle print the same bytes on all {len(o1)} fixtures')
        failures += f1 + f2 + len(diff)
    return failures



# ---- stage 2: the forge; stage 3: the forged court against harb ------------

MACHINE_STZU = r'D:\GitHub\harobanda\declarative\machine\machine.stzu'
# the pinned floor of stage 3 on the default declaration: a fixture harb refuses
# and the court now ACCEPTS reads as "beyond the declaration", never as a defect,
# so a court that silently got weaker would pass -- it did once, 95 -> 67 read
# as 47 rules "beyond" (2026-10-01). The floor is the guard for that.
AGREE_FLOOR = 117
MACHINE_FIXTURES = r'D:\GitHub\harobanda\declarative\machine\fixtures.json'
MAKEEN = r'D:\GitHub\harobanda\machines\makeen_box.machine'
HARB = r'D:\GitHub\harobanda\zig-out\bin\harb.exe'
FORGE_RING = os.path.join(HERE, 'forge.ring')

SYNTAX_FRAGMENTS = ('Expected', 'Unknown', 'not part of', 'neither', 'Unterminated',
                    'A list', 'given twice', 'RATIONALE is mandatory', 'declares nothing')
# the fragments of court_lib's tokenizer and parser alone -- what a grammar derivation
# must never trip (stage 4); the shapes and duplicates above are the court's own stages
PARSE_FRAGMENTS = ('Expected', 'Unknown', 'not part of', 'neither', 'Unterminated',
                   'RATIONALE is mandatory', 'declares nothing')


def run_args(exe, args, cwd):
    env = dict(os.environ)
    env['RNXC_NOCACHE'] = '1'
    r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=120, cwd=cwd)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def stage2(stzu_path=MACHINE_STZU, label='machine'):
    """The forge on rnxc writes <lang>_court.ring and <lang>.gbnf beside
    court_lib.ring; the forge on the oracle writes the same into a scratch
    folder, and the two must be byte-identical (the forge is A/B'd too)."""
    print(f'stage 2 -- the forge: {os.path.basename(stzu_path)} -> a court and a grammar, on rnxc and on the oracle')
    out_rnx = run_args(RNXC, ['forge.ring', stzu_path, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    failures = 0
    if not out_rnx.startswith('forged '):
        print('  FAIL the forge did not forge')
        return 1, None
    lang = out_rnx.split()[1].rstrip(':')
    # the oracle forges into a scratch folder BESIDE the forge, by a relative
    # name: Ring's write() refused the temp folder's path on this machine
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')   # runtime/ is gitignored
    os.makedirs(td, exist_ok=True)
    for art in (f'{lang}_court.ring', f'{lang}.gbnf'):
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', stzu_path, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in (f'{lang}_court.ring', f'{lang}.gbnf'):
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    return failures, lang


def harb_verdict(path, verb='check', prefix='machine'):
    out = run_args(HARB, [verb, path], os.path.dirname(HARB)).strip()
    first = out.split('\n')[0] if out else ''
    if first.startswith(prefix + ' (line'):
        return False, first
    return True, first


# the fleet language (the fourth rung): harb's fleet fixtures carry the machine
# files their members name, written beside each case; `harb fleet <file>` is
# the native court, and its refusal reads `fleet (line N): ...`
FLEET_FIXTURES = r'D:\GitHub\harobanda\declarative\fleet\fixtures.json'
FLEET_STZU = os.path.join(HERE, 'fleet_v04.haro')
FLEET_FLOOR = 32
FLEET_COUNTS = {'members': 'MEMBER', 'retirements': 'RETIREMENT'}
MACHINE_COUNTS = {'services': 'SERVICE', 'capabilities': 'CAPABILITY', 'mounts': 'MOUNT',
                  'pins': 'PIN', 'networks': 'NETWORK', 'users': 'USER'}


def court_verdict(exe, court, path):
    out = run_args(exe, [court, 'check', path], HERE)
    return parse_verdict(out)


def stage3(lang, court=None, floor=0, fixtures=MACHINE_FIXTURES, verb='check', counts=MACHINE_COUNTS,
           scalars=('name', 'rationale', 'profile', 'arch', 'kernel', 'link')):
    """Every fixture of the language through harb and through the forged court.
    The verdicts are classified, and the class 'beyond the declaration'
    (harb refuses on a rule the .stzu does not carry) is the measurement.
    A fixture harb accepts and the forged court refuses is a DEFECT; an
    agree count under the pinned floor is one too."""
    court = court or f'{lang}_court.ring'
    print(f'stage 3 -- the forged court ({court}) against harb on the {lang} fixtures')
    doc = json.load(open(fixtures, encoding='utf-8'))
    cases = doc['accepts'] + doc['rejects']
    agree = []          # same verdict, and fragment / structural fields agree
    beyond = []         # harb refuses, the declaration cannot: a rule beyond it
    phrasing = []       # both refuse, the fixture's fragment is not in ours
    drift = []          # the DECLARATION lags the court: a clause, a kind or a
                        # type harb knows and the .stzu does not declare
    defects = []        # harb accepts, we refuse, and it is not drift
    unjudged = {}       # accept expectation keys the court does not claim
    ab_diff = []

    def is_drift(msg):
        return msg.split('): ', 1)[-1].startswith(('Unknown clause', 'Unknown kind', 'Clause '))
    with tempfile.TemporaryDirectory() as td:
        for case in cases:
            # each case in its own folder, with the files it carries beside it
            cd = os.path.join(td, case['id'])
            os.makedirs(cd, exist_ok=True)
            for fname, text in case.get('files', {}).items():
                with open(os.path.join(cd, fname), 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
            p = os.path.join(cd, case['id'] + '.' + lang)
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(case['source'])
            h_ok, h_line = harb_verdict(p, verb, lang)
            c_ok, c_got = court_verdict(RNXC, court, p)
            o_ok, o_got = court_verdict(ORACLE, court, p)
            if (c_ok, c_got) != (o_ok, o_got):
                ab_diff.append(case['id'])
            is_accept = 'expect' in case
            if h_ok and c_ok:
                # structural fields the court claims: name, rationale, the
                # first declaration's scalar clauses, the counts per verb
                e = case.get('expect', {})
                # the fleet fixtures put the counts beside the scalars
                flat = {}
                for k, want in e.items():
                    if k == 'counts':
                        flat.update(want)
                    else:
                        flat[k] = want
                why = ''
                for k, want in flat.items():
                    if k in counts:
                        got = c_got.get(f'count {counts[k]}')
                        if got is None:
                            unjudged[k] = unjudged.get(k, 0) + 1
                        elif int(got) != want:
                            why = f'{k}: expected {want} got {got}'
                    elif k in scalars:
                        got = c_got.get(k)
                        if want is None:
                            if got is not None:
                                why = f"{k}: expected none, got '{got}'"
                        elif got is None:
                            unjudged[k] = unjudged.get(k, 0) + 1
                        elif got != want:
                            why = f"{k}: expected '{want}' got '{got}'"
                    else:
                        unjudged[k] = unjudged.get(k, 0) + 1
                if why:
                    defects.append((case['id'], why))
                else:
                    agree.append(case['id'])
            elif (not h_ok) and (not c_ok):
                frag = case.get('refusal', '')
                if frag and frag in c_got:
                    agree.append(case['id'])
                elif is_drift(c_got):
                    drift.append((case['id'], c_got))
                else:
                    phrasing.append((case['id'], frag, c_got))
            elif (not h_ok) and c_ok:
                beyond.append((case['id'], h_line))
            elif is_drift(c_got):
                drift.append((case['id'], c_got))
            else:
                defects.append((case['id'], f'harb accepts, the court refuses: {c_got}'))
    if PLANT:
        defects.append(('A1', 'PLANTED: a verdict the guard must refuse'))
    n = len(cases)
    print(f'  {n} fixtures: {len(agree)} agree with harb; {len(beyond)} refused by harb on a rule BEYOND the declaration;')
    print(f'  {len(drift)} where the DECLARATION LAGS the court (a clause, kind or type it does not declare);')
    print(f'  {len(phrasing)} refused by both with a different fragment; {len(defects)} DEFECT(s) of the forged court')
    if unjudged:
        print('  accept expectations the declaration cannot claim (not judged):',
              ', '.join(f'{k} x{v}' for k, v in sorted(unjudged.items())))
    if '--verbose' in sys.argv:
        for cid, line in beyond:
            print(f'    beyond  {cid}: {line[:110]}')
        for cid, got in drift:
            print(f'    drift   {cid}: {got[:110]}')
    for cid, frag, got in phrasing:
        print(f'    phrase  {cid}: expected fragment {frag!r}; the court said: {got[:100]}')
    for cid, why in defects:
        print(f'    DEFECT  {cid}: {why[:140]}')
    if ab_diff:
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} fixture(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle agree on all {n} fixtures through the forged court')
    under = 0
    if floor and len(agree) < floor:
        under = 1
        print(f'  FAIL {len(agree)} agree with harb, under the pinned floor of {floor}: the court got weaker '
              f'(a fixture harb refuses and the court accepts reads as "beyond", never as a defect; the floor is the guard)')
    elif floor:
        print(f'  ok   {len(agree)} agree, at or above the pinned floor of {floor}')
    return len(defects) + len(ab_diff) + under


# ---- stage 4: the grammar, sampled and held by the engine's decoder ----------

import random, re

PACKAGE_RNXC = os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
GBNF_PROBE = os.path.join(HERE, 'gbnf_probe.ring')


class Gbnf:
    """A sampler over the forge's own GBNF dialect: rules `name ::= alts`,
    sequences of "literals", rule refs, [classes], groups with * + ?.
    Enough to derive random sentences of the emitted grammar."""
    TOK = re.compile(r'\s*(::=|\|\||\||\(|\)|\*|\+|\?|"(?:[^"\\]|\\.)*"|\[(?:[^\]\\]|\\.)*\]|[A-Za-z_][A-Za-z0-9_]*)')

    def __init__(self, text):
        self.rules = {}
        for line in text.splitlines():
            line = line.split('#', 1)[0].strip()
            if not line or '::=' not in line:
                continue
            name, rhs = line.split('::=', 1)
            self.rules[name.strip()] = self.parse_alts(self.tokens(rhs))

    def tokens(self, s):
        out, pos = [], 0
        while pos < len(s):
            m = self.TOK.match(s, pos)
            if not m:
                break
            out.append(m.group(1))
            pos = m.end()
        return out

    def parse_alts(self, toks):
        alts, seq = [], []
        i = 0
        while i < len(toks):
            t = toks[i]
            if t == '|':
                alts.append(seq); seq = []
            elif t == '(':
                depth, j = 1, i + 1
                while depth:
                    if toks[j] == '(': depth += 1
                    elif toks[j] == ')': depth -= 1
                    j += 1
                seq.append(('group', self.parse_alts(toks[i + 1:j - 1])))
                i = j - 1
            elif t in ('*', '+', '?'):
                seq[-1] = ('rep', seq[-1], t)
            elif t.startswith('"'):
                seq.append(('lit', bytes(t[1:-1], 'utf-8').decode('unicode_escape')))
            elif t.startswith('['):
                seq.append(('cls', t))
            else:
                seq.append(('ref', t))
            i += 1
        alts.append(seq)
        return alts

    def sample(self, rnd, name='root', depth=0):
        return self.seq(rnd, rnd.choice(self.rules[name]), depth)

    def seq(self, rnd, seq, depth):
        return ''.join(self.item(rnd, it, depth) for it in seq)

    def item(self, rnd, it, depth):
        kind = it[0]
        if kind == 'lit':
            return it[1]
        if kind == 'ref':
            return self.sample(rnd, it[1], depth + 1)
        if kind == 'group':
            return self.seq(rnd, rnd.choice(it[1]), depth + 1)
        if kind == 'cls':
            return self.cls(rnd, it[1])
        if kind == 'rep':
            lo = 1 if it[2] == '+' else 0
            hi = 1 if it[2] == '?' else (3 if depth < 6 else lo)
            n = rnd.randint(lo, hi)
            return ''.join(self.item(rnd, it[1], depth + 1) for _ in range(n))
        raise ValueError(kind)

    def cls(self, rnd, spec):
        body = spec[1:-1]
        neg = body.startswith('^')
        if neg:
            body = body[1:]
        body = bytes(body, 'utf-8').decode('unicode_escape')
        chars = []
        i = 0
        while i < len(body):
            if i + 2 < len(body) and body[i + 1] == '-':
                chars.extend(chr(c) for c in range(ord(body[i]), ord(body[i + 2]) + 1))
                i += 3
            else:
                chars.append(body[i]); i += 1
        if neg:
            pool = [chr(c) for c in range(32, 127) if chr(c) not in chars and chr(c) != '"']
            return rnd.choice(pool)
        return rnd.choice(chars)


def stage4(lang, court=None, n=200):
    """(a) n derivations of the forged grammar all pass the forged court's
    SYNTAX (a refusal, if any, is the court's semantic stage: a clause
    given twice or a required seat absent -- the grammar is context-free);
    (b) the engine's decoder accepts the grammar text and accepts the
    reference machine under it, through Softanza on rnxc in the package."""
    court = court or f'{lang}_court.ring'
    gbnf_path = os.path.join(HERE, f'{lang}.gbnf')
    print(f'stage 4 -- the grammar: {lang}.gbnf sampled {n} times, and held by the engine')
    failures = 0
    g = Gbnf(open(gbnf_path, encoding='utf-8').read())
    rnd = random.Random(20261001)
    syntax_refusals = 0
    semantic_refusals = {}
    with tempfile.TemporaryDirectory() as td:
        for k in range(n):
            text = g.sample(rnd)
            p = os.path.join(td, f's{k}.machine')
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            ok, got = court_verdict(RNXC, court, p)
            if not ok:
                msg = got.split('): ', 1)[-1]
                # a SYNTAX refusal comes from the court's tokenizer or parser and
                # carries one of their fragments; every other refusal is a stage
                # the grammar cannot carry, bucketed by what the declaration said
                if any(f in msg for f in PARSE_FRAGMENTS):
                    syntax_refusals += 1
                    if syntax_refusals <= 3:
                        print(f'    SYNTAX refusal of a derivation: {got[:120]}')
                        print('      ' + text[:160].replace('\n', ' | '))
                else:
                    bucket = ('a required seat absent' if 'is required on' in msg else
                              'a clause given twice' if 'given twice' in msg else
                              'a name declared twice' if 'already declared' in msg else
                              'a value shape' if msg.startswith(('Clause ', 'A list is')) else
                              'the WORLD (one, first)' if 'declares exactly one' in msg or 'comes first' in msg else
                              'a declared rule (menu, range, format, reference, constraint)')
                    semantic_refusals[bucket] = semantic_refusals.get(bucket, 0) + 1
    if syntax_refusals:
        failures += 1
        print(f'  FAIL {syntax_refusals} of {n} derivations refused for a SYNTAX reason: the grammar is wider than the court')
    else:
        sem = sum(semantic_refusals.values())
        print(f'  ok   {n} derivations: every one is a sentence to the court\'s parser; {sem} refused at the court\'s own stages'
              f' ({", ".join(f"{k.strip()} x{v}" for k, v in semantic_refusals.items())})')
    # (b) the engine: the grammar is held, and a sentence the forged court
    # ACCEPTS is accepted under it (qemu_hello.machine under the pinned
    # declaration; makeen_box.machine needs the clauses it lacks, HF-31)
    if not os.path.exists(PACKAGE_RNXC):
        print('  SKIP the engine probe: no package at runtime/package/ringpp-win64 (bench/package.py builds it)')
        return failures
    sentence = r'D:\GitHub\harobanda\machines\qemu_hello.machine'
    ok_c, _ = court_verdict(RNXC, court, sentence)
    if not ok_c:
        sentence = MAKEEN
    out = run_args(PACKAGE_RNXC, [GBNF_PROBE, gbnf_path, sentence], os.path.dirname(PACKAGE_RNXC))
    lines = {l.split(':')[0]: l.split(': ', 1)[-1] for l in out.splitlines() if ': ' in l}
    if lines.get('refusal') == '[]' and lines.get('accepts') == '1' and lines.get('supported') == '1':
        print(f'  ok   the engine\'s decoder (gbnf_machine.zig) holds the grammar and accepts {os.path.basename(sentence)} under it')
    else:
        failures += 1
        print(f'  FAIL the engine said: {out.strip()[:300]}')
    return failures


# ---- stage 5: one refinement through the gate ----------------------------------

C2_CODE = re.compile(r'^[A-Z][A-Z0-9]*([_-][A-Z0-9]+)*$')
C2_CITE = re.compile(r'^(rule|article|right|pattern):[A-Za-z0-9_.-]+$')


def c2_valid(rec):
    for k in ('code', 'severity', 'message', 'span', 'cites', 'language'):
        if k not in rec:
            return f'missing {k}'
    if not C2_CODE.match(rec['code']):
        return 'bad code'
    if rec['severity'] not in ('error', 'warning'):
        return 'bad severity'
    if not isinstance(rec['span'], dict) or 'file' not in rec['span'] or not isinstance(rec['span'].get('line'), int):
        return 'bad span'
    if any(not C2_CITE.match(c) for c in rec['cites']):
        return 'bad cite'
    if not re.match(r'^[a-z][a-z0-9_]*$', rec['language']):
        return 'bad language'
    for k, v in rec.items():
        if k not in ('code', 'severity', 'message', 'span', 'cites', 'language') and (v is None or isinstance(v, bool)):
            return f'extension {k} is a bare boolean or null'
    return None


def stage5(lang, court=None, v02=False):
    court = court or f'{lang}_court.ring'
    print('stage 5 -- one refinement through the gate: hello.RESTART never -> always'
          + (' (v0.2: the points and floors the language declares)' if v02 else ''))
    failures = 0
    floor = 'external' if v02 else 'trusted'
    src = open(r'D:\GitHub\harobanda\machines\qemu_hello.machine', 'rb').read()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'hello.machine')
        open(p, 'wb').write(src)
        if v02:
            # (v) a point the language does not declare refinable; a value outside the
            # knob's MENU; the external actor admitted at the point's declared floor
            o = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'refine_point.rfn')], HERE)
            if "is not a declared refinement point" in o and 'NOT_A_POINT' in o:
                print('  ok   a seat outside REFINE\'s POINTS is refused: qemu_hello.ARCH is not a declared point')
            else:
                failures += 1; print(f'  FAIL expected NOT_A_POINT, got: {o.strip()[:160]}')
            o = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'refine_kind.rfn')], HERE)
            if "'qemu_hello.PROFILE' is a policy, not a knob" in o and 'KIND_MISMATCH' in o:
                print('  ok   a declared point of another KIND is refused: qemu_hello.PROFILE is a policy, not a knob')
            else:
                failures += 1; print(f'  FAIL expected KIND_MISMATCH, got: {o.strip()[:160]}')
            o = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'hello_menu.rfn')], HERE)
            if "RESTART is never, always or on_failure, not 'sometimes'" in o and 'OUT_OF_BOUNDS' in o:
                print('  ok   a value outside the knob\'s MENU is refused at constraint, in the menu\'s own words')
            else:
                failures += 1; print(f'  FAIL expected the menu\'s refusal, got: {o.strip()[:160]}')
            o = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'hello_external.rfn')], HERE)
            if o.startswith('admitted: hello.RESTART never -> always [external]'):
                print('  ok   an external actor is admitted at the point\'s declared floor, external')
                for ext in ('.refined', '.revert.rfn'):
                    if os.path.exists(p + ext):
                        os.remove(p + ext)
            else:
                failures += 1; print(f'  FAIL expected admission as :external, got: {o.strip()[:160]}')
        # (a) the model-composed proposal is refused at the trust stage, with a C2 record
        out = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'hello_llm.rfn')], HERE)
        if PLANT:
            out = out.replace('trust: posture :llm', 'PLANTED: posture :llm')
        lines = [l for l in out.splitlines() if l]
        if len(lines) >= 2 and f'trust: posture :llm below the required floor :{floor}' in lines[0]:
            try:
                rec = json.loads(lines[1])
                why = c2_valid(rec)
                if why or rec['code'] != 'TRUST_FLOOR' or 'todo' not in rec:
                    failures += 1
                    print(f'  FAIL the refusal record is not a C2 envelope: {why or rec}')
                else:
                    print(f'  ok   refused at trust, as :llm against a floor of :{floor}; the record is C2 with why and todo')
            except json.JSONDecodeError as e:
                failures += 1
                print(f'  FAIL the record is not JSON: {e}: {lines[1][:120]}')
        else:
            failures += 1
            print(f'  FAIL expected a trust refusal, got: {out.strip()[:200]}')
        if os.path.exists(p + '.refined'):
            failures += 1
            print('  FAIL a refused refinement wrote a refined file')
        # (b) the trusted proposal is admitted; the refined file differs on the one value
        out = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'hello_trusted.rfn')], HERE)
        if out.startswith('admitted: hello.RESTART never -> always [trusted]'):
            refined = open(p + '.refined', 'rb').read()
            ok2, _ = court_verdict(RNXC, court, p + '.refined')
            if refined.count(b'RESTART always') == 1 and refined.replace(b'RESTART always', b'RESTART never', 1) == src and ok2:
                print('  ok   admitted as :trusted; the refined file differs on the one value and is a sentence of the language')
            else:
                failures += 1
                print('  FAIL the refined file is not the original with one value changed')
            # (c) the inverse, computed before the refinement landed, restores the bytes
            out2 = run_args(RNXC, [court, 'refine', p + '.refined', p + '.revert.rfn'], HERE)
            reverted = open(p + '.refined.refined', 'rb').read() if os.path.exists(p + '.refined.refined') else b''
            if out2.startswith('admitted:') and reverted == src:
                print('  ok   the revert restores the original byte for byte')
            else:
                failures += 1
                print(f'  FAIL the revert did not restore the original: {out2.strip()[:120]}')
        else:
            failures += 1
            print(f'  FAIL expected admission, got: {out.strip()[:200]}')
        # the same gate on the oracle: byte-identical verdicts
        o = run_args(ORACLE, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'hello_llm.rfn')], HERE)
        r = run_args(RNXC, [court, 'refine', p, os.path.join(HERE, 'fixtures', 'hello_llm.rfn')], HERE)
        if o == r:
            print('  ok   rnxc and the oracle print the same refusal, byte for byte')
        else:
            failures += 1
            print('  FAIL the two runtimes differ on the refusal')
            print('    rnxc  :', r.strip()[:160]); print('    oracle:', o.strip()[:160])
    return failures


# ---- stage 6: edit to verdict, measured ------------------------------------------

# ---- stage 8: W, an EXPRESSION language forged whole (the fifth rung) ---------------
# stz's W is declared in w_v05.haro; the forge emits w_expr.ring (court and
# evaluator) and w_expr.gbnf; stz's 29 fixtures (declarative/w/fixtures.json,
# read by reference, unadapted) judge the evaluator on rnxc and on the oracle,
# byte for byte; 200 derivations of the grammar must all be sentences to it.

W_STZU = os.path.join(HERE, 'w_v05.haro')
W_FIXTURES = r'D:\GitHub\stz\declarative\w\fixtures.json'
W_FLOOR = 29


def w_run(exe, args):
    return run_args(exe, ['w_expr.ring'] + args, HERE).strip()


def stage8():
    print('stage 8 -- W, an EXPRESSION language forged whole: w_v05.haro -> w_expr.ring and w_expr.gbnf, judged by stz\'s W fixtures unadapted')
    failures = 0
    out_rnx = run_args(RNXC, ['forge.ring', W_STZU, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    if not out_rnx.startswith('forged w'):
        print('  FAIL the forge did not forge W')
        return 1
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')
    os.makedirs(td, exist_ok=True)
    for art in ('w_expr.ring', 'w_expr.gbnf'):
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', W_STZU, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in ('w_expr.ring', 'w_expr.gbnf'):
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    doc = json.load(open(W_FIXTURES, encoding='utf-8'))
    assert doc['grammar'] == 'W' and doc['version'] == '0.1', 'unexpected W fixture file'
    passed = failed = 0
    ab_diff = []
    for case in doc['cases']:
        kind = case['kind']
        if kind == 'refuse':
            seat = 'map' if case['seat'] in ('map', 'filter') else 'reduce'
            args = ['check', seat, case['expr']]
        else:
            args = ['eval', kind, case['expr']]
            if 'input' in case:
                args.append(json.dumps(case['input']))
            if 'init' in case:
                args.append(json.dumps(case['init']))
        r = w_run(RNXC, args)
        o = w_run(ORACLE, args)
        if r != o:
            ab_diff.append(case['id'])
        if kind == 'refuse':
            ok = r.startswith('refused:')
            why = '' if ok else f' -- not refused: {r[:120]}'
        else:
            try:
                got = json.loads(r)
                ok = got == case['expected']
                why = '' if ok else f' -- expected {json.dumps(case["expected"])} got {r[:120]}'
            except json.JSONDecodeError:
                ok = False
                why = f' -- not a value: {r[:120]}'
        if PLANT and case['id'] == 'eval-precedence':
            ok, why = False, ' -- PLANTED'
        if ok:
            passed += 1
        else:
            failed += 1
            print(f'  FAIL {case["id"]} ({kind}): {case["expr"]}{why}')
    print(f'W-CONFORMANCE (the forged evaluator on rnxc): {passed} passed, {failed} failed')
    failures += failed
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} case(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {len(doc["cases"])} cases')
    if W_FLOOR and passed < W_FLOOR:
        failures += 1
        print(f'  FAIL {passed} passed, under the pinned floor of {W_FLOOR}')
    # the grammar: every derivation is a sentence to the forged court
    g = Gbnf(open(os.path.join(HERE, 'w_expr.gbnf'), encoding='utf-8').read())
    rnd = random.Random(20261002)
    bad = 0
    n = 200
    for k in range(n):
        text = g.sample(rnd)
        r = w_run(RNXC, ['check', 'reduce', text])
        if r != 'ok':
            bad += 1
            if bad <= 3:
                print(f'    a derivation the court refuses: {text[:80]!r}: {r[:100]}')
    if bad:
        failures += 1
        print(f'  FAIL {bad} of {n} derivations of w_expr.gbnf are not sentences to the forged court')
    else:
        print(f'  ok   {n} derivations of w_expr.gbnf: every one is a sentence to the forged court')
    return failures


# ---- stage 9: Z, a WORLD forged whole -- court AND runtime -- judged by zing's 16 cases

Z_STZU = os.path.join(HERE, 'z_v16.haro')   # z_v10.haro plus a NARRATE that tells a question (the sixteenth rung); the 16 cases and 25 questions are unchanged
Z_SENTENCE = 'tontine.z'
Z_FIXTURES = r'D:\GitHub\zing\conformance\fixtures.json'
Z_FLOOR = 16
Z_COUNTS = {'entities': 'ENTITY', 'norms': 'NORM', 'flows': 'FLOW', 'zones': 'LANDING_ZONE'}


def z_run(exe, args):
    return run_args(exe, ['z_court.ring'] + args, HERE).strip()


def stage9():
    """The sixth rung. z_v06.haro declares ZQL in the Grammar Commons' shape
    (an EXPRESSION with ABSENT/DIVISION/EQUALITY, entities with pair-list
    FIELDS, norms and steps with expression seats, a WALK of flows); the
    forge emits its sentence court, its expression court and both grammars;
    tontine.z is zing's fixture source re-expressed in that shape (the ONE
    adaptation, haro/SPIKE.md); and the 16 cases -- 4 norms on records, 8
    flows on records with their computed fields, 4 destructive rejects --
    are judged on the forged court unadapted, their data and expectations
    read from zing's file. A step is named lower_snake in the Commons where
    ZQL names it UPPER, so `at` is compared case-blind; nothing else is."""
    print('stage 9 -- Z, a WORLD forged whole: z_v06.haro -> z_court.ring, z.gbnf, z_expr.ring, z_expr.gbnf; tontine.z judged by zing\'s 16 cases unadapted')
    failures = 0
    out_rnx = run_args(RNXC, ['forge.ring', Z_STZU, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    if not out_rnx.startswith('forged z'):
        print('  FAIL the forge did not forge Z')
        return 1
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')
    os.makedirs(td, exist_ok=True)
    arts = ('z_court.ring', 'z.gbnf', 'z_expr.ring', 'z_expr.gbnf', 'z_ask.gbnf')
    for art in arts:
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', Z_STZU, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in arts:
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    doc = json.load(open(Z_FIXTURES, encoding='utf-8'))
    assert doc['name'] == 'tontine conformance fixtures v1', 'unexpected Z fixture file'
    ab_diff = []
    # the sentence itself: accepted, with the fixture's counts
    r = z_run(RNXC, ['check', Z_SENTENCE])
    o = z_run(ORACLE, ['check', Z_SENTENCE])
    if r != o:
        ab_diff.append('check tontine.z')
    ok, fields = parse_verdict(r)
    if not ok:
        failures += 1
        print(f'  FAIL tontine.z is refused: {fields}')
    else:
        for k, verb in Z_COUNTS.items():
            want = doc['counts'][k]
            got = int(fields.get('count ' + verb, '-1'))
            if got != want:
                failures += 1
                print(f'  FAIL tontine.z counts {got} {verb}, the fixture {want} {k}')
        print(f'  ok   tontine.z is a sentence of z: ' + ', '.join(f'{doc["counts"][k]} {k}' for k in Z_COUNTS))
    passed = failed = 0
    for case in doc['normCases']:
        args = ['eval', Z_SENTENCE, case['norm'], 'rule', json.dumps(case['data'])]
        r = z_run(RNXC, args)
        o = z_run(ORACLE, args)
        if r != o:
            ab_diff.append(case['name'])
        ok = r == json.dumps(case['expect'])
        if ok:
            passed += 1
        else:
            failed += 1
            print(f'  FAIL norm {case["norm"]} / {case["name"]}: expected {json.dumps(case["expect"])} got {r[:120]}')
    for case in doc['flowCases']:
        args = ['walk', Z_SENTENCE, case['flow'], json.dumps(case['data'])]
        r = z_run(RNXC, args)
        o = z_run(ORACLE, args)
        if r != o:
            ab_diff.append(case['name'])
        why = ''
        try:
            got = json.loads(r)
            ok = got.get('status') == case['expect']
            if ok and 'at' in case:
                ok = got.get('at', '').lower() == case['at'].lower()
            if ok and 'computed' in case:
                ok = got.get('computed') == case['computed']
            if not ok:
                why = f' -- expected {case["expect"]}' + (f' at {case["at"]}' if 'at' in case else '') + \
                      (f' computed {json.dumps(case["computed"])}' if 'computed' in case else '') + f', got {r[:160]}'
        except json.JSONDecodeError:
            ok = False
            why = f' -- not a verdict: {r[:160]}'
        if PLANT and case['name'].startswith('FORMULA: [4,5,3,4,5]'):
            ok, why = False, ' -- PLANTED'
        if ok:
            passed += 1
        else:
            failed += 1
            print(f'  FAIL flow {case["flow"]} / {case["name"]}{why}')
    with tempfile.TemporaryDirectory() as tdr:
        for k, text in enumerate(doc['rejects']):
            p = os.path.join(tdr, f'reject{k}.z')
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(text + '\n')
            r = z_run(RNXC, ['check', p])
            o = z_run(ORACLE, ['check', p])
            if r != o:
                ab_diff.append(text)
            ok = not r.startswith('ok') and 'closed' in r
            if ok:
                passed += 1
            else:
                failed += 1
                print(f'  FAIL reject {text!r}: {r[:160]}')
    # the walk orders the steps by ORDER, not by their place in the file: the
    # same sentence with every STEP declaration in reverse order must answer
    # the flow cases identically (HF-52: Ring's insert() is after-the-index)
    src = open(os.path.join(HERE, Z_SENTENCE), encoding='utf-8').read()
    blocks = src.split('DEFINE STEP ')
    steps = ['DEFINE STEP ' + b for b in blocks[1:]]
    # a block runs to the next DEFINE; keep what follows the last step's own text
    tail_at = steps[-1].find('DEFINE ', 1)
    tail = steps[-1][tail_at:] if tail_at > 0 else ''
    if tail_at > 0:
        steps[-1] = steps[-1][:tail_at]
    reversed_src = blocks[0] + ''.join(reversed(steps)) + tail
    with tempfile.TemporaryDirectory() as tdr:
        p = os.path.join(tdr, 'tontine_reversed.z')
        with open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(reversed_src)
        for case in doc['flowCases']:
            r1 = z_run(RNXC, ['walk', Z_SENTENCE, case['flow'], json.dumps(case['data'])])
            r2 = z_run(RNXC, ['walk', p, case['flow'], json.dumps(case['data'])])
            if r1 != r2:
                failed += 1
                print(f"  FAIL the walk depends on where its steps stand in the file: {case['name']}: {r2[:120]}")
    n = len(doc['normCases']) + len(doc['flowCases']) + len(doc['rejects'])
    print(f'Z-CONFORMANCE (the forged court and runtime on rnxc): {passed} passed, {failed} failed of {n}; the {len(doc["flowCases"])} flow cases identical with the steps declared in reverse')
    failures += failed
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} case(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {n} cases and the sentence')
    if Z_FLOOR and passed < Z_FLOOR:
        failures += 1
        print(f'  FAIL {passed} passed, under the pinned floor of {Z_FLOOR}')
    return failures


# ---- stage 10: Q, the question grammar of the declared world, judged by zing's own answers

Q_FIXTURES = os.path.join(HERE, 'v07', 'q_cases.json')
Q_FLOOR = 25
ZING = r'D:\GitHub\zing\cli\zig-out\bin\zing.exe'
ZING_EXAMPLE = r'D:\GitHub\zing\examples\bedrock-query'
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def zing_rows(out):
    rows = []
    for line in out.splitlines():
        m = re.match(r'\s*#(\d+)\s+\S+ \S+\s+by \S+ -- (.*)$', line)
        if m:
            rows.append(json.loads(m.group(2)))
    return rows


def stage10():
    """The seventh rung. z_v07.haro adds the ASK (the Q letter) to Z; the forged
    court's `ask` verb answers a question on the rows handed in; the judge is
    zing itself: v07/q_cases.json holds zing's own answers to 25 questions on a
    scratch copy of its bedrock-query example (6 ledger deposits plus 4 replayed
    through `zing flow`), captured by the probe that wrote the file, and this
    stage re-runs zing live when it is built here and reports any drift. The
    one case zing and the declared altitude answer differently (a FROM that
    names no declared flow: zing lists nothing, Haro refuses) is marked
    haro_only and recorded as HF-51."""
    print('stage 10 -- Q, the question grammar of a declared world: z_v07.haro\'s ASK -> the ask verb and z_ask.gbnf, judged by zing\'s own answers on its bedrock-query example')
    failures = 0
    doc = json.load(open(Q_FIXTURES, encoding='utf-8'))
    assert doc['grammar'] == 'Q' and doc['version'] == '0.7', 'unexpected Q fixture file'
    rows_json = json.dumps(doc['rows'])
    passed = failed = 0
    ab_diff = []
    for case in doc['cases']:
        args = ['ask', Z_SENTENCE, case['query'], rows_json]
        r = z_run(RNXC, args)
        o = z_run(ORACLE, args)
        if r != o:
            ab_diff.append(case['id'])
        if 'refusal' in case:
            ok = (not r.startswith('[')) and case['refusal'] in r
            why = '' if ok else f' -- expected a refusal holding {case["refusal"]!r}, got {r[:160]}'
        else:
            try:
                got = json.loads(r)
                ok = got == case['expect']
                why = '' if ok else f' -- expected {json.dumps(case["expect"])[:120]}, got {r[:160]}'
            except json.JSONDecodeError:
                ok = False
                why = f' -- not an answer: {r[:160]}'
        if PLANT and case['id'] == 'q03':
            ok, why = False, ' -- PLANTED'
        if ok:
            passed += 1
        else:
            failed += 1
            print(f'  FAIL {case["id"]}: {case["query"]}{why}')
    n = len(doc['cases'])
    print(f'Q-CONFORMANCE (the forged court\'s ask verb on rnxc): {passed} passed, {failed} failed of {n}')
    failures += failed
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} question(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {n} questions')
    if Q_FLOOR and passed < Q_FLOOR:
        failures += 1
        print(f'  FAIL {passed} passed, under the pinned floor of {Q_FLOOR}')
    # zing live: the fixture's answers are zing's, re-taken when zing is built here
    if os.path.exists(ZING) and os.path.isdir(ZING_EXAMPLE):
        env = dict(os.environ)
        env['STZW_WIDTH'] = '200'
        with tempfile.TemporaryDirectory() as td:
            work = os.path.join(td, 'tontine')
            shutil.copytree(ZING_EXAMPLE, work)
            def zing(args):
                p = subprocess.run([ZING] + args, cwd=work, capture_output=True, env=env, timeout=60)
                return p.returncode, ANSI.sub('', p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace'))
            for data, actor in doc['replay']:
                rc, out = zing(['flow', 'collect', '--data', json.dumps(data), '--actor', actor])
                if 'COMMITTED' not in out:
                    failures += 1
                    print(f'  FAIL zing did not commit the replayed deposit {json.dumps(data)}: {out[:160]}')
            live_rows = []
            for line in open(os.path.join(work, '.stz', 'bedrock.jsonl'), encoding='utf-8'):
                if line.strip():
                    live_rows.append(json.loads(json.loads(line)['data']))
            if live_rows != doc['rows']:
                failures += 1
                print(f'  FAIL the fixture\'s rows are not zing\'s ledger: {len(live_rows)} live against {len(doc["rows"])} in the file')
            agree = judged = 0
            for case in doc['cases']:
                if case.get('haro_only'):
                    continue
                judged += 1
                rc, out = zing(['query', case['query']])
                if 'refusal' in case:
                    ok = rc != 0 and not zing_rows(out)
                else:
                    ok = rc == 0 and zing_rows(out) == case['expect']
                if ok:
                    agree += 1
                else:
                    failures += 1
                    print(f'  FAIL zing live disagrees with the fixture on {case["id"]}: {case["query"]} -> {out.strip()[:160]}')
            print(f'  ok   zing live, on its own example replayed: agrees with the fixture on {agree} of {judged} judged questions; {n - judged} haro-only (HF-51)')
    else:
        print('  SKIP zing is not built here; the fixture stands on the answers captured from it')
    return failures


# ---- stage 11: F, the flow of work -- RingFlex's .wflow re-declared, judged by its own fixtures

F_STZU = os.path.join(HERE, 'f_v13.haro')   # f_v11.haro plus a NARRATE (the thirteenth rung); the 27 fixtures are unchanged
F_DIR = os.path.join(HERE, 'f')
F_FLOOR = 26
RINGFLEX = r'D:\GitHub\ringflex'
RING_OFFICIAL = r'D:\ring127\bin\ring.exe'


def f_run(exe, args):
    return run_args(exe, ['f_court.ring'] + args, HERE).strip()


def f_expect(src):
    for line in src.splitlines():
        line = line.strip()
        if line.startswith('-- EXPECT: '):
            return line[len('-- EXPECT: '):].strip()
    return ''


def stage11():
    """The eighth rung. f_v08.haro declares RingFlex's .wflow v0 in the Commons'
    shape; the forge emits its court; and the judge is RingFlex's own fixture
    suite -- 24 one-defect workflows and the two reference workflows, each
    carrying its expected verdict on its first line (clean / refuse Cn /
    parse-error <fragment>), re-expressed in haro/spike/f/ (notation only,
    the one defect each kept). The forged court must give the expected verdict
    on rnxc and on the oracle, byte-identical. RingFlex's own court is run
    live on the ORIGINAL fixtures when official Ring 1.27 is installed (its
    runner loads Ring's full stdlib, which the oracle cannot), to show the
    expectations hold on their own side."""
    print('stage 11 -- F, the flow of work: f_v08.haro -> f_court.ring and f.gbnf, judged by RingFlex\'s 26 fixtures re-expressed in the Commons\' shape')
    failures = 0
    out_rnx = run_args(RNXC, ['forge.ring', F_STZU, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    if not out_rnx.startswith('forged f'):
        print('  FAIL the forge did not forge F')
        return 1
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')
    os.makedirs(td, exist_ok=True)
    for art in ('f_court.ring', 'f.gbnf'):
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', F_STZU, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in ('f_court.ring', 'f.gbnf'):
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    files = sorted(f for f in os.listdir(F_DIR) if f.endswith('.f'))
    passed = failed = 0
    ab_diff = []
    for name in files:
        src = open(os.path.join(F_DIR, name), encoding='utf-8').read()
        exp = f_expect(src)
        if not exp:
            failed += 1
            print(f'  FAIL {name}: no -- EXPECT: line')
            continue
        r = f_run(RNXC, ['check', os.path.join('f', name)])
        o = f_run(ORACLE, ['check', os.path.join('f', name)])
        if r != o:
            ab_diff.append(name)
        kind, _, arg = exp.partition(' ')
        first = r.split('\n')[0] if r else ''
        if kind == 'clean':
            ok = first == 'ok'
            why = '' if ok else f' -- expected clean, got: {first[:160]}'
        elif kind == 'parse-error':
            ok = first != 'ok' and arg in r
            why = '' if ok else f' -- expected a refusal holding {arg!r}, got: {first[:160]}'
        elif kind == 'refuse':
            ok = first != 'ok' and re.search(r'\b' + re.escape(arg) + r'\b', r) is not None
            why = '' if ok else f' -- expected a refusal under {arg}, got: {first[:160]}'
        else:
            ok, why = False, f' -- unknown expectation {exp!r}'
        if PLANT and name == 'dead-step.f':
            ok, why = False, ' -- PLANTED'
        if ok:
            passed += 1
        else:
            failed += 1
            print(f'  FAIL {name} ({exp}){why}')
    print(f'F-CONFORMANCE (the forged court on rnxc, RingFlex\'s fixtures re-expressed): {passed} passed, {failed} failed of {len(files)}')
    failures += failed
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} fixture(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {len(files)} fixtures')
    if F_FLOOR and passed < F_FLOOR:
        failures += 1
        print(f'  FAIL {passed} passed, under the pinned floor of {F_FLOOR}')
    # RingFlex's own court on the original fixtures: the expectations hold there
    if os.path.exists(RING_OFFICIAL) and os.path.isdir(RINGFLEX):
        p = subprocess.run([RING_OFFICIAL, 'tests/run.ring'], cwd=RINGFLEX, capture_output=True, timeout=120)
        out = p.stdout.decode('utf-8', 'replace')
        m = re.search(r'(\d+) passed, (\d+) failed', out)
        if m and m.group(2) == '0' and int(m.group(1)) >= F_FLOOR:
            print(f'  ok   RingFlex\'s own court (official Ring 1.27, read-only): {m.group(1)} passed, 0 failed on its original fixtures')
        else:
            failures += 1
            print(f'  FAIL RingFlex\'s own court did not hold its fixtures: {out[-200:]}')
    else:
        print('  SKIP RingFlex\'s own court: its runner loads Ring\'s full stdlib.ring, which the oracle cannot, and official Ring 1.27 is not installed here')
    return failures


# ---- stage 12: A, the algorithm -- stz's W cases and zing's formulas re-expressed as step trees

A_STZU = os.path.join(HERE, 'a_v16.haro')   # a_v09.haro plus a NARRATE that tells a run (the sixteenth rung); the 35 cases are unchanged
A_SENTENCE = os.path.join('a', 'w_in_a.a')
A_CASES = os.path.join(HERE, 'v09', 'a_cases.json')
A_FLOOR = 35


def a_run(exe, args):
    return run_args(exe, ['a_court.ring'] + args, HERE).strip()


def stage12():
    """The ninth rung. a_v09.haro declares A -- five constructs, a step tree, a
    RUN -- and the forge emits its court and its runner. The judge is other
    repositories' numbers: stz's 29 W cases (map, filter, count, partition,
    groupby, reduce, the constant evaluations and the five refusals) and
    zing's formula cases, each re-expressed as an algorithm in a/w_in_a.a
    with its expected value copied from the source file by the generator;
    plus three hand cases that the W shape cannot say (nested iteration, a
    running maximum, a branch inside a branch), each computed by hand and
    marked so."""
    print('stage 12 -- A, the algorithm: a_v09.haro -> a_court.ring and its runner, judged by stz\'s W cases and zing\'s formulas re-expressed as step trees')
    failures = 0
    out_rnx = run_args(RNXC, ['forge.ring', A_STZU, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    if not out_rnx.startswith('forged a'):
        print('  FAIL the forge did not forge A')
        return 1
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')
    os.makedirs(td, exist_ok=True)
    arts = ('a_court.ring', 'a.gbnf', 'a_expr.ring', 'a_expr.gbnf')
    for art in arts:
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', A_STZU, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in arts:
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    doc = json.load(open(A_CASES, encoding='utf-8'))
    assert doc['grammar'] == 'A' and doc['version'] == '0.9', 'unexpected A case file'
    ab_diff = []
    r = a_run(RNXC, ['check', A_SENTENCE])
    o = a_run(ORACLE, ['check', A_SENTENCE])
    if r != o:
        ab_diff.append('check')
    ok, fields = parse_verdict(r)
    if not ok:
        failures += 1
        print(f'  FAIL w_in_a.a is refused: {fields}')
    else:
        print(f'  ok   w_in_a.a is a sentence of a: {fields.get("count ALGORITHM")} algorithms over {sum(int(v) for k, v in fields.items() if k.startswith("count ") and k != "count ALGORITHM")} steps')
    passed = failed = 0
    with tempfile.TemporaryDirectory() as tdr:
        for case in doc['cases']:
            if 'source' in case:
                p = os.path.join(tdr, case['id'] + '.a')
                with open(p, 'w', encoding='utf-8', newline='') as f:
                    f.write(case['source'])
                r = a_run(RNXC, ['check', p])
                o = a_run(ORACLE, ['check', p])
                ok = (not r.startswith('ok')) and case['refusal'] in r
                why = '' if ok else f' -- expected a refusal holding {case["refusal"]!r}, got {r[:160]}'
            else:
                args = ['run', A_SENTENCE, case['algorithm'], json.dumps(case['input'])]
                r = a_run(RNXC, args)
                o = a_run(ORACLE, args)
                if 'refusal' in case:
                    ok = case['refusal'] in r
                    why = '' if ok else f' -- expected a refusal holding {case["refusal"]!r}, got {r[:160]}'
                else:
                    try:
                        got = json.loads(r)
                        ok = got == case['expected']
                        why = '' if ok else f' -- expected {json.dumps(case["expected"])} got {r[:160]}'
                    except json.JSONDecodeError:
                        ok = False
                        why = f' -- not a value: {r[:160]}'
            if r != o:
                ab_diff.append(case['id'])
            if PLANT and case['id'] == 'map-scale':
                ok, why = False, ' -- PLANTED'
            if ok:
                passed += 1
            else:
                failed += 1
                print(f'  FAIL {case["id"]} ({case["from"]}){why}')
    n = len(doc['cases'])
    print(f'A-CONFORMANCE (the forged runner on rnxc): {passed} passed, {failed} failed of {n}')
    failures += failed
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} case(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {n} cases and the sentence')
    if A_FLOOR and passed < A_FLOOR:
        failures += 1
        print(f'  FAIL {passed} passed, under the pinned floor of {A_FLOOR}')
    # the totality guard: a step tree that re-enters itself is refused at check
    cyc = ('DEFINE ALGORITHM loop AS (STEPS [again], RESULT [n]) RATIONALE "x"\n'
           'DEFINE COMPUTE bump AS (INTO n, VALUE "n + 1") RATIONALE "x"\n'
           'DEFINE BRANCH again AS (WHEN "n < 10", THEN [bump, again]) RATIONALE "a loop in disguise"\n')
    with tempfile.TemporaryDirectory() as tdr:
        p = os.path.join(tdr, 'loop.a')
        with open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(cyc)
        r = a_run(RNXC, ['check', p])
        if r.startswith('ok') or 're-enters itself' not in r:
            failures += 1
            print(f'  FAIL a step tree with a cycle was not refused at check: {r[:160]}')
        else:
            print('  ok   a step tree that re-enters itself is refused at check: termination is structural')
    return failures


# ---- stage 13: the WORLD as versioned data -- C1 rows emitted, C3 3.2 resolved, judged by RingFlex's placement fixtures

RINGFLEX_WORLDS = os.path.join(RINGFLEX, 'fixtures', 'world')


def stage13():
    """The tenth rung. F's INVOKES and COMPENSATED_BY are SYMBOL seats resolved
    against a C1 world handed to `check`; Z PUBLISHes its flows, entities, norms
    and zones, and `world <file>` emits a sentence's C1 rows. The judge is
    RingFlex's placement gate (tests/boundary-run.ring, sections C and D) on its
    own world fixtures, read-only: the lawful workflow resolves against
    world.json; a world missing one flow refuses exactly the step that names it;
    a world missing the compensating flow refuses the compensating step by the
    flow's name; no world at all is a warning, not a refusal; and the rows a
    workflow contributes are one process symbol and three calls refs, no flow
    symbol. Then the seam between two forged letters: the world Z's court emits
    from tontine.z resolves an F workflow that invokes two of its flows, and the
    merged rows satisfy C1 3.2 (every ref's ends are symbols)."""
    print('stage 13 -- the WORLD as versioned data: z_v10.haro publishes, f_v10.haro resolves; judged by RingFlex\'s placement fixtures and the Z->F seam')
    failures = 0
    for stzu in (Z_STZU, F_STZU):
        out = run_args(RNXC, ['forge.ring', stzu, '.'], HERE).strip()
        if not out.startswith('forged '):
            print(f'  FAIL the forge did not forge {os.path.basename(stzu)}: {out[:120]}')
            return 1
    ab_diff = []
    def both(court, args, label):
        r = run_args(RNXC, [court] + args, HERE).strip()
        o = run_args(ORACLE, [court] + args, HERE).strip()
        if r != o:
            ab_diff.append(label)
        return r
    checks = 0
    wf = os.path.join('f', 'boundary-invokes-flow.f')
    worlds = {k: os.path.join(RINGFLEX_WORLDS, k + '.json') for k in ('world', 'world-missing-flow', 'world-missing-compensating')}
    if not all(os.path.exists(p) for p in worlds.values()):
        print('  SKIP RingFlex\'s world fixtures are not here')
        return 0
    r = both('f_court.ring', ['check', wf, worlds['world']], 'resolved')
    ok = r.startswith('ok') and 'warning' not in r
    checks += 1; failures += 0 if ok else 1
    print(('  ok   ' if ok else '  FAIL ') + f'the lawful workflow resolves every INVOKES against world.json: {r.splitlines()[0][:60]}')
    r = both('f_court.ring', ['check', wf, worlds['world-missing-flow']], 'missing-flow')
    ok = (not r.startswith('ok')) and 'declares no flow:' in r and 'notifier' in r and 'notifier_client' in r
    checks += 1; failures += 0 if ok else 1
    print(('  ok   ' if ok else '  FAIL ') + f'a world missing one flow refuses the step that names it, by both names: {r[:110]}')
    r = both('f_court.ring', ['check', wf, worlds['world-missing-compensating']], 'missing-compensating')
    ok = (not r.startswith('ok')) and 'declares no flow:' in r and 'encaisser' in r and 'rembourser_paiement' in r
    checks += 1; failures += 0 if ok else 1
    print(('  ok   ' if ok else '  FAIL ') + f'a world missing the compensating flow refuses the compensating step by the flow\'s name: {r[:110]}')
    r = both('f_court.ring', ['check', wf], 'no-world')
    ok = r.startswith('ok') and 'warning NO_WORLD' in r
    checks += 1; failures += 0 if ok else 1
    print(('  ok   ' if ok else '  FAIL ') + f'no world at all is a warning, not a refusal: {r.splitlines()[-1][:90]}')
    r = both('f_court.ring', ['world', wf], 'rows')
    try:
        w = json.loads(r)
        syms = w['symbols']; refs = w['refs']
        ok = (len(syms) == 1 and syms[0]['kind'] == 'process' and syms[0]['name'] == 'paiement'
              and len(refs) == 3 and all(x['kind'] == 'calls' and x['to'].startswith('flow:') for x in refs)
              and w.get('contract') == '1.0')
    except (json.JSONDecodeError, KeyError, TypeError):
        ok = False
    checks += 1; failures += 0 if ok else 1
    print(('  ok   ' if ok else '  FAIL ') + f'the rows a workflow contributes: one process symbol, three calls refs, no flow symbol: {r[:100]}')
    # the seam between two forged letters
    z = both('z_court.ring', ['world', 'tontine.z'], 'z-world')
    with tempfile.TemporaryDirectory() as td:
        try:
            zw = json.loads(z)
            kinds = sorted(set(s['kind'] for s in zw['symbols']))
            names = sorted(s['name'] for s in zw['symbols'] if s['kind'] == 'flow')
            ok = names == ['collect', 'indice'] and 'entity' in kinds and 'norm' in kinds
        except (json.JSONDecodeError, KeyError, TypeError):
            ok = False; zw = None
        checks += 1; failures += 0 if ok else 1
        print(('  ok   ' if ok else '  FAIL ') + f'Z publishes its world: flows {names if ok else "?"}, kinds {kinds if ok else "?"}')
        if zw is not None:
            p = os.path.join(td, 'tontine_world.json')
            with open(p, 'w', encoding='utf-8', newline='') as f:
                json.dump(zw, f)
            cyc = os.path.join('f', 'tontine_cycle.f')
            r = both('f_court.ring', ['check', cyc, p], 'seam-resolved')
            ok = r.startswith('ok') and 'warning' not in r
            checks += 1; failures += 0 if ok else 1
            print(('  ok   ' if ok else '  FAIL ') + f'an F workflow invoking two Z flows resolves against the world Z emitted: {r.splitlines()[0][:60]}')
            r = both('f_court.ring', ['check', cyc, worlds['world']], 'seam-unresolved')
            ok = (not r.startswith('ok')) and 'declares no flow:' in r and 'collect' in r
            checks += 1; failures += 0 if ok else 1
            print(('  ok   ' if ok else '  FAIL ') + f'and against RingFlex\'s world, which declares no collect, the deposit step is refused: {r[:100]}')
            fw = json.loads(both('f_court.ring', ['world', cyc], 'f-rows'))
            merged = zw['symbols'] + fw['symbols']
            ids = set(s['kind'].lower() + ':' + s['name'].lower() for s in merged)
            dangling = [x for x in zw['refs'] + fw['refs'] if x['from'].lower() not in ids or x['to'].lower() not in ids]
            ok = not dangling
            checks += 1; failures += 0 if ok else 1
            print(('  ok   ' if ok else '  FAIL ') + f'the merged rows satisfy C1 3.2: every ref\'s ends are symbols ({len(merged)} symbols, {len(zw["refs"] + fw["refs"])} refs, {len(dangling)} dangling)')
    if PLANT:
        failures += 1
        print('  FAIL the seam -- PLANTED')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} check(s): {ab_diff}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {checks} checks')
    if os.path.exists(RING_OFFICIAL) and os.path.isdir(RINGFLEX):
        p = subprocess.run([RING_OFFICIAL, 'tests/boundary-run.ring'], cwd=RINGFLEX, capture_output=True, timeout=120)
        out = p.stdout.decode('utf-8', 'replace')
        m = re.search(r'(\d+) passed, (\d+) failed', out)
        if m and m.group(2) == '0':
            print(f'  ok   RingFlex\'s own placement gate (official Ring 1.27, read-only): {m.group(1)} passed, 0 failed on its original fixtures')
        else:
            failures += 1
            print(f'  FAIL RingFlex\'s placement gate did not hold: {out[-200:]}')
    else:
        print('  SKIP RingFlex\'s placement gate: official Ring 1.27 is not installed here')
    return failures


# ---- stage 14: the Diagnostic Contract (C2 v1.2.0) on every forged court, judged by the schema and by RingFlex's codes

C2_SCHEMA = r'D:\GitHub\stzzui\doc\diagnostic-contract.schema.json'
C2_CODE = re.compile(r'^[A-Z][A-Z0-9]*([_-][A-Z0-9]+)*$')
C2_CITE = re.compile(r'^(rule|article|right|pattern):[A-Za-z0-9_.-]+$')
C2_LANG = re.compile(r'^[a-z][a-z0-9_]*$')


def c2_scalars_ok(v):
    """C2 2.8, to full depth: no bare true, false or null anywhere."""
    if v is None or isinstance(v, bool):
        return False
    if isinstance(v, dict):
        return all(c2_scalars_ok(x) for x in v.values())
    if isinstance(v, list):
        return all(c2_scalars_ok(x) for x in v)
    return True


def c2_validate(report):
    """The contract's shape, by hand (no jsonschema module here): returns a list of defects."""
    bad = []
    if not isinstance(report, dict) or 'diagnostics' not in report or not isinstance(report['diagnostics'], list):
        return ['the machine form is not one object carrying a diagnostics array']
    if not c2_scalars_ok(report):
        bad.append('a bare true, false or null (2.8)')
    for d in report['diagnostics']:
        if not isinstance(d, dict):
            bad.append('a diagnostic is not an object'); continue
        for k in ('code', 'severity', 'message', 'span', 'cites', 'language'):
            if k not in d:
                bad.append(f'missing {k}')
        if not isinstance(d.get('code'), str) or not C2_CODE.match(d.get('code', '')):
            bad.append(f'code {d.get("code")!r} is not in the format')
        if d.get('severity') not in ('error', 'warning'):
            bad.append(f'severity {d.get("severity")!r} is off the ladder')
        if not isinstance(d.get('message'), str) or not d.get('message'):
            bad.append('an empty message')
        sp = d.get('span')
        if not isinstance(sp, dict) or set(sp) - {'file', 'line', 'col'} or 'file' not in sp or 'line' not in sp:
            bad.append(f'span {sp!r} is not {{file, line[, col]}}')
        else:
            if not isinstance(sp['file'], str) or not sp['file']:
                bad.append('span.file is empty')
            if not isinstance(sp['line'], int) or isinstance(sp['line'], bool) or sp['line'] < 0:
                bad.append(f'span.line {sp["line"]!r} is not an integer >= 0')
        if not isinstance(d.get('cites'), list) or not all(isinstance(c, str) and C2_CITE.match(c) for c in d.get('cites', [])):
            bad.append(f'cites {d.get("cites")!r} are not kind:value in the four kinds')
        if not isinstance(d.get('language'), str) or not C2_LANG.match(d.get('language', '')):
            bad.append(f'language {d.get("language")!r} is not a lowercase identifier')
        if d.get('code') == 'PARSE' and d.get('cites'):
            bad.append('PARSE cites something: a grammar diagnostic enforces no pinned instrument')
    return bad


RF_DIAG = os.path.join(HERE, 'rf_diag.ring')


def stage14():
    """The eleventh rung. Every forged court answers `diagnose <file> [world]`
    in C2 v1.2.0's machine form. Judged three ways: the contract's own shape,
    checked by hand against the schema's rules on every diagnostic every court
    emits over its fixtures; RingFlex's codes -- its court, run live under
    official Ring on its ORIGINAL fixtures and world fixtures through
    rf_diag.ring (read-only), must give the same code, the same cites and the
    same line-or-file-wide as the forged court gives on the re-expressed ones,
    which is what CODE, CODES and CITES in f_v11.haro declare; and the family's
    one consumer, which must be able to tell a clean run from no output."""
    print('stage 14 -- the Diagnostic Contract (C2 v1.2.0): every forged court\'s `diagnose`, judged by the contract\'s shape and by RingFlex\'s own codes, live')
    failures = 0
    # every court this stage asks is re-forged first: a court forged before the
    # forge learned a global is a court the ORACLE refuses (a `$name` first
    # assigned inside a function is that function's local on Ring, R24 at the
    # next read) while rnxc, under Rule A, runs it -- which is how a stale
    # a_court.ring passed on one runtime and failed on the other
    for stzu in (F_STZU, Z_STZU, A_STZU, os.path.join(HERE, 'machine_v03.haro')):
        run_args(RNXC, ['forge.ring', stzu, '.'], HERE)
    ab_diff = []
    def both(court, args, label):
        r = run_args(RNXC, [court] + args, HERE).strip()
        o = run_args(ORACLE, [court] + args, HERE).strip()
        if r != o:
            ab_diff.append(label)
        return r
    # 1. the shape, on every court's fixtures
    reports = {}
    n_diag = 0
    shape_bad = []
    for name in sorted(f for f in os.listdir(F_DIR) if f.endswith('.f')):
        r = both('f_court.ring', ['diagnose', os.path.join('f', name)], 'f:' + name)
        try:
            rep = json.loads(r)
        except json.JSONDecodeError:
            shape_bad.append((name, 'not JSON: ' + r[:80])); continue
        bad = c2_validate(rep)
        if bad:
            shape_bad.append((name, '; '.join(bad)))
        reports[name] = rep
        n_diag += len(rep['diagnostics'])
    # the machine sentence the forged court accepts (stage 4's rule: qemu_hello under the
    # pinned declaration, makeen_box under machine_v03.haro; HF-31)
    machine_sentence = r'D:\GitHub\harobanda\machines\qemu_hello.machine'
    if not court_verdict(RNXC, 'machine_court.ring', machine_sentence)[0]:
        machine_sentence = MAKEEN
    others = [('z_court.ring', 'tontine.z'), ('a_court.ring', os.path.join('a', 'w_in_a.a')), ('machine_court.ring', machine_sentence)]
    for court, f in others:
        r = both(court, ['diagnose', f], court + ':' + os.path.basename(f))
        try:
            rep = json.loads(r)
            bad = c2_validate(rep)
            if rep['diagnostics']:
                bad.append(f'{len(rep["diagnostics"])} diagnostic(s) on a clean sentence')
        except json.JSONDecodeError:
            bad = ['not JSON: ' + r[:80]]
        if bad:
            shape_bad.append((os.path.basename(f), '; '.join(bad)))
    # a refusal of another language, and a cyclic algorithm, carry codes too
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'drop.z')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write('DROP TABLE deposit\n')
        r = both('z_court.ring', ['diagnose', p], 'z:drop')
        try:
            rep = json.loads(r); bad = c2_validate(rep)
            if len(rep['diagnostics']) != 1 or rep['diagnostics'][0]['code'] != 'UNKNOWN_VERB' or rep['diagnostics'][0]['severity'] != 'error':
                bad.append(f'expected one UNKNOWN_VERB error, got {rep["diagnostics"]}')
        except json.JSONDecodeError:
            bad = ['not JSON: ' + r[:80]]
        if bad:
            shape_bad.append(('drop.z', '; '.join(bad)))
        p = os.path.join(td, 'loop.a')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write('DEFINE ALGORITHM loop AS (STEPS [again], RESULT [n]) RATIONALE "x"\nDEFINE COMPUTE bump AS (INTO n, VALUE "n + 1") RATIONALE "x"\nDEFINE BRANCH again AS (WHEN "n < 10", THEN [bump, again]) RATIONALE "x"\n')
        r = both('a_court.ring', ['diagnose', p], 'a:loop')
        try:
            rep = json.loads(r); bad = c2_validate(rep)
            if len(rep['diagnostics']) != 1 or rep['diagnostics'][0]['code'] != 'CYCLE' or rep['diagnostics'][0]['cites'] != ['rule:run']:
                bad.append(f'expected one CYCLE error citing rule:run, got {rep["diagnostics"]}')
        except json.JSONDecodeError:
            bad = ['not JSON: ' + r[:80]]
        if bad:
            shape_bad.append(('loop.a', '; '.join(bad)))
    if shape_bad:
        failures += len(shape_bad)
        for name, why in shape_bad[:6]:
            print(f'  FAIL {name}: {why}')
    print(('  FAIL ' if shape_bad else '  ok   ') + f'the contract\'s shape on {n_diag} diagnostics over {len(reports)} F fixtures and 5 other sentences ({len(shape_bad)} defect(s))')
    # 2. the codes RingFlex gives, from its own court, live
    expect = {}
    for name, rep in reports.items():
        src = open(os.path.join(F_DIR, name), encoding='utf-8').read()
        exp = f_expect(src)
        kind, _, arg = exp.partition(' ')
        if kind == 'refuse':
            expect[name] = arg
        elif kind == 'parse-error':
            stem = name[:-2]
            expect[name] = {'uses-flow': 'FLOW_IS_ZQL', 'invoked-by-flow': 'SEAM_UPWARD', 'step-invoked-by-flow': 'SEAM_UPWARD'}.get(stem, 'PARSE')
        else:
            expect[name] = None
    code_bad = []
    for name, rep in reports.items():
        errs = [d for d in rep['diagnostics'] if d['severity'] == 'error']
        warns = [d for d in rep['diagnostics'] if d['severity'] == 'warning']
        want = expect[name]
        if want is None:
            if errs:
                code_bad.append((name, f'clean, but {errs[0]["code"]}'))
            if any(w['code'] != 'NO_WORLD' or w['span']['line'] != 0 for w in warns):
                code_bad.append((name, f'a warning that is not NO_WORLD at line 0: {warns}'))
        else:
            # a collecting court may state one law more than once (a missing TIMEOUT and a missing
            # ON_TIMEOUT are two seats under C1): every error carries RingFlex's code
            if not errs:
                code_bad.append((name, 'expected an error, got none'))
            elif any(e['code'] != want for e in errs):
                code_bad.append((name, f'codes {sorted(set(e["code"] for e in errs))} where RingFlex says {want}'))
            elif want.startswith('C') and want[1:].isdigit() and errs[0]['cites'] != ['rule:' + want]:
                code_bad.append((name, f'cites {errs[0]["cites"]} where RingFlex cites rule:{want}'))
            elif want in ('FLOW_IS_ZQL', 'SEAM_UPWARD') and errs[0]['cites'] != ['article:placement-3']:
                code_bad.append((name, f'cites {errs[0]["cites"]} where RingFlex cites article:placement-3'))
            elif want == 'PARSE' and errs[0]['cites']:
                code_bad.append((name, f'PARSE cites {errs[0]["cites"]}'))
            elif errs[0]['span']['line'] < 1:
                code_bad.append((name, 'a court refusal at line 0'))
    if code_bad:
        failures += len(code_bad)
        for name, why in code_bad[:6]:
            print(f'  FAIL {name}: {why}')
    print(('  FAIL ' if code_bad else '  ok   ') + f'every F fixture\'s code and cites are RingFlex\'s own, from its EXPECT lines ({len(code_bad)} differ)')
    # the resolution codes against the world fixtures
    wf = os.path.join('f', 'boundary-invokes-flow.f')
    res_bad = []
    for wname, want in (('world', None), ('world-missing-flow', 'UNRESOLVED_FLOW'), ('world-missing-compensating', 'UNRESOLVED_FLOW')):
        r = both('f_court.ring', ['diagnose', wf, os.path.join(RINGFLEX_WORLDS, wname + '.json')], 'diag:' + wname)
        try:
            rep = json.loads(r)
            bad = c2_validate(rep)
            ds = rep['diagnostics']
            if want is None and ds:
                bad.append(f'expected no diagnostic, got {ds}')
            if want and (len(ds) != 1 or ds[0]['code'] != want or ds[0]['cites'] != ['article:placement-3.2'] or ds[0]['span']['line'] < 1):
                bad.append(f'expected one {want} citing article:placement-3.2 on a line, got {ds}')
        except json.JSONDecodeError:
            bad = ['not JSON: ' + r[:80]]
        if bad:
            res_bad.append((wname, '; '.join(bad)))
    r = both('f_court.ring', ['diagnose', wf], 'diag:absent')
    try:
        ds = json.loads(r)['diagnostics']
        if len(ds) != 1 or ds[0]['code'] != 'NO_WORLD' or ds[0]['severity'] != 'warning' or ds[0]['span']['line'] != 0 or ds[0]['cites'] != ['article:placement-3.2']:
            res_bad.append(('absent', f'expected one NO_WORLD warning at line 0 citing article:placement-3.2, got {ds}'))
    except json.JSONDecodeError:
        res_bad.append(('absent', 'not JSON'))
    if res_bad:
        failures += len(res_bad)
        for name, why in res_bad:
            print(f'  FAIL resolution {name}: {why}')
    print(('  FAIL ' if res_bad else '  ok   ') + 'the resolution codes: UNRESOLVED_FLOW citing article:placement-3.2 on the step\'s line, NO_WORLD a warning at line 0, as RingFlex\'s')
    if PLANT:
        failures += 1
        print('  FAIL the envelope -- PLANTED')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} diagnose run(s): {ab_diff[:5]}')
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on every diagnose run')
    # 3. RingFlex's court live: its codes on its originals, compared one by one
    if os.path.exists(RING_OFFICIAL) and os.path.isdir(RINGFLEX):
        p = subprocess.run([RING_OFFICIAL, RF_DIAG], cwd=RINGFLEX, capture_output=True, timeout=120)
        out = p.stdout.decode('utf-8', 'replace')
        live = {}
        for line in out.splitlines():
            if '\t' in line:
                k, _, js = line.partition('\t')
                try:
                    live[k] = json.loads(js)['diagnostics']
                except (json.JSONDecodeError, KeyError):
                    pass
        live_bad = []
        for name, rep in reports.items():
            stem = name[:-2]
            lk = stem + '.wflow'
            if lk not in live:
                continue
            theirs = [d['code'] for d in live[lk]]
            ours = [d['code'] for d in rep['diagnostics'] if d['severity'] == 'error']
            if theirs[:1] != ours[:1]:
                live_bad.append((name, f'RingFlex {theirs[:1]} / forged {ours[:1]}'))
            elif theirs and sorted(live[lk][0]['cites']) != sorted([d for d in rep['diagnostics'] if d['severity'] == 'error'][0]['cites']):
                live_bad.append((name, f'cites RingFlex {live[lk][0]["cites"]} / forged {[d for d in rep["diagnostics"] if d["severity"] == "error"][0]["cites"]}'))
        for wname in ('world', 'world-missing-flow', 'world-missing-compensating', 'absent'):
            if 'resolve:' + wname in live:
                theirs = [(d['code'], d['severity']) for d in live['resolve:' + wname]]
                rr = both('f_court.ring', ['diagnose', wf] + ([os.path.join(RINGFLEX_WORLDS, wname + '.json')] if wname != 'absent' else []), 'live:' + wname)
                ours = [(d['code'], d['severity']) for d in json.loads(rr)['diagnostics']]
                if theirs != ours:
                    live_bad.append(('resolve:' + wname, f'RingFlex {theirs} / forged {ours}'))
        if not live:
            failures += 1
            print(f'  FAIL RingFlex\'s court printed no envelopes: {out[-200:]}')
        elif live_bad:
            failures += len(live_bad)
            for name, why in live_bad[:6]:
                print(f'  FAIL {name}: {why}')
        else:
            print(f'  ok   RingFlex\'s own court, live under official Ring on its {len([k for k in live if k.endswith(".wflow")])} original fixtures and 4 worlds: the same first code, the same cites, the same severities as the forged court on the re-expressed ones')
    else:
        print('  SKIP RingFlex\'s court live: official Ring 1.27 is not installed here')
    return failures


# ---- stage 15: FORMS, principle 7's function-name grammar as data, judged by the forms document and by Softanza's own spellings

STZV_STZU = os.path.join(HERE, 'stzv_v12.haro')
STZV_SENTENCE = os.path.join('stz', 'string.stzv')
FORMS_CASES = os.path.join(HERE, 'v12', 'forms_cases.json')
DOC_NAMES = os.path.join('v12', 'doc_names.txt')
STZ_STRING = r'D:\GitHub\stzlib\libraries\stzlib\base\string\stzString.ring'
# the pinned floor of the live census: how many of stzString's Find*, Replace* and
# Remove* definitions agree with the FORMS stzv_v12.haro declares (measured 2026-10-02)
FORMS_FLOOR = 584


def stzv_run(exe, args):
    return run_args(exe, ['stzv_court.ring'] + args, HERE).strip()


def stage15():
    """The twelfth rung. stzv_v12.haro declares the Softanza vocabulary's
    FORMS -- the fluent, passive and statement forms, the parameter suffixes,
    one meaning per suffix, and the FAMILY declaration that spells a family
    from a base verb and the forms it offers -- and the forge emits a court
    with `family` (the members, generated) and `spellings` (a list of names
    judged). Two judges that are not mine: the forms document's own examples
    (stz-functions-as-linguistic-expressions.md), re-expressed as names with
    the verdict principle 7's rule gives each; and Softanza's shipped
    spellings, every Find*, Replace* and Remove* definition of stzString.ring
    read live from the author's tree (read-only), whose agreement count is
    pinned and whose disagreements are the number the migration measures."""
    print('stage 15 -- FORMS, the function-name grammar as data: stzv_v12.haro -> stzv_court.ring with `family` and `spellings`, judged by the forms document and by stzString\'s own spellings')
    failures = 0
    out_rnx = run_args(RNXC, ['forge.ring', STZV_STZU, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    if not out_rnx.startswith('forged stzv'):
        print('  FAIL the forge did not forge stzv')
        return 1
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')
    os.makedirs(td, exist_ok=True)
    arts = ('stzv_court.ring', 'stzv.gbnf')
    for art in arts:
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', STZV_STZU, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in arts:
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    ab_diff = []
    def both(args, label):
        r = stzv_run(RNXC, args)
        o = stzv_run(ORACLE, args)
        if r != o:
            ab_diff.append(label)
        return r
    r = both(['check', STZV_SENTENCE], 'check')
    if not r.startswith('ok'):
        failures += 1
        print(f'  FAIL string.stzv is refused: {r[:200]}')
    else:
        print(f'  ok   string.stzv is a sentence of stzv: {[l for l in r.splitlines() if l.startswith("count ")]}')
    # a family offering a form the FORMS does not declare is refused, under the FORMS code (C2)
    with tempfile.TemporaryDirectory() as tdir:
        p = os.path.join(tdir, 'bad.stzv')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write('DEFINE FAMILY find AS (BASE "Find", FORMS [cs, deep]) RATIONALE "x"\n')
        r = both(['diagnose', p], 'diagnose:bad')
        try:
            ds = json.loads(r)['diagnostics']
            if len(ds) != 1 or ds[0]['code'] != 'FORMS' or ds[0]['cites'] != ['rule:FORMS'] or 'deep' not in ds[0]['message']:
                failures += 1
                print(f'  FAIL a family offering an undeclared form: expected one FORMS error naming deep, got {ds}')
            else:
                print('  ok   a family offering a form the FORMS does not declare is refused, code FORMS citing rule:FORMS (the menu that types the seat)')
        except (json.JSONDecodeError, KeyError):
            failures += 1
            print(f'  FAIL a family offering an undeclared form: not an envelope: {r[:120]}')
    # the forms document's examples: the families it spells and the verdicts its names get
    doc = json.load(open(FORMS_CASES, encoding='utf-8'))
    assert doc['grammar'] == 'stzv' and doc['version'] == '0.12', 'unexpected forms case file'
    fam = both(['family', STZV_SENTENCE], 'family')
    got_fams = {}
    cur = None
    for line in fam.splitlines():
        if line.startswith('family '):
            cur = line[len('family '):].split(':')[0]
            got_fams[cur] = []
        elif line.startswith('  ') and cur:
            got_fams[cur].append(line.strip())
    fam_bad = 0
    for name, members in doc['families'].items():
        if got_fams.get(name) != members:
            fam_bad += 1
            print(f'  FAIL family {name}: expected {members}, got {got_fams.get(name)}')
    failures += fam_bad
    print(('  FAIL ' if fam_bad else '  ok   ') + f'{len(doc["families"])} families of the forms document generated member for member ({sum(len(m) for m in doc["families"].values())} names)')
    sp = both(['spellings', STZV_SENTENCE, DOC_NAMES], 'spellings:doc')
    verdicts = {}
    for line in sp.splitlines():
        if line.startswith('agree ') or line.startswith('disagree '):
            kind, _, rest = line.partition(' ')
            nm = rest.split(':')[0].split(' ')[0]
            verdicts[nm] = (kind, line)
    sp_bad = 0
    n_cases = 0
    for case in doc['spellings']:
        n_cases += 1
        got = verdicts.get(case['name'])
        if got is None:
            sp_bad += 1; print(f'  FAIL {case["name"]}: no verdict'); continue
        if got[0] != case['verdict'] or case.get('contains', '') not in got[1]:
            sp_bad += 1; print(f'  FAIL {case["name"]}: expected {case["verdict"]} containing {case.get("contains", "")!r}, got: {got[1]}')
    if PLANT:
        sp_bad += 1
        print('  FAIL RemoveFFQ -- PLANTED')
    failures += sp_bad
    print(('  FAIL ' if sp_bad else '  ok   ') + f'{n_cases} names of the forms document judged as principle 7 judges them ({sp_bad} differ)')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} run(s): {ab_diff}')
    else:
        print('  ok   rnxc and the oracle print the same bytes on every family and spellings run')
    # the live census: Softanza's own spellings, read-only
    if not os.path.exists(STZ_STRING):
        print('  SKIP the live census: stzString.ring is not at its path')
        return failures
    src = open(STZ_STRING, encoding='utf-8', errors='replace').read()
    names = sorted(set(re.findall(r'^\s*def\s+((?:Find|Replace|Remove)[A-Za-z0-9_]*)', src, re.M | re.I)))
    names_path = os.path.join(ROOT, 'runtime', 'stz_names.txt')
    with open(names_path, 'w', encoding='utf-8', newline='') as fh:
        fh.write('\n'.join(names) + '\n')
    r = stzv_run(RNXC, ['spellings', STZV_SENTENCE, names_path])
    o = stzv_run(ORACLE, ['spellings', STZV_SENTENCE, names_path])
    summary = [l for l in r.splitlines() if l.startswith('spellings:')]
    m = re.match(r'spellings: (\d+) agree, (\d+) disagree of (\d+); (\d+) declared members missing', summary[0]) if summary else None
    if r != o:
        failures += 1
        print('  FAIL rnxc and the oracle differ on the live census')
    if not m:
        failures += 1
        print(f'  FAIL the census printed no summary: {r[-200:]}')
    else:
        agree, disagree, total, missing = (int(x) for x in m.groups())
        dis = [l for l in r.splitlines() if l.startswith('disagree ')]
        print(f'  {len(names)} definitions of stzString.ring (Find*, Replace*, Remove*), read-only: {agree} agree with the FORMS, {disagree} disagree, {missing} declared members missing')
        for l in dis[:8]:
            print('    ' + l[:150])
        if len(dis) > 8:
            print(f'    ... and {len(dis) - 8} more')
        if FORMS_FLOOR and agree < FORMS_FLOOR:
            failures += 1
            print(f'  FAIL {agree} agree, under the pinned floor of {FORMS_FLOOR}')
        elif FORMS_FLOOR:
            print(f'  ok   {agree} agree, at or above the pinned floor of {FORMS_FLOOR}; the same bytes on both runtimes')
    return failures


# ---- stage 16: NARRATE, the court's voice, judged by the StzNarration law and stzn's honesty guard

NARR_CASES = os.path.join(HERE, 'v13', 'narration_cases.json')
DEF_RE = re.compile(r'^DEFINE\s+(\w+)\s+(\w+)\s+AS\s*\((.*)\)\s*RATIONALE\s+"(.*)"\s*$')


def narr_run(exe, args):
    return run_args(exe, ['f_court.ring'] + args, HERE).strip()


def read_definitions(path):
    """The sentence read the way a person reads it, by Python, never by the court:
    (kind, name, body, rationale) for every DEFINE statement, which may span
    lines; a line that begins with -- is a comment and is skipped, one that
    merely contains -- inside a string is not."""
    stmts = []
    cur = None
    for line in open(path, encoding='utf-8').read().splitlines():
        t = line.strip()
        if t.startswith('--'):
            continue
        if t.startswith('DEFINE '):
            if cur is not None:
                stmts.append(cur)
            cur = t
        elif cur is not None and t:
            cur += ' ' + t
    if cur is not None:
        stmts.append(cur)
    out = []
    for st in stmts:
        m = re.match(r'DEFINE\s+(\w+)\s+(\w+)\s+AS\s*\(', st)
        k = st.rfind('RATIONALE')
        if not m or k < 0:
            continue
        body = st[m.end():st.rfind(')', 0, k)]
        q = st[k:]
        rationale = q[q.index('"') + 1:q.rindex('"')]
        out.append((m.group(1), m.group(2), body, rationale))
    return out


def stage16():
    """The thirteenth rung. f_v13.haro gives the F court a voice -- a template
    per declaration kind, an opening, an ending, a refusal -- and `narrate
    <file>` answers a sentence back in it. The judges are the estate's laws,
    read in Python by code that never asks the court what it said: the
    StzNarration law (a narration is a rendering of a real run, never stored,
    the plain-text sentence the document: so `narrate` writes no file, and what
    it prints is not a sentence of the language -- never parsed back) and
    stzn v0's honesty guard (a narration never alters a value it shows: every
    name, every rationale, every seat value of every declaration appears in it
    verbatim, in order). Plus one hand-written narration, composed before the
    court, and a refusal narrated with the code and the line the envelope of
    v0.11 gives the same verdict."""
    print('stage 16 -- NARRATE, the court\'s voice: f_v13.haro -> `narrate`, judged by the StzNarration law and stzn\'s honesty guard, read by Python')
    failures = 0
    out_rnx = run_args(RNXC, ['forge.ring', F_STZU, '.'], HERE).strip()
    print('  rnxc  :', out_rnx.splitlines()[0] if out_rnx else 'NO OUTPUT')
    if not out_rnx.startswith('forged f'):
        print('  FAIL the forge did not forge F')
        return 1
    td = os.path.join(ROOT, 'runtime', 'haro-forge-oracle')
    os.makedirs(td, exist_ok=True)
    arts = ('f_court.ring', 'f.gbnf')
    for art in arts:
        if os.path.exists(os.path.join(td, art)):
            os.remove(os.path.join(td, art))
    out_or = run_args(ORACLE, ['forge.ring', F_STZU, '../../runtime/haro-forge-oracle'], HERE).strip()
    print('  oracle:', out_or.splitlines()[0] if out_or else 'NO OUTPUT')
    for art in arts:
        a = open(os.path.join(HERE, art), 'rb').read()
        b = open(os.path.join(td, art), 'rb').read() if os.path.exists(os.path.join(td, art)) else b''
        if a != b:
            failures += 1
            print(f'  FAIL {art} differs between the two runtimes ({len(a)} vs {len(b)} bytes)')
        else:
            print(f'  ok   {art}: {len(a)} bytes, byte-identical on both runtimes')
    ab_diff = []
    def both(args, label):
        r = narr_run(RNXC, args)
        o = narr_run(ORACLE, args)
        if r != o:
            ab_diff.append(label)
        return r
    # 1. the hand-written narration of the smallest lawful workflow
    doc = json.load(open(NARR_CASES, encoding='utf-8'))
    r = both(['narrate', doc['sentence']], 'hand')
    want = '\n'.join(doc['narration'])
    if r != want:
        failures += 1
        print('  FAIL the hand-written narration of ' + doc['sentence'])
        for a, b in zip(r.splitlines() + [''] * 8, doc['narration'] + [''] * 8):
            if a != b:
                print('    court :', a[:150]); print('    hand  :', b[:150]); break
    else:
        print(f'  ok   {doc["sentence"]} narrated as composed by hand before the court ({len(doc["narration"])} lines)')
    # 2. every F sentence: completeness and honesty for the lawful, the envelope's own verdict for the refused
    complete_bad = []
    refused_bad = []
    n_clean = n_refused = n_values = 0
    for name in sorted(f for f in os.listdir(F_DIR) if f.endswith('.f')):
        path = os.path.join('f', name)
        nar = both(['narrate', path], 'narrate:' + name)
        env = json.loads(both(['diagnose', path], 'diagnose:' + name))['diagnostics']
        errs = [d for d in env if d['severity'] == 'error']
        if errs:
            n_refused += 1
            d = errs[0]
            want_line = f'I stopped at line {d["span"]["line"]}: {d["message"]} ({d["code"]})'
            if nar != want_line:
                refused_bad.append((name, f'narrated {nar[:120]!r}, the envelope says {want_line[:120]!r}'))
            continue
        n_clean += 1
        defs = read_definitions(os.path.join(HERE, path))
        lines = nar.splitlines()
        if len(lines) != len(defs) + 2:
            complete_bad.append((name, f'{len(lines)} lines for {len(defs)} declarations (want {len(defs) + 2})')); continue
        if f'{len(defs)} declarations' not in lines[0] or f'{len(defs)} declarations' not in lines[-1]:
            complete_bad.append((name, 'the count is not the number of DEFINE lines'))
        for (kind, dname, body, rationale), line in zip(defs, lines[1:-1]):
            if dname not in line:
                complete_bad.append((name, f'{dname} is not named in {line[:80]!r}')); break
            if rationale not in line:
                complete_bad.append((name, f'the rationale of {dname} is not verbatim: {rationale[:60]!r}')); break
            # every bare or quoted scalar the line's own seats hold, verbatim, for the seats the voice speaks
            for key, val in re.findall(r'\b(INVOKES|ON_COMMITTED|ON_REJECTED|ON_HELD|ROLE|OUTCOME|CALENDAR|LOCALE|ZQL)\s+("[^"]*"|[\w.]+)', body):
                v = val.strip('"')
                n_values += 1
                if v not in line:
                    complete_bad.append((name, f'{dname}: {key} {v!r} is missing or altered in {line[:90]!r}')); break
    failures += len(complete_bad) + len(refused_bad)
    for name, why in (complete_bad + refused_bad)[:6]:
        print(f'  FAIL {name}: {why}')
    print(('  FAIL ' if complete_bad else '  ok   ') + f'honesty: {n_clean} lawful sentences narrated whole -- every declaration named, every rationale and {n_values} seat values verbatim, in order, the count right ({len(complete_bad)} defect(s))')
    print(('  FAIL ' if refused_bad else '  ok   ') + f'{n_refused} refused sentences narrated as the one line the envelope of v0.11 gives the same verdict: its line, its message, its code ({len(refused_bad)} differ)')
    # 3. never parsed back: the narration of a sentence is not a sentence
    with tempfile.TemporaryDirectory() as tdir:
        nar = both(['narrate', os.path.join('f', 'minimal-clean.f')], 'back')
        p = os.path.join(tdir, 'back.f')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(nar + '\n')
        r = narr_run(RNXC, ['check', p])
        if r.startswith('ok'):
            failures += 1
            print('  FAIL a narration was accepted as a sentence: the court reads one back')
        else:
            print('  ok   the narration is not a sentence of the language: the court refuses it, and has no verb that reads one back')
    # 4. never stored: narrating writes nothing anywhere the court can reach
    before = sorted(os.listdir(HERE)) + sorted(os.listdir(os.path.join(HERE, 'f')))
    both(['narrate', os.path.join('f', 'commande-fournisseur.f')], 'stored')
    after = sorted(os.listdir(HERE)) + sorted(os.listdir(os.path.join(HERE, 'f')))
    if before != after:
        failures += 1
        print('  FAIL narrating changed the folder: a narration is stored')
    else:
        print('  ok   narrating writes no file: the narration is a rendering of a run, never stored')
    # 5. a language that declares no voice has none (re-forged first: a court forged before the
    # forge learned a global is a court the oracle refuses and rnxc runs, HF-61). z had been the
    # voiceless one until the sixteenth rung gave it a voice that tells a question; the machine
    # language declares none
    run_args(RNXC, ['forge.ring', os.path.join(HERE, 'machine_v03.haro'), '.'], HERE)
    r = run_args(RNXC, ['machine_court.ring', 'narrate', 'x'], HERE).strip()
    o = run_args(ORACLE, ['machine_court.ring', 'narrate', 'x'], HERE).strip()
    if r != o:
        ab_diff.append('machine:narrate')
    if 'declares no NARRATE' not in r:
        failures += 1
        print(f'  FAIL a court with no NARRATE narrated: {r[:120]}')
    else:
        print('  ok   a language that declares no NARRATE has no voice: the machine language refuses to narrate')
    if PLANT:
        failures += 1
        print('  FAIL the voice -- PLANTED')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} run(s): {ab_diff[:5]}')
    else:
        print('  ok   rnxc and the oracle print the same bytes on every narrate and diagnose run')
    return failures


# ---- stage 17: a court that collects, judged by RingFlex's own Check() pass live

MULTI_DIR = os.path.join(HERE, 'v14', 'multi')
MULTI_CASES = os.path.join(HERE, 'v14', 'multi_cases.json')
RF_MULTI = os.path.join(HERE, 'rf_multi.ring')
WFLOW_START = re.compile(r'^[A-Z_]+\s+(\w+)')
F_START = re.compile(r'^DEFINE\s+\w+\s+(\w+)')
NO_DECL_CODES = ('PARSE', 'FLOW_IS_ZQL', 'SEAM_UPWARD')


def decl_starts(path, notation):
    out = []
    rx = F_START if notation == 'f' else WFLOW_START
    for i, line in enumerate(open(path, encoding='utf-8').read().splitlines(), 1):
        m = rx.match(line)
        if m:
            out.append((i, m.group(1)))
    return out


def decl_at(starts, line):
    name = None
    for ln, nm in starts:
        if ln <= line:
            name = nm
    return name


def pairs_of(diags, starts):
    """(code, declaration) for each error; a grammar refusal names no declaration -- the two
    notations spell the same sentence on different lines, so only its code is compared."""
    out = []
    for d in diags:
        if d['severity'] != 'error':
            continue
        out.append((d['code'], None if d['code'] in NO_DECL_CODES else decl_at(starts, d['span']['line'])))
    return out


def rf_findings(paths, script):
    p = subprocess.run([RING_OFFICIAL, script] + paths, cwd=RINGFLEX, capture_output=True, timeout=180)
    live = {}
    for line in p.stdout.decode('utf-8', 'replace').splitlines():
        if '\t' in line:
            k, _, js = line.partition('\t')
            try:
                live[os.path.basename(k)] = json.loads(js)['diagnostics']
            except (json.JSONDecodeError, KeyError):
                pass
    return live


def stage17():
    """The fourteenth rung. `diagnose` goes on past a refusal to the next element of
    every pass and answers every finding, in the order of the file; `check` still
    stops at the first. The judge is RingFlex's own court: its Check() pass collects
    every finding, run live under official Ring (read-only) on the .wflow twin of five
    sentences with several defects written, with my predictions, BEFORE the court, and on
    its 24 original fixtures. The forged court must report every (code, declaration) pair
    RingFlex reports and no pair RingFlex does not; it may say a pair more often (a missing
    TIMEOUT and a missing ON_TIMEOUT are two seats under one law)."""
    print('stage 17 -- a court that collects: `diagnose` answers every finding, judged by RingFlex\'s own Check() pass, live')
    failures = 0
    run_args(RNXC, ['forge.ring', F_STZU, '.'], HERE)
    ab_diff = []
    def both(args, label):
        r = narr_run(RNXC, args)
        o = narr_run(ORACLE, args)
        if r != o:
            ab_diff.append(label)
        return r
    if not (os.path.exists(RING_OFFICIAL) and os.path.isdir(RINGFLEX)):
        print('  SKIP RingFlex\'s court live: official Ring 1.27 is not installed here')
        return 0
    doc = json.load(open(MULTI_CASES, encoding='utf-8'))
    wpaths = [os.path.join(MULTI_DIR, c['name'] + '.wflow') for c in doc['cases']]
    live = rf_findings(wpaths, RF_MULTI)
    miss = [c['name'] for c in doc['cases'] if c['name'] + '.wflow' not in live]
    if miss:
        print(f'  FAIL RingFlex printed nothing for {miss}')
        return 1
    # 1. the hand-written predictions against RingFlex, then the forged court against RingFlex
    pred_bad = []
    forged_bad = []
    n_pairs = n_more = 0
    for c in doc['cases']:
        name = c['name']
        wstarts = decl_starts(os.path.join(MULTI_DIR, name + '.wflow'), 'wflow')
        fstarts = decl_starts(os.path.join(MULTI_DIR, name + '.f'), 'f')
        rf = sorted((a, b or '') for a, b in pairs_of(live[name + '.wflow'], wstarts))
        hand = sorted((code, d) for code, ds in c['predict'].items() for d in ds)
        if rf != hand:
            pred_bad.append((name, f'hand {hand} / RingFlex {rf}'))
        fd = json.loads(both(['diagnose', os.path.join('v14', 'multi', name + '.f')], 'multi:' + name))['diagnostics']
        fg = sorted((a, b or '') for a, b in pairs_of(fd, fstarts))
        if set(fg) != set(rf):
            forged_bad.append((name, f'forged {sorted(set(fg))} / RingFlex {sorted(set(rf))}'))
        for pr in set(rf):
            n_pairs += 1
            want_n = 1 if pr[0] in doc.get('stated_once', []) else rf.count(pr)
            if fg.count(pr) < want_n:
                forged_bad.append((name, f'{pr} said {fg.count(pr)} time(s), RingFlex says {rf.count(pr)}'))
            elif fg.count(pr) > want_n:
                n_more += 1
    # the one prediction RingFlex corrected is recorded in the case file itself
    corrected = [c['name'] for c in doc['cases'] if c.get('missed')]
    if pred_bad:
        failures += len(pred_bad)
        for name, why in pred_bad:
            print(f'  FAIL prediction {name}: {why}')
    print(('  FAIL ' if pred_bad else '  ok   ') + f'the hand-written predictions are RingFlex\'s findings ({len(doc["cases"])} sentences; {len(corrected)} corrected after RingFlex spoke: {", ".join(corrected) or "none"})')
    if forged_bad:
        failures += len(forged_bad)
        for name, why in forged_bad[:6]:
            print(f'  FAIL {name}: {why}')
    print(('  FAIL ' if forged_bad else '  ok   ') + f'the forged court reports every (code, declaration) pair RingFlex reports and none it does not: {n_pairs} pairs over {len(doc["cases"])} sentences, {n_more} said more often')
    # 2. no cascade where RingFlex finds one thing: the 24 originals, every finding, not only the first
    names = sorted(f[:-len('.wflow')] for f in os.listdir(os.path.join(RINGFLEX, 'fixtures')) if f.endswith('.wflow'))
    wpaths = [os.path.join(RINGFLEX, 'fixtures', n + '.wflow') for n in names]
    live2 = rf_findings(wpaths, RF_MULTI)
    orig_bad = []
    n_orig = 0
    for n in names:
        fpath = os.path.join(F_DIR, n + '.f')
        if not os.path.exists(fpath) or n + '.wflow' not in live2:
            continue
        n_orig += 1
        rf = sorted((a, b or '') for a, b in pairs_of(live2[n + '.wflow'], decl_starts(os.path.join(RINGFLEX, 'fixtures', n + '.wflow'), 'wflow')))
        fd = json.loads(both(['diagnose', os.path.join('f', n + '.f')], 'orig:' + n))['diagnostics']
        fg = sorted((a, b or '') for a, b in pairs_of(fd, decl_starts(fpath, 'f')))
        if set(fg) != set(rf):
            orig_bad.append((n, f'forged {sorted(set(fg))} / RingFlex {sorted(set(rf))}'))
    if orig_bad:
        failures += len(orig_bad)
        for name, why in orig_bad[:6]:
            print(f'  FAIL {name}: {why}')
    print(('  FAIL ' if orig_bad else '  ok   ') + f'collecting adds nothing where RingFlex finds one thing: all {n_orig} original fixtures, every finding, the same (code, declaration) pairs ({len(orig_bad)} differ)')
    # 3. `check` is unchanged: one line, the first refusal, which is one of the findings
    r = both(['check', os.path.join('v14', 'multi', 'three_laws.f')], 'check')
    fd = json.loads(both(['diagnose', os.path.join('v14', 'multi', 'three_laws.f')], 'check-d'))['diagnostics']
    if len(r.splitlines()) != 1 or not any(d['message'] in r for d in fd):
        failures += 1
        print(f'  FAIL check on a sentence with several defects is not one line, one of the findings: {r[:140]!r}')
    else:
        print('  ok   check still stops at the first refusal, one line, to the byte: it is one of the findings diagnose answers')
    # 4. a sentence that does not parse has nothing to collect from: one finding, the parse's
    fd = json.loads(both(['diagnose', os.path.join('f', 'uses-flow.f')], 'parse'))['diagnostics']
    if len(fd) != 1 or fd[0]['code'] != 'FLOW_IS_ZQL':
        failures += 1
        print(f'  FAIL a sentence that does not parse answered {[d["code"] for d in fd]}')
    else:
        print('  ok   a sentence that does not parse is one finding, the parse\'s: there is no declaration to judge past it')
    # 5. a sentence with no defect is still the empty array
    fd = json.loads(both(['diagnose', os.path.join('f', 'minimal-clean.f')], 'clean'))['diagnostics']
    if [d for d in fd if d['severity'] == 'error']:
        failures += 1
        print('  FAIL a clean sentence answered an error')
    else:
        print('  ok   a clean sentence has no error')
    if PLANT:
        failures += 1
        print('  FAIL the collection -- PLANTED')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} run(s): {ab_diff[:5]}')
    else:
        print('  ok   rnxc and the oracle print the same bytes on every diagnose and check run')
    return failures


# ---- stage 18: the meta-court that collects, judged by its own first refusal, one defect at a time

META_CASES = os.path.join(HERE, 'v15', 'multi_cases.json')
LAW_BASES = ['f_v13.haro', 'z_v10.haro', 'a_v09.haro', 'machine_v03.haro', 'stzv_v12.haro', 'w_v05.haro', 'fleet_v04.haro']
# the seeds are chosen so that every protection of the court is load-bearing under THIS sampling
# (each was switched off in turn and the stage failed); HARO_LAW_SEEDS / HARO_LAW_PER only widen it
LAW_SEEDS = tuple(int(x) for x in os.environ.get('HARO_LAW_SEEDS', '1').split(','))
LAW_PER = int(os.environ.get('HARO_LAW_PER', '8'))
# floors on how much the law must actually check: a stage that checks nothing passes (HF-64's "all 0")
LAW_SINGLES_FLOOR = 165
LAW_COMBOS_FLOOR = 100
META_LINE = re.compile(r'^haro \(line (\d+)\): (.*)$')


def meta_run(exe, path, mode=None):
    out = run_args(exe, ['haro.ring', path] + ([mode] if mode else []), HERE)
    return [l for l in out.split('\n') if l != '']


def stage18():
    """The fifteenth rung. The meta-court gains `haro.ring <file> all`: every defect of a
    language declaration, one line each, in the order of the file, where it gave the first.
    The judge is the court's own first refusal. A defect put into a sound declaration by
    haro_mutate.py is refused alone in default mode; the court that collects must give
    exactly that one line for it (nothing echoing it), and for several defects on different
    declarations exactly the union of their single lines (nothing hidden behind another).
    Defects found while the declarations are read, registered and have their types resolved
    come before the relations among declarations are judged (a barrier, as RingFlex's parser
    stands before its Check()), so when any of the first two kinds is present the relational
    ones wait. Before that, five files whose findings were written by hand."""
    print('stage 18 -- the meta-court that collects: `haro.ring <file> all`, judged by its own first refusal one defect at a time, and by findings written by hand')
    failures = 0
    ab_diff = []
    def both(path, mode):
        r = meta_run(RNXC, path, mode)
        o = meta_run(ORACLE, path, mode)
        if r != o:
            ab_diff.append(os.path.basename(path) + ':' + str(mode))
        return r
    # 1. the hand-written cases
    doc = json.load(open(META_CASES, encoding='utf-8'))
    hand_bad = 0
    for c in doc['cases']:
        path = os.path.join('v15', c['file'])
        got = both(path, 'all')
        if not c['findings']:
            want = meta_run(RNXC, path, None)
            if got != want or not got or got[0] != 'ok':
                hand_bad += 1
                print(f'  FAIL {c["file"]}: a clean declaration must print what the default prints')
            continue
        parsed = [META_LINE.match(l) for l in got]
        if len(got) != len(c['findings']) or not all(parsed):
            hand_bad += 1
            print(f'  FAIL {c["file"]}: {len(got)} line(s), {len(c["findings"])} written by hand: {got[:6]}')
            continue
        for m, w in zip(parsed, c['findings']):
            if int(m.group(1)) != w['line'] or w['contains'] not in m.group(2):
                hand_bad += 1
                print(f'  FAIL {c["file"]}: line {m.group(1)} {m.group(2)[:70]!r}, written by hand: line {w["line"]} containing {w["contains"]!r}')
                break
    failures += hand_bad
    print(('  FAIL ' if hand_bad else '  ok   ') + f'{len(doc["cases"])} files whose findings were written by hand: the same findings on the same lines ({hand_bad} differ)')
    # 2. the union law, on the real declarations of the letters
    import random, haro_mutate as hm
    mut = os.path.join(HERE, 'zz_mut.haro')
    n_single = n_combo = n_clean = 0
    law_bad = []
    try:
        for seed in LAW_SEEDS:
            rng = random.Random(seed)
            for base in LAW_BASES:
                text = open(os.path.join(HERE, base), encoding='utf-8', newline='').read()
                head, stmts = hm.split_statements(text)
                elig = hm.eligible(head, stmts, text)
                if seed == LAW_SEEDS[0]:
                    n_clean += 1
                    if both(os.path.join(HERE, base), 'all') != meta_run(RNXC, os.path.join(HERE, base), None):
                        law_bad.append((base, 'a sound declaration: all differs from the default'))
                pick = []
                for op in ('clause', 'rationale', 'dup', 'dangle', 'on'):
                    cands = [e for e in elig if e['op'] == op]
                    rng.shuffle(cands)
                    pick += cands[:LAW_PER]
                singles = {}
                for m in pick:
                    mt = hm.apply(text, [m])
                    if mt is None:
                        continue
                    with open(mut, 'w', encoding='utf-8', newline='') as fh:
                        fh.write(mt)
                    d = meta_run(RNXC, mut, None)
                    a = both(mut, 'all')
                    singles[(m['op'], m['at'])] = (m, d)
                    n_single += 1
                    if not (len(d) == 1 and a == d):
                        law_bad.append((base, f'{m["op"]} at {m["at"]} alone: default {d[:1]}, all gave {len(a)} line(s)'))
                keys = list(singles)
                for size in (2, 3, 4):
                    for _ in range(LAW_PER):
                        if len(keys) < size:
                            break
                        ch = rng.sample(keys, size)
                        muts = [singles[k][0] for k in ch]
                        mt = hm.apply(text, muts)
                        if mt is None:
                            continue
                        with open(mut, 'w', encoding='utf-8', newline='') as fh:
                            fh.write(mt)
                        lo = min(hm.STAGE[singles[k][0]['op']] for k in ch)
                        want = sorted(l for k in ch for l in singles[k][1] if hm.STAGE[singles[k][0]['op']] <= 2 or lo == 3)
                        got = sorted(both(mut, 'all'))
                        n_combo += 1
                        if got != want:
                            law_bad.append((base, f'{[(k[0], k[1]) for k in ch]}: wanted {len(want)} line(s), got {len(got)}'))
    finally:
        try:
            os.remove(mut)
        except OSError:
            pass
    failures += len(law_bad)
    for base, why in law_bad[:6]:
        print(f'  FAIL {base}: {why}')
    print(('  FAIL ' if law_bad else '  ok   ') + f'the union law: {n_clean} sound declarations print what the default prints; {n_single} single defects each give exactly their own line; {n_combo} combinations of two to four give exactly the union ({len(law_bad)} differ)')
    if n_single < LAW_SINGLES_FLOOR or n_combo < LAW_COMBOS_FLOOR:
        failures += 1
        print(f'  FAIL the law checked {n_single} single(s) and {n_combo} combination(s), under the pinned floors of {LAW_SINGLES_FLOOR} and {LAW_COMBOS_FLOOR}')
    elif LAW_SINGLES_FLOOR:
        print(f'  ok   at or above the pinned floors of {LAW_SINGLES_FLOOR} single(s) and {LAW_COMBOS_FLOOR} combination(s)')
    if PLANT:
        failures += 1
        print('  FAIL the meta-court collection -- PLANTED')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} run(s): {ab_diff[:5]}')
    else:
        print('  ok   rnxc and the oracle print the same bytes on every collecting run')
    return failures


# ---- stage 19: NARRATE tells a run and a question, judged by laws Python reads out of the declarations

RUN_CASES16 = os.path.join(HERE, 'v16', 'run_cases.json')
A_TELLS = {
    'run': 'Running {algorithm} on {record}.',
    'compute': '{name}: {into} is now {value}.',
    'collect': '{name}: {value} added to {into}.',
    'group': '{name}: {value} filed under {key} in {into}.',
    'branch': '{name}: when {when} the {taken} steps are taken.',
    'iterate': '{name}: for each of the {count} items of {over}, as {as}:',
    'result': '{algorithm} answers {result}.',
}
Z_TELLS = {
    'ask': 'Asking {from}: {question}',
    'matched': '{count} of the {total} rows match.',
    'ordered': 'Ordered by {field} {direction}.',
    'cut': 'Only the first {limit} are kept.',
    'answer': 'The answer is {count} row(s): {rows}',
}
A16_RUNS_FLOOR = 30
A16_REBUILT_FLOOR = 31
Z16_ASKS_FLOOR = 22
# a LIMIT above what matched cuts nothing, so a question with one has the answer of the same question
# without it -- which zing already gave: (the question, the fixture case whose answer it shares)
Q16_UNCUT = [('SELECT * FROM collect LIMIT 99', 'q01'), ('SELECT * FROM collect WHERE round = 1 LIMIT 99', 'q02'),
             ('SELECT * FROM collect ORDER BY amount LIMIT 10', 'q05')]


def read_tells(path):
    """The voice as the declaration spells it, read by Python: key -> template."""
    text = open(path, encoding='utf-8').read()
    m = re.search(r'TELLS \[\n(.*?)\n  \],', text, re.S)
    return dict(re.findall(r'(\w+): "([^"]*)"', m.group(1))) if m else {}


def step_defs(path):
    """name -> the step's seats, read by Python from the sentence's own text."""
    out = {}
    for kind, name, body, _ in read_definitions(path):
        def one(rx):
            m = re.search(rx, body)
            return m.group(1) if m else None

        def lst(key):
            m = re.search(r'\b' + key + r'\s*\[([^\]]*)\]', body)
            return [x.strip() for x in m.group(1).split(',') if x.strip()] if m else None
        out[name] = {'kind': kind, 'into': one(r'\bINTO\s+(\w+)'), 'when': one(r'\bWHEN\s+"([^"]*)"'),
                     'over': one(r'\bOVER\s+(\w+)'), 'as': one(r'\bAS\s+(\w+)'), 'then': lst('THEN'),
                     'else': lst('ELSE'), 'do': lst('DO'), 'steps': lst('STEPS'), 'result': lst('RESULT')}
    return out


class _Cut(Exception):
    pass


class _Lost(Exception):
    pass


def judge_run(lines, defs, alg, rec, expected, refusal):
    """The laws of a told run. The narration is parsed into the tree the declarations
    and the record say it must be -- never by asking the court what it meant -- and the
    values it shows are rebuilt and compared with the answer the stz and zing fixtures
    give. Returns (problems, number of names rebuilt from what was told)."""
    bad = []
    rebuilt_n = 0
    if len(lines) < 2:
        return [f'{len(lines)} line(s) told'], 0
    m = re.match(r'^Running (\w+) on (.*)\.$', lines[0])
    if not m or m.group(1) != alg:
        return [f'the first line does not announce {alg}: {lines[0][:80]!r}'], 0
    try:
        if json.loads(m.group(2)) != rec:
            bad.append('the record told is not the record given')
    except ValueError:
        bad.append('the record told is not JSON')
    last = lines[-1]
    body = lines[1:-1]
    if refusal is not None and (not last.startswith('I stopped: ') or refusal not in last):
        bad.append(f'a refused run does not end on the refusal: {last[:100]!r}')
    pos = [0]
    told = {'collect': {}, 'compute': {}, 'group': {}}

    def take(depth, name):
        if pos[0] >= len(body):
            raise _Cut()
        line = body[pos[0]]
        pos[0] += 1
        ind = '  ' * depth
        if not line.startswith(ind) or line[len(ind):len(ind) + 1] == ' ':
            bad.append(f'{name} is told at the wrong depth: {line[:70]!r} (want {depth})')
            raise _Lost()
        t = line[len(ind):]
        if not t.startswith(name + ': '):
            bad.append(f'{name} is the declared step here and the narration tells {t[:60]!r}')
            raise _Lost()
        return t[len(name) + 2:]

    def is_(rx, t, name):
        m2 = re.match(rx, t)
        if not m2:
            bad.append(f'{name} is not told in the voice: {t[:70]!r}')
            raise _Lost()
        return m2

    def walk(names, depth, env):
        for name in names:
            d = defs[name]
            k = d['kind']
            t = take(depth, name)
            if k == 'COMPUTE':
                m2 = is_(r'^(\w+) is now (.*)\.$', t, name)
                if m2.group(1) != d['into']:
                    bad.append(f'{name} computes into {d["into"]} and the narration says {m2.group(1)}')
                told['compute'].setdefault(d['into'], []).append(json.loads(m2.group(2)))
            elif k == 'COLLECT':
                m2 = is_(r'^(.*) added to (\w+)\.$', t, name)
                if m2.group(2) != d['into']:
                    bad.append(f'{name} collects into {d["into"]} and the narration says {m2.group(2)}')
                told['collect'].setdefault(d['into'], []).append(json.loads(m2.group(1)))
            elif k == 'GROUP':
                m2 = is_(r'^(.*) filed under (.*) in (\w+)\.$', t, name)
                if m2.group(3) != d['into']:
                    bad.append(f'{name} groups into {d["into"]} and the narration says {m2.group(3)}')
                gl = told['group'].setdefault(d['into'], [])
                key, val = m2.group(2), json.loads(m2.group(1))
                for pair in gl:
                    if pair[0] == key:
                        pair[1].append(val)
                        break
                else:
                    gl.append([key, [val]])
            elif k == 'BRANCH':
                m2 = is_(r'^when (.*) the (then|else) steps are taken\.$', t, name)
                if m2.group(1) != d['when']:
                    bad.append(f'{name} is declared WHEN {d["when"]!r} and the narration says {m2.group(1)!r}')
                walk(d[m2.group(2)] or [], depth + 1, env)
            elif k == 'ITERATE':
                m2 = is_(r'^for each of the (\d+) items of (\w+), as (\w+):$', t, name)
                n = int(m2.group(1))
                if m2.group(2) != d['over'] or m2.group(3) != d['as']:
                    bad.append(f'{name} is declared OVER {d["over"]} AS {d["as"]} and the narration says {m2.group(2)}, {m2.group(3)}')
                lst = env.get(d['over'])
                if not isinstance(lst, list):
                    bad.append(f'{name} iterates over {d["over"]}, which holds no list here')
                    raise _Lost()
                if n != len(lst):
                    bad.append(f'{name}: the narration walks {n} item(s) of a list of {len(lst)}')
                    raise _Lost()
                for p in range(n):
                    walk(d['do'] or [], depth + 1, dict(env, **{d['as']: lst[p]}))

    ended = True
    try:
        walk(defs[alg]['steps'], 0, dict(rec))
        if pos[0] != len(body):
            bad.append(f'{len(body) - pos[0]} line(s) left over after the declared steps')
    except _Cut:
        ended = False
        if refusal is None:
            bad.append('the narration stops before the declared steps do')
    except _Lost:
        return bad, 0
    if refusal is not None:
        # the told steps are a prefix of the run, and a refused run answers nothing
        if re.match(r'^(\w+) answers ', last):
            bad.append('a refused run is told as answering')
        return bad, 0
    m = re.match(r'^(\w+) answers (.*)\.$', last)
    if not m or m.group(1) != alg:
        return bad + [f'the last line is not {alg}\'s answer: {last[:80]!r}'], 0
    try:
        got = json.loads(m.group(2))
    except ValueError:
        return bad + ['the answer told is not JSON'], 0
    if got != expected:
        bad.append(f'the answer told is {m.group(2)[:60]} and the fixture says {json.dumps(expected)[:60]}')
    # every name the answer is made of, rebuilt from what the narration said was added, computed or filed
    res = defs[alg]['result']
    vals = expected if len(res) > 1 else [expected]
    writes = {}

    def scan(names):
        for n in names:
            d = defs[n]
            if d['kind'] in ('COMPUTE', 'COLLECT', 'GROUP'):
                writes.setdefault(d['into'], set()).add(d['kind'])
            elif d['kind'] == 'BRANCH':
                scan(d['then'] or [])
                scan(d['else'] or [])
            elif d['kind'] == 'ITERATE':
                scan(d['do'] or [])
    scan(defs[alg]['steps'])
    for i, r in enumerate(res):
        kinds = writes.get(r, set())
        if kinds == {'COLLECT'}:
            rebuilt = told['collect'].get(r, [])
        elif kinds == {'GROUP'}:
            rebuilt = [[k, vs] for k, vs in told['group'].get(r, [])]
            vals_i = [[str(k), vs] for k, vs in vals[i]]
            if rebuilt != vals_i:
                bad.append(f'{r}: rebuilt from the told lines {json.dumps(rebuilt)[:70]}, the fixture says {json.dumps(vals[i])[:70]}')
            rebuilt_n += 1
            continue
        elif kinds == {'COMPUTE'} and r in told['compute']:
            rebuilt = told['compute'][r][-1]
        else:
            continue
        rebuilt_n += 1
        if rebuilt != vals[i]:
            bad.append(f'{r}: rebuilt from the told lines {json.dumps(rebuilt)[:70]}, the fixture says {json.dumps(vals[i])[:70]}')
    return bad, rebuilt_n


def judge_ask(lines, query, rows_total, expect, refusal):
    """The laws of a told question: how many matched of how many, the order, the cut and the
    answer are checked against the query's own clauses and the answer zing gave, never against
    the court's own evaluation of the condition."""
    if refusal is not None:
        if len(lines) != 1 or not lines[0].startswith('I stopped: ') or refusal not in lines[0]:
            return [f'a refused question is not told as the one refusal: {lines[0][:100]!r}']
        return []
    bad = []
    m = re.match(r'^SELECT \* FROM (\w+)(.*)$', query)
    frm, rest = m.group(1), m.group(2)
    order = re.search(r'\bORDER BY (\w+)(?: (ASC|DESC))?', rest)
    limit = re.search(r'\bLIMIT (\d+)', rest)
    want_n = None
    i = 0

    def line():
        nonlocal i
        if i >= len(lines):
            return ''
        i += 1
        return lines[i - 1]
    l = line()
    if l != f'Asking {frm}: {query}':
        bad.append(f'the first line is {l[:80]!r}')
    l = line()
    m = re.match(r'^(\d+) of the (\d+) rows match\.$', l)
    if not m:
        return bad + [f'no matched line: {l[:80]!r}']
    n_match, total = int(m.group(1)), int(m.group(2))
    if total != rows_total:
        bad.append(f'{total} rows told, {rows_total} given')
    kept = n_match
    if limit:
        kept = min(n_match, int(limit.group(1)))
    if kept != len(expect):
        bad.append(f'{n_match} matched under a {limit.group(0) if limit else "no limit"} cannot leave the {len(expect)} rows the fixture answers')
    if order:
        l = line()
        if l != f'Ordered by {order.group(1)} {order.group(2) or "ASC"}.':
            bad.append(f'the order told is {l[:70]!r} for {order.group(0)}')
    if limit and n_match > int(limit.group(1)):
        l = line()
        if l != f'Only the first {int(limit.group(1))} are kept.':
            bad.append(f'the cut told is {l[:70]!r} for {limit.group(0)} over {n_match} matches')
    l = line()
    m = re.match(r'^The answer is (\d+) row\(s\): (.*)$', l)
    if not m:
        return bad + [f'no answer line: {l[:80]!r}']
    if int(m.group(1)) != len(expect):
        bad.append(f'{m.group(1)} row(s) told, {len(expect)} answered')
    try:
        if json.loads(m.group(2)) != expect:
            bad.append('the rows told are not the rows the fixture answers')
    except ValueError:
        bad.append('the rows told are not JSON')
    if i != len(lines):
        bad.append(f'{len(lines) - i} line(s) told after the answer (a cut or an order told that did not happen?)')
    return bad


def one_call(body, call):
    return body.count(call) == 1


def stage19():
    """The sixteenth rung. NARRATE gains TELLS, a template per event of a run or a question,
    and `narrate-run` / `narrate-ask` answer in the language's own voice. The narration is a
    projection of the very run `run` or `ask` makes -- a flag raised, each step noting what it
    did -- never a replay and never stored. The judges are laws read in Python out of the
    declarations and the cases' own expected values, none of them asking the court what it
    meant: the told answer is the fixture's answer; the depth-0 steps are the declared STEPS,
    in order; an ITERATE walks as many items as the list holds and its steps run once per item;
    a BRANCH's steps are those of the arm it announced; every collected, computed or filed
    value rebuilt from the lines is the value the answer holds. A question's matched, order,
    cut and answer lines agree with its own clauses and zing's rows. Plus three runs and a
    question composed by hand BEFORE the court, and the same court under a voice that tells
    almost nothing, also composed by hand."""
    print('stage 19 -- NARRATE tells a run and a question: a_v16.haro and z_v16.haro -> `narrate-run` and `narrate-ask`, judged by laws read in Python')
    failures = 0
    for stzu, lead in ((A_STZU, 'forged a'), (Z_STZU, 'forged z')):
        out = run_args(RNXC, ['forge.ring', stzu, '.'], HERE).strip()
        if not out.startswith(lead):
            print(f'  FAIL the forge did not forge {os.path.basename(stzu)}: {out[:100]}')
            return 1
    ab_diff = []

    def both(court, args, label):
        r = run_args(RNXC, [court] + args, HERE).strip()
        o = run_args(ORACLE, [court] + args, HERE).strip()
        if r != o:
            ab_diff.append(label)
        return r
    # 0. the voice the judge assumes is the voice the declaration spells
    voice_bad = 0
    for path, want, tag in ((A_STZU, A_TELLS, 'a'), (Z_STZU, Z_TELLS, 'z')):
        got = read_tells(path)
        if got != want:
            voice_bad += 1
            print(f'  FAIL the judge reads the voice of {tag} as {want} and the declaration spells {got}')
    failures += voice_bad
    if not voice_bad:
        print('  ok   the templates the laws parse are the templates a_v16.haro and z_v16.haro declare')
    doc = json.load(open(RUN_CASES16, encoding='utf-8'))
    # 1. hand-written narrations: three runs and a question
    bad_hand = 0
    for c in doc['runs']:
        r = both('a_court.ring', ['narrate-run', c['sentence'], c['algorithm'], c['record']], 'hand:' + c['algorithm'])
        if r != '\n'.join(c['narration']):
            bad_hand += 1
            print(f'  FAIL the hand-written narration of {c["algorithm"]}')
            for a, b in zip(r.splitlines() + [''] * 12, c['narration'] + [''] * 12):
                if a != b:
                    print('    court :', a[:140]); print('    hand  :', b[:140]); break
    for c in doc['asks']:
        r = both('z_court.ring', ['narrate-ask', c['sentence'], c['question'], c['rows']], 'hand:ask')
        if r != '\n'.join(c['narration']):
            bad_hand += 1
            print('  FAIL the hand-written narration of a question')
            for a, b in zip(r.splitlines() + [''] * 8, c['narration'] + [''] * 8):
                if a != b:
                    print('    court :', a[:140]); print('    hand  :', b[:140]); break
    failures += bad_hand
    if not bad_hand:
        print(f'  ok   {len(doc["runs"])} runs and {len(doc["asks"])} question narrated as composed by hand before the court')
    # 2. every A case that runs: the laws
    defs = step_defs(os.path.join(HERE, A_SENTENCE))
    acases = json.load(open(A_CASES, encoding='utf-8'))
    n_runs = n_refused = n_rebuilt = 0
    run_bad = []
    for c in acases['cases']:
        if 'algorithm' not in c:
            continue
        refusal = c.get('refusal')
        r = both('a_court.ring', ['narrate-run', A_SENTENCE, c['algorithm'], json.dumps(c['input'])], 'run:' + c['id'])
        bad, rb = judge_run(r.splitlines(), defs, c['algorithm'], c['input'], c.get('expected'), refusal)
        if refusal is None:
            n_runs += 1
        else:
            n_refused += 1
        n_rebuilt += rb
        if PLANT and c['id'] == 'map-scale':
            bad = bad + ['PLANTED']
        for b in bad:
            run_bad.append((c['id'], b))
    failures += len(run_bad)
    for cid, why in run_bad[:6]:
        print(f'  FAIL {cid}: {why}')
    print(('  FAIL ' if run_bad else '  ok   ') + f'told runs: {n_runs} narrated whole and {n_refused} refused partway, each parsed into the tree its declarations and record say it must be -- the answer, the declared steps in order, every loop\'s item count, every branch\'s arm, and {n_rebuilt} answer(s) rebuilt from the lines ({len(run_bad)} defect(s))')
    if n_runs < A16_RUNS_FLOOR or n_rebuilt < A16_REBUILT_FLOOR:
        failures += 1
        print(f'  FAIL the laws judged {n_runs} run(s) and rebuilt {n_rebuilt} answer(s), under the pinned floors of {A16_RUNS_FLOOR} and {A16_REBUILT_FLOOR}')
    else:
        print(f'  ok   at or above the pinned floors of {A16_RUNS_FLOOR} runs and {A16_REBUILT_FLOOR} rebuilt answers')
    # 3. every Q case: the laws
    qdoc = json.load(open(Q_FIXTURES, encoding='utf-8'))
    rows_json = json.dumps(qdoc['rows'])
    n_asks = n_qref = 0
    ask_bad = []
    for c in qdoc['cases']:
        refusal = c.get('refusal')
        r = both('z_court.ring', ['narrate-ask', Z_SENTENCE, c['query'], rows_json], 'ask:' + c['id'])
        b = judge_ask(r.splitlines(), c['query'], len(qdoc['rows']), c.get('expect'), refusal)
        if refusal is None:
            n_asks += 1
        else:
            n_qref += 1
        for x in b:
            ask_bad.append((c['id'], x))
    by_id = {c['id']: c for c in qdoc['cases']}
    for query, base_id in Q16_UNCUT:
        r = both('z_court.ring', ['narrate-ask', Z_SENTENCE, query, rows_json], 'ask:uncut:' + base_id)
        for x in judge_ask(r.splitlines(), query, len(qdoc['rows']), by_id[base_id]['expect'], None):
            ask_bad.append(('uncut ' + base_id, x))
        n_asks += 1
    failures += len(ask_bad)
    for cid, why in ask_bad[:6]:
        print(f'  FAIL {cid}: {why}')
    print(('  FAIL ' if ask_bad else '  ok   ') + f'told questions: {n_asks} narrated and {n_qref} refused, each line checked against the query\'s own clauses and zing\'s rows -- how many matched of how many, the order, the cut (told only when it dropped rows), the answer ({len(ask_bad)} defect(s))')
    if n_asks < Z16_ASKS_FLOOR:
        failures += 1
        print(f'  FAIL the laws judged {n_asks} question(s), under the pinned floor of {Z16_ASKS_FLOOR}')
    # 4. the default voice: an event the voice does not tell is told plainly; hand-written
    d = doc['defaults']
    def variant(stzu, tells, label):
        text = open(stzu, encoding='utf-8').read()
        new = re.sub(r'TELLS \[\n.*?\n  \],', 'TELLS [\n    ' + tells + '\n  ],', text, flags=re.S)
        assert new != text
        with open(os.path.join(tdir, label + '.haro'), 'w', encoding='utf-8', newline='') as fh:
            fh.write(new)
        return os.path.join(tdir, label + '.haro')
    bad_def = 0
    with tempfile.TemporaryDirectory() as tdir:
        try:
            out = run_args(RNXC, ['forge.ring', variant(A_STZU, d['a_tells'], 'a_plain'), '.'], HERE).strip()
            if not out.startswith('forged a'):
                bad_def += 1
                print(f'  FAIL the plain voice of a did not forge: {out[:100]}')
            for c in d['runs']:
                r = both('a_court.ring', ['narrate-run', c['sentence'], c['algorithm'], c['record']], 'plain:' + c['algorithm'])
                if r != '\n'.join(c['narration']):
                    bad_def += 1
                    print(f'  FAIL the plain narration of {c["algorithm"]}')
                    for x, y in zip(r.splitlines() + [''] * 12, c['narration'] + [''] * 12):
                        if x != y:
                            print('    court :', x[:140]); print('    hand  :', y[:140]); break
            out = run_args(RNXC, ['forge.ring', variant(Z_STZU, d['z_tells'], 'z_plain'), '.'], HERE).strip()
            if not out.startswith('forged z'):
                bad_def += 1
                print(f'  FAIL the plain voice of z did not forge: {out[:100]}')
            for c in d['asks']:
                r = both('z_court.ring', ['narrate-ask', c['sentence'], c['question'], c['rows']], 'plain:ask')
                if r != '\n'.join(c['narration']):
                    bad_def += 1
                    print('  FAIL the plain narration of a question')
                    for x, y in zip(r.splitlines() + [''] * 8, c['narration'] + [''] * 8):
                        if x != y:
                            print('    court :', x[:140]); print('    hand  :', y[:140]); break
        finally:
            for stzu in (A_STZU, Z_STZU):
                run_args(RNXC, ['forge.ring', stzu, '.'], HERE)
    failures += bad_def
    if not bad_def:
        print(f'  ok   a voice that tells almost nothing: {len(d["runs"])} runs and {len(d["asks"])} question told plainly, as composed by hand; the real courts re-forged after')
    # 5. one run, one question: the narration is the run, not a second execution of it
    src = open(os.path.join(HERE, 'narrate_lib.ring'), encoding='utf-8').read()
    def body_of(fn):
        i = src.index('func ' + fn + '(')
        j = src.find('\nfunc ', i + 1)
        return src[i:j if j > 0 else len(src)]
    ok_run = one_call(body_of('NarTellRun'), 'RunAlgorithm(')
    ok_ask = one_call(body_of('NarTellAsk'), 'AskRun(')
    doctored = body_of('NarTellRun') + '\n\taRes = RunAlgorithm(aDecls, cAlg, aRecord)\n'
    if one_call(doctored, 'RunAlgorithm('):
        failures += 1
        print('  FAIL the one-execution law cannot fail: it passes a narration that runs the algorithm twice')
    elif not (ok_run and ok_ask):
        failures += 1
        print('  FAIL a narration executes the run or the question more than once (or not at all): it is a replay, not a projection')
    else:
        print('  ok   a narration is one execution: NarTellRun calls RunAlgorithm once and NarTellAsk calls AskRun once (and the check fails on a doctored copy that calls it twice)')
    # 6. never stored, never read back
    before = sorted(os.listdir(HERE))
    both('a_court.ring', ['narrate-run', A_SENTENCE, 'map_scale', '{"items":[1,2,3]}'], 'stored:a')
    both('z_court.ring', ['narrate-ask', Z_SENTENCE, 'SELECT * FROM collect LIMIT 1', rows_json], 'stored:z')
    after = sorted(os.listdir(HERE))
    if before != after:
        failures += 1
        print('  FAIL telling a run or a question changed the folder: a narration is stored')
    else:
        print('  ok   telling writes no file: a narration is a rendering of a run, never stored')
    with tempfile.TemporaryDirectory() as tdir:
        nar = both('a_court.ring', ['narrate-run', A_SENTENCE, 'map_scale', '{"items":[1,2,3]}'], 'back')
        p = os.path.join(tdir, 'back.a')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(nar + '\n')
        r = run_args(RNXC, ['a_court.ring', 'check', p], HERE).strip()
        if r.startswith('ok'):
            failures += 1
            print('  FAIL a told run was accepted as a sentence of A: the court reads one back')
        else:
            print('  ok   a told run is not a sentence of the language: the court refuses it, and has no verb that reads one back')
    # 7. a voice needs a run to tell, and a run needs a voice
    refuse_bad = 0
    for court, verb, want, what in (('machine_court.ring', 'narrate-run', 'declares no NARRATE', 'a language with no voice'),
                                    ('f_court.ring', 'narrate-run', 'declares no RUN', 'a voice over a language with no RUN'),
                                    ('f_court.ring', 'narrate-ask', 'declares no ASK', 'a voice over a language with no ASK'),
                                    ('a_court.ring', 'narrate-ask', 'declares no ASK', 'a language with a RUN and no ASK'),
                                    ('z_court.ring', 'narrate-run', 'declares no RUN', 'a language with an ASK and no RUN')):
        r = both(court, [verb, 'x', 'y', '[]'], f'refuse:{court}:{verb}')
        if want not in r:
            refuse_bad += 1
            failures += 1
            print(f'  FAIL {what} told something: {r[:120]}')
    if not refuse_bad:
        print('  ok   a language with no voice, no RUN or no ASK refuses the verb it cannot honour, and says which')
    if PLANT:
        failures += 1
        print('  FAIL the telling -- PLANTED')
    if ab_diff:
        failures += 1
        print(f'  FAIL rnxc and the oracle differ on {len(ab_diff)} run(s): {ab_diff[:5]}')
    else:
        print('  ok   rnxc and the oracle print the same bytes on every told run and question')
    return failures


# ---- stage 20: N, the natural letter, drawn from Ringua's Phase 1.5 study and built (rung 17)

N_CHECK = os.path.join(HERE, 'v17', 'n_check.py')


def stage20():
    """The seventeenth rung: n_v17.haro declares N and, with the UNDERSTAND meta-clause, the forge emits a court that
    checks sentences of N (17 defects the declaration's vocabulary refuses, 21 more the court's own rules catch, each
    of the 15 codes load-bearing) and answers tokens, understand, ask, vocabulary and examples; n/tontine.n is the
    tontine's natural door in English and French. The judge is v17/n_check.py's: the REAL court, asked the Phase 1.5
    study's 74 questions, answers what the study answered and what a reference model (read from the sentence alone)
    answers, a sample byte-identical on the oracle; with its gate removed it disagrees on the attacks."""
    print('stage 20 -- N, the natural letter built: n_v17.haro (UNDERSTAND) -> n_court.ring, n/tontine.n, judged by v17/n_check.py (the forged court reproduces the Phase 1.5 study on 74 questions)')
    failures = 0
    p = subprocess.run([sys.executable, N_CHECK], capture_output=True, cwd=ROOT, timeout=900)
    out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('n_check:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL n_check.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the drawn N letter -- PLANTED')
    return failures


# ---- stage 21: the v0.3 scans -- two of the Compass's principles, held by a guard (charter section 15)

CHARTER_SCANS = os.path.join(HERE, 'charter_scans.py')


def stage21():
    """Principle 13's refusal rule and principle 14, read off the committed tree: no refusal text addresses or names a
    person, and no letter outside the machine's declares a width. Each scan is made to fail first, on planted text."""
    print('stage 21 -- the v0.3 scans: a refusal names a state and never a person; a declared language names no width')
    failures = 0
    p = subprocess.run([sys.executable, CHARTER_SCANS], capture_output=True, cwd=ROOT, timeout=300)
    out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('charter_scans:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL charter_scans.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the v0.3 scans -- PLANTED')
    return failures


# ---- stage 22: the structure level of the computing altitude, Ring++ face (rung 18, Haro v0.18)

L1_CHECK = os.path.join(HERE, 'v18', 'l1_check.py')


def stage22():
    """The eighteenth rung: a program graph of Ring (v18/l1.py), a canonical printer, and a round-trip court (v18/l1_check.py) whose judge is
    the compiled code, not the tool's own sense of itself: 22 hand-composed fixtures (one per Ring trap, written before the code), two
    controls that must fail (an abstraction that drops a `for`'s step, caught only by `rnxc dis`; a printer that drops comments, caught by
    the round trip) and a corpus of Ring files -- every graph prints a text that parses back to the same graph, prints the same text again,
    and compiles to the same code. Where rnxc does not read Ring (`see`, `put`), the oracle judges."""
    print('stage 22 -- the program graph and its canonical printer, judged by round trip and by compiled code: v18/l1_check.py (22 fixtures, 2 controls, a corpus of Ring files)')
    failures = 0
    p = subprocess.run([sys.executable, L1_CHECK], capture_output=True, cwd=ROOT, timeout=900)
    out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('l1_check:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL l1_check.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the program graph -- PLANTED')
    return failures


# ---- stage 23: node identity on the program graph (rung 19, Haro v0.19)

IDS_CHECK = os.path.join(HERE, 'v19', 'ids_check.py')


def stage23():
    """The nineteenth rung: ids on the items of rung 18's graph, recovered when edited text is parsed again, by a matcher (v19/ids.py) that
    knows nothing but the graph that was and the graph that is. Judged by 23 edits written before the matcher (each: the ids the new program
    must hold and the ones that are gone), by controls that must fail (a matcher that pairs by position, one that keeps nothing, and each
    pass of the real one switched off in turn), and by Haro's own history: every hand-written Ring file of haro/spike, consecutive revisions
    read with `git show`, each old statement a refinement target that must still resolve. The floor is CODEGRAPH 3.7's 95 percent."""
    print('stage 23 -- node identity: v19/ids_check.py (23 edits, controls, Haro\'s own history replayed: does an old target still resolve?)')
    failures = 0
    p = subprocess.run([sys.executable, IDS_CHECK], capture_output=True, cwd=ROOT, timeout=1800)
    out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('ids_check:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL ids_check.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL node identity -- PLANTED')
    return failures


# ---- stage 24: refinement over the program graph (rung 20, Haro v0.20)

REFINE_CHECK = os.path.join(HERE, 'v20', 'refine_check.py')


def stage24():
    """The twentieth rung: a refinement is a sentence (rfn's shape) against a point a program declares in a `<R:KIND>` tag, put through five stages in
    stzRefinableCode's order and lowered to RCP's twelve primitives over rung 18's graph, with ids from rung 19; the diff is the printer's. Judged by 89
    fixtures written before the engine (v20/refine_check.py), by Softanza's own stzRefinableCode put the same proposals on the Ring++ package, by `rnxc graph`
    for a retargeted call, by the engine's constrained decoder for the grammar scoped to each program (the agent's write surface, charter 6.2), by controls
    that must fail, by Haro's own history (a drafted refinement still lands after the next human edit) and by a corpus of real Ring files refined at a literal."""
    print('stage 24 -- refinement over the program graph: v20/refine_check.py (147 fixtures, the BLOCK, FUNCTION and METHOD kinds and the allowlist rules among them, the live gate, rnxc graph, the scoped grammar, controls, history, a corpus)')
    failures = 0
    p = subprocess.run([sys.executable, REFINE_CHECK], capture_output=True, cwd=ROOT, timeout=3600)
    out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('refine_check:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL refine_check.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL refinement over the program graph -- PLANTED')
    return failures


# ---- stage 25: a second face of the program graph, in Python's shape (rung 21, Haro v0.21)

FACE_CHECK = os.path.join(HERE, 'v21', 'face_check.py')


def stage25():
    """The twenty-first rung: rung 18's graph printed in Python's shape, one-way, one meaning -- Ring's. What reads the same is spelt plainly, what Ring
    means differently is spelt with an explicit word (at, setat, eq, cat, plus, span, rng, G., return ""), and what has no spelling is refused by name
    from a collision table that travels with the face as its banner. Judged by fixtures written before the printer (v21/face_check.py), by Python's own
    parser on every text, by controls that must fail, and by Softanza's base through the face -- the measurement of kill criterion K3."""
    print('stage 25 -- a second face, in Python\'s shape: v21/face_check.py (72 fixtures, 22 collisions, ast.parse, controls, a corpus, K3)')
    failures = 0
    p = subprocess.run([sys.executable, FACE_CHECK], capture_output=True, cwd=ROOT, timeout=3600)
    out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('face_check:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL face_check.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL a second face -- PLANTED')
    return failures


# ---- stage 26: the reader of the Python-shaped face (rung 22, Haro v0.22)

FACE_READ_CHECK = os.path.join(HERE, 'v22', 'face_read_check.py')


def stage26():
    """The twenty-second rung: a text in the Python-shaped face read back to rung 18's graph, accepting exactly the printer's image (v21), so that what is read has one
    Ring meaning. Judged by fixtures written before the reader (v22/face_read_check.py), by the printer's own text read back to the same text, by the corpus read back
    to the same graph up to twelve declared losses (each shown needed by a control), by controls that must fail, and by the oracle: every runnable probe of bench/exec
    that the face can spell, printed, read back and run, prints what it printed before."""
    print('stage 26 -- the reader of the face: v22/face_read_check.py (67 fixtures, the round trip, 12 declared losses, controls, a corpus, the oracle)')
    failures = 0
    p = subprocess.run([sys.executable, FACE_READ_CHECK], capture_output=True, cwd=ROOT, timeout=3600)
    out = p.stdout.decode('utf-8', 'replace').replace(chr(13) + chr(10), chr(10))
    for line in out.splitlines():
        if line.startswith('  ') or line.startswith('face_read_check:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL face_read_check.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the reader of the face -- PLANTED')
    return failures


# ---- stage 27: the write-surface grammars of the two shapes (rung 22, Haro v0.22; K4, v22/k4/K4.md)

GRAMMAR_COURT = os.path.join(HERE, 'v22', 'grammar_court.py')


def stage27():
    """The grammars a model writes under, for the Python-shaped face (v22/face_gbnf.py) and for Ring++ (v22/ringpp_gbnf.py): the engine's own decoder holds each (under its 128 rules), accepts
    the twenty K4 programs as each shape's printer writes them and every v21 fixture the grammar's core covers, rejects what the shape excludes, and a grammar broken or loosened on
    purpose is caught. No model is loaded: the court is SHAPE only, so it runs in the guard (the model runs -- k4_local.py -- do not)."""
    print('stage 27 -- the write-surface grammars: v22/grammar_court.py (held by the decoder, K4 gold accepted, exclusions rejected, controls with teeth)')
    failures = 0
    p = subprocess.run([sys.executable, GRAMMAR_COURT], capture_output=True, cwd=ROOT, timeout=3600)
    out = p.stdout.decode('utf-8', 'replace').replace(chr(13) + chr(10), chr(10))
    for line in out.splitlines():
        if (line.startswith('  ') and 'not accepted' not in line) or line.startswith('GRAMMAR COURT') or line.startswith('grammars:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL grammar_court.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the grammars -- PLANTED')
    return failures


# ---- stage 28: the agent's body grammar (rung 5, a model as the agent; v20/agent/AGENT.md)

BODY_COURT = os.path.join(HERE, 'v20', 'agent', 'body_court.py')
AGENT_SELFTEST = os.path.join(HERE, 'v20', 'agent', 'r5_agent.py')
BYPASS_COURT = os.path.join(HERE, 'v20', 'agent', 'bypass_court.py')
LINT_COURT = os.path.join(HERE, 'v20', 'agent', 'lint_court.py')


def stage28():
    """The write surface of a body, scoped to its point (v20/agent/body_gbnf.py), and the tasks a model is measured on (v20/agent/tasks.py): the sixteen gold bodies each admitted by the gate and
    right on both data sets (rnxc and the oracle agreeing), a body that returns the shown answer admitted and wrong on the other, four forbidden shapes refused at their stage; the one-line and the
    lines grammar each held by the engine's decoder with every gold body accepted, what the gate would refuse for the shape rejected, a broken and a loosened grammar caught, and the grammar derived
    from a program's own point identical to the task-built one. And the bypass court (v20/agent/bypass_court.py): 50 bodies in two subjects written to reach what a point does not allow -- a forbidden call by
    nine routes, a forbidden write by sixteen, a for-in variable written through to a list, an accessor run by a member, a sentence closed from inside its TO -- judged by what the program DOES, each refused or inert except the named
    limits (an allowed callee's effects, operators on objects, reads, output, termination), and a gate that admits everything shown to fail it. And the task lint (v20/agent/lint_court.py, task_lint.py): 47 fixtures composed before the lint -- 18 requests that name a call, a write or an authority their point does not give
    (refused), 3 that may ask to change the caller's list (warned), 26 ordinary ones (clean: prose parentheses, a read of a global, `position(s)`) -- the sixteen tasks clean and the eleven adversarial ones judged as
    written down, a lint that finds nothing and one that finds everything shown to fail it. No model is loaded: the model runs
    (r5_local.py) are measurements, not guards."""
    print('stage 28 -- the body grammar of an agent: v20/agent/r5_agent.py selftest and v20/agent/body_court.py (no model loaded)')
    failures = 0
    for label, script, args in (('selftest', AGENT_SELFTEST, ['selftest']), ('adversarial selftest', AGENT_SELFTEST, ['selftest', '--set', 'adv']), ('body court', BODY_COURT, []), ('bypass court', BYPASS_COURT, []), ('lint court', LINT_COURT, [])):
        p = subprocess.run([sys.executable, script] + args, capture_output=True, cwd=ROOT, timeout=3600)
        out = p.stdout.decode('utf-8', 'replace').replace(chr(13) + chr(10), chr(10))
        for line in out.splitlines():
            if label == 'lint court':
                if 'FAIL' in line or 'fixtures:' in line or 'real tasks' in line or 'teeth' in line or line.startswith('LINT COURT'):
                    print(line)
            elif label == 'bypass court':
                if 'FAIL' in line or 'by family' in line or 'body grammar of the point' in line or 'teeth' in line or line.startswith('BYPASS COURT'):
                    print(line)
            elif line.startswith('  ') or line.startswith('r5_agent selftest') or line.startswith('BODY COURT') or 'grammar:' in line:
                print(line)
        if p.returncode != 0:
            failures += 1
            print(f'  FAIL {label} exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the body grammar of an agent -- PLANTED')
    return failures


def stage6(lang, court=None, n=15):
    court = court or f'{lang}_court.ring'
    print(f'stage 6 -- edit to verdict on makeen_box.machine, minima of {n}')
    def best(cmd, cwd, cache):
        env = dict(os.environ)
        if cache:
            env.pop('RNXC_NOCACHE', None)
        else:
            env['RNXC_NOCACHE'] = '1'
        ts = []
        for _ in range(n):
            t0 = time.perf_counter()
            subprocess.run(cmd, capture_output=True, env=env, cwd=cwd, timeout=120)
            ts.append(time.perf_counter() - t0)
        return min(ts) * 1000, sorted(ts)[n // 2] * 1000
    h = best([HARB, 'check', MAKEEN], os.path.dirname(HARB), False)
    r = best([RNXC, court, 'check', MAKEEN], HERE, False)
    rc = best([RNXC, court, 'check', MAKEEN], HERE, True)
    o = best([ORACLE, court, 'check', MAKEEN], HERE, False)
    print(f'  harb check (Zig, the native court)       min {h[0]:7.1f} ms   median {h[1]:7.1f} ms')
    print(f'  forged court on rnxc, compiled each run  min {r[0]:7.1f} ms   median {r[1]:7.1f} ms')
    print(f'  forged court on rnxc, its image reused   min {rc[0]:7.1f} ms   median {rc[1]:7.1f} ms')
    print(f'  forged court on the oracle               min {o[0]:7.1f} ms   median {o[1]:7.1f} ms')
    target = 100.0
    if r[0] <= target:
        print(f'  ok   under the {target:.0f} ms target on rnxc, image or no image')
        return 0
    print(f'  FAIL {r[0]:.1f} ms is over the {target:.0f} ms target on rnxc')
    return 1


if __name__ == '__main__':
    t0 = time.perf_counter()
    stage = None
    for a in sys.argv[1:]:
        if a.startswith('--stage='):
            stage = int(a.split('=')[1])
    # the default is the v0.3 declaration, the rung of record since 2026-10-01 (v0.2
    # is machine_v02.haro); the pinned v0.1 run is
    # `--haro=D:\GitHub\harobanda\declarative\machine\machine.stzu`
    stzu = os.path.join(HERE, 'machine_v03.haro')
    for a in sys.argv[1:]:
        if a.startswith('--haro='):
            stzu = os.path.abspath(a.split('=', 1)[1])
    failures = 0
    lang = None
    # the timing (stage 6) is measured FIRST in a full pass, on the machine as
    # it is when the pass starts: measured after stages 1-5, which write
    # hundreds of fixture files and launch hundreds of processes, it read
    # 114 ms with harb's own control at 1.85x its idle figure (HF-53)
    if stage in (None, 2, 3, 4, 5, 6):
        f2, lang = stage2(stzu)
        failures += f2
        if lang and stage in (None, 6):
            failures += stage6(lang)
    if stage in (None, 1):
        failures += stage1()
    if lang and stage in (None, 3):
        failures += stage3(lang, floor=AGREE_FLOOR if os.path.basename(stzu) == 'machine_v03.haro' else 0)
    # the fourth rung: the fleet language, a vocabulary over the machine language,
    # forged from fleet_v04.haro (which names machine_v03.haro beside it) and judged
    # against harb's fleet fixtures; `--stage=7` runs it alone
    if stage in (None, 7) and os.path.basename(stzu) == 'machine_v03.haro' and os.path.exists(FLEET_STZU):
        f7, lang7 = stage2(FLEET_STZU, 'fleet')
        failures += f7
        if lang7:
            failures += stage3(lang7, floor=FLEET_FLOOR, fixtures=FLEET_FIXTURES, verb='fleet', counts=FLEET_COUNTS)
    if lang and stage in (None, 4):
        failures += stage4(lang)
    if lang and stage in (None, 5):
        failures += stage5(lang, v02=os.path.basename(stzu) in ('machine_v02.haro', 'machine_v03.haro'))
    if stage in (None, 8) and os.path.exists(W_STZU):
        failures += stage8()
    if stage in (None, 9) and os.path.exists(Z_STZU):
        failures += stage9()
    if stage in (None, 10) and os.path.exists(Z_STZU) and os.path.exists(Q_FIXTURES):
        if stage == 10:
            run_args(RNXC, ['forge.ring', Z_STZU, '.'], HERE)
        failures += stage10()
    if stage in (None, 11) and os.path.exists(F_STZU) and os.path.isdir(F_DIR):
        failures += stage11()
    if stage in (None, 12) and os.path.exists(A_STZU) and os.path.exists(A_CASES):
        failures += stage12()
    if stage in (None, 13) and os.path.exists(Z_STZU) and os.path.exists(F_STZU):
        failures += stage13()
    if stage in (None, 14) and os.path.exists(F_STZU) and os.path.exists(STZU11_FIXTURES):
        failures += stage14()
    if stage in (None, 15) and os.path.exists(STZV_STZU) and os.path.exists(FORMS_CASES):
        failures += stage15()
    if stage in (None, 16) and os.path.exists(F_STZU) and os.path.exists(NARR_CASES):
        failures += stage16()
    if stage in (None, 17) and os.path.exists(F_STZU) and os.path.exists(MULTI_CASES):
        failures += stage17()
    if stage in (None, 18) and os.path.exists(META_CASES):
        failures += stage18()
    if stage in (None, 19) and os.path.exists(RUN_CASES16) and os.path.exists(A_CASES):
        failures += stage19()
    if stage in (None, 20) and os.path.exists(N_CHECK):
        failures += stage20()
    if stage in (None, 21) and os.path.exists(CHARTER_SCANS):
        failures += stage21()
    if stage in (None, 22) and os.path.exists(L1_CHECK):
        failures += stage22()
    if stage in (None, 23) and os.path.exists(IDS_CHECK):
        failures += stage23()
    if stage in (None, 24) and os.path.exists(REFINE_CHECK):
        failures += stage24()
    if stage in (None, 25) and os.path.exists(FACE_CHECK):
        failures += stage25()
    if stage in (None, 26) and os.path.exists(FACE_READ_CHECK):
        failures += stage26()
    if stage in (None, 27) and os.path.exists(GRAMMAR_COURT):
        failures += stage27()
    if stage in (None, 28) and os.path.exists(BODY_COURT):
        failures += stage28()
    print(f'haro_forge: {"FAIL" if failures else "PASS"} ({failures} failure(s), {time.perf_counter()-t0:.1f} s)')
    sys.exit(1 if failures else 0)
