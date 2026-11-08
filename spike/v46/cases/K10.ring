o1 = new P
o2 = new P
p1 = object2pointer(o1)
p2 = object2pointer(o1)
p3 = object2pointer(o2)
? ptrcmp(p1, p2)
? ptrcmp(p1, p3)
? pointercompare(p1, p2)
class P
	x = 1
