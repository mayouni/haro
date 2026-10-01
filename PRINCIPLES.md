# Haro -- the principles, in full

**Status: v0.2 DRAFT, 2026-10-01, with `haro/CHARTER.md`.** The charter gives each
principle its verdict; this file gives each its full text: the lesson, its source, the
rule, what the rule costs, and how a guard would check it. Grades as in the charter:
[M] measured, [R] recorded, [D] designed.

**v0.2 note.** Principles 1-7 below are written for the computing altitude (v0.1's Haro) and
stand there unchanged; the charter's section 11 says what each means at the declaring and
declared altitudes. Principle 8 is amended a second time, and principles 9, 10 and 11 are
added, at the end of this file, on the author's ruling of 2026-10-01 that Haro is the
language of languages and embraces refinement.

The principles are numbered as the launch prompt numbered them (1-8), preceded by the ten
Haro inherits from the Ring++ design charter (P1-P10, `softanza/memos/2026-08-30-ringpp-
design-charter.md` section 3), which are not restated here beyond the charter's table.

---

## 1. No silent global

**Verdict: KEPT, made structural.**

**The lesson, with its bill.**
- `nL = len(cPixels)` in a caller replaced the `NL` newline constant with a NUMBER for the
  whole process; library code building a string with `NL` raised deep inside the string
  layer with nothing pointing back at the caller's variable. `TAB` and `CR` are equally
  exposed. Swept library-wide in 2026-08: 2,898 reads across 75 files. [R, stzlib/
  CLAUDE.md "What NOT to do"]
- `TRUE`, `FALSE`, `NULL` are globals; `true = 0` replaces them for the process, and with
  `TRUE` clobbered `(1=1) = TRUE` answers 0: the logic runs backwards and nothing errors.
  4,460 reads remain. [R, same]
- The library clobbered `NL` itself: `nL = len(_aRes_)` in `stzWordStream.
  MostFrequentWords`, and three `cR = ...` locals -- found by the `writes-a-mutable-
  constant` rule's first run. [R, same]
- Ring has no strict anything: no strict mode, no immutable core, no fail-fast; truth
  itself is a variable. [R, analysis 2.1; 3.1 "one type, absent, is carrying an entire
  family of production hazards"]
- A bare assignment inside a function to a name that exists above it writes that name
  (analysis 2.7); Ring++ accepted the divergence and pinned the base unit's exposure at 0
  (C-2, `bench/shadows_bare.max`). [R]

**The rule [D].**
1. No predefined variable exists. `true`, `false` and `nil` are literals of two types.
   Newline, tab and return are the escapes `"\n"`, `"\t"`, `"\r"` (F-55 closed).
2. A name is one of three things by its spelling and nothing else: `$name` a global
   declared at the top level, `@name` an attribute of the enclosing class, a bare name a
   local of the enclosing definition. A bare name never resolves upward -- not in a
   function, a method, or a lambda (C-14's top-level-lambda exception is not carried;
   captures of an enclosing local are explicit, `use n`).
3. A read of a name nothing declared is a compile-time refusal. The four absence rules of
   `rnxc check` (undefined-function, uninitialized-variable, unknown-class,
   unknown-package) are refusals with no hole to silence them, because the language has
   no `eval` and no `loadlib` (P4, sharpened).
4. Shadowing is refused: a local may not take the name of a `$global` or `@attribute`
   visible at its site; a nested definition may not take the name of an enclosing one.
   The refusal names both sites.
5. A `const` at the top level is a global that may not be assigned after its declaration;
   the refusal is `CONST_ASSIGN`.

**What it costs.** The Rule A migration surface in Mansour's tree: 160 sites classified
2026-09-09 (90 class attributes without `@`, 51 eval-assigned locals now moot under
principle 3, 6 `sysargv`, 8 typos and a capture) [M, ringpp/CLAUDE.md]. Nothing at run
time: a compile-time resolution is what `rnx` already does.

**The guard.** `rnxc shadows` and `bench/shadows_bare.py` already count the exposure on
Ring++; on Haro the count is zero by construction and the guard is the refusal fixtures:
one per rule above, each made to fail on a build that lacks the rule.

---

## 2. One obvious spelling

**Verdict: KEPT, with the case rule decided (H-2).**

**The lesson, with its bill.**
- `N` and `n` are the same variable (F-18); one C22 "Function redefinition" anywhere in a
  file makes every method call fail with R14 across every test that loads it, and the
  error count balloons from about 200 to about 770 from one stray duplicate [R, stzlib
  "Editing discipline" 1]; 887 of the classic suites' errors are C22 case collisions
  [R, compass page lane 03].
- `def Load()` is a C6 error (`load`); a variable `cAll` is a C13 error because it
  contains `call`; `oK` and `oR` are keywords [R, stzlib "What NOT to do"].
- Ring accepts several spellings of most constructs: `ok/next/off/done` against `end`
  (32,180 vs 859 in Softanza), `def` against `func` (36,543 vs 7,872), `&& || !` against
  `and or not`, `but` against `elseif` (2,898 vs 12), three comment forms, `see` against
  `?` (26 vs 2,754) [M, Ring++ charter 4c]. The author: "I don't think there is any added
  value from the multiplicity of styles ... other than complexifying the compiler work
  and the programmer mental model" [R, 2026-08-31].
- The colon does three jobs at once -- atom, pair constructor, implicit lowercase -- and
  the lowercasing "buys nothing, measured" [R, charter 4d]; 27,807 symbol sites keep
  working if comparison stays case-insensitive and only the stored text improves.
- DHH: "convention over configuration leads directly to things like token efficiency"
  [R, compass page]. A choice between equivalent spellings is a token spent for nothing,
  on every line, forever.

**The rule [D].**
1. Identifiers are case-sensitive. Two names in one namespace that differ only by case
   are refused (`CASE_COLLISION`), naming both sites. Softanza's mixed-case names are
   unchanged.
2. Keywords are a closed set, reserved in every casing; a keyword cannot be an
   identifier, and an identifier that *contains* a keyword is an identifier (the C13
   trap is a tokenizer defect, not a rule).
3. One spelling per construct, Rule C adopted whole. The table is in
   `GRAMMAR-SKETCH.md`; the author ratifies the choices.
4. A symbol keeps its text (Rule D1); symbol comparison is case-insensitive; a symbol
   is its own type.
5. A second definition of a name is refused, naming the first.
6. The Misspelled Form is refused: a name that resolves to nothing is `UNKNOWN_NAME`
   with a `did you mean` suggestion in `todo`, computed the way `StzSuggestWord` does
   [R, stzNatural.ring 1211-1223].

**What it costs.** For Softanza, the Rule C sweep sizes above (mechanical, and Ring
already accepts every surviving spelling, so the swept code still runs on the oracle).
For the agent, nothing: the grammar offers one spelling, so the decoder cannot emit
another.

**The guard.** Reject fixtures for each spelling that is gone; an accept fixture that
is the whole Rule C table; the case-collision fixture drawn from the real `NthStz` /
`NthSTZ` pair.

---

## 3. Grammar the decoder can hold

**Verdict: KEPT, with its limit stated and one grain added (H-8).**

**The lesson, with its bill.**
- C9: a declared grammar makes a violating token unemittable; 10 of 10 valid on first
  attempt against 2 of 10 unconstrained [M, SOFTANZA_STRUCTURED_OUTPUT.md 88-97].
- The kernel promises GBNF for every declared grammar; today only C9's schemas emit one
  [R, compass page lane 09]. `.pia` emits none; W's grammar is a comment in `expr.zig`;
  the `-ex` classes have none [R, FINDINGS HF-8].
- The engine takes any GBNF text: `StzGenerateXT(prompt, [:Grammar = g])`; three
  functions judge a grammar with no model loaded (`StzGrammarRefusal`,
  `StzGrammarAccepts`, `StzGrammarCouldContinue`) [R, stzNeuralModel.ring 195-216].
- The amendment travels with every claim: "structure kills malformedness, not falsehood"
  [R, C9 line 40, clause 8].

**The rule [D].**
1. The grammar is one source file; parser, GBNF and editor grammar are generated from it
   and never edited by hand.
2. The GBNF is emitted at three grains: the file, the hole (statement, expression,
   definition), and the scoped hole (the hole with the reachable names inlined as
   terminals, each function with its parameter shape). Grain 3 makes an undefined name, a
   wrong arity and an unknown named parameter unemittable.
3. Declared languages embedded in Haro (W, the `-ex` patterns) splice their own GBNF into
   Haro's at the literal's position.
4. What the grammar cannot hold is said beside every claim: types, values, truth.

**What it costs.** The generator, once. Grain 3's cost is the pushdown machine's cost per
alternative times the reachable names; a Softanza unit has about 45,000 function names,
so the grain lists reachable names and its cost is measured at the spike before it is
promised. Non-ASCII in a character class is unsupported by the machine [R,
gbnf_machine.zig 40-47]: identifiers are ASCII; strings go through byte ranges.

**The guard.** Section 4 of the charter: accept and reject fixtures under parser and
machine; sampled derivations all parse; one grammar version across the three artefacts.

---

## 4. Refuse, then explain

**Verdict: KEPT; the shape is C2 plus `why`, `todo`, `frames` (H-5).**

**The lesson, with its bill.**
- `StzRaise([:Where, :What, :Why, :Todo])` exists and is used 5 times in 3,956 calls [R,
  compass page]; 118 REFUSED-style sites in 36 files [R, same].
- Ring's error is a string with the code inside the message; `raise()` cannot carry
  structure; `cCatchError` is process-wide (analysis 2.17; F-68; C-15) [R].
- Where it happened was wrong by design until measured: a multi-line call reports the
  callee's line, a `raise` its closing paren (C-8, 2026-09-22) [R].
- The family's refusal envelope is C2 v1.2.0, six fields, extensions permitted, no bare
  boolean [R, stzzui/doc/diagnostic-contract.md; schema `additionalProperties`].
- Ringua: "errors answer in [the domain's vocabulary] too. A host stack trace reaching
  the domain expert is a defect." [R, ringua/README.md 31]; stzu declares refusal
  phrasing as data beside the grammar (`DEFINE REFUSAL ... MESSAGE`) [R].
- LAW 3: "every ambiguity refuses rather than guesses" [R].

**The rule [D].**
1. An error is a value of type `error`, and its machine form is the C2 envelope with
   `why`, `todo` and `frames` as extension fields. `todo.edit` is an applicable patch
   when the fix is mechanical; `todo.say` is the sentence otherwise.
2. Every refusal code is Haro's own, stable, never reused, and declared beside the
   grammar with its message, the way stzu declares `REFUSAL`; the court keeps its own
   law (C2's rule).
3. Ambiguity refuses: a text with two parses is unparseable; a call with two readings
   (F-59's `:name = value`) is two syntaxes; an `if` whose condition is not a boolean is
   refused.
4. A caught error is a value in the handler's own variable; there is no process-wide
   last-error.
5. Severity has C2's two rungs; a wrong program is never a warning.

**What it costs.** The `why` and `todo` texts are written once per code, beside the
grammar; the cost is authorship. `todo.edit` needs the span machinery `rnxc check`
already has (tree-sitter spans).

**The guard.** Every refusal fixture pins the record against the C2 schema and the human
line against a text; the schema validation is the same one StzZui's court runs.

---

## 5. Self-describing by construction

**Verdict: KEPT; it is already family law (H-6).**

**The lesson, with its bill.**
- About 41% of public methods in the big three classes carry their own doc-comment
  (String 49.8%, List 29.0%, Number 43.6%); the harvester fills the rest by forward,
  suffix and sibling inheritance; `#@` intent tags: 112 lines in 4 files [M, compass
  page].
- `Ask`, `HowTo`, `ExplainMethod`, `BestMethodFor`, `WhatIs` are deterministic and
  zero-hallucination because they read tables (lexical-IDF first, measured 19/30 against
  a reranker's 15) [M, compass page lane 05].
- The Grammar Commons legislates `RATIONALE` as a mandatory trailing clause on every
  declaration; a trailing clause binds it syntactically so a lossless AST cannot lose it
  [R, ringua/docs/commons.md 3.8]. stzu v0.1 carries it on every declaration [R].
- The compiled image already carries names, locals, owners, parents [R, ringpp CLAUDE.md
  image VERSION 2, prefix VERSION 2].

**The rule [D].**
1. Every definition carries an intent clause, trailing, prose: `def Name(...) is
   "..."`. A definition without one is refused (`MISSING_INTENT`).
2. The image carries per definition: name, form, typed signature with parameter names,
   intent, owner, and the fixtures that mention it. `Ask`/`HowTo`/`ExplainMethod` read
   those tables and nothing else.
3. Under the migration profile only, an intent may be marked `inferred "..."`, taken from
   the harvester; the strict profile refuses it.
4. A fixture (a narrated guard) that calls a definition is indexed as that definition's
   example; "the e.g." the harvester already builds becomes a table.

**What it costs.** The 59% of public methods without an own intent line: authorship, or
the harvester's proposals accepted under the migration profile. The image grows by the
intent strings (a few MB on the Softanza unit, to be measured).

**The guard.** `rnxc ask Twice` prints the intent from the image; a definition without an
intent is refused in a fixture; a `HowTo` probe answers from tables only, with the
harvester off.

---

## 6. Cheap to be wrong

**Verdict: KEPT; the number is corrected and the target is stated.**

**The lesson, with its bill.**
- 2-3 s of process start times 277 files = 14 minutes of startup; "flaky is a latency
  defect"; "a re-run is the most expensive wait there is" [R, stzlib CLAUDE.md, PX law
  CENTRAL-PXLATENCY-01].
- A Softanza program paid 7.28 s before its first statement (613 files, 3.38 s of
  tree-sitter), 0.12 s with the image, 0.25 s for a never-run child on the prefix
  [M, ringpp CLAUDE.md 2026-09-14, 2026-09-23].
- The launch prompt's "12-156x over Ring 1.27" is the hand-compiled spike's number
  [M, NOTES.md]; the shipped `rnxc` is behind Luau by 1.04-1.88x on all six rows, x64
  [M, softanza/memos/2026-09-13.md 19:16].
- Measured today, a six-line program, minima of 15: oracle 26.7 ms, `rnxc exec`
  18.4 ms, `rnxc <file>` 16.2 ms -- process start on both, inside one tick [M,
  2026-09-26 01:40, `px_measure.py` in the session scratchpad; `bench/haro_px.py` will
  hold it].

**The rule [D].**
1. Every fact that is compile-time is judged at compile time: a wrong program costs a
   parse and a check, never a run.
2. The library is resident (image, prefix); a program's verdict does not pay for the
   library.
3. The guard measures the library-loaded case, never the toy, and reports minima.
4. The target for the spike: under 100 ms from edit to verdict on a one-file program
   with the Softanza prefix resident. A target until measured.

**What it costs.** Nothing new: the image and the prefix exist. The cost that remains is
the first cold compile of the library, paid once per build.

**The guard.** `bench/haro_px.py`, section 7 of the charter.

---

## 7. Forms as execution modes

**Verdict: KEPT, corrected, made the language's (H-7).**

**The lesson, with its bill.**
- The forms document (`stz-functions-as-linguistic-expressions.md`, 1,109 lines) is a
  catalogue in 23 sections: active, passive, fluent (Q), immutable (QC), partial (@),
  plural (Many), exceptional (Except), negative (IsNot), alternative, named parameters,
  conditional (W), prefixes (viz), suffixes (CS, ST; IB used once and never explained),
  small functions, future (F/FF), random (rnd), deep, multilingual, free form (FF -- a
  clash with the future form's FF), default (dft/inf), free order, misspelled, statement
  (X); plus three planned. It states no percentage and no count of 24 [R, FINDINGS HF-1].
- "Q = returns the object" [R, the document, lines 80 and 620-630]; `q-returns-object`
  and `q-has-plain-twin` exist as house rules, run nowhere automatically [R, compass page
  lane 06].
- 46,493 definitions, 37,126 distinct names, about 10,600 spelling variants of an
  existing base, 35 spellings of `find` [M, analysis 5.3]. "No macros, no templates, no
  compile-time code generation, and no way to define a family of functions from a rule."
- The Ring++ charter: "compile-time function generation from a stated rule: one
  declaration of the Many/CS/Q grammar produces the family, the checker verifies every
  member against it" [R, charter 4e.6].

**The rule [D].**
1. The active form may mutate its receiver; the passive form (`Verbed`) may not, and a
   passive body that writes an attribute is refused.
2. `VerbQ` returns the receiver; a `Q` body returning anything else is refused; `VerbQ`
   requires `Verb` in the same class.
3. Suffixes `CS`, `ST`, `XT`, `IB` (and any suffix the family declares) name parameters,
   and suffix order is parameter order; the call cannot omit or reorder them.
4. `...W(cond)` takes a W literal, parsed at compile time; `...X()` is an assertion whose
   failure is a Haro error.
5. `Many`, `Except`, `IsNot`, `Deep`, `viz`, `rnd` are verified against the base
   definition's signature.
6. A definition declares the forms it offers (`forms [Many, CS, Q]`); the compiler
   generates the family and checks each member; a hand-written member that disagrees
   with the rule is refused.
7. Refused as grammar: the misspelled form, free-order parameters, per-language method
   names, and the `FF` clash (one meaning per suffix).

**What it costs.** Every hand-written family member in Softanza becomes either generated
or checked; the census of members that disagree with their rule is a number the
migration measures. A `Q` method that today returns a value is a refusal.

**The guard.** A form fixture per rule; the family generator's output pinned; the checker
run over the Softanza base unit printing members that disagree.

---

## 8. Humans read; agents write

**Verdict: AMENDED -- one grammar, one text, two audiences (H-1).**

**The lesson, with its bill.**
- NNL: "the human is the parser ... the sentence arrives already compiled. This is the
  exact mirror image of Naturally(), where the MACHINE parses and must refuse what it
  cannot prove" [R, NNL_REVIEW.md 25-29].
- NaturalLib failed at its own game: no referential context, immediate execution, the
  host's keywords fighting the vocabulary, reflection as parser (10x), natural code not
  data [R, analysis 6, five limits verified in source]. stzNatural replaced it with a
  whole-text compiler over a semantic core with per-language data skins.
- `Naturally()` today is deterministic and table-driven, and ends in `eval()` of
  generated Ring source [R, stzNatural.ring 1097-1098; FINDINGS HF-3]; its strict mode
  raises on unresolved words and on off-list operations, and the allow-list gate covers
  `METHOD_*` semantics only [R, HF-4].
- Two readers of one format drift: the `TO:`/`FROM:` header incident made thirteen
  delivered answers read as unanswered [R, mailbox/README.md].

**The rule [D].**
1. One grammar. The canonical text is what the agent writes and the human reads.
2. The narration (stzn) is a projection from programs and runs, never parsed back.
3. The natural door (`Naturally`, `NaturallyIn`, `HowTo`) is a library feature over a
   closed vocabulary; it parses, refuses, and emits a Haro program the compiler judges.
   No `eval`. Strict mode is the only mode for an agent; the allow-list gate covers every
   semantic kind, not `METHOD_*` alone.
4. No natural syntax in the grammar.

**What it costs.** The natural plane changes its last step from `eval` to program
emission; nothing else. The human loses nothing: the text was already the sentence.

**The guard.** A `Naturally` fixture whose result is a Haro program text that the
compiler accepts; a strict-mode fixture where `CREATE_OBJECT` outside the allow-list is
refused (the gap named in HF-4).

---

## 8, amended in v0.2. Humans read; agents write -- the default venue is declarative

**Verdict: AMENDED AGAIN (H-1 reversed by the author, 2026-10-01).**

**The lesson, with its bill.** v0.1's amendment stands at the computing altitude (one
grammar, one text, the narration a projection, the natural door a library feature). The
ruling adds what the alphabet already ratified: "the default venue -- 100% declarative and
natural. A solution designer declares the world in Z, gets an executable immediately,
constrains and computes in W, asks in Q, moves work in F, steps in A, and converses in N.
End users get Q and N too"; "the expert venue -- any combination with the lower level ...
One governed door per level, never a hidden escape" [R, 06-ALPHABET, ratified 2026-09-27].
And N's ink lines: "natural language asks; it never declares"; "N may DRAFT declarations ...
produced through the closed compile target ... a draft enters the world only as a proposal
judged by the court ... N proposes; the court decides; the human ratifies" [R, same].

**The rule [D].**
1. The maker's and the agent's default venue is the declared altitude; the human reads the
   same sentence the agent emitted, in the domain's jargon.
2. The natural door (N, Aicha) asks and drafts; it never declares; its drafts are sentences
   of the declared language produced through the closed compile target, judged by the court
   and ratified by a human. It never produces computing-altitude code for evaluation.
3. The computing altitude is reached through one declared door, never by default.
4. Within each altitude, one grammar and one text; the narration is a projection.

**What it costs.** Nothing new: it is the ratified alphabet applied to the language.

**The guard.** A fixture where N drafts a Z sentence, the court judges it, and the draft is
refused when it names a thing the world does not declare.

---

## 9. Declaring a language is as easy as declaring a variable

**Verdict: ADDED (the ruling of 2026-10-01).**

**The lesson, with its bill.**
- The founding act: "DECLARE A LANGUAGE ... let the machinery return it as a true language --
  executable, judged, governed, intelligent" [R, 01-KERNEL]. "Softanza is the machinery that
  makes declaring such a language as easy as declaring a variable" [R, same].
- Ringua's five contracts and three strata [R, ringua/README.md 27-33; mission.md 1]; its
  honest boundary: "no code exists in this repository yet" [R].
- What exists: stzu v0.1 declares W, ZQL and the machine language, with a meta-court and
  fixtures [R, stz/declarative/stzu]; `machine.stzu` is 79 lines for a language that boots
  a computer [R, harobanda].
- The alphabet: six letters, "learnable in an evening each", composing to "the most complex
  enterprise reality" [R, 06-ALPHABET].

**The rule [D].**
1. The declaring altitude is first-class in Haro: a language is a value with a `VERSION`, a
   `GRAMMAR`, a `COURT` and an `EXTENSION` (stzu v0.1's `DEFINE LANGUAGE`, kept).
2. A maker composes a domain language from the alphabet: a vocabulary over Z W Q F A N; one
   word belongs to one letter.
3. The forge produces, from the declaration alone: parser, court, printer, GBNF, knowledge
   graph, query grammar, natural door, narration, runtime, one static binary.
4. A language is judged by the meta-court before it exists, and by its own court after.

**What it costs.** The forge, which does not exist (ST-8 is "the standing rung" [R,
softanza/memos/2026-09-13.md]); the seats stzu v0.1 lacks; Ringua's Phase 1.5 study before
the knowledge and pragmatics seats are drawn [R, mission.md 6].

**The guard.** The spike of the charter's section 10: `machine.stzu` forged on `rnx`, 54
fixtures agreeing with `harb check`.

---

## 10. Every change is a refinement

**Verdict: ADDED (the ruling of 2026-10-01).**

**The lesson, with its bill.**
- "AI removed the bottleneck on producing code and created a new one: trusting code -- yours
  or an agent's -- that arrives faster than anyone can review" [R, refine/README.md 3-5].
- "A refinement is a typed, bounded change to a declared point in a system, validated
  against declared rules before it lands, attributed to its author, aware of everything it
  affects, and reversible by construction" [R, rop-book.md 205].
- "Every named thing is a candidate refinement point. The boundaries are not author-chosen;
  they are language-required" [R, DECLARATIVE_FOUNDATIONS_FOR_REFINEMENT 64].
- "A refinement compiler takes a stream of refinements as its source language" [R,
  THE_REFINEMENT_COMPILER 18]; "the diff is a derived view, the cascade is the primary one"
  [R, START_HERE 18-21].
- "A typed proposal against a declared point is the safest write surface you can hand an
  autonomous system" [R, rop-book.md 557]; a trust floor refuses model-composed proposals
  "not by convention, by construction" [R, 565].
- Today: `stzRefinableCode.ring` runs five stages (structural, constraint, governance,
  trust posture, derivation) on `<R:KIND ...>` tags in comments; its header says four; the
  constraint stage checks `param`, `algo` and `lib` only; `Save()` writes the raw source
  and no history [R, HF-19, HF-22]. "A change to a machine is a refinement" [R, 07-SYSTEM].

**The rule [D].**
1. Every named thing is a refinement point by the language; a declaration is its own point,
   carrying kind, bounds and trust floor; the comment tag is the lift for foreign code only.
2. A refinement is a sentence of Haro: `target`, `from`, `to`, `author`, `reason`, and the
   optional `policy`, `cascade`, `gates`, `reverts`; it does not compute.
3. The compiler takes refinements as a second source language (`haro refine`).
4. One gate over all altitudes: structural (the language's own court), constraint,
   derivation, governance, trust posture; a refusal names its stage and carries the four
   parts (what, why, what next, where to learn).
5. The inverse is computed before the refinement lands; a revert is its own event; nothing
   is erased; the audit chain is a by-product.
6. The refinement point's grammar is the agent's write surface (v0.1's grain 3).
7. A language's grammar version is a point whose cascade is its fixtures and its consumers'
   pins.

**What it costs.** Kind, bounds and trust floor on every declaration (the Commons' typed
seats and mandatory `RATIONALE` carry most of it; profiles default the rest); the gate on
every change; the authorship of trust floors and risk tiers.

**The guard.** The spike's refinement fixture: a `RESTART` value refined through the gate,
admitted, refused at the trust stage as `:llm`, and reverted, with its C2 record pinned.

---

## 11. Total by default

**Verdict: ADDED (the alphabet's totality doctrine, made the language's).**

**The lesson, with its bill.** "The alphabet is deliberately not Turing-complete, and that
is its power, not its poverty": W's evaluator is total and terminating; F has no expression
production at all; A iterates over declared collections only; "nothing in the alphabet can
run away ... non-termination is unexpressible. This is the claim no general-purpose language
can make" [R, 06-ALPHABET, "The totality doctrine"]. Ringua: "a Ringua language that grows
conditionals, loops, and user functions has left the jurisdiction" [R, design.md 4].

**The rule [D].**
1. The declared altitude is total: no unbounded loop, no recursion, no user function, no
   host call is expressible in any declared language.
2. Computation beyond totality passes through one declared door to the computing altitude:
   an `A` step naming a computing-altitude verb with its capability, judged like any seat.
3. The computing altitude is the expert venue and keeps v0.1's rules; its programs are
   general-purpose and say so.

**What it costs.** A maker who needs an unbounded computation writes it at the computing
altitude and declares the door; the court names the door in the narration.

**The guard.** A fixture where an `A` declaration attempts an unbounded iteration and is
unparseable, and one where the declared door is named and the narration shows it.
