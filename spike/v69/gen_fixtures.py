"""Haro v0.69, `haro check` names what the run refuses (HARO-CHECKRUN-01): the cases of v69/fixtures.json and their files, written
BEFORE the checker changed. Every expectation is typed here, none is read off a build.

  python spike/v69/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  a form the run refuses is an error of `haro check`, at the run's line and in the run's words (S01-S13)
  L2  check names every refused form of a file; the run names the first it reaches (M01)
  L3  the unit: a refused form in a loaded file is named under that file (U01)
  L4  a program with no refused form has no such error (N01)
  L5  a .ring file keeps its own reading: the same forms are no error there (N02)
  L6  `check --facts` carries each one, in its function or at the file's top (G01)
  L7  in a .haro file a definition closed by `end` holds nothing after it: the statements after it are the program's, so the unit
      runs, and what the run raises there check reports (T01, T02)
  L8  a .ring file's definition holds what follows it, as before (T03)
  L9  the facts give a closed function its own lines (T04)
  L10 a trap the compiler rolled back is no refusal: a function it compiles a second time has none (W01, written after the code)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RULE = 'haro/refused-form'
cases = []


def case(cid, line, what, file, src, run, check, facts=None, extra=None):
    """run: {'refuses': [file, row, reason, written]} or {'stdout': text} or {'raises': text}; check: {'errors': n, 'found': [[file, row,
    rule]], 'refused': [[file, row, reason, written]], 'library': bool}"""
    files = {file: src}
    files.update(extra or {})
    for name, text in files.items():
        with open(os.path.join(HERE, 'cases', name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + file, 'run': run, 'check': check}
    if facts is not None:
        c['facts'] = facts
    cases.append(c)


def one(cid, what, file, src, row, reason, written):
    """L1: one refused form; the run refuses it at `row`, and check names the same row and words"""
    ref = [file, row, reason, written]
    case(cid, 'L1', what, file, src, {'refuses': ref}, {'errors': 1, 'found': [[file, row, RULE]], 'refused': [ref], 'library': False})


one('S01', 'a definition written with empty parentheses', 's01.haro', '''func F()
    return 1
end
print F()
''', 1, 'a definition without parameters has no parentheses; written', '()')

one('S02', '`but` for elseif', 's02.haro', '''iX = 2
if iX = 1
    print "one"
but iX = 2
    print "two"
end
''', 4, 'one spelling: `elseif`; written', 'but')

one('S03', '`:key = value` in a list', 's03.haro', '''vL = [:name = "ada"]
print Len(vL)
''', 1, '`:key = value` is no pair in a .haro file: write ["key": value] for a map, [:key, value] for a pair, or declare a record for '
        'named fields (HARO-SURFACE-01)', ':name = "ada"')

one('S04', '`see` for print', 's04.haro', '''see "x"
''', 1, 'one spelling: `print`; written', 'see')

one('S05', '`null`', 's05.haro', '''tA = null
print tA
''', 1, '`null` is no value of Haro -- the empty text is "", and absence is none; written', 'null')

one('S06', 'a block closed with `ok`', 's06.haro', '''iX = 1
if iX = 1
    print "one"
ok
''', 4, 'a block ends with `end`; written', 'ok')

one('S07', '`==`', 's07.haro', '''iA = 1
iB = 1
if iA == iB
    print "same"
end
''', 3, '`==` is no operator: equality is `=`; written', 'iA == iB')

one('S08', 'a name in another spelling', 's08.haro', '''nCount = 1
print ncount
''', 2, 'one spelling per name -- declared `nCount` at line 1; written', 'ncount')

one('S09', 'a loop closed with `next`', 's09.haro', '''for i = 1 to 2
    print i
next
''', 3, 'a block ends with `end`; written', 'next')

one('S10', 'a method written with empty parentheses', 's10.haro', '''class P
    def Show()
        print 1
    end
end
oP = new P
oP.Show()
''', 2, 'a definition without parameters has no parentheses; written', '()')

one('S11', 'a definition in braces', 's11.haro', '''func Add(iA, iB) {
    return iA + iB
}
print Add(1, 2)
''', 1, 'a definition ends with `end`, and this one has none; written', 'Add')

one('S12', 'the letter c', 's12.haro', '''cName = "ada"
print cName
''', 1, "`c` is Softanza's letter and no type's -- text is t: tName; written", 'cName')

one('S13', '`IsNull`', 's13.haro', '''tA = "x"
if IsNull(tA)
    print 1
end
''', 2, 'one spelling: `IsEmpty`; written', 'IsNull')

M = [['m01.haro', 1, 'one spelling: `print`; written', 'see'],
     ['m01.haro', 5, 'one spelling: `elseif`; written', 'but'],
     ['m01.haro', 10, '`:key = value` is no pair in a .haro file: write ["key": value] for a map, [:key, value] for a pair, or declare a '
                      'record for named fields (HARO-SURFACE-01)', ':name = "ada"']]
M_SRC = '''see "top"
func F(iX)
    if iX = 1
        return "one"
    but iX = 2
        return "two"
    end
    return "many"
end
vL = [:name = "ada"]
print F(2)
'''
case('M01', 'L2', 'three refused forms, one of them in a function: check names the three, the run the first', 'm01.haro', M_SRC,
     {'refuses': M[0]}, {'errors': 3, 'found': [[m[0], m[1], RULE] for m in M], 'refused': M, 'library': False})

U = ['u01lib.haro', 3, 'one spelling per name -- declared `iY` at line 2; written', 'iy']
case('U01', 'L3', 'a refused form in a loaded file is named under that file', 'u01.haro', '''load "u01lib.haro"
print Twice(2)
''', {'refuses': U}, {'errors': 1, 'found': [[U[0], U[1], RULE]], 'refused': [U], 'library': False},
     extra={'u01lib.haro': '''func Twice(iX)
    iY = iX * 2
    return iy
end
'''})

case('N01', 'L4', 'a program with no refused form', 'n01.haro', '''func Add(iA, iB)
    return iA + iB
end
class P
    nX = 1
    def Show
        print nX
    end
end
oP = new P
oP.Show()
print Add(1, 2)
''', {'stdout': '1\n3\n'}, {'errors': 0, 'found': [], 'refused': [], 'library': False})

case('N02', 'L5', "the same forms in a .ring file are that file's own reading", 'n02.ring', '''x = 2
if x = 1
    see "one" + nl
but x = 2
    see "two" + nl
ok
aL = [:name = "ada"]
see len(aL)
see nl
see F()
see nl
func F()
    return 7
''', {'stdout': 'two\n1\n7\n'}, {'errors': 0, 'found': [], 'refused': [], 'library': False})

case('G01', 'L6', "the facts carry each refused form: two at the file's top, one in its function", 'g01.haro', M_SRC,
     {'refuses': ['g01.haro', 1, M[0][2], M[0][3]]},
     {'errors': 3, 'found': [['g01.haro', m[1], RULE] for m in M], 'refused': [['g01.haro', m[1], m[2], m[3]] for m in M], 'library': False},
     facts={'top': [[RULE, 1], [RULE, 10]], 'functions': {'F': {'line': 2, 'end_line': 9, 'compiled': False, 'findings': [[RULE, 5]]}}})

case('T01', 'L7', "a statement after a closed function is the program's: the call it makes to no function is reported", 't01.haro', '''func F
    return 1
end
print Zed()
''', {'raises': 'Line 4 Error (R3) : Calling Function without definition: zed'},
     {'errors': 1, 'found': [['t01.haro', 4, 'haro/undefined-function']], 'refused': [], 'library': False})

case('T02', 'L7', "a statement after a closed class is the program's: its `new` of no class is reported", 't02.haro', '''class P
    nX = 1
end
oP = new Q
''', {'raises': 'Line 4 Error (R11)'},
     {'errors': 1, 'found': [['t02.haro', 4, 'haro/unknown-class']], 'refused': [], 'library': False})

case('T03', 'L8', 'a .ring definition holds what follows it: the unit runs nothing and is read as a library', 't03.ring', '''func F
    return 1
see Zed()
''', {'stdout': ''}, {'errors': 0, 'found': [], 'refused': [], 'library': True})

case('T04', 'L9', 'the facts give a closed function its own lines, and the print after it is not its own', 't04.haro', '''print G()
func G
    return 2
end
print G() + 1
''', {'stdout': '2\n3\n'}, {'errors': 0, 'found': [], 'refused': [], 'library': False},
     facts={'top': [], 'functions': {'G': {'line': 2, 'end_line': 4, 'compiled': True, 'findings': [], 'impure': None}}})

# WRITTEN AFTER THE CODE, said so: counting on stzlib showed 63 errors in one function of stzDiagram.ring that the run does not refuse -- its
# locals pass the register window, so the compiler compiles it a second time with shared registers and throws the first attempt away, traps
# and all. A trap that was rolled back is no refusal.
W_SRC = 'func Wide\n' + ''.join(f'    iV{k} = {k}\n' for k in range(1, 261)) + '    return iV1 + iV260\nend\nprint Wide()\n'
case('W01', 'L10', 'a function compiled twice (260 locals share registers) has no refused form: a trap rolled back is none', 'w01.haro', W_SRC,
     {'stdout': '261\n'}, {'errors': 0, 'found': [], 'refused': [], 'library': False})

doc = {'version': '0.69', 'task': 'HARO-CHECKRUN-01', 'rule': RULE,
       'law': 'a form the run refuses is an error of `haro check`, at the same line and in the same words', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
