f(2)
func f n
	for i = 1 to n
		if i = 1 put "a" but i = 2 see "b" ok
	next
	switch n on 2 put "c" other put "d" off
	try raise("e") catch put "f" done
	if 1 && !0 { put "g" }
	put nl
end
