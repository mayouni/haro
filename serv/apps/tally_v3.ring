# the tally app redeployed with an attribute added: the running object was
# laid out without it, and takes it at its first use, starting as declared
# (the resident VM's rung 7) -- the tally it holds is kept
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
