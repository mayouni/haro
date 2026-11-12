"""Haro v0.61 -- structure, its letters: `a` retires, `e` is checked (TYPES.md T6, HARO-STRUCTURE-01). Written FIRST, before the compiler
is touched.

THE RULING. TYPES.md T6 (D55): a vector is `v`, a map `m`, a record `r`, an object `o`, an error `e` -- "the caught value of v0.37 made a
type of its own"; T2 kept `a` "until structure". The Principal: "Start structure" (2026-11-12). The desk's readings (D73): T6 is built in
three rungs -- its letters (this one), records (v0.62), maps (v0.63) -- because the last two are new kinds of value.

THE LINES:
  S1  `a` is no type's letter: a name lettered `a` is refused, naming `v` (a vector) and `x` (any value); a parameter keeps its p mark
  S2  `e` is checked: an error -- the value a catch binds -- and nothing else
  S3  a .ring file untouched

  python spike/v61/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


HEAD = ['print "before"', 'f()', 'func f']

CASES = [
    ('Q01', 'S1', 'a name lettered a is refused, naming v and x', HEAD + [T + 'aList = [1, 2]', T + 'print Len(aList)', 'end'],
     refused('Q01', 4, '`a` is no type\'s letter -- a vector is v, any value x: vList or xList; written', 'aList'), 1),
    ('Q02', 'S1', 'a parameter lettered a keeps its p mark in the todo', ['print "before"', 'f([1])', 'func f(paItems)', T + 'print Len(paItems)',
                                                                           'end'],
     refused('Q02', 3, '`a` is no type\'s letter -- a vector is v, any value x: pvItems or pxItems; written', 'paItems'), 1),
    ('Q03', 'S1', 'v and x hold what a held', ['vList = [1, 2]', 'xAny = "t"', 'xAny = [3]', 'print Len(vList) + Len(xAny)'],
     '3\n', 0),
    ('Q04', 'S2', 'a catch binds an error to an e name', ['try', T + 'Raise("boom")', 'catch eErr', T + 'print eErr.Message()', 'end'],
     'boom\n', 0),
    ('Q05', 'S2', 'an e name given a text is refused where it is given', HEAD + [T + 'eErr = Upper("a")', 'end'],
     trap('Q05', 4, 'Error (TYPE_LETTER) : `eErr` is lettered e, an error, and is given a text'), 1),
    ('Q06', 'S3', 'a .ring file reads its names as it did', ['aList = [1, 2]', '? len(aList)'],
     '2\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'Q06' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.61',
        'decision': 'HARO-STRUCTURE-01: TYPES.md T6 (D55), the Principal\'s "Start structure"; the desk\'s readings are D73',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'S1': 'a retires: v or x', 'S2': 'e is an error', 'S3': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
