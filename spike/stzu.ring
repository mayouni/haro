# stzu.ring -- `rnxc stzu.ring <file.stzu>`: judge a language declaration
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

load "stzu_lib.ring"

$aStzuToks = []
$nStzuPos = 1

if len(sysargv) < 3
	? "usage: stzu.ring <file.stzu>"
else
	cPath = sysargv[3]
	cSrc = read(cPath)
	try
		aLang = StzuDeclare(cSrc)
		StzuPrintLanguage(aLang)
	catch
		? cCatchError
	done
ok
