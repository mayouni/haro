f()
func f
	aSeen = []
	aSeen["a"] = 1
	for i = 1 to 3
		x = aSeen["b"]
		? isString(x) + len(x)
		x = 5
		? x
	next
	? aSeen["a"]
