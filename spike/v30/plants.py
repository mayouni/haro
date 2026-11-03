"""Every protection of the one reader and the printer switched off in turn: the court must fail, for the fixture that
protection exists for (the W discipline: each protection load-bearing).

Each plant is one text substitution in a COPY of block_lib.haro, run from a temporary folder beside a copy of block.haro;
no file of the spike is changed. The planted copy is judged on the Haro VM against v30/fixtures.json; printed is CAUGHT
with the fixtures that failed, or MISSED -- a MISSED plant is a protection no fixture pins, and the answer to it is a
fixture, written before the protection is touched (as the study's D05 and F06 were).

  python spike/v30/plants.py
"""
import os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]                       # never --plant here
import block_court as bc

NL, Q = '\n', '"'
PLANTS = [
    ('a string folds its continuation indent to one space (L03)',
     '					while i <= n and (cSrc[i] = " " or cSrc[i] = char(9) or cSrc[i] = char(13))' + NL + '						i++' + NL + '					end' + NL + '					cBuf += " "',
     '					cBuf += " "'),
    ('a comment inside a list or a group is kept (L07, D05, K05)',
     '			aSeg + ["comment", t[2]]' + NL, ''),
    ('a comment at the top level is kept (K06)',
     '			aOut + ["comment", BlkPeek()[2]]' + NL, ''),
    ('a trailing comma is layout (L02)',
     '		if t[1] = cClose' + NL + '			$nBlkPos++',
     '		if t[1] = cClose' + NL + '			if len(aItems) > 0 and len(aSeg) = 0 BlkFail(t[3], "a trailing comma") ok' + NL + '			$nBlkPos++'),
    ('an empty item between commas is refused (F06)',
     '			if BlkCountValues(aSeg) = 0' + NL + '				BlkFail(t[3], "an empty item before a comma")' + NL + '			ok' + NL, ''),
    ('a comma outside a list or a group is refused by name (F04)',
     '	if t[1] = "comma" BlkFail(t[3], "a comma outside a list or a group") ok' + NL, ''),
    ('several values of one item are a row (D01)',
     '		aItems + ["row", aVals]',
     '		for i = 1 to len(aVals)' + NL + '			aItems + aVals[i]' + NL + '		next'),
    ('CRLF is LF (L04)',
     '		but c = " " or c = char(9) or c = char(13)', '		but c = " " or c = char(9)'),
    ("Haro's `?` makes the value before it optional, Q-B1 (H01, D07, K04)",
     '	while BlkPeek()[1] = "question"', '	while 0'),
    ("a string as a pair's key is refused by name until C6's amendment lands, Q-B2 (F07)",
     '		if BlkPeek()[1] = "colon"' + NL + '			# Q-B2', '		if 0' + NL + '			# Q-B2'),
    ("a doubled quote inside a string is refused by name until C6's amendment lands, Q-B2 (F08)",
     "			if i <= n and cSrc[i] = '\"'" + NL + '				aToks + ["error", "doubled_quote", nStart, ""]',
     "			if 0" + NL + '				aToks + ["error", "doubled_quote", nStart, ""]'),
    ('a path is words joined by dots with no space (F09)',
     '	while BlkPeek()[1] = "dot" and BlkPeek()[4] = nEnd and BlkPeekAt(1)[1] = "ident" and BlkPeekAt(1)[4] = BlkPeek()[5]',
     '	while BlkPeek()[1] = "dot" and BlkPeekAt(1)[1] = "ident"'),
    ('mixed case is neither a word nor a keyword (F11)',
     '				aToks + ["error", "mixed_case", nLine, cW]' + NL + '				return aToks',
     '				aToks + ["ident", cW, nLine, i, j]'),
    ('a blank line between declarations (K02, K06)',
     '		if p > 1 cOut += char(10) ok' + NL, ''),
    ('a list holding a comment or a group prints one item a line (K05)',
     '		if BlkHoldsCommentOrGroup(v[2]) return "[" + BlkLines(v[2], nInd) + "]" ok' + NL, ''),
    ('a comment prints on a line of its own (K06)',
     '		if v[1] = "comment"' + NL + '			if len(aCur) > 0', '		if 0' + NL + '			if len(aCur) > 0'),
]


def main():
    src = open(os.path.join(SPIKE, 'block_lib.haro'), encoding='utf-8', newline='').read()
    caught = 0
    with tempfile.TemporaryDirectory() as td:
        shutil.copyfile(os.path.join(SPIKE, 'block.haro'), os.path.join(td, 'block.haro'))
        bc.CWD = td
        for what, a, b in PLANTS:
            assert src.count(a) == 1, (what, src.count(a))
            with open(os.path.join(td, 'block_lib.haro'), 'w', encoding='utf-8', newline='') as fh:
                fh.write(src.replace(a, b))
            bad, ids = bc.fixtures(builds=(('haro', None),), quiet=True)
            caught += bool(bad)
            print(('CAUGHT ' if bad else 'MISSED ') + what + (' -- ' + ', '.join(ids) if ids else ''))
    print(f'PLANTS: {caught} of {len(PLANTS)} protections load-bearing')
    return len(PLANTS) - caught


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
