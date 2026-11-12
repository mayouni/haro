"""Haro v0.65 -- a .haro decimal crossing into .ring code is a float (HARO-RINGBOUNDARY-DECIMAL-OUT-01). Written FIRST, before the VM is
touched.

THE FINDING. stzlib-haroport, 2026-11-12 13:10, module 3 on v0.63: stzPattern.haro's cycle positions, decimals, reach the guard
sound_mu3 (.ring) under decimals(4) and print as 0.000000000000001, 0.333333333333334 -- Ring's decimals(n) formats a float, and a
decimal stayed a decimal in .ring code. The guard expects "c@0 b@0.3333 a@0.6667", as the positions printed when they were floats.

THE READING (D77, StzLib's (a), the mirror of v0.63's D75): a decimal crossing from .haro into .ring code -- a .haro function's answer
to a .ring caller, a .haro caller's argument at a .ring function's parameter -- is the float nearest it. Ring code holds Ring's one
number type. A .haro caller keeps its decimals; a .ring file's own numbers are untouched.

THE LINES:
  E1  a .haro function's decimal answered to a .ring caller is a float: decimals(n) formats it, type() is NUMBER
  E2  a .haro caller's decimal at a .ring function's parameter is a float
  E3  a .haro caller keeps its decimal
  E4  the round trip: a .ring fraction is a decimal in .haro (v0.63) and a float again when it comes back

  python spike/v65/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
DEC = ['func Third', T + 'return Divide(1, 3, 15)', 'end', 'func Tenth', T + 'return 0.1', 'end', 'func Echo(pxV)', T + 'return pxV',
       'end']
KIND = ['func Kind x', T + 'return type(x)', 'func Twice x', T + 'return x * 2']

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
