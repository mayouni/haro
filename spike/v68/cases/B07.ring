load "bools.haro"
cOut = ""
for x in Mixed()
	cOut += Fmt(x) + " "
next
? cOut
func Fmt x
	if isNumber(x) return "N" + x
	but isString(x) return "S" + x
	ok
	raise("Unsupported value type")
