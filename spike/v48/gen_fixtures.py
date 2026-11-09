"""Haro v0.48 -- a built-in is spelled as Softanza writes a name, in a .haro file. Written FIRST, before the compiler is touched.

THE RULING. The Principal, 2026-11-09, asked with the history (their 2026-11-07 ruling for v0.42 was "Lowercase (Recommended)") and three
options -- ParentClassName, keep lowercase, parent_class_name: "ParentClassName". It REVISES v0.42's rule that a native is spelled in
lowercase. The table of spellings is study/v48/builtin_names.py, drawn by the desk under the Principal's "I let you decide" (2026-11-09).

THE LINES, in a .haro file (a .ring file reads every spelling as Ring does):
  P1  a built-in -- one of Ring's 258 or one of the VM's own -- is called by one spelling, Softanza's casing (Len, IsNull, SubStr,
      ParentClassName); any other spelling, lowercase included, is refused when compiling, naming the one to write
  P2  a built-in whose registered name holds an underscore is reached by its spelling without one (tui_size is TUISize)
  P3  a program's own function of a built-in's name is the program's, as Ring has it: no spelling of the built-in is asked of it
  P4  an eval in a .haro program spells as the root does

  python spike/v48/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
REFUSED = 'and did not compile it -- running past it would give a wrong answer '


def refused(cid, line, want, text, called=2, where='function f()'):
    return ['before', '', f'Line {line} Haro refused this statement (a built-in is spelled `{want}`; written `{text}`, line {line} of {cid}.haro) '
            + REFUSED, f'In {where} in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


B = '? "before"'
CASES = [
    ('P01', 'P1', 'the built-ins in Softanza\'s casing run', '.haro', [
        'f()', 'func f', T + '? Len("abc")', T + '? IsNull(null)', T + '? SubStr("abcdef", 2, 3)', T + '? Upper("ab")', T + '? Char(65)',
        T + '? ParentClassName(new B)', 'class A', 'class B from A'],
     ['3', 'true', 'bcd', 'AB', 'A', 'a']),
    ('P02', 'P1', 'a built-in in lowercase is refused, naming its spelling', '.haro', [B, 'f()', 'func f', T + '? len("abc")'],
     refused('P02', 4, 'Len', 'len'), 1),
    ('P03', 'P1', 'a built-in in another mixed casing is refused', '.haro', [B, 'f()', 'func f', T + '? isNull(null)'],
     refused('P03', 4, 'IsNull', 'isNull'), 1),
    ('P04', 'P2', 'a built-in registered with an underscore is refused under that name', '.haro', [B, 'f()', 'func f', T + '? tui_size()'],
     refused('P04', 4, 'TUISize', 'tui_size'), 1),
    ('P05', 'P2', 'a built-in registered with an underscore is reached by its spelling without one', '.haro', [
        'f()', 'func f', T + 'aS = TUISize()', T + '? Len(aS)', T + '? aS[1] + aS[2]'],
     ['2', '0']),
    ('P06', 'P3', 'a .ring file reads every spelling as Ring does', '.ring', [
        '? len("ab")', '? Len("ab")', '? LEN("ab")', '? isNull("")', '? substr("abc", 2, 1)'],
     ['2', '2', '2', '1', 'b']),
    ('P07', 'P3', 'a program\'s own function of a built-in\'s name is the program\'s', '.haro', [
        'f()', 'func f', T + '? Max([3, 9, 2])', 'func Max aL', T + 'nBest = aL[1]', T + 'for x in aL', T * 2 + 'if x > nBest', T * 3 + 'nBest = x',
        T * 2 + 'ok', T + 'next', T + 'return nBest'],
     ['9']),
    ('P08', 'P4', 'an eval in a .haro program spells a built-in as the root does', '.haro', [
        'f()', 'func f', T + 'eval("? len(' + "'ab'" + ')")'],
     ['', 'Line 3 Error (E1) : a built-in is spelled `Len`; written `len` ', 'In function f() in file P08.haro', '',
      'Called from line 1 in file P08.haro '], 1),
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
doc = {'rung': 'v0.48', 'decision': 'the Principal 2026-11-09: a built-in in a .haro file is spelled ParentClassName, Softanza\'s casing',
       'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
       'lines': {'P1': 'one spelling per built-in, Softanza\'s casing', 'P2': 'an underscore name reached without its underscore',
                 'P3': 'a program\'s own function of that name is its own; a .ring file reads every spelling',
                 'P4': 'an eval spells as the root does'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
