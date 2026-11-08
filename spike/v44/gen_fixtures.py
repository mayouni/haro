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
  P5  zip_openfile(f, "a") on a file that is no archive answers a null handle, every later call on it does nothing, and the file is not
      rewritten -- as Ring's zip does
  P6  zip_extract_allfiles writes every entry, the last of a name winning, and answers nothing, as Ring's does

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
    ('Q01', 'P1', 'sqrt of a negative raises R51, as Ring does', '.ring', ['? "before"', 'x = sqrt(-2)', '? x'],
     ['before', '', f'Line 2 {R51} ', 'In sqrt() in file Q01.ring '], 1),
    ('Q02', 'P1', 'every domain error raises R51; a value at the edge or an overflow is none', '.haro', [
        'f()', 'func f',
        T + 'for tE in ["log(-1)", "log(0)", "log10(0)", "acos(2)", "asin(2)", "pow(-8, 0.5)", "pow(0, -1)", "sqrt(-3)"]',
        T * 2 + 'try', T * 3 + 'eval("x = " + tE)', T * 3 + '? tE + " answered"', T * 2 + 'catch e', T * 3 + '? tE + " " + e.Code()', T * 2 + 'done',
        T + 'next',
        T + '? sqrt(0)', T + '? pow(-8, 3)', T + '? pow(0, 0)', T + '? sqrt(-0.0)', T + '? pow(2, 2000)', T + '? acos(1)'],
     ['log(-1) R51', 'log(0) R51', 'log10(0) R51', 'acos(2) R51', 'asin(2) R51', 'pow(-8, 0.5) R51', 'pow(0, -1) R51', 'sqrt(-3) R51',
      '0', '-512', '1', '0', 'inf', '0']),
    ('Q03', 'P2', 'a NaN is unordered in a .ring file: Ring\'s answers', '.ring', [
        'x = exp(1000)', 'y = x - x', '? y <= 0', '? y >= 0', '? y < 0', '? y > 0', '? y = y', '? y != y', '? y = 0',
        'if y >= 0 ? "ge" else ? "not ge" ok', 'if y < 0 ? "lt" else ? "not lt" ok', 'if y <= y ? "le" else ? "not le" ok'],
     ['0', '0', '0', '0', '0', '1', '0', 'not ge', 'not lt', 'not le']),
    ('Q04', 'P2', 'a NaN is unordered in a .haro file', '.haro', [
        'f()', 'func f', T + 'nX = exp(1000)', T + 'nY = nX - nX', T + '? nY <= 0', T + '? nY >= 0', T + '? nY < 0', T + '? nY > 0',
        T + '? nY = nY', T + '? nY != nY', T + 'if nY >= 0', T * 2 + '? "ge"', T + 'else', T * 2 + '? "not ge"', T + 'ok'],
     ['false', 'false', 'false', 'false', 'false', 'true', 'not ge']),
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
    ('Q10', 'P5', 'appending to a file that is no archive answers a null handle and leaves the file', '.ring', [
        'write("notzip.zip", "This is a plain text file.." + nl)', 'oZip = zip_openfile("notzip.zip", "a")', '? isnull(oZip)',
        'zip_entry_open(oZip, "a.txt")', 'zip_entry_write(oZip, "hello", 5)', 'zip_entry_close(oZip)', 'zip_close(oZip)',
        '? len(read("notzip.zip"))'],
     ['1', '28']),
    ('Q11', 'P6', 'extracting writes every entry, the last of a name winning, and answers nothing', '.ring', [
        'oZip = zip_openfile("dup.zip", "w")',
        'zip_entry_open(oZip, "a.txt")', 'zip_entry_write(oZip, "first", 5)', 'zip_entry_close(oZip)',
        'zip_entry_open(oZip, "a.txt")', 'zip_entry_write(oZip, "second", 6)', 'zip_entry_close(oZip)',
        'zip_entry_open(oZip, "b.txt")', 'zip_entry_write(oZip, "bee", 3)', 'zip_entry_close(oZip)', 'zip_close(oZip)',
        '? zip_extract_allfiles("dup.zip", "out")', '? read("out/a.txt")', '? read("out/b.txt")'],
     ['', 'second', 'bee']),
    ('Q12', 'P5', 'appending to an archive keeps its entries and adds one (must not move)', '.ring', [
        'oZip = zip_openfile("two.zip", "w")', 'zip_entry_open(oZip, "a.txt")', 'zip_entry_write(oZip, "one", 3)', 'zip_entry_close(oZip)',
        'zip_close(oZip)', 'oZip = zip_openfile("two.zip", "a")', 'zip_entry_open(oZip, "b.txt")', 'zip_entry_write(oZip, "two", 3)',
        'zip_entry_close(oZip)', 'zip_close(oZip)', 'oZip = zip_openfile("two.zip", "r")', '? zip_filescount(oZip)', 'zip_close(oZip)'],
     ['2']),
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
