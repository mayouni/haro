# Haro -- the charter

**Status: v0.1 DRAFT, 2026-09-26, awaiting the author's ratification.** Written by the
`haro-charter` session (task `COMPASS-HARO-CHARTER-01`, launch prompt of 2026-09-25) on
branch `next` of `ringpp`, under the visibility rule: nothing here reaches `main` or any
public remote. Nothing is built. No parser, no compiler, no VM change exists for Haro.

**How to read it.** Every claim is one of three things, and says which: **[M] measured**
(a number, with the file and date it came from), **[R] recorded** (a ruling, a finding or a
correction already in the estate's record, cited), or **[D] designed** (this charter's own
proposal, which the author may reverse by name). A number quoted without a source is a
defect in this document.

**The one sentence.** Haro is the language an agent writes and a human governs, on the
`rnx` register VM: every sentence it can write is grammatical by construction, every
refusal tells the writer what to do next, every definition says what it is for, and
nothing a program does can change what its own words mean.

---

## 0. Provenance -- what this charter stands on

Read in the order the launch prompt gave, each a source cited below by its path:

- `ringpp/CLAUDE.md` (the five commitments, the oracle, the corrections C-1..C-16, the
  wide clock), `ringpp/README.md`, `ringpp/NOTES.md` (the F-39 rows and *What flatters the
  spike*), `ringpp/docs/CORRECTIONS.md`, `ringpp/docs/FINDINGS.md`, `ringpp/src/check.zig`,
  `types.zig`, `why.zig`.
- `softanza/memos/2026-08-30-ringpp-design-charter.md` -- the Ring++ design charter: the
  defect catalogue, principles P1..P10, Rules A..E. Haro inherits all ten (section 2.0).
- `softanza/memos/2026-08-30-ring-critical-analysis.md` -- *Ring, Judged by the Record*:
  sections 2.1-2.18, 3.1-3.3, 4.x, 5.2, 5.3, 6. The "leaves" list (section 3) uses that
  document's numbering, so every item can be checked against its evidence grade.
- `softanza/vision/01-KERNEL.md`, `02-STACK.md`, `08-NORTH-STAR.md`.
- `stzlib/CLAUDE.md` "What NOT to do" and "Editing discipline".
- `stzlib/.../doc/design/SOFTANZA_INTELLIGENCE_ARCHITECTURE.md` LAW 1-6; `NNL_REVIEW.md`;
  `doc/narrations/stz-functions-as-linguistic-expressions.md`; `meta/stzCodeRules.ring`;
  `natural/stzNatural.ring`; `agentic/stzAgentDeclaration.ring`;
  `neural/SOFTANZA_STRUCTURED_OUTPUT.md` (C9); the engine's `gbnf_machine.zig`,
  `schema_gbnf.zig`, `neural_gen.zig`.
- `ringua/README.md`, `docs/mission.md`, `docs/design.md`, `docs/commons.md` (the Grammar
  Commons C6); `stzzql/GRAMMAR.md`, `conformance/fixtures.json`; `stz/declarative/stzu/
  GRAMMAR.md` (stzu v0.1); `stzzui/doc/diagnostic-contract.md` (C2 v1.2.0) and its schema.
- The two compass pages (the manual-vs-agentic check of 2026-09-26; the programming model).
- The field, read and not copied: Luau's sandbox and gradual types; Rust's ownership;
  Lean 4; DHH's Rails World keynote of 2026-09-23 as the compass page reports it.

Where a source and this charter disagree, the source is right and the disagreement is
listed in `haro/FINDINGS.md`. The findings that belong to other repositories are routed
through Central, not fixed here.

---

## 1. Who speaks, who reads, and what each is owed

### 1.1 The speaker is an agent

Not a metaphor: the estate's own record. The author wrote 300,000 lines of Ring by hand
before any assistant existed and has written none by hand for more than a year [R,
launch prompt section 1]; the same estate was built by "one human, one machine, about
fifteen sessions" [R, Bangalo, quoted in the compass page]. DHH said the same thing about
Rails on 2026-09-23. So the speaker of Haro is a program that:

- **iterates by running.** It does not read the manual first; it writes, runs, reads the
  verdict, and writes again. The loop is the interface.
- **reads errors as instructions.** An error it cannot act on is a wasted turn; an error
  that names the edit is a turn saved.
- **emits tokens under a sampler.** Contract C9 [R] can constrain that sampler to a
  grammar, so a token outside the grammar is never produced. This is the one property no
  human-first language could have, because no human writes under a decoder.
- **cannot be trusted with a silent global**, or with any silent semantics: it writes at
  volume, and what a human would catch once it reproduces a hundred times (the critics'
  answer to DHH, "the same Swiss cheese failures at higher volume" [R, compass page]).
- **has no memory of what it did not read**, so the language's tables, not its comments,
  must carry what a definition is and does.

**What the speaker is owed**, each traced to a paid-for lesson in section 2:

| owed | which principle pays it |
|---|---|
| a grammar the decoder holds, at the grain of the edit it is making | 3 |
| a refusal that is an instruction: where, what, why, and what to do | 4 |
| a verdict at compile time where the fact is compile-time, in milliseconds | 6 |
| one obvious spelling, so no token is spent choosing between equivalents | 2 |
| the language's own tables answering *what is this* and *how do I* | 5 |
| no silent success: nothing that is wrong runs quietly | 1 |

### 1.2 The reader is a human who governs

The human directs, reviews and governs, and does not type. The reader must be able to
read a Haro program as a sentence, decide whether it is the program wanted, and stop it
from doing what was not wanted. **What the reader is owed:**

- **a canonical text that reads as prose.** The Softanza vocabulary is already that
  text: `Q("ring").RemoveQ("x").Uppercase()` is a sentence because the function-name
  grammar (principle 7) makes the name carry the parameters, their order and the
  execution mode. The reader's surface is the same text the agent writes (section 2.8:
  there is one grammar, not two).
- **every definition saying what it is for**, in the definition, not in a comment the
  harvester infers (principle 5).
- **a narration of every run** (stzn, "how the machine speaks back" [R, 01-KERNEL]), so
  what happened is readable without reading code.
- **governance by construction**: effects declared and gated (the `.pia` posture model
  [R]), a change judged before it lands (Refine), an agent that proposes while only a
  gate commits.

### 1.3 The third party: the court

Between the two stands the court -- the compiler and its fixtures. It is owed
determinism (the same text, the same verdict, on every machine, "nothing is believed,
everything is judged" [R, 02-STACK]) and the C2 envelope for every refusal (section 5).

---

## 2. The eight principles, answered

Each principle is **kept**, **amended** or **refused**, with the lesson it comes from.
`haro/PRINCIPLES.md` carries the full text; this is the verdict table.

### 2.0 Before the eight: the ten Haro inherits

The Ring++ design charter [R, 2026-08-30 section 3] stated ten principles, each answering
a numbered defect. Haro inherits all ten unchanged; three are sharpened because Haro is not
bound by Ring's surface:

| Ring++ | Haro |
|---|---|
| P1 strict by default; any relaxation opt-in, never silent | inherited; the relaxations are a declared **profile**, never a flag |
| P2 a read never writes | inherited (C-13 already decided it; "Haro will not have it" [R]) |
| P3 values are values | inherited (the value model is `rnx`'s) |
| P4 resolve at compile time; runtime search reported | **sharpened**: runtime name search does not exist; no `eval`, no `loadlib` hole, so the four absence rules are refusals, never "NOT checked" |
| P5 one mechanism per concept | inherited (`for/in` and `for/to` one machine) |
| P6 order-free declarations | inherited (F-21's position rules are gone) |
| P7 Unicode is not a dependency | inherited |
| P8 one binary, every target | inherited (commitment 5) |
| P9 performance stays inside the language | inherited |
| P10 decisions documented and contestable | **sharpened**: a Haro decision is a C-number in `docs/CORRECTIONS.md` or an H-number here, never prose alone |

### 2.1 No silent global -- KEPT, and made structural

**The lesson [R].** `nL = len(cPixels)` replaced the `NL` constant with a number for the
whole process; `cR = 7` did the same to `CR`; `TRUE = 0` inverts every comparison and
nothing errors; 2,898 reads of `NL`/`TAB`/`CR` were swept and 4,460 reads of
`TRUE`/`FALSE`/`NULL` remain exposed [stzlib/CLAUDE.md "What NOT to do"; analysis 2.1].
The library itself clobbered `NL` four times [R, the `writes-a-mutable-constant` rule's
first run].

**Haro [D].** There are no predefined *variables*. `true`, `false`, `nil` are literals of
a boolean type and of an absence type (analysis 3.1: "one type, absent, is carrying an
entire family of production hazards"). Newline, tab and return are string escapes
(`"\n"`, F-55 closed), so no name stands for them. A global is declared at the top level
and spelled `$name` wherever it is read or written (Rule A [R]); an attribute is
`@name`; a bare name is a local and resolves nowhere else, in a function, a method or a
lambda alike (analysis 2.7; C-2's accepted divergence becomes the rule, and C-14's
lambda exception is not carried). A read of a name nothing declared is a compile-time
refusal (P4), and it cannot be silenced by a hole, because the language has none.
**Shadowing is refused**: a local may not reuse the name of a global or an attribute
visible at that point; the refusal names both sites.

**What it costs.** Softanza's Rule A migration surface: 160 bare-name sites classified
2026-09-09 [M, ringpp/CLAUDE.md], 90 of them class attributes without `@` -- the `rnxc
migrate` surface -- plus C-14's seven top-level-lambda sites. Nothing at run time.

### 2.2 One obvious spelling -- KEPT, with the case rule decided

**The lesson [R].** `N` and `n` are the same variable (F-18); 887 of the classic suites'
errors are C22 case collisions [compass page]; `NthStz` and `NthSTZ` collide [stzlib
"Editing discipline" 2]; `oK` and `oR` are keywords because `ok` and `or` are; `cAll`
was a C13 error for containing `call`; and Ring accepts two or three spellings of almost
every construct, measured at 32,180 `ok/next/off/done` against 859 `end`, 36,543 `def`
against 7,872 `func` [M, Ring++ charter 4c].

**Haro [D].**
- **Identifiers are case-sensitive, and a case-only collision is refused.** Two names in
  one scope that differ only by case are a refusal naming both (the C22 class becomes a
  `todo`). Softanza's mixed-case method names stay exactly as written.
- **Keywords are a closed set, reserved in every casing**, and no keyword is a valid
  identifier or a valid prefix trap: `cAll` is a name. The mixed-case keyword trap is
  closed at the tokenizer, as stzu v0.1 already does [R, stz/declarative/stzu/GRAMMAR.md,
  "Lexical form"].
- **One spelling per construct** (Rule C [R], adopted whole): one block closer, one
  comment form, one print, one logical-operator family, one definition keyword, one
  string quote. The table is in `haro/GRAMMAR-SKETCH.md`; the choices are the author's
  to ratify, the rule is not.
- **A symbol keeps its text** (Rule D1 [R]): `:StartingAt` is `StartingAt`; comparison
  stays case-insensitive symbol-to-symbol, which keeps the 27,807 sites working [M].
- **No redefinition is silently accepted**: a second definition of a name is a refusal
  naming the first (Ring dies at load with C22; Ring++ took one silently [R, CLAUDE.md
  "Named, not done"]; Haro refuses at compile time).
- **Refused, by design: the Misspelled Form.** The forms document lists typo-tolerant
  names (`WithoutSapces`, `NearstTo`) as a form [R, stz-functions-as-linguistic-
  expressions.md, "Misspelled Form"]. An agent must be corrected, not accommodated; the
  refusal carries the suggestion (`did you mean`) exactly as `NaturallyStrict` does.

### 2.3 Grammar the decoder can hold -- KEPT, with its limit stated and one grain added

**The lesson [R].** C9: "a declared grammar makes a violating token unemittable"; measured
10 of 10 valid on first attempt against 2 of 10 unconstrained [M, SOFTANZA_STRUCTURED_
OUTPUT.md 88-97]. Today the kernel promises this for every declared grammar and ships it
only for C9's schemas [R, compass page lane 09]; no `.pia`, W, `-ex` or `.zknw` surface
emits a grammar [R, haro/FINDINGS.md HF-8].

**Haro [D].** The grammar is written **once**, in one source file, and one generator
emits from it (a) the parser tables `rnxc` uses, (b) the GBNF the sampler holds, (c) the
editor grammar. A gate proves the three agree on the fixtures (section 4). The GBNF is
emitted at **three grains**:

1. **the file** -- a whole Haro program;
2. **the hole** -- one statement, expression or definition, for an agent editing in
   place;
3. **the scoped hole** -- the hole's grammar with the names in scope inlined as
   terminals, each with its arity and its parameter names. At this grain an undefined
   name, a wrong arity and an unknown named parameter are all *unemittable*, not merely
   refused. This is the one grain that is new to the estate, and it is the one an agent
   needs most.

**The limit, stated on the face of the claim** (C9's own amendment, clause 8): a
context-free grammar kills malformedness and structural absence. It does not kill type
errors, does not know a value, and does not know truth. Those are the court's. Two
constraints of the machine itself: `gbnf_machine.zig` cannot express non-ASCII inside a
character class [R, its lines 40-47], so Haro identifiers are ASCII (Softanza's already
are) and string literals go through byte ranges; and the cost of a scoped grammar grows
with the names in scope -- a Softanza unit has about 45,000 function names -- so the
grain-3 grammar for a hole lists the *reachable* names (this class, this unit's
functions, the imports), and its cost per alternative in the pushdown machine is a
number the spike measures before the grain is promised.

### 2.4 Refuse, then explain -- KEPT; the shape is C2 plus two fields

**The lesson [R].** `StzRaise([:Where, :What, :Why, :Todo])` is the right shape and is
used in 5 of 3,956 calls [compass page]; Ring's error is a string, and the string is a
global (analysis 2.17); where it happened is qualified only by discipline (2.18); an
ambiguity that guesses is LAW 3's own failure; ZQL refuses with "the verb set is closed
-- destructive or unrecognized operations are not part of the grammar" [R, stzzql/
GRAMMAR.md 15-16].

**Haro [D].** A Haro error is a **value**, not a string, and it is a **C2 v1.2.0
envelope** [R, stzzui/doc/diagnostic-contract.md] -- `code`, `severity`, `message`,
`span`, `cites`, `language: "haro"` -- with extension fields C2 permits: `why` (the
rule, and the finding it descends from, as `cites` entries plus one sentence) and `todo`
(an applicable edit when the fix is mechanical, a sentence otherwise). Section 5 gives
the record and three examples. **Ambiguity refuses**: a sentence with two parses is
unparseable, never resolved by precedence folklore (the `:` that is a range, a pair and
a lowercase operator at once [R, analysis 2.14, Rule D] is three different tokens in
Haro).

### 2.5 Self-describing by construction -- KEPT, and it is already family law

**The lesson [R].** About 41% of Softanza's public methods carry their own doc-comment;
the harvester infers the rest by forward, suffix and sibling inheritance [compass page];
`Ask`/`HowTo`/`ExplainMethod` are deterministic and zero-hallucination *because* they
read tables, and they would be better with better tables. The Grammar Commons legislates
`RATIONALE` as a mandatory trailing clause on every declaration [R, ringua/docs/
commons.md 3.8], and stzu v0.1 is the first family language to carry it on every
declaration [R].

**Haro [D].** A definition -- function, method, class, global, form family -- carries an
**intent clause**, and a definition without one does not compile. The intent is prose,
never compared, never parsed for meaning (the standing C2 gives `message`). The compiled
image carries, per definition: name, form (parsed from the name), typed signature with
parameter names, intent, owner, and the fixtures that call it. `Ask`, `HowTo` and
`ExplainMethod` read those tables. Softanza's `#@` tags and the harvester's inferred
prose survive as the **migration source**: an intent the harvester inferred is marked
`inferred` and is legal under the migration profile only (a decision for the author,
section 8).

### 2.6 Cheap to be wrong -- KEPT, and the number is corrected

**The lesson [R].** 2-3 s of process start times 277 files was fourteen minutes of
nothing [stzlib/CLAUDE.md PX]; a Softanza program paid 7.28 s of read, parse and compile
before its first statement, against Ring's 3.06 s, until the compiled image took it to
0.12 s and the prefix took a never-run child to 0.25 s [M, ringpp/CLAUDE.md 2026-09-14
and 2026-09-23].

**Measured today [M], because the launch prompt quotes "12-156x" and that number is the
hand-compiled spike's, not the shipped compiler's** (haro/FINDINGS.md HF-9):

    a six-line program, no library, minima of 15 runs, 2026-09-26 01:40, this machine
      oracle  runtime/win64/ring.exe          26.7 ms
      rnxc exec (zig-out/bin/rnxc.exe)        18.4 ms
      rnxc <file>                             16.2 ms
    process start dominates both; the difference is inside one scheduler tick

    the shipped rnxc against Luau, x64, 2026-09-13 [M, softanza/memos/2026-09-13.md]
      Luau leads all six F-39 rows, 1.04-1.88x. Ring++ is in Luau's class, which no
      Ring ever was; the 12-156x over Ring 1.27 is the spike's, with its caveats in
      NOTES.md "What flatters the spike"

So "cheap to be wrong" is not a speed claim about a toy; on a toy both runtimes are
already inside a tick. It is three things: **(1)** the verdict arrives at *compile*
time wherever the fact is compile-time (P4), so being wrong costs a parse, not a run;
**(2)** the library is *resident* -- the prefix and the image -- so a Softanza program's
verdict is not paid for 613 files at a time; **(3)** the guard measures the
library-loaded case, never the toy. The spike's target (section 7): a verdict under
100 ms on a one-file Haro program with the Softanza prefix resident, minima of 15,
against the oracle's number for the Ring twin. A target, not a claim, until measured.

### 2.7 Forms as execution modes -- KEPT, corrected, and made the language's

**The lesson [R].** The forms document is a designed grammar: `Remove` acts, `Removed`
copies, `RemoveQ` chains, `@Removed` works on the selected part, `Many` takes a
collection, `Except` subtracts, `CS`/`ST` fix the parameters and their order, `W` takes
a condition, `X` asserts, `viz` draws, `Deep` recurses, `rnd` randomises, `F`/`FF`
defer. **Two corrections to the launch prompt:** the document catalogues 22 to 23 forms
in 23 sections, not 24, and it contains no usage percentage -- "71% live" has no source
in the tree [R, HF-1]. And the price of writing the grammar by hand is 46,493
definitions of which about 10,600 exist only as a spelling variant of a base, 35
spellings of `find` alone [M, analysis 5.3].

**Haro [D].** The forms whose semantics are mechanical become **grammar and type rules**:

| form | Haro rule |
|---|---|
| `Verb()` / `Verbed()` | the active form may mutate its receiver; the passive form returns a value and may not (checked: a passive body that writes `@attr` is refused) |
| `VerbQ()` | returns the receiver; a `Q` body that returns anything else is refused (`q-returns-object` as a compile rule); `VerbQ` requires `Verb` (`q-has-plain-twin`) |
| `...CS`, `...ST`, `...XT`, `...IB` | suffix order is parameter order; the suffix declares the parameter, so a call cannot omit or reorder it |
| `...W(cond)` | the argument is a W literal, parsed at compile time by the W grammar |
| `...X()` | an assertion; its failure is a Haro error, not a printed line |
| `...Many`, `...Except`, `IsNot...`, `Deep...`, `viz...`, `rnd...` | naming rules the checker verifies against the base definition |

And the families are **derived from a rule, once**: a definition declares the forms it
offers (`forms [Many, CS, Q]`) and the compiler generates the members and checks each
against the base -- the compile-time metaprogramming the Ring++ charter asked for [R,
4e.6 and analysis 5.3]. **Refused as grammar**: the Misspelled Form (2.2), free-order
parameters (the same call meaning the same thing in two orders is two spellings), and
per-language method names (packs of data for the natural door, not identifiers).

### 2.8 Humans read; agents write -- AMENDED: one grammar, one text, two audiences

**The lesson [R].** "In NNL the human is the parser" [NNL_REVIEW.md 25]; `Naturally()`
is "the exact mirror image", where the machine parses and must refuse; NaturalLib failed
because natural code was not data and executed as it appeared [analysis 6]; and the
estate keeps relearning that "a format the tooling reads is not prose" and that a drift a
human eye forgives is the one that survives [R, mailbox/README.md, CENTRAL-BLOCKHEAD-01].

**Haro [D]. One language, one grammar, one canonical text.** The launch prompt's "two
surfaces" is answered without a second parser, because a second parsed surface is two
courts that drift:

- the **canonical text** is what the agent writes and what the human reads; it reads as a
  sentence because the forms and the NNL device catalogue (articles, prepositions,
  conjunction, agreement, anaphora as method conventions) are the vocabulary. The human
  is still the parser of the *sentence*; the machine is the parser of the *text*.
- the **narration** (stzn) is a projection *from* the program and its runs -- never
  parsed back. It is where the governing reader lives.
- the **natural door** (`Naturally`, `HowTo`) stays a library feature over a closed
  vocabulary: it parses, refuses ambiguity and unresolved words, and produces a **Haro
  program judged by the same compiler**. It never produces source text for an `eval`,
  because Haro has no `eval`; today it does end in `eval()` [R, HF-3], so this is a
  change the natural plane must make on the way to Haro.

Refused: natural syntax *in* the grammar (Inform 7's lesson runs the other way: a
whole-text compiler with referential context is what stzNatural already is, and it
belongs beside the language, not inside it).

---

## 3. Carry, leave, decide

### 3.1 Carried [R, author's ruling 2026-09-12 in 01-KERNEL; this charter's reading]

- **Ring's simplicity**: a small statement set (`if/but/else`, `for`, `while`, `switch/on`,
  `try/catch`, `return`, `?`), one aggregate literal (the list), the `obj { }` block, no
  ceremony to move between styles (Ring++ charter 4e.7 refuses a paradigm keyword).
- **Multiparadigm expressiveness**: classes with attributes and `This`; first-class
  functions and lambdas; the declarative brace form, given its missing reading direction
  (4e.5: "a DSL author defines a shape once and gets both a text reader and the brace
  form"); operator overloading, declared (F-69).
- **The Softanza vocabulary as the compatibility specification**: every Softanza public
  signature is a Haro signature; the migration is a census, and `rnxc census` already
  measures it (118,638 statements, 118,413 compiled, 224 refused [M, 2026-09-25]).
- **Rule A's sigils** (`$global`, `@attribute`, bare local), Rule C (one spelling), Rule D1
  (symbols keep their text), the two-element pair as the one destructuring shape (532 of
  556 sites [M, charter 4g.4]).
- **Named arguments as a call protocol** (analysis 5.2: 6.3-7.8 us per call in Ring,
  550x Python's), spelled as Softanza spells them, `:Name = value`, resolved at compile
  time -- see decision D4.

### 3.2 Left -- each item is a section of *Ring, Judged by the Record* or a finding

| left behind | Haro's answer | source |
|---|---|---|
| truth is a variable | boolean type, literals, unassignable | 2.1, 3.1 |
| a read that writes (`aHash[k]` inserts) | P2; C-13 already decided | 2.2, F-49 |
| the language redefinable from inside (`ChangeRingKeyword`, `eval`) | closed grammar; no `eval`, no keyword change; C-9's own text says the rule "belongs to HARO" | 2.3, C-9 |
| equality that does not compare (`[1,2] = [1,2]` is 0) | structural equality for values; identity (`is`) for objects | 2.4, 2.9 |
| case-insensitivity at scale | decided at parse (2.2) | 2.5, F-18 |
| names resolve at run time and die at run time | P4; the four absence rules are refusals | 2.6 |
| a method cannot own a name | a bare name is a local, always | 2.7 |
| equality that converts (`"" = 0` is true; `1 = "01.01"`) | no implicit string-number conversion; C-8 kept it for the bridge and named the strict build as the place it goes | 2.8, C-8 |
| rounding is a mutable process-global | `decimals` is a formatting argument | 2.10, C-10 |
| `switch` takes one value per `on`, silently | multi-value `on` (Ring++ has it) | 2.11 |
| the loop variable after the loop, four rules | scoped to the loop (C-11) | 2.12 |
| block comments do not nest | one comment form (Rule C) | 2.13 |
| a bare colon lowercases the next word | symbols keep text (Rule D1); the three jobs are three tokens | 2.14 |
| the range answers with the wrong type | typed ranges | 2.15, C-5 |
| `sort` is not stable | stable by contract | 2.16 |
| an error is a string, and a global | the C2 record (section 5) | 2.17, F-68, C-15 |
| where the error happened, qualified | exact spans, the frame chain, the callee's line rule (C-8, 2026-09-22) | 2.18 |
| four types asked to carry more | the Lua-sized answer already demonstrated: boolean, integer, float, string, array, map, object, plus `nil` | 3.2, 3.3 |
| doubles for everything | integer and float; a number carries its own precision | 4.5, 4.6 |
| no named parameters | named parameters (3.1) | 5.2, F-59 |
| no static metaprogramming | form families from a rule (2.7) | 5.3 |
| natural programming that executes as it appears | the natural door beside the language (2.8) | 6 |
| every `func` after the first `class` becomes a method; bodies by position | P6 order-free; a definition owns its body by structure, closed by `end` | F-21, NOTES "four findings" 1 |
| `get`/`put` cannot be method names | no accidental reservations: keywords are the closed set and nothing else | F-20 |
| no string escapes; `\"` fails silently | escapes (`\n`, `\t`, `\"`) | F-55 |
| `char()` wraps modulo 256 | refuse out of range | F-56 |
| `n++` as a value is a pre-increment | `++` is a statement only | F-64 |
| `if cond : stmt` builds a list that is always true | a list is not a truth: a condition must be boolean | F-65 |
| a function with no `return` yields `""` | it yields `nil`, and its type says so | F-66 |
| `aList + v` appends in place anywhere | `+` never mutates; append is a verb | F-68 |
| reading an unknown name in a class body creates the attribute | refused at compile time | F-70 |
| `substr(s, a, b)` is find with two arguments and replace with three | no arity-changes-meaning; the forms fix parameters | stzlib "What NOT to do" |
| a method named `len` shadows the builtin for every caller | a method may not take a builtin's name (`no-len-method` as grammar) | stzlib, F-17 |
| `for x in list` re-evaluates its source | one loop machine, bounds once (P5) | stzlib, F-43 |
| non-ASCII console output garbles | UTF-8 out by default (P7) | stzlib |
| Ring's runtime, governance, OpenGL-era bindings | not carried (01-KERNEL) | ruling |

### 3.3 Decided by this charter, reversible by name (H-numbers)

- **H-1** one language, one grammar, one canonical text (2.8).
- **H-2** case-sensitive identifiers, case-only collisions refused, keywords reserved in
  every casing (2.2).
- **H-3** no `eval`, no `loadlib` from the language; foreign code through stzx's one door.
- **H-4** a bare name is a local everywhere; `$` and `@` are the only ways up.
- **H-5** the error is a C2 envelope with `why` and `todo` (section 5).
- **H-6** the intent clause is mandatory; `inferred` is legal under the migration profile
  only.
- **H-7** the forms in 2.7 are grammar; families derive from a rule.
- **H-8** the GBNF is generated from the one grammar source at three grains (2.3).
- **H-9** Haro is the floor of the family; declared languages embed as typed literals
  (section 6).

### 3.4 Put to the author -- section 8.

---

## 4. The grammar contract: how the GBNF is produced and how C9 holds it

**One source.** `haro/grammar/haro.ebnf` (name illustrative), written in the Grammar
Commons' lexical form [R, C6: `--` comments, double-quoted strings, UTF-8, LF or CRLF
accepted and never diagnosed]. It is the only place the grammar is written. Three
artefacts are **generated** from it and never edited by hand:

1. the parser `rnxc` uses for `.haro` files (a hand-written recursive-descent parser is
   acceptable for the spike *if* the gate below proves it against the GBNF; the
   generated parser is the target);
2. `haro.gbnf`, the whole-file grammar, in the dialect `gbnf_machine.zig` accepts;
3. `tree-sitter-haro`, for editors and for `rnxc check`'s span machinery.

**The gate**, in `bench/gate.py`'s style, made to fail before it is trusted:

- every accept fixture parses under (1) and is accepted by (2) through
  `StzGrammarAccepts(gbnf, text)` [R, stzNeuralModel.ring 204, works with no model
  loaded];
- every reject fixture is refused by (1) *and* by (2), and the refusal carries the
  fragment the fixture names (the exemplar's gap G8 [R, ringua/docs/exemplar-zql.md]);
- N derivations sampled from (2) all parse under (1) -- the direction that catches a
  grammar wider than its parser;
- the three artefacts carry the same grammar version, and a fixture change lands with
  the prose in the same commit (the W discipline, "fixtures first, prose second" [R]).

**The three grains** (2.3) are produced by the compiler, not stored: grain 1 is the
file; grain 2 is the nonterminal the agent's edit targets; grain 3 is grain 2 with the
`ident` production rewritten as the alternation of the names reachable at the hole,
each function name followed by its parameter shape. The compiler already carries every
table this needs -- `global_names`, the per-function locals table, `fn_owner`,
`class_parent`, the dispatch table [R, ringpp/CLAUDE.md, image VERSION 2 and prefix
VERSION 2].

**How C9 holds it** [R, the engine, read 2026-09-26]: `StzGenerateXT(prompt, [:Grammar
= gbnf])` installs the grammar through `StzEngineNeuralSetGrammar`, then
`neural_gen_set_grammar`, then `stz_grammar_set`; at every step `sampleIdConstrained`
keeps only tokens whose whole byte piece the pushdown machine accepts, and
end-of-generation is allowed only when `stz_grammar_can_end` is satisfied; the run
reports masked, judged, steps, stalled, complete through `StzLastGrammarRun()`, and
`StzEngineGbnfDecodingSupported` says honestly whether decoding was constrained at all.
Any GBNF text is accepted today; there is no JSON-Schema path and Haro needs none.
Streaming refuses `:Grammar`; a Haro agent that wants tokens as they come pays that
until the engine changes.

**What travels with every claim** (C9 clause 8): *structure kills malformedness, not
falsehood.* A grammatical Haro program can still be the wrong program. That is what the
court, the fixtures, the narration and the governance gate are for, and this charter
promises none of them from the grammar.

---

## 5. The shape of a Haro error

**The record [D]** -- C2 v1.2.0's six fields, unchanged in meaning, plus three extension
fields C2 permits (none boolean, per its v1.2.0 clause):

```
{
  "code":     "CONST_ASSIGN",                     -- Haro's own, stable, never reused
  "severity": "error",
  "message":  "true is a literal and cannot be assigned.",
  "span":     { "file": "walk.haro", "line": 12, "col": 5 },
  "cites":    [ "rule:no-silent-global", "pattern:ring-2.1" ],
  "language": "haro",
  "why":      "On Ring, TRUE was a variable holding 1; assigning it inverted every
               comparison in the process and nothing errored (Ring, Judged by the
               Record, 2.1). In Haro true is a literal.",
  "todo":     { "say":  "If a flag was wanted, declare a local: bDone = true.",
                "edit": { "span": {...}, "replace": "bDone = true" } },
  "frames":   [ "Walk() walk.haro:12", "Main() walk.haro:3" ]
}
```

- `why` is one sentence and the citations; it names the paid-for lesson, so the agent
  learns the rule and not only the fix.
- `todo` is the instruction. When the fix is mechanical, `edit` is an applicable patch at
  a span; when it is a judgement, `say` alone. An agent applies `edit`; a human reads
  `say`.
- `frames` is Ring++'s own call chain (C-8), oldest last.
- The human line, one per error, is the same record folded: `haro walk.haro:12:5
  CONST_ASSIGN: true is a literal and cannot be assigned. Why: ... Todo: ...`.
- `severity` has C2's two rungs. Haro has **no warning that is a wrong program**: a
  house-rule finding is a warning only under the migration profile.

**Three examples, each a Ring trap the estate paid for:**

**(1) The constant clobber** -- `stzWordStream.MostFrequentWords` wrote `nL = len(_aRes_)`
and left `NL` a number for the rest of the process [R, stzlib/CLAUDE.md]. In Haro the
trap does not exist to be diagnosed: `nL` is a local and newline is `"\n"`. What Haro
refuses is the nearest thing an agent can still write:

```
haro stream.haro:41:5 CONST_ASSIGN: true is a literal and cannot be assigned.
  why:  On Ring TRUE was a variable; writing it inverted every comparison silently.
  todo: declare a local instead: bDone = true
```

**(2) The case collision** -- `NthStz` and `NthSTZ` in one class, a C22 at load that
made every method call fail with R14 across every test [R, stzlib "Editing discipline"
1-2; 887 such errors in the classic suites]:

```
haro stzString.haro:2210:9 CASE_COLLISION: NthSTZ differs only by case from NthStz,
  defined at stzString.haro:1187.
  why:  Haro identifiers are case-sensitive and a case-only difference is never a
        different name on purpose (Ring, Judged by the Record, 2.5; F-18).
  todo: rename one of the two, or delete the later one if it is the same method.
        edit: replace line 2210 `def NthSTZ(` with `def NthStz(`  -- if a duplicate
```

**(3) The colon that builds a list** -- `stzSurfacePlot.ring:697-700`, `if _bUp_ :
_nConnections_++` four times: the `:` is Ring's range, the expression is a list, a list
is truthy, so the increment happens whatever `_bUp_` is [R, F-65, ringpp/CLAUDE.md
"THE SIX DIAGNOSTIC REFUSALS"]:

```
haro surface.haro:697:12 COND_NOT_BOOLEAN: the condition is a list; a condition must
  be a boolean.
  why:  On Ring `_bUp_ : n++` was a two-element list and a list is always true, so the
        branch ran on every call (F-65). Haro has no one-line if with a colon.
  todo: write the statement on its own line inside the if:
        edit: replace `if _bUp_ : _nConnections_++` with
              `if _bUp_` / `    _nConnections_++` / `end`
```

The fourth shape worth naming without an example: **arity that changes meaning** --
`substr(s, needle)` finds and `substr(s, old, new)` replaces [R, stzlib]. Haro has no
such function, and a call with the wrong shape refuses with the definition's signature
*and its intent line* in `message`, because the intent line exists (2.5).

---

## 6. Relations

### 6.1 To the eleven declared surfaces

Measured on the tree on 2026-09-26 [M, haro/FINDINGS.md HF-5..HF-8]: only `.pia` has all
three properties of a declared language -- a closed vocabulary, a version gate, and a
load-time court whose findings accumulate in the family shape (22 refusal codes, 53
sites). `.zopt` is versioned and refuses at load with plain-string findings. `.zrlz` and
`.stzrulz` refuse only unknown names. `.zknw`, `.zrfn` and the six `-ex` pattern classes
accept malformed input without refusing it. `W` is compiled by the engine at the call
and refuses there. `Naturally` refuses only in strict mode. None emits a grammar.

**Haro's relation [D]: the floor, and a typed door for each.**

| surface | today | under Haro |
|---|---|---|
| `.pia` | closed, versioned, judged at load; the pattern | unchanged; the model Haro's own profiles follow. A Haro unit declares its capabilities the way a `.pia` declares its posture |
| `W` (`'{ @item > 5 }'`) | a string handed to `expr.zig` at the call | a **W literal**, parsed at compile time by the W grammar (stz/declarative/w), so a malformed W is a compile refusal, and the sampler's grammar includes W's |
| the `-ex` strings (listex, numbrex, matrex, graphex, tablex, timex) | parsed at construction; unknown tokens silently answer `[]` or an `"ERROR"` token never raised | each becomes a **declared grammar with fixtures** and embeds as a typed literal; the silent acceptance is a finding for its owner, routed |
| `.zknw`, `.zopt`, `.zrfn`, `.zrlz`, `.stzrulz`, `.narration` | data formats with loaders of uneven strictness | data, read through their loaders; Haro adds nothing and demands one thing: a loader refuses in the C2 envelope. `.narration` is stzn's output and is never parsed back |
| notations, rules-as-data | profiles built by API calls; a misspelt primitive never fires | data; the profile's own court is its owner's |
| `Naturally()` | parses, executes, ends in `eval` | parses, refuses, emits a Haro program the compiler judges; no `eval` (2.8) |

**And the family.** Haro is the general-purpose **floor**; a declared language is a world
above it (06-ALPHABET's "one governed door per level" [R]). stzu v0.1 declares languages
whose expressions come from closed menus with no `call`, no `eval`, no statement
position [R, stz/declarative/stzu/GRAMMAR.md, "Refused, by design"]; it cannot declare
Haro and must not, because Haro is where computation lives and stzu is where it is
refused. What Haro offers the family: the runtime in which stzf's forged courts and
runtimes are written, and the typed literal by which a Haro program carries a declared
sentence with the declared grammar's own GBNF spliced into Haro's at that position.

### 6.2 To Luau

Luau is the script host of `stz` today, "Luau-first, Ring-still", and stays Luau-judged
until the author routes a migration; a Ring++ host enters through the same script-host
C-ABI [R, stz/README.md, stz/CLAUDE.md]. Haro does not target Luau's VM. What it takes
from Luau, read and not copied:

- **the sandbox by absence**: no `loadstring` exists to cheat with, so the platform
  enforces closure [R, 02-STACK L1]; Haro has no `eval`, and a unit's reach (file,
  network, process) is a declared capability the host grants, the way `.pia` postures
  are granted -- the standard library is *limited*, not guarded;
- **gradual, checked types**: `--!strict` is what Ring's discarded annotation channel
  was reaching for [R, ringpp/README.md]; in Haro the hints are real, and the checker is
  the compiler (commitment 4);
- **the honest row**: the shipped `rnxc` is in Luau's class and behind it by 1.04-1.88x on
  x64 [M, 2026-09-13]. Haro inherits that VM and that number, and claims nothing faster
  until measured.

### 6.3 To Ring++'s checker

`rnxc check` carries 34 rule ids: 17 in `check.zig`, 17 in `types.zig`; the "37" in
CLAUDE.md counts expected findings, not rules [R, HF-13]. Each becomes one of three
things in Haro:

| becomes | rules |
|---|---|
| **impossible by grammar** (nothing to check) | string-escape, exit-outside-loop, exit-bad-depth, type-not-a-hint, anchor-unknown, default-not-trailing, default-missing-value, default-unknown-param |
| **a compile refusal** (the checker is the compiler) | undefined-function, uninitialized-variable, unknown-class, unknown-package (the four absence rules, with no holes to silence them), type-duplicate-func, type-arity, type-arg-mismatch, type-return-mismatch, type-declared-conflict, method-shadows-builtin, keyed-read-inserts (moot under P2), char-truncates, empty-catch (an empty handler is refused), varptr-unknown-name |
| **advice under a profile** (performance facts, not errors) | advise-forin, advise-patch-rebuild, len-in-loop-header, substr-in-loop, genarray-in-loop, varptr-in-loop, memcpy-string-dest, memcpy-nul-source, cache-reads-object, cache-impure, type-hints-missing, unparsed |

The 14 house rules of `stzCodeRules.ring` (15 run; `for_in_loop` is unregistered [R,
HF-2]) split the same way -- decision D3.

---

## 7. The spike plan -- the smallest Haro program that runs on `rnx`

**Not before ratification.** This section is the plan the spike will be measured against.

**The program**, `haro/spike/twice.haro`, and its Ring twin `twice.ring` for the oracle:

```
# twice.haro -- one definition with its intent, one typed parameter, one call

def Twice(n: integer) -> integer  is "doubles a number"
    return n * 2
end

? Twice(21)
```

**And its refused twin**, `twice_refused.haro`, which is the same file with `true = 0`
inserted before the call, and must produce the CONST_ASSIGN record of section 5, exit 1,
validated against the C2 schema.

**What the spike builds, and nothing more:**

1. a front end for this subset in `rnxc` (`rnxc haro <file>`): `def`/`end`, typed
   parameters, the intent clause, `return`, `?`, integer and string literals, a call, a
   local, `true`/`false`; compiled to the bytecode the Ring front end already emits, so
   the VM is untouched;
2. the intent clause carried in the image's function table, and one query that reads it
   back (`rnxc ask Twice` printing the intent) -- principle 5 in its smallest form;
3. one refusal in the C2 envelope with `why` and `todo`;
4. `haro/grammar/haro-subset.ebnf` and the generated `haro-subset.gbnf`, accepted by
   `gbnf_machine.zig`;
5. the guard.

**The guard**, `bench/haro_px.py`, born standalone and folded into `gate.py` only when
green, made to fail before it is trusted:

- **edit-to-verdict**: minima of 15 of `rnxc haro twice.haro` against `rnxc twice.ring`
  and the oracle on `twice.ring`; then the same with the Softanza prefix resident and a
  `load` of the library in the twin -- the number that matters. Target: **under 100 ms**
  with the library resident. Today's baseline for the toy is above (16-27 ms, both
  sides); the library-resident baseline is 0.25 s for a never-run child on the prefix
  [M].
- **the refusal**: the record validates against `diagnostic-contract.schema.json`, exit 1,
  and the human line matches a pinned fixture.
- **the grammar**: 200 derivations from the GBNF all parse; the reject fixtures are
  refused by parser and machine alike; `twice.haro` is accepted by `StzGrammarAccepts`.
- **the oracle**: `? Twice(21)` prints the same bytes on `rnxc haro`, `rnxc` and
  `ring.exe`.

**Not in the spike**: classes, forms, W literals, named parameters, grain-3 grammars, the
migration profile, Softanza compiled from Haro source. Each is a later rung with its own
guard.

---

## 8. The decisions only the author can make

Five, and the charter stops there. Each has this session's recommendation, which the
author may reverse by name.

**D1 -- One language or a family?** *Recommendation: one language, one grammar, one
canonical text (H-1); the family stays in stzu above Haro; the "second surface" is stzn's
projection and the natural door, never a second parser.* Reversing it means two grammars
and a round-trip court between them; the estate has paid for drift between two readers
of one format more than once this month.

**D2 -- The natural surface's scope.** *Recommendation: `Naturally` and `HowTo` stay
library doors over a closed, per-language vocabulary; they emit a Haro program the
compiler judges; no natural syntax enters the grammar; strict mode is the only mode for
an agent.* The alternative -- natural phrases as Haro statements -- is NaturalLib's
design, and the record says why it failed (analysis 6).

**D3 -- Which of the house rules become compile rules?** *Recommendation: six become the
language -- `q-returns-object`, `q-has-plain-twin`, `no-case-collision`, `no-len-method`,
`writes-a-mutable-constant`, `value-called-as-function` -- because each is a grammatical
or type fact; eight become a declared profile (`profile softanza`) the compiler enforces
when a unit declares it -- `engine-first`, `no-aggressive-verbs`, `library-prints`,
`dead-knob`, `setter-resets-on-reject`, `setter-only-moves-one-way`, `misspelled-name`,
`empty-method-body` -- because each is library policy, right for Softanza and wrong for a
script.* The line between the two is the author's to draw.

**D4 -- Named arguments and the `:Name = value` spelling.** F-59 stands for Ring++:
`:Name = value` is a two-element list, and Softanza spells about a thousand arguments
that way [R]. *Recommendation: in Haro the same spelling is a real named argument bound
at compile time (analysis 5.2's answer), and a Softanza method that today tests
`isList(p) and Q(p).IsXNamedParam()` declares its named parameters instead; the
migration is a census, and the two readings cannot both hold for one call.* This
touches the calling convention of the whole library and is not this session's to take.

**D5 -- The first spike's target and its number.** *Recommendation: the program and the
guard of section 7, with the 100 ms library-resident target and the grain-1 GBNF only.*
And the standing item the record already names: **the name** -- the Haro naming check
was pending on 2026-09-13 [R, softanza/memos/2026-09-13.md] and nothing here should seal
it.

Two further decisions the charter took and flags because they are large: the case rule
(H-2) and the value model. On the value model the charter follows `rnx`'s measured
answer -- assignment copies, a parameter is by reference (C-7) -- and adds Rust's lesson
in the smallest form the forms already carry: the active form may mutate, the passive
may not, and a *function* that mutates a list parameter says so in its definition. The
author may want that frame more explicit than this, or less.

---

## 9. What this costs, named

- **Softanza's migration surface** [M, all from the census and the record]: 160 Rule A
  sites (90 of them attributes without `@`); 136 `eval` sites in 44 files, which C-9 kept
  for the bridge and this charter drops for Haro; about 1,000 `:name = value` arguments
  whose reading D4 decides; 27,807 colon sites that keep working under D1; the 59% of
  public methods whose intent line is inferred, not written; every `for x in` loop
  (fixed silently); every `substr` (already banned by the house rules).
- **What Haro gives up on purpose**: typo tolerance in names; free spelling of
  constructs; free-order parameters; runtime reflection deepening (redirected to
  compile-time families, charter 4e.6); `eval`; the one-line `if cond : stmt`.
- **What it does not claim**: a speed. The shipped VM is in Luau's class and behind it;
  the toy edit-to-verdict is inside a scheduler tick on both runtimes; the
  library-resident number is a target until the spike measures it.
- **What it asks of the engine**: nothing new for the spike. Grain-3 grammars and
  streaming under a grammar are asks for later rungs, each with a cost to measure.
