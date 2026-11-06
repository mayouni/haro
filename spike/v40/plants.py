"""Every protection of v0.40 (D51's declared half) switched off in turn: the v0.40 meta fixtures or stage 45 must fail, for the fixture the
protection exists for (the W discipline). BYTES names stage 45's byte check: a language that NEEDS nothing forges its committed court and grammar.

Each plant is one text substitution in one of spike/haro_lib.haro, forge.haro, court_lib.haro, needs_lib.haro. Nothing is built: the meta-court
and the courts are Haro programs, run on haro as they stand. Every file is restored byte for byte before the next plant -- verified by its
digest, and restored even when the script is stopped.

  python spike/v40/plants.py            all plants (a few seconds each)
  python spike/v40/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)

PLANTS = [
    # ---- the meta-court
    ('P1', 'R1', 'haro_lib.haro', 'NEEDS takes any word', '				if not InStrList(aLNeeds[i], StzuCapabilities())', '				if 0'),
    ('P2', 'R2', 'haro_lib.haro', 'NEEDS may name a word twice', 'if aLNeeds[j] = aLNeeds[i] StzuFail(', 'if 0 StzuFail('),
    ('P3', 'R3', 'haro_lib.haro', 'a kind may open a door the language does not NEED (A6\'s gate open)',
     'if not bBySeat and not InStrList(cOp, aLNeeds)', 'if 0'),
    ('P4', 'R4', 'haro_lib.haro', 'a kind may open a door in a language that NEEDS nothing',
     '			if isNull(aLNeeds)\n				StzuFail(aDeclarations[i][5], cKn + " OPENS "', '			if 0\n				StzuFail(aDeclarations[i][5], cKn + " OPENS "'),
    ('P5', 'R5', 'haro_lib.haro', 'a NEEDS word no kind opens is let stand', 'if not InStrList(aLNeeds[i], aOpened) StzuFail(', 'if 0 StzuFail('),
    ('P6', 'R6', 'haro_lib.haro', 'OPENS may name nothing', 'if isNull(aOs) StzuFail(', 'if 0 StzuFail('),
    ('P7', 'R7', 'haro_lib.haro', 'OPENS may name a seat that is no MENU', 'if isNull(aCanOpen) StzuFail(', 'if 0 StzuFail('),
    ('P8', 'R8', 'haro_lib.haro', 'an OPENS seat\'s MENU may hold any word', '					if not InStrList(aCanOpen[j], StzuCapabilities())', '					if 0'),
    ('P9', 'A1', 'haro_lib.haro', 'a word of an OPENS seat\'s MENU does not count as opened', 'for j = 1 to len(aCanOpen) aOpened + aCanOpen[j] next', 'aOpened + cOp'),
    ('P10', 'A1', 'haro_lib.haro', 'the verdict does not say what the language NEEDS', '		? "needs " + cNd', '		? "needx " + cNd'),
    ('P11', 'A1', 'haro_lib.haro', 'the verdict does not say what each kind opens', '			cOpn += aOpn[i][1] + ":" + aOpn[i][2]', '			cOpn += aOpn[i][1]'),
    ('P12', 'R9', 'haro_lib.haro', 'NEEDS is a clause of a DECLARATION too', '["OPENS", "ident"], ["SEATS", "seatlist"]', '["NEEDS", "namelist"], ["OPENS", "ident"], ["SEATS", "seatlist"]'),
    # ---- the forge
    ('P13', 'D2', 'forge.haro', 'the court is not told the doors', '		cNeeds = "[" + NamesSource(aDoors) + ", " + RowsSource(aOpRows, nl) + "]"', '		cNeeds = ""'),
    ('P14', 'BYTES', 'forge.haro', 'every court loads the doors library', '	if bNeeds c += \'load "needs_lib.haro"\' + nl ok', '	c += \'load "needs_lib.haro"\' + nl'),
    ('P15', 'BYTES', 'forge.haro', 'every language entry is written as if it NEEDed', '	if cPatterns = ""\n		c += "    " + cUnderstand + nl\n	but cNeeds = ""',
     '	if 0\n		c += "    " + cUnderstand + nl\n	but cNeeds = ""'),
    ('P16', 'D5', 'forge.haro', 'a language that NEEDS but has no world carries the stub', '	if bSym or bDoors', '	if bSym'),
    # ---- the court
    ('P17', 'D1', 'court_lib.haro', 'an empty 24th element is read as patterns', '			if len(aEPat[24]) > 0 CtCheckPatterns(aDecls, cSrc) ok', '			CtCheckPatterns(aDecls, cSrc)'),
    ('P18', 'D2', 'court_lib.haro', 'the court does not judge the doors a sentence opens', '		if len(aENd) >= 25 NdCheck(aDecls, aENd[25]) ok', '		if 0 NdCheck(aDecls, aENd[25]) ok'),
    ('P19', 'D5', 'court_lib.haro', 'the world rows do not publish the doors', '				if len(aEW) >= 25 aWRows + ["opens"', '				if 0 aWRows + ["opens"'),
    ('P20', 'D2', 'needs_lib.haro', 'every door is NEEDED', '						if aDoors[1][n] = aW[m] bNeeded = 1 ok', '						bNeeded = 1'),
    ('P21', 'D3', 'needs_lib.haro', 'the refusal carries no code of its own', '"CAPABILITY_NOT_NEEDED"', '"PARSE"'),
    ('P22', 'D5', 'needs_lib.haro', 'a kind that opens a seat is published as opening the seat\'s name', '		if not aDoors[2][i][3] return [aDoors[2][i][2]] ok', '		return [aDoors[2][i][2]]'),
    ('P23', 'D5', 'needs_lib.haro', 'a kind that opens nothing is published too', '		if isNull(aO) loop ok\n', '		if isNull(aO) aO = [] ok\n'),
    ('P24', 'D5', 'needs_lib.haro', 'a list seat is published as one value', '				for k = 1 to len(aV[2]) aOut + aV[2][k] next', '				aOut + aV[2]'),
]

JUDGE = ("import sys; sys.argv = ['x']; sys.path.insert(0, r'%s'); import haro_forge as h; "
         "h.judge_stzu(h.HARO_VM, 'haro', h.STZU40_FIXTURES)") % SPIKE


def digest(b):
    return hashlib.sha256(b).hexdigest()


def failing():
    """the v0.40 meta fixtures and stage 45 on haro: the ids that fail (BYTES for the byte check)"""
    m = subprocess.run([sys.executable, '-c', JUDGE], capture_output=True, cwd=SPIKE, timeout=600).stdout.decode('utf-8', 'replace')
    s = subprocess.run([sys.executable, os.path.join(SPIKE, 'haro_forge.py'), '--stage=45'], capture_output=True, cwd=SPIKE, timeout=600).stdout.decode('utf-8', 'replace')
    ids = re.findall(r'^  FAIL ([AR]\d+) \(', m, re.M) + re.findall(r'^  FAIL (D\d+):', s, re.M)
    if re.search(r'^  FAIL panel\.(gbnf|court\.haro)|^  FAIL panel_court\.haro', s, re.M):
        ids.append('BYTES')
    if 'FAIL the forge did not forge' in s:
        ids.append('FORGE')
    return ids


def main():
    want = set(sys.argv[1:])
    names = {p[2] for p in PLANTS}
    files = {f: os.path.join(SPIKE, f) for f in names}
    original = {f: open(p, 'rb').read() for f, p in files.items()}

    def restore():
        for f, p in files.items():
            open(p, 'wb').write(original[f])
            assert digest(open(p, 'rb').read()) == digest(original[f])

    results = []
    try:
        for pid, fixture, f, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            text = original[f].decode('utf-8')
            if text.count(old) != 1:
                print(f'{pid} STALE: its text is in {f} {text.count(old)} times', flush=True)
                results.append((pid, 'STALE'))
                continue
            open(files[f], 'wb').write(text.replace(old, new).encode('utf-8'))
            try:
                failed = failing()
            finally:
                restore()
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}; failed {", ".join(failed) or "none"}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
