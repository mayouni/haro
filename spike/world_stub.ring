# world_stub.ring -- what a court whose language declares no SYMBOL and no PUBLISH has of a
# world: nothing (Haro v0.14). It stands where world_lib.ring would, so the court's own calls
# resolve, and costs the compiler a handful of lines instead of a hundred (HF-49).
# Functions only; the globals are the generated court's.

func CtSymbolByName(cName)
	return NULL

func CtSymbolSites(aDecls)
	return []

func CtResolveWorld(aDecls)
	return

func CtSymbolCode(aSy)
	return ["UNRESOLVED", []]

func CtWorldStem(cPath)
	return cPath

func CtWorldLoad(cPath)
	CtFail(1, "this language declares no SYMBOL and no PUBLISH, so it has no world to read")

func CtWorldRows(aDecls, cFile)
	CtFail(1, "this language declares no SYMBOL and no PUBLISH, so it publishes no world")
