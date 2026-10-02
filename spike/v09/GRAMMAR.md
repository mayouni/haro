# Haro v0.9 -- the A letter: RUN, structured steps that always stop

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.9 is the declaring altitude of Haro grown by what A -- the
alphabet's A letter, the ALGORITHM: "bounded iteration, structured steps", the one letter
with no shipped ancestor (`haro/SPIKE.md`, the ninth rung) -- needs and nothing else. v0.9
refuses nothing v0.8 accepted (fixture A4 is v0.8's A2, unchanged).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `RUN` | `OF [kind, steps, result]` the kind that runs, its step-list seat and its result-name seat; `COMPUTE [kind, into, value]`, `COLLECT [kind, into, value]`, `GROUP [kind, into, by, value]`, `BRANCH [kind, when, then, else]`, `ITERATE [kind, over, as, do]` -- each a kind of the language and its seats by role | the five constructs are extracted from the three named sources: Zcd's names for what Zex runs and VizCode composes (SEQUENCE is the step list itself, BRANCH its then/else, ITERATE its body; TRY, PARALLEL and RETRY are not A's -- they are F's waits and the engine's), RingFlex's seam (computation belongs in a declared, judged place), W (a total evaluator). A role's seat is checked by type: `into`, `over`, `as` are `name` seats, `value`, `when`, `by` are EXPRESSION seats, `steps`, `result`, `then`, `else`, `do` are list seats (R2, R3, R6); a language runs one way (R4) |
| a list seat whose element is a `UNION` of declarations | `steps: [step]` with `UNION step AS (OF [compute, collect, group, branch, iterate])` | a step list names steps of several kinds, each resolved by name in one namespace; the court judges it in the references pass, and a MESSAGES entry may speak for it (A3, R5) |

## Grammar (EBNF), the v0.8 text with these additions

```
RUN:         OF name_list, COMPUTE name_list, COLLECT name_list, GROUP name_list,
             BRANCH name_list, ITERATE name_list
             -- each name_list a kind and its seats, in the role order above

in a sentence: a step list is a name_list whose names are declarations of the UNION's kinds
```

## What the forge makes of it

A language that declares a RUN gets its court as before, and its sentence court loads
`run_lib.ring` and gains the verb:

```
<lang>_court.ring run <file> <algorithm> <record json>     the result, as JSON
```

The record is a JSON object; its fields are the names the expressions read (`ABSENT
refuse`: a name that holds nothing is refused by name). `COMPUTE` writes a value into a
name; `COLLECT` appends to a list born at the first append; `GROUP` files a value under a
key, groups in the order keys first appear, as `[[key, values], ...]`; `BRANCH` takes its
THEN or ELSE list by the condition's truth -- under `EQUALITY kind` the value's own truth
(W's: a number is true when not 0, a text always), under `value` a boolean shape (zql's);
`ITERATE` binds each item of the collection the record holds under OVER to the AS name
and runs the DO list -- over a SNAPSHOT of the collection, so a COLLECT into the same
list cannot lengthen the walk. The result is the value of the one RESULT name, or the
list of several. There is no call, no recursion, no loop but over a collection: **a step
tree that leads back to a step on the way down is refused at `check`** (`RunCheckAcyclic`),
and the guard's stage 12 plants one to show it. Termination is structural: every walk
is bounded by the collections the record holds when it begins.

## A, re-declared, and what the re-expression is

`a_v09.haro` declares A: one EXPRESSION (`aexpr`, W's grammar over the record's names with
aggregates and ROUND, `EQUALITY kind`), five construct kinds, the `step` union, the
`algorithm` kind, and the RUN. A has no ancestor artifact to re-express, so the judge was
MADE from numbers other repositories pin: stz's 29 W cases (6 constant evaluations, 4
maps, 8 filters, a count, a partition, a groupby, 3 reduces, 5 refusals) and zing's three
`indice` flow cases (the FORMULA as a COMPUTE, its VALIDATE as a BRANCH, the empty survey
answering VIDE), each re-expressed as an algorithm in `a/w_in_a.a` BY A GENERATOR that
copies the expected values from the source files and never types one; plus three hand
cases the W shape cannot say -- nested iteration, a running maximum, a branch inside a
branch -- computed by hand and marked so.

**What the re-expression is**: W's `@item` is the record's name `item`, bound by ITERATE;
W's `@accumulator` is `acc`, seeded by a COMPUTE; a `map` is an ITERATE whose body COLLECTs
the expression; a `filter` an ITERATE whose body BRANCHes to a COLLECT; `count` a seeded
COMPUTE bumped under a BRANCH; `partition` two COLLECTs on a BRANCH with `RESULT [yes,
no]`; `groupby` a GROUP; `reduce` a seeded COMPUTE folded by an ITERATE; `reduce_noinit`
the same with a first-item flag. W's five refusals: four are refused at `check`, where the
court parses every expression seat (`print(item)` and `item > 2 zzz` as trailing input,
`(item > 2` unclosed, the empty expression); the fifth -- a name nothing holds -- at
`run`, by name, as `ABSENT refuse` says.

## Measured

`a/w_in_a.a`: 29 algorithms over 77 steps, a sentence of A on `rnxc` and the oracle.
`v09/a_cases.json`: 35 cases -- 24 W values, 5 W refusals, 3 zing flow cases, 3 hand --
35 of 35 on `rnxc` and the oracle, byte-identical, on the first run once the court's
shape pass learned that a LIST of a union is a name list (its first reading tried the
union's scalar shapes on it). Four artefacts byte-identical on both runtimes. The
machine court 117 of 120, the fleet court 32 of 32, W 29 of 29, Z 16 of 16, Q 25 of 25,
F 26 of 26 unchanged. Pinned at 35.
