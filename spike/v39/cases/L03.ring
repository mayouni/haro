f()
func f
	try
		raise("x")
	catch e
		? e
	done
	try
		raise("y")
	catch cCatchError
		? "bound"
	done
	cCatchError = ""
	o = new K
	? o.cCatchError
class K
	cCatchError = "an attribute"
