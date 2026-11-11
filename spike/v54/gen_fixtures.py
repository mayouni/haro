"""Haro v0.54 -- the letter rule takes Softanza's p mark and a vector's element letter (HARO-LETTER-SOFTANZA-01). Written FIRST, before the
compiler is touched.

THE RULING. The Principal, 2026-11-11 05:59, ruling stzlib-haroport's HAROPORT-SPELLINGS-02 in chat (recorded at stzlib 18608e029,
base/doc/design/HAROPORT_SPELLINGS.md section 0), choosing among its options: (a) "Keep p as a mark" -- a parameter is p + its type letter +
a capital, `ptSubStr`, `piStartingAt`, as `$` and `@` stand before a letter; (c) "v + second letter" -- a vector keeps its element's letter
after v, `viPos`, `vtNames`, `voItems`; (d) "Keep constants in caps" -- a constant is its letter + capitals and underscores,
`$iMAX_NUMBER_SIZE`, `@tNL`. TYPES.md T2 read "a lowercase type letter followed by a capital"; this rung extends it so. The order -- these
letters before absence -- the Principal's in this desk's chat, 2026-11-11 ("Letters first").

THE DESK'S READINGS (D66), judged below:
  - the p mark names a PARAMETER: it is checked by the letter after it, and a name carrying it that is no parameter of its function is
    refused, naming the function; the parameter may be given a new value in its body, as any parameter
  - the element letter is CHECKED where a value is given, as every checked letter is (v0.47): the value is a vector and each item holds
    the element's type -- an item at a time, the first that does not named with its place
  - (d) holds already (a letter then a capital); a case pins it

THE LINES:
  E1  a parameter p + letter + capital: accepted, checked by its letter where it is given
  E2  a p name that is no parameter is refused, naming its function
  E3  v + element letter + capital: a vector each of whose items holds the element's type, checked where it is given
  E4  a constant: its letter and capitals and underscores
  E5  a .ring file is untouched

  python spike/v54/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def in_f(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return in_f(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


CASES = [
    ('L01', 'E1', 'a parameter written p + letter + capital is accepted and read', '.haro',
     ['f("ab", 2)', 'func f ptSubStr, piAt', T + '? ptSubStr', T + '? piAt + 1'],
     'ab\n3\n', 0),
    ('L02', 'E1', 'a p parameter is checked by the letter after p', '.haro',
     ['? "before"', 'f(5, 2)', 'func f ptSubStr, piAt', T + '? ptSubStr'],
     in_f('L02', 3, 'Error (TYPE_LETTER) : `ptSubStr` is lettered t, a text, and is given an integer'), 1),
    ('L03', 'E1', 'a p parameter may be given a new value in its body', '.haro',
     ['f("ab")', 'func f ptS', T + 'ptS = ptS + "!"', T + '? ptS'],
     'ab!\n', 0),
    ('L04', 'E2', 'a p name that is no parameter of its function is refused, naming the function', '.haro',
     ['? "before"', 'f()', 'func f', T + 'ptX = "a"'],
     refused('L04', 4, 'the p mark names a parameter -- `ptX` is none of f\'s; written', 'ptX'), 1),
    ('L05', 'E3', 'v + element letter + capital: vectors of their element\'s type', '.haro',
     ['viPos = [1, 2]', 'vtNames = ["a", "b"]', 'voItems = [new P]', 'vvRows = [[1], [2, 3]]', 'viNone = []',
      '? Len(viPos) + Len(vtNames) + Len(voItems) + Len(vvRows) + Len(viNone)', 'class P'],
     '7\n', 0),
    ('L06', 'E3', 'an item that does not hold the element\'s type is refused, with its place', '.haro',
     ['? "before"', 'f()', 'func f', T + 'viPos = [1, "a", 3]'],
     in_f('L06', 4, 'Error (TYPE_LETTER) : `viPos` is lettered vi, a vector of integers, and its item 2 is a text'), 1),
    ('L07', 'E3', 'a value that is no vector is refused as for v', '.haro',
     ['? "before"', 'f()', 'func f', T + 'vtNames = Upper("a")'],
     in_f('L07', 4, 'Error (TYPE_LETTER) : `vtNames` is lettered vt, a vector of texts, and is given a text'), 1),
    ('L08', 'E3', 'a parameter p + v + element letter is checked item by item where it is given', '.haro',
     ['? "before"', 'f([1, "x"])', 'func f pviPos', T + '? Len(pviPos)'],
     in_f('L08', 3, 'Error (TYPE_LETTER) : `pviPos` is lettered vi, a vector of integers, and its item 2 is a text'), 1),
    ('L09', 'E3', 'a vector of vectors checks each item is a vector', '.haro',
     ['? "before"', 'f()', 'func f', T + 'vvRows = [[1], 2]'],
     in_f('L09', 4, 'Error (TYPE_LETTER) : `vvRows` is lettered vv, a vector of vectors, and its item 2 is an integer'), 1),
    ('L10', 'E3', 'a plain v name still holds any vector', '.haro',
     ['vItems = [1, "a", [2]]', '? Len(vItems)'],
     '3\n', 0),
    ('L11', 'E4', 'a constant is its letter and capitals and underscores, a global, an attribute or a local', '.haro',
     ['$iMAX_NUMBER_SIZE = 5', '$oP = new P', 'f()', 'func f', T + 'tSEP = "-"', T + '? $iMAX_NUMBER_SIZE', T + '? tSEP + $oP.tNL', 'class P',
      T + 'tNL = "n"'],
     '5\n-n\n', 0),
    ('L12', 'E1', 'Softanza\'s c after p is refused, its todo the t form with p kept', '.haro',
     ['? "before"', 'f("a")', 'func f pcName', T + '? pcName'],
     refused('L12', 3, '`c` is Softanza\'s letter and no type\'s -- text is t: ptName; written', 'pcName'), 1),
    ('L13', 'E5', 'a .ring file reads its names as it did', '.ring',
     ['f("a")', 'func f pcName', T + 'anPos = "x"', T + '? pcName + anPos'],
     'ax\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
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
        'rung': 'v0.54',
        'decision': 'HARO-LETTER-SOFTANZA-01: the Principal\'s HAROPORT-SPELLINGS-02 (a), (c), (d), 2026-11-11; the desk\'s readings are D66',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'E1': 'a p parameter, checked by its letter', 'E2': 'a p name that is no parameter refused',
                  'E3': 'v + element letter, each item checked', 'E4': 'a constant in capitals', 'E5': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
