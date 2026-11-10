"""Haro v0.53 -- the classic Ring surface's 1 and 0 cross into a .haro file as false and true (TYPES.md section 6). Written FIRST, before the
VM is touched.

THE ASK. HARO-RINGBOUNDARY-BOOL-01, from stzlib-haroport (2026-11-10 04:12): in a .haro file, `bFlag = OldFlag()` where a .ring function
returns 1 is TYPE_LETTER, and `if OldFlag()` is BOOLEAN_EXPECTED -- so no .haro code can call Softanza's .ring predicates while the library
moves, bottom up, to .haro. Repro: old.ring = `func OldFlag() return 1`; new.haro loads it and binds or tests the answer.

THE RULING. TYPES.md section 6 (D55, ruled 2026-11-07): "A value crossing from .ring code into a .haro name is checked at that binding: an
integer 0 or 1 entering a b name becomes false or true, and any other integer is refused." A condition is not written there.

THE DESK'S READING (D65), judged below: the compiler converts where a boolean is required -- a b name given the value with `=`, a
condition (if, elseif, while), an operand of not, and, or -- when the value is the answer of a call it cannot prove is Haro's: a function
declared in a .ring file, a method dispatched by name. 1 becomes true and 0 false; any other value is left as it is, so the check that
stood refuses it in its own words. A call the compiler proves is Haro's -- a function of a .haro file, a built-in, a method of the .haro
class through This -- stays strict. Nothing is marked when Ring code returns, so the call path pays nothing.

THE LINES:
  R1  a .ring answer 1 or 0 given to a b name is true or false
  R2  ... in a condition (if, elseif, while) and as an operand of not, and, or
  R3  ... from a method dispatched by name
  R4  any other answer is refused by the check that stood: TYPE_LETTER at a b name, BOOLEAN_EXPECTED in a condition
  R5  a call the compiler proves is Haro's stays strict; a value no longer a call's answer is not converted; arithmetic sees the integer
  R6  a .ring file reads as it did

  python spike/v53/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
OLD = ['func OldFlag', T + 'return 1', 'func OldNo', T + 'return 0', 'func OldSeven', T + 'return 7', 'func OldText', T + 'return "yes"',
       'class OldK', T + 'func IsOn', T + T + 'return 1', T + 'func IsOff', T + T + 'return 0']
L = 'load "old.ring"'


def err(line, code, msg, f):
    return f'\nLine {line} Error ({code}) : {msg} \nin file {f} '


CASES = [
    ('V01', 'R1', 'a .ring 1 and 0 given to b names are true and false', '.haro',
     [L, 'bFlag = OldFlag()', 'bNo = OldNo()', '? bFlag', '? bNo', '? Type(bFlag)'],
     'true\nfalse\nBOOLEAN\n', 0),
    ('V02', 'R2', 'a .ring 1 and 0 as conditions: if, elseif', '.haro',
     [L, 'if OldFlag()', T + '? "if"', 'ok', 'if OldNo()', T + '? "no"', 'elseif OldFlag()', T + '? "elseif"', 'ok'],
     'if\nelseif\n', 0),
    ('V03', 'R2', 'a .ring 1 and 0 as operands of not, and, or', '.haro',
     [L, '? not OldNo()', '? OldFlag() and OldNo()', '? OldNo() or OldFlag()', 'bBoth = OldFlag() and OldFlag()', '? bBoth'],
     'true\nfalse\ntrue\ntrue\n', 0),
    ('V04', 'R2', 'a .ring answer as a while condition', '.haro',
     [L, 'iN = 0', 'while OldNo()', T + 'iN = iN + 1', 'end', '? iN'],
     '0\n', 0),
    ('V05', 'R3', 'a method dispatched by name answers 1 and 0 as true and false', '.haro',
     [L, 'oK = new OldK', 'if oK.IsOn()', T + '? "on"', 'ok', 'bOff = oK.IsOff()', '? bOff', '? not oK.IsOff()'],
     'on\nfalse\ntrue\n', 0),
    ('V06', 'R4', 'any other integer at a b name is refused, as before', '.haro',
     [L, '? "before"', 'bX = OldSeven()'],
     'before\n' + err(3, 'TYPE_LETTER', '`bX` is lettered b, a boolean, and is given an integer', 'V06.haro'), 1),
    ('V07', 'R4', 'any other integer in a condition is refused, as before', '.haro',
     [L, '? "before"', 'if OldSeven()', T + '? "seven"', 'ok'],
     'before\n' + err(3, 'BOOLEAN_EXPECTED', 'a condition takes a boolean, and this is an integer -- say what is meant: x != 0', 'V07.haro'), 1),
    ('V08', 'R4', 'a text in a condition is refused, as before', '.haro',
     [L, 'if OldText()', T + '? "text"', 'ok'],
     err(2, 'BOOLEAN_EXPECTED', 'a condition takes a boolean, and this is a text -- say what is meant: x != ""', 'V08.haro'), 1),
    ('V09', 'R5', 'a .haro function answering 1 stays strict: the compiler proves it is Haro\'s', '.haro',
     ['? "before"', 'if HaroOne()', T + '? "one"', 'ok', 'func HaroOne', T + 'return 1'],
     'before\n' + err(2, 'BOOLEAN_EXPECTED', 'a condition takes a boolean, and this is an integer -- say what is meant: x != 0', 'V09.haro'), 1),
    ('V10', 'R5', 'a value no longer a call\'s answer is not converted: an integer name holding the 1 stays an integer', '.haro',
     [L, 'iX = OldFlag()', '? iX + 1', '? "before"', 'if iX', T + '? "x"', 'ok'],
     '2\nbefore\n' + err(5, 'BOOLEAN_EXPECTED', 'a condition takes a boolean, and this is an integer -- say what is meant: x != 0', 'V10.haro'), 1),
    ('V11', 'R5', 'arithmetic sees the integer: only a boolean place converts', '.haro',
     [L, '? OldFlag() + 1', 'iN = OldFlag()', '? iN'],
     '2\n1\n', 0),
    ('V12', 'R5', 'a built-in answering an integer stays strict in a condition', '.haro',
     ['if Len("ab")', T + '? "len"', 'ok'],
     err(1, 'BOOLEAN_EXPECTED', 'a condition takes a boolean, and this is an integer -- say what is meant: x != 0', 'V12.haro'), 1),
    ('V13', 'R5', 'a method of the .haro class through this stays strict', '.haro',
     ['oP = new P', 'oP.Run()', 'class P', 'func Run', T + 'if this.One()', T + T + '? "one"', T + 'ok', 'func One', T + 'return 1'],
     None, 1),
    ('V14', 'R6', 'a .ring file reads its own answers as it did', '.ring',
     [L, 'if OldFlag()', T + '? "ring"', 'ok', 'x = OldSeven()', '? x', 'if OldSeven()', T + '? "seven"', 'ok'],
     'ring\n7\nseven\n', 0),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    with open(os.path.join(HERE, 'cases', 'old.ring'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(OLD) + '\n')
    out = []
    for cid, line, why, ext, src, stdout, code in CASES:
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        if stdout is None:  # V13: refused inside a method, with its frames
            stdout = (err(5, 'BOOLEAN_EXPECTED', 'a condition takes a boolean, and this is an integer -- say what is meant: x != 0', 'V13.haro')
                      .replace('\nin file V13.haro ', '\nIn method run() in file V13.haro\n\nCalled from line 2 in file V13.haro '))
        row = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.53',
        'decision': 'TYPES.md section 6 (D55); HARO-RINGBOUNDARY-BOOL-01; the desk\'s reading is D65',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {
            'R1': 'a .ring 1 or 0 given to a b name is true or false',
            'R2': '... in a condition and as an operand of not, and, or',
            'R3': '... from a method dispatched by name',
            'R4': 'any other answer refused by the check that stood',
            'R5': 'a call proven Haro\'s stays strict; no later conversion; arithmetic sees the integer',
            'R6': 'a .ring file reads as it did',
        },
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
