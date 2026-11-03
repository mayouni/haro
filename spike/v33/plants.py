"""Every protection of INCLUDES, ON a FORM, EXCEPT, the quantifier over a FORM and the condition printer switched off in turn: the guard must fail, for the fixture
that protection exists for (the W discipline: each protection load-bearing).

Each plant is one or two text substitutions in a COPY of haro_lib.haro or form_expand.haro in a temporary folder that holds copies of every file a run needs; no file
of the spike is changed. For each plant the folder is judged on the Haro VM by:
  the meta fixtures    the 28+ of v33/fixtures.json (accepts by their counts, rejects by the fragment of why)
  the court cases      medium_v33.haro forged in the folder, then each case of v33/court_cases.json
  the twin             v33/medium_expanded.haro forged in the folder: its court and grammar must equal the sugar's byte for byte
  the printer          every condition of the repository through CondPrint (v33/cond_court.py), parse -> print -> parse
The judge must pass the unplanted folder first, or the script stops. Printed is CAUGHT with what failed, or MISSED: a protection no fixture pins, and the answer to
it is a fixture, written before the protection is touched (as A11, A12 and R19 were, found by exactly this script).

  python spike/v33/plants.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]                       # never --plant here
import paths
import cond_court as cc

HARO_VM, _ = paths.need_bins()
NL, T = '\n', '\t'
CODE_FILES = ['haro.haro', 'haro_lib.haro', 'forge.haro', 'court_lib.haro', 'cond_lib.haro', 'block_lib.haro', 'pattern_lib.haro', 'pattern_judge.haro',
              'world_stub.haro', 'form_expand.haro', 'cond_rt.haro', 'medium_v33.haro']


def run(folder, args, timeout=120):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([HARO_VM] + args, capture_output=True, env=env, timeout=timeout, cwd=folder)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT\n'
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


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


def judge(folder, conds, hand_from):
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
    for gen in ('medium_court.haro', 'medium.gbnf'):
        if os.path.exists(os.path.join(folder, gen)):
            os.remove(os.path.join(folder, gen))
    forged = run(folder, ['forge.haro', 'medium_v33.haro', '.'])
    cases = json.load(open(os.path.join(HERE, 'court_cases.json'), encoding='utf-8'))['cases']
    if not forged.startswith('forged medium'):
        failed += [c['id'] for c in cases]
    else:
        for c in cases:
            verb = c['verb']
            out = run(folder, ['haro.haro'] + c['args'] if verb == 'meta' else ['medium_court.haro', verb] + c['args'])
            lines = [l for l in out.split('\n') if l]
            first = lines[0] if lines else ''
            good = ('first' not in c or c['first'] in first) and (not c.get('refused') or not first.startswith('ok'))
            if 'counts' in c:
                f = fields(out)
                good = good and out.startswith('ok') and all(f.get('count ' + k) == str(v) for k, v in c['counts'].items())
            good = good and all(x in out for x in c.get('contains', [])) and not any(x in out for x in c.get('lacks', []))
            if 'diagnose' in c:
                try:
                    d = json.loads(out)['diagnostics'][0]
                except (ValueError, KeyError, IndexError, TypeError):
                    d = {}
                want = c['diagnose']
                good = good and d.get('code') == want['code'] and d.get('cites') == want['cites']
            if not good:
                failed.append(c['id'])
        out_dir = os.path.join(folder, 'twin_out')
        os.makedirs(out_dir, exist_ok=True)
        for gen in ('medium_court.haro', 'medium.gbnf'):
            if os.path.exists(os.path.join(out_dir, gen)):
                os.remove(os.path.join(out_dir, gen))
        run(folder, ['forge.haro', 'v33/medium_expanded.haro', 'twin_out'])
        for gen in ('medium_court.haro', 'medium.gbnf'):
            a = open(os.path.join(folder, gen), 'rb').read() if os.path.exists(os.path.join(folder, gen)) else b'1'
            b = open(os.path.join(out_dir, gen), 'rb').read() if os.path.exists(os.path.join(out_dir, gen)) else b'2'
            if a != b:
                failed.append('TWIN:' + gen)
    cc.CWD = folder
    bad = cc.judge(conds, hand_from, builds=(('haro', None),), quiet=True)[1]
    if bad:
        failed.append('PRINTER x%d' % len(bad))
    return failed


def plants():
    P = []

    def add(label, fname, old, new):
        P.append((label, fname, old if isinstance(old, list) else [old], new if isinstance(new, list) else [new]))
    H, E = 'haro_lib.haro', 'form_expand.haro'
    # ---- the meta-court's clauses and record
    add('INCLUDES is a clause of DECLARATION', H, '["INCLUDES", "namelist"], ', '')
    add('EXCEPT is a clause of CONSTRAINT', H, '["EXCEPT", "namelist"], ', '')
    add('a declaration keeps what it includes', H, 'aMsgs, aCodes, aInc]', 'aMsgs, aCodes, []]')
    add('a constraint keeps what it excepts', H, 'cCnSev, aCnExc]', 'cCnSev, []]')
    add('INCLUDES is resolved before any pass reads a kind\'s seats', H, T + 'aDeclarations = StzuExpandIncludes(aDeclarations, aForms, aDeclared)' + NL, '')
    add('ON a FORM and the quantifier are resolved', H, T + 'aConstraints = StzuExpandConstraints(aConstraints, aFormTab, aDeclarations, aDeclared)' + NL, '')
    add('a VIEW\'s WHERE is resolved', H, T + 'aViews = StzuExpandViews(aViews, aFormTab, aDeclarations)' + NL, '')
    # ---- INCLUDES
    add('INCLUDES names something that exists (R1)', E, 'if cK = "" StzuFail(aDecls[i][5], "INCLUDES: \'', 'if 0 StzuFail(aDecls[i][5], "INCLUDES: \'')
    add('INCLUDES names a FORM (R2)', E, 'if cK != "FORM" StzuFail(aDecls[i][5], "INCLUDES must name', 'if 0 StzuFail(aDecls[i][5], "INCLUDES must name')
    add('INCLUDES names a FORM once (R3)', E, 'if aInc[m] = cF StzuFail(', 'if 0 StzuFail(')
    add('a seat comes once: from two FORMs (R5)', E, T * 6 + 'if aNew[q][1] = aFS[m][1]', T * 6 + 'if 0')
    add('a seat comes once: from a FORM and from the kind\'s own SEATS (R4)', E, T * 5 + 'if aNew[q][1] = aOwn[m][1]', T * 5 + 'if 0')
    add('a kind takes the seats of what it includes', E, 'aDecls[i][3] = aNew', 'aDecls[i][3] = aDecls[i][3]')
    # ---- ON a FORM, EXCEPT
    add('a constraint ON a FORM is named <constraint>_<kind>', E, 'cNm = aC[1] + "_" + aKinds[k]', 'cNm = aC[1] + "_x"')
    add('the name a constraint ON a FORM makes may not be a declared one (R10)', E, 'if DeclaredKind(aDeclared, cNm) != "" or StzuNameIn(cNm, aOut)', 'if StzuNameIn(cNm, aOut)')
    add('EXCEPT skips the kinds it names (A9, M17)', E, 'if not InStrList(aKinds[k], aExc) aKept + aKinds[k] ok', 'aKept + aKinds[k]')
    add('EXCEPT names something that exists (R15)', E, 'if DeclaredKind(aDeclared, aExc[e]) = "" StzuFail(', 'if 0 StzuFail(')
    add('EXCEPT names a kind that includes the FORM (R16)', E, 'if not InStrList(aExc[e], aKinds) StzuFail(', 'if 0 StzuFail(')
    add('EXCEPT names a kind once (R17)', E, 'if aExc[m] = aExc[e] StzuFail(', 'if 0 StzuFail(')
    add('EXCEPT leaves a kind (R18)', E, 'if len(aKept) = 0 StzuFail(', 'if 0 StzuFail(')
    add('EXCEPT belongs to a constraint ON a FORM (R14)', E, 'if len(aExc) > 0 and cOnKind != ""', 'if 0')
    # ---- the quantifier over a FORM
    add('some, all, earlier range over the kinds that include the FORM', E, T + T + 'if nF > 0' + NL + T * 3 + '$bFormChanged = 1' + NL + T * 3 + 'aNodes = []' + NL + T * 3 + 'for j = 1 to len(aTab[nF][2])' + NL + T * 4 + 'aP = ',
        T + T + 'if nF > 99' + NL + T * 3 + '$bFormChanged = 1' + NL + T * 3 + 'aNodes = []' + NL + T * 3 + 'for j = 1 to len(aTab[nF][2])' + NL + T * 4 + 'aP = ')
    add('exists ranges over the kinds that include the FORM', E, T + 'if k = "exists"' + NL + T + T + 'nF = StzuFormAt(aTab, aAst[2])' + NL + T + T + 'if nF > 0', T + 'if k = "exists"' + NL + T + T + 'nF = StzuFormAt(aTab, aAst[2])' + NL + T + T + 'if nF > 99')
    add('a name that is a seat of the constraint\'s kind keeps its meaning (A7)', E, T * 3 + 'if not isNull(StzuSeatNamed(StzuSeatsOf(aDecls, cOn), cHead)) nF = 0 ok' + NL, '')
    add('all is the and of its kinds', E, 'if aAst[2] = "all" cOp = "and" ok', '')
    add('a where is expanded too (A11)', E, 'if not isNull(aCond) aCond = StzuFormAst(aCond, cOn, aTab, aDecls) ok', '')
    add('a condition with nothing to expand is stored as written', E, 'if not $bFormChanged return cCond ok', '')
    add('an unreadable condition is the validator\'s to speak of (R19)', E, 'if cErr != "" return cCond ok', '')
    # ---- the printer
    add('a quantifier prints in parentheses', E, ['c = "(" + aAst[2] + " " + CondPathText(aAst[3])', 'return c + ")"' + NL + T + 'ok' + NL + T + 'if k = "cmp"'],
        ['c = aAst[2] + " " + CondPathText(aAst[3])', 'return c' + NL + T + 'ok' + NL + T + 'if k = "cmp"'])
    add('an or under an and is parenthesised', E, 'if nCtx > 1 return "(" + c + ")" ok', '')
    add('an and under an and\'s right is parenthesised', E, 'if nCtx > 2 return "(" + c + ")" ok', '')
    add('a not parenthesises what it negates', E, 'if k = "not" return "not " + CondPrintP(aAst[2], 3) ok', 'if k = "not" return "not " + CondPrintP(aAst[2], 0) ok')
    add('a value that is not a bare word is quoted', E, 'if bBare and CondIsBareWord(cV) and cV != "this" and cV != "self" return cV ok', 'return cV')
    add('the right of a relation is a place unless quoted', E, 'CondPathText(aAst[3]) + " " + aAst[2] + " " + CondPrintRight(aAst[4], 0)', 'CondPathText(aAst[3]) + " " + aAst[2] + " " + CondPrintRight(aAst[4], 1)')
    return P


def main():
    rep, _ = cc.corpus()
    conds = rep + cc.HAND
    with tempfile.TemporaryDirectory() as td:
        for name in CODE_FILES:
            shutil.copyfile(os.path.join(SPIKE, name), os.path.join(td, name))
        shutil.copytree(os.path.join(SPIKE, 'medium'), os.path.join(td, 'medium'))
        os.makedirs(os.path.join(td, 'v33'))
        shutil.copyfile(os.path.join(HERE, 'medium_expanded.haro'), os.path.join(td, 'v33', 'medium_expanded.haro'))
        base = judge(td, conds, len(rep))
        if base:
            print('the unplanted folder fails the judge on', base, '-- fix that first')
            return 1
        meta = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
        nmeta = len(meta['accepts']) + len(meta['rejects'])
        print(f'the unplanted folder passes the judge: {nmeta} meta fixtures, 18 court cases, the twin, and {len(conds)} conditions through the printer')
        caught = 0
        P = plants()
        for label, fname, olds, news in P:
            src = open(os.path.join(SPIKE, fname), encoding='utf-8', newline='').read()
            planted = src
            for old, new in zip(olds, news):
                if planted.count(old) != 1:
                    print(f'ANCHOR {label}: {planted.count(old)} matches in {fname} for {old[:60]!r}')
                    return 2
                planted = planted.replace(old, new)
            with open(os.path.join(td, fname), 'w', encoding='utf-8', newline='') as fh:
                fh.write(planted)
            failed = judge(td, conds, len(rep))
            shutil.copyfile(os.path.join(SPIKE, fname), os.path.join(td, fname))
            caught += bool(failed)
            print(('CAUGHT ' if failed else 'MISSED ') + label + (' -- ' + ', '.join(failed[:9]) + (' ...' if len(failed) > 9 else '') if failed else ''), flush=True)
        print(f'PLANTS: {caught} of {len(P)} protections load-bearing')
        return len(P) - caught


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
