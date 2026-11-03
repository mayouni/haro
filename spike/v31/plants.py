"""Every protection of the pattern engine switched off in turn: the court must fail, for the fixture that protection exists for (the W
discipline: each protection load-bearing).

Each plant is one text substitution in a COPY of pattern_lib.haro, run from a temporary folder beside copies of pattern.haro and
block_lib.haro; no file of the spike is changed. The planted copy is judged on the Haro VM against v31/fixtures.json and the Python
reference (a plant that makes the engine differ from the reference is caught by the twin, by name). Printed is CAUGHT with the fixtures
that failed, or MISSED -- a MISSED plant is a protection no fixture pins, and the answer to it is a fixture, written before the
protection is touched (as P62 and X35 to X37 were, found by exactly this script).

  python spike/v31/plants.py
"""
import os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]                       # never --plant here
import pattern_court as pc

NL = '\n'


def word_off(w):
    return (f'\tif cW = "{w}" return', f'\tif cW = "{w}_" return')


PLANTS = [
    # -- the bound, refused at declaration
    ('no recursion: the named rules form a DAG (X01, X02, X31, X32)', '\t\tPatVisit(i, [])' + NL, ''),
    ('every repetition moves: a nullable body is refused (X03, X04, X05, X16, X27, X28)', '\t\tPatCheck($aPatRoots[i], aNames[i])' + NL, ''),
    ('WHILE is refused (X06)',) + word_off('WHILE'),
    ('DO is refused (X15)',) + word_off('DO'),
    ('EVAL is refused (X20)',) + word_off('EVAL'),
    ('IF is refused (X21)',) + word_off('IF'),
    ('CHANGE is refused (X08)',) + word_off('CHANGE'),
    ('INSERT is refused (X22)',) + word_off('INSERT'),
    ('REMOVE is refused (X23)',) + word_off('REMOVE'),
    ('a group in a rule is the host escape (X07)', 'if cK = "group"' + NL + '\t\tPatFail("pattern " + cWhere + ": ( ) in a rule', 'if cK = "group_"' + NL + '\t\tPatFail("pattern " + cWhere + ": ( ) in a rule'),
    ('a REPEAT count is a whole number (X29, X30)', '\tif not bOk' + NL, '\tif 0' + NL),
    ('REPEAT: the minimum is not above the maximum (X11)', '\t\t\tif nMax < nMin' + NL, '\t\t\tif 0' + NL),
    ('REPEAT begins with a count (X12)', '\t\t\tif aSeq[nPos][1] != "num"' + NL, '\t\t\tif 0' + NL),
    ('REPEAT ends with a rule (X35)', '\t\t\taX = PatItem(aSeq, nPos, cWhere)' + NL + '\t\t\tif aX[1] = 0' + NL + '\t\t\t\tPatFail("pattern " + cWhere + ": REPEAT takes a count, then a rule")' + NL + '\t\t\tok' + NL + '\t\t\treturn [PatNew("repeat"',
     '\t\t\taX = PatItem(aSeq, nPos, cWhere)' + NL + '\t\t\treturn [PatNew("repeat"'),
    ('a RULE names a pattern (X09, X34)', '\t\t\tif find($aPatNames, aRefs[j]) = 0', '\t\t\tif 0'),
    ('a MEMBER names a set (X10, X33)', '\t\t\tif find($aPatSetNames, aMems[j]) = 0', '\t\t\tif 0'),
    ('OR needs a rule on each side (X25, X26)', '\t\t\tif len(aBranches[i]) = 0', '\t\t\tif 0'),
    ('a rule is a list (X24)', '\tif len(aVals) != 1 or aVals[1][1] != "list"', '\tif 0'),
    ('a unary word takes a rule (X13)', '\t\t\tif aX[1] = 0' + NL + '\t\t\t\tPatFail("pattern " + cWhere + ": " + cW + " takes a rule")', '\t\t\tif 0' + NL + '\t\t\t\tPatFail("pattern " + cWhere + ": " + cW + " takes a rule")'),
    ('a word that is no pattern word is refused (X14)', '\t\tPatFail("pattern " + cWhere + ": " + cW + " is not a pattern word")', '\t\treturn [PatNew("lit", v, 0, 0), nPos]'),
    ('RULE and MEMBER take a name (X36, X37)', '\t\t\tif aSeq[nPos][1] != "word"', '\t\t\tif 0'),
    ('LIT takes a value (X19)', '\t\t\tif nPos > len(aSeq)' + NL + '\t\t\t\tPatFail("pattern " + cWhere + ": LIT takes a value")', '\t\t\tif 0' + NL + '\t\t\t\tPatFail("pattern " + cWhere + ": LIT takes a value")'),
    # -- the words
    ('OPTIONAL is a type word, Q-B1 (P38, P43)', '\tif cW = "OPTIONAL" return "opt" ok' + NL, ''),
    ('INTO descends into an optional, Q-B1 (P41, P42, P43)', ' or cKind = "opt")', ')'),
    ('INTO reads a pair as its key then its value (P17)', 'aInner = [v[2], v[3]]', 'aInner = [v[3], v[2]]'),
    ('INTO must consume the whole value it enters (P12)', 'if aR[1] and aR[2] = $aPatSeqLen[nKid] return', 'if aR[1] return'),
    ('SOME needs at least one (P06)', '\t\tif cK = "some" and nCount = 0 return [0, i, []] ok' + NL, ''),
    ('ordered choice: the first alternative that matches (P07, P09)', '\t\t\tif aR[1] return aR ok' + NL + '\t\tnext' + NL + '\t\treturn [0, i, []]', '\t\tnext' + NL + '\t\treturn [0, i, []]'),
    ('NOT inverts (P25, P26)', '\t\taR = PatM(aN[2], nSeq, i)' + NL + '\t\tif aR[1] return [0, i, []] ok' + NL + '\t\treturn [1, i, []]',
     '\t\taR = PatM(aN[2], nSeq, i)' + NL + '\t\tif aR[1] return [1, i, []] ok' + NL + '\t\treturn [0, i, []]'),
    ('AHEAD consumes nothing (P27)', '\t\tif aR[1] return [1, i, []] ok' + NL + '\t\treturn [0, i, []]', '\t\tif aR[1] return [1, aR[2], []] ok' + NL + '\t\treturn [0, i, []]'),
    ('TO stops before what matches (P23)', 'if cK = "to" return [1, p, []] ok', 'if cK = "to" return [1, aR[2], []] ok'),
    ('THRU goes past what matches (P24)', 'return [1, aR[2], aR[3]]', 'return [1, p, aR[3]]'),
    ('KEEP keeps what its rule matched (P21, P22)', '\t\tfor p = i + 1 to aR[2]', '\t\tfor p = i + 1 to i'),
    ('COLLECT wraps what was kept in a list (P51)', '[1, aR[2], [["list", aR[3]]]]', '[1, aR[2], aR[3]]'),
    ('a top-level COLLECT is the result (P21, P51)', '\t\t\taKept = aKept[1][2]', '\t\t\taKept = aKept'),
    ('REPEAT stops at its maximum (P30)', '\t\twhile nCount < aN[3]', '\t\twhile nCount < aN[2]'),
    ('REPEAT needs its minimum (P62)', '\t\tif nCount >= aN[2] return [1, j, aKept] ok', '\t\tif 1 return [1, j, aKept] ok'),
    ('MEMBER is drawn from its set (P19)', '$aPatSeqVals[nSeq][i + 1][2]) > 0 return', '$aPatSeqVals[nSeq][i + 1][2]) >= 0 return'),
    ('MEMBER reads a number by its text (P52)', ' or cKind = "kw" or cKind = "num"', ' or cKind = "kw"'),
    ('LIT matches the value itself, not only its kind (P47)', '\t\t\t\tif BlkDump($aPatSeqVals[nSeq][i + 1]) = BlkDump(aN[2]) return', '\t\t\t\tif 1 return'),
    ('a rule matches only when it consumes its whole input (P55)', '\tbWhole = aR[1] and aR[2] = len(aVals)', '\tbWhole = aR[1]'),
    ('a comment is not a value of the input (P32)',
     'names no pattern")' + NL + '	ok' + NL + '	aAll = BlkLoad(cText)' + NL + '	aVals = []' + NL + '	for i = 1 to len(aAll)' + NL + '		if aAll[i][1] != "comment" aVals + aAll[i] ok',
     'names no pattern")' + NL + '	ok' + NL + '	aAll = BlkLoad(cText)' + NL + '	aVals = []' + NL + '	for i = 1 to len(aAll)' + NL + '		aVals + aAll[i]'),
    # -- the packrat
    ('the memo stores what it computed (P61)', '\t$aPatMemo[nIdx] = aR' + NL, ''),
    ('the memo is read before computing (P61)', '\tif isList(aMemo) return aMemo ok' + NL, ''),
    ("the bound counts an optional's positions: the twin refuses a differing bound (P41, P42, P43)",
     '\t\t\tbut cK = "opt"' + NL + '\t\t\t\tnTotal += PatPositions([v[2]])' + NL, ''),
]


def main():
    src = open(os.path.join(SPIKE, 'pattern_lib.haro'), encoding='utf-8', newline='').read()
    caught = 0
    with tempfile.TemporaryDirectory() as td:
        for name in ('pattern.haro', 'block_lib.haro'):
            shutil.copyfile(os.path.join(SPIKE, name), os.path.join(td, name))
        pc.CWD = td
        for what, a, b in PLANTS:
            assert src.count(a) == 1, (what, src.count(a))
            with open(os.path.join(td, 'pattern_lib.haro'), 'w', encoding='utf-8', newline='') as fh:
                fh.write(src.replace(a, b))
            bad, ids = pc.judge_fixtures(builds=(('haro', None),), quiet=True)
            caught += bool(bad)
            print(('CAUGHT ' if bad else 'MISSED ') + what + (' -- ' + ', '.join(ids[:8]) + (' ...' if len(ids) > 8 else '') if ids else ''))
    print(f'PLANTS: {caught} of {len(PLANTS)} protections load-bearing')
    return len(PLANTS) - caught


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
