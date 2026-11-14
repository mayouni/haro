"""Haro v0.72, the language of doors and the place (doc/DOORS.md rung 1, D88): the cases of v72/fixtures.json and their files, written
BEFORE the code. Every expectation is typed here. The spellings are this desk's, under D84: the standard language `doors`, its kind
ROOT (AT a folder, or ANYWHERE yes; ALLOWS read, write, list, remove), the judge `Place`, the refusals named below.

  python spike/v72/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  `load "doors.haro"` is Haro's standard language of doors, found wherever the program stands; a sentence of it declares roots
  L2  `sDoors.Place(root, text)` answers a place: its root, its path beneath the root made plain, what the root allows; it prints
      as its path; the letter h holds it; a sentence of another language judges none
  L3  a text that leaves its root is PLACE_ESCAPES; a name a place cannot hold is PLACE_NAME
  L4  a root the sentence does not declare is ROOT_UNKNOWN
  L5  a root ANYWHERE takes the file a person names, wherever it is, and reads only
  L6  the declaration's court: a root with no folder that does not say ANYWHERE, one that says both, one ANYWHERE that lists what it
      allows, a permission outside the four -- each refused when the program is compiled, its verdict the standalone court's
  L7  a door takes a place: Read, FExists, Write, Remove and Dir, each allowed by the root or PLACE_NOT_ALLOWED
  L8  the door checks again where it opens: a link beneath the root that leads out of it is PLACE_ESCAPES at the door
  L9  a place is made by its judge alone, and is not written into
  L10 a door still takes text as it did: nothing that ran is refused by this rung
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []
RULE = 'haro/refused-form'
CASES = os.path.join(HERE, 'cases')
for d in ('data', os.path.join('data', 'sub'), 'out', 'own'):
    os.makedirs(os.path.join(CASES, d), exist_ok=True)
for name, text in (('data/note.txt', 'hello'), ('data/sub/inner.txt', 'inner'), ('secret.txt', 'outside the root'), ('out/.keep', ''),
                   ('own/doors.haro', 'print "a file of the program"\n')):
    with open(os.path.join(CASES, *name.split('/')), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

DATA = 'DEFINE ROOT data AS (AT "data", ALLOWS [read, list]) RATIONALE "the notes this program reads"'
OUT = 'DEFINE ROOT out AS (AT "out", ALLOWS [read, write, remove]) RATIONALE "what this program makes"'
GIVEN = 'DEFINE ROOT given AS (ANYWHERE yes) RATIONALE "the file a person names"'


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, judged=None, check=None, setup=None):
    """run: {'stdout': text} exact with exit 0; {'raises': text} with 'never'; {'refuses': [row, reason, written]}. judged: [[language,
    text, code or None, message]] for the law. check: {'errors': n, 'found': [[row, rule]]}. setup: 'link' -- the court makes, beneath
    cases/data, a link named `way_out` that leads to cases/ itself, and takes it away after."""
    name = cid.lower() + '.haro'
    with open(os.path.join(CASES, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if judged is not None:
        c['judged'] = judged
    if check is not None:
        c['check'] = check
    if setup is not None:
        c['setup'] = setup
    cases.append(c)


case('D01', 'L1', 'the standard language loaded, a root declared, a place judged and held by an h name', f'''load "doors.haro"
sDoors = doors'{DATA}'
hNote = sDoors.Place("data", "note.txt")
print hNote
print hNote.Root()
print hNote.Path()
print Len(hNote.Allows())
''', {'stdout': 'data/note.txt\ndata\ndata/note.txt\n2\n'}, judged=[['doors', DATA, None, '']], check={'errors': 0, 'found': []})

case('D02', 'L2', 'the path made plain: a folder beneath, a dot, a step back inside the root, either slash', f'''load "doors.haro"
sDoors = doors'{DATA}'
print sDoors.Place("data", "sub/inner.txt")
print sDoors.Place("data", "sub/./deep/../inner.txt")
print sDoors.Place("data", "sub" + Char(92) + "inner.txt")
print sDoors.Place("data", "./note.txt")
''', {'stdout': 'data/sub/inner.txt\ndata/sub/inner.txt\ndata/sub/inner.txt\ndata/note.txt\n'})

case('D03', 'L3', 'a text that leaves its root is PLACE_ESCAPES: a step back out, a rooted path, a drive, a share, a scheme', f'''load "doors.haro"
sDoors = doors'{DATA}'
vTexts = ["../secret.txt", "sub/../../secret.txt", "/etc/passwd", "C:/Windows/win.ini", Char(92) + Char(92) + "server" + Char(92) + "share", "file://note.txt"]
for i = 1 to Len(vTexts)
    try
        hAny = sDoors.Place("data", vTexts[i])
        print "placed"
    catch e
        print e.Code()
    end
end
try
    hAny = sDoors.Place("data", "../secret.txt")
catch e
    print e.Message()
end
''', {'stdout': 'PLACE_ESCAPES\n' * 6 + said('PLACE_ESCAPES', '`../secret.txt` leaves the root `data`') + '\n'})

case('D04', 'L3', 'a name a place cannot hold is PLACE_NAME: nothing, a control byte, a device, a trailing dot or blank, a stream', f'''load "doors.haro"
sDoors = doors'{DATA}'
vTexts = ["", "a" + Char(7) + "b", "con", "sub/NUL.txt", "name.", "name ", "note.txt:hidden"]
for i = 1 to Len(vTexts)
    try
        hAny = sDoors.Place("data", vTexts[i])
        print "placed"
    catch e
        print e.Code()
    end
end
try
    hAny = sDoors.Place("data", "name.")
catch e
    print e.Message()
end
''', {'stdout': 'PLACE_NAME\n' * 7 + said('PLACE_NAME', '`name.` is no name a place can hold') + '\n'})

case('D05', 'L4', 'a root the sentence does not declare is ROOT_UNKNOWN, and names the ones it does', f'''load "doors.haro"
sDoors = doors'{DATA}
{OUT}'
try
    hAny = sDoors.Place("nowhere", "note.txt")
    print "placed"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'ROOT_UNKNOWN\n' + said('ROOT_UNKNOWN', 'no root called `nowhere` is declared here; the roots are data, out') + '\n'},
     judged=[['doors', DATA + '\n' + OUT, None, '']])

case('D06', 'L5', 'a root ANYWHERE takes the file a person names, wherever it is, and reads only', f'''load "doors.haro"
sDoors = doors'{GIVEN}'
hFar = sDoors.Place("given", "C:/some/where/else.txt")
print hFar
hNear = sDoors.Place("given", "data/../data/note.txt")
print hNear
print hNear.Allows()[1]
print Len(hNear.Allows())
try
    hAny = sDoors.Place("given", "name.")
catch e
    print e.Code()
end
''', {'stdout': 'C:/some/where/else.txt\ndata/note.txt\nread\n1\nPLACE_NAME\n'}, judged=[['doors', GIVEN, None, '']])

NOWHERE = 'DEFINE ROOT a AS (ALLOWS [read]) RATIONALE "x"'
M_NOWHERE = 'ROOT a names no folder: give it AT, or say ANYWHERE for the files a person names'
case('D07', 'L6', 'a root with no folder that does not say ANYWHERE is refused when the program is compiled', f'''load "doors.haro"
print "before"
sDoors = doors'{NOWHERE}'
''', {'refuses': [3, 'the court of doors refuses this literal -- ROOT_NOWHERE: ' + M_NOWHERE + '; written', "'" + NOWHERE + "'"], 'never': 'before'},
     judged=[['doors', NOWHERE, 'ROOT_NOWHERE', M_NOWHERE],
             ['doors', 'DEFINE ROOT b AS (ANYWHERE yes, AT "x") RATIONALE "x"', 'ROOT_TWICE', 'ROOT b says ANYWHERE and AT: it is one or the other'],
             ['doors', 'DEFINE ROOT c AS (ANYWHERE yes, ALLOWS [write]) RATIONALE "x"', 'ROOT_ANYWHERE_READS',
              'ROOT c is ANYWHERE and lists what it allows: a root with no folder reads, and nothing more'],
             ['doors', 'DEFINE ROOT d AS (AT "x", ALLOWS [execute]) RATIONALE "x"', 'UNKNOWN_PERMISSION',
              "A root allows read, write, list or remove, not 'execute'"]],
     check={'errors': 1, 'found': [[3, RULE]]})

case('D08', 'L7', 'a door takes a place: Read, FExists and Dir beneath a root that allows them', f'''load "doors.haro"
sDoors = doors'{DATA}'
hNote = sDoors.Place("data", "note.txt")
print Read(hNote)
print FExists(hNote)
print FExists(sDoors.Place("data", "absent.txt"))
print Len(Dir(sDoors.Place("data", "sub")))
''', {'stdout': 'hello\ntrue\nfalse\n1\n'}, check={'errors': 0, 'found': []})

case('D09', 'L7', 'a door the root does not allow is PLACE_NOT_ALLOWED, and nothing is done', f'''load "doors.haro"
sDoors = doors'{DATA}'
hNote = sDoors.Place("data", "note.txt")
try
    Write(hNote, "changed")
    print "written"
catch e
    print e.Code()
    print e.Message()
end
try
    Remove(hNote)
    print "removed"
catch e
    print e.Code()
end
print Read(hNote)
''', {'stdout': 'PLACE_NOT_ALLOWED\n' + said('PLACE_NOT_ALLOWED', 'the root `data` does not allow write') + '\nPLACE_NOT_ALLOWED\nhello\n'})

case('D10', 'L7', 'beneath a root that allows them: Write, Read, Remove', f'''load "doors.haro"
sDoors = doors'{OUT}'
hMade = sDoors.Place("out", "made.txt")
Write(hMade, "made")
print Read(hMade)
Remove(hMade)
print FExists(hMade)
''', {'stdout': 'made\nfalse\n'})

case('D11', 'L8', 'the door checks again where it opens: a link beneath the root that leads out of it', f'''load "doors.haro"
sDoors = doors'{DATA}'
hOut = sDoors.Place("data", "way_out/secret.txt")
print hOut
try
    print Read(hOut)
catch e
    print e.Code()
end
''', {'stdout': 'data/way_out/secret.txt\nPLACE_ESCAPES\n'}, setup='link')

FAKE = 'new HaroPlace("data", "data", "secret.txt", ["read"])'
case('D12', 'L9', 'a place is made by its judge alone: `new` of one is refused when compiling', f'''load "doors.haro"
xFake = {FAKE}
print "made"
''', {'refuses': [2, 'a place is made by its judge -- <doors>.Place(root, text); written', FAKE], 'never': 'made'},
     check={'errors': 1, 'found': [[2, RULE]]})

case('D13', 'L9', 'a write into a place is refused, and the place is what it was', f'''load "doors.haro"
sDoors = doors'{DATA}'
hNote = sDoors.Place("data", "note.txt")
try
    hNote.tPath = "secret.txt"
    print "written"
catch e
    print e.Code()
end
print hNote
''', {'stdout': 'PLACE_FIXED\ndata/note.txt\n'})

case('D14', 'L10', 'a door still takes text as it did', '''tName = "data/" + "note.txt"
print Read("data/note.txt")
print Read(tName)
print FExists(tName)
''', {'stdout': 'hello\nhello\ntrue\n'}, check={'errors': 0, 'found': []})

LAMP = 'DEFINE LAMP north AS (SHOWS green) RATIONALE "x"'
# added after the code, when the plants were written: the judge's first refusal had no case of its own
case('D15', 'L2', 'a place is judged by a sentence of doors: a sentence of another language answers PLACE_NO_DOORS', f'''load "doors.haro"
load "../../v70/cases/signal.haro"
sLamp = signal'{LAMP}'
try
    hAny = sLamp.Place("data", "note.txt")
    print "placed"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'PLACE_NO_DOORS\n' + said('PLACE_NO_DOORS', 'a place is judged by a sentence of doors, and this is a sentence of signal') + '\n'})

DROP = 'DEFINE ROOT drop AS (AT "out", ALLOWS [write]) RATIONALE "what is left here and not read back"'
# added after the code, when the plants were written: no root of the cases withheld read or list, DirExists stood in no case, and a
# scheme under a root ANYWHERE was typed nowhere
case('D16', 'L7', 'each door asks its own permission: Dir asks list, Read and FExists ask read; DirExists takes a place', f"""load "doors.haro"
sDoors = doors'{DATA}
{OUT}
{DROP}
{GIVEN}'
print DirExists(sDoors.Place("data", "sub"))
print DirExists(sDoors.Place("data", "absent"))
try
    Dir(sDoors.Place("out", "."))
    print "listed"
catch e
    print e.Message()
end
try
    print Read(sDoors.Place("drop", ".keep"))
catch e
    print e.Message()
end
try
    print FExists(sDoors.Place("drop", ".keep"))
catch e
    print e.Code()
end
try
    hAny = sDoors.Place("given", "file://note.txt")
    print "placed"
catch e
    print e.Code()
end
""", {'stdout': 'true\nfalse\n' + said('PLACE_NOT_ALLOWED', 'the root `out` does not allow list') + '\n'
      + said('PLACE_NOT_ALLOWED', 'the root `drop` does not allow read') + '\nPLACE_NOT_ALLOWED\nPLACE_NAME\n'})

# added after the code, when the plants were written: the compiler's look in the forge's folder failed no case, because a load is
# also matched by the end of its name; here two loaded files end alike, and each load must find its own
case('D17', 'L1', 'the standard language is found by where it stands: a file of its name in a folder of the program is another file', f"""load "own/doors.haro"
load "doors.haro"
sDoors = doors'{DATA}'
print sDoors.Place("data", "note.txt")
""", {'stdout': 'a file of the program\ndata/note.txt\n'})

# added after the code, likewise: the report of a load that cannot be opened read the loaded declaration as code
case('D18', 'L1', 'a declaration a program loads is no code: a load that cannot be opened is reported for itself alone', """load "doors.haro"
load "absent.haro"
print "ran"
""", {'raises': "Can't open file absent.haro", 'also': 'd18.haro errors count : 1', 'never': 'ran'})

doc = {'version': '0.72', 'task': 'doc/DOORS.md rung 1: the language of doors and the place', 'languages': ['doors'],
       'law': 'the verdict on a sentence of doors is the one its own forged court answers, standing alone, on the same text', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
