# e1_graph.ring -- Phase 1.5, experiment E1: the tontine's knowledge graph, built with
# stzKnowledgeGraph, queried, judged by its laws, shipped as a plain-text artifact and reloaded.
#
#   E1a  the ontology and the facts                       (entities, relations)
#   E1b  a law judges a fact                              (:Unique -- a member receives the pot once)
#   E1c  closed queries: a triple pattern is DATA         (Query([s, p, o]), "?x" a variable)
#   E1d  the artifact: export to text, reload, compare    (rule 3: world-as-data, versioned)
#   E1e  what does NOT survive the artifact               (node properties, laws)
#   E1f  a two-pattern question                           (QueryPath: is there a join?)
#
# Run on the Ring++ package: rnxc.exe e1_graph.ring   (Softanza is the subject; it needs its engine)

load "stzlib.ring"

$cArtifact = "data/tontine.zknw"

o = new stzKnowledgeGraph("tontine")
for cM in ["aminata", "moussa", "fatima", "sanda", "boubacar", "zeinab"]
	o.Know(cM, "member")
next
for cR in ["round1", "round2", "round3"]
	o.Know(cR, "round")
next
o.Know("treasurer", "role")
o.Know("collector", "role")

o.AddFact("fatima",   "received_pot_in", "round1")
o.AddFact("moussa",   "received_pot_in", "round2")
o.AddFact("aminata",  "received_pot_in", "round3")
o.AddFact("boubacar", "guarantees", "sanda")
o.AddFact("fatima",   "guarantees", "zeinab")
o.AddFact("aminata",  "guarantees", "moussa")
o.AddFact("zeinab",   "holds_role", "treasurer")
o.AddFact("boubacar", "holds_role", "collector")

? "E1a facts=" + len(o.Facts())

# a member receives the pot at most once
o.ConstrainRelation("received_pot_in", :Unique)

? "E1c who received the pot in round2  " + Flat(o.Query(["?x", "received_pot_in", "round2"]))
? "E1c who guarantees sanda            " + Flat(o.Query(["?x", "guarantees", "sanda"]))
? "E1c whom does aminata guarantee     " + Flat(o.Query(["aminata", "guarantees", "?x"]))
? "E1c who is the treasurer            " + Flat(o.Query(["?x", "holds_role", "treasurer"]))
? "E1c every guarantee                 " + Flat(o.Query(["?x", "guarantees", "?y"]))
? "E1c does boubacar guarantee sanda   " + o.Query(["boubacar", "guarantees", "sanda"])

# the display name the LEDGER uses ("Moussa") is not the node id ("moussa"): a node property?
o.SetNodeProperty("moussa", "display", "Moussa")
? "E1e property on the live graph       " + o.NodeProperty("moussa", "display")

write($cArtifact, o.ExportToKnow())
? "E1d artifact written: " + len(read($cArtifact)) + " bytes, " + len(split(read($cArtifact), nl)) + " lines"

o2 = new stzKnowledgeGraph("tontine2")
o2.ImportKnow($cArtifact)
? "E1d reloaded facts=" + len(o2.Facts()) + " (original " + len(o.Facts()) + ")"
? "E1d same answer after reload: " + Flat(o2.Query(["?x", "received_pot_in", "round2"]))
? "E1e law survives the artifact? unique=" + o2.RelationHasLaw("received_pot_in", "unique")
cDisp = ""
try
	cDisp = "" + o2.NodeProperty("moussa", "display")
catch
	cDisp = "RAISED " + cCatchError
done
? "E1e property survives the artifact? <" + cDisp + ">"

# E1b -- the law judges a fact. Done on the live graph AFTER the artifact was written, so the
# artifact holds only the canonical facts
aV = o.Admit("fatima", "received_pot_in", "round3", [])
? "E1b a second pot for fatima:        admitted=" + aV[:admitted] + " why=" + aV[:why]
aV = o.Admit("sanda", "received_pot_in", "round3", [])
? "E1b round3 already has aminata; a second beneficiary for it: admitted=" + aV[:admitted] + "  (:Unique is the subject's side only)"

# a question with two patterns and a shared variable: who received the pot in round 1, and whom
# do they guarantee?  Joined, the answer is fatima -> zeinab; the first pattern alone answers fatima.
aPath = []
try
	aPath = o.QueryPath([ ["?x", "received_pot_in", "round1"], ["?x", "guarantees", "?y"] ])
catch
	aPath = ["RAISED " + cCatchError]
done
? "E1f two patterns, shared ?x:        QueryPath answers " + Flat(aPath)
? "E1f the first pattern alone answers " + Flat(o.Query(["?x", "received_pot_in", "round1"]))
? "E1f a join would add                 " + Flat(o.Query(["fatima", "guarantees", "?y"]))

# E1g -- is an artifact judged when it is LOADED?  A lawless one: two pots for fatima, the :Unique law declared
cBad = 'knowledge "lawless"' + nl + nl + "facts" + nl +
	"    fatima | received_pot_in | round1" + nl +
	"    fatima | received_pot_in | round3" + nl + nl +
	"ontology" + nl + "    received_pot_in | unique" + nl
write("scratch/lawless.zknw", cBad)
o3 = new stzKnowledgeGraph("lawless")
cErr3 = ""
try
	o3.ImportKnow("scratch/lawless.zknw")
catch
	cErr3 = cCatchError
done
? "E1g a lawless artifact: raised=<" + cErr3 + "> facts loaded=" + len(o3.Facts()) + " law present=" + o3.RelationHasLaw("received_pot_in", "unique")

func Flat v
	if isList(v)
		return substr(substr(substr(list2code(v), char(13), ""), nl, " "), tab, "")
	ok
	return "" + v
