class Plan
	def Owns(pcVerb)
		return ring_find([ "lockaccount" ], lower("" + pcVerb)) > 0

	def LockAccount(pcTarget)
		This._Auth().LockAccount("" + pcTarget, "locked")

	def RevokeSession(pcTarget)
		if pcTarget = "" return 0 ok
		return 1
