# expr_lib.ring -- the generic court AND evaluator of a declared EXPRESSION
# language (Haro v0.5), in pure core Ring.
#
# A court FORGED from a .haro declaration that holds an EXPRESSION loads this
# file and fills five tables (see forge.ring): the language's name, its
# OPERATORS and OPERANDS (words of the closed menus), its VARIABLES, and its
# CONTEXTS -- the seats a host offers the expression, each with the variables
# it admits. The grammar is W's (stz/declarative/w/GRAMMAR.md), the one
# expression shape the estate declares: or < and < not < comparison < additive
# < multiplicative < unary < primary. What the declaration does NOT admit --
# an operator outside its menu, an operand kind outside its menu, a variable
# outside the seat -- is refused at compile time, by name, never answered nil.
#
#   <court>.ring check <seat> "<expr>"                  ok | refused: why
#   <court>.ring eval  <seat> "<expr>" [input] [init]    the value, as JSON
#
# The seats a host gives a list expression -- eval, map, filter, count,
# partition, groupby, reduce, reduce_noinit -- are the harness's operations
# (stz's list face, experiment/run_w.luau), implemented here once so the
# forged evaluator can be judged by W's own fixtures unadapted. Numbers are
# the host's numbers (Ring's doubles); a comparison answers 1 or 0; a string
# is always true, as on the Luau host.
#
# Functions only. Globals ($cExprLang, $aExprOperators, $aExprOperands,
# $aExprVariables, $aExprContexts, $aExprToks, $nExprPos, $aExprAllowed) are
# born in the generated court, at its top level, for both runtimes' sake.

func ExInList(cS, aL)
	for i = 1 to len(aL)
		if aL[i] = cS return 1 ok
	next
	return 0

func ExFail(cMsg)
	raise($cExprLang + ": " + cMsg)

# ---- character classes by byte code (HF-30) ----------------------------------

func ExIsDigit(c)
	n = ascii(c)
	return (n >= 48 and n <= 57)

func ExIsAlpha(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or (n >= 65 and n <= 90)

func ExIsNameChar(c)
	return ExIsAlpha(c) or ExIsDigit(c) or c = "_"

# ---- tokenizer: [type, text]; types: num str var and or not cmp op lparen rparen
func ExTokenize(cS)
	aT = []
	n = len(cS)
	i = 1
	while i <= n
		c = cS[i]
		if c = " " or c = char(9) or c = char(13) or c = char(10)
			i++
		but ExIsDigit(c)
			j = i
			while j <= n and (ExIsDigit(cS[j]) or cS[j] = ".")
				j++
			end
			cNum = substr(cS, i, j - i)
			nDots = 0
			for k = 1 to len(cNum)
				if cNum[k] = "." nDots++ ok
			next
			if nDots > 1 or cNum[len(cNum)] = "." ExFail("bad number '" + cNum + "'") ok
			aT + ["num", cNum]
			i = j
		but c = "'" or c = '"'
			j = i + 1
			while j <= n and cS[j] != c
				j++
			end
			if j > n ExFail("unterminated string starting at '" + substr(cS, i) + "'") ok
			aT + ["str", substr(cS, i + 1, j - i - 1)]
			i = j + 1
		but c = "@"
			j = i + 1
			if j > n or not ExIsAlpha(cS[j]) ExFail("'@' must be followed by a variable name") ok
			while j <= n and ExIsNameChar(cS[j])
				j++
			end
			aT + ["var", lower(substr(cS, i + 1, j - i - 1))]
			i = j
		but ExIsAlpha(c)
			j = i
			while j <= n and ExIsNameChar(cS[j])
				j++
			end
			cW = substr(cS, i, j - i)
			cL = lower(cW)
			if cL = "and" or cL = "or" or cL = "not"
				aT + [cL, cL]
			else
				ExFail("'" + cW + "' is not part of the " + $cExprLang + " grammar -- no calls, no host names")
			ok
			i = j
		else
			cTwo = ""
			if i < n cTwo = substr(cS, i, 2) ok
			if cTwo = ">=" or cTwo = "<=" or cTwo = "!=" or cTwo = "<>"
				if cTwo = "<>" cTwo = "!=" ok
				aT + ["cmp", cTwo]
				i += 2
			but c = "=" or c = ">" or c = "<"
				aT + ["cmp", c]
				i++
			but c = "+" or c = "-" or c = "*" or c = "/" or c = "%"
				aT + ["op", c]
				i++
			but c = "("
				aT + ["lparen", c]
				i++
			but c = ")"
				aT + ["rparen", c]
				i++
			else
				ExFail("character '" + c + "' is not part of the " + $cExprLang + " grammar")
			ok
		ok
	end
	aT + ["eof", ""]
	return aT

func ExPeek()
	return $aExprToks[$nExprPos]

func ExTake()
	t = $aExprToks[$nExprPos]
	if t[1] != "eof" $nExprPos++ ok
	return t

# the menu word an operator token stands for, and whether the menu admits it
func ExWantOperator(cMenuWord, cShown)
	if not ExInList(cMenuWord, $aExprOperators)
		ExFail("'" + cShown + "' is not an operator of " + $cExprLang + " (its menu: " + ExJoin($aExprOperators, ", ") + ")")
	ok

func ExWantOperand(cMenuWord, cShown)
	if not ExInList(cMenuWord, $aExprOperands)
		ExFail("'" + cShown + "' is not an operand of " + $cExprLang + " (its menu: " + ExJoin($aExprOperands, ", ") + ")")
	ok

func ExJoin(aL, cSep)
	cOut = ""
	for i = 1 to len(aL)
		if i > 1 cOut += cSep ok
		cOut += aL[i]
	next
	return cOut

# ---- parser: one function per grammar rule; nodes are lists --------------------
#   ["num", n] ["str", s] ["var", name] ["neg", l] ["arith", op, l, r]
#   ["cmp", op, l, r] ["not", l] ["and", l, r] ["or", l, r]
# A node is built in a fresh variable and assigned after (HF-36).

func ExParse(cS, aAllowed)
	$aExprToks = ExTokenize(cS)
	$nExprPos = 1
	$aExprAllowed = aAllowed
	if ExPeek()[1] = "eof" ExFail("empty expression") ok
	aRoot = ExOr()
	if ExPeek()[1] != "eof"
		ExFail("trailing input from '" + ExPeek()[2] + "'")
	ok
	return aRoot

func ExPrimary()
	t = ExPeek()
	if t[1] = "eof" ExFail("expression ends where a value was expected") ok
	if t[1] = "num"
		ExTake()
		ExWantOperand("number", t[2])
		return ["num", 0 + t[2]]
	ok
	if t[1] = "str"
		ExTake()
		ExWantOperand("text", "'" + t[2] + "'")
		return ["str", t[2]]
	ok
	if t[1] = "var"
		ExTake()
		ExWantOperand("var", "@" + t[2])
		if not ExInList(t[2], $aExprAllowed)
			ExFail("unknown variable @" + t[2] + " in this seat")
		ok
		return ["var", t[2]]
	ok
	if t[1] = "lparen"
		ExTake()
		aInner = ExOr()
		if ExPeek()[1] != "rparen" ExFail("unclosed '('") ok
		ExTake()
		return aInner
	ok
	ExFail("unexpected '" + t[2] + "'")

func ExUnary()
	t = ExPeek()
	if t[1] = "op" and t[2] = "-"
		ExTake()
		ExWantOperator("neg", "-")
		aInner = ExUnary()
		aNode = ["neg", aInner]
		return aNode
	ok
	return ExPrimary()

func ExMul()
	aL = ExUnary()
	while 1
		t = ExPeek()
		if t[1] != "op" exit ok
		if t[2] != "*" and t[2] != "/" and t[2] != "%" exit ok
		ExTake()
		cWord = "mul"
		if t[2] = "/" cWord = "div" ok
		if t[2] = "%" cWord = "mod" ok
		ExWantOperator(cWord, t[2])
		aR = ExUnary()
		aNode = ["arith", t[2], aL, aR]
		aL = aNode
	end
	return aL

func ExAdd()
	aL = ExMul()
	while 1
		t = ExPeek()
		if t[1] != "op" exit ok
		if t[2] != "+" and t[2] != "-" exit ok
		ExTake()
		cWord = "add"
		if t[2] = "-" cWord = "sub" ok
		ExWantOperator(cWord, t[2])
		aR = ExMul()
		aNode = ["arith", t[2], aL, aR]
		aL = aNode
	end
	return aL

func ExComparison()
	aL = ExAdd()
	t = ExPeek()
	if t[1] = "cmp"
		ExTake()
		ExWantOperator("cmp", t[2])
		aR = ExAdd()
		aNode = ["cmp", t[2], aL, aR]
		return aNode
	ok
	return aL

func ExNot()
	t = ExPeek()
	if t[1] = "not"
		ExTake()
		ExWantOperator("not", "not")
		aInner = ExNot()
		aNode = ["not", aInner]
		return aNode
	ok
	return ExComparison()

func ExAnd()
	aL = ExNot()
	while ExPeek()[1] = "and"
		ExTake()
		ExWantOperator("and", "and")
		aR = ExNot()
		aNode = ["and", aL, aR]
		aL = aNode
	end
	return aL

func ExOr()
	aL = ExAnd()
	while ExPeek()[1] = "or"
		ExTake()
		ExWantOperator("or", "or")
		aR = ExAnd()
		aNode = ["or", aL, aR]
		aL = aNode
	end
	return aL

# ---- evaluator: env is [[name, value], ...]; a comparison answers 1 or 0 --------

func ExTruthy(v)
	if isNumber(v) return v != 0 ok
	if isString(v) return 1 ok
	if isList(v) return 1 ok
	return 0

func ExEnvGet(aEnv, cName)
	for i = 1 to len(aEnv)
		if aEnv[i][1] = cName return aEnv[i][2] ok
	next
	return 0

func ExEval(aNode, aEnv)
	cK = aNode[1]
	if cK = "num" or cK = "str" return aNode[2] ok
	if cK = "var" return ExEnvGet(aEnv, aNode[2]) ok
	if cK = "neg" return -ExEval(aNode[2], aEnv) ok
	if cK = "arith"
		a = ExEval(aNode[3], aEnv)
		b = ExEval(aNode[4], aEnv)
		op = aNode[2]
		if op = "+" return a + b ok
		if op = "-" return a - b ok
		if op = "*" return a * b ok
		if op = "/" return a / b ok
		return a % b
	ok
	if cK = "cmp"
		a = ExEval(aNode[3], aEnv)
		b = ExEval(aNode[4], aEnv)
		op = aNode[2]
		if op = "="
			if ExSame(a, b) return 1 ok
			return 0
		ok
		if op = "!="
			if ExSame(a, b) return 0 ok
			return 1
		ok
		if op = ">"
			if a > b return 1 ok
			return 0
		ok
		if op = "<"
			if a < b return 1 ok
			return 0
		ok
		if op = ">="
			if a >= b return 1 ok
			return 0
		ok
		if a <= b return 1 ok
		return 0
	ok
	if cK = "not"
		if ExTruthy(ExEval(aNode[2], aEnv)) return 0 ok
		return 1
	ok
	if cK = "and"
		if not ExTruthy(ExEval(aNode[2], aEnv)) return 0 ok
		if ExTruthy(ExEval(aNode[3], aEnv)) return 1 ok
		return 0
	ok
	if cK = "or"
		if ExTruthy(ExEval(aNode[2], aEnv)) return 1 ok
		if ExTruthy(ExEval(aNode[3], aEnv)) return 1 ok
		return 0
	ok
	ExFail("internal -- unknown node kind " + cK)

# equality by value and by kind: a number and a string are never equal (W's
# rule on the Luau host), whatever the host's own = would say
func ExSame(a, b)
	if isNumber(a) and isNumber(b) return a = b ok
	if isString(a) and isString(b) return a = b ok
	return 0

# ---- the seats -------------------------------------------------------------------

# the variables a seat admits: its CONTEXTS entry, or every VARIABLE when the
# declaration names no contexts
func ExAllowedIn(cSeat)
	if len($aExprContexts) = 0 return $aExprVariables ok
	for i = 1 to len($aExprContexts)
		if $aExprContexts[i][1] = cSeat return $aExprContexts[i][2] ok
	next
	ExFail("no seat '" + cSeat + "' in " + $cExprLang + " (its seats: " + ExJoin(ExSeatNames(), ", ") + ")")

func ExSeatNames()
	aN = []
	for i = 1 to len($aExprContexts)
		aN + $aExprContexts[i][1]
	next
	return aN

# ---- JSON, the harness's exchange form ---------------------------------------------

func ExNumText(n)
	cS = "" + n
	if substr(cS, ".") > 0
		while len(cS) > 1 and cS[len(cS)] = "0"
			cS = left(cS, len(cS) - 1)
		end
		if cS[len(cS)] = "." cS = left(cS, len(cS) - 1) ok
	ok
	return cS

func ExJson(v)
	if isNumber(v) return ExNumText(v) ok
	if isString(v) return '"' + v + '"' ok
	if isList(v)
		cOut = "["
		for i = 1 to len(v)
			if i > 1 cOut += ", " ok
			cOut += ExJson(v[i])
		next
		return cOut + "]"
	ok
	return "null"

# a small reader: numbers, strings, lists; $aExprToks/$nExprPos reused as the cursor
func ExJsonParse(cS)
	$aExprToks = cS
	$nExprPos = 1
	v = ExJsonValue()
	ExJsonWs()
	if $nExprPos <= len(cS) ExFail("input: trailing text at " + $nExprPos) ok
	return v

func ExJsonWs()
	while $nExprPos <= len($aExprToks) and ($aExprToks[$nExprPos] = " " or $aExprToks[$nExprPos] = char(9) or $aExprToks[$nExprPos] = char(10) or $aExprToks[$nExprPos] = char(13))
		$nExprPos++
	end

func ExJsonValue()
	ExJsonWs()
	cS = $aExprToks
	if $nExprPos > len(cS) ExFail("input: a value was expected") ok
	c = cS[$nExprPos]
	if c = "["
		$nExprPos++
		aOut = []
		ExJsonWs()
		if $nExprPos <= len(cS) and cS[$nExprPos] = "]"
			$nExprPos++
			return aOut
		ok
		while 1
			aOut + ExJsonValue()
			ExJsonWs()
			if $nExprPos > len(cS) ExFail("input: unclosed '['") ok
			if cS[$nExprPos] = ","
				$nExprPos++
			but cS[$nExprPos] = "]"
				$nExprPos++
				return aOut
			else
				ExFail("input: expected ',' or ']'")
			ok
		end
	ok
	if c = '"'
		j = $nExprPos + 1
		while j <= len(cS) and cS[j] != '"'
			j++
		end
		if j > len(cS) ExFail("input: unterminated string") ok
		v = substr(cS, $nExprPos + 1, j - $nExprPos - 1)
		$nExprPos = j + 1
		return v
	ok
	j = $nExprPos
	if cS[j] = "-" j++ ok
	while j <= len(cS) and (ExIsDigit(cS[j]) or cS[j] = ".")
		j++
	end
	if j = $nExprPos ExFail("input: unexpected '" + c + "'") ok
	v = 0 + substr(cS, $nExprPos, j - $nExprPos)
	$nExprPos = j
	return v

# ---- the command: check <seat> "<expr>" | eval <seat> "<expr>" [input] [init] ------

func ExRun(cSeat, cExpr, aInput, vInit, bHasInit)
	aAllowed = ExAllowedIn(cSeat)
	aAst = ExParse(cExpr, aAllowed)
	if cSeat = "eval" return ExEval(aAst, []) ok
	if cSeat = "map"
		aOut = []
		for i = 1 to len(aInput)
			aOut + ExEval(aAst, [["item", aInput[i]]])
		next
		return aOut
	ok
	if cSeat = "filter"
		aOut = []
		for i = 1 to len(aInput)
			if ExTruthy(ExEval(aAst, [["item", aInput[i]]])) aOut + aInput[i] ok
		next
		return aOut
	ok
	if cSeat = "count"
		n = 0
		for i = 1 to len(aInput)
			if ExTruthy(ExEval(aAst, [["item", aInput[i]]])) n++ ok
		next
		return n
	ok
	if cSeat = "partition"
		aYes = []
		aNo = []
		for i = 1 to len(aInput)
			if ExTruthy(ExEval(aAst, [["item", aInput[i]]]))
				aYes + aInput[i]
			else
				aNo + aInput[i]
			ok
		next
		return [aYes, aNo]
	ok
	if cSeat = "groupby"
		aGroups = []
		for i = 1 to len(aInput)
			k = ExEval(aAst, [["item", aInput[i]]])
			cKey = "" + k
			if isNumber(k) cKey = ExNumText(k) ok
			nAt = 0
			for j = 1 to len(aGroups)
				if aGroups[j][1] = cKey nAt = j ok
			next
			if nAt = 0
				aGroups + [cKey, [aInput[i]]]
			else
				aGroups[nAt][2] + aInput[i]
			ok
		next
		return aGroups
	ok
	if cSeat = "reduce" or cSeat = "reduce_noinit"
		nStart = 1
		acc = vInit
		if not bHasInit
			if len(aInput) = 0 ExFail("reduce without an initial value needs one item") ok
			acc = aInput[1]
			nStart = 2
		ok
		for i = nStart to len(aInput)
			acc = ExEval(aAst, [["accumulator", acc], ["item", aInput[i]]])
		next
		return acc
	ok
	# a seat the declaration names and this harness has no operation for:
	# judged, and evaluated once with no variable bound
	return ExEval(aAst, [])

func ExMain()
	if len(sysargv) < 5
		? "usage: <court>.ring check <seat> <expr> | eval <seat> <expr> [input] [init]"
		return
	ok
	cVerb = sysargv[3]
	cSeat = sysargv[4]
	cExpr = sysargv[5]
	try
		if cVerb = "check"
			ExParse(cExpr, ExAllowedIn(cSeat))
			? "ok"
		but cVerb = "eval"
			aInput = []
			if len(sysargv) >= 6 aInput = ExJsonParse(sysargv[6]) ok
			vInit = 0
			bHasInit = 0
			if len(sysargv) >= 7
				vInit = ExJsonParse(sysargv[7])
				bHasInit = 1
			ok
			? ExJson(ExRun(cSeat, cExpr, aInput, vInit, bHasInit))
		else
			? "unknown verb '" + cVerb + "'; this court answers: check, eval"
		ok
	catch
		? "refused: " + cCatchError
	done
