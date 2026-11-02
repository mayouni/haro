"""Judges N as BUILT, the seventeenth rung: python haro/spike/v17/n_check.py [--plant]   (exit 1 on any failure)

  A  the letter, the forge and the sentence: the meta-court accepts n_v17.haro (its UNDERSTAND included), the forge
     forges N from it, and the forged court accepts n/tontine.n -- `check`, and `check ... surfaces`, which asks the
     ledger's own court to judge every ledger query -- on rnxc and on the oracle, byte for byte
  B  17 defects the declaration's own vocabulary catches: refused with the message and code the letter declares
  C  22 defects a rule of the rung must catch: the forged court answers the declared code, and the reference model
     (n_model.rules, a second implementation read from the sentence alone) answers the same codes; the unmutated
     sentence has no finding; rnxc and the oracle print the same bytes
  C' each of the 16 codes, switched off in the court in turn, is the one thing that makes its fixtures fail
  C'' the door: `check ... surfaces` runs the court a sentence names, so a court named by a path is refused and NOT run
  D  the REAL court, asked the Phase 1.5 study's 74 questions, answers what the study answered -- the closed query,
     the graph answer, the sentence told, the refusal kind, one meaning sequence in both tongues of every pair --
     and what the model answers; `tokens`, `vocabulary` and `examples` agree with the model; a sample of the asks is
     byte-identical on the oracle
  E  the check can fail: the same comparison on a court whose gate is removed disagrees on the attacks

Reads the study's fixtures and its recorded run (haro/study/phase15/); runs nothing of Softanza.
"""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
HARO_VM = paths.HARO_VM
TWIN = paths.TWIN
STUDY = os.path.join(paths.HARO, 'study', 'phase15')
PLANT = '--plant' in sys.argv
sys.path.insert(0, HERE)
import n_model

fails = []
NOCACHE = dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1')


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def court(exe, args, cwd=SP, cache=False):
    r = subprocess.run([exe] + args, capture_output=True, cwd=cwd, env=os.environ if cache else NOCACHE, timeout=300)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip()


def both(args):
    a, b = court(HARO_VM, args), court(TWIN, args)
    return a, a == b


print('n_check -- N as built (n_v17.haro, n/tontine.n, the forged n_court.haro)')
SENTENCE = os.path.join('n', 'tontine.n')
# a mutated sentence is written beside the real one, so the worlds it names are found where they are
for stale in os.listdir(os.path.join(SP, 'n')):
    if stale.startswith('_mut_'):
        os.remove(os.path.join(SP, 'n', stale))

# the forge first: a court forged before the forge learned something is a court the oracle refuses (HF-61)
out = court(HARO_VM, ['forge.haro', 'n_v17.haro', '.'])
check(out.startswith('forged n'), f'the forge forges N from n_v17.haro: {out.splitlines()[0][:80] if out else "NO OUTPUT"}')
doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
sentence = open(os.path.join(SP, doc['sentence']), encoding='utf-8', newline='').read()
# the floors: a judge that checks nothing cannot pass
COURT_FLOOR, RULES_FLOOR, CODES_FLOOR, STUDY_FLOOR, PAIRS_FLOOR = 17, 22, 16, 74, 17
check(len(doc['court']) >= COURT_FLOOR and len(doc['rules']) >= RULES_FLOOR,
      f"the fixtures hold {len(doc['court'])} court cases and {len(doc['rules'])} rule cases, at or above the pinned floors of {COURT_FLOOR} and {RULES_FLOOR}")
CODES = sorted({c['code'] for c in doc['rules']})
check(len(CODES) >= CODES_FLOOR, f'the rule fixtures reach {len(CODES)} codes, at or above the pinned floor of {CODES_FLOOR}')

# ---- A -------------------------------------------------------------------------------------------------------------------
a, same = both(['haro.haro', 'n_v17.haro', 'all'])
check(a.startswith('ok') and same and 'understands 1' in a, 'A the meta-court accepts n_v17.haro, its UNDERSTAND included, the same bytes on both runtimes')
a, same = both(['n_court.haro', 'check', SENTENCE])
check(a.startswith('ok') and same, 'A the forged N court accepts n/tontine.n, the same bytes on both runtimes (' + ', '.join(f'{l.split()[1]} {l.split()[2]}' for l in a.splitlines() if l.startswith('count ')) + ')')
a, same = both(['n_court.haro', 'check', SENTENCE, 'surfaces'])
check(a.startswith('ok') and same, 'A `check ... surfaces` asks the ledger\'s own court to judge every ledger query: accepted, the same bytes on both runtimes')
u1, u2 = court(HARO_VM, ['n_court.haro', 'examples', SENTENCE]), court(TWIN, ['n_court.haro', 'examples', SENTENCE])
check(u1 == u2 and json.loads(u1)['examples']['failed'] == 0, f'A `examples` on both runtimes: {u1[:110]}')


def ledger_runner(query):
    """The ledger's own court as the surface that judges a ledger query: what the court's `surfaces` does, from outside."""
    r = subprocess.run([HARO_VM, 'z_court.haro', 'ask', 'tontine.z', query, '[]'], capture_output=True, cwd=SP, env=NOCACHE, timeout=120)
    o = r.stdout.decode('utf-8', 'replace').strip()
    return (o.startswith('['), o[:120])


# ---- B -------------------------------------------------------------------------------------------------------------------
bad = []
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, 'x.n')
    for c in doc['court']:
        assert sentence.count(c['old']) == 1, (c['id'], sentence.count(c['old']))
        open(p, 'w', encoding='utf-8', newline='').write(sentence.replace(c['old'], c['new']))
        r, same = both(['n_court.haro', 'check', p])
        if r.startswith('ok') or c['message'] not in r:
            bad.append((c['id'], f"expected {c['message']!r}, got {r[:100]!r}"))
        elif not same:
            bad.append((c['id'], 'haro and its checked build differ'))
        elif c['code']:
            d = json.loads(court(HARO_VM, ['n_court.haro', 'diagnose', p]))
            if c['code'] not in [x['code'] for x in d['diagnostics']]:
                bad.append((c['id'], f"expected code {c['code']}, got {[x['code'] for x in d['diagnostics']]}"))
for cid, why in bad[:5]:
    print(f'  FAIL {cid}: {why}')
fails.extend(f'B {c}' for c, _ in bad)
check(not bad, f"B {len(doc['court'])} defects the declaration's own vocabulary catches are refused by the forged court, with the declared message and code, the same on both runtimes ({len(bad)} differ)")

# ---- C -------------------------------------------------------------------------------------------------------------------
n0 = n_model.N(sentence, os.path.join(SP, 'n'))
base = n_model.rules(n0, ledger_runner)
d0 = json.loads(court(HARO_VM, ['n_court.haro', 'diagnose', SENTENCE, 'surfaces']))['diagnostics']
check(not base and not d0, f'C the unmutated sentence has no finding, in the court or in the model: {len(n0.decls)} declarations, every ledger query judged by the ledger\'s own court ({base[:1]} {d0[:1]})')


def mutate(case, root=SP):
    """Write the case's sentence beside the real one; returns its path relative to the spike folder."""
    assert sentence.count(case['old']) == 1, (case['id'], sentence.count(case['old']))
    rel = os.path.join('n', '_mut_' + case['id'] + '.n')
    open(os.path.join(SP, rel), 'w', encoding='utf-8', newline='').write(sentence.replace(case['old'], case['new']))
    return rel


def codes_of(exe, rel, surfaces, cwd=SP):
    d = json.loads(court(exe, ['n_court.haro', 'diagnose', rel] + (['surfaces'] if surfaces else []), cwd=cwd))
    return sorted(x['code'] for x in d['diagnostics']), d


bad = []
try:
    for c in doc['rules']:
        rel = mutate(c)
        got, d = codes_of(HARO_VM, rel, c['surfaces'])
        want = sorted(x[0] for x in n_model.rules(n_model.N(open(os.path.join(SP, rel), encoding='utf-8', newline='').read(), os.path.join(SP, 'n')),
                                                  ledger_runner if c['surfaces'] else None))
        if c['code'] not in got:
            bad.append((c['id'], f"the court did not answer {c['code']}: {sorted(set(got))}"))
        elif got != want:
            bad.append((c['id'], f"the court answers {sorted(set(got))}, the model {sorted(set(want))}"))
        elif not all(x['severity'] == 'error' and x['language'] == 'n' and x['cites'] == ['rule:' + x['code'].lower()] for x in d['diagnostics']):
            bad.append((c['id'], 'a finding is not a C2 envelope with its rule cite'))
        else:
            args = ['n_court.haro', 'check', rel] + (['surfaces'] if c['surfaces'] else [])
            r, same = both(args)
            if r.startswith('ok') or not same or c['code'] not in json.dumps(d):
                bad.append((c['id'], f"`check` {'agrees' if same else 'differs between the runtimes'}: {r[:90]!r}"))
finally:
    for f in os.listdir(os.path.join(SP, 'n')):
        if f.startswith('_mut_'):
            os.remove(os.path.join(SP, 'n', f))
for cid, why in bad[:5]:
    print(f'  FAIL {cid}: {why}')
fails.extend(f'C {c}' for c, _ in bad)
check(not bad, f"C {len(doc['rules'])} defects are caught by the forged court with the declared code, as the model catches them, `check` refusing and the runtimes agreeing ({len(bad)} not)")


# ---- C' ------------------------------------------------------------------------------------------------------------------
def court_copy(patch=None):
    """A copy of the court's files, one of them patched: a court that differs from the real one in exactly one thing."""
    os.makedirs(paths.OUT, exist_ok=True)
    td = tempfile.mkdtemp(dir=paths.OUT)
    for f in os.listdir(SP):
        if f.endswith('.ring'):
            shutil.copy(os.path.join(SP, f), td)
    for f in ('tontine.z',):
        shutil.copy(os.path.join(SP, f), td)
    if patch:
        p = os.path.join(td, 'n_lib.haro')
        s = open(p, encoding='utf-8', newline='').read()
        old, new = patch
        assert s.count(old) == 1, (old, s.count(old))
        open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
    return td


bad = []
try:
    for code in CODES:
        td = court_copy(('func NatAdd(aF, cCode, nLine, cMsg)\n', f'func NatAdd(aF, cCode, nLine, cMsg)\n\tif cCode = "{code}" return ok\n'))
        for c in doc['rules']:
            if c['code'] != code:
                continue
            rel = mutate(c)
            r = json.loads(court(HARO_VM, [os.path.join(td, 'n_court.haro'), 'diagnose', os.path.join(SP, rel)] + (['surfaces'] if c['surfaces'] else []), cwd=td))
            if code in [x['code'] for x in r['diagnostics']]:
                bad.append((code, f"{c['id']}: the code is still answered with its rule switched off"))
        shutil.rmtree(td)
finally:
    for f in os.listdir(os.path.join(SP, 'n')):
        if f.startswith('_mut_'):
            os.remove(os.path.join(SP, 'n', f))
for cid, why in bad[:5]:
    print(f'  FAIL {cid}: {why}')
fails.extend(f"C' {c}" for c, _ in bad)
check(not bad, f"C' each of the {len(CODES)} codes, with its rule switched off in the court, is no longer answered: every rule is the one thing that catches its fixtures ({len(bad)} still answered)")

# ---- C'' -----------------------------------------------------------------------------------------------------------------
# `check ... surfaces` RUNS the court file a surface names, so what a sentence may name there is a door (principle 12, the
# Compass's "no effect without a door"): a sibling court, never a path. A program that proves it ran by writing a marker is
# named by a path (must not run) and, as the control, beside the court (must run, or the marker shows nothing)
os.makedirs(paths.OUT, exist_ok=True)
MARKER = os.path.join(paths.OUT, 'zz_marker.txt')
PROGRAM = 'write("' + paths.rel(MARKER, SP) + '", "ran")\n'   # the court runs from SP
HOSTILE, SIBLING = os.path.join(SP, 'v17', 'zz_marker.ring'), os.path.join(SP, 'zz_marker_court.haro')


def marker_after(court_name):
    rel = mutate({'id': 'M1', 'old': 'COURT "z_court.haro ask"', 'new': 'COURT "' + court_name + ' ask"'})
    seen = {}
    for exe in (HARO_VM, TWIN):
        if os.path.exists(MARKER):
            os.remove(MARKER)
        r = court(exe, ['n_court.haro', 'check', rel, 'surfaces'])
        seen[exe] = (os.path.exists(MARKER), 'names the court file' in r)   # by path: both judges are haro.exe
        if os.path.exists(MARKER):
            os.remove(MARKER)
    return seen


try:
    for f in (HOSTILE, SIBLING):
        open(f, 'w', encoding='utf-8', newline='').write(PROGRAM)
    hostile, control = marker_after('v17/zz_marker.ring'), marker_after('zz_marker_court.haro')
finally:
    for f in (HOSTILE, SIBLING, MARKER) + tuple(os.path.join(SP, 'n', x) for x in os.listdir(os.path.join(SP, 'n')) if x.startswith('_mut_')):
        if os.path.exists(f):
            os.remove(f)
check(all(not ran and said for ran, said in hostile.values()),
      f"C'' a court named by a path is refused (N_SURFACE_COURT) and the program it names is NOT run, on both runtimes ({hostile})")
check(all(ran for ran, _ in control.values()),
      f"C'' the control: the same program, named as a court beside the court, IS run -- so the marker can show a run ({control})")

# ---- D -------------------------------------------------------------------------------------------------------------------
study = json.load(open(os.path.join(STUDY, 'fixtures', 'questions.json'), encoding='utf-8'))['cases']
recorded, plans = {}, {}
for line in open(os.path.join(STUDY, 'e4_result.txt'), encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    if f[0] == 'RESULT' and f[2] == 'refused':
        r = f[4]
        recorded[f[1]] = 'shape' if ('this shape' in r or 'cette forme' in r) else ('character' if ('character' in r or 'caractere' in r) else 'word')
    if f[0] == 'PLAN' and len(f) >= 4:
        plans[f[1]] = f[3]
TONGUE = {'tn-en': 'english', 'tn-fr': 'french'}
FRAME = lambda s: 'beneficiary_deposits' if s == 'plan-beneficiary-deposits' else s.replace('-', '_')


def norm_target(t):
    """The study's internal templates -> the notation of the sentence: triples as three terms, ZQL strings single-quoted."""
    if ' => ' in t:
        a, b = t.split(' => ')
        return norm_target(a) + ' => ' + b.replace('"', "'").replace('{MEMBER}', '{member}')
    if t.startswith('['):
        return ' '.join(re.findall(r'"([^"]*)"', t))
    return t.replace('"', "'")


def normalise(j):
    """What the court's JSON says, in the shape the model answers (and the study's judge reads)."""
    if 'refused' in j:
        r = j['refused']
        return {'refused': r['kind'], 'what': r['what'], 'message': r['message']}
    u = {'frame': j['frame'], 'surface': j['surface'], 'slots': j['slots']}
    if 'steps' in j:
        u['steps'] = [(s['surface'], s['query'], s.get('binds', '')) for s in j['steps']]
        u['query'] = ' => '.join(q for _, q, _ in u['steps'])
    else:
        u['query'] = j['query']
    for k in ('answer', 'told', 'query2'):
        if k in j:
            u[k] = j[k]
    u['run'] = [(r['surface'], r['court'], r['world'], r['query']) for r in j.get('run', [])]
    return u


class CourtN:
    """The forged court, asked as the model is asked: n_court.haro on rnxc, one process a question."""

    def __init__(self, cwd=SP, court_file='n_court.haro', sentence_path=SENTENCE, cache=True):
        self.cwd, self.court_file, self.sentence_path, self.cache = cwd, court_file, sentence_path, cache
        self.memo = {}

    def say(self, verb, tongue, text, exe=HARO_VM):
        key = (verb, tongue, text, exe)
        if key not in self.memo:
            self.memo[key] = court(exe, [self.court_file, verb, self.sentence_path, tongue, text], cwd=self.cwd, cache=self.cache and exe == HARO_VM)
        return self.memo[key]

    def ask(self, tongue, text):
        return normalise(json.loads(self.say('ask', tongue, text)))

    def tokens(self, tongue, text):
        j = json.loads(self.say('tokens', tongue, text))
        if 'refused' in j:
            return None, (j['refused']['kind'], j['refused']['what'])
        return [(t['meaning'], t.get('slot'), t['word']) for t in j['tokens']], None


def judge(model):
    out = []
    n_ok = 0
    toks = {}
    for c in study:
        e = c['expect']
        text = c['text'].replace('~NL~', '\n')
        tg = TONGUE[c['lang']]
        u = model.ask(tg, text)
        if e['kind'] == 'refused':
            if u.get('refused') != recorded[c['id']]:
                out.append((c['id'], f"the study refused it as {recorded[c['id']]}, the answer: {u.get('refused') or u.get('frame')}"))
            else:
                n_ok += 1
            continue
        if 'frame' not in u:
            out.append((c['id'], f"the study compiled it, the answer refused it as {u['refused']} ({u['what']!r})"))
            continue
        want = norm_target(e['target'])
        if u['frame'] != FRAME(e['frame']) or u['query'] != want or u['surface'] != e['kind']:
            out.append((c['id'], f"want {FRAME(e['frame'])} {want!r}, got {u['frame']} {u['query']!r}"))
            continue
        if 'answer' in e and u.get('answer') != e['answer']:
            out.append((c['id'], f"want answer {e['answer']}, got {u.get('answer')}"))
            continue
        if 'say' in e and u.get('told') != e['say']:
            out.append((c['id'], f"want sentence {e['say']!r}, got {u.get('told')!r}"))
            continue
        if e['kind'] == 'plan':
            want2 = plans[c['id']].replace('"', "'")
            if u.get('query2') != want2:
                out.append((c['id'], f"want second query {want2!r}, got {u.get('query2')!r}"))
                continue
        n_ok += 1
        if c['group'] == 'pair':
            toks.setdefault(c['pair'], {})[tg] = [m for m, _, _ in model.tokens(tg, text)[0]]
    split = [p for p, d in toks.items() if len(d) == 2 and d['english'] != d['french']]
    return out, n_ok, split, len(toks)


if PLANT:
    study[0]['expect']['target'] += ' PLANTED'
real = CourtN()
diffs, n_ok, split, n_pairs = judge(real)
check(len(study) >= STUDY_FLOOR, f'D the study\'s fixtures hold {len(study)} questions, at or above the pinned floor of {STUDY_FLOOR}')
for cid, why in diffs[:6]:
    print(f'  FAIL D {cid}: {why}')
fails.extend(f'D {c}' for c, _ in diffs)
check(not diffs, f'D the forged court, asked the study\'s questions, reproduces the study on {n_ok} of {len(study)}: the closed query, the graph answer, the sentence told, the refusal kind ({len(diffs)} differ)')
check(not split and n_pairs >= PAIRS_FLOOR, f'D the meaning sequence is identical in English and French for {n_pairs - len(split)} of {n_pairs} pairs ({split[:3]})')

# the court and the model, field for field, on every question; tokens too
unlike, tk_unlike = [], []
for c in study:
    text = c['text'].replace('~NL~', '\n')
    tg = TONGUE[c['lang']]
    a = {k: v for k, v in real.ask(tg, text).items() if v is not None}
    m = n0.ask(tg, text)
    b = {k: v for k, v in m.items() if v is not None}
    if 'steps' in b:
        b['steps'] = [tuple(x) for x in b['steps']]
    b['run'] = [tuple(x) for x in b.get('run', [])] if 'refused' not in b else []
    if 'refused' in a:
        a, b = {k: a[k] for k in ('refused', 'what', 'message')}, {k: b[k] for k in ('refused', 'what', 'message')}
    else:
        a['run'] = a.get('run', [])
    if a != b:
        unlike.append((c['id'], f'court {a} / model {b}'))
    tj = json.loads(real.say('tokens', tg, text))
    tm = n0.tokens_full(tg, text)
    if 'refused' in tj:
        same_t = tm.get('refused') == tj['refused']['kind'] and tm.get('what') == tj['refused']['what']
    else:
        same_t = tj == tm
    if not same_t:
        tk_unlike.append((c['id'], f'court {tj} / model {tm}'))
for cid, why in (unlike + tk_unlike)[:4]:
    print(f'  FAIL D {cid}: {why[:300]}')
fails.extend(f'D court/model {c}' for c, _ in unlike + tk_unlike)
check(not unlike and not tk_unlike, f'D the court and the model agree field for field on `ask` and on `tokens` for all {len(study)} questions ({len(unlike)} and {len(tk_unlike)} differ)')

voc = [(tg, json.loads(court(HARO_VM, ['n_court.haro', 'vocabulary', SENTENCE, tg], cache=True)), n0.vocabulary(tg)) for tg in ('english', 'french')]
ex_c, ex_m = json.loads(court(HARO_VM, ['n_court.haro', 'examples', SENTENCE], cache=True)), n0.examples_report()
check(all(c == m for _, c, m in voc) and ex_c == ex_m and sum(len(c['words']) for _, c, _ in voc) > 60,
      f"D `vocabulary` (both tongues, {sum(len(c['words']) for _, c, _ in voc)} words) and `examples` ({ex_c['examples']['understood']} of {ex_c['examples']['texts']} texts understood, {ex_c['counterexamples']['refused']} of {ex_c['counterexamples']['texts']} refused) agree with the model")

# a sample of the asks on the oracle: the same bytes (the oracle takes ~0.6 s a question, so one in four)
sample = [c for i, c in enumerate(study) if i % 4 == 0]
odd = []
for c in sample:
    text = c['text'].replace('~NL~', '\n')
    tg = TONGUE[c['lang']]
    if real.say('ask', tg, text) != real.say('ask', tg, text, exe=TWIN):
        odd.append(c['id'])
check(not odd and len(sample) >= 18, f'D {len(sample)} of the questions, asked on the checked build, give the same bytes as on haro ({odd[:3]})')

# ---- E -------------------------------------------------------------------------------------------------------------------
td = court_copy(('func NatGate(aT, cText)\n', 'func NatGate(aT, cText)\n\treturn ""\n'))
try:
    r = json.loads(court(HARO_VM, [os.path.join(td, 'n_court.haro'), 'diagnose', os.path.join(SP, SENTENCE)], cwd=td))
    check('N_COUNTEREXAMPLE_FAILED' in [x['code'] for x in r['diagnostics']],
          f"E a court without its gate is refused by the sentence's own counterexamples: {len(r['diagnostics'])} finding(s), N_COUNTEREXAMPLE_FAILED among them")
finally:
    shutil.rmtree(td)
td = court_copy(('func NatGate(aT, cText)\n', 'func NatGate(aT, cText)\n\treturn ""\n'))
try:
    p = os.path.join(td, 'n_lib.haro')
    lib = open(p, encoding='utf-8', newline='').read()
    assert lib.count('func NatCheckRules(aDecls)\n') == 1
    open(p, 'w', encoding='utf-8', newline='').write(lib.replace('func NatCheckRules(aDecls)\n', 'func NatCheckRules(aDecls)\n\treturn 0\n'))
    nogate = CourtN(cwd=td, court_file=os.path.join(td, 'n_court.haro'), sentence_path=os.path.join(SP, SENTENCE), cache=False)
    attacks = [c for c in study if c['group'] == 'attack']
    save, study[:] = list(study), attacks
    d2, _, _, _ = judge(nogate)
    study[:] = save
finally:
    shutil.rmtree(td)
caught = {cid for cid, _ in d2}
check(len(caught) >= 10, f'E the comparison can fail: with the gate removed from the court it disagrees with the study on {len(caught)} of {len(attacks)} attacks')

print(f'n_check: {"FAIL" if fails else "PASS"} ({len(fails)} failure(s))')
sys.exit(1 if fails else 0)
