# k4_gen.ring -- K4 on a LOCAL model: generate programs under a grammar with the engine's constrained decoder, offline.
#
#     rnxc k4_gen.ring <model.gguf> <manifest> <directory> [count]
#
# Runs on the Ring++ package (runtime/package/ringpp-win64/bin/rnxc.exe), where `load "stzlib.ring"` reaches Softanza and its engine.
# The manifest holds one job a line:  id|prompt file|grammar file or -|seed|temperature|max tokens   (names relative to the directory)
# and writes, for each job, <directory>/<id>.out (the generated text) and one result line on stdout:
#     J|<id>|<seconds>|<tokens emitted>|<grammar judged>|<masked>|<stalled>|<complete>
# The same model, prompt, grammar, seed and temperature give the same text (Softanza's StzGenerateXT is reproducible under a seed).
#
# THE ENGINE KEEPS ONLY THE LAST 512 TOKENS OF A FRESH PROMPT (neural_gen.zig: `const cap: usize = 512`, `prompt[prompt.len - cap ..]`), silently, so a prompt longer than that loses its HEAD --
# the system message and the first examples. Found 2026-10-20 when the first local K4 runs read like a model that had never seen its primer (probe: a secret word in the system message,
# forgotten behind 1,200 tokens of filler). So every prompt is counted FIRST, with the generator's own tokenizer, and nothing is generated unless all of them fit in LIMIT tokens:
#     T|<id>|<tokens>          one line per job;  with `count` as the fourth argument the run stops there.
#     ERR|prompt too long|<id>|<tokens>

load "stzlib.ring"

# Calibrated on smollm2 (a secret word in the system message, filler after it, token counts by StzEngineNeuralGenTokenize): the word survives at 506 tokens and is gone at 514.
LIMIT = 510

cModel = sysargv[3]
cManifest = read(sysargv[4])
cDir = sysargv[5]
bCountOnly = (len(sysargv) >= 6 and sysargv[6] = "count")

StzNeuralModelQ(cModel)
if StzHasGenerativeModel() = 0
	? "ERR|no generative model: " + cModel
	bye
ok
? "MODEL|" + cModel + "|decoding enforced at the sampler: " + StzConstrainedDecodingSupported()

acJobs = str2list(substr(cManifest, char(13), ""))
nJobs = len(acJobs)

nWorst = 0
bTooLong = 0
for i = 1 to nJobs
	cJob = acJobs[i]
	if len(cJob) > 0
		aF = split(cJob, "|")
		nTok = StzEngineNeuralGenTokenize(read(cDir + "/" + aF[2]))
		? "T|" + aF[1] + "|" + nTok
		if nTok > nWorst
			nWorst = nTok
		ok
		if nTok > LIMIT
			? "ERR|prompt too long|" + aF[1] + "|" + nTok
			bTooLong = 1
		ok
	ok
next
? "WORST|" + nWorst + "|limit " + LIMIT
if bTooLong = 1 or bCountOnly = 1
	bye
ok

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
