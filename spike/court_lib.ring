# court_lib.ring -- the generic court of a declared language, in pure core Ring.
#
# A court FORGED from a .haro declaration is a generated program that loads
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
# v0.2 (haro/spike/v02/GRAMMAR.md): a seat's type may be a MENU (a word of
# its WORDS), a RANGE (a number within it), a FORMAT (a text of its shape)
# or a DECLARATION (a reference that must resolve); a declaration's NAMES
# are drawn from a MENU or a FORMAT; the WORLD's ONE and FIRST hold; every
# CONSTRAINT's condition is evaluated on every declaration of its ON kind,
# and its MESSAGE is spoken with {name}, {seat}, {other} and {decl.seat}
# filled in. The refinement gate reads the REFINE's POINTS and FLOOR.
#
# v0.3 (haro/spike/v03/GRAMMAR.md): a UNION seat takes a value of one of
# several shapes and is checked as the alternative the shape names; a
# declaration's MESSAGES speak for its reference seats; a condition reads
# through a reference, quantifies, and tests the closed relations; and the
# order of the court is: shapes, the WORLD, the local types, the
# CONSTRAINTs, then the references.
#
# v0.17 (haro/spike/v17/GRAMMAR.md): UNDERSTAND -- a language that declares how a human language reaches its
# closed questions gets `tokens`, `understand`, `ask`, `vocabulary` and `examples`, and the rules of its
# sentences (n_lib.ring, loaded only by a court forged from such a language): `check <file> surfaces` asks each
# surface's own court to judge its queries too.
#
# v0.14 (haro/spike/v14/GRAMMAR.md): a court that collects -- `diagnose` goes on
# past a refusal to the next element of every pass and answers every finding,
# in the order of the file; `check` still stops at the first, to the byte.
#
# v0.13 (haro/spike/v13/GRAMMAR.md): NARRATE -- `narrate <file>` answers the
# sentence back in the language's own voice (narrate_lib.ring, loaded only where
# a NARRATE is declared): a projection of the sentence on stdout, never stored,
# never read back.
#
# v0.12 (haro/spike/v12/GRAMMAR.md): FORMS -- `family <file>` generates every
# declared family from its base and the forms it offers; `spellings <file>
# <names>` judges a list of names against the FORMS and the families
# (forms_lib.ring, loaded only where a FORMS is declared).
#
# v0.11 (haro/spike/v11/GRAMMAR.md): the Diagnostic Contract -- `diagnose
# <file> [world]` answers the court's verdict as C2 v1.2.0's one object of
# six-field envelopes; a typed refusal carries the declaration's CODE / CODES
# and CITES (CtFailC), a parse-level one is PARSE with no cites.
#
# v0.10 (haro/spike/v10/GRAMMAR.md): the WORLD as versioned data -- a SYMBOL
# seat resolves against a C1 world.json handed to `check <file> [world]`
# (UNRESOLVED in the symbol's words; NO_WORLD a warning without one), and
# `world <file>` emits the sentence's own C1 rows.
#
# v0.9 (haro/spike/v09/GRAMMAR.md): the RUN -- the A letter -- and the `run`
# verb: `run <file> <algorithm> <record json>` walks an algorithm's step tree
# on a record and answers its result (run_lib.ring, loaded by the generated
# court when its language declares a RUN); a step tree with a cycle is
# refused at check.
#
# v0.8 (haro/spike/v08/GRAMMAR.md): a refusal by NAME for a known trespasser;
# pair lists keyed by a MENU (a sequence) or a DECLARATION (resolved) with
# reference values; a UNION of declarations resolved by name; the references
# pass judges every reference, scalar, listed, keyed or valued.
#
# v0.7 (haro/spike/v07/GRAMMAR.md): the ASK -- the Q letter -- and the `ask`
# verb: `ask <file> "<question>" <rows json>` answers a question of the
# declared world on the records handed in (ask_lib.ring, loaded by the
# generated court when its language declares an ASK).
#
# v0.6 (haro/spike/v06/GRAMMAR.md): a list of a FORM that is a name and a
# scalar is written as name: value pairs; a seat typed by an EXPRESSION holds
# an expression text the court parses with the expression's own menus
# (expr_lib.ring); and the sentence court RUNS what the declaration says a
# record does -- `eval <file> <decl> <seat> <json>` evaluates one expression
# seat on a record, `walk <file> <name> <json>` walks the record through the
# steps the WALK of that kind names, in ORDER, under its GUARDS, computing
# its COMPUTE seats by their FORMULAs, stopping at the first guard that fails.
#
# Functions only. Globals ($cCourtLang, $cCourtExt, $aCourtKinds,
# $aCourtForms, $aCourtRefusals, $aCourtMenus, $aCourtRanges,
# $aCourtFormats, $aCourtUnions, $aCourtConstraints, $aCourtWorld,
# $aCourtPoints, $aCourtFloors, $aCourtToks, $nCourtPos, and cond_lib's)
# are born in the generated court, at its top level, for both runtimes' sake.

load "cond_lib.ring"
# expr_lib.ring is loaded by the GENERATED court, and only when its language
# declares an EXPRESSION (forge.ring): a court carries what its language says,
# and the machine court's edit-to-verdict stays under its 100 ms target

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

# v0.11: a refusal that enforces a provision of the declaration -- the pinned
# instrument -- carries its code and its cites out through two globals the
# `diagnose` verb reads; a parse-level refusal leaves them at PARSE and [],
# which C2 2.5 calls honest. A code of PARSE never cites.
func CtFailC(nLine, cCode, aCites, cMsg)
	CtSetCode(cCode, aCites)
	CtFail(nLine, cMsg)

# v0.14: a collecting court. In collect mode a refusal that a pass meets at one
# of its raising sites is NOTED and the pass goes on to its next element; out
# of collect mode it is raised again, same string, same globals, so `check` is
# unchanged to the byte. A declaration whose clause has the wrong SHAPE is
# broken: the passes that read its values say nothing more about it.
func CtNote(cErr)
	if not $bCourtCollect raise(cErr) ok
	$aCourtFound + [$cCourtCode, $aCourtCites, CtLineOf(cErr), CtStripPrefix(cErr)]
	CtSetCode("PARSE", [])

func CtIsBroken(nDecl)
	for i = 1 to len($aCourtBroken)
		if $aCourtBroken[i] = nDecl return 1 ok
	next
	return 0

# the findings in the order of the file, ties in the order they were met
func CtSortFound(aF)
	aOut = []
	for i = 1 to len(aF)
		nAt = len(aOut) + 1
		for j = len(aOut) to 1 step -1
			if aOut[j][3] > aF[i][3]
				nAt = j
			else
				exit
			ok
		next
		insert(aOut, nAt - 1, aF[i])
	next
	return aOut

func CtSetCode(cCode, aCites)
	if cCode = "" cCode = "PARSE" ok
	$cCourtCode = cCode
	if cCode = "PARSE"
		$aCourtCites = []
	else
		$aCourtCites = aCites
	ok

# a declaration kind's CODES entry for a seat, or ""
func CtCodeFor(aKind, cSeat)
	if len(aKind) < 6 return "" ok
	for i = 1 to len(aKind[6])
		if aKind[6][i][1] = cSeat return aKind[6][i][2] ok
	next
	return ""

# the code and cites of a refusal that a declaration element owns: the
# element's CODE when it has one (cited as rule:<CODE>), else a default code
# cited as rule:<element name>
func CtElementCode(cOwn, cDefault, cName)
	if cOwn != "" return [cOwn, ["rule:" + cOwn]] ok
	return [cDefault, ["rule:" + cName]]

# a REFUSAL category's code, codes per NAMED word and cites
func CtRefusalRow(cCategory)
	for i = 1 to len($aCourtRefusals)
		if $aCourtRefusals[i][1] = cCategory return $aCourtRefusals[i] ok
	next
	return NULL

func CtRefusalCode(cCategory, cWord, cDefault)
	aR = CtRefusalRow(cCategory)
	if isNull(aR) return [cDefault, []] ok
	cCode = ""
	if cWord != "" and len(aR) >= 5
		for i = 1 to len(aR[5])
			if aR[5][i][1] = cWord cCode = aR[5][i][2] ok
		next
	ok
	if cCode = "" and len(aR) >= 4 cCode = aR[4] ok
	if cCode = "" cCode = cDefault ok
	aCites = []
	if len(aR) >= 6 aCites = aR[6] ok
	return [cCode, aCites]

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
# v0.8: a refusal's NAMED word -- its own message, or ""
func CtRefusalNamed(cCategory, cWord)
	for i = 1 to len($aCourtRefusals)
		if $aCourtRefusals[i][1] = cCategory and len($aCourtRefusals[i]) >= 3
			aN = $aCourtRefusals[i][3]
			for j = 1 to len(aN)
				if aN[j][1] = cWord return aN[j][2] ok
			next
		ok
	next
	return ""

func CtRefusalMessage(cCategory)
	for i = 1 to len($aCourtRefusals)
		if $aCourtRefusals[i][1] = cCategory return $aCourtRefusals[i][2] ok
	next
	return ""

# ---- v0.4: one court, several languages ------------------------------------------
# The generated court carries $aCourtLangs, one record per language -- its own
# first, then every language a SENTENCE names, recursively: [name, ext, kinds,
# forms, refusals, menus, ranges, formats, unions, constraints, world, points,
# floors, views, sentences]. CtUseLanguage loads one record into the tables
# the court reads; a SENTENCE seat is judged by switching to its language and
# back, the judged declarations kept in $aCourtSentences for the conditions
# that read through them.

func CtDirOf(cPath)
	n = 0
	for i = 1 to len(cPath)
		if cPath[i] = "/" or cPath[i] = char(92) n = i ok
	next
	if n = 0 return "" ok
	return left(cPath, n - 1)

func CtReplace(cS, cOld, cNew)
	cOut = ""
	i = 1
	n = len(cS)
	m = len(cOld)
	while i <= n
		if i + m - 1 <= n and substr(cS, i, m) = cOld
			cOut += cNew
			i += m
		else
			cOut += cS[i]
			i++
		ok
	end
	return cOut

func CtLangEntry(cName)
	for i = 1 to len($aCourtLangs)
		if $aCourtLangs[i][1] = cName return $aCourtLangs[i] ok
	next
	return NULL

func CtUseLanguage(cName)
	aE = CtLangEntry(cName)
	if isNull(aE) raise("the court carries no language called '" + cName + "'") ok
	$cCourtLang = aE[1]
	$cCourtExt = aE[2]
	$aCourtKinds = aE[3]
	$aCourtForms = aE[4]
	$aCourtRefusals = aE[5]
	$aCourtMenus = aE[6]
	$aCourtRanges = aE[7]
	$aCourtFormats = aE[8]
	$aCourtUnions = aE[9]
	$aCourtConstraints = aE[10]
	$aCourtWorld = aE[11]
	$aCourtPoints = aE[12]
	$aCourtFloors = aE[13]
	$aCourtViews = aE[14]
	$aCourtSentenceKinds = aE[15]
	# v0.6: the EXPRESSIONs [name, ops, opds, aggs, vars, contexts, absent,
	# division, equality] and the WALKs [name, of, steps, through, order,
	# guards, compute, formula, fail]
	$aCourtExprs = []
	$aCourtWalks = []
	if len(aE) >= 17
		$aCourtExprs = aE[16]
		$aCourtWalks = aE[17]
	ok
	# v0.7: the ASK [name, from kinds, where, clauses], or NULL
	$aCourtAsk = NULL
	if len(aE) >= 18 $aCourtAsk = aE[18] ok
	# v0.9: the RUN [[role, [kind, seat, ...]], ...], or NULL
	$aCourtRun = NULL
	if len(aE) >= 19 $aCourtRun = aE[19] ok
	# v0.10: the SYMBOLs [name, kind, ref, message]
	$aCourtSymbols = []
	if len(aE) >= 20 $aCourtSymbols = aE[20] ok
	# v0.12: the FORMS [name, fluent, passive, statement, params, family], or NULL
	$aCourtFormset = NULL
	if len(aE) >= 21 $aCourtFormset = aE[21] ok
	# v0.13: the NARRATE [name, opens, ends, refuses, says], or NULL
	$aCourtNarrate = NULL
	if len(aE) >= 22 $aCourtNarrate = aE[22] ok
	# v0.17: the UNDERSTAND [name, [[role, kind], ...]], or NULL -- a human language reaches closed questions (n_lib.ring)
	$aCourtUnderstand = NULL
	if len(aE) >= 23 $aCourtUnderstand = aE[23] ok

# the condition tables of every language the court carries, built once
func CtBuildCondLangs()
	$aCondLangs = []
	for i = 1 to len($aCourtLangs)
		aE = $aCourtLangs[i]
		aKinds = aE[3]
		aSents = aE[15]
		aDeclSeats = []
		aVerbOf = []
		for j = 1 to len(aKinds)
			aS = aKinds[j][3]
			aInfo = []
			for k = 1 to len(aS)
				cTK = "prim"
				if len(aS[k]) >= 5 cTK = aS[k][5] ok
				cTarget = ""
				if cTK = "decl" cTarget = aE[1] ok
				if cTK = "sentence"
					for m = 1 to len(aSents)
						if aSents[m][1] = aS[k][2] cTarget = aSents[m][2] ok
					next
				ok
				aInfo + [aS[k][1], aS[k][2], aS[k][3], cTK, cTarget]
			next
			aDeclSeats + [aKinds[j][2], aInfo]
			aVerbOf + [aKinds[j][2], aKinds[j][1]]
		next
		aViews = []
		for j = 1 to len(aE[14])
			aV = aE[14][j]
			aViews + [aV[1], aV[2], NULL, aV[3], aV[4], aV[5]]
		next
		# v0.8: the WORLD's ENTRY kinds and the forms' seat kinds
		aEntry = []
		if len(aE[11]) >= 3 aEntry = aE[11][3] ok
		aFormTable = []
		for j = 1 to len(aE[4])
			aFS = aE[4][j][2]
			aInfo = []
			for k = 1 to len(aFS)
				aInfo + [aFS[k][1], aFS[k][2], CtTypeKind(aFS[k])]
			next
			aFormTable + [aE[4][j][1], aInfo]
		next
		$aCondLangs + [aE[1], aDeclSeats, aE[11][1], aViews, aVerbOf, aEntry, aFormTable]
	next

# the court's state, so a SENTENCE can be judged in its own language and the
# judge returned to its own; $aCourtSentences and $aCondLangs are shared
func CtSnapshot()
	return [$cCourtLang, $cCourtExt, $cCourtDir, $aCourtKinds, $aCourtForms, $aCourtRefusals,
	        $aCourtMenus, $aCourtRanges, $aCourtFormats, $aCourtUnions, $aCourtConstraints,
	        $aCourtWorld, $aCourtPoints, $aCourtFloors, $aCourtViews, $aCourtSentenceKinds,
	        $aCourtToks, $nCourtPos, $aCondDecls, $cCondLang, $cCondOther, $bCondUnread,
	        $aCondFormats, $aCondToks, $nCondPos, $aCourtExprs, $aCourtWalks, $aCourtAsk, $aCourtRun,
	        $aCourtSymbols, $aCourtWorldFile, $aCourtFormset, $aCourtNarrate, $aCourtUnderstand]

func CtRestore(aS)
	$cCourtLang = aS[1]
	$cCourtExt = aS[2]
	$cCourtDir = aS[3]
	$aCourtKinds = aS[4]
	$aCourtForms = aS[5]
	$aCourtRefusals = aS[6]
	$aCourtMenus = aS[7]
	$aCourtRanges = aS[8]
	$aCourtFormats = aS[9]
	$aCourtUnions = aS[10]
	$aCourtConstraints = aS[11]
	$aCourtWorld = aS[12]
	$aCourtPoints = aS[13]
	$aCourtFloors = aS[14]
	$aCourtViews = aS[15]
	$aCourtSentenceKinds = aS[16]
	$aCourtToks = aS[17]
	$nCourtPos = aS[18]
	$aCondDecls = aS[19]
	$cCondLang = aS[20]
	$cCondOther = aS[21]
	$bCondUnread = aS[22]
	$aCondFormats = aS[23]
	$aCondToks = aS[24]
	$nCondPos = aS[25]
	$aCourtExprs = aS[26]
	$aCourtWalks = aS[27]
	$aCourtAsk = aS[28]
	$aCourtRun = aS[29]
	$aCourtSymbols = aS[30]
	$aCourtWorldFile = aS[31]
	$aCourtFormset = aS[32]
	$aCourtNarrate = aS[33]
	$aCourtUnderstand = aS[34]

# ---- v0.11: the Diagnostic Contract (C2 v1.2.0) -------------------------------------
# `diagnose <file> [world]` runs the same court and answers in the family's
# machine form: one object carrying `diagnostics`, each a six-field envelope --
# code, severity, message, span {file, line}, cites, language. A refusal is one
# error (the court stops at the first); a sentence with SYMBOL seats and no
# world adds one NO_WORLD warning at line 0; a clean run is `"diagnostics": []`.
# No value is ever a bare true, false or null (C2 2.8).

func CtStripPrefix(cMsg)
	n = substr(cMsg, "): ")
	if n > 0 return substr(cMsg, n + 3) ok
	return cMsg

func CtLineOf(cMsg)
	nAt = substr(cMsg, "(line ")
	if nAt = 0 return 0 ok
	nEnd = substr(cMsg, "): ")
	if nEnd <= nAt return 0 ok
	return 0 + substr(cMsg, nAt + 6, nEnd - nAt - 6)

func CtDiagnosticJson(aD)
	c = '{"code": ' + CtJson(aD[1]) + ', "severity": ' + CtJson(aD[2]) + ', "message": ' + CtJson(aD[3])
	c += ', "span": {"file": ' + CtJson(aD[4]) + ', "line": ' + aD[5] + '}, "cites": ['
	for i = 1 to len(aD[6])
		if i > 1 c += ", " ok
		c += CtJson(aD[6][i])
	next
	c += '], "language": ' + CtJson($cCourtLang) + '}'
	return c

func CtDiagnosticsJson(aDiags)
	c = '{"diagnostics": ['
	for i = 1 to len(aDiags)
		if i > 1 c += ", " ok
		c += CtDiagnosticJson(aDiags[i])
	next
	return c + ']}'

func CtDiagnose(cFile, cWorldPath)
	aDiags = []
	cSrc = read(cFile)
	CtSetCode("PARSE", [])
	# v0.14: this verb collects -- every pass goes on past a refusal to its next element
	$bCourtCollect = 1
	$aCourtFound = []
	$aCourtBroken = []
	cErr = ""
	aDecls = NULL
	try
		if cWorldPath != "" $aCourtWorldFile = CtWorldLoad(cWorldPath) ok
		aDecls = CtDeclare(cSrc)
	catch
		cErr = cCatchError
	done
	$bCourtCollect = 0
	# a refusal nothing could resume from (the sentence did not parse, or a pass met
	# something it cannot judge past) ends the run and is the last finding
	if cErr != ""
		$aCourtFound + [$cCourtCode, $aCourtCites, CtLineOf(cErr), CtStripPrefix(cErr)]
	ok
	if len($aCourtFound) > 0
		aF = CtSortFound($aCourtFound)
		for i = 1 to len(aF)
			aDiags + [aF[i][1], "error", aF[i][4], cFile, aF[i][3], aF[i][2]]
		next
		return aDiags
	ok
	if isNull($aCourtWorldFile) and len($aCourtSymbols) > 0
		aSites = CtSymbolSites(aDecls)
		if len(aSites) > 0
			aSy = CtSymbolByName(aSites[1][2][2])
			aCites = []
			if not isNull(aSy) aCites = CtSymbolCode(aSy)[2] ok
			aDiags + ["NO_WORLD", "warning", "no world to resolve against; " + len(aSites) + " symbol reference(s) unresolved, which is what C3 section 3.2 asks a project to close", cFile, 0, aCites]
		ok
	ok
	return aDiags

# ---- v0.6: the EXPRESSION tables, handed to expr_lib.ring ----------------------

func CtExprByName(cName)
	for i = 1 to len($aCourtExprs)
		if $aCourtExprs[i][1] = cName return $aCourtExprs[i] ok
	next
	return NULL

func CtExprUse(aE)
	$cExprLang = aE[1]
	$aExprOperators = aE[2]
	$aExprOperands = aE[3]
	$aExprAggregates = aE[4]
	$aExprVariables = aE[5]
	$aExprContexts = aE[6]
	$cExprAbsent = aE[7]
	$cExprDivision = aE[8]
	$cExprEquality = aE[9]

# a SENTENCE seat type's record: [name, lang, message, refused]
func CtSentenceKind(cName)
	for i = 1 to len($aCourtSentenceKinds)
		if $aCourtSentenceKinds[i][1] = cName return $aCourtSentenceKinds[i] ok
	next
	return NULL

# a kind's MESSAGES entry for a seat, or ""
func CtMessageFor(aKind, cSeat)
	if len(aKind) < 5 return "" ok
	for i = 1 to len(aKind[5])
		if aKind[5][i][1] = cSeat return aKind[5][i][2] ok
	next
	return ""

# judge the file a SENTENCE seat names, beside the file being judged, with
# the language's own tables; keep its declarations, or refuse in the
# sentence's own words
func CtJudgeSentence(aDecl, aSeat, aClause)
	cRel = aClause[3][2]
	aSK = CtSentenceKind(aSeat[2])
	if isNull(aSK) CtFail(aClause[2], "Clause " + aClause[1] + " names a SENTENCE the court does not carry") ok
	cPath = cRel
	if $cCourtDir != "" cPath = $cCourtDir + "/" + cRel ok
	if cRel = "" or not fexists(cPath)
		cMsg = aSK[3]
		if cMsg = "" cMsg = "{VERB} {name} names {value}, which cannot be read from beside this file" ok
		CtFail(aClause[2], CtFill(cMsg, aDecl, cRel))
	ok
	cText = read(cPath)
	aSnap = CtSnapshot()
	CtUseLanguage(aSK[2])
	$cCourtDir = CtDirOf(cPath)
	cErr = ""
	aInner = NULL
	bWas = $bCourtCollect
	$bCourtCollect = 0
	try
		aInner = CtDeclare(cText)
	catch
		cErr = cCatchError
	done
	$bCourtCollect = bWas
	CtRestore(aSnap)
	if cErr != ""
		# "<lang> (line N): why" -> why and N
		cWhy = cErr
		cLine = "?"
		nAt = substr(cErr, "(line ")
		if nAt > 0
			nEnd = substr(cErr, "): ")
			if nEnd > nAt
				cLine = substr(cErr, nAt + 6, nEnd - nAt - 6)
				cWhy = substr(cErr, nEnd + 3)
			ok
		ok
		cMsg = aSK[4]
		if cMsg = "" cMsg = "{VERB} {name} is refused: {why} (line {line} of {value})" ok
		cMsg = CtReplace(CtReplace(cMsg, "{why}", cWhy), "{line}", cLine)
		CtFailC(aDecl[3], "SENTENCE", [], CtFill(cMsg, aDecl, cRel))
	ok
	$aCourtSentences + [$cCourtLang, aDecl[1], aDecl[2], aSeat[1], cRel, aInner, aSK[2]]

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
			but c = ":" cT = "colon"
			ok
			if cT = ""
				cMsgC = CtRefusalMessage("unexpected_character")
				if cMsgC != "" cMsgC = " -- " + cMsgC ok
				CtFail(nLine, "The character '" + c + "' is not part of the " + $cCourtLang + " grammar" + cMsgC)
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

# a seat is [name, of, isList, optional, typeKind]; its clause name is the
# seat's name in UPPER_SNAKE, and its value shape follows its type:
#   text / a FORMAT -> string, name/flag/ref / a MENU / a DECLARATION -> word,
#   number / a RANGE -> number, [form] -> a list whose items follow the form's
#   first seat (text or a FORMAT -> stringlist, else namelist), [decl] and
#   [menu] -> namelist
func CtTypeKind(aSeat)
	if len(aSeat) >= 5 return aSeat[5] ok
	return "prim"

func CtIsPairForm(aFS)
	if len(aFS) != 2 return 0 ok
	if aFS[1][3] or aFS[2][3] return 0 ok
	cK1 = CtTypeKind(aFS[1])
	if aFS[1][2] != "name" and cK1 != "menu" and cK1 != "decl" return 0 ok
	return 1

# v0.8: does a seat take part in the references pass -- a reference, a UNION
# of declarations, or a pair list whose keys or values are references -- and
# in the local pass -- everything else, and a pair list's menu keys and
# scalar values
func CtUnionHasDecls(cName)
	aU = CtUnionByName(cName)
	if isNull(aU) return 0 ok
	for i = 1 to len(aU[2])
		if aU[2][i][3] = "decl" return 1 ok
	next
	return 0

func CtSeatPasses(aSeat)
	cK = CtTypeKind(aSeat)
	if cK = "decl" return [0, 1] ok
	if aSeat[3] and cK = "union" return [0, 1] ok
	if cK = "union"
		if CtUnionHasDecls(aSeat[2]) return [1, 1] ok
		return [1, 0]
	ok
	if aSeat[3] and cK = "form"
		aF = CtFormByName(aSeat[2])
		if not isNull(aF) and CtIsPairForm(aF[2])
			bRef = 0
			if CtTypeKind(aF[2][1]) = "decl" bRef = 1 ok
			if CtTypeKind(aF[2][2]) = "decl" bRef = 1 ok
			if CtTypeKind(aF[2][2]) = "union" and CtUnionHasDecls(aF[2][2][2]) bRef = 1 ok
			return [1, bRef]
		ok
	ok
	return [1, 0]

func CtClauseShape(aSeat)
	cOf = aSeat[2]
	cK = CtTypeKind(aSeat)
	if aSeat[3]
		if cK = "union" return "namelist" ok
		if cK = "form"
			aF = CtFormByName(cOf)
			if isNull(aF) return "namelist" ok
			aFS = aF[2]
			# v0.6: a FORM that is a name and a scalar is written as pairs
			if CtIsPairForm(aFS) return "pairlist" ok
			if len(aFS) > 0 and (aFS[1][2] = "text" or CtTypeKind(aFS[1]) = "format") return "stringlist" ok
		ok
		return "namelist"
	ok
	if cK = "union" return "union" ok
	if cK = "sentence" return "string" ok
	if cK = "expr" return "string" ok
	if cK = "symbol" return "word" ok
	if cOf = "text" or cK = "format" return "string" ok
	if cOf = "number" or cK = "range" return "number" ok
	return "word"

func CtMenuByName(cName)
	for i = 1 to len($aCourtMenus)
		if $aCourtMenus[i][1] = cName return $aCourtMenus[i] ok
	next
	return NULL

func CtRangeByName(cName)
	for i = 1 to len($aCourtRanges)
		if $aCourtRanges[i][1] = cName return $aCourtRanges[i] ok
	next
	return NULL

func CtFormatByName(cName)
	for i = 1 to len($aCourtFormats)
		if $aCourtFormats[i][1] = cName return $aCourtFormats[i] ok
	next
	return NULL

func CtKindByDeclName(cName)
	for i = 1 to len($aCourtKinds)
		if $aCourtKinds[i][2] = cName return $aCourtKinds[i] ok
	next
	return NULL

# ---- v0.3: a UNION seat takes a value of one of several shapes -------------------
# a union is [name, [[of, isList, typeKind], ...], message]

func CtUnionByName(cName)
	for i = 1 to len($aCourtUnions)
		if $aCourtUnions[i][1] = cName return $aCourtUnions[i] ok
	next
	return NULL

# an alternative's value shape, as CtClauseShape gives a seat's
func CtAltShape(aAlt)
	return CtClauseShape([aAlt[1], aAlt[1], aAlt[2], 0, aAlt[3]])

# the alternative whose shape the written value has, or NULL; an empty list
# fits either list shape
func CtUnionAlt(aSeat, aClause)
	aU = CtUnionByName(aSeat[2])
	if isNull(aU) return NULL ok
	cGot = aClause[3][1]
	bEmpty = 0
	if cGot = "namelist" or cGot = "stringlist"
		if len(aClause[3][2]) = 0 bEmpty = 1 ok
	ok
	aAlts = aU[2]
	for i = 1 to len(aAlts)
		cShape = CtAltShape(aAlts[i])
		if cShape = cGot return aAlts[i] ok
		if bEmpty and (cShape = "namelist" or cShape = "stringlist") return aAlts[i] ok
	next
	return NULL

# the union's own MESSAGE speaks when the value fits no alternative
func CtWantUnion(aDecl, aClause, aSeat)
	if not isNull(CtUnionAlt(aSeat, aClause)) return ok
	aU = CtUnionByName(aSeat[2])
	if isNull(aU) CtFail(aClause[2], "Clause " + aClause[1] + " names a UNION the court does not carry") ok
	cMsg = aU[3]
	if cMsg = ""
		aNames = []
		for i = 1 to len(aU[2])
			aNames + aU[2][i][1]
		next
		cMsg = "Clause " + aClause[1] + " takes one of " + CtJoin(aNames, ", ")
	ok
	cV = ""
	if aClause[3][1] = "word" or aClause[3][1] = "string" or aClause[3][1] = "number" cV = aClause[3][2] ok
	cOwn = ""
	if len(aU) >= 4 cOwn = aU[4] ok
	aCC = CtElementCode(cOwn, "UNION", aU[1])
	CtFailC(aClause[2], aCC[1], aCC[2], CtFill(cMsg, aDecl, cV))

# {name}, {VERB}, {value}, {other}, {seat} and {decl.seat} in a declared message
func CtFill(cMsg, aDecl, cValue)
	cOut = ""
	n = len(cMsg)
	i = 1
	while i <= n
		c = cMsg[i]
		if c = "{"
			j = i + 1
			while j <= n and cMsg[j] != "}"
				j++
			end
			if j > n
				cOut += c
				i++
				loop
			ok
			cKey = substr(cMsg, i + 1, j - i - 1)
			cRep = ""
			if cKey = "name"
				if not isNull(aDecl) cRep = aDecl[2] ok
			but cKey = "VERB"
				if not isNull(aDecl) cRep = aDecl[1] ok
			but cKey = "value"
				cRep = cValue
			but cKey = "other"
				cRep = $cCondOther
			else
				if not isNull(aDecl)
					v = CondScalar(aDecl, cKey)
					if not isNull(v)
						cRep = v
					else
						aL = CondListOf(aDecl, cKey)
						if not isNull(aL)
							cRep = CtJoin(aL, ", ")
						else
							# a path: {x.seat} through a reference seat, a ONE kind or a
							# VIEW, {view} a VIEW's declaration (v0.3, v0.4)
							bSave = $bCondUnread
							v = CondPathScalar(["path", CondSplit(cKey, ".")], ["decl", $cCondLang, aDecl, $aCondDecls], NULL)
							$bCondUnread = bSave
							if not isNull(v) cRep = v ok
						ok
					ok
				ok
			ok
			cOut += cRep
			i = j + 1
		else
			cOut += c
			i++
		ok
	end
	return cOut

# ---- the shapes of a FORMAT -----------------------------------------------------

func CtIsHexChar(c)
	n = ascii(c)
	return (n >= 48 and n <= 57) or (n >= 97 and n <= 102) or (n >= 65 and n <= 70)

func CtIsLabelChar(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or (n >= 48 and n <= 57) or n = 45

func CtIsIpv4(cS)
	aParts = CtSplit(cS, ".")
	if len(aParts) != 4 return 0 ok
	for i = 1 to 4
		p = aParts[i]
		if len(p) = 0 or len(p) > 3 return 0 ok
		for j = 1 to len(p)
			if not CtIsDigit(p[j]) return 0 ok
		next
		if 0 + p > 255 return 0 ok
	next
	return 1

func CtSplit(cS, cSep)
	aOut = []
	cCur = ""
	for i = 1 to len(cS)
		if cS[i] = cSep
			aOut + cCur
			cCur = ""
		else
			cCur += cS[i]
		ok
	next
	aOut + cCur
	return aOut

func CtIsLabel(cS)
	if len(cS) = 0 return 0 ok
	for i = 1 to len(cS)
		if not CtIsLabelChar(cS[i]) return 0 ok
	next
	if cS[1] = "-" or cS[len(cS)] = "-" return 0 ok
	return 1

# one definition of the shapes, in cond_lib.ring, since v0.3's `matches`
# tests them inside a condition too
func CtHasShape(cS, cShape)
	return CondHasShape(cS, cShape)

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
		aPairs = []
		while 1
			e = CtPeek()
			if e[1] = "rbracket"
				CtNext()
				exit
			ok
			item = CtNext()
			if item[1] = "ident" and CtPeek()[1] = "colon"
				# v0.6: a name: value pair; the value a word, a string or a number
				CtNext()
				tv = CtNext()
				if tv[1] != "ident" and tv[1] != "string" and tv[1] != "number"
					CtFail(tv[3], "A pair's value is a word, a string or a number, found '" + CtShown(tv) + "'")
				ok
				aPair = [item[2], tv[2], tv[1]]
				aPairs + aPair
			but item[1] = "ident"
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
		if len(aPairs) > 0 and (len(aNames) > 0 or len(aStrings) > 0)
			CtFail(t[3], "A list is all name: value pairs or none")
		ok
		nListEnd = $aCourtToks[$nCourtPos - 1][5]
		if len(aPairs) > 0 return ["pairlist", aPairs, t[4], nListEnd] ok
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
		aCC = CtRefusalCode("unknown_verb", "", "UNKNOWN_VERB")
		CtFailC(tV[3], aCC[1], aCC[2], "Unknown verb '" + CtShown(tV) + "': " + cMsg)
	ok
	tK = CtNext()
	aKind = NULL
	if tK[1] = "keyword" aKind = CtKindByVerb(tK[2]) ok
	if isNull(aKind)
		cNamed = CtRefusalNamed("unknown_declaration", lower(CtShown(tK)))
		if cNamed != ""
			aCC = CtRefusalCode("unknown_declaration", lower(CtShown(tK)), "UNKNOWN_KIND")
			CtFailC(tK[3], aCC[1], aCC[2], cNamed)
		ok
		cMsg = CtRefusalMessage("unknown_declaration")
		if cMsg = "" cMsg = "the kinds are closed (" + CtJoin(CtVerbs(), ", ") + ")" ok
		aCC = CtRefusalCode("unknown_declaration", "", "UNKNOWN_KIND")
		CtFailC(tK[3], aCC[1], [], "Unknown kind '" + CtShown(tK) + "': " + cMsg)
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
			cNamed = CtRefusalNamed("unknown_seat", lower(tC[2]))
			if cNamed != ""
				aCC = CtRefusalCode("unknown_seat", lower(tC[2]), "UNKNOWN_CLAUSE")
				CtFailC(tC[3], aCC[1], aCC[2], cNamed)
			ok
			cMsg = CtRefusalMessage("unknown_seat")
			if cMsg = "" cMsg = "allowed are " + CtJoin(aAllowed, ", ") ok
			aCC = CtRefusalCode("unknown_seat", "", "UNKNOWN_CLAUSE")
			CtFailC(tC[3], aCC[1], [], "Unknown clause '" + tC[2] + "' for " + aKind[1] + ": " + cMsg)
		ok
		for i = 1 to len(aClauses)
			if aClauses[i][1] = tC[2]
				CtFail(tC[3], "Clause " + tC[2] + " given twice")
			ok
		next
		aVal = CtParseValue()
		# a FORMAT that FOLDs case reads its value folded (v0.4): hex is case-blind
		aSeatF = CtSeatByClause(aKind, tC[2])
		if not isNull(aSeatF)
			if CtTypeKind(aSeatF) = "format" and aVal[1] = "string"
				aF = CtFormatByName(aSeatF[2])
				if not isNull(aF)
					if len(aF) >= 4
						if aF[4] = "case" aVal[2] = lower(aVal[2]) ok
					ok
				ok
			ok
		ok
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
	but cShape = "pairlist"
		if cGot = "namelist" and len(aClause[3][2]) = 0 return ok
		if cGot != "pairlist" CtFail(aClause[2], "Clause " + cName + " takes name: value pairs") ok
	ok

# parse a whole source and judge what the declaration can judge; returns the
# list of declarations
func CtDeclare(cSrc)
	CtSetCode("PARSE", [])
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
				aCC = CtRefusalCode("duplicate_name", "", "DUPLICATE_NAME")
				try
					CtFailC(aDecls[i][3], aCC[1], aCC[2], "'" + aDecls[i][2] + "' is already declared (line " + aDecls[j][3] + "); " + cMsg)
				catch
					CtNote(cCatchError)
				done
				exit
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
			try
				if CtTypeKind(aSeat) = "union" and not aSeat[3]
					CtWantUnion(aD, aC[j], aSeat)
				else
					# a LIST of a union of declarations is a name list (v0.9)
					CtWantShape(aD, aC[j], CtClauseShape(aSeat))
				ok
			catch
				CtNote(cCatchError)
				$aCourtBroken + i
			done
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
				# the declaration's own MESSAGES for a required seat speaks first (v0.4);
				# its CODES give the envelope's code (v0.11)
				cMsgR = CtMessageFor(aKind, aSeat[1])
				cCodeR = CtCodeFor(aKind, aSeat[1])
				aCC = CtElementCode(cCodeR, "REQUIRED", aKind[2] + "." + aSeat[1])
				try
					if cMsgR != "" CtFailC(aD[3], aCC[1], aCC[2], CtFill(cMsgR, aD, "")) ok
					CtFailC(aD[3], aCC[1], aCC[2], upper(aSeat[1]) + " is required on " + aD[1] + " " + aD[2])
				catch
					CtNote(cCatchError)
				done
			ok
		next
	next

	# ---- v0.2: what the WORLD, the types, the names and the constraints say ----
	$aCondDecls = aDecls
	$cCondLang = $cCourtLang
	$aCondFormats = []
	for i = 1 to len($aCourtFormats)
		$aCondFormats + [$aCourtFormats[i][1], $aCourtFormats[i][2]]
	next

	# the WORLD: exactly one of each ONE kind, and the FIRST kind first
	aOne = $aCourtWorld[1]
	for i = 1 to len(aOne)
		aK = CtKindByDeclName(aOne[i])
		if isNull(aK) loop ok
		n = 0
		for j = 1 to len(aDecls)
			if aDecls[j][1] = aK[1] n++ ok
		next
		if n != 1
			try
				CtFailC(aDecls[1][3], "WORLD_ONE", ["rule:world"], "A " + $cCourtLang + " file declares exactly one " + aK[1] + " (found " + n + ")")
			catch
				CtNote(cCatchError)
			done
		ok
	next
	if $aCourtWorld[2] != ""
		aK = CtKindByDeclName($aCourtWorld[2])
		if not isNull(aK) and aDecls[1][1] != aK[1]
			try
				CtFailC(aDecls[1][3], "WORLD_FIRST", ["rule:world"], "The " + aK[1] + " declaration comes first")
			catch
				CtNote(cCatchError)
			done
		ok
	ok

	# the NAMES of a declaration kind, and every seat's typed value -- the
	# local facts first (a menu, a range, a format, a union); a reference is a
	# fact about the whole sentence and is checked after the constraints, which
	# are the maker's own words about the whole sentence (v0.3)
	CtCheckValues(aDecls, 0)

	# the CONSTRAINTs, each on every declaration of its ON kind; a condition
	# that reads through a reference that resolves to nothing says nothing,
	# and the reference's own refusal speaks below
	for i = 1 to len($aCourtConstraints)
		aCn = $aCourtConstraints[i]
		aK = CtKindByDeclName(aCn[2])
		if isNull(aK) loop ok
		aWhen = CondParse(aCn[3])
		aThen = NULL
		if aCn[4] != "" aThen = CondParse(aCn[4]) ok
		for j = 1 to len(aDecls)
			aD = aDecls[j]
			if aD[1] != aK[1] loop ok
			if CtIsBroken(j) loop ok
			$cCondOther = ""
			$bCondUnread = 0
			bWhen = CondEval(aWhen, aD)
			if $bCondUnread loop ok
			if bWhen
				# WHEN alone names a forbidden state; with THEN, the consequence must hold
				bFail = 1
				if not isNull(aThen)
					bFail = not CondEval(aThen, aD)
					if $bCondUnread loop ok
				ok
				if bFail
					cCnC = ""
					if len(aCn) >= 6 cCnC = aCn[6] ok
					aCC = CtElementCode(cCnC, "CONSTRAINT", aCn[1])
					try
						CtFailC(aD[3], aCC[1], aCC[2], CtFill(aCn[5], aD, ""))
					catch
						CtNote(cCatchError)
					done
				ok
			ok
		next
	next

	# the references, last
	CtCheckValues(aDecls, 1)
	# v0.9: an algorithm's step tree is a tree
	if not isNull($aCourtRun)
		try
			RunCheckAcyclic(aDecls)
		catch
			CtNote(cCatchError)
		done
	ok
	# v0.12: a family offers only forms the FORMS declares
	if not isNull($aCourtFormset)
		try
			FormsCheck(aDecls)
		catch
			CtNote(cCatchError)
		done
	ok
	# v0.17: the rules of a language that is UNDERSTOOD (n_lib.ring). They read a sentence whose references
	# resolve, so a sentence that already has a finding is not read by them; `check` stops at the first
	if not isNull($aCourtUnderstand) and len($aCourtFound) = 0
		try
			NatCheckRules(aDecls)
		catch
			CtNote(cCatchError)
		done
	ok
	# v0.10: the symbols resolve against the world, when one is handed in
	if not isNull($aCourtWorldFile) CtResolveWorld(aDecls) ok
	return aDecls

# the NAMES and the typed seat values of every declaration: bRefs 0 checks
# the local types and skips the references, 1 the references alone
func CtCheckValues(aDecls, bRefs)
	for i = 1 to len(aDecls)
		if CtIsBroken(i) loop ok
		aD = aDecls[i]
		aKind = CtKindByVerb(aD[1])
		if not bRefs
			if len(aKind) >= 4 and aKind[4] != ""
				cWhy = CtCheckNamed(aKind[4], aD[2])
				if cWhy != ""
					try
						CtFail(aD[3], "'" + aD[2] + "' " + cWhy)
					catch
						CtNote(cCatchError)
					done
				ok
			ok
		ok
		aC = aD[4]
		for j = 1 to len(aC)
			aSeat = CtSeatByClause(aKind, aC[j][1])
			aP = CtSeatPasses(aSeat)
			if not aP[bRefs + 1] loop ok
			if CtTypeKind(aSeat) = "sentence"
				# v0.4: the file a SENTENCE seat names is judged in its own language
				try
					CtJudgeSentence(aD, aSeat, aC[j])
				catch
					CtNote(cCatchError)
				done
				loop
			ok
			cWhy = CtCheckSeatValue(aD, aSeat, aC[j], bRefs)
			if cWhy != ""
				try
					CtFail(aC[j][2], cWhy)
				catch
					CtNote(cCatchError)
				done
			ok
		next
	next

# a declaration's name against its kind's NAMES (a MENU or a FORMAT); "" or why
func CtCheckNamed(cNames, cName)
	aM = CtMenuByName(cNames)
	if not isNull(aM)
		if CtInList(cName, aM[2]) return "" ok
		cMsg = aM[3]
		if cMsg = "" cMsg = "is not a " + cNames + ": the menu is " + CtJoin(aM[2], ", ") ok
		cOwn = ""
		if len(aM) >= 4 cOwn = aM[4] ok
		aCC = CtElementCode(cOwn, "MENU", aM[1])
		CtSetCode(aCC[1], aCC[2])
		return CtFill(cMsg, NULL, cName)
	ok
	aF = CtFormatByName(cNames)
	if not isNull(aF)
		if CtHasShape(cName, aF[2]) return "" ok
		cMsg = aF[3]
		if cMsg = "" cMsg = "is not a " + aF[2] ok
		cOwn = ""
		if len(aF) >= 5 cOwn = aF[5] ok
		aCC = CtElementCode(cOwn, "FORMAT", aF[1])
		CtSetCode(aCC[1], aCC[2])
		return CtFill(cMsg, NULL, cName)
	ok
	return ""

# one scalar value against a seat's type (menu, range, format, reference); "" or why
func CtCheckScalar(aDecl, aSeat, cValue)
	cK = CtTypeKind(aSeat)
	cClause = upper(aSeat[1])
	if cK = "menu"
		aM = CtMenuByName(aSeat[2])
		if isNull(aM) or CtInList(cValue, aM[2]) return "" ok
		cMsg = aM[3]
		if cMsg = "" cMsg = cClause + " is " + CtJoin(aM[2], ", ") ok
		if substr(cMsg, "{value}") = 0 cMsg += ", not '{value}'" ok
		cOwn = ""
		if len(aM) >= 4 cOwn = aM[4] ok
		aCC = CtElementCode(cOwn, "MENU", aM[1])
		CtSetCode(aCC[1], aCC[2])
		return CtFill(cMsg, aDecl, cValue)
	but cK = "range"
		aR = CtRangeByName(aSeat[2])
		if isNull(aR) return "" ok
		n = 0 + cValue
		if n >= 0 + aR[2] and n <= 0 + aR[3] return "" ok
		cMsg = aR[4]
		if cMsg = "" cMsg = cClause + " {value} is out of range (" + aR[2] + ".." + aR[3] + ")" ok
		cOwn = ""
		if len(aR) >= 5 cOwn = aR[5] ok
		aCC = CtElementCode(cOwn, "RANGE", aR[1])
		CtSetCode(aCC[1], aCC[2])
		return CtFill(cMsg, aDecl, cValue)
	but cK = "format"
		aF = CtFormatByName(aSeat[2])
		if isNull(aF) or CtHasShape(cValue, aF[2]) return "" ok
		cMsg = aF[3]
		if cMsg = "" cMsg = cClause + " is not a " + aF[2] + ": '{value}'" ok
		cOwn = ""
		if len(aF) >= 5 cOwn = aF[5] ok
		aCC = CtElementCode(cOwn, "FORMAT", aF[1])
		CtSetCode(aCC[1], aCC[2])
		return CtFill(cMsg, aDecl, cValue)
	but cK = "expr"
		# v0.6: the text is an expression of the seat's language, or the refusal says why
		aE = CtExprByName(aSeat[2])
		if isNull(aE) return "" ok
		CtExprUse(aE)
		cErr = ""
		try
			ExParse(cValue, [])
		catch
			cErr = cCatchError
		done
		if cErr != ""
			CtSetCode("EXPRESSION", ["rule:" + aSeat[2]])
			return cClause + " of " + aDecl[1] + " " + aDecl[2] + " is not a " + aSeat[2] + " expression -- " + cErr
		ok
		return ""
	but cK = "decl"
		aK = CtKindByDeclName(aSeat[2])
		if isNull(aK) return "" ok
		for i = 1 to len($aCondDecls)
			if $aCondDecls[i][1] = aK[1] and $aCondDecls[i][2] = cValue return "" ok
		next
		# the declaration's own MESSAGES for this seat speaks first (v0.3); its
		# CODES give the envelope's code (v0.11)
		aKd = CtKindByVerb(aDecl[1])
		aCC = CtElementCode(CtCodeFor(aKd, aSeat[1]), "DANGLING", aKd[2] + "." + aSeat[1])
		CtSetCode(aCC[1], aCC[2])
		if len(aKd) >= 5
			for i = 1 to len(aKd[5])
				if aKd[5][i][1] = aSeat[1] return CtFill(aKd[5][i][2], aDecl, cValue) ok
			next
		ok
		cMsg = CtRefusalMessage("dangling_reference")
		cOut = aDecl[2] + " " + cClause + " '" + cValue + "', which resolves to nothing: no such " + aK[1]
		if cMsg != "" cOut += " -- " + cMsg ok
		return cOut
	ok
	return ""

# a clause's value against its seat: scalars directly, lists item by item; a
# UNION seat is checked as the alternative whose shape the value has (v0.3)
# v0.8: a word against a UNION of declarations -- it resolves to a declaration
# of one of the union's kinds, or the union's own MESSAGE speaks
func CtCheckUnionWord(aDecl, aSeat, cValue)
	aU = CtUnionByName(aSeat[2])
	if isNull(aU) return "" ok
	aVerbs = []
	for i = 1 to len(aU[2])
		if aU[2][i][3] != "decl" loop ok
		aK = CtKindByDeclName(aU[2][i][1])
		if isNull(aK) loop ok
		aVerbs + aK[1]
		for j = 1 to len($aCondDecls)
			if $aCondDecls[j][1] = aK[1] and $aCondDecls[j][2] = cValue return "" ok
		next
	next
	cMsg = aU[3]
	if cMsg = "" cMsg = "{VERB} {name} " + upper(aSeat[1]) + " '{value}', which resolves to nothing: no such " + CtJoin(aVerbs, " or ") ok
	cOwn = ""
	if len(aU) >= 4 cOwn = aU[4] ok
	aCC = CtElementCode(cOwn, "UNION", aU[1])
	CtSetCode(aCC[1], aCC[2])
	return CtFill(cMsg, aDecl, cValue)

func CtCheckSeatValue(aDecl, aSeat, aClause, bRefs)
	if CtTypeKind(aSeat) = "union" and not aSeat[3]
		aAlt = CtUnionAlt(aSeat, aClause)
		if isNull(aAlt) return "" ok
		if aAlt[3] = "decl"
			if not bRefs return "" ok
			if aClause[3][1] != "word" return "" ok
			return CtCheckUnionWord(aDecl, aSeat, aClause[3][2])
		ok
		if bRefs return "" ok
		return CtCheckSeatValue(aDecl, [aSeat[1], aAlt[1], aAlt[2], aSeat[4], aAlt[3]], aClause, bRefs)
	ok
	cShape = aClause[3][1]
	if cShape = "word" or cShape = "string" or cShape = "number"
		return CtCheckScalar(aDecl, aSeat, aClause[3][2])
	ok
	cK = CtTypeKind(aSeat)
	aItems = aClause[3][2]
	if aSeat[3] and cK = "union"
		# v0.9: a list of references to several kinds
		aKind = CtKindByVerb(aDecl[1])
		cMsgL = CtMessageFor(aKind, aSeat[1])
		for i = 1 to len(aItems)
			cWhy = CtCheckUnionWord(aDecl, aSeat, aItems[i])
			if cWhy != ""
				if cMsgL != "" return CtFill(cMsgL, aDecl, aItems[i]) ok
				return cWhy
			ok
		next
		return ""
	ok
	if cShape = "pairlist"
		# v0.6: each pair's value takes the form's second seat's type; v0.8: a
		# key is a name (once), a MENU word (a sequence, keys may repeat) or a
		# declaration (resolved), and a value may be a reference
		aF = CtFormByName(aSeat[2])
		if isNull(aF) or len(aF[2]) < 2 return "" ok
		aKeySeat = aF[2][1]
		aValSeat = aF[2][2]
		cKeyK = CtTypeKind(aKeySeat)
		cValK = CtTypeKind(aValSeat)
		aKind = CtKindByVerb(aDecl[1])
		cMsgL = CtMessageFor(aKind, aSeat[1])
		if not bRefs
			if cKeyK != "menu"
				for i = 1 to len(aItems)
					for j = 1 to i - 1
						if aItems[j][1] = aItems[i][1]
							CtSetCode("PARSE", [])
							return "'" + aItems[i][1] + "' is named twice in " + upper(aSeat[1]) + " of " + aDecl[1] + " " + aDecl[2]
						ok
					next
				next
			else
				for i = 1 to len(aItems)
					cWhy = CtCheckScalar(aDecl, aKeySeat, aItems[i][1])
					if cWhy != "" return cWhy ok
				next
			ok
			if cValK != "decl" and cValK != "union"
				for i = 1 to len(aItems)
					cWhy = CtCheckScalar(aDecl, aValSeat, aItems[i][2])
					if cWhy != "" return cWhy ok
				next
			ok
			return ""
		ok
		if cKeyK = "decl"
			for i = 1 to len(aItems)
				cWhy = CtCheckScalar(aDecl, aKeySeat, aItems[i][1])
				if cWhy != ""
					if cMsgL != "" return CtFill(cMsgL, aDecl, aItems[i][1]) ok
					return cWhy
				ok
			next
		ok
		if cValK = "decl"
			for i = 1 to len(aItems)
				cWhy = CtCheckScalar(aDecl, aValSeat, aItems[i][2])
				if cWhy != ""
					if cMsgL != "" return CtFill(cMsgL, aDecl, aItems[i][2]) ok
					return cWhy
				ok
			next
		but cValK = "union"
			for i = 1 to len(aItems)
				cWhy = CtCheckUnionWord(aDecl, aValSeat, aItems[i][2])
				if cWhy != "" return cWhy ok
			next
		ok
		return ""
	ok
	if cK = "menu" or cK = "decl"
		for i = 1 to len(aItems)
			cWhy = CtCheckScalar(aDecl, aSeat, aItems[i])
			if cWhy != "" return cWhy ok
		next
	but cK = "form"
		# a form's one seat may be a FORMAT: each item takes its shape
		aF = CtFormByName(aSeat[2])
		if not isNull(aF) and len(aF[2]) > 0 and CtTypeKind(aF[2][1]) = "format"
			for i = 1 to len(aItems)
				cWhy = CtCheckScalar(aDecl, aF[2][1], aItems[i])
				if cWhy != "" return cWhy ok
			next
		ok
	ok
	return ""

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

# the refinement sentence's own tables (rfn.haro), read by the same parser
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
	if cShape = "union"
		# a UNION seat's shape is the shape of the value written (v0.3)
		cShape = "word"
		aCw = aDecl[4]
		for i = 1 to len(aCw)
			if aCw[i][1] = cClause cShape = aCw[i][3][1] ok
		next
	ok
	if cShape != "word" and cShape != "string" and cShape != "number"
		CtRefuse("constraint", "NOT_A_KNOB", cClause + " is a list seat; this gate refines scalar points only", cRfnFile, nRLine,
		         ["rule:constraint"], "the spike's gate refines knobs, fields and symbols, not composites", "refine a scalar clause")
		return
	ok
	# v0.2: the point is declared in REFINE's POINTS, with its kind. A language
	# that declares no REFINE at all keeps the spike's first rule: every
	# scalar seat is a point (a word or number a knob, a text a field) at the
	# court's floor, trusted.
	cPointName = aKind[2] + "." + lower(cClause)
	cDeclaredKind = ""
	for i = 1 to len($aCourtPoints)
		if $aCourtPoints[i][1] = cPointName cDeclaredKind = $aCourtPoints[i][2] ok
	next
	if len($aCourtPoints) = 0
		cDeclaredKind = "field"
		if cShape = "word" or cShape = "number" cDeclaredKind = "knob" ok
	ok
	if cDeclaredKind = ""
		CtRefuse("constraint", "NOT_A_POINT", "'" + cTarget + "' is not a declared refinement point of " + $cCourtLang + " (" + cPointName + " is not in REFINE's POINTS)",
		         cRfnFile, nRLine, ["rule:refine-points"], "every refinable point is declared by the language, with its kind; the boundaries are language-required, not author-chosen",
		         "propose a change to a declared point, or declare this one in the language's REFINE")
		return
	ok
	cKindGiven = CtClauseText(aR, "KIND")
	if cKindGiven != cDeclaredKind
		CtRefuse("constraint", "KIND_MISMATCH", "'" + cTarget + "' is a " + cDeclaredKind + ", not a " + cKindGiven, cRfnFile, nRLine,
		         ["rule:refine-points"], "the point's kind is declared by the language", "say KIND " + cDeclaredKind)
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
	# v0.2: the bounds of the point are the seat's declared type (a MENU, a RANGE, a FORMAT)
	cWhy = CtCheckScalar(aDecl, aSeat, cTo)
	if cWhy != ""
		CtRefuse("constraint", "OUT_OF_BOUNDS", cWhy, cRfnFile, nRLine, ["rule:constraint"],
		         "a knob's bounds are the declared type of its seat; the court speaks the type's own message",
		         "propose a value the seat's type admits")
		return
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
	# v0.2: the floor is the point's own (REFINE's FLOOR), trusted when it declares none
	cFloor = "trusted"
	for i = 1 to len($aCourtFloors)
		if $aCourtFloors[i][1] = cPointName cFloor = $aCourtFloors[i][2] ok
	next
	if nRank < CtPostureRank(cFloor)
		CtRefuse("trust", "TRUST_FLOOR", "posture :" + cPosture + " below the required floor :" + cFloor + " for '" + cTarget + "'", cRfnFile, nRLine,
		         ["rule:trust-floor"], "the point's floor is declared by the language (REFINE's FLOOR; trusted when none is declared): a proposal below it is refused by construction, not by convention",
		         "an actor of posture :" + cFloor + " or above may propose the same change; or lower the point's floor in the language's REFINE")
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

# ---- v0.6: a sentence's expressions evaluated, and a WALK run ---------------------
# `<court>.ring eval <file> <decl> <seat> <json>`: the expression in SEAT of the
# declaration DECL, evaluated on the record, answers true or false.
# `<court>.ring walk <file> <name> <json>`: the record walks the steps of the
# declaration NAME under the WALK of its kind -- every step whose THROUGH seat
# names it, in ORDER; at each step the FORMULA, when written, computes the
# COMPUTE seat's value into the record first (for this step's guards and every
# later one, as zing's runner does), then each GUARD in the WALK's order must
# hold; the first that does not stops the walk. The verdict is JSON:
#   {"status": "complete", "computed": {name: value, ...}}
#   {"status": "failed", "at": step, "code": <the FAIL seat>, "reason": why}
# A guard read through a reference (enforcing.rule) takes its reason from the
# referenced declaration's `message` seat when it has one.

func CtDeclNamed(aDecls, cName)
	for i = 1 to len(aDecls)
		if aDecls[i][2] = cName return aDecls[i] ok
	next
	return NULL

func CtWalkOf(cKindName)
	for i = 1 to len($aCourtWalks)
		if $aCourtWalks[i][2] = cKindName return $aCourtWalks[i] ok
	next
	return NULL

# the node of an expression seat, parsed under its language; NULL when the
# clause is not written
func CtExprNode(aDecl, cSeat)
	aKind = CtKindByVerb(aDecl[1])
	aSeat = CtSeatByClause(aKind, upper(cSeat))
	if isNull(aSeat) raise("no seat '" + cSeat + "' on " + aDecl[1]) ok
	if CtTypeKind(aSeat) != "expr" raise(upper(cSeat) + " of " + aDecl[1] + " " + aDecl[2] + " is not an expression seat") ok
	cText = CondScalar(aDecl, cSeat)
	if isNull(cText) return NULL ok
	aE = CtExprByName(aSeat[2])
	if isNull(aE) raise("the court carries no EXPRESSION called '" + aSeat[2] + "'") ok
	CtExprUse(aE)
	return ExParse(cText, [])

func CtEval(aDecls, cDecl, cSeat, aRecord)
	aD = CtDeclNamed(aDecls, cDecl)
	if isNull(aD) raise("no declaration named '" + cDecl + "' in this file") ok
	aNode = CtExprNode(aD, cSeat)
	if isNull(aNode) raise(upper(cSeat) + " is not written on " + aD[1] + " " + aD[2]) ok
	ExSetRecord(aRecord)
	return ExBool(aNode, [])

# a guard of a step: [node, reason], or [NULL, ""] when the seat is not written
func CtGuard(aDecls, aStep, cPath)
	nDot = substr(cPath, ".")
	if nDot = 0
		aNode = CtExprNode(aStep, cPath)
		return [aNode, upper(cPath) + " failed"]
	ok
	cHead = left(cPath, nDot - 1)
	cTail = substr(cPath, nDot + 1)
	cRef = CondScalar(aStep, cHead)
	if isNull(cRef) return [NULL, ""] ok
	aTarget = CtDeclNamed(aDecls, cRef)
	if isNull(aTarget) return [NULL, ""] ok
	aNode = CtExprNode(aTarget, cTail)
	cReason = CondScalar(aTarget, "message")
	if isNull(cReason) cReason = upper(cTail) + " of " + aTarget[1] + " " + aTarget[2] + " failed" ok
	return [aNode, cReason]

func CtWalk(aDecls, cName, aRecord)
	aD = CtDeclNamed(aDecls, cName)
	if isNull(aD) raise("no declaration named '" + cName + "' in this file") ok
	aKind = CtKindByVerb(aD[1])
	aW = CtWalkOf(aKind[2])
	if isNull(aW) raise("no WALK of " + aKind[2] + " is declared, so " + aD[1] + " " + cName + " cannot be walked") ok
	aStepKind = CtKindByDeclName(aW[3])
	# the steps THROUGH this declaration, in ORDER (an insertion sort on the
	# number: Ring's sort() orders a column of text)
	aSteps = []
	for i = 1 to len(aDecls)
		if aDecls[i][1] != aStepKind[1] loop ok
		cThrough = CondScalar(aDecls[i], aW[4])
		if isNull(cThrough) or cThrough != cName loop ok
		nOrder = 0 + CondScalar(aDecls[i], aW[5])
		nAt = len(aSteps) + 1
		for j = 1 to len(aSteps)
			if nOrder < aSteps[j][1]
				nAt = j
				exit
			ok
		next
		aEntry = [nOrder, aDecls[i]]
		if nAt > len(aSteps)
			aSteps + aEntry
		else
			# Ring's insert() puts the item AFTER the index: before j is after j-1 (HF-52)
			insert(aSteps, nAt - 1, aEntry)
		ok
	next
	ExSetRecord(aRecord)
	aComputed = [ExObjMark()]
	for i = 1 to len(aSteps)
		aStep = aSteps[i][2]
		if aW[7] != "" and aW[8] != ""
			cTarget = CondScalar(aStep, aW[7])
			aF = CtExprNode(aStep, aW[8])
			if not isNull(cTarget) and not isNull(aF)
				v = ExNum(ExEval(aF, []))
				$aExprOverlay + [cTarget, v]
				aPair = [cTarget, v]
				aComputed + aPair
			ok
		ok
		aG = aW[6]
		for j = 1 to len(aG)
			aGuard = CtGuard(aDecls, aStep, aG[j])
			if isNull(aGuard[1]) loop ok
			if not ExBool(aGuard[1], [])
				aOut = [ExObjMark(), ["status", "failed"], ["at", aStep[2]]]
				if aW[9] != ""
					cCode = CondScalar(aStep, aW[9])
					if not isNull(cCode)
						aPair = ["code", cCode]
						aOut + aPair
					ok
				ok
				aPair = ["reason", aGuard[2]]
				aOut + aPair
				return aOut
			ok
		next
	next
	aOut = [ExObjMark(), ["status", "complete"], ["computed", aComputed]]
	return aOut

# the command: check <file> | refine <file> <file.rfn> | eval ... | walk ... | ask ...
func CtMain()
	if len(sysargv) < 4
		? "usage: <court>.ring check <file" + $cCourtExt + "> | refine <file" + $cCourtExt + "> <file.rfn> | eval <file> <decl> <seat> <json> | walk <file> <name> <json> | ask <file> <question> <rows json>"
		return
	ok
	cVerb = sysargv[3]
	# the judged file's folder: a SENTENCE seat's file is read beside it (v0.4)
	$cCourtDir = CtDirOf(sysargv[4])
	if cVerb = "check"
		# v0.10: `check <file> [<world.json>]` -- with a world, every SYMBOL seat
		# resolves against it; without one, a sentence that holds SYMBOL seats is
		# judged alone and the last line says so, a warning (C2's "undecidable
		# without more input"), never a refusal
		cSrc = read(sysargv[4])
		try
			# v0.17: `surfaces` asks each surface's own court to judge its queries (a language that is understood)
			if not isNull($aCourtUnderstand) and len(sysargv) >= 5
				if sysargv[5] = "surfaces" $bNSurfaces = 1 ok
			ok
			if len(sysargv) >= 5 and not $bNSurfaces $aCourtWorldFile = CtWorldLoad(sysargv[5]) ok
			aDecls = CtDeclare(cSrc)
			CtPrintVerdict(aDecls)
			if isNull($aCourtWorldFile) and len($aCourtSymbols) > 0
				nSites = len(CtSymbolSites(aDecls))
				if nSites > 0
					? "warning NO_WORLD: no world to resolve against; " + nSites + " symbol reference(s) unresolved, which is what C3 section 3.2 asks a project to close"
				ok
			ok
		catch
			? cCatchError
		done
	but cVerb = "diagnose"
		# v0.11: the same court, in the family's machine form (C2 v1.2.0)
		cWorldPath = ""
		if not isNull($aCourtUnderstand) and len(sysargv) >= 5
			if sysargv[5] = "surfaces" $bNSurfaces = 1 ok
		ok
		if len(sysargv) >= 5 and not $bNSurfaces cWorldPath = sysargv[5] ok
		? CtDiagnosticsJson(CtDiagnose(sysargv[4], cWorldPath))
	but cVerb = "world"
		# v0.10: the sentence's own C1 rows, as JSON
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			? ExJson(CtWorldRows(aDecls, CtWorldStem(sysargv[4]) + $cCourtExt))
		catch
			? cCatchError
		done
	but cVerb = "refine"
		if len(sysargv) < 5
			? "usage: <court>.ring refine <file" + $cCourtExt + "> <file.rfn>"
			return
		ok
		CtRefine(sysargv[4], sysargv[5])
	but cVerb = "eval"
		if len(sysargv) < 7
			? "usage: <court>.ring eval <file" + $cCourtExt + "> <decl> <seat> <json>"
			return
		ok
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			aRecord = ExJsonParse(sysargv[7])
			if CtEval(aDecls, sysargv[5], sysargv[6], aRecord)
				? "true"
			else
				? "false"
			ok
		catch
			? cCatchError
		done
	but cVerb = "walk"
		if len(sysargv) < 6
			? "usage: <court>.ring walk <file" + $cCourtExt + "> <name> <json>"
			return
		ok
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			aRecord = ExJsonParse(sysargv[6])
			? ExJson(CtWalk(aDecls, sysargv[5], aRecord))
		catch
			? cCatchError
		done
	but cVerb = "run"
		# v0.9: an algorithm run on a record
		if len(sysargv) < 6
			? "usage: <court>.ring run <file" + $cCourtExt + "> <algorithm> <record json>"
			return
		ok
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			if isNull($aCourtRun) CtFail(1, "this language declares no RUN, so nothing in it runs") ok
			aRecord = ExJsonParse(sysargv[6])
			? ExJson(RunAlgorithm(aDecls, sysargv[5], aRecord))
		catch
			? cCatchError
		done
	but cVerb = "narrate"
		# v0.13: the sentence narrated back in the language's own voice, on stdout, never stored
		if len(sysargv) < 4
			? "usage: <court>.ring narrate <file" + $cCourtExt + ">"
			return
		ok
		try
			if isNull($aCourtNarrate) CtFail(1, "this language declares no NARRATE, so it has no voice") ok
			NarrateRun(sysargv[4])
		catch
			? cCatchError
		done
	but cVerb = "narrate-run"
		# v0.16: an algorithm run on a record, told in the language's own voice -- the same run `run` makes, never a second one
		if len(sysargv) < 6
			? "usage: <court>.ring narrate-run <file" + $cCourtExt + "> <algorithm> <record json>"
			return
		ok
		try
			if isNull($aCourtNarrate) CtFail(1, "this language declares no NARRATE, so it has no voice") ok
			if isNull($aCourtRun) CtFail(1, "this language declares no RUN, so nothing in it runs") ok
			NarTellRun(sysargv[4], sysargv[5], sysargv[6])
		catch
			? cCatchError
		done
	but cVerb = "narrate-ask"
		# v0.16: a question answered on rows, told in the language's own voice -- the same answer `ask` gives
		if len(sysargv) < 6
			? "usage: <court>.ring narrate-ask <file" + $cCourtExt + "> <question> <rows json>"
			return
		ok
		try
			if isNull($aCourtNarrate) CtFail(1, "this language declares no NARRATE, so it has no voice") ok
			if isNull($aCourtAsk) CtFail(1, "this language declares no ASK, so it answers no question") ok
			NarTellAsk(sysargv[4], sysargv[5], sysargv[6])
		catch
			? cCatchError
		done
	but cVerb = "family"
		# v0.12: the members of every declared family, generated from the FORMS
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			if isNull($aCourtFormset) CtFail(1, "this language declares no FORMS, so it spells no family") ok
			FormsPrintFamilies(aDecls)
		catch
			? cCatchError
		done
	but cVerb = "spellings"
		# v0.12: a list of names judged against the FORMS and the declared families
		if len(sysargv) < 5
			? "usage: <court>.ring spellings <file" + $cCourtExt + "> <names.txt>"
			return
		ok
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			if isNull($aCourtFormset) CtFail(1, "this language declares no FORMS, so it judges no spelling") ok
			FormsPrintSpellings(aDecls, FormsReadNames(sysargv[5]))
		catch
			? cCatchError
		done
	but not isNull($aCourtUnderstand) and CtInList(cVerb, ["tokens", "understand", "ask", "vocabulary", "examples"])
		# v0.17: a human language over a declared world, understood (n_lib.ring); `ask` here takes a tongue and
		# a text, where the Q letter's takes a question and rows -- different courts, different arguments
		NatMain(cVerb)
	but cVerb = "ask"
		# v0.7: a question of the declared world, answered on the rows handed in
		if len(sysargv) < 6
			? "usage: <court>.ring ask <file" + $cCourtExt + "> <question> <rows json>"
			return
		ok
		cSrc = read(sysargv[4])
		try
			aDecls = CtDeclare(cSrc)
			if isNull($aCourtAsk) CtFail(1, "this language declares no ASK, so it answers no question") ok
			aRows = ExJsonParse(sysargv[6])
			? ExJson(AskRun(aDecls, sysargv[5], aRows))
		catch
			? cCatchError
		done
	else
		? "unknown verb '" + cVerb + "'; this court answers: check, refine, eval, walk, ask, run, world, diagnose, family, spellings, narrate, narrate-run, narrate-ask"
	ok
