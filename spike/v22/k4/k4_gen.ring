# k4_gen.ring -- K4 on a LOCAL model: generate programs under a grammar with the engine's constrained decoder, offline.
#
#     rnxc k4_gen.ring <model.gguf> <manifest> <directory>
#
# Runs on the Ring++ package (runtime/package/ringpp-win64/bin/rnxc.exe), where `load "stzlib.ring"` reaches Softanza and its engine.
# The manifest holds one job a line:  id|prompt file|grammar file or -|seed|temperature|max tokens   (names relative to the directory)
# and writes, for each job, <directory>/<id>.out (the generated text) and one result line on stdout:
#     J|<id>|<seconds>|<tokens emitted>|<grammar judged>|<masked>|<stalled>|<complete>
# The same model, prompt, grammar, seed and temperature give the same text (Softanza's StzGenerateXT is reproducible under a seed).

load "stzlib.ring"

cModel = sysargv[3]
cManifest = read(sysargv[4])
cDir = sysargv[5]

StzNeuralModelQ(cModel)
if StzHasGenerativeModel() = 0
	? "ERR|no generative model: " + cModel
	bye
ok
? "MODEL|" + cModel + "|decoding enforced at the sampler: " + StzConstrainedDecodingSupported()

acJobs = str2list(substr(cManifest, char(13), ""))
nJobs = len(acJobs)
for i = 1 to nJobs
	cJob = acJobs[i]
	if len(cJob) > 0
		aF = split(cJob, "|")
		cId = aF[1]
		cPrompt = read(cDir + "/" + aF[2])
		cGrammar = ""
		if aF[3] != "-"
			cGrammar = read(cDir + "/" + aF[3])
		ok
		nSeed = 0 + aF[4]
		nTemp = 0 + aF[5]
		nMax = 0 + aF[6]
		aOpt = [ [ :MaxTokens, nMax ], [ :Temperature, nTemp ], [ :Seed, nSeed ] ]
		if cGrammar != ""
			add(aOpt, [ :Grammar, cGrammar ])
		ok
		t0 = clock()
		cOut = StzGenerateXT(cPrompt, aOpt)
		nSec = (clock() - t0) / clockspersecond()
		write(cDir + "/" + cId + ".out", cOut)
		aRun = StzLastGrammarRun()
		? "J|" + cId + "|" + nSec + "|" + aRun[:steps] + "|" + aRun[:judged] + "|" + aRun[:masked] + "|" + aRun[:stalled] + "|" + aRun[:complete]
	ok
next
