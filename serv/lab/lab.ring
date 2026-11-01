# THE SOFTANZA LAB -- shared code in HaroServer's base: a page that runs Softanza's own
# narrated assertions live on the server, a playground, and the endpoints the web
# comparison measures (haro/serv/bench/webbench.py). Deployed by lab/lab.py, before
# Softanza itself, so the page answers while the library compiles in the background:
#
#     POST /base/lab    this file, with $cLabDir = the folder that holds it, put first
#     POST /base/stz    load "stzlib.ring" -- Softanza's library (rung 9: the loop serves on)
#
# A check is code POST /run admits, calls and releases (`func Run` returning
# LabThen(actual, expected)); the lab only judges it, as the suite's Then does.
# What it calls of Softanza before Softanza is admitted reaches it once it is
# (the late link, rung 1).

RouteAs("GET", "/lab", "LabPage", "text/html; charset=utf-8")
RouteAs("GET", "/lab/checks", "LabChecks", "application/json; charset=utf-8")
RouteAs("GET", "/lab/results", "LabResults", "application/json; charset=utf-8")
RouteAs("GET", "/lab/verdicts", "LabVerdicts", "application/json; charset=utf-8")
Route("GET", "/bench/hello", "BenchHello")
Route("GET", "/bench/text", "BenchText")
Route("GET", "/bench/textring", "BenchTextRing")
Route("GET", "/bench/primes", "BenchPrimes")

$cLabText = LabText()

# the text the text workload works on: nine words, twenty times, one space between
func LabText
	cText = ""
	for i = 1 to 20
		if i > 1
			cText += " "
		ok
		cText += "the quick brown fox jumps over the lazy dog"
	next
	return cText

func LabPage cBody
	return read($cLabDir + "/lab.html")

func LabChecks cBody
	return read($cLabDir + "/checks.json")

func LabResults cBody
	return LabJsonFile("results.json")

# Ring's answer to every check, taken by lab/verdicts.py on the oracle
func LabVerdicts cBody
	return LabJsonFile("verdicts.json")

func LabJsonFile cName
	cFile = $cLabDir + "/" + cName
	if fexists(cFile)
		return read(cFile)
	ok
	return "null"

# a narrated assertion, decided as base/test/_narrated.ring decides it: `=`, and
# @@ to show what was expected and what came
func LabThen xActual, xExpected
	if xActual = xExpected
		return "PASS"
	ok
	return "FAIL" + char(10) + @@(xExpected) + char(10) + @@(xActual)

# what the playground shows: a string as it is, anything else as Softanza shows it
func LabShow vValue
	if isString(vValue)
		return vValue
	ok
	return @@(vValue)

# ---- the web comparison's workloads, served alike by every server it measures ----

func BenchHello cBody
	return "hello"

# Softanza: the text upper-cased, its number of words, its words in reverse order
func BenchText cBody
	oText = Q($cLabText)
	return oText.Uppercased() + char(10) + oText.NumberOfWords() + char(10) + Q(Q(oText.Words()).Reversed()).Joined(" ")

# the same answer in plain Ring, without Softanza
func BenchTextRing cBody
	aWords = split($cLabText, " ")
	cRev = ""
	for i = len(aWords) to 1 step -1
		cRev += aWords[i]
		if i > 1
			cRev += " "
		ok
	next
	return upper($cLabText) + char(10) + len(aWords) + char(10) + cRev

# the primes below 20,000, counted by a sieve
func BenchPrimes cBody
	n = 20000
	aSieve = list(n)
	nCount = 0
	for i = 2 to n - 1
		if aSieve[i] = 0
			nCount++
			for j = i * i to n - 1 step i
				aSieve[j] = 1
			next
		ok
	next
	return "" + nCount
