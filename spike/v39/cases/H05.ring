$o = new Token
$o.Open()
func StzEngineCancelCreate
	return 1
func StzEngineCancelDestroy n
	return 0
class Token
	pHandle = 0
	func Open
		pHandle = StzEngineCancelCreate()
	func Release
		StzEngineCancelDestroy(pHandle)
