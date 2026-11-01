# Refinement over the program graph, built -- the computing altitude's change model (Haro v0.20, the twentieth rung)

**Rung 5 of the code-graph memo** (`haro/CODEGRAPH.md`, section 7), built on the author's "great! start Rung 5" (2026-10-05). **Written after** the fixtures in
`fixtures.txt` (89 of them: 65 composed by hand before `refine.py` existed -- the W discipline: fixtures first, prose second -- and 24 written after it from
the survivors of a mutation study, HF-89), after the court that judges them (`refine_check.py`), and after `refine.py`, whose first run against them failed
10 of the court's checks (section 8 is what building found). Four files of fixtures came after, each written before its engine: `fixtures_block.txt` (15),
`fixtures_function.txt` (20), `fixtures_allowlist.txt` (8) and `fixtures_method.txt` (13) -- 147 with the 91 of `fixtures.txt` (sections 11 to 14).

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
| the court: 11 families of check, 21 controls, a mutation study | **built**, `python haro/spike/v20/refine_check.py`, guard stage 24 | section 7 |
| the kind `block`: an agent proposes the BODY of a function whose signature a human declared | **built** (2026-10-19) | section 11 |
| `node.create` and `node.delete` as the lowering of a sentence | **built**, for a body | section 11 |
| the kind `function`: an agent proposes a function that is not there yet, or the body of one that is | **built** (2026-10-19) | section 12 |
| a point's own `calls` and `writes` refined as rules: widening a tier-4 act, narrowing below the body refused | **built** (2026-10-20) | section 13 |
| `reads`: the globals and attributes a body may read, closed by default | **built** (2026-10-22) | section 15 |
| the kind `method`: an agent proposes a method of a class that is not there yet, or the body of one that is | **built** (2026-10-20) | section 14 |
| **a local model as the agent**, on sixteen tasks (the body free or under its point's grammar, one line or lines) | **measured** (2026-10-21): 1.5B 3 of 16 on one line, **10 of 16 on lines under the grammar** (HF-116) | `agent/AGENT.md` |
| the agent's write surface for a body: the lines grammar of the point, `scoped.body_lines_gbnf` | **built** (2026-10-21), guard stage 28 | `agent/body_gbnf.py` |
| a body kind on a library file (a class and no top level), refined through the program that loads it: a closed derivation (D32) | **built** (2026-11-01) | section 16 |
| the kinds `type`, `lib`, `custom`: declared, refused when proposed against | **not built** | section 9 |
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
| `block` | a `func`, the tag alone on the line above it | the body's canonical text, named by its digest `sha:` + 12 hex | `calls`, `writes`, `reads` (sections 11, 15) |
| `function` | nothing: a comment alone at the top level | `absent`, or the body's digest | `params`, `calls`, `writes`, `reads` (section 12) |
| `method` | nothing: a comment among a class's members, with a member below it | `absent`, or the body's digest | `params`, `calls`, `writes`, `reads` (section 14) |
| `type` `custom` | -- | -- | declared, not built |

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

Five stages, in the order `StzRefinableCodeQ().To()` runs them; the first to fail ends the proposal, and **a proposal that fails anywhere changes nothing** (the gate works on a copy).

| stage | asks | refuses with |
|---|---|---|
| **structural** -- "delegated back to the language itself" (charter 6.4) | the sentence is a sentence; the declarations lift; the point exists; its KIND is the declared one and it is built; AT is the id it stands at; FROM is what it holds now; TO has the right shape (a number, a string Ring can write, a function the program defines and that takes as many arguments as the call passes, a governance that exists); for a revert, the event exists, was admitted, is not reverted, its prior state is TO and its post state is what is there; and, once the stages below have let it through the bounds, **the refined program is read back by the compiler's own parser and is the same graph** | `stale: 'floor' is at id 2, not 1`; `'HeapSort' takes 2 argument(s), the call passes 1`; `kind 'algo' does not match point 'vat', which is declared param` |
| **constraint** | the point's bounds, options and shape: a number inside `min` and `max`, an algorithm among its `options`, a pipeline whose every stage is an option, appears once, and is not empty; a bound that does not pass the other | `0.95 above max 0.9`; `'radix' not in options quick|merge|heap` |
| **governance** | `StzGovernanceQ().MayProceed` over the action `refine-<point>`: a declared **risk tier** (undeclared never proceeds), the actor's **permission**, an **authority** that covers the tier -- only for a point that names its `governed_by`, and a governance that is not configured refuses | `refused: 'bot' holds 'delegated' authority (level 2) but 'refine-sort' is risk tier 3 (SHOULD does not cover it)` |
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
| `node.create` | a node in a block of a parent, at an index; ids kept if it holds them, fresh if not | `node.delete` | a `block` body: a statement that comes |
| `node.delete` | removes an item; its inverse restores it with the **same ids**, at the same index | `node.create` | a `block` body: a statement that goes |
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
| **F** | 126 fixtures through the gate, the BLOCK and FUNCTION kinds' 35 among them (234 steps: 88 admitted, 2 flagged, 144 refused): the verdict, the stage, the words, the primitives. **For every fixture, whatever it says:** a refused proposal changes neither the text nor the ids; an admitted one changes exactly one line and no id -- a BODY refinement changes nothing outside its function, keeps the order of every id that stays and loses none it did not delete; the inverses put the original back, byte for byte, with its ids; the log replayed from JSON through the gate, and the transactions with no gate, give the same text; the refined text is canonical on **the other printer** (`rnxc fmt --check`); and 11 programs run on the oracle and on rnxc before and after, printing what the refinement says they should | 0 fail |
| **T** | the twelve primitives (23 transactions), each applied, undone and applied again; a transaction that fails halfway leaves nothing; an inverse refuses a state that has moved on | 12 of 12 |
| **L** | declarations that do not lift (14 fixtures): the gate fails closed | 0 fail |
| **C** | the commutation predicate over every pair of a pool of 16 sentences, each in both orders | 60 commuting (and are), 11 conflicting and order-dependent, 49 conservative, **0 unsound** |
| **A** | four text edits read back as refinements (a bound broken, a rule widened, a reformat, a respelling) | 0 fail |
| **S** | **Softanza's own `stzRefinableCode`** on the Ring++ package, put 504 proposals (56 the fixtures', the rest a sweep of points x values x actors x postures over two programs): admitted-or-not, the refusing stage and the value left | **418 agree**; 85 the language itself refuses at a stage the live gate has none for (most of them no-ops, D25); 1 carries a value its tag form cannot hold; 0 disagree |
| **G** | a retargeted call, 0/1/2 arguments x a function of each arity, one that does not exist, a case variant: the structural stage says it stands exactly when `rnxc graph` shows a static call edge from the refined program -- but for a case variant, which Ring binds and the gate refuses by name (D24) | 18 of 18 |
| **W** | the grammar scoped to each program (83 grammars, each held by the engine's constrained decoder, and a task's grammar of 3 points of a 15-point program, D26): every admitted fixture sentence its author could write is a sentence of it; the decoder refuses all 35 proposals the gate refuses for their shape; 600 sentences sampled from it are all accepted and **none is refused for its shape** | 0 fail |
| **D** | 16 controls that must FAIL (a gate that skips each of its four stages, one that edits the live program before judging, a cascade that sees nothing, an inverse that loses ids, a revert that does not check, a grammar that does not name the points; and the BLOCK and FUNCTION kinds' seven rules taken out in turn -- no calls or writes allowlist, no shape refusals, a lowering that keeps no statement, a compiler that finds nothing, a lift that reads a BLOCK tag or a FUNCTION tag without checking it, a new function written beside its tag) | each fails the court |
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

- **The kinds `type`, `lib`, `custom`.** Declared and refused when proposed against, not built. `block`, `function` and `method` are built (sections 11, 12, 14).
- **A writer for a file that is not canonical.** The estate's files are not (rung 3: none of Softanza's 6,061 is `fmt`'s fixed point), and the refinement's text is the printer's. `--write` refuses; a span-preserving
  writer needs the byte span of the literal, which the lossless export (`rnxc dump --json`) has and the graph (L1) does not keep. Until then, a refinement on the estate is a diff to read or `fmt` first, with the
  author's word (D23).
- ~~A body kind on a library.~~ Built 2026-11-01 (section 16, D32): the derivation is closed, and a library is refined through the program that loads it.
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

## 11. The BLOCK kind -- a function's body, proposed by an agent (built 2026-10-19)

**On the author's "go"** (2026-10-19, after "what is next?"). The fixtures came first, `fixtures_block.txt`, 15 of them (B01-B11, L15-L18), committed
before the engine read them; its header is the design. `python haro/spike/v20/refine_check.py --block` runs them alone in seconds, and the full court
folds them in.

**The point.** `# <R:BLOCK name="gross" calls="Tax|Round" writes="$nTotal">` alone on the line above a `func`. The point is the function's body; the
signature -- its name and parameters -- is the human's, and no block refinement changes it. The tag cannot stand on the func line: the grammar reads a
comment there as the body's first line (the printer moves it there), which would put the tag inside its own point -- found by the first probe, and the
fixtures moved (HF-95). `calls` names every function, method, class (`new K`) and builtin the body may call, spelt as declared (D24); absent, nothing.
`writes` names every global (`$x`), attribute (`@x`) and parameter whose CONTENTS the body may write -- a list parameter is the caller's list; absent,
the body writes its own locals only, and rebinding a parameter is one (C-29). A name in either list that the program does not have is a fault; a near
miss names the declared spelling.

**The value** is the body's canonical text, named by its digest: `sha:` and the first 12 hex digits of its SHA-256 (the empty body is
`sha:e3b0c44298fc`). FROM is that digest -- a compare-and-swap over what the proposer saw, comments included, which a one-line string cannot carry --
and the lift prints it. TO is the new body on ONE line, as Ring reads statements without separators (`nTax = Tax(nNet) return nNet + nTax`); the
compiler's parser reads it and the printer writes it out canonically. A respacing is not a refinement (D25). A revert's TO is the digest of the
state it returns to: the event's inverse transaction carries the body, comments and ids included.

**The gate.**

| stage | for a body |
|---|---|
| structural | TO parses, and is a statement list and nothing else: it defines nothing (`func`, `class`, `package`), loads nothing, holds no `eval`, no `call` by name, no brace block, no comment (the gate does not judge prose, and a model's comment can mislead the reader of the diff), no `bye`; FROM is the digest now; the refined program reads back as itself |
| constraint | every call is one `calls` names, by its declared spelling -- builtins too, and the function's own name; every write outside the frame is one `writes` names, and a loop variable, a `give` target and a `catch` binding are writes like any other, and a for-in variable is a reference into the list it walks, so writing through it writes that list's owner's contents (2026-10-22, HF-118); a member read or assignment whose class declares `get<name>` / `set<name>` is a CALL of it -- Ring runs it by itself -- and must be named in `calls` (`This.x` and `self.x` are exempt, as on Ring) |
| governance, trust | as for every point |
| derivation | `rnxc check` on the refined program reports no error or warning it did not report on the program before -- a wrong argument count (`rpp/type-arity`), a name nothing assigns (`rpp/uninitialized-variable`) -- and the refusal quotes it; a program whose absence rules the checker shuts (an eval, a loadlib) is not refined by a body at all |

**The lowering.** The old body and the new are matched statement by statement on their canonical text (difflib's longest matching blocks): a
statement that stays keeps its id and the comments attached to it (rung 18's rule: a comment belongs to the next statement); one that goes is
`node.delete`, one that comes `node.create` with a fresh id, deletes first. Inserting one statement between two that stay is one `node.create`.

**The court.** The 15 fixtures, each run as every fixture is (refusals change nothing, the inverses restore every id, replay, `rnxc fmt`), four of
them on the oracle and on rnxc before and after (`[]` then `[120]` for a body written into an empty signature); the body's locality in place of
"one line out, one line in": nothing outside the function changes, every id that stays keeps its order, none goes without a `node.delete`; the
write surface (section 6) fixes a block point's target and the digest FROM must be, and leaves TO one line of text, which no context-free grammar can
say is Ring; and five controls, each rule taken out in turn and caught by at least one fixture (HF-97).

**Not built, named:** ~~a `reads` attribute, closed by default~~ (built 2026-10-22, section 15; what is left open: an operator on an object a caller passes, an allowed callee's effects, output and termination -- HF-118, D28); ~~refining a BLOCK point's own `calls` and `writes` as rules~~ (built 2026-10-20, section 13: widening is a tier-4 act, as widening options is); a body proposed with a comment; a human's edit of a body read back by the audit as a block refinement (it is counted a raw
edit: the gate governs proposals, the human writes the body); a per-call check that a callee in `calls` is called with the right arguments before
the compiler is asked (the compiler answers it at derivation); the kinds `type`, `custom`.

## 12. The FUNCTION kind -- a function that may not be there yet (built 2026-10-19)

**On the author's "continue"**, after the BLOCK kind. The fixtures came first, `fixtures_function.txt`, 20 of them (FN01-FN12, L19-L26), committed before
the engine read them; its header is the design. `refine_check.py --block` runs them with the BLOCK kind's, in seconds.

**The point declares; it does not attach.** `# <R:FUNCTION name="Round" params="n|m" calls="floor" writes="$nTotal">` alone on a line at the top level, among
the statements. A BLOCK point is the body of a function a human wrote; a FUNCTION point is the function itself, signature declared and body to come, and
the function may not exist. So the tag is carried by its own comment, as a rule's is, and the point's id (AT) is that comment's: it does not move when
the function appears. `name` is the function's name, exact (D24), an identifier, and not a Ring builtin or `Main`, which Ring calls after the top level
(F-60); `params` its parameter names, in order, none repeated; a function that exists must take exactly these (the signature is the human's), and a class
or a function of another case in its way is a fault. `calls`, `writes`, `risk`, `floor` and `governed_by` are a BLOCK point's. A tag inside another
definition or written as a trailing comment is a fault: the point stands alone, at the top level, in the statements before the first function.

**The value** is `absent` while no top-level function has the name, and the digest of the body's canonical text once one does. FROM is that; TO is the
body on one line, judged exactly as a BLOCK body is -- structural, constraint, governance, trust, derivation. **TO `absent` is refused**: a refinement
does not delete a function, and a revert of its creation, which restores `absent` and deletes the function with its ids, is the way back.

**The lowering.** A function that is there: BLOCK's. A function that is not: ONE `node.create` of the whole function, parameters and body, fresh ids.
**Where it goes is the finding** (HF-98): after the last function and before the first class. Ring ends a function at the next function or class and at
nothing else, so a function written beside its tag, among the top-level statements, would swallow every statement after it; and after a class it would
be that class's method (F-21). The oracle pins it: FN03 prints `start` before and after, FN04 puts the function before a class and still prints 3.

**The court.** 20 fixtures, 7 of them on the oracle and rnxc with those of the BLOCK kind; the body's locality counts a function that appears or goes as
the one thing allowed to; the write surface gives a FUNCTION point the BLOCK shape (FROM exact, TO one line); and two controls added to the five:
a new function written beside its tag is caught by 7 fixtures, a lift that checks no FUNCTION tag by 8.

**Not built, named:** a FUNCTION point refined as a rule (`Round.params`, which would change a signature a human declared: a tier-4 act, if ever);
~~a method (a function in a class)~~ (built 2026-10-20, section 14); a function whose body is proposed with a comment; the kinds `type` and `custom`.

## 13. The allowlist rules -- a point's calls and writes, refined (built 2026-10-20)

**On the author's "ok proceed as you suggested"** (2026-10-20, after "should we close the not built points before the Python face?"). The fixtures came first,
`fixtures_allowlist.txt`, 8 of them (AL01-AL07, L27), committed before the engine read them; its header is the design.

**Why.** Until now the only way to let a body call something its point did not name was a human editing the tag as text, outside the gate. An allowlist is the
point's RULE for its body (charter 6.4: "the rules themselves are refinable"), so it goes through the same five stages as every rule: TARGET `gross.calls` (or
`.writes`), KIND `block` or `function`, FROM the list now (`|` apart, `""` when absent), TO the list wanted.

| stage | for an allowlist |
|---|---|
| structural | the attribute belongs to a BLOCK, FUNCTION or METHOD point; TO is a list of distinct names, none empty (`""` clears it); every name is one the program has -- a call a function, class or builtin, a write a global, an attribute or a parameter of the function -- spelt as declared (D24), and a FUNCTION or METHOD point's own name is a call it may make; FROM is what is there; TO is not FROM |
| constraint | nothing of its own: an allowlist has no bounds or options, and its names are judged at structural |
| governance | WIDENING is a tier-4 act whatever the point's risk (a name in TO that FROM did not have); NARROWING is the point's own tier |
| trust | the origin must be `:trusted` whatever the point's floor says: a rule is not changed by a model-composed proposal |
| derivation | the body that is THERE must still satisfy the new list: narrowing below what it calls or writes leaves it outside its own rule, refused as `own rule`, as a bound below the value is |

**The lowering** is one `node.update_property` of the tag's comment text, so no id moves. A text edit of an allowlist is read back by the audit as the
refinement it amounts to (AL07: `as llm by boss`, then `refine gross.calls Tax Tax|Round => rejected trust rule`).

**A body outside its own rule is a state, not a fault.** A human may write more than the point names; the lift reports `point 'gross' body is outside its own rule`
(L27) and does not stop a refinement of any other point. The allowlist can be widened to repair it, which is the loop AL05 closes: a FUNCTION point's body is
refused for a call the list lacks, the list is widened by a trusted tier-4 actor, and the same body is then admitted.

**The write surface** gives `.calls` and `.writes` targets a shape of their own in the scoped grammar (`qnames`: names joined by `|`, or empty), so an agent that
may write a body may also be shown, in advance, that it may not write a rule.

**The court.** 8 fixtures; three controls: an allowlist widening counted as an ordinary change (caught by 1), a TO list that is never checked (2), a body never
judged against its own point's rule (4, the last shared with the BODY kinds). Guard stage 24 PASS.

**Not built, named:** a rule-like refinement of a METHOD or FUNCTION point's `params` (a tier-4 act, if ever: it changes a signature a human declared); the
`calls` of a name that exists only in a loaded file the engine does not read (section 14, "A program, not a library").

## 14. The METHOD kind -- a method of a class that may not be there yet (built 2026-10-20)

**On the same word.** Softanza is 34,672 methods against 9,764 functions (`rnxc graph`), so without this kind FUNCTION reaches a fifth of the estate. A method is
not a function in a class: it has `This`, the class's attributes, dispatch by receiver and inheritance, and a few names Ring calls by itself. The fixtures came
first, `fixtures_method.txt`, 13 of them (MT01-MT08, L28-L32).

**The point stands INSIDE the class.** `# <R:METHOD name="Grow" params="n" calls="Size" writes="@nCount">` among the class's members, with a member below it. The
class is the one the tag stands in. `name` exact and an identifier, `params` the signature (no `self`; `This` is implicit), `calls`, `writes`, `risk`, `floor`,
`governed_by` as a FUNCTION's; the value is `absent` or the body's digest; TO is the body on one line; TO `absent` is refused and a revert of a creation deletes
the method with its ids. **Where a tag may stand is a finding (HF-100)**: before the first method, between two, among the attributes and after `private` all keep
it in the class, but a tag after the LAST member ends the class and lands at the top level, where the printer moves it, so that is a fault, by name. A tag
outside a class, inside a function or inside another definition is a fault too.

**The lowering.** A method that is there: BLOCK's. One that is not: ONE `node.create` of the whole method into the class's members, after the last of them and
**before the `private` marker** if there is one -- `private` is a flat marker in the graph, so a method placed after it would be private without anyone saying so
(MT04, caught by the control that puts it there).

**Names a method may not take**, as faults of the declaration, because Ring calls them itself and creating one changes what other code does without anyone naming it:

- `operator` (F-69: one method for every operator) and the brace hooks `BraceStart`, `BraceEnd`, `BraceError`, `BraceExprEval`, `BraceNewLine`;
- `get<x>` and `set<x>` where the class assigns an attribute `<x>` (F-73: `o.x` calls the getter, `o.x = v` the setter);
- a builtin or a top-level function: inside the class's methods a bare call goes to the class's own method first, so the new one would SHADOW it;
- **a keyword Ring will not take as a name** (HF-101), for a method, a function and a parameter alike: 47 of Ring's 75 keywords, read from the vendored scanner and parser
  rather than listed here. `Get`, `Put`, `Give`, `See`, `Next` and `If` are refused; `To`, `In`, `From`, `Step`, `This`, `Main`, `Init` and the like are names.

A human who wants one of these writes it; a BLOCK point still refines the body of one that exists (MT08, which also counts `This.x` as an attribute write).

**A program, not a library (HF-103).** The derivation asks `rnxc check`, whose absence rules are shut on a file with no top level and no Main (`nothing in this unit
runs`), and the gate fails closed (HF-96). So a class alone is refused at derivation: every program in the fixtures begins with a top-level statement. That is
exact, not cautious -- and it means the body kinds refine **a program, and not Softanza's library files**, which are almost all classes. Reaching the estate
needs a derivation that asks the checker about the unit through the program that loads the file; the engine does not read that yet. **Built 2026-11-01** (section 16).

**The court.** 13 fixtures, MT03 on the oracle and rnxc before and after (`3` and `3`: the method is added and the program prints the same), the programs of MT04-MT08 each carrying a `? "start"` for the reason above. The
body's locality counts a method that appears or goes as the one thing allowed to, outside the class's own members nothing moves. Two controls added to the
body kinds': a new method written after the class's `private` marker is caught by 1 fixture (MT04), a name Ring refuses accepted as a name by 1 (L32); the
lift that checks no FUNCTION or METHOD tag is now caught by 13. Guard stage 24 PASS: 147 fixtures, 21 controls, 471 s.

**Not built, named:** a method whose body is proposed with a comment; a refinement of a METHOD point's `params` (the signature is the human's); the kinds `type` and `custom`. (A refinement of a library through its loading program: section 16.)

## 15. `reads` -- what a body may read of the world outside its frame (built 2026-10-22)

**On the author's "go ahead with the reads attribute"**, after HF-118: the bypass court pinned five limits of the body gate, and three of them -- a read of a global the point does not name, an operator on a
global object, a getter reached through one -- were one gap: a point named what a body may call and write and never what it may READ. `reads` closes it, as `calls` and `writes` close theirs: **closed by default**.

**The attribute.** `# <R:BLOCK name="peek" calls="Safe" reads="$nVat|@nCount">` on a BLOCK, FUNCTION or METHOD point: the globals (`$x`) and attributes (`@x`) a body may read, spelt as declared (D24). Absent, a body reads its
parameters and its own locals and nothing else. **What a body may write it may read** (`$nCount += 1` reads `$nCount`); a plain write (`$nCount = 0`) reads nothing. A parameter is not a name for `reads`: it is the function's own.

| stage | for a body |
|---|---|
| constraint | every `$x`, `@x` and `This.x` the body reads is one `reads` or `writes` names -- in an expression, an index, an argument, the root of a member chain, a `for` bound; not where it is only written (the target of a plain `=`, a loop variable, a `give` target, a `catch` binding); `This.M()` is a call, not a read |
| structural (the allowlist) | `reads` is refined as `calls` and `writes` are: TARGET `gross.reads`; every name a global or an attribute (a parameter is refused: `is no global and no attribute`); widening a tier-4 act, narrowing the point's own tier, below what the body reads refused as `own rule` |

**The write surface.** The body grammars (`agent/body_gbnf.py`) give a `$x` or `@x` a production only for the names the point reads or writes -- one rule more (`gref`) and no more than 94 by the decoder's count; the scoped sentence grammar gets a `.reads`
shape beside `.calls` and `.writes`. The task lint (`agent/task_lint.py`) refuses a request that names a global the point may not read (`names-read`), and the runner's prompt says `may read: ...` for a task that declares it (and nothing for one that does not: their prompts are what they were).

**What it closes** (bypass court, three subjects, 60 cases): a read of a secret global, an operator or a for-in on a global object (`$oBox + 1`), a read of a global list copied into a local (`aL = $aBox`), a global read inside the index of one the point may read. **What a grant includes**, pinned as a named limit by
the same court: a point that MAY read an object may use it as a value, so `x = $oBox + 1` runs the object's `operator`; its getters and setters stay the calls' business (`getsecret` is refused unless the point names it). **What is still open**: an operator on an object a CALLER passes
as a parameter (the point has no say in what its caller hands it), an allowed callee's effects, output, termination.

**The court.** Fixtures composed before the rule: B12 (a body reads the globals its point names, and what it may write, and no other), AL09 (the allowlist rule for `reads`), MT09 (a method and its attributes): all three passed as composed; the existing 56 pass unchanged but one,
where my first reads collector took the call `This.Size()` for a read of an attribute `@Size` (MT06) -- fixed, and a body-held-to-no-reads control added (it fails the three fixtures that carry `reads`; I wrote "at least 4" before measuring). Guard stage 24 PASS, stage 28 PASS.

**Cost.** The gate: one more walk of the body's nodes at the constraint stage, which is milliseconds beside `rnxc check`. The compatibility: a body point that reads a global it does not name, written before this, is now outside its own rule -- the lift says so and the allowlist can be widened (as `calls` and `writes` always could).

## 16. The library derivation -- a body point in a file that runs nothing, refined through the program that loads it (built 2026-11-01)

**On the author's "go ahead with the library derivation of rung 5"**, after HF-103: `rnxc check` says "nothing in this unit runs" of a file of classes and "the unit calls loadlib() or eval()" of Softanza's
whole unit, and the derivation failed closed on both -- so no body of the estate could be refined. Those answers are right for Ring's question (is this an error the moment the line runs?). **The gate asks its own,
closed (D32): does the unit DEFINE every name the body uses?**

**`rnxc check --closed`** (ringpp, `src/universe.zig`, `src/types.zig`, `src/rnxc.zig`). A unit in which nothing runs is asked about all the same; eval, loadlib and an admission do not shut the absence rules -- a
name only one of them could make is absent; a call's arity resolves through the whole unit (one definition per name, C22; a name two files define says nothing); a file that could not be read or parsed is still a
hole. The findings say what was proved -- `... -- checked closed` in place of `Error (R3) the moment this line runs` -- and keep Ring's first clause, so a fixture's expected words still match. `--natives=<file>`
names what native libraries register (the engine's own list, from `cfunctions()`); `--subst=<file>=<text>` checks the unit with one file's text replaced, the file on disk untouched. A plain `rnxc check` is
unchanged. ringpp's gate step `check --closed (D32)` (`bench/check_closed.py`): 12 cases, the build before fails 5.

**The engine.** `Model(text, ctx, unit)`, `unit = {'root', 'file', 'natives'}`; the CLI's `--unit root.ring [--natives names.txt]`. Every body derivation is closed; with a unit it checks the ROOT's unit with the file's
text replaced by the refined one, and the lift reads the unit's names (`rnxc graph` of the root, spelt as each file declares them, and the natives) -- a library's point may call what its loading program defines.
A native is spelt as the engine registers it, lower case (D24).

**The court.** `fixtures_library.txt`, 11 fixtures composed before the engine read them, with two sections of their own (`--- root`, `--- natives`): a class alone refined (LB01, refused before D32); a call into the
loading program admitted through it (LB02) and refused alone (LB03); an allowlist naming nothing the unit defines (LB04); eval and loadlib in the loading program no longer stopping a body (LB05); a native refused
untold (LB06) and admitted when the engine's list names it (LB07); a global the loading program assigns (LB08) and the same read alone (LB09); a load the unit cannot read (LB10, fails closed); an arity against the
loading program's function, found only once the closed check resolved signatures through the unit (LB11). **Three were composed as derivation refusals and the lift answered first** (LB03, LB04, LB06): an
allowlist naming what the unit does not define does not lift -- the same fault one stage earlier, and the fixtures say so. B09 and FN10 said "an eval anywhere stops a body"; D32 inverts them. The body kinds' fixtures:
70 of 70, 131 steps. Five plants, each caught: no unit in the derivation (6 fixtures), an open check (7), a lift blind to the unit (5), no natives (1), no `--subst` (1).

**On Softanza itself** (`probes/library_softanza.py`, the installed Softanza main, read and never written): a METHOD point in the model of `base/common/stzCancelToken.ring`. One argument short to `StzRetryBudget`,
which another file defines: refused at derivation, R19 in the compiler's words. The right call: admitted. An engine native: admitted through the engine's list (3,670 names). The native spelt as Softanza spells
it, `StzEngineCancelSignal`: refused by name -- the engine registers `stzenginecancelsignal`. The same refinement with the file alone: refused at the lift. The file on disk: unchanged. About 14 s a derivation,
the first of a model about 44 s (it also reads the unit's names).

**Cost.** A derivation checks the whole unit: milliseconds for a fixture, ~14 s at Softanza's size. A body that calls a native needs the engine's list. A program holding an eval no longer stops a body refinement,
so a name only an opaque eval assigns is refused by name instead. A closed check's findings are claims about definitions, not Ring's run-time proof, and they say so.

**Not built, named:** a plain `rnxc check`'s cross-file arity (still unwired; only the closed check resolves through the unit); a writer for a non-canonical file, so a refinement of Softanza is a model and a diff,
not yet a file (`--write` still refuses a file that is not its own canonical text, section 9); the kinds `type` and `custom`.
