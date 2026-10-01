# cond_lib.ring -- the condition language of stzu's CONSTRAINT (v0.2, grown
# in v0.3), in pure core Ring.
#
# Closed and total: a condition is read, never run. The grammar is in
# haro/spike/stzu3/GRAMMAR.md (v0.2's in stzu2/). One parser, two readers:
# the meta-court VALIDATES a condition against a declaration's seats (every
# name it uses must exist) and the forged court EVALUATES it on a sentence's
# declarations.
#
#   cond   = term { ("and" | "or") term }       -- and binds tighter than or
#   term   = [ "not" ] atom
#   atom   = "(" cond ")"
#          | "exists" decl
#          | ("some" | "all") target [ "named" value ] [ "where" cond ]   (v0.3)
#          | place "=" value | place "!=" value | place ">" number | place "<" number
#          | place "present" | place "absent" | place "contains" value
#          | place "empty" | place "nonempty" | place "unique" | place "distinct"
#          | place ("within" | "host_of" | "under" | "covers") (place | value)  (v0.3)
#          | place "cyclic" | place "matches" format                            (v0.3)
#   place  = "self" | "this" "." seat | seat | x "." seat
#            x is a scalar reference seat of the current declaration (v0.3), or a
#            ONE kind; inside a quantifier a bare seat is the quantified
#            declaration's and this.seat is the ON declaration's
#   target = a declaration kind, or a list seat of references (v0.3)
#   value  = IDENT | NUMBER | "'" text "'" | "self"  -- self: the declaration's own name
#   a quantifier's "where" runs to the closing parenthesis or the end
#
# The AST is nested lists: ["or", a, b]  ["and", a, b]  ["not", a]  ["exists", decl]
#   ["cmp", op, place, value]        op in = != > <
#   ["has", test, place]             test in present absent empty nonempty unique distinct
#   ["contains", place, value]
#   ["rel", name, place, right]      name in within host_of under covers; right a place or ["val", text]
#   ["cyclic", place]  ["matches", place, format]
#   ["quant", some|all, target, named, cond]   target a name (resolved by both readers the
#                                               same way: a list seat first, then a kind)
#   a place: ["seat", name]  ["this", name]  ["via", x, name]  ["self"]
# Functions only.

func CondIsWordChar(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or (n >= 65 and n <= 90) or n = 95 or (n >= 48 and n <= 57)

func CondIsDigit(c)
	n = ascii(c)
	return (n >= 48 and n <= 57)

# tokens: [type, text]; types: word number string eq ne gt lt lparen rparen dot eof
func CondTokenize(cS)
	aT = []
	n = len(cS)
	i = 1
	while i <= n
		c = cS[i]
		if c = " " or c = char(9)
			i++
		but c = "'"
			j = i + 1
			while j <= n and cS[j] != "'"
				j++
			end
			if j > n raise("condition: unterminated quote in '" + cS + "'") ok
			aT + ["string", substr(cS, i + 1, j - i - 1)]
			i = j + 1
		but CondIsDigit(c)
			j = i
			while j <= n and CondIsDigit(cS[j])
				j++
			end
			aT + ["number", substr(cS, i, j - i)]
			i = j
		but CondIsWordChar(c)
			j = i
			while j <= n and CondIsWordChar(cS[j])
				j++
			end
			aT + ["word", substr(cS, i, j - i)]
			i = j
		but c = "!" and i < n and cS[i+1] = "="
			aT + ["ne", "!="]
			i += 2
		but c = "="
			aT + ["eq", "="]
			i++
		but c = ">"
			aT + ["gt", ">"]
			i++
		but c = "<"
			aT + ["lt", "<"]
			i++
		but c = "("
			aT + ["lparen", "("]
			i++
		but c = ")"
			aT + ["rparen", ")"]
			i++
		but c = "."
			aT + ["dot", "."]
			i++
		else
			raise("condition: the character '" + c + "' is not part of the condition language")
		ok
	end
	aT + ["eof", ""]
	return aT

func CondPeek()
	return $aCondToks[$nCondPos]

func CondNext()
	t = $aCondToks[$nCondPos]
	if t[1] != "eof" $nCondPos++ ok
	return t

func CondParse(cS)
	$aCondToks = CondTokenize(cS)
	$nCondPos = 1
	aAst = CondOr()
	if CondPeek()[1] != "eof"
		raise("condition: unexpected '" + CondPeek()[2] + "' in '" + cS + "'")
	ok
	return aAst

# A node is built in a fresh variable and assigned after: `aL = ["or", aL,
# aR]` puts the variable being assigned inside the list assigned to it, and
# on Ring the copy taken of aL dangles once aL is replaced -- an R2 at the
# next read (Ring, Judged by the Record, 4.4). rnxc ran the one-line form
# correctly; the oracle named it (HF-36).
func CondOr()
	aL = CondAnd()
	while CondPeek()[1] = "word" and CondPeek()[2] = "or"
		CondNext()
		aR = CondAnd()
		aNode = ["or", aL, aR]
		aL = aNode
	end
	return aL

func CondAnd()
	aL = CondTerm()
	while CondPeek()[1] = "word" and CondPeek()[2] = "and"
		CondNext()
		aR = CondTerm()
		aNode = ["and", aL, aR]
		aL = aNode
	end
	return aL

func CondTerm()
	if CondPeek()[1] = "word" and CondPeek()[2] = "not"
		CondNext()
		return ["not", CondTerm()]
	ok
	return CondAtom()

func CondValue()
	t = CondNext()
	if t[1] = "word" or t[1] = "number" or t[1] = "string" return t[2] ok
	raise("condition: expected a value, found '" + t[2] + "'")

# a place, its first word already consumed as t
func CondPlace(t)
	if t[2] = "self" return ["self"] ok
	if t[2] = "this"
		if CondPeek()[1] != "dot" raise("condition: this is read as this.SEAT") ok
		CondNext()
		s = CondNext()
		if s[1] != "word" raise("condition: expected a seat after 'this.'") ok
		return ["this", s[2]]
	ok
	if CondPeek()[1] = "dot"
		CondNext()
		s = CondNext()
		if s[1] != "word" raise("condition: expected a seat after '.'") ok
		return ["via", t[2], s[2]]
	ok
	return ["seat", t[2]]

# the right side of a relation: a quoted or numeric value, or a place
func CondRight()
	t = CondNext()
	if t[1] = "string" or t[1] = "number" return ["val", t[2]] ok
	if t[1] != "word" raise("condition: expected a seat or a value, found '" + t[2] + "'") ok
	return CondPlace(t)

func CondAtom()
	t = CondNext()
	if t[1] = "lparen"
		aC = CondOr()
		if CondNext()[1] != "rparen" raise("condition: expected ')'") ok
		return aC
	ok
	if t[1] != "word"
		raise("condition: expected a seat, found '" + t[2] + "'")
	ok
	if t[2] = "exists"
		d = CondNext()
		if d[1] != "word" raise("condition: exists names a declaration") ok
		return ["exists", d[2]]
	ok
	if t[2] = "some" or t[2] = "all"
		d = CondNext()
		if d[1] != "word" raise("condition: " + t[2] + " names a declaration kind or a list of references") ok
		cNamed = ""
		if CondPeek()[1] = "word" and CondPeek()[2] = "named"
			CondNext()
			cNamed = CondValue()
		ok
		aCond = NULL
		if CondPeek()[1] = "word" and CondPeek()[2] = "where"
			CondNext()
			aCond = CondOr()
		ok
		return ["quant", t[2], d[2], cNamed, aCond]
	ok
	aPlace = CondPlace(t)
	op = CondNext()
	if op[1] = "eq" or op[1] = "ne" or op[1] = "gt" or op[1] = "lt"
		v = CondValue()
		if (op[1] = "gt" or op[1] = "lt") and not CondIsNumberText(v)
			raise("condition: " + op[2] + " compares numbers, and '" + v + "' is not one")
		ok
		return ["cmp", op[2], aPlace, v]
	ok
	if op[1] = "word"
		if op[2] = "present" or op[2] = "absent" or op[2] = "empty" or op[2] = "nonempty" or op[2] = "unique" or op[2] = "distinct"
			return ["has", op[2], aPlace]
		ok
		if op[2] = "contains"
			return ["contains", aPlace, CondValue()]
		ok
		if op[2] = "within" or op[2] = "host_of" or op[2] = "under" or op[2] = "covers"
			return ["rel", op[2], aPlace, CondRight()]
		ok
		if op[2] = "cyclic"
			return ["cyclic", aPlace]
		ok
		if op[2] = "matches"
			f = CondNext()
			if f[1] != "word" raise("condition: matches names a FORMAT") ok
			return ["matches", aPlace, f[2]]
		ok
	ok
	raise("condition: '" + op[2] + "' is not an operator of the condition language")

func CondIsNumberText(v)
	if len(v) = 0 return 0 ok
	for i = 1 to len(v)
		if not CondIsDigit(v[i]) return 0 ok
	next
	return 1

# ---- validation (the meta-court) ------------------------------------------------
# $aCondDeclSeats: [[declname, [[seat, of, isList, kind], ...]], ...] for every
# DECLARATION of the language; kind is prim, form, expr, menu, range, format,
# decl or union. $aCondFormats: [[name, shape], ...]. aOneDecls: the names in
# WORLD's ONE. cInner: "" outside a quantifier, else the quantified kind.
# Returns "" or the refusal text.

func CondSeatsOf(cDecl)
	for i = 1 to len($aCondDeclSeats)
		if $aCondDeclSeats[i][1] = cDecl return $aCondDeclSeats[i][2] ok
	next
	return NULL

func CondSeatInfo(cDecl, cSeat)
	aS = CondSeatsOf(cDecl)
	if isNull(aS) return NULL ok
	for i = 1 to len(aS)
		if aS[i][1] = cSeat return aS[i] ok
	next
	return NULL

func CondHasSeat(cDecl, cSeat)
	return not isNull(CondSeatInfo(cDecl, cSeat))

func CondInList(cS, aL)
	for i = 1 to len(aL)
		if aL[i] = cS return 1 ok
	next
	return 0

func CondFormatShape(cName)
	for i = 1 to len($aCondFormats)
		if $aCondFormats[i][1] = cName return $aCondFormats[i][2] ok
	next
	return ""

func CondCurName(cOn, cInner)
	if cInner != "" return cInner ok
	return cOn

func CondPlaceText(aP)
	if aP[1] = "self" return "self" ok
	if aP[1] = "this" return "this." + aP[2] ok
	if aP[1] = "via" return aP[2] + "." + aP[3] ok
	return aP[2]

func CondValidatePlace(aP, cOn, cInner, aOneDecls)
	cCur = CondCurName(cOn, cInner)
	if aP[1] = "self" return "" ok
	if aP[1] = "seat"
		if not CondHasSeat(cCur, aP[2]) return "no seat '" + aP[2] + "' on " + cCur ok
		return ""
	ok
	if aP[1] = "this"
		if cInner = "" return "this." + aP[2] + " is read inside some or all, where a bare seat is the quantified declaration's" ok
		if not CondHasSeat(cOn, aP[2]) return "no seat '" + aP[2] + "' on " + cOn ok
		return ""
	ok
	x = aP[2]
	s = aP[3]
	aInfo = CondSeatInfo(cCur, x)
	if not isNull(aInfo)
		if aInfo[4] = "decl" and not aInfo[3]
			if not CondHasSeat(aInfo[2], s) return "no seat '" + s + "' on " + aInfo[2] ok
			return ""
		ok
	ok
	if isNull(CondSeatsOf(x))
		return "'" + x + "' is not a ONE kind, and neither a reference seat of " + cCur + ": X.seat reads through a reference seat, or the one declaration of a ONE kind"
	ok
	if not CondInList(x, aOneDecls)
		return "'" + x + "' is not a ONE kind, and neither a reference seat of " + cCur + ": only the one declaration of a ONE kind can be read from a condition"
	ok
	if not CondHasSeat(x, s) return "no seat '" + s + "' on " + x ok
	return ""

func CondValidate(aAst, cOn, aOneDecls, cInner)
	cCur = CondCurName(cOn, cInner)
	cK = aAst[1]
	if cK = "and" or cK = "or"
		e = CondValidate(aAst[2], cOn, aOneDecls, cInner)
		if e != "" return e ok
		return CondValidate(aAst[3], cOn, aOneDecls, cInner)
	but cK = "not"
		return CondValidate(aAst[2], cOn, aOneDecls, cInner)
	but cK = "exists"
		if isNull(CondSeatsOf(aAst[2]))
			return "'" + aAst[2] + "' resolves to nothing: exists names a declaration of this language"
		ok
		return ""
	but cK = "cmp"
		return CondValidatePlace(aAst[3], cOn, cInner, aOneDecls)
	but cK = "has"
		return CondValidatePlace(aAst[3], cOn, cInner, aOneDecls)
	but cK = "contains"
		return CondValidatePlace(aAst[2], cOn, cInner, aOneDecls)
	but cK = "rel"
		e = CondValidatePlace(aAst[3], cOn, cInner, aOneDecls)
		if e != "" return e ok
		if aAst[2] = "covers"
			# a list seat, or a UNION seat (one of whose alternatives may be a
			# list; a word written there covers nothing)
			aP = aAst[3]
			bList = 0
			aInfo = NULL
			if aP[1] = "seat"
				aInfo = CondSeatInfo(cCur, aP[2])
			but aP[1] = "this"
				aInfo = CondSeatInfo(cOn, aP[2])
			ok
			if not isNull(aInfo)
				if aInfo[3] or aInfo[4] = "union" bList = 1 ok
			ok
			if not bList return "covers takes a list seat on its left, and '" + CondPlaceText(aP) + "' is not one" ok
		ok
		if aAst[4][1] != "val"
			return CondValidatePlace(aAst[4], cOn, cInner, aOneDecls)
		ok
		return ""
	but cK = "cyclic"
		aP = aAst[2]
		bOk = 0
		if aP[1] = "seat"
			aInfo = CondSeatInfo(cCur, aP[2])
			if not isNull(aInfo)
				if aInfo[3] and aInfo[4] = "decl" and aInfo[2] = cCur bOk = 1 ok
			ok
		ok
		if not bOk return "cyclic follows a list of references to the declaration's own kind, and '" + CondPlaceText(aP) + "' is not one" ok
		return ""
	but cK = "matches"
		e = CondValidatePlace(aAst[2], cOn, cInner, aOneDecls)
		if e != "" return e ok
		if CondFormatShape(aAst[3]) = "" return "'" + aAst[3] + "' must name a FORMAT of this language: matches tests a shape" ok
		return ""
	but cK = "quant"
		cTarget = aAst[3]
		cInnerKind = ""
		aInfo = CondSeatInfo(cCur, cTarget)
		if not isNull(aInfo)
			if aInfo[3] and aInfo[4] = "decl"
				if aAst[4] != "" return "named goes with a kind, and '" + cTarget + "' is a list of references, already named" ok
				cInnerKind = aInfo[2]
			ok
		ok
		if cInnerKind = ""
			if isNull(CondSeatsOf(cTarget))
				return "'" + cTarget + "' names neither a declaration kind nor a list of references: some and all quantify over a declaration kind or a list of references"
			ok
			cInnerKind = cTarget
		ok
		if not isNull(aAst[5])
			return CondValidate(aAst[5], cOn, aOneDecls, cInnerKind)
		ok
		return ""
	ok
	return "'" + cK + "' is not a condition"

# ---- evaluation (the forged court) -------------------------------------------------
# A declaration here is the court's [VERB, name, line, clauses, rationale] with a
# clause [NAME, line, [shape, payload, start, end]]. The seat's clause name is
# upper(seat). $aCondDecls holds every declaration of the sentence; $aCondVerbOf
# maps a declaration (kind) name to its VERB as [declname, VERB] pairs;
# $aCondRefSeats maps a kind name to its reference seats as
# [declname, [[seat, targetkind, isList], ...]]. $cCondOther receives the name of
# the conflicting declaration when unique, distinct or all fails. $bCondUnread
# is raised when a place reads through a reference that resolves to nothing:
# such a condition says nothing, and the reference's own refusal speaks.

func CondVerbOf(cDecl)
	for i = 1 to len($aCondVerbOf)
		if $aCondVerbOf[i][1] = cDecl return $aCondVerbOf[i][2] ok
	next
	return ""

func CondDeclNameOf(cVerb)
	for i = 1 to len($aCondVerbOf)
		if $aCondVerbOf[i][2] = cVerb return $aCondVerbOf[i][1] ok
	next
	return ""

func CondRefOf(cDeclName, cSeat)
	for i = 1 to len($aCondRefSeats)
		if $aCondRefSeats[i][1] = cDeclName
			aR = $aCondRefSeats[i][2]
			for j = 1 to len(aR)
				if aR[j][1] = cSeat return aR[j] ok
			next
			return NULL
		ok
	next
	return NULL

func CondFindDecl(cDeclName, cName)
	cVerb = CondVerbOf(cDeclName)
	for i = 1 to len($aCondDecls)
		if $aCondDecls[i][1] = cVerb and $aCondDecls[i][2] = cName return $aCondDecls[i] ok
	next
	return NULL

func CondClauseOf(aDecl, cSeat)
	aC = aDecl[4]
	cN = upper(cSeat)
	for i = 1 to len(aC)
		if aC[i][1] = cN return aC[i] ok
	next
	return NULL

# the text of a scalar value, or NULL when the seat is absent or a list
func CondScalar(aDecl, cSeat)
	aC = CondClauseOf(aDecl, cSeat)
	if isNull(aC) return NULL ok
	cShape = aC[3][1]
	if cShape = "word" or cShape = "string" or cShape = "number" return aC[3][2] ok
	return NULL

func CondListOf(aDecl, cSeat)
	aC = CondClauseOf(aDecl, cSeat)
	if isNull(aC) return NULL ok
	cShape = aC[3][1]
	if cShape = "namelist" or cShape = "stringlist" return aC[3][2] ok
	return NULL

func CondOneDecl(cDecl)
	cVerb = CondVerbOf(cDecl)
	for i = 1 to len($aCondDecls)
		if $aCondDecls[i][1] = cVerb return $aCondDecls[i] ok
	next
	return NULL

func CondSameText(a, b)
	return a = b

func CondCur(aOuter, aInner)
	if isNull(aInner) return aOuter ok
	return aInner

# a place resolved on the current declarations: [decl, seat] with seat "" for
# self; NULL (and $bCondUnread raised) when a reference resolves to nothing
func CondResolve(aP, aOuter, aInner)
	aCur = CondCur(aOuter, aInner)
	if aP[1] = "self" return [aCur, ""] ok
	if aP[1] = "seat" return [aCur, aP[2]] ok
	if aP[1] = "this" return [aOuter, aP[2]] ok
	aRef = CondRefOf(CondDeclNameOf(aCur[1]), aP[2])
	if not isNull(aRef)
		if not aRef[3]
			v = CondScalar(aCur, aP[2])
			if isNull(v)
				$bCondUnread = 1
				return NULL
			ok
			aT = CondFindDecl(aRef[2], v)
			if isNull(aT)
				$bCondUnread = 1
				return NULL
			ok
			return [aT, aP[3]]
		ok
	ok
	aOne = CondOneDecl(aP[2])
	if isNull(aOne)
		$bCondUnread = 1
		return NULL
	ok
	return [aOne, aP[3]]

func CondPlaceScalar(aP, aOuter, aInner)
	r = CondResolve(aP, aOuter, aInner)
	if isNull(r) return NULL ok
	if r[2] = "" return r[1][2] ok
	return CondScalar(r[1], r[2])

func CondPlaceList(aP, aOuter, aInner)
	r = CondResolve(aP, aOuter, aInner)
	if isNull(r) return NULL ok
	if r[2] = "" return NULL ok
	return CondListOf(r[1], r[2])

func CondRightText(aR, aOuter, aInner)
	if aR[1] = "val" return aR[2] ok
	return CondPlaceScalar(aR, aOuter, aInner)

func CondEval(aAst, aDecl)
	return CondEvalIn(aAst, aDecl, NULL)

func CondEvalIn(aAst, aOuter, aInner)
	aCur = CondCur(aOuter, aInner)
	cK = aAst[1]
	if cK = "and"
		if not CondEvalIn(aAst[2], aOuter, aInner) return 0 ok
		return CondEvalIn(aAst[3], aOuter, aInner)
	but cK = "or"
		if CondEvalIn(aAst[2], aOuter, aInner) return 1 ok
		return CondEvalIn(aAst[3], aOuter, aInner)
	but cK = "not"
		return not CondEvalIn(aAst[2], aOuter, aInner)
	but cK = "exists"
		cVerb = CondVerbOf(aAst[2])
		for i = 1 to len($aCondDecls)
			if $aCondDecls[i][1] = cVerb return 1 ok
		next
		return 0
	but cK = "cmp"
		op = aAst[2]
		v = CondPlaceScalar(aAst[3], aOuter, aInner)
		if isNull(v) return 0 ok
		w = aAst[4]
		if w = "self" w = aCur[2] ok
		if op = "="  return CondSameText(v, w) ok
		if op = "!=" return not CondSameText(v, w) ok
		if not CondIsNumberText(v) return 0 ok
		if op = ">" return 0 + v > 0 + w ok
		return 0 + v < 0 + w
	but cK = "contains"
		aL = CondPlaceList(aAst[2], aOuter, aInner)
		if isNull(aL) return 0 ok
		w = aAst[3]
		if w = "self" w = aCur[2] ok
		for i = 1 to len(aL)
			if aL[i] = w return 1 ok
		next
		return 0
	but cK = "rel"
		cRel = aAst[2]
		if cRel = "covers"
			aL = CondPlaceList(aAst[3], aOuter, aInner)
			if isNull(aL) return 0 ok
			cR = CondRightText(aAst[4], aOuter, aInner)
			if isNull(cR) return 0 ok
			return CondCovers(aL, cR)
		ok
		v = CondPlaceScalar(aAst[3], aOuter, aInner)
		if isNull(v) return 0 ok
		cR = CondRightText(aAst[4], aOuter, aInner)
		if isNull(cR) return 0 ok
		if cRel = "within" return CondWithin(v, cR) ok
		if cRel = "host_of" return CondHostOf(v, cR) ok
		return CondUnder(v, cR)
	but cK = "cyclic"
		r = CondResolve(aAst[2], aOuter, aInner)
		if isNull(r) return 0 ok
		if r[2] = "" return 0 ok
		return CondCyclic(r[1], r[2])
	but cK = "matches"
		v = CondPlaceScalar(aAst[2], aOuter, aInner)
		if isNull(v) return 0 ok
		return CondHasShape(v, CondFormatShape(aAst[3]))
	but cK = "quant"
		return CondQuant(aAst, aOuter, aInner)
	else
		# has
		cTest = aAst[2]
		r = CondResolve(aAst[3], aOuter, aInner)
		if isNull(r) return 0 ok
		if r[2] = ""
			if cTest = "present" return 1 ok
			return 0
		ok
		aD = r[1]
		cSeat = r[2]
		aC = CondClauseOf(aD, cSeat)
		if cTest = "present" return not isNull(aC) ok
		if cTest = "absent" return isNull(aC) ok
		if cTest = "empty"
			aL = CondListOf(aD, cSeat)
			if isNull(aL) return 0 ok
			return len(aL) = 0
		ok
		if cTest = "nonempty"
			aL = CondListOf(aD, cSeat)
			if isNull(aL) return 0 ok
			return len(aL) > 0
		ok
		if cTest = "distinct"
			aL = CondListOf(aD, cSeat)
			if isNull(aL) return 1 ok
			for i = 1 to len(aL)
				for j = 1 to i - 1
					if aL[i] = aL[j]
						$cCondOther = aL[i]
						return 0
					ok
				next
			next
			return 1
		ok
		if cTest = "unique"
			# against the declarations BEFORE this one, so the later of two
			# is the one refused and {other} names the earlier ("already a's")
			v = CondScalar(aD, cSeat)
			if isNull(v) return 1 ok
			for i = 1 to len($aCondDecls)
				aO = $aCondDecls[i]
				if aO[1] = aD[1] and aO[2] = aD[2] and aO[3] = aD[3] exit ok
				if aO[1] = aD[1] and aO[2] != aD[2]
					w = CondScalar(aO, cSeat)
					if not isNull(w) and w = v
						$cCondOther = aO[2]
						return 0
					ok
				ok
			next
			return 1
		ok
		return 0
	ok

# some/all over the declarations of a kind (narrowed by named), or over the
# declarations a list seat of references names; all records the first failure
func CondQuant(aAst, aOuter, aInner)
	aCur = CondCur(aOuter, aInner)
	cKind = aAst[2]
	cTarget = aAst[3]
	cNamed = aAst[4]
	if cNamed = "self" cNamed = aCur[2] ok
	aCond = aAst[5]
	aItems = []
	aRef = CondRefOf(CondDeclNameOf(aCur[1]), cTarget)
	bList = 0
	if not isNull(aRef)
		if aRef[3] bList = 1 ok
	ok
	if bList
		aL = CondListOf(aCur, cTarget)
		if isNull(aL) aL = [] ok
		for i = 1 to len(aL)
			aT = CondFindDecl(aRef[2], aL[i])
			if not isNull(aT) aItems + aT ok
		next
	else
		cVerb = CondVerbOf(cTarget)
		for i = 1 to len($aCondDecls)
			aD = $aCondDecls[i]
			if aD[1] = cVerb
				if cNamed = "" or aD[2] = cNamed aItems + aD ok
			ok
		next
	ok
	if cKind = "some"
		for i = 1 to len(aItems)
			if isNull(aCond) return 1 ok
			if CondEvalIn(aCond, aOuter, aItems[i]) return 1 ok
		next
		return 0
	ok
	for i = 1 to len(aItems)
		if not isNull(aCond)
			if not CondEvalIn(aCond, aOuter, aItems[i])
				$cCondOther = aItems[i][2]
				return 0
			ok
		ok
	next
	return 1

# ---- the relations, each total ---------------------------------------------------

func CondSplit(cS, cSep)
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

func CondIsHexChar(c)
	n = ascii(c)
	return (n >= 48 and n <= 57) or (n >= 97 and n <= 102) or (n >= 65 and n <= 70)

func CondIsLabelChar(c)
	n = ascii(c)
	return (n >= 97 and n <= 122) or (n >= 48 and n <= 57) or n = 45

func CondIsIpv4(cS)
	aParts = CondSplit(cS, ".")
	if len(aParts) != 4 return 0 ok
	for i = 1 to 4
		p = aParts[i]
		if len(p) = 0 or len(p) > 3 return 0 ok
		for j = 1 to len(p)
			if not CondIsDigit(p[j]) return 0 ok
		next
		if 0 + p > 255 return 0 ok
	next
	return 1

func CondIsLabel(cS)
	if len(cS) = 0 return 0 ok
	for i = 1 to len(cS)
		if not CondIsLabelChar(cS[i]) return 0 ok
	next
	if cS[1] = "-" return 0 ok
	if cS[len(cS)] = "-" return 0 ok
	return 1

# the shapes of a FORMAT: absolute_path, ipv4, cidr, mac, label, domain
func CondHasShape(cS, cShape)
	if cShape = "absolute_path"
		if len(cS) = 0 return 0 ok
		return cS[1] = "/"
	but cShape = "ipv4"
		return CondIsIpv4(cS)
	but cShape = "cidr"
		aP = CondSplit(cS, "/")
		if len(aP) != 2 return 0 ok
		if not CondIsIpv4(aP[1]) return 0 ok
		if len(aP[2]) = 0 or len(aP[2]) > 2 return 0 ok
		for j = 1 to len(aP[2])
			if not CondIsDigit(aP[2][j]) return 0 ok
		next
		return 0 + aP[2] <= 32
	but cShape = "mac"
		aP = CondSplit(cS, ":")
		if len(aP) != 6 return 0 ok
		for i = 1 to 6
			if len(aP[i]) != 2 return 0 ok
			if not (CondIsHexChar(aP[i][1]) and CondIsHexChar(aP[i][2])) return 0 ok
		next
		return 1
	but cShape = "label"
		return CondIsLabel(cS)
	but cShape = "domain"
		aP = CondSplit(cS, ".")
		for i = 1 to len(aP)
			if not CondIsLabel(aP[i]) return 0 ok
		next
		return 1
	ok
	return 1

# an address as a number (0..4294967295), or -1
func CondIpNum(cS)
	if not CondIsIpv4(cS) return -1 ok
	aP = CondSplit(cS, ".")
	return ((0 + aP[1]) * 16777216) + ((0 + aP[2]) * 65536) + ((0 + aP[3]) * 256) + (0 + aP[4])

func CondBlock(nBits)
	n = 1
	for i = 1 to nBits
		n *= 2
	next
	return n

# a prefix as [first, last], or NULL
func CondCidrRange(cS)
	if not CondHasShape(cS, "cidr") return NULL ok
	aP = CondSplit(cS, "/")
	nIp = CondIpNum(aP[1])
	nBlock = CondBlock(32 - (0 + aP[2]))
	nLo = nIp - (nIp % nBlock)
	return [nLo, nLo + nBlock - 1]

func CondWithin(cIp, cCidr)
	n = CondIpNum(cIp)
	if n < 0 return 0 ok
	aR = CondCidrRange(cCidr)
	if isNull(aR) return 0 ok
	return n >= aR[1] and n <= aR[2]

func CondHostOf(cIp, cCidr)
	n = CondIpNum(cIp)
	if n < 0 return 0 ok
	if not CondHasShape(cCidr, "cidr") return 0 ok
	aP = CondSplit(cCidr, "/")
	return n = CondIpNum(aP[1])

# a path under a directory: the directory itself, or a path that continues
# past it at a slash; "/" keeps every absolute path (harb's rule)
func CondUnder(cPath, cDir)
	if len(cDir) = 0 return 0 ok
	if cDir = "/"
		if len(cPath) = 0 return 0 ok
		return cPath[1] = "/"
	ok
	if cPath = cDir return 1 ok
	if len(cPath) <= len(cDir) return 0 ok
	if left(cPath, len(cDir)) != cDir return 0 ok
	return cPath[len(cDir) + 1] = "/"

# a list of prefixes covers a prefix when their ranges, taken together, hold
# every address of it: sweep the ranges in order of their first address
func CondCovers(aList, cCidr)
	aT = CondCidrRange(cCidr)
	if isNull(aT) return 0 ok
	aR = []
	for i = 1 to len(aList)
		r = CondCidrRange(aList[i])
		if not isNull(r)
			# insertion, by first address
			nAt = len(aR) + 1
			for j = 1 to len(aR)
				if aR[j][1] > r[1]
					nAt = j
					exit
				ok
			next
			insert(aR, nAt - 1, r)
		ok
	next
	nCur = aT[1]
	for i = 1 to len(aR)
		if aR[i][1] <= nCur and aR[i][2] >= nCur
			nCur = aR[i][2] + 1
			if nCur > aT[2] return 1 ok
		ok
	next
	return nCur > aT[2]

# the references of a list seat, followed through declarations of the same
# kind, return to the declaration they started from
func CondCyclic(aDecl, cSeat)
	aRef = CondRefOf(CondDeclNameOf(aDecl[1]), cSeat)
	if isNull(aRef) return 0 ok
	aSeen = []
	return CondReaches(aDecl, cSeat, aDecl[2], aRef[2], aSeen)

func CondReaches(aFrom, cSeat, cStart, cTargetKind, aSeen)
	aL = CondListOf(aFrom, cSeat)
	if isNull(aL) return 0 ok
	for i = 1 to len(aL)
		if aL[i] = cStart return 1 ok
		if CondInList(aL[i], aSeen) loop ok
		aSeen + aL[i]
		aT = CondFindDecl(cTargetKind, aL[i])
		if isNull(aT) loop ok
		if CondReaches(aT, cSeat, cStart, cTargetKind, aSeen) return 1 ok
	next
	return 0
