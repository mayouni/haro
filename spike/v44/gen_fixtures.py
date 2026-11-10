"""Haro v0.44 -- four runtime defects stzlib found on Ring++ and reproduced on haro.exe (HARO-PORTED-FINDINGS-01), fixed in Haro under the
author's Haro-first ruling. Written FIRST, before the VM is touched.

THE RULINGS. The author, 2026-11-08 (PRINCIPAL-HAROFIRST-01, LEDGER line 207, carried by Central 08:18): "I want all our projects to work
against Haro and not Ring++ ... the fixes and enhancements should go into Haro and not Ring++." And on this desk's order: "Yes, that order".

THE LINES. Ring 1.27 is the specification of a .ring file's surface; every expected answer below was read off Ring 1.27 (D:\\Ring127),
which is this rung's subject and never its judge.
  P1  a math native outside its domain raises R51 "Value Error", as Ring's does: sqrt of a negative, log and log10 of a number at or
      below zero, acos and asin beyond 1, pow of a negative to a non-integer power or of 0 to a negative one; an overflow to inf is no error
  P2  a NaN is unordered: every ordering is false, = is false, != is true, in a condition as in a value -- in a .ring and a .haro file
  P3  a letter of a text is written by `s[i] = c` in a .ring file, as Ring writes it: one character, or a number taken as its byte; more or
      fewer than one is R7, an index past the end R2; the text is a value, so another name holding it does not change
  P4  a .haro file refuses it: a text is not written in place (TEXT_IN_PLACE; D56 (c): bytes are, text is not)
  P5  (RETIRED v0.49, with zip.zig) zip_openfile(f, "a") on a file that is no archive answers a null handle, every later call on it does nothing, and the file is not
      rewritten -- as Ring's zip does
  P6  (RETIRED v0.49, with zip.zig) zip_extract_allfiles writes every entry, the last of a name winning, and answers nothing, as Ring's does; a name that leaves the
      folder is not written (Ring writes it: a named divergence)

THE DESK'S READINGS, recorded as its own:
  - a letter of a text held by a global, an attribute or a list item is REFUSED in a .ring file for now, by name: the VM writes the letter
    into a register its holder does not read back, so allowing it would be a wrong answer with no error; Ring allows it (a named
    divergence, until the compiler writes the text back)
  - TEXT_IN_PLACE's todo builds the new text: left(t, i - 1) + c + substr(t, i + 1)

MEASURED on haro 5ef8a04, before the rung: sqrt(-2) is -nan, and `x <= 0` and `x >= 0` are both true; `s[2] = "x"` is "Bad parameter type!"
in a .ring and a .haro file; append to a 28-byte text writes a 109-byte archive over it; entries a.txt, a.txt, b.txt extract to a.txt only,
answering 0.

  python spike/v44/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def err(cid, ext, line, msg, where=None, called=None):
    """an uncaught error at `line`: Ring's report, the program's file named"""
    out = ['', f'Line {line} {msg} ']
    if where:
        out.append(f'{where} in file {cid}{ext}')
        out.append('')
        out.append(f'Called from line {called} in file {cid}{ext} ')
    else:
        out.append(f'in file {cid}{ext} ')
    return out


R51 = 'Error (R51) : Value Error'
CASES = [
    # Q10, Q11, Q12 AND Q14 RETIRED 2026-11-09 (v0.49): they judged zip.zig, the twelve zip_ natives Haro published, retired when
    # Softanza's engine took ZIP (stz_compress; stzlib cb6f5de65; the author's "we have zip covered by the engine!!"). What they asked
    # is now the engine's, judged by stzlib's own guard; v49 judges that a zip_ call is Ring's R3. Their plants, Z17 to Z22, go with them.
    # v0.48 RE-SPELLED, 2026-11-09, AFTER THIS COURT SPOKE (the Principal's ruling, "ParentClassName"): a .haro program's calls of
    # built-ins are spelled as Softanza writes a name (Len, IsNull, SubStr), by study/v48/respell.py, ported here by
    # study/v47/port_cases.py --respell. A report still names a built-in as the VM registers it. Each case asks what it asked.
    ('Q01', 'P1', 'sqrt of a negative raises R51, as Ring does', '.ring', ['? "before"', 'x = sqrt(-2)', '? x'],
     ['before', '', f'Line 2 {R51} ', 'In sqrt() in file Q01.ring '], 1),
    ('Q02', 'P1', 'every domain error raises R51; a value at the edge or an overflow is none', '.haro', [
        'f()', 'func f',
        T + 'for tE in ["Log(-1)", "Log(0)", "Log10(0)", "ACos(2)", "ASin(2)", "Pow(-8, 0.5)", "Pow(0, -1)", "Sqrt(-3)"]',
        T * 2 + 'try', T * 3 + 'Eval("x = " + tE)', T * 3 + '? tE + " answered"', T * 2 + 'catch e', T * 3 + '? tE + " " + e.Code()', T * 2 + 'done',
        T + 'next',
        T + '? Sqrt(0)', T + '? Pow(-8, 3)', T + '? Pow(0, 0)', T + '? Sqrt(-0.0)', T + '? Pow(2, 2000)', T + '? ACos(1)'],
     ['Log(-1) R51', 'Log(0) R51', 'Log10(0) R51', 'ACos(2) R51', 'ASin(2) R51', 'Pow(-8, 0.5) R51', 'Pow(0, -1) R51', 'Sqrt(-3) R51',
      '0', '-512', '1', '0', 'inf', '0']),
    # Q02 RE-SPELLED AFTER ITS COURT SPOKE, 2026-11-09 (v0.48): its expressions are eval'd in a .haro program, which spells a built-in as
    # the Principal ruled (Log, ACos, Pow); the case asks what it asked.
    ('Q03', 'P2', 'a NaN is unordered in a .ring file: Ring\'s answers', '.ring', [
        'x = exp(1000)', 'y = x - x', '? y <= 0', '? y >= 0', '? y < 0', '? y > 0', '? y = y', '? y != y', '? y = 0',
        'if y >= 0 ? "ge" else ? "not ge" ok', 'if y < 0 ? "lt" else ? "not lt" ok', 'if y <= y ? "le" else ? "not le" ok'],
     ['0', '0', '0', '0', '0', '1', '0', 'not ge', 'not lt', 'not le']),
    # Q04 CHANGED AFTER v0.52's code, said so (v52/GRAMMAR.md): in a .haro file a float meets only a float, so the NaN is ordered
    # against 0f, and = and != on two floats are refused (FLOAT_EQUALITY, v0.52's N12 and N13) -- the two lines that asked them go
    ('Q04', 'P2', 'a NaN is unordered in a .haro file', '.haro', [
        'f()', 'func f', T + 'nX = Exp(1000)', T + 'nY = nX - nX', T + '? nY <= 0f', T + '? nY >= 0f', T + '? nY < 0f', T + '? nY > 0f',
        T + 'if nY >= 0f', T * 2 + '? "ge"', T + 'else', T * 2 + '? "not ge"', T + 'ok'],
     ['false', 'false', 'false', 'false', 'not ge']),
    ('Q05', 'P3', 'a letter of a local text is written as Ring writes it, and a copy does not move', '.ring', [
        'f()', 'func f', T + 's = "abc"', T + 's[2] = "x"', T + '? s', T + 't = s', T + 's[1] = "z"', T + '? t', T + '? s', T + 's[3] = 66',
        T + '? s', T + '? len(s)'],
     ['axc', 'axc', 'zxc', 'zxB', '3']),
    ('Q06', 'P3', 'more than one character is R7', '.ring', ['f()', 'func f', T + 's = "abc"', T + 's[2] = "xy"'],
     ['', 'Line 4 Error (R7) : Can\'t assign to a string letter more than one character ', 'In function f() in file Q06.ring', '',
      'Called from line 1 in file Q06.ring '], 1),
    ('Q07', 'P3', 'an index past the end is R2', '.ring', ['f()', 'func f', T + 's = "abc"', T + 's[4] = "x"'],
     ['', 'Line 4 Error (R2) : Array Access (Index out of range) ', 'In function f() in file Q07.ring', '', 'Called from line 1 in file Q07.ring '], 1),
    ('Q08', 'P3', 'a letter of a global\'s text is refused by name, never dropped', '.ring', ['$g = "abc"', '$g[2] = "x"', '? $g'],
     ['', 'Line 2 Haro: a letter of a text held by a global, an attribute or a list item is not written yet -- copy it to a local, write the '
      'letter, and assign it back ', 'in file Q08.ring '], 1),
    ('Q09', 'P4', 'a .haro file refuses a letter written in place', '.haro', ['f()', 'func f', T + 'tS = "abc"', T + 'tS[2] = "x"'],
     ['', 'Line 4 Error (TEXT_IN_PLACE) : a text is not written in place -- build a new one: left(t, i - 1) + c + substr(t, i + 1) ',
      'In function f() in file Q09.haro', '', 'Called from line 1 in file Q09.haro '], 1),
    ('Q13', 'P2', 'a NaN compared through a global (cmpv) is unordered too', '.ring', [
        '$y = exp(1000) - exp(1000)', '? $y <= 0', '? $y > 0', '? $y = $y'],
     ['0', '0', '0']),
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
    out.append(case)
doc = {'rung': 'v0.44', 'decision': 'HARO-PORTED-FINDINGS-01, under PRINCIPAL-HAROFIRST-01: four runtime defects fixed in Haro, Ring 1.27 the specification of a .ring file',
       'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build, each case in a folder of its own',
       'lines': {'P1': 'a domain error raises R51', 'P2': 'a NaN is unordered', 'P3': 'a letter of a local text is written as Ring writes it',
                 'P4': 'a .haro file refuses a text written in place', 'P5': 'append to no archive answers a null handle and leaves the file',
                 'P6': 'extraction writes every entry, the last of a name winning'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
