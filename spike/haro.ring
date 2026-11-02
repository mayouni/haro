# haro.ring -- `rnxc haro.ring <file.haro>`: judge a language declaration
# with the stzu v0.1 meta-court, in pure core Ring, on rnx or on the oracle.
#
# Prints "ok" and the structural fields on acceptance, or the one refusal
# line "stzu (line N): message". The spike's first act: the declaring
# altitude of Haro, judged by the same fixtures as the Luau meta-court.
#
# sysargv is [interpreter, script, args...] on both runtimes, so the file
# is sysargv[3]. The two parse-state globals are born here, at the top
# level, because on Ring a `$name` first assigned inside a function is
# that function's local (C-2's own note), and on Ring++ `$` is the global.

load "haro_lib.ring"

$aStzuToks = []
$aStzuUnions = []
$nStzuPos = 1
$aCondToks = []
$nCondPos = 1
$aCondDeclSeats = []
$aCondDecls = []
$aCondVerbOf = []
$cCondOther = ""
$aCondRefSeats = []
$aCondFormats = []
$bCondUnread = 0
$aCondLangs = []
$cCondLang = ""
$aCourtSentences = []
$cStzuDir = ""
$bStzuCollect = 0
$aStzuFound = []
$aStzuBroken = []
$aStzuLastName = ""
$aStzuUnresolved = []
$aStzuWarnings = []
$aStzuNotes = []

if len(sysargv) < 3
	? "usage: haro.ring <file.haro> [all]"
else
	cPath = sysargv[3]
	cSrc = read(cPath)
	$cStzuDir = StzuDirOf(cPath)
	bAll = 0
	if len(sysargv) >= 4
		if sysargv[4] = "all" bAll = 1 ok
	ok
	if bAll
		HaroAll(cSrc)
	else
		try
			aLang = StzuDeclare(cSrc)
			StzuPrintLanguage(aLang)
		catch
			? cCatchError
		done
	ok
ok

# v0.15: `all` -- every defect of the declaration, one line each, in the order of the file.
# A FUNCTION, not top-level code, on purpose: on Ring a bare assignment inside a function to a
# name that exists as a global writes the GLOBAL, so the names used here (cE, aL, aFd) must be
# ones no script-level variable of this file is called -- cErr and aLang are, and StzuDeclare
# assigns both of its own (found on the oracle: its cErr leaked into the top level's)
func HaroAll(cText)
	$bStzuCollect = 1
	cE = ""
	aL = NULL
	try
		aL = StzuDeclare(cText)
	catch
		cE = cCatchError
	done
	$bStzuCollect = 0
	if cE != ""
		$aStzuFound + [StzuLineOf(cE), StzuStripPrefix(cE)]
	ok
	if len($aStzuFound) > 0
		aFd = StzuSortFound($aStzuFound)
		for k = 1 to len(aFd)
			? "haro (line " + aFd[k][1] + "): " + aFd[k][2]
		next
	else
		StzuPrintLanguage(aL)
	ok
