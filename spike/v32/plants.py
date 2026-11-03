"""Every protection of DEFINE PATTERN switched off in turn: the guard must fail, for the fixture that protection exists for (the W discipline:
each protection load-bearing).

Each plant is one text substitution in a COPY of one library (haro_lib.haro, forge.haro or pattern_judge.haro) in a temporary folder that holds
copies of every file a run needs; no file of the spike is changed. For each plant the folder is judged by a compact judge over the SAME fixtures
the guard uses -- the 33 meta fixtures of v32/fixtures.json (accepts by their counts, rejects by the fragment of why) and the 16 court cases of
v32/court_cases.json (the grants court forged in the folder, then each case run) -- on the Haro VM. The judge must pass the unplanted folder
first, or the script stops. Printed is CAUGHT with the fixtures that failed, or MISSED: a protection no fixture pins, and the answer to it is a
fixture, written before the protection is touched (as R26, R27, G15 and G16 were, found by reading the code that is planted here and by planting it off).

  python spike/v32/plants.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
import paths

HARO_VM, _ = paths.need_bins()
NL = '\n'
CODE_FILES = ['haro.haro', 'haro_lib.haro', 'forge.haro', 'court_lib.haro', 'cond_lib.haro', 'block_lib.haro', 'pattern_lib.haro',
              'pattern_judge.haro', 'world_stub.haro', 'grants_v32.haro']


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


def judge(folder):
    """The ids of the fixtures and cases that fail in this folder."""
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
                good = out.startswith('ok') and f.get('language') == case['expect']['language'] and \
                    all(f.get(k) == str(v) for k, v in case['expect']['counts'].items())
            if not good:
                failed.append(case['id'])
    for gen in ('grants_court.haro', 'grants.gbnf'):
        if os.path.exists(os.path.join(folder, gen)):
            os.remove(os.path.join(folder, gen))
    forged = run(folder, ['forge.haro', 'grants_v32.haro', '.'])
    cases = json.load(open(os.path.join(HERE, 'court_cases.json'), encoding='utf-8'))['cases']
    if not forged.startswith('forged grants'):
        return failed + [c['id'] for c in cases]
    for c in cases:
        verb = c['verb']
        out = run(folder, ['haro.haro'] + c['args'] if verb == 'meta' else ['grants_court.haro', verb] + c['args'])
        lines = [l for l in out.split('\n') if l]
        first = lines[0] if lines else ''
        good = True
        if 'first' in c and c['first'] not in first:
            good = False
        if c.get('refused') and first.startswith('ok'):
            good = False
        if 'counts' in c:
            f = fields(out)
            good = good and out.startswith('ok') and all(f.get('count ' + k) == str(v) for k, v in c['counts'].items())
        good = good and all(frag in out for frag in c.get('contains', [])) and not any(frag in out for frag in c.get('lacks', []))
        if 'diagnose' in c:
            try:
                d = json.loads(out)['diagnostics'][0]
            except (ValueError, KeyError, IndexError, TypeError):
                d = {}
            want = c['diagnose']
            good = good and d.get('code') == want['code'] and d.get('cites') == want['cites'] and ('severity' not in want or d.get('severity') == want['severity'])
        if not good:
            failed.append(c['id'])
    return failed


def plants():
    P = []

    def add(label, fname, old, new):
        P.append((label, fname, old, new))
    # ---- the meta-court: haro_lib.haro
    H = 'haro_lib.haro'
    add('PATTERN is a kind of declaration (every accept)', H, '"UNDERSTAND", "CONSTITUTION", "PATTERN"])', '"UNDERSTAND", "CONSTITUTION"])')
    add('OVER is required (R17)', H, 'return ["OVER", "MATCH", "MESSAGE"]', 'return ["MATCH", "MESSAGE"]')
    add('MATCH is required (R18)', H, 'return ["OVER", "MATCH", "MESSAGE"]', 'return ["OVER", "MESSAGE"]')
    add('MESSAGE is required (R26)', H, 'return ["OVER", "MATCH", "MESSAGE"]', 'return ["OVER", "MATCH"]')
    add("a rule opens with a bracket (R5)", H, "t0 = StzuExpect(\"lbracket\", \"'[': a rule is written [ ... ]\")", 't0 = StzuPeek()')
    add('a rule that is never closed is refused (R6)', H, '\t\tif t[1] = "eof"' + NL + '\t\t\tStzuFail(t0[3], "a rule is not closed', '\t\tif 0' + NL + '\t\t\tStzuFail(t0[3], "a rule is not closed')
    add('a rule with both quote marks is refused (R22)', H, "if substr(cOut, '\"') > 0 and substr(cOut, \"'\") > 0", 'if 0')
    add('OVER names a seat as declaration.seat (R4)', H, "StzuExpect(\"dot\", \"'.' after the declaration: OVER names a seat as declaration.seat\")", 'StzuPeek()')
    add('SEVERITY is error or warning (R19)', H, "if cPSev != \"error\" and cPSev != \"warning\"" + NL + "\t\t\t\t\t\tStzuFail(nLine, \"'\" + cPSev + \"' is not a SEVERITY of a PATTERN", "if 0" + NL + "\t\t\t\t\t\tStzuFail(nLine, \"'\" + cPSev + \"' is not a SEVERITY of a PATTERN")
    add('OVER resolves to a declaration of the language (R1)', H, '\t\t\tif cK = "" StzuFail(aP[7], "OVER:', '\t\t\tif 0 StzuFail(aP[7], "OVER:')
    add('OVER names a DECLARATION (R2)', H, '\t\t\tif cK != "DECLARATION" StzuFail(aP[7], "OVER must name', '\t\t\tif 0 StzuFail(aP[7], "OVER must name')
    add('OVER names a seat the declaration has (R3)', H, '\t\t\tif isNull(StzuSeatNamed(StzuSeatsOf(aDeclarations, aP[2]), aP[3]))', '\t\t\tif 0')
    add('SETS resolves to a declaration (R13)', H, '\t\t\t\tif cK = "" StzuFail(aPS[j][4], "SETS:', '\t\t\t\tif 0 StzuFail(aPS[j][4], "SETS:')
    add('SETS names a seat the declaration has (R14)', H, '\t\t\t\tif isNull(StzuSeatNamed(StzuSeatsOf(aDeclarations, aPS[j][1]), aPS[j][2]))', '\t\t\t\tif 0')
    add('a set is not named like a MENU or a kind (R15)', H, '\t\t\t\tif cSK != "" StzuFail(', '\t\t\t\tif 0 StzuFail(')
    add('a set has one declaration (R16)', H, '\t\t\t\tif InStrList(aPS[j][3], aSetSeen) StzuFail(', '\t\t\t\tif 0 StzuFail(')
    add("the pattern engine judges the rules: the bound and the names (R7-R12)", H, '\t\t\tPatDeclare(aPN, aPT, aPSN, aPSM)', '\t\t\tcPErr = ""')
    add('a set draws from words, strings and numbers: a list of pairs is refused (R27)', H, '\t\t\t\tif StzuIsPairListSeat(aSetSeat, aDeclared, aForms)', '\t\t\t\tif 0')
    add('a MENU is a set under its own name (A2)', H, '\t\tfor i = 1 to len(aMenus)' + NL + '\t\t\taPSN + aMenus[i][1]' + NL + '\t\t\taPSM + []' + NL + '\t\tnext' + NL, '')
    add('Art. 1: a pattern carries a CODE (R25)', H, '\t\t\t\t\t\tif aPatterns[j][8] = ""', '\t\t\t\t\t\tif 0')
    add('the printed record counts the patterns (every accept)', H, 'if len(aPaL) > 0 ? "patterns " + len(aPaL) ok', 'if 0 ? "" ok')
    add('a pattern\'s CODE and CITES are judged as an element\'s (R20, R23)', H, 'StzuCodeOf(aClauses, nLine, cName), StzuCitesOf(aClauses, nLine, cName), cPSev]', '"", [], cPSev]')
    # ---- the forge: forge.haro
    F = 'forge.haro'
    add('the patterns ride into the court (the 24th element)', F, '\tif cPatterns = ""' + NL + '\t\tc += "    " + cUnderstand + nl', '\tif 1' + NL + '\t\tc += "    " + cUnderstand + nl')
    add('the court loads the pattern engine where a language declares one', F, "\t\tc += 'load \"pattern_lib.haro\"' + nl" + NL, '')
    add('the court loads the pattern judge where a language declares one', F, "\t\tc += 'load \"pattern_judge.haro\"' + nl" + NL, '')
    add("a pattern's sets ride into the court", F, '\t\t\t\tif len(aSetRows) > 0', '\t\t\t\tif 0')
    add("a pattern's severity rides into the court (G9)", F, 'RingStr(aPt[i][10])', 'RingStr("error")')
    add("a pattern's cites ride into the court (G4)", F, 'CitesSource(aPt[i][9])', '"[]"')
    # ---- the court: pattern_judge.haro
    J = 'pattern_judge.haro'
    add('a set is the UNION of the values across declarations (G11)', J, '\tfor j = 1 to len(aDecls)' + NL + '\t\tif aDecls[j][1] != aK[1] loop ok' + NL + '\t\tif CtIsBroken(j) loop ok' + NL + '\t\taCl = CtClauseNamed(aDecls[j], cClause)',
        '\tfor j = 1 to 1' + NL + '\t\tif aDecls[j][1] != aK[1] loop ok' + NL + '\t\tif CtIsBroken(j) loop ok' + NL + '\t\taCl = CtClauseNamed(aDecls[j], cClause)')
    add("the language's MENUs are sets under their names (G7)", J, '\tfor i = 1 to len($aCourtMenus)' + NL + '\t\taSetN + $aCourtMenus[i][1]' + NL + '\t\taSetM + $aCourtMenus[i][2]' + NL + '\tnext' + NL, '')
    add('a seat the sentence does not write is not judged (G12)', J, '\t\t\tif isNull(aCl) loop ok' + NL + '\t\t\tcText', '\t\t\tcText')
    add('the value judged is the seat as written: its span (G3)', J, 'aCl[3][4] - aCl[3][3])', 'aCl[3][4] - aCl[3][3] + 1)')
    add('a declaration the structural court refused is not judged again (G15)', J, '\t\t\tif aD[1] != aK[1] loop ok' + NL + '\t\t\tif CtIsBroken(j) loop ok', '\t\t\tif aD[1] != aK[1] loop ok')
    add('CITES none: the envelope cites nothing (G8)', J, '\t\t\tif isString(aP[9])' + NL + '\t\t\t\taCC[2] = []', '\t\t\tif 0' + NL + '\t\t\t\taCC[2] = []')
    add('declared CITES replace the default (G4)', J, '\t\t\tbut len(aP[9]) > 0' + NL + '\t\t\t\taCC[2] = aP[9]', '\t\t\tbut 0' + NL + '\t\t\t\taCC[2] = aP[9]')
    add('a warning does not refuse (G9, G10)', J, '\t\t\tif aP[10] = "warning"', '\t\t\tif 0')
    add("the refusal speaks the declared message, filled (G3)", J, 'CtFailC(aCl[2], aCC[1], aCC[2], CtFill(aP[6], aD, ""))', 'CtFailC(aCl[2], aCC[1], aCC[2], aP[6])')
    add("the warning speaks the declared message, filled (G9)", J, '$aCourtWarnings + [aCC[1], aCC[2], aCl[2], CtFill(aP[6], aD, "")]', '$aCourtWarnings + [aCC[1], aCC[2], aCl[2], aP[6]]')
    add("the finding stands at the line of the seat's clause (G3, G5, G7)", J, 'CtFailC(aCl[2], aCC[1]', 'CtFailC(aD[3], aCC[1]')
    add("a pattern judges the seat of its own kind only (G16)", J, '\t\t\tif aD[1] != aK[1] loop ok', '\t\t\tif 0 loop ok')
    return P


def main():
    with tempfile.TemporaryDirectory() as td:
        for name in CODE_FILES:
            shutil.copyfile(os.path.join(SPIKE, name), os.path.join(td, name))
        shutil.copytree(os.path.join(SPIKE, 'grants'), os.path.join(td, 'grants'))
        base = judge(td)
        if base:
            print('the unplanted folder fails the judge on', base, '-- fix that first')
            return 1
        print('the unplanted folder passes the judge: 33 meta fixtures and 16 court cases')
        caught = 0
        P = plants()
        for label, fname, old, new in P:
            src = open(os.path.join(SPIKE, fname), encoding='utf-8', newline='').read()
            if src.count(old) != 1:
                print(f'ANCHOR {label}: {src.count(old)} matches in {fname}')
                return 2
            with open(os.path.join(td, fname), 'w', encoding='utf-8', newline='') as fh:
                fh.write(src.replace(old, new))
            failed = judge(td)
            shutil.copyfile(os.path.join(SPIKE, fname), os.path.join(td, fname))
            caught += bool(failed)
            print(('CAUGHT ' if failed else 'MISSED ') + label + (' -- ' + ', '.join(failed[:9]) + (' ...' if len(failed) > 9 else '') if failed else ''))
        print(f'PLANTS: {caught} of {len(P)} protections load-bearing')
        return len(P) - caught


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
