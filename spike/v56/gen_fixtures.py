"""Haro v0.56 -- every definition ends with `end`, in any order; `func` a function, `def` a method (HARO-DEFINITIONS-01). Written FIRST,
before the compiler is touched.

THE RULING. The Principal, 2026-11-11, in this desk's chat, after v0.55: "the ring's style of positioning classes at the end etc, shloud not
be adopted by haro. it was one of the things that let agents suffer most (including you) and waste token to remind them tat each time!
aloso, i would like to keep func for functions and def for methods so they are clearley separate" -- and "i let you decide" for the rest.
His own: no position rule; func for functions, def for methods. The desk's reading (D68), on his delegation: a definition is a block like
every other and ends with `end`, so the tree says where each one stops, and what stands at the top level is the program's whatever its
place. This replaces v0.55's F2 ("a definition has no end word") and its `func` for methods (D67 F3).

THE LINES:
  G1  every definition -- func, def, class, package -- ends with `end`; one without is refused, naming it; endfunc, endfunction, endclass
      and endpackage are refused, naming `end`
  G2  `func` defines a function and `def` a method: `func` inside a class and `def` outside one are refused, each naming the other
  G3  any order: a class, a function and the program's statements stand where the writer puts them; a statement at the top level is the
      program's, run in the order written, before or after any definition; a function after a class is a function
  G4  a .ring file reads as Ring reads it: a func after a class is its method, a statement after a func belongs to it

  python spike/v56/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


NONE = 'a definition ends with `end`, and this one has none; written'

CASES = [
    # G3 -- any order
    ('E01', 'G3', 'a class, then a function, then the program: each where it is written', [
        'class P', T + 'nX = 1', T + 'def Show', T + T + '? nX', T + 'end', 'end',
        'func g', T + '? "g"', 'end',
        'oP = new P', 'oP.Show()', 'g()', '? "last"'],
     '1\ng\nlast\n', 0),
    ('E02', 'G3', 'a function after a class is a function, and a method may call it', [
        'oP = new P', 'oP.Run()',
        'class P', T + 'def Run', T + T + '? Twice(2)', T + 'end', 'end',
        'func Twice(iN)', T + 'return iN * 2', 'end'],
     '4\n', 0),
    ('E03', 'G3', 'statements between definitions run in the order written', [
        '? 1', 'func a', T + '? "a"', 'end', '? 2', 'class P', 'end', '? 3', 'a()'],
     '1\n2\n3\na\n', 0),
    ('E04', 'G3', 'blocks inside definitions close before them: if, for, within, then the function', [
        '$iG = 1', 'f()', '? $iG', 'func f', T + 'for iI = 1 to 2', T + T + 'if iI = 2', T + T + T + 'within $iG = 5', T + T + T + T + '? $iG',
        T + T + T + 'end', T + T + 'end', T + 'end', 'end', '? "after"'],
     '5\n1\nafter\n', 0),
    ('E05', 'G3', 'a class with a private section ends with end, and what follows is the program\'s', [
        'oP = new P', 'oP.Show()', 'class P', T + 'def Show', T + T + '? Secret()', T + 'end', T + 'private', T + 'def Secret',
        T + T + 'return "s"', T + 'end', 'end', '? "top"'],
     's\ntop\n', 0),
    # G1 -- every definition ends with end
    ('E06', 'G1', 'a function without its end is refused, naming it', ['? "before"', 'f()', 'func f', T + '? 1'],
     refused('E06', 3, NONE, 'f'), 1),
    ('E07', 'G1', 'a class without its end is refused where its method is entered', [
        '? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'def f', T + T + '? 1', T + 'end'],
     refused('E07', 4, NONE, 'P', called=3, where='method f()'), 1),
    ('E08', 'G1', 'endfunc is refused: end', ['? "before"', 'f()', 'func f', T + '? 1', 'endfunc'],
     refused('E08', 5, 'one spelling: `end`; written', 'endfunc'), 1),
    ('E09', 'G1', 'endclass is refused: end', ['? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'def f', T + T + '? 1', T + 'end',
                                               'endclass'],
     refused('E09', 8, 'one spelling: `end`; written', 'endclass', called=3, where='method f()'), 1),
    # G2 -- func a function, def a method
    ('E10', 'G2', 'func inside a class is refused: a method is def', [
        '? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'func f', T + T + '? 1', T + 'end', 'end'],
     refused('E10', 5, 'a method is defined with `def`; written', 'func', called=3, where='method f()'), 1),
    ('E11', 'G2', 'def outside a class is refused: a function is func', ['? "before"', 'f()', 'def f', T + '? 1', 'end'],
     refused('E11', 3, 'a function is defined with `func`; written', 'def'), 1),
    # G4 -- a .ring file reads as Ring reads it
    ('E12', 'G4', 'a .ring file: a func after a class is its method, a statement after a func belongs to it', [
        'o = new P', 'o.g()', 'f()', 'func f', '? "f"', '? "still f"', 'class P', 'func g', '? "g, a method"'],
     'g, a method\nf\nstill f\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'E12' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.56',
        'decision': 'HARO-DEFINITIONS-01: the Principal, 2026-11-11 (no position rule; func for functions, def for methods); the desk\'s '
                    'reading, a definition ends with end, is D68 on his delegation',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'G1': 'every definition ends with end', 'G2': 'func a function, def a method', 'G3': 'any order',
                  'G4': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
