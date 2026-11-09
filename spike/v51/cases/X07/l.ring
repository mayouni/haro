func f o
	o.run()
	q = func x { return g(x) }
	return call q(1)
func g n
	return n
class A
	func run
		return 1
class B
	func run
		return 2
