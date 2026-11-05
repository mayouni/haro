"""Every protection of the per-seat severity switched off in turn: the guard must fail, for the fixture that protection exists for (the W discipline).

Each plant is one or two text substitutions in a COPY of haro_lib.haro, forge.haro, court_lib.haro, world_lib.haro or severity_lib.haro, in a temporary folder that
holds copies of every .haro file of the spike and the panel sentences; no file of the spike is changed. For each plant the folder is judged on the Haro VM by:
  the meta fixtures   v35/fixtures.json: SEVERITIES accepted and refused, each refusal by the fragment of why
  the cases           the court forged from panel_v35.haro in the folder, then each case of v35/court_cases.json (first, contains, lacks, counts, diagnose)
The judge must pass the unplanted folder first, or the script stops. Printed is CAUGHT with what failed, or MISSED: a protection no fixture pins, and the answer to it is a
fixture (P24, the explicit errors on NEXT and GADGET, and the words of P15 and P16 were found by designing exactly this list).

  python spike/v35/plants.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
sys.argv = [sys.argv[0]]
import paths

HARO_VM, _ = paths.need_bins()
NL, T = '\n', '\t'


def run(folder, args, timeout=30):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([HARO_VM] + args, capture_output=True, env=env, timeout=timeout, cwd=folder)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
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
    for gen in ('panel_court.haro', 'panel.gbnf'):
        if os.path.exists(os.path.join(folder, gen)):
            os.remove(os.path.join(folder, gen))
    forged = run(folder, ['forge.haro', 'panel_v35.haro', '.'])
    cases = json.load(open(os.path.join(HERE, 'court_cases.json'), encoding='utf-8'))['cases']
    if not forged.startswith('forged panel'):
        return failed + ['FORGE']
    for c in cases:
        out = run(folder, ['panel_court.haro', c['verb']] + c['args'])
        lines = [l for l in out.split('\n') if l]
        first = lines[0] if lines else ''
        good = ('first' not in c or c['first'] in first)
        if 'counts' in c:
            f = fields(out)
            good = good and out.startswith('ok') and all(f.get('count ' + k) == str(v) for k, v in c['counts'].items())
        good = good and all(x in out for x in c.get('contains', [])) and not any(x in out for x in c.get('lacks', []))
        if 'diagnose' in c:
            try:
                d = json.loads(out)['diagnostics'][0]
            except (ValueError, KeyError, IndexError, TypeError):
                d = {}
            w = c['diagnose']
            good = good and d.get('code') == w['code'] and d.get('cites') == w['cites'] and d.get('severity') == w['severity']
        if not good:
            failed.append(c['id'])
    return failed


def plants():
    P = []

    def add(label, fname, old, new):
        P.append((label, fname, old if isinstance(old, list) else [old], new if isinstance(new, list) else [new]))
    H, F, C, W, S = 'haro_lib.haro', 'forge.haro', 'court_lib.haro', 'world_lib.haro', 'severity_lib.haro'
    # ---- the meta-court
    add('SEVERITIES is a clause of DECLARATION', H, '["SEATS", "seatlist"], ["SEVERITIES", "pairlist"], ["VERB", "string"]', '["SEATS", "seatlist"], ["VERB", "string"]')
    add('SEVERITIES is a clause of REFUSAL', H, '["NAMED", "messagelist"], ["SEVERITIES", "pairlist"]]', '["NAMED", "messagelist"]]')
    add('the declaration keeps its SEVERITIES', H, 'cNames, aMsgs, aCodes, aInc, aSevs]', 'cNames, aMsgs, aCodes, aInc, []]')
    add('the refusal keeps its SEVERITIES', H, 'aRCodes, aRCites, aRSevs]', 'aRCodes, aRCites, []]')
    add('SEVERITIES names a seat of the kind (R1)', H, 'if isNull(aSvSeat) StzuFail(', 'if isNull(aSvSeat) loop ok if 0 StzuFail(')
    add('only a reference may be a warning (R3, R4)', H, 'if not StzuIsReferenceSeat(aSvSeat, aDeclared, aForms, aUnions)', 'if 0')
    add('a UNION holding a declaration is a reference (A3)', H, '= "DECLARATION" and not aUnions[i][2][j][2] return 1 ok', '= "DECLARATION" and 0 return 1 ok')
    add('a SYMBOL is a reference (A4)', H, 'if cK = "DECLARATION" or cK = "SYMBOL" return 1 ok', 'if cK = "DECLARATION" return 1 ok')
    add('an entry is named once (R5, R10)', H, 'if aSv[j][1] = aSv[i][1] StzuFail(', 'if 0 StzuFail(')
    add('a severity is error or warning (R2, R9)', H, 'if aSv[i][2] != "error" and aSv[i][2] != "warning"', 'if 0')
    add('a REFUSAL\'s SEVERITIES belongs to unknown_declaration (R6, R11)', H, 'if cName != "unknown_declaration"' + NL + T * 7 + 'StzuFail(nLine, "SEVERITIES belongs', 'if 0' + NL + T * 7 + 'StzuFail(nLine, "SEVERITIES belongs')
    add('the word is a NAMED word (R7, R8)', H, 'if not bNamed StzuFail(aRSevs[i][3]', 'if 0 StzuFail(aRSevs[i][3]')
    # ---- the forge
    add('the forge hands the court a kind\'s severities', F, 'if len(aD[i][10]) > 0 cSevs = ", " + MessagesSource(aD[i][10]) ok', '')
    add('the forge hands the court a refusal\'s severities', F, 'if len(aR[i][9]) > 0 cRSevs = ", " + MessagesSource(aR[i][9]) ok', '')
    add('the severity library rides along', F, 'if bSev c += \'load "severity_lib.haro"\' + nl ok', '')
    # ---- the court
    add('a kind read past declares nothing', C, 'if not isNull(aPD) aDecls + aPD ok', 'aDecls + aPD')
    add('a NAMED kind held at warning is read past', C, 'if SevSkipNamed(aSevR, tK) return NULL ok', '')
    add('a reference seat held at warning is spoken, not refused', C, 'if SevSeatIs(aKind, aSeat[1]) = "warning"' + NL + T * 5 + 'SevWarnClause', 'if 0' + NL + T * 5 + 'SevWarnClause')
    add('a SYMBOL seat held at warning is spoken, not refused', W, 'if SevSeatIs(aKW, aSites[i][2][1]) = "warning"', 'if 0')
    add('only warning demotes: a seat written at error stays an error (P3)', C, 'if SevSeatIs(aKind, aSeat[1]) = "warning"', 'if SevSeatIs(aKind, aSeat[1]) != ""')
    # ---- the library
    add('a list warns once per element that resolves to nothing (P24)', S, 'if aV[1] = "namelist" or aV[1] = "pairlist" or aV[1] = "stringlist"', 'if 0')
    add('a warning keeps the code its refusal would carry (P7)', S, '$aCourtWarnings + [$cCourtCode, $aCourtCites, aClause[2], cWhy]', '$aCourtWarnings + ["DANGLING", $aCourtCites, aClause[2], cWhy]')
    add('only warning reads a NAMED kind past: a word at error is refused (P13)', S, 'if cSev != "warning" return 0 ok', 'if cSev = "" return 0 ok')
    add('a kind read past balances its parentheses (P11)', S, 'if t[1] = "lparen" nDepth++ ok', '')
    add('a body that never closes is refused, not run off the end (P15)', S, 'if t[1] = "eof"' + NL, 'if 0' + NL)
    add('a kind read past carries its RATIONALE (P16)', S, 'if not (tR[1] = "keyword" and tR[2] = "RATIONALE")', 'if 0')
    add('a NAMED warning speaks the NAMED words (P11)', S, '$aCourtWarnings + [aCC[1], aCC[2], tK[3], cNamed]', '$aCourtWarnings + [aCC[1], aCC[2], tK[3], "a kind"]')
    add('a NAMED warning carries the refusal\'s code and cites (P18)', S, 'aCC = CtRefusalCode("unknown_declaration", cWord, "UNKNOWN_KIND")', 'aCC = ["UNKNOWN_KIND", []]')
    return P


def main():
    with tempfile.TemporaryDirectory() as td:
        for name in os.listdir(SPIKE):
            if name.endswith('.haro'):
                shutil.copyfile(os.path.join(SPIKE, name), os.path.join(td, name))
        shutil.copytree(os.path.join(SPIKE, 'panel'), os.path.join(td, 'panel'))
        base = judge(td)
        if base:
            print('the unplanted folder fails the judge on', base, '-- fix that first')
            return 1
        meta = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
        ncase = len(json.load(open(os.path.join(HERE, 'court_cases.json'), encoding='utf-8'))['cases'])
        print(f'the unplanted folder passes the judge: {len(meta["accepts"]) + len(meta["rejects"])} meta fixtures and {ncase} cases', flush=True)
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
