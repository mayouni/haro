"""Haro v0.55 -- one form for each construct (HARO-ONEFORM-01). Written FIRST, before the compiler is touched.

THE ASK. The Principal, 2026-11-11, in this desk's chat: "Ring uses different keywords to end a block (ok, end, }, off, done...). I want
Hero to end this chao and do not enherit it. Opt for a strict one form. Try to identify any simular issue and solve it." The choice of
each form is delegated ("Opt for a strict one form"); the desk's choices are D67, each the word that says what the construct does, and
among equals the one Haro's own code already writes. A .ring file reads every spelling as it always has.

THE TABLE (D67):
  F1  a block ends with `end` -- if, while, for, switch, try, within, using; never ok, next, off, done, endif, endwhile, endfor,
      endswitch, endtry, and never braces
  F2  a definition -- func, class, package -- has no end word: it ends where the next definition begins; never end, endfunc,
      endfunction, endclass, endpackage, and never braces
  F3  one word each: func (never def, function), elseif (never but), else (never other, in a switch too), case (never on), for (never
      foreach), see (never put), give (never get), exit (never break), loop (never continue), and, or, not (never &&, ||, !), from (never
      `:` or `<` before a class's parent), `#` for a line's comment (never //), this for the method's object (self only inside a brace,
      where it is the brace's object)
  F4  a definition's parameters stand in parentheses -- `func Add(iA, iB)` -- and a definition without parameters has none -- `func Main`
  F5  a statement has no trailing period
  F6  kept, each a different construct: `?` (prints a line) beside `see` (prints, ending no line); the three quote marks (each lets the
      other two stand inside); /* */ (a comment across lines); self inside a brace; a .ring file untouched

  python spike/v55/gen_fixtures.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'port'))
import haroport as H

# written with their definitions' ends by hand: v0.56 changed what they judge (O09-O12), or where a line stands (O22)
HAND = {'O09', 'O10', 'O11', 'O12', 'O22'}


def top(cid, line, why, text):
    """v0.56: a definition's end word is read from the tokens before the parse, so an end word in another spelling refuses the program"""
    return (f'\nLine {line} Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
            f'past it would give a wrong answer \nin file {cid}.haro ')


T = '\t'


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


END = 'a block ends with `end`; written'
DEF = 'a definition has no end word -- it ends where the next begins; written'
BRACE = 'a block has no braces -- it ends with `end`; written'


def one(w):
    return f'one spelling: `{w}`; written'


HEAD = ['? "before"', 'f()', 'func f']

CASES = [
    # F1 -- a block ends with end
    ('O01', 'F1', 'an if closed by ok is refused', HEAD + [T + 'if true', T + T + '? 1', T + 'ok'],
     refused('O01', 6, END, 'ok'), 1),
    ('O02', 'F1', 'a for closed by next is refused', HEAD + [T + 'for iI = 1 to 2', T + T + '? iI', T + 'next'],
     refused('O02', 6, END, 'next'), 1),
    ('O03', 'F1', 'a switch closed by off is refused', HEAD + [T + 'switch 1', T + 'case 1', T + T + '? 1', T + 'off'],
     refused('O03', 7, END, 'off'), 1),
    ('O04', 'F1', 'a try closed by done is refused', HEAD + [T + 'try', T + T + '? 1', T + 'catch', T + T + '? 2', T + 'done'],
     refused('O04', 8, END, 'done'), 1),
    ('O05', 'F1', 'a while closed by endwhile is refused', HEAD + [T + 'iI = 0', T + 'while iI < 1', T + T + 'iI++', T + 'endwhile'],
     refused('O05', 7, END, 'endwhile'), 1),
    ('O06', 'F1', 'a block in braces is refused', HEAD + [T + 'if true {', T + T + '? 1', T + '}'],
     refused('O06', 4, BRACE, '{'), 1),
    ('O07', 'F1', 'within closes with end, and its global is restored', ['$iG = 1', 'f()', '? $iG', 'func f', T + 'within $iG = 2',
                                                                         T + T + '? $iG', T + 'end'],
     '2\n1\n', 0),
    ('O30', 'F1', 'an if inside a within: each end closes its own block', ['$iG = 1', 'f()', '? $iG', 'func f', T + 'within $iG = 2',
                                                                          T + T + 'if true', T + T + T + '? $iG', T + T + 'end',
                                                                          T + T + '? 3', T + 'end'],
     '2\n3\n1\n', 0),
    ('O08', 'F1', 'within closed by done is refused', HEAD + [T + '$iG = 1', T + 'within $iG = 2', T + T + '? $iG', T + 'done'],
     refused('O08', 7, END, 'done'), 1),
    # F2 -- a definition has no end word
    # O09-O12 changed by v0.56 (D68, the Principal 2026-11-11): a definition ends with `end`, `func` a function and `def` a method
    ('O09', 'F2', 'a function closed by end runs (v0.56: a definition ends with end)', HEAD + [T + '? 1', 'end'],
     'before\n1\n', 0),
    ('O10', 'F2', 'a function closed by endfunc is refused: end', HEAD + [T + '? 1', 'endfunc'],
     top('O10', 5, one('end'), 'endfunc'), 1),
    ('O11', 'F2', 'a class closed by endclass is refused where its method is entered: end', ['? "before"', 'oP = new P', 'oP.f()', 'class P',
                                                                                             T + 'def f', T + T + '? 1', T + 'end', 'endclass'],
     top('O11', 8, one('end'), 'endclass'), 1),
    # F3 -- one word each
    ('O12', 'F3', 'def outside a class is refused: a function is func (v0.56)', ['? "before"', 'f()', 'def f', T + '? 1', 'end'],
     refused('O12', 3, 'a function is defined with `func`; written', 'def'), 1),
    ('O13', 'F3', 'but is refused: elseif', HEAD + [T + 'if false', T + T + '? 1', T + 'but true', T + T + '? 2', T + 'end'],
     refused('O13', 6, one('elseif'), 'but'), 1),
    ('O14', 'F3', 'other is refused in a switch: else', HEAD + [T + 'switch 2', T + 'case 1', T + T + '? 1', T + 'other', T + T + '? 2',
                                                                T + 'end'],
     refused('O14', 7, one('else'), 'other'), 1),
    ('O15', 'F3', 'on is refused: case', HEAD + [T + 'switch 1', T + 'on 1', T + T + '? 1', T + 'end'],
     refused('O15', 5, one('case'), 'on'), 1),
    ('O16', 'F3', 'foreach is refused: for', HEAD + [T + 'foreach iI in [1]', T + T + '? iI', T + 'end'],
     refused('O16', 4, one('for'), 'foreach'), 1),
    ('O17', 'F3', 'put is refused: see', HEAD + [T + 'put "a"'],
     refused('O17', 4, one('see'), 'put'), 1),
    ('O18', 'F3', 'break is refused: exit', HEAD + [T + 'for iI = 1 to 2', T + T + 'break', T + 'end'],
     refused('O18', 5, one('exit'), 'break'), 1),
    ('O19', 'F3', 'continue is refused: loop', HEAD + [T + 'for iI = 1 to 2', T + T + 'continue', T + 'end'],
     refused('O19', 5, one('loop'), 'continue'), 1),
    ('O20', 'F3', '&& is refused: and', HEAD + [T + 'if true && true', T + T + '? 1', T + 'end'],
     refused('O20', 4, one('and'), '&&'), 1),
    ('O21', 'F3', '! is refused: not', HEAD + [T + 'if !false', T + T + '? 1', T + 'end'],
     refused('O21', 4, one('not'), '!'), 1),
    ('O22', 'F3', 'a parent after : is refused: from', ['? "before"', 'oP = new Q', 'oP.f()', 'class Q : P', T + 'def f', T + T + '? 1',
                                                        T + 'end', 'end', 'class P', 'end'],
     refused('O22', 4, one('from'), ':', called=3, where='method f()'), 1),
    ('O23', 'F3', 'a comment after // is refused: #', HEAD + [T + '? 1 // one'],
     refused('O23', 4, one('#'), '// one'), 1),
    ('O24', 'F3', 'self outside a brace is refused: this', ['? "before"', 'oP = new P', 'oP.f()', 'class P', T + 'func f',
                                                            T + T + '? ClassName(self)'],
     refused('O24', 6, one('this'), 'self', called=3, where='method f()'), 1),
    # F4 -- parameters in parentheses, none without
    ('O25', 'F4', 'a definition without parameters written with () is refused', ['? "before"', 'f()', 'func f()', T + '? 1'],
     refused('O25', 3, 'a definition without parameters has no parentheses; written', '()'), 1),
    ('O26', 'F4', 'parameters written without parentheses are refused', ['? "before"', 'f(1, 2)', 'func f iA, iB', T + '? iA + iB'],
     refused('O26', 3, 'a definition\'s parameters stand in parentheses; written', 'iA, iB'), 1),
    # F5 -- no trailing period
    ('O27', 'F5', 'a call statement with a trailing period is refused', HEAD + [T + 'g().', 'func g', T + '? 1'],
     refused('O27', 4, 'a statement has no trailing period; written', '.'), 1),
    # F6 -- what stays, and the one forms together
    ('O28', 'F6', 'the one forms run: end, elseif, else, case, for, see, ?, give-free, exit, loop, and/or/not, from, #, this, self in a brace',
     ['f(3)', 'oQ = new Q', 'oQ.g()', '/* a comment', 'across lines */',
      'func f(iN)', T + 'for iI = 1 to iN', T + T + 'if iI = 1', T + T + T + 'loop', T + T + 'elseif iI = 3 and not false',
      T + T + T + 'exit', T + T + 'else', T + T + T + 'see "i"', T + T + T + '? iI', T + T + 'end', T + 'end',
      T + 'switch iN', T + 'case 1', T + T + '? "one"', T + 'else', T + T + '? \'other "n"\'', T + 'end', T + 'try', T + T + 'Raise("x")',
      T + 'catch', T + T + '? "caught"', T + 'end',
      'class P', T + 'nX = 1', 'class Q from P', T + 'func g', T + T + 'oP = new P {', T + T + T + 'nX = 5', T + T + T + '? ClassName(self)', T + T + '}',
      T + T + '? ClassName(this)  # this is the method\'s object', T + T + '? oP.nX'],
     'i2\nother "n"\ncaught\np\nq\n5\n', 0),
    ('O29', 'F6', 'a .ring file reads every spelling as it did', [
        'f(2)', 'func f n', T + 'for i = 1 to n', T + T + 'if i = 1 put "a" but i = 2 see "b" ok', T + 'next', T + 'switch n on 2 put "c" other put "d" off',
        T + 'try raise("e") catch put "f" done', T + 'if 1 && !0 { put "g" }', T + 'put nl', 'end'],
     'abcfg\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'O29' else '.haro'
        name = f'cases/{cid}{ext}'
        text = '\n'.join(src) + '\n'
        if ext == '.haro' and cid not in HAND:
            # v0.56 (D68): every definition ends with `end`, a method is `def` -- added by haroport's rule, each end after its definition's
            # last line, so the lines a case names keep their numbers
            text = ''.join(v for _, v in H.def_ends(H.tokens(text), []))
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.55',
        'decision': 'HARO-ONEFORM-01: the Principal, 2026-11-11, "Opt for a strict one form"; the table is D67, the desk\'s on his delegation',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'F1': 'a block ends with end', 'F2': 'a definition has no end word', 'F3': 'one word each',
                  'F4': 'parameters in parentheses, none without', 'F5': 'no trailing period', 'F6': 'what stays, and a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
