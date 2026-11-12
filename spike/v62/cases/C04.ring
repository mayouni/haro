oBox = new Box
hB = object2pointer(oBox)
f(hB)
? oBox.nVal
func f hX
	? pointer2object(hX).nVal
	oU = pointer2object(hX)
	oU.nVal = 5
class Box
	nVal = 1
