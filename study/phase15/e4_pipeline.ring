# e4_pipeline.ring -- Phase 1.5, experiment E4: questions in two human languages, compiled to closed
# queries, the graph ones answered, the ledger ones handed (as text) to the ledger's court.
#
#   rnxc.exe e4_pipeline.ring <questions.txt> [world.zknw]    one question per line:  id|lang|text   (newline in text: ~NL~)
#
# prints, one per question (fields separated by TAB):
#   RESULT id kind target reason frame
#   ANSWER id <ids...>                  a graph pattern's answer, ids as the graph spells them
#   PLAN   id <step-1 ids> <ZQL>        a plan: the graph's answer, then the ledger question built from it
#   SAY    id <sentence>                the graph answer told in the language of the question

load "stzlib.ring"
load "nlq.ring"

cFile = sysargv[3]
cT = char(9)

# the canary: a function a question might try to call. If a question's text ever runs as code, this runs.
$nMarker = 0

# the world artifact: data/tontine.zknw beside this file, or the path given as the second argument
cWorld = "data/tontine.zknw"
if len(sysargv) >= 4
	cWorld = sysargv[4]
ok
NlqLoadWorld(cWorld)

for cLine in split(read(cFile), nl)
	cLine = trim(cLine)
	if len(cLine) = 0 loop ok
	# fields are id|lang|text, split by hand: Ring's split(s, char(9)) splits on ALL whitespace (both
	# runtimes agree), and a question may hold anything. A newline in a question travels as ~NL~
	nP1 = substr(cLine, "|")
	cId = left(cLine, nP1 - 1)
	cRest = substr(cLine, nP1 + 1)
	nP2 = substr(cRest, "|")
	cLang = left(cRest, nP2 - 1)
	cText = substr(substr(cRest, nP2 + 1), "~NL~", nl)
	aR = NlqCompile(cLang, cText)
	? "RESULT" + cT + cId + cT + aR[1] + cT + aR[2] + cT + aR[3] + cT + aR[4]
	if aR[1] = "graph"
		aAns = NlqRunPattern(aR[2])
		? "ANSWER" + cT + cId + cT + NlqJoin(aAns, ",")
		? "SAY" + cT + cId + cT + NlqSay(cLang, aR[4], aAns, aR[5])
	elseif aR[1] = "plan"
		aBoth = split(aR[2], " => ")
		aAns = NlqRunPattern(aBoth[1])
		cZql = ""
		if len(aAns) = 1
			cZql = substr(aBoth[2], "{MEMBER}", NlqDisplay(aAns[1], "ledger"))
		ok
		? "PLAN" + cT + cId + cT + NlqJoin(aAns, ",") + cT + cZql
		? "SAY" + cT + cId + cT + NlqSay(cLang, aR[4], aAns, aR[5])
	ok
next

? "CANARY" + cT + $nMarker

func Marker
	$nMarker++
	return 5000
