"""Haro v0.42 -- case-exact names (D55, ruled 2026-11-07): in a .haro file a name is spelled as it is declared, and a keyword in another case is
no name. Written FIRST, before the compiler is touched.

THE RULINGS. The author, 2026-11-07, on the desk's advice (names case-exact, a collision by case refused): "I agree with you!"; on TYPES.md's
decision (e), a keyword in another case refused as PRINCIPLES 2.2 reads it and not a name as v0.41 read it: "Yes as recommended"; and on the
natives' spelling, asked with the measurement below: "Lowercase (Recommended)" -- a native is spelled as the VM registers it.

THE LINES.
  N1  a local, a parameter, a global, a function, a class, an attribute and a method are spelled where they are used as where they are declared;
      any other spelling is refused, naming the declared spelling and its line
  N2  a second spelling of a name in one scope is the same refusal: `oclient = 2` after `oClient = 1` is not a second variable
  N3  two functions whose names differ only by case are refused at a call of either, naming both
  N4  a native is spelled in lowercase, as the VM registers it: `isnull`, not `isNull`
  N5  a keyword in another case is no name in a .haro file (aNd, If, NULL; and Haro's block words, Using): refused, not read as a name
  N6  a .ring file folds case as Ring does, and a .haro file calls a .ring file's function by the spelling its definition gives

The refusal's words, so the courts pin them:
  one spelling per name -- declared `X` at line R; written `x`          (X declared in the same file)
  one spelling per name -- declared `X` in F; written `x`               (X declared in another file F)
  two functions differ only by case -- `Foo` at line R and `foo` at line S; written `Foo`
  a native is spelled in lowercase -- `isnull`; written `isNull`
  a keyword in another case is no name -- `and` is a keyword; written `aNd`

MEASURED before the rung (runtime/v42/spell_scan.py, Haro's 34 code files, lexical): 2,000 native calls, 433 not in lowercase (isNull 377, isString
31, isList 16, isNumber 8, isWindows 1); 8 words written in two spellings in one file (cT/ct, aFS/aFs, aPts/aPtS ...), each to be read as one name
or two; no keyword in another case (v0.41 lowered them).

On haro 9c6a080, before this rung: `oclient` reads `oClient`, `foo()` reaches `Foo` silently (the first of two wins), `o.getx()` reaches `GetX`,
`isNull` is `isnull`, `aNd = 1` is a name.

  python spike/v42/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
REFUSED = 'and did not compile it -- running past it would give a wrong answer '


def why_decl(decl, row):
    return f'one spelling per name -- declared `{decl}` at line {row}; written'


def refused(cid, line, why, text, called=2, where='function f()'):
    """the program prints "before", then f() (called at line `called`) is stopped at its refused statement"""
    return ['before', '', f'Line {line} Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) ' + REFUSED,
            f'In {where} in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


B = '? "before"'
CASES = [
    ('N01', 'N1', 'every kind of name spelled as declared runs', '.haro', [
        '$nTotal = 10', 'f()', 'func f', T + 'oClient = 2', T + '? oClient + Twice(3)', T + '? isnull(null)', T + 'o = new Point',
        T + '? o.GetX()', T + '? $nTotal', 'func Twice nN', T + 'return nN * 2', 'class Point', T + '@nX = 3', T + 'func GetX', T * 2 + 'return @nX'],
     ['8', 'true', '3', '10']),
    # N01 CHANGED AFTER ITS COURT SPOKE, 2026-11-08: `isnull(null)` answers a boolean in a .haro file and prints `true` (v0.43, D55 T3,
    # the author's ruling of 2026-11-07); the case asks the same question.
    ('N02', 'N1', 'a local read in another spelling is refused', '.haro', [
        B, 'f()', 'func f', T + 'oClient = 1', T + '? oclient'],
     refused('N02', 5, why_decl('oClient', 4), 'oclient'), 1),
    ('N03', 'N2', 'a local assigned in another spelling is no second variable: refused', '.haro', [
        B, 'f()', 'func f', T + 'oClient = 1', T + 'oclient = 2', T + '? oClient'],
     refused('N03', 5, why_decl('oClient', 4), 'oclient'), 1),
    ('N04', 'N1', 'a parameter used in another spelling is refused', '.haro', [
        B, 'f(1)', 'func f nCount', T + '? ncount'],
     refused('N04', 4, why_decl('nCount', 3), 'ncount'), 1),
    ('N05', 'N1', 'a function called in another spelling is refused', '.haro', [
        B, 'f()', 'func f', T + '? twice(2)', 'func Twice nN', T + 'return nN * 2'],
     refused('N05', 4, why_decl('Twice', 5), 'twice'), 1),
    ('N06', 'N3', 'two functions differing only by case: a call of either is refused, naming both', '.haro', [
        B, 'f()', 'func f', T + '? Foo()', 'func Foo', T + 'return 1', 'func foo', T + 'return 2'],
     refused('N06', 4, 'two functions differ only by case -- `Foo` at line 5 and `foo` at line 7; written', 'Foo'), 1),
    ('N07', 'N4', 'a native in another case is refused: natives are lowercase', '.haro', [
        B, 'f()', 'func f', T + '? isNull(null)'],
     refused('N07', 4, 'a native is spelled in lowercase -- `isnull`; written', 'isNull'), 1),
    ('N08', 'N1', 'a class named in another spelling is refused', '.haro', [
        B, 'f()', 'func f', T + 'o = new point', 'class Point'],
     refused('N08', 4, why_decl('Point', 5), 'point'), 1),
    ('N09', 'N1', 'a global used in another spelling is refused', '.haro', [
        '$nTotal = 1', B, 'f()', 'func f', T + '? $ntotal'],
     refused('N09', 5, why_decl('$nTotal', 1), '$ntotal', called=3), 1),
    ('N10', 'N1', 'an attribute used in another spelling is refused', '.haro', [
        B, 'o = new Point', '? o.GetX()', 'class Point', T + '@nX = 3', T + 'func GetX', T * 2 + 'return @nx'],
     refused('N10', 7, why_decl('@nX', 5), '@nx', called=3, where='method getx()'), 1),
    ('N11', 'N1', 'a method called in another spelling is refused', '.haro', [
        B, 'f()', 'func f', T + 'o = new Point', T + '? o.getx()', 'class Point', T + 'func GetX', T * 2 + 'return 3'],
     refused('N11', 5, why_decl('GetX', 7), 'getx'), 1),
    ('N12', 'N5', 'a keyword in another case is no name in a .haro file', '.haro', [
        B, 'f()', 'func f', T + 'aNd = 1', T + '? aNd'],
     refused('N12', 4, 'a keyword in another case is no name -- `and` is a keyword; written', 'aNd'), 1),
    ('N13', 'N6', 'a .ring file folds case as Ring does: locals, natives, functions', '.ring', [
        'f()', 'func f', T + 'oClient = 1', T + '? oclient', T + '? isNull(NULL)', T + '? twice(2)', 'func Twice nN', T + 'return nN * 2'],
     ['1', '1', '4']),
    ('N14', 'N6', 'a .haro file calls a .ring function by its definition\'s spelling; another spelling is refused', '.haro', [
        'load "N14_lib.ring"', '? StzThing()', '? stzthing()'],
     ['7', '', 'Line 3 Haro refused this statement (one spelling per name -- declared `StzThing` in N14_lib.ring; written `stzthing`, line 3 of N14.haro) '
      + REFUSED, 'in file N14.haro '], 1, {'N14_lib.ring': ['func StzThing', T + 'return 7']}),
    # N14 CORRECTED AFTER THE COURT SPOKE: a refusal at a file's top level prints `in file N14.haro ` with a trailing space, as every top-level
    # trap does (v41's probe printed it too); the fixture as first written left the space out -- a transcription slip, not a change of rule.
    # WRITTEN AFTER THE CODE, found while building it: a bare attribute in a method is checked as an @attribute is (N15); a member named like a
    # keyword in another case is refused, since a .ring class's keyword-shaped method is declared lowered and a .haro one may not be named so
    # (N16); an eval in a .haro program spells as the root does, its refusal the eval's own error (N17, N18).
    ('N15', 'N1', 'a bare attribute read in a method in another spelling is refused', '.haro', [
        B, 'o = new App', '? o.GetX()', 'class App', T + 'nX = 3', T + 'func GetX', T * 2 + 'return nx'],
     refused('N15', 7, why_decl('nX', 5), 'nx', called=3, where='method getx()'), 1),
    ('N16', 'N5', 'a member named like a keyword in another case is refused', '.haro', [
        B, 'f()', 'func f', T + 'o = new App', T + 'x = o.See()', 'class App', T + 'func See', T * 2 + 'return 1'],
     refused('N16', 5, 'a keyword in another case is no name -- `see` is a keyword; written', 'See'), 1),
    ('N17', 'N1', 'an eval in a .haro program spells a local as declared', '.haro', [
        'f()', 'func f', T + 'nA = 4', T + 'eval("? na")'],
     ['', 'Line 4 Error (E1) : one spelling per name -- declared `nA`; written `na` ', 'In function f() in file N17.haro', '',
      'Called from line 1 in file N17.haro '], 1),
    ('N18', 'N5', 'an eval in a .haro program refuses a keyword in another case', '.haro', [
        'f()', 'func f', T + 'eval("aNd = 4")'],
     ['', 'Line 3 Error (E1) : a keyword in another case is no name -- `and` is a keyword; written `aNd` ', 'In function f() in file N18.haro', '',
      'Called from line 1 in file N18.haro '], 1),
    # WRITTEN AFTER THE PLANTS: plant P7 (the hook where a global is written) MISSED, because every case read its global; N19 writes one.
    ('N19', 'N2', 'a global assigned in another spelling is no second global: refused', '.haro', [
        B, '$nTotal = 1', '$ntotal = 2', '? $nTotal'],
     ['before', '', 'Line 3 Haro refused this statement (one spelling per name -- declared `$nTotal` at line 2; written `$ntotal`, line 3 of N19.haro) '
      + REFUSED, 'in file N19.haro '], 1),
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
    if len(row) > 7:
        for fname, lines in row[7].items():
            with open(os.path.join(HERE, 'cases', fname), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(lines) + '\n')
    out.append(case)
doc = {'rung': 'v0.42', 'decision': 'D55 (a ruled part): names case-exact in a .haro file; a keyword in another case no name; natives lowercase',
       'lines': {'N1': 'a name is spelled where used as where declared', 'N2': 'a second spelling in one scope is refused, not a second name',
                 'N3': 'two functions differing only by case are refused at a call, naming both', 'N4': 'a native is spelled in lowercase',
                 'N5': 'a keyword in another case is no name in a .haro file', 'N6': 'a .ring file folds case; a .haro file calls it as defined'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
