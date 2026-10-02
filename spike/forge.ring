# forge.ring -- `rnxc forge.ring <file.haro> <out dir>`: the forge's smallest act.
#
# Reads a language declaration with the stzu meta-court (haro_lib.ring) and
# EMITS, into <out dir>:
#   <lang>_court.ring   a court for the declared language: this generated
#                       program loads court_lib.ring and carries the
#                       declaration as tables; `rnxc <lang>_court.ring check
#                       <file>` judges a sentence of the language
#   <lang>.gbnf         the language's grammar for the engine's constrained
#                       decoder (contract C9), in the llama.cpp dialect
#                       gbnf_machine.zig reads
# Pure core Ring; runs on rnx and on the oracle alike.

load "haro_lib.ring"

$aStzuToks = []
$aStzuUnions = []
$nStzuPos = 1
$aCondToks = []
$nCondPos = 1
$aCondDeclSeats = []
$aCondDecls = []
$aCondVerbOf = []
$cCondOther = ""
$aCondRefSeats = []
$aCondFormats = []
$bCondUnread = 0
$aCondLangs = []
$cCondLang = ""
$aCourtSentences = []
$cStzuDir = ""

# The top level's names are its own (cInPath, cOutDir, ...): on Ring a
# function's bare assignment to a name that exists as a global WRITES THE
# GLOBAL (Ring, Judged by the Record, 2.7; Rule A's hazard), and the first
# version of this file lost its output directory to a helper's `cOut`
# while rnxc, under Rule A, ran it correctly (HF-33).
if len(sysargv) < 4
	? "usage: forge.ring <file.haro> <out dir>"
else
	cInPath = sysargv[3]
	cOutDir = sysargv[4]
	cStzuText = read(cInPath)
	$cStzuDir = StzuDirOf(cInPath)
	try
		aForgedLang = StzuDeclare(cStzuText)
		cLangName = LangGet(aForgedLang, "name")
		cForgedWhat = ""
		if len(LangGet(aForgedLang, "declarations")) > 0 or len(LangGet(aForgedLang, "expressions")) = 0
			cCourtText = ForgeCourt(aForgedLang)
			cGbnfText = ForgeGbnf(aForgedLang)
			write(cOutDir + "/" + cLangName + "_court.ring", cCourtText)
			write(cOutDir + "/" + cLangName + ".gbnf", cGbnfText)
			# a string first: a number on the left of + would read the string as a number (R41)
			cForgedWhat = "" + len(LangGet(aForgedLang, "declarations")) + " kinds, " +
			  len(LangGet(aForgedLang, "forms")) + " forms, " + len(LangGet(aForgedLang, "refusals")) + " refusals -> " +
			  cLangName + "_court.ring, " + cLangName + ".gbnf"
		ok
		# v0.5: an EXPRESSION language is forged whole -- its court and its
		# evaluator -- into <lang>_expr.ring, and its grammar into <lang>_expr.gbnf
		if len(LangGet(aForgedLang, "expressions")) > 0
			write(cOutDir + "/" + cLangName + "_expr.ring", ForgeExprCourt(aForgedLang))
			write(cOutDir + "/" + cLangName + "_expr.gbnf", ForgeExprGbnf(aForgedLang))
			if cForgedWhat != "" cForgedWhat += "; " ok
			cForgedWhat += "" + len(LangGet(aForgedLang, "expressions")) + " expression(s) -> " + cLangName + "_expr.ring, " + cLangName + "_expr.gbnf"
		ok
		# v0.7: an ASK's question grammar, for the decoder
		if not isNull(LangGet(aForgedLang, "ask"))
			write(cOutDir + "/" + cLangName + "_ask.gbnf", ForgeAskGbnf(aForgedLang))
			if cForgedWhat != "" cForgedWhat += "; " ok
			cForgedWhat += "1 ask -> " + cLangName + "_ask.gbnf"
		ok
		? "forged " + cLangName + ": " + cForgedWhat
	catch
		? cCatchError
	done
ok

# ---- the court, as Ring source -----------------------------------------------

func RingStr(cS)
	# a Ring string literal; the Commons allows no escapes and no double
	# quote inside a string, so double quotes are safe delimiters unless the
	# text holds one, in which case single quotes are used
	if substr(cS, '"') > 0 return "'" + cS + "'" ok
	return '"' + cS + '"'

# what a seat's type name resolves to in the language: prim form expr menu range
# format decl union sentence -- the meta-court's own answer (haro_lib.ring)
func TypeKindOf(aLang, cOf)
	return StzuTypeKindOf(aLang, cOf)

func UnionOf(aLang, cName)
	aU = LangGet(aLang, "unions")
	for i = 1 to len(aU)
		if aU[i][1] = cName return aU[i] ok
	next
	return NULL

# a declaration's MESSAGES as [[seat, text], ...]
func MessagesSource(aMsgs)
	cBuf = "["
	for i = 1 to len(aMsgs)
		if i > 1 cBuf += ", " ok
		cBuf += "[" + RingStr(aMsgs[i][1]) + ", " + RingStr(aMsgs[i][2]) + "]"
	next
	return cBuf + "]"

# a union's alternatives as [[of, isList, typeKind], ...]
func AltsSource(aLang, aAlts)
	cBuf = "["
	for i = 1 to len(aAlts)
		if i > 1 cBuf += ", " ok
		cBuf += "[" + RingStr(aAlts[i][1]) + ", " + aAlts[i][2] + ", " + RingStr(TypeKindOf(aLang, aAlts[i][1])) + "]"
	next
	return cBuf + "]"

# a seat in the court's table is [name, of, isList, optional, typeKind]
func SeatsSource(aLang, aSeats)
	cBuf = "["
	for i = 1 to len(aSeats)
		if i > 1 cBuf += ", " ok
		cBuf += "[" + RingStr(aSeats[i][1]) + ", " + RingStr(aSeats[i][2]) + ", " + aSeats[i][3] + ", " + aSeats[i][4] + ", " + RingStr(TypeKindOf(aLang, aSeats[i][2])) + "]"
	next
	return cBuf + "]"

func NamesSource(aNames)
	cBuf = "["
	for i = 1 to len(aNames)
		if i > 1 cBuf += ", " ok
		cBuf += RingStr(aNames[i])
	next
	return cBuf + "]"

func PointsSource(aPoints)
	cBuf = "["
	for i = 1 to len(aPoints)
		if i > 1 cBuf += ", " ok
		cBuf += "[" + RingStr(aPoints[i][1] + "." + aPoints[i][2]) + ", " + RingStr(aPoints[i][3]) + "]"
	next
	return cBuf + "]"

# a table of rows as a Ring list literal, one row a line; fnRow is applied by the
# caller, so this takes the rows' texts
func RowsSource(aRows, nl)
	c = "[" + nl
	for i = 1 to len(aRows)
		c += "      " + aRows[i]
		if i < len(aRows) c += "," ok
		c += nl
	next
	return c + "    ]"

# an EXPRESSION's tables as the court reads them (v0.6): [name, ops, opds,
# aggs, vars, contexts, absent, division, equality]
func ExprSource(aE)
	aAgg = aE[4]
	if isNull(aAgg) aAgg = [] ok
	aVars = aE[5]
	if isNull(aVars) aVars = [] ok
	aCtx = []
	if len(aE) >= 8 aCtx = aE[8] ok
	cCtx = "["
	for i = 1 to len(aCtx)
		if i > 1 cCtx += ", " ok
		cCtx += "[" + RingStr(aCtx[i][1]) + ", " + NamesSource(aCtx[i][2]) + "]"
	next
	cCtx += "]"
	cAbsent = "" cDivision = "" cEquality = ""
	if len(aE) >= 11
		cAbsent = aE[9]
		cDivision = aE[10]
		cEquality = aE[11]
	ok
	return "[" + RingStr(aE[1]) + ", " + NamesSource(aE[2]) + ", " + NamesSource(aE[3]) + ", " + NamesSource(aAgg) + ", " +
	       NamesSource(aVars) + ", " + cCtx + ", " + RingStr(cAbsent) + ", " + RingStr(cDivision) + ", " + RingStr(cEquality) + "]"

# a WALK as the court reads it (v0.6): [name, of, steps, through, order,
# guards, compute, formula, fail]
func WalkSource(aW)
	aPaths = []
	for i = 1 to len(aW[6])
		aPaths + aW[6][i][1]
	next
	return "[" + RingStr(aW[1]) + ", " + RingStr(aW[2]) + ", " + RingStr(aW[3]) + ", " + RingStr(aW[4]) + ", " + RingStr(aW[5]) + ", " +
	       NamesSource(aPaths) + ", " + RingStr(aW[7]) + ", " + RingStr(aW[8]) + ", " + RingStr(aW[9]) + "]"

# one language's record, as the court reads it (v0.4, grown in v0.6 and v0.7):
# [name, ext, kinds, forms, refusals, menus, ranges, formats, unions,
# constraints, world, points, floors, views, sentences, expressions, walks, ask, run]
func LangSource(aLang)
	nl = char(10)
	aRows = []
	aD = LangGet(aLang, "declarations")
	for i = 1 to len(aD)
		aRows + ("[" + RingStr(aD[i][2]) + ", " + RingStr(aD[i][1]) + ", " + SeatsSource(aLang, aD[i][3]) + ", " + RingStr(aD[i][6]) + ", " + MessagesSource(aD[i][7]) + "]")
	next
	cKinds = RowsSource(aRows, nl)
	aRows = []
	aF = LangGet(aLang, "forms")
	for i = 1 to len(aF)
		aRows + ("[" + RingStr(aF[i][1]) + ", " + SeatsSource(aLang, aF[i][2]) + "]")
	next
	cForms = RowsSource(aRows, nl)
	aRows = []
	aR = LangGet(aLang, "refusals")
	for i = 1 to len(aR)
		aNamed = []
		if len(aR[i]) >= 5 aNamed = aR[i][5] ok
		aRows + ("[" + RingStr(aR[i][1]) + ", " + RingStr(aR[i][2]) + ", " + MessagesSource(aNamed) + "]")
	next
	cRefusals = RowsSource(aRows, nl)
	aRows = []
	aM = LangGet(aLang, "menus")
	for i = 1 to len(aM)
		aRows + ("[" + RingStr(aM[i][1]) + ", " + NamesSource(aM[i][2]) + ", " + RingStr(aM[i][3]) + "]")
	next
	cMenus = RowsSource(aRows, nl)
	aRows = []
	aRg = LangGet(aLang, "ranges")
	for i = 1 to len(aRg)
		aRows + ("[" + RingStr(aRg[i][1]) + ", " + aRg[i][2] + ", " + aRg[i][3] + ", " + RingStr(aRg[i][4]) + "]")
	next
	cRanges = RowsSource(aRows, nl)
	aRows = []
	aFm = LangGet(aLang, "formats")
	for i = 1 to len(aFm)
		cFold = ""
		if len(aFm[i]) >= 5 cFold = aFm[i][5] ok
		aRows + ("[" + RingStr(aFm[i][1]) + ", " + RingStr(aFm[i][2]) + ", " + RingStr(aFm[i][3]) + ", " + RingStr(cFold) + "]")
	next
	cFormats = RowsSource(aRows, nl)
	aRows = []
	aU = LangGet(aLang, "unions")
	for i = 1 to len(aU)
		aRows + ("[" + RingStr(aU[i][1]) + ", " + AltsSource(aLang, aU[i][2]) + ", " + RingStr(aU[i][3]) + "]")
	next
	cUnions = RowsSource(aRows, nl)
	aRows = []
	aC = LangGet(aLang, "constraints")
	for i = 1 to len(aC)
		aRows + ("[" + RingStr(aC[i][1]) + ", " + RingStr(aC[i][2]) + ", " + RingStr(aC[i][3]) + ", " + RingStr(aC[i][4]) + ", " + RingStr(aC[i][5]) + "]")
	next
	cConstraints = RowsSource(aRows, nl)
	aW = LangGet(aLang, "world")
	cWorld = "[[], " + '""' + ", []]"
	if not isNull(aW)
		aEntry = []
		if len(aW) >= 4 aEntry = aW[4] ok
		cWorld = "[" + NamesSource(aW[1]) + ", " + RingStr(aW[2]) + ", " + NamesSource(aEntry) + "]"
	ok
	aRf = LangGet(aLang, "refine")
	cPoints = "[]"
	cFloors = "[]"
	if not isNull(aRf)
		cPoints = PointsSource(aRf[1])
		cFloors = PointsSource(aRf[2])
	ok
	aRows = []
	aV = LangGet(aLang, "views")
	for i = 1 to len(aV)
		aRows + ("[" + RingStr(aV[i][1]) + ", " + RingStr(aV[i][2]) + ", " + RingStr(aV[i][3]) + ", " + RingStr(aV[i][4]) + ", " + RingStr(aV[i][5]) + "]")
	next
	cViews = RowsSource(aRows, nl)
	aRows = []
	aS = LangGet(aLang, "sentences")
	for i = 1 to len(aS)
		cInner = ""
		if not isNull(aS[i][3]) cInner = LangGet(aS[i][3], "name") ok
		aRows + ("[" + RingStr(aS[i][1]) + ", " + RingStr(cInner) + ", " + RingStr(aS[i][4]) + ", " + RingStr(aS[i][5]) + "]")
	next
	cSentences = RowsSource(aRows, nl)
	aRows = []
	aE = LangGet(aLang, "expressions")
	for i = 1 to len(aE)
		aRows + ExprSource(aE[i])
	next
	cExprs = RowsSource(aRows, nl)
	aRows = []
	aWk = LangGet(aLang, "walks")
	if isNull(aWk) aWk = [] ok
	for i = 1 to len(aWk)
		aRows + WalkSource(aWk[i])
	next
	cWalks = RowsSource(aRows, nl)
	aAsk = LangGet(aLang, "ask")
	cAsk = "NULL"
	if not isNull(aAsk)
		cAsk = "[" + RingStr(aAsk[1]) + ", " + NamesSource(aAsk[2]) + ", " + RingStr(aAsk[3]) + ", " + NamesSource(aAsk[4]) + "]"
	ok
	aRun = LangGet(aLang, "run")
	cRun = "NULL"
	if not isNull(aRun)
		cRun = "["
		for i = 1 to len(aRun[2])
			if i > 1 cRun += ", " ok
			cRun += "[" + RingStr(aRun[2][i][1]) + ", " + NamesSource(aRun[2][i][2]) + "]"
		next
		cRun += "]"
	ok
	c = "  [" + RingStr(LangGet(aLang, "name")) + ", " + RingStr(LangGet(aLang, "extension")) + "," + nl
	c += "    " + cKinds + "," + nl
	c += "    " + cForms + "," + nl
	c += "    " + cRefusals + "," + nl
	c += "    " + cMenus + "," + nl
	c += "    " + cRanges + "," + nl
	c += "    " + cFormats + "," + nl
	c += "    " + cUnions + "," + nl
	c += "    " + cConstraints + "," + nl
	c += "    " + cWorld + "," + nl
	c += "    " + cPoints + "," + nl
	c += "    " + cFloors + "," + nl
	c += "    " + cViews + "," + nl
	c += "    " + cSentences + "," + nl
	c += "    " + cExprs + "," + nl
	c += "    " + cWalks + "," + nl
	c += "    " + cAsk + "," + nl
	c += "    " + cRun + nl
	c += "  ]"
	return c

# the language and, recursively, every language its SENTENCEs name, each once
func ForgeLangRecords(aLang, aSeen)
	aOut = []
	cName = LangGet(aLang, "name")
	if InStrList(cName, aSeen) return aOut ok
	aSeen + cName
	aOut + aLang
	aS = LangGet(aLang, "sentences")
	for i = 1 to len(aS)
		if not isNull(aS[i][3])
			aMore = ForgeLangRecords(aS[i][3], aSeen)
			for j = 1 to len(aMore)
				aOut + aMore[j]
			next
		ok
	next
	return aOut

func ForgeCourt(aLang)
	cForgeName = LangGet(aLang, "name")
	nl = char(10)
	c = "# " + cForgeName + "_court.ring -- GENERATED by forge.ring from the " + cForgeName + " declaration; do not edit." + nl
	c += "# `rnxc " + cForgeName + "_court.ring check <file" + LangGet(aLang, "extension") + ">` judges one sentence of the language;" + nl
	c += "# `... refine <file> <file.rfn>` judges one refinement. What the declaration says is judged" + nl
	c += "# by court_lib.ring over the records below, one per language -- this one first, then" + nl
	c += "# every language a SENTENCE seat names: kinds [VERB, name, seats, names, messages]," + nl
	c += "# forms, refusals, menus, ranges, formats, unions, constraints, world, points, floors," + nl
	c += "# views, sentences, expressions, walks and the ask." + nl + nl
	c += 'load "court_lib.ring"' + nl
	# v0.6: the expression library rides along only when an EXPRESSION is declared
	# (v0.7: or an ASK, whose rows are JSON); the question library only with an ASK
	bAsk = not isNull(LangGet(aLang, "ask"))
	bRun = not isNull(LangGet(aLang, "run"))
	if len(LangGet(aLang, "expressions")) > 0 or bAsk or bRun
		c += 'load "expr_lib.ring"' + nl
	ok
	if bAsk
		c += 'load "ask_lib.ring"' + nl
	ok
	if bRun
		c += 'load "run_lib.ring"' + nl
	ok
	c += nl
	c += "$cCourtLang = " + '""' + nl + "$cCourtExt = " + '""' + nl + "$cCourtDir = " + '""' + nl
	c += "$aCourtToks = []" + nl + "$nCourtPos = 1" + nl
	c += "$aCondToks = []" + nl + "$nCondPos = 1" + nl + "$aCondDeclSeats = []" + nl
	c += "$aCondDecls = []" + nl + "$aCondVerbOf = []" + nl + "$cCondOther = " + '""' + nl
	c += "$aCondRefSeats = []" + nl + "$aCondFormats = []" + nl + "$bCondUnread = 0" + nl
	c += "$aCondLangs = []" + nl + "$cCondLang = " + '""' + nl + "$aCourtSentences = []" + nl
	c += "$aCourtKinds = []" + nl + "$aCourtForms = []" + nl + "$aCourtRefusals = []" + nl + "$aCourtMenus = []" + nl
	c += "$aCourtRanges = []" + nl + "$aCourtFormats = []" + nl + "$aCourtUnions = []" + nl + "$aCourtConstraints = []" + nl
	c += "$aCourtWorld = [[], " + '""' + ", []]" + nl + "$aCourtPoints = []" + nl + "$aCourtFloors = []" + nl
	c += "$aCourtViews = []" + nl + "$aCourtSentenceKinds = []" + nl
	c += "$aCourtExprs = []" + nl + "$aCourtWalks = []" + nl + "$aCourtAsk = NULL" + nl + "$aCourtRun = NULL" + nl
	c += ExprGlobals()
	c += "$aCourtLangs = [" + nl
	aRecs = ForgeLangRecords(aLang, [])
	for i = 1 to len(aRecs)
		c += LangSource(aRecs[i])
		if i < len(aRecs) c += "," ok
		c += nl
	next
	c += "]" + nl
	c += "CtUseLanguage(" + RingStr(cForgeName) + ")" + nl
	c += "CtBuildCondLangs()" + nl
	c += nl + "CtMain()" + nl
	return c

# the globals expr_lib.ring reads, born empty at a court's top level (v0.6)
func ExprGlobals()
	nl = char(10)
	c = "$cExprLang = " + '""' + nl + "$aExprOperators = []" + nl + "$aExprOperands = []" + nl
	c += "$aExprAggregates = []" + nl + "$aExprVariables = []" + nl + "$aExprContexts = []" + nl
	c += "$cExprAbsent = " + '""' + nl + "$cExprDivision = " + '""' + nl + "$cExprEquality = " + '""' + nl
	c += "$aExprToks = []" + nl + "$nExprPos = 1" + nl + "$aExprAllowed = []" + nl
	c += "$aExprRecord = []" + nl + "$aExprOverlay = []" + nl
	return c

# ---- the expression court, as Ring source (v0.5) -------------------------------
# One EXPRESSION per language is forged whole: the first declared one. Its
# operators, operands, variables and contexts become the tables expr_lib.ring
# reads; the court checks and evaluates an expression in a named seat.

func ForgeExprCourt(aLang)
	nl = char(10)
	cName = LangGet(aLang, "name")
	aE = LangGet(aLang, "expressions")[1]
	c = "# " + cName + "_expr.ring -- GENERATED by forge.ring from the " + cName + " declaration; do not edit." + nl
	c += "# `rnxc " + cName + "_expr.ring check <seat> <expr>` judges one expression of the language in a seat;" + nl
	c += "# `... eval <seat> <expr> [input] [init]` evaluates it. What the declaration says is judged" + nl
	c += "# by expr_lib.ring over the tables below: the operator and operand menus, the" + nl
	c += "# variables, and the seats with the variables each admits." + nl + nl
	c += 'load "expr_lib.ring"' + nl + nl
	c += "$cExprLang = " + RingStr(cName) + nl
	c += "$aExprOperators = " + NamesSource(aE[2]) + nl
	c += "$aExprOperands = " + NamesSource(aE[3]) + nl
	aAgg = aE[4]
	if isNull(aAgg) aAgg = [] ok
	c += "$aExprAggregates = " + NamesSource(aAgg) + nl
	aVars = aE[5]
	if isNull(aVars) aVars = [] ok
	c += "$aExprVariables = " + NamesSource(aVars) + nl
	c += "$aExprContexts = ["
	aCtx = []
	if len(aE) >= 8 aCtx = aE[8] ok
	for i = 1 to len(aCtx)
		if i > 1 c += ", " ok
		c += "[" + RingStr(aCtx[i][1]) + ", " + NamesSource(aCtx[i][2]) + "]"
	next
	c += "]" + nl
	cAbsent = "" cDivision = "" cEquality = ""
	if len(aE) >= 11
		cAbsent = aE[9]
		cDivision = aE[10]
		cEquality = aE[11]
	ok
	c += "$cExprAbsent = " + RingStr(cAbsent) + nl + "$cExprDivision = " + RingStr(cDivision) + nl + "$cExprEquality = " + RingStr(cEquality) + nl
	c += "$aExprToks = []" + nl + "$nExprPos = 1" + nl + "$aExprAllowed = []" + nl
	c += "$aExprRecord = []" + nl + "$aExprOverlay = []" + nl
	c += nl + "ExMain()" + nl
	return c

# the expression's grammar for the decoder, from its menus: a rule per
# precedence level, present when its operators are, the operands it admits,
# and its variables by name
func ForgeExprGbnf(aLang)
	return ForgeExprGbnfOf(aLang, LangGet(aLang, "expressions")[1])

func ForgeExprGbnfOf(aLang, aE)
	nl = char(10)
	cName = LangGet(aLang, "name")
	aOps = aE[2]
	aOpd = aE[3]
	aVars = aE[5]
	if isNull(aVars) aVars = [] ok
	q = char(34)
	bs = char(92)
	aAgg = aE[4]
	if isNull(aAgg) aAgg = [] ok
	g = "# " + cName + "_expr.gbnf -- GENERATED by forge.ring from the " + cName + " declaration (Haro v0.5, grown in v0.6)." + nl
	g += "# W's shape: or < and < not < comparison < additive < multiplicative < unary < primary;" + nl
	g += "# each level is present when the declaration admits its operators." + nl + nl
	g += "root ::= ws or_expr ws" + nl
	# a word operator is set off by at least one space (sp), or `not1` and
	# `@itemand` would be one word to the tokenizer
	if InStrList("or", aOps)
		g += "or_expr ::= and_expr (sp " + q + "or" + q + " sp and_expr)*" + nl
	else
		g += "or_expr ::= and_expr" + nl
	ok
	if InStrList("and", aOps)
		g += "and_expr ::= not_expr (sp " + q + "and" + q + " sp not_expr)*" + nl
	else
		g += "and_expr ::= not_expr" + nl
	ok
	if InStrList("not", aOps)
		g += "not_expr ::= (" + q + "not" + q + " sp)? comparison" + nl
	else
		g += "not_expr ::= comparison" + nl
	ok
	bCmp = InStrList("cmp", aOps)
	bContains = InStrList("contains", aOps)
	if bCmp and bContains
		g += "comparison ::= additive (ws cmpop ws additive | sp " + q + "CONTAINS" + q + " sp additive)?" + nl
	but bCmp
		g += "comparison ::= additive (ws cmpop ws additive)?" + nl
	but bContains
		g += "comparison ::= additive (sp " + q + "CONTAINS" + q + " sp additive)?" + nl
	else
		g += "comparison ::= additive" + nl
	ok
	if bCmp
		g += "cmpop ::= " + q + ">=" + q + " | " + q + "<=" + q + " | " + q + "!=" + q + " | " + q + "<>" + q + " | " + q + "=" + q + " | " + q + ">" + q + " | " + q + "<" + q + nl
	ok
	aAdd = []
	if InStrList("add", aOps) aAdd + (q + "+" + q) ok
	if InStrList("sub", aOps) aAdd + (q + "-" + q) ok
	if len(aAdd) > 0
		g += "additive ::= multiplicative (ws (" + StzuJoin(aAdd, " | ") + ") ws multiplicative)*" + nl
	else
		g += "additive ::= multiplicative" + nl
	ok
	aMul = []
	if InStrList("mul", aOps) aMul + (q + "*" + q) ok
	if InStrList("div", aOps) aMul + (q + "/" + q) ok
	if InStrList("mod", aOps) aMul + (q + "%" + q) ok
	if len(aMul) > 0
		g += "multiplicative ::= unary (ws (" + StzuJoin(aMul, " | ") + ") ws unary)*" + nl
	else
		g += "multiplicative ::= unary" + nl
	ok
	if InStrList("neg", aOps)
		g += "unary ::= (" + q + "-" + q + " ws)? primary" + nl
	else
		g += "unary ::= primary" + nl
	ok
	aPrim = []
	if InStrList("number", aOpd) aPrim + "number" ok
	if InStrList("text", aOpd) aPrim + "string" ok
	if InStrList("flag", aOpd) aPrim + "flag" ok
	if InStrList("var", aOpd) and len(aVars) > 0 aPrim + "variable" ok
	if InStrList("agg", aOpd) and len(aAgg) > 0 aPrim + "aggregate" ok
	if InStrList("ref", aOpd) aPrim + "reference" ok
	if InStrList("round", aOps) aPrim + (q + "ROUND" + q + " ws " + q + "(" + q + " ws or_expr ws " + q + ")" + q) ok
	aPrim + (q + "(" + q + " ws or_expr ws " + q + ")" + q)
	g += "primary ::= " + StzuJoin(aPrim, " | ") + nl
	if InStrList("flag", aOpd)
		g += "flag ::= " + q + "true" + q + " | " + q + "false" + q + nl
	ok
	if InStrList("agg", aOpd) and len(aAgg) > 0
		aA = []
		for i = 1 to len(aAgg)
			aA + (q + upper(aAgg[i]) + q)
		next
		g += "aggregate ::= (" + StzuJoin(aA, " | ") + ") ws " + q + "(" + q + " ws reference ws " + q + ")" + q + nl
	ok
	if InStrList("ref", aOpd) or (InStrList("agg", aOpd) and len(aAgg) > 0)
		g += "reference ::= [a-z_] [a-z0-9_]* (" + q + "." + q + " [a-z_] [a-z0-9_]*)*" + nl
	ok
	g += "number ::= [0-9]+ (" + q + "." + q + " [0-9]+)?" + nl
	g += "string ::= " + q + "'" + q + " [^']* " + q + "'" + q + " | " + q + bs + q + q + " [^" + q + "]* " + q + bs + q + q + nl
	if len(aVars) > 0
		aV = []
		for i = 1 to len(aVars)
			aV + (q + aVars[i] + q)
		next
		g += "variable ::= " + q + "@" + q + " (" + StzuJoin(aV, " | ") + ")" + nl
	ok
	g += "sp ::= [ " + bs + "t]+" + nl
	g += "ws ::= [ " + bs + "t]*" + nl
	return g

# ---- the question grammar, for the decoder (v0.7) ------------------------------
# the ASK's frame -- SELECT * FROM name, then the clauses it admits -- over the
# WHERE expression's own grammar, its root renamed where_expr
func ForgeAskGbnf(aLang)
	nl = char(10)
	q = char(34)
	cName = LangGet(aLang, "name")
	aAsk = LangGet(aLang, "ask")
	aCl = aAsk[4]
	g = "# " + cName + "_ask.gbnf -- GENERATED by forge.ring from the " + cName + " declaration (Haro v0.7)." + nl
	g += "# The Q letter: SELECT * FROM name, then the clauses the ASK admits, in this order." + nl + nl
	cRoot = "root ::= ws " + q + "SELECT" + q + " sp " + q + "*" + q + " sp " + q + "FROM" + q + " sp ident"
	if InStrList("where", aCl) cRoot += " (sp " + q + "WHERE" + q + " sp where_expr)?" ok
	if InStrList("order", aCl) cRoot += " (sp " + q + "ORDER" + q + " sp " + q + "BY" + q + " sp reference (sp (" + q + "ASC" + q + " | " + q + "DESC" + q + "))?)?" ok
	if InStrList("limit", aCl) cRoot += " (sp " + q + "LIMIT" + q + " sp number)?" ok
	g += cRoot + " ws" + nl
	g += "ident ::= [a-z_] [a-z0-9_]*" + nl
	cBody = ""
	if aAsk[3] != ""
		aE = NULL
		aEs = LangGet(aLang, "expressions")
		for i = 1 to len(aEs)
			if aEs[i][1] = aAsk[3] aE = aEs[i] ok
		next
		cExpr = ForgeExprGbnfOf(aLang, aE)
		# keep the rules, drop the header and the root
		nAt = substr(cExpr, "root ::= ws or_expr ws" + nl)
		if nAt > 0 cBody = substr(cExpr, nAt + len("root ::= ws or_expr ws" + nl)) ok
		g += "where_expr ::= or_expr" + nl + cBody
	ok
	if substr(cBody, "reference ::=") = 0
		g += "reference ::= [a-z_] [a-z0-9_]* (" + q + "." + q + " [a-z_] [a-z0-9_]*)*" + nl
	ok
	if substr(cBody, "number ::=") = 0 g += "number ::= [0-9]+" + nl ok
	if substr(cBody, "sp ::=") = 0 g += "sp ::= [ " + char(92) + "t]+" + nl ok
	if substr(cBody, "ws ::=") = 0 g += "ws ::= [ " + char(92) + "t]*" + nl ok
	return g

# ---- the grammar, for the decoder --------------------------------------------
# One rule per kind, one alternative per clause with the clause's own value
# shape, so a derivation is well-typed; a clause given twice or a required
# seat absent are the court's, not the grammar's (a context-free grammar
# cannot say "at most once" without enumerating orders).

func GbnfShape(aSeat, aLang)
	cOf = aSeat[2]
	cK = TypeKindOf(aLang, cOf)
	if cK = "union"
		# one alternative per shape, in the union's order (v0.3)
		aU = UnionOf(aLang, cOf)
		cOut = "("
		for i = 1 to len(aU[2])
			if i > 1 cOut += " | " ok
			cOut += GbnfShape([aU[2][i][1], aU[2][i][1], aU[2][i][2], 0], aLang)
		next
		return cOut + ")"
	ok
	if aSeat[3]
		if cK = "form"
			aF = FormOf(aLang, cOf)
			aFS = aF[2]
			aDeclaredK = []
			aDL = LangGet(aLang, "declarations")
			for i = 1 to len(aDL) aDeclaredK + [aDL[i][1], "DECLARATION"] next
			aML = LangGet(aLang, "menus")
			for i = 1 to len(aML) aDeclaredK + [aML[i][1], "MENU"] next
			if StzuIsPairForm(aFS, aDeclaredK) return "pairlist" ok
			if len(aFS) > 0 and (aFS[1][2] = "text" or TypeKindOf(aLang, aFS[1][2]) = "format") return "stringlist" ok
		ok
		return "namelist"
	ok
	if cOf = "text" or cK = "format" or cK = "sentence" or cK = "expr" return "string" ok
	if cOf = "number" or cK = "range" return "number" ok
	return "ident"

func FormOf(aLang, cName)
	aF = LangGet(aLang, "forms")
	for i = 1 to len(aF)
		if aF[i][1] = cName return aF[i] ok
	next
	return NULL

func ForgeGbnf(aLang)
	nl = char(10)
	cName = LangGet(aLang, "name")
	aD = LangGet(aLang, "declarations")
	g = "# " + cName + ".gbnf -- GENERATED by forge.ring from the " + cName + " declaration (stzu v0.1)." + nl
	g += "# The Commons' lexical form (C6): -- comments, double-quoted strings, UPPER_SNAKE keywords," + nl
	g += "# lower_snake identifiers, trailing commas. A clause given twice and a required seat" + nl
	g += "# absent are the court's to refuse; the decoder holds the shape." + nl + nl
	g += "root ::= ws decl (ws decl)* ws" + nl
	g += "decl ::= "
	for i = 1 to len(aD)
		if i > 1 g += " | " ok
		g += "decl_" + aD[i][2]
	next
	g += nl
	# Ring has no string escapes (F-55): the grammar's own quotes and
	# backslashes are spelled with char(), never with \" or \n
	q = char(34)
	bs = char(92)
	for i = 1 to len(aD)
		cK = aD[i][2]
		aS = aD[i][3]
		# a declaration is [name, verb, seats, rationale, line]: the VERB is spoken
		g += "decl_" + cK + ' ::= "DEFINE" sp "' + cK + '" sp ident sp "AS" ws "(" ws (clause_' + cK + ' (ws "," ws clause_' + cK + ')* (ws ",")?)? ws ")" ws "RATIONALE" sp string' + nl
		g += "clause_" + cK + " ::= "
		if len(aS) = 0
			g += '"NOTHING"'
		ok
		for j = 1 to len(aS)
			if j > 1 g += " | " ok
			g += '"' + upper(aS[j][1]) + '" sp ' + GbnfShape(aS[j], aLang)
		next
		g += nl
	next
	g += nl
	g += 'ident ::= [a-z_] [a-z0-9_]*' + nl
	g += "string ::= " + q + bs + q + q + " [^" + q + "]* " + q + bs + q + q + nl
	g += 'number ::= [0-9]+' + nl
	g += 'namelist ::= "[" ws (ident (ws "," ws ident)* (ws ",")?)? ws "]"' + nl
	g += 'stringlist ::= "[" ws (string (ws "," ws string)* (ws ",")?)? ws "]"' + nl
	# v0.6: a pair list, emitted when a kind writes one
	bPairs = 0
	for i = 1 to len(aD)
		aS = aD[i][3]
		for j = 1 to len(aS)
			if GbnfShape(aS[j], aLang) = "pairlist" bPairs = 1 ok
		next
	next
	if bPairs
		g += 'pairlist ::= "[" ws (pair (ws "," ws pair)* (ws ",")?)? ws "]"' + nl
		g += 'pair ::= ident ws ":" ws (ident | string | number)' + nl
	ok
	g += "sp ::= [ " + bs + "t]+" + nl
	g += "ws ::= ([ " + bs + "t" + bs + "r" + bs + "n] | " + q + "--" + q + " [^" + bs + "n]* " + q + bs + "n" + q + ")*" + nl
	return g
