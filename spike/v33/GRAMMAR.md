# Haro v0.33 -- what a family of kinds shares, said once: INCLUDES, ON a FORM, EXCEPT and a quantifier over a FORM (Central's item 4, stzzui's S5), and S14 answered

**Written after `fixtures.json`, `court_cases.json`, the world `medium_v33.haro` and its hand-expanded twin beside it, which are the judges** (the W discipline:
fixtures first, prose second; the fixtures, the two worlds and the sentences are ec856e3, and the extension for `EXCEPT` is 686c6f5, both before any code read an
`INCLUDES`; the fixtures added after the code say so in their names). v0.33 is the second half of what was owed on Central's batch of 2026-11-03 12:33, taken on the
author's word ("Items 4 and S14"): **item 4**, a seat shared by ten kinds, which StzZui met as its seam S5 -- `SATISFIES`, `ALWAYS_REACHABLE`, `SIGNALS` and `ACTOR` written
on all ten kinds, and a constraint written ten times for the ten kinds that share it -- and **S14**, a guarantee read in two lists. It is the thirty-third rung (charter D47).

## S14, first: already expressible

*Is reading a second list in one constraint form expressible, or is it the same seat as item 4?* **Both, and the first needs nothing new.** A `where` takes `and` and `or`, so one
quantifier reads two lists of a kind: `some vibe where satisfies contains zoom or always_reachable contains zoom`. It was proved before it was fixed, on a scratch language: the
constraint fires only when neither list holds the verb. StzZui's generator emits one `VERB_NOT_CARRIED` constraint for each of 77 absent cells, each a ten-way disjunction
`(some intent_flow where satisfies contains zoom) or (some form where ...) ...`; to read `ALWAYS_REACHABLE` too it adds `or always_reachable contains zoom` inside each of the
ten `where`s. That is the part that is item 4: the ten-way repetition, which a quantifier over a FORM says once. Judged by M7 and M8 (the first list, the second list), M9 (the envelope).

## What is new, and where it comes from

| form | declares | the lesson it carries |
|---|---|---|
| `INCLUDES [form, ...]` on a `DECLARATION` | the kind takes the seats of the named FORMs, **first**, in order, then its own `SEATS` | a FORM is a named bundle of seats; a kind may include it. A seat may come once (refused otherwise, naming both sources); `SEATS` stays required, so a kind that adds nothing writes `SEATS []`: one exact spelling |
| `ON form` on a `CONSTRAINT` | the constraint is made once for each kind that includes the FORM, in declaration order, named `<constraint>_<kind>` | StzZui already named its ten copies `select_act_collapse_intent_flow` and so on. The generated name may not be a declared one (one namespace) |
| `EXCEPT [kind, ...]` on a constraint ON a FORM | the kinds it is not made for | **found by running the rewrite on StzZui's real declaration**: two of its five repeated stems are identical for nine kinds and differ for `interaction` alone, which has the extra seat `role`. That kind keeps an explicit constraint of its own. Each name must be a kind that includes the FORM, named once, and not all of them |
| `some`, `all`, `earlier`, `exists` over a FORM, in a `CONSTRAINT`'s `WHEN` and `THEN` and a `VIEW`'s `WHERE` | the `or` (`and` for `all`) of the quantifier over each kind that includes the FORM | **an existing reading never changes**: a name that is already a seat of the constraint's kind keeps its meaning (A7). A FORM no kind includes is no quantifier head, and `ON` it keeps the refusal it had (R6, R7, R9) |

**All of it is sugar with a definition, and the court never sees it.** The meta-court resolves it between reading the file and the first pass that reads a kind's seats
(`form_expand.haro`, loaded by the meta-court only). The court, the forge and `cond_lib.haro` are untouched, so no court's cold compile moves and every committed court is
byte-identical. The definition is a test: `medium_v33.haro`, written with the forms, and `v33/medium_expanded.haro`, the same language with every kind's seats and every constraint
written out by hand, **forge a court and a grammar that are byte for byte the same, on `haro` and on its checked build** (stage 38).

The expansion of a condition is made on its parse and printed back by `CondPrint` in the canonical text: tokens joined by single spaces, a quantifier always in parentheses, an
`or` under an `and` (or either under a `not`) in parentheses, a value bare where a bare word is a value and quoted where it would be a place. **A condition with nothing to expand is
never parsed or printed: it is stored as written** (a plant pins that). The printer is the one risk, since it writes a condition the author wrote, so it is proved on every condition the
repository holds (`v33/cond_court.py`, below).

## Grammar (EBNF), the v0.32 text with these additions

```
DECLARATION: VERB string, INCLUDES name_list, SEATS seat_list, ...     -- INCLUDES names FORMs; VERB and SEATS required
CONSTRAINT:  ON IDENT, EXCEPT name_list, WHEN string, THEN string, MESSAGE string, CODE string, CITES cites, SEVERITY IDENT
on          = declaration | form_included_by_some_declaration ;       -- EXCEPT only with the second
quantifier  = ("some" | "all" | "earlier" | "exists") head ...         -- head: a kind, a list of references, or a FORM that some kind includes
```

## The world judged: medium

`medium_v33.haro` declares three kinds (`screen`, `vibe`, `panel`) that include `guarantees` (`satisfies`, `always_reachable`, `actor`), and five constraints that make seven:
`confirm_needs_cancel` ON the FORM (made three times), `satisfies_something` ON the FORM EXCEPT `panel` (made twice, a warning), `verb_not_carried` (S14: one `where`, two lists, a
quantifier over the FORM) and `every_actor_named` (`all` over the FORM, a warning). The fifteen sentences are in `medium/`; the 18 cases are judged by `haro_forge.py --stage=38`:

| case | what | holds |
|---|---|---|
| M1, M2 | the clean sentence; the meta-court reads the world: three declarations, one form, seven constraints | ok |
| M3, M4, M5, M6 | a constraint ON the FORM enforced on a `screen`, a `vibe` and a `panel`; its envelope carries the code and cite as if written by hand | ok |
| M7, M8, M9 | S14: a verb guaranteed in `SATISFIES` of one kind, or in `ALWAYS_REACHABLE` of another, refuses a `vibe` on print; the envelope | ok |
| M10, M11 | on print and the verb guaranteed nowhere, or guaranteed and the surface visual: lawful | ok |
| M12 | `all` over the FORM: one kind names no actor, the sentence stands and the `vibe` warns at its own line | ok |
| M13, M14, M15 | a seat got from the FORM is checked by its own MENU; a seat a kind adds beside the included ones is lawful; the expanded kinds are closed | ok |
| M16, M17, M18 | `EXCEPT [panel]`: a `screen` and a `vibe` that satisfy nothing warn, a `panel` is lawful and silent | ok |

## The real test: StzZui's own declaration

`haro/zui.stzu` of StzZui, read at `stzzui` origin/main 870c45c (a read-only copy; nothing in that repository is touched), was rewritten **mechanically** with the new forms
(`runtime/zui/rewrite.py`, an experiment of this desk and not part of the guard) and forged beside the original:

| | the original | with the forms |
|---|---|---|
| lines | 1,169 | 883 |
| constraints written | 136 | 93 (30 become 3 ON the FORM, 18 become 2 ON the FORM EXCEPT `interaction`) |
| medium constraints (the 77 `VERB_NOT_CARRIED`) | each a ten-way disjunction | each one `some guarantees where ...` |
| the court forged | 83,536 bytes | the same 136 constraint rows (in another order for the two `EXCEPT` stems) and one new row, the FORM `guarantees` |
| the grammar forged | -- | byte-identical |

It was run on the read-only copy under the current code. StzZui's own judge (`judge-zui-court.js`, its 57 fixtures) was **not** run against the rewritten court: it needs StzZui's tooling.

## The court: the numbers

| what | judged | holds |
|---|---|---|
| the meta fixtures | `v33/fixtures.json`: 12 accepts by their counts, 19 rejects by the fragment of why, on `haro` and on its checked build | 31 of 31, stage 1 |
| the court cases | `v33/court_cases.json` over `medium/`, the court forged from `medium_v33.haro` on both runtimes, the two printing the same bytes | 18 of 18, stage 38 |
| **the definition** | `medium_v33.haro` (with the forms) against `v33/medium_expanded.haro` (written out by hand): the court and the grammar forged | byte-identical, on `haro` and on its checked build |
| the printer | `v33/cond_court.py`: every condition the repository holds (160) and 57 written by hand, parse to print to parse | 213 of 217 (the 4 are written to be refused), the same bytes on both builds |
| the committed courts | every pattern-less and form-less language re-forged | byte-identical to HEAD: the court, the forge and `cond_lib.haro` are unchanged |
| the protections | `v33/plants.py`: 34, each switched off in turn in a copy of `haro_lib.haro` or `form_expand.haro`, judged by the meta fixtures, the cases, the twin and the printer | 34 of 34 load-bearing, the fixtures each fails printed beside it; `--plant` fails the stage |
| the cold compile | stage 6, the machine court, minima of 15 | 145.6 ms and 16.2 ms for the edit: no court changed, and the library every court loads did not grow |
| the meta-court's cold start | `haro.haro machine_v03.haro`, alternating A/B, minima of 25 | 125.2 ms before, 131.3 after (+6.1 ms): it loads `form_expand.haro` |

## What building found (HF-138)

1. **S14 was already expressible, and was proved before it was fixed.** A `where` takes `or`, so one quantifier reads two lists of a kind; on a scratch language the constraint fires only when neither list holds the verb. What is item 4 in S14 is the ten-way repetition, which a quantifier over a FORM says once.
2. **The forms are sugar with a definition, and that is why they cost no court anything.** A court cannot probe for an optional feature: reading a global nobody assigned is an error (R24), so a feature the court had to know about would have changed every generated court's prologue and regenerated the ten committed ones. Resolved in the meta-court, the court, the forge and `cond_lib.haro` are untouched, and the proof is a test: the court forged from the language written with the forms is byte-identical to the one forged from its hand-expanded twin, on `haro` and on its checked build.
3. **Running the rewrite on StzZui's real declaration found `EXCEPT`.** Of its five repeated constraint stems, three are identical for all ten kinds and merge; two are identical for nine kinds and differ for `interaction` alone, which has the extra seat `role`. Without a way to say "every kind but this one" those 18 stay written out. The data decided the form, not a guess at what a file might need.
4. **The printer is the one risk, because it writes back a condition the author wrote.** A condition with nothing to expand is never parsed or printed (a plant pins it through the twin's bytes); the printer is proved on every condition the repository holds, 217 with 57 written by hand for each node kind and each precedence, and on StzZui's 92. It round-trips parse to print to parse to the same tree and the same text.
5. **The plants found three missing fixtures and one dead guard.** A11 (a quantifier inside a `where`), A12 (a `VIEW`'s `WHERE`), R19 (an unreadable condition in a language that has forms) were added after the code. The guard that only a name resolving to a FORM counts could not be observed in any mode: the collecting meta-court stops before it judges relations once a declaration is unresolved, so a bad `INCLUDES` is always a finding and the language is refused anyway. It was deleted, not pinned.
6. **The family's list of extensions drifted a second time** (`.medium`, 15 files; `.grant` was the first). It is now one copy, in `v30/block_court.py`, imported by the pattern court, and a check fails when a language declares an extension that files carry and the family neither counts nor ignores with a stated reason (`.rfn` is ignored: refinement requests are another text). The check is made to fail first, in the court itself.
7. **An existing reading never changes**, and five fixtures hold before and after (A8, R6, R7, R9, and A7 for the seat that wins over a FORM's name).
8. **My rewrite script was wrong three times and the language never was**: a regex that swallowed trailing blank lines made identical bodies look different, a heredoc ate a backslash, and the first line count was inflated by blank lines. The result about StzZui's file is measured only from the third run.
9. **The meta-court pays for the sugar.** `form_expand.haro` is 331 lines and its cold start on `machine_v03.haro` rose 6.1 ms (alternating A/B, minima of 25), on top of the 15.1 ms the pattern engine cost it in v0.32. Nothing gates the meta-court's time; the remedy, if it ever matters, is to load each half only where a language uses it.

## What v0.33 does not do, named

- **The remaining repetition in StzZui's file is its own specialisation**, not the language's: `decorative_animation` differs between `feedback` and `vibe`, and `missing_cancel` has two kinds; they stay explicit.
- **A kind that includes a FORM that includes a FORM**: a FORM has no `INCLUDES`; nesting is not built (R11).
- **The seats' order is the FORM's first, then the kind's own**; a kind that wants its own seat first cannot say so. StzZui's file has them in that order, which is why its court is identical.
- **StzZui's fixtures against the rewritten court** (above), and **StzZui's own rewrite**: both are StzZui's, with its generator.
- **A `VIEW ON` a FORM**: a view applies to one kind; only its `WHERE` ranges over a FORM.
