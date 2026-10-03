# e3_naturallib.ring -- Phase 1.5, experiment E3: NaturalLib 1.27 AS SHIPPED, asked to be the
# natural-language surface of the tontine, retargeted to a closed query grammar.
#
# What it measures, on the official Ring 1.27 install (the library's own runtime):
#   E3a  a command whose function EMITS a ZQL string instead of executing something   (retargeting)
#   E3b  a second human language                                                       (a second set of commands)
#   E3c  text the vocabulary does not know                                             (refusal or silence?)
#   E3d  text that is Ring                                                             (is the surface closed?)
#
# NaturalLib's answer path is RunString (naturallanguage.ring:243): the user's text is pasted into
# a Ring source string and eval'd. E3d asks what that means for a question.

load "stdlib.ring"
load "naturallib.ring"

$cQuery = ""

DefineNaturalCommand.SyntaxIsCommandNumber([
	:Package = "Tontine.Natural",
	:Command = "show deposits over",
	:Function = func {
		$cQuery = "SELECT * FROM collect WHERE amount > " + Expr(1)
		CommandReturn($cQuery)
	}
])

# a second language is a second set of commands: the words are the class name
DefineNaturalCommand.SyntaxIsCommandNumber([
	:Package = "Tontine.Natural",
	:Command = "montre les depots au dessus de",
	:Function = func {
		$cQuery = "SELECT * FROM collect WHERE amount > " + Expr(1)
		CommandReturn($cQuery)
	}
])

Tontine = New NaturalLanguage {
	SetLanguageName(:Tontine)
	SetPackageName("Tontine.Natural")
	loadCommand("show deposits over")
	loadCommand("montre les depots au dessus de")
}

? "E3a " + ProbeText("show deposits over 5000")
? "E3b " + ProbeText("montre les depots au dessus de 5000")
? "E3c1 " + ProbeText("show deposits over lots")
? "E3c2 " + ProbeText("show me the deposits please")
? "E3d " + ProbeText("show deposits over 5000" + nl + '? "ESCAPED: this line ran as Ring"')

func ProbeText cText
	$cQuery = ""
	cErr = ""
	try
		Tontine.RunString(cText)
	catch
		cErr = cCatchError
	done
	cShown = substr(cText, nl, " | ")
	return "[" + cShown + "] query=<" + $cQuery + "> error=<" + cErr + ">"
