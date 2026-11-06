$g = "a"
f()
func f
	cOld = $g
	$g = "b"
	try
		work()
	catch e
		$g = cOld
		raise(e)
	done
	$g = cOld
func work
	return 0
