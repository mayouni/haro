"""Haro v0.34 -- COMPASS-KERN-03's field check, judged: the forged Z court's `ask` verb on the sentences that declare their records' fields.

Three judges, on the court the guard forged from z_v34.haro (spike/z_court.haro), on `haro` and on its checked build, the two printing the same bytes (D41):

  the cases   v34/q_cases.json, written first: 18 questions with the answer or the refusal each must have, each refusal by the fragment of why; a case may also carry
              `speaks`, a fragment of the DECLARING LANGUAGE's own words (its unknown_seat refusal), which the refusal must end with
  the twin    a reference that shares nothing with the court's code: it reads tontine/records.z with regular expressions (the entities' field names, the flows' RECORDS, the
              steps' FLOW and COMPUTE), and for every flow x every candidate name x WHERE, ORDER BY and an aggregate decides by itself whether the question is lawful. The court
              must refuse exactly those it refuses and answer the rest (D43: a second evaluator must agree)
  the link    a flow whose RECORDS names no entity is refused by the references pass, before any question: records_dangling.z

  python spike/v34/ask_court.py [--plant]          (--plant switches one judge off and must fail the court)
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
import paths

HARO_VM, TWIN = paths.need_bins()


def run(exe, folder, args, timeout=120):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=timeout, cwd=folder)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip()


def ask(exe, folder, sentence, query, rows):
    return run(exe, folder, ['z_court.haro', 'ask', sentence, query, json.dumps(rows)])


def judge_case(c, out, rows_default):
    if 'refusal' in c:
        if out.startswith('[') or c['refusal'] not in out:
            return f'expected a refusal holding {c["refusal"]!r}, got {out[:160]}'
        if 'speaks' in c and c['speaks'] not in out:
            return f'the refusal does not speak in the declaring language\'s words ({c["speaks"]!r}): {out[:160]}'
        return ''
    try:
        got = json.loads(out)
    except json.JSONDecodeError:
        return f'not an answer: {out[:160]}'
    return '' if got == c['expect'] else f'expected {json.dumps(c["expect"])[:100]}, got {out[:160]}'


# ---- the twin: the sentence read by regular expressions, nothing of the court's code ------------------------------------------------------------
def read_world(path):
    text = open(path, encoding='utf-8').read()
    entities = {}
    for m in re.finditer(r'DEFINE ENTITY (\w+) AS \(\s*FIELDS \[(.*?)\]', text, re.S):
        entities[m.group(1)] = [p.split(':')[0].strip() for p in m.group(2).split(',') if ':' in p]
    flows = {m.group(1): m.group(2) for m in re.finditer(r'DEFINE FLOW (\w+) AS \(RECORDS (\w+)\)', text)}
    computed = {}
    for m in re.finditer(r'DEFINE STEP (\w+) AS \((.*?)\) RATIONALE', text, re.S):
        body = m.group(2)
        f = re.search(r'FLOW (\w+)', body)
        c = re.search(r'COMPUTE (\w+)', body)
        if f and c:
            computed.setdefault(f.group(1), []).append(c.group(1))
    return {f: entities[e] + [c for c in computed.get(f, []) if c not in entities[e]] for f, e in flows.items()}


CANDIDATES = ['id', 'member', 'amount', 'round', 'status', 'reponses', 'score', 'total', 'ammount', 'nope', 'member.first', 'nope.sub', 'score.x']
FORMS = (('WHERE', 'SELECT * FROM {f} WHERE {n} = 1'), ('ORDER BY', 'SELECT * FROM {f} ORDER BY {n}'), ('WHERE', 'SELECT * FROM {f} WHERE SUM({n}) > 0'))
LAWFUL_SPECIALS = ['SELECT * FROM {f} WHERE {first} CONTAINS "nope"', 'SELECT * FROM {f} WHERE "ammount" = "ammount"', 'SELECT * FROM {f} LIMIT 1']


def sweep(exe, folder, world, rows_of):
    bad = []
    n = 0
    for f, names in world.items():
        for cand in CANDIDATES:
            for clause, form in FORMS:
                q = form.format(f=f, n=cand)
                out = ask(exe, folder, 'tontine/records.z', q, rows_of[f])
                n += 1
                head = cand.split('.')[0]
                if head in names:
                    if not out.startswith('['):
                        bad.append(f'{q}: a declared name was refused: {out[:120]}')
                else:
                    want = f"{clause} names '{head}', which {f} does not declare"
                    if out.startswith('[') or want not in out:
                        bad.append(f'{q}: expected the refusal {want!r}, got {out[:120]}')
        for form in LAWFUL_SPECIALS:
            q = form.format(f=f, first=names[0])
            out = ask(exe, folder, 'tontine/records.z', q, rows_of[f])
            n += 1
            if not out.startswith('['):
                bad.append(f'{q}: lawful, but refused: {out[:120]}')
    return n, bad


def main():
    doc = json.load(open(os.path.join(HERE, 'q_cases.json'), encoding='utf-8'))
    rows = doc['rows']
    folder = SPIKE
    failures = 0
    outs = {}
    for label, exe in (('haro', HARO_VM), ('checked', TWIN)):
        bad = []
        for c in doc['cases']:
            out = ask(exe, folder, c['sentence'], c['query'], c['rows'] if 'rows' in c else rows)
            outs[(label, c['id'])] = out
            why = judge_case(c, out, rows)
            if PLANT and c['id'] == 'f07':
                why = 'PLANTED'
            if why:
                bad.append(f'{c["id"]} ({c["name"][:50]}): {why}')
        for b in bad:
            print(f'  FAIL {label}: {b}')
        failures += len(bad)
        print(f'  {"FAIL" if bad else "ok  "} the cases on {label}: {len(doc["cases"]) - len(bad)} of {len(doc["cases"])}')
    diff = [c['id'] for c in doc['cases'] if outs[('haro', c['id'])] != outs[('checked', c['id'])]]
    if diff:
        failures += 1
        print(f'  FAIL haro and its checked build print different bytes on {diff}')
    else:
        print(f'  ok   haro and its checked build print the same bytes on all {len(doc["cases"])} cases')
    world = read_world(os.path.join(SPIKE, 'tontine', 'records.z'))
    rows_of = {'collect': rows, 'indice': [{'reponses': '5,5,5', 'score': 100}]}
    if not (world.get('collect') and world.get('indice')):
        failures += 1
        print(f'  FAIL the twin could not read the world: {world}')
    else:
        n, bad = sweep(HARO_VM, folder, world, rows_of)
        for b in bad[:6]:
            print(f'  FAIL twin: {b}')
        failures += len(bad)
        print(f'  {"FAIL" if bad else "ok  "} the twin: {n} questions over {len(world)} flows, a regular-expression reading of the sentence decides each; the court agrees on {n - len(bad)}')
    # the link: a RECORDS that names nothing
    out = run(HARO_VM, folder, ['z_court.haro', 'check', 'tontine/records_dangling.z'])
    if "RECORDS 'ghost'" in out and 'resolves to nothing' in out:
        print('  ok   a flow whose RECORDS names no entity is refused by the references pass, before any question')
    else:
        failures += 1
        print(f'  FAIL a dangling RECORDS was not refused: {out[:160]}')
    print(f'ASK COURT (v0.34): {"FAIL" if failures else "PASS"} ({failures} failure(s))')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
