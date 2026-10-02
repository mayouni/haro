# Haro -- the charter

**Status: v0.2 RATIFIED by the author, 2026-10-01** -- "Ratified, go with your
recommendations on D1 to D7" -- so every recommendation in section 13 is a ruling, marked
there. v0.1 was written 2026-09-26 (commit 7c772ee) by the `haro-charter` session; v0.2
answered the author's note of 2026-10-01 and the vision he published on the Softanza site
the same day. With ratification the brief's next step opens: the spike of section 10, built
under `haro/spike/` and measured; its record is `haro/SPIKE.md`. Nothing else is built. No
parser, no compiler, no VM change exists for Haro beyond the `rnx` VM and `rnxc` compiler
that run the platform's code today.

**What changed since v0.1, in the author's words (2026-10-01):** "Haro is actually a
language of languages as designed in the Ringua project. The idea is that the agentic makers
will define a language for their domain and start programming in it, or let their agents
(including Aicha, our Softanza agentic model and conversational agent) program in it. Haro
is also embracing the refinement-oriented paradigm developed in the Refine project and the
Refine book. It works hand in hand with the other stack of our technology, from Harobanda
OS to any application and any target platform." And on the site, read 2026-10-01: "Haro --
the language of languages: you declare the language of your own domain, and Haro runs it";
"one engine and one language covering twenty-eight areas"; the estate drawn as hardware,
Harobanda, Haro, Softanza, Aicha, applications, with Takamba beside.

**So v0.1's first decision is reversed by the author, and this charter records it as such.**
v0.1 chartered Haro as the general-purpose floor and left the family of declared languages to
stzu above it (its H-1 and H-9, its D1). The ruling is the other way round: Haro IS the
family's language. What v0.1 designed survives as one of Haro's three altitudes (section 6);
everything else is re-centred below.

**How to read it.** Every claim is **[M] measured** (a number, with file and date), **[R]
recorded** (a ruling, finding or correction in the estate's record, cited) or **[D] designed**
(this charter's proposal, reversible by name). A number without a source is a defect in this
document. The spelling of the intelligence layer's name follows the site (Aicha, with a
diaeresis), which is also the author's own correction of 2026-09-30 ("the product is Aicha,
not Aichat" [R, softanza/memos/2026-09-30-escep-launch.md 9-10]); his note of 2026-10-01
spells it with a circumflex, and he rules the spelling.

**The one sentence.** Haro is one language with three altitudes: in it a maker declares the
language of a world, an agent speaks that language under a grammar it cannot break, a human
governs what the world becomes, and every change to any of them is a refinement judged before
it lands; it runs on the `rnx` VM, from the declared machine to any application and any
target.

---

## 0. Provenance -- what this version stands on, beyond v0.1's list

- The author's note of 2026-10-01 and the site pages `stzsite/content/en/vision.md`,
  `agentic.md`, `platform.md`, `tour.md`, the journal, and `doc/LEARNING-FROM-WOLFRAM.md`.
- `ringua/README.md`, `docs/mission.md` (ratified 2026-08-06, amended 2026-08-10 and 14),
  `docs/design.md`, `docs/commons.md` (C6), `docs/exemplar-zql.md`.
- `softanza/vision/06-ALPHABET.md` (ratified 2026-09-27: the letters Z W Q F A N, the two
  venues, the totality doctrine, N's ink lines), `03-PRODUCTS.md`, `07-SYSTEM.md` (ratified
  2026-09-27 by delegation).
- `stz/declarative/stzu/GRAMMAR.md` (stzu v0.1), `harobanda/declarative/machine/
  machine.stzu` (79 lines, judged by the meta-court), `harobanda/README.md`,
  `harobase/README.md`.
- `refine/README.md`, `START_HERE.md`, `REFINE_INTRODUCTION.md`, `specs/REFINEMENT_
  CENTERED_PROGRAMMING_v3.md`, `docs/REFINE_RFN_LANGUAGE_v0_1.md`, `docs/THE_REFINEMENT_
  COMPILER_v1_0.md`, `specs/DECLARATIVE_FOUNDATIONS_FOR_REFINEMENT_v1_0.md`; the book
  `ayouni/BOOK.md`, `manuscript/rop-book.md`, `manuscript/rop-manifesto.md`;
  `stzlib/.../base/refine/stzRefinableCode.ring`.
- v0.1's own list: Ring++'s record, *Ring, Judged by the Record*, the Ring++ design charter,
  the kernel, the traps, LAW 3 and LAW 6, C2 v1.2.0, C9, the forms document.

Where a source and this charter disagree, the source is right and the disagreement is in
`haro/FINDINGS.md`.

---

## 1. Haro in one picture: three altitudes, one law

```
                 the human GOVERNS            the court JUDGES everything
                       |                              |
   DECLARING   def language tontine ...  Haro's meta-language: Ringua realised.
   altitude    a maker (or Aicha) declares a language: its grammar, its world,
               its questions, its refusals, its narration. The forge turns it
               into a court, a GBNF, a printer, a knowledge graph, a runtime.
                       |
   DECLARED    DEFINE ENTITY deposit ...  the maker's own language, in its jargon.
   altitude    Closed, total, judged. The agent speaks it under its GBNF. The
               estate's first six are the alphabet: Z W Q F A N. A machine
               (.machine) is one. A world (Z) is one. A course is one.
                       |
   COMPUTING   Q("ring").RemoveQ("x")...   the Softanza vocabulary on rnx: the
   altitude    expert venue, the 28 areas, where courts, forges and runtimes
               are themselves written. v0.1's design, kept whole.
                       |
   REFINEMENT  across all three: every named thing is a refinement point; every
               change is a typed, bounded, gated, attributed, reversible
               refinement; the compiler takes refinements as a source language.
                       |
   THE STACK   Harobanda (the declared machine) -- HaroBase (governed data) --
               stzApp/stzSuperApp worlds -- stzp projections (app, server,
               page, device, constellation) -- one static binary per language.
```

**The law across the altitudes** is the estate's own, unchanged: *everything is a
declaration; every declaration is judged; computation is the judged evaluation of declared
sentences over declared worlds; anything beyond passes through one governed door per level*
[R, 06-ALPHABET, "One computational model"].

**Why three altitudes and not one grammar.** The two-surface doctrine, RingFace's founding
decision imported by Ringua as its rule 4 and elevated by the alphabet to a product
principle: "the programmable, expressive layer lives on the designer's side; what ships is
always the closed plain-text artifact, re-judged. Programmability and closure never occupy
the same surface" [R, ringua/docs/mission.md 4; 06-ALPHABET, "The two venues"]. So Haro has
one *law* and three *surfaces*: a declared language's text can never contain computing-
altitude code (closure, Ringua contract 1), and computing code reaches a declared world only
through the doors the forge generates (Q, the API) -- never by evaluating text. v0.1's "one
grammar, one text" stands *within* each altitude; across them the doctrine forbids it, and
v0.1 was wrong to put the family outside the language.

---

## 2. Who makes, who speaks, who governs -- and what each is owed

v0.1 had a speaker and a reader. The ruling adds the maker, and makes the agent a speaker of
*declared* languages first and of the computing altitude only as an expert.

**The maker** (the site's first word: "someone who turns what they know about a world into
something that runs, without waiting for the software industry ... not defined by programming
skill but by ownership" [R, vision.md]) declares the language of a world -- its things, its
rules, its flows, its questions -- and programs in it, or lets an agent program in it. Owed:
that declaring a language is as easy as declaring a variable; that the declaration is plain
text the maker keeps; that the court judges it in the maker's own words; that the artefact
ships as one binary and expires never.

**The agent** -- Aicha, "the name the author gives to the Softanza language model and
conversational agent", the coming face of the neural tier (a local model through ggml,
structured output under C9, the semantic index) and of the agentic layer, a name and nothing
else yet [R, the site's estate page, "named"; softanza/memos/2026-09-30-escep-launch.md
128-134] -- or any agent under C9 -- speaks the declared language. Owed, as in v0.1: a grammar the decoder holds (now emitted by the forge
for every declared language, by construction); refusals that are instructions, in the
domain's jargon; verdicts in milliseconds; one spelling; the language's own tables. And one
thing more: **a write surface that is a refinement** -- "a typed proposal against a declared
point is the safest write surface you can hand an autonomous system: bounded, discoverable,
gate-validated, reversible, attributed" [R, rop-book.md 557]. The agent proposes; it never
commits [R, the estate's loop, agentic.md].

**The human governor** reads the declared world as sentences in its jargon, reads every run
as a narration, ratifies or refuses a refinement, and holds the capability to commit. Owed:
the Zui law's non-accusatory pathfinding in every refusal; the audit chain as a query ("who
decided this three years ago"); reversibility built into the data model, never layered on.

**The court** -- the forge's generated judge for each declared language, the compiler for the
computing altitude, the gate for every refinement -- is owed determinism and the C2 envelope.

---

## 3. The declaring altitude: Ringua, realised in Haro

**The lesson [R].** Ringua's mission: "allow anyone to design a domain language, give it a
knowledge base, and start using it -- a computable language, deployable on any platform as
one static binary ... the description of the application's world stops being imperative code
owned by programmers and becomes a declared, judged, auditable asset owned by the business"
[mission.md 3]. Its five contracts, each learned from a named industry failure: closed, plain
text, jargon-fluent both ways, judged, free-standing [README.md 27-33]. Its three strata:
syntax, knowledge-graph semantics, conversational pragmatics [mission.md 1]. Its status:
"blueprint and studies only; no code exists in this repository yet" [README.md]. And what
does exist: stzu v0.1, the meta-language in which W, ZQL and the machine language are
declared and judged today [R, stz/declarative/stzu/GRAMMAR.md; harobanda machine.stzu, "7
declarations, 5 forms, 0 expressions"].

**Haro [D]: stzu v0.1's grammar is Haro's declaring altitude, kept verbatim and grown.** Not
redesigned: the grammar is pinned, its fixtures are the judge, and the machine language and
W already conform to it. What Haro adds is what Ringua's three strata and the refinement
paradigm require and stzu v0.1 refuses by design (its "Refused, by design" names no logic,
no expression position, no escape):

| seat | stzu v0.1 | Haro's declaring altitude |
|---|---|---|
| `LANGUAGE`, `DECLARATION`, `FORM`, `EXPRESSION`, `REFUSAL` | the five meta-kinds | kept, with their menus, their meta-court and their refusal channel |
| `RATIONALE` on every declaration | mandatory (C6 3.8) | kept; it is principle 5 at this altitude |
| **`WORLD`** (the knowledge stratum) | absent | the ontology declared beside the grammar: entities, relations, constraints, as versioned data (C1, `world.json`); never a mutable runtime store [R, mission.md rule 3]. *Built in three slices: cardinality (v0.2), entry (v0.8), the C1 rows a sentence publishes and resolves against (v0.10, the tenth rung).* |
| **`ASK`** (the pragmatics stratum) | absent | the language's own closed query grammar (the Q letter) and the human languages its natural door speaks; NL asks, never declares; the engine compiles to this grammar and never to host code [R, mission.md rules 1-2]. *The query grammar is built, v0.7 (the seventh rung); the natural door is not.* |
| **`NARRATE`** | absent | how a run of the language is narrated back (stzn); the court's voice |
| **`REFINE`** | absent | which declared points of a sentence may be refined, by whom, within what bounds, at what trust floor (section 7) |
| **`FORMS` inside a vocabulary** | absent | the function-name grammar of principle 7 declared as data for the computing altitude's families |

**Built 2026-10-01, the first slice of two of these rows -- Haro v0.2, the spike's second
rung (`haro/spike/v02/GRAMMAR.md`, 30 fixtures, `haro/SPIKE.md`).** `WORLD` as cardinality
(`ONE`, `FIRST`), the typed seats a knowledge stratum needs before it needs an ontology
(`MENU`, `RANGE`, `FORMAT`, a seat typed by another declaration, `NAMES`), and `CONSTRAINT`
with a closed, total condition language over one declaration and the `ONE` kinds; `REFINE`
as `POINTS` (which seats, of which kind) and `FLOOR` (at what trust posture). The ontology
as versioned data, `ASK`, `NARRATE` and `FORMS` are not built. Measured on the machine
language: 95 of `harb`'s 120 fixtures agree with a court forged from the v0.2 declaration,
against 41 from v0.1. **Haro v0.3, the same night (`haro/spike/v03/GRAMMAR.md`, 27
fixtures):** a `UNION` seat whose value has one of two shapes, a declaration's `MESSAGES`
for its reference seats, and a condition language that reads through a reference,
quantifies over a kind or a list of references, and tests five closed relations (an
address within a prefix, its host, a path under a directory, a perimeter covering every
address, a cycle through references) -- each total, each a fixed line of the court, none
a computation the declaration writes, so the totality doctrine holds. 117 of 120; the
three left are the fleet file's kinds, another language's. **Haro v0.4, 2026-10-02
(`haro/spike/v04/GRAMMAR.md`, 23 fixtures): a language over a language.** A `SENTENCE`
seat names a file of another declared language, judged by that language's own court; a
`VIEW` is a derived place by a closed rule; a condition's places are paths through
sentences and views. The fleet language declared over the machine language
(`fleet_v04.haro`) forges one court carrying both records, and it agrees with `harb` on
32 of 32 -- this section's "composition is the normal way to declare a language", measured.
**Haro v0.5, the same day (`haro/spike/v05/GRAMMAR.md`, 7 fixtures): an expression
language forged whole.** `CONTEXTS` on an `EXPRESSION` says which seat admits which
variables; W, the alphabet's W letter, declared by its own grammar text (`w_v05.haro`),
is forged into its court AND its evaluator and its grammar for the decoder, and passes
stz's 29 fixtures unadapted on `rnxc` and the oracle. The forge is measured on two
shapes of language: sentences of `DEFINE`s, and an expression. **Haro v0.6, the same day
(`haro/spike/v06/GRAMMAR.md`, 14 fixtures): a WORLD forged whole, court and runtime.** A
list of a FORM that is a name and a scalar written as pairs; an EXPRESSION's `ABSENT`,
`DIVISION` and `EQUALITY` declared, so two correct evaluators of one grammar stop
disagreeing in silence; and `WALK`, the one kinetic declaration -- which kind is walked,
by which steps, in what order, under which guards, computing what, failing how. Z, the
alphabet's Z letter, declared in the Commons' shape (`z_v06.haro`) and zing's 16 tontine
cases judged on the forged court and walker unadapted: 16 of 16 on `rnxc` and the oracle.
This is section 7's "the forge produces the runtime" with its first number, and the
`WORLD` row above has its second slice: the declared world's norms and flows RUN. The
notation gap between ZQL v0 and the Commons is HF-47 and the author's (D8). **Haro v0.7,
the same day (`haro/spike/v07/GRAMMAR.md`, 12 fixtures): the Q letter.** `ASK` -- the row
above, "the language's own closed query grammar" -- says FROM which kinds a question may
be asked, WHERE in which expression, and which clauses it admits; the forge emits the
question grammar and the court's `ask` verb, and the judge is zing itself: its own
answers to 25 questions on its bedrock-query example, re-taken live by the guard, 25 of
25 on `rnxc` and the oracle. The natural door of the same row -- N -- is not built.
**Haro v0.8, the same day (`haro/spike/v08/GRAMMAR.md`, 13 fixtures): the F letter.** RingFlex's
`.wflow` v0 -- the FLOW OF WORK, a shipped normative grammar with its own court and fixture
suite -- declared in the Commons' shape (`f_v08.haro`): a step is one of six kinds, an arrow a
reference into a UNION of declarations, a deadline a FORMAT, an escalation's actions a
MENU-keyed sequence, a routing's branches GUARD-keyed pairs, and its fifteen court rules
seats, messages and three closed relations (`reachable`, `referenced`, `keyed_by`); no
expression, by design. 26 of 26 of RingFlex's fixtures and reference workflows, re-expressed,
on `rnxc` and the oracle, with RingFlex's own court holding the same expectations beside it.
Four letters of the alphabet are forged from declarations now: Z, W, Q, F. **Haro v0.9,
the same day (`haro/spike/v09/GRAMMAR.md`, 10 fixtures): the A letter.** `RUN` -- which
kind of a language runs and which kinds play COMPUTE, COLLECT, GROUP, BRANCH and ITERATE,
each with its seats by role -- and a list seat of a UNION of declarations; `a_v09.haro`
declares the ALGORITHM, the one letter with no shipped ancestor, from its three named
sources, and the forge emits its runner: ITERATE over a snapshot of a declared collection,
a step tree that re-enters itself refused at check -- the totality doctrine of section 3,
structural. Judged by stz's 29 W cases and zing's formula cases re-expressed as algorithms
(35 of 35 on `rnxc` and the oracle), because A has no suite of its own. Five letters of
six are forged: Z, W, Q, F, A; N waits on the ringua Phase 1.5 study, the author's gate.
**Haro v0.10, the same day (`haro/spike/v10/GRAMMAR.md`, 7 fixtures): the WORLD as versioned
data.** The `WORLD` row above, past cardinality and entry: `SYMBOL`, a seat resolved against a
C1 `world.json` when the court is handed one, and `PUBLISH`, the kinds a sentence contributes
as symbols. Z publishes its flows, entities, norms and zones; F resolves INVOKES and
COMPENSATED_BY through a `flow` symbol and publishes one `process` -- the placement contract's
C3 3.2, in the declaring altitude, judged by RingFlex's own placement gate and by the seam
between the two forged letters, nine of nine on `rnxc` and the oracle. The world is emitted
and resolved, never stored, as the row says.
**Haro v0.11, the same day (`haro/spike/v11/GRAMMAR.md`, 7 fixtures): the Diagnostic
Contract.** What section 5 says every court owes: `CODE`, `CODES` and `CITES` declared beside
the words, and every forged court answering `diagnose <file> [world]` in C2 v1.2.0's one
object of six-field envelopes -- a refusal one error with its element's code and cites, no
world one warning at line 0, a clean sentence an empty array. F declares RingFlex's own codes;
judged against the contract's shape and against RingFlex's court live, 28 of 28, first run.

**What the forge produces from one declaration** (Ringua's kit, 02-STACK's L1, now Haro's
compiler verbs rather than separate organs): the parser; the court with the fixtures as its
constitution and the runner as its drift alarm; the canonical printer (the round-trip
fixpoint of contract 2); the GBNF, so an agent is sampler-constrained to valid sentences (C9);
the knowledge graph on the engine's substrate; the query grammar and the natural door; the
narration; and the runtime on `rnx`, shippable as **one static binary per language**
(Ringua's fifth property, which is Ring++'s commitment 5 in another register: `rnxc` plus the
image is that binary).

**The alphabet is the estate's first six declared languages, and composition is the normal
way to declare one.** Z declares the world, W constrains it, Q asks it, F moves it, A steps it,
N speaks to it [R, 06-ALPHABET, ratified 2026-09-27]. A maker's domain language -- the tontine,
a shop, a clinic, a machine -- is a vocabulary over those letters: its entities and norms in
Z, its conditions in W, its flows in F, its questions in Q, its conversation in N. "Declaring
a language is as easy as declaring a variable" means exactly this: the letters are the types
and the maker's declaration is the value. One vocabulary registry, every word belonging to
one letter [R, 06-ALPHABET, execution route 4].

**The totality doctrine is kept, and it is the point.** The declared altitude is deliberately
not Turing-complete: W's evaluator is total; F has no expression production; A iterates over
declared collections only, so no unbounded loop is expressible [R, 06-ALPHABET, "The totality
doctrine"]. An agent constrained to it has "expressive power without the pathology:
malformedness dies at the sampler, falsehood dies at the court, and non-termination is
unexpressible". Computation that needs the halting problem passes through one governed door
to the computing altitude -- and that door is itself declared (an `A` step naming a
computing-altitude verb, with its capability).

---

## 4. The declared altitude: a sentence in your own language

A declared language's sentence is what the maker writes and what the agent emits. It is
closed (unknown verbs are unparseable, "destructive or unrecognized operations are not part
of the grammar" [R, stzzql/GRAMMAR.md 15-16]), plain text in the Commons' lexical form (C6:
`--` comments, double-quoted strings, UPPER_SNAKE keywords, `lower_snake` identifiers,
case-sensitive, UTF-8, LF or CRLF never diagnosed), judged by its court in its own jargon
("mydsl (line N): the money received must cover the total" [R, ringua/docs/design.md 24]),
and spoken by the agent under the GBNF the forge emitted for it.

What a sentence can do: declare (Z), constrain (W), ask (Q), move (F), step (A), converse
(N). What it cannot do: call host code, evaluate text, loop without bound, mutate a store at
run time. Where it lives: a file the maker keeps; the machine's `/etc/machine`; a world's
`.zknw`; a course; a fleet. How it reaches people: stzp's five projections (section 8).

**The eight principles at this altitude** are mostly consequences of the five contracts
(section 11's table); two deserve the sentence: *no silent global* becomes "a dangling
reference is a check failure with a jargon phrase, not a runtime surprise" [R, commons.md
5.2, exemplar gap G6]; *refuse, then explain* becomes "what a language says when it refuses is
declared beside its grammar, not authored per runtime" [R, stzu GRAMMAR.md, DEFINE REFUSAL].

---

## 5. The computing altitude: v0.1, kept whole as the expert venue

v0.1's design -- the Softanza vocabulary as the canonical text, forms as grammar, the intent
clause, Rule A's sigils, no `eval`, the C2 error, the GBNF at three grains, the corrections
C-1..C-20 carried or dropped by name -- is this altitude, and `haro/PRINCIPLES.md` carries it
in full. What the ruling changes about it:

- **It is the expert venue, not the product.** "The default venue is the product. The expert
  venue is the honesty about what the product stands on" [R, 06-ALPHABET]. The 28 areas of
  the engine, the courts, the forges, the runtimes and the projections are written here;
  a maker reaches it through one governed door, never by default.
- **Its surface today is the Ring-shaped one `rnxc` compiles.** The site labels that code
  "Softanza" and says "every code block on this site is Softanza code as it runs on the
  platform today" [R, platform.md]. The 531,012 lines of library and the 306,302 lines of
  tests [M, stzsite journal, 0e72e2e2c] are its compatibility specification. v0.1's rules
  land on it as **profiles** (P1: relaxations declared, never silent), each a refinement of
  the library judged by the wide suite [M, 3,231 of 5,112 programs agree with the oracle on
  every stable line; Ring++ passes 8,501 of Ring's 8,507 assertions, ringpp CLAUDE.md
  2026-09-30].
- **Its families are declared.** The forms (`Verb`, `Verbed`, `VerbQ`, `CS`, `ST`, `W`, `X`,
  `Many`, `Except`...) are the computing altitude's own closed vocabulary, declared at the
  declaring altitude (`FORMS`) and generated by the compiler, which is the compile-time
  metaprogramming the Ring++ charter asked for [R, 4e.6] and the 10,600 hand-typed spelling
  variants it retires [M, analysis 5.3].

---

## 6. Refinement: the change model at every altitude

**The lesson [R].** "AI removed the bottleneck on producing code and created a new one:
trusting code -- yours or an agent's -- that arrives faster than anyone can review" [refine/
README.md 3-5]. "Stop trying to govern the intelligence, and govern the change" [rop-book.md
93]. "A refinement is a typed, bounded change to a declared point in a system, validated
against declared rules before it lands, attributed to its author, aware of everything it
affects, and reversible by construction" [rop-book.md 205]. "The declarative approach makes
the declaration itself the refinement surface. There is no separate annotation layer ...
Every named thing is a candidate refinement point. The boundaries are not author-chosen;
they are language-required" [DECLARATIVE_FOUNDATIONS 32, 64]. "A refinement compiler takes
a stream of refinements as its source language" [THE_REFINEMENT_COMPILER 18]. "The rules
themselves are refinable ... graphs all the way down, and one gate over all of it"
[rop-book.md 677]. At the floor: "a change to a machine is a refinement -- the two slots
exist so that an update is a trial before it is a commitment, which is refine's gate at the
floor" [07-SYSTEM].

**Haro [D].**

1. **Every named thing is a refinement point, by the language.** Not an annotation in a
   comment: `<R:PARAM name="vat" ...>` in a comment is the *lift* for foreign code (the
   language-agnostic form stzlib carries today [R, stzRefinableCode.ring 410]); in Haro a
   declaration *is* its point. A `DEFINE NORM` is a policy point; a seat's value is a
   parameter point; an `A` step's verb is an algorithm point; a `FORM` is a composite point;
   a `LANGUAGE`'s `GRAMMAR` version is a point whose cascade is its fixtures and its
   consumers' pins. The kinds are Refine's eight (parameter, block, algorithm, function,
   pipeline, variable type, library, custom [R, RCP v3 71-80]) at the computing altitude and
   the book's six (knob, field, symbol, policy, composite, pipeline [R, rop-manifesto 277])
   at the declared one -- the two taxonomies are a finding (HF-20), and the author picks one
   name per kind.
2. **A refinement is a sentence of Haro.** Its required fields are RFN's: `target`, `from`,
   `to`, `author`, `reason`; optional `policy`, `cascade` (stated, it becomes an assertion),
   `gates`, `reverts` [R, REFINE_RFN_LANGUAGE 97-120]. RFN "does not compute: no loops, no
   conditionals against runtime state, no I/O" [R, 599] -- so it is a declared language of
   the alphabet's kind, total by construction, and its GBNF is the agent's write surface.
3. **The compiler takes refinements as a second source language.** `haro refine <file>` is
   as first-class as `haro run <file>`: the diff is a derived view, the cascade the primary
   one [R, START_HERE 18-21].
4. **The gate is one gate over all altitudes**, with the structural stage "delegated back to
   the language itself" [R, rop-book.md 687] -- the declared language's own court, or the
   computing altitude's compiler -- then constraint (bounds), derivation (the declared
   rules), governance (who may turn which knob, risk tier and reversibility class as two
   axes [R, agentic.md]), and trust posture (a point may declare a trust floor; `policy/*`
   refuses model-composed proposals "not by convention, by construction" [R, rop-book.md
   565]). The record disagrees on whether this is four or five stages (HF-19); the five of
   `stzRefinableCode.ring` are the ones that run today, and this charter names five.
5. **Reversibility is in the data model**: the inverse is computed before the refinement
   lands; a revert is its own event; nothing is erased [R, RCP v3 94-96]. The audit chain --
   author, authority, rule, verdict -- is a by-product [R, REFINE_INTRODUCTION 29].
6. **v0.1's "scoped hole" is the refinement point's grammar.** v0.1 asked for a GBNF of a
   hole with the names in scope inlined, so an agent's edit is grammatical by construction.
   A hole is a point; the names in scope are the point's bounds; grain 3 is the refinement
   grammar. One mechanism, not two: the agent never edits text, it proposes a refinement
   against a point, under that point's GBNF.
7. **A refinement of a language is a refinement.** Bumping `GRAMMAR "0.1"` to `"0.2"` is a
   typed change whose cascade is every fixture and every consumer pinned by hash (stzzql's
   discipline: "a pinned copy that drifts from its recorded sha256 is a finding" [R,
   stzzql/README.md 24-27]); the gate runs the court; the consumers re-pin. This is how a
   maker's language evolves without a maker's world breaking silently.

**What it costs.** Every declaration carries its kind and bounds, which the Commons' form
already carries for the most part (seats are typed; `RATIONALE` is mandatory). The gate's
five stages run on every change; today's stzlib gate judges a refinement in milliseconds
[M, gate_deepening_narrated, 40 lines byte-identical on both runtimes]. The cost that is new
is authorship: trust floors and risk tiers declared per point, which a profile can default.

---

## 7. The stack: hand in hand, from the declared machine to any target

| member | what it is (stage, as the site reads it 2026-10-01) | its relation to Haro |
|---|---|---|
| **Harobanda** | the declared machine: one text file boots exactly that and judges every boot; Linux pinned beneath, PID 1 the one binary, no shell, no login (built, MIT) [R] | its language, `.machine`, is declared in stzu v0.1 -- 79 lines, 7 declarations, 5 forms, 0 expressions, 54 fixtures [R, machine.stzu; 07-SYSTEM] -- so it is Haro's first customer at the declaring altitude; a machine update through two slots is a refinement; the image's boot path holds exactly two binaries, `harb` and `stzr`, and the worlds are Luau under `stzr` today (four reference machines); Harobanda's own record names the successor: "the runtime: stzr today, Ring++ and Haro tomorrow ... ship as the image's second binary. Status: real for stzr. For Haro, by design: one path in `experiment/os2_image.sh` and one SERVICE word" [R, harobanda/doc/DIVIDEND.md 179-232, seam 12]; the Haro tool names (HaroServ, HaroScript, MicroHaro) stand today for RingServ, RingScript and MicroRing at those tools' own stated levels [R, PROVENANCE.md, STZ-OS-RULING-10]; `rnx` appears nowhere in the repository yet |
| **HaroBase** | the governed data store: SQLite in the process, governed, a Zig library with a C ABI, no Ring inside (specification; HB1 and HB2 built) [R, harobase/README.md] | the data refinement domain's store; a world's records persist through it; "shared by every face of the estate (Haro, Zin, and Softanza's engine while Ring lasts)" [R]; its charter already names the seam: "Haro writes its binding against the C ABI when its charter is ratified and its runtime exists. Until then, HaroBase owes Haro one thing: that the C ABI does not change shape after HB1 without a version bump" [R, harobase/CHARTER.md 9.3] |
| **the worlds** | stzApp ("an application is a living world of meaning"), stzSuperApp ("a living constellation of worlds") [R, 02-STACK L3] | declared in the alphabet; governed by Z's norms and Zui's constitution; refined through the gate |
| **the projections** | stzp: app, server/service, edge/browser via wasm, device, constellation [R, 03-PRODUCTS] | one Haro world, five targets; one static binary per language (contract 5 = commitment 5) |
| **Zin** | the constitutional federation: 56 pillars under a compile-time constitution; ZML the meta-language behind its pillar DSLs; ZinScript its scripting language (built, commercial) [R] | ZML and Haro's declaring altitude elevate losslessly by construction (the stzu-to-ZML table [R, stzu GRAMMAR.md]); "ZinScript may stay close to Zin or embrace Haro" is Zin's call [R, stz/CLAUDE.md, author 2026-09-13]; the convergence point is refine's gate enforcing zin's constitution [R, 03-PRODUCTS] |
| **Refine** | refinement-oriented programming: a corpus of over a hundred specifications, a prototype, the first module of a Zig engine, a book in manuscript (specification) [R] | section 6 is Refine's paradigm made the language's own; Refine the product is the governed-change environment over it |
| **Aicha** | the coming intelligence layer, language model and conversational agent: knowledge, models and agents on your own device, "bound by the rule that a model proposes and never commits" (named, and nothing else yet) [R, the site's estate page; escep-launch memo 2026-09-30]; not the Aicha of Refine's Sonibank pilot, who is a persona, a compliance officer in Niamey [R, refine/SONIBANK_PILOT_v0_1.md 34] | the speaker of declared languages: it drafts sentences of Z/W/Q/F/A through the closed compile target (N's governed middle [R, 06-ALPHABET]), proposes refinements against declared points, and holds no `effectful` capability [R, agentic.md, 610 deletions proposed and none committed]; built on the natural plane, the neural plane under C9, `.pia` declarations judged at load, and the knowledge graph |
| **Takamba** | the harness, formerly Bangalo: many sessions on one body of work with a directory and git; laws cited to incidents (built) [R] | how Haro is built; its refinement discipline is law 1 made structural, which "IS the audit chain" [R, 03-PRODUCTS] |
| **Luau** | stz's script host today, "Luau-first, Ring-still" [R, stz/README.md] | hosts stzr and the four reference machines' worlds; the meta-court that judges `.stzu` files runs in Luau today (`face/stz/Stzu.luau`) [R, machine.stzu header]; the spike (section 10) re-judges with `rnx`; convergence is the author's ruling at the critical point [R, 01-KERNEL] |
| **Softanza, the library** | the foundation, built: 531K lines, the Zig engine, 501 narrated guards [M, site] | the computing altitude's compatibility specification, and the engine behind every altitude (graphs, text, the decoder, the natural plane) |

---

## 8. The grammar contract, extended to the declaring altitude

v0.1's contract stands for the computing altitude (one grammar source; parser, GBNF and
editor grammar generated from it; the gate proving them equal on fixtures; three grains). The
ruling adds:

- **Every declared language emits its GBNF by construction**, because the forge emits it
  from the declaration; a language without a grammar for the sampler is not a Haro
  language. This is the kernel's promise ("every declared grammar also emits its GBNF" [R,
  01-KERNEL]) made structural, and it closes HF-8: today no surface but C9's schemas emits
  one.
- **The declaring altitude has its own GBNF** (stzu v0.1's grammar is EBNF already [R,
  GRAMMAR.md]), so Aicha can draft a *language*, not only a sentence -- a draft the
  meta-court judges and the human ratifies, under N's ink lines.
- **The refinement grammar** per point is grain 3 (section 6.6).
- **C9's mechanics and limits** are v0.1's: `StzGenerateXT(prompt, [:Grammar = g])`,
  `sampleIdConstrained`, `stz_grammar_can_end`, the honest `StzEngineGbnfDecodingSupported`;
  non-ASCII in a character class is unsupported by the machine, so identifiers are ASCII and
  strings go through byte ranges [R, gbnf_machine.zig 40-47]; and the amendment travels with
  every claim: *structure kills malformedness, not falsehood* (C9 clause 8).

---

## 9. The error, at every altitude

v0.1's record stands: a C2 v1.2.0 envelope (`code`, `severity`, `message`, `span`, `cites`,
`language`) with `why`, `todo` and `frames` as the extensions C2 permits [R, diagnostic-
contract.schema.json, no bare booleans]. The ruling adds two things:

- **The refusal's phrasing is declared beside the grammar, in the domain's jargon and human
  language** (`DEFINE REFUSAL ... MESSAGE`), so the `message` an agent or a maker reads is the
  maker's own sentence, and "a host stack trace reaching the domain expert is a defect"
  [R, ringua/README.md 31]. The `language` field names the declared language, not "haro".
- **A gate's refusal names its stage** -- structural, constraint, derivation, governance,
  trust -- as `stzRefinableCode.ring` does today ("constraint: 0.30 above max 0.25";
  "trust: posture :llm below the required floor for 'vat'" [R, lines 257, 278]), and carries
  the book's four parts: what happened, why, what to do next, where to learn more [R,
  rop-book.md 364]. `todo` is the third part; `cites` the fourth.

v0.1's three examples (the constant clobber, the case collision, the colon that builds a
list) stand for the computing altitude. One example for the declared altitude, from the
machine language as it refuses today: a service written as a shell line is refused by the
grammar, "a service is an argv, never a shell line" [R, machine.stzu, FORM word]; the court
says so in that sentence, with the line.

---

## 10. The spike -- the forge's first act on `rnx`

**BUILT 2026-10-01, the day of ratification, and measured: `haro/SPIKE.md` is the record,
`python haro/spike/haro_forge.py` the guard (six stages, PASS, 52 s; `--plant` makes it
fail).** The numbers that matter: the meta-court passes its 28 fixtures on `rnxc` and on the
oracle, byte-identical; the forge is byte-identical on both; the forged court agrees with
`harb` on 30 of 120 machine fixtures from the pinned declaration and 41 from one brought up
to date, with 0 defects, and the 70 rules a court carries that its declaration cannot are
counted and named (the `WORLD` and `REFINE` seats' size on a real language); 200
derivations of the forged grammar all parse and the engine's decoder holds it; a
refinement is refused at the trust floor as `:llm` with a C2 record, admitted as
`:trusted`, and reverted byte for byte; edit to verdict is 14.9 ms on `rnxc` with the
court's image (33.5 ms without; `harb` 12.0; the oracle 27.4). One correction to the plan
below: the machine language has **120** fixtures, not 54 (HF-34). The plan stands as
written, as the record of what was asked.

**The second rung, the same day, at the author's word ("Go for the WORLD and REFINE
seats, fixtures first"): Haro v0.2** (`haro/spike/v02/`, 30 fixtures, then the prose;
section 3's note). The machine language re-declared in it (`machine_v02.haro`) forges a
court that agrees with `harb` on **95 of 120** (14 computations beyond a declaration, 9
the union and fleet kinds, 2 fragments, 0 defects), byte-identical on `rnxc` and the
oracle; the refinement gate reads the declared `POINTS` and `FLOOR` (eight rows); 200
derivations all parse and the decoder holds the grammar; edit to verdict 13.9 ms with the
image (45.3 without; `harb` 9.3; the oracle 44.9). The oracle found the rung's one defect
and it was Ring's (HF-36). Record: `haro/SPIKE.md`, "The second rung".

**The third rung, 2026-10-01, at the author's word ("Go for v0.3, fixtures first"): stzu
v0.3** (section 3's note). The machine language re-declared in it forges a court that
agrees with `harb` on **117 of 120** (0 beyond, 0 fragments, 0 defects; the three left are
the fleet file's kinds), byte-identical on `rnxc` and the oracle; edit to verdict 24.6 ms
with the image (68.1 without; `harb` 11.5; the oracle 77.1), under the target and named
as the cost of 62 constraints with quantifiers. The guard gained a pinned floor after its
own measuring class absorbed a court that had lost its constraints (HF-39). Record:
`haro/SPIKE.md`, "The third rung".

**The fourth rung, 2026-10-02, decided on the author's behalf ("decide on what is next on
my behalf"): Haro v0.4, the fleet language declared OVER the machine language** (section
3's note). One court, two languages' records, judged against `harb`'s 32 fleet fixtures as
the guard's stage 7: **32 of 32**, 0 defects, byte-identical on `rnxc` and the oracle,
pinned at 32; 102.8 s a pass. The composition claim of section 3 has its number (HF-41).
Record: `haro/SPIKE.md`, "The fourth rung".

**The fifth rung, 2026-10-02, on the author's "next": Haro v0.5, W forged whole** (section
3's note). An expression language -- the second shape the estate declares -- declared in
Haro and forged into its court, its evaluator and its grammar: **29 of 29** of stz's W
fixtures unadapted, byte-identical on `rnxc` and the oracle, the guard's stage 8, pinned
at 29; 200 derivations of the emitted grammar all sentences to the court. Z is named and
not taken: 06-ALPHABET's route 3 needs a runtime for a declared world, the
computing-altitude bridge, and is the author's to open (HF-45). Record: `haro/SPIKE.md`,
"The fifth rung".

**The sixth rung, 2026-10-02, on the author's delegation: Haro v0.6, Z forged whole**
(section 3's note). The computing-altitude bridge opened as route 3 words it: Z
re-expressed in the Commons' shape, its court AND its runtime (`eval`, `walk`) emitted by
the forge from `z_v06.haro`, and zing's 16 tontine cases judged unadapted on
`tontine.z`: **16 of 16**, byte-identical on `rnxc` and the oracle, the guard's stage 9,
pinned at 16, first run. Three findings: the notation gap (HF-47, D8), the pinned judge
narrowing a new rule (HF-48), the guard catching a 20 ms regression the rung would have
shipped (HF-49). Record: `haro/SPIKE.md`, "The sixth rung".

**The seventh rung, 2026-10-02, on the author's "then next": Haro v0.7, the Q letter**
(section 3's note). `ASK` forged into the question grammar and the court's `ask` verb,
and judged by a RUNTIME: zing's own answers to 25 questions on its bedrock-query example,
captured into the fixture and re-taken live by the guard's stage 10 -- **25 of 25** on
`rnxc` and the oracle, byte-identical, pinned. Three findings: `ABSENT missing` (HF-50),
zing's unresolved FROM (HF-51), and Ring's after-the-index `insert()` that had left the
walk's ordering untested (HF-52). Record: `haro/SPIKE.md`, "The seventh rung".

**The eighth rung, 2026-10-02, on the author's "next": Haro v0.8, F re-declared** (section
3's note). RingFlex's workflow grammar in the Commons' shape, forged into its court, and
judged by RingFlex's own fixture suite re-expressed -- 24 one-defect workflows and two
reference workflows, each with its expected verdict: **26 of 26** on `rnxc` and the oracle,
byte-identical, first run, pinned; RingFlex's court 26 of 26 on the originals under official
Ring. v0.8 grew by what F needs (NAMED refusals, keyed pairs, a UNION of declarations,
deadlines, ENTRY, three relations) and reversed two earlier fixtures out loud (HF-55).
Record: `haro/SPIKE.md`, "The eighth rung".

**The ninth rung, 2026-10-02, on the author's "next": Haro v0.9, the A letter** (section
3's note). The ALGORITHM declared from its three named sources and forged into a court and
a runner that stops by construction; judged by stz's and zing's own numbers re-expressed
as algorithms: **35 of 35** on `rnxc` and the oracle, byte-identical, first run, pinned; a
cyclic step tree refused at check. Three findings: an edit script's tolerance that
duplicated two blocks across two commits (HF-57), the judge made from other repositories'
numbers (HF-58), a list of a union judged by scalar shapes (HF-59). Five letters of six
are forged. Record: `haro/SPIKE.md`, "The ninth rung".

**The tenth rung, 2026-10-02, on the author's delegation: Haro v0.10, the WORLD as versioned
data** (section 3's note). SYMBOL and PUBLISH; the court's `check <file> [world.json]` and
`world <file>`; the placement contract's C3 3.2 judged by RingFlex's own placement gate on its
world fixtures and by the seam between Z and F -- **nine of nine** on `rnxc` and the oracle,
first run; RingFlex's gate 44 of 44 beside it (HF-60). D9 ruled on the delegation: A lives in
stz beside W. Record: `haro/SPIKE.md`, "The tenth rung".

**The eleventh rung, 2026-10-02, on the author's second delegation: Haro v0.11, the Diagnostic
Contract** (section 3's note, section 5's channel). CODE, CODES and CITES; every forged court's
`diagnose`; `f_v11.haro` carrying RingFlex's codes -- judged by the contract's shape and by
RingFlex's court run live on its originals: **28 of 28** codes, cites and severities the same,
first run, the same bytes on `rnxc` and the oracle (HF-61). Record: `haro/SPIKE.md`, "The
eleventh rung".

v0.1's spike (`twice.haro`, a definition with an intent clause) proved one altitude. The
ruling asks for three to meet, and the estate has already named the smallest program that
makes them: the alphabet's own proof obligation, "Z re-expressed through stzf from `z.stzu`
must pass zing's 16 fixtures unadapted" [R, 06-ALPHABET, execution route 3], and the machine
language that already conforms to stzu v0.1 and runs a real stack.

**The program.** `harobanda/declarative/machine/machine.stzu` (79 lines) read by a Haro
front end in `rnxc` as a declaring-altitude file; the forge generates the machine language's
court as a computing-altitude program on `rnx`; that court judges `machines/makeen_box.machine`
and the 54 fixtures in `fixtures.json`.

**What the spike builds, and nothing more:**

1. a reader for stzu v0.1's grammar in `rnxc` (`rnxc haro <file.haro>`), judged by the
   meta-court's own fixtures (`stz/declarative/stzu/fixtures.json`) -- the verdicts must match
   the Luau meta-court's on every fixture;
2. the forge's smallest act: from the declaration, a generated court (tokenizer, parser,
   checks, refusal channel) for the declared language, compiled to `rnx` bytecode;
3. that court judging the machine language's 54 fixtures with the same verdicts, and the
   same refusal fragments, as `harb check` gives today;
4. the GBNF of the machine language, emitted by the forge and accepted by `gbnf_machine.zig`;
   `makeen_box.machine` accepted by `StzGrammarAccepts`;
5. one refinement through the gate: a `SERVICE` clause's `RESTART` value changed by a
   refinement sentence, admitted at the structural and constraint stages, refused at the
   trust stage when posed as `:llm` against a floor of `:trusted`, and reverted;
6. the guard.

**The guard**, `bench/haro_forge.py`, born standalone and folded into `gate.py` only when
green, made to fail before it is trusted:

- the two meta-courts (Luau's, `rnx`'s) agree on every stzu fixture; the two machine courts
  (`harb check`, the forged one) agree on all 54, verdict and fragment;
- edit-to-verdict: minima of 15 of judging `makeen_box.machine` through the forged court on
  `rnx`, against `harb check`; target **under 100 ms** -- a target until measured, and the
  record says v0.1's toy measurement was inside one scheduler tick on both runtimes [M,
  HF-10];
- 200 derivations from the machine language's GBNF all parse under the forged court; the
  reject fixtures are refused by court and machine alike;
- the refinement fixture pins the C2 record of the trust refusal and the revert.

**Not in the spike**: `WORLD`, `ASK`, `NARRATE` seats; the alphabet beyond what the machine
language uses; Aicha; a Haro world booting on Harobanda; the computing altitude's profiles.
Each is a later rung with its own guard.

---

## 11. The principles, re-answered at three altitudes

v0.1's eight, each kept, and three the ruling adds. The full text of each is in
`haro/PRINCIPLES.md`.

| # | principle | declaring | declared | computing |
|---|---|---|---|---|
| 1 | no silent global | a language's names are its declarations; one namespace, duplicates refused (stzu check 3) | a dangling reference is a check failure in jargon (G6) | v0.1: literals, `$`/`@`/bare, no upward resolution, shadowing refused |
| 2 | one obvious spelling | the Commons' lexical form (C6), one | the Commons' form, one spelling per verb, the vocabulary registry | v0.1: Rule C, case decided, keywords reserved |
| 3 | grammar the decoder holds | stzu's EBNF emitted as GBNF | emitted by the forge for every language, by construction | v0.1: one source, three grains |
| 4 | refuse, then explain | the meta-court's channel, C2 | refusal phrasing declared beside the grammar, in jargon | v0.1: C2 + why/todo/frames; v0.11: every forged court's `diagnose`, its codes and cites declared beside the words (CODE, CODES, CITES) |
| 5 | self-describing | `RATIONALE` mandatory (C6 3.8) | `explain` on every declaration (Ringua's CLI contract) | v0.1: the intent clause |
| 6 | cheap to be wrong | the meta-court in ms | a total language terminates; the court judges in ms | v0.1: compile-time verdicts, the library resident |
| 7 | forms as execution modes | `FORMS` declared as data | closed verb sets, one word per letter | v0.1: the forms as grammar, families from a rule |
| 8 | humans read; agents write | **amended again**: the default venue is declarative and natural; N drafts, the court judges, the human ratifies | the agent's sentence is the human's sentence | the expert venue, one governed door |
| 9 | **declaring a language is as easy as declaring a variable** | the founding act is first-class: a language is a value with a version, a court, a grammar; composition over the alphabet is the normal way | | |
| 10 | **every change is a refinement** | a grammar version is a point with its fixtures as cascade | every named thing is a point; the refinement is the agent's write surface | profiles are refinements of the library |
| 11 | **total by default** | | not Turing-complete: W total, F expression-free, A bounded; non-termination unexpressible | computation reached through one declared door |

---

## 12. Carry, leave, decide -- updated

**Carried**, beyond v0.1's list: stzu v0.1's grammar, menus, meta-court and fixtures,
verbatim; the Grammar Commons C6 as the one lexical form of every declared language; the
alphabet Z W Q F A N as ratified; the two-surface doctrine and the totality doctrine;
Ringua's five contracts and four rules (NL asks, never declares; the NL engine compiles to
the closed query grammar; the knowledge graph is part of the language definition; the two
surfaces); Refine's refinement, cascade, gate, audit chain, trust floor, reversibility; the
machine language as the first declared language with a real stack beneath it.

**Left**, beyond v0.1's table: a general-purpose venue as the maker's default; a comment-
annotation as the only refinement surface; a declared language that grows "conditionals,
loops and user functions" (it "has left the jurisdiction" [R, ringua/docs/design.md 4]);
a mutable runtime knowledge store; natural-language declaration.

**Decided by this version, reversible by name:**

- **H-1 (reversed by the author)** Haro is the language of languages: one language, three
  altitudes, one law. The family is inside Haro, not above it.
- **H-9 (reversed with it)** stzu's grammar is Haro's declaring altitude, kept verbatim and
  grown by the `WORLD`, `ASK`, `NARRATE`, `REFINE`, `FORMS` seats.
- **H-10** every named thing is a refinement point by the language; a refinement is a
  sentence of Haro; the compiler takes refinements as a second source language.
- **H-11** the refinement point's grammar is v0.1's grain 3; the agent never edits text.
- **H-12** the declared altitude is total; computation passes through one declared door.
- **H-13** the machine language is the spike's program; the forge's first act runs on `rnx`.
- v0.1's H-2 to H-8 stand for the computing altitude.

---

## 13. The decisions only the author can make -- RULED 2026-10-01

Seven, re-cut on the ruling of 2026-10-01 and **ratified the same day, each on this
session's recommendation** ("go with your recommendations on D1 to D7"). The
recommendations below are therefore the rulings; the alternatives stay named so a reversal
has its text.

**D1 -- ruled 2026-10-01: Haro is the language of languages.** What remains is the *name*:
whether stzu and Ringua survive as names of Haro's declaring altitude (the `.stzu` extension,
the stzf/stzu organs) or retire into Haro (`.haro` files at every altitude; `haro forge`,
`haro check`, `haro refine`, `haro run`, `haro project`, `haro narrate` as the verbs; the
organs' letters kept as the family sentence's rhyme). *Recommendation: retire the names into
Haro and keep the grammar and the fixtures verbatim -- the site already says "the language of
languages" and never says stzu; the fixtures' history keeps its names.* And the standing
item: the Haro naming check was pending on 2026-09-13 [R] and nothing here seals it.
*Carried into `haro/` on 2026-10-02, at the author's reminder: `.haro` files, `haro.ring`,
"Haro v0.N"; the pinned v0.1 judge and the sibling repositories' files keep `stzu` (HF-44).*

**D2 -- the natural surface's scope.** Ratified by the alphabet: N asks, never declares; may
draft, through the closed compile target; the court judges, the human ratifies [R,
06-ALPHABET, ratified 2026-09-27]. *The charter conforms; nothing is asked.* What is asked:
whether Aicha's first speech is a declared language's sentence (recommended) or the
computing altitude's code.

**D3 -- which house rules become compile rules.** Unchanged from v0.1 (six language, eight
profile), with one addition the ruling makes natural: a profile is a sealed rule set, a
declared thing (`.zrlz`), and switching it is a refinement.

**D4 -- named arguments and `:Name = value`.** Unchanged from v0.1: a real named argument at
the computing altitude; the migration a census; the two readings cannot both hold.

**D5 -- the spike.** *Recommendation: section 10 -- the machine language forged on `rnx`,
54 fixtures, one refinement through the gate, the 100 ms target -- in place of v0.1's
`twice.haro`.* It proves the three altitudes and the stack at once, on a program the estate
already pins.

**And two the ruling raises, named here and put to him:**

- **D6 -- the refinement point's syntax and file.** The record carries two taxonomies of
  kinds (eight in Refine's spec, six in the manifesto) and two file extensions (`.rfn` in
  Refine, `.zrfn` in stzlib) [R, HF-19, HF-20]. *Recommendation, now the ruling: RFN's
  kinds -- knob, field, symbol, policy, composite, pipeline -- because RFN is the refinement
  language and a Haro refinement is a sentence of it; Refine's eight remain the computing
  altitude's point kinds, each mapped onto one of the six; and `.rfn`, Refine's own
  extension, with `.zrfn` retired to stzlib's comment-tag lift.*
- **D7 -- Zin.** Whether ZinScript embraces Haro, and whether Zin's pillar DSLs are forged
  from Haro's declaring altitude, is Zin's call "recorded, never forced from here" [R,
  06-ALPHABET]; the charter asks nothing and records the lossless elevation.

- **D8 -- ZQL's notation, opened by the sixth rung (2026-10-02, HF-47) -- RULED 2026-10-02:
  the Commons' shape** ("go with the Commons' shape for D8"). StzZql's `GRAMMAR.md` moves to
  it and zing's three runtimes follow; `z_v06.haro` and `tontine.z` are the proposal, routed
  through Central (HARO-Z-02). Haro admits no second notation for a kind. ZQL v0 writes
  `ENTITY deposit (id: uuid, ...)`, `NORM x AS (RULE: expr, MESSAGE: "...")`, `STEP 1: RECORD
  -> { ... }` and `AS JSON INTO`; the Grammar Commons writes `DEFINE KIND name AS (CLAUSE
  value, ...) RATIONALE`, and section 3 says every letter does. Haro v0.6 declares Z in the
  Commons' shape (`z_v06.haro`) and re-expresses zing's fixture source in it (`tontine.z`);
  the 16 cases pass unadapted. The ruling is yours: StzZql's `GRAMMAR.md` moves to the
  Commons' shape and zing's three runtimes follow, or Haro admits a second notation for a
  kind (a `NOTATION` clause, which the forge would have to emit a reader for). *Recommendation:
  the Commons' shape, because every other letter and vocabulary already has it, the forge
  already emits its court, and a second notation is a second grammar to keep in step.*

- **D9 -- where A lives -- RULED 2026-10-02 on the author's delegation: stz, beside W**
  (`declarative/a/`). A's judge is W's own fixtures; the alphabet's sentence pairs them
  ("constrain it in W, step it in A"); stz holds the pinned declarative homes (`stzu`, `w`,
  `zql`); and Zex "owns no authoring DSL -- it runs what other pillars declare". `a_v09.haro`,
  `a/w_in_a.a` and `v09/a_cases.json` are the proposal, routed through Central (HARO-A-01);
  nothing in stz is written from here.

---

## 14. What this costs, named

- **To the estate's names**: if D1 retires stzu and Ringua into Haro, three repositories and
  the vision chapters change a word; the fixtures and grammars do not change a byte.
- **To the computing altitude**: v0.1's costs stand (the Rule A surface, 136 `eval` sites,
  the `:name = value` reading, the 59% of methods without an own intent line).
- **To the declared altitude**: the seats stzu v0.1 lacks (`WORLD`, `ASK`, `NARRATE`,
  `REFINE`, `FORMS`) are grammar growth with fixtures first, prose second -- the W
  discipline; Ringua's Phase 1.5 study (the tontine given a graph and a natural door in two
  human languages) remains the named gate before `WORLD` and `ASK` are drawn [R, mission.md
  6], and this charter does not pretend past it.
- **To the agent**: nothing it had is lost; what it gains is bounded.
- **What it does not claim**: a speed (the shipped `rnxc` is in Luau's class and behind it
  [M, 2026-09-13]); a running Aicha; a Haro world booting on Harobanda; a forge that exists.
  Haro is "in construction" and the site says so; this charter is the construction's
  drawing.
