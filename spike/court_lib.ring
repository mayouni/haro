# court_lib.ring -- the generic court of a declared language, in pure core Ring.
#
# A court FORGED from a .stzu declaration is a generated program that loads
# this file and fills five tables (see forge.ring): the language's name and
# extension, its declaration kinds with their typed seats, its forms, and
# its declared refusal phrasings. Everything the DECLARATION says is judged
# here: the Commons' lexical form (C6), the DEFINE shape, the closed verb
# set, the closed clause set per kind, each clause's value shape, a clause
# given twice, a missing RATIONALE, a required seat absent, one namespace.
# What the declaration does NOT say -- a menu of words, a default, an order,
# a rule between two declarations -- is not judged here, and the guard
# counts those apart. That count is the spike's measurement.
#
# Phrasings follow harb's court (harobanda/src/machine.zig) for the shapes
# the Grammar Commons gives every court, so the fixtures' fragments can be
# compared; where the declaration carries a REFUSAL message, it is spoken.
#
# Functions only. Globals ($cCourtLang, $cCourtExt, $aCourtKinds,
# $aCourtForms, $aCourtRefusals, $aCourtToks, $nCourtPos) are born in the
# generated court, at its top level, for both runtimes' sake.

# ---- character classes by byte code (HF-30) ---------------------------------

func CtIsDigit(c)
	n = ascii(c)
	return (n >= 48 and n <= 57)

func CtIsLowerish(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or n = 95 or (n >= 48 and n <= 57)

func CtIsUpperish(c)
	n = ascii(c)
	return (n >= 65 and n <= 90) or n = 95 or (n >= 48 and n <= 57)

func CtIsWordChar(c)
	return CtIsLowerish(c) or CtIsUpperish(c)

func CtFail(nLine, cMsg)
	raise($cCourtLang + " (line " + nLine + "): " + cMsg)

func CtInList(cS, aL)
	for i = 1 to len(aL)
		if aL[i] = cS return 1 ok
	next
	return 0

func CtJoin(aL, cSep)
	cOut = ""
	for i = 1 to len(aL)
		if i > 1 cOut += cSep ok
		cOut += aL[i]
	next
	return cOut

# the declared refusal message of a category, or ""
func CtRefusalMessage(cCategory)
	for i = 1 to len($aCourtRefusals)
		if $aCourtRefusals[i][1] = cCategory return $aCourtRefusals[i][2] ok
	next
	return ""

# ---- tokenizer: the Commons' lexical form, as harb's court reads it ---------
# a token is [type, text, line]; types: string number ident keyword
# lparen rparen lbracket rbracket comma eof

func CtTokenize(cSrc)
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
			# C6 3.2: a continuation line's leading whitespace folds to one
			# space (harb keeps what stands before the newline; \r is dropped)
			nStart = nLine
			nStrBeg = i
			cBuf = ""
			i++
			bClosed = 0
			while i <= n
				d = cSrc[i]
				if d = '"'
					bClosed = 1
					i++
					exit
				ok
				if d = char(10)
					nLine++
					i++
					while i <= n and (cSrc[i] = " " or cSrc[i] = char(9) or cSrc[i] = char(13))
						i++
					end
					cBuf += " "
					loop
				ok
				if d = char(13)
					i++
					loop
				ok
				cBuf += d
				i++
			end
			if not bClosed
				CtFail(nStart, "Unterminated string")
			ok
			# a token is [type, text, line, start, end]: start is the index of
			# its first byte, end the index after its last, so the gate can
			# splice a value's span and nothing else (nStrBeg was set at the quote)
			aToks + ["string", cBuf, nStart, nStrBeg, i]
		but CtIsDigit(c)
			j = i
			while j <= n and CtIsDigit(cSrc[j])
				j++
			end
			if j <= n and CtIsWordChar(cSrc[j])
				CtFail(nLine, "'" + substr(cSrc, i, j - i + 1) + "' is neither a number nor a word")
			ok
			aToks + ["number", substr(cSrc, i, j - i), nLine, i, j]
			i = j
		but CtIsWordChar(c)
			j = i
			while j <= n and CtIsWordChar(cSrc[j])
				j++
			end
			cW = substr(cSrc, i, j - i)
			bLower = 1
			bUpper = 1
			for k = 1 to len(cW)
				nK = ascii(cW[k])
				if nK >= 97 and nK <= 122 bUpper = 0 ok
				if nK >= 65 and nK <= 90 bLower = 0 ok
			next
			if bLower
				aToks + ["ident", cW, nLine, i, j]
			but bUpper
				aToks + ["keyword", cW, nLine, i, j]
			else
				CtFail(nLine, "'" + cW + "' is neither a lower_snake identifier nor an UPPER_SNAKE keyword")
			ok
			i = j
		else
			cT = ""
			if c = "(" cT = "lparen"
			but c = ")" cT = "rparen"
			but c = "[" cT = "lbracket"
			but c = "]" cT = "rbracket"
			but c = "," cT = "comma"
			ok
			if cT = ""
				CtFail(nLine, "The character '" + c + "' is not part of the " + $cCourtLang + " grammar")
			ok
			aToks + [cT, c, nLine, i, i + 1]
			i++
		ok
	end
	aToks + ["eof", "", nLine, n + 1, n + 1]
	return aToks

# ---- the tables, read ---------------------------------------------------------

func CtKindByVerb(cVerb)
	for i = 1 to len($aCourtKinds)
		if $aCourtKinds[i][1] = cVerb return $aCourtKinds[i] ok
	next
	return NULL

func CtVerbs()
	aV = []
	for i = 1 to len($aCourtKinds)
		aV + $aCourtKinds[i][1]
	next
	return aV

func CtFormByName(cName)
	for i = 1 to len($aCourtForms)
		if $aCourtForms[i][1] = cName return $aCourtForms[i] ok
	next
	return NULL

# a seat is [name, of, isList, optional]; its clause name is the seat's name
# in UPPER_SNAKE, and its value shape follows its type:
#   text -> string, name/flag/ref -> word, number -> number,
#   [form] -> a list whose items follow the form's first seat (text ->
#   stringlist, else namelist)
func CtClauseShape(aSeat)
	cOf = aSeat[2]
	if aSeat[3]
		aF = CtFormByName(cOf)
		if isNull(aF) return "namelist" ok
		aFS = aF[2]
		if len(aFS) > 0 and aFS[1][2] = "text" return "stringlist" ok
		return "namelist"
	ok
	if cOf = "text" return "string" ok
	if cOf = "number" return "number" ok
	return "word"

func CtAllowedClauses(aKind)
	aS = aKind[3]
	aOut = []
	for i = 1 to len(aS)
		aOut + upper(aS[i][1])
	next
	return aOut

func CtSeatByClause(aKind, cClause)
	aS = aKind[3]
	for i = 1 to len(aS)
		if upper(aS[i][1]) = cClause return aS[i] ok
	next
	return NULL

# ---- parser ----------------------------------------------------------------

func CtPeek()
	return $aCourtToks[$nCourtPos]

func CtNext()
	t = $aCourtToks[$nCourtPos]
	if t[1] != "eof" $nCourtPos++ ok
	return t

func CtShown(t)
	if t[1] = "eof" return "end of file" ok
	return t[2]

func CtExpect(cType, cWhat)
	t = CtNext()
	if t[1] != cType
		CtFail(t[3], "Expected " + cWhat + ", found '" + CtShown(t) + "'")
	ok
	return t

# a value is [shape, payload, start, end]: word/string/number carry text;
# namelist and stringlist carry a list; an empty list is [namelist, []];
# start and end are the value's byte span in the source
func CtParseValue()
	t = CtNext()
	if t[1] = "ident" return ["word", t[2], t[4], t[5]] ok
	if t[1] = "string" return ["string", t[2], t[4], t[5]] ok
	if t[1] = "number" return ["number", t[2], t[4], t[5]] ok
	if t[1] = "lbracket"
		aNames = []
		aStrings = []
		while 1
			e = CtPeek()
			if e[1] = "rbracket"
				CtNext()
				exit
			ok
			item = CtNext()
			if item[1] = "ident"
				aNames + item[2]
			but item[1] = "string"
				aStrings + item[2]
			else
				CtFail(item[3], "A list holds words or strings, found '" + CtShown(item) + "'")
			ok
			sep = CtPeek()
			if sep[1] = "comma"
				CtNext()
			but sep[1] != "rbracket"
				CtFail(sep[3], "Expected ',' or ']' in a list, found '" + CtShown(sep) + "'")
			ok
		end
		if len(aNames) > 0 and len(aStrings) > 0
			CtFail(t[3], "A list is all words or all strings, never mixed")
		ok
		nListEnd = $aCourtToks[$nCourtPos - 1][5]
		if len(aStrings) > 0 return ["stringlist", aStrings, t[4], nListEnd] ok
		return ["namelist", aNames, t[4], nListEnd]
	ok
	CtFail(t[3], "Expected a clause value, found '" + CtShown(t) + "'")

# one DEFINE <VERB> <name> AS ( clauses ) RATIONALE "..."
# returns [verb, name, line, clauses, rationale]; a clause is [NAME, line, value]
func CtParseDecl()
	tV = CtNext()
	if not (tV[1] = "keyword" and tV[2] = "DEFINE")
		cMsg = CtRefusalMessage("unknown_verb")
		if cMsg = "" cMsg = "the " + $cCourtLang + " verb set is closed (DEFINE)" ok
		CtFail(tV[3], "Unknown verb '" + CtShown(tV) + "': " + cMsg)
	ok
	tK = CtNext()
	aKind = NULL
	if tK[1] = "keyword" aKind = CtKindByVerb(tK[2]) ok
	if isNull(aKind)
		cMsg = CtRefusalMessage("unknown_declaration")
		if cMsg = "" cMsg = "the kinds are closed (" + CtJoin(CtVerbs(), ", ") + ")" ok
		CtFail(tK[3], "Unknown kind '" + CtShown(tK) + "': " + cMsg)
	ok
	tName = CtExpect("ident", "a lower_snake name")
	tAs = CtNext()
	if not (tAs[1] = "keyword" and tAs[2] = "AS")
		CtFail(tAs[3], "Expected AS after the name, found '" + CtShown(tAs) + "'")
	ok
	CtExpect("lparen", "'('")
	aClauses = []
	aAllowed = CtAllowedClauses(aKind)
	while 1
		t = CtPeek()
		if t[1] = "rparen"
			CtNext()
			exit
		ok
		tC = CtNext()
		if tC[1] != "keyword"
			CtFail(tC[3], "Expected a clause name, found '" + CtShown(tC) + "'")
		ok
		if not CtInList(tC[2], aAllowed)
			cMsg = CtRefusalMessage("unknown_seat")
			if cMsg = "" cMsg = "allowed are " + CtJoin(aAllowed, ", ") ok
			CtFail(tC[3], "Unknown clause '" + tC[2] + "' for " + aKind[1] + ": " + cMsg)
		ok
		for i = 1 to len(aClauses)
			if aClauses[i][1] = tC[2]
				CtFail(tC[3], "Clause " + tC[2] + " given twice")
			ok
		next
		aVal = CtParseValue()
		# a clause is [NAME, line, value, start, end] -- the value's span
		aClauses + [tC[2], tC[3], aVal, aVal[3], aVal[4]]
		sep = CtPeek()
		if sep[1] = "comma"
			CtNext()
		but sep[1] != "rparen"
			CtFail(sep[3], "Expected ',' or ')' after a clause, found '" + CtShown(sep) + "'")
		ok
	end
	tR = CtNext()
	if not (tR[1] = "keyword" and tR[2] = "RATIONALE")
		CtFail(tR[3], "RATIONALE is mandatory on every declaration (" + aKind[1] + " " + tName[2] + " has none)")
	ok
	tRS = CtExpect("string", "the RATIONALE string")
	return [aKind[1], tName[2], tName[3], aClauses, tRS[2]]

# ---- the structural court ---------------------------------------------------

func CtWantShape(aDecl, aClause, cShape)
	cGot = aClause[3][1]
	cName = aClause[1]
	if cShape = "word"
		if cGot != "word" CtFail(aClause[2], "Clause " + cName + " takes a word") ok
	but cShape = "string"
		if cGot != "string" CtFail(aClause[2], "Clause " + cName + " takes a string") ok
	but cShape = "number"
		if cGot != "number" CtFail(aClause[2], "Clause " + cName + " takes a number") ok
	but cShape = "namelist"
		if cGot = "stringlist" and len(aClause[3][2]) = 0 return ok
		if cGot != "namelist" CtFail(aClause[2], "Clause " + cName + " takes a list of words") ok
	but cShape = "stringlist"
		if cGot = "namelist" and len(aClause[3][2]) = 0 return ok
		if cGot != "stringlist" CtFail(aClause[2], "Clause " + cName + " takes a string list, one word per string") ok
	ok

# parse a whole source and judge what the declaration can judge; returns the
# list of declarations
func CtDeclare(cSrc)
	$aCourtToks = CtTokenize(cSrc)
	$nCourtPos = 1
	aDecls = []
	while CtPeek()[1] != "eof"
		aDecls + CtParseDecl()
	end
	if len(aDecls) = 0
		CtFail(1, "A " + $cCourtLang + " file declares nothing")
	ok
	# one namespace
	for i = 1 to len(aDecls)
		for j = 1 to i - 1
			if aDecls[i][2] = aDecls[j][2]
				cMsg = CtRefusalMessage("duplicate_name")
				if cMsg = "" cMsg = "one namespace, no duplicates" ok
				CtFail(aDecls[i][3], "'" + aDecls[i][2] + "' is already declared (line " + aDecls[j][3] + "); " + cMsg)
			ok
		next
	next
	# every clause's value has the seat's shape; every required seat is present
	for i = 1 to len(aDecls)
		aD = aDecls[i]
		aKind = CtKindByVerb(aD[1])
		aC = aD[4]
		for j = 1 to len(aC)
			aSeat = CtSeatByClause(aKind, aC[j][1])
			CtWantShape(aD, aC[j], CtClauseShape(aSeat))
		next
		aSeats = aKind[3]
		for j = 1 to len(aSeats)
			aSeat = aSeats[j]
			if aSeat[3] or aSeat[4] loop ok
			bFound = 0
			for k = 1 to len(aC)
				if aC[k][1] = upper(aSeat[1]) bFound = 1 ok
			next
			if not bFound
				CtFail(aD[3], upper(aSeat[1]) + " is required on " + aD[1] + " " + aD[2])
			ok
		next
	next
	return aDecls

# ---- the printed verdict -----------------------------------------------------

func CtPrintVerdict(aDecls)
	? "ok"
	aFirst = aDecls[1]
	? "name " + aFirst[2]
	? "rationale " + aFirst[5]
	aC = aFirst[4]
	for i = 1 to len(aC)
		if aC[i][3][1] = "word" or aC[i][3][1] = "string" or aC[i][3][1] = "number"
			? lower(aC[i][1]) + " " + aC[i][3][2]
		ok
	next
	aV = CtVerbs()
	for i = 1 to len(aV)
		n = 0
		for j = 1 to len(aDecls)
			if aDecls[j][1] = aV[i] n++ ok
		next
		? "count " + aV[i] + " " + n
	next

# ---- the refinement gate ------------------------------------------------------
# `<court>.ring refine <file> <file.rfn>`: one refinement, judged by the
# five stages before it lands (charter section 6; stzRefinableCode.ring's
# order): structural -- the refined text is a sentence of the language;
# constraint -- the point exists, FROM is its value, TO has the seat's
# shape; derivation -- the whole file still holds (one namespace, required
# seats); governance -- an author and a reason are named; trust -- the
# proposal's posture reaches the point's floor. Admitted, the refined text
# is written to <file>.refined and the inverse to <file>.revert.rfn; the
# refusal is one human line and one C2 record (JSON) beneath it.

func CtJson(cS)
	cOut = ""
	for i = 1 to len(cS)
		c = cS[i]
		if c = '"' or c = char(92)
			cOut += char(92) + c
		but c = char(10)
			cOut += char(92) + "n"
		else
			cOut += c
		ok
	next
	return '"' + cOut + '"'

func CtRecord(cCode, cMsg, cFile, nLine, aCites, cWhy, cTodo)
	cC = ""
	for i = 1 to len(aCites)
		if i > 1 cC += ", " ok
		cC += CtJson(aCites[i])
	next
	return '{"code": ' + CtJson(cCode) + ', "severity": "error", "message": ' + CtJson(cMsg) +
	       ', "span": {"file": ' + CtJson(cFile) + ', "line": ' + nLine + '}, "cites": [' + cC + ']' +
	       ', "language": ' + CtJson($cCourtLang) + ', "why": ' + CtJson(cWhy) + ', "todo": ' + CtJson(cTodo) + '}'

func CtPostureRank(cP)
	if cP = "trusted" return 3 ok
	if cP = "external" return 2 ok
	if cP = "sandboxed" return 1 ok
	if cP = "llm" return 0 ok
	return -1

# the refinement sentence's own tables (rfn.stzu), read by the same parser
func CtRfnKinds()
	return [ ["REFINE", "refinement", [ ["target", "text", 0, 0], ["kind", "name", 0, 0], ["from", "text", 0, 0],
	          ["to", "text", 0, 0], ["author", "text", 0, 0], ["posture", "name", 0, 0], ["reason", "text", 0, 0] ]] ]

func CtClauseText(aDecl, cClause)
	aC = aDecl[4]
	for i = 1 to len(aC)
		if aC[i][1] = cClause return aC[i][3][2] ok
	next
	return NULL

func CtRefuse(cStage, cCode, cMsg, cFile, nLine, aCites, cWhy, cTodo)
	? $cCourtLang + " (line " + nLine + "): " + cStage + ": " + cMsg
	? CtRecord(cCode, cStage + ": " + cMsg, cFile, nLine, aCites, cWhy, cTodo)

func CtRefine(cFile, cRfnFile)
	cSrc = read(cFile)
	cRfn = read(cRfnFile)

	# the refinement sentence, parsed by this court with the rfn tables
	aSaveKinds = $aCourtKinds
	aSaveLang = $cCourtLang
	$aCourtKinds = CtRfnKinds()
	$cCourtLang = "rfn"
	aR = NULL
	cErr = ""
	try
		aRs = CtDeclare(cRfn)
		aR = aRs[1]
	catch
		cErr = cCatchError
	done
	$aCourtKinds = aSaveKinds
	$cCourtLang = aSaveLang
	if not isNull(cErr) and cErr != ""
		? cErr
		return
	ok
	cTarget = CtClauseText(aR, "TARGET")
	cFrom = CtClauseText(aR, "FROM")
	cTo = CtClauseText(aR, "TO")
	cAuthor = CtClauseText(aR, "AUTHOR")
	cPosture = CtClauseText(aR, "POSTURE")
	cReason = CtClauseText(aR, "REASON")
	nRLine = aR[3]

	# structural, on the ORIGINAL: the file must be a sentence before it is refined
	aDecls = NULL
	try
		aDecls = CtDeclare(cSrc)
	catch
		CtRefuse("structural", "NOT_A_SENTENCE", cCatchError, cFile, 1, ["rule:structural"],
		         "the gate's structural stage is the language's own court, and the file to refine is not a sentence of it",
		         "make the file a sentence of the language first; then propose the refinement")
		return
	done

	# constraint: the point exists, FROM is its value, TO fits the seat
	nDot = substr(cTarget, ".")
	if nDot = 0
		CtRefuse("constraint", "NO_SUCH_POINT", "the target '" + cTarget + "' is not declaration.CLAUSE", cRfnFile, nRLine,
		         ["rule:constraint"], "a point is a clause of a declaration, named declaration.CLAUSE", "name the point as <declaration>.<CLAUSE>")
		return
	ok
	cDeclName = left(cTarget, nDot - 1)
	cClause = substr(cTarget, nDot + 1)
	aDecl = NULL
	for i = 1 to len(aDecls)
		if aDecls[i][2] = cDeclName aDecl = aDecls[i] ok
	next
	if isNull(aDecl)
		CtRefuse("constraint", "NO_SUCH_POINT", "no declaration '" + cDeclName + "' in " + cFile, cRfnFile, nRLine,
		         ["rule:constraint"], "every named thing is a refinement point, and nothing by this name is declared", "name a declaration the file carries")
		return
	ok
	aKind = CtKindByVerb(aDecl[1])
	aSeat = CtSeatByClause(aKind, cClause)
	if isNull(aSeat)
		CtRefuse("constraint", "NO_SUCH_POINT", aDecl[1] + " has no clause " + cClause + "; allowed are " + CtJoin(CtAllowedClauses(aKind), ", "),
		         cRfnFile, nRLine, ["rule:constraint"], "the point's clause is not a seat of its declaration kind", "name one of the allowed clauses")
		return
	ok
	cShape = CtClauseShape(aSeat)
	if cShape != "word" and cShape != "string" and cShape != "number"
		CtRefuse("constraint", "NOT_A_KNOB", cClause + " is a list seat; this gate refines scalar points only", cRfnFile, nRLine,
		         ["rule:constraint"], "the spike's gate refines knobs, fields and symbols, not composites", "refine a scalar clause")
		return
	ok
	# the clause as written, with its token span
	aClause = NULL
	aC = aDecl[4]
	for i = 1 to len(aC)
		if aC[i][1] = cClause aClause = aC[i] ok
	next
	if isNull(aClause)
		CtRefuse("constraint", "POINT_UNSET", aDecl[1] + " " + cDeclName + " does not write " + cClause + "; this gate refines a clause that is written",
		         cRfnFile, nRLine, ["rule:constraint"], "a refinement changes a value the sentence carries", "write the clause first, then refine it")
		return
	ok
	cCurrent = aClause[3][2]
	if cCurrent != cFrom
		CtRefuse("constraint", "FROM_MISMATCH", cClause + " of " + cDeclName + " is '" + cCurrent + "', not '" + cFrom + "'", cRfnFile, nRLine,
		         ["rule:constraint"], "FROM is an assertion about the point's value, and it does not hold", "state the value the file carries")
		return
	ok
	if cShape = "number"
		for i = 1 to len(cTo)
			if not CtIsDigit(cTo[i])
				CtRefuse("constraint", "SHAPE", cClause + " takes a number, and '" + cTo + "' is not one", cRfnFile, nRLine,
				         ["rule:constraint"], "the seat's shape is declared", "propose a number")
				return
			ok
		next
	but cShape = "word"
		for i = 1 to len(cTo)
			if not CtIsLowerish(cTo[i])
				CtRefuse("constraint", "SHAPE", cClause + " takes a word, and '" + cTo + "' is not lower_snake", cRfnFile, nRLine,
				         ["rule:constraint"], "the seat's shape is declared", "propose a lower_snake word")
				return
			ok
		next
	ok

	# the refined text: the value's span replaced, nothing else touched
	nStart = aClause[4]
	nEnd = aClause[5]
	cNew = cTo
	if cShape = "string" cNew = '"' + cTo + '"' ok
	cRefined = left(cSrc, nStart - 1) + cNew + substr(cSrc, nEnd)

	# derivation: the whole file still holds (the court's checks on the refined text)
	try
		CtDeclare(cRefined)
	catch
		CtRefuse("derivation", "DERIVATION", cCatchError, cFile, aClause[2], ["rule:derivation"],
		         "the refined sentence breaks a rule of the language", "choose a value the language admits")
		return
	done

	# governance: an author and a reason
	if cAuthor = "" or cReason = ""
		CtRefuse("governance", "UNATTRIBUTED", "a refinement names its author and its reason; this one does not", cRfnFile, nRLine,
		         ["rule:governance"], "the audit chain is author, authority, rule, verdict, and an unattributed change has no chain", "name the author and the reason")
		return
	ok

	# trust: the point's floor (this court: trusted for every point) against the posture
	nRank = CtPostureRank(cPosture)
	if nRank < 0
		CtRefuse("trust", "POSTURE", "'" + cPosture + "' is not a posture: trusted, external, sandboxed or llm", cRfnFile, nRLine,
		         ["rule:trust"], "the trust ladder is closed", "name one of the four postures")
		return
	ok
	cFloor = "trusted"
	if nRank < CtPostureRank(cFloor)
		CtRefuse("trust", "TRUST_FLOOR", "posture :" + cPosture + " below the required floor :" + cFloor + " for '" + cTarget + "'", cRfnFile, nRLine,
		         ["rule:trust-floor"], "a point may declare a trust floor, and this court's floor for every point is trusted: a model-composed proposal is refused by construction, not by convention",
		         "a trusted actor may propose the same change; or lower the point's floor in a profile")
		return
	ok

	# admitted: the refined text, and its inverse, written beside the file
	write(cFile + ".refined", cRefined)
	cRevert = "DEFINE REFINE revert_of_" + aR[2] + " AS (" + char(10) +
	          '  TARGET "' + cTarget + '", KIND ' + CtClauseText(aR, "KIND") + ',' + char(10) +
	          '  FROM "' + cTo + '", TO "' + cFrom + '",' + char(10) +
	          '  AUTHOR "' + cAuthor + '", POSTURE ' + cPosture + ',' + char(10) +
	          '  REASON "the inverse of ' + aR[2] + ', computed before it landed"' + char(10) +
	          ') RATIONALE "A revert is its own event; nothing is erased"' + char(10)
	write(cFile + ".revert.rfn", cRevert)
	? "admitted: " + cTarget + " " + cFrom + " -> " + cTo + " [" + cPosture + "] (structural + constraint + derivation + governance + trust passed); inverse in " + cFile + ".revert.rfn"

# the command: check <file> | refine <file> <file.rfn>
func CtMain()
	if len(sysargv) < 4
		? "usage: <court>.ring check <file" + $cCourtExt + "> | refine <file" + $cCourtExt + "> <file.rfn>"
		return
	ok
	cVerb = sysargv[3]
	if cVerb = "check"
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			CtPrintVerdict(aDecls)
		catch
			? cCatchError
		done
	but cVerb = "refine"
		if len(sysargv) < 5
			? "usage: <court>.ring refine <file" + $cCourtExt + "> <file.rfn>"
			return
		ok
		CtRefine(sysargv[4], sysargv[5])
	else
		? "unknown verb '" + cVerb + "'; this court answers: check, refine"
	ok
