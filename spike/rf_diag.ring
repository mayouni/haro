# rf_diag.ring -- RingFlex's own court, asked for its C2 envelope on every
# fixture and on the boundary workflow against each world fixture. Run by the
# guard's stage 14 under official Ring 1.27 with RingFlex's root as the working
# directory, READ-ONLY: it loads src/wflow.ring and src/placement.ring from
# there and writes nothing. Prints one line per file: <name><TAB><C2 JSON>.
# The guard compares the codes, lines and cites with the forged court's on the
# same fixtures re-expressed in the Commons' shape (haro/spike/f/).

load "stdlib.ring"
load "src/wflow.ring"
load "src/placement.ring"

func main
	aD = dir("fixtures")
	aNames = []
	for i = 1 to len(aD)
		if aD[i][2] = 0 and right(aD[i][1], 6) = ".wflow" aNames + aD[i][1] ok
	next
	aNames = sort(aNames)
	for i = 1 to len(aNames)
		cPath = "fixtures/" + aNames[i]
		aDiags = WflowDiagnose(cPath, read(cPath))
		see aNames[i] + char(9) + OneLine(WflowDiagnosticsJson(aDiags)) + nl
	next
	cB = "fixtures/boundary-invokes-flow.wflow"
	o = WflowParse(read(cB))
	aWorlds = ["world", "world-missing-flow", "world-missing-compensating", "absent"]
	for i = 1 to len(aWorlds)
		aR = WflowResolve(o, WorldLoad("fixtures/world/" + aWorlds[i] + ".json"), cB)
		see "resolve:" + aWorlds[i] + char(9) + OneLine(WflowDiagnosticsJson(aR)) + nl
	next

func OneLine(cS)
	cOut = ""
	for i = 1 to len(cS)
		if cS[i] != char(10) and cS[i] != char(13) cOut += cS[i] ok
	next
	return cOut
