oP = new Point
p = object2pointer(oP)
? type(p)
? isPointer(p)
o2 = pointer2object(p)
o2.x = 5
? oP.x
? type(o2)
p2 = object2pointer(oP)
? p = p2
? isNull(p)
class Point
	x = 1
