# the tally app redeployed with an attribute added: the running object was
# laid out without it, so the resident VM refuses the replacement
Route("GET", "/tally", "TallyGet")

func TallyGet cBody
	return "tally " + $oTally.Total() + " in " + $oTally.nAdds + " add(s)"

class Tally
	nTotal = 0
	nAdds = 0
	def Add n
		nTotal += n
		nAdds++
	def Total
		return nTotal
