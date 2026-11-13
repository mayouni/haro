f()
func f
	nH = StzEngineCacheCreate(8)
	try
		use(nH)
	finally
		StzEngineCacheDestroy(nH)
	done
func StzEngineCacheCreate n
	return 1
func StzEngineCacheDestroy n
	return 0
func use n
	return 0
