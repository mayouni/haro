# gbnf_batch.ring -- asks the engine's constrained decoder (gbnf_machine.zig, contract C9) a list of questions in one run: does it hold this grammar, and
# does the grammar accept this sentence. Runs on rnxc inside the package (runtime/package/ringpp-win64), where `load "stzlib.ring"` reaches Softanza and its
# engine; the grammar functions judge with no model loaded (stzNeuralModel.ring 195-216). The court of rung 20 (v20/refine_check.py) writes the jobs.
#
#     rnxc gbnf_batch.ring <manifest> <directory>
#
# The manifest holds one job a line, `grammar file|sentence file`, both names relative to the directory; one line comes back for each:
# `J|<n>|<the refusal, empty when the engine holds the grammar>|<1 when the grammar accepts the sentence>`.

load "stzlib.ring"

cManifest = read(sysargv[3])
cDir = sysargv[4]
acJobs = str2list(substr(cManifest, char(13), ""))
nJobs = len(acJobs)
for i = 1 to nJobs
	cJob = acJobs[i]
	if len(cJob) > 0
		nBar = substr(cJob, "|")
		cG = read(cDir + "/" + left(cJob, nBar - 1))
		cS = read(cDir + "/" + right(cJob, len(cJob) - nBar))
		? "J|" + i + "|" + StzGrammarRefusal(cG) + "|" + StzGrammarAccepts(cG, cS)
	ok
next
