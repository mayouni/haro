# an app that reads a top-level name bare in a function: Rule A refuses it,
# and the program stays as it was
nLimit = 3
Route("GET", "/bad", "BadApp")

func BadApp cBody
	return nLimit
