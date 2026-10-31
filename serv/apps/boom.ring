# an app whose handler raises: the request answers 500, the server goes on
Route("GET", "/boom", "BoomApp")

func BoomApp cBody
	raise("the boom app said no")
