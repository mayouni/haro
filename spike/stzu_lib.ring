# stzu_lib.ring -- the stzu v0.1 meta-court, in pure core Ring (no Softanza).
#
# A port of stz/face/stz/Stzu.luau (437 lines, the first conforming
# implementation) so that the declaring altitude of Haro is judged on rnx,
# and A/B'd against the oracle: the same file runs on rnxc and on ring.exe
# and must print the same bytes. The normative text is
# stz/declarative/stzu/GRAMMAR.md; the judge is its fixtures.json.
#
# Refusals are one channel, "stzu (line N): message", raised with raise()
# and caught by the caller. Nothing here executes anything.
#
# Functions only: this file is loaded, never run. Globals carry the $ of
# Rule A so the same text means the same thing on both runtimes.

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

# kind -> list of [clause, shape]; shape is "string", "namelist" or "seatlist"
func StzuClauses(cKind)
	if cKind = "LANGUAGE"
		return [["COURT", "string"], ["EXTENSION", "string"], ["GRAMMAR", "string"], ["VERSION", "string"]]
	but cKind = "DECLARATION"
		return [["SEATS", "seatlist"], ["VERB", "string"]]
	but cKind = "FORM"
		return [["SEATS", "seatlist"]]
	but cKind = "EXPRESSION"
		return [["AGGREGATES", "namelist"], ["OPERANDS", "namelist"], ["OPERATORS", "namelist"], ["VARIABLES", "namelist"]]
	but cKind = "REFUSAL"
		return [["MESSAGE", "string"]]
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
	ok
	return []

func StzuIsKind(cWord)
	return InStrList(cWord, ["LANGUAGE", "DECLARATION", "FORM", "EXPRESSION", "REFUSAL"])

# the allowed clause names of a kind, sorted and comma-joined (the tables
# above are already in sorted order, as Luau's table.sort gives)
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

# Character classes by byte code, never by string ordering: on Ring an
# ordering of two strings where one is numeric ("D" >= "0") converts and
# raises R41 (Ring, Judged by the Record, 2.8); the oracle found it on
# this file's first run, where rnxc had compared silently (HF-30).

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
	raise("stzu (line " + nLine + "): " + cMsg)

# ---- tokenizer --------------------------------------------------------------
# a token is [type, value, line]; types: string number ident keyword
# lparen rparen lbracket rbracket comma colon question eof

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
			# a comment runs to the end of the line
			while i <= n and cSrc[i] != char(10)
				i++
			end
		but c = '"'
			# a string may span lines; continuation whitespace folds to one
			# space (the commons, 3.2): [ \t]*\r?\n[ \t]* -> " ". No escapes.
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
			# ^-?\d+\.?\d*
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

# Luau: string.gsub(raw, "[ \t]*\r?\n[ \t]*", " ") -- spaces and tabs on
# BOTH sides of the newline fold into the one space.
func FoldString(cRaw)
	cOut = ""
	n = len(cRaw)
	i = 1
	while i <= n
		c = cRaw[i]
		if c = char(10) or (c = char(13) and i < n and cRaw[i+1] = char(10))
			# strip the spaces and tabs already emitted before the newline
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

# ---- parser + the meta-court -----------------------------------------------
# The parse state lives in two globals so the small helpers can share it.

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

# [ ident, ident, ] -- trailing comma legal
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

# [ name: type?, other: [form], ] -- a seat is [name, of, isList, optional, line]
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
# returns [kind, name, clauses, rationale, line]; clauses is a list of [NAME, value]
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
		else
			aClauses + [ct[2], StzuParseSeatList()]
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

# The language record: a list of pairs read with LangGet(). Its members:
#   name version grammar court extension rationale
#   declarations: list of [name, verb, seats, rationale, line]
#   forms:        list of [name, seats, rationale, line]
#   expressions:  list of [name, operators, operands, aggregates, variables, rationale, line]
#                 (aggregates / variables are NULL when absent)
#   refusals:     list of [name, message, rationale, line]
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
		StzuFail(1, "an empty file declares nothing -- a .stzu file opens with DEFINE LANGUAGE")
	ok

	bHaveLang = 0
	cLName = "" cLVersion = "" cLGrammar = "" cLCourt = "" cLExtension = "" cLRationale = ""
	aDeclarations = []
	aForms = []
	aExpressions = []
	aRefusals = []
	aDeclared = []     # [name, kind] -- one namespace
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
				StzuFail(nLine, "a .stzu file declares exactly one LANGUAGE")
			ok
			bHaveLang = 1
			cLName = cName
			cLVersion = ClauseValue(aClauses, "VERSION")
			cLGrammar = ClauseValue(aClauses, "GRAMMAR")
			cLCourt = ClauseValue(aClauses, "COURT")
			cLExtension = ClauseValue(aClauses, "EXTENSION")
			cLRationale = cRationale
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
				aDeclarations + [cName, cVerb, ClauseValue(aClauses, "SEATS"), cRationale, nLine]
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
				aExpressions + [cName, aOps, aOpd, aAgg, aVars, cRationale, nLine]
			else
				if not InStrList(cName, StzuRefusalCategories())
					StzuFail(nLine, "'" + cName + "' is not a refusal category")
				ok
				aRefusals + [cName, ClauseValue(aClauses, "MESSAGE"), cRationale, nLine]
			ok
		ok
	end

	# the resolution pass (order-free: forward references are legal; a name
	# resolving to nothing is refused now, never a later surprise)
	for i = 1 to len(aDeclarations)
		StzuResolveSeats(aDeclarations[i][3], aDeclared)
	next
	for i = 1 to len(aForms)
		StzuResolveSeats(aForms[i][2], aDeclared)
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

	return [ ["name", cLName], ["version", cLVersion], ["grammar", cLGrammar],
	         ["court", cLCourt], ["extension", cLExtension], ["rationale", cLRationale],
	         ["declarations", aDeclarations], ["forms", aForms],
	         ["expressions", aExpressions], ["refusals", aRefusals] ]

func StzuResolveSeats(aSeats, aDeclared)
	for i = 1 to len(aSeats)
		aS = aSeats[i]
		cOf = aS[2]
		if aS[3]
			cK = DeclaredKind(aDeclared, cOf)
			if cK = ""
				StzuFail(aS[5], "seat type '" + cOf + "' resolves to nothing in this declaration")
			ok
			if cK != "FORM"
				StzuFail(aS[5], "a list seat's element must be a declared FORM; '" + cOf + "' is not")
			ok
		but not InStrList(cOf, StzuPrimitives())
			cK = DeclaredKind(aDeclared, cOf)
			if cK = ""
				StzuFail(aS[5], "seat type '" + cOf + "' resolves to nothing in this declaration")
			ok
			if cK != "FORM" and cK != "EXPRESSION"
				StzuFail(aS[5], "seat type '" + cOf + "' must name a FORM or an EXPRESSION, not a " + cK)
			ok
		ok
	next

# ---- the printed verdict ----------------------------------------------------
# The structural fields the fixtures' accepts ask for, one per line, so a
# harness reads them without a JSON reader; "ok" first.

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
