# HAROSERVER, THE HOST LOOP -- one live program that takes its apps and its
# requests itself, on the resident VM (rnxc resident, rungs 1 to 5). RingServ's
# design, from its lesson (CLAUDE.md, "RINGSERV ON RING++"): one resident
# program, apps arriving as code that defines functions and classes, every
# request a call into the same live program -- here with the deployment a
# request too, and the loop the program's own.
#
#     rnxc resident host.ring            (HAROSERV_PORT, default 8642)
#
#   POST /admit/<app>      the body is the app's source, admitted into the running
#                          program (admitcode): 201, or 422 and the reason
#   POST /replace/<app>    the body REPLACES what the app defined (replacecode):
#                          every request after it runs the new code, and what the
#                          app holds -- its objects -- is kept: 201, or 422
#   GET  /stats            requests served, deployments admitted and refused, routes
#   POST /stop             answers, then the loop ends
#   anything else          the route an app registered for its method and path,
#                          called by name with the request's body: 200 and what
#                          it returned, 500 and the error, or 404
#
# An app registers its routes when its top level runs:
#     Route("GET", "/hello", "Hello")

$aRoutes = []
$nServed = 0
$nAdmitted = 0
$nRefused = 0

cPort = sysget("HAROSERV_PORT")
nPort = 8642
if cPort != ""
	nPort = 0 + cPort
ok
if rpp_http_listen(nPort)
	? "haroserv: listening on 127.0.0.1:" + nPort
	ServeLoop()
	? "haroserv: stopped after " + $nServed + " request(s), " + $nAdmitted + " deployment(s) admitted, " + $nRefused + " refused"
else
	? "haroserv: port " + nPort + " is not ours"
ok

func ServeLoop
	while rpp_http_next()
		$nServed++
		cMethod = rpp_http_method()
		cPath = rpp_http_path()
		if cMethod = "POST" and left(cPath, 7) = "/admit/"
			Deploy(substr(cPath, 8), rpp_http_body(), false)
		but cMethod = "POST" and left(cPath, 9) = "/replace/"
			Deploy(substr(cPath, 10), rpp_http_body(), true)
		but cMethod = "GET" and cPath = "/stats"
			rpp_http_reply(200, "text/plain", Stats())
		but cMethod = "POST" and cPath = "/stop"
			rpp_http_reply(200, "text/plain", "stopping")
			exit
		else
			Dispatch(cMethod, cPath, rpp_http_body())
		ok
	end

# a deployment: the app's code admitted, or replacing what it defined, while
# the program runs -- a refusal leaves the program exactly as it was
func Deploy cApp, cSource, bReplace
	try
		if bReplace
			replacecode(cApp, cSource)
		else
			admitcode(cApp, cSource)
		ok
		$nAdmitted++
		rpp_http_reply(201, "text/plain", "admitted " + cApp)
	catch
		$nRefused++
		rpp_http_reply(422, "text/plain", cCatchError)
	done

func Route cMethod, cPath, cHandler
	for i = 1 to len($aRoutes)
		if $aRoutes[i][1] = cMethod and $aRoutes[i][2] = cPath
			$aRoutes[i][3] = cHandler
			return
		ok
	next
	add($aRoutes, [cMethod, cPath, cHandler])

func Dispatch cMethod, cPath, cBody
	for i = 1 to len($aRoutes)
		if $aRoutes[i][1] = cMethod and $aRoutes[i][2] = cPath
			cHandler = $aRoutes[i][3]
			try
				vOut = call cHandler(cBody)
				rpp_http_reply(200, "text/plain", "" + vOut)
			catch
				rpp_http_reply(500, "text/plain", cCatchError)
			done
			return
		ok
	next
	rpp_http_reply(404, "text/plain", "no route for " + cMethod + " " + cPath)

func Stats
	return "served " + $nServed + nl + "admitted " + $nAdmitted + nl + "refused " + $nRefused + nl + "routes " + len($aRoutes)
