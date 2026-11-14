"""Haro v0.74, a folder made and a run answered whole (doc/DOORS.md rung 2's two debts, HF-179): the cases of v74/fixtures.json and their
files, written BEFORE the code. Every expectation is typed here. The spellings are this desk's, under D84, chosen after reading the
lines they serve on stzlib 2a5b3ca7f: `MakeDir` is the name stzlib's own function bears (core/common/stkRingStdFuncs.haro, which runs
the shell's mkdir; 100 calls in its .ring files), so its function gives way to the built-in by being taken out; and one line of it
(base/test/neural/_measure_screen_formats.haro 189) reads the exit code and the output of one run.

  python spike/v74/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  `MakeDir(tPath)` makes the folder and the folders above it that are missing; a folder that stands is left as it is
  L2  `MakeDir(hPlace)` takes a place: its root allows write, or PLACE_NOT_ALLOWED and nothing is made
  L3  the door checks again where it opens: a place that leads out of its root through a link is PLACE_ESCAPES, and nothing is made
  L4  a folder that cannot be made is FOLDER_NOT_MADE; what is neither a text nor a place is a bad parameter
  L5  a program's own function named MakeDir is the program's; a .ring file reads the name as it did
  L6  `hCall.Run()` runs the invocation with no shell and answers a record: `iCode` the exit code, `tOutput` what the child wrote,
      `tErrors` what it wrote to its standard error -- the last line end of each dropped; nothing of the child's reaches the
      program's output; the child stands where the command says (IN)
  L7  a program that cannot be started is COMMAND_NOT_STARTED
  L8  the door beneath is the judging library's alone: `SystemRun` written in a program is refused when compiling
  L9  `haro check` reads no error where MakeDir and Run are written rightly
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []
RULE = 'haro/refused-form'
CASES = os.path.join(HERE, 'cases')
for d in ('data', 'outside'):
    os.makedirs(os.path.join(CASES, d), exist_ok=True)
FAIL = '''print "out"
print "more"
FWrite(stderr, "said on its standard error" + Char(10))
Shutdown(3)
'''
WHERE = '''print FExists("note.txt")
'''
for name, text in (('data/note.txt', 'hello'), ('outside/.keep', ''), ('fail.haro', FAIL), ('where.haro', WHERE)):
    with open(os.path.join(CASES, *name.split('/')), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

MADE = 'DEFINE ROOT made AS (AT "made", ALLOWS [read, write]) RATIONALE "what this program makes"'
DATA = 'DEFINE ROOT data AS (AT "data", ALLOWS [read]) RATIONALE "the notes this program reads"'
FAILS = 'DEFINE COMMAND fails AS (ITSELF yes, TAKES [word]) RATIONALE "a child that ends with 3"'
INSIDE = 'DEFINE COMMAND inside AS (ITSELF yes, TAKES [text], IN data) RATIONALE "this haro, run in the folder of the notes"'
ABSENT = 'DEFINE COMMAND gone AS (RUNS "no-such-program-of-haro-v74", TAKES [word]) RATIONALE "a program that is not there"'


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, check=None, setup=None, ext='.haro'):
    """run: {'stdout': text} exact with exit 0; {'raises': text} with 'never'; {'refuses': [row, reason, written]}; beside any of them
    'stderr': {'never': text}. check: {'errors': n, 'found': [[row, rule]]}. setup: 'link' -- the court makes, beneath cases/made, a
    link named `way_out` that leads to cases/outside, and takes it away after. Before every case the court makes cases/made empty."""
    name = cid.lower() + ext
    with open(os.path.join(CASES, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if check is not None:
        c['check'] = check
    if setup is not None:
        c['setup'] = setup
    cases.append(c)


case('W01', 'L1', 'MakeDir makes the folder and the folders above it; one that stands is left as it is', '''print DirExists("made/a/b/c")
MakeDir("made/a/b/c")
print DirExists("made/a/b/c")
Write("made/a/b/c/kept.txt", "kept")
MakeDir("made/a/b/c")
MakeDir("made/a")
print Read("made/a/b/c/kept.txt")
''', {'stdout': 'false\ntrue\nkept\n'}, check={'errors': 0, 'found': []})

case('W02', 'L2', 'MakeDir takes a place: beneath a root that allows write it is made; beneath one that does not, PLACE_NOT_ALLOWED', f'''load "doors.haro"
sDoors = doors'{MADE}
{DATA}'
MakeDir(sDoors.Place("made", "x/y"))
print DirExists("made/x/y")
try
    MakeDir(sDoors.Place("data", "new"))
    print "made"
catch e
    print e.Message()
end
print DirExists("data/new")
''', {'stdout': 'true\n' + said('PLACE_NOT_ALLOWED', 'the root `data` does not allow write') + '\nfalse\n'}, check={'errors': 0, 'found': []})

case('W03', 'L3', 'the door checks again where it opens: a link beneath the root that leads out of it', f'''load "doors.haro"
sDoors = doors'{MADE}'
hOut = sDoors.Place("made", "way_out/new")
print hOut
try
    MakeDir(hOut)
    print "made"
catch e
    print e.Code()
end
print DirExists("outside/new")
''', {'stdout': 'made/way_out/new\nPLACE_ESCAPES\nfalse\n'}, setup='link')

case('W04', 'L4', 'a folder that cannot be made is FOLDER_NOT_MADE: a file stands where a folder would', '''try
    MakeDir("data/note.txt/under")
    print "made"
catch e
    print e.Code()
    print e.Message()
end
try
    MakeDir("data/note.txt")
    print "made"
catch e
    print e.Code()
end
print Read("data/note.txt")
''', {'stdout': 'FOLDER_NOT_MADE\n' + said('FOLDER_NOT_MADE', 'the folder `data/note.txt/under` could not be made') + '\nFOLDER_NOT_MADE\nhello\n'})

case('W05', 'L4', 'what is neither a text nor a place is a bad parameter', '''print "before"
MakeDir(7)
print "after"
''', {'raises': 'Bad parameter type!', 'never': 'after'})

case('W06', 'L5', 'a program\'s own function named MakeDir is the program\'s', '''func MakeDir(ptPath)
    print "mine: " + ptPath
end
MakeDir("made/never")
print DirExists("made/never")
''', {'stdout': 'mine: made/never\nfalse\n'})

case('W07', 'L5', 'a .ring file reads the name as it did: no built-in', '''see "before" + nl
makedir("made/never")
see "after" + nl
''', {'raises': 'Error (R3) : Calling Function without definition: makedir', 'never': 'after'}, ext='.ring')

case('W08', 'L6', 'Run answers a record: the exit code, what the child wrote, what it wrote to its standard error', f'''load "doors.haro"
sDoors = doors'{FAILS}'
hCall = sDoors.Invocation("fails", ["fail.haro"])
print "before"
rRun = hCall.Run()
print rRun.iCode
print "[" + rRun.tOutput + "]"
print "[" + rRun.tErrors + "]"
''', {'stdout': 'before\n3\n[out\nmore]\n[said on its standard error]\n', 'stderr': {'never': 'said on its standard error'}},
     check={'errors': 0, 'found': []})

case('W09', 'L6', 'the child stands where the command says, and a child that ends well answers 0', f'''load "doors.haro"
sDoors = doors'{DATA}
{INSIDE}'
rRun = sDoors.Invocation("inside", ["../where.haro"]).Run()
print rRun.iCode
print rRun.tOutput
print rRun.tErrors = ""
''', {'stdout': '0\ntrue\ntrue\n'})

case('W10', 'L7', 'a program that cannot be started is COMMAND_NOT_STARTED', f'''load "doors.haro"
sDoors = doors'{ABSENT}'
try
    rRun = sDoors.Invocation("gone", ["x"]).Run()
    print "ran"
catch e
    print e.Message()
end
''', {'stdout': said('COMMAND_NOT_STARTED', 'the command `gone` runs `no-such-program-of-haro-v74`, which could not be started') + '\n'})

DOOR = 'SystemRun(hCall)'
case('W11', 'L8', 'the door beneath is the judging library\'s alone: SystemRun written in a program is refused when compiling', f'''load "doors.haro"
sDoors = doors'{FAILS}'
hCall = sDoors.Invocation("fails", ["fail.haro"])
vGot = {DOOR}
print "ran"
''', {'refuses': [4, 'a run is asked of its invocation -- hCall.Run(); written', DOOR], 'never': 'ran'},
     check={'errors': 1, 'found': [[4, RULE]]})

case('W12', 'L8', 'the door beneath, given what is no invocation, has nothing to run and says so', '''see "before" + nl
systemrun("dir")
see "after" + nl
''', {'raises': 'Error (RUN_TAKES_INVOCATION) : a run is asked of an invocation -- hCall.Run()', 'never': 'after'}, ext='.ring')

doc = {'version': '0.74', 'task': 'a folder made and a run answered whole: the two debts of DOORS.md rung 2', 'languages': ['doors'], 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
