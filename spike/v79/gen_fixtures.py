"""Haro v0.79, the fixtures, written before any code: what the desks found on v0.78, where `haro check` and haro.exe disagree,
and one reply that could carry a header the program never wrote.

  H   MARBOOHA-HARO-01 (marbooha): `rpp_http_reply(iStatus, tType, tBody)` put its type into the reply's head as given, cut at 200
      bytes -- a type holding CR or LF ends the Content-Type line and writes a header of its own. Read on v0.78 at httpd.zig line
      289. The type is now refused with HEADER_VALUE when it holds CR or LF or is over 200 bytes; the reply is not sent, the
      request stays open, and the program may answer it again.
  B   MARBOOHA-HARO-01: `haro check` called `Divide` and every `rpp_http_*` undefined (Error R3) while haro.exe ran them. The checker
      knew the 258 names of the older runtime and three of Haro's own; it now knows every name haro.exe answers -- its compiler's built-ins and
      the natives it publishes at start-up. A name neither knows is still undefined.
  T   stzlib-gpu (2026-11-27 06:53) and marbooha: a sum or a product whose two sides the file alone shows are text and a number,
      or a decimal and a float, or a float and an integer, is refused by the run (NO_COERCION, NUMBER_MIX) and was passed by
      `check`. A side is shown by a literal or by a name's type letter (t, i, d, f); a side lettered x, or any other, is not.
  Q   stzlib-gpu: a quotient of two integer literals with no exact decimal (DECIMAL_INEXACT), and any quotient given to a name
      lettered i (TYPE_LETTER: `/` answers a decimal) -- refused by the run, passed by `check`.
  N   stzlib-gpu: a .haro file's top-level `nL = 5` replaced the line end that every older file of the program reads as `nl`
      (`"x" + nl + "y"` printed x5y); so does `tAb`. Neither the run nor `check` said so. In a .haro file a
      top-level assignment to a name that is one of the six -- nl, tab, cr, stdin, stdout, stderr, in any case -- is refused
      when compiling, NAME_RESERVED, and `check` names it where the run does. A function's own local of that name is its own.
  I   MARBOOHA-HARO-01: a list indexed by a decimal (or a float) stopped with "Bad parameter type!". In a .haro file it is
      refused with INDEX_NOT_INTEGER, naming the value; `check` names it where a literal or a d or f name is the index.
  E   HARO-GRAPH-LATEEVAL-01 (stzlib-testoor): `haro graph` printed no line for `Eval`, whose text may call any function. An
      Eval that no function of the unit answers counts with the late calls: `CALL|<caller>|*|late|<n>`.
  C   found writing these fixtures: Add(), Add(x) and Len() crash the compiler (exit 3) in `check` and in a run; they are
      refused by name, as every other built-in called with a wrong count is.
  L   IRIS-NEED-HARO-02 (a): `check` of a 6-line file loading stzBase took 596 s and 1,307 MB on v0.78 and reported 9,670
      findings in 623 files, none in the file named. `check <file>` reports the named file's folder and below; a file
      loaded from elsewhere is read for its names, not reported, and counted in one line (`--all` reports all); the
      compile stands on a kept library where there is one, and HARO_PATH=1 says the path.

The spellings are this desk's, chosen with these fixtures under D84 (delegated):

  HEADER_VALUE        a reply's type holds CR or LF, or is over 200 bytes
  INDEX_NOT_INTEGER   a list's index in a .haro file is a decimal or a float
  NAME_RESERVED       a .haro top-level assignment to nl, tab, cr, stdin, stdout or stderr
  check --all         every file of the unit reported; without it, the named file's folder and below
  haro/no-coercion, haro/number-mix, haro/decimal-inexact, haro/type-letter, haro/index-not-integer
                      `check`'s rules, each named after the run's code it foresees, and each saying that code in its words

  python spike/v79/gen_fixtures.py     writes fixtures.json and cases/
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
VMSRC = os.path.join(os.path.dirname(SPIKE), 'vm', 'src')
CASES = os.path.join(HERE, 'cases')


def put(rel, text):
    p = os.path.join(CASES, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


cases = []


def case(**c):
    cases.append(c)


# ---------------------------------------------------------------------------------------------- H: the reply's head
# The court serves each program on a free port of 127.0.0.1 (it writes the port into the copy it runs, where {PORT} stands),
# sends one GET, and reads the reply's bytes whole; the program prints what it saw.
SERVE = '''iOk = rpp_http_listen({PORT})
print "listening " + String(iOk)
iGot = rpp_http_next()
'''
put('h/h01.haro', SERVE + '''rpp_http_reply(200, "text/plain; charset=utf-8", "hello")
print "replied"
''')
put('h/h02.haro', SERVE + '''try
	rpp_http_reply(200, "text/plain" + Char(13) + Char(10) + "X-Injected: yes", "hello")
	print "sent with the header"
catch e
	print e.Code()
end
rpp_http_reply(400, "text/plain", "refused")
print "replied"
''')
put('h/h03.haro', SERVE + '''try
	rpp_http_reply(200, "text/plain" + Char(10) + "X-Injected: yes", "hello")
catch e
	print e.Code()
end
rpp_http_reply(400, "text/plain", "refused")
''')
put('h/h04.haro', SERVE + '''try
	rpp_http_reply(200, "text/plain" + Char(13) + "X-Injected: yes", "hello")
catch e
	print e.Code()
end
rpp_http_reply(400, "text/plain", "refused")
''')
put('h/h05.haro', SERVE + '''tType = "text/plain; x="
for iK = 1 to 187
	tType = tType + "a"
end
print Len(tType)
try
	rpp_http_reply(200, tType, "hello")
catch e
	print e.Code()
end
rpp_http_reply(400, "text/plain", "refused")
''')
put('h/h06.haro', SERVE + '''tType = "text/plain; x="
for iK = 1 to 186
	tType = tType + "a"
end
print Len(tType)
rpp_http_reply(200, tType, "whole")
print "replied"
''')
put('h/h07.haro', SERVE + '''rpp_http_reply(200, "text/plain" + Char(13) + Char(10) + "X-Injected: yes", "hello")
print "not reached"
''')
HEAD = 'HTTP/1.1 {s} {r}\r\nContent-Type: {t}\r\nContent-Length: {n}\r\nConnection: close\r\n\r\n{b}'
REFUSED = HEAD.format(s=400, r='Bad Request', t='text/plain', n=7, b='refused')
case(id='H01', line='H1', kind='http', file='h/h01.haro', what='a reply with a plain type is sent as it was: the head and the body',
     reply=HEAD.format(s=200, r='OK', t='text/plain; charset=utf-8', n=5, b='hello'), stdout='listening 1\nreplied\n', exit=0)
case(id='H02', line='H1', kind='http', file='h/h02.haro', what='a type holding CR LF is refused with HEADER_VALUE, nothing is sent, and the program answers the request again',
     reply=REFUSED, stdout='listening 1\nHEADER_VALUE\nreplied\n', exit=0, never='X-Injected')
case(id='H03', line='H1', kind='http', file='h/h03.haro', what='a type holding LF alone is refused with HEADER_VALUE',
     reply=REFUSED, stdout='listening 1\nHEADER_VALUE\n', exit=0, never='X-Injected')
case(id='H04', line='H1', kind='http', file='h/h04.haro', what='a type holding CR alone is refused with HEADER_VALUE',
     reply=REFUSED, stdout='listening 1\nHEADER_VALUE\n', exit=0, never='X-Injected')
case(id='H05', line='H1', kind='http', file='h/h05.haro', what='a type of 201 bytes is refused with HEADER_VALUE, where v0.78 cut it at 200',
     reply=REFUSED, stdout='listening 1\n201\nHEADER_VALUE\n', exit=0)
case(id='H06', line='H1', kind='http', file='h/h06.haro', what='a type of 200 bytes is sent whole',
     reply=HEAD.format(s=200, r='OK', t='text/plain; x=' + 'a' * 186, n=5, b='whole'), stdout='listening 1\n200\nreplied\n', exit=0)
case(id='H07', line='H1', kind='http', file='h/h07.haro', what='a refusal nobody catches ends the program with 1, naming HEADER_VALUE, and no reply carries the header',
     reply='', has=['HEADER_VALUE'], never_out='not reached', exit=1, never='X-Injected')

# ---------------------------------------------------------------------------------------------- B: every name haro.exe answers
put('b/b01.haro', '''dA = 7 / 2
dB = Divide(1, 3, 4)
fC = Float(dA)
dD = Decimal(fC, 2)
iE = Integer(4.0)
bF = Near(fC, 3.5f, 0.01f)
tG = Text(dB, 4)
dH = Round(dB, 2)
mI = ["k": 1]
vJ = Keys(mI)
bK = HasKey(mI, "k")
bL = IsEmpty("")
print tG
print bK
''')
put('b/b02.haro', '''if false
	iA = rpp_http_listen(8080)
	iB = rpp_http_next()
	tC = rpp_http_method()
	tD = rpp_http_path()
	tE = rpp_http_query()
	tF = rpp_http_header("Host")
	tG = rpp_http_body()
	iH = rpp_http_reply(200, "text/plain", "ok")
	tI = SystemCmd("haro")
end
print "named"
''')
put('b/b03.haro', '''dA = Divid(1, 3, 4)
iB = rpp_http_listn(8080)
''')
put('b/b04.ring', '''if false
	x = rpp_http_listen(8080)
	y = rpp_http_reply(200, "text/plain", "ok")
ok
? "named"
''')


def names_haro_answers():
    """every name haro.exe answers with no load: its compiler's built-ins (compile.zig's table) and the spellings builtins.zig
    gives the natives and built-ins a .haro file writes -- read from the sources as they stand when these fixtures are written"""
    comp = open(os.path.join(VMSRC, 'compile.zig'), encoding='utf-8').read()
    intrinsic = dict(re.findall(r'\.\{ \.name = "([a-z_0-9]+)", \.id = \.\w+, \.argc = (\d+) \}', comp))
    bt = open(os.path.join(VMSRC, 'builtins.zig'), encoding='utf-8').read()
    pascal = dict(re.findall(r'\.\{ "([a-z_0-9]+)", "([A-Za-z0-9]+)" \}', bt))
    return intrinsic, pascal


intrinsic, pascal = names_haro_answers()


def asked(intrinsic, pascal):
    """the names B05 calls: all of them but those that switch the rule off for their file (eval, loadlib, and the calls that
    admit code while the program runs), and isnull, which a .haro file refuses (v0.59)"""
    off = {'eval', 'loadlib', 'isnull'}
    return {n for n in set(intrinsic) | set(pascal) if n not in off and not n.startswith(('admit', 'replace', 'release'))}


lines = ['xA = 1', 'if false']
for low in sorted(asked(intrinsic, pascal)):
    spelt = pascal.get(low, low)
    argc = int(intrinsic.get(low, 1))
    lines.append(f'\txR = {spelt}(' + ', '.join(['xA'] * argc) + ')')
lines += ['end', 'print "every name"']
put('b/b05.haro', '\n'.join(lines) + '\n')
NAMES = len(asked(intrinsic, pascal))

case(id='B01', line='B1', kind='check', file='b/b01.haro', what='`check` knows Divide, Float, Decimal, Integer, Near, Text, Round, Keys, HasKey and IsEmpty, which haro.exe runs',
     never=['haro/undefined-function'], run={'stdout': '0.3333\ntrue\n', 'exit': 0})
case(id='B02', line='B1', kind='check', file='b/b02.haro', what='`check` knows the eight rpp_http_ natives and SystemCmd, which haro.exe publishes at start-up',
     never=['haro/undefined-function'], run={'stdout': 'named\n', 'exit': 0})
case(id='B03', line='B2', kind='check', file='b/b03.haro', what='a name haro.exe does not answer is still undefined: one letter off a built-in, one off a native',
     rules=[[1, 'haro/undefined-function'], [2, 'haro/undefined-function']])
case(id='B04', line='B1', kind='check', file='b/b04.ring', what='a .ring file reaches the natives too, and `check` knows them there',
     never=['haro/undefined-function'], run={'stdout': 'named\n', 'exit': 0})
case(id='B05', line='B1', kind='check', file='b/b05.haro', what=f'`check` knows every one of the {NAMES} names the compiler\'s table and the spelling table name, as written today (Eval, LoadLib and the calls that admit code apart: any one switches the rule off for its file, as it always has)',
     never=['haro/undefined-function'])

# ---------------------------------------------------------------------------------------------- T: text, numbers, mixes
put('t/t01.haro', 'tM = "count " + 3\nprint tM\n')
put('t/t02.haro', 'tA = "count "\niB = 3\ntC = tA + iB\nprint tC\n')
put('t/t03.haro', 'tA = "count "\niB = 3\ntC = tA + String(iB)\nprint tC\n')
put('t/t04.haro', 'xV = 3\ntC = "count " + xV\nprint tC\n')
put('t/t05.haro', 'dA = 1.5\nfB = 2.0f\nfC = dA + fB\nprint fC\n')
put('t/t06.haro', 'fA = 2.0f\nfC = fA * 3\nprint fC\n')
put('t/t07.haro', 'fA = 2.0f\nfC = fA * Float(3)\nprint String(fC)\n')
put('t/t08.haro', 'func Main\n\ttA = "a"\n\tiN = 2\n\tprint tA + iN\nend\n')
case(id='T01', line='T1', kind='check', file='t/t01.haro', what='text + an integer literal: `check` says NO_COERCION where the run refuses it',
     rules=[[1, 'haro/no-coercion']], says=['NO_COERCION'], run={'has': ['Error (NO_COERCION)'], 'exit': 1})
case(id='T02', line='T1', kind='check', file='t/t02.haro', what='a t name + an i name: the letters show it, and `check` says NO_COERCION',
     rules=[[3, 'haro/no-coercion']], says=['NO_COERCION'], run={'has': ['Error (NO_COERCION)'], 'exit': 1})
case(id='T03', line='T2', kind='check', file='t/t03.haro', what='text + String(i) is text + text: no finding, and the run prints it',
     never=['haro/no-coercion'], run={'stdout': 'count 3\n', 'exit': 0})
case(id='T04', line='T2', kind='check', file='t/t04.haro', what='a name lettered x shows no type: `check` says nothing, and the run still refuses it -- what stays',
     never=['haro/no-coercion'], run={'has': ['Error (NO_COERCION)'], 'exit': 1})
case(id='T05', line='T1', kind='check', file='t/t05.haro', what='a d name + an f name: `check` says NUMBER_MIX where the run refuses it',
     rules=[[3, 'haro/number-mix']], says=['NUMBER_MIX'], run={'has': ['Error (NUMBER_MIX)'], 'exit': 1})
case(id='T06', line='T1', kind='check', file='t/t06.haro', what='an f name * an integer literal: NUMBER_MIX in `check` and in the run',
     rules=[[2, 'haro/number-mix']], says=['NUMBER_MIX'], run={'has': ['Error (NUMBER_MIX)'], 'exit': 1})
case(id='T07', line='T2', kind='check', file='t/t07.haro', what='an f name * Float(3) is two floats: no finding, and the run prints it',
     never=['haro/number-mix'], run={'stdout': '6\n', 'exit': 0})
case(id='T08', line='T1', kind='check', file='t/t08.haro', what='inside a function as at the top level: a t local + an i local is NO_COERCION in `check`',
     rules=[[4, 'haro/no-coercion']], says=['NO_COERCION'], run={'has': ['Error (NO_COERCION)'], 'exit': 1})

# ---------------------------------------------------------------------------------------------- Q: quotients
put('q/q01.haro', 'dQ = 1 / 3\nprint dQ\n')
put('q/q02.haro', 'dQ = 1 / 4\nprint dQ\n')
put('q/q03.haro', 'iN = 10 / 5\nprint iN\n')
put('q/q04.haro', 'dN = 10 / 5\nprint dN\n')
put('q/q05.haro', 'iA = 1\niB = 3\ndQ = iA / iB\nprint dQ\n')
put('q/q06.haro', 'iA = 10\niB = 5\niN = iA / iB\nprint iN\n')
case(id='Q01', line='Q1', kind='check', file='q/q01.haro', what='1 / 3 has no exact decimal: `check` says DECIMAL_INEXACT where the run refuses it',
     rules=[[1, 'haro/decimal-inexact']], says=['DECIMAL_INEXACT'], run={'has': ['Error (DECIMAL_INEXACT)'], 'exit': 1})
case(id='Q02', line='Q2', kind='check', file='q/q02.haro', what='1 / 4 is exactly 0.25: no finding, and the run prints it',
     never=['haro/decimal-inexact'], run={'stdout': '0.25\n', 'exit': 0})
case(id='Q03', line='Q1', kind='check', file='q/q03.haro', what='a quotient given to an i name, even 10 / 5: `check` says TYPE_LETTER where the run refuses it',
     rules=[[1, 'haro/type-letter']], says=['TYPE_LETTER'], run={'has': ['Error (TYPE_LETTER)'], 'exit': 1})
case(id='Q04', line='Q2', kind='check', file='q/q04.haro', what='10 / 5 given to a d name: no finding, and the run prints 2',
     never=['haro/type-letter', 'haro/decimal-inexact'], run={'stdout': '2\n', 'exit': 0})
case(id='Q05', line='Q2', kind='check', file='q/q05.haro', what='a quotient of two names: their values are the run\'s, so `check` says nothing and the run still refuses 1 / 3 -- what stays',
     never=['haro/decimal-inexact'], run={'has': ['Error (DECIMAL_INEXACT)'], 'exit': 1})
case(id='Q06', line='Q1', kind='check', file='q/q06.haro', what='a quotient of two names given to an i name: the letter shows it whatever the values',
     rules=[[3, 'haro/type-letter']], says=['TYPE_LETTER'], run={'has': ['Error (TYPE_LETTER)'], 'exit': 1})

# ---------------------------------------------------------------------------------------------- N: the six names older code reads
put('n/show.ring', 'func Show\n\t? "x" + tab + "y" + nl + "z"\n')
put('n/n01.haro', 'load "show.ring"\nnL = 5\nShow()\n')
put('n/n02.haro', 'load "show.ring"\ntAb = "T"\nShow()\n')
put('n/n03.haro', 'load "show.ring"\nfunc Main\n\tWork()\n\tShow()\nend\nfunc Work\n\tnL = 5\n\tprint nL\nend\n')
put('n/n04.haro', 'load "show.ring"\nnLines = 5\nShow()\nprint nLines\n')
put('n/n05.haro', 'nL = 5\nprint "after"\n')
put('n/n06.ring', 'load "show.ring"\nnl = "|"\nShow()\n')
SHOWN = 'x\ty\nz\n'
case(id='N01', line='N1', kind='check', file='n/n01.haro', what='a top-level `nL = 5` is refused when compiling, NAME_RESERVED, and `check` names it at the run\'s line',
     rules=[[2, 'haro/refused-form']], says=['NAME_RESERVED'], run={'has': ['NAME_RESERVED'], 'never': 'x5y', 'exit': 1})
case(id='N02', line='N1', kind='check', file='n/n02.haro', what='a top-level `tAb` is refused the same: it would replace the tab every older file reads',
     rules=[[2, 'haro/refused-form']], says=['NAME_RESERVED'], run={'has': ['NAME_RESERVED'], 'never': 'xTy', 'exit': 1})
case(id='N03', line='N2', kind='check', file='n/n03.haro', what='a function\'s own `nL` is its local: no refusal, and the older file\'s line end is untouched',
     never=['NAME_RESERVED'], run={'stdout': '5\n' + SHOWN, 'exit': 0})
case(id='N04', line='N2', kind='check', file='n/n04.haro', what='`nLines` is another name: no refusal',
     never=['NAME_RESERVED'], run={'stdout': SHOWN + '5\n', 'exit': 0})
case(id='N05', line='N1', kind='check', file='n/n05.haro', what='a top-level `nL` is refused in a file that loads no older file too: the name is reserved, wherever it would land',
     rules=[[1, 'haro/refused-form']], says=['NAME_RESERVED'], run={'has': ['NAME_RESERVED'], 'never': 'after', 'exit': 1})
case(id='N06', line='N2', kind='check', file='n/n06.ring', what='a .ring file reads as it did: its own `nl = "|"` replaces the line end, as it always has',
     never=['NAME_RESERVED'], run={'stdout': 'x\ty|z\n', 'exit': 0})

# ---------------------------------------------------------------------------------------------- I: a list's index
put('i/i01.haro', 'vL = ["a", "b", "c"]\ndI = 2.0\nprint vL[dI]\n')
put('i/i02.haro', 'vL = ["a", "b", "c"]\nfI = 2.0f\nprint vL[fI]\n')
put('i/i03.haro', 'vL = ["a", "b", "c"]\nprint vL[2.0]\n')
put('i/i04.haro', 'vL = ["a", "b", "c"]\ndI = 2.0\nprint vL[Integer(dI)]\n')
put('i/i05.haro', 'vL = ["a", "b", "c"]\nxI = 2.0\nprint vL[xI]\n')
put('i/i06.haro', 'vL = ["a", "b", "c"]\ndI = 2.0\nvL[dI] = "z"\n')
case(id='I01', line='I1', kind='check', file='i/i01.haro', what='a d name as an index: INDEX_NOT_INTEGER in `check` and in the run, naming the decimal',
     rules=[[3, 'haro/index-not-integer']], says=['INDEX_NOT_INTEGER'], run={'has': ['Error (INDEX_NOT_INTEGER)', '2.0'], 'never': 'Bad parameter type', 'exit': 1})
case(id='I02', line='I1', kind='check', file='i/i02.haro', what='an f name as an index: INDEX_NOT_INTEGER, naming the float',
     rules=[[3, 'haro/index-not-integer']], says=['INDEX_NOT_INTEGER'], run={'has': ['Error (INDEX_NOT_INTEGER)'], 'never': 'Bad parameter type', 'exit': 1})
case(id='I03', line='I1', kind='check', file='i/i03.haro', what='a decimal literal as an index: INDEX_NOT_INTEGER',
     rules=[[2, 'haro/index-not-integer']], says=['INDEX_NOT_INTEGER'], run={'has': ['Error (INDEX_NOT_INTEGER)'], 'exit': 1})
case(id='I04', line='I2', kind='check', file='i/i04.haro', what='Integer(dI) is an integer: no finding, and the run prints b',
     never=['haro/index-not-integer'], run={'stdout': 'b\n', 'exit': 0})
case(id='I05', line='I2', kind='check', file='i/i05.haro', what='an x name holding a decimal: `check` cannot see it, and the run names it -- INDEX_NOT_INTEGER, not "Bad parameter type!"',
     never=['haro/index-not-integer'], run={'has': ['Error (INDEX_NOT_INTEGER)'], 'never': 'Bad parameter type', 'exit': 1})
case(id='I06', line='I1', kind='check', file='i/i06.haro', what='a decimal index written into is refused the same',
     rules=[[3, 'haro/index-not-integer']], says=['INDEX_NOT_INTEGER'], run={'has': ['Error (INDEX_NOT_INTEGER)'], 'exit': 1})

# ---------------------------------------------------------------------------------------------- C: a call the compiler crashed on
# Found writing B05 (runtime/v79/arity_sweep*.py, 283 names, 0 to 4 arguments, 3,614 runs on v0.78): three calls crash the compiler
# -- a segmentation fault, exit 3 -- in `check` and in a run alike. Every other wrong count is refused by name, as these now are.
put('c/c01.haro', 'vA = [1]\nAdd(vA)\nprint "after"\n')
put('c/c02.haro', 'vA = [1]\nAdd()\nprint "after"\n')
put('c/c03.haro', 'iN = Len()\nprint "after"\n')
put('c/c04.ring', 'a = [1]\nadd(a)\n? "after"\n')
put('c/c05.haro', 'func Main\n\tvA = [1]\n\tAdd(vA)\nend\n')
WRONG = 'a builtin called with the wrong number of arguments'
for cid, f, line, what in [('C01', 'c/c01.haro', 2, 'Add(vA), the value to add missing'), ('C02', 'c/c02.haro', 2, 'Add() with nothing'),
                           ('C03', 'c/c03.haro', 1, 'Len() with nothing'), ('C04', 'c/c04.ring', 2, 'add(a) in a .ring file'),
                           ('C05', 'c/c05.haro', 3, 'Add(vA) on a function\'s local')]:
    case(id=cid, line='C1', kind='check', file=f, what=f'{what}: refused by name in `check` and in the run, where v0.78 crashed both',
         rules=[[line, 'haro/refused-form']], says=[WRONG], never=['Segmentation fault'],
         run={'has': [WRONG], 'never': 'Segmentation fault', 'exit': 1})

# ---------------------------------------------------------------------------------------------- E: Eval in the graph
put('e/e01.haro', 'func Hello\n\tprint "hi"\nend\nfunc Go(ptCode)\n\tEval(ptCode)\n\tHello()\nend\nGo("Hello()")\n')
put('e/e02.haro', 'func Go(ptCode)\n\tEval(ptCode)\n\tEval(ptCode)\n\tcall ptCode()\nend\nfunc Hello\n\tprint "hi"\nend\nGo("Hello")\n')
put('e/e03.ring', 'go()\nfunc eval x\n\treturn x\nfunc go\n\teval("a")\n')
put('e/e04.haro', 'Eval("print 1")\n')
case(id='E01', line='E1', kind='graph', file='e/e01.haro', what='an Eval in a function is a late call of that function',
     stdout='FILE|e01.haro\nFUNC|Hello|1\nFUNC|Go|4\nCALL|<top>|Go|static\nCALL|Go|*|late|1\nCALL|Go|Hello|static\n')
case(id='E02', line='E1', kind='graph', file='e/e02.haro', what='two Evals and a call by a built name: late, 3',
     stdout='FILE|e02.haro\nFUNC|Go|1\nFUNC|Hello|6\nCALL|<top>|Go|static\nCALL|Go|*|late|3\n')
case(id='E03', line='E2', kind='graph', file='e/e03.ring', what='a function of the unit named eval answers the call: a static edge, no late line',
     stdout='FILE|e03.ring\nFUNC|eval|2\nFUNC|go|4\nCALL|<top>|go|static\nCALL|go|eval|static\n')
case(id='E04', line='E1', kind='graph', file='e/e04.haro', what='an Eval of the file\'s own statements is a late call of <top>',
     stdout='FILE|e04.haro\nCALL|<top>|*|late|1\n')

# ---------------------------------------------------------------------------------------------- L: what `check` reports
# IRIS-NEED-HARO-02 (a), measured on v0.78 (runtime/v79/iris_check.txt): a 6-line file loading stzBase -- 596 s, 1,307 MB at
# its peak, 9,670 findings in 623 files and none of them in the file named. From v0.79 `check <file>` reports the files of the
# named file's own folder and below; a file loaded from elsewhere is read for its names and not reported, and one line says how
# many (`--all` reports every file, as v0.78 did). Its compile stands on a kept library where there is one, and HARO_PATH=1
# says which path it took, as a run's does.
put('l/lib/lib.haro', 'func Twice(iN)\n\treturn iN * 2\nend\n\nfunc Broken\n\tNoSuchInLib()\nend\n\nfunc Refused\n\tTwo = 1\nend\n')
put('l/app/root6.haro', 'load "../lib/lib.haro"\nfunc Twice(iN)\n\treturn iN\nend\nprint Twice(2)\nif false\n\tNoSuchInRoot()\nend\n')
put('l/app/helper.haro', 'func Help\n\tNoSuchInHelper()\nend\n')
put('l/app/root.haro', 'load "../lib/lib.haro"\nload "helper.haro"\nprint Twice(21)\nif false\n\tNoSuchInRoot()\nend\n')
SCOPE = 'loaded from outside its folder: read for their names, not reported (--all reports them)'
case(id='L01', line='L1', kind='scope', file='l/app/root.haro', what='`check` reports the named file and the files of its folder; the library loaded from outside is not reported, and one line says so',
     args=[], rules=[['root.haro', 5, 'haro/undefined-function'], ['helper.haro', 2, 'haro/undefined-function']],
     never=['lib.haro', 'haro/refused-form', 'Twice()'], says=['1 file(s) ' + SCOPE])
case(id='L02', line='L1', kind='scope', file='l/app/root.haro', what='`check --all` reports every file of the unit, the library too, as v0.78 did',
     args=['--all'], rules=[['root.haro', 5, 'haro/undefined-function'], ['helper.haro', 2, 'haro/undefined-function'],
                            ['lib.haro', 6, 'haro/undefined-function'], ['lib.haro', 10, 'haro/refused-form']], never=[SCOPE])
case(id='L03', line='L2', kind='scope', file='l/app/root.haro', what='with the library kept (`haro prefix`), `check` compiles on top of it and says so with HARO_PATH=1',
     args=[], prefix='../lib/lib.haro', path='path: kept library', rules=[['root.haro', 5, 'haro/undefined-function']],
     never=['lib.haro', 'haro/refused-form', 'Twice()'], says=['1 file(s) ' + SCOPE])
case(id='L06', line='L2', kind='scope', file='l/app/root6.haro', what='a root that defines a name the kept library has is checked whole, and HARO_PATH=1 names the name',
     args=[], prefix='../lib/lib.haro', path_starts='path: whole, the kept library does not apply (', rules=[['root6.haro', 7, 'haro/undefined-function']],
     never=['lib.haro', 'haro/refused-form'])
case(id='L04', line='L2', kind='scope', file='l/app/root.haro', what='with no library kept, HARO_PATH=1 says `check` compiled whole',
     args=[], path='path: whole', rules=[['root.haro', 5, 'haro/undefined-function']], never=['lib.haro'])
case(id='L05', line='L1', kind='scope', file='l/lib/lib.haro', what='`check` of the library itself: it loads nothing from outside, so no scope line, and a library\'s calls are still left to the program that loads it',
     args=[], says=['a library\'s calls resolve through whoever loads it'], never=[SCOPE, 'haro/undefined-function'])

doc = {'rung': 'v0.79', 'written': 'before any code', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(f'{len(cases)} cases; B05 names {NAMES} built-ins and natives')
