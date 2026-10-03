# e2_stznatural.ring -- Phase 1.5, experiment E2: stzNatural AS SHIPPED, then with the tontine's
# vocabulary added as DATA, asked to be the natural-language surface of the tontine.
#
#   E2a  a tontine question, executed as shipped                   (does it refuse?)
#   E2b  the same under strict mode                                 (does it say what it did not understand?)
#   E2c  the tontine vocabulary as two language packs, data only    (do two languages give ONE semantic form?)
#   E2d  text with a bracketed section, in a dry run                (is the front end closed?)
#
# Run on the Ring++ package: rnxc.exe e2_stznatural.ring

load "stzlib.ring"
load "nlq.ring"

$nMarker = 0

# --- E2a / E2b: as shipped -----------------------------------------------------------------------
? "E2a " + Probe('NaturallyIn("en", "show deposits over 5000")')
? "E2a " + Probe('NaturallyIn("fr", "montre les depots au dessus de 5000")')
? "E2b " + Probe('NaturallyStrictIn("en", "show deposits over 5000", ["METHOD_UPPERCASE"])')

# --- E2c: the vocabulary as data ---------------------------------------------------------------------
NlqLoadWorld("data/tontine.zknw")

aPairs = [
	["show deposits over 5000",             "montre les depots au dessus de 5000"],
	["who received the pot in round 2",     "qui a reçu la cagnotte au tour 2"],
	["who is the treasurer",                "qui est le trésorier"]
]
nSame = 0
for aP in aPairs
	cEn = SemanticForm("tn-en", aP[1])
	cFr = SemanticForm("tn-fr", aP[2])
	? "E2c [" + aP[1] + "] -> " + cEn
	? "E2c [" + aP[2] + "] -> " + cFr
	if cEn = cFr nSame++ ok
next
? "E2c pairs with one semantic form in both languages: " + nSame + " of " + len(aPairs)

# --- E2d: the front end and a bracketed section ----------------------------------------------------
? "E2d plain:     " + SemanticForm("tn-en", "show deposits over 5000") + "   marker=" + $nMarker
? "E2d quoted:    " + SemanticForm("tn-en", 'show deposits over "Marker()"') + "   marker=" + $nMarker
? "E2d bracketed: " + SemanticForm("tn-en", "show deposits over [ Marker() ]") + "   marker=" + $nMarker

func SemanticForm cLang, cText
	oE = new stzNaturalEngine(cLang, "", [], "")
	oE.Analyze(cText)
	cOut = ""
	for aT in oE.Tokens()
		if cOut != "" cOut += " " ok
		cOut += aT[:type] + ":" + aT[:value]
	next
	return cOut

func Probe cCode
	try
		eval("vR = " + cCode)
		return "returned"
	catch
		return "RAISED " + cCatchError
	done

func Marker
	$nMarker++
	return 5000
