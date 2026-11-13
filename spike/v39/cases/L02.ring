f()
func f
	try
		raise("x")
	catch
		c = 1
	done
	? cCatchError
