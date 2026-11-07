"""Haro v0.41 -- HARO-SURFACE-01: a .haro file is read by Haro's rules, a .ring file by Ring's. Written FIRST, before the grammar, the lift or the
compiler is touched.

THE RULINGS. The author, in the session, 2026-11-06, after `aNd` -- a variable -- was read as the keyword `and`: "I don't the aNd error to happen
in Haro so fix it by design. don't feel constrained by Ring heritage since we cut wit it, and hence we are not obliged to opt forcase inceseniftvity
if you find the inverse moure useful and more robust to Haro langyage"; and "the same thing applies to the use of : in :key = value turning it to a
list and the special undocumented case (in ring) of using :str and turning str to lowercase!!! i saw some code embracing this but we should not be
obliged to do so!!"

THE DECISION, the desk's under them (HARO-SURFACE-01). The extension of a file says how it is read:

  S1  in a .haro file a keyword is spelled in lowercase, exactly; any other spelling -- aNd, oK, If, NULL -- is a name
  S2  in a .ring file a keyword is Ring's, in any case: Softanza's code reads exactly as it did (`oK = ...` is the keyword ok, as on Ring)
  S3  in a .haro file a symbol keeps its spelling: :Name is "Name"; in a .ring file it is lowered, as Ring lowers it
  S4  in a .haro file `:key = value` is no pair: refused by name, and [:key, value] says it; in a .ring file it is Ring's pair
  S5  an eval reads its text by the rules of the program's root file
  S6  a program in .haro may load a .ring file: each file is read by its own rules
  S7  `haro fmt` reads each file by its rules: a .ring file's keywords are still keywords, a .haro file's mixed-case word still a name

Note, found while writing these: `? :Name = "name"` is itself Ring's pair -- the trap S4 closes -- so the comparisons go through a variable.

MEASURED before the rung (runtime/v41): stzlib origin/main f77486b5a, 7,126 .ring files -- keywords 79.6% lowercase, 16.2% Capital, 4.0% UPPER, 0.2%
in no single case (980 of them Softanza's o-prefix objects oN, oK, oR, read as keywords by Ring itself); 23,754 `:key = value` pairs; 25,914 symbols
with a capital. Haro's own .haro code: 293 NULL, 2 Other, 1 Catch -- the cost of S1, rewritten by this rung -- and no pair, no capital symbol.
On haro d169ea8 before this rung: `aNd = 1` in a .haro file is the keyword and (an ERROR node), `:Name` is "name", `[:a = 1]` is a pair.

  python spike/v41/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
REFUSED = 'and did not compile it -- running past it would give a wrong answer '
R_PAIR = '`:key = value` is no pair in a .haro file: write [:key, value] (HARO-SURFACE-01)'


def KEYWORD(word):
    return f'a keyword in another case is no name -- `{word}` is a keyword; written'


def refused(cid, ext, line, why, text, at, called):
    return ['before', '', f'Line {line} Haro refused this statement ({why} `{text}`, line {at} of {cid}{ext}) ' + REFUSED,
            f'In function f() in file {cid}{ext}', '', f'Called from line {called} in file {cid}{ext} ']


# (id, line, why, ext, program, expected, exit, extra files)
CASES = [
    # CHANGED AFTER THE COURT SPOKE, 2026-11-07, by the author's ruling (TYPES.md decision (e)): a keyword in another case is refused in a .haro
    # file, as PRINCIPLES 2.2 reads it, not read as a name as v0.41 first built it. S01, S02 and S14 now expect v0.42's refusal; the misreading
    # the author ruled against stays closed either way. S02's `isNull` is `isnull`, a native spelled as the VM registers it (v0.42's N4); S09's
    # eval no longer names a variable `aNd`.
    ('S01', 'S1', 'in a .haro file a word in no single case is no name and no keyword: aNd refused', '.haro', [
        '? "before"', 'f()', 'func f', T + 'aNd = 1', T + 'oN = 2', T + '? aNd + oN'],
     refused('S01', '.haro', 4, KEYWORD('and'), 'aNd', 4, 2), 1),
    ('S02', 'S1', 'in a .haro file a Capital or UPPER keyword is refused; the lowercase word is the keyword', '.haro', [
        '? "before"', 'f()', 'func f', T + 'if isnull(null)', T * 2 + '? "null is the keyword"', T + 'ok', T + 'If = "a name"'],
     ['before', 'null is the keyword', ''] + refused('S02', '.haro', 7, KEYWORD('if'), 'If', 7, 2)[2:], 1),
    ('S03', 'S2', 'in a .ring file the keywords are Ring\'s in any case: If, See, Ok -- and oK, as Ring reads it', '.ring', [
        'f()', 'func f', T + 'x = 1', T + 'If x = 1', T * 2 + 'See "yes" + nl', T + 'Ok', T + 'oK = "fine"'],
     ['yes']),
    ('S04', 'S3', 'in a .haro file a symbol keeps its spelling', '.haro', [
        'f()', 'func f', T + '? :Name', T + '? :name', T + 'x = :Name', T + '? x = "Name"'],
     ['Name', 'name', '1']),
    ('S05', 'S3', 'in a .ring file a symbol is lowered, as Ring lowers it', '.ring', [
        'f()', 'func f', T + '? :Name', T + 'x = :Name', T + '? x = "name"'],
     ['name', '1']),
    ('S06', 'S4', 'in a .haro file `:key = value` is refused by name', '.haro', [
        '? "before"', 'f()', 'func f', T + 'aL = [:a = 1]', T + '? len(aL)'],
     refused('S06', '.haro', 4, R_PAIR, ':a = 1', 4, 2), 1),
    ('S07', 'S4', 'in a .haro file the pair is written as a list', '.haro', [
        'f()', 'func f', T + 'aL = [[:a, 1], [:Key, 2]]', T + '? aL[2][1]', T + '? len(aL)'],
     ['Key', '2']),
    ('S08', 'S4', 'in a .ring file `:key = value` is Ring\'s pair, and its key lowered', '.ring', [
        'f()', 'func f', T + 'aL = [:a = 1, :Key = 2]', T + '? aL[2][1]', T + '? len(aL)'],
     ['key', '2']),
    ('S09', 'S5', 'an eval in a .haro program reads by Haro\'s rules', '.haro', [
        'f()', 'func f', T + 'eval("? :Name")', T + 'eval("nA = 4  ? nA")'],
     ['Name', '4']),
    ('S10', 'S5', 'an eval in a .ring program reads by Ring\'s', '.ring', [
        'f()', 'func f', T + 'eval("? :Name")', T + 'eval("If 1 See \'ring\' + nl Ok")'],
     ['name', 'ring']),
    ('S11', 'S6', 'a .haro program loads a .ring file: each file is read by its own rules', '.haro', [
        'load "S11_lib.ring"', '? g()', '? :Name'],
     ['name', 'Name'], 0, {'S11_lib.ring': ['func g', T + 'If 1', T * 2 + 'Return :Name', T + 'Ok']}),
    # WRITTEN AFTER THE CODE, found by designing the plants: a .ring file's strings are not lowered (S12); the expression form of a pair is
    # refused as the list form is (S13); Haro's block words are lowercase, so a lone `Using` is a name (S14).
    ('S12', 'S2', 'in a .ring file the keywords inside a string are text, kept as written', '.ring', [
        'f()', 'func f', T + 'See "Ok, If and NULL" + nl', T + '? \'Return\''],
     ['Ok, If and NULL', 'Return']),
    ('S13', 'S4', 'in a .haro file `:key = value` given to a call is refused too', '.haro', [
        '? "before"', 'f()', 'func f', T + 'g(:k = 1)', 'func g x', T + 'return x'],
     refused('S13', '.haro', 4, R_PAIR, ':k = 1', 4, 2), 1),
    ('S14', 'S1', 'in a .haro file Haro\'s block words are lowercase too: a lone `Using` is refused', '.haro', [
        '? "before"', 'f()', 'func f', T + 'Using = 5'],
     refused('S14', '.haro', 4, KEYWORD('using'), 'Using', 4, 2), 1),
]

FMT = [
    ('K01', 'S7', '`haro fmt` on a .haro file: a word in no single case is a name, printed as written', '.haro', [
        'f()', 'func f', T + 'aNd = 1', T + 'oK = :Name', T + '? aNd'],
     ['f()', '', 'func f()', T + 'aNd = 1', T + 'oK = :Name', T + '? aNd']),
    ('K02', 'S7', '`haro fmt` on a .ring file: its keywords are Ring\'s in any case, printed in lowercase as before', '.ring', [
        'f()', 'func f', T + 'x = 1', T + 'If x = 1', T * 2 + 'See "yes" + nl', T + 'Ok', T + '? :Name'],
     ['f()', '', 'func f()', T + 'x = 1', T + 'if x = 1', T * 2 + 'see "yes" + nl', T + 'ok', T + '? :Name']),
    # WRITTEN AFTER THE CODE, found by plant P11 missing: the lowering reaches a .ring file's names spelled like keywords (a method Get, a member
    # See), and fmt printed them lowered until its leaves read the file's own bytes. The expected text is what `haro fmt` printed before the rung.
    ('K03', 'S7', '`haro fmt` on a .ring file: a name spelled like a keyword is printed as written', '.ring', [
        'f()', 'func f', T + 'o = new Foo', T + '? o.Get()', T + '? o.See', T + 'x = o.Done()', 'class Foo', T + 'func Get', T * 2 + 'return 1'],
     ['f()', '', 'func f()', T + 'o = new Foo', T + '? o.Get()', T + '? o.See', T + 'x = o.Done()', '', 'class Foo', T + 'func Get()', T * 2 + 'return 1']),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for kind, rows in (('run', CASES), ('fmt', FMT)):
    for row in rows:
        cid, line, why, ext, prog, want = row[:6]
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(prog) + '\n')
        case = {'id': cid, 'kind': kind, 'line': line, 'why': why, 'file': name, 'stdout': '\n'.join(want) + '\n'}
        if len(row) > 6 and row[6]:
            case['stdout'] = '\n'.join(want)
            case['exit'] = row[6]
        if len(row) > 7:
            for fname, lines in row[7].items():
                with open(os.path.join(HERE, 'cases', fname), 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write('\n'.join(lines) + '\n')
        out.append(case)
doc = {'rung': 'v0.41', 'decision': 'HARO-SURFACE-01: a .haro file read by Haro\'s rules, a .ring file by Ring\'s',
       'lines': {'S1': 'in a .haro file a keyword is lowercase, exactly; any other spelling is a name',
                 'S2': 'in a .ring file a keyword is Ring\'s, in any case',
                 'S3': 'a symbol keeps its spelling in a .haro file, and is lowered in a .ring file',
                 'S4': '`:key = value` is refused by name in a .haro file, and Ring\'s pair in a .ring file',
                 'S5': 'an eval reads by the rules of the program\'s root file',
                 'S6': 'each loaded file is read by its own rules',
                 'S7': 'haro fmt reads each file by its rules'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
