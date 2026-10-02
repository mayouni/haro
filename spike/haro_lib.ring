# haro_lib.ring -- the stzu meta-court, v0.2, in pure core Ring (no Softanza).
#
# v0.1 was a port of stz/face/stz/Stzu.luau (437 lines); it still is, and the
# 28 v0.1 fixtures still pass unchanged. v0.2 is the declaring altitude of Haro
# grown by the WORLD and REFINE seats and the type kinds a real language's
# court needs (haro/spike/v02/GRAMMAR.md; the judge is v02/fixtures.json,
# written first): MENU, RANGE, FORMAT as seat types; a seat typed by a
# DECLARATION as a reference; NAMES on a declaration; CONSTRAINT with a
# condition in the closed language of cond_lib.ring; WORLD (ONE, FIRST);
# REFINE (POINTS, FLOOR).
#
# v0.6 (haro/spike/v06/GRAMMAR.md): a list of a two-seat FORM written as
# name: value pairs; an EXPRESSION's ABSENT, DIVISION and EQUALITY; and
# WALK, the one kinetic kind -- which kind is walked, by which steps, in
# what order, under which guards, computing what, failing how.
#
# The same file runs on rnxc and on the oracle and must print the same bytes.
# Refusals are one channel, "stzu (line N): message". Functions only; the
# globals ($aStzuToks, $nStzuPos, and cond_lib's) are born in the root file.

load "cond_lib.ring"

# ---- the closed menus -------------------------------------------------------

func StzuOperators()
	return ["or", "and", "not", "cmp", "contains", "add", "sub", "mul", "div", "mod", "round", "neg"]

func StzuOperands()
	return ["number", "text", "flag", "ref", "var", "agg"]

func StzuAggregates()
	return ["sum", "count", "avg", "min", "max"]

func StzuPrimitives()
	return ["name", "text", "number", "flag", "ref"]

func StzuRefusalCategories()
	return ["unknown_verb", "unknown_declaration", "unknown_seat", "unknown_variable",
	        "unterminated_string", "unexpected_character", "dangling_reference", "duplicate_name"]

func StzuShapes()
	return ["absolute_path", "ipv4", "cidr", "mac", "label", "domain", "hex64", "hex64_lower"]

func StzuRefinementKinds()
	return ["knob", "field", "symbol", "policy", "composite", "pipeline"]

func StzuPostures()
	return ["trusted", "external", "sandboxed", "llm"]

# kind -> list of [clause, shape]; shapes: string namelist seatlist number ident pointlist
# (sorted by clause name, as Luau's table.sort gives, for the allowed-list text)
func StzuClauses(cKind)
	if cKind = "LANGUAGE"
		return [["COURT", "string"], ["EXTENSION", "string"], ["GRAMMAR", "string"], ["VERSION", "string"]]
	but cKind = "DECLARATION"
		return [["MESSAGES", "messagelist"], ["NAMES", "ident"], ["SEATS", "seatlist"], ["VERB", "string"]]
	but cKind = "FORM"
		return [["SEATS", "seatlist"]]
	but cKind = "EXPRESSION"
		return [["ABSENT", "ident"], ["AGGREGATES", "namelist"], ["CONTEXTS", "contextlist"], ["DIVISION", "ident"], ["EQUALITY", "ident"], ["OPERANDS", "namelist"], ["OPERATORS", "namelist"], ["VARIABLES", "namelist"]]
	but cKind = "REFUSAL"
		return [["MESSAGE", "string"]]
	but cKind = "MENU"
		return [["MESSAGE", "string"], ["WORDS", "namelist"]]
	but cKind = "RANGE"
		return [["MAX", "number"], ["MESSAGE", "string"], ["MIN", "number"]]
	but cKind = "FORMAT"
		return [["FOLD", "ident"], ["MESSAGE", "string"], ["SHAPE", "ident"]]
	but cKind = "SENTENCE"
		return [["MESSAGE", "string"], ["OF", "string"], ["REFUSED", "string"]]
	but cKind = "VIEW"
		return [["NAMED", "string"], ["ON", "ident"], ["ONE", "string"], ["WHERE", "string"]]
	but cKind = "CONSTRAINT"
		return [["MESSAGE", "string"], ["ON", "ident"], ["THEN", "string"], ["WHEN", "string"]]
	but cKind = "WORLD"
		return [["FIRST", "ident"], ["ONE", "namelist"]]
	but cKind = "REFINE"
		return [["FLOOR", "pointlist"], ["POINTS", "pointlist"]]
	but cKind = "UNION"
		return [["MESSAGE", "string"], ["OF", "typelist"]]
	but cKind = "WALK"
		return [["COMPUTE", "ident"], ["FAIL", "ident"], ["FORMULA", "ident"], ["GUARDS", "pathlist"], ["OF", "ident"], ["ORDER", "ident"], ["STEPS", "ident"], ["THROUGH", "ident"]]
	ok
	return []

func StzuRequired(cKind)
	if cKind = "LANGUAGE"
		return ["VERSION", "GRAMMAR", "COURT", "EXTENSION"]
	but cKind = "DECLARATION"
		return ["VERB", "SEATS"]
	but cKind = "FORM"
		return ["SEATS"]
	but cKind = "EXPRESSION"
		return ["OPERATORS", "OPERANDS"]
	but cKind = "REFUSAL"
		return ["MESSAGE"]
	but cKind = "MENU"
		return ["WORDS"]
	but cKind = "RANGE"
		return ["MIN", "MAX"]
	but cKind = "FORMAT"
		return ["SHAPE"]
	but cKind = "CONSTRAINT"
		return ["ON", "WHEN", "MESSAGE"]
	but cKind = "WORLD"
		return []
	but cKind = "REFINE"
		return ["POINTS"]
	but cKind = "UNION"
		return ["OF"]
	but cKind = "SENTENCE"
		return ["OF"]
	but cKind = "VIEW"
		return ["ONE"]
	but cKind = "WALK"
		return ["OF", "STEPS", "THROUGH", "ORDER"]
	ok
	return []

func StzuIsKind(cWord)
	return InStrList(cWord, ["LANGUAGE", "DECLARATION", "FORM", "EXPRESSION", "REFUSAL",
	                         "MENU", "RANGE", "FORMAT", "CONSTRAINT", "WORLD", "REFINE", "UNION",
	                         "SENTENCE", "VIEW", "WALK"])

# the directory part of a path, "" when none (core Ring has no dirname)
func StzuDirOf(cPath)
	n = 0
	for i = 1 to len(cPath)
		if cPath[i] = "/" or cPath[i] = char(92) n = i ok
	next
	if n = 0 return "" ok
	return left(cPath, n - 1)

# what a seat's type name resolves to in a language record:
# prim form expr menu range format decl union sentence
func StzuTypeKindOf(aLang, cOf)
	if InStrList(cOf, StzuPrimitives()) return "prim" ok
	aL = LangGet(aLang, "forms")
	for i = 1 to len(aL) if aL[i][1] = cOf return "form" ok next
	aL = LangGet(aLang, "menus")
	for i = 1 to len(aL) if aL[i][1] = cOf return "menu" ok next
	aL = LangGet(aLang, "ranges")
	for i = 1 to len(aL) if aL[i][1] = cOf return "range" ok next
	aL = LangGet(aLang, "formats")
	for i = 1 to len(aL) if aL[i][1] = cOf return "format" ok next
	aL = LangGet(aLang, "declarations")
	for i = 1 to len(aL) if aL[i][1] = cOf return "decl" ok next
	aL = LangGet(aLang, "unions")
	for i = 1 to len(aL) if aL[i][1] = cOf return "union" ok next
	aL = LangGet(aLang, "sentences")
	for i = 1 to len(aL) if aL[i][1] = cOf return "sentence" ok next
	return "expr"

# the condition tables of a language record and of the languages its
# SENTENCEs name (v0.4): one entry per language, [lang, declseats, onedecls,
# views, verbof]
func StzuCondLangs(aLang, aViewEntries)
	aOut = [StzuCondLang(aLang, aViewEntries)]
	aS = LangGet(aLang, "sentences")
	for i = 1 to len(aS)
		if not isNull(aS[i][3])
			aInner = StzuCondLangs(aS[i][3], [])
			for j = 1 to len(aInner)
				aOut + aInner[j]
			next
		ok
	next
	return aOut

func StzuCondLang(aLang, aViewEntries)
	aDecls = LangGet(aLang, "declarations")
	aSents = LangGet(aLang, "sentences")
	aDeclSeats = []
	aVerbOf = []
	for i = 1 to len(aDecls)
		aS = aDecls[i][3]
		aInfo = []
		for j = 1 to len(aS)
			cOf = aS[j][2]
			cTK = StzuTypeKindOf(aLang, cOf)
			cTarget = ""
			if cTK = "decl" cTarget = LangGet(aLang, "name") ok
			if cTK = "sentence"
				for k = 1 to len(aSents)
					if aSents[k][1] = cOf
						if not isNull(aSents[k][3]) cTarget = LangGet(aSents[k][3], "name") ok
					ok
				next
			ok
			aInfo + [aS[j][1], cOf, aS[j][3], cTK, cTarget]
		next
		aDeclSeats + [aDecls[i][1], aInfo]
		aVerbOf + [aDecls[i][1], aDecls[i][2]]
	next
	aOne = []
	aW = LangGet(aLang, "world")
	if not isNull(aW) aOne = aW[1] ok
	return [LangGet(aLang, "name"), aDeclSeats, aOne, aViewEntries, aVerbOf]

func StzuAllowedList(cKind)
	aC = StzuClauses(cKind)
	cOut = ""
	for i = 1 to len(aC)
		if i > 1 cOut += ", " ok
		cOut += aC[i][1]
	next
	return cOut

func StzuClauseShape(cKind, cClause)
	aC = StzuClauses(cKind)
	for i = 1 to len(aC)
		if aC[i][1] = cClause return aC[i][2] ok
	next
	return ""

# ---- small helpers ----------------------------------------------------------

func InStrList(cS, aL)
	for i = 1 to len(aL)
		if aL[i] = cS return 1 ok
	next
	return 0

func StzuJoin(aL, cSep)
	cOut = ""
	for i = 1 to len(aL)
		if i > 1 cOut += cSep ok
		cOut += aL[i]
	next
	return cOut

# character classes by byte code, never by string ordering (HF-30)
func IsLowerStart(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or n = 95

func IsLowerChar(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or n = 95 or (n >= 48 and n <= 57)

func IsUpperStart(c)
	n = ascii(c)
	return (n >= 65 and n <= 90)

func IsUpperChar(c)
	n = ascii(c)
	return (n >= 65 and n <= 90) or n = 95 or (n >= 48 and n <= 57)

func IsWordStart(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or (n >= 65 and n <= 90) or n = 95

func IsWordChar(c)
	return IsWordStart(c) or IsDigitChar(c)

func IsDigitChar(c)
	n = ascii(c)
	return (n >= 48 and n <= 57)

func IsLowerSnake(cW)
	if len(cW) = 0 return 0 ok
	if not IsLowerStart(cW[1]) return 0 ok
	for i = 2 to len(cW)
		if not IsLowerChar(cW[i]) return 0 ok
	next
	return 1

func IsUpperSnake(cW)
	if len(cW) = 0 return 0 ok
	if not IsUpperStart(cW[1]) return 0 ok
	for i = 2 to len(cW)
		if not IsUpperChar(cW[i]) return 0 ok
	next
	return 1

func StzuFail(nLine, cMsg)
	raise("haro (line " + nLine + "): " + cMsg)

# ---- tokenizer --------------------------------------------------------------
# a token is [type, value, line]; types: string number ident keyword
# lparen rparen lbracket rbracket comma colon question dot eof

func StzuTokenize(cSrc)
	aToks = []
	n = len(cSrc)
	i = 1
	nLine = 1
	while i <= n
		c = cSrc[i]
		if c = char(10)
			nLine++
			i++
		but c = " " or c = char(9) or c = char(13)
			i++
		but c = "-" and i < n and cSrc[i+1] = "-"
			while i <= n and cSrc[i] != char(10)
				i++
			end
		but c = '"'
			nStart = nLine
			j = i + 1
			cRaw = ""
			while j <= n and cSrc[j] != '"'
				if cSrc[j] = char(10) nLine++ ok
				cRaw += cSrc[j]
				j++
			end
			if j > n
				StzuFail(nStart, "Unterminated string")
			ok
			aToks + ["string", FoldString(cRaw), nStart]
			i = j + 1
		but IsDigitChar(c) or (c = "-" and i < n and IsDigitChar(cSrc[i+1]))
			j = i
			if cSrc[j] = "-" j++ ok
			while j <= n and IsDigitChar(cSrc[j])
				j++
			end
			if j <= n and cSrc[j] = "."
				j++
				while j <= n and IsDigitChar(cSrc[j])
					j++
				end
			ok
			aToks + ["number", substr(cSrc, i, j - i), nLine]
			i = j
		but IsWordStart(c)
			j = i
			while j <= n and IsWordChar(cSrc[j])
				j++
			end
			cW = substr(cSrc, i, j - i)
			if IsLowerSnake(cW)
				aToks + ["ident", cW, nLine]
			but IsUpperSnake(cW)
				aToks + ["keyword", cW, nLine]
			else
				StzuFail(nLine, "'" + cW + "' is neither a lower_snake identifier nor an UPPER_SNAKE keyword")
			ok
			i = j
		else
			cT = ""
			if c = "(" cT = "lparen"
			but c = ")" cT = "rparen"
			but c = "[" cT = "lbracket"
			but c = "]" cT = "rbracket"
			but c = "," cT = "comma"
			but c = ":" cT = "colon"
			but c = "?" cT = "question"
			but c = "." cT = "dot"
			ok
			if cT = ""
				StzuFail(nLine, "character '" + c + "' is not part of the stzu grammar")
			ok
			aToks + [cT, c, nLine]
			i++
		ok
	end
	aToks + ["eof", "", nLine]
	return aToks

# Luau: string.gsub(raw, "[ \t]*\r?\n[ \t]*", " ")
func FoldString(cRaw)
	cOut = ""
	n = len(cRaw)
	i = 1
	while i <= n
		c = cRaw[i]
		if c = char(10) or (c = char(13) and i < n and cRaw[i+1] = char(10))
			while len(cOut) > 0 and (cOut[len(cOut)] = " " or cOut[len(cOut)] = char(9))
				cOut = left(cOut, len(cOut) - 1)
			end
			if c = char(13) i++ ok
			i++
			while i <= n and (cRaw[i] = " " or cRaw[i] = char(9))
				i++
			end
			cOut += " "
		else
			cOut += c
			i++
		ok
	end
	return cOut

# ---- parser -----------------------------------------------------------------

func StzuPeek()
	return $aStzuToks[$nStzuPos]

func StzuAdvance()
	t = $aStzuToks[$nStzuPos]
	$nStzuPos++
	return t

func StzuExpect(cType, cWhat)
	t = StzuPeek()
	if t[1] != cType
		StzuFail(t[3], "Expected " + cWhat + " but found '" + t[2] + "'")
	ok
	return StzuAdvance()

func StzuExpectKeyword(cV)
	t = StzuPeek()
	if t[1] != "keyword" or t[2] != cV
		StzuFail(t[3], "Expected " + cV + " but found '" + t[2] + "'")
	ok
	StzuAdvance()

func StzuParseNameList()
	StzuExpect("lbracket", "'['")
	aNames = []
	while StzuPeek()[1] != "rbracket"
		t = StzuExpect("ident", "an identifier")
		aNames + t[2]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aNames

# a seat is [name, of, isList, optional, line]
func StzuParseSeatList()
	StzuExpect("lbracket", "'['")
	aSeats = []
	while StzuPeek()[1] != "rbracket"
		tName = StzuExpect("ident", "a seat name")
		StzuExpect("colon", "':'")
		bList = 0
		cOf = ""
		if StzuPeek()[1] = "lbracket"
			StzuAdvance()
			bList = 1
			tOf = StzuExpect("ident", "a seat type")
			cOf = tOf[2]
			StzuExpect("rbracket", "']'")
		else
			tOf = StzuExpect("ident", "a seat type")
			cOf = tOf[2]
		ok
		bOpt = 0
		if StzuPeek()[1] = "question"
			StzuAdvance()
			bOpt = 1
		ok
		aSeats + [tName[2], cOf, bList, bOpt, tName[3]]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aSeats

# a point is [decl, seat, word, line]: [ decl.seat: word, ... ]
func StzuParsePointList()
	StzuExpect("lbracket", "'['")
	aPoints = []
	while StzuPeek()[1] != "rbracket"
		tD = StzuExpect("ident", "a declaration name")
		StzuExpect("dot", "'.'")
		tS = StzuExpect("ident", "a seat name")
		StzuExpect("colon", "':'")
		tW = StzuExpect("ident", "a word")
		aPoints + [tD[2], tS[2], tW[2], tD[3]]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aPoints

# an alternative of a UNION is [type, isList, line]: [ a, [b], ... ]   (v0.3)
func StzuParseTypeList()
	StzuExpect("lbracket", "'['")
	aTypes = []
	while StzuPeek()[1] != "rbracket"
		bList = 0
		if StzuPeek()[1] = "lbracket"
			StzuAdvance()
			bList = 1
			tOf = StzuExpect("ident", "a type")
			StzuExpect("rbracket", "']'")
		else
			tOf = StzuExpect("ident", "a type")
		ok
		aTypes + [tOf[2], bList, tOf[3]]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aTypes

# a context is [name, [variables], line]: [ seat: [a, b], ... ]   (v0.5)
func StzuParseContextList()
	StzuExpect("lbracket", "'['")
	aCtx = []
	while StzuPeek()[1] != "rbracket"
		tN = StzuExpect("ident", "a seat name")
		StzuExpect("colon", "':'")
		aVars = StzuParseNameList()
		aCtx + [tN[2], aVars, tN[3]]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aCtx

# a path is a dotted name as written, with its line: [ seat, ref.seat, ... ]   (v0.6)
func StzuParsePathList()
	StzuExpect("lbracket", "'['")
	aPaths = []
	while StzuPeek()[1] != "rbracket"
		t = StzuExpect("ident", "a seat or a path")
		cP = t[2]
		while StzuPeek()[1] = "dot"
			StzuAdvance()
			t2 = StzuExpect("ident", "a seat name after '.'")
			cP += "." + t2[2]
		end
		aPaths + [cP, t[3]]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aPaths

# a message is [seat, text, line]: [ seat: "text", ... ]   (v0.3)
func StzuParseMessageList()
	StzuExpect("lbracket", "'['")
	aMsgs = []
	while StzuPeek()[1] != "rbracket"
		tS = StzuExpect("ident", "a seat name")
		StzuExpect("colon", "':'")
		tT = StzuExpect("string", "a message string")
		aMsgs + [tS[2], tT[2], tS[3]]
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rbracket"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ']' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	return aMsgs

func ClauseValue(aClauses, cName)
	for i = 1 to len(aClauses)
		if aClauses[i][1] = cName return aClauses[i][2] ok
	next
	return NULL

func HasClause(aClauses, cName)
	for i = 1 to len(aClauses)
		if aClauses[i][1] = cName return 1 ok
	next
	return 0

# one DEFINE <KIND> <name> AS ( clauses ) RATIONALE "..."
# returns [kind, name, clauses, rationale, line]
func StzuParseDeclaration()
	t = StzuPeek()
	if t[1] != "keyword" or t[2] != "DEFINE"
		StzuFail(t[3], "Unknown verb '" + t[2] + "'. The stzu verb set is closed -- a language is declared, never programmed.")
	ok
	nDeclLine = t[3]
	StzuAdvance()
	tKind = StzuPeek()
	if tKind[1] != "keyword" or not StzuIsKind(tKind[2])
		StzuFail(tKind[3], "Unknown declaration 'DEFINE " + tKind[2] + "'. The stzu verb set is closed -- a language is declared, never programmed.")
	ok
	cKind = StzuAdvance()[2]
	tName = StzuExpect("ident", "a lower_snake name")
	cName = tName[2]
	StzuExpectKeyword("AS")
	StzuExpect("lparen", "'('")
	aClauses = []
	while StzuPeek()[1] != "rparen"
		ct = StzuPeek()
		if ct[1] != "keyword"
			StzuFail(ct[3], "Expected a clause name but found '" + ct[2] + "'")
		ok
		cShape = StzuClauseShape(cKind, ct[2])
		if cShape = ""
			StzuFail(ct[3], "Unknown clause '" + ct[2] + "' in " + cKind + " -- allowed: " + StzuAllowedList(cKind))
		ok
		if HasClause(aClauses, ct[2])
			StzuFail(ct[3], "clause " + ct[2] + " given twice")
		ok
		StzuAdvance()
		if cShape = "string"
			tv = StzuExpect("string", "a string")
			aClauses + [ct[2], tv[2]]
		but cShape = "namelist"
			aClauses + [ct[2], StzuParseNameList()]
		but cShape = "seatlist"
			aClauses + [ct[2], StzuParseSeatList()]
		but cShape = "number"
			tv = StzuExpect("number", "a number")
			aClauses + [ct[2], tv[2]]
		but cShape = "ident"
			tv = StzuExpect("ident", "a lower_snake name")
			aClauses + [ct[2], tv[2]]
		but cShape = "typelist"
			aClauses + [ct[2], StzuParseTypeList()]
		but cShape = "messagelist"
			aClauses + [ct[2], StzuParseMessageList()]
		but cShape = "contextlist"
			aClauses + [ct[2], StzuParseContextList()]
		but cShape = "pathlist"
			aClauses + [ct[2], StzuParsePathList()]
		else
			aClauses + [ct[2], StzuParsePointList()]
		ok
		if StzuPeek()[1] = "comma"
			StzuAdvance()
		but StzuPeek()[1] != "rparen"
			t = StzuPeek()
			StzuFail(t[3], "Expected ',' or ')' but found '" + t[2] + "'")
		ok
	end
	StzuAdvance()
	rt = StzuPeek()
	if rt[1] != "keyword" or rt[2] != "RATIONALE"
		StzuFail(rt[3], "every stzu declaration carries its RATIONALE (the commons, 3.8)")
	ok
	StzuAdvance()
	tr = StzuExpect("string", "the rationale string")
	aReq = StzuRequired(cKind)
	for i = 1 to len(aReq)
		if not HasClause(aClauses, aReq[i])
			StzuFail(nDeclLine, cKind + " requires the " + aReq[i] + " clause")
		ok
	next
	return [cKind, cName, aClauses, tr[2], nDeclLine]

# ---- the language record ------------------------------------------------------
#   name version grammar court extension rationale
#   declarations: [name, verb, seats, rationale, line, names, messages]
#                 (names "" or a MENU/FORMAT; messages [seat, text, line] per reference seat, v0.3)
#   unions:       [name, alternatives, message, line]            (an alternative [type, isList, line], v0.3)
#   forms:        [name, seats, rationale, line]
#   expressions:  [name, operators, operands, aggregates, variables, rationale, line, contexts,
#                  absent, division, equality]
#                 (a context [seat, [variables], line], v0.5; the three semantics words
#                  "" when not declared, v0.6: ABSENT zero|refuse, DIVISION calm|refuse,
#                  EQUALITY kind|value)
#   walks:        [name, of, steps, through, order, guards, compute, formula, fail, line]
#                 (guards a list of [path, line]; compute, formula, fail "" when absent, v0.6)
#   refusals:     [name, message, rationale, line]
#   menus:        [name, words, message, line]
#   ranges:       [name, min, max, message, line]
#   formats:      [name, shape, message, line, fold]            (fold "" or "case", v0.4)
#   sentences:    [name, of, language record, message, refused, line]   (v0.4)
#   views:        [name, on, one, named, where, line]            (on "" for the whole sentence, v0.4)
#   constraints:  [name, on, when, then, message, line]        (then "" when absent)
#   world:        [one, first] or NULL                          (one a list, first "" or a name)
#   refine:       [points, floors] or NULL                       (lists of [decl, seat, word, line])

func LangGet(aLang, cKey)
	for i = 1 to len(aLang)
		if aLang[i][1] = cKey return aLang[i][2] ok
	next
	return NULL

func DeclaredKind(aDeclared, cName)
	for i = 1 to len(aDeclared)
		if aDeclared[i][1] = cName return aDeclared[i][2] ok
	next
	return ""

func StzuDeclare(cSrc)
	$aStzuToks = StzuTokenize(cSrc)
	$nStzuPos = 1

	if StzuPeek()[1] = "eof"
		StzuFail(1, "an empty file declares nothing -- a .haro file opens with DEFINE LANGUAGE")
	ok

	bHaveLang = 0
	cLName = "" cLVersion = "" cLGrammar = "" cLCourt = "" cLExtension = "" cLRationale = ""
	aDeclarations = []
	aForms = []
	aExpressions = []
	aRefusals = []
	aMenus = []
	aRanges = []
	aFormats = []
	aConstraints = []
	aUnions = []
	aSentences = []
	aViews = []
	aWalks = []
	aWorld = NULL
	aRefine = NULL
	aDeclared = []
	aVerbs = []
	nCount = 0

	while StzuPeek()[1] != "eof"
		aD = StzuParseDeclaration()
		cKind = aD[1] cName = aD[2] aClauses = aD[3] cRationale = aD[4] nLine = aD[5]
		nCount++
		if nCount = 1 and cKind != "LANGUAGE"
			StzuFail(nLine, "the LANGUAGE declaration comes first")
		ok
		if cKind = "LANGUAGE"
			if bHaveLang
				StzuFail(nLine, "a .haro file declares exactly one LANGUAGE")
			ok
			bHaveLang = 1
			cLName = cName
			cLVersion = ClauseValue(aClauses, "VERSION")
			cLGrammar = ClauseValue(aClauses, "GRAMMAR")
			cLCourt = ClauseValue(aClauses, "COURT")
			cLExtension = ClauseValue(aClauses, "EXTENSION")
			cLRationale = cRationale
		but cKind = "WORLD"
			if not isNull(aWorld)
				StzuFail(nLine, "a .haro file declares at most one WORLD")
			ok
			aOne = []
			if HasClause(aClauses, "ONE") aOne = ClauseValue(aClauses, "ONE") ok
			cFirst = ""
			if HasClause(aClauses, "FIRST") cFirst = ClauseValue(aClauses, "FIRST") ok
			aWorld = [aOne, cFirst, nLine]
		but cKind = "REFINE"
			if not isNull(aRefine)
				StzuFail(nLine, "a .haro file declares at most one REFINE")
			ok
			aFloors = []
			if HasClause(aClauses, "FLOOR") aFloors = ClauseValue(aClauses, "FLOOR") ok
			aRefine = [ClauseValue(aClauses, "POINTS"), aFloors, nLine]
		else
			if DeclaredKind(aDeclared, cName) != ""
				StzuFail(nLine, "'" + cName + "' is already declared -- one namespace, one name, one meaning")
			ok
			aDeclared + [cName, cKind]
			if cKind = "DECLARATION"
				cVerb = ClauseValue(aClauses, "VERB")
				if not IsUpperSnake(cVerb)
					StzuFail(nLine, "VERB '" + cVerb + "' must be UPPER_SNAKE")
				ok
				if InStrList(cVerb, aVerbs)
					StzuFail(nLine, "verb '" + cVerb + "' is already declared")
				ok
				aVerbs + cVerb
				cNames = ""
				if HasClause(aClauses, "NAMES") cNames = ClauseValue(aClauses, "NAMES") ok
				aMsgs = []
				if HasClause(aClauses, "MESSAGES") aMsgs = ClauseValue(aClauses, "MESSAGES") ok
				aDeclarations + [cName, cVerb, ClauseValue(aClauses, "SEATS"), cRationale, nLine, cNames, aMsgs]
			but cKind = "FORM"
				aForms + [cName, ClauseValue(aClauses, "SEATS"), cRationale, nLine]
			but cKind = "EXPRESSION"
				aOps = ClauseValue(aClauses, "OPERATORS")
				for i = 1 to len(aOps)
					if not InStrList(aOps[i], StzuOperators())
						StzuFail(nLine, "'" + aOps[i] + "' is not in the closed operator menu -- an escape hatch is unexpressible, not forbidden")
					ok
				next
				aOpd = ClauseValue(aClauses, "OPERANDS")
				for i = 1 to len(aOpd)
					if not InStrList(aOpd[i], StzuOperands())
						StzuFail(nLine, "'" + aOpd[i] + "' is not in the closed operand menu -- an escape hatch is unexpressible, not forbidden")
					ok
				next
				aAgg = NULL
				if HasClause(aClauses, "AGGREGATES")
					aAgg = ClauseValue(aClauses, "AGGREGATES")
					for i = 1 to len(aAgg)
						if not InStrList(aAgg[i], StzuAggregates())
							StzuFail(nLine, "'" + aAgg[i] + "' is not in the closed aggregate menu")
						ok
					next
				ok
				aVars = NULL
				if HasClause(aClauses, "VARIABLES")
					aVars = ClauseValue(aClauses, "VARIABLES")
				ok
				# v0.5: the seats a host offers the expression, each with the
				# VARIABLES it admits
				aCtx = []
				if HasClause(aClauses, "CONTEXTS")
					aCtx = ClauseValue(aClauses, "CONTEXTS")
					if isNull(aVars) StzuFail(nLine, "CONTEXTS requires a VARIABLES clause: a seat is a choice among the variables") ok
					for i = 1 to len(aCtx)
						for j = 1 to i - 1
							if aCtx[j][1] = aCtx[i][1]
								StzuFail(aCtx[i][3], "context '" + aCtx[i][1] + "' is named twice")
							ok
						next
						for j = 1 to len(aCtx[i][2])
							if not InStrList(aCtx[i][2][j], aVars)
								StzuFail(aCtx[i][3], "'" + aCtx[i][2][j] + "' is not a VARIABLE of " + cName + " (its VARIABLES: " + StzuJoin(aVars, ", ") + ")")
							ok
						next
					next
				ok
				# v0.6: the semantics an evaluator needs, each a closed choice
				cAbsent = ""
				if HasClause(aClauses, "ABSENT")
					cAbsent = ClauseValue(aClauses, "ABSENT")
					if cAbsent != "zero" and cAbsent != "refuse"
						StzuFail(nLine, "ABSENT takes zero or refuse: what a reference to nothing reads as; '" + cAbsent + "' is neither")
					ok
				ok
				cDivision = ""
				if HasClause(aClauses, "DIVISION")
					cDivision = ClauseValue(aClauses, "DIVISION")
					if cDivision != "calm" and cDivision != "refuse"
						StzuFail(nLine, "DIVISION takes calm or refuse: what a division by zero yields; '" + cDivision + "' is neither")
					ok
				ok
				cEquality = ""
				if HasClause(aClauses, "EQUALITY")
					cEquality = ClauseValue(aClauses, "EQUALITY")
					if cEquality != "kind" and cEquality != "value"
						StzuFail(nLine, "EQUALITY takes kind or value: whether a number and a text can be equal; '" + cEquality + "' is neither")
					ok
				ok
				aExpressions + [cName, aOps, aOpd, aAgg, aVars, cRationale, nLine, aCtx, cAbsent, cDivision, cEquality]
			but cKind = "REFUSAL"
				if not InStrList(cName, StzuRefusalCategories())
					StzuFail(nLine, "'" + cName + "' is not a refusal category")
				ok
				aRefusals + [cName, ClauseValue(aClauses, "MESSAGE"), cRationale, nLine]
			but cKind = "MENU"
				aWords = ClauseValue(aClauses, "WORDS")
				if len(aWords) = 0
					StzuFail(nLine, "a MENU names at least one word")
				ok
				cMsg = ""
				if HasClause(aClauses, "MESSAGE") cMsg = ClauseValue(aClauses, "MESSAGE") ok
				aMenus + [cName, aWords, cMsg, nLine]
			but cKind = "RANGE"
				nMin = 0 + ClauseValue(aClauses, "MIN")
				nMax = 0 + ClauseValue(aClauses, "MAX")
				if nMin > nMax
					StzuFail(nLine, "RANGE " + cName + " has MIN above MAX (" + ClauseValue(aClauses, "MIN") + " > " + ClauseValue(aClauses, "MAX") + ")")
				ok
				cMsg = ""
				if HasClause(aClauses, "MESSAGE") cMsg = ClauseValue(aClauses, "MESSAGE") ok
				aRanges + [cName, ClauseValue(aClauses, "MIN"), ClauseValue(aClauses, "MAX"), cMsg, nLine]
			but cKind = "FORMAT"
				cShape = ClauseValue(aClauses, "SHAPE")
				if not InStrList(cShape, StzuShapes())
					StzuFail(nLine, "'" + cShape + "' is not a shape: the menu is absolute_path, ipv4, cidr, mac, label, domain, hex64, hex64_lower")
				ok
				cMsg = ""
				if HasClause(aClauses, "MESSAGE") cMsg = ClauseValue(aClauses, "MESSAGE") ok
				cFold = ""
				if HasClause(aClauses, "FOLD") cFold = ClauseValue(aClauses, "FOLD") ok
				if cFold != "" and cFold != "case"
					StzuFail(nLine, "FOLD takes case, the one folding a court knows; '" + cFold + "' is not it")
				ok
				aFormats + [cName, cShape, cMsg, nLine, cFold]
			but cKind = "SENTENCE"
				cMsg = ""
				if HasClause(aClauses, "MESSAGE") cMsg = ClauseValue(aClauses, "MESSAGE") ok
				cRefused = ""
				if HasClause(aClauses, "REFUSED") cRefused = ClauseValue(aClauses, "REFUSED") ok
				aSentences + [cName, ClauseValue(aClauses, "OF"), NULL, cMsg, cRefused, nLine]
			but cKind = "VIEW"
				cOn = ""
				if HasClause(aClauses, "ON") cOn = ClauseValue(aClauses, "ON") ok
				cNamed = ""
				if HasClause(aClauses, "NAMED") cNamed = ClauseValue(aClauses, "NAMED") ok
				cWhere = ""
				if HasClause(aClauses, "WHERE") cWhere = ClauseValue(aClauses, "WHERE") ok
				aViews + [cName, cOn, ClauseValue(aClauses, "ONE"), cNamed, cWhere, nLine]
			but cKind = "WALK"
				aGuards = []
				if HasClause(aClauses, "GUARDS") aGuards = ClauseValue(aClauses, "GUARDS") ok
				cCompute = ""
				if HasClause(aClauses, "COMPUTE") cCompute = ClauseValue(aClauses, "COMPUTE") ok
				cFormula = ""
				if HasClause(aClauses, "FORMULA") cFormula = ClauseValue(aClauses, "FORMULA") ok
				cFailSeat = ""
				if HasClause(aClauses, "FAIL") cFailSeat = ClauseValue(aClauses, "FAIL") ok
				aWalks + [cName, ClauseValue(aClauses, "OF"), ClauseValue(aClauses, "STEPS"), ClauseValue(aClauses, "THROUGH"),
				          ClauseValue(aClauses, "ORDER"), aGuards, cCompute, cFormula, cFailSeat, nLine]
			but cKind = "UNION"
				aAlts = ClauseValue(aClauses, "OF")
				if len(aAlts) < 2
					StzuFail(nLine, "a UNION names at least two alternatives")
				ok
				cMsg = ""
				if HasClause(aClauses, "MESSAGE") cMsg = ClauseValue(aClauses, "MESSAGE") ok
				aUnions + [cName, aAlts, cMsg, nLine]
			else
				# CONSTRAINT: resolved after the whole file is read
				cThen = ""
				if HasClause(aClauses, "THEN") cThen = ClauseValue(aClauses, "THEN") ok
				aConstraints + [cName, ClauseValue(aClauses, "ON"), ClauseValue(aClauses, "WHEN"), cThen, ClauseValue(aClauses, "MESSAGE"), nLine]
			ok
		ok
	end

	# the resolution pass (order-free; a name resolving to nothing is refused now)
	for i = 1 to len(aDeclarations)
		StzuResolveSeats(aDeclarations[i][3], aDeclared)
		cNames = aDeclarations[i][6]
		if cNames != ""
			cK = DeclaredKind(aDeclared, cNames)
			if cK = ""
				StzuFail(aDeclarations[i][5], "NAMES '" + cNames + "' resolves to nothing in this declaration")
			ok
			if cK != "MENU" and cK != "FORMAT"
				StzuFail(aDeclarations[i][5], "NAMES must name a MENU or a FORMAT; '" + cNames + "' is a " + cK)
			ok
		ok
	next
	for i = 1 to len(aForms)
		StzuResolveSeats(aForms[i][2], aDeclared)
	next
	# v0.6: a list of a FORM writes one value an item (a one-seat FORM) or a
	# name: value pair an item (a two-seat FORM whose first seat is a name)
	for i = 1 to len(aDeclarations)
		StzuCheckListForms(aDeclarations[i][3], aDeclared, aForms)
	next
	for i = 1 to len(aForms)
		StzuCheckListForms(aForms[i][2], aDeclared, aForms)
	next

	# v0.3: a UNION's alternatives are value types, told apart by shape
	for i = 1 to len(aUnions)
		aU = aUnions[i]
		aAlts = aU[2]
		aShapes = []
		for j = 1 to len(aAlts)
			cShape = StzuAltShape(aAlts[j], aDeclared, aForms, aU[4])
			for k = 1 to len(aShapes)
				if aShapes[k] = cShape
					StzuFail(aU[4], "'" + aAlts[k][1] + "' and '" + aAlts[j][1] + "' have the same shape (" + cShape + "): a UNION's alternatives are told apart by shape")
				ok
			next
			aShapes + cShape
		next
	next
	# v0.3: MESSAGES speaks for a reference seat
	for i = 1 to len(aDeclarations)
		aMsgs = aDeclarations[i][7]
		aSeats = aDeclarations[i][3]
		for j = 1 to len(aMsgs)
			aFound = NULL
			for k = 1 to len(aSeats)
				if aSeats[k][1] = aMsgs[j][1] aFound = aSeats[k] ok
			next
			if isNull(aFound)
				StzuFail(aMsgs[j][3], "MESSAGES: no seat '" + aMsgs[j][1] + "' on " + aDeclarations[i][1])
			ok
			bRef = 0
			if DeclaredKind(aDeclared, aFound[2]) = "DECLARATION" bRef = 1 ok
			bReq = 1
			if aFound[3] or aFound[4] bReq = 0 ok
			if not bRef and not bReq
				StzuFail(aMsgs[j][3], "MESSAGES speaks for a reference seat when its name resolves to nothing, or for a required seat when it is absent; '" + aMsgs[j][1] + "' is neither")
			ok
		next
	next

	# v0.4: a SENTENCE names another language's declaration, read beside this
	# one and judged by this same meta-court; its record is kept for the paths
	# that read through it
	for i = 1 to len(aSentences)
		aS = aSentences[i]
		cPath = aS[2]
		if $cStzuDir != "" cPath = $cStzuDir + "/" + cPath ok
		if not fexists(cPath)
			StzuFail(aS[6], "SENTENCE " + aS[1] + ": '" + aS[2] + "' cannot be read from beside this declaration")
		ok
		cInnerSrc = read(cPath)
		aSaveToks = $aStzuToks
		nSavePos = $nStzuPos
		cSaveDir = $cStzuDir
		$cStzuDir = StzuDirOf(cPath)
		cErr = ""
		aInner = NULL
		try
			aInner = StzuDeclare(cInnerSrc)
		catch
			cErr = cCatchError
		done
		$aStzuToks = aSaveToks
		$nStzuPos = nSavePos
		$cStzuDir = cSaveDir
		if cErr != ""
			StzuFail(aS[6], "SENTENCE " + aS[1] + ": " + aS[2] + " is refused: " + cErr)
		ok
		aSentences[i][3] = aInner
	next

	# menu coherence, both ways
	for i = 1 to len(aExpressions)
		aE = aExpressions[i]
		bVar = 0 bAgg = 0
		aOpd = aE[3]
		for j = 1 to len(aOpd)
			if aOpd[j] = "var" bVar = 1 ok
			if aOpd[j] = "agg" bAgg = 1 ok
		next
		if bVar and isNull(aE[5]) StzuFail(aE[7], "operand 'var' requires a VARIABLES clause") ok
		if not isNull(aE[5]) and not bVar StzuFail(aE[7], "a VARIABLES clause requires operand 'var'") ok
		if bAgg and isNull(aE[4]) StzuFail(aE[7], "operand 'agg' requires an AGGREGATES clause") ok
		if not isNull(aE[4]) and not bAgg StzuFail(aE[7], "an AGGREGATES clause requires operand 'agg'") ok
	next

	# the WORLD: ONE and FIRST name declarations
	aOneDecls = []
	if not isNull(aWorld)
		aOne = aWorld[1]
		for i = 1 to len(aOne)
			cK = DeclaredKind(aDeclared, aOne[i])
			if cK = "" StzuFail(aWorld[3], "ONE: '" + aOne[i] + "' resolves to nothing in this declaration") ok
			if cK != "DECLARATION" StzuFail(aWorld[3], "ONE must name a DECLARATION; '" + aOne[i] + "' is a " + cK) ok
		next
		aOneDecls = aOne
		if aWorld[2] != ""
			cK = DeclaredKind(aDeclared, aWorld[2])
			if cK = "" StzuFail(aWorld[3], "FIRST: '" + aWorld[2] + "' resolves to nothing in this declaration") ok
			if cK != "DECLARATION" StzuFail(aWorld[3], "FIRST must name a DECLARATION; '" + aWorld[2] + "' is a " + cK) ok
		ok
	ok

	# the condition tables: this language and the languages its SENTENCEs name
	aRec = [ ["name", cLName], ["version", cLVersion], ["grammar", cLGrammar],
	         ["court", cLCourt], ["extension", cLExtension], ["rationale", cLRationale],
	         ["declarations", aDeclarations], ["forms", aForms],
	         ["expressions", aExpressions], ["refusals", aRefusals],
	         ["menus", aMenus], ["ranges", aRanges], ["formats", aFormats],
	         ["constraints", aConstraints], ["world", aWorld], ["refine", aRefine],
	         ["unions", aUnions], ["sentences", aSentences], ["views", aViews],
	         ["walks", aWalks] ]
	$cCondLang = cLName
	$aCondLangs = StzuCondLangs(aRec, [])
	$aCondFormats = []
	for i = 1 to len(aFormats)
		$aCondFormats + [aFormats[i][1], aFormats[i][2]]
	next

	# v0.4: the VIEWs, in order (a VIEW reads the VIEWs declared before it)
	aViewEntries = []
	for i = 1 to len(aViews)
		aV = aViews[i]
		cOn = aV[2]
		if cOn != ""
			cK = DeclaredKind(aDeclared, cOn)
			if cK = "" StzuFail(aV[6], "ON: '" + cOn + "' resolves to nothing in this declaration") ok
			if cK != "DECLARATION" StzuFail(aV[6], "ON must name a DECLARATION; '" + cOn + "' is a " + cK) ok
			if StzuHasSeat(aDeclarations, cOn, aV[1])
				StzuFail(aV[6], "VIEW '" + aV[1] + "' is already a seat of " + cOn + ": one name, one meaning")
			ok
		ok
		aOut = [NULL]
		cErr = ""
		cWhy = ""
		try
			cWhy = CondValidateView([aV[1], cOn, aV[3], aV[4], aV[5]], cLName, aOut)
		catch
			cErr = cCatchError
		done
		if cErr != "" StzuFail(aV[6], "VIEW " + aV[1] + ": " + cErr) ok
		if cWhy != "" StzuFail(aV[6], "VIEW " + aV[1] + ": " + cWhy) ok
		aViewEntries + [aV[1], cOn, aOut[1], aV[3], aV[4], aV[5]]
		$aCondLangs = StzuCondLangs(aRec, aViewEntries)
	next

	# the CONSTRAINTs: ON names a declaration; every name a condition uses exists
	for i = 1 to len(aConstraints)
		aC = aConstraints[i]
		cK = DeclaredKind(aDeclared, aC[2])
		if cK = "" StzuFail(aC[6], "ON: '" + aC[2] + "' resolves to nothing in this declaration") ok
		if cK != "DECLARATION" StzuFail(aC[6], "ON must name a DECLARATION; '" + aC[2] + "' is a " + cK) ok
		StzuCheckCondition(aC[3], aC[2], aOneDecls, aC[6])
		if aC[4] != ""
			StzuCheckCondition(aC[4], aC[2], aOneDecls, aC[6])
		ok
	next

	# v0.6: a WALK names the kind it walks, the kind of its steps, and the seats
	# of a step that carry its walk, its rank, its guards, its computed value
	# and its failure
	for i = 1 to len(aWalks)
		aW = aWalks[i]
		nL = aW[10]
		for j = 1 to i - 1
			if aWalks[j][2] = aW[2]
				StzuFail(nL, "'" + aW[2] + "' is already walked by " + aWalks[j][1] + ": a kind is walked once")
			ok
		next
		cK = DeclaredKind(aDeclared, aW[2])
		if cK = "" StzuFail(nL, "OF: '" + aW[2] + "' resolves to nothing in this declaration") ok
		if cK != "DECLARATION" StzuFail(nL, "OF must name a DECLARATION; '" + aW[2] + "' is a " + cK) ok
		cK = DeclaredKind(aDeclared, aW[3])
		if cK = "" StzuFail(nL, "STEPS: '" + aW[3] + "' resolves to nothing in this declaration") ok
		if cK != "DECLARATION" StzuFail(nL, "STEPS must name a DECLARATION; '" + aW[3] + "' is a " + cK) ok
		aStepSeats = StzuSeatsOf(aDeclarations, aW[3])
		aT = StzuSeatNamed(aStepSeats, aW[4])
		if isNull(aT) or aT[2] != aW[2] or aT[3]
			StzuFail(nL, "THROUGH names a seat of " + aW[3] + " that refers to " + aW[2] + "; '" + aW[4] + "' is not one")
		ok
		aO = StzuSeatNamed(aStepSeats, aW[5])
		if isNull(aO) or aO[3] or not (aO[2] = "number" or DeclaredKind(aDeclared, aO[2]) = "RANGE")
			StzuFail(nL, "ORDER names a number seat of " + aW[3] + "; '" + aW[5] + "' is not one")
		ok
		aG = aW[6]
		for j = 1 to len(aG)
			cP = aG[j][1]
			nDot = substr(cP, ".")
			if nDot = 0
				aS = StzuSeatNamed(aStepSeats, cP)
				if isNull(aS) StzuFail(aG[j][2], "GUARDS: no seat '" + cP + "' on " + aW[3]) ok
				if aS[3] or DeclaredKind(aDeclared, aS[2]) != "EXPRESSION"
					StzuFail(aG[j][2], "GUARDS: '" + cP + "' is not an expression seat of " + aW[3])
				ok
			else
				cHead = left(cP, nDot - 1)
				cTail = substr(cP, nDot + 1)
				aS = StzuSeatNamed(aStepSeats, cHead)
				if isNull(aS) StzuFail(aG[j][2], "GUARDS: no seat '" + cHead + "' on " + aW[3]) ok
				if aS[3] or DeclaredKind(aDeclared, aS[2]) != "DECLARATION"
					StzuFail(aG[j][2], "GUARDS: '" + cHead + "' is not a reference seat of " + aW[3] + ", so '" + cP + "' reads through nothing")
				ok
				aS2 = StzuSeatNamed(StzuSeatsOf(aDeclarations, aS[2]), cTail)
				if isNull(aS2) or aS2[3] or DeclaredKind(aDeclared, aS2[2]) != "EXPRESSION"
					StzuFail(aG[j][2], "GUARDS: '" + cP + "' is not an expression seat (no expression seat '" + cTail + "' on " + aS[2] + ")")
				ok
			ok
		next
		if aW[7] != ""
			aS = StzuSeatNamed(aStepSeats, aW[7])
			if isNull(aS) or aS[3] or not (aS[2] = "name" or aS[2] = "text")
				StzuFail(nL, "COMPUTE names a name or text seat of " + aW[3] + "; '" + aW[7] + "' is not one")
			ok
		ok
		if aW[8] != ""
			aS = StzuSeatNamed(aStepSeats, aW[8])
			if isNull(aS) or aS[3] or DeclaredKind(aDeclared, aS[2]) != "EXPRESSION"
				StzuFail(nL, "FORMULA names an expression seat of " + aW[3] + "; '" + aW[8] + "' is not one")
			ok
		ok
		if (aW[7] = "") != (aW[8] = "")
			StzuFail(nL, "COMPUTE and FORMULA go together: the computed seat and the expression that fills it")
		ok
		if aW[9] != ""
			aS = StzuSeatNamed(aStepSeats, aW[9])
			if isNull(aS) or aS[3] or not (aS[2] = "name" or aS[2] = "text" or DeclaredKind(aDeclared, aS[2]) = "MENU")
				StzuFail(nL, "FAIL names a name, text or MENU seat of " + aW[3] + "; '" + aW[9] + "' is not one")
			ok
		ok
	next

	# the REFINE: every point is a seat of a declaration; kinds and floors are closed
	if not isNull(aRefine)
		aPoints = aRefine[1]
		for i = 1 to len(aPoints)
			aP = aPoints[i]
			if not StzuHasSeat(aDeclarations, aP[1], aP[2])
				StzuFail(aP[4], "no such point '" + aP[1] + "." + aP[2] + "': a point is a seat of a declaration of this language")
			ok
			if not InStrList(aP[3], StzuRefinementKinds())
				StzuFail(aP[4], "'" + aP[3] + "' is not a refinement kind: knob, field, symbol, policy, composite or pipeline")
			ok
		next
		aFloors = aRefine[2]
		for i = 1 to len(aFloors)
			aF = aFloors[i]
			if not InStrList(aF[3], StzuPostures())
				StzuFail(aF[4], "'" + aF[3] + "' is not a posture: trusted, external, sandboxed or llm")
			ok
			bPoint = 0
			for j = 1 to len(aPoints)
				if aPoints[j][1] = aF[1] and aPoints[j][2] = aF[2] bPoint = 1 ok
			next
			if not bPoint
				StzuFail(aF[4], "'" + aF[1] + "." + aF[2] + "' is not a declared point: a FLOOR stands on a POINT")
			ok
		next
	ok

	return aRec

# the value shape of a UNION's alternative, or the refusal (v0.3)
func StzuAltShape(aAlt, aDeclared, aForms, nLine)
	cOf = aAlt[1]
	cK = DeclaredKind(aDeclared, cOf)
	if aAlt[2]
		if cK = ""
			StzuFail(nLine, "alternative '" + cOf + "' resolves to nothing in this declaration")
		ok
		if cK != "FORM"
			StzuFail(nLine, "'" + cOf + "' cannot be an alternative of a UNION as a list: a list alternative is a list of a FORM")
		ok
		for i = 1 to len(aForms)
			if aForms[i][1] = cOf
				aFS = aForms[i][2]
				if len(aFS) > 0
					if aFS[1][2] = "text" return "stringlist" ok
					if DeclaredKind(aDeclared, aFS[1][2]) = "FORMAT" return "stringlist" ok
				ok
			ok
		next
		return "namelist"
	ok
	if cOf = "text" return "string" ok
	if cOf = "number" return "number" ok
	if InStrList(cOf, StzuPrimitives()) return "word" ok
	if cK = ""
		StzuFail(nLine, "alternative '" + cOf + "' resolves to nothing in this declaration")
	ok
	if cK = "MENU" return "word" ok
	if cK = "RANGE" return "number" ok
	if cK = "FORMAT" return "string" ok
	StzuFail(nLine, "'" + cOf + "' cannot be an alternative of a UNION: an alternative is a MENU, a RANGE, a FORMAT, a primitive or a list of a FORM, not a " + cK)

func StzuSeatsOf(aDeclarations, cDecl)
	for i = 1 to len(aDeclarations)
		if aDeclarations[i][1] = cDecl return aDeclarations[i][3] ok
	next
	return []

func StzuSeatNamed(aSeats, cSeat)
	for i = 1 to len(aSeats)
		if aSeats[i][1] = cSeat return aSeats[i] ok
	next
	return NULL

# v0.6: a list seat whose element is a FORM of exactly two seats, the first a
# name and the second a scalar, is written as name: value pairs; every other
# FORM keeps v0.1's reading (its items follow the form's first seat), because
# the pinned judge lists a six-seat FORM and v0.6 refuses nothing v0.5 accepted
func StzuIsPairForm(aFS)
	if len(aFS) != 2 return 0 ok
	if aFS[1][2] != "name" or aFS[1][3] return 0 ok
	if aFS[2][3] return 0 ok
	return 1

func StzuCheckListForms(aSeats, aDeclared, aForms)
	for i = 1 to len(aSeats)
		aS = aSeats[i]
		if not aS[3] loop ok
		if DeclaredKind(aDeclared, aS[2]) != "FORM" loop ok
		for j = 1 to len(aForms)
			if aForms[j][1] != aS[2] loop ok
			aFS = aForms[j][2]
			if StzuIsPairForm(aFS)
				# the pair's value is a scalar of the second seat's type: a
				# primitive, a MENU, a RANGE or a FORMAT
				cK2 = DeclaredKind(aDeclared, aFS[2][2])
				if not (InStrList(aFS[2][2], StzuPrimitives()) or cK2 = "MENU" or cK2 = "RANGE" or cK2 = "FORMAT")
					StzuFail(aS[5], "a list of a FORM writes name: value pairs when the FORM is a name and a scalar; the second seat of '" + aS[2] + "' is a " + cK2 + ", which a pair cannot hold")
				ok
			ok
		next
	next

func StzuHasSeat(aDeclarations, cDecl, cSeat)
	for i = 1 to len(aDeclarations)
		if aDeclarations[i][1] = cDecl
			aS = aDeclarations[i][3]
			for j = 1 to len(aS)
				if aS[j][1] = cSeat return 1 ok
			next
		ok
	next
	return 0

func StzuCheckCondition(cCond, cOn, aOneDecls, nLine)
	aAst = NULL
	cErr = ""
	try
		aAst = CondParse(cCond)
	catch
		cErr = cCatchError
	done
	if cErr != ""
		StzuFail(nLine, cErr + " -- in '" + cCond + "'")
	ok
	cWhy = CondValidate(aAst, cOn, aOneDecls, "")
	if cWhy != ""
		StzuFail(nLine, cWhy + " -- in '" + cCond + "'")
	ok

# a seat type resolves to a primitive, a FORM, an EXPRESSION, a MENU, a RANGE,
# a FORMAT or a DECLARATION (a reference); a list seat's element is a FORM, a
# DECLARATION or a MENU
func StzuResolveSeats(aSeats, aDeclared)
	for i = 1 to len(aSeats)
		aS = aSeats[i]
		cOf = aS[2]
		if aS[3]
			cK = DeclaredKind(aDeclared, cOf)
			if cK = ""
				StzuFail(aS[5], "seat type '" + cOf + "' resolves to nothing in this declaration")
			ok
			if cK != "FORM" and cK != "DECLARATION" and cK != "MENU"
				StzuFail(aS[5], "a list seat's element must be a declared FORM, DECLARATION or MENU; '" + cOf + "' is not")
			ok
		but not InStrList(cOf, StzuPrimitives())
			cK = DeclaredKind(aDeclared, cOf)
			if cK = ""
				StzuFail(aS[5], "seat type '" + cOf + "' resolves to nothing in this declaration")
			ok
			if cK != "FORM" and cK != "EXPRESSION" and cK != "MENU" and cK != "RANGE" and cK != "FORMAT" and cK != "DECLARATION" and cK != "UNION" and cK != "SENTENCE"
				StzuFail(aS[5], "seat type '" + cOf + "' must name a FORM, an EXPRESSION, a MENU, a RANGE, a FORMAT, a DECLARATION, a UNION or a SENTENCE, not a " + cK)
			ok
		ok
	next

# ---- the printed verdict ----------------------------------------------------

func StzuPrintLanguage(aLang)
	? "ok"
	? "language " + LangGet(aLang, "name")
	? "version " + LangGet(aLang, "version")
	? "grammar " + LangGet(aLang, "grammar")
	? "court " + LangGet(aLang, "court")
	? "extension " + LangGet(aLang, "extension")
	? "rationale " + LangGet(aLang, "rationale")
	? "declarations " + len(LangGet(aLang, "declarations"))
	? "forms " + len(LangGet(aLang, "forms"))
	? "expressions " + len(LangGet(aLang, "expressions"))
	? "refusals " + len(LangGet(aLang, "refusals"))
	? "menus " + len(LangGet(aLang, "menus"))
	? "ranges " + len(LangGet(aLang, "ranges"))
	? "formats " + len(LangGet(aLang, "formats"))
	? "unions " + len(LangGet(aLang, "unions"))
	? "sentences " + len(LangGet(aLang, "sentences"))
	? "views " + len(LangGet(aLang, "views"))
	? "constraints " + len(LangGet(aLang, "constraints"))
	nCtx = 0
	aE = LangGet(aLang, "expressions")
	for i = 1 to len(aE)
		if len(aE[i]) >= 8 nCtx += len(aE[i][8]) ok
	next
	? "contexts " + nCtx
	? "walks " + len(LangGet(aLang, "walks"))
	nWorld = 0
	if not isNull(LangGet(aLang, "world")) nWorld = 1 ok
	? "world " + nWorld
	nPoints = 0
	aR = LangGet(aLang, "refine")
	if not isNull(aR) nPoints = len(aR[1]) ok
	? "points " + nPoints
	aD = LangGet(aLang, "declarations")
	aV = []
	for i = 1 to len(aD)
		aV + aD[i][2]
	next
	aV = sort(aV)
	cV = ""
	for i = 1 to len(aV)
		if i > 1 cV += "," ok
		cV += aV[i]
	next
	? "verbs " + cV
