"""Haro v0.52 -- numbers (D55 T4): three kinds of number, each saying whether it is exact. Written FIRST, before the VM is touched.

THE RULING. D55 T4 (TYPES.md, RULED by the author 2026-11-07, decision (c) "yes; measurement 2 before its rung"): an `integer` (i) is whole
and exact to 64 bits; a `decimal` (d) is base-10, as money and measured quantities are written, exact to its digits; a `float` (f) is binary
floating point, near and never exact. A literal with a point is a decimal (`0.1 + 0.2 = 0.3` is true); a float is asked for (`0.1f`, or
`Float(x)`). Mixing is refused but for one widening: an integer may join a decimal. Comparing two floats with `=` is refused; `Near(fA, fB,
fTolerance)` says it. The author, 2026-11-10: "start the next type rung".

MEASUREMENT 2, taken before this file: Haro's own .haro code holds 15 literals with a point in 274 files (10 files), and a .ring file never
reads a decimal, so stzMax, a .ring program, carries none. The arithmetic's own cost is measured on the build (v52/GRAMMAR.md).

THE DESK'S READINGS INSIDE T4 (D64), each judged below:
  - a decimal keeps the digits written after its point (`12.50` prints 12.50); + and - keep the larger scale, * adds them
  - `/` on integers and decimals answers the exact decimal in the fewest digits (7 / 2 = 3.5, 10 / 5 = 2), or raises DECIMAL_INEXACT
    when the quotient has no end (1 / 3); `Divide(a, b, iPlaces)` rounds half to even
  - a decimal is 64 bits of digits and a scale up to 18: past them, DECIMAL_OVERFLOW
  - `Decimal(x)` from an integer or a text, `Decimal(x, iPlaces)` rounding (a float only so), `Float(x)`, `Integer(x)` of a whole number
  - `Type()` names a decimal DECIMAL; a float keeps NUMBER, the word a .ring file and its integers share
  - a decimal reaching .ring code, or Softanza's engine, is a double there

THE LINES (in a .haro file; a .ring file reads as it did):
  N1  a literal with a point is a decimal, exact: printed as its digits, compared by value, DECIMAL to Type()
  N2  a literal ending in f is a float
  N3  + - * on decimals and integers are exact; an integer joins a decimal; past 64 bits of digits, DECIMAL_OVERFLOW
  N4  / on integers and decimals is the exact decimal, or DECIMAL_INEXACT; Divide rounds half to even
  N5  a float does not mix with a decimal or an integer: NUMBER_MIX, naming the conversion
  N6  = and != on two floats are refused: FLOAT_EQUALITY, naming Near; the orderings stand
  N7  Near(fA, fB, fTolerance)
  N8  Float, Decimal, Integer convert, each refusing what it cannot say exactly
  N9  the letters: d a decimal, f a float, n any number
  N10 a .ring file is untouched; a decimal is a double in .ring code

  python spike/v52/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def err(line, code, msg, f):
    return f'\nLine {line} Error ({code}) : {msg} \nin file {f} '


INEXACT = 'this quotient has no exact decimal -- round it, Divide(a, b, iPlaces), or divide floats, Float(a) / Float(b)'

CASES = [
    ('N01', 'N1', 'a literal with a point is an exact decimal, printed as its digits', '.haro',
     ['? 0.1 + 0.2', '? 0.1 + 0.2 = 0.3', '? 12.50', '? Type(1.5)', '? IsNumber(1.5)'],
     '0.3\ntrue\n12.50\nDECIMAL\ntrue\n', 0),
    ('N02', 'N3', 'an integer joins a decimal; + and - keep the larger scale, * adds them; a negative decimal', '.haro',
     ['? 1.5 * 2', '? 2 + 0.25', '? 10 - 0.75', '? 1.25 * 1.2', '? -2.50 + 1'],
     '3.0\n2.25\n9.25\n1.500\n-1.50\n', 0),
    ('N03', 'N1', 'decimals compare by value, with each other and with integers', '.haro',
     ['? 0.10 = 0.1', '? 1.5 < 2', '? 2 > 1.99', '? 1.0 = 1', '? 0.3 != 0.30'],
     'true\ntrue\ntrue\ntrue\nfalse\n', 0),
    ('N04', 'N4', '/ on integers and decimals is the exact decimal in the fewest digits', '.haro',
     ['? 7 / 2', '? 1 / 8', '? 10 / 5', '? 1.5 / 0.5', '? Type(10 / 5)'],
     '3.5\n0.125\n2\n3\nDECIMAL\n', 0),
    ('N05', 'N4', 'a quotient with no end raises DECIMAL_INEXACT, naming the ways', '.haro',
     ['? "before"', '? 1 / 3'],
     'before\n' + err(2, 'DECIMAL_INEXACT', INEXACT, 'N05.haro'), 1),
    ('N06', 'N4', 'Divide rounds half to even, to the places asked', '.haro',
     ['? Divide(1, 3, 4)', '? Divide(2, 3, 2)', '? Divide(1, 8, 2)', '? Divide(5, 8, 2)', '? Divide(10, 4, 0)', '? Divide(-1, 3, 2)'],
     '0.3333\n0.67\n0.12\n0.62\n2\n-0.33\n', 0),
    ('N07', 'N10', 'a .ring file reads numbers as it did', '.ring',
     ['? 0.1 + 0.2 = 0.3', '? 7 / 2', '? type(1.5)', '? 1.5 * 2'],
     '0\n3.50\nNUMBER\n3\n', 0),
    ('N08', 'N2', 'a literal ending in f is a float', '.haro',
     ['? Type(0.5f)', '? 0.5f + 0.25f', '? 2f * 0.5f', '? 0.5f < 1f'],
     'NUMBER\n0.75\n1\ntrue\n', 0),
    ('N09', 'N5', 'a decimal and a float do not mix', '.haro',
     ['? "before"', '? 1.5 + 0.5f'],
     'before\n' + err(2, 'NUMBER_MIX', 'decimal + float -- a decimal and a float do not mix; convert one: Float(d), or Decimal(f, iPlaces)',
                      'N09.haro'), 1),
    ('N10', 'N5', 'an integer and a float do not mix', '.haro',
     ['? 2 * 0.5f'],
     err(1, 'NUMBER_MIX', 'integer * float -- an integer and a float do not mix; convert one: Float(i)', 'N10.haro'), 1),
    ('N11', 'N5', 'a decimal is not ordered against a float', '.haro',
     ['? 1.5 < 2f'],
     err(1, 'NUMBER_MIX', 'decimal < float -- a decimal and a float do not mix; convert one: Float(d), or Decimal(f, iPlaces)', 'N11.haro'), 1),
    ('N12', 'N6', 'two floats are ordered, never claimed equal', '.haro',
     ['? 0.5f < 1f', '? 0.5f = 0.5f'],
     'true\n' + err(2, 'FLOAT_EQUALITY', 'float = float claims a sameness binary floating point does not keep -- say how near: '
                    'Near(fA, fB, fTolerance)', 'N12.haro'), 1),
    ('N13', 'N6', '!= on two floats is refused too', '.haro',
     ['? 1f != 2f'],
     err(1, 'FLOAT_EQUALITY', 'float != float claims a sameness binary floating point does not keep -- say how near: '
         'Near(fA, fB, fTolerance)', 'N13.haro'), 1),
    ('N14', 'N7', 'Near says how near two floats are', '.haro',
     ['fA = 0.1f + 0.2f', '? Near(fA, 0.3f, 0.000001f)', '? Near(1f, 2f, 0.5f)', '? Near(1f, 1.5f, 0.5f)'],
     'true\nfalse\ntrue\n', 0),
    ('N15', 'N8', 'Float, Decimal and Integer convert', '.haro',
     ['? Float(1.5) + 0.25f', '? Decimal(2) + 0.5', '? Decimal("12.50")', '? Decimal(0.1f, 2)', '? Decimal(2.675, 2)', '? Integer(4.0)',
      '? Integer(10 / 5)', '? Float(3)'],
     '1.75\n2.5\n12.50\n0.10\n2.68\n4\n2\n3\n', 0),
    ('N16', 'N8', 'a float has no exact decimal unless the places are said', '.haro',
     ['? Decimal(0.1f)'],
     err(1, 'DECIMAL_INEXACT', 'a float has no exact decimal -- say how many places: Decimal(f, iPlaces)', 'N16.haro'), 1),
    ('N17', 'N8', 'Integer of a number that is not whole is refused', '.haro',
     ['? Integer(2.5)'],
     err(1, 'NOT_WHOLE', 'this number is not whole -- round it first: Decimal(d, 0)', 'N17.haro'), 1),
    ('N18', 'N9', 'the letters: d holds a decimal, f a float, n any number; d given a float is refused', '.haro',
     ['dPrice = 12.50', 'fRatio = 0.5f', 'nAny = 1.5', 'nAny = 2f', '? dPrice', 'dBad = Float(1)'],
     '12.50\n' + err(6, 'TYPE_LETTER', '`dBad` is lettered d, a decimal, and is given a float', 'N18.haro'), 1),
    ('N19', 'N9', 'an integer letter refuses a decimal literal when compiling', '.haro',
     ['? "before"', 'iN = 2.5'],
     None, 1),
    ('N20', 'N10', 'a decimal is a double in .ring code', '.haro',
     ['load "lib.ring"', '? half(1.5)', '? Type(half(1.5))'],
     '0.75\nNUMBER\n', 0),
    ('N21', 'N3', 'past 64 bits of digits, DECIMAL_OVERFLOW', '.haro',
     ['? 99999999999999999.9 * 1000'],
     err(1, 'DECIMAL_OVERFLOW', 'decimal * integer leaves 64 bits of digits', 'N21.haro'), 1),
    # N22 CHANGED AFTER THE CODE, said so: String(0.125) added -- Ring's two places print 12.50 too, so only a digit past them shows
    # that String is the decimal's own text
    ('N22', 'N1', 'a decimal is text only when asked; asked, it is its digits', '.haro',
     ['? "price " + String(12.50)', '? String(0.125)', '? "x" + 1.5'],
     'price 12.50\n0.125\n' + err(3, 'NO_COERCION', 'text + decimal -- a value changes type only when asked: string(x) or number(x)', 'N22.haro'), 1),
    ('N23', 'N4', 'a decimal divided by zero is Ring\'s R1', '.haro',
     ['? 1.5 / 0'],
     err(1, 'R1', 'Can\'t divide by zero', 'N23.haro'), 1),
    # N24 to N29 were ADDED AFTER THE CODE, said so: the plants found six protections no case asked about
    ('N24', 'N2', 'a float\'s arithmetic stays a float, never narrowed to an integer', '.haro',
     ['fX = 2f * 0.5f', 'fY = fX + 1f', '? fY'],
     '2\n', 0),
    ('N25', 'N1', 'decimals are equal and ordered exactly, past a double\'s seventeen digits', '.haro',
     ['? 1234567890.12345678 = 1234567890.12345679', '? 1234567890.12345678 < 1234567890.12345679'],
     'false\ntrue\n', 0),
    ('N26', 'N10', 'a .ring file has none of Haro\'s number built-ins: near() is Ring\'s R3 there', '.ring',
     ['? "before"', '? near(1, 2, 3)'],
     'before\n\nLine 2 Error (R3) : Calling Function without definition: near \nin file N26.ring ', 1),
    ('N27', 'N5', 'a float\'s operator is named as written; a float is negated', '.haro',
     ['fX = 0.5f', '? -fX', '? fX - 1'],
     '-0.50\n' + err(3, 'NUMBER_MIX', 'float - integer -- an integer and a float do not mix; convert one: Float(i)', 'N27.haro'), 1),
    ('N28', 'N3', '% on decimals is exact, the dividend\'s sign', '.haro',
     ['? 7.5 % 2', '? -7 % 2.5', '? 7.5f % 2f'],
     '1.5\n-2.0\n1.50\n', 0),
    ('N29', 'N1', 'a decimal keeps its digits through the compiled image: the second run reads it back', '.haro',
     ['? 12.50', '? 0.005'],
     '12.50\n0.005\n', 0),
    ('N30', 'N9', 'an f name refuses an integer given when the program runs', '.haro',
     ['fX = 1.5f', '? "before"', 'fX = Len("ab")'],
     'before\n' + err(3, 'TYPE_LETTER', '`fX` is lettered f, a float, and is given an integer', 'N30.haro'), 1),
]
CACHED = {'N29'}

LIB = {'N20': ('lib.ring', ['func half x', T + 'return x / 2'])}


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, ext, src, stdout, code in CASES:
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        if cid in LIB:
            lname, lsrc = LIB[cid]
            with open(os.path.join(HERE, 'cases', lname), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(lsrc) + '\n')
        if stdout is None:  # N19: the compiler's refusal, as v0.47's Y12 words it
            stdout = ('before\n\nLine 2 Haro refused this statement (i is the letter '
                      'of an integer, and this literal is a decimal; written `iN`, line 2 of N19.haro) and did not compile it -- running past it '
                      'would give a wrong answer \nin file N19.haro ')
        row = {'id': cid, 'kind': 'cached' if cid in CACHED else 'run', 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.52',
        'decision': 'D55 T4, numbers (TYPES.md, ruled 2026-11-07); the desk\'s readings inside it are D64',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
        'lines': {
            'N1': 'a literal with a point is an exact decimal', 'N2': 'a literal ending in f is a float',
            'N3': '+ - * exact; an integer joins a decimal; DECIMAL_OVERFLOW', 'N4': '/ exact or DECIMAL_INEXACT; Divide rounds half to even',
            'N5': 'a float mixes with neither: NUMBER_MIX', 'N6': '= and != on floats: FLOAT_EQUALITY', 'N7': 'Near',
            'N8': 'Float, Decimal, Integer', 'N9': 'd, f, n', 'N10': 'a .ring file untouched; a decimal is a double in .ring code',
        },
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
