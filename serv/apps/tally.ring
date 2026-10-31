# an app that holds state: one object for the server's life
$oTally = new Tally
Route("POST", "/tally", "TallyAdd")
Route("GET", "/tally", "TallyGet")

func TallyAdd cBody
	$oTally.Add(0 + cBody)
	return $oTally.Total()

func TallyGet cBody
	return $oTally.Total()

class Tally
	nTotal = 0
	def Add n
		nTotal += n
	def Total
		return nTotal
