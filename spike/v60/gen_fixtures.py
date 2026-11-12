"""Haro v0.60 -- symbols: data that keeps its text, compared by its name (HARO-SYMBOL-01). Written FIRST, before the compiler is touched.

THE ASK. stzlib-haroport, 2026-11-12 00:58: Softanza's named parameters compare an item with a symbol (`pvList[1] = :To`), 3,829 times in
330 files of base/. Two findings block its module 3: HARO-SYMBOL-KEYWORD-01, `kA = :And` refused as "a keyword in another case"; and
HARO-SYMBOL-TEXT-EQ-01, `vL[1] = :To` false when vL[1] is the text "to" -- which is what a .ring caller's `:to` is, Ring lowering it --
with no error. PRINCIPLES.md principle 4 and v0.41 (S3): a symbol is data and keeps its text; its comparison ignores case.

THE DESK'S READINGS (D72), on the Principal's "i let you decide":
  - a symbol's word is no keyword: `:And`, `:To`, `:End` are symbols
  - where one side of `=` or `!=` is a symbol written in the code, the other side is compared with the symbol's name by its text, case
    ignored; a value that is not a text is never equal to a symbol (no refusal: a named-parameter list may hold any value first)

THE LINES:
  K1  a symbol's word is no keyword
  K2  a text compared with a symbol, case ignored; a value that is not text is not the symbol
  K3  a .ring caller's lowered symbol reaches a .haro comparison and holds
  K4  a .ring file untouched

  python spike/v60/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

IS_TO = ['func IsTo(xV)', T + 'if xV = :To', T + T + 'return "yes"', T + 'end', T + 'return "no"', 'end']

CASES = [
    ('Y01', 'K1', 'symbols spelled like keywords are symbols', ['kA = :And', 'kB = :To', 'kC = :End', 'print kA', 'print kB', 'print kC'],
     'And\nTo\nEnd\n', 0),
    ('Y02', 'K2', 'a text and a symbol compare by the symbol\'s name, case ignored', [
        'vL = ["to", 5]', 'print vL[1] = :To', 'print vL[1] = :to', 'print vL[1] = :TO', 'print vL[1] != :To', 'print vL[1] = :From'],
     'true\ntrue\ntrue\nfalse\nfalse\n', 0),
    ('Y03', 'K2', 'a value that is not a text is not the symbol', ['vL = [5, [1]]', 'print vL[1] = :To', 'print vL[1] != :To',
                                                                  'print vL[2] = :To'],
     'false\ntrue\nfalse\n', 0),
    ('Y04', 'K2', 'in a condition, and with the symbol on the left', ['tW = "From"', 'if tW = :from', T + 'print "from"', 'end',
                                                                      'if not (:FROM != tW)', T + 'print "FROM"', 'end'],
     'from\nFROM\n', 0),
    ('Y05', 'K3', 'a .ring caller\'s :to reaches a .haro function and is the symbol', ['load "is_to.haro"', '? IsTo(:to)', '? IsTo(:To)',
                                                                                       '? IsTo("from")'],
     'yes\nyes\nno\n', 0),
    ('Y06', 'K4', 'a .ring file reads symbols as Ring does: lowered texts', ['? "to" = :To', '? "To" = :To'],
     '1\n0\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    with open(os.path.join(HERE, 'cases', 'is_to.haro'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(IS_TO) + '\n')
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid in ('Y05', 'Y06') else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.60',
        'decision': 'HARO-SYMBOL-01: stzlib-haroport\'s HARO-SYMBOL-KEYWORD-01 and HARO-SYMBOL-TEXT-EQ-01 (2026-11-12), PRINCIPLES.md '
                    'principle 4; the desk\'s readings are D72',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'K1': 'a symbol\'s word is no keyword', 'K2': 'a text and a symbol compared by name, case ignored',
                  'K3': 'a .ring caller\'s lowered symbol holds', 'K4': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
