"""Writes the v0.29 records (D53, HF-144, the twenty-ninth rung) into CHARTER.md, FINDINGS.md and SPIKE.md. Every anchor must match exactly once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def edit(name, old, new):
    p = os.path.join(ROOT, name)
    t = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert t.count(old) == 1, (name, t.count(old), old[:80])
    open(p, 'w', encoding='utf-8', newline='').write(t.replace(old, new))
    print(name, 'edited')


D53 = ("- **D53 -- five of the six carried weaves judge what they can with no new seat; the rest wait for theirs** (WC1 of the constitution desk's second charge,\n"
"  the six carried weaves, filed by the compass on the author's word of 2026-11-02; `spike/v29/GRAMMAR.md`, `spike/v29/ZIN-WEAVES-INVENTORY.md`; HF-144; the twenty-ninth\n"
"  rung, the number this repository's CLAUDE.md holds for the desk). WC0 read Zin's 42 rules of W1, W2, W5, W6, W7 and W8 against Haro's mechanisms: 28 have one (8\n"
"  judged through what exists, 20 needing a declared seat) and 14 are absent at this altitude. **Built here are the eight that need no seat, and six of them can be\n"
"  refused**: W1.5 (a warning CONSTRAINT citing an article the world stands under), W2.2 and W2.3 (a point floored llm, and a gate that denies, in a world with no\n"
"  chain), W5.2 (the same gate, its changes unversioned), W7.4 (a denial with no voice or no CODE) and W8.5 (a policy point floored llm without predictable_authority).\n"
"  W1.2 and W7.1 are held by construction and judge nothing. **Each rule is an article's condition read at the weave's severity** -- constitutional refuses,\n"
"  governance warns, advisory notes, the v0.25 machinery -- and where the world stands under the article its own refusal comes first, so a weave never says a\n"
"  constitutional thing twice. A refusal names the rule, the weave, the declared thing in the world's words and the article it serves. The court prints `judged`,\n"
"  `held` and `carried` when one of the six is named, so a weave judged on some of its rules is never read as judged on all. `cost_awareness`, none of whose 13 rules\n"
"  can be judged without a budget, stays refused by name, the message now counting rules and built from a table. v23's R13 and v25's R7 named `resilience` and were\n"
"  amended to name it, said so in their names. *Cost:* a language that names one of the five weaves is judged on conditions it was not before and prints three lines\n"
"  more; a language that names none prints what it printed, to the byte. *The author's question, parked 2026-11-06 (\"Raise at WC2\"):* whether a world must say which\n"
"  weaves it leaves out, as Zin's SUPPRESS ... BECAUSE makes auditable; until WC2's first rung a world may leave any weave out, as it may leave any article. *Not built:*\n"
"  the twenty rules that need a seat (WC2, one entry each), the record plane (WC3), the proof world (WC4).\n")

edit('CHARTER.md', "- **D38 -- every element that carries a CODE may carry CITES", D53 + "- **D38 -- every element that carries a CODE may carry CITES")

HF144 = ("| HF-144 | **Five of the six carried weaves: what building WC1 found.** v0.29 (D53): the rules of the six carried weaves that need no new seat are judged, each an article's condition read at the weave's severity. (1) **Eight were in the sort, six can be refused**: W1.2 (the gate writes a change's inverse unconditionally) and W7.1 (a missing RATIONALE is a grammar error before any weave looks) have no shape the court can refuse and are *held by construction*, printed as such and pinned by naming. (2) **W5.2 rests on Art. 3 alone**, where WC0 said Art. 2 and 3: the revert is written under any articles, and what versions an update is the numbered chain; W5.2 and W2.3 share one condition and are different weaves making different claims. (3) **A plant showed a protection no fixture pinned**: P14, a cite read without its kind, was missed by all seventeen fixtures -- `pattern:visible_state` spells the article after the same eight characters as `article:` -- and A8 was added after the court spoke; fifteen plants, every one caught, the file restored byte for byte. (4) **A guard that could never matter was removed**: W8.5 skipped itself when predictable_authority is declared, but Art. 4 raises first and the weave is never reached. (5) **W1.5 is a reading**: Haro's degradations are warnings and an article's refusal is never one, so the shape refused is the maker's own, a constraint held at warning that cites the law it degrades. (6) **WC0's `five others` was wrong in eight places** and counted weaves where it should count rules; the new refusal is built from a table. (7) **The rule WC0 inferred held**: every judged rule is an article's condition, and the article's own refusal comes first when the world stands under it. | measured, stage 1 on haro and its checked build 0 failures (155.7 s), the 18 fixtures of v29, fifteen plants, 2026-11-06 | this desk; WC2 (the twenty rules that need a seat) |\n")

def insert_after_row(name, row_prefix, new_row):
    p = os.path.join(ROOT, name)
    t = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    lines = t.split(nl)
    idx = [i for i, l in enumerate(lines) if l.startswith(row_prefix)]
    assert len(idx) == 1, (row_prefix, idx)
    lines.insert(idx[0] + 1, new_row.rstrip('\n'))
    open(p, 'w', encoding='utf-8', newline='').write(nl.join(lines))
    print(name, 'row inserted after', row_prefix)


insert_after_row('FINDINGS.md', '| HF-143 |', HF144)

RUNG = ("## The twenty-ninth rung -- Haro v0.29, five of the six carried weaves judge what they can with no new seat -- 2026-11-06\n\n"
"**WC1 of the constitution desk's second charge** (the six carried weaves, filed by the compass on the author's word of 2026-11-02; WC0 is\n"
"`v29/ZIN-WEAVES-INVENTORY.md`, D53, HF-144). The guard has been green from this repository since 2026-11-02 22:29; the desk took the number this\n"
"repository's CLAUDE.md holds for it. Fixtures first (15 of 17 failing on the court of the day, 2 holding), the court second, the plants third.\n\n"
"    v29/gen_fixtures.py, fixtures.json   18 meta fixtures: 8 accepts, 10 rejects -- W1.5, W2.2, W2.3, W5.2, W7.4, W8.5, W1.2 and W7.1 held,\n"
"                                         cost_awareness still refused by name, v0.25's A1 unchanged\n"
"    haro_lib.haro                        the weave loop of the constitution block: StzuWeaveRules, StzuCitedArticle, StzuArtTail, the six\n"
"                                         judgements; the refusal by name counts rules; judged / held / carried printed when a new weave is named\n"
"    v23/fixtures.json R13, v25/fixtures.json R7   amended: the weave they name is cost_awareness, said so in their names\n"
"    v29/plants.py                        fifteen protections switched off in turn: every one caught, haro_lib.haro restored byte for byte\n"
"    v29/apply_court.py                   the court edit as one reviewable, reproducible script\n"
"    haro_forge.py                        stage 1 grows by v0.29\n\n"
"**Results.** 18 of 18 on haro; stage 1 passes on haro and its checked build, byte-identical (0 failures, 155.7 s). What building found is in HF-144:\n"
"six of the eight sorted rules can be refused and two are held by construction; W5.2 rests on Art. 3 alone; a plant showed a protection no fixture\n"
"pinned (A8, added after the court spoke); W1.5 is a stated reading. **Not built:** the twenty rules that need a seat (WC2), the record plane (WC3),\n"
"the proof world and the author's own reading of its refusals (WC4). **Parked by the author (2026-11-06, \"Raise at WC2\"):** whether a world must say\n"
"which weaves it leaves out.\n\n")

edit('SPIKE.md', "## The thirtieth rung -- Haro v0.30", RUNG + "## The thirtieth rung -- Haro v0.30")
