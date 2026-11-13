$g = "a"
f()
func f
	cOld = $g
	try
		$g = "b"
	finally
		$g = cOld
	done
	within $g = "c"
		? $g
	done
