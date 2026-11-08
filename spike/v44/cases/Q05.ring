f()
func f
	s = "abc"
	s[2] = "x"
	? s
	t = s
	s[1] = "z"
	? t
	? s
	s[3] = 66
	? s
	? len(s)
