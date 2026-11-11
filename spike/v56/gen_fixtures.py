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


def top(cid, line, why, text):
    """refused at the program's first statement: nothing runs"""
    return (f'\nLine {line} Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
            f'past it would give a wrong answer \nin file {cid}.haro ')

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
        'func Twice(iN)', T + 'return iN * 2', 'end', '? Twice(3)'],
     '4\n6\n', 0),
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
    # E06 and E07 changed after the code, on Radar's finding (2026-11-11 12:22): without its end a definition's body falls to the top
    # level, where it ran before the definition's refusal was reached -- so the program refuses its first statement, naming it
    ('E06', 'G1', 'a function without its end: the program is refused before it runs, naming it', ['? "before"', 'f()', 'func f', T + '? 1'],
     top('E06', 3, NONE, 'f'), 1),
    ('E07', 'G1', 'a class without its end: the program is refused before it runs, naming it', [
        '? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'def f', T + T + '? 1', T + 'end'],
     top('E07', 4, NONE, 'P'), 1),
    # E08 and E09 changed after the code: a definition's structure is read from its tokens before the parse (lift.zig, defBraces), so
    # an end word in another spelling refuses the program, as a missing end does
    ('E08', 'G1', 'endfunc refuses the program: end', ['? "before"', 'f()', 'func f', T + '? 1', 'endfunc'],
     top('E08', 5, 'one spelling: `end`; written', 'endfunc'), 1),
    ('E09', 'G1', 'endclass refuses the program: end', ['? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'def f', T + T + '? 1',
                                                        T + 'end', 'endclass'],
     top('E09', 8, 'one spelling: `end`; written', 'endclass'), 1),
    # G2 -- func a function, def a method
    ('E10', 'G2', 'func inside a class is refused: a method is def', [
        '? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'func f', T + T + '? 1', T + 'end', 'end'],
     refused('E10', 5, 'a method is defined with `def`; written', 'func', called=3, where='method f()'), 1),
    ('E11', 'G2', 'def outside a class is refused: a function is func', ['? "before"', 'f()', 'def f', T + '? 1', 'end'],
     refused('E11', 3, 'a function is defined with `func`; written', 'def'), 1),
    # G5 -- a chain across lines: its dot starts the next line (HARO-PORTTOOL-CHAINDOT-01, stzlib-haroport 2026-11-11 09:54; the form is
    # the desk's, on the Principal's "i let you decide") -- added before its code
    ('E13', 'G5', 'a chain across lines continues with its dot at the start of the next line', [
        'oP = new P', 'oP.AQ(1)', T + '.SQ(3)', '? "end"', 'class P', T + 'def AQ(xX)', T + T + 'return this', T + 'end', T + 'def SQ(iN)',
        T + T + '? iN', T + 'end', 'end'],
     '3\nend\n', 0),
    ('E14', 'G5', 'a dot that ends a line is refused: the dot starts the next line', [
        '? "before"', 'f()', 'func f', T + 'oP = new P', T + 'oP.AQ(1).', T + T + 'SQ(3)', 'end', 'class P', T + 'def AQ(xX)',
        T + T + 'return this', T + 'end', T + 'def SQ(iN)', T + T + '? iN', T + 'end', 'end'],
     refused('E14', 5, 'a chain across lines continues with its dot at the start of the next line; written', '.'), 1),
    # E15-E19 written after the code, said so: the definitions' structure is read from the tokens before the parse (lift.zig, defBraces)
    ('E15', 'G1', 'a method whose last line holds a + keeps its end, and the class its own', [
        'oRes = new Res', 'oRes.Show(1)', '? "after"', 'class Res', T + 'tName = "x"', T + 'def a', T + T + '? 2', T + 'end', T + 'def Show(iX)',
        T + T + '? "r" + tName', T + 'end', 'end'],
     'rx\nafter\n', 0),
    ('E16', 'G1', 'an end that closes nothing refuses the program', ['? "before"', 'f()', 'func f', T + '? 1', 'end', 'end'],
     top('E16', 6, 'an `end` closes nothing here; written', 'end'), 1),
    ('E17', 'G1', 'a definition\'s body on its header\'s line refuses the program', ['? "before"', '? f()', 'func f() return 1 end'],
     top('E17', 3, 'a definition\'s body starts on the line after its header; written', 'f'), 1),
    ('E18', 'G1', 'a block closed by ok inside a definition is refused at its statement, naming end', [
        '? "before"', 'f()', 'func f', T + 'if true', T + T + '? 1', T + 'ok', 'end'],
     refused('E18', 6, 'a block ends with `end`; written', 'ok'), 1),
    ('E19', 'G1', 'a block in braces inside a definition is refused at its statement', [
        '? "before"', 'f()', 'func f', T + 'if true {', T + T + '? 1', T + '}', 'end'],
     refused('E19', 4, 'a block has no braces -- it ends with `end`; written', '{'), 1),
    ('E20', 'G1', 'an eval\'s text: a within closed by end restores its global', [
        '$tG = "a"', 'f()', '? $tG', 'func f', T + 'Eval("within $tG = " + Char(34) + "b" + Char(34) + nl + "? $tG" + nl + "end")', 'end'],
     'b\na\n', 0),
    # E21 written after the code, said so: stzlib's stzSoundTransport passes a function written in place, `func { ... }`, which the
    # first scan read as a definition waiting for its end
    ('E21', 'G1', 'a function written in place, func { ... }, is closed by its brace', [
        'f()', 'func f', T + 'xG = func { return 7 }', T + 'print call xG()', 'end'],
     '7\n', 0),
    ('E22', 'G1', 'a function written in place with parameters, inside a call, is closed by its brace', [
        'f()', 'func f', T + 'xG = Twice(func(iX) { return iX * 2 })', T + 'print xG', 'end', 'func Twice(xF)', T + 'return call xF(4)', 'end'],
     '8\n', 0),
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
                  'G4': 'a .ring file untouched', 'G5': 'a chain across lines: its dot starts the next line'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
