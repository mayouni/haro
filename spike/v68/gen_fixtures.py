"""Haro v0.68 -- in .ring code a boolean is the number 1 or 0 (HARO-RINGBOUNDARY-BOOL-OUT-01). Written FIRST, before the VM is touched.

THE FINDING. stzlib-haroport, 2026-11-12, module 5 (base/object): stzObject's b attributes hold true and false since the port, and
stzObject_defects_narrated.ring lists an object's attribute values and formats each with stzListShow.ring's FormatValue, which dispatches
on isNumber / isString / isList / isObject. A boolean matches none of them and raises "Unsupported value type". About 25 .ring sites
compare a .haro predicate's answer with 1.

THE READING (D80), the desk's, StzLib's (a), on v0.65's reading of a decimal: in .ring code a boolean is the number 1 or 0, wherever it
came from -- an answer, an argument, a list item, an attribute. There isNumber is 1, type() is NUMBER, it prints, joins into text and
string()s as 1 or 0, number() reads it, find() and sort() take it as its number, and it compares with 1 and 0 as before. Nothing is
converted at a boundary: a boolean that goes back to .haro code is still a boolean, and .haro code prints true and false.

FOUND WHILE PROBING, built in this rung, said so: in a .haro file Find([true, false], false) answered 0 -- find's equality had no case for
two booleans. A boolean finds a boolean; in .haro it meets no number (B11).

THE LINES:
  L1  .ring code prints a boolean as 1 or 0: alone, with see, as a list's item, as an object's attribute
  L2  type() is NUMBER and isNumber is 1
  L3  string(), number(), list2str and text joined with + read it as 1 or 0
  L4  it compares with 1 and 0 as before (held before the rung)
  L5  find() and sort() in .ring code take it as its number
  L6  StzLib's case: a dispatch on isNumber / isString over values a .haro function gave
  L7  a .haro caller's boolean at a .ring function's parameter is the number there
  L8  .haro code keeps true and false, and a boolean that passes through .ring code comes back a boolean
  L9  Find in a .haro file finds a boolean

  python spike/v68/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
BOOLS = ['func Yes', T + 'return true', 'end', 'func No', T + 'return false', 'end', 'func Both', T + 'return [true, false]', 'end',
         'func Mixed', T + 'return [true, "a", 2]', 'end', 'class Flag', T + 'bOk = true', T + 'nN = 1', 'end', 'func MakeFlag',
         T + 'return new Flag', 'end']
KIND = ['func Kind x', T + 'return type(x)', 'func Twice x', T + 'return x * 2', 'func Same x', T + 'return x']

CASES = [
    ('B01', 'L1', 'printed as 1 or 0 by .ring code: alone, with see, as a list\'s item', '.ring',
     ['load "bools.haro"', '? Yes()', '? No()', 'see Yes()', 'see nl', '? Both()', 'aL = [No(), 2]', '? aL'],
     '1\n0\n1\n1\n0\n\n0\n2\n\n', 0),
    ('B02', 'L1', 'an object\'s boolean attribute printed by .ring code', '.ring',
     ['load "bools.haro"', 'o = MakeFlag()', '? o', '? o.bOk'],
     'bok: 1\nnn: 1\n\n1\n', 0),
    ('B03', 'L2', 'type() is NUMBER and isNumber is 1', '.ring',
     ['load "bools.haro"', '? type(Yes())', '? isNumber(No())', '? isNumber(MakeFlag().bOk)', '? isString(Yes())'],
     'NUMBER\n1\n1\n0\n', 0),
    ('B04', 'L3', 'string(), number(), list2str and + read it as 1 or 0', '.ring',
     ['load "bools.haro"', '? string(Yes())', '? len(string(No()))', '? number(Yes()) + 1', '? list2str(Both())', '? "v=" + No()'],
     '1\n1\n2\n1\n0\nv=0\n', 0),
    ('B05', 'L4', 'it compares with 1 and 0 as before', '.ring',
     ['load "bools.haro"', 'if Yes() = 1 ? "yes is 1" ok', 'if No() = 0 ? "no is 0" ok', 'if Yes() != 0 ? "yes is not 0" ok',
      '? Yes() + 1'],
     'yes is 1\nno is 0\nyes is not 0\n2\n', 0),
    ('B06', 'L5', 'find() and sort() in .ring code take it as its number', '.ring',
     ['load "bools.haro"', '? find(Both(), 1)', '? find(Both(), 0)', '? find([1, 0], Yes())', '? sort([Yes(), No(), 0])'],
     '1\n2\n1\n0\n0\n1\n\n', 0),
    ('B07', 'L6', 'StzLib\'s case: a dispatch on isNumber and isString over values a .haro function gave', '.ring',
     ['load "bools.haro"', 'cOut = ""', 'for x in Mixed()', T + 'cOut += Fmt(x) + " "', 'next', '? cOut', 'func Fmt x',
      T + 'if isNumber(x) return "N" + x', T + 'but isString(x) return "S" + x', T + 'ok', T + 'raise("Unsupported value type")'],
     'N1 Sa N2 \n', 0),
    ('B08', 'L7', 'a .haro caller\'s boolean at a .ring function\'s parameter is the number there', '.haro',
     ['load "kind.ring"', 'print Kind(true)', 'print Twice(true)'],
     'NUMBER\n2\n', 0),
    ('B09', 'L8', '.haro code keeps true and false', '.haro',
     ['load "bools.haro"', 'print Yes()', 'print String(No())', 'print Type(Yes())', 'print IsNumber(true)'],
     'true\nfalse\nBOOLEAN\nfalse\n', 0),
    ('B10', 'L8', 'a boolean that passes through .ring code comes back a boolean', '.haro',
     ['load "kind.ring"', 'bX = Same(true)', 'print bX', 'print Type(Same(false))'],
     'true\nBOOLEAN\n', 0),
    ('B11', 'L9', 'Find in a .haro file finds a boolean, and a boolean meets no number', '.haro',
     ['print Find([true, false], false)', 'print Find([true, false], true)', 'print Find([1, 0], false)'],
     '2\n1\n0\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    for name, lines in (('bools.haro', BOOLS), ('kind.ring', KIND)):
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
        'rung': 'v0.68',
        'decision': 'HARO-RINGBOUNDARY-BOOL-OUT-01 (stzlib-haroport, 2026-11-12), its reading (a); the desk\'s reading is D80',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'L1': 'printed as 1 or 0', 'L2': 'type() NUMBER, isNumber 1', 'L3': 'string, number, list2str, +',
                  'L4': 'compares with 1 and 0', 'L5': 'find and sort', 'L6': 'StzLib\'s dispatch', 'L7': 'at a .ring parameter',
                  'L8': '.haro keeps its booleans', 'L9': 'Find finds a boolean in .haro'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
