# Haro -- the charter

**Status: v0.2 RATIFIED by the author, 2026-10-01** -- "Ratified, go with your
recommendations on D1 to D7" -- so every recommendation in section 13 is a ruling, marked
there. v0.1 was written 2026-09-26 (commit 7c772ee) by the `haro-charter` session; v0.2
answered the author's note of 2026-10-01 and the vision he published on the Softanza site
the same day. With ratification the brief's next step opens: the spike of section 10, built
under `haro/spike/` and measured; its record is `haro/SPIKE.md`. Nothing else is built. No
parser, no compiler, no VM change exists for Haro beyond the `rnx` VM and `rnxc` compiler
that run the platform's code today.

**v0.3 amendments, 2026-10-04.** The Softanza Compass published the bar for Haro as input for this charter and Central
routed COMPASS-HARO-02 to this desk: adopt its fifteen dimensions and four principles, or refuse each with a reason.
Section 15 answers all nineteen; D16 to D22 are ruled on the author's delegation ("I would like you start COMPASS-HARO-02")
and are reversible by naming them; principles 12 to 15 and two amendments are in `PRINCIPLES.md`. Sections 1 to 14 are v0.2
as ratified and change only here: four rows in section 11's table, D13's update (N is built) and one bullet of section 14;
**the version stays v0.2 RATIFIED until the author has read section 15.**

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
- **For section 2's constitution clause (ZC1, 2026-11-01):** the author's ruling of 2026-11-01 on
  Zin (COMPASS-KERN-09; `softanza/memos/2026-11-01-constitution-launch.md`, section 0);
  `zin/doc/design/ZIN_CONSTITUTIONAL_WEAVES.md`, `ZIN_ZLM_CONSTITUTIONAL_LAYER.md`,
  `ZIN_PRIVACY_WEAVE_DESIGN.md`, `zin/src/compiler/constitution.zig`, `constitutional.zig`,
  `zin/src/csp/validators_stage4.zig` (cc98126, 2026-05-13), read against this charter's sections
  2, 3 and 6, `haro/spike/v20`, `narrate_lib.ring`, `court_lib.ring`, `haro_lib.ring`,
  `stzlib/base/refine/stzRefinableCode.ring` and `harobanda/declarative/machine/machine.stzu`:
  `haro/spike/v23/ZIN-INVENTORY.md`, HF-124. **Ratification of the constitution clause: RATIFIED
  by the author, 2026-11-01 23:32 -- "Ratified, start ZC2".** ZC2 (the court, fixtures first)
  opened on that line.

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

**The constitution** (ZC1, proposed 2026-11-01 by the constitution desk on the author's ruling of
the same day, COMPASS-KERN-09; **RATIFIED by the author the same night, section 0**). Zin's six immutable articles --
explainability, reversibility, visible state, predictable authority, organizational sovereignty,
trust hierarchy -- and its weaves enter Haro as a **declared governance sentence**: a declaration
of the declaring altitude, written in Haro's own shape (seats typed, `RATIONALE` mandatory, the
Commons' form), that a world declares itself under, and that the courts judge over any declared
world. The four articles Haro already holds are judged THROUGH the mechanisms this charter names
and are never reimplemented: explainability through `RATIONALE` and the narration (section 3's
`NARRATE`, principle 4's C2 envelope); reversibility through refinement (section 6, item 5: the
inverse computed before anything lands); predictable authority through the gate's governance stage
and the capability a door grants (section 6, item 4; principle 12); trust hierarchy through the
trust posture and a point's floor (section 6, item 4). The two Haro lacks -- visible state and
organizational sovereignty -- are rungs with fixtures first (ZC3), the second on the zones Z
already declares. A refusal under an article names its number and the article, in the domain's
words (COMPASS-KERN-06, adopted here, not copied). No letter: the alphabet Z W Q F A N is closed,
and the sentence is a declaration like any other. Zin keeps its federation, its pillars, its
foundry, its IDE and every customer's constitution text. The inventory behind this clause is
`haro/spike/v23/ZIN-INVENTORY.md` (HF-124): 4 articles mapped, 2 absent, 63 fixture candidates.

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
| **`NARRATE`** | absent | how a run of the language is narrated back (stzn); the court's voice. *Built, v0.13 (the thirteenth rung): SAYS, OPENS, ENDS, REFUSES; `narrate <file>`; a projection, never stored, never parsed back.* |
| **`REFINE`** | absent | which declared points of a sentence may be refined, by whom, within what bounds, at what trust floor (section 7) |
| **`FORMS` inside a vocabulary** | absent | the function-name grammar of principle 7 declared as data for the computing altitude's families. *Built, v0.12 (the twelfth rung): FLUENT, PASSIVE, STATEMENT, PARAMS and FAMILY; the families generated, the shipped spellings judged live.* |

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
six are forged: Z, W, Q, F, A; N waits on the ringua Phase 1.5 study, the author's gate (the study ran 2026-10-03: `haro/study/phase15/STUDY.md`; the N API is then drawn: `haro/spike/v17/GRAMMAR.md`).
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
**Haro v0.12, 2026-10-03 (`haro/spike/v12/GRAMMAR.md`, 10 fixtures): FORMS as data.** The
`FORMS` row above and principle 7's own guard: the fluent, passive and statement forms, the
parameter suffixes with one meaning each, and the FAMILY declaration that spells a family from
a base verb and the forms it offers. `stzv_v12.haro` declares Softanza's forms as the document
spells them; the court generates every member and judges stzString's 595 shipped spellings
live -- 584 agree, 11 do not, 41 generated members are not shipped -- the number the migration
measures, read from the author's tree and never written to it.
**Haro v0.13, the same day (`haro/spike/v13/GRAMMAR.md`, 10 fixtures): NARRATE.** The last
section-3 row no rung had built, on the author's blanket delegation (D10 to D15): a voice
declared beside the grammar -- a template per declaration kind, an opening, an ending, a
refusal -- and the forged court's `narrate <file>`: the sentence back in the language's own
words, to stdout, never stored, never parsed back. F speaks four of its kinds; the rest are
narrated with the author's own reason. Judged by a narration composed by hand first and by
the StzNarration law and stzn's honesty guard, read by Python: 5 lawful sentences whole,
92 seat values verbatim, 22 refusals as the envelope's own line (HF-63). Section 3's rows are
now all built but ASK's natural door, which is N's.
**Haro v0.14, the same day (`haro/spike/v14/GRAMMAR.md`; no clause grew): a court that
collects.** `diagnose` notes a refusal at each raising site and goes on, so a sentence wrong
in several places answers every finding, in the order of the file; `check` still stops at the
first, to the byte; a sentence that does not parse stops the run. Judged by RingFlex's own
`Check()` pass, live: five sentences with hand predictions (four right, one corrected), 11
(code, declaration) pairs the same, all 24 original fixtures the same on every finding (HF-64).
**Haro v0.15, the same day (`haro/spike/v15/GRAMMAR.md`; no clause grew): the meta-court
collects.** `haro.ring <file> all` answers every defect of a language declaration, in the order
of the file, where the default answers the first -- an author who mistyped a clause, forgot a
RATIONALE and named a type nothing declares now sees all three. Three phases and a barrier:
read and register, resolve, and only then the relations among declarations, which are
undefined while one of them is missing. Judged by the court's own first refusal one defect at
a time over the real declarations of seven letters -- 183 single defects and 116 combinations,
zero differences -- and by five files whose findings were written by hand (HF-65).
**Haro v0.16, the same day (`haro/spike/v16/GRAMMAR.md`; one clause grew): NARRATE tells a run
and a question.** `TELLS` is a template per event of a run or of a question, and `narrate-run`
and `narrate-ask` answer in the language's own voice -- a projection of the run itself, one
execution, never stored, never read back. Judged by laws read in Python out of the
declarations (30 runs, 31 answers rebuilt from the told lines, 22 questions), by narrations
written by hand before the court, and by thirteen protections each switched off (HF-66).

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

**The twelfth rung, 2026-10-03, on the author's "continue": Haro v0.12, FORMS as data**
(section 3's FORMS row, principle 7's guard). FLUENT, PASSIVE, STATEMENT, PARAMS, FAMILY; the
forged court's `family` and `spellings`; judged by the forms document's own examples (30
names, 3 families member for member) and by stzString's 595 shipped spellings read live:
**584 agree**, the 11 and the 41 named (HF-62). Record: `haro/SPIKE.md`, "The twelfth rung".

**The thirteenth rung, 2026-10-03, on the author's blanket delegation: Haro v0.13, NARRATE**
(section 3's last open row). The decisions first (D10 to D15), then the voice: SAYS, OPENS,
ENDS, REFUSES; `f_v13.haro`; the forged court's `narrate`; judged by a hand-written narration
and by the StzNarration law and stzn's honesty guard read in Python -- 5 lawful sentences
narrated whole, 22 refused ones as the envelope's own line, never parsed back, never stored
(HF-63). Record: `haro/SPIKE.md`, "The thirteenth rung".

**The fourteenth rung, 2026-10-03, on the author's "continue": Haro v0.14, a court that
collects.** `diagnose` answers every finding and `check` the first; judged by RingFlex's own
`Check()` live -- five multi-defect sentences with hand predictions, 11 pairs the same, all 24
original fixtures the same on every finding, nothing cascading (HF-64). The world's 121
lines left `court_lib.ring` to keep the cold start under its pinned 100 ms. Record:
`haro/SPIKE.md`, "The fourteenth rung".

**The fifteenth rung, 2026-10-03, on the author's "do meta-court collecting": Haro v0.15, the
meta-court collects.** `haro.ring <file> all`; three phases and a barrier; judged by the
court's own first refusal over mutated real declarations (183 singles, 116 combinations, zero
differences, every protection proved load-bearing by switching it off) and by five hand-written
files (HF-65). The owed timing re-take was taken on a quiet machine: 94.0 ms against the pinned
100. Record: `haro/SPIKE.md`, "The fifteenth rung".

**The sixteenth rung, 2026-10-03, on the author's "narrate a run": Haro v0.16, NARRATE tells
a run and a question.** `TELLS`; `narrate-run` and `narrate-ask`; judged by laws read in Python
(the told answer, the declared steps in order, every loop's count, every branch's arm, 31
answers rebuilt from the lines, 22 questions against their own clauses), by narrations written
by hand, and by thirteen protections each proved load-bearing (HF-66). Record: `haro/SPIKE.md`,
"The sixteenth rung".

**The Phase 1.5 study, 2026-10-03, on the author's "run the Phase 1.5 study"** (not a rung: ringua's exemplar
extension study, run from `haro/study/phase15/`). The tontine given a knowledge graph (`stzKnowledgeGraph`, 19
facts and a law, a 25-line text artifact) and a natural-language question surface in English and French that is
`stzNatural`'s architecture with its compile target changed to ZQL and triple patterns, judged by the ledger's
court on two runtimes, zing live, an independent evaluator and hand-composed expectations; NaturalLib 1.27 as
shipped found open (a `?` statement in a question ran; unknown prose silently accepted; it does not run on
Ring++). The engine verdict is confirmed on the architecture and corrected on two claims; the closure is a
gate's (HF-67). Record: `haro/study/phase15/STUDY.md`.

**N, drawn, 2026-10-03, on the author's "draw the N API from the study"** (`haro/spike/v17/GRAMMAR.md`; not a built
rung). `n_v17.haro` declares the natural letter -- eight kinds (TONGUE, MEANING, ALIAS, SURFACE, STEP, FRAME,
EXAMPLE, COUNTEREXAMPLE), five menus, four forms -- **in the meta-vocabulary Haro already has**: the meta-court
accepts it and the forge emits a court that checks sentences of N. `n/tontine.n` is the tontine's natural door in
English and French (85 declarations). The rules the existing vocabulary cannot say are drawn as an executable
model (`v17/n_model.py`): 14 codes, 20 fixtures the existing court calls `ok`, each rule switched off failing its
fixtures; and that model, read from the sentence alone, reproduces the study's behaviour on 74 of 74 questions. The
one growth the rung needs is a meta-clause, `UNDERSTAND`. **Decisions D-N1 to D-N15, taken on the delegation and
recorded with their costs** (GRAMMAR section 9); the drafting half of N (`propose`) is reserved, not drawn. Guard
stage 20 (HF-68).

**N, built, 2026-10-04, on the author's "build rung 17"** (`haro/spike/v17/GRAMMAR.md`, the seventeenth rung, Haro v0.17). The meta-court takes the one meta-clause the drawing asked for, `UNDERSTAND` (eight roles, each one declaration with the seats the court reads; 12 fixtures in stage 1); the forge emits a court that carries `n_lib.ring`: the rules of GRAMMAR 4b (15 codes, 21 fixtures, each load-bearing) and the verbs `tokens`, `understand`, `ask`, `vocabulary`, `examples`, with `check <file> surfaces` asking the ledger's own court to judge every ledger query. The forged court reproduces the study on 74 of 74 questions and agrees with the reference model field for field. Found by building and recorded as decisions: case folding is ASCII and Latin-1 only (D-N16), N never runs a query surface and hands the host a `run` hint (D-N17), `surfaces` is opt-in (D-N18), a tongue needs a `JOINS` seat, a world that cannot be read is a finding (`N_WORLD_UNREAD`). Guard: 20 stages, PASS in 333.4 s, every plant fails (HF-69). `propose` stays reserved.

**The structure level of the computing altitude, built, 2026-10-04, on the author's "start rung 1 of the code graph memo"** (`haro/spike/v18/GRAMMAR.md`, the eighteenth rung, Haro v0.18; HF-73 to HF-75). A program graph of Ring (49 kinds), its abstraction from `rnxc dump`'s tree repaired by Ring's own flow (nine rules, each measured on the oracle), a canonical printer that writes no `end` (Ring's `end` closes nothing), and a round-trip court in the guard (stage 22: 22 fixtures composed first, two controls that fail, a 78-file corpus; ten seconds) whose judge is the compiled code. Softanza's 6,068 Ring files: 5,958 exact, 52 as graphs only, 58 refused by Ring itself, none failing. **Not claimed:** identity (rung 2), `rnxc fmt` (rung 3), resolved edges (rung 4), that a second face helps a model.

**Node identity, built, 2026-10-04, on the author's "rung 2"** (`haro/spike/v19/IDENTITY.md`, the nineteenth rung, Haro v0.19; HF-76, HF-77). A matcher (`ids.py`) that recovers an item's id when the edited text is parsed again, from nothing but the graph that was and the graph that is: a definition by its name, a statement by its text, what is left by a similarity of 0.6, a renamed definition by the share of its body that is unchanged, and the same text anywhere in the same function. A court in the guard (stage 23: 23 edits written first, six controls that must fail, Haro's own history replayed, twenty seconds) on whose history **98.3 percent of the statements a refinement could have targeted still resolve after the next human edit**: CODEGRAPH 3.7's 95 percent holds, K2 does not fire, and option A stands -- the ids are not written into the text. **Not claimed:** a lineage of edits (per edit, not cumulative), the cache that holds the last graph with its ids, an id inside an expression.

**`rnxc fmt` and the lossless export, built, 2026-10-05, on the author's "rung 3"** (ringpp's `src/fmt.zig` and `src/dumpjson.zig`, `CLAUDE.md` there; HF-78 to HF-81). `rnxc dump --json` is the parse of a file with nothing lost (a flat pre-order array of nodes with spans, gaps and full leaf text, every string as bytes), and `rnxc fmt [--write | --check]` is rung 18's printer as a verb -- the canonical text, one spelling per construct. Judged on the real binary, in the gate: 21 fixtures byte for byte; every Softanza file under 400 KB (6,061) printed as the reference prints it or refused by both (58, of which Ring itself refuses 57); idempotent; the graph read back exact; the same compiled code on about 590; the 115 probes, formatted, the same on the oracle; 13.8 seconds for all of it. **A statement that begins with a unary `+` or `-` is read by the grammar over the whole rest and by Ring over the first operand** -- the first `fmt` changed what such a statement does on Ring while the graph, `rnxc dis` and the probes agreed it had not; fixed in the graph, judged by the oracle (fixture 23), the compiler's own half open and ringpp's. **Not claimed:** that `fmt` ships before Haro (Q4, the author's), a CRLF-preserving mode.

**`rnxc graph`, the resolved graph, first slice built, 2026-10-05, on the author's "continue"** (ringpp's `src/graph.zig`; HF-82 to HF-84). L2 of the code-graph memo as stzCodeGraph's own line protocol -- classes, methods, functions, imports, and the call edges the COMPILER bound while it emitted code (one target, or by name with the width of the name, and a mark where it could not finish) -- judged by five fixtures written first, the Softanza unit's consistency, and, standalone, by stzRingCodeGraph's name-based scan over the same 612 files: 97.0 percent of its edges are the compiler's, and all 1,556 that differ have a cause read out of the source (a builtin's name, a comment, a `func` method it never registers, a `class` line inside a comment). stzCodeGraph ingests the stream unchanged, 13 seconds against the scan's 73. **Not claimed:** edges for `new K`, references, scope, `depends_on`; that stzlib has wired it.

**Refinement over the program graph, built, 2026-10-05, finished 2026-10-19, on the author's "start rung 5"** (`haro/spike/v20/GRAMMAR.md`, Haro v0.20; HF-85 to HF-90). A refinement is a sentence in `rfn.haro`'s shape against a point a program declares in a `<R:KIND ...>` tag, put through five stages in `stzRefinableCode`'s order and lowered to RCP's twelve primitives over rung 18's graph with rung 19's ids; the diff is the printer's, one line out and one in. Judged by 89 fixtures (guard stage 24), by Softanza's own `stzRefinableCode` put the same 501 proposals (488 agree, 0 disagree; its three limits measured), by `rnxc graph` for a retargeted call, by the engine's decoder for the grammar scoped to each program (the agent's write surface, charter 6.2), by ten controls, by Haro's own history (98.2% of drafted refinements land after the next edit) and by a mutation study (505 of 519 defects killed). **The BLOCK kind, built 2026-10-19:** an agent proposes the body of a function whose signature a human declared, held to the calls and writes the point names, refused at structural for what the gate cannot follow, and judged at derivation by the compiler (`rnxc check`), failing closed where the compiler cannot vouch for the program (HF-95 to HF-97). **The FUNCTION kind, the same day:** a point that declares a function -- name, parameters, what its body may call and write -- which the agent then creates or fills in, never deletes (HF-98, HF-99). **Not claimed:** the kinds `type`, `lib`, `custom`; a scoped grammar for a program of more than about a dozen points, which the decoder does not hold (HF-87). **The allowlist rules and the METHOD kind, 2026-10-20** (HF-100 to HF-103): a point's own `calls` and `writes` are refinable rules (widening a tier-4 act), and a method of a class is declared and created like a function, before the class's `private` marker and off the names Ring calls itself or refuses; a body kind refines a program, not a library (HF-103).

**A local model as the agent of a refinement, measured, 2026-10-21, on the author's "decide on my behalf and start the work"** (`haro/spike/v20/agent/AGENT.md`; HF-116, HF-117). Rung 5's court had never put a model in the loop: its agent was a harness. Sixteen refinement tasks (a BLOCK or FUNCTION point, its allowlists, a function's body to write, two data sets), the gate as judge, rnxc running the refined program, the harness proven on gold answers first (guard stage 28). Qwen2.5-Coder-1.5B gets **3 of 16 right on both data sets when it writes the one-line TO that `scoped.py` leaves as free text, and 10 of 16 when it writes lines under the point's own grammar** and the harness flattens them into the TO; the 0.5B 0 and 3, SmolLM2-135M 1 and 0. **For a body kind the charter's 6.2 ("the agent's only write surface is a sentence") becomes: the agent writes the body, as lines, under a grammar scoped to its point (`scoped.body_lines_gbnf`), and the harness writes the sentence around it** -- **ruled on his delegation, 2026-10-22, as D27.** Three of the six failures are a body that does not end, and a GBNF cannot say "an identifier that is not a keyword" (HF-117).

**A second face of the program graph, built, 2026-10-19, on the author's "go ahead with rung 6"** (`haro/spike/v21/GRAMMAR.md`, Haro v0.21; HF-91 to HF-94). Rung 18's graph printed in Python's shape for a reader, with one meaning -- Ring's: plain where Python reads it as Ring means it, an explicit word where it would not (`at`/`setat` 1-based, `eq` Ring's comparison, `cat`/`plus` Ring's `+`, `span`/`rng` inclusive, `G.` the global, `return ""` NULL), and refused by name from a table of sixteen collisions that travels as the face's banner. Judged by 46 fixtures (guard stage 25), by Python's own parser on every text, by five controls, and by 300 files of Softanza's base, 76% of which print whole. **K3 is measured and not met**, so a reader of the face (rung 7) stays open. **Not claimed:** K4 -- that a model writes better in this face -- and the memo's 20-task protocol, which need that reader. **The reader, built 2026-10-20** (`haro/spike/v22/GRAMMAR.md`, Haro v0.22; HF-104 to HF-109): a text in the face read back to the graph and to Ring, accepting exactly the printer's image, so that what is read has one Ring meaning; judged by 67 fixtures written before it, by 300 files of Softanza's base read back to the same graph up to twelve declared losses, and by the oracle (95 of 95 runnable probes behave the same after print, read and run). It made the printer injective and a formatter (23 collisions) and found that rnxc binds `not` looser than Ring does (HF-105, reported; fixed 2026-10-20, ringpp C-32, which retired one collision: 22). **K4 was then measured** (2026-10-20, `haro/spike/v22/k4/K4.md`, HF-110): capable models do no better writing the face than Ring -- Ring 19-20 of 20 with or without a primer, the face at best ties -- so, for them, it is a reading aid and the formatter's respeller, not a write surface; small local models under a decoder -- Softanza's direction -- are unmeasured and a grammar for them is owed.

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
| 7 | forms as execution modes | `FORMS` declared as data -- v0.12: FLUENT, PASSIVE, STATEMENT, PARAMS, FAMILY; the families generated, the spellings judged | closed verb sets, one word per letter | v0.1: the forms as grammar, families from a rule |
| 8 | humans read; agents write | **amended again**: the default venue is declarative and natural; N drafts, the court judges, the human ratifies | the agent's sentence is the human's sentence | the expert venue, one governed door |
| 9 | **declaring a language is as easy as declaring a variable** | the founding act is first-class: a language is a value with a version, a court, a grammar; composition over the alphabet is the normal way | | |
| 10 | **every change is a refinement** | a grammar version is a point with its fixtures as cascade | every named thing is a point; the refinement is the agent's write surface | profiles are refinements of the library |
| 11 | **total by default** | | not Turing-complete: W total, F expression-free, A bounded; non-termination unexpressible | computation reached through one declared door |
| 12 | **no effect without a door** (v0.3) | a judge runs nothing its text names; the door is the judge's (HF-70) | no declared text acts; a refinement is a plan until a governed actor commits it | an effect is a typed capability granted to an actor *(owed)* |
| 13 | **every claim is judged, and says its class** (v0.3) | a fixtures file names its class *(owed)* | a promise, a seam, a projection each name their class | a promise is part of the program's text |
| 14 | **compute is the engine's decision** (v0.3) | no letter spells a width (stage 21); a machine declares what it has | the engine chooses the width | the engine chooses the width |
| 15 | **a human language is a data file** (v0.3) | a tongue is a declaration (N, built) | questions, refusals, narration per tongue, judged to agree | one tongue |

v0.3 also amends principle 4 (a refusal names a state, never a person: stage 21's S1) and principle 5 (the catalogue is
data: owed).

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

- **D10 -- HF-30, ordering two strings -- RULED 2026-10-03 on the author's blanket
  delegation: keep.** `rnxc` orders strings by bytes where Ring raises R41. A Ring program
  that reaches the comparison stops there, so no program that worked on Ring holds a
  successful string ordering whose meaning could change: the answer is a strict extension.
  *Cost*: code that used a caught R41 as a probe for "is this a number" would stop raising;
  the spike's own court keeps classifying characters by byte code, because it is judged on
  both runtimes. Routed to the ringpp session for `docs/CORRECTIONS.md` as "keep" with this
  reason; the exec probe is still to be pinned there.

- **D11 -- HF-36, a list literal that names the variable it assigns -- RULED 2026-10-03:
  fix silently.** `rnxc`'s reading (the old value goes inside) is the one every other
  language gives; Ring's (the new list inside itself) is the cycle the "object held itself"
  defect already paid for. *Cost, measured by one read-only scan*: of 10 sites in Softanza's
  core, base and max that match the shape, 7 are live -- each guarded by `isString` or
  `NOT isList` and wrapping a non-list -- and 3 sit in an archived monolith; none nests a
  list, so none can change meaning. Routed, as D10.

- **D12 -- NARRATE's shape -- RULED 2026-10-03: a voice declared beside the grammar.**
  Templates per kind, an opening, an ending and a refusal; a projection of the sentence, to
  stdout, never stored, never parsed back (the StzNarration law, principle 8). stzn's HTML
  skins stay stzn's: the declaration holds the words, not the wardrobe. Built as Haro v0.13.
  *Cost*: stzn v0's page and a forged court's narration are two renderings of one idea until
  stzn takes its templates from a declaration (HARO-NARRATE-01).

- **D2, its one open half -- RULED 2026-10-03: Aicha's first speech is a declared language's
  sentence**, not the computing altitude's code -- the recommendation, now the ruling. N
  drafts a sentence; the court judges it; the human ratifies. Computing code stays the expert
  venue, behind one governed door.

- **D13 -- N and the Phase 1.5 study: the gate holds.** Not a decision to take: the study
  (the tontine given a graph and a natural door in two human languages, mission.md 6) is an
  experiment, and no ruling produces its result. N is built behind it, as the alphabet says.
  **UPDATE 2026-10-03 -- the study ran, on the author's "run the Phase 1.5 study"** (`haro/study/phase15/`,
  `STUDY.md`). The roadmap's condition -- the composed exemplar answers domain questions in two human
  languages without the answer path leaving the closed surfaces -- is met on the measurements (74 questions,
  English and French; 17 of 17 pairs compile to one closed query; 16 attacks refused with the canary at 0, and at 1
  with the gate removed; the same bytes on official Ring 1.27 and on Ring++), **with one qualification: the
  closure is the gate's, because `stzNatural`'s shipped tokenizer evaluates bracketed text**. Whether that closes
  the gate is the author's reading. **The N API was then drawn from it**, on the author's "draw the N API from the study"
  (`haro/spike/v17/GRAMMAR.md`): drawn, then **built on 2026-10-04 as the seventeenth rung** (the meta-clause
  `UNDERSTAND`, the court's five verbs and sixteen rules; HF-69, HF-70). STUDY.md section 6 (K1-K10) was its input.

- **D14 -- the forge as an `rnxc` verb: stays the ringpp session's, routed.** Today the forge
  is Ring source `rnxc` runs (`rnxc forge.ring <file>`); a verb is a change to
  `src/rnxc.zig`, outside `haro/` and that session's own work. The guard folding into
  `bench/gate.py` is routed with it. This session writes neither.

- **D15 -- `origin/next` (HF-18): remove it -- DONE 2026-10-03, at the author's word.** The
  visibility rule says `next` never goes to origin, and it was there at `026ac97` with
  `haro/*.md` inside. Decided on the delegation and left unexecuted, because deleting a
  public branch is an act on the public remote and `ringpp/CLAUDE.md` names pushes to
  origin his; he then said "if the removal is what we should do while keeping everything
  consistent, then remove it". Consistency checked first: no pull request from or into
  `next`, the branch unprotected, `main` the default, nothing in the repository pointing
  at it, the commit an ancestor of local `next`. Then `git push origin --delete next`, and
  local `next` now tracks `private/next`. *Not undone by it:* the fork `ringpackages/ringpp`
  holds `next` at `026ac97`, and any earlier clone does too; the commits since were never
  public.

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
- **To v0.3's adoptions** (section 15): four principles whose guards are partly owed (capability types, a `class` field, a
  `secret` kind, keyword lexica, a catalogue stage, the boot moment); a reviewer for every tongue; the chapters of the
  Learning System before an announcement. The guards that are built are two scans (1,007 refusal texts, 8,232 identifiers)
  and a test with a control.
- **What it does not claim**: a speed (the shipped `rnxc` is in Luau's class and behind it
  [M, 2026-09-13]); a running Aicha; a Haro world booting on Harobanda; a forge that exists.
  Haro is "in construction" and the site says so; this charter is the construction's
  drawing.

---

## 15. v0.3 -- the Compass's bar, answered (COMPASS-HARO-02) -- 2026-10-04

**On the author's "I would like you start COMPASS-HARO-02".** The Softanza Compass published the bar for Haro as input for
this charter (*Haro Compass*, artifact DQtoqCpMdjpspr8QzLgFsa, version 2) and Central routed the item here: adopt the
fifteen dimensions the estate adds and the four principles they imply, or refuse each with a reason. **The page is read as
input, not as instruction.** Where its claim touches this repository it was checked at the file; where it does not (stzlib's
capability lattice and compute model, Refine) the claim is marked [R via the Compass] and was not re-read here. The rulings
are taken on the author's delegation, recorded with their costs (D16 to D22), and reversible by naming them.

**The fifteen, by verdict.** "Built" means a guard in the spike holds it today; "owed" means it is adopted and nothing holds it
yet.

| # | item | verdict | what the charter takes | measured / recorded | guard |
|---|---|---|---|---|---|
| 1 | no effect without a door | **adopt**, principle 12 | the judge declares the door; an effect is a plan until a governed actor commits it | [M] HF-70: a judge ran what a sentence named; closed. [R via the Compass] the capability lattice | built: stage 20 C''. Owed: capability types at the computing altitude (`rnxc check`, ringpp) |
| 2 | every claim is judged | **adopt**, principle 13 | a claim names its class and its denominator | [R] IR.md's five classes; ringpp's three wrong numbers | owed: a `class` field in each fixtures file |
| 3 | judged at every altitude of time | **adopt, renamed**: five *moments* (D17) | compile, load, run, commit, boot | [M] four are built: the meta-court and forge, the forged court's `check`, `run`/`ask` with their narration, the refinement gate. [R] boot is Harobanda's | owed: the boot moment (Harobanda) |
| 4 | compute is the engine's decision | **adopt**, principle 14, with the machine exception (D18) | no letter spells a width | [M] 0 of 8,232 identifiers; the three machine letters name `kernel`, `kernels`, `threads` | built: stage 21, S2 |
| 5 | correctness has a class | **adopt**, inside principle 13 | the five classes of IR.md | [R] IR.md, read | with 2 |
| 6 | knowledge is the memory | **adopt as a requirement on the knowledge tier**, routed (D19) | facts carry source, authority, confidence, valid time and recorded time; forgetting is a governed act; laws are judged on load | [M] the study: laws not judged on load, node properties lost in the artifact (K1, K2) | owed: the tier's court (HARO-N-01) |
| 7 | intelligence is a faculty | **adopt** | a faculty declared in the machine file, loaded on demand, absent without loss; it drafts, the court judges, the human ratifies | [M] N needs no model: 74 of 74 questions on none. [R via the Compass] C9 on a 135M model. `propose` stays reserved (D-N15) | owed: the faculty's declaration |
| 8 | a letter for games | **not ruled here**: COMPASS-HARO-03, the author's | recommendation recorded: a letter, after N has a second sentence | [M] N is one sentence in two tongues | -- |
| 9 | a human language is a data file | **adopt**, principle 15, scope the declared altitude (D18) | a tongue is a declaration; the same-query law; a reviewed speaker | [M] N built: 17 of 17 pairs one meaning sequence | built: N's rules. Owed: keyword lexica; a tongue beyond Latin-1 |
| 10 | learnable by construction | **adopt as a release criterion** (D21), not a provision of the language | no construct is announced without its chapter and a running cell | [M] 17 rungs, each with a GRAMMAR.md and fixtures: the seed | owed: the chapters (stzlib's Learning System) |
| 11 | self-describing, in tables | **adopt**, amends principle 5 | the catalogue is emitted as data | [M] a GBNF per language; N's `vocabulary` (68 words) equals the model's | owed: a catalogue stage |
| 12 | secure by construction | **adopt as a rung**: a `secret` seat type, fixtures first (D20); the SBOM routed to ringpp | a secret is never narrated, never in a diagnostic, never compared except through its gate | [M] N's gate: 16 attacks refused, the canary at 0, at 1 with the gate removed. [R] ringpp's gate checks 296 vendored hashes | owed: the rung |
| 13 | the refusal names states | **adopt**, amends principle 4 | no second person, no "the user" | [M] 0 of 1,007 refusal texts | built: stage 21, S1 |
| 14 | measured before claimed | **adopt**: already this charter's reading rule; the public half is the author's | no public sentence about speed, size or helpfulness without its measurement | [R] "How to read it"; HF-27 | -- |
| 15 | a declared machine beneath | **adopt**: already section 7 and H-13 | a program names its machine; the machine's needs are declared | [M] the machine court agrees with harb on 117 of 120 fixtures (the pinned floor) | built |

**By count: twelve adopted in substance, one narrowed to a release criterion (10), one routed as a requirement on another
desk (6), one left to the author's own routed item (8). None is refused outright; five changed in wording or scope (3, 4, 6,
9, 10), each with its reason above.**

**The four principles.** Twelve, thirteen, fourteen and fifteen are adopted as written in `PRINCIPLES.md`: item 1 gives
twelve, items 2 and 5 give thirteen, item 4 gives fourteen, item 9 gives fifteen. Items 11 and 13 amend five and four.

**Two things the adoption measured.** *One:* applying principle 12 to the court written the day before found a door -- `check
<file> surfaces` ran any file a sentence named (HF-70) -- closed the same day and held by a test with a control. *Two:* two of
the four principles held at zero before they were adopted (stage 21: no refusal addresses a person among 1,007; no letter
outside the machine's spells a width among 8,232 identifiers), which is why adopting them costs a guard and not a rewrite
(HF-71). The machine letters do name `kernel` and `threads`: a machine declares what it has, and that is the exception that
states principle 14.

**What the Compass asks that is not among the nineteen, and is not ruled here.**
- **The code graph beneath the faces** (the page's tensions T1 and T5; the author's third dimension, "other faces, with a
  code graph at the heart"). It is the page's one genuinely new design: the computing altitude compiles a graph, every face
  is a parser and printer pair judged by a round trip, and a Python-shaped face is a spelling, not Python. It is not an item
  of COMPASS-HARO-02 and wants a design memo of its own: the levels document's structure level extended to the computing
  altitude, and one round-trip court on the Ring++ face before any other face. Until then the public sentence about a
  "running polyglot engine" stays "designed" (COMPASS-HARO-04, the Harobanda desk's). **The design memo is written** (2026-10-04, COMPASS-HARO-05, on
  the author's "do the design memo for the code graph"): `haro/CODEGRAPH.md`, recommendations R1 to R12 and four decisions, Q1 to
  Q4, that are the author's; **nothing in it is ruled**.
- **T2, one executable or two** (COMPASS-HARO-01): the author's. The facts were sent to the Compass on 2026-10-04: no `haro`
  command exists, the spike's verbs are `rnxc haro.ring`, `rnxc forge.ring` and `rnxc <lang>_court.ring <verb>`, D14 keeps
  the forge-as-verb ringpp's, and Q's and N's `ask` share a name and would dispatch on the sentence's extension.
- **T3, the games letter** (COMPASS-HARO-03, item 8): the author's.

**The decisions, ruled on the delegation and reversible by name.**

- **D16 -- principles 12 to 15 are adopted** as written in `PRINCIPLES.md`, with amendments to 4 and 5. *Cost:* four more
  rules for a reader to carry, each with a guard that is built or owed (see the table).
- **D17 -- "altitude of time" is renamed "moment".** The charter's *altitudes* are three (declaring, declared, computing);
  the Compass's five times of judgement are compile, load, run, commit and boot. *Cost:* the page's wording changes; the
  claim does not.
- **D18 -- two narrowings.** Principle 14 has the machine exception (a machine declares what it has). Principle 15's scope is
  the declared altitude; the computing altitude stays in one tongue (the page's T6, as recommended). The first Zarma or Hausa
  tongue needs a speaker to review it and the court's fold table extended with a fixture first (D-N16). *Cost:* no
  multilingual keywords of the computing altitude, ever, unless this is reversed.
- **D19 -- knowledge is a requirement on the knowledge tier, not a Haro grammar.** Facts with provenance and two times,
  governed forgetting, laws judged on load: routed with HARO-N-01 to whoever owns the tier. *Cost:* until the tier exists N
  asks a surface and judges nothing of the world.
- **D20 -- the `secret` seat type is a rung, fixtures first** (never narrated, never in a diagnostic, never compared except
  through its gate); the SBOM for each binary is routed to ringpp, whose gate already hashes the vendored trees. *Cost:* the
  rung is not built; until it is, no letter declares a secret.
- **D21 -- two release criteria, not language provisions.** "Learnable by construction" (no construct is announced without its
  chapter and a running cell) and "measured before claimed" (no public sentence about speed, size or helpfulness without its
  measurement beside it). The announcement is the author's. *Cost:* the chapters are stzlib's Learning System's to write.
- **D22 -- principles 4 and 5 are amended** (a refusal names a state, never a person; the catalogue is data), with stage 21's
  S1 holding the first. *Cost:* a refusal text that says "you" now fails the guard.
- **D24 -- names are exact in the Haro layer; Ring's case folding is not inherited** (rung 5, ruled on the author's delegation, 2026-10-19:
  "take any opportunity to not inherit bad Ring habits"). A point's name, a rule's sides, a governance, an actor, the points an actor may refine,
  the KIND and POSTURE seats, a tag's keys (lower case) and kind (upper case), the callee a refined call names: one spelling each, matched
  exactly. Two names that differ only in case are **look-alikes, refused** -- names are exact, and a reader would take them for one. A
  near miss is refused with the declared spelling named (`no refinement point 'Vat' (names are exact: 'vat' is declared)`). Ring's
  folding stays only where the gate *describes the Ring program*: which statements read or write a variable (F-18 is Ring's behaviour,
  and the cascade must be right about it). *Cost:* a sentence written in another case is refused rather than understood; the court's
  folding fixtures became refusal fixtures. `stzRefinableCode` already matches exactly, so the two gates now agree by construction (HF-88).
- **D25 -- a refinement is a change; a no-op is refused** (same delegation). TO the very text FROM found is refused at the structural
  stage, `nothing to refine`, for a value and for a rule's attribute alike, so every admitted refinement changes exactly one line --
  what the court already required. The same number spelt otherwise (`0.20` to `0.2`) changes a line and stays a refinement, as A04
  reads a human respelling. *Cost:* a no-op the live gate admits is refused here (85 of the court's 504 proposals, counted apart); the
  branch `'x' is not governed` became unreachable and is gone.
- **D26 -- the write surface is what a task may change** (same delegation; HF-87). `scoped.py` takes the points a task names
  (`points=`), and the grammar holds their sentences and no others: least authority, and a grammar small enough for the engine's decoder
  whatever the program's size -- so the decoder's 128-rule cap stays where it is. A task naming a point the program does not declare is
  refused by name; a whole-program grammar the decoder cannot hold is refused by the engine by name (GBNF-M2), never silently.
- **D27 -- for a body kind the agent writes the body, under the point's grammar; the sentence is the harness's** (rung 5 with a model as the agent, ruled on the author's delegation, 2026-10-22: "close any pending task or decision on my behalf";
  HF-116). The charter's 6.2 said an agent's only write surface is a sentence. For BLOCK, FUNCTION and METHOD points that is amended: the agent writes the BODY, as lines, under the grammar derived from its point
  (`scoped.body_lines_gbnf`: the point's own calls and writes, a statement a line, a closing sentinel), and the harness writes the sentence around it -- TARGET, KIND, FROM, AUTHOR, POSTURE and REASON are the harness's, so an agent
  cannot write a stronger posture than it holds. The lines are flattened into the TO the gate reads, so the gate judges the same body whatever shape the agent wrote it in. *Cost:* `scoped.py`'s sentence grammar no longer
  fixes the whole of a body kind's output (its TO stays `qbody`, which is what a one-line agent still writes); the body's shape is the body grammar's and its meaning the gate's. VALUE and RULE kinds are unchanged.
- **D28 -- what the body gate does not govern is named and kept; Haro makes every call a named call** (same delegation; HF-118). The gate governs the names a body calls and the variables it writes. It does not govern: the effects of a callee the
  point allows, an operator applied to an object (an implicit call of `operator`), a read of a global, output, or termination -- each pinned by the bypass court as a limit, none a verdict. Not built here: a `reads` attribute, closed by default,
  is the next rung-5 item and closes the reads and, with them, the objects a body can reach but are not its own. Decided for Haro, not built: no implicit dispatch -- an operator on an object, an accessor and a constructor are calls that are
  written, so that an allowlist of calls is the whole of what a body can run. *Cost:* Haro programs written like Ring's overloaded classes need the call spelt out; the gate then needs no types to be exact.
- **D29 -- a task whose text names what its point forbids is refused before any model is asked** (rung 5, ruled on the author's delegation, 2026-10-22: "go ahead with the task lint"; HF-119, HF-120, HF-121). The allowlist is the point's
  tag, not the request's text: a task that names a call its point does not allow, asks to write a global its point does not name, or claims the allowlist is out of date is a contradiction, and the harness refuses it with the reason
  (`task_lint.py`) rather than asking a model to resolve it -- a 1.5B model resolved it for the request in 8 of 8 bodies, and the gate's reason did not move it. A request that may ask to change the caller's list only warns. *Cost:* a task that names a
  call it allows must spell it exactly (D24); a task is refused until it is reworded, including one that only reads a global after a write verb; and the harness that WANTS to measure the pull (the adversarial set) runs with the lint off, which is why `--lint` is opt-in.
- **D30 -- a body reads only what its point names: `reads`, closed by default** (rung 5, ruled on the author's delegation, 2026-10-22: "go ahead with the reads attribute"; HF-118, HF-122). A BLOCK, FUNCTION or METHOD point carries
  `reads="$x|@y"` beside `calls` and `writes`; absent, a body reads its parameters and locals and nothing outside its frame, and what it may write it may read. It is refined as the other allowlists are (widening a tier-4 act, narrowing refused
  below what the body reads), enforced at the constraint stage, written into the body grammars and the task lint. Least authority had been stated for calls and writes and left open for reads, which is where a secret, a global object and its
  operators were reachable. *Cost:* a body point written before this that reads a global it does not name is outside its own rule until its author names it; a grant to read an object includes using it as a value (its `operator` runs), which the
  author sees in the tag and the court pins as a limit.
- **D31 -- an app is a namespace of its own: HaroServer's apps never share names** (HaroServer, ruled on the author's delegation, 2026-11-01: "do the open question of haroserv on my behalf"). Running the server
  answered that every app shared one namespace with the library and with every other app -- Softanza defines `echo`, so an app's `Echo` was refused (C22), and two apps could not both define `Init`. The Haro answer:
  each admitted app is a namespace, and what it defines -- functions, classes, globals -- is its own and nobody else's. Inside an app a name resolves to the app's own definition first, then to the BASE (the host and
  the library it admitted before any app) and nowhere else, so the base growing a name never breaks an app. Another app is reached only through a name that app EXPORTS -- declared by the app, nothing by default
  (least authority) -- spelt qualified and exact, `ledger.Entry` (D24); there is no `import` that pours another app's names into this one, and a qualified name nothing exports is refused when the line runs, as a
  late name is (rung 8). Ring's `package`/`import` stay refused in Ring++ (C-28): this is Haro's rule, carried by HaroServer's resident host, not Ring's. *Cost:* the resident VM must resolve per app -- an app's
  definitions stored under its own name, an unqualified call looking in the app and then the base, and the late links (`name_fn`, `name_cls`), `call "f"()` and eval looking the same way -- a compiler change confined
  to a resident program's admitted code (a plain program compiles as before); an app that uses another's class writes `new ledger.Entry(...)` and the other app exports `Entry`; RingServ's shape (every app eval'd into
  one global namespace) is not reproduced. **BUILT the same day**, on the author's word ("go ahead with building D31"): `admitapp(cApp,
  cSource, aExports)` and `replaceapp(cApp, cSource)`; an app's late names fall back to the base's at run time (VM.name_up); exports answer by
  their public names (the installer's `applyExports`). What the build decided beyond the decision, recorded so it is not lost: the BASE reaches an
  app's names by their internal spelling `app::Name` -- the host owns its apps, and its router calls their handlers that way; only apps are held to
  exports. An app's top level and its lambdas resolve a name given by string as the base does, and an `eval` in its code resolves every name as the base
  does, because none of them carries the app in its name; and an app's admission is not released, because another app may hold its exports. Guards: the resident VM's section 11 (golden: Ring
  has no namespaces) and HaroServer's court; a plain program compiles to the same code as before.
- **D32 -- a body's derivation asks whether the unit DEFINES what the body uses: `rnxc check --closed`, through the program that loads a library** (rung 5, ruled on the author's delegation, 2026-11-01: "go ahead
  with the library derivation of rung 5"; HF-123). The derivation asked Ring's question -- is this an error the moment the line runs? -- which has no answer in a library (nothing runs) nor in a unit holding eval,
  loadlib or an admission, so the gate failed closed on both, and therefore on every body of the estate (HF-103). It asks the gate's own question now, closed: a name only eval, loadlib or an admission could make
  is absent, because the gate cannot see what it calls (D28; Ring++'s eval defines no function, F-72); a native counts when the engine's own list names it (`cfunctions()` on a run that loaded it), spelt as the
  engine registers it (D24 -- lower case, so `stzenginecancelsignal`, not Softanza's `StzEngineCancelSignal`, which case folding reaches); a call's arity resolves through the whole unit (one definition per name,
  C22); a file the unit cannot read or parse is still a hole, and the gate fails closed on it. A library file is refined THROUGH the program that loads it: the lift reads that unit's names, and the derivation
  checks the unit with the file's text replaced (`--subst`) -- the file is never written. *Cost:* each derivation checks the whole unit, about 14-16 s at Softanza's size (697 files; the first of a model about
  35-45 s, which also reads the unit's names); a body that calls a native needs the engine's list; an eval elsewhere in a program no longer stops a body's refinement (B09 and FN10 say the opposite of what they
  said), so what an opaque eval assigns is refused by name instead; and a closed check's findings are claims about what the unit defines, not Ring's run-time proof -- its words say so.
- **D23 -- `rnxc fmt` is a Ring++ feature, not held for Haro** (CODEGRAPH Q4, ruled on the author's delegation, 2026-10-05: "take
  whatever decision you think is wiser on my behalf"). It is a verb of the one binary (commitment 5), depends on nothing of Haro's, is
  judged against the oracle and refuses what Ring refuses (58 of 6,061 Softanza files, 57 of them Ring's own refusals). It ships inside
  `rnxc` with the rest of `next` when the author announces, not separately and not early: the visibility rule stands. Limits: **it is
  never run with `--write` on the author's tree except at his word** (it rewrites the layout of the estate: tabs, LF, blank lines, and a
  statement written after a function's `end` moves into the function, which is where Ring runs it); the court stays in the gate, and a
  shape on which the reference and the oracle part is a finding before it is a feature (HF-79); the canonical spelling is the one the
  printer writes, with no option for width or style until a customer asks. *Cost:* a formatted file differs from its source in layout
  everywhere; `--check` and a diff are how a person sees it first. The same delegation keeps the compiler's half of HF-79 as a recorded
  divergence (C-23).

**Unchanged, and recorded so it is not lost:** nothing here moves a ratified decision of sections 1 to 14. D1's verbs
(`haro forge`, `haro run`, `haro refine`) are not touched: they are COMPASS-HARO-01's.
