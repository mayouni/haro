# an app that answers with what it was sent, after the first file -- a new
# CLASS admitted while the server runs
Route("POST", "/echo", "EchoApp")

func EchoApp cBody
	return new Echoer().Say(cBody)

class Echoer
	def Say c
		return "echo " + len(c) + " byte(s): " + c
