o = new K
? "A"
-o - 3
? "B"
-(o - 3)
? "C"
(-o) - 3
? "D"
-o + 1 - 2
? "E"
-(o + 1 - 2)
? "F"
((-o) + 1) - 2
class K
	func operator cOp, v
		? "   op " + cOp
		return This
