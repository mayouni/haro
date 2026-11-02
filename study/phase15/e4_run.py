"""Phase 1.5, E4: the retargeted question surface, judged.

Compiles every case of fixtures/questions.json through e4_pipeline.ring (stzNatural's architecture
retargeted, on the Ring++ package) and judges:

  G1  the closed target each question compiles to is the one composed by hand; a graph question's answer
      is the one composed by hand; a ledger question's answer is judged by THREE witnesses that must agree:
      the ledger's court (Haro's Z `ask`, on rnxc AND the oracle), zing itself (live), and an independent
      evaluation of the predicate over the ledger's rows, written here
  G2  one question in two languages compiles to the same closed target (the semantic core is shared)
  G3  the closure audit: no question is run as code (the canary), and the source of the answer path holds
      no eval / system / LoadLib
  G4  every question the language cannot understand is REFUSED, by name, in the words of its own language
  G5  the ledger's court refuses what is outside the grammar, so a wrong target cannot be answered
  G7  the compile stage gives the same bytes on the reference VM (official Ring 1.27, the author's engine) as on Ring++
  G6  the answer comes back in the language of the question: a graph answer as a sentence, a ledger answer in
      the voice the language declares (Haro v0.16's NARRATE; French is a second declaration), each equal to
      what was composed by hand or by rule from the independent evaluation

Usage: python haro/study/phase15/e4_run.py [--plant]     exit 1 on any failure.
"""
import json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voices

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
SPIKE = paths.SPIKE
PACKAGE_RNXC = os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
RNXC = paths.RNXC
ORACLE = paths.RING
OFFICIAL_RING = r'D:\ring127\bin\ring.exe'
STZLIB = r'D:\GitHub\stzlib\libraries\stzlib'
ZING = r'D:\GitHub\zing\cli\zig-out\bin\zing.exe'
ZING_EXAMPLE = r'D:\GitHub\zing\examples\bedrock-query'
ANSI = re.compile(r'\x1b\[[0-9;]*m')
PLANT = '--plant' in sys.argv

doc = json.load(open(os.path.join(HERE, 'fixtures', 'questions.json'), encoding='utf-8'))
Q = json.load(open(os.path.join(SPIKE, 'v07', 'q_cases.json'), encoding='utf-8'))
ROWS = Q['rows']
SENTENCE = 'tontine.z'

fails = []
notes = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def run(exe, args, cwd, env_extra=None):
    env = dict(os.environ)
    env['RNXC_NOCACHE'] = '1'
    env['HARO_NOCACHE'] = '1'
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([exe] + args, capture_output=True, cwd=cwd, env=env, timeout=600)
    return p.returncode, p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), p.stderr.decode('utf-8', 'replace')


# ---- 1. compile every question ------------------------------------------------------------------------------
os.makedirs(os.path.join(HERE, 'scratch'), exist_ok=True)
qfile = os.path.join(HERE, 'scratch', 'questions.txt')
with open(qfile, 'w', encoding='utf-8', newline='') as f:
    for c in doc['cases']:
        assert '|' not in c['id'] and '|' not in c['lang']
        f.write(f"{c['id']}|{c['lang']}|{c['text'].replace(chr(10), '~NL~')}\n")
env = dict(os.environ)
env.pop('RNXC_NOCACHE', None); env.pop('HARO_NOCACHE', None)      # the pipeline compiles Softanza once; the image is reused after
p = subprocess.run([PACKAGE_RNXC, 'e4_pipeline.ring', os.path.join('scratch', 'questions.txt')], capture_output=True, cwd=HERE, env=env, timeout=900)
out = p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
open(os.path.join(HERE, 'e4_result.txt'), 'w', encoding='utf-8', newline='').write(out)
res, ans, plan, says, canary = {}, {}, {}, {}, None
for line in out.split('\n'):
    f = line.split('\t')
    if f[0] == 'RESULT' and len(f) >= 6:
        res[f[1]] = {'kind': f[2], 'target': f[3], 'reason': f[4], 'frame': f[5]}
    elif f[0] == 'ANSWER' and len(f) >= 3:
        ans[f[1]] = [x for x in f[2].split(',') if x]
    elif f[0] == 'PLAN' and len(f) >= 4:
        plan[f[1]] = {'step1': [x for x in f[2].split(',') if x], 'zql': f[3]}
    elif f[0] == 'SAY' and len(f) >= 3:
        says[f[1]] = f[2]
    elif f[0] == 'CANARY':
        canary = int(f[1])
cases = doc['cases']
print(f'pipeline: exit {p.returncode}, {len(res)} of {len(cases)} questions compiled, canary={canary}')
check(p.returncode == 0 and len(res) == len(cases), f'the pipeline compiled all {len(cases)} questions (exit {p.returncode}, {len(res)} results)')

# ---- 2. the independent evaluator of a ledger predicate -----------------------------------------------------


def num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str) and re.fullmatch(r'-?\d+(\.\d+)?', v):
        return float(v)
    return None


def evaluate(zql):
    """The rows a ZQL question means, read by Python from the query's text alone."""
    m = re.fullmatch(r'SELECT \* FROM collect(?: WHERE (.*?))?(?: ORDER BY (\w+) (ASC|DESC))?(?: LIMIT (\d+))?', zql)
    assert m, f'the evaluator cannot read {zql!r}'
    cond, ofield, odir, limit = m.groups()
    rows = list(ROWS)
    if cond:
        keep = []
        for r in rows:
            ok = True
            for part in cond.split(' AND '):
                mm = re.fullmatch(r'amount ([<>]) (\d+)', part)
                if mm:
                    a = num(r.get('amount'))
                    ok = ok and a is not None and (a > int(mm.group(2)) if mm.group(1) == '>' else a < int(mm.group(2)))
                    continue
                mm = re.fullmatch(r'member = "(\w+)"', part)
                if mm:
                    ok = ok and r.get('member') == mm.group(1)
                    continue
                mm = re.fullmatch(r'round = (\d+)', part)
                if mm:
                    ok = ok and r.get('round') == int(mm.group(1))
                    continue
                raise AssertionError(f'the evaluator cannot read the condition {part!r}')
            if ok:
                keep.append(r)
        rows = keep
    if ofield:
        rows = sorted(rows, key=lambda r: (num(r.get(ofield)) if num(r.get(ofield)) is not None else float('-inf')), reverse=(odir == 'DESC'))
    if limit is not None:
        rows = rows[:int(limit)]
    return rows


# ---- 3. zing live ---------------------------------------------------------------------------------------------
zing_dir = None
if os.path.exists(ZING) and os.path.isdir(ZING_EXAMPLE):
    zing_dir = tempfile.mkdtemp(prefix='phase15-zing-')
    work = os.path.join(zing_dir, 'tontine')
    shutil.copytree(ZING_EXAMPLE, work)
    zenv = dict(os.environ)
    zenv['STZW_WIDTH'] = '200'

    def zing(args):
        r = subprocess.run([ZING] + args, cwd=work, capture_output=True, env=zenv, timeout=60)
        return r.returncode, ANSI.sub('', r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace'))
    for data, actor in Q['replay']:
        zing(['flow', 'collect', '--data', json.dumps(data), '--actor', actor])

    def zing_rows(zql):
        rc, o = zing(['query', zql])
        rows = []
        for line in o.splitlines():
            m = re.match(r'\s*#(\d+)\s+\S+ \S+\s+by \S+ -- (.*)$', line)
            if m:
                rows.append(json.loads(m.group(2)))
        return rc, rows
else:
    zing_rows = None

# ---- 4. G1 / G4 / G5: judge every case ------------------------------------------------------------------------
rows_json = json.dumps(ROWS)
court_cache = {}


def court(zql):
    if zql not in court_cache:
        r = subprocess.run([RNXC, 'z_court.ring', 'ask', SENTENCE, zql, rows_json], capture_output=True, cwd=SPIKE, env=dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1'), timeout=120)
        o = subprocess.run([ORACLE, 'z_court.ring', 'ask', SENTENCE, zql, rows_json], capture_output=True, cwd=SPIKE, env=dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1'), timeout=120)
        court_cache[zql] = (r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip(), o.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip())
    return court_cache[zql]


bad_target, bad_answer, bad_ledger, n_ledger, n_graph, n_plan, n_zing = [], [], [], 0, 0, 0, 0
refused_bad = []
n_refused = 0
for c in cases:
    cid, e, r = c['id'], c['expect'], res.get(c['id'])
    if r is None:
        bad_target.append((cid, 'no result'))
        continue
    if e['kind'] == 'refused':
        n_refused += 1
        fr = c['lang'] == 'tn-fr'
        named = bool(r['reason']) and r['kind'] == 'refused' and r['target'] == ''
        spoken = (('caractere' in r['reason'] or 'mot' in r['reason'] or 'forme' in r['reason']) if fr else
                  ('character' in r['reason'] or 'word' in r['reason'] or 'shape' in r['reason']))
        if not (named and spoken):
            refused_bad.append((cid, f"kind={r['kind']} reason={r['reason'][:80]!r}"))
        continue
    if r['kind'] != e['kind'] or r['target'] != e['target'] or r['frame'] != e['frame']:
        bad_target.append((cid, f"want {e['kind']} {e['target']!r}, got {r['kind']} {r['target']!r}"))
        continue
    if e['kind'] == 'graph':
        n_graph += 1
        if ans.get(cid) != e['answer']:
            bad_answer.append((cid, f"want {e['answer']}, got {ans.get(cid)}"))
    elif e['kind'] == 'plan':
        n_plan += 1
        pl = plan.get(cid)
        want_zql = e['target'].split(' => ')[1].replace('{MEMBER}', e['answer'][0].capitalize())
        if not pl or pl['step1'] != e['answer'] or pl['zql'] != want_zql:
            bad_answer.append((cid, f'plan: want {e["answer"]} then {want_zql!r}, got {pl}'))
            continue
        zql = pl['zql']
    else:
        zql = r['target']
    if e['kind'] in ('ledger', 'plan'):
        n_ledger += 1
        mine = evaluate(zql)
        rc_out, or_out = court(zql)
        try:
            got = json.loads(rc_out)
        except ValueError:
            bad_ledger.append((cid, f'the court did not answer: {rc_out[:80]!r}'))
            continue
        if rc_out != or_out:
            bad_ledger.append((cid, 'rnxc and the oracle differ on the court\'s answer'))
        if got != mine:
            bad_ledger.append((cid, f'the court answers {len(got)} row(s) {json.dumps(got)[:70]}, the independent evaluation {len(mine)} {json.dumps(mine)[:70]}'))
        if zing_rows:
            rc, zr = zing_rows(zql)
            n_zing += 1
            if zr != got:
                bad_ledger.append((cid, f'zing answers {len(zr)} row(s), the court {len(got)}'))
if PLANT:
    bad_target.append(('PLANT', 'planted'))
for lst, label in ((bad_target, 'targets'), (bad_answer, 'graph and plan answers'), (bad_ledger, 'ledger answers'), (refused_bad, 'refusals')):
    for cid, why in lst[:6]:
        print(f'  FAIL {label}: {cid}: {why}')
    fails.extend(f'{label}: {cid}' for cid, _ in lst)
non_ref = [c for c in cases if c['expect']['kind'] != 'refused']
print(f'  {"ok  " if not bad_target else "FAIL"} G1 targets: {len(non_ref) - len(bad_target)} of {len(non_ref)} questions compile to the closed query composed by hand')
print(f'  {"ok  " if not bad_answer else "FAIL"} G1 answers: {n_graph} graph questions and {n_plan} plans answered as composed by hand ({len(bad_answer)} differ)')
print(f'  {"ok  " if not bad_ledger else "FAIL"} G1 ledger: {n_ledger} ledger answers, each equal across the court on rnxc, the court on the oracle, an independent evaluation' + (f', and zing live ({n_zing})' if zing_rows else ' (zing not built here: skipped)') + f' ({len(bad_ledger)} differ)')

# ---- 5. G2: two languages, one meaning ------------------------------------------------------------------------
pairs = {}
for c in cases:
    if c['group'] == 'pair':
        pairs.setdefault(c['pair'], {})[c['lang']] = res.get(c['id'])
diff = [pid for pid, d in pairs.items() if not d.get('tn-en') or not d.get('tn-fr') or d['tn-en']['target'] != d['tn-fr']['target']]
check(not diff and len(pairs) >= 16, f'G2 {len(pairs) - len(diff)} of {len(pairs)} questions asked in English and in French compile to the SAME closed query ({diff[:3]})')

# ---- 6. G3: the closure audit ---------------------------------------------------------------------------------
n_attack = sum(1 for c in cases if c['group'] == 'attack')
attack_open = [c['id'] for c in cases if c['group'] == 'attack' and res.get(c['id'], {}).get('kind') != 'refused']
check(canary == 0 and not attack_open, f'G3 {n_attack} attacks on the answer path (brackets, calls, quotes, a second statement, a range, raw ZQL, a Ring global) all refused; the canary was called {canary} time(s)')
src = ''
for fn in ('nlq.ring', 'e4_pipeline.ring'):
    src += open(os.path.join(HERE, fn), encoding='utf-8').read() + '\n'
src_nocomment = '\n'.join(l.split('#', 1)[0] for l in src.splitlines())
forbidden = [w for w in ('eval(', 'system(', 'loadlib', 'execute(', 'call ', 'write(', 'fopen(', 'sysget(') if w in src_nocomment.lower()]
check(not forbidden, f'G3 the code of the answer path (nlq.ring, e4_pipeline.ring) holds none of eval, system, LoadLib, execute, call, write, fopen, sysget: found {forbidden}')

# ---- 7. G4: refusals ---------------------------------------------------------------------------------------------
check(not refused_bad, f'G4 {n_refused} questions the language cannot understand: each REFUSED, naming the word, the character or the shape, in the words of the question\'s own language ({len(refused_bad)} not)')

# ---- 7b. G3 control: the canary can fire -------------------------------------------------------------------------
# The same attack, with the gate removed (a scratch copy of nlq.ring whose NlqGate returns at once):
# the shipped tokenizer evals the bracketed section and the canary is called. A canary that cannot fire
# proves nothing when it stays at 0.
ctl = os.path.join(HERE, 'scratch', 'nogate')
shutil.rmtree(ctl, ignore_errors=True)
os.makedirs(os.path.join(ctl, 'data'))
nl = open(os.path.join(HERE, 'nlq.ring'), encoding='utf-8').read()
assert nl.count('func NlqGate cText\n') == 1
open(os.path.join(ctl, 'nlq.ring'), 'w', encoding='utf-8', newline='').write(nl.replace('func NlqGate cText\n', 'func NlqGate cText\n\treturn ""\n'))
shutil.copy(os.path.join(HERE, 'e4_pipeline.ring'), ctl)
shutil.copy(os.path.join(HERE, 'data', 'tontine.zknw'), os.path.join(ctl, 'data'))
open(os.path.join(ctl, 'q.txt'), 'w', encoding='utf-8', newline='').write('X01|tn-en|show deposits over [ Marker() ]\n')
env2 = dict(os.environ)
env2.pop('RNXC_NOCACHE', None); env2.pop('HARO_NOCACHE', None)
pc = subprocess.run([PACKAGE_RNXC, 'e4_pipeline.ring', 'q.txt'], capture_output=True, cwd=ctl, env=env2, timeout=900)
oc = pc.stdout.decode('utf-8', 'replace')
m = re.search(r'CANARY\t(\d+)', oc)
fired = int(m.group(1)) if m else -1
check(fired >= 1, f'G3 control: with the gate removed, the same attack calls the canary ({fired} time(s)): the canary can fire, so its 0 above means something')
shutil.rmtree(ctl, ignore_errors=True)

# ---- 8. G5: the court refuses what is outside the grammar --------------------------------------------------------
tampered = ['SELECT * FROM collect; DROP TABLE collect', 'SELECT * FROM collect WHERE amount > 5000 OR 1=1; --', 'DROP TABLE collect', 'SELECT member FROM collect']
refused_by_court = 0
for t in tampered:
    r = subprocess.run([RNXC, 'z_court.ring', 'ask', SENTENCE, t, rows_json], capture_output=True, cwd=SPIKE, env=dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1'), timeout=120)
    o = r.stdout.decode('utf-8', 'replace').strip()
    if not o.startswith('[') and o:
        refused_by_court += 1
check(refused_by_court == len(tampered), f'G5 the ledger\'s court refuses {refused_by_court} of {len(tampered)} tampered targets: a target outside the grammar is not answered')

# ---- 9. G6: the answer OUT, in the language of the question --------------------------------------------------------
voices.build()


def expected_narration(lang, zql):
    total = len(ROWS)
    m = re.fullmatch(r'(SELECT \* FROM collect(?: WHERE .*?)?)(?: ORDER BY (\w+) (ASC|DESC))?(?: LIMIT (\d+))?', zql)
    base, ofield, odir, limit = m.groups()
    matched = len(evaluate(base))
    rows = evaluate(zql)
    rj = json.dumps(rows, ensure_ascii=False)
    lines = []
    if lang == 'tn-en':
        lines.append(f'Asking collect: {zql}')
        lines.append(f'{matched} of the {total} rows match.')
        if ofield:
            lines.append(f'Ordered by {ofield} {odir}.')
        if limit is not None and matched > int(limit):
            lines.append(f'Only the first {int(limit)} are kept.')
        lines.append(f'The answer is {len(rows)} row(s): {rj}')
    else:
        lines.append(f'Question posée à collect : {zql}')
        lines.append(f'{matched} lignes sur {total} correspondent.')
        if ofield:
            lines.append(f'Triées par {ofield}, ordre {odir}.')
        if limit is not None and matched > int(limit):
            lines.append(f'Seules les {int(limit)} premières sont gardées ({matched - int(limit)} écartées).')
        lines.append(f'La réponse tient en {len(rows)} ligne(s) : {rj}')
    return '\n'.join(lines)


bad_say, bad_voice, n_say, n_voice = [], [], 0, 0
for c in cases:
    e = c['expect']
    if 'say' in e:
        n_say += 1
        if says.get(c['id']) != e['say']:
            bad_say.append((c['id'], f"want {e['say']!r}, got {says.get(c['id'])!r}"))
    if c['group'] == 'pair' and e['kind'] in ('ledger', 'plan'):
        zql = plan[c['id']]['zql'] if e['kind'] == 'plan' else res[c['id']]['target']
        want = expected_narration(c['lang'], zql)
        got_r = voices.tell(RNXC, c['lang'], zql, rows_json)
        got_o = voices.tell(ORACLE, c['lang'], zql, rows_json)
        n_voice += 1
        if got_r != want:
            bad_voice.append((c['id'], f'want {want[:90]!r}, got {got_r[:90]!r}'))
        elif got_r != got_o:
            bad_voice.append((c['id'], 'rnxc and the oracle tell it differently'))
for lst, label in ((bad_say, 'sentences'), (bad_voice, 'voices')):
    for cid, why in lst[:6]:
        print(f'  FAIL {label}: {cid}: {why}')
    fails.extend(f'{label}: {cid}' for cid, _ in lst)
print(f'  {"ok  " if not bad_say else "FAIL"} G6 {n_say} graph and plan answers told as a sentence in the language of the question, as composed by hand ({len(bad_say)} differ)')
print(f'  {"ok  " if not bad_voice else "FAIL"} G6 {n_voice} ledger answers told in the voice of the question\'s language (English: the spike\'s Z court; French: a second declaration), equal to the narration composed by rule from the independent evaluation, on rnxc and on the oracle ({len(bad_voice)} differ)')

# ---- 10. G7: the reference VM ----------------------------------------------------------------------------------------
# The same pipeline, unchanged but for the two load lines made absolute, on official Ring 1.27 and the author's
# own engine build, run from inside his tree (where the loader finds the engine). Read-only there.
if os.path.exists(OFFICIAL_RING) and os.path.isdir(STZLIB):
    wrapper = open(os.path.join(HERE, 'e4_pipeline.ring'), encoding='utf-8').read()
    wrapper = wrapper.replace('load "stzlib.ring"', 'load "' + STZLIB.replace(chr(92), '/') + '/stzlib.ring"')
    wrapper = wrapper.replace('load "nlq.ring"', 'load "' + HERE.replace(chr(92), '/') + '/nlq.ring"')
    wpath = os.path.join(HERE, 'scratch', 'e4_official.ring')
    open(wpath, 'w', encoding='utf-8', newline='').write(wrapper)
    po = subprocess.run([OFFICIAL_RING, wpath, qfile, os.path.join(HERE, 'data', 'tontine.zknw')], capture_output=True, cwd=STZLIB, timeout=900)
    oo = po.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    same = oo == out
    nd = sum(1 for x, y in zip(oo.split('\n'), out.split('\n')) if x != y)
    check(same and po.returncode == 0, f'G7 the whole compile stage gives the same {len(out.splitlines())} lines on official Ring 1.27 with the author\'s engine as on Ring++ (exit {po.returncode}, {nd} differ)')
else:
    print('  SKIP G7: official Ring 1.27 or the author\'s tree is not at its place')

if zing_dir:
    shutil.rmtree(zing_dir, ignore_errors=True)
print(f'e4: {"FAIL" if fails else "PASS"} ({len(fails)} failure(s))')
sys.exit(1 if fails else 0)
