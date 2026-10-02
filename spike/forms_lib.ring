# forms_lib.ring -- FORMS: a vocabulary's function-name grammar as data
# (Haro v0.12, principle 7 of haro/PRINCIPLES.md), in pure core Ring.
#
# A court FORGED from a .haro declaration that holds a FORMS loads this file
# beside court_lib.ring and carries the FORMS as
#   $aCourtFormset = [name, fluent, passive, statement, [[key, suffix], ...],
#                     [kind, base seat, forms seat]]
# The grammar is the forms document's (stzlib base/doc/narrations/
# stz-functions-as-linguistic-expressions.md) under the rule principle 7
# ruled (H-7): a name is a BASE (CamelCase words, never judged here) followed
# by parameter SUFFIXES, each spelt once, then the FLUENT form, then the
# STATEMENT form -- `RemoveManyCS`, `FindNextSTCS`, `ReplaceAllCSQ`,
# `AllNumbersInQX`. Suffix order is parameter order and is free (point 3);
# a suffix twice, the fluent form not last, or a trailing run of capitals no
# suffix spells is a disagreement (point 7, the FF clash); a fluent name
# requires its plain twin in the same list (point 2); a name whose base is a
# declared FAMILY's must be one of the members that family generates (point
# 6). The PASSIVE inflection is applied only when a family is GENERATED
# (Replace -> Replaced, Spacify -> Spacified): no dictionary can invert it,
# so a name is never read as passive.
#
#   <court>.ring family <file>               every FAMILY's members, generated
#   <court>.ring spellings <file> <names>    one verdict per name, then a summary
#
# Functions only; the globals are the generated court's.

func FormsFail(nLine, cMsg)
	CtFailC(nLine, "FORMS", ["rule:forms"], cMsg)

func FormsKindByName(cName)
	for i = 1 to len($aCourtKinds)
		if $aCourtKinds[i][2] = cName return $aCourtKinds[i] ok
	next
	return NULL

func FormsIsUpper(c)
	return ascii(c) >= 65 and ascii(c) <= 90

func FormsIsVowel(c)
	return InStrListCs(lower(c), ["a", "e", "i", "o", "u"])

func InStrListCs(cS, aL)
	for i = 1 to len(aL)
		if aL[i] = cS return 1 ok
	next
	return 0

func FormsEndsWith(cS, cSuf)
	if len(cSuf) = 0 return 0 ok
	if len(cS) < len(cSuf) return 0 ok
	return right(cS, len(cSuf)) = cSuf

func FormsSuffixOf(cKey)
	aP = $aCourtFormset[5]
	for i = 1 to len(aP)
		if aP[i][1] = cKey return aP[i][2] ok
	next
	return ""

# the words a FAMILY may offer: every PARAMS key, and fluent / passive when declared
func FormsOffered()
	aOut = []
	aF = $aCourtFormset
	for i = 1 to len(aF[5])
		aOut + aF[5][i][1]
	next
	if aF[2] != "" aOut + "fluent" ok
	if aF[3] != "" aOut + "passive" ok
	return aOut

# the FAMILY declarations of a sentence, as [name, base, offered words, line]
func FormsFamilies(aDecls)
	aOut = []
	aF = $aCourtFormset
	if len(aF) < 6 return aOut ok
	if len(aF[6]) < 3 return aOut ok
	aKind = FormsKindByName(aF[6][1])
	if isNull(aKind) return aOut ok
	for i = 1 to len(aDecls)
		aD = aDecls[i]
		if aD[1] != aKind[1] loop ok
		cBase = ""
		aWords = []
		aC = aD[4]
		for j = 1 to len(aC)
			if lower(aC[j][1]) = aF[6][2] and (aC[j][3][1] = "string" or aC[j][3][1] = "word") cBase = aC[j][3][2] ok
			if lower(aC[j][1]) = aF[6][3] and aC[j][3][1] = "namelist" aWords = aC[j][3][2] ok
		next
		aOut + [aD[2], cBase, aWords, aD[3]]
	next
	return aOut

# at check: a family offers only forms the FORMS declares, each once
func FormsCheck(aDecls)
	aFam = FormsFamilies(aDecls)
	aOffered = FormsOffered()
	for i = 1 to len(aFam)
		aSeen = []
		for j = 1 to len(aFam[i][3])
			cW = aFam[i][3][j]
			if not InStrListCs(cW, aOffered)
				FormsFail(aFam[i][4], "FAMILY " + aFam[i][1] + " offers '" + cW + "', which the FORMS " + $aCourtFormset[1] + " declares no form for: it declares " + CtJoin(aOffered, ", "))
			ok
			if InStrListCs(cW, aSeen)
				FormsFail(aFam[i][4], "FAMILY " + aFam[i][1] + " offers '" + cW + "' twice")
			ok
			aSeen + cW
		next
		if aFam[i][2] = ""
			FormsFail(aFam[i][4], "FAMILY " + aFam[i][1] + " has no base verb")
		ok
	next

# the passive inflection of a base verb: Replace -> Replaced, Spacify -> Spacified, Find -> Finded
func FormsPassive(cBase)
	cInf = $aCourtFormset[3]
	if cInf != "ed" return cBase + cInf ok
	n = len(cBase)
	if n = 0 return cBase ok
	cLast = cBase[n]
	if cLast = "e" return cBase + "d" ok
	if cLast = "y" and n >= 2
		if not FormsIsVowel(cBase[n - 1]) return left(cBase, n - 1) + "ied" ok
	ok
	return cBase + "ed"

# every member a family generates: each subset of its parameter forms, in the
# order offered, as the plain name, then the fluent name, then the passive name
func FormsMembers(cBase, aWords)
	aKeys = []
	bFluent = 0
	bPassive = 0
	for i = 1 to len(aWords)
		if aWords[i] = "fluent"
			bFluent = 1
		but aWords[i] = "passive"
			bPassive = 1
		else
			aKeys + aWords[i]
		ok
	next
	nCombos = 1
	for i = 1 to len(aKeys)
		nCombos = nCombos * 2
	next
	aOut = []
	for m = 0 to nCombos - 1
		cSuf = ""
		v = m
		for i = 1 to len(aKeys)
			if v % 2 = 1 cSuf += FormsSuffixOf(aKeys[i]) ok
			v = floor(v / 2)
		next
		aOut + (cBase + cSuf)
		if bFluent aOut + (cBase + cSuf + $aCourtFormset[2]) ok
		if bPassive aOut + (FormsPassive(cBase) + cSuf) ok
	next
	return aOut

func FormsPrintFamilies(aDecls)
	aFam = FormsFamilies(aDecls)
	for i = 1 to len(aFam)
		aM = FormsMembers(aFam[i][2], aFam[i][3])
		? "family " + aFam[i][1] + ": " + aFam[i][2] + " offering [" + CtJoin(aFam[i][3], ", ") + "], " + len(aM) + " members"
		for j = 1 to len(aM)
			? "  " + aM[j]
		next
	next
	if len(aFam) = 0 ? "no family declared" ok

# a name split under the FORMS: [base, keys, fluent, statement, why]; why "" when it parses
func FormsSplit(cName)
	aF = $aCourtFormset
	cRest = cName
	bStmt = 0
	if FormsEndsWith(cRest, aF[4])
		cRest = left(cRest, len(cRest) - len(aF[4]))
		bStmt = 1
	ok
	bFluent = 0
	if FormsEndsWith(cRest, aF[2])
		cRest = left(cRest, len(cRest) - len(aF[2]))
		bFluent = 1
	ok
	aKeys = []
	while 1
		cBest = ""
		cBestKey = ""
		for i = 1 to len(aF[5])
			cSuf = aF[5][i][2]
			if FormsEndsWith(cRest, cSuf) and len(cSuf) > len(cBest)
				cBest = cSuf
				cBestKey = aF[5][i][1]
			ok
		next
		if cBest = "" exit ok
		if InStrListCs(cBestKey, aKeys)
			return [cRest, aKeys, bFluent, bStmt, "the suffix " + cBest + " appears twice"]
		ok
		cRest = left(cRest, len(cRest) - len(cBest))
		insert(aKeys, 0, cBestKey)
		if len(cRest) = 0
			return [cRest, aKeys, bFluent, bStmt, "nothing is left of the name but suffixes"]
		ok
	end
	if FormsEndsWith(cRest, aF[2])
		return [cRest, aKeys, bFluent, bStmt, "the fluent form " + aF[2] + " is not last"]
	ok
	if FormsEndsWith(cRest, aF[4])
		return [cRest, aKeys, bFluent, bStmt, "the statement form " + aF[4] + " is not outermost"]
	ok
	n = len(cRest)
	i = n
	while i >= 1
		if not FormsIsUpper(cRest[i]) exit ok
		i--
	end
	if i < n and i >= 1
		cRun = substr(cRest, i + 1)
		if len(cRun) >= 2
			return [cRest, aKeys, bFluent, bStmt, "ends in '" + cRun + "', which no declared suffix spells"]
		ok
	ok
	return [cRest, aKeys, bFluent, bStmt, ""]

# the plain twin of a fluent name: the name with the fluent form removed
func FormsPlainTwin(aSplit)
	cOut = aSplit[1]
	for i = 1 to len(aSplit[2])
		cOut += FormsSuffixOf(aSplit[2][i])
	next
	if aSplit[4] cOut += $aCourtFormset[4] ok
	return cOut

func FormsReadNames(cPath)
	if not fexists(cPath) CtFail(1, "no names file at '" + cPath + "'") ok
	cText = read(cPath)
	aOut = []
	cL = ""
	for i = 1 to len(cText)
		c = cText[i]
		if c = char(10)
			FormsTakeName(aOut, cL)
			cL = ""
		else
			cL += c
		ok
	next
	FormsTakeName(aOut, cL)
	return aOut

func FormsTakeName(aOut, cRaw)
	cL = FormsTrim(cRaw)
	if len(cL) = 0 return ok
	if cL[1] = "#" return ok
	aOut + cL

func FormsTrim(cS)
	i = 1
	n = len(cS)
	while i <= n
		c = cS[i]
		if c != " " and c != char(9) and c != char(13) exit ok
		i++
	end
	j = n
	while j >= i
		c = cS[j]
		if c != " " and c != char(9) and c != char(13) exit ok
		j--
	end
	if j < i return "" ok
	return substr(cS, i, j - i + 1)

func FormsPrintSpellings(aDecls, aNames)
	aFam = FormsFamilies(aDecls)
	aMembers = []
	for i = 1 to len(aFam)
		aMembers + FormsMembers(aFam[i][2], aFam[i][3])
	next
	nAgree = 0
	nDis = 0
	for i = 1 to len(aNames)
		cName = aNames[i]
		aS = FormsSplit(cName)
		cWhy = aS[5]
		cOf = ""
		if cWhy = "" and aS[3]
			cTwin = FormsPlainTwin(aS)
			if not InStrListCs(cTwin, aNames)
				cWhy = cName + " requires " + cTwin + ": the fluent form stands beside its plain twin"
			ok
		ok
		if cWhy = ""
			for j = 1 to len(aFam)
				cBase = aFam[j][2]
				bOfFamily = 0
				if InStrListCs(cName, aMembers[j])
					bOfFamily = 1
				but aS[1] = cBase
					bOfFamily = 1
				but len(aFam[j][3]) > 0
					if InStrListCs("passive", aFam[j][3]) and aS[1] = FormsPassive(cBase) bOfFamily = 1 ok
				ok
				if bOfFamily
					if InStrListCs(cName, aMembers[j])
						cOf = " member of " + aFam[j][1]
					else
						cWhy = "the family " + aFam[j][1] + " offers [" + CtJoin(aFam[j][3], ", ") + "] and not the forms of " + cName
					ok
					exit
				ok
			next
		ok
		if cWhy = ""
			nAgree++
			cLine = "agree " + cName + " base=" + aS[1] + " forms=[" + CtJoin(aS[2], ", ") + "]"
			if aS[3] cLine += " fluent" ok
			if aS[4] cLine += " statement" ok
			? cLine + cOf
		else
			nDis++
			? "disagree " + cName + ": " + cWhy
		ok
	next
	nMissing = 0
	for i = 1 to len(aFam)
		for j = 1 to len(aMembers[i])
			if not InStrListCs(aMembers[i][j], aNames)
				nMissing++
				? "missing " + aMembers[i][j] + " (family " + aFam[i][1] + ")"
			ok
		next
	next
	? "spellings: " + nAgree + " agree, " + nDis + " disagree of " + len(aNames) + "; " + nMissing + " declared members missing"
