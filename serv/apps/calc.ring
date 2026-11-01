# an app that reaches another app's exported function by its public name, and fails on one it keeps
Route("GET", "/calc", "Calc")
Route("GET", "/peek", "Peek")

func Calc cBody
	return "2 + 3 = " + sum.Sum(2, 3)

func Peek cBody
	return sum.Secret()
