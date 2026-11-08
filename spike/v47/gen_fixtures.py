"""Haro v0.47 -- a name's first letter is its type, and the compiler holds it to it (D55 T2), in a .haro file. Written FIRST, before the
compiler or the VM is touched.

THE RULINGS. D55 (a), the author 2026-11-07: "letters on every name ... yes"; and on this rung's scope, asked with the measurement below,
2026-11-08: "Yes, as recommended" -- check the letters whose types exist, re-letter Haro's code by rule, the `a` names wait for v0.50
(map and record) so each is renamed once, a single lowercase letter only as a loop counter.

THE LINES, in a .haro file (a .ring file is untouched):
  Y1  a value's name -- local, parameter, global, attribute -- begins with a type's letter then a capital: one of D55's sixteen
      (b i d f n t x k v m r o e h s w) or `a`, Softanza's list, accepted until v0.50 letters it v, m or r. A name with no letter is refused
      when compiling; Softanza's `c` is refused with t as its todo
  Y2  a single lowercase letter is a name only as a `for` counter or a `catch` name
  Y3  the letters whose types exist are checked: b boolean, i integer, n any number, f a number (until v0.48 splits float from decimal),
      t text, v vector, o object, h handle. A literal of another type is refused when compiling; any other value is checked where it is
      assigned -- a statement, a parameter on entry, a `for` counter -- and raises TYPE_LETTER
  Y4  the letters whose types are not built yet (a d k x m r e s w) are accepted and not checked, each until its rung
  Y5  the empty text NULL is absence until v0.49 builds `none`, and passes any letter

THE DESK'S READINGS, recorded as its own (the ruling's scope, read):
  - `n` on a local stays accepted until v0.48: D55 (f) keeps n for parameters, but a local lettered i now would be relettered d when a
    pointed literal becomes a decimal -- renamed once, as the ruling keeps the `a` names
  - functions, methods and classes are not lettered: a letter names the type of a VALUE

MEASURED before the rung (study/v47/letters.py, Haro's 69 code files): 2,949 declared names -- a 1,617, c 757, n 223, b 162, single
letters 126, words 33, t 24 (tokens), v 4, x 3.

  python spike/v47/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
REFUSED = 'and did not compile it -- running past it would give a wrong answer '


def refused(cid, line, why, text, called=2, where='function f()'):
    return ['before', '', f'Line {line} Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) ' + REFUSED,
            f'In {where} in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


def letter_err(cid, line, name, letter, word, got, called=2, where='function f()'):
    return ['before', '', f'Line {line} Error (TYPE_LETTER) : `{name}` is lettered {letter}, {word}, and is given {got} ',
            f'In {where} in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


B = '? "before"'
CASES = [
    ('Y01', 'Y3', 'every checked letter holding its own type runs', '.haro', [
        'f()', 'func f', T + 'bOk = 1 < 2', T + 'iN = 3', T + 'nX = 2.5', T + 'fX = 0.5', T + 'tName = "ada"', T + 'vItems = [1, 2]',
        T + 'oP = new P', T + 'hF = fopen("Y01.txt", "w")', T + 'fclose(hF)', T + '? bOk', T + '? iN + 1', T + '? nX', T + '? tName',
        T + '? len(vItems)', T + '? oP.iX', 'class P', T + 'iX = 7'],
     ['true', '4', '2.50', 'ada', '2', '7']),
    ('Y02', 'Y1', 'a name with no letter is refused when compiling', '.haro', [B, 'f()', 'func f', T + 'count = 3'],
     refused('Y02', 4, 'a name begins with its type\'s letter -- `count` has none; written', 'count'), 1),
    ('Y03', 'Y1', 'Softanza\'s c is no letter in a .haro file', '.haro', [B, 'f()', 'func f', T + 'cName = "ada"'],
     refused('Y03', 4, '`c` is Softanza\'s letter and no type\'s -- text is t: tName; written', 'cName'), 1),
    ('Y04', 'Y3', 'a literal of another type is refused when compiling', '.haro', [B, 'f()', 'func f', T + 'tName = 3'],
     refused('Y04', 4, 't is the letter of a text, and this literal is an integer; written', 'tName'), 1),
    ('Y05', 'Y3', 'a value of another type raises TYPE_LETTER where it is assigned', '.haro', [
        B, 'f()', 'func f', T + 'nX = Word()', 'func Word', T + 'return "abc"'],
     letter_err('Y05', 4, 'nX', 'n', 'a number', 'a text'), 1),
    ('Y06', 'Y3', 'a parameter is checked on entry', '.haro', [B, 'f()', 'func f', T + 'Twice("3")', 'func Twice iN', T + 'return iN * 2'],
     ['before', '', 'Line 5 Error (TYPE_LETTER) : `iN` is lettered i, an integer, and is given a text ', 'In function twice() in file Y06.haro', '',
      'Called from line 4 In function f() in file Y06.haro', '', 'Called from line 2 in file Y06.haro '], 1),
    ('Y07', 'Y2', 'a single letter is a for counter, of either form, and a catch name', '.haro', [
        'f()', 'func f', T + 'for i = 1 to 2', T * 2 + '? i', T + 'next', T + 'for x in [5, 6]', T * 2 + '? x', T + 'next', T + 'try',
        T * 2 + 'raise("no")', T + 'catch e', T * 2 + '? e.Message()', T + 'done'],
     ['1', '2', '5', '6', 'no']),
    ('Y08', 'Y2', 'a single letter anywhere else is refused', '.haro', [B, 'f()', 'func f', T + 'x = 3'],
     refused('Y08', 4, 'a name begins with its type\'s letter -- `x` has none; written', 'x'), 1),
    ('Y09', 'Y4', 'a letter whose type is not built yet is accepted and not checked', '.haro', [
        'f()', 'func f', T + 'aRows = 5', T + 'mIndex = "k"', T + 'rUser = [1]', T + '? aRows', T + '? mIndex', T + '? len(rUser)'],
     ['5', 'k', '1']),
    ('Y10', 'Y5', 'null is absence until v0.49, and passes any letter', '.haro', [
        'f()', 'func f', T + 'oDoc = null', T + 'vItems = null', T + 'iN = null', T + '? isnull(oDoc) and isnull(vItems) and isnull(iN)'],
     ['true']),
    ('Y11', 'Y1', 'a .ring file is untouched: no letter, Softanza\'s c, a single letter', '.ring', [
        'f()', 'func f', T + 'count = 3', T + 'cName = 5', T + 'x = "a"', T + 'tName = 3', T + '? count + cName', T + '? x + tName'],
     ['8', 'a3']),
    ('Y12', 'Y3', 'an integer letter refuses a number with a point when compiling', '.haro', [B, 'f()', 'func f', T + 'iN = 2.5'],
     refused('Y12', 4, 'i is the letter of an integer, and this literal is a number; written', 'iN'), 1),
    ('Y13', 'Y1', 'a global and an attribute are lettered too', '.haro', [
        '$iTotal = 1', 'o = new P', '? $iTotal', 'class P', T + 'count = 2'],
     ['', 'Line 5 Haro refused this statement (a name begins with its type\'s letter -- `count` has none; written `count`, line 5 of Y13.haro) '
      + REFUSED, 'in file Y13.haro '], 1),
    ('Y14', 'Y3', 'a for counter is checked as its letter says, and a lettered counter too', '.haro', [
        B, 'f()', 'func f', T + 'for tW in [1]', T * 2 + '? tW', T + 'next'],
     letter_err('Y14', 4, 'tW', 't', 'a text', 'an integer'), 1),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for row in CASES:
    cid, line, why, ext, prog, want = row[:6]
    name = f'cases/{cid}{ext}'
    with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(prog) + '\n')
    case = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': '\n'.join(want) + '\n'}
    if len(row) > 6 and row[6]:
        case['stdout'] = '\n'.join(want)
        case['exit'] = row[6]
    out.append(case)
doc = {'rung': 'v0.47', 'decision': 'D55 T2: a name\'s first letter is its type, checked, in a .haro file; the scope as the author ruled it 2026-11-08',
       'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
       'lines': {'Y1': 'a value\'s name begins with a type\'s letter', 'Y2': 'a single letter only as a for counter or a catch name',
                 'Y3': 'the letters whose types exist are checked', 'Y4': 'the others are accepted until their rungs',
                 'Y5': 'NULL passes any letter until v0.49'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
