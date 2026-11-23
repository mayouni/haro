"""Haro v0.78, the fixtures, written before any code: three findings of the desks.

  X   HARO-COMPILE-EXIT-01 (stzlib-security; ruled for the Principal on his delegation of 2026-11-17): a compile that fails,
      for memory or for any other reason, ends haro.exe with a non-zero exit code. Read on the installed v0.77 first: under a
      memory limit of 80 MB a program of 6,000 functions prints `compile failed: OutOfMemory` and ends with 0.
  L   HARO-LIBIMAGE-01 (stzlib-general): the library compiled once and kept (`haro prefix <library>`), a root whose first
      statement loads it compiled on top. In the VM since the fork, and held by no stage until this one. Four things are new:
      the path a run took is said after the compile (HARO_PATH); a root's image is neither used nor written when asked
      (HARO_NOIMAGE); the usage text names `prefix`; and this court.
  R   HARO-INVOCATION-STDIN-01 (stzradar): an invocation whose child reads its standard input from a place --
      `rRun = hCall.RunReading(hPlace)`.

The spellings are this desk's, chosen with these fixtures under D84 (delegated):

  exit code 1            a failed compile, as every other way a program does not complete already ends (a raise, a refused
                         statement, a file that does not scan, a load that names no file)
  HARO_PATH=1            one line on the standard error, after the compile and before the program's first statement:
                           path: kept library
                           path: kept image
                           path: whole
                           path: whole, the kept library does not apply (<name>)
                           path: whole, the kept library is stale
  HARO_NOIMAGE=1         a root's own image is neither used nor written; a kept library is taken as it is without the setting
  hCall.RunReading(h)    Run, with the file at the place as the child's standard input; the place's root allows read
                           RUN_INPUT        what is given is no place
                           INPUT_NOT_READ   the place names a file that could not be read

  python spike/v78/gen_fixtures.py     writes fixtures.json and cases/
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, 'cases')


def put(rel, text):
    p = os.path.join(CASES, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


# ---------------------------------------------------------------------------------------------- L: a library and its roots
put('lib/lib.haro', '''print "the library is loaded"

func Twice(iN)
	return iN * 2
end

func Greet(tName)
	return "hello, " + tName
end

class Counter
	iCount = 0

	def Add(iN)
		iCount = iCount + iN
		return this
	end

	def Total
		return iCount
	end
end
''')
put('lib/l01.haro', '''load "lib.haro"
print Twice(21)
print Greet("ada")
oC = new Counter
oC.Add(3).Add(4)
print oC.Total()
''')
put('lib/l02.haro', '''load "lib.haro"
print Twice(4)
oC = new Counter
oC.NoSuchMethod()
print "not reached"
''')
put('lib/l03.haro', '''load "lib.haro"
try
	oC = new Counter
	oC.NoSuchMethod()
catch e
	print "caught"
end
print Greet("after")
''')
put('lib/l04.haro', '''load "lib.haro"
iX = 0
Eval("iX = Twice(5)")
print iX
''')
put('lib/l05.haro', '''print "before the load"
load "lib.haro"
print Twice(1)
''')
put('lib/l06.ring', '''load "lib.haro"
? Twice(3)

func Twice n
	return n * 20
''')

L01_OUT = 'the library is loaded\n42\nhello, ada\n7\n'
LIB = [
    {'id': 'L01', 'line': 'L1', 'what': 'a root whose first statement loads the kept library is compiled on top of it, and prints what its whole compile prints',
     'kind': 'library', 'root': 'l01.haro', 'stdout': L01_OUT, 'exit': 0,
     'steps': [['fresh', 'path: whole'], ['prefix', None], ['run', 'path: kept library'], ['run', 'path: kept image']]},
    {'id': 'L02', 'line': 'L1', 'what': 'a root that dies part-way dies the same on the kept library: the same bytes, the same exit code',
     'kind': 'library', 'root': 'l02.haro', 'has': ['the library is loaded\n8\n', 'Error (R14)'], 'never': 'not reached', 'exit': 1,
     'steps': [['fresh', 'path: whole'], ['prefix', None], ['run', 'path: kept library']]},
    {'id': 'L03', 'line': 'L1', 'what': 'an error caught in a root that stands on the kept library is caught, and the root goes on',
     'kind': 'library', 'root': 'l03.haro', 'stdout': 'the library is loaded\ncaught\nhello, after\n', 'exit': 0,
     'steps': [['fresh', 'path: whole'], ['prefix', None], ['run', 'path: kept library']]},
    {'id': 'L04', 'line': 'L1', 'what': 'text run as code in a root on the kept library reaches the library\'s functions',
     'kind': 'library', 'root': 'l04.haro', 'stdout': 'the library is loaded\n10\n', 'exit': 0,
     'steps': [['fresh', 'path: whole'], ['prefix', None], ['run', 'path: kept library']]},
    {'id': 'L05', 'line': 'L2', 'what': 'a root that writes before it loads the library is compiled whole, and the path says so',
     'kind': 'library', 'root': 'l05.haro', 'stdout': 'before the load\nthe library is loaded\n2\n', 'exit': 0,
     'steps': [['prefix', None], ['run', 'path: whole']]},
    {'id': 'L06', 'line': 'L2', 'what': 'a root that defines a function the library defines is compiled whole -- its own definition answers -- and the path names the function',
     'kind': 'library', 'root': 'l06.ring', 'stdout': 'the library is loaded\n60\n', 'exit': 0,
     'steps': [['fresh', 'path: whole'], ['prefix', None], ['run', 'path: whole, the kept library does not apply (Twice)']]},
    {'id': 'L07', 'line': 'L2', 'what': 'a kept library whose file changed since is not taken: the root is compiled whole on the library as it is now, and the path says stale',
     'kind': 'library', 'root': 'l01.haro', 'stdout': 'the library is loaded\nchanged\n42\nhello, ada\n7\n', 'exit': 0,
     'steps': [['prefix', None], ['append', 'print "changed"\n'], ['run', 'path: whole, the kept library is stale']]},
    {'id': 'L08', 'line': 'L3', 'what': 'HARO_NOIMAGE: the root stands on the kept library at every run, and no image of the root is written',
     'kind': 'library', 'root': 'l01.haro', 'stdout': L01_OUT, 'exit': 0, 'env': {'HARO_NOIMAGE': '1'},
     'steps': [['prefix', None], ['run', 'path: kept library'], ['run', 'path: kept library'], ['images', 0]]},
    {'id': 'L09', 'line': 'L3', 'what': 'what stays: without the setting a root on the kept library writes its image, one file',
     'kind': 'library', 'root': 'l01.haro', 'stdout': L01_OUT, 'exit': 0,
     'steps': [['prefix', None], ['run', 'path: kept library'], ['images', 1]]},
    {'id': 'L10', 'line': 'L3', 'what': 'HARO_NOIMAGE with no kept library: compiled whole at every run, and no image is written',
     'kind': 'library', 'root': 'l01.haro', 'stdout': L01_OUT, 'exit': 0, 'env': {'HARO_NOIMAGE': '1'},
     'steps': [['fresh', 'path: whole'], ['run', 'path: whole'], ['images', 0]]},
    {'id': 'L11', 'line': 'L4', 'what': 'what stays: without HARO_PATH a run writes no line about its path',
     'kind': 'library', 'root': 'l01.haro', 'stdout': L01_OUT, 'exit': 0, 'silent': True,
     'steps': [['prefix', None], ['run', None], ['run', None]]},
    {'id': 'L12', 'line': 'L4', 'what': '`haro prefix <library>` says what it kept and ends with 0',
     'kind': 'prefix', 'library': 'lib.haro', 'has': ['prefix: 1 file(s), ', ' class(es), '], 'exit': 0},
    {'id': 'L13', 'line': 'L4', 'what': 'the usage text names `prefix` and what it is for',
     'kind': 'usage', 'has': ['haro prefix <library.haro>', 'a program whose first statement loads it']},
]

# ------------------------------------------------------------------------------------- X: a compile that fails, and its code
# The program is written by the court from this rule, so no megabyte of generated text is committed: FUNCTIONS functions of one
# shape and one call. The ladder is the memory each run may commit, in megabytes; where a run says the fixture's words, its exit
# code is the fixture's, and at least one rung must say them -- else the case did not ask its question.
BIG = {'functions': 6000, 'stdout': '4\n'}
LADDER = [160, 130, 110, 100, 90, 80, 70]
EXIT = [
    {'id': 'X01', 'line': 'L5', 'what': 'a run whose compile fails for memory ends with 1, where it ended with 0',
     'kind': 'limit', 'args': ['{big}'], 'ladder': LADDER, 'says': 'compile failed', 'exit': 1},
    {'id': 'X02', 'line': 'L5', 'what': 'what stays: the same program with the memory it needs prints its answer and ends with 0',
     'kind': 'limit', 'args': ['{big}'], 'ladder': [0], 'stdout': '4\n', 'exit': 0},
    {'id': 'X03', 'line': 'L5', 'what': 'another command whose compile fails ends with 1 too: the code is the driver\'s, not one command\'s',
     'kind': 'limit', 'args': ['dis', '{big}'], 'ladder': LADDER, 'says': 'compile failed', 'exit': 1},
    {'id': 'X04', 'line': 'L5', 'what': '`haro check` whose compiler stopped before the unit\'s end says so and ends with 1: a gate that reads 0 reads a whole check',
     'kind': 'limit', 'args': ['check', '{big}'], 'ladder': LADDER, 'says': 'the compiler stopped before the unit\'s end', 'exit': 1},
    {'id': 'X05', 'line': 'L5', 'what': 'what stays: a check that reads the whole unit ends with 0',
     'kind': 'limit', 'args': ['check', '{big}'], 'ladder': [0], 'has': [' 0 error, '], 'exit': 0},
]

# ------------------------------------------------------------------------------------------- R: a run that reads from a place
put('r/data/three.txt', 'one\ntwo\nthree\n')
put('r/reader.haro', '''iLines = 0
tAll = ""
while not FEOF(stdin)
	give tLine
	if FEOF(stdin) and tLine = ""
		exit
	end
	iLines = iLines + 1
	tAll = tAll + Upper(tLine) + "|"
end
print iLines
print tAll
''')
put('r/echo.haro', '''while not FEOF(stdin)
	give tLine
	if FEOF(stdin) and tLine = ""
		exit
	end
	print tLine
end
''')
DOORS = ('load "doors.haro"\n'
         'sDoors = doors\'DEFINE ROOT data AS (AT "data", ALLOWS [read]) RATIONALE "what the child reads"\n'
         'DEFINE ROOT made AS (AT "made", ALLOWS [write]) RATIONALE "what this program writes and may not read"\n'
         'DEFINE COMMAND count AS (ITSELF yes, TAKES [word]) RATIONALE "a child that counts the lines of its standard input"\'\n'
         'hCall = sDoors.Invocation("count", ["reader.haro"])\n')
put('r/r01.haro', DOORS + '''hIn = sDoors.Place("data", "three.txt")
rRun = hCall.RunReading(hIn)
print rRun.iCode
print rRun.tOutput
print "[" + rRun.tErrors + "]"
''')
put('r/r02.haro', DOORS + '''hIn = sDoors.Place("made", "three.txt")
try
	rRun = hCall.RunReading(hIn)
	print "ran"
catch e
	print e.Code()
end
''')
put('r/r03.haro', DOORS + '''try
	rRun = hCall.RunReading("data/three.txt")
	print "ran"
catch e
	print e.Code()
	print e.Message()
end
''')
put('r/r04.haro', DOORS + '''hIn = sDoors.Place("data", "nothere.txt")
try
	rRun = hCall.RunReading(hIn)
	print "ran"
catch e
	print e.Code()
end
''')
put('r/r05.haro', '''load "doors.haro"
sDoors = doors'DEFINE ROOT made AS (AT "made", ALLOWS [read, write]) RATIONALE "a large input this program writes and its child reads"
DEFINE COMMAND echo AS (ITSELF yes, TAKES [word]) RATIONALE "a child that writes back each line it reads"'
tAll = ""
for i = 1 to 5000
	tAll = tAll + "line " + String(i) + " of the large input, a line of some length" + Char(10)
end
MakeDir("made")
hBig = sDoors.Place("made", "big.txt")
Write(hBig, tAll)
hCall = sDoors.Invocation("echo", ["echo.haro"])
rRun = hCall.RunReading(hBig)
print rRun.iCode
print Len(tAll) > 200000
print Len(rRun.tOutput) > 200000
''')
put('r/r06.haro', DOORS + '''rRun = hCall.Run()
print rRun.iCode
print "[" + rRun.tOutput + "]"
''')
RUN = [
    {'id': 'R01', 'line': 'L6', 'what': 'RunReading gives the child the file at the place as its standard input, and answers what Run answers',
     'kind': 'run', 'dir': 'r', 'file': 'r01.haro', 'stdout': '0\n3\nONE|TWO|THREE|\n[]\n', 'exit': 0},
    {'id': 'R02', 'line': 'L6', 'what': 'a place whose root does not allow read is refused by name, and the child is not started',
     'kind': 'run', 'dir': 'r', 'file': 'r02.haro', 'stdout': 'PLACE_NOT_ALLOWED\n', 'exit': 0},
    {'id': 'R03', 'line': 'L6', 'what': 'a text is no place: refused by name, in words that say what a run reads from',
     'kind': 'run', 'dir': 'r', 'file': 'r03.haro',
     'stdout': 'RUN_INPUT\nError (RUN_INPUT) : a run reads its standard input from a place -- <doors>.Place(root, text); given a text\n', 'exit': 0},
    {'id': 'R04', 'line': 'L6', 'what': 'a place that names no file is refused by name, and the child is not started',
     'kind': 'run', 'dir': 'r', 'file': 'r04.haro', 'stdout': 'INPUT_NOT_READ\n', 'exit': 0},
    {'id': 'R05', 'line': 'L6', 'what': 'a large input and a large output pass whole: the child reads 5,000 lines and writes each back',
     'kind': 'run', 'dir': 'r', 'file': 'r05.haro', 'stdout': '0\ntrue\ntrue\n', 'exit': 0, 'clean': ['made']},
    {'id': 'R06', 'line': 'L6', 'what': 'what stays: Run gives the child no standard input -- it reads its end at once',
     'kind': 'run', 'dir': 'r', 'file': 'r06.haro', 'stdout': '0\n[0\n]\n', 'exit': 0},
]

doc = {
    'version': 'v0.78',
    'task': 'three findings of the desks: a failed compile ends with a non-zero code (HARO-COMPILE-EXIT-01); the kept library is '
            'held by a court, says its path and can write no image (HARO-LIBIMAGE-01); a run reads its standard input from a place '
            '(HARO-INVOCATION-STDIN-01)',
    'big': BIG,
    'cases': LIB + EXIT + RUN,
}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(doc['cases']), 'cases written')
