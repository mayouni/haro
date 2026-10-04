# Node identity on the program graph, built -- the structure level of the computing altitude, part two (Haro v0.19, the nineteenth rung)

**Rung 2 of the code-graph memo** (`haro/CODEGRAPH.md`, section 7), built on the author's "rung 2". **Written after** the fixtures in
`fixtures.txt` (23 edits, each the ids a new program must hold, composed by hand before `ids.py` existed -- the W discipline) and after
the measurements of `probes/` that priced every pass of the matcher. `ids.py` is the reference implementation of this file; the graph
it works on is rung 18's (`v18/GRAMMAR.md`).

**What this is, in one line.** A refinement targets a node, and the node has to survive a change (RCP wants a stable identifier). The
face is edited as TEXT (option A of CODEGRAPH 3.7), so identity is **recovered when the edited text is parsed again**, by a matcher
that knows nothing but two graphs: the one that was, whose items carry ids, and the one that is, whose items carry none.

## 0. What exists, and what does not

| | status | where |
|---|---|---|
| ids on the items of the graph, in pre-order, and the matcher that carries them across an edit | **built** | `ids.py` |
| the court: 23 edits, 6 controls that must fail, Haro's own history replayed; guard stage 23 | **built**, `python haro/spike/v19/ids_check.py`, 20 s | `ids_check.py` |
| the price of every pass and of both thresholds | **measured** (section 4) | `probes/sweep.py`, `probes/near.py` |
| **where the ids live between two parses** -- the cache that holds the last graph with its ids, keyed by content hash | **not built.** Option A says the graph is a cache; the cache is rung 3's | -- |
| a refinement applied to the graph, printed as a text diff (CODEGRAPH 3.4) | **not built.** Rung 5 | -- |
| ids for nodes inside an expression | **not built, by design**: such a node is the statement's id and a path (section 1) | -- |

## 1. What has an id

An **item**: a statement, a definition (`func`, `class`, `package`), a comment, a `private` marker, a parameter -- whatever stands in a
block, at any depth, the body of a lambda or a brace inside an expression included. A block is `items`, `then`, `else`, `other`,
`finally` or `params`, found in an item by its path through the expressions around it (`e.args.0.items` is the body of a lambda that is
the first argument of a call). **An expression holds no id**: the node `a + b` is the statement that holds it and a path, and a
refinement that targets it names both. The comment that ends a line (`trail`) belongs to its statement.

`number(g)` gives a first graph its ids, 1, 2, 3, in **pre-order**: an item, then the items of its blocks in field order (a `func` holds
its parameters first, then its statements; an `if` its `then`, its `elif`s, its `else`). `g['_next']` is the next unused id. An id is
an integer in the lineage of one file; two files' ids are not comparable.

## 2. The matcher

`carry(old, new)`: `new` gets the id of what it keeps from `old`, a fresh id for what is new, and the answer is a report of what was kept,
edited and lost. Inside one list of items, in this order:

1. **A definition by its name** -- (kind, name, occurrence) -- wherever it stands in the list. Reordering functions moves no id (fixture 11).
2. **The rest, by the hash of its whole text** (A): the longest common run of identical statements. Then **what is left in each gap
   between runs by similarity** (B): two items of the same kind whose tokens -- the kind and the values in the header, the bodies set
   aside -- are 0.6 alike are one edited item; the best order-preserving pairing wins. `b = 2` becoming `b = 20` keeps its id (fixture 5);
   `b = 2` becoming `foo(bar)` does not (fixture 6): **identity is a claim**, and a refinement aimed at the first must not land on the
   second. A comment is its words; an `if` is its condition.
3. **A move inside the list** (C): what is still unmatched, by identical text, in order.
4. **A renamed definition** by the share of its body that is unchanged (0.6), after the names have had their say (fixtures 12, 13, 14, 16).

Then, for every matched pair, **the same inside each of its blocks**, paired by path; and for a matched **function**, one more pass (D)
over everything still unmatched in it, at any depth, by identical text: **a statement wrapped in an `if`, or taken out of one, keeps its
id** (fixture 9). Parameters are matched by name (fixture 17).

**What is lost on purpose.** A statement moved to *another function* keeps nothing (fixture 22): `return 0` is everywhere, and the same
text in another place is not thereby the same statement. A renamed definition whose body was also rewritten is a new definition (fixture
14). Two identical statements, one deleted, settle the way the diff settles them -- the later pair survives (fixture 19), because the
text cannot say which was meant. An `elif` or a `case` is found by its position among its siblings.

The constants are `SIM_MIN = 0.6` and `RENAME_MIN = 0.6`; both are priced in section 4 and move little.

## 3. The court

`python haro/spike/v19/ids_check.py [--plant] [--quick] [--wide]`; guard stage 23; twenty seconds warm, forty cold.

**F -- 23 edits**, `fixtures.txt`: an old Ring program, a new one, the ids the new one's items must hold in pre-order (an old id, or `*`
for an item the edit made) and the old ids that are gone. Every id unique, and a graph carried onto itself moves none.

**C -- controls that must fail.** A matcher that pairs items by position fails 12 of the 23; one that keeps nothing fails 22. **Each pass
of the real matcher is load-bearing**: with the move pass (C) switched off fixture 23 fails, with the function pool (D) off fixture 9 fails,
with similarity off seven fail, with the rename pass off three. And on real history the positional matcher keeps 33.2 percent --
under the floor, as it must.

**H -- Haro's own history.** Every hand-written Ring file of `haro/spike` (19 files; the ones `forge.ring` generates are not edited by
a human and are left out), consecutive revisions read with `git show` across a rename (`stzu.ring` became `haro.ring`), the last seven
of each: **38 pairs, 28,996 old statements**, each a refinement target. Does it resolve in the next revision? Floors, pinned: 20 pairs
and 8,000 statements (the sample may not shrink) and **95 percent** of the targets resolving (CODEGRAPH 3.7: below it, ids move into a
sidecar, option C). K2 (90 percent, CODEGRAPH 6) is printed beside it.

## 4. Measured

```
Haro's history        38 pairs over 11 files, 28,996 old statements:
                      97.1% kept with the same text, 98.3% keep their id   (definitions 98.7%, comments 98.6%)
                      matched by: text 31,308, name 4,062, function pool 816, similarity 395, rename 2, move 1
the memo's seven      56 pairs (the memo's 56), 49,622 statements (49,933): 97.7% same text (the memo: 98.1%), 99.1% keep their id
```

The memo's 98.1 percent and this rung's 97.7 on the same seven files differ by the graph (L1's items against the token-level
statements of the study) and agree otherwise: **the memo's measure, a function's statements flattened at every depth, is the function
pool.**

**What each pass buys**, Haro's history replayed with it off (`probes/sweep.py`):

| | statements | definitions | comments |
|---|---|---|---|
| everything | 98.26% | 98.68% | 98.56% |
| no move pass (C) | 98.26% | 98.68% | 98.56% |
| no function pool (D) | **95.56%** | 98.68% | 97.75% |
| no similarity (B) | 97.45% | 98.68% | 97.28% |
| name and text only | **85.95%** | 98.56% | 93.37% |

**The cleverness is the pool.** Name and text alone keep 86 percent; the function pool, which only asks whether the same text is still
somewhere in the same function, takes it to 95.6; similarity to 98.3. The move pass (C) buys nothing on this history, because (D)
reaches every list a function holds; it is kept, and pinned by fixture 23, for the lists outside a function (a class, a file's top
level), which Haro's history does not edit.

**The thresholds move little.** `SIM_MIN` from 0.4 to 0.9 moves the statements from 98.31 to 98.08 percent; with no similarity at all
97.45. `RENAME_MIN` from 0.3 to 0.8 moves nothing, because Haro's history holds two renames and both clear every one of those bars; with the
rename pass off, definitions fall 98.68 to 98.56. 0.6 is the middle of a flat curve, and the claims **nearest it**
(`probes/near.py`) are mostly the line an author rewrote in place -- `cSeat = t[2]` becoming `aPlace = CondPlace(t)` in the commit that
renamed seat to place; a comment line reworded; a condition with a clause dropped -- which a reader would call the same line and no
instrument can prove is. **At least one is a claim a reader might refuse**: `cSeat = r[2]` becoming `v = aC[2]`, the same shape with
every name changed. That is what 0.6 costs, and why it is not lower.

**Verdicts.** Option A holds on Haro's own history: 98.3 percent of the statements a refinement could have targeted still resolve
after the next human edit, against the 95 percent the memo set. **K2 does not fire** (90 percent). Identity can be recovered from the
text, with no id written into it.

## 5. What this does not say

* **That the ids survive more than one edit.** Each pair is measured on its own; a lineage of fifty edits loses a little at every step,
  and the cache that holds the lineage (the last graph with its ids) is not built. The 95 percent is *per edit*.
* **That a false identity cannot happen.** At 0.6, 395 items of 28,996 were kept by similarity alone and 59 of them under 0.7; each is a
  claim that the edited line is the old one. A claim not made is a lost id, which the 95 percent floor sees; a claim made wrongly
  retargets a refinement, which nothing sees. The asymmetry is why the threshold is not lower.
* **That the history is representative.** It is Haro's own, three weeks old, one author, a spike growing fast; its edits are commits, not
  keystrokes. The memo's seven files agree with it (99.1 percent), and that is two samples, not a law.
* **That the agent never edits text.** CODEGRAPH 3.4 says its refinement is a graph transformation against ids taken from the *current*
  parse. This rung is the half that makes the human's edit survivable; the agent's half is rung 5.

## 6. Left, named

* The id cache (rung 3's store): the last graph with its ids, keyed by the content hash of the text it was parsed from.
* An id inside an expression (a statement id and a path), if a refinement ever needs one.
* `elif` and `case` matched by content rather than position.
* A move across functions, if a measurement ever shows it matters.
