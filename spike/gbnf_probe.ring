# gbnf_probe.ring -- asks the engine's constrained decoder (gbnf_machine.zig,
# contract C9) whether it holds a forged grammar and accepts a sentence under
# it. Runs on rnxc inside the package (runtime/package/ringpp-win64), where
# `load "stzlib.ring"` reaches Softanza and its engine; the three grammar
# functions judge with no model loaded (stzNeuralModel.ring 195-216).
#   rnxc gbnf_probe.ring <grammar.gbnf> <sentence file>

load "stzlib.ring"

cGbnfText = read(sysargv[3])
cSentence = read(sysargv[4])
? "supported: " + StzEngineGbnfDecodingSupported()
? "refusal: [" + StzGrammarRefusal(cGbnfText) + "]"
? "accepts: " + StzGrammarAccepts(cGbnfText, cSentence)
? "could continue after 40 bytes: " + StzGrammarCouldContinue(cGbnfText, left(cSentence, 40))
