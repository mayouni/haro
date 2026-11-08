"""Haro v0.43 -- a real boolean, and no coercion (D55 T1 and T3, ruled 2026-11-07). Written FIRST, before the VM or the compiler is touched.

THE RULINGS. The author, 2026-11-07: "Ok but I noticed Haro holds no bolean type which was one of my strong critics to ring! Think of this
widely and redeesign a good correct typesystem for Haro"; and on TYPES.md: "Yes as recommended". T1: every value has exactly one type, and no
value changes type unasked -- `"1" + 1` refused, `1 = "1"` refused, an integer that overflows raises INTEGER_OVERFLOW and never becomes a
float. T3: `true` and `false` are the two values of `boolean`; a comparison answers a boolean; `if`, `while`, and `and`, `or`, `not` take
booleans only; a boolean prints `true` or `false`; it is not a number.

THE LINES.
  B1  in a .haro file `true` and `false` are the booleans: printed `true` and `false`, typed BOOLEAN
  B2  a comparison and `and`, `or`, `not` in a .haro file answer a boolean
  B3  a condition, and an operand of `and`, `or`, `not`, takes a boolean in a .haro file: a literal of another type is refused when
      compiling; any other value raises BOOLEAN_EXPECTED, naming its type and the comparison it may have meant
  B4  the natives that answer yes or no (isnull, isstring, isnumber, islist, isobject, ...) answer a boolean to a .haro file
  B5  a boolean is no number: in arithmetic or concatenation it raises NO_COERCION; string() of it is "true" or "false"
  B6  no coercion in a .haro file: text with a number under + - * / %, and a numeric text as a number, raise NO_COERCION; `=`, `!=` and the
      orderings between two types raise TYPE_MISMATCH (an integer and a float are one type of number until v0.45 splits them)
  B7  an integer in a .haro file stays an integer to 64 bits and raises INTEGER_OVERFLOW past them -- never a float
  B8  a .ring file reads as Ring reads: its coercions and its truth unchanged; a boolean reaching .ring code reads as 1 or 0 there, and a
      .ring function's 1 or 0 is an integer to a .haro condition (refused: the conversion at a b-name is v0.44's)

THE DESK'S READINGS, under D55's ruling, recorded as its own (no new ruling asked):
  - the error codes are the names TYPES.md already spells, in capitals, where Ring's are R-numbers: `Error (NO_COERCION) : ...`; a caught
    one answers them from Code()
  - the type names in a message: boolean, integer, number (a value with a point, until v0.45 calls it decimal or float), text, vector,
    object, none, handle
  - the F-98 exception (a number + nl is text) is a coercion and is not kept in a .haro file: `string(n) + nl`

The errors' words, so the courts pin them:
  a condition takes a boolean, and this is <type> -- say what is meant: <todo>
       todo: integer `x != 0`, number `x != 0`, text `x != ""`, vector `len(x) > 0`, otherwise `a comparison`
  <type> <op> <type> -- a value changes type only when asked: <todo>
       todo: text with a number `string(x)` or `number(x)`; a boolean `a comparison, or string(b)`
  <type> <op> <type> -- <op> compares two values of one type
  integer <op> integer leaves 64 bits

MEASURED before the rung, on haro 8c2e320:
  - statically (study/v43/cond_census.py, Haro's 35 code files): 2,931 conditions -- 1,696 comparisons, 733 logic, 288 calls named as
    predicates (isX, HasX), 120 other calls, 53 b-names, 30 subscripts (a list item used as a flag), 10 `while 1`; and 1,828 operands of
    and / or / not, of the same shapes. The non-boolean shapes are what B3 will refuse once their values stop being 0 or 1.
  - dynamically (study/v43/patch_census.py, a census build never committed: every coercion and every non-boolean truth test in code
    from a .haro file, one row per site, while the 47-stage guard ran on it -- PASS, 1,832 s, its twin the unpatched checked build):
    131 distinct lines, ALL of them `+` between a text and a number (6,864 + 2,034 hits; 3 sites with a float); 90 in the libraries and
    the forge, 41 in earlier rungs' case programs. No condition met a text, a vector, an object, none, or an integer other than 0 or 1;
    no `=` or ordering met two types; no arithmetic met a text. Rows: study/v43/census_lines.txt.

  python spike/v43/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
REFUSED = 'and did not compile it -- running past it would give a wrong answer '


def err(cid, line, code, msg, called=2, where='function f()'):
    """the program prints "before", then f() (called at line `called`) stops at `line` with a Haro error"""
    return ['before', '', f'Line {line} Error ({code}) : {msg} ', f'In {where} in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


def refused(cid, line, why, text, called=2, where='function f()'):
    return ['before', '', f'Line {line} Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) ' + REFUSED,
            f'In {where} in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


def cond(t, todo):
    return f'a condition takes a boolean, and this is {t} -- say what is meant: {todo}'


def coerce(a, op, b, todo):
    return f'{a} {op} {b} -- a value changes type only when asked: {todo}'


def mismatch(a, op, b):
    return f'{a} {op} {b} -- {op} compares two values of one type'


B = '? "before"'
CASES = [
    ('B01', 'B1', 'true and false print as themselves and are typed BOOLEAN', '.haro', [
        '? true', '? false', '? type(true)', '? [true, false]'],
     ['true', 'false', 'BOOLEAN', 'true', 'false', '']),
    ('B02', 'B2', 'a comparison and and, or, not answer a boolean', '.haro', [
        'f()', 'func f', T + 'bA = 1 < 2', T + '? bA', T + '? not (1 = 2)', T + '? (1 < 2) and (3 < 2)', T + '? "a" = "a"', T + '? type(2 > 1)'],
     ['true', 'true', 'false', 'true', 'BOOLEAN']),
    ('B03', 'B3', 'a condition that is a literal of another type is refused when compiling', '.haro', [
        B, 'f()', 'func f', T + 'while 1', T * 2 + 'exit', T + 'end'],
     refused('B03', 4, 'a condition takes a boolean -- this literal is an integer; written', '1'), 1),
    ('B04', 'B3', 'an integer in an if raises BOOLEAN_EXPECTED', '.haro', [
        B, 'f()', 'func f', T + 'nCount = 3', T + 'if nCount', T * 2 + '? "some"', T + 'ok'],
     err('B04', 5, 'BOOLEAN_EXPECTED', cond('an integer', 'x != 0')), 1),
    ('B05', 'B3', 'a text in a while raises BOOLEAN_EXPECTED', '.haro', [
        B, 'f()', 'func f', T + 'tName = "x"', T + 'while tName', T * 2 + 'exit', T + 'end'],
     err('B05', 5, 'BOOLEAN_EXPECTED', cond('a text', 'x != ""')), 1),
    ('B06', 'B3', 'a vector under not raises BOOLEAN_EXPECTED', '.haro', [
        B, 'f()', 'func f', T + 'vItems = [1, 2]', T + '? not vItems'],
     err('B06', 5, 'BOOLEAN_EXPECTED', cond('a vector', 'len(x) > 0')), 1),
    ('B07', 'B3', 'an integer as an operand of and raises BOOLEAN_EXPECTED', '.haro', [
        B, 'f()', 'func f', T + 'nA = 1', T + '? true and nA'],
     err('B07', 5, 'BOOLEAN_EXPECTED', cond('an integer', 'x != 0')), 1),
    ('B08', 'B4', 'the yes-or-no natives answer a boolean', '.haro', [
        'f()', 'func f', T + '? isstring("a")', T + '? isnumber("a")', T + '? islist([])', T + 'if isnull(null)', T * 2 + '? "none"', T + 'ok'],
     ['true', 'false', 'true', 'none']),
    ('B09', 'B5', 'a boolean in arithmetic raises NO_COERCION', '.haro', [
        B, 'f()', 'func f', T + '? true + 1'],
     err('B09', 4, 'NO_COERCION', coerce('boolean', '+', 'integer', 'a comparison, or string(b)')), 1),
    ('B10', 'B5', 'string() of a boolean is its word', '.haro', [
        'f()', 'func f', T + 'bReady = 2 > 1', T + '? "ready: " + string(bReady)'],
     ['ready: true']),
    ('B11', 'B6', 'a text plus an integer raises NO_COERCION', '.haro', [
        B, 'f()', 'func f', T + 'nLine = 3', T + '? "line " + nLine'],
     err('B11', 5, 'NO_COERCION', coerce('text', '+', 'integer', 'string(x) or number(x)')), 1),
    ('B12', 'B6', 'an integer plus a numeric text raises NO_COERCION', '.haro', [
        B, 'f()', 'func f', T + '? 1 + "2"'],
     err('B12', 4, 'NO_COERCION', coerce('integer', '+', 'text', 'string(x) or number(x)')), 1),
    ('B13', 'B6', 'a numeric text times an integer raises NO_COERCION', '.haro', [
        B, 'f()', 'func f', T + '? "3" * 2'],
     err('B13', 4, 'NO_COERCION', coerce('text', '*', 'integer', 'string(x) or number(x)')), 1),
    ('B14', 'B6', 'an integer equal to a text raises TYPE_MISMATCH', '.haro', [
        B, 'f()', 'func f', T + 'if 1 = "1"', T * 2 + '? "same"', T + 'ok'],
     err('B14', 4, 'TYPE_MISMATCH', mismatch('integer', '=', 'text')), 1),
    ('B15', 'B6', 'an integer ordered against a text raises TYPE_MISMATCH', '.haro', [
        B, 'f()', 'func f', T + '? 2 < "3"'],
     err('B15', 4, 'TYPE_MISMATCH', mismatch('integer', '<', 'text')), 1),
    ('B16', 'B6', 'a boolean equal to an integer raises TYPE_MISMATCH', '.haro', [
        B, 'f()', 'func f', T + '? true = 1'],
     err('B16', 4, 'TYPE_MISMATCH', mismatch('boolean', '=', 'integer')), 1),
    ('B17', 'B6', 'what is one type compares, and an integer meets a number', '.haro', [
        'f()', 'func f', T + '? 2 = 2.0', T + '? "a" < "b"', T + '? true = true', T + '? 3 + 0.5', T + '? "a" + "b"'],
     ['true', 'true', 'true', '3.50', 'ab']),
    ('B18', 'B7', 'an integer stays exact past 2^53', '.haro', [
        'f()', 'func f', T + 'nBig = 9007199254740993', T + '? nBig + 0', T + '? nBig * 2'],
     ['9007199254740993', '18014398509481986']),
    ('B19', 'B7', 'an integer past 64 bits raises INTEGER_OVERFLOW', '.haro', [
        B, 'f()', 'func f', T + 'nMax = 9223372036854775807', T + '? nMax + 1'],
     err('B19', 5, 'INTEGER_OVERFLOW', 'integer + integer leaves 64 bits'), 1),
    ('B20', 'B6', 'a caught coercion answers its code', '.haro', [
        'f()', 'func f', T + 'try', T * 2 + '? "a" + 1', T + 'catch e', T * 2 + '? e.Code()', T + 'done'],
     ['NO_COERCION']),
    ('B21', 'B8', 'a .ring file reads as Ring reads: coercion and truth unchanged', '.ring', [
        'f()', 'func f', T + '? 1 + "2"', T + '? "a" + 1', T + 'if 5 ? "yes" ok', T + '? 1 = 1', T + '? true'],
     ['3', 'a1', 'yes', '1', '1']),
    ('B22', 'B8', 'a boolean read by .ring code is 1 or 0; a .ring 1 is an integer to a .haro condition', '.haro', [
        'load "B22_lib.ring"', 'f()', 'func f', T + '? Plus1(2 > 1)', T + 'if Ready()', T * 2 + '? "ready"', T + 'ok'],
     ['2', '', 'Line 5 Error (BOOLEAN_EXPECTED) : ' + cond('an integer', 'x != 0') + ' ', 'In function f() in file B22.haro', '',
      'Called from line 2 in file B22.haro '], 1, {'B22_lib.ring': ['func Plus1 x', T + 'return x + 1', 'func Ready', T + 'return 1']}),
    # WRITTEN AFTER THE CODE, before the plants, found while writing them: no case reached the left of `or` (a jtruthy the VM judges, B23), nor a
    # comparison whose operand may be an object, which the VM answers through cmpv rather than a jump (B24).
    ('B23', 'B3', 'an integer on the left of or raises BOOLEAN_EXPECTED', '.haro', [
        B, 'f()', 'func f', T + 'nA = 1', T + '? nA or true'],
     err('B23', 5, 'BOOLEAN_EXPECTED', cond('an integer', 'x != 0')), 1),
    # B24 CHANGED AFTER THE PLANTS: plant P28 missed, because a call's answer is compared by a jump and not by cmpv; a global's value may be
    # an object, so it is the operand that sends a comparison to cmpv (read off `haro dis`). The case asks the same question of that path.
    ('B24', 'B6', 'a comparison whose operand may be an object (cmpv) is judged as every comparison is', '.haro', [
        B, 'f()', 'func f', T + '$nTwo = 2', T + '? $nTwo = 2', T + '? $nTwo = "2"'],
     ['before', 'true', '', 'Line 6 Error (TYPE_MISMATCH) : ' + mismatch('integer', '=', 'text') + ' ', 'In function f() in file B24.haro', '',
      'Called from line 2 in file B24.haro '], 1),
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
doc = {'rung': 'v0.43', 'decision': 'D55 T1 and T3: a real boolean, and no coercion, in a .haro file; a .ring file reads as Ring reads',
       'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
       'lines': {'B1': 'true and false are the booleans', 'B2': 'a comparison and the logic answer a boolean',
                 'B3': 'a condition takes a boolean', 'B4': 'the yes-or-no natives answer a boolean', 'B5': 'a boolean is no number',
                 'B6': 'no coercion; = and the orderings between two types refused', 'B7': 'an integer stays exact to 64 bits, then raises',
                 'B8': 'a .ring file reads as Ring reads; a boolean is 1 or 0 to it'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
