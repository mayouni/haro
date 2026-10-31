# the tally app redeployed: a new answer for GET and for Total, the same
# object -- its top level does not make a new one, so the tally is kept
Route("GET", "/tally", "TallyGet")

func TallyGet cBody
	return "tally " + $oTally.Total() + " (v2)"

class Tally
	nTotal = 0
	def Add n
		nTotal += n
	def Total
		return nTotal
