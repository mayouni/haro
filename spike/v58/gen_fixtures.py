"""Haro v0.58 -- absence: `none`, `maybe`, resolved where it lands (D55 T5, HARO-ABSENCE-01). Written FIRST, before the compiler is touched.

THE RULING. TYPES.md T5, ruled in D55 (2026-11-07): "`none` belongs to no type. A function that may find nothing returns `maybe T`, and its
caller resolves it where it lands ... A `maybe` never travels in a local ... Only a return and an attribute may be declared `maybe`. Ring's
NULL, which was the empty string, is gone". The spelling, the Principal's in this desk's chat, 2026-11-11: `maybe` a trailing word --
`func Find kId maybe` (with v0.56's parentheses, `func Find(kId) maybe`), `oParent = none maybe` -- and the resolution `x = E else D`.

THE DESK'S READINGS (D70):
  - `none` stands only where a maybe is declared: `return none` in a maybe function, and a maybe attribute given it
  - a maybe -- a call of a maybe function or method, a read of a maybe attribute -- stands where it lands: the left of `E else D`, the
    value a maybe function returns, or a statement of its own; anywhere else it is refused, naming it
  - `E else D` is D when E is none; D may raise. Written after `=`, `return` or `print`; an `else` that begins its line, or that follows an
    if opened on its line, is the if's
  - a maybe function that ends without a return returns none; a non-maybe value is never none, so `else` after one is refused

THE LINES:
  A1  a maybe function's value, resolved where it lands
  A2  none only where a maybe is declared
  A3  a maybe resolved, or refused where it stands unresolved
  A4  a maybe attribute
  A5  else is a resolution only where a maybe lands; an if's else is the if's; "" is a text
  A6  a .ring file untouched

  python spike/v58/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


R_NONE = '`none` stands only where a maybe is declared; written'
R_MAYBE = 'a maybe is resolved where it lands -- x = E else D; written'
R_ELSE = 'else resolves a maybe, and this value is never none; written'

TITLE = ['func Title(bHas) maybe', T + 'if bHas', T + T + 'return "Haro"', T + 'end', T + 'return none', 'end']
HEAD = ['print "before"', 'f()', 'func f']

CASES = [
    ('M01', 'A1', 'a maybe function\'s value, or else its default', [
        'f()', 'func f', T + 'tT = Title(true) else "untitled"', T + 'print tT', T + 'tT = Title(false) else "untitled"', T + 'print tT',
        'end'] + TITLE,
     'Haro\nuntitled\n', 0),
    ('M02', 'A1', 'a maybe function that ends without a return gives none', [
        'f()', 'func f', T + 'tT = Find(2) else "nothing"', T + 'print tT', 'end', 'func Find(iK) maybe', T + 'if iK = 1', T + T + 'return "one"',
        T + 'end', 'end'],
     'nothing\n', 0),
    ('M03', 'A1', 'else raises when it has nothing to give', HEAD + [T + 'oU = Find(9) else Raise("no user 9")', T + 'print "never"', 'end',
                                                                     'func Find(iK) maybe', T + 'return none', 'end'],
     'before\n\nLine 4 no user 9 \nIn raise() In function f() in file M03.haro\n\nCalled from line 2 in file M03.haro ', 1),
    ('M04', 'A3', 'a maybe given to a local unresolved is refused', HEAD + [T + 'tT = Title(true)', T + 'print tT', 'end'] + TITLE,
     refused('M04', 4, R_MAYBE, 'Title'), 1),
    ('M05', 'A3', 'a maybe passed as an argument is refused', HEAD + [T + 'print Len(Title(true))', 'end'] + TITLE,
     refused('M05', 4, R_MAYBE, 'Title'), 1),
    ('M06', 'A2', 'none returned by a function not declared maybe is refused', HEAD + [T + 'print g()', 'end', 'func g', T + 'return none', 'end'],
     refused('M06', 8, R_NONE, 'none', called=4, where='function g()'), 1),
    ('M07', 'A2', 'none given to a local is refused', HEAD + [T + 'xV = none', 'end'],
     refused('M07', 4, R_NONE, 'none'), 1),
    ('M08', 'A4', 'a maybe attribute starts as none and is resolved where it is read', [
        'oA = new Node("a")', 'oB = new Node("b")', 'oB.SetParent(oA)', 'print oB.ParentName()', 'print oA.ParentName()',
        'class Node', T + 'oParent = none maybe', T + 'tName = ""', T + 'def init(tN)', T + T + 'tName = tN', T + 'end',
        T + 'def SetParent(oP)', T + T + 'oParent = oP', T + 'end', T + 'def ParentName', T + T + 'oP = oParent else new Node("-")',
        T + T + 'return oP.tName', T + 'end', 'end'],
     'a\n-\n', 0),
    ('M09', 'A4', 'a maybe attribute read unresolved is refused', [
        'print "before"', 'oA = new Node', 'oA.Bad()', 'class Node', T + 'oParent = none maybe', T + 'def Bad', T + T + 'oP = oParent',
        T + 'end', 'end'],
     refused('M09', 7, R_MAYBE, 'oParent', called=3, where='method bad()'), 1),
    ('M10', 'A5', 'else after a value that is never none is refused', HEAD + [T + 'tT = "a" else "b"', 'end'],
     refused('M10', 4, R_ELSE, '"a"'), 1),
    ('M11', 'A5', 'an else that follows an if opened on its line is the if\'s', [
        'f()', 'func f', T + 'if false tT = "x" else tT = "y" end', T + 'print tT', 'end'],
     'y\n', 0),
    ('M12', 'A5', '"" is a text of length 0, and no absence', ['tE = ""', 'print Len(tE)', 'print IsString(tE)'],
     '0\ntrue\n', 0),
    ('M13', 'A1', 'return E else D in a function not declared maybe', [
        'print Name()', 'func Name', T + 'return Title(false) else "anon"', 'end'] + TITLE,
     'anon\n', 0),
    ('M14', 'A1', 'a maybe function returns another maybe as it is', [
        'tT = Outer(true) else "x"', 'print tT', 'tT = Outer(false) else "x"', 'print tT', 'func Outer(bHas) maybe', T + 'return Title(bHas)',
        'end'] + TITLE,
     'Haro\nx\n', 0),
    ('M15', 'A1', 'print E else D', ['print Title(false) else "no title"'] + TITLE,
     'no title\n', 0),
    ('M16', 'A6', 'a .ring file: none and maybe are names', ['none = 5', 'maybe = 2', '? none + maybe'],
     '7\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'M16' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.58',
        'decision': 'HARO-ABSENCE-01: TYPES.md T5 (D55) with the Principal\'s spelling of 2026-11-11 (maybe a trailing word, x = E else D); '
                    'the desk\'s readings are D70',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'A1': 'a maybe resolved where it lands', 'A2': 'none only where a maybe is declared', 'A3': 'an unresolved maybe refused',
                  'A4': 'a maybe attribute', 'A5': 'else only for a maybe; an if\'s else; "" a text', 'A6': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
