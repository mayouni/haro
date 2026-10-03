# n_lib.ring -- the dynamic half of N, the natural letter, in pure core Ring (the seventeenth rung).
#
# Loaded by a court FORGED from a letter that declares an UNDERSTAND (forge.ring), and only by one. It
# reads the sentence the court has already parsed -- the court's own declaration records, never a second
# parser -- through the eight roles the UNDERSTAND names ($aCourtUnderstand), so it knows no kind by its
# spelling: a letter that plays the roles with other declarations is understood the same way.
#
#   NatCheckRules(aDecls)    the rules of v17/GRAMMAR.md section 4b, raised through the court's own CtFailC
#   NatMain(cVerb)           tokens, understand, ask, vocabulary, examples -- one JSON object on stdout
#
# The algorithm is v17/n_model.py's, ported and judged against it (v17/n_check.py): gate, separators, case
# folding, each token ignored, a word of a meaning, a generated entity or alias word, or digits (1 to 12);
# the meanings, in order, against each frame's SHAPE; the template filled. Nothing a question says is
# evaluated. Case is folded for ASCII and for Latin-1 (the two-byte letters U+00C0 to U+00DE), and for no
# other script: a tongue whose script has case needs the court to learn it, in the open.
#
# A context aN is built once per verb from the declaration records:
#   1 the records  2 the worlds [surface, [[s, p, o], ...], read?, path]  3 tongues  4 meanings  5 aliases
#   6 surfaces  7 steps  8 frames  9 examples  10 counterexamples
# A result of understand/ask is ["ok", frame, slots [[name, value]], surface, query, steps [[surface, query,
# binds]], answer, answered?, told, query2, runs [[surface, court, world, query]]] or ["refused", kind, what,
# message, tongue].
#
# Functions only, and no global of its own beyond the two the forge emits ($aCourtUnderstand, $bNSurfaces).

# ---- bytes and words ---------------------------------------------------------------------------------

func NatFold(cS)
	cOut = ""
	nLen = len(cS)
	i = 1
	while i <= nLen
		cC = cS[i]
		nA = ascii(cC)
		if nA >= 65 and nA <= 90
			cOut += char(nA + 32)
			i++
		but nA = 195 and i < nLen
			nB = ascii(cS[i + 1])
			if nB >= 128 and nB <= 158 and nB != 151
				cOut += cC + char(nB + 32)
			else
				cOut += cC + cS[i + 1]
			ok
			i += 2
		else
			cOut += cC
			i++
		ok
	end
	return cOut

func NatUpperFirst(cS)
	if len(cS) = 0 return cS ok
	nA = ascii(cS[1])
	if nA >= 97 and nA <= 122
		if len(cS) = 1 return char(nA - 32) ok
		return char(nA - 32) + substr(cS, 2)
	ok
	return cS

func NatSpell(cEnt, cHow)
	if cHow = "upper_first" return NatUpperFirst(cEnt) ok
	return cEnt

# the words of a text: split on a space, a tab, a line feed or a carriage return
func NatWords(cS)
	aOut = []
	cWord = ""
	for i = 1 to len(cS)
		cC = cS[i]
		if cC = " " or cC = char(9) or cC = char(10) or cC = char(13)
			if len(cWord) > 0
				aOut + cWord
				cWord = ""
			ok
		else
			cWord += cC
		ok
	next
	if len(cWord) > 0 aOut + cWord ok
	return aOut

func NatTrim(cS)
	nFrom = 1
	nTo = len(cS)
	while nFrom <= nTo and NatIsSpace(cS[nFrom])
		nFrom++
	end
	while nTo >= nFrom and NatIsSpace(cS[nTo])
		nTo--
	end
	if nTo < nFrom return "" ok
	return substr(cS, nFrom, nTo - nFrom + 1)

func NatIsSpace(cC)
	nA = ascii(cC)
	return nA = 32 or nA = 9 or nA = 10 or nA = 13

func NatIsDigits(cS)
	if len(cS) = 0 return 0 ok
	for i = 1 to len(cS)
		nA = ascii(cS[i])
		if nA < 48 or nA > 57 return 0 ok
	next
	return 1

func NatIsWordChar(cC)
	nA = ascii(cC)
	return (nA >= 48 and nA <= 57) or (nA >= 65 and nA <= 90) or (nA >= 97 and nA <= 122) or nA = 95 or nA >= 128

func NatLess(cA, cB)
	nMin = len(cA)
	if len(cB) < nMin nMin = len(cB) ok
	for i = 1 to nMin
		nX = ascii(cA[i])
		nY = ascii(cB[i])
		if nX < nY return 1 ok
		if nX > nY return 0 ok
	next
	return len(cA) < len(cB)

func NatLines(cS)
	aOut = []
	cLine = ""
	for i = 1 to len(cS)
		cC = cS[i]
		if cC = char(10)
			aOut + cLine
			cLine = ""
		but cC != char(13)
			cLine += cC
		ok
	next
	aOut + cLine
	return aOut

# the fields of a line separated by |, each trimmed
func NatSplitBar(cS)
	aOut = []
	cField = ""
	for i = 1 to len(cS)
		if cS[i] = "|"
			aOut + NatTrim(cField)
			cField = ""
		else
			cField += cS[i]
		ok
	next
	aOut + NatTrim(cField)
	return aOut

func NatCount(cS, cCh)
	nN = 0
	for i = 1 to len(cS)
		if cS[i] = cCh nN++ ok
	next
	return nN

# every {name} of a template, in order
func NatPlaceholders(cS)
	aOut = []
	nLen = len(cS)
	i = 1
	while i <= nLen
		if cS[i] = "{"
			j = i + 1
			while j <= nLen and NatIsWordChar(cS[j])
				j++
			end
			if j > i + 1 and j <= nLen and cS[j] = "}"
				aOut + substr(cS, i + 1, j - i - 1)
				i = j + 1
			else
				i++
			ok
		else
			i++
		ok
	end
	return aOut

func NatHex(nN)
	nHi = floor(nN / 16)
	nLo = nN - nHi * 16
	return substr("0123456789abcdef", nHi + 1, 1) + substr("0123456789abcdef", nLo + 1, 1)

# a JSON string
func NatQ(cS)
	cOut = ""
	for i = 1 to len(cS)
		cC = cS[i]
		nA = ascii(cC)
		if cC = char(34)
			cOut += char(92) + char(34)
		but cC = char(92)
			cOut += char(92) + char(92)
		but nA = 10
			cOut += char(92) + "n"
		but nA = 13
			cOut += char(92) + "r"
		but nA = 9
			cOut += char(92) + "t"
		but nA < 32
			cOut += char(92) + "u00" + NatHex(nA)
		else
			cOut += cC
		ok
	next
	return char(34) + cOut + char(34)

func NatQList(aL)
	cOut = "["
	for i = 1 to len(aL)
		if i > 1 cOut += ", " ok
		cOut += NatQ(aL[i])
	next
	return cOut + "]"

func NatSameList(aA, aB)
	if len(aA) != len(aB) return 0 ok
	for i = 1 to len(aA)
		if aA[i] != aB[i] return 0 ok
	next
	return 1

# ---- the declaration records, read by seat -----------------------------------------------------------------

# the clause of a seat, [NAME, line, value, start, end], or NULL
func NatClause(aD, cSeat)
	cU = upper(cSeat)
	aC = aD[4]
	for i = 1 to len(aC)
		if aC[i][1] = cU return aC[i] ok
	next
	return NULL

func NatHas(aD, cSeat)
	return not isNull(NatClause(aD, cSeat))

# a word or a string, else ""
func NatText(aD, cSeat)
	aC = NatClause(aD, cSeat)
	if isNull(aC) return "" ok
	if aC[3][1] = "word" or aC[3][1] = "string" return aC[3][2] ok
	return ""

# a list of words, else []
func NatNames(aD, cSeat)
	aC = NatClause(aD, cSeat)
	if isNull(aC) return [] ok
	if aC[3][1] = "namelist" return aC[3][2] ok
	return []

# name: value pairs as [[name, value], ...], else []
func NatPairs(aD, cSeat)
	aOut = []
	aC = NatClause(aD, cSeat)
	if isNull(aC) return aOut ok
	if aC[3][1] != "pairlist" return aOut ok
	aP = aC[3][2]
	for i = 1 to len(aP)
		aOut + [aP[i][1], aP[i][2]]
	next
	return aOut

# the value of a key in a list of pairs, or ""; the second answer is whether the key is there
func NatPairValue(aPairs, cKey)
	for i = 1 to len(aPairs)
		if aPairs[i][1] = cKey return aPairs[i][2] ok
	next
	return ""

func NatHasKey(aPairs, cKey)
	for i = 1 to len(aPairs)
		if aPairs[i][1] = cKey return 1 ok
	next
	return 0

# the verb of the declaration kind that plays a role of the UNDERSTAND
func NatVerbOf(cRole)
	aR = $aCourtUnderstand[2]
	for i = 1 to len(aR)
		if aR[i][1] = cRole
			aK = CtKindByDeclName(aR[i][2])
			if not isNull(aK) return aK[1] ok
		ok
	next
	return ""

func NatOf(aDecls, cRole)
	cV = NatVerbOf(cRole)
	aOut = []
	for i = 1 to len(aDecls)
		if aDecls[i][1] = cV aOut + aDecls[i] ok
	next
	return aOut

func NatFind(aList, cName)
	for i = 1 to len(aList)
		if aList[i][2] = cName return aList[i] ok
	next
	return NULL

# ---- the world: a surface's versioned artifact (facts `s | p | o` under a `facts` line) -------------------

func NatPath(cRel)
	if $cCourtDir = "" return cRel ok
	return $cCourtDir + "/" + cRel

# [read?, [[s, p, o], ...]]
func NatReadWorld(cPath)
	if not fexists(cPath) return [0, []] ok
	aLines = NatLines(read(cPath))
	cSection = ""
	aTriples = []
	for i = 1 to len(aLines)
		cT = NatTrim(aLines[i])
		if cT = "facts" or cT = "ontology"
			cSection = cT
		but cSection = "facts" and NatCount(cT, "|") = 2
			aP = NatSplitBar(cT)
			aTriples + [aP[1], aP[2], aP[3]]
		ok
	next
	return [1, aTriples]

func NatBuild(aDecls)
	aWorlds = []
	aSurf = NatOf(aDecls, "SURFACE")
	for i = 1 to len(aSurf)
		cW = NatText(aSurf[i], "world")
		if cW != ""
			aR = NatReadWorld(NatPath(cW))
			aWorlds + [aSurf[i][2], aR[2], aR[1], NatPath(cW)]
		ok
	next
	return [aDecls, aWorlds, NatOf(aDecls, "TONGUE"), NatOf(aDecls, "MEANING"), NatOf(aDecls, "ALIAS"), aSurf,
	        NatOf(aDecls, "STEP"), NatOf(aDecls, "FRAME"), NatOf(aDecls, "EXAMPLE"), NatOf(aDecls, "COUNTEREXAMPLE")]

func NatTriples(aN, cSurface)
	aW = aN[2]
	for i = 1 to len(aW)
		if aW[i][1] = cSurface return aW[i][2] ok
	next
	return []

# the ids a surface enumerates for the entity kind a meaning is OF
func NatEntities(aN, aMeaning)
	aOut = []
	if NatText(aMeaning, "slot") != "entity" return aOut ok
	cFrom = NatText(aMeaning, "from")
	cOf = NatText(aMeaning, "of")
	if cFrom = "" or cOf = "" return aOut ok
	aT = NatTriples(aN, cFrom)
	for i = 1 to len(aT)
		if aT[i][2] = "is-a" and aT[i][3] = cOf aOut + aT[i][1] ok
	next
	return aOut

# ---- the lexicon of a tongue: [ignored, [[word, meaning, entity], ...], [[word, meaning, meaning], ...]] ------

func NatAddWord(aWords, aClash, cWord, cMeaning, cEnt)
	cKey = NatFold(cWord)
	for i = 1 to len(aWords)
		if aWords[i][1] = cKey
			if not (aWords[i][2] = cMeaning and aWords[i][3] = cEnt)
				aClash + [cKey, aWords[i][2], cMeaning]
			ok
			aWords[i][2] = cMeaning
			aWords[i][3] = cEnt
			return
		ok
	next
	aWords + [cKey, cMeaning, cEnt]

func NatLexicon(aN, cTongue)
	aT = NatFind(aN[3], cTongue)
	aIgnored = []
	aIg = NatWords(NatText(aT, "ignores"))
	for i = 1 to len(aIg)
		aIgnored + NatFold(aIg[i])
	next
	aWords = []
	aClash = []
	aM = aN[4]
	for i = 1 to len(aM)
		aP = NatPairs(aM[i], "words")
		for j = 1 to len(aP)
			if aP[j][1] = cTongue
				aTx = NatWords(aP[j][2])
				for k = 1 to len(aTx)
					NatAddWord(aWords, aClash, aTx[k], aM[i][2], "")
				next
			ok
		next
		if NatText(aM[i], "slot") = "entity"
			aE = NatEntities(aN, aM[i])
			for j = 1 to len(aE)
				NatAddWord(aWords, aClash, aE[j], aM[i][2], aE[j])
			next
		ok
	next
	aA = aN[5]
	for i = 1 to len(aA)
		aP = NatPairs(aA[i], "words")
		for j = 1 to len(aP)
			if aP[j][1] = cTongue
				aTx = NatWords(aP[j][2])
				for k = 1 to len(aTx)
					NatAddWord(aWords, aClash, aTx[k], NatText(aA[i], "meaning"), NatText(aA[i], "entity"))
				next
			ok
		next
	next
	return [aIgnored, aWords, aClash]

# the word an answer is told in: an alias's first word, else the tongue's own spelling of a name
func NatCanonical(aN, cTongue, cEnt)
	aA = aN[5]
	for i = 1 to len(aA)
		if NatText(aA[i], "entity") = cEnt
			aP = NatPairs(aA[i], "words")
			for j = 1 to len(aP)
				if aP[j][1] = cTongue
					aTx = NatWords(aP[j][2])
					if len(aTx) > 0 return aTx[1] ok
				ok
			next
		ok
	next
	cHow = NatText(NatFind(aN[3], cTongue), "names")
	if cHow = "" cHow = "as_is" ok
	return NatSpell(cEnt, cHow)

# the one meaning that captures digits: the only text of a question a query may hold
func NatNumMeaning(aN)
	aM = aN[4]
	for i = 1 to len(aM)
		if NatText(aM[i], "slot") = "number" return aM[i][2] ok
	next
	return ""

# ---- the gate and the tokens ------------------------------------------------------------------------------------

# "" when every character passes; else the one refused, a control character by its code
func NatGate(aT, cText)
	cAllows = NatText(aT, "allows")
	for i = 1 to len(cText)
		cC = cText[i]
		nA = ascii(cC)
		bOk = 0
		if nA >= 128 or nA = 32 or (nA >= 48 and nA <= 57) or (nA >= 65 and nA <= 90) or (nA >= 97 and nA <= 122)
			bOk = 1
		ok
		if not bOk
			for j = 1 to len(cAllows)
				if cAllows[j] = cC bOk = 1 ok
			next
		ok
		if not bOk
			if nA < 32 or nA = 127 return "(control character " + nA + ")" ok
			return cC
		ok
	next
	return ""

func NatRefuse(aN, cTongue, cKind, cWhat)
	cMsg = cKind + ": " + cWhat
	aR = NatPairs(NatFind(aN[3], cTongue), "refuses")
	if NatHasKey(aR, cKind) cMsg = CtReplace(NatPairValue(aR, cKind), "{what}", cWhat) ok
	return ["refused", cKind, cWhat, cMsg, cTongue]

# ["refused", kind, what] or ["ok", [[meaning, entity, raw], ...], [ignored raw words]]
func NatTokens(aN, cTongue, cText)
	aT = NatFind(aN[3], cTongue)
	cBad = NatGate(aT, cText)
	if cBad != "" return ["refused", "character", cBad] ok
	aLex = NatLexicon(aN, cTongue)
	cNorm = cText
	cSeps = "'?,."
	for i = 1 to len(cSeps)
		cNorm = CtReplace(cNorm, cSeps[i], " ")
	next
	cNum = NatNumMeaning(aN)
	aToks = []
	aSkipped = []
	aRaw = NatWords(cNorm)
	for i = 1 to len(aRaw)
		cKey = NatFold(aRaw[i])
		if CtInList(cKey, aLex[1])
			aSkipped + aRaw[i]
			loop
		ok
		nAt = 0
		for j = 1 to len(aLex[2])
			if aLex[2][j][1] = cKey nAt = j ok
		next
		if nAt > 0
			aToks + [aLex[2][nAt][2], aLex[2][nAt][3], aRaw[i]]
		but cNum != "" and NatIsDigits(cKey) and len(cKey) <= 12
			aToks + [cNum, cKey, aRaw[i]]
		else
			return ["refused", "word", aRaw[i]]
		ok
	next
	return ["ok", aToks, aSkipped]

# ---- understand ---------------------------------------------------------------------------------------------------

# a template with its slots filled: an entity spelled the way the target surface spells its kind
func NatFill(aN, cTemplate, aSlots, cSurface)
	cOut = cTemplate
	aSpells = NatPairs(NatFind(aN[6], cSurface), "spells")
	for i = 1 to len(aSlots)
		cVal = aSlots[i][2]
		aM = NatFind(aN[4], aSlots[i][1])
		if not isNull(aM)
			if NatText(aM, "slot") = "entity"
				cHow = "as_is"
				if NatHasKey(aSpells, NatText(aM, "of")) cHow = NatPairValue(aSpells, NatText(aM, "of")) ok
				cVal = NatSpell(cVal, cHow)
			ok
		ok
		cOut = CtReplace(cOut, "{" + aSlots[i][1] + "}", cVal)
	next
	return cOut

func NatSetSlot(aSlots, cName, cVal)
	for i = 1 to len(aSlots)
		if aSlots[i][1] = cName
			aSlots[i][2] = cVal
			return
		ok
	next
	aSlots + [cName, cVal]

func NatUnderstand(aN, cTongue, cText)
	aTk = NatTokens(aN, cTongue, cText)
	if aTk[1] = "refused" return NatRefuse(aN, cTongue, aTk[2], aTk[3]) ok
	aToks = aTk[2]
	aShape = []
	for i = 1 to len(aToks)
		aShape + aToks[i][1]
	next
	aFrames = aN[8]
	for i = 1 to len(aFrames)
		aF = aFrames[i]
		if not NatSameList(NatNames(aF, "shape"), aShape) loop ok
		aSlots = []
		for j = 1 to len(aToks)
			aM = NatFind(aN[4], aToks[j][1])
			cSlot = NatText(aM, "slot")
			if cSlot = "number" or cSlot = "entity" NatSetSlot(aSlots, aToks[j][1], aToks[j][2]) ok
		next
		# a sentence under construction may name a surface or a step nobody declared: a finding of the rules,
		# never a crash of the court
		bLawful = 0
		if NatHas(aF, "steps")
			bLawful = 1
			aSn = NatNames(aF, "steps")
			for j = 1 to len(aSn)
				aS = NatFind(aN[7], aSn[j])
				if isNull(aS)
					bLawful = 0
				else
					if isNull(NatFind(aN[6], NatText(aS, "target"))) bLawful = 0 ok
				ok
			next
		else
			if not isNull(NatFind(aN[6], NatText(aF, "target"))) and NatHas(aF, "query") bLawful = 1 ok
		ok
		if not bLawful return NatRefuse(aN, cTongue, "surface", aF[2]) ok
		cSurface = NatText(aF, "target")
		cQuery = ""
		aSteps = []
		if NatHas(aF, "steps")
			cSurface = "plan"
			aSn = NatNames(aF, "steps")
			for j = 1 to len(aSn)
				aS = NatFind(aN[7], aSn[j])
				cQ = NatFill(aN, NatText(aS, "query"), aSlots, NatText(aS, "target"))
				aSteps + [NatText(aS, "target"), cQ, NatText(aS, "binds")]
			next
		else
			cQuery = NatFill(aN, NatText(aF, "query"), aSlots, cSurface)
		ok
		return ["ok", aF[2], aSlots, cSurface, cQuery, aSteps, [], 0, "", "", []]
	next
	return NatRefuse(aN, cTongue, "shape", NatJoinNames(aShape))

func NatJoinNames(aL)
	return CtJoin(aL, " ")

# ---- ask: a pattern surface answered, and told --------------------------------------------------------------------

# [ran?, [answer terms]]: a triple pattern over the surface's facts, `?x` a variable
func NatRunPattern(aN, cSurface, cQuery)
	aTerms = NatWords(cQuery)
	if len(aTerms) != 3 return [0, []] ok
	aT = NatTriples(aN, cSurface)
	aAns = []
	for i = 1 to len(aT)
		bAll = 1
		for j = 1 to 3
			if left(aTerms[j], 1) != "?" and aTerms[j] != aT[i][j] bAll = 0 ok
		next
		if bAll
			for j = 1 to 3
				if left(aTerms[j], 1) = "?" aAns + aT[i][j] ok
			next
		ok
	next
	return [1, aAns]

# the answer told by the frame's own template in the tongue, or "" when the frame has none
func NatTell(aN, cTongue, aF, aAnswer, aSlots)
	cKey = "answers"
	if len(aAnswer) = 0 cKey = "empty" ok
	aP = NatPairs(aF, cKey)
	if not NatHasKey(aP, cTongue) return "" ok
	cTpl = NatPairValue(aP, cTongue)
	aNames = []
	for i = 1 to len(aAnswer)
		aNames + NatCanonical(aN, cTongue, aAnswer[i])
	next
	cConj = NatText(NatFind(aN[3], cTongue), "joins")
	if cConj = "" cConj = "and" ok
	cJoined = ""
	if len(aNames) = 1
		cJoined = aNames[1]
	but len(aNames) > 1
		for i = 1 to len(aNames) - 1
			if i > 1 cJoined += ", " ok
			cJoined += aNames[i]
		next
		cJoined += " " + cConj + " " + aNames[len(aNames)]
	ok
	cOut = CtReplace(cTpl, "{answer}", cJoined)
	for i = 1 to len(aSlots)
		cVal = aSlots[i][2]
		aM = NatFind(aN[4], aSlots[i][1])
		if not isNull(aM)
			if NatText(aM, "slot") = "entity" cVal = NatCanonical(aN, cTongue, cVal) ok
		ok
		cOut = CtReplace(cOut, "{" + aSlots[i][1] + "}", cVal)
	next
	return cOut

func NatRunOf(aN, cSurface, cQuery)
	aSf = NatFind(aN[6], cSurface)
	return [cSurface, NatText(aSf, "court"), NatText(aSf, "world"), cQuery]

func NatAsk(aN, cTongue, cText)
	aU = NatUnderstand(aN, cTongue, cText)
	if aU[1] = "refused" return aU ok
	aF = NatFind(aN[8], aU[2])
	if aU[4] = "plan"
		aSn = NatNames(aF, "steps")
		aS1 = NatFind(aN[7], aSn[1])
		cT1 = NatText(aS1, "target")
		cQ1 = NatFill(aN, NatText(aS1, "query"), aU[3], cT1)
		if NatText(NatFind(aN[6], cT1), "kind") != "pattern"
			aU[11] + NatRunOf(aN, cT1, cQ1)
			return aU
		ok
		aRun = NatRunPattern(aN, cT1, cQ1)
		if not aRun[1] return NatRefuse(aN, cTongue, "surface", cQ1) ok
		aAns = aRun[2]
		if len(aAns) > 1 return NatRefuse(aN, cTongue, "ambiguous", NatJoinNames(aAns)) ok
		aU[7] = aAns
		aU[8] = 1
		aU[9] = NatTell(aN, cTongue, aF, aAns, aU[3])
		if len(aAns) = 1 and len(aSn) > 1
			aS2 = NatFind(aN[7], aSn[2])
			aSl = aU[3]
			if NatText(aS1, "binds") != "" NatSetSlot(aSl, NatText(aS1, "binds"), aAns[1]) ok
			aU[10] = NatFill(aN, NatText(aS2, "query"), aSl, NatText(aS2, "target"))
			if NatText(NatFind(aN[6], NatText(aS2, "target")), "kind") != "pattern"
				aU[11] + NatRunOf(aN, NatText(aS2, "target"), aU[10])
			ok
		ok
		return aU
	ok
	if NatText(NatFind(aN[6], aU[4]), "kind") = "pattern"
		aRun = NatRunPattern(aN, aU[4], aU[5])
		if not aRun[1] return NatRefuse(aN, cTongue, "surface", aU[5]) ok
		aU[7] = aRun[2]
		aU[8] = 1
		aU[9] = NatTell(aN, cTongue, aF, aRun[2], aU[3])
	else
		aU[11] + NatRunOf(aN, aU[4], aU[5])
	ok
	return aU

# ---- the answers, as JSON ---------------------------------------------------------------------------------------

func NatJsonRefusal(aR)
	return '{"refused": {"kind": ' + NatQ(aR[2]) + ', "code": ' + NatQ("N_" + upper(aR[2])) + ', "what": ' + NatQ(aR[3]) +
	       ', "tongue": ' + NatQ(aR[5]) + ', "message": ' + NatQ(aR[4]) + '}}'

func NatJsonResult(aR)
	if aR[1] = "refused" return NatJsonRefusal(aR) ok
	cOut = '{"frame": ' + NatQ(aR[2]) + ', "surface": ' + NatQ(aR[4])
	if aR[4] != "plan" cOut += ', "query": ' + NatQ(aR[5]) ok
	cOut += ', "slots": {'
	for i = 1 to len(aR[3])
		if i > 1 cOut += ", " ok
		cOut += NatQ(aR[3][i][1]) + ": " + NatQ(aR[3][i][2])
	next
	cOut += "}"
	if len(aR[6]) > 0
		cOut += ', "steps": ['
		for i = 1 to len(aR[6])
			if i > 1 cOut += ", " ok
			cOut += '{"surface": ' + NatQ(aR[6][i][1]) + ', "query": ' + NatQ(aR[6][i][2])
			if aR[6][i][3] != "" cOut += ', "binds": ' + NatQ(aR[6][i][3]) ok
			cOut += "}"
		next
		cOut += "]"
	ok
	if aR[8] cOut += ', "answer": ' + NatQList(aR[7]) ok
	if aR[9] != "" cOut += ', "told": ' + NatQ(aR[9]) ok
	if aR[10] != "" cOut += ', "query2": ' + NatQ(aR[10]) ok
	if len(aR[11]) > 0
		cOut += ', "run": ['
		for i = 1 to len(aR[11])
			if i > 1 cOut += ", " ok
			cOut += '{"surface": ' + NatQ(aR[11][i][1]) + ', "court": ' + NatQ(aR[11][i][2]) + ', "world": ' + NatQ(aR[11][i][3]) + ', "query": ' + NatQ(aR[11][i][4]) + "}"
		next
		cOut += "]"
	ok
	return cOut + "}"

func NatJsonTokens(aN, cTongue, cText)
	aTk = NatTokens(aN, cTongue, cText)
	if aTk[1] = "refused" return NatJsonRefusal(NatRefuse(aN, cTongue, aTk[2], aTk[3])) ok
	cOut = '{"tongue": ' + NatQ(cTongue) + ', "tokens": ['
	for i = 1 to len(aTk[2])
		if i > 1 cOut += ", " ok
		cOut += '{"meaning": ' + NatQ(aTk[2][i][1]) + ', "word": ' + NatQ(aTk[2][i][3])
		if aTk[2][i][2] != "" cOut += ', "slot": ' + NatQ(aTk[2][i][2]) ok
		cOut += "}"
	next
	return cOut + '], "ignored": ' + NatQList(aTk[3]) + "}"

func NatJsonVocabulary(aN, cTongue)
	aLex = NatLexicon(aN, cTongue)
	cOut = '{"tongue": ' + NatQ(cTongue) + ', "ignored": ' + NatQList(aLex[1]) + ', "words": ['
	for i = 1 to len(aLex[2])
		if i > 1 cOut += ", " ok
		cOut += '{"word": ' + NatQ(aLex[2][i][1]) + ', "meaning": ' + NatQ(aLex[2][i][2])
		if aLex[2][i][3] != "" cOut += ', "entity": ' + NatQ(aLex[2][i][3]) ok
		cOut += "}"
	next
	cOut += '], "uncovered": ['
	nSeen = 0
	aM = aN[4]
	for i = 1 to len(aM)
		if NatText(aM[i], "slot") = "none" and not NatHasKey(NatPairs(aM[i], "words"), cTongue)
			if nSeen > 0 cOut += ", " ok
			cOut += NatQ(aM[i][2])
			nSeen++
		ok
	next
	cOut += '], "clashes": ['
	for i = 1 to len(aLex[3])
		if i > 1 cOut += ", " ok
		cOut += '{"word": ' + NatQ(aLex[3][i][1]) + ', "meanings": ' + NatQList([aLex[3][i][2], aLex[3][i][3]]) + "}"
	next
	return cOut + "]}"

# the sentence's own conformance, counted
func NatJsonExamples(aN)
	nTexts = 0
	nUnderstood = 0
	nFailed = 0
	nDiverging = 0
	aEx = aN[9]
	for i = 1 to len(aEx)
		cMeans = NatText(aEx[i], "means")
		aP = NatPairs(aEx[i], "asking")
		aQ = []
		for j = 1 to len(aP)
			if isNull(NatFind(aN[3], aP[j][1])) loop ok
			nTexts++
			aU = NatUnderstand(aN, aP[j][1], aP[j][2])
			if aU[1] = "ok" and aU[2] = cMeans
				nUnderstood++
				if not CtInList(aU[4] + " " + aU[5] + NatStepsText(aU[6]), aQ) aQ + (aU[4] + " " + aU[5] + NatStepsText(aU[6])) ok
			else
				nFailed++
			ok
		next
		if len(aQ) > 1 nDiverging++ ok
	next
	nCTexts = 0
	nRefused = 0
	nCFailed = 0
	aCe = aN[10]
	for i = 1 to len(aCe)
		cWant = NatText(aCe[i], "refused")
		aP = NatPairs(aCe[i], "asking")
		for j = 1 to len(aP)
			if isNull(NatFind(aN[3], aP[j][1])) loop ok
			nCTexts++
			aU = NatUnderstand(aN, aP[j][1], aP[j][2])
			if aU[1] = "refused" and aU[2] = cWant
				nRefused++
			else
				nCFailed++
			ok
		next
	next
	return '{"examples": {"declared": ' + len(aEx) + ', "texts": ' + nTexts + ', "understood": ' + nUnderstood + ', "failed": ' + nFailed +
	       ', "diverging": ' + nDiverging + '}, "counterexamples": {"declared": ' + len(aCe) + ', "texts": ' + nCTexts +
	       ', "refused": ' + nRefused + ', "failed": ' + nCFailed + "}}"

# a plan's queries as one text: two tongues compile to the SAME plan when this is the same
func NatStepsText(aSteps)
	cOut = ""
	for i = 1 to len(aSteps)
		cOut += " => " + aSteps[i][1] + " " + aSteps[i][2]
	next
	return cOut

# ---- the rules of v17/GRAMMAR.md section 4b ---------------------------------------------------------------------

# the safe set of punctuation: a tongue may allow a subset of it, never more
func NatSafeSet()
	return "-'?,."

func NatAdd(aF, cCode, nLine, cMsg)
	aF + [cCode, nLine, cMsg]

# the sample a surface is asked about: a number is 1, an entity is Sample, a slot nobody declared stays
func NatSampleFill(aN, cTemplate)
	cOut = cTemplate
	aPh = NatPlaceholders(cTemplate)
	for i = 1 to len(aPh)
		aM = NatFind(aN[4], aPh[i])
		if not isNull(aM)
			cSv = "x"
			if NatText(aM, "slot") = "number" cSv = "1" ok
			if NatText(aM, "slot") = "entity" cSv = "Sample" ok
			cOut = CtReplace(cOut, "{" + aPh[i] + "}", cSv)
		ok
	next
	return cOut

# a temporary file beside the user's own temporary folder
func NatTempFile()
	cDir = sysget("TEMP")
	if cDir = "" cDir = "." ok
	return cDir + "/nat_" + clock() + "_" + random(99999) + ".txt"

func NatQuote(cS)
	return char(34) + cS + char(34)

# [ok?, why]: a surface judges a query of its grammar WITHOUT data. `triples` is three terms, judged here; a
# surface whose COURT is a court file is asked as the Q letter's court is -- its own `ask` over no rows answers
# [] for a lawful question and refuses the rest -- and only when the check was asked to reach the surfaces
func NatSurfaceCheck(aN, aSf, cQuery)
	if NatText(aSf, "grammar") = "triples"
		if len(NatWords(cQuery)) = 3 return [1, ""] ok
		return [0, "a triple pattern is three terms"]
	ok
	if not $bNSurfaces return [1, ""] ok
	aCw = NatWords(NatText(aSf, "court"))
	if len(aCw) < 2 return [1, ""] ok
	if right(aCw[1], 5) != ".ring" return [1, ""] ok
	if NatText(aSf, "world") = "" return [1, ""] ok
	cCourt = aCw[1]
	cDir = CtDirOf(sysargv[2])
	if cDir != "" cCourt = cDir + "/" + cCourt ok
	cVerbs = ""
	for i = 2 to len(aCw)
		if i > 2 cVerbs += " " ok
		cVerbs += aCw[i]
	next
	cTmp = NatTempFile()
	# the surface's answer is what it writes to its stdout; what a runtime says of itself on stderr is not an answer
	cNoErr = " 2>/dev/null"
	if isWindows() cNoErr = " 2>NUL" ok
	cInner = NatQuote(exefilename()) + " " + NatQuote(cCourt) + " " + cVerbs + " " + NatQuote(NatPath(NatText(aSf, "world"))) + " " + NatQuote(cQuery) + " [] > " + NatQuote(cTmp) + cNoErr
	system(NatQuote(cInner))
	cOut = ""
	if fexists(cTmp)
		cOut = NatTrim(read(cTmp))
		remove(cTmp)
	ok
	if left(cOut, 1) = "[" return [1, ""] ok
	nNl = substr(cOut, char(10))
	if nNl > 0 cOut = left(cOut, nNl - 1) ok
	return [0, left(cOut, 200)]

func NatRules(aN)
	aF = []
	aMeanings = aN[4]
	aFrames = aN[8]
	aTongues = aN[3]
	# a surface whose world is not there cannot be judged
	aSurf = aN[6]
	for i = 1 to len(aSurf)
		if NatText(aSurf[i], "world") != ""
			bRead = 0
			for j = 1 to len(aN[2])
				if aN[2][j][1] = aSurf[i][2] bRead = aN[2][j][3] ok
			next
			if not bRead
				NatAdd(aF, "N_WORLD_UNREAD", aSurf[i][3], "SURFACE " + aSurf[i][2] + " reads the world '" + NatText(aSurf[i], "world") + "', which cannot be read from the sentence's folder")
			ok
		ok
	next
	for i = 1 to len(aFrames)
		aFr = aFrames[i]
		aShape = NatNames(aFr, "shape")
		aSlots = []
		for j = 1 to len(aShape)
			aM = NatFind(aMeanings, aShape[j])
			if not isNull(aM)
				cSl = NatText(aM, "slot")
				if cSl = "number" or cSl = "entity" aSlots + aShape[j] ok
			ok
		next
		for j = 1 to len(aSlots)
			nTimes = 0
			for k = 1 to len(aSlots)
				if aSlots[k] = aSlots[j] nTimes++ ok
			next
			if nTimes > 1
				NatAdd(aF, "N_SLOT_REPEATED", aFr[3], "FRAME " + aFr[2] + " names a slot meaning twice in its SHAPE: '" + aSlots[j] + "'")
				exit
			ok
		next
		bHasQ = NatHas(aFr, "target") and NatHas(aFr, "query")
		bHasS = NatHas(aFr, "steps")
		if bHasQ = bHasS
			NatAdd(aF, "N_FRAME_TARGET", aFr[3], "FRAME " + aFr[2] + " must have either a TARGET and a QUERY or STEPS, and not both nor neither")
		ok
		aAvail = []
		for j = 1 to len(aSlots)
			aAvail + aSlots[j]
		next
		if bHasS
			aSn = NatNames(aFr, "steps")
			for j = 1 to len(aSn)
				aSt = NatFind(aN[7], aSn[j])
				if isNull(aSt) loop ok
				aPh = NatPlaceholders(NatText(aSt, "query"))
				for k = 1 to len(aPh)
					if not CtInList(aPh[k], aAvail)
						NatAdd(aF, "N_SLOT_UNKNOWN", aSt[3], "STEP " + aSt[2] + " uses {" + aPh[k] + "}, which is neither a slot of FRAME " + aFr[2] + "'s SHAPE nor bound by an earlier step")
					ok
				next
				if NatText(aSt, "binds") != "" aAvail + NatText(aSt, "binds") ok
			next
		but bHasQ
			aPh = NatPlaceholders(NatText(aFr, "query"))
			for k = 1 to len(aPh)
				if not CtInList(aPh[k], aAvail)
					NatAdd(aF, "N_SLOT_UNKNOWN", aFr[3], "FRAME " + aFr[2] + " QUERY uses {" + aPh[k] + "}, which is not a slot of its SHAPE")
				ok
			next
		ok
		for nKey = 1 to 2
			cKey = "answers"
			if nKey = 2 cKey = "empty" ok
			aP = NatPairs(aFr, cKey)
			for j = 1 to len(aP)
				aPh = NatPlaceholders(aP[j][2])
				for k = 1 to len(aPh)
					if not CtInList(aPh[k], aSlots) and not (aPh[k] = "answer" and cKey = "answers") and not CtInList(aPh[k], aAvail)
						NatAdd(aF, "N_SLOT_UNKNOWN", aFr[3], "FRAME " + aFr[2] + " " + upper(cKey) + " in " + aP[j][1] + " uses {" + aPh[k] + "}, which is not a slot of its SHAPE")
					ok
				next
			next
		next
		# the query is judged by its surface, here, without data
		aTargets = []
		if bHasQ
			aTargets + [NatText(aFr, "target"), NatText(aFr, "query")]
		else
			aSn = NatNames(aFr, "steps")
			for j = 1 to len(aSn)
				aSt = NatFind(aN[7], aSn[j])
				if not isNull(aSt) aTargets + [NatText(aSt, "target"), NatText(aSt, "query")] ok
			next
		ok
		for j = 1 to len(aTargets)
			aSf = NatFind(aN[6], aTargets[j][1])
			if isNull(aSf) or aTargets[j][2] = "" loop ok
			aVd = NatSurfaceCheck(aN, aSf, NatSampleFill(aN, aTargets[j][2]))
			if not aVd[1]
				NatAdd(aF, "N_QUERY_REFUSED", aFr[3], "FRAME " + aFr[2] + ": the surface '" + aTargets[j][1] + "' refuses the query '" + aTargets[j][2] + "': " + aVd[2])
			ok
		next
		# every tongue can tell the answer: by the frame's template, or by the surface's own voice
		cTgt = NatText(aFr, "target")
		if cTgt = "" and bHasS
			aSn = NatNames(aFr, "steps")
			if len(aSn) > 0
				aLast = NatFind(aN[7], aSn[len(aSn)])
				if not isNull(aLast) cTgt = NatText(aLast, "target") ok
			ok
		ok
		aTells = []
		aSfT = NatFind(aN[6], cTgt)
		if not isNull(aSfT) aTells = NatNames(aSfT, "tells") ok
		aAnsP = NatPairs(aFr, "answers")
		aEmpP = NatPairs(aFr, "empty")
		for j = 1 to len(aTongues)
			cTn = aTongues[j][2]
			bHave = NatHasKey(aAnsP, cTn)
			bEmpty = NatHasKey(aEmpP, cTn)
			if bHave and not bEmpty
				NatAdd(aF, "N_TELL_UNCOVERED", aFr[3], "FRAME " + aFr[2] + " has ANSWERS in " + cTn + " but no EMPTY: an answer may be nobody")
			ok
			if bHasS
				if not bHave
					NatAdd(aF, "N_TELL_UNCOVERED", aFr[3], "FRAME " + aFr[2] + " has no ANSWERS in " + cTn + " for its first step")
				ok
				if not CtInList(cTn, aTells)
					NatAdd(aF, "N_TELL_UNCOVERED", aFr[3], "FRAME " + aFr[2] + " cannot tell its last step in " + cTn + ": the surface '" + cTgt + "' does not tell in " + cTn)
				ok
			but not bHave and not CtInList(cTn, aTells)
				NatAdd(aF, "N_TELL_UNCOVERED", aFr[3], "FRAME " + aFr[2] + " cannot be told in " + cTn + ": no ANSWERS in " + cTn + " and the surface '" + cTgt + "' does not tell in " + cTn)
			ok
		next
	next
	aKinds = ["character", "word", "shape", "ambiguous", "surface"]
	for i = 1 to len(aTongues)
		aT = aTongues[i]
		aRp = NatPairs(aT, "refuses")
		aMiss = []
		for j = 1 to len(aKinds)
			if not NatHasKey(aRp, aKinds[j]) aMiss + aKinds[j] ok
		next
		if len(aMiss) > 0
			NatAdd(aF, "N_REFUSAL_UNCOVERED", aT[3], "TONGUE " + aT[2] + " does not say how it refuses: " + CtJoin(aMiss, ", "))
		ok
		cAllows = NatText(aT, "allows")
		for j = 1 to len(cAllows)
			if substr(NatSafeSet(), cAllows[j]) = 0
				NatAdd(aF, "N_GATE_WIDENED", aT[3], "TONGUE " + aT[2] + " ALLOWS '" + cAllows[j] + "', outside the court's safe set " + NatSafeSet() + ": a tongue cannot widen the gate")
				exit
			ok
		next
		aLex = NatLexicon(aN, aT[2])
		for j = 1 to len(aLex[3])
			NatAdd(aF, "N_WORD_AMBIGUOUS", aT[3], "in " + aT[2] + " the word '" + aLex[3][j][1] + "' means both " + aLex[3][j][2] + " and " + aLex[3][j][3])
		next
		aShown = []
		for j = 1 to len(aLex[1])
			for k = 1 to len(aLex[2])
				if aLex[2][k][1] = aLex[1][j] and not CtInList(aLex[1][j], aShown)
					aShown + aLex[1][j]
					NatAdd(aF, "N_WORD_IGNORED", aT[3], "in " + aT[2] + " the word '" + aLex[1][j] + "' is both ignored and a word of " + aLex[2][k][2])
				ok
			next
		next
	next
	for i = 1 to len(aMeanings)
		aM = aMeanings[i]
		cSl = NatText(aM, "slot")
		if cSl = "none"
			aWp = NatPairs(aM, "words")
			for j = 1 to len(aTongues)
				if not NatHasKey(aWp, aTongues[j][2])
					NatAdd(aF, "N_TONGUE_UNCOVERED", aM[3], "MEANING " + aM[2] + " has no words in " + aTongues[j][2])
				ok
			next
		ok
		if cSl = "entity"
			aSf = NatFind(aN[6], NatText(aM, "from"))
			if NatText(aM, "of") = "" or NatText(aM, "from") = ""
				NatAdd(aF, "N_ENTITY_UNKNOWN", aM[3], "MEANING " + aM[2] + " is an entity and needs both OF and FROM")
			but not isNull(aSf) and not CtInList(NatText(aM, "of"), NatNames(aSf, "entities"))
				NatAdd(aF, "N_ENTITY_UNKNOWN", aM[3], "MEANING " + aM[2] + " is of '" + NatText(aM, "of") + "', which the surface '" + NatText(aM, "from") + "' does not enumerate")
			ok
		ok
	next
	aEx = aN[9]
	for i = 1 to len(aEx)
		cMeans = NatText(aEx[i], "means")
		if isNull(NatFind(aFrames, cMeans)) loop ok
		aP = NatPairs(aEx[i], "asking")
		aGot = []
		for j = 1 to len(aP)
			if isNull(NatFind(aTongues, aP[j][1])) loop ok
			aU = NatUnderstand(aN, aP[j][1], aP[j][2])
			if aU[1] = "ok" and aU[2] = cMeans
				cShape = aU[4] + " " + aU[5] + NatStepsText(aU[6])
				if not CtInList(cShape, aGot) aGot + cShape ok
			else
				cWas = "refused as " + aU[2]
				if aU[1] = "ok" cWas = "understood as " + aU[2] ok
				NatAdd(aF, "N_EXAMPLE_FAILED", aEx[i][3], "EXAMPLE " + aEx[i][2] + " in " + aP[j][1] + " ('" + aP[j][2] + "') is " + cWas + ", not as " + cMeans)
			ok
		next
		if len(aGot) > 1
			NatAdd(aF, "N_EXAMPLE_DIVERGES", aEx[i][3], "EXAMPLE " + aEx[i][2] + " compiles to different queries in different tongues: " + CtJoin(aGot, " | "))
		ok
	next
	aCe = aN[10]
	for i = 1 to len(aCe)
		cWant = NatText(aCe[i], "refused")
		aP = NatPairs(aCe[i], "asking")
		for j = 1 to len(aP)
			if isNull(NatFind(aTongues, aP[j][1])) loop ok
			aU = NatUnderstand(aN, aP[j][1], aP[j][2])
			if not (aU[1] = "refused" and aU[2] = cWant)
				cWas = "refused as " + aU[2]
				if aU[1] = "ok" cWas = "understood as " + aU[2] ok
				NatAdd(aF, "N_COUNTEREXAMPLE_FAILED", aCe[i][3], "COUNTEREXAMPLE " + aCe[i][2] + " in " + aP[j][1] + " ('" + aP[j][2] + "') was " + cWas + ", not refused as " + cWant)
			ok
		next
	next
	return NatSort(aF)

# findings [code, line, message], by line and then by code, stable
func NatSort(aF)
	aOut = []
	for i = 1 to len(aF)
		nAt = len(aOut) + 1
		for j = len(aOut) to 1 step -1
			if aOut[j][2] > aF[i][2] or (aOut[j][2] = aF[i][2] and NatLess(aF[i][1], aOut[j][1]))
				nAt = j
			else
				exit
			ok
		next
		insert(aOut, nAt - 1, aF[i])
	next
	return aOut

# the court's own refusal path: each finding is a refusal with its code and its cite; `check` raises the first,
# `diagnose` notes them all
func NatCheckRules(aDecls)
	aN = NatBuild(aDecls)
	aF = NatRules(aN)
	for i = 1 to len(aF)
		try
			CtFailC(aF[i][2], aF[i][1], ["rule:" + lower(aF[i][1])], aF[i][3])
		catch
			CtNote(cCatchError)
		done
	next

# ---- the verbs ------------------------------------------------------------------------------------------------------

func NatMain(cVerb)
	nNeed = 6
	if cVerb = "vocabulary" nNeed = 5 ok
	if cVerb = "examples" nNeed = 4 ok
	if len(sysargv) < nNeed
		cUse = "usage: <court>.ring " + cVerb + " <file" + $cCourtExt + ">"
		if nNeed >= 5 cUse += " <tongue>" ok
		if nNeed = 6 cUse += " <text>" ok
		? cUse
		return
	ok
	try
		aDecls = CtDeclare(read(sysargv[4]))
		aN = NatBuild(aDecls)
		if cVerb = "examples"
			? NatJsonExamples(aN)
		else
			cTongue = sysargv[5]
			if isNull(NatFind(aN[3], cTongue)) CtFail(1, "the sentence declares no tongue '" + cTongue + "'") ok
			if cVerb = "vocabulary"
				? NatJsonVocabulary(aN, cTongue)
			but cVerb = "tokens"
				? NatJsonTokens(aN, cTongue, sysargv[6])
			but cVerb = "understand"
				? NatJsonResult(NatUnderstand(aN, cTongue, sysargv[6]))
			else
				? NatJsonResult(NatAsk(aN, cTongue, sysargv[6]))
			ok
		ok
	catch
		? cCatchError
	done
