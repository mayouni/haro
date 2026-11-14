"""Haro v0.75, a command line is not built as text (doc/DOORS.md, D88 (d)): the cases of v75/fixtures.json and their files, written
BEFORE the code. Every expectation is typed here. The rule, this desk's reading of D88 (b) and (d) until `unjudged` gives a text
its origin: in a .haro file `System` and `SystemCmd` take a text written at the call, or an invocation.

  python spike/v75/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  a text written at the call runs as it did: a literal, and literals joined
  L2  a command line built as text is refused when the program is compiled: a text joined with anything that is not written
      there, and a name lettered as a text -- at either door
  L3  a text that reaches the door another way -- a function's answer, a name that may hold anything -- is COMMAND_LINE_BUILT
      when the program runs, and can be caught
  L4  an invocation passes, by any way it reaches the door
  L5  a .ring file reads as it did; a program's own function named System or SystemCmd is the program's
  L6  a court whose library holds a sentence of doors still judges, and runs its sibling court with no shell: what it answers
      is what it answered
  L7  a sentence of doors is read once: its judges answer from what was read
  L8  `haro check` lists the refused line, and reads no error where the door is given what it takes
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []
RULE = 'haro/refused-form'
CASES = os.path.join(HERE, 'cases')
os.makedirs(os.path.join(CASES, 'data'), exist_ok=True)
ECHO = '''for i = 3 to Len(sysargv)
    print "[" + sysargv[i] + "]"
end
'''
for name, text in (('data/note.txt', 'hello'), ('echo.haro', ECHO)):
    with open(os.path.join(CASES, *name.split('/')), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

SHOW = 'DEFINE COMMAND show AS (ITSELF yes, TAKES [word, text]) RATIONALE "this haro, printing what it is given"'
DATA = 'DEFINE ROOT data AS (AT "data", ALLOWS [read]) RATIONALE "the notes this program reads"'
WHY = 'a command line is written at the call, or is an invocation of a declared COMMAND; written'


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, check=None, kind=None, ext='.haro'):
    """run: {'stdout': text} exact with exit 0; {'raises': text} with 'never'; {'refuses': [row, reason, written]} with 'never'.
    check: {'errors': n, 'found': [[row, rule]]}. kind: 'ncourt' -- L6, the court's own procedure; 'reads' -- L7, likewise."""
    name = cid.lower() + ext
    with open(os.path.join(CASES, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if check is not None:
        c['check'] = check
    if kind is not None:
        c['kind'] = kind
    cases.append(c)


case('X01', 'L1', 'a text written at the call runs as it did: a literal, and literals joined', '''print SystemCmd("echo literal")
print SystemCmd("echo " + "joined")
print System("echo passed")
''', {'stdout': 'literal\njoined\npassed\n0\n'}, check={'errors': 0, 'found': []})

case('X02', 'L2', 'System given a text joined with a name is refused when the program is compiled', '''tWord = "built"
print "before"
System("echo " + tWord)
print "after"
''', {'refuses': [3, WHY, '"echo " + tWord'], 'never': 'after'}, check={'errors': 1, 'found': [[3, RULE]]})

case('X03', 'L2', 'SystemCmd given a text joined with a call is refused when the program is compiled', '''print "before"
print SystemCmd("echo " + Upper("built"))
print "after"
''', {'refuses': [2, WHY, '"echo " + Upper("built")'], 'never': 'after'}, check={'errors': 1, 'found': [[2, RULE]]})

case('X04', 'L2', 'a name lettered as a text is refused when the program is compiled, at either door', '''tLine = "echo held"
print "before"
System(tLine)
print "after"
''', {'refuses': [3, WHY, 'tLine'], 'never': 'after'}, check={'errors': 1, 'found': [[3, RULE]]})

M_BUILT = 'a command line is written at the call, or is an invocation of a declared COMMAND; this text was made elsewhere'
case('X05', 'L3', 'a text that reaches the door another way is COMMAND_LINE_BUILT when the program runs', '''func Line(ptWord)
    return "echo " + ptWord
end
xAny = "echo any"
try
    System(Line("made"))
    print "ran"
catch e
    print e.Code()
    print e.Message()
end
try
    print SystemCmd(xAny)
catch e
    print e.Code()
end
try
    print SystemCmd(Line("made"))
catch e
    print e.Code()
end
''', {'stdout': 'COMMAND_LINE_BUILT\n' + said('COMMAND_LINE_BUILT', M_BUILT) + '\nCOMMAND_LINE_BUILT\nCOMMAND_LINE_BUILT\n'},
     check={'errors': 0, 'found': []})

case('X06', 'L4', 'an invocation passes, by any way it reaches the door', f'''load "doors.haro"
sDoors = doors'{SHOW}'
func MakeCall(psDoors, ptText)
    return psDoors.Invocation("show", ["echo.haro", ptText])
end
hCall = sDoors.Invocation("show", ["echo.haro", "held by a name"])
print SystemCmd(hCall)
print SystemCmd(MakeCall(sDoors, "a function's answer"))
xAny = MakeCall(sDoors, "a name that may hold anything")
print SystemCmd(xAny)
print System(MakeCall(sDoors, "passed through"))
''', {'stdout': '[held by a name]\n[a function\'s answer]\n[a name that may hold anything]\n[passed through]\n0\n'}, check={'errors': 0, 'found': []})

# sharpened after the code, when the plants were written: System's line was a literal, so the .ring file's reading of a built
# command line was asked at one door only
case('X07', 'L5', 'a .ring file reads as it did: a built command line runs through the shell, at either door', '''cWord = "built"
see systemcmd("echo " + cWord) + nl
system("echo " + cWord)
''', {'stdout': 'built\nbuilt\n'}, ext='.ring')

case('X08', 'L5', 'a program\'s own function named System or SystemCmd is the program\'s', '''func SystemCmd(ptLine)
    return "mine: " + ptLine
end
func System(ptLine)
    print "also mine: " + ptLine
end
tWord = "built"
print SystemCmd("echo " + tWord)
System("echo " + tWord)
''', {'stdout': 'mine: echo built\nalso mine: echo built\n'})

REFUSED = "n (line 157): FRAME ledger_under: the surface 'ledger' refuses the query 'SELECT member FROM collect WHERE amount < {num}': z (line 1): Expected '*' after SELECT: a question asks for whole records (SELECT * only), found 'member'\n"
case('X09', 'L6', 'a court whose library holds a sentence of doors still judges, and asks its sibling court with no shell', '''# the court's own procedure: n/tontine.n with one ledger query its ledger's court refuses, judged by `n_court.haro check <file>
# surfaces` -- the answer is the sibling court's refusal, in its words, as it was before n_lib.haro held a sentence of doors
''', {'stdout': REFUSED}, kind='ncourt')

case('X10', 'L7', 'a sentence of doors is read once: its judges answer from what was read', f'''load "doors.haro"
sDoors = doors'{DATA}
{SHOW}'
for i = 1 to 40
    hNote = sDoors.Place("data", "note.txt")
    hCall = sDoors.Invocation("show", ["echo.haro", "again"])
end
print hNote
print hCall
print HaroDoorsReads()
''', {'stdout': 'data/note.txt\nshow echo.haro again\n1\n'}, kind=None)

doc = {'version': '0.75', 'task': 'a command line is not built as text (D88 (d)); Haro\'s own run of a program converted', 'languages': ['doors'], 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
