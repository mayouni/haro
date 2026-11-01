# the class apps/ledger.ring makes -- deployed after it, exporting Entry
class Entry
	cWhat = ""
	nAmount = 0

	def init w, n
		cWhat = w
		nAmount = n

	def Show
		return cWhat + ": " + nAmount
