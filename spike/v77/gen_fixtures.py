"""Haro v0.77, three findings of the desks, 2026-11-15: the cases of v77/fixtures.json and their files, written BEFORE the code.
Every expectation is typed here; each finding was first read on the installed v0.74, as its desk reported it.

  HARO-SIGLINE-01 (stzlib-testoor)            a statement on a definition's header line, and a header over two lines, were read
                                              as something else and said nothing: on v0.74 a program that writes either prints
                                              nothing, or runs the body as the file's own statements
  HARO-IMAGE-EVAL-LENIENT-01 (stzlib-intelligence)   a program served from its kept image let Eval take spellings a fresh
                                              compile of the same program refuses: a verdict depended on the cache
  HARO-GRAPH-LATECALL-01 (stzlib-testoor)     `haro graph` printed no line for a call by a name built when the program runs

  python spike/v77/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  a definition's body starts on the line after its header: a statement after the header on its line is refused when the
      program is compiled, for a function and for a method
  L2  a definition's header is written on one line: a parameter list that runs on to the next line is refused when compiling
  L3  what a header holds stays: its parameters, `maybe`, a comment; a class and its parent; a function with no parameter
  L4  a program run from its kept image is the program a fresh compile runs: what Eval refuses in one it refuses in the other,
      and what it takes in one it takes in the other
  L5  `haro graph` names a call by a name built when the program runs: `CALL|<caller>|*|late|<n>`; a unit that holds none prints
      what it printed
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []
RULE = 'haro/refused-form'
CASES = os.path.join(HERE, 'cases')
os.makedirs(CASES, exist_ok=True)

ONELINE = "a definition's body starts on the line after its header; written"
HEADLINE = "a definition's header is written on one line; written"


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, check=None, kind=None):
    """run: {'stdout': text} exact with exit 0; {'refuses': [row, reason, written]} with 'never'. check: {'errors': n, 'found':
    [[row, rule]]}. kind: 'kept' -- the program is run three times with its image kept, and each run prints run's stdout; 'graph'
    -- `haro graph <file>` prints run's stdout."""
    name = cid.lower() + '.haro'
    with open(os.path.join(CASES, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if check is not None:
        c['check'] = check
    if kind is not None:
        c['kind'] = kind
    cases.append(c)


case('F01', 'L1', 'a statement after a function\'s header on its line is refused when the program is compiled', '''func PageUtc(nMs) print "hit"
    return nMs + 1
end
print "before"
print PageUtc(41)
''', {'refuses': [1, ONELINE, 'PageUtc'], 'never': 'before'}, check={'errors': 1, 'found': [[1, RULE]]})

case('F02', 'L1', 'a `return` after the header, the `end` on the next line', '''print "before"
func Quick(nX) return nX
end
print Quick(7)
''', {'refuses': [2, ONELINE, 'Quick'], 'never': 'before'}, check={'errors': 1, 'found': [[2, RULE]]})

case('F03', 'L1', 'a method likewise', '''class Box
    iSide = 2

    def Twice(iTimes) return iSide * iTimes
    end
end
print "before"
''', {'refuses': [4, ONELINE, 'Twice'], 'never': 'before'}, check={'errors': 1, 'found': [[4, RULE]]})

case('F04', 'L2', 'a parameter list that runs on to the next line is refused when compiling', '''print "before"
func Label(tName,
    nNet)
    return tName
end
print Label("a", 1)
''', {'refuses': [2, HEADLINE, 'Label'], 'never': 'before'}, check={'errors': 1, 'found': [[2, RULE]]})

case('F05', 'L3', 'what a header holds stays: parameters, `maybe`, a comment, a class and its parent, no parameter', '''class Shape
    tName = "shape"

    def Name      # a method with no parameter
        return tName
    end
end

class Square from Shape      # a class and its parent
    iSide = 3

    def Area(iScale)      # (a comment that holds a parenthesis)
        return iSide * iSide * iScale
    end
end

func Find(iWanted) maybe      # an answer that may be none
    if iWanted = 1 return "one" end
    return none
end

func Main
    oSquare = new Square
    print oSquare.Name()
    print oSquare.Area(2)
    print Find(1) else "nothing"
    print Find(2) else "nothing"
end
''', {'stdout': 'shape\n18\none\nnothing\n'}, check={'errors': 0, 'found': []})

M_CASE = said('E1', 'a built-in is spelled `Len`; written `len`')
case('F06', 'L4', 'a built-in in another case inside Eval is refused from the kept image as from a fresh compile', '''tCode = "x = len(" + Char(34) + "abc" + Char(34) + ")"
try
    Eval(tCode)
    print "evaluated"
catch e
    print e.Message()
end
''', {'stdout': M_CASE + '\n'}, kind='kept')

M_PAIR = said('E1', '`:key = value` is no pair in a .haro file: write ["key": value] for a map, [:key, value] for a pair, or declare a record for named fields (HARO-SURFACE-01) `:name = 5`')
case('F07', 'L4', '`:key = value` inside Eval is refused from the kept image as from a fresh compile', '''tCode = "v = [:name = 5]"
try
    Eval(tCode)
    print "evaluated"
catch e
    print e.Message()
end
''', {'stdout': M_PAIR + '\n'}, kind='kept')

case('F08', 'L4', 'what Eval takes from a fresh compile it takes from the kept image', '''tCode = "x = Len(" + Char(34) + "abc" + Char(34) + ")"
try
    Eval(tCode)
    print "evaluated"
catch e
    print e.Message()
end
print Eval("return 2 + 3")
''', {'stdout': 'evaluated\n5\n'}, kind='kept')

case('F09', 'L5', '`haro graph` names a call by a name built when the program runs', '''func Hello
    print "hi"
end
func Go(ptName)
    call ptName()
    call ptName()
    Hello()
end
Go("Hello")
''', {'stdout': 'FILE|f09.haro\nFUNC|Hello|1\nFUNC|Go|4\nCALL|<top>|Go|static\nCALL|Go|*|late|2\nCALL|Go|Hello|static\n'}, kind='graph')

case('F10', 'L5', 'a unit that holds no such call prints what it printed', '''func Hello
    print "hi"
end
func Go
    Hello()
end
Go()
''', {'stdout': 'FILE|f10.haro\nFUNC|Hello|1\nFUNC|Go|4\nCALL|<top>|Go|static\nCALL|Go|Hello|static\n'}, kind='graph')

# Added 2026-11-16, after the court spoke and before the fix: the count on stzlib's files found that the header's rule ended a
# name at its first byte that is no letter, digit or underscore. A name holds `@` (497 of stzlib's definitions write one after
# their first word), and a name that starts with `@` was not looked at. The three cases below say both.
case('F11', 'L3', 'a name holds `@`, and starts with it: the header ends where the name ends', """class Box
    iSide = 2

    def Is@(iWanted)
        return iSide = iWanted
    end

    def @Side
        return iSide
    end
end

func Stz@(tType, tGiven)
    return tType + ":" + tGiven
end

func @Twice(iN) maybe      # a name that starts with the mark
    if iN = 0 return none end
    return iN * 2
end

func Main
    oBox = new Box
    print oBox.Is@(2)
    print oBox.@Side()
    print Stz@("text", "a")
    print @Twice(21) else 0
    print @Twice(0) else 0
end
""", {'stdout': 'true\n2\ntext:a\n42\n0\n'}, check={'errors': 0, 'found': []})

case('F12', 'L1', 'a statement after the header of a name that starts with `@`', """print "before"
func @Twice(iN) return iN * 2
end
print @Twice(7)
""", {'refuses': [2, ONELINE, '@Twice'], 'never': 'before'}, check={'errors': 1, 'found': [[2, RULE]]})

case('F13', 'L1', 'a statement after the header of a name that holds `@`: the refusal writes the name whole', """print "before"
func Stz@(tType) print "hit"
    return tType
end
print Stz@("a")
""", {'refuses': [2, ONELINE, 'Stz@'], 'never': 'before'}, check={'errors': 1, 'found': [[2, RULE]]})

doc = {'version': '0.77', 'task': 'three findings of the desks: HARO-SIGLINE-01, HARO-IMAGE-EVAL-LENIENT-01, HARO-GRAPH-LATECALL-01', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
