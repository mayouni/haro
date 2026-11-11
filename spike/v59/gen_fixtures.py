"""Haro v0.59 -- `null` leaves Haro: `""` is the empty text, `none` is absence, `IsEmpty` tests the empty text (HARO-NULL-01). Written FIRST,
before the compiler is touched.

THE RULINGS. TYPES.md T5 (D55): "Ring's NULL, which was the empty string, is gone with the global it lived in: `""` is a text of length 0
and nothing else." The order, the Principal's in this desk's chat (2026-11-11, "Right after absence"): Haro's own `null` and `IsNull`
migrated, then `null` refused in a .haro file. The test's name, his (2026-11-12, choosing among three): "IsEmpty(x)" -- the built-in that
answers whether x holds the empty text, true for `""` and false for any other value or type, in place of `IsNull`.

THE DESK'S READINGS (D71):
  - `null` in a .haro file is refused, naming `""` and `none`
  - `IsNull` in a .haro file is refused, naming `IsEmpty`
  - `IsEmpty(x)` is true for the empty text only -- the text "NULL" is a text, and a list, a number or an object is not empty text
  - a .ring file keeps Ring's `null` and `isnull`, which is also true for the text "NULL"

THE LINES:
  N1  IsEmpty: the empty text, and nothing else
  N2  null and IsNull refused in a .haro file
  N3  a .ring file untouched

  python spike/v59/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


R_NULL = '`null` is no value of Haro -- the empty text is "", and absence is none; written'
R_ISNULL = 'one spelling: `IsEmpty`; written'
HEAD = ['print "before"', 'f()', 'func f']

CASES = [
    ('U01', 'N1', 'IsEmpty is true for the empty text and false for any other value', [
        'print IsEmpty("")', 'print IsEmpty("a")', 'print IsEmpty("NULL")', 'print IsEmpty([])', 'print IsEmpty(0)', 'print IsEmpty(new P)',
        'class P', 'end'],
     'true\nfalse\nfalse\nfalse\nfalse\nfalse\n', 0),
    ('U02', 'N1', 'IsEmpty answers a condition', ['tX = ""', 'if IsEmpty(tX)', T + 'print "empty"', 'end', 'tX = "x"',
                                                   'if not IsEmpty(tX)', T + 'print "full"', 'end'],
     'empty\nfull\n', 0),
    ('U03', 'N2', 'null is refused, naming "" and none', HEAD + [T + 'tX = null', T + 'print tX', 'end'],
     refused('U03', 4, R_NULL, 'null'), 1),
    ('U04', 'N2', 'IsNull is refused: IsEmpty', HEAD + [T + 'print IsNull("")', 'end'],
     refused('U04', 4, R_ISNULL, 'IsNull'), 1),
    ('U05', 'N3', 'a .ring file: null is the empty text, and isnull is true for it and for "NULL"', [
        '? isnull(null)', '? isnull("NULL")', '? isnull("a")', 'x = null', '? len(x)'],
     '1\n1\n0\n0\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'U05' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.59',
        'decision': 'HARO-NULL-01: TYPES.md T5 (D55); the Principal\'s "Right after absence" (2026-11-11) and "IsEmpty(x)" (2026-11-12); '
                    'the desk\'s readings are D71',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'N1': 'IsEmpty: the empty text, and nothing else', 'N2': 'null and IsNull refused', 'N3': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
