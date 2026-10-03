# e3_probe_rnx.ring -- asks Ring++ to load NaturalLib 1.27 as shipped (by its absolute path: the
# library is not part of this repository, and that is the point). The first thing that happens is
# a Rule A refusal inside the library's own source; what lies beneath it is named by e3_run.py.

load "stdlibcore.ring"
load "D:/ring127/libraries/naturallib/naturallib.ring"

DefineNaturalCommand.SyntaxIsCommandNumber([
	:Package = "Tontine.Natural",
	:Command = "show deposits over",
	:Function = func {
		CommandReturn("SELECT * FROM collect WHERE amount > " + Expr(1))
	}
])
