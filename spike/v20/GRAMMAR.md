# Refinement over the program graph, built -- the computing altitude's change model (Haro v0.20, the twentieth rung)

**Rung 5 of the code-graph memo** (`haro/CODEGRAPH.md`, section 7), built on the author's "great! start Rung 5" (2026-10-05). **Written after** the fixtures in
`fixtures.txt` (89 of them: 65 composed by hand before `refine.py` existed -- the W discipline: fixtures first, prose second -- and 24 written after it from
the survivors of a mutation study, HF-89), after the court that judges them (`refine_check.py`), and after `refine.py`, whose first run against them failed
10 of the court's checks (section 8 is what building found).

**What this is, in one line.** A refinement is a *sentence* in the shape `rfn.haro` declares for the declared altitude (TARGET, KIND, FROM, TO, AUTHOR, POSTURE, REASON),
written against a *point* that a Ring program declares in a `<R:KIND ...>` comment tag; it goes through five stages in `stzRefinableCode`'s order, is lowered to RCP's twelve
primitives over rung 18's graph with rung 19's ids, and the diff a human reads is the printer's: one line out, one line in. **The agent never edits text.** Its only write
surface is a sentence against a point, a grammar scoped to the program it is looking at says in advance what it may write, and the gate decides the rest.

## 0. What exists, and what does not

| | status | where |
|---|---|---|
| the lift: tags in comments to points, rules and faults, over the graph with ids | **built** | `refine.py` (`lift`), section 1 |
| the sentence, its reader, and a command line (`refine.py program sentences [--write]`) | **built** | section 2 |
| the gate: structural, constraint, governance, trust, derivation; flagged on a cascade | **built** | `refine.py` (`evaluate`), section 3 |
| RCP's twelve primitives, each with the inverse captured before it lands, atomic | **built** | `refine.py` (`apply_prim`, `apply_tx`), section 4 |
| the event log, a revert as its own event, replay, commutation, the audit of a text edit | **built** | `Model`, `replay`, `commutes`, `audit`, section 5 |
| the write surface: a GBNF scoped to the program, judged by the engine's decoder | **built** | `scoped.py`, section 6 |
| the court: 11 families of check, 8 controls, a mutation study | **built**, `python haro/spike/v20/refine_check.py`, guard stage 24 | section 7 |
| the kinds `block`, `function`, `type`, `lib`, `custom`: declared, refused when proposed against | **not built** | section 9 |
| `node.create` and `node.delete` as the lowering of a sentence | **not built**: raw transactions only | section 9 |
| a writer that keeps the layout of a file that is not canonical (the estate's) | **not built**: `--write` refuses | section 9 |
| derivation rules that PROPOSE (RCP's `derived_proposals`) | **not built**: they only judge | section 9 |

## 1. The point

A point is declared where the code is, in a comment (charter 6.1: "the lift for foreign code"). `<R:KIND key="value" ...>` is read wherever it stands in a comment -- on
the statement's own line, or alone on the lines above it -- and the first tag in a comment is the one read.

| kind | attached to | its value | what it needs |
|---|---|---|---|
| `param` | `x = <literal>`: a number, a signed number or a string | the literal | `min`, `max` on a number |
| `algo` | `x = "name"`, or a call `x = F(...)` / `F(...)` whose callee is a plain name | the string, or the callee's name | `options` |
| `pipeline` | `x = ["a", "b", ...]`, a list of string literals | the stages joined by `|` | `options` |
| `rule` | nothing: it is a declaration of the program | `expr`: `<operand> <op> <operand>`, over point names and numbers | `message` |
| `lib` | `load "path"` | the path | declared, not built (section 9) |
| `block` `function` `type` `custom` | -- | -- | declared, not built |

Every point also takes `risk` (a tier from 1 to 4), `floor` (the lowest posture that may refine it) and `governed_by` (the governance whose actors decide).

**The literal in the code is the value.** `stzRefinableCode`'s tag form carries `value="..."` in the tag, which the code beside it can drift from; here the tag carries the
point's rules and nothing that the code already says, so a refinement edits the literal and the tag cannot disagree with it. **Attachment** is the memo's (3.3): a trailing
comment belongs to the statement on its line, a comment on its own lines to the next statement in the same block; a tag with nothing below it is an orphan.

**A fault is an error, and a gate that cannot read its own declarations refuses everything** (it fails closed): a tag with no name, an attribute twice, a name used twice
(names are exact, D24, and two that differ only in case are refused as look-alikes), a key not in lower case or a kind not in upper case, an orphan, two points on one statement, bounds on something that is not a number, options missing, a rule over a name nobody
declared or ordering something that is not a number. **A value outside its own bounds or options is not a fault: it is a state** (section 3, derivation), because a text edit
can leave one and the way back must be a refinement.

## 2. The sentence

```
DEFINE REFINE raise_vat AS (
  TARGET "vat", KIND param,
  FROM "0.20", TO "0.30",
  AUTHOR "mansour", POSTURE trusted,
  REASON "the rate went up"
) RATIONALE "a rate is a parameter"
```

Seven required seats (`rfn.haro`'s five and the spike's two), three the charter names as optional: `AT` (the id of the statement the proposal was drafted against: rung 19's id,
so it survives a human edit -- section 5), `CASCADE` (the ids of the statements that read the name: stated, it becomes an assertion), `REVERTS` (the event the sentence undoes).
`TARGET` is a point's name, or `name.attr` to refine the point's own rules: `min`, `max`, `options`, `risk`, `floor`, `governed_by` ("the rules themselves are refinable").
Strings are written in `"`, `'` or a backtick, and have no escapes, as Ring's have none (F-55): a value holding all three cannot be proposed at all, nor one
holding a line break (a refinement is one line out, one line in).
`FROM` is a compare-and-swap: the value the proposer saw, compared as a number when it is one (`0.2` is `0.20`) and as written otherwise. **Names and words are
exact** (D24): `KIND param`, `POSTURE trusted`, a point, an actor and a governance as declared; a near miss is refused with the declared spelling named. **A
no-op is not a refinement** (D25): TO the text FROM found is refused, `nothing to refine`.

`python haro/spike/v20/refine.py program.ring sentences.rfn [--ctx governance.txt] [--write]` runs the sentences in order against what the earlier ones left, prints each
verdict, the primitives it lowered to and its diff, and exits 0 (all admitted), 1 (one refused) or 2. `--write` replaces the program with the canonical text of the result and
**refuses when the program is not already canonical** (rung 3's `rnxc fmt --write`, never on a tree that is not yours to reformat): the diff would otherwise carry layout the
refinement did not make.

## 3. The gate

Five stages, in the order `stzRefinableCode.To()` runs them; the first to fail ends the proposal, and **a proposal that fails anywhere changes nothing** (the gate works on a copy).

| stage | asks | refuses with |
|---|---|---|
| **structural** -- "delegated back to the language itself" (charter 6.4) | the sentence is a sentence; the declarations lift; the point exists; its KIND is the declared one and it is built; AT is the id it stands at; FROM is what it holds now; TO has the right shape (a number, a string Ring can write, a function the program defines and that takes as many arguments as the call passes, a governance that exists); for a revert, the event exists, was admitted, is not reverted, its prior state is TO and its post state is what is there; and, once the stages below have let it through the bounds, **the refined program is read back by the compiler's own parser and is the same graph** | `stale: 'floor' is at id 2, not 1`; `'HeapSort' takes 2 argument(s), the call passes 1`; `kind 'algo' does not match point 'vat', which is declared param` |
| **constraint** | the point's bounds, options and shape: a number inside `min` and `max`, an algorithm among its `options`, a pipeline whose every stage is an option, appears once, and is not empty; a bound that does not pass the other | `0.95 above max 0.9`; `'radix' not in options quick|merge|heap` |
| **governance** | `stzGovernance.MayProceed` over the action `refine-<point>`: a declared **risk tier** (undeclared never proceeds), the actor's **permission**, an **authority** that covers the tier -- only for a point that names its `governed_by`, and a governance that is not configured refuses | `refused: 'bot' holds 'delegated' authority (level 2) but 'refine-sort' is risk tier 3 (SHOULD does not cover it)` |
| **trust** | the posture of the origin (`trusted` 3, `external` 2, `sandboxed` 1, `llm` 0) clears the point's `floor` -- origin is not identity: the same actor, the same value | `posture :llm below the required floor for 'sort'` |
| **derivation** | the state the change would leave: the point's **own** bounds and options hold, every `rule` that names the point holds, and a stated `CASCADE` is the readers' ids | `rule 'vat-above-floor' violated -- vat must not drop below floor` |

**A refinement answers for the rules of the point it touched, and for nothing else.** `stzRefinableCode` evaluates every rule of the program on every proposal, so a program
that already breaks one cannot be refined at all, and one text edit freezes every point. Here a program already outside a bound or a rule can be repaired by a refinement and
refined elsewhere meanwhile (fixtures 32, 33); where the program is consistent the two gates are the same function (section 7, S).

**A refinement of a rule is a refinement of a point, and the rules of a gate are not for every origin.** `vat.max`, `sort.options`, `vat.governed_by` go through the same five stages
with two additions: the origin must be `trusted` whatever the point's own floor says (a rule cannot be changed by a model-composed proposal, "not by convention, by construction",
charter 6.4), and **widening a rule is always a tier-4 act** -- a larger maximum, a smaller minimum, an option added, a risk tier or floor lowered or removed, a governance moved or
dropped -- which only the highest authority covers, whatever the point's own tier is. Tightening is the point's own tier.

**The outcome** is RCP's (5.4): `admitted`, `flagged`, `rejected`; the stage that refused and why; the five stages' results; the cascade; the transaction and its inverse; the diff.
**Flagged** is admitted with a warning: the name the literal gives is **assigned again** somewhere else in the file, so the refinement is not the only definition of it
(`also assigned at id 2 (<top>)`). The cascade is the readers of the name -- each as the id of its statement and the function it stands in -- by Ring's case-folded name over the whole file:
an over-approximation across scopes, and it says so by printing the owner.

## 4. The twelve primitives

A refinement is lowered to a **transaction** -- a list of RCP's primitives -- applied atomically to a copy (all or none), each one returning the inverse **captured before it lands**.
The inverse of a change carries what it expects to find, so it refuses to run over a state that has moved on since (`conflict`).

| primitive | what it does to the graph | inverse | reached by a sentence |
|---|---|---|---|
| `node.update_property` | a property of a node named by item id and path: the text of a trailing comment, of a literal | itself, with the old value | `vat.max`, `vat.min`, `.risk`, `.floor` |
| `node.create` | a node in a block of a parent, at an index; ids kept if it holds them, fresh if not | `node.delete` | **no** -- transactions only |
| `node.delete` | removes an item; its inverse restores it with the **same ids**, at the same index | `node.create` | **no** -- transactions only |
| `edge.create` | a `governed_by` edge: the attribute appended to the tag | `edge.delete` | `vat.governed_by` from nothing |
| `edge.delete` | removes it; the inverse puts it back as the same attribute, in the same place | `edge.create` | `vat.governed_by` to nothing |
| `edge.retarget` | a `governed_by` edge to another governance, or a `calls` edge: the callee a statement calls | itself, reversed | an `algo` point on a call; `vat.governed_by` |
| `refinement.set_value` | the literal of a param or an algo named by a string; the old literal's text is kept, so a single-quoted string comes back single-quoted | itself | `vat`, `sort` |
| `refinement.add_option` | an option of an algo or a pipeline, at a position | `remove_option` | `sort.options` |
| `refinement.remove_option` | removes it; the inverse restores its position | `add_option` | `sort.options` |
| `pipeline.insert_stage` | a string node in the list, at an index | `remove_stage` | `steps` |
| `pipeline.remove_stage` | removes one; the inverse restores its literal | `insert_stage` | `steps` |
| `pipeline.reorder_stages` | the list in a given order | itself, with the old order | `steps` |

**The lowering of a pipeline** is an algorithm, and its result is checked: remove what is not wanted, insert what is missing at its place in the new order, reorder what is left if
it is still out of order -- so `a|b|c` to `c|b|a` is one primitive and `parse|check|emit` to `emit|optimize|parse` is three, in that order.

## 5. Events, reversal, replay, commutation, and the text edit

**An event is a record, and a revert is a refinement.** Every proposal, admitted or refused, is an event in the model's log: its sentence, its verdict and stage, and the digest
of the canonical text before and after (content-addressed states). A revert is written as a sentence with `REVERTS n` -- `Model.revert(n)` writes it -- and is **gated like any other**:
the same governance and trust stages (an `llm` origin cannot undo a trusted change to a floored point), no constraint stage (it restores a state that was admitted), derivation
on the state it leaves. It names its event, which becomes `reverted_by`; nothing is erased. A revert of an event whose point has since changed is a **conflict**, not a silent overwrite.

**Replay is deterministic.** The log, serialised as JSON and run again from the base text through the gate, gives the same verdicts and the same final text; the transactions of the
admitted events applied with no gate give the same text. Both are checked for every fixture.

**Commutation** is RCP's predicate over two sentences' footprints: a value refinement reads its point's declaration and the value of every point that shares a rule with it, and
writes its value; a refinement of a rule writes the declaration. Two commute unless one writes what the other reads or writes. It is **sound** on every pair tried -- nothing it calls
commuting gives two results when applied in either order -- and conservative: a pair that shares a rule is called conflicting even when the orders agree.

**A human edit made as text is read back (`audit`).** The edit's graph is given the old ids by rung 19's matcher; each point whose literal or rule changed is the sentence that would
have made the same change, judged by the gate **on the old program** as the author and at the posture the caller names; every other change is counted as raw. So a model that
writes the file directly is judged by the gate that would have judged its sentence, after the fact, and a respelling (`0.20` to `0.2000`) is a refinement and a reformat is not.

**A sentence drafted against ids lands after an edit.** `AT` is the id of the statement the point stands on in the parse the proposal was drafted against; the matcher carries it across
a human edit, and the gate refuses it as stale -- never applies it elsewhere -- when the edit changed the value it expected (`FROM`), removed the point, or moved the point to an id
of another statement (fixtures 29 to 31, H below).

## 6. The write surface

Charter 6.2: the refinement sentence's grammar is the agent's write surface. `scoped.py` writes, for ONE program as it stands, the GBNF of the sentences that may be written against it:
each point is an alternative of its own, so the point's name, its kind, **the id of its statement (AT), the value the sentence expects to find (FROM), the readers of its name (CASCADE)**,
the options TO may take, and the governances that exist are in the grammar. `posture` and `author` can be fixed to what the harness stands for: an agent run under `:llm` cannot write `:trusted`.
What no context-free grammar says stays the gate's: a number inside its bounds, an actor's authority, a rule over two points, a callee that exists, a list of options without a
duplicate, a revert (the harness writes those).

**The decoder holds a scoped grammar only up to a size** (HF-87). The engine's decoder takes at most 128 rules and 1024 elements in a rule, and makes every
parenthesised group and every repeat a rule of its own, so the grammar names its shapes once (a number, a tier, a posture, a governance, a list of options)
and gives each point one rule of its own: a point costs about seven rules, and a program of 10 or 11 points is held where one of 15 is not. **So the grammar is
scoped to the points a task names** (D26, `scoped_gbnf(model, points=[...])`): an agent can write only what its task may change, and the grammar stays small
whatever the program; a task naming a point the program does not declare is refused by name.

## 7. The court

`python haro/spike/v20/refine_check.py [--plant] [--quick] [--wide] [--fx]` (exit 1 on any failure); guard stage 24; about five and a half minutes (327 s on 2026-10-19). `--fx` runs the fixtures and the
small checks in about ten seconds.

| | what it judges | number |
|---|---|---|
| **F** | 91 fixtures through the gate (177 steps: 72 admitted, 2 flagged, 103 refused): the verdict, the stage, the words, the primitives. **For every fixture, whatever it says:** a refused proposal changes neither the text nor the ids; an admitted one changes exactly one line and no id; the inverses put the original back, byte for byte, with its ids; the log replayed from JSON through the gate, and the transactions with no gate, give the same text; the refined text is canonical on **the other printer** (`rnxc fmt --check`); and 4 programs run on the oracle and on rnxc before and after, printing what the refinement says they should | 0 fail |
| **T** | the twelve primitives (23 transactions), each applied, undone and applied again; a transaction that fails halfway leaves nothing; an inverse refuses a state that has moved on | 12 of 12 |
| **L** | declarations that do not lift (14 fixtures): the gate fails closed | 0 fail |
| **C** | the commutation predicate over every pair of a pool of 16 sentences, each in both orders | 60 commuting (and are), 11 conflicting and order-dependent, 49 conservative, **0 unsound** |
| **A** | four text edits read back as refinements (a bound broken, a rule widened, a reformat, a respelling) | 0 fail |
| **S** | **Softanza's own `stzRefinableCode`** on the Ring++ package, put 504 proposals (56 the fixtures', the rest a sweep of points x values x actors x postures over two programs): admitted-or-not, the refusing stage and the value left | **418 agree**; 85 the language itself refuses at a stage the live gate has none for (most of them no-ops, D25); 1 carries a value its tag form cannot hold; 0 disagree |
| **G** | a retargeted call, 0/1/2 arguments x a function of each arity, one that does not exist, a case variant: the structural stage says it stands exactly when `rnxc graph` shows a static call edge from the refined program -- but for a case variant, which Ring binds and the gate refuses by name (D24) | 18 of 18 |
| **W** | the grammar scoped to each program (83 grammars, each held by the engine's constrained decoder, and a task's grammar of 3 points of a 15-point program, D26): every admitted fixture sentence its author could write is a sentence of it; the decoder refuses all 35 proposals the gate refuses for their shape; 600 sentences sampled from it are all accepted and **none is refused for its shape** | 0 fail |
| **D** | 9 controls that must FAIL (a gate that skips each of its four stages, one that edits the live program before judging, a cascade that sees nothing, an inverse that loses ids, a revert that does not check, a grammar that does not name the points) | each fails the court |
| **H** | Haro's own history: a refinement drafted against a literal assignment at one revision, **does it still land at the next?** | 1,550 of 1,578 land (98.2%) |
| **K** | a literal of each of 80 real Ring files made a point and refined | 165 literals, 0 fail |
| mutation | 519 defects of one token each put into the engine (`probes/mutate.py`), the fast court asked | 505 killed (97.3%); the 14 left change nothing a sentence can reach (HF-89) |

**K** judges each by a second route (the graph route and the line spliced by hand give the same text), by the other printer, by the compiler (`rnxc dis`: the same instructions, which
the 32-bit immediate is the one place it cannot be -- a literal that crosses 2^31 changes `loadi` to `loadk`, 3 of them, counted apart), and by locality (one line out, one line in).

## 8. What building found

**HF-85 -- Two gates, one verdict wherever both can judge.** Softanza's own `stzRefinableCode`, put the same 501 proposals on the Ring++ package (the
fixtures' 53 and a sweep of 448), agrees with this gate on admitted-or-not, the refusing stage and the value left in all 488 it can judge; 12 more are refused by
the language itself at a stage the live gate has none for, and 1 carries a value its tag form cannot hold. Where they differ it is measured
(`probes/live_gate_limits.ring`): the live gate RAISES R41 on a value that is not a number instead of refusing it, cuts a value at a double quote without a word,
and judges every rule of the program on every proposal, so a program that already breaks one cannot be refined at all (fixtures 32 and 33 are not put to it).
And `rnxc graph` judges a retargeted call: the structural stage says it stands exactly when the compiler binds a static edge from the refined program, 21 of 21.

**HF-86 -- A refinement is one line, on real code and across real edits.** 165 literals of 80 real Ring files made points and refined: each one line out and
one in, canonical on `rnxc fmt`, restored by its inverse, and in 146 the same code shape under `rnxc dis` (3 cross the 32-bit immediate, where the instruction
itself changes). Across 38 pairs of consecutive revisions of Haro's own history, 1,550 of 1,578 drafted refinements (98.2%) still land after the next human
edit; of the 28 that do not, 22 are gone in a refactor and 6 now name a different variable -- which AT refuses, where a gate checking only the name would
apply the change elsewhere.

**HF-87 -- The write surface is bounded by the decoder, and the first grammar met the bound at five points.** The engine's constrained decoder
(`gbnf_machine.zig`, Softanza's) holds at most 128 rules and 1024 elements in one rule, and makes every parenthesised group and every repeat a rule of its own.
The grammar scoped to a program gave each point its own copy of the number, tier and posture patterns and inlined every point's sentences: fixture 36, five
points, crossed the rule count -- and the court's thread then died without a word, unpacking an answer that was not there (it reports the refusal by name now).
Shared named rules and one rule per point bring a point to about seven rules: a program of 10 or 11 points is held, one of 15 is not (`scratch/capacity.py`).
**A program with more points has no single scoped grammar**: a larger limit in the decoder, or a grammar scoped to the points a task names, is the next design
question, and the first is an ask of the engine's owner.

**HF-88 -- Names: this gate folded them as Ring does; `stzRefinableCode` matched them exactly -- decided for exact (D24).** `TARGET "Vat"` for a point
declared `vat` was admitted here and refused at the structural stage by the live gate. Found by fixture 37, the first fixture to spell a target otherwise.
The author's delegation of 2026-10-19 decided it the Haro way: no folding in the Haro layer, look-alikes refused, a near miss refused with the declared
name. The two gates now agree by construction, and `stzRefinableCode` needs no change.

**HF-89 -- The court is load-bearing, and its mutation study said where it was not.** 519 one-token defects put into the engine: the fast court killed 376
(72.4%) on 2026-10-05. The 143 survivors were read one by one -- about twenty refusals no fixture reached, the revert checks, widening at its edges, the case
folds, the boundaries of rules and bounds, the cascade's writes, the shapes a tag cannot attach to, transaction indices and the commutation footprint -- and 24
fixtures written from them (36 to 46, L10 to L14, T17 to T23, C02) with one line-break check kill 129 more: 505 of 519 (97.3%), every new expectation met by the
engine on its first run. The 14 left change nothing a sentence can reach: no posture ranks below 0; a sentence carries no line break and no value with all
three quotes; inserting at the end of a list is appending; three refusals stand behind literals the printer always writes; the inverse's own state check
catches what one check misses; an action name appears only in a refusal's text; and widening at equality, for a risk tier and a floor, is a no-op refinement,
which decision 7 admits and the court's one-line property keeps out of every fixture.

**HF-90 -- One raise in 488, on 2026-10-05, was a compiler the package had not been given.** The live stack raised R14 `nodesids` once and passed alone: the
package's `rnxc` was a copy of 2026-09-28, whose lambda lookup matched a byte offset across every file of the unit (ringpp's `CLAUDE.md`). The court says first
now whether the package's compiler is older than the repository's, and on 2026-10-19 they are the same build.

## 9. What it does not say

- **The kinds `block`, `function`, `type`, `lib`, `custom`.** Declared and refused when proposed against, not built. A `block` refinement -- an agent proposing the body of a function inside its signature
  -- is where `node.create` and `node.delete` would be the lowering of a sentence, and the first thing to build next; it needs the parser of the face to read a proposed statement list, and a derivation stage
  that can ask the compiler (`rnxc check`) what the body does to the program's calls.
- **A writer for a file that is not canonical.** The estate's files are not (rung 3: none of Softanza's 6,061 is `fmt`'s fixed point), and the refinement's text is the printer's. `--write` refuses; a span-preserving
  writer needs the byte span of the literal, which the lossless export (`rnxc dump --json`) has and the graph (L1) does not keep. Until then, a refinement on the estate is a diff to read or `fmt` first, with the
  author's word (D23).
- **Derivation rules that propose.** RCP's derivation stage can produce `derived_proposals`; here a rule only judges, as `stzRefinableCode`'s do.
- **RCP's authority taxonomy.** The twelve authorities (`developer.direct`, `planner.graphplanner`, ...) and the policy authorities are the governance table's actors and levels here; the mapping is not drawn.
- **Edges beyond `calls` and `governed_by`.** `references`, `depends_on` and the rest are L2 (`rnxc graph`), which has no `new K` edge yet and no references.
- **A lineage of events across sessions.** The log is a JSON-able list in memory; the file format of an event history, and who owns it, are not decided.
- **The sentence's own GBNF is the agent's surface for VALUES, not for reverts**, which the harness writes.

## 10. Decisions taken in the spike, for the author's reading

Taken on the delegation of 2026-10-05 ("take whatever decision you think is wiser on my behalf then continue"), each with what it costs; none is in the charter until he reads it.
7, 9 and 10 were decided on his delegation of 2026-10-19 and are in the charter as D24 to D26.

1. **Points are declared by tags at this altitude.** The charter says a declaration is its own point; Ring has no such declaration, so the lift for foreign code is the tag. *Cost:* a point exists only where someone wrote a tag, which is
   the point of "declared" and the reason nothing in the estate is refinable today (7 tags in Softanza's base, all in strings).
2. **The literal is the value; the tag carries no `value=`.** *Cost:* `stzRefinableCode`'s tag form is not read by this lift (one more form to migrate).
3. **A refinement answers for the rules of the point it touched.** *Cost:* the two gates differ on a program that already breaks a rule (section 3); where it is consistent they agree.
4. **Rules are refinable, widening is tier 4, and a rule's refiner must be `trusted`.** *Cost:* an `llm` origin can never change a bound, an option or a floor -- which is the intent, and is more than `stzRefinableCode` says.
5. **A revert is a refinement with REVERTS, gated by governance and trust, and a conflict is refused.** *Cost:* undoing a trusted change on a floored point needs a trusted origin.
6. **`flagged` means the name is assigned again elsewhere.** *Cost:* a PARAM on a variable the program also reassigns is always flagged, which is the warning's meaning.
7. ~~A no-op refinement (TO is FROM) is admitted and changes nothing~~ -- **reversed by D25 (2026-10-19): a no-op is refused**, `nothing to refine`; every
   admitted refinement changes one line, which the court required already (HF-89). *Cost:* the live gate admits a no-op, so the two differ there, counted apart.
9. **Names are exact (D24)**, look-alikes refused, a near miss named; Ring's folding only where the gate describes the Ring program (the cascade).
10. **The grammar is scoped to the points a task names (D26)**; the decoder's cap stays where it is.
8. **`--write` refuses on a file that is not canonical.** *Cost:* the estate needs `fmt` first (D23) or the span-preserving writer of section 9.
