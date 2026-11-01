# two apps that define the same names -- a handler and a helper -- and never meet (D31)
Route("GET", "/twin_a", "Greet")

func Greet cBody
	return Name() + " answers"

func Name
	return "twin a"
