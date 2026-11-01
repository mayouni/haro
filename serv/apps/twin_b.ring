# the other twin: the same function names, its own answers
Route("GET", "/twin_b", "Greet")

func Greet cBody
	return Name() + " answers"

func Name
	return "twin b"
