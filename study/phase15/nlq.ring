# nlq.ring -- Phase 1.5: the natural-language QUESTION surface of the tontine, retargeted.
#
# The architecture is stzNatural's -- language packs as data, tokens as semantic ids, one semantic
# core under many linguistic skins -- with the compile target changed per Ringua rule 2: the
# generate-Ring-and-eval stage is NOT used. A question ends as one of
#
#   a ZQL question   SELECT * FROM collect WHERE ...     judged by the ledger's court (ask verb)
#   a triple pattern ["?x", "received_pot_in", "round2"]  judged by the knowledge graph (Query)
#   a plan           one of each, the second built from the first's answer
#   a refusal        the word, the character or the shape that was not understood
#
# and nothing in the question's TEXT reaches any of them except as a digit string. Names come from
# the knowledge graph (the lexicon is generated from its facts), never from the question.
#
# Closed on purpose, in this order:  gate (characters) -> tokens (StzNaturalEngineQ().Analyze, which
# does not generate or run code) -> frames (a table, data) -> templates (a table, data).

$aNlqMembers = []     # ids from the graph, e.g. "aminata"
$aNlqRounds  = []
$aNlqRoles   = []
$oNlqGraph   = NULL

# ---- vocabulary: DATA ---------------------------------------------------------------------------
# semantic ids are "KIND" or "KIND:argument"; the entity entries are generated from the graph below

func NlqPackEnglish
	return [
		:code = "tn-en", :name = "tontine english", :script = "latin",
		:ignored_words = ["the", "a", "an", "of", "me", "please", "is", "are", "in", "by", "than", "all",
				"did", "does", "was", "were", "to", "for", "pot"],
		:semantic_mappings = [
			[:natural = "show", :semantic = "Q_SHOW"], [:natural = "list", :semantic = "Q_SHOW"],
			[:natural = "display", :semantic = "Q_SHOW"], [:natural = "give", :semantic = "Q_SHOW"],
			[:natural = "who", :semantic = "Q_WHO"],
			[:natural = "deposit", :semantic = "ENT_DEPOSIT"], [:natural = "deposits", :semantic = "ENT_DEPOSIT"],
			[:natural = "over", :semantic = "CMP_GT"], [:natural = "above", :semantic = "CMP_GT"],
			[:natural = "exceeding", :semantic = "CMP_GT"], [:natural = "more", :semantic = "CMP_GT"],
			[:natural = "under", :semantic = "CMP_LT"], [:natural = "below", :semantic = "CMP_LT"],
			[:natural = "less", :semantic = "CMP_LT"],
			[:natural = "round", :semantic = "KW_ROUND"],
			[:natural = "biggest", :semantic = "KW_BIGGEST"], [:natural = "largest", :semantic = "KW_BIGGEST"],
			[:natural = "highest", :semantic = "KW_BIGGEST"],
			[:natural = "received", :semantic = "REL_RECEIVED"], [:natural = "got", :semantic = "REL_RECEIVED"],
			[:natural = "guarantees", :semantic = "REL_GUARANTEES"], [:natural = "guarantee", :semantic = "REL_GUARANTEES"],
			[:natural = "guaranteed", :semantic = "REL_GUARANTEED_BY"],
			[:natural = "beneficiary", :semantic = "KW_BENEFICIARY"]
		]
	]

func NlqPackFrench
	return [
		:code = "tn-fr", :name = "tontine francais", :script = "latin",
		:ignored_words = ["le", "la", "les", "l", "de", "des", "du", "d", "au", "aux", "a", "est", "se", "porte",
				"par", "un", "une", "moi", "plus", "cagnotte", "pot"],
		:semantic_mappings = [
			[:natural = "montre", :semantic = "Q_SHOW"], [:natural = "montrez", :semantic = "Q_SHOW"],
			[:natural = "affiche", :semantic = "Q_SHOW"], [:natural = "liste", :semantic = "Q_SHOW"],
			[:natural = "qui", :semantic = "Q_WHO"],
			[:natural = "depot", :semantic = "ENT_DEPOSIT"], [:natural = "depots", :semantic = "ENT_DEPOSIT"],
			[:natural = "dépôt", :semantic = "ENT_DEPOSIT"], [:natural = "dépôts", :semantic = "ENT_DEPOSIT"],
			[:natural = "dessus", :semantic = "CMP_GT"], [:natural = "superieur", :semantic = "CMP_GT"],
			[:natural = "supérieur", :semantic = "CMP_GT"],
			[:natural = "dessous", :semantic = "CMP_LT"], [:natural = "inferieur", :semantic = "CMP_LT"],
			[:natural = "inférieur", :semantic = "CMP_LT"],
			[:natural = "tour", :semantic = "KW_ROUND"],
			[:natural = "gros", :semantic = "KW_BIGGEST"], [:natural = "grand", :semantic = "KW_BIGGEST"],
			[:natural = "recu", :semantic = "REL_RECEIVED"], [:natural = "reçu", :semantic = "REL_RECEIVED"],
			[:natural = "garant", :semantic = "REL_GUARANTEES"], [:natural = "garantit", :semantic = "REL_GUARANTEES"],
			[:natural = "garanti", :semantic = "REL_GUARANTEED_BY"],
			[:natural = "beneficiaire", :semantic = "KW_BENEFICIARY"], [:natural = "bénéficiaire", :semantic = "KW_BENEFICIARY"]
		]
	]

# the role words per language: the ROLE id is the graph's, the word is the language's
func NlqRoleWords cLang
	if cLang = "tn-fr"
		# the first spelling of a role is the one an answer is told in; the others are accepted in a question
		return [["trésorier", "treasurer"], ["tresorier", "treasurer"], ["collecteur", "collector"]]
	ok
	return [["treasurer", "treasurer"], ["collector", "collector"]]

# ---- the world: the knowledge graph artifact, and the lexicon generated from it ---------------------

func NlqLoadWorld cArtifact
	$oNlqGraph = new stzKnowledgeGraph("tontine")
	$oNlqGraph.ImportKnow(cArtifact)
	$aNlqMembers = $oNlqGraph.Query(["?x", "is-a", "member"])
	$aNlqRounds  = $oNlqGraph.Query(["?x", "is-a", "round"])
	$aNlqRoles   = $oNlqGraph.Query(["?x", "is-a", "role"])
	for cLang in ["tn-en", "tn-fr"]
		if cLang = "tn-en"
			aPack = NlqPackEnglish()
		else
			aPack = NlqPackFrench()
		ok
		aMap = aPack[:semantic_mappings]
		# every member of the graph is a word of the language, in either language: a name is not translated
		for cM in $aNlqMembers
			aMap + [:natural = cM, :semantic = "ENT_MEMBER:" + cM]
		next
		for aRw in NlqRoleWords(cLang)
			if find($aNlqRoles, aRw[2]) > 0
				aMap + [:natural = aRw[1], :semantic = "ENT_ROLE:" + aRw[2]]
			ok
		next
		aPack[:semantic_mappings] = aMap
		StzAddNaturalLanguage(aPack)
	next

# ---- gate: the characters a question may use --------------------------------------------------------

func NlqGate cText
	# an allow-list. letters and digits of Latin script and any UTF-8 letter (bytes >= 128), the space,
	# and the punctuation of a sentence. Everything Ring or ZQL reads as syntax -- [ ] { } ( ) " ` ; : = < > $ @
	# # \ / ! % & * + | ~ ^ -- is refused before the tokenizer (which evals a bracketed section) sees it.
	for i = 1 to len(cText)
		c = cText[i]
		n = ascii(c)
		if n >= 128 loop ok
		if (n >= 48 and n <= 57) or (n >= 65 and n <= 90) or (n >= 97 and n <= 122) loop ok
		if c = " " or c = "-" or c = "'" or c = "?" or c = "," or c = "." loop ok
		# the refusal names the character; a control character is named by its code, never printed
		if n < 32 or n = 127 return "(control character " + n + ")" ok
		return c
	next
	return ""

func NlqNormalise cText
	cText = trim(cText)
	cText = substr(cText, "?", " ")
	cText = substr(cText, ",", " ")
	cText = substr(cText, "'", " ")
	cText = substr(cText, ".", " ")
	return cText

# ---- frames: the shapes of a question, DATA -----------------------------------------------------------
# [id, token kinds in order, kind, target template]   slots: {NUM} {MEMBER} {ROLE}

func NlqFrames
	return [
		["ledger-all",      "Q_SHOW ENT_DEPOSIT",                     "ledger", 'SELECT * FROM collect'],
		["ledger-over",     "Q_SHOW ENT_DEPOSIT CMP_GT NUM",          "ledger", 'SELECT * FROM collect WHERE amount > {NUM}'],
		["ledger-under",    "Q_SHOW ENT_DEPOSIT CMP_LT NUM",          "ledger", 'SELECT * FROM collect WHERE amount < {NUM}'],
		["ledger-member",   "Q_SHOW ENT_DEPOSIT ENT_MEMBER",          "ledger", 'SELECT * FROM collect WHERE member = "{MEMBER}"'],
		["ledger-round",    "Q_SHOW ENT_DEPOSIT KW_ROUND NUM",        "ledger", 'SELECT * FROM collect WHERE round = {NUM}'],
		["ledger-biggest",  "Q_SHOW KW_BIGGEST ENT_DEPOSIT",          "ledger", 'SELECT * FROM collect ORDER BY amount DESC LIMIT 1'],
		["ledger-member-over", "Q_SHOW ENT_DEPOSIT ENT_MEMBER CMP_GT NUM", "ledger", 'SELECT * FROM collect WHERE member = "{MEMBER}" AND amount > {NUM}'],
		["graph-pot",       "Q_WHO REL_RECEIVED KW_ROUND NUM",        "graph",  '["?x", "received_pot_in", "round{NUM}"]'],
		["graph-guarantor", "Q_WHO REL_GUARANTEES ENT_MEMBER",        "graph",  '["?x", "guarantees", "{MEMBER}"]'],
		["graph-guaranteed-by", "Q_WHO REL_GUARANTEED_BY ENT_MEMBER", "graph",  '["{MEMBER}", "guarantees", "?x"]'],
		["graph-role",      "Q_WHO ENT_ROLE",                         "graph",  '["?x", "holds_role", "{ROLE}"]'],
		["plan-beneficiary-deposits", "Q_SHOW ENT_DEPOSIT KW_BENEFICIARY KW_ROUND NUM", "plan", '["?x", "received_pot_in", "round{NUM}"] => SELECT * FROM collect WHERE member = "{MEMBER}"']
	]

# ---- compile: question -> closed query | refusal ----------------------------------------------------

# returns [kind, target, reason, frame id]
func NlqCompile cLang, cText
	cBad = NlqGate(cText)
	if cBad != ""
		return ["refused", "", NlqMsg(cLang, "char", cBad), "", []]
	ok
	oE = new stzNaturalEngine(cLang, "", [], "")
	oE.Analyze(NlqNormalise(cText))
	aToks = oE.Tokens()
	aKinds = []
	aArgs = []
	for aT in aToks
		cType = aT[:type]
		cVal = "" + aT[:value]
		if cType = "semantic"
			nColon = substr(cVal, ":")
			if nColon > 0
				aKinds + left(cVal, nColon - 1)
				aArgs + substr(cVal, nColon + 1)
			else
				aKinds + cVal
				aArgs + ""
			ok
		elseif cType = "literal" and NlqIsDigits(cVal)
			aKinds + "NUM"
			aArgs + cVal
		else
			return ["refused", "", NlqMsg(cLang, "word", cVal), "", []]
		ok
	next
	cShape = NlqJoin(aKinds, " ")
	aFrames = NlqFrames()
	for aF in aFrames
		if aF[2] = cShape
			cTarget = aF[4]
			aSlots = []
			for i = 1 to len(aKinds)
				if aKinds[i] = "NUM"
					cTarget = substr(cTarget, "{NUM}", aArgs[i])
					aSlots + ["NUM", aArgs[i]]
				elseif aKinds[i] = "ENT_MEMBER"
					cTarget = substr(cTarget, "{MEMBER}", NlqDisplay(aArgs[i], aF[3]))
					aSlots + ["MEMBER", aArgs[i]]
				elseif aKinds[i] = "ENT_ROLE"
					cTarget = substr(cTarget, "{ROLE}", aArgs[i])
					aSlots + ["ROLE", aArgs[i]]
				ok
			next
			return [aF[3], cTarget, "", aF[1], aSlots]
		ok
	next
	return ["refused", "", NlqMsg(cLang, "shape", cShape), "", []]

# the refusal says what it did not understand in the words of the question's own language: DATA
func NlqMsg cLang, cKey, cArg
	if cLang = "tn-fr"
		if cKey = "char" return "la question contient un caractere que cette langue n'emploie pas : " + cArg ok
		if cKey = "word" return "le mot « " + cArg + " » ne fait pas partie du vocabulaire de la tontine" ok
		return "les mots sont connus mais aucune question n'a cette forme : " + cArg
	ok
	if cKey = "char" return "the question carries a character this language does not use: " + cArg ok
	if cKey = "word" return "the word '" + cArg + "' is not part of the tontine's vocabulary" ok
	return "the words are known but no question has this shape: " + cArg

func NlqIsDigits cS
	if len(cS) = 0 or len(cS) > 12 return false ok
	for i = 1 to len(cS)
		n = ascii(cS[i])
		if n < 48 or n > 57 return false ok
	next
	return true

func NlqJoin aList, cSep
	cOut = ""
	for i = 1 to len(aList)
		if i > 1 cOut += cSep ok
		cOut += aList[i]
	next
	return cOut

# the name the LEDGER spells a member with; a graph pattern uses the id. The graph artifact keeps ids
# only (node properties do not survive it -- E1), so the ledger's spelling is a convention here:
# the first letter, upper-cased. Held for all six members; it is a finding, not a design.
func NlqDisplay cId, cKind
	if cKind = "graph" return cId ok
	return upper(left(cId, 1)) + substr(cId, 2)

# ---- the answer OUT: a sentence in the language of the question, from templates (DATA) -------------------
# [frame, language, sentence when someone answers, sentence when no one does]   {A} the answer, capitalised
# and joined; {NUM} {MEMBER} the question's own slots; {ROLEW} the role in the language's word

func NlqSayTemplates
	return [
		["graph-pot", "tn-en", "{A} received the pot in round {NUM}.", "Nobody received the pot in round {NUM}."],
		["graph-pot", "tn-fr", "{A} a reçu la cagnotte au tour {NUM}.", "Personne n'a reçu la cagnotte au tour {NUM}."],
		["graph-guarantor", "tn-en", "{A} guarantees {MEMBER}.", "Nobody guarantees {MEMBER}."],
		["graph-guarantor", "tn-fr", "{A} se porte garant de {MEMBER}.", "Personne ne se porte garant de {MEMBER}."],
		["graph-guaranteed-by", "tn-en", "{MEMBER} guarantees {A}.", "{MEMBER} guarantees nobody."],
		["graph-guaranteed-by", "tn-fr", "{MEMBER} se porte garant de {A}.", "{MEMBER} ne se porte garant de personne."],
		["graph-role", "tn-en", "The {ROLEW} is {A}.", "Nobody is the {ROLEW}."],
		["graph-role", "tn-fr", "Le {ROLEW} est {A}.", "Personne n'est {ROLEW}."],
		["plan-beneficiary-deposits", "tn-en", "The beneficiary of round {NUM} is {A}.", "Nobody received the pot in round {NUM}, so there is no beneficiary."],
		["plan-beneficiary-deposits", "tn-fr", "Le bénéficiaire du tour {NUM} est {A}.", "Personne n'a reçu la cagnotte au tour {NUM} : il n'y a pas de bénéficiaire."]
	]

func NlqRoleWord cLang, cRole
	for aRw in NlqRoleWords(cLang)
		if aRw[2] = cRole return aRw[1] ok
	next
	return cRole

func NlqSay cLang, cFrame, aAns, aSlots
	for aT in NlqSayTemplates()
		if aT[1] = cFrame and aT[2] = cLang
			if len(aAns) = 0
				cOut = aT[4]
			else
				cOut = aT[3]
			ok
			aNames = []
			for cId in aAns
				aNames + NlqDisplay(cId, "ledger")
			next
			cAnd = " and "
			if cLang = "tn-fr" cAnd = " et " ok
			cJoined = ""
			for i = 1 to len(aNames)
				if i > 1
					if i = len(aNames)
						cJoined += cAnd
					else
						cJoined += ", "
					ok
				ok
				cJoined += aNames[i]
			next
			cOut = substr(cOut, "{A}", cJoined)
			for aS in aSlots
				if aS[1] = "NUM" cOut = substr(cOut, "{NUM}", aS[2]) ok
				if aS[1] = "MEMBER" cOut = substr(cOut, "{MEMBER}", NlqDisplay(aS[2], "ledger")) ok
				if aS[1] = "ROLE" cOut = substr(cOut, "{ROLEW}", NlqRoleWord(cLang, aS[2])) ok
			next
			return cOut
		ok
	next
	return ""

# ---- run a closed graph pattern ------------------------------------------------------------------------

func NlqRunPattern cPattern
	# cPattern is the template text '["?x", "p", "o"]': read it as DATA, never evaluated
	aParts = NlqParsePattern(cPattern)
	if len(aParts) != 3 return ["refused: not a triple pattern"] ok
	return $oNlqGraph.Query(aParts)

func NlqParsePattern cP
	cP = trim(cP)
	cP = substr(cP, "[", "")
	cP = substr(cP, "]", "")
	aOut = []
	for cPart in split(cP, ",")
		cPart = trim(cPart)
		cPart = substr(cPart, '"', "")
		aOut + cPart
	next
	return aOut
