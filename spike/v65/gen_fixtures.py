"""Haro v0.65 -- a .haro decimal crossing into .ring code is a float (HARO-RINGBOUNDARY-DECIMAL-OUT-01). Written FIRST, before the VM is
touched.

THE FINDING. stzlib-haroport, 2026-11-12 13:10, module 3 on v0.63: stzPattern.haro's cycle positions, decimals, reach the guard
sound_mu3 (.ring) under decimals(4) and print as 0.000000000000001, 0.333333333333334 -- Ring's decimals(n) formats a float, and a
decimal stayed a decimal in .ring code. The guard expects "c@0 b@0.3333 a@0.6667", as the positions printed when they were floats.

THE READING (D77), AMENDED BEFORE THE CODE WAS WRITTEN, said so. It was StzLib's (a), a decimal converted to a float where it crosses
into .ring code. StzLib then found (2026-11-12) that the decimals sound_mu3 reads are list items, two levels deep in a returned list,
which no conversion of a bare answer reaches, and walking every list a .haro function returns would cost each return its size. So: in
.ring code a decimal is Ring's number, wherever it came from -- an answer, an argument, a list item, an attribute. It prints and becomes
text as Ring writes a number (decimals(n)), and type() answers NUMBER; Ring's arithmetic already reads it as a number. Nothing is
converted at a boundary, so a decimal that passes through .ring code and back to .haro is still exact. E5-E7 were added with the
amendment, before the code.

THE LINES:
  E1  a .haro function's decimal printed by a .ring caller is formatted by decimals(n), and type() is NUMBER
  E2  a .haro caller's decimal at a .ring function's parameter is Ring's number there
  E3  a .haro caller keeps its decimal
  E4  the round trip: a .ring fraction is a decimal in .haro (v0.63) and Ring's number again when it comes back
  E5  a decimal inside a returned list, joined into text by .ring code: StzLib's case
  E6  a list of decimals printed by .ring code
  E7  a decimal that passes through .ring code comes back to .haro exact

  python spike/v65/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
DEC = ['func Third', T + 'return Divide(1, 3, 15)', 'end', 'func Tenth', T + 'return 0.1', 'end', 'func Echo(pxV)', T + 'return pxV',
       'end', 'func Rows', T + 'return [[0.000000000000001, "c"], [Divide(1, 3, 15), "b"]]', 'end']
KIND = ['func Kind x', T + 'return type(x)', 'func Twice x', T + 'return x * 2', 'func Same x', T + 'return x']

CASES = [
    ('O01', 'E1', 'the finding: a .haro decimal answered to .ring code is formatted by decimals(n)', '.ring',
     ['load "dec.haro"', 'decimals(4)', '? Third()', '? Tenth() * 3', '? type(Third())'],
     '0.3333\n0.3000\nNUMBER\n', 0),
    ('O02', 'E2', 'a .haro caller\'s decimal at a .ring function\'s parameter is a float', '.haro',
     ['load "kind.ring"', 'print Kind(0.5)', 'print Twice(0.25)'],
     'NUMBER\n0.5\n', 0),
    ('O03', 'E3', 'a .haro caller keeps its decimal', '.haro',
     ['load "dec.haro"', 'print Type(Tenth())', 'print Tenth() * 3 = 0.3'],
     'DECIMAL\ntrue\n', 0),
    ('O04', 'E4', 'the round trip: .ring to .haro is a decimal, and back to .ring a float', '.ring',
     ['load "dec.haro"', '? type(Echo(0.25))', '? Echo(0.25) + 1'],
     'NUMBER\n1.25\n', 0),
    ('O05', 'E5', 'StzLib\'s case: a decimal two levels deep in a returned list, joined into text by .ring code', '.ring',
     ['load "dec.haro"', 'decimals(4)', 'vR = Rows()', '? vR[2][2] + "@" + vR[2][1]', '? "" + vR[1][1]', '? string(vR[2][1])'],
     'b@0.3333\n0.0000\n0.3333\n', 0),
    ('O06', 'E6', 'a list of decimals printed by .ring code', '.ring',
     ['load "dec.haro"', 'decimals(4)', '? Rows()[2]'],
     '0.3333\nb\n', 0),
    ('O07', 'E7', 'a decimal that passes through .ring code comes back to .haro exact', '.haro',
     ['load "kind.ring"', 'print Type(Same(0.1))', 'print Same(0.1) * 3 = 0.3'],
     'DECIMAL\ntrue\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    for name, lines in (('dec.haro', DEC), ('kind.ring', KIND)):
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
        'rung': 'v0.65',
        'decision': 'HARO-RINGBOUNDARY-DECIMAL-OUT-01 (stzlib-haroport, 2026-11-12), its reading (a); the desk\'s reading is D77',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'E1': 'a .haro decimal answered to .ring code is a float', 'E2': 'a .haro decimal at a .ring parameter is a float',
                  'E3': 'a .haro caller keeps its decimal', 'E4': 'the round trip'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
