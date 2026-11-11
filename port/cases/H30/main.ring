f(2)
func f n
	for i = 1 to n
		if i = 1 put "a" but i = 2 see "b" ok
	next
	switch n on 2 put "c" other put "d" off
	try raise("e") catch put "f" done
	if n = 2 && !(n = 3) { put "g" }
	put char(10)
end
