"""Haro v0.57 -- one way to print: `print`, and `?` its shortcut (HARO-PRINT-01). Written FIRST, before the compiler is touched.

THE RULING. The Principal, 2026-11-11, in this desk's chat: "I don't want Haro to enherit the Ring pathology of having serveral laternative
to the same fauture like 'see', 'print' and '?'. Although, one could accept a unique keyword (print for example) along with a useful
shortuct like '?'." His own: one keyword, `print`, and the shortcut `?`. The desk's reading (D69), on his "i let you decide": `print` and `?`
are the same statement -- the value written, then the end of the line, as `?` always did; `see` and `put` are refused in a .haro file,
naming `print`; output that ends no line goes through the stream, `FWrite(stdout, tText)` (v0.50). In a .ring file `print` stays Ring's
function: the lift writes a bare `print` word as `Print` before the parse, which Ring reads alike.

THE LINES:
  P1  `print v` writes v and ends the line; `?` is its shortcut, the same statement
  P2  `see` and `put` are refused, naming `print`
  P3  output that ends no line: FWrite(stdout, ...)
  P4  a .ring file reads `see`, `put`, `?` and its `print(...)` calls as Ring reads them

  python spike/v57/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def trap(cid, line, msg, called=2, where='function f()'):
    return f'before\n\nLine {line} {msg} \nIn {where} in file {cid}.haro\n\nCalled from line {called} in file {cid}.haro '


def refused(cid, line, why, text, called=2, where='function f()'):
    return trap(cid, line, f'Haro refused this statement ({why} `{text}`, line {line} of {cid}.haro) and did not compile it -- running '
                           f'past it would give a wrong answer', called, where)


PRINT = 'one spelling: `print`; written'

CASES = [
    ('R01', 'P1', 'print writes a value and ends the line', ['print "a"', 'print 2 + 3', 'print [1, 2]'], 'a\n5\n1\n2\n\n', 0),
    ('R02', 'P1', '? is print\'s shortcut: the same bytes (a list: its items, then an empty line, as `?` writes it)',
     ['? "a"', '? 2 + 3', '? [1, 2]'], 'a\n5\n1\n2\n\n', 0),
    ('R03', 'P1', 'print in a one-line if, in a function, in a method', [
        'f()', 'oP = new P', 'oP.g()', 'func f', T + 'if true print "f" end', 'end', 'class P', T + 'def g', T + T + 'print "g"', T + 'end',
        'end'],
     'f\ng\n', 0),
    ('R04', 'P2', 'see is refused: print', ['? "before"', 'f()', 'func f', T + 'see "a"', 'end'], refused('R04', 4, PRINT, 'see'), 1),
    ('R05', 'P2', 'put is refused: print', ['? "before"', 'f()', 'func f', T + 'put "a"', 'end'], refused('R05', 4, PRINT, 'put'), 1),
    ('R06', 'P3', 'output that ends no line goes through the stream', ['FWrite(stdout, "a")', 'FWrite(stdout, "b")', 'print "c"'],
     'abc\n', 0),
    # R08 written after the code, said so: stzlib's stzObject has a method named print, which the first build rewrote as `?`
    ('R08', 'P1', 'a method named print is a method; the statement print beside it prints', [
        'oP = new P', 'oP.print()', 'print "b"', 'class P', T + 'def print', T + T + 'print "a"', T + 'end', 'end'],
     'a\nb\n', 0),
    ('R07', 'P4', 'a .ring file: see, put, ? as Ring reads them, and print(...) is the function it calls', [
        'see "a"', 'put "b"', '? "c"', 'print("d")', 'func print t', '  see "[" + t + "]" + nl'],
     'abc\n[d]\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, src, stdout, code in CASES:
        ext = '.ring' if cid == 'R07' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.57',
        'decision': 'HARO-PRINT-01: the Principal, 2026-11-11 (one keyword, print, and the shortcut ?); the desk\'s reading is D69',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {'P1': 'print, and ? its shortcut', 'P2': 'see and put refused', 'P3': 'output that ends no line',
                  'P4': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
