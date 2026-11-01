# an app that exports a function (deployed as /admit/sum?Sum) and keeps another to itself
func Sum a, b
	return a + b

func Secret
	return "kept"
