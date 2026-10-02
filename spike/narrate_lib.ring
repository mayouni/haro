# narrate_lib.ring -- NARRATE: the court's voice (Haro v0.13), in pure core Ring.
#
# A court FORGED from a .haro declaration that holds a NARRATE loads this file
# beside court_lib.ring and carries the voice as
#   $aCourtNarrate = [name, opens, ends, refuses, [[kind, template], ...]]
# `narrate <file>` answers a sentence back in that voice: the opening, one
# sentence per declaration in file order, the ending -- or, when the court
# stops, the one refusal line with the line, the message and the code the
# envelope of v0.11 gives the same verdict.
#
# Two laws of the estate keep it honest (stz CLAUDE.md, stzn v0):
#   the StzNarration law -- a narration is a RENDERING of a real run, never
#   stored, the plain-text sentence being the document: this court prints to
#   stdout, writes no file, and has no verb that reads a narration back;
#   stzn's honesty guard -- a narration never alters a value it shows: a
#   placeholder is filled with the sentence's own text, verbatim, never
#   uppercased, trimmed or rephrased.
#
# A placeholder is {name}, {verb}, {rationale}, {line} or a seat of the kind
# (the meta-court refused any other at declaration). A seat the sentence left
# out fills as nothing; a list seat fills as its items joined by ", ", a pair
# list as key -> value joined by ", ". A kind the voice does not speak is
# narrated plainly: its verb, its name and the author's own reason -- the
# rationale is mandatory on every declaration (C6 3.8), so a narration never
# drops it.
#
# Functions only; the globals are the generated court's.

func NarBaseName(cPath)
	nCut = 0
	for i = 1 to len(cPath)
		if cPath[i] = "/" or ascii(cPath[i]) = 92 nCut = i ok
	next
	return substr(cPath, nCut + 1)

# a seat's value as text, verbatim
func NarSeatText(aDecl, cSeat)
	aC = aDecl[4]
	for i = 1 to len(aC)
		if lower(aC[i][1]) = cSeat
			aV = aC[i][3]
			cK = aV[1]
			if cK = "word" or cK = "string" or cK = "number" return aV[2] ok
			cOut = ""
			if cK = "pairlist"
				for j = 1 to len(aV[2])
					if j > 1 cOut += ", " ok
					cOut += aV[2][j][1] + " -> " + aV[2][j][2]
				next
				return cOut
			ok
			for j = 1 to len(aV[2])
				if j > 1 cOut += ", " ok
				cOut += aV[2][j]
			next
			return cOut
		ok
	next
	return ""

# fill a template: aVals is [[key, text], ...]; an unknown key fills as nothing
func NarFill(cT, aVals)
	cOut = ""
	n = len(cT)
	i = 1
	while i <= n
		c = cT[i]
		if c = "{"
			j = i + 1
			cW = ""
			while j <= n and cT[j] != "}"
				cW += cT[j]
				j++
			end
			for k = 1 to len(aVals)
				if aVals[k][1] = cW cOut += aVals[k][2] ok
			next
			i = j
		else
			cOut += c
		ok
		i++
	end
	return cOut

func NarSays(cKind)
	aS = $aCourtNarrate[5]
	for i = 1 to len(aS)
		if aS[i][1] = cKind return aS[i][2] ok
	next
	return ""

func NarrateRun(cFile)
	cSrc = read(cFile)
	CtSetCode("PARSE", [])
	cErr = ""
	aDecls = NULL
	try
		aDecls = CtDeclare(cSrc)
	catch
		cErr = cCatchError
	done
	cBase = NarBaseName(cFile)
	if cErr != ""
		cRefuses = $aCourtNarrate[4]
		if cRefuses = "" cRefuses = "I stopped at line {line}: {message}" ok
		cCites = ""
		for i = 1 to len($aCourtCites)
			if i > 1 cCites += ", " ok
			cCites += $aCourtCites[i]
		next
		? NarFill(cRefuses, [["language", $cCourtLang], ["file", cBase], ["line", "" + CtLineOf(cErr)], ["code", $cCourtCode], ["message", CtStripPrefix(cErr)], ["cites", cCites]])
		return
	ok
	cOpens = $aCourtNarrate[2]
	if cOpens = "" cOpens = "{file} is a sentence of {language}, {count} declarations." ok
	cEnds = $aCourtNarrate[3]
	if cEnds = "" cEnds = "That is all of it." ok
	aTop = [["language", $cCourtLang], ["file", cBase], ["count", "" + len(aDecls)]]
	? NarFill(cOpens, aTop)
	for i = 1 to len(aDecls)
		aD = aDecls[i]
		aKind = CtKindByVerb(aD[1])
		cT = ""
		if not isNull(aKind) cT = NarSays(aKind[2]) ok
		if cT = ""
			? lower(aD[1]) + " " + aD[2] + ": " + aD[5]
		else
			aVals = [["name", aD[2]], ["verb", aD[1]], ["rationale", aD[5]], ["line", "" + aD[3]]]
			if not isNull(aKind)
				for j = 1 to len(aKind[3])
					aVals + [aKind[3][j][1], NarSeatText(aD, aKind[3][j][1])]
				next
			ok
			? NarFill(cT, aVals)
		ok
	next
	? NarFill(cEnds, aTop)
