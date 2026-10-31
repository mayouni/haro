# an app: a route and its handler
Route("GET", "/hello", "HelloApp")

func HelloApp cBody
	return "hello from HaroServer"
