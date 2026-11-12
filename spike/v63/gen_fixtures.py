"""Haro v0.63 -- a .ring number crossing into .haro is an exact decimal (TYPES.md section 6, HARO-RINGBOUNDARY-NUMBER-01). Written FIRST,
before the VM is touched.

THE FINDING. stzlib-haroport, 2026-11-12, base/common: the guard sound_mu3 (.ring) calls oPattern.Off(0.25) on stzPattern (.haro), whose
`if not IsNumber(pxCycles) or pxCycles <= 0 or pxCycles >= 1` stops with NUMBER_MIX (float <= integer). Ring has one number type, so every
.ring caller's fraction reaches a .haro library as a float, and the library's integer literals refuse it -- the same shape all over Softanza.

THE RULING. TYPES.md section 6 (D55): "A value crossing from .ring code into a .haro name is checked at that binding." The desk's reading
(D75), the first of the two StzLib named: a fraction crossing from .ring code into .haro -- a .ring caller's argument at a .haro
function's parameter, a .ring function's answer to a .haro caller -- is the exact decimal of its shortest text (0.25 is 0.25, 0.1 is
0.1). A whole number is already an integer. Decimals and integers mix (v0.52), so the library's literals hold; a float stays where .haro
code asks for one; a NaN or an infinity has no decimal and stays a float; the items of a list are not converted.

THE LINES:
  D1  a .ring caller's fraction at a .haro parameter is an exact decimal, its shortest text
  D2  a .ring caller's whole number at a .haro parameter is the integer it was
  D3  a .ring function's fraction, answered to a .haro caller, is an exact decimal
  D4  a .haro caller's float is not converted: it meets an integer as before (NUMBER_MIX)
  D5  a .ring file reads its own numbers as it did

  python spike/v63/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
PAT = ['func Within(pxCycles)', T + 'if pxCycles <= 0 or pxCycles >= 1', T + T + 'return "out"', T + 'end', T + 'return "in"', 'end',
       'func Plus(pxV)', T + 'return pxV + 1', 'end',
       'func IsThird(pxV)', T + 'if pxV * 3 = 0.3', T + T + 'return "exact"', T + 'end', T + 'return "inexact"', 'end',
       'func Twice(pfV)', T + 'return pfV * 2.0f', 'end']
OLD = ['func Half n', T + 'return n / 2', 'func Tenth', T + 'return 0.1', 'func Whole', T + 'return 4']


def err(line, code, msg, f, where):
    return f'\nLine {line} Error ({code}) : {msg} \nIn {where} in file {f}\n\nCalled from line 1 in file {f} '


CASES = [
    ('M01', 'D1', 'the finding: a .ring caller\'s 0.25 meets the library\'s 0 and 1', '.ring',
     ['load "pat.haro"', '? Within(0.25)', '? Within(1.5)', '? Plus(0.25)'],
     'in\nout\n1.25\n', 0),
    ('M02', 'D1', 'the decimal is the shortest text: 0.1 times 3 is exactly 0.3', '.ring',
     ['load "pat.haro"', '? IsThird(0.1)'],
     'exact\n', 0),
    ('M03', 'D2', 'a .ring caller\'s whole number is the integer it was', '.ring',
     ['load "pat.haro"', '? Within(1)', '? Plus(2)'],
     'out\n3\n', 0),
    ('M04', 'D3', 'a .ring function\'s fraction answered to a .haro caller is a decimal', '.haro',
     ['load "old.ring"', 'xH = Half(1)', 'if xH < 1', T + 'print "less"', 'end', 'print xH + 1', 'print Tenth() * 3 = 0.3'],
     'less\n1.5\ntrue\n', 0),
    ('M05', 'D3', 'a .ring function\'s whole number answered to a .haro caller is an integer', '.haro',
     ['load "old.ring"', 'iW = Whole()', 'print iW + 1'],
     '5\n', 0),
    ('M06', 'D4', 'a .haro caller\'s float is not converted', '.haro',
     ['print Within(0.25f)'] + PAT[:6],
     err(3, 'NUMBER_MIX', 'float <= integer -- an integer and a float do not mix; convert one: Float(i)', 'M06.haro', 'function within()'),
     1),
    # M08 and M09 written after the code was edited and before it was built or run, said so
    ('M08', 'D4', 'a .ring caller\'s fraction at a .haro f parameter stays a float', '.ring',
     ['load "pat.haro"', '? Twice(0.25)'],
     '0.50\n', 0),
    ('M09', 'D5', 'a .ring function\'s fraction answered to a .ring caller stays a float', '.ring',
     # `type` ADDED AFTER THE PLANTS, said so: plant Q8 (converted here too) missed, because .ring prints a decimal 1.5 as it prints the
     # float; .ring's type() names the difference
     ['load "old.ring"', '? Half(1) * 3', '? type(Half(1))'],
     '1.50\nNUMBER\n', 0),
    ('M07', 'D5', 'a .ring file reads its own numbers as it did', '.ring',
     ['x = 0.25', '? x + 1', '? 0.1 * 3'],
     '1.25\n0.30\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    for name, lines in (('pat.haro', PAT), ('old.ring', OLD)):
        with open(os.path.join(HERE, 'cases', name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(lines) + '\n')
    out = []
    for cid, line, why, ext, src, stdout, code in CASES:
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.63',
        'decision': 'TYPES.md section 6 (D55); HARO-RINGBOUNDARY-NUMBER-01 (stzlib-haroport, 2026-11-12); the desk\'s reading is D75',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {
            'D1': 'a .ring fraction at a .haro parameter is an exact decimal, its shortest text',
            'D2': 'a .ring whole number at a .haro parameter is the integer it was',
            'D3': 'a .ring function\'s fraction answered to a .haro caller is an exact decimal',
            'D4': 'a .haro caller\'s float is not converted',
            'D5': 'a .ring file reads its own numbers as it did',
        },
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
