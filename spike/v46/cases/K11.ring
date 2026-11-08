o = new P
p = obj2ptr(o)
? type(p)
o2 = ptr2obj(p)
o2.x = 7
? o.x
class P
	x = 1
