"""Haro v0.64 -- records (TYPES.md T6, HARO-RECORD-01). Written FIRST, before the compiler is touched.

THE RULING. TYPES.md T6 (D55): a record is `r`, "named fields fixed when it is made", and "a record's fields are checked when
compiling: rUser.nmae is refused with did you mean name"; v0.41's refusal of `:key = value` points at the record once records land. The
Principal, 2026-11-12, asked how a record is written, chose "Declared, built in order":

    record User
        tName
        iAge
    end
    rAda = User("ada", 36)

THE DESK'S READINGS (D76), judged below: a record is a block of lettered fields, one per line, ended by `end`, in any place a definition
stands; it holds no method. It is built by its name with one value per field, in order -- the count checked when compiling, each value
checked against its field's letter where it is given. A field is read and written by name; a field the record lacks is refused when
compiling where the record's type is proven (a name given `User(...)`), naming the nearest field, and refused when running anywhere else
(NO_FIELD). An `r` name holds a record and nothing else; an `o` name an object and no record. A record is a value: assigning it copies it.
`new User` is refused -- a record is built by its name. A .ring file is untouched.

THE LINES:
  K1  declared, built by its name in field order, its fields read and written by name
  K2  the number of values is checked when compiling
  K3  a field the record lacks is refused when compiling, naming the nearest field
  K4  a value of another type for a field is refused where it is given
  K5  an r name holds a record and nothing else; an o name holds no record
  K6  a record is a value: assigning it copies it
  K7  new User is refused: a record is built by its name
  K8  a record holds no method
  K9  where the record's type is not proven, a missing field is refused when running (NO_FIELD), naming the nearest
  K10 a .ring file is untouched
  K11 v0.41's refusal of `:key = value` names the record

  python spike/v64/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
REC = ['record User', T + 'tName', T + 'iAge', 'end']
HEAD = ['print "before"', 'f()', 'func f']


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


CASES = [
    ('R01', 'K1', 'declared, built in field order, read and written by name',
     ['rAda = User("ada", 36)', 'print rAda.tName', 'rAda.iAge = 37', 'print rAda.iAge'] + REC,
     'ada\n37\n', 0),
    ('R02', 'K2', 'the number of values is checked when compiling',
     HEAD + [T + 'rU = User("ada")', 'end'] + REC,
     refused('R02', 4, '`User` is built from 2 values, in this order: tName, iAge; written', 'User("ada")'), 1),
    ('R03', 'K3', 'a field the record lacks is refused when compiling, naming the nearest',
     HEAD + [T + 'rU = User("ada", 36)', T + 'print rU.tNmae', 'end'] + REC,
     refused('R03', 5, '`User` has no field `tNmae` -- did you mean tName; written', 'rU.tNmae'), 1),
    ('R04', 'K3', 'a field the record lacks is refused when written to, and nothing near is named',
     HEAD + [T + 'rU = User("ada", 36)', T + 'rU.tCity = "x"', 'end'] + REC,
     refused('R04', 5, '`User` has no field `tCity`; written', 'rU.tCity'), 1),
    ('R05', 'K4', 'a value of another type for a field is refused where it is given',
     HEAD + [T + 'rU = User(36, 36)', 'end'] + REC,
     trap('R05', 4, 'Error (TYPE_LETTER) : `tName` is lettered t, a text, and is given an integer'), 1),
    ('R06', 'K5', 'an r name holds a record and nothing else',
     HEAD + [T + 'rX = new P', 'end', 'class P', 'end'],
     trap('R06', 4, 'Error (TYPE_LETTER) : `rX` is lettered r, a record, and is given an object'), 1),
    ('R07', 'K5', 'an o name holds no record',
     HEAD + [T + 'oX = User("a", 1)', 'end'] + REC,
     trap('R07', 4, 'Error (TYPE_LETTER) : `oX` is lettered o, an object, and is given a record'), 1),
    ('R08', 'K6', 'a record is a value: assigning it copies it',
     ['rA = User("ada", 36)', 'rB = rA', 'rB.iAge = 1', 'print rA.iAge', 'print rB.iAge'] + REC,
     '36\n1\n', 0),
    ('R09', 'K7', 'new User is refused: a record is built by its name',
     HEAD + [T + 'rU = new User', 'end'] + REC,
     refused('R09', 4, 'a record is built by its name, with its values: User(...); written', 'new User'), 1),
    ('R10', 'K8', 'a record holds no method',
     ['print "before"', 'record User', T + 'tName', T + 'def Hi', T + T + 'return 1', T + 'end', 'end'],
     '\nLine 4 Haro refused this statement (a record holds fields and no method; written `Hi`, line 4 of R10.haro) and did not compile it '
     '-- running past it would give a wrong answer \nin file R10.haro ', 1),
    ('R11', 'K9', 'where the type is not proven, a missing field is refused when running, naming the nearest',
     ['rU = User("ada", 36)', 'Show(rU)', 'func Show(prUser)', T + 'print prUser.tName', T + 'print prUser.tNmae', 'end'] + REC,
     'ada\n\nLine 5 Error (NO_FIELD) : `User` has no field `tNmae` -- did you mean tName \nIn function show() in file R11.haro\n\n'
     'Called from line 2 in file R11.haro ', 1),
    ('R12', 'K10', 'a .ring file is untouched: record is a name there',
     ['record = 5', '? record'],
     '5\n', 0),
    ('R13', 'K11', 'the refusal of :key = value names the record',
     HEAD + [T + 'vP = [:a = 1]', 'end'],
     refused('R13', 4, '`:key = value` is no pair in a .haro file: write [:key, value] for a pair, or declare a record for named fields '
                       '(HARO-SURFACE-01)', ':a = 1'), 1),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'R12' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.64',
        'decision': 'HARO-RECORD-01: TYPES.md T6 (D55), the Principal\'s "Declared, built in order" (2026-11-12); the desk\'s readings are D76',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'K1': 'declared, built in order', 'K2': 'the count checked when compiling', 'K3': 'a missing field refused when compiling',
                  'K4': 'a field\'s letter checked', 'K5': 'r holds a record, o no record', 'K6': 'a record is a value',
                  'K7': 'new User refused', 'K8': 'no method', 'K9': 'NO_FIELD when running', 'K10': 'a .ring file untouched',
                  'K11': 'the pair refusal names the record'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
