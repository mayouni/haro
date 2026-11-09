"""Applies the v0.29 court edits to spike/haro_lib.haro (WC1 of the weaves charge). One-shot, kept so the change is reproducible and reviewable;
every anchor must match exactly once or nothing is written."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', 'haro_lib.haro')
t = open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'


def edit(old, new):
    global t
    old = old.replace('\n', nl)
    new = new.replace('\n', nl)
    assert t.count(old) == 1, ('anchor count', t.count(old), old[:90])
    t = t.replace(old, new)


# 1. the weaves refused by name: now only a weave none of whose rules is judged or held
edit('''			# v0.25: sovereignty (W3) and privacy (W4) are judged below; the five other weaves are carried and refused by name
			for i = 1 to len(aWv)
				if aWv[i][1] != "sovereignty" and aWv[i][1] != "privacy"
					StzuFail(aWv[i][3], "WEAVES names '" + aWv[i][1] + "', and no weave but sovereignty (W3) and privacy (W4) is judged in Haro v0.25 -- the five others are Zin's design, carried, not built")
				ok
			next
''', '''			# v0.25: sovereignty (W3) and privacy (W4) are judged below. v0.29 (WC1): so are the rules of the six carried weaves that need no
			# new seat (StzuWeaveRules); a weave none of whose rules is judged or held is carried, and refused by name
			for i = 1 to len(aWv)
				if aWv[i][1] != "sovereignty" and aWv[i][1] != "privacy"
					aWR = StzuWeaveRules(aWv[i][1])
					if len(aWR[1]) + len(aWR[2]) = 0
						StzuFail(aWv[i][3], "WEAVES names '" + aWv[i][1] + "', and none of its " + len(aWR[3]) + " rules is judged in Haro v0.29 -- they are Zin's design, carried, not built")
					ok
				ok
			next
''')

# 2. the judgements, after the weaves over the marks, inside the same try
edit('''				next
			ok
		catch
			StzuNote(cCatchError)
		done
	ok

	return aRec
''', '''\t\t\t\tnext
\t\t\tok
\t\t\t# v0.29 (WC1): the six carried weaves, as far as the court judges them with no new seat. Each rule is an article's condition read at
\t\t\t# the WEAVE's severity (ZIN-WEAVES-INVENTORY.md): where the world stands under the article, the article's own refusal came first
\t\t\t# above, constitutional, and the weave does not say it twice. W1.2 and W7.1 hold by construction and judge nothing.
\t\t\taAn = StzuArticles()
\t\t\tfor i = 1 to len(aWv)
\t\t\t\ttWN = aWv[i][1]
\t\t\t\ttWS = aWv[i][2]
\t\t\t\tif tWN = "resilience"
\t\t\t\t\t# W1.5: a degradation preserves the invariants -- a CONSTRAINT held at warning that cites an article the world stands under
\t\t\t\t\tfor j = 1 to len(aConstraints)
\t\t\t\t\t\tif aConstraints[j][9] = "warning" and isList(aConstraints[j][8])
\t\t\t\t\t\t\taCts = aConstraints[j][8]
\t\t\t\t\t\t\tfor k = 1 to len(aCts)
\t\t\t\t\t\t\t\tnCA = StzuCitedArticle(aCts[k])
\t\t\t\t\t\t\t\tif nCA > 0
\t\t\t\t\t\t\t\t\tif InStrList(aAn[nCA], aArts)
\t\t\t\t\t\t\t\t\t\tStzuWeave(tWS, aConstraints[j][6], "W1.5 resilience: CONSTRAINT '" + aConstraints[j][1] + "' is SEVERITY warning and cites " + aCts[k] + ", and the world stands under " + aAn[nCA] + " -- a degradation must not pass a law the world declares" + StzuArtTail(nCA))
\t\t\t\t\t\t\t\t\tok
\t\t\t\t\t\t\t\tok
\t\t\t\t\t\t\tnext
\t\t\t\t\t\tok
\t\t\t\t\tnext
\t\t\t\tok
\t\t\t\tif tWN = "observability"
\t\t\t\t\t# W2.2 and W2.3: a model's proposal and a gate's denial are traced by the audit chain, which is Art. 3's
\t\t\t\t\tif not isNull(aRefine) and not InStrList("visible_state", aArts)
\t\t\t\t\t\taFlO = aRefine[2]
\t\t\t\t\t\tfor j = 1 to len(aFlO)
\t\t\t\t\t\t\tif aFlO[j][3] = "llm"
\t\t\t\t\t\t\t\tStzuWeave(tWS, aFlO[j][4], "W2.2 observability: point '" + aFlO[j][1] + "." + aFlO[j][2] + "' has FLOOR llm -- a model may propose it -- and visible_state is not among ARTICLES: no chain keeps the model's proposal or its refusal" + StzuArtTail(3))
\t\t\t\t\t\t\tok
\t\t\t\t\t\tnext
\t\t\t\t\t\tStzuWeave(tWS, aRefine[3], "W2.3 observability: '" + tLName + "' declares a REFINE, whose gate denies, and visible_state is not among ARTICLES: a denial enters no audit chain" + StzuArtTail(3))
\t\t\t\t\tok
\t\t\t\tok
\t\t\t\tif tWN = "temporal_integrity"
\t\t\t\t\t# W5.2: the changes of points that have a history are versioned by the numbered chain, which is Art. 3's
\t\t\t\t\tif not isNull(aRefine) and not InStrList("visible_state", aArts)
\t\t\t\t\t\tStzuWeave(tWS, aRefine[3], "W5.2 temporal_integrity: '" + tLName + "' declares a REFINE, which changes points that have a history, and visible_state is not among ARTICLES: no numbered chain versions the changes" + StzuArtTail(3))
\t\t\t\t\tok
\t\t\t\tok
\t\t\t\tif tWN = "learnability"
\t\t\t\t\t# W7.4: a denial is explained -- told by a voice and met by a stable identifier, Art. 1's two conditions
\t\t\t\t\tnDen = len(aRefusals) + len(aConstraints)
\t\t\t\t\tif nDen > 0 and isNull(aNarrate)
\t\t\t\t\t\tnDL = aConstraints[1][6]
\t\t\t\t\t\tif len(aRefusals) > 0
\t\t\t\t\t\t\tnDL = aRefusals[1][4]
\t\t\t\t\t\tok
\t\t\t\t\t\tStzuWeave(tWS, nDL, "W7.4 learnability: '" + tLName + "' declares " + nDen + " denial(s) (CONSTRAINT or REFUSAL) and no NARRATE -- a denial no voice tells is not explained" + StzuArtTail(1))
\t\t\t\t\tok
\t\t\t\t\tfor j = 1 to len(aRefusals)
\t\t\t\t\t\tif aRefusals[j][6] = ""
\t\t\t\t\t\t\tStzuWeave(tWS, aRefusals[j][4], "W7.4 learnability: REFUSAL '" + aRefusals[j][1] + "' carries no CODE -- a denial is explained to its reader by a stable identifier (C2 2.1)" + StzuArtTail(1))
\t\t\t\t\t\tok
\t\t\t\t\tnext
\t\t\t\t\tfor j = 1 to len(aConstraints)
\t\t\t\t\t\tif aConstraints[j][7] = ""
\t\t\t\t\t\t\tStzuWeave(tWS, aConstraints[j][6], "W7.4 learnability: CONSTRAINT '" + aConstraints[j][1] + "' carries no CODE -- a denial is explained to its reader by a stable identifier (C2 2.1)" + StzuArtTail(1))
\t\t\t\t\t\tok
\t\t\t\t\tnext
\t\t\t\tok
\t\t\t\tif tWN = "structural_integrity"
\t\t\t\t\t# W8.5: synthesis never overrides what the court proved -- a policy point a model may propose, Art. 4's condition
\t\t\t\t\tif not isNull(aRefine)
\t\t\t\t\t\taPtS = aRefine[1]
\t\t\t\t\t\taFlS = aRefine[2]
\t\t\t\t\t\tfor j = 1 to len(aPtS)
\t\t\t\t\t\t\tif aPtS[j][3] = "policy"
\t\t\t\t\t\t\t\tfor k = 1 to len(aFlS)
\t\t\t\t\t\t\t\t\tif aFlS[k][1] = aPtS[j][1] and aFlS[k][2] = aPtS[j][2] and aFlS[k][3] = "llm"
\t\t\t\t\t\t\t\t\t\tStzuWeave(tWS, aFlS[k][4], "W8.5 structural_integrity: policy point '" + aPtS[j][1] + "." + aPtS[j][2] + "' has FLOOR llm -- a model-composed proposal could replace a rule the court proved" + StzuArtTail(4))
\t\t\t\t\t\t\t\t\tok
\t\t\t\t\t\t\t\tnext
\t\t\t\t\t\t\tok
\t\t\t\t\t\tnext
\t\t\t\t\tok
\t\t\t\tok
\t\t\tnext
\t\tcatch
\t\t\tStzuNote(cCatchError)
\t\tdone
\tok

\treturn aRec

# v0.29 (WC1): the rules of the six carried weaves, as the court judges them -- [judged, held by construction, carried]. Judged: a
# refusal exists at the weave's severity. Held: nothing can fail (W1.2: the gate writes a change's inverse before the change lands;
# W7.1: a declaration without a RATIONALE is refused whatever the weaves say). Carried: Zin's design, not judged. The rule ids are
# Zin's (ZIN_CONSTITUTIONAL_WEAVES.md); a weave with no rule judged or held is refused by name
func StzuWeaveRules(tWeave)
\tif tWeave = "resilience"
\t\treturn [["W1.5"], ["W1.2"], ["W1.1", "W1.3", "W1.4", "W1.6", "W1.7"]]
\tbut tWeave = "observability"
\t\treturn [["W2.2", "W2.3"], [], ["W2.1", "W2.4", "W2.5", "W2.6"]]
\tbut tWeave = "temporal_integrity"
\t\treturn [["W5.2"], [], ["W5.1", "W5.3", "W5.4", "W5.5"]]
\tbut tWeave = "cost_awareness"
\t\treturn [[], [], ["W6.1", "W6.2", "W6.3", "W6.4", "W6.5", "W6.6", "W6.7", "W6.8", "W6.9", "W6.10", "W6.11", "W6.12", "W6.13"]]
\tbut tWeave = "learnability"
\t\treturn [["W7.4"], ["W7.1"], ["W7.2", "W7.3", "W7.5", "W7.6"]]
\tbut tWeave = "structural_integrity"
\t\treturn [["W8.5"], [], ["W8.1", "W8.2", "W8.3", "W8.4"]]
\tok
\treturn [[], [], []]

# the number of the article a cite names, `article:3` or `article:visible_state`, and 0 for any other cite
func StzuCitedArticle(tCite)
\tif left(tCite, 8) != "article:" return 0 ok
\ttV = substr(tCite, 9)
\taAn = StzuArticles()
\tfor i = 1 to len(aAn)
\t\tif tV = aAn[i] or tV = "" + i return i ok
\tnext
\treturn 0

# the article a weave refusal serves, in the form the articles' own refusals use
func StzuArtTail(nArt)
\taAn = StzuArticles()
\treturn " [Art. " + nArt + " " + aAn[nArt] + "]"

# a comma-joined list with more words added to it
func StzuAppendWords(tList, aWords)
\tfor i = 1 to len(aWords)
\t\tif tList != "" tList += "," ok
\t\ttList += aWords[i]
\tnext
\treturn tList
''')

# 3. what the court prints on acceptance: the rules of the new weaves it judges, holds and carries
edit('''\t? "safeguards " + tSafeg
''', '''\t? "safeguards " + tSafeg
\t# v0.29: the rules of the six carried weaves a constitution names -- judged, held by construction, carried -- printed only when one is named
\ttJudged = ""
\ttHeld = ""
\ttCarried = ""
\tbSix = 0
\tif not isNull(aCs)
\t\tfor i = 1 to len(aCs[3])
\t\t\ttWn = aCs[3][i][1]
\t\t\tif tWn != "sovereignty" and tWn != "privacy"
\t\t\t\tbSix = 1
\t\t\t\taWr = StzuWeaveRules(tWn)
\t\t\t\ttJudged = StzuAppendWords(tJudged, aWr[1])
\t\t\t\ttHeld = StzuAppendWords(tHeld, aWr[2])
\t\t\t\ttCarried = StzuAppendWords(tCarried, aWr[3])
\t\t\tok
\t\tnext
\tok
\tif bSix
\t\t? "judged " + tJudged
\t\t? "held " + tHeld
\t\t? "carried " + tCarried
\tok
''')

open(P, 'w', encoding='utf-8', newline='').write(t)
print('haro_lib.haro: the v0.29 court written')
