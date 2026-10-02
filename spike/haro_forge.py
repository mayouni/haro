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


def judge_stzu(exe, label, fixtures=STZU_FIXTURES):
    """Mirror experiment/run_stzu.luau: accepts carry structural
    expectations, rejects carry the fragment the refusal must contain.
    v0.2's fixtures add the keys menus/ranges/formats/constraints (under
    counts), world and points."""
    doc = json.load(open(fixtures, encoding='utf-8'))
    # the pinned v0.1 judge is stzu's; everything since is Haro's (D1)
    assert doc['grammar'] in ('stzu', 'haro') and doc['version'] in ('0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.10', '0.11')
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
                            ('v0.11, the Diagnostic Contract: CODE, CODES, CITES', STZU11_FIXTURES)):
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

Z_STZU = os.path.join(HERE, 'z_v10.haro')   # z_v07.haro plus PUBLISH (the tenth rung); the 16 cases and 25 questions are unchanged
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

F_STZU = os.path.join(HERE, 'f_v11.haro')   # f_v10.haro plus RingFlex's codes and cites (the eleventh rung); the 27 fixtures are unchanged
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

A_STZU = os.path.join(HERE, 'a_v09.haro')
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
            if len(errs) != 1:
                code_bad.append((name, f'expected one error, got {len(errs)}'))
            elif errs[0]['code'] != want:
                code_bad.append((name, f'code {errs[0]["code"]} where RingFlex says {want}'))
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
    print(f'haro_forge: {"FAIL" if failures else "PASS"} ({failures} failure(s), {time.perf_counter()-t0:.1f} s)')
    sys.exit(1 if failures else 0)
