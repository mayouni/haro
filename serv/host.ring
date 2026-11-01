# HAROSERVER, THE HOST LOOP -- one live program that takes its apps and its
# requests itself, on the resident VM (rnxc resident, rungs 1 to 6). RingServ's
# design, from its lesson (CLAUDE.md, "RINGSERV ON RING++"): one resident
# program, apps arriving as code that defines functions and classes, every
# request a call into the same live program -- here with the deployment a
# request too, and the loop the program's own.
#
#     rnxc resident host.ring            (HAROSERV_PORT, default 8642)
#
#   POST /admit/<app>?<exports>
#                          the body is the app's source, admitted into the running
#                          program as a NAMESPACE of its own (admitapp, D31): its
#                          functions, classes and globals are its own, it reads the
#                          base's after its own, and another app reaches it only
#                          through the names it exports -- the query, comma-separated
#                          (`?Entry,Sum`), spelt `app.Name` by the other app: 201,
#                          or 422 and the reason
#   POST /replace/<app>    the body REPLACES what the app defined (replaceapp):
#                          every request after it runs the new code, and what the
#                          app holds -- its objects -- is kept: 201, or 422
#   POST /base/<name>      the body is admitted into the BASE (admitcode) -- what
#                          every app reads after its own names, Softanza's library
#                          for one: 201, or 422
#                          EVERY DEPLOYMENT COMPILES IN THE BACKGROUND (rung 9):
#                          the loop serves on while it does, and installs it
#                          between two requests. Answered with its outcome when
#                          that is known within $nDeployWait ms -- a small app's
#                          is -- and otherwise 202; one that arrives while another
#                          compiles is queued behind it, 202 too
#   GET  /deploy/<name>    where that deployment stands: 202 "compiling" or
#                          "queued", 200 "admitted ...", 422 and the reason, 404
#   POST /run?<input>      the body is code that defines `func Run cInput`: admitted,
#                          called with what followed `?`, and RELEASED (releasecode,
#                          rung 6) -- the program after the request is the program
#                          before it: 200 and what Run returned, 500 and its error,
#                          422 when it could not be admitted -- or released: code
#                          that defines a class or a lambda stays, and says so;
#                          503 while a deployment compiles (one compiles at a time)
#   GET  /stats            requests served, deployments admitted and refused, runs
#                          released, routes, the program's functions
#   POST /stop             answers, then the loop ends
#   anything else          the route an app registered for its method and path,
#                          called by name with the request's body: 200 and what
#                          it returned, 500 and the error, or 404
#
# An app registers its routes when its top level runs, by its handler's name in
# the app -- the host keeps it as `app::Handler`, which only the host may call:
#     Route("GET", "/hello", "HelloApp")

$aRoutes = []
$cDeploying = ""
# deployments: the one compiling in the background, by name and verb; those queued
# behind it, [verb, name, source, exports]; and where each name's last one stands,
# [name, state, answer] -- "queued", "compiling", "admitted" or "refused"
$cCompiling = ""
$cCompilingVerb = ""
$aQueue = []
$aDeploys = []
# how long a deployment request waits for its compile before answering 202
$nDeployWait = 50
$nServed = 0
$nAdmitted = 0
$nRefused = 0
$nRuns = 0

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
	while true
		# with a deployment under way the wait is short, so a compile that ends
		# while nobody asks is installed within ~10 ms all the same
		if $cCompiling != ""
			nGot = rpp_http_next(10)
		else
			nGot = rpp_http_next()
		ok
		if nGot = 0
			exit
		ok
		Advance()
		if nGot < 0
			loop
		ok
		$nServed++
		cMethod = rpp_http_method()
		cPath = rpp_http_path()
		if cMethod = "POST" and left(cPath, 7) = "/admit/"
			Deploy("admitapp", substr(cPath, 8), rpp_http_body(), Exports(rpp_http_query()))
		but cMethod = "POST" and left(cPath, 9) = "/replace/"
			Deploy("replaceapp", substr(cPath, 10), rpp_http_body(), [])
		but cMethod = "POST" and left(cPath, 6) = "/base/"
			Deploy("admitcode", substr(cPath, 7), rpp_http_body(), [])
		but cMethod = "GET" and left(cPath, 8) = "/deploy/"
			Answer(substr(cPath, 9), 200)
		but cMethod = "POST" and cPath = "/run"
			RunOnce(rpp_http_body(), rpp_http_query())
		but cMethod = "GET" and cPath = "/stats"
			rpp_http_reply(200, "text/plain", Stats())
		but cMethod = "POST" and cPath = "/stop"
			rpp_http_reply(200, "text/plain", "stopping")
			exit
		else
			Dispatch(cMethod, cPath, rpp_http_body())
		ok
	end

# a deployment: an app's code admitted into a namespace of its own
# (admitapp), replacing what it defined (replaceapp), or shared code admitted
# into the base (admitcode) -- compiled in the background while the loop
# serves, a refusal leaving the program exactly as it was. Queued behind the
# one compiling; otherwise started, and answered with its outcome when that
# is known within $nDeployWait ms, else 202
func Deploy cVerb, cName, cSource, aExports
	if $cCompiling != ""
		add($aQueue, [cVerb, cName, cSource, aExports])
		Record(cName, "queued", "queued " + cName)
		rpp_http_reply(202, "text/plain", "queued " + cName)
		return
	ok
	Start(cVerb, cName, cSource, aExports)
	if $cCompiling = cName and admitstate($nDeployWait) = "compiled"
		Finish()
	ok
	Answer(cName, 201)

func Start cVerb, cName, cSource, aExports
	try
		if cVerb = "admitapp"
			admitstart(cVerb, cName, cSource, aExports)
		else
			admitstart(cVerb, cName, cSource)
		ok
		$cCompiling = cName
		$cCompilingVerb = cVerb
		Record(cName, "compiling", "compiling " + cName)
	catch
		$nRefused++
		Record(cName, "refused", cCatchError)
	done

# the deployment compiled: installed, its top level run -- an app's routes are
# registered as the app's (Route) -- or refused, as the verb would have been
func Finish
	cName = $cCompiling
	cVerb = $cCompilingVerb
	$cCompiling = ""
	if cVerb != "admitcode"
		$cDeploying = cName
	ok
	try
		admitfinish()
		$nAdmitted++
		if cVerb = "admitcode"
			Record(cName, "admitted", "admitted " + cName + " into the base")
		else
			Record(cName, "admitted", "admitted " + cName)
		ok
	catch
		$nRefused++
		Record(cName, "refused", cCatchError)
	done
	$cDeploying = ""

# between two requests: a compile that is over is installed, and the next
# queued deployment starts
func Advance
	if $cCompiling != "" and admitstate() = "compiled"
		Finish()
	ok
	while $cCompiling = "" and len($aQueue) > 0
		aD = $aQueue[1]
		del($aQueue, 1)
		Start(aD[1], aD[2], aD[3], aD[4])
	end

func Record cName, cState, cAnswer
	for i = 1 to len($aDeploys)
		if $aDeploys[i][1] = cName
			$aDeploys[i][2] = cState
			$aDeploys[i][3] = cAnswer
			return
		ok
	next
	add($aDeploys, [cName, cState, cAnswer])

# where a deployment stands, as an answer: nAdmitted when it is admitted (201
# to the request that made it, 200 to GET /deploy/<name>), 202 under way, 422
func Answer cName, nAdmitted
	for i = 1 to len($aDeploys)
		if $aDeploys[i][1] = cName
			cState = $aDeploys[i][2]
			if cState = "admitted"
				rpp_http_reply(nAdmitted, "text/plain", $aDeploys[i][3])
			but cState = "refused"
				rpp_http_reply(422, "text/plain", $aDeploys[i][3])
			else
				rpp_http_reply(202, "text/plain", $aDeploys[i][3])
			ok
			return
		ok
	next
	rpp_http_reply(404, "text/plain", "no deployment " + cName)

# `Entry,Sum` -> ["Entry", "Sum"]
func Exports cQuery
	aOut = []
	cCur = ""
	for i = 1 to len(cQuery)
		if cQuery[i] = ","
			if cCur != "" add(aOut, cCur) ok
			cCur = ""
		else
			cCur += cQuery[i]
		ok
	next
	if cCur != "" add(aOut, cCur) ok
	return aOut

# code that comes with a request and leaves with it: admitted, run, released.
# The release comes before the reply, so a refusal to release is the answer;
# what Run returned outlives the code that made it (its constants included)
func RunOnce cSource, cInput
	if $cCompiling != ""
		rpp_http_reply(503, "text/plain", "a deployment is compiling (" + $cCompiling + "); one admission at a time")
		return
	ok
	try
		admitcode("run", cSource)
	catch
		$nRefused++
		rpp_http_reply(422, "text/plain", cCatchError)
		return
	done
	nStatus = 200
	try
		cOut = "" + Run(cInput)
	catch
		nStatus = 500
		cOut = cCatchError
	done
	try
		releasecode("run")
		$nRuns++
	catch
		nStatus = 422
		cOut = cCatchError
	done
	rpp_http_reply(nStatus, "text/plain", cOut)

func Route cMethod, cPath, cHandler
	if $cDeploying != "" and substr(cHandler, "::") = 0
		cHandler = $cDeploying + "::" + cHandler
	ok
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
	return "served " + $nServed + nl + "admitted " + $nAdmitted + nl + "refused " + $nRefused + nl + "runs released " + $nRuns + nl + "routes " + len($aRoutes) + nl + "functions " + len(functions()) + nl + "queued " + len($aQueue)
