"""haroport (HARO-PORTTOOL-01): the cases, written FIRST, before port/haroport.py.

THE ASK. stzlib-haroport (2026-11-10 04:12), for stzlib's move to .haro (CENTRAL-NORING-SCOPE-01 (2)): "your keyword lowering,
study/v48/respell.py and study/v47/reletter.py as one command (or script) that takes a tree root, with reletter's conflict check and a plan
mode" -- its scratch scripts had no collision check, and unwrapping _x_ landed 15 locals on keywords (_new_ -> new, _try_ -> try).

THE TOOL (the desk's design, judged below):
  python port/haroport.py plan  ROOT              what it would do, file by file; writes nothing
  python port/haroport.py apply ROOT --out DIR    the ported tree in DIR, each .ring file as .haro and each load rewritten to it
THE REWRITES, each mechanical and each refused where it would land on something already there:
  K  a keyword in any case is written in lowercase (lift.zig's ring_keywords, read from there); a symbol (:Name), a string, a comment
     are never touched
  B  a built-in called by name is written in its one spelling (study/v48/builtin_names.py); a name the tree defines as its own
     function is the program's, not the built-in, and is left
  C  Softanza's c (text) is t and its v (any value) is x: cName -> tName, $cX -> $tX, @cX -> @tX, everywhere the token is so spelled
  L  a bare name declared in a function -- assigned, a parameter -- is lettered by what it holds (reletter's R3): n, t, a, o or x;
     never at the top level or in a class body, never a name the class declares as an attribute (in a method a bare assignment to one
     writes the attribute, and a local would change the program)
  U  Softanza's method-local spelling _name_ is unwrapped to name, then lettered by L where L letters; where it stands bare (the top
     level) and is a keyword in any case, the rename is refused -- the collision stzlib's scratch scripts did not check
A rename is REFUSED, and listed in the plan, when the new name is a keyword in any case, is already a name in that scope, or is an
attribute the class declares; the tree is then written without it.

  python port/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

# each case: a small tree, the command's answer judged by asserts on the plan (a JSON report: --json) and on the applied files
CASES = [
    ('H01', 'K', 'a keyword in another case is lowered; a symbol, a string and a comment are not', {
        'main.ring': ['If 1 = 1 See "If" Ok   # If stays in a comment', 'x = :Next', 'For i = 1 To 2 Next']},
     [("applied['main.haro']", 'if 1 = 1 FWrite(stdout, "If") end   # If stays in a comment\nx = :Next\nfor i = 1 to 2 end\n')]),
    ('H02', 'B', 'a built-in is spelled as Haro writes it; a function the tree defines is left as written', {
        'main.ring': ['? len("ab")', '? upper("a")', '? isnull(1)', 'func f', T + '? trim(" a ")'],
        'lib.ring': ['func trim x', T + 'return x']},
     [("'? Len(\"ab\")' in applied['main.haro']", True), ("'? Upper(\"a\")' in applied['main.haro']", True),
      ("'? IsEmpty(1)' in applied['main.haro']", True), ("'? trim(\" a \")' in applied['main.haro']", True)]),
    ('H03', 'C', 'Softanza\'s c is t and its v is x, the same in every file', {
        'main.ring': ['load "lib.ring"', '$cTitle = "a"', 'vAny = 1', '? Shout($cTitle)'],
        'lib.ring': ['func Shout cWord', T + 'return cWord + $cTitle']},
     [("'$tTitle = \"a\"' in applied['main.haro']", True), ("'xAny = 1' in applied['main.haro']", True),
      ("'func Shout(tWord)' in applied['lib.haro']", True), ("'return tWord + $tTitle' in applied['lib.haro']", True)]),
    ('H04', 'L', 'a bare name in a function is lettered by what it holds; the top level and a class body are not', {
        'main.ring': ['count = 1', 'func f', T + 'count = 3', T + 'name = "a"', T + 'items = [1, 2]', T + 'o = new P', T + '? count + 1',
                      'class P', T + 'size = 2']},
     [("applied['main.haro'].splitlines()[0]", 'count = 1'),
      ("'nCount = 3' in applied['main.haro'] and 'tName = \"a\"' in applied['main.haro'] and 'vItems = [1, 2]' in applied['main.haro']", True),
      ("'oO = new P' in applied['main.haro'] and '? nCount + 1' in applied['main.haro']", True),
      ("applied['main.haro'].splitlines()[-2:]", ['\tsize = 2', 'end'])]),
    ('H05', 'L', 'a method\'s bare assignment to an attribute of its class is not made a local: refused, named', {
        'main.ring': ['class P', T + 'count = 0', T + 'func Bump', T + T + 'count = count + 1']},
     [("'\\t\\tcount = count + 1' in applied['main.haro']", True),
      ("any(r['old'] == 'count' and 'attribute' in r['why'] for r in plan['refused'])", True)]),
    ('H06', 'L', 'a rename landing on a name already in the scope is refused, named', {
        'main.ring': ['func f', T + 'cName = "a"', T + 'tName = "b"', T + '? cName + tName']},
     [("'cName = \"a\"' in applied['main.haro']", True),
      ("any(r['old'] == 'cName' and r['new'] == 'tName' and 'already' in r['why'] for r in plan['refused'])", True)]),
    ('H07', 'U', 'Softanza\'s method-local _name_ is unwrapped and lettered as any local', {
        'main.ring': ['func f', T + '_count_ = 1', T + '_new_ = "a"', T + '? _count_ + 1', T + '? _new_']},
     [("'nCount = 1' in applied['main.haro'] and 'tNew = \"a\"' in applied['main.haro']", True),
      ("'? nCount + 1' in applied['main.haro'] and '? tNew' in applied['main.haro']", True)]),
    ('H08', 'U', 'an unwrapped name that stands bare and is a keyword in any case is refused, named (the _new_ -> new kind)', {
        'main.ring': ['_new_ = 1', '_Try_ = 2', '_size_ = 3', '? _new_ + _Try_ + _size_']},
     [("'_new_ = 1' in applied['main.haro'] and '_Try_ = 2' in applied['main.haro']", True),
      ("'size = 3' in applied['main.haro']", True),
      ("sorted(r['old'] for r in plan['refused'] if 'keyword' in r['why'])", ['_Try_', '_new_'])]),
    ('H09', 'C', 'a c name whose t name is a keyword-free word is renamed: tAnd is no keyword', {
        'main.ring': ['func f', T + 'cAnd = 1', T + '? cAnd']},
     [("'tAnd = 1' in applied['main.haro']", True)]),
    ('H10', '-', 'plan writes nothing; apply writes every .ring as .haro, and rewrites its loads', {
        'main.ring': ['load "lib.ring"', '? Half(4)'], 'lib.ring': ['func Half n', T + 'return n / 2']},
     [("sorted(applied)", ['lib.haro', 'main.haro']), ("applied['main.haro'].splitlines()[0]", 'load "lib.haro"'),
      ("plan_wrote", False), ("plan['files']", 2)]),
    # H12 ADDED AFTER THE TOOL, said so: H06's refusal is the tree-wide one (C); a lettered local landing on a name already in its
    # function (L) had no case
    ('H12', 'L', 'a lettered local landing on a name already in its function is refused, named', {
        'main.ring': ['func f', T + 'count = 1', T + 'nCount = 2', T + '? count + nCount']},
     [("'\\tcount = 1' in applied['main.haro']", True),
      ("any(r['old'] == 'count' and r['new'] == 'nCount' and 'already' in r['why'] for r in plan['refused'])", True)]),
    # ---- the second round (stzlib-haroport 2026-11-10 15:32), written before its code
    # HARO-PORTTOOL-ATTR-01: an attribute assigned WITH its @ in a method is no bare assignment
    ('H13', 'L', 'an attribute written with its @ in a method is no refusal; Softanza\'s c is t there too', {
        'main.ring': ['class P', T + '@cLast = ""', T + 'func Set cWhy', T + T + '@cLast = cWhy', T + 'func Get', T + T + 'return @cLast']},
     [("any(r['old'] in ('@cLast', '@tLast') for r in plan['refused'])", False),
      ("'@tLast = tWhy' in applied['main.haro']", True)]),
    # HARO-PORTTOOL-BOM-01: a load on the first line after a byte order mark
    ('H14', '-', 'a load on a first line after a byte order mark is rewritten, the mark kept', {
        'main.ring': ['﻿load "lib.ring"', '? Two()'], 'lib.ring': ['func Two', T + 'return 2']},
     [("applied['main.haro'].splitlines()[0]", '﻿load "lib.haro"')]),
    # HARO-PORTTOOL-NEXT-01 (a): $_name, a library-internal global, is $name
    ('H15', 'G', 'a $_name global is $name in every file', {
        'main.ring': ['load "lib.ring"', '$_cCount = "1"', '? Show()'], 'lib.ring': ['func Show', T + 'return $_cCount']},
     [("'$tCount = \"1\"' in applied['main.haro']", True), ("'return $tCount' in applied['lib.haro']", True)]),
    ('H16', 'G', 'a $_name landing on a $name already in the tree is refused, named', {
        'main.ring': ['$_tTotal = 1', '$tTotal = 2', '? $_tTotal + $tTotal']},
     [("'$_tTotal = 1' in applied['main.haro']", True),
      ("any(r['old'] == '$_tTotal' and 'already' in r['why'] for r in plan['refused'])", True)]),
    # (b) a call to a function the tree declares, as declared
    ('H17', 'D', 'a call to a function the tree declares is written as it is declared', {
        'main.ring': ['load "lib.ring"', '? shout("a")', '? SHOUT("b")', '? o.shout()'], 'lib.ring': ['func Shout x', T + 'return x']},
     [("'? Shout(\"a\")' in applied['main.haro'] and '? Shout(\"b\")' in applied['main.haro']", True),
      ("'? o.shout()' in applied['main.haro']", True)]),
    ('H18', 'D', 'a name the tree declares in two spellings is refused, named', {
        'main.ring': ['? mix()'], 'a.ring': ['func Mix', T + 'return 1'], 'b.ring': ['func mIX', T + 'return 2']},
     [("'? mix()' in applied['main.haro']", True),
      ("any(r['old'] == 'mix' and 'two spellings' in r['why'] for r in plan['refused'])", True)]),
    # (c) HARO-SURFACE-01: `:key = value` is the pair [:key, value]
    ('H19', 'P', ':key = value is the pair [:key, value], the value read to its depth\'s comma or bracket', {
        'main.ring': ['aX = [ :a = 1, :b = "x, y", :c = [1, 2], :d = max(3, 4) ]', '? :k = 5']},
     [("applied['main.haro'].splitlines()[0]", 'vX = [ [:a, 1], [:b, "x, y"], [:c, [1, 2]], [:d, Max(3, 4)] ]'),
      ("applied['main.haro'].splitlines()[1]", '? [:k, 5]')]),
    # (d) --unit FILE: a function only a file the unit never loads defines does not keep a built-in as it is
    ('H20', 'B', 'with --unit, a function in a file the unit never loads leaves the built-in respelled', {
        'main.ring': ['load "lib.ring"', '? len("ab")', '? half(4)'], 'lib.ring': ['func half n', T + 'return n / 2'],
        'tools/extra.ring': ['func len x', T + 'return 0']},
     [("'? Len(\"ab\")' in applied['main.haro']", True), ("'? half(4)' in applied['main.haro']", True)], 'main.ring'),
    # H21 and H22 ADDED AFTER THE SECOND ROUND'S CODE, said so: its run on stzlib 4e354d7cc found a pair whose value goes on past a line
    # ending in an operator closed at the line's end (291 statements no longer parsed), and an unwrapped _cName_ left as cName
    ('H21', 'P', 'a pair\'s value goes on past a line that ends in an operator, as Ring reads it', {
        'main.ring': ['aX = [ :q = "a" + "|" +', T + '"b", :r = 2 ]', '? aX[1][2]']},
     [("applied['main.haro'].splitlines()[0]", 'vX = [ [:q, "a" + "|" +'),
      ("applied['main.haro'].splitlines()[1]", '\t"b"], [:r, 2] ]')]),
    ('H22', 'U', 'an unwrapped _cName_ takes Softanza\'s c rule too: tName', {
        'main.ring': ['func f', T + '_cPath_ = "a"', T + '? _cPath_']},
     [("'tPath = \"a\"' in applied['main.haro'] and '? tPath' in applied['main.haro']", True)]),
    # ---- the third round (HARO-PORTTOOL-ROUND3-01, the Principal's HAROPORT-SPELLINGS-02 of 2026-11-11), written before its code
    ('H23', 'R', '(a) a parameter keeps its p mark: pc is pt, pa with an element letter is pv with it, pn and pb stay', {
        'main.ring': ['func f pcName, pnAt, pbOk, panPos, paList', T + '? pcName + pnAt', T + '? Len(panPos) + Len(paList)']},
     [("applied['main.haro'].splitlines()[0]", 'func f(ptName, pnAt, pbOk, pviPos, pxList)'),
      ("'? ptName + pnAt' in applied['main.haro'] and '? Len(pviPos) + Len(pxList)' in applied['main.haro']", True)]),
    ('H24', 'R', '(b) a b name given 1 or 0 is given true or false; a condition on a 1 or 0 literal is true or false', {
        'main.ring': ['bReady = 1', '$bDone = 0', 'func f', T + 'bOk = 1', T + 'while 1', T + T + 'exit', T + 'end', T + 'if 0', T + T + '? "no"',
                      T + 'ok', T + 'return bOk', 'class P', T + '@bOpen = 0']},
     [("applied['main.haro'].splitlines()[:4]", ['bReady = true', '$bDone = false', 'func f', '\tbOk = true']),
      ("'\\twhile true' in applied['main.haro'] and '\\tif false' in applied['main.haro'] and '\\t@bOpen = false' in applied['main.haro']", True)]),
    ('H25', 'R', '(c) Softanza\'s two-letter list letters are v and the element\'s letter', {
        'main.ring': ['func f', T + 'anPos = [1]', T + 'acNames = ["a"]', T + 'aoItems = []', T + 'aaRows = [[1]]', T + 'aList = [1]',
                      T + '? Len(anPos) + Len(acNames) + Len(aoItems) + Len(aaRows) + Len(aList)']},
     [("'viPos = [1]' in applied['main.haro'] and 'vtNames = [\"a\"]' in applied['main.haro'] and 'voItems = []' in applied['main.haro']", True),
      ("'vvRows = [[1]]' in applied['main.haro'] and 'vList = [1]' in applied['main.haro']", True)]),
    ('H26', 'R', '(d) an ALL_CAPS name takes its letter by what it holds, its capitals kept', {
        'main.ring': ['$MAX_NUMBER_SIZE = 5', '$SEP = "-"', '$RATE = 0.5', 'func f', T + '? $MAX_NUMBER_SIZE', T + '? $SEP', 'class P', T + '@NL = "n"']},
     [("'$iMAX_NUMBER_SIZE = 5' in applied['main.haro'] and '? $iMAX_NUMBER_SIZE' in applied['main.haro']", True),
      ("'$tSEP = \"-\"' in applied['main.haro'] and '$dRATE = 0.5' in applied['main.haro'] and '@tNL = \"n\"' in applied['main.haro']", True)]),
    ('H27', 'R', '(d) a capitalised attribute takes its letter first: 1 or 0 alone is a boolean, a count is a number', {
        'main.ring': ['class P', T + '@CaseSensitive = 1', T + '@Count = 0', T + '@Title = "t"', T + 'func Bump', T + T + '@Count++']},
     [("'@bCaseSensitive = true' in applied['main.haro'] and '@nCount = 0' in applied['main.haro'] and '@tTitle = \"t\"' in applied['main.haro']", True),
      ("'@nCount++' in applied['main.haro']", True)]),
    # rule O (D67, HARO-ONEFORM-01): written after the rule's code, before its commit -- said so
    ('H28', 'O', 'every block ends with end, and a definition\'s end word goes, leaving its line', {
        'main.ring': ['func f', T + 'if true', T + T + 'see "a"', T + 'ok', T + 'while false', T + 'end', T + 'switch 1', T + 'on 1 see "b"',
                      T + 'other see "c"', T + 'off', T + 'try', T + 'catch', T + 'done', T + 'if true { see "d" }', 'end', 'func g', T + 'return 1']},
     [("applied['main.haro'].count('\\tend\\n')", 4),
      ("[w for w in ('ok', 'off', 'done', 'other', '{', '}') if w in applied['main.haro']]", []),
      ("applied['main.haro'].splitlines()[14:16]", ['end', 'func g']),
      ("'\\tcase 1 FWrite(stdout, \"b\")' in applied['main.haro'] and '\\telse FWrite(stdout, \"c\")' in applied['main.haro']", True)]),
    ('H29', 'O', 'one word each, from, #, this outside a brace, parameters in parentheses and none without, no trailing period', {
        'main.ring': ['k()', 'class P', 'class Q : P', T + 'func g', T + T + '? classname(self) // the object', T + T + 'new P { see self }',
                      'def h a, b', T + 'if a && !b', T + T + 'put "x"', T + 'but a || b', T + T + 'get v', T + 'ok', 'func k()', T + 'h(1, 0).']},
     [("'class Q from P' in applied['main.haro'] and '? ClassName(this) # the object' in applied['main.haro']", True),
      ("'new P { FWrite(stdout, self) }' in applied['main.haro']", True),
      ("[l for l in applied['main.haro'].splitlines() if l.startswith(('def h(', 'def k'))]", ['def h(xA, xB)', 'def k']),
      ("' and not ' in applied['main.haro'] and ' or ' in applied['main.haro'] and '\\telseif ' in applied['main.haro']", True),
      ("'\\t\\tFWrite(stdout, \"x\")' in applied['main.haro'] and '\\t\\tgive ' in applied['main.haro'] and '\\th(1, 0)\\n' in applied['main.haro']", True)]),
    ('H30', 'O', 'a tree in every spelling ported runs on haro and prints what it printed', {
        'main.ring': ['f(2)', 'func f n', T + 'for i = 1 to n', T + T + 'if i = 1 put "a" but i = 2 see "b" ok', T + 'next',
                      T + 'switch n on 2 put "c" other put "d" off', T + 'try raise("e") catch put "f" done', T + 'if n = 2 && !(n = 3) { put "g" }',
                      T + 'put char(10)', 'end']},
     [("ran['main.haro']", "abcfg\n"), ("ran_ring['main.ring']", "abcfg\n")]),
    # v0.56 (D68): written after the rule's code, before its commit -- said so; H04, H28, H29 expect the definitions' ends by the ruling
    ('H31', 'O', 'every definition ends with end; a definition after a class is its method, def; private ends the method before it; a '
                 'one-line definition\'s body goes to its own line; the lines after a blank line keep their numbers', {
        'main.ring': ['? "top"', 'func f', T + '? 1', '', 'class P', T + 'nX = 1', T + 'func Show()   return count', T + 'func Run', T + T + '? 2',
                      'private', T + 'func Secret', T + T + '? 3', 'class Q from P']},
     [("applied['main.haro'].splitlines()[:5]", ['? "top"', 'func f', '\t? 1', 'end', 'class P']),
      ("applied['main.haro'].splitlines()[6:9]", ['\tdef Show', '\t\treturn count', '\tend']),
      ("applied['main.haro'].splitlines()[9:13]", ['\tdef Run', '\t\t? 2', '\tend', 'private']),
      ("applied['main.haro'].splitlines()[13:]", ['\tdef Secret', '\t\t? 3', '\tend', 'end', 'class Q from P', 'end'])]),
    # HARO-PORTTOOL-CHAINDOT-01 and -DIGITNAME-01 (stzlib-haroport 2026-11-11 09:54): written before their code
    ('H32', 'O', 'a dot that ends a line continues a chain: it moves to the start of the next line; a call\'s period before a keyword goes', {
        'main.ring': ['o = new P', 'o.FillQ(1).StrokeQ(2).', '  AddRect(3)', 'o.Name().', 'see "x"', 'class P',
                      'func FillQ n return self', 'func StrokeQ n return self', 'func AddRect n see n', 'func Name return "p"']},
     [("applied['main.haro'].splitlines()[1:5]", ['o.FillQ(1).StrokeQ(2)', '  .AddRect(3)', 'o.Name()', 'FWrite(stdout, "x")'])]),
    ('H33', 'O', 'a definition whose name starts with a digit loses its empty parentheses', {
        'main.ring': ['func 2Hearts()', '  return 2', 'func 3Ways(n)', '  return n']},
     [("[l for l in applied['main.haro'].splitlines() if 'Hearts' in l or 'Ways' in l]", ['func 2Hearts', 'func 3Ways(xN)'])]),
    # v0.57 (D69): written before its code
    ('H34', 'O', 'see and put: a line that ends with + nl prints with print, any other writes through the stream', {
        'main.ring': ['see "a" + nl', 'put "b"', 'x = 2', 'see x', '  see "c" + x + nl  # a comment', '? "d"']},
     [("applied['main.haro'].splitlines()[:2]", ['print "a"', 'FWrite(stdout, "b")']),
      ("applied['main.haro'].splitlines()[3:6]", ['FWrite(stdout, x)', '  print "c" + x  # a comment', '? "d"'])]),
    # v0.59 (D71): written before its code
    ('H35', 'N', 'null is written "", and isnull is IsEmpty', {
        'main.ring': ['x = null', 'if isnull(x) see "e" ok', 'o.isnull()', 'y = :null']},
     [("applied['main.haro'].splitlines()[:2]", ['x = ""', 'if IsEmpty(x) FWrite(stdout, "e") end']),
      ("'o.isnull()' in applied['main.haro'] and 'y = :null' in applied['main.haro']", True)]),
    # HARO-PORTTOOL-CALLNAME-01 and -NAMETEXT-01 (stzlib-haroport, 2026-11-12): written before their code
    ('H36', 'L', 'a parameter named like a built-in is lettered, and the call of that built-in keeps its name', {
        'main.ring': ['? ring_substr1("abc", "b")', 'func ring_substr1 str, substr', T + 'return substr(str, substr)']},
     [("'return SubStr(tStr, tSubstr)' in applied['main.haro'] or 'return SubStr(xStr, xSubstr)' in applied['main.haro']", True)]),
    ('H37', 'C', 'a global named in text or as a symbol follows its rename', {
        'main.ring': ['$cDenyFile = "x"', '$_logo = 1', '? isglobal("$cDenyFile")', '? isglobal(:$_logo)', "? isglobal('$cDenyFile')"]},
     [("'IsGlobal(\"$tDenyFile\")' in applied['main.haro'] and \"IsGlobal('$tDenyFile')\" in applied['main.haro']", True),
      ("'IsGlobal(:$logo)' in applied['main.haro']", True)]),
    # ---- v0.61 (D73, TYPES.md T6, the Principal's "Start structure"), written before rule A's code. Changed by the same ruling, and
    # said so: H04 and H25 (a list is v: vItems, vList), H19 and H21 (Softanza's aX given only a list literal is vX), H23 (paList, a
    # parameter the tree never assigns, is pxList)
    ('H38', 'A', 'a name lettered a is v when the tree gives it only list literals, x otherwise; a global and a parameter alike', {
        'main.ring': ['$aCfg = []', 'aRows = [1]', 'aRows = rows()', 'func f paItems', T + 'aSeen = [1]', T + 'aSeen + 2',
                      T + 'return Len(paItems) + Len(aSeen) + Len($aCfg)', 'func rows', T + 'return [2]']},
     [("applied['main.haro'].splitlines()[:3]", ['$vCfg = []', 'xRows = [1]', 'xRows = rows()']),
      ("'func f(pxItems)' in applied['main.haro'] and 'vSeen = [1]' in applied['main.haro']", True),
      ("'return Len(pxItems) + Len(vSeen) + Len($vCfg)' in applied['main.haro']", True)]),
    ('H39', 'A', 'an a name whose new name is another rename\'s is refused and left: vResult -> xResult beside aResult', {
        'main.ring': ['func f', T + 'vResult = 1', T + 'return vResult', 'func g', T + 'aResult = f()', T + 'return aResult']},
     [("'xResult = 1' in applied['main.haro'] and 'aResult = f()' in applied['main.haro']", True),
      ("any(r['old'] == 'aResult' and r['new'] == 'xResult' for r in plan['refused'])", True)]),
    # HARO-PORTTOOL-UNDERSCORE-01 (stzlib-haroport, 2026-11-12), before its code: rule B read a definition's own name as a call and looked
    # it up with its underscores removed, so stzPattern's `def _Number()` became `def Number` and this._Number() met R14
    ('H40', 'B', 'a definition\'s own name is never respelled as a built-in, nor a name with a leading underscore', {
        'main.ring': ['o = new P', '? o._Number() + o.len()', '? _Number()', 'func _Number()', T + 'return 5', 'class P',
                      'def _Number()', T + 'return 1', 'def len()', T + 'return 2', 'def _Len()', T + 'return 3', 'def Twice()',
                      T + 'return _Len() * 2']},
     [("'def _Number' in applied['main.haro'] and 'def len' in applied['main.haro']", True),
      ("'? _Number()' in applied['main.haro'] and 'func _Number' in applied['main.haro']", True),
      # a bare call of an underscore method, no top-level function of its name: added after plant T65 missed, said so
      ("'return _Len() * 2' in applied['main.haro']", True)]),
    # v0.66 (D78, HARO-NUMBERS-CORE-01), before its code: fabs is Abs, dec is FromHex, and a decimals(n) setting -- which Haro has none
    # of -- is listed for its writer, who moves the places to the values written
    ('H41', 'N', 'fabs is Abs, dec is FromHex, and a decimals(n) setting is listed for its writer', {
        'main.ring': ['? fabs(-2)', '? dec("ff")', 'decimals(3)', '? 1/3']},
     [("'? Abs(-2)' in applied['main.haro'] and '? FromHex(\"ff\")' in applied['main.haro']", True),
      ("any(r['old'] == 'decimals(3)' and 'Text(x, iPlaces)' in r['why'] for r in plan['refused'])", True)]),
    ('H11', '-', 'the ported tree runs on haro and prints what the classic Ring surface printed', {
        'main.ring': ['load "lib.ring"', 'cName = Greet("ada")', '? cName', '? Len(cName)'],
        'lib.ring': ['func Greet cWho', T + 'cOut = "hi " + cWho', T + 'return cOut']},
     [("ran['main.haro']", "hi ada\n6\n"), ("ran_ring['main.ring']", "hi ada\n6\n")]),
]


def main():
    out = []
    for case in CASES:
        cid, line, why, tree, asserts = case[:5]
        unit = case[5] if len(case) > 5 else None
        folder = os.path.join(HERE, 'cases', cid)
        os.makedirs(folder, exist_ok=True)
        for name, lines in tree.items():
            os.makedirs(os.path.dirname(os.path.join(folder, name)), exist_ok=True)
            with open(os.path.join(folder, name), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(lines) + '\n')
        row = {'id': cid, 'line': line, 'why': why, 'folder': 'cases/' + cid, 'files': sorted(tree),
               'asserts': [[e, v] for e, v in asserts]}
        if unit:
            row['unit'] = unit
        out.append(row)
    doc = {'tool': 'port/haroport.py', 'ask': 'HARO-PORTTOOL-01 (stzlib-haroport, 2026-11-10)',
           'class': 'each case: `plan ROOT --json` read as `plan` (and `plan_wrote`: whether it wrote any file), `apply ROOT --out DIR` read '
                    'as `applied` (published name -> text); for H11 each tree run on haro: `ran` (the ported) and `ran_ring` (the original)',
           'cases': out}
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
