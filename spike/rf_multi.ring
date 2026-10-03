# rf_multi.ring -- RingFlex's own court, asked for every finding on the files
# named on the command line (the .wflow twins of v14/multi). Run by the guard's
# stage 17 under official Ring 1.27 with RingFlex's root as the working
# directory, READ-ONLY: it loads src/wflow.ring from there and writes nothing.
# Prints one line per file: <path><TAB><C2 JSON>.

load "stdlib.ring"
load "src/wflow.ring"

func main
	for i = 3 to len(sysargv)
		cPath = sysargv[i]
		aDiags = WflowDiagnose(cPath, read(cPath))
		see cPath + char(9) + OneLine(WflowDiagnosticsJson(aDiags)) + nl
	next

func OneLine(cS)
	cOut = ""
	for i = 1 to len(cS)
		if cS[i] != char(10) and cS[i] != char(13) cOut += cS[i] ok
	next
	return cOut
