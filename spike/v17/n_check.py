"""Judges the N letter as DRAWN: python haro/spike/v17/n_check.py [--plant]   (exit 1 on any failure)

  A  the letter and the sentence: n_v17.haro is a lawful declaration and n/tontine.n a lawful sentence, on rnxc and
     on the oracle, byte for byte
  B  17 defects the EXISTING meta-vocabulary must make the forged court refuse, with the message and code the
     letter declares
  C  20 defects the existing court CANNOT see (it says `ok`) and that the rules of the next rung must catch:
     n_model.rules() must answer the declared code. The unmutated sentence has no finding, the ledger's own court
     judging every ledger query it holds
  D  the model, read from the sentence ALONE, reproduces the Phase 1.5 study's behaviour on all 74 questions:
     the closed query each compiles to, the graph answers, the sentences told, the kind of every refusal, the
     meaning sequence identical across the two tongues of every pair. It shares no code with the study's pipeline
  E  the check can fail: the same comparison with the gate removed from the model must disagree on the attacks

Reads the study's fixtures and its recorded run (haro/study/phase15/); runs nothing of Softanza.
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(SP, '..', '..'))
RNXC = os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
ORACLE = os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
STUDY = os.path.join(ROOT, 'haro', 'study', 'phase15')
PLANT = '--plant' in sys.argv
sys.path.insert(0, HERE)
import n_model

fails = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def court(exe, args, cwd=SP):
    r = subprocess.run([exe] + args, capture_output=True, cwd=cwd, env=dict(os.environ, RNXC_NOCACHE='1'), timeout=300)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip()


def both(args):
    a, b = court(RNXC, args), court(ORACLE, args)
    return a, a == b


print('n_check -- the N letter as drawn (n_v17.haro, n/tontine.n)')
# the forge first: a court forged before the forge learned something is a court the oracle refuses (HF-61)
out = court(RNXC, ['forge.ring', 'n_v17.haro', '.'])
check(out.startswith('forged n'), f'the forge forges N from n_v17.haro: {out.splitlines()[0][:80] if out else "NO OUTPUT"}')
doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
sentence = open(os.path.join(SP, doc['sentence']), encoding='utf-8', newline='').read()
# the floors: a judge that checks nothing cannot pass
COURT_FLOOR, RULES_FLOOR, STUDY_FLOOR, PAIRS_FLOOR = 17, 20, 74, 17
check(len(doc['court']) >= COURT_FLOOR and len(doc['rules']) >= RULES_FLOOR,
      f"the fixtures hold {len(doc['court'])} court cases and {len(doc['rules'])} rule cases, at or above the pinned floors of {COURT_FLOOR} and {RULES_FLOOR}")

# ---- A -------------------------------------------------------------------------------------------------------------------
a, same = both(['haro.ring', 'n_v17.haro', 'all'])
check(a.startswith('ok') and same, 'A the meta-court accepts n_v17.haro, the same bytes on both runtimes')
a, same = both(['n_court.ring', 'check', doc['sentence']])
check(a.startswith('ok') and same, 'A the forged N court accepts n/tontine.n, the same bytes on both runtimes (' + ', '.join(f'{l.split()[1]} {l.split()[2]}' for l in a.splitlines() if l.startswith('count ')) + ')')

# ---- the ledger's own court, as the surface that judges a ledger query -------------------------------------------------
def ledger_runner(query):
    r = subprocess.run([RNXC, 'z_court.ring', 'ask', 'tontine.z', query, '[]'], capture_output=True, cwd=SP, env=dict(os.environ, RNXC_NOCACHE='1'), timeout=120)
    o = r.stdout.decode('utf-8', 'replace').strip()
    return (o.startswith('['), o[:120])


# ---- B -------------------------------------------------------------------------------------------------------------------
bad = []
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, 'x.n')
    for c in doc['court']:
        assert sentence.count(c['old']) == 1, (c['id'], sentence.count(c['old']))
        open(p, 'w', encoding='utf-8', newline='').write(sentence.replace(c['old'], c['new']))
        r, same = both(['n_court.ring', 'check', p])
        if r.startswith('ok') or c['message'] not in r:
            bad.append((c['id'], f"expected {c['message']!r}, got {r[:100]!r}"))
        elif not same:
            bad.append((c['id'], 'rnxc and the oracle differ'))
        elif c['code']:
            d = json.loads(court(RNXC, ['n_court.ring', 'diagnose', p]))
            if c['code'] not in [x['code'] for x in d['diagnostics']]:
                bad.append((c['id'], f"expected code {c['code']}, got {[x['code'] for x in d['diagnostics']]}"))
for cid, why in bad[:5]:
    print(f'  FAIL {cid}: {why}')
fails.extend(f'B {c}' for c, _ in bad)
check(not bad, f"B {len(doc['court'])} defects the existing vocabulary catches are refused by the forged court, with the declared message and code, the same on both runtimes ({len(bad)} differ)")

# ---- C -------------------------------------------------------------------------------------------------------------------
n0 = n_model.N(sentence, STUDY)
base = n_model.rules(n0, ledger_runner)
check(not base, f'C the unmutated sentence has no finding: {len(n0.decls)} declarations, every ledger query judged by the ledger\'s own court ({base[:1]})')
bad, unseen = [], 0
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, 'x.n')
    for c in doc['rules']:
        assert sentence.count(c['old']) == 1, (c['id'], sentence.count(c['old']))
        mutated = sentence.replace(c['old'], c['new'])
        open(p, 'w', encoding='utf-8', newline='').write(mutated)
        if not court(RNXC, ['n_court.ring', 'check', p]).startswith('ok'):
            bad.append((c['id'], 'the existing court already refuses it: this is not a rule of the next rung'))
            continue
        unseen += 1
        got = [x[0] for x in n_model.rules(n_model.N(mutated, STUDY), ledger_runner)]
        if c['code'] not in got:
            bad.append((c['id'], f"expected {c['code']}, got {sorted(set(got))}"))
for cid, why in bad[:5]:
    print(f'  FAIL {cid}: {why}')
fails.extend(f'C {c}' for c, _ in bad)
check(not bad, f"C {len(doc['rules'])} defects the existing court says `ok` to ({unseen} of them) are each caught by the rule that names them ({len(bad)} not)")

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
                out.append((c['id'], f"the study refused it as {recorded[c['id']]}, the model: {u.get('refused') or u.get('frame')}"))
            else:
                n_ok += 1
            continue
        if 'frame' not in u:
            out.append((c['id'], f"the study compiled it, the model refused it as {u['refused']} ({u['what']!r})"))
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
diffs, n_ok, split, n_pairs = judge(n0)
check(len(study) >= STUDY_FLOOR, f'D the study\'s fixtures hold {len(study)} questions, at or above the pinned floor of {STUDY_FLOOR}')
for cid, why in diffs[:6]:
    print(f'  FAIL D {cid}: {why}')
fails.extend(f'D {c}' for c, _ in diffs)
check(not diffs, f'D the model, from the sentence alone, reproduces the study on {n_ok} of {len(study)} questions: the closed query, the graph answer, the sentence told, the refusal kind ({len(diffs)} differ)')
check(not split and n_pairs >= PAIRS_FLOOR, f'D the meaning sequence is identical in English and French for {n_pairs - len(split)} of {n_pairs} pairs ({split[:3]})')

# ---- E -------------------------------------------------------------------------------------------------------------------
class NoGate(n_model.N):
    def gate(self, tongue, text):
        return None


ng = NoGate(sentence, STUDY)
d2, _, _, _ = judge(ng)
attacks = {c['id'] for c in study if c['group'] == 'attack'}
caught = {cid for cid, _ in d2 if cid in attacks}
check(len(caught) >= 10, f'E the comparison can fail: with the gate removed from the model it disagrees with the study on {len(caught)} of {len(attacks)} attacks')

print(f'n_check: {"FAIL" if fails else "PASS"} ({len(fails)} failure(s))')
sys.exit(1 if fails else 0)
