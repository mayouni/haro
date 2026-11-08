$aTV = []
$bOn = 1
oA = new O
oA.Add()
oA.Add()
? len(oA.Vals())
$bOn = 0
for i = 1 to 3
	try
		oA.Add()
	catch
		? "caught"
	done
next
? len(oA.Vals())
s = "banana"
aCopy = oA.Vals()
? len(aCopy)
$aTV + 5
? len($aTV)
? "done"
class O
	def Add()
		$aTV + This.T()
	def T()
		if $bOn = 0
			raise("off")
		ok
		return 1
	def Vals()
		return $aTV
