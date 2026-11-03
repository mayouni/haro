"""Every protection of the field check (COMPASS-KERN-03) switched off in turn: the guard must fail, for the fixture that protection exists for (the W discipline).

Each plant is one or two text substitutions in a COPY of haro_lib.haro, forge.haro or ask_lib.haro in a temporary folder that holds copies of every .haro file of the spike
and the sentences; no file of the spike is changed. For each plant the folder is judged on the Haro VM by:
  the meta fixtures    v34/fixtures.json: FIELDS accepted and refused, each refusal by the fragment of why
  the cases            Z forged from z_v34.haro in the folder, then the questions of v34/q_cases.json on tontine/records.z (the answers, the refusals, the language's own words)
The judge must pass the unplanted folder first, or the script stops. Printed is CAUGHT with what failed, or MISSED: a protection no fixture pins, and the answer to it is a
fixture, written before the protection is touched (f16 to f19 and `speaks` were found by exactly this script).

  python spike/v34/plants.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
sys.argv = [sys.argv[0]]                       # never --plant here
import paths

HARO_VM, _ = paths.need_bins()
NL, T = '\n', '\t'


def run(folder, args, timeout=120):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([HARO_VM] + args, capture_output=True, env=env, timeout=timeout, cwd=folder)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip()


def fields(out):
    f = {}
    for line in out.split('\n')[1:]:
        k, _, v = line.partition(' ')
        if k == 'count':
            verb, _, n = v.partition(' ')
            f['count ' + verb] = n
        elif k:
            f[k] = v
    return f


def judge(folder):
    failed = []
    meta = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    with tempfile.TemporaryDirectory() as td:
        for case in meta['accepts'] + meta['rejects']:
            p = os.path.join(td, case['id'] + '.haro')
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(case['source'])
            out = run(folder, ['haro.haro', p])
            if 'refusal' in case:
                good = (not out.startswith('ok')) and case['refusal'] in out
            else:
                f = fields(out)
                good = out.startswith('ok') and f.get('language') == case['expect']['language'] and all(f.get(k) == str(v) for k, v in case['expect']['counts'].items())
            if not good:
                failed.append(case['id'])
    for gen in ('z_court.haro', 'z.gbnf', 'z_expr.haro', 'z_expr.gbnf', 'z_ask.gbnf'):
        if os.path.exists(os.path.join(folder, gen)):
            os.remove(os.path.join(folder, gen))
    forged = run(folder, ['forge.haro', 'z_v34.haro', '.'])
    doc = json.load(open(os.path.join(HERE, 'q_cases.json'), encoding='utf-8'))
    if not forged.startswith('forged z'):
        return failed + [c['id'] for c in doc['cases']]
    for c in doc['cases']:
        rows = c['rows'] if 'rows' in c else doc['rows']
        out = run(folder, ['z_court.haro', 'ask', c['sentence'], c['query'], json.dumps(rows)])
        if 'refusal' in c:
            good = (not out.startswith('[')) and c['refusal'] in out and c.get('speaks', '') in out
        else:
            try:
                good = json.loads(out) == c['expect']
            except ValueError:
                good = False
        if not good:
            failed.append(c['id'])
    return failed


def plants():
    P = []

    def add(label, fname, old, new):
        P.append((label, fname, old if isinstance(old, list) else [old], new if isinstance(new, list) else [new]))
    H, F, A = 'haro_lib.haro', 'forge.haro', 'ask_lib.haro'
    # ---- the meta-court
    add('FIELDS is a clause of ASK', H, '["FIELDS", "path"], ', '')
    add('FIELDS is written seat.seat (R6)', H, 'FIELDS is written seat.seat")', 'FIELDS")')
    add('the ASK keeps its FIELDS', H, 'cRationale, nLine, cAskFields]', 'cRationale, nLine, ""]')
    add('FIELDS names a seat of the kind asked (R1)', H, 'if isNull(aFSeat) StzuFail(', 'if isNull(aFSeat) loop ok if 0 StzuFail(')
    add('the seat is one reference, not a list (R2)', H, 'if aFSeat[3] StzuFail(', 'if 0 StzuFail(')
    add('the seat refers to a declaration (R3)', H, 'if DeclaredKind(aDeclared, aFSeat[2]) != "DECLARATION"', 'if 0')
    add('the second seat is a seat of that declaration (R4)', H, 'if isNull(aFSeat2) StzuFail(', 'if isNull(aFSeat2) loop ok if 0 StzuFail(')
    add('the second seat is a list of name: type pairs (R5)', H, 'if not StzuIsPairListSeat(aFSeat2, aDeclared, aForms)', 'if 0')
    add('every kind asked has the seat (R7)', H, 'for i = 1 to len(aFrom)' + NL + T * 5 + 'aFSeat = ', 'for i = 1 to 1' + NL + T * 5 + 'aFSeat = ')
    # ---- the forge and the court
    add('the forge hands the court the FIELDS path', F, 'if aAsk[7] != "" cAsk += ", " + RingStr(aAsk[7]) ok', '')
    add('the check is made', A, '\tAskCheckFields(aDecls, aFromDecl, aWhere, cField)' + NL, '')
    add('a WHERE that names an undeclared field is refused', A, 'if not CtInList(AskHead(aRefs[i]), aNames) AskFieldFail("WHERE"', 'if 0 AskFieldFail("WHERE"')
    add('an ORDER BY that names an undeclared field is refused', A, 'if cField != "" and not CtInList(AskHead(cField), aNames) AskFieldFail(', 'if 0 AskFieldFail(')
    add('a dotted name is judged by its head, in ORDER BY', A, 'not CtInList(AskHead(cField), aNames)', 'not CtInList(cField, aNames)')
    add('a dotted name is judged by its head, in WHERE', A, 'if not CtInList(AskHead(aRefs[i]), aNames) AskFieldFail("WHERE"', 'if not CtInList(aRefs[i], aNames) AskFieldFail("WHERE"')
    add('what a step computes is a field of its flow\'s records', A, 'if bThis and cComputed != "" and not', 'if 0 and cComputed != "" and not')
    add('a step computes into ITS flow\'s records only', A, 'if aSC[i][1] = cThr and aSC[i][3][2] = aFromDecl[2] bThis = 1 ok', 'if aSC[i][1] = cThr bThis = 1 ok')
    add('the fields are those of the entity the flow\'s records are', A, '\t\tif aDecls[d][2] != cEntity loop ok' + NL, '')
    add('a flow that writes no RECORDS is not checked', A, 'if cEntity = "" return [] ok', 'if cEntity = "" return ["id"] ok')
    add('the refusal speaks the declaring language\'s words', A, 'cMsg = CtRefusalMessage("unknown_seat")', 'cMsg = ""')
    add('the refusal says what the declaration does have', A, 'does not declare (its fields: " + CtJoin(aNames, ", ") + ")"', 'does not declare"')
    return P


def main():
    with tempfile.TemporaryDirectory() as td:
        for name in os.listdir(SPIKE):
            if name.endswith('.haro'):
                shutil.copyfile(os.path.join(SPIKE, name), os.path.join(td, name))
        os.makedirs(os.path.join(td, 'tontine'))
        shutil.copyfile(os.path.join(SPIKE, 'tontine.z'), os.path.join(td, 'tontine.z'))
        for name in ('records.z', 'records_dangling.z'):
            shutil.copyfile(os.path.join(SPIKE, 'tontine', name), os.path.join(td, 'tontine', name))
        base = judge(td)
        if base:
            print('the unplanted folder fails the judge on', base, '-- fix that first')
            return 1
        meta = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
        ncase = len(json.load(open(os.path.join(HERE, 'q_cases.json'), encoding='utf-8'))['cases'])
        print(f'the unplanted folder passes the judge: {len(meta["accepts"]) + len(meta["rejects"])} meta fixtures and {ncase} questions')
        caught = 0
        P = plants()
        for label, fname, olds, news in P:
            src = open(os.path.join(SPIKE, fname), encoding='utf-8', newline=None).read()
            planted = src
            for old, new in zip(olds, news):
                if planted.count(old) != 1:
                    print(f'ANCHOR {label}: {planted.count(old)} matches in {fname} for {old[:60]!r}')
                    return 2
                planted = planted.replace(old, new)
            with open(os.path.join(td, fname), 'w', encoding='utf-8', newline='') as fh:
                fh.write(planted)
            failed = judge(td)
            shutil.copyfile(os.path.join(SPIKE, fname), os.path.join(td, fname))
            caught += bool(failed)
            print(('CAUGHT ' if failed else 'MISSED ') + label + (' -- ' + ', '.join(failed[:9]) + (' ...' if len(failed) > 9 else '') if failed else ''), flush=True)
        print(f'PLANTS: {caught} of {len(P)} protections load-bearing')
        return len(P) - caught


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
