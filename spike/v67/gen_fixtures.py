"""Haro v0.67 -- maps (TYPES.md T6, HARO-MAP-01). Written FIRST, before the VM is touched.

THE RULING. TYPES.md T6 (D55): a map is `m`, "a key to a value, keys unique; what Softanza's pair lists were used for when the keys
vary"; section 6: a list of pairs entering an `m` name is converted, refused if a key repeats. The Principal, 2026-11-12, asked how a
map is written and what reading a missing key does, chose "A literal with key: value" and "A maybe, resolved with else":

    mAges = ["ada": 36, "bob": 41]
    mEmpty = [:]
    iAge = mAges["eve"] else 0

THE DESK'S READINGS (D79), judged below: a key is a text, in its exact case, or an integer -- any other is KEY_TYPE; a literal holds a
key once (DUPLICATE_KEY); writing `mX[k] = v` adds the key or replaces its value; insertion order is kept; `Keys`, `Values`, `HasKey`,
and `Del(mX, k)` (the list's `Del`, by key); `for vP in mX` gives each [key, value] pair; an `m` name holds a map, a `v` name no map; a
map is a value, copied when assigned; printed as written. A .ring caller's pair list at a .haro `m` parameter is a map. A .ring file
reads its pair lists as it did. v0.41's refusal of `:key = value` names the map.

THE LINES:
  M1  the literal, the empty map, a read resolved with else, a write that adds or replaces, Len
  M2  a read left unresolved is refused when compiling
  M3  keys: a text in its exact case, an integer; any other key KEY_TYPE; a literal's repeated key DUPLICATE_KEY
  M4  Keys, Values, HasKey, Del, in insertion order
  M5  an m name holds a map, a v name no map
  M6  a map is a value
  M7  printed as written
  M8  for-in gives the pairs
  M9  a .ring caller's pair list at an m parameter is a map
  M10 a .ring file is untouched
  M11 the refusal of :key = value names the map

  python spike/v67/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
HEAD = ['print "before"', 'f()', 'func f']
CSV = ['func Csv(vX)', T + 'tOut = ""', T + 'for i = 1 to Len(vX)', T + T + 'if i > 1', T + T + T + 'tOut += ","', T + T + 'end',
       T + T + 'tOut += String(vX[i])', T + 'end', T + 'return "[" + tOut + "]"', 'end']
MAPS = ['func Get(pmX)', T + 'return pmX["b"] else 0', 'end']


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


CASES = [
    ('G01', 'M1', 'the literal, the empty map, a read resolved with else, a write, Len',
     ['mAges = ["ada": 36, "bob": 41]', 'mEmpty = [:]', 'mAges["cyd"] = 29', 'mAges["ada"] = 37', 'print mAges["ada"] else 0',
      'print mAges["eve"] else 0', 'print Len(mAges)', 'print Len(mEmpty)'],
     '37\n0\n3\n0\n', 0),
    ('G02', 'M2', 'a read left unresolved is refused when compiling',
     HEAD + [T + 'mAges = ["ada": 36]', T + 'iAge = mAges["eve"]', 'end'],
     refused('G02', 5, 'a map\'s read may find nothing -- resolve it where it lands: x = E else D; written', 'mAges["eve"]'), 1),
    ('G03', 'M3', 'a text key in its exact case; an integer key',
     ['mX = ["Ada": 1]', 'print mX["ada"] else 0', 'print mX["Ada"] else 0', 'mN = [1: "one", 2: "two"]', 'print mN[2] else ""'],
     '0\n1\ntwo\n', 0),
    ('G04', 'M3', 'any other key is KEY_TYPE',
     HEAD + [T + 'mX = [1.5: "x"]', 'end'],
     trap('G04', 4, 'Error (KEY_TYPE) : a map\'s key is a text or an integer, and this is a decimal'), 1),
    ('G05', 'M3', 'a literal holds a key once',
     HEAD + [T + 'mX = ["a": 1, "a": 2]', 'end'],
     trap('G05', 4, 'Error (DUPLICATE_KEY) : the map holds the key "a" once'), 1),
    ('G06', 'M4', 'Keys, Values, HasKey, Del, in insertion order',
     ['mAges = ["ada": 36, "bob": 41, "cyd": 29]', 'print Csv(Keys(mAges))', 'print Csv(Values(mAges))', 'print HasKey(mAges, "bob")',
      'Del(mAges, "bob")', 'print HasKey(mAges, "bob")', 'print Csv(Keys(mAges))'] + CSV,
     '[ada,bob,cyd]\n[36,41,29]\ntrue\nfalse\n[ada,cyd]\n', 0),
    ('G07', 'M5', 'a vector literal given to an m name is refused when compiling',
     HEAD + [T + 'mX = [1, 2]', 'end'],
     refused('G07', 4, 'm is the letter of a map, and this literal is a vector; written', 'mX'), 1),
    ('G08', 'M5', 'a v name holds no map',
     HEAD + [T + 'vX = Make()', 'end', 'func Make', T + 'return ["a": 1]', 'end'],
     trap('G08', 4, 'Error (TYPE_LETTER) : `vX` is lettered v, a vector, and is given a map'), 1),
    ('G09', 'M6', 'a map is a value: assigning it copies it',
     ['mA = ["a": 1]', 'mB = mA', 'mB["a"] = 2', 'print mA["a"] else 0', 'print mB["a"] else 0'],
     '1\n2\n', 0),
    ('G10', 'M7', 'printed as written',
     ['mX = ["ada": 36, "bob": 41]', 'print mX', 'mE = [:]', 'print mE', 'mN = [1: "one"]', 'print mN'],
     '["ada": 36, "bob": 41]\n[:]\n[1: "one"]\n', 0),
    ('G11', 'M8', 'for-in gives each [key, value] pair',
     ['mX = ["a": 1, "b": 2]', 'for vP in mX', T + 'print vP[1]', T + 'print vP[2]', 'end'],
     'a\n1\nb\n2\n', 0),
    ('G12', 'M9', 'a .ring caller\'s pair list at an m parameter is a map',
     ['load "maps.haro"', '? Get([["a", 1], ["b", 2]])'],
     '2\n', 0),
    ('G13', 'M10', 'a .ring file reads its pair lists as it did',
     ['aL = [["Ada", 1]]', '? aL["ada"]'],
     '1\n', 0),
    ('G14', 'M11', 'the refusal of :key = value names the map',
     HEAD + [T + 'vP = [:a = 1]', 'end'],
     refused('G14', 4, '`:key = value` is no pair in a .haro file: write ["key": value] for a map, [:key, value] for a pair, or declare a '
                       'record for named fields (HARO-SURFACE-01)', ':a = 1'), 1),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    with open(os.path.join(HERE, 'cases', 'maps.haro'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(MAPS) + '\n')
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid in ('G12', 'G13') else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.67',
        'decision': 'HARO-MAP-01: TYPES.md T6 (D55), the Principal\'s "A literal with key: value" and "A maybe, resolved with else" '
                    '(2026-11-12); the desk\'s readings are D79',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'M1': 'literal, else, write, Len', 'M2': 'an unresolved read refused', 'M3': 'keys', 'M4': 'Keys, Values, HasKey, Del',
                  'M5': 'm holds a map, v no map', 'M6': 'a value', 'M7': 'printed as written', 'M8': 'for-in pairs',
                  'M9': 'a .ring pair list at an m parameter', 'M10': 'a .ring file untouched', 'M11': 'the pair refusal names the map'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
