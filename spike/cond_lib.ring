# cond_lib.ring -- the condition language of stzu v0.2's CONSTRAINT, in pure core Ring.
#
# Closed and total: a condition is read, never run. The grammar is in
# haro/spike/stzu2/GRAMMAR.md. One parser, two readers: the meta-court
# VALIDATES a condition against a declaration's seats (every name it uses
# must exist) and the forged court EVALUATES it on a sentence's declarations.
#
#   cond   = term { ("and" | "or") term }       -- and binds tighter than or
#   term   = [ "not" ] atom
#   atom   = "(" cond ")"
#          | ref "=" value | ref "!=" value | ref ">" number | ref "<" number
#          | seat "present" | seat "absent" | seat "contains" value
#          | seat "empty" | seat "nonempty" | seat "unique" | seat "distinct"
#          | "exists" decl
#   ref    = seat | decl "." seat               -- decl must be a ONE kind
#   value  = IDENT | NUMBER | "'" text "'" | "self"  -- self: the declaration's own name
#
# The AST is nested lists: ["or", a, b]  ["and", a, b]  ["not", a]
#   ["cmp", op, decl, seat, value]  op in = != > <   (decl "" for the declaration's own seat)
#   ["has", test, seat]            test in present absent empty nonempty unique distinct
#   ["contains", seat, value]      ["exists", decl]
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
	cDecl = ""
	cSeat = t[2]
	if CondPeek()[1] = "dot"
		CondNext()
		s = CondNext()
		if s[1] != "word" raise("condition: expected a seat after '.'") ok
		cDecl = cSeat
		cSeat = s[2]
	ok
	op = CondNext()
	if op[1] = "eq" or op[1] = "ne" or op[1] = "gt" or op[1] = "lt"
		v = CondValue()
		if (op[1] = "gt" or op[1] = "lt") and not CondIsNumberText(v)
			raise("condition: " + op[2] + " compares numbers, and '" + v + "' is not one")
		ok
		return ["cmp", op[2], cDecl, cSeat, v]
	ok
	if op[1] = "word"
		if cDecl != ""
			raise("condition: '" + cDecl + "." + cSeat + "' takes = or !=, not '" + op[2] + "'")
		ok
		if op[2] = "present" or op[2] = "absent" or op[2] = "empty" or op[2] = "nonempty" or op[2] = "unique" or op[2] = "distinct"
			return ["has", op[2], cSeat]
		ok
		if op[2] = "contains"
			return ["contains", cSeat, CondValue()]
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
# aSeatNames: the ON declaration's seat names; aDeclNames: every declaration name
# of the language; aOneDecls: the names in WORLD's ONE; fnSeatsOf: a lookup of
# another declaration's seat names is done through $aCondDeclSeats, a list of
# [declname, [seatnames]]. Returns "" or the refusal text.

func CondSeatsOf(cDecl)
	for i = 1 to len($aCondDeclSeats)
		if $aCondDeclSeats[i][1] = cDecl return $aCondDeclSeats[i][2] ok
	next
	return NULL

func CondInList(cS, aL)
	for i = 1 to len(aL)
		if aL[i] = cS return 1 ok
	next
	return 0

func CondValidate(aAst, cOn, aOneDecls)
	cK = aAst[1]
	if cK = "and" or cK = "or"
		e = CondValidate(aAst[2], cOn, aOneDecls)
		if e != "" return e ok
		return CondValidate(aAst[3], cOn, aOneDecls)
	but cK = "not"
		return CondValidate(aAst[2], cOn, aOneDecls)
	but cK = "exists"
		if isNull(CondSeatsOf(aAst[2]))
			return "'" + aAst[2] + "' resolves to nothing: exists names a declaration of this language"
		ok
		return ""
	but cK = "cmp"
		cDecl = aAst[3]
		cSeat = aAst[4]
		if cDecl = ""
			if not CondInList(cSeat, CondSeatsOf(cOn))
				return "no seat '" + cSeat + "' on " + cOn
			ok
			return ""
		ok
		if isNull(CondSeatsOf(cDecl))
			return "'" + cDecl + "' resolves to nothing"
		ok
		if not CondInList(cDecl, aOneDecls)
			return "'" + cDecl + "' is not a ONE kind: only the one declaration of a ONE kind can be read from a condition"
		ok
		if not CondInList(cSeat, CondSeatsOf(cDecl))
			return "no seat '" + cSeat + "' on " + cDecl
		ok
		return ""
	else
		cSeat = aAst[3]
		if cK = "contains" cSeat = aAst[2] ok
		if not CondInList(cSeat, CondSeatsOf(cOn))
			return "no seat '" + cSeat + "' on " + cOn
		ok
		return ""
	ok

# ---- evaluation (the forged court) -------------------------------------------------
# A declaration here is the court's [VERB, name, line, clauses, rationale] with a
# clause [NAME, line, [shape, payload, start, end]]. The seat's clause name is
# upper(seat). $aCondDecls holds every declaration of the sentence; $aCondVerbOf
# maps a declaration (kind) name to its VERB as [declname, VERB] pairs.
# $cCondOther receives the name of the conflicting declaration when unique fails.

func CondVerbOf(cDecl)
	for i = 1 to len($aCondVerbOf)
		if $aCondVerbOf[i][1] = cDecl return $aCondVerbOf[i][2] ok
	next
	return ""

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

func CondEval(aAst, aDecl)
	cK = aAst[1]
	if cK = "and"
		if not CondEval(aAst[2], aDecl) return 0 ok
		return CondEval(aAst[3], aDecl)
	but cK = "or"
		if CondEval(aAst[2], aDecl) return 1 ok
		return CondEval(aAst[3], aDecl)
	but cK = "not"
		return not CondEval(aAst[2], aDecl)
	but cK = "exists"
		cVerb = CondVerbOf(aAst[2])
		for i = 1 to len($aCondDecls)
			if $aCondDecls[i][1] = cVerb return 1 ok
		next
		return 0
	but cK = "cmp"
		op = aAst[2]
		aTarget = aDecl
		if aAst[3] != ""
			aTarget = CondOneDecl(aAst[3])
			if isNull(aTarget) return 0 ok
		ok
		v = CondScalar(aTarget, aAst[4])
		if isNull(v) return 0 ok
		w = aAst[5]
		if w = "self" w = aDecl[2] ok
		if op = "="  return CondSameText(v, w) ok
		if op = "!=" return not CondSameText(v, w) ok
		if not CondIsNumberText(v) return 0 ok
		if op = ">" return 0 + v > 0 + w ok
		return 0 + v < 0 + w
	but cK = "contains"
		aL = CondListOf(aDecl, aAst[2])
		if isNull(aL) return 0 ok
		w = aAst[3]
		if w = "self" w = aDecl[2] ok
		for i = 1 to len(aL)
			if aL[i] = w return 1 ok
		next
		return 0
	else
		cTest = aAst[2]
		cSeat = aAst[3]
		aC = CondClauseOf(aDecl, cSeat)
		if cTest = "present" return not isNull(aC) ok
		if cTest = "absent" return isNull(aC) ok
		if cTest = "empty"
			aL = CondListOf(aDecl, cSeat)
			if isNull(aL) return 0 ok
			return len(aL) = 0
		ok
		if cTest = "nonempty"
			aL = CondListOf(aDecl, cSeat)
			if isNull(aL) return 0 ok
			return len(aL) > 0
		ok
		if cTest = "distinct"
			aL = CondListOf(aDecl, cSeat)
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
			v = CondScalar(aDecl, cSeat)
			if isNull(v) return 1 ok
			for i = 1 to len($aCondDecls)
				aO = $aCondDecls[i]
				if aO[1] = aDecl[1] and aO[2] = aDecl[2] and aO[3] = aDecl[3] exit ok
				if aO[1] = aDecl[1] and aO[2] != aDecl[2]
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
