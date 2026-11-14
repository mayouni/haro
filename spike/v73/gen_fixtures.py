"""Haro v0.73, the command and the invocation (doc/DOORS.md rung 2, D88 (d)): the cases of v73/fixtures.json and their files, written
BEFORE the code. Every expectation is typed here. The spellings are this desk's, under D84: the kind COMMAND of the language of
doors (RUNS a program, or ITSELF yes for this haro; TAKES the shapes of its arguments; QUIET yes), the judge `Invocation`, the
refusals named below.

CHANGED AFTER THE COURT SPOKE, before the install, when stzlib's own lines were read (2a5b3ca7f: of its 10 lines that build a command
line, 6 change folder first and 7 want the exit code with everything the child writes sent away): V03 runs a command that is not
quiet; V15 expects System of a quiet command to print nothing of the child's; V20 and V21 are new (IN).

  python spike/v73/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  a sentence of doors declares commands; `sDoors.Invocation(command, vArguments)` answers an invocation: its command, its
      arguments as texts; it prints as its command and arguments; the letter h holds it; a sentence of another language judges none
  L2  `SystemCmd(hCall)` runs the program with no shell and answers what it wrote: an argument arrives as one argument, byte for
      byte, whatever a shell would read in it
  L3  `System(hCall)` runs it and answers its exit code; what the child writes passes through, after what the program wrote first
  L4  each argument is judged by its declared shape -- word, option, number, place, text, words -- or INVOCATION_SHAPE; the count
      of arguments is the declaration's, or INVOCATION_COUNT; `words` stands once in a command, or COMMAND_WORDS
  L5  a command the sentence does not declare is COMMAND_UNKNOWN, and the refusal names the ones it does
  L6  no shell: a command that runs a shell, or a file a shell reads, is COMMAND_SHELL
  L7  the declaration's court: a command that runs nothing (COMMAND_NOTHING), one that says RUNS and ITSELF (COMMAND_TWICE), a shape
      outside the six (UNKNOWN_SHAPE) -- each refused when the program is compiled, its verdict the standalone court's
  L8  ITSELF yes runs this haro; RUNS names a program found as the platform finds one; a program that cannot be started is
      COMMAND_NOT_STARTED
  L9  an invocation is made by its judge alone, and is not written into
  L10 QUIET yes: nothing the child writes reaches the program's output -- SystemCmd still answers what it wrote, System answers its
      exit code alone; without it, the child's standard error passes through, and under System its standard output too
  L11 a door still takes text as it did: the rung refuses nothing that ran
  L12 a forged court's folder is named by which haro forged it too: another haro at the same place forges its own
  L13 a command runs IN a root: the child's working folder is the root's folder, and a place it is given is given whole; a root
      that is not declared is the court's DANGLING, a root with no folder COMMAND_IN
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
FAIL = '''print "out"
FWrite(stderr, "said on its standard error" + Char(10))
Shutdown(3)
'''
WHERE = '''print FExists("note.txt")
print FExists(sysargv[3])
print Read(sysargv[3])
'''
for name, text in (('data/note.txt', 'hello'), ('echo.haro', ECHO), ('fail.haro', FAIL), ('where.haro', WHERE)):
    with open(os.path.join(CASES, *name.split('/')), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

SHOW = 'DEFINE COMMAND show AS (ITSELF yes, TAKES [word, text, text, text]) RATIONALE "this haro, printing what it is given"'
ALL = 'DEFINE COMMAND all AS (ITSELF yes, TAKES [word, option, number, place, words, text]) RATIONALE "one argument of each shape"'
FAILS = 'DEFINE COMMAND fails AS (ITSELF yes, TAKES [word]) RATIONALE "a child that ends with 3"'
HUSH = 'DEFINE COMMAND hush AS (ITSELF yes, TAKES [word], QUIET yes) RATIONALE "the same child, nothing it writes shown"'
DATA = 'DEFINE ROOT data AS (AT "data", ALLOWS [read]) RATIONALE "the notes this program reads"'


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, judged=None, check=None, kind=None):
    """run: {'stdout': text} exact with exit 0; {'raises': text} with 'never'; {'refuses': [row, reason, written]}; beside any of them
    'stderr': {'has': text, 'times': n} or {'never': text} for what the run writes to its standard error. judged: [[language, text, code or None,
    message]] for the law. check: {'errors': n, 'found': [[row, rule]]}. kind: 'identity' -- L12, the court's own procedure."""
    name = cid.lower() + '.haro'
    with open(os.path.join(CASES, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if judged is not None:
        c['judged'] = judged
    if check is not None:
        c['check'] = check
    if kind is not None:
        c['kind'] = kind
    cases.append(c)


case('V01', 'L1', 'a command declared, an invocation judged and held by an h name', f'''load "doors.haro"
sDoors = doors'{SHOW}'
hCall = sDoors.Invocation("show", ["echo.haro", "one", "two words", ""])
print hCall
print hCall.Command()
print Len(hCall.Arguments())
print hCall.Arguments()[3]
''', {'stdout': 'show echo.haro one "two words" ""\nshow\n4\ntwo words\n'}, judged=[['doors', SHOW, None, '']], check={'errors': 0, 'found': []})

case('V02', 'L2', 'no shell: each argument arrives as one argument, byte for byte, whatever a shell would read in it', f'''load "doors.haro"
sDoors = doors'{SHOW}'
tQuote = Char(34)
hCall = sDoors.Invocation("show", ["echo.haro", "two words & more | less > out.txt", "%PATH% $HOME `id` ; rm *", "say " + tQuote + "hi" + tQuote + " back" + Char(92)])
tOut = SystemCmd(hCall)
print tOut
print FExists("out.txt")
''', {'stdout': '[two words & more | less > out.txt]\n[%PATH% $HOME `id` ; rm *]\n[say "hi" back\\]\nfalse\n'})

case('V03', 'L3', '`System` of an invocation answers the exit code; what the child writes passes through, in order', f'''load "doors.haro"
sDoors = doors'{FAILS}'
print "before"
iCode = System(sDoors.Invocation("fails", ["fail.haro"]))
print iCode
''', {'stdout': 'before\nout\n3\n'})

case('V04', 'L4', 'each shape, rightly given: a word, an option, a number, a place, some words, a text', f'''load "doors.haro"
sDoors = doors'{ALL}
{DATA}'
hNote = sDoors.Place("data", "note.txt")
print SystemCmd(sDoors.Invocation("all", ["echo.haro", "--deep", 42, hNote, "a", "b,c", "d=1", "free text, as it is"]))
print SystemCmd(sDoors.Invocation("all", ["echo.haro", "-x", 2.5, hNote, "one", ""]))
''', {'stdout': '[--deep]\n[42]\n[data/note.txt]\n[a]\n[b,c]\n[d=1]\n[free text, as it is]\n[-x]\n[2.5]\n[data/note.txt]\n[one]\n[]\n'})

# the last three of vBad were added after the code, when the plants were written: a number given where a word, an option or a
# text stands had no line of its own
case('V05', 'L4', 'an argument that is not its shape is INVOCATION_SHAPE, and says which', f'''load "doors.haro"
sDoors = doors'{ALL}
{DATA}'
hNote = sDoors.Place("data", "note.txt")
vGood = ["echo.haro", "--deep", 42, hNote, "a", "free"]
vBad = [[1, "two words"], [1, "-rf"], [1, ""], [2, "deep"], [2, "--a b"], [3, "42"], [4, "data/note.txt"], [5, "a b"], [6, "-o"], [6, "a" + Char(10) + "b"], [1, 7], [2, 7], [6, 7]]
for i = 1 to Len(vBad)
    vArgs = []
    for k = 1 to Len(vGood)
        if k = vBad[i][1]
            vArgs + vBad[i][2]
        else
            vArgs + vGood[k]
        end
    end
    try
        hAny = sDoors.Invocation("all", vArgs)
        print "judged"
    catch e
        print e.Message()
    end
end
try
    hAny = sDoors.Invocation("all", "echo.haro")
catch e
    print e.Message()
end
''', {'stdout': ''.join(said('INVOCATION_SHAPE', 'argument ' + str(n) + ' of `all` is no ' + shape) + '\n' for n, shape in
                        ((1, 'word'), (1, 'word'), (1, 'word'), (2, 'option'), (2, 'option'), (3, 'number'), (4, 'place'), (5, 'word'),
                         (6, 'text'), (6, 'text'), (1, 'word'), (2, 'option'), (6, 'text')))
      + said('INVOCATION_SHAPE', 'the arguments of `all` are given as a vector') + '\n'})

case('V06', 'L4', 'the count of arguments is the declaration\'s: INVOCATION_COUNT', f'''load "doors.haro"
sDoors = doors'{SHOW}
{ALL}
{DATA}'
hNote = sDoors.Place("data", "note.txt")
vTries = [["show", ["echo.haro", "a"]], ["show", ["echo.haro", "a", "b", "c", "d"]], ["all", ["echo.haro", "--deep", 42, hNote, "free"]]]
for i = 1 to Len(vTries)
    try
        hAny = sDoors.Invocation(vTries[i][1], vTries[i][2])
        print "judged"
    catch e
        print e.Message()
    end
end
''', {'stdout': said('INVOCATION_COUNT', '`show` takes 4 arguments, and is given 2') + '\n'
      + said('INVOCATION_COUNT', '`show` takes 4 arguments, and is given 5') + '\n'
      + said('INVOCATION_COUNT', '`all` takes at least 6 arguments, and is given 5') + '\n'})

case('V07', 'L5', 'a command the sentence does not declare is COMMAND_UNKNOWN, and names the ones it does', f'''load "doors.haro"
sDoors = doors'{SHOW}
{FAILS}
{DATA}'
try
    hAny = sDoors.Invocation("format", ["c"])
    print "judged"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'COMMAND_UNKNOWN\n' + said('COMMAND_UNKNOWN', 'no command called `format` is declared here; the commands are show, fails') + '\n'},
     judged=[['doors', SHOW + '\n' + FAILS + '\n' + DATA, None, '']])

SHELLS = [('a', 'cmd'), ('b', 'sh'), ('c', '/bin/bash'), ('d', 'PowerShell.exe'), ('e', 'tools/run.bat'), ('f', 'build.CMD'), ('g', 'go.sh')]
SHELL_DECLS = '\n'.join(f'DEFINE COMMAND {n} AS (RUNS "{p}", TAKES [text]) RATIONALE "x"' for n, p in SHELLS)
case('V08', 'L6', 'no shell: a command that runs a shell, or a file a shell reads, is COMMAND_SHELL', f'''load "doors.haro"
sDoors = doors'{SHELL_DECLS}'
vNames = ["a", "b", "c", "d", "e", "f", "g"]
for i = 1 to Len(vNames)
    try
        hAny = sDoors.Invocation(vNames[i], ["dir"])
        print "judged"
    catch e
        print e.Code()
    end
end
try
    hAny = sDoors.Invocation("c", ["dir"])
catch e
    print e.Message()
end
''', {'stdout': 'COMMAND_SHELL\n' * 7 + said('COMMAND_SHELL', 'the command `c` runs a shell, `/bin/bash`: a command is a program and its arguments') + '\n'})

NOTHING = 'DEFINE COMMAND a AS (TAKES [word]) RATIONALE "x"'
M_NOTHING = 'COMMAND a runs nothing: give it RUNS, or say ITSELF for this haro'
case('V09', 'L7', 'a command that runs nothing is refused when the program is compiled', f'''load "doors.haro"
print "before"
sDoors = doors'{NOTHING}'
''', {'refuses': [3, 'the court of doors refuses this literal -- COMMAND_NOTHING: ' + M_NOTHING + '; written', "'" + NOTHING + "'"], 'never': 'before'},
     judged=[['doors', NOTHING, 'COMMAND_NOTHING', M_NOTHING],
             ['doors', 'DEFINE COMMAND b AS (ITSELF yes, RUNS "x") RATIONALE "x"', 'COMMAND_TWICE', 'COMMAND b says ITSELF and RUNS: it is one or the other'],
             ['doors', 'DEFINE COMMAND c AS (RUNS "x", TAKES [word, line]) RATIONALE "x"', 'UNKNOWN_SHAPE',
              "An argument is a word, an option, a number, a place, a text or words, not 'line'"]],
     check={'errors': 1, 'found': [[3, RULE]]})

BYNAME = 'DEFINE COMMAND other AS (RUNS "haro", TAKES [word, text]) RATIONALE "a haro found as the platform finds a program"'
case('V10', 'L8', 'RUNS names a program found as the platform finds one', f'''load "doors.haro"
sDoors = doors'{BYNAME}'
hCall = sDoors.Invocation("other", ["echo.haro", "found by name"])
print hCall
print SystemCmd(hCall)
''', {'stdout': 'other echo.haro "found by name"\n[found by name]\n'})

ABSENT = 'DEFINE COMMAND gone AS (RUNS "no-such-program-of-haro-v73", TAKES [word]) RATIONALE "a program that is not there"'
case('V11', 'L8', 'a program that cannot be started is COMMAND_NOT_STARTED, at either door', f'''load "doors.haro"
sDoors = doors'{ABSENT}'
hCall = sDoors.Invocation("gone", ["x"])
try
    print SystemCmd(hCall)
catch e
    print e.Message()
end
try
    print System(hCall)
catch e
    print e.Code()
end
''', {'stdout': said('COMMAND_NOT_STARTED', 'the command `gone` runs `no-such-program-of-haro-v73`, which could not be started') + '\nCOMMAND_NOT_STARTED\n'})

FAKE = 'new HaroInvocation("show", false, "show", ["cmd", "/c", "dir"])'
case('V12', 'L9', 'an invocation is made by its judge alone: `new` of one is refused when compiling', f'''load "doors.haro"
xFake = {FAKE}
print "made"
''', {'refuses': [2, 'an invocation is made by its judge -- <doors>.Invocation(command, arguments); written', FAKE], 'never': 'made'},
     check={'errors': 1, 'found': [[2, RULE]]})

case('V13', 'L9', 'a write into an invocation is refused, and it is what it was', f'''load "doors.haro"
sDoors = doors'{SHOW}'
hCall = sDoors.Invocation("show", ["echo.haro", "a", "b", "c"])
try
    hCall.vArgv = ["cmd", "/c", "dir"]
    print "written"
catch e
    print e.Code()
end
print hCall
''', {'stdout': 'INVOCATION_FIXED\nshow echo.haro a b c\n'})

# `times` was added after the code, when the plants were written: one door passing the line through hid the other dropping it
case('V14', 'L10', 'without QUIET what the child writes to its standard error passes through, at either door', f'''load "doors.haro"
sDoors = doors'{FAILS}'
print SystemCmd(sDoors.Invocation("fails", ["fail.haro"]))
print System(sDoors.Invocation("fails", ["fail.haro"]))
''', {'stdout': 'out\nout\n3\n', 'stderr': {'has': 'said on its standard error', 'times': 2}})

case('V15', 'L10', 'QUIET yes: nothing the child writes reaches the program\'s output; System answers the exit code alone', f'''load "doors.haro"
sDoors = doors'{HUSH}'
print SystemCmd(sDoors.Invocation("hush", ["fail.haro"]))
print System(sDoors.Invocation("hush", ["fail.haro"]))
''', {'stdout': 'out\n3\n', 'stderr': {'never': 'said on its standard error'}})

case('V16', 'L11', 'a door still takes text as it did: a literal and a built command line run through the shell', '''tWord = "built"
print SystemCmd("echo literal")
print SystemCmd("echo " + tWord)
print System("echo passed")
''', {'stdout': 'literal\nbuilt\npassed\n0\n'}, check={'errors': 0, 'found': []})

LAMP = 'DEFINE LAMP north AS (SHOWS green) RATIONALE "x"'
case('V17', 'L1', 'an invocation is judged by a sentence of doors: a sentence of another language answers INVOCATION_NO_DOORS', f'''load "doors.haro"
load "../../v70/cases/signal.haro"
sLamp = signal'{LAMP}'
try
    hAny = sLamp.Invocation("show", [])
    print "judged"
catch e
    print e.Message()
end
''', {'stdout': said('INVOCATION_NO_DOORS', 'an invocation is judged by a sentence of doors, and this is a sentence of signal') + '\n'})

case('V18', 'L12', 'a forged court\'s folder is named by which haro forged it: another haro at the same place forges its own', f'''load "doors.haro"
sDoors = doors'{SHOW}'
print sDoors.Invocation("show", ["echo.haro", "a", "b", "c"])
''', {'stdout': 'show echo.haro a b c\n'}, kind='identity')

TWICE = 'DEFINE COMMAND two AS (ITSELF yes, TAKES [word, words, text, words]) RATIONALE "two runs of words"'
case('V19', 'L4', 'a command that takes `words` twice has no one reading: COMMAND_WORDS', f"""load "doors.haro"
sDoors = doors'{TWICE}'
try
    hAny = sDoors.Invocation("two", ["echo.haro", "a", "b", "c", "d"])
    print "judged"
catch e
    print e.Message()
end
""", {'stdout': said('COMMAND_WORDS', 'the command `two` takes words twice: one run of words has a place') + '\n'})

INSIDE = 'DEFINE COMMAND inside AS (ITSELF yes, TAKES [text, place], IN data) RATIONALE "this haro, run in the folder of the notes"'
GIVEN = 'DEFINE ROOT given AS (ANYWHERE yes) RATIONALE "the file a person names"'
NOFOLDER = 'DEFINE COMMAND loose AS (ITSELF yes, TAKES [word], IN given) RATIONALE "a command in a root that has no folder"'
case('V20', 'L13', 'a command runs IN a root: the child stands in the root\'s folder, and a place it is given is given whole', f"""load "doors.haro"
sDoors = doors'{DATA}
{INSIDE}'
hCall = sDoors.Invocation("inside", ["../where.haro", sDoors.Place("data", "note.txt")])
print hCall.In()
print SystemCmd(hCall)
print System(hCall)
""", {'stdout': 'data\ntrue\ntrue\nhello\ntrue\ntrue\nhello\n0\n'}, judged=[['doors', DATA + '\n' + INSIDE, None, '']])

DANGLES = 'DEFINE COMMAND adrift AS (ITSELF yes, TAKES [word], IN nowhere) RATIONALE "x"'
case('V21', 'L13', 'IN names a root that has a folder: a root with none is COMMAND_IN; one not declared is the court\'s DANGLING', f"""load "doors.haro"
sDoors = doors'{GIVEN}
{NOFOLDER}'
try
    hAny = sDoors.Invocation("loose", ["x"])
    print "judged"
catch e
    print e.Message()
end
""", {'stdout': said('COMMAND_IN', 'the command `loose` runs in the root `given`, which has no folder') + '\n'},
     judged=[['doors', DANGLES, 'DANGLING', "adrift IN 'nowhere', which resolves to nothing: no such ROOT"]])

doc = {'version': '0.73', 'task': 'doc/DOORS.md rung 2: the command and the invocation', 'languages': ['doors'],
       'law': 'the verdict on a sentence of doors is the one its own forged court answers, standing alone, on the same text', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
