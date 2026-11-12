"""Haro v0.66 -- Haro's numbers, as NUMBERS.md proposes (HARO-NUMBERS-CORE-01). Written FIRST, before the VM is touched.

THE RULING. The Principal, 2026-11-12: Haro must not change the places of every number for the whole program; "if we need the
decimals(10.257) we get a list [2, 5, 7], if we want the decimal part we say DecimalPart(10.257) and we get 0.257"; Softanza's names;
the best-designed languages as the model. NUMBERS.md (ad4d0a5) proposed the set, and he ruled "Build it as proposed".

ONE DEPARTURE, said so: NUMBERS.md listed `Truncate(x)` beside `IntegerPart(x)`; both answer the integer toward zero, so building both
would give one thing two names, which his rulings of one way each (D67, D69) refuse. `IntegerPart` is built; `Truncate` is not.

THE LINES (in a .haro file):
  L1  a float is written as the shortest text that reads back the same; no setting reaches .haro code
  L2  Text(x, iPlaces): exactly iPlaces after the point, the last rounded half to even
  L3  Round(x) an integer, Round(x, iPlaces) the same kind, half to even; Floor and Ceil an integer
  L4  IntegerPart, DecimalPart; Decimals and Digits, vectors of integers
  L5  Abs, Sign, Clamp
  L6  FromHex beside Hex
  L7  refused, naming what to write: Decimals(n) as a setting, FAbs, Dec
  L8  a .ring file is untouched

  python spike/v66/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
HEAD = ['print "before"', 'f()', 'func f']
CSV = ['func Csv(vX)', T + 'tOut = ""', T + 'for i = 1 to Len(vX)', T + T + 'if i > 1', T + T + T + 'tOut += ","', T + T + 'end',
       T + T + 'tOut += String(vX[i])', T + 'end', T + 'return "[" + tOut + "]"', 'end']


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


CASES = [
    ('U01', 'L1', 'a float is written as the shortest text that reads back the same',
     ['print 0.1f', 'print 1.0f / 3.0f', 'print String(1.0f / 3.0f)', 'print 2.0f', 'print 12.50'],
     '0.1\n0.3333333333333333\n0.3333333333333333\n2\n12.50\n', 0),
    ('U03', 'L2', 'Text writes exactly the places asked, half to even',
     ['print Text(2.5, 2)', 'print Text(1.0f / 3.0f, 4)', 'print Text(7, 2)', 'print Text(2.345, 2)', 'print Text(2.355, 2)',
      'print Text(10.257, 0)'],
     '2.50\n0.3333\n7.00\n2.34\n2.36\n10\n', 0),
    ('U04', 'L3', 'Round: an integer, or the same kind at iPlaces, half to even',
     ['print Round(2.5)', 'print Round(3.5)', 'print Round(-2.5)', 'print Round(2.5f)', 'print Round(10.257, 2)', 'print Round(7, 2)',
      'print Round(2.675f, 2)', 'print Type(Round(10.257, 2))', 'print Type(Round(2.5))'],
     '2\n4\n-2\n2\n10.26\n7\n2.67\nDECIMAL\nNUMBER\n', 0),
    ('U05', 'L3', 'Floor and Ceil answer an integer',
     ['print Floor(10.7)', 'print Ceil(10.2)', 'print Floor(-10.2)', 'print Ceil(-10.7)', 'print Floor(2.5f)', 'print Type(Floor(2.5f))'],
     '10\n11\n-11\n-10\n2\nNUMBER\n', 0),
    ('U06', 'L4', 'IntegerPart toward zero, DecimalPart the same kind and sign',
     ['print IntegerPart(10.257)', 'print IntegerPart(-10.257)', 'print DecimalPart(10.257)', 'print DecimalPart(-10.257)',
      'print DecimalPart(7)', 'print DecimalPart(2.5f)'],
     '10\n-10\n0.257\n-0.257\n0\n0.5\n', 0),
    ('U07', 'L4', 'Decimals and Digits, vectors of integers',
     ['print Csv(Decimals(10.257))', 'print Csv(Decimals(3.50))', 'print Csv(Decimals(7))', 'print Csv(Decimals(0.005))',
      'print Csv(Decimals(0.25f))', 'print Csv(Decimals(-10.257))', 'print Csv(Digits(10.257))', 'print Csv(Digits(-42))'] + CSV,
     '[2,5,7]\n[5,0]\n[]\n[0,0,5]\n[2,5]\n[2,5,7]\n[1,0,2,5,7]\n[4,2]\n', 0),
    ('U08', 'L5', 'Abs, Sign, Clamp',
     ['print Abs(-3)', 'print Abs(-2.50)', 'print Abs(-0.5f)', 'print Sign(-7)', 'print Sign(0)', 'print Sign(0.25)', 'print Clamp(15, 0, 10)',
      'print Clamp(-1, 0, 10)', 'print Clamp(2.5, 0, 10)'],
     '3\n2.50\n0.5\n-1\n0\n1\n10\n0\n2.5\n', 0),
    ('U09', 'L6', 'FromHex beside Hex', ['print FromHex("ff")', 'print Hex(255)'], '255\nff\n', 0),
    ('U10', 'L7', 'Decimals(n) as a setting is refused, naming Text and Round',
     HEAD + [T + 'Decimals(4)', 'end'],
     refused('U10', 4, 'there is no setting for places in a .haro file: write Text(x, iPlaces) or Round(x, iPlaces); written',
             'Decimals(4)'), 1),
    ('U11', 'L7', 'FAbs is refused, naming Abs',
     HEAD + [T + 'print FAbs(-1.5f)', 'end'],
     refused('U11', 4, '`FAbs` takes only a float: write Abs(x); written', 'FAbs'), 1),
    ('U12', 'L7', 'Dec is refused, naming FromHex',
     HEAD + [T + 'print Dec("ff")', 'end'],
     refused('U12', 4, '`Dec` reads hex text, and its name says decimal: write FromHex(t); written', 'Dec'), 1),
    ('U13', 'L8', 'a .ring file reads its own names as it did',
     ['decimals(3)', '? 1/3', '? fabs(-2)', '? dec("ff")'],
     '0.333\n2\n255\n', 0),
    ('U02', 'L1', 'a .ring file\'s decimals(n) does not reach .haro code',
     ['load "show.haro"', 'decimals(5)', 'Show(0.25)', '? 0.25'],
     '0.25\n0.25000\n', 0),
]
SHOW = ['func Show(pfX)', T + 'print pfX', 'end']


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    with open(os.path.join(HERE, 'cases', 'show.haro'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(SHOW) + '\n')
    out = []
    for cid, line, why, src, stdout, code in sorted(CASES, key=lambda c: c[0]):
        ext = '.ring' if cid in ('U13', 'U02') else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.66',
        'decision': 'HARO-NUMBERS-CORE-01: NUMBERS.md (ad4d0a5), the Principal\'s "Build it as proposed" (2026-11-12); Truncate left out, '
                    'said so; the desk\'s readings are D78',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'L1': 'a float written exactly; no setting', 'L2': 'Text', 'L3': 'Round, Floor, Ceil', 'L4': 'parts and digits',
                  'L5': 'Abs, Sign, Clamp', 'L6': 'FromHex', 'L7': 'refused: Decimals as a setting, FAbs, Dec', 'L8': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
