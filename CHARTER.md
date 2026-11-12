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
trust posture and a point's floor (section 6, item 4). The two Haro lacked -- visible state and
organizational sovereignty -- were built as rungs, fixtures first (ZC3, 2026-11-02, D34): the first
through the access paths a language declares (told, asked, published) and the gate's events kept
as an audit chain the court answers as a query; the second on the zones a world declares, each
held by a named organization and entered through a declared flow. The whole was then proved on a real world (ZC5, 2026-11-02, D36): the Commons' tontine
declared under the six articles and both weaves and judged end to end on both runtimes, with no clause added to the grammar -- the constitution changed
its sentence by one clause, who holds the zone; the author's reading of its refusals is the gate. A refusal under an article names its number and the article, in the domain's
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
| **`CONSTITUTION`** | absent | the articles a world declares itself under, judged through the seats above and the gate, never reimplemented (section 2; D33). *Built, v0.23 (ZC2, 2026-11-02): `ARTICLES` drawn from Zin's six by name and number, `WEAVES` and `REGIME` carried for ZC4; 22 fixtures and a bank's ledger judged on both runtimes. v0.24 (ZC3, the same day, D34): `ZONE`, `SOVEREIGN`, `MOVEMENT`; visible state through the access paths and the audit chain; 18 fixtures and the bank under all six. v0.25 (ZC4's Haro slice, D35): `PERSONAL`, the sovereignty and privacy weaves at their severities, the regime read, `SEVERITY` on a constraint; 16 fixtures and the clinic. v0.26 (ZC5, the same day, D36): no clause -- Z, the tontine language, declared under all six and both weaves and judged end to end on the tontine, zing's cases unchanged; 13 fixtures and 16 cases; the author's reading of the refusals is the gate. v0.27 (ZTAG, the same day, D37): a pair form's mark (`member: text personal`), `PERSONAL` by a three-part path, `SAFEGUARDS` on the ask and the voice; the court names the marked fields, answers whole under consent, tells redacted under redaction; 14 fixtures and 11 cases* |
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
- **Its system grain is Softanza's system language -- RULED by the author 2026-11-06, binding
  on this section** (his words, "Yes to the three parts, start SG0 now", carried by Central
  2026-11-06 11:25, COMPASS-SYSLANG-07 part a; written here 2026-11-07). (a) Softanza's system
  language IS the system grain of this altitude: never a sibling language, never a letter, and
  no second language is drafted beside it. (b) C is the grain's first native target and
  WebAssembly its second, behind one owned compiler; LLVM and MLIR refused. (c) Self-hosting is
  tripwire T4: the day the grain compiles the Haro VM's own compiler byte for byte under the
  spike's guard stages. The Substrate ruling of 2026-10-30 (Zig at the pin for the engine, Rust
  plan B) stands whole. The grain's design (COMPASS-SYSLANG-02, SG1) is this desk's and starts
  on SG0's decision memo; its types are D55's (`TYPES.md`).

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
| 4 | refuse, then explain | the meta-court's channel, C2 | refusal phrasing declared beside the grammar, in jargon | v0.1: C2 + why/todo/frames; v0.11: every forged court's `diagnose`, its codes and cites declared beside the words (CODE, CODES, CITES); v0.28: every coded element cites, and `CITES none` cites nothing (D38) |
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
- **D33 -- the constitution is a `CONSTITUTION` declaration of the declaring altitude, one per language, and its articles are judged through the mechanisms section 2 names** (ZC2, built on the author's
  "Ratified, start ZC2", 2026-11-01 23:32; `haro/spike/v23/GRAMMAR.md`). `DEFINE CONSTITUTION <name> AS (ARTICLES [...], WEAVES [...], REGIME ...) RATIONALE "..."`: `ARTICLES` names, each at most once, the
  articles the world declares itself under, drawn from Zin's six in Zin's order and numbering -- `explainability` (1), `reversibility` (2), `visible_state` (3), `predictable_authority` (4),
  `organizational_sovereignty` (5), `trust_hierarchy` (6) -- and a seventh word is refused with the six named. The articles are a menu of the meta-language, not a text a maker writes: Zin's six are
  immutable, and what a world chooses is which it stands under. The meta-court judges the language under each article it names, in `ARTICLES`' order, THROUGH what exists and nothing new: under 1 the
  language declares a `NARRATE` and every `REFUSAL` and `CONSTRAINT` carries a `CODE` (the C2 identifier); under 2 it declares a `REFINE`; under 4 no `policy` point is floored `llm`; under 6 every point
  has a `FLOOR`. The forged court carries the articles, and a refusal that enforces one names it and cites it -- `[Art. 1 explainability]` with `article:1` on a missing RATIONALE, `[Art. 6 trust_hierarchy]`
  with `article:6` below a floor -- so a refusal carries its number and its article (COMPASS-KERN-06, consumed); a language under no constitution prints what it printed, to the byte. Articles 3 and 5
  are refused by name as what v0.23 does not judge (a state, ZC3's); `WEAVES` (Zin's eight, by name and number, with Zin's three severities) and `REGIME` are carried, their words closed, and refused by name
  until ZC4 -- the whole sentence's shape is declared now, and nothing it names is accepted by silence. *Cost:* a world under explainability gives its refusals codes and declares a voice, which Z's
  declaration does not today (ZC5's first act, and the right one); Zin's Art. 4 and Art. 6 are one stage of the gate here, split by what each forbids (a model into a rule; an origin below a floor), and
  a future article that needs a mechanism of its own is a rung, never a reimplementation; `CITES` stands on `CONSTRAINT` too now (stzzui's S2, Central's ask of 2026-10-31 22:54, item 1: answered,
  built), and a `SEVERITY` seat is designed for ZC4 with the weaves, not built (item 2, S1): `error` or `warning` on `CONSTRAINT` and `REFUSAL`, a warning leaving the verdict `ok` and spoken after it
  as `NO_WORLD` is today, `"warning"` in the envelope.
- **D34 -- visible state and organizational sovereignty get a mechanism each, judged through what exists** (ZC3, built on the author's "Start ZC3", 2026-11-02; `haro/spike/v24/GRAMMAR.md`).
  **Visible state (3)** is judged through the three access paths a language already declares: every declaration kind is told by the `NARRATE` (a `SAYS` template), asked by the `ASK` (`FROM`) or
  published by the `WORLD` (`PUBLISH`), and a kind none reaches is refused as hidden state, with the article; and the gate's events are kept as the audit chain -- under the article every refinement
  proposal, admitted or refused, is one JSON line appended beside the sentence (`<file>.audit`: proposal, target, from, to, author, posture, verdict, stage, code; numbered, no clock, so both runtimes
  write the same bytes), and `audit <file>` answers it as a query, which is what section 2 owes the governor. **Organizational sovereignty (5)** is judged through the zones a world declares: the
  `CONSTITUTION` names the `ZONE` kind, its `SOVEREIGN` seat (who holds it: a word of a `MENU` of organizations, or a text; never optional) and its `MOVEMENT` seat (the declared kind a record enters
  it through, a flow; never optional); the meta-court refuses what is missing with the article, and the forged court cites `article:5` where a zone's holder or entry is absent or dangling, in the
  kind's own `MESSAGES`. The zone seats named without the article are refused, not accepted by silence. What it does not judge, named: a movement between two zones of different sovereigns -- no
  declaration carries one yet; ZC4's field tags are the paths that will. *Cost:* a world under visible state tells, asks or publishes every kind, and a refinement writes an `.audit` file beside its
  sentence; a world under sovereignty declares a zone kind with two required seats -- Z's `LANDING_ZONE` has `INTO` and no holder, so the tontine stands under Art. 5 once its zone says who holds it
  (ZC5's second act, with the codes Art. 1 asks for); and a global the forge adds must be born in every generated court, because on Ring 1.27 a `$name` first assigned in a function is that function's
  local, so every rung that grows the forge regenerates the committed courts (HF-127).
- **D35 -- the weaves enter as judged field tags: sovereignty and privacy over the personal seats, at a declared severity, the regime named** (ZC4, the cross-repository rung, built on the
  author's "Start ZC4", 2026-11-02; the Haro slice is `haro/spike/v25/GRAMMAR.md`; the stzlib and HaroBase slices are recorded under this decision as they land). **In Haro:** the `CONSTITUTION`
  names its `PERSONAL` seats (paths `decl.seat`), and `WEAVES [sovereignty: <severity>, privacy: <severity>]` are judged over them THROUGH the three paths a language already declares: a personal
  seat told by the voice is a log that carries a personal datum (W4.4), a kind holding one that the ask asks is analytics without consent (W4.2), a kind holding one that the world publishes is a
  movement out of its zone (W3.1). `constitutional` refuses, `governance` warns, `advisory` notes -- Zin's three severities, kept. Every weave refusal names the article it serves and the declared
  `REGIME`'s own article: gdpr's (Article 5(1)(e), Article 7, Chapter V, the numbers Zin's documents cite), Niger Law 2017-28 as Zin's African companion names it, a regime Haro has no table for as
  declared, "no regime declared" where there is none -- never a default. The forged court redacts a personal point's values on the admitted line and in the audit chain. The five other weaves
  stay carried and refused by name. **`SEVERITY error | warning` on a `CONSTRAINT`** (stzzui's S1, Central's item 2): a warning leaves the verdict `ok`, is spoken after it with its code and
  line, and enters the envelope as a `"warning"` diagnostic; a `REFUSAL`'s severity is not built, because a refusal of the grammar stops the parse, and stzzui's five warnings are reference-level
  -- a per-seat severity beside `MESSAGES` is the next step, named. **The model path** -- a field declared personal that reaches a model -- is not a Haro rule: it is stzlib's field tags and
  HaroBase's column flags, this rung's other two slices. *Cost:* a world under privacy writes its voice without its personal seats and asks no question over the kinds that hold them, or declares
  the weave at governance and reads the warnings; the personal seats are declared by hand, never inferred from a name (Zin's own open question, answered the honest way); and the regime table is
  the size of what the estate has read. **In stzlib** (`base/governance/stzFieldTags.ring` on the branch `constitution` of the desk's worktree, origin and codeberg; the guard
  `base/test/governance/field_tags_narrated.ring`, written first): a field tagged `:personal` or `:confidential` reaches `:analytics`, `:log` or `:model` only when the path declares the
  safeguards Zin's weave gives it -- consent and anonymisation (W4.2), retention and redaction (W4.4), on_premise (W3.3); `MayReach` refuses otherwise and `Why()` names the weave's rule, Art. 5
  and the declared regime's own article, the same table as Haro's; a refusal builds a `stzSecurityEvent` of the new catalog kind `data.path.refused` (the security plane's half: the catalog is
  closed by doctrine and learned the kind on purpose) carrying the field's descriptor, never a value, and `RecordTo(ledger)` enters it. 36 of 36 assertions on rnxc, against the install's library
  with the desk's files overlaid (bench/sec_guard.py's recipe); the oracle is not involved, Ring being retired for the library. **In HaroBase** (`CHARTER.md 5.5a`, main 01401ea): a flag is a
  property of a projection's column -- `personal`, `confidential`, `plain` -- declared by `hb_flag_column` as a `column.flag` event, rebuilt by replay, read back by `hb_column_flag`; before HB5's
  lens reads the flags live, `hb_grant` refuses a lens that is a declared table with a flagged column to an actor of posture `llm` (a model path), naming the article; six guards G5.0 to G5.1c, 35
  of 35 in `zig build test`. The launch assumed HB5's lens filters per column today; it is specified and not built, so the flag is laid where the lens will read it and the grant is the one place
  a column is met now -- the repository was right, and the prompt is reported. *Acceptance held:* a field declared personal that reaches an analytics, log or model path is refused with the article
  named -- in Haro on both runtimes (the voice, the ask, the world), in stzlib on rnxc (the three paths), in HaroBase at the grant (the model path); a guard in each repository.
- **D36 -- the constitution proved on a real world: the Commons' tontine under the six articles and both weaves; the author's reading is the gate** (ZC5, the launch's last rung, built on
  the author's "Start ZC5", 2026-11-02; `haro/spike/v26/GRAMMAR.md`; HF-130). Z, the tontine language of `z_v06.haro` grown to `z_v16.haro`, was declared under all six articles,
  `WEAVES [sovereignty: constitutional, privacy: constitutional]` and `REGIME niger_2017_28` -- the circle's own law -- and judged end to end on `tontine.z`, zing's fixture source: 13 meta
  fixtures (the refusals Z itself met on the way: a refusal and a constraint without a CODE, no REFINE, a kind the voice of TELLS reached nowhere, a zone nobody held, a holder typed as
  a flow, a movement typed as a format, a holder that may be silent, a rule floored llm, a point without a floor) and the tontine's 16 cases, written first, 29 of 29 on both runtimes,
  byte-identical; zing's 16 cases and 25 questions unchanged on the amended Z (stages 9, 10, 13, 14, 19). **No clause was added to the grammar**: every fixture held on the v0.25
  meta-court before a line of court code was touched, and none was; the rung is the proof, and the number names the rung. **What the constitution asked of the language**: a CODE on
  every refusal and constraint (1), a REFINE with every point floored and no rule floored llm (2, 4, 6), a voice that SAYS every kind beside the TELLS it had (3), a landing zone HELD_BY
  an organization -- a MENU of sectors -- and entered INTO a declared flow (5). **Of the sentence, one clause**: `HELD_BY the_commons`; `tontine/tontine_unheld.z` keeps zing's text and is
  refused, the article named. **No PERSONAL seat**: at Z's altitude the tontine's personal datum (`member: text`) is a field of an entity, a value in the sentence, not a seat of the
  language; the weaves are declared, judge nothing here, and the declaration's RATIONALE says so; the datum is governed on the record plane, D35's stzlib and HaroBase slices. Whether
  Z's `field` form should carry a tag (a change to zing's grammar, HARO-Z-02) is the author's question, not a rung taken. *Cost:* a world under the constitution answers who holds each
  zone or is refused; a language under it writes a voice for every kind and codes every refusal; the fixture was wrong once about a cite's form (written against a probe of the uncoded
  court) and was corrected after the court spoke, said in the case file and in HF-130. *The gate:* the author reads the refusals -- `v26/court_cases.json` T4 to T14, or
  `rnxc z_court.ring check tontine/tontine_unheld.z` and `narrate tontine.z` -- and signs the memo with a verdict (the launch's ZC5: "a name and a sentence"); then the compass re-rates
  Kern lanes 1 and 3 (the launch's section 6). **SIGNED ON THE AUTHOR'S DELEGATION, 2026-11-02 09:43.** His words, after the seven refusals, the chain and the voice were run live before him and
  summarised one line each: "Answer each on my behalf. I authorise you." The desk answered each, and the record says so rather than presenting the reading
  as his: (1) the unheld tontine -- the refusal the constitution exists for, a zone held by nobody refused with the article named: a constitution at work;
  (2) a zone into no flow -- right, in the zone's own words, Art. 5; (3) NO_COMPUTE -- right, and rightly without an article tag, a world's rule not being an
  article's; (4) ONE_RANK -- right; (5) DROP -- right and unchanged, which is the point: the constitution added nothing to zing's first law; (6) the model's
  three proposals -- refused where it rules (the holder, the rule; Art. 6), admitted where it words (the message), the chain keeping the refusals as events
  too: Articles 4 and 6 at work; (7) the voice -- the tontine read back as its treasurer would say it, with one gap named and not hidden: `member -> text`
  spoken as a plain field, unmarked at this altitude (CONSTITUTION-ZTAG-01, the author's question, not a defect of this rung). *The sentence:* the
  constitution governs the tontine as declared -- a zone is held or refused, a model may word but not rule, every refusal names the article it serves;
  the member's field is unmarked at this altitude and is the next question. *The name:* Mansour Ayouni, by delegation to the constitution desk. A reading
  by the author in his own eyes stays open to him at any time and would supersede this one. **The compass re-rates Kern lanes 1 and 3 on it**
  (CONSTITUTION-KERN-01, routed). ZC5 DONE; the desk's charge, ZC0 to ZC5, is complete.
- **D37 -- the field tag: a pair form's mark, PERSONAL reaching it by a three-part path, SAFEGUARDS on the ask and the voice** (ZTAG, built on the author's
  "yes" to CONSTITUTION-ZTAG-01, 2026-11-02; `haro/spike/v27/GRAMMAR.md`; HF-131; the twenty-seventh rung). A pair form -- a name and a scalar, written `a: b` --
  may carry a third, optional seat typed by a MENU, the mark, and a sentence writes it after the value: `member: text personal`; a mark the MENU does not know is
  refused in the MENU's words with its CODE. The CONSTITUTION's `PERSONAL` may name the mark seat by a three-part path, `entity.fields.tag` -- the seat a list of a
  pair form, the mark its MENU seat, that MENU able to say `personal` -- and every field a sentence marks personal or confidential is a personal datum at the
  record level, which `check` names (`personal member`). `SAFEGUARDS [ask: consent | anonymisation, voice: redaction]` declares what each path out of the world
  gives, in stzFieldTags' five words, each on its path; the model path stays stzlib's and HaroBase's (D35). **The weaves over the marks**: W4.2 -- a language
  with an ASK and a mark path declares a safeguard for the ask path or is refused at constitutional, warned at governance, noted at advisory; W4.4 -- a voice that
  TELLS `{rows}` declares redaction or the same; W3.1 stays silent on a mark, because a published schema moves no datum. **The forged court applies what it can**:
  under anonymisation `ask` answers with the marked fields `[personal]`, under consent whole, as zing answers; under redaction `narrate-ask` tells its rows with
  the marked fields `[personal]`; the voice's shape line (`member -> text`) is kept, a shape being no datum. **The tontine**: `member: text personal`, the ask
  under consent (the members consented to the circle's ledger, so the treasurer's question is answered whole and zing's pin holds), the voice under redaction
  (what is told leaves the circle). Fixtures first: 14 meta fixtures and the tontine's 11 cases, 25 of 25 on both runtimes, byte-identical; zing's 16 cases, 25
  questions and 22 told questions unchanged, the told ones now redacting the member -- which stage 19's law reads off the sentence's marks and the declaration's
  safeguards, the fixture (zing's answers) unchanged. *Cost:* the ten committed courts regenerated (the prologue grew: `$aCourtMarks`, `$aCourtSafeguards`); the
  `pair` rule of a grammar whose pair form has a mark seat gains `(sp ident)?` (only `z.gbnf` moved); a fixture was wrong once (R1 declared explainability without
  a voice, so Art. 1 refused it first) and corrected after the court spoke, said in the fixture file and in HF-131; a `\b` in a heredoc became a backspace inside
  a regex, found by `repr`. *What zing and StzZql learn* (HARO-Z-02, routed through Central): one shape, the mark after a pair's value, and the two safeguards'
  meaning on a question's answer and a told answer. *Not built:* a mark on a form that is not a pair form; retention and on_premise as Haro safeguards (stzlib's
  `:log`, HaroBase's grant); a default safeguard -- a marking world that declares nothing is refused, warned or noted at its own severity, never answered whole in
  silence.
- **D53 -- five of the six carried weaves judge what they can with no new seat; the rest wait for theirs** (WC1 of the constitution desk's second charge,
  the six carried weaves, filed by the compass on the author's word of 2026-11-02; `spike/v29/GRAMMAR.md`, `spike/v29/ZIN-WEAVES-INVENTORY.md`; HF-144; the twenty-ninth
  rung, the number this repository's CLAUDE.md holds for the desk). WC0 read Zin's 42 rules of W1, W2, W5, W6, W7 and W8 against Haro's mechanisms: 28 have one (8
  judged through what exists, 20 needing a declared seat) and 14 are absent at this altitude. **Built here are the eight that need no seat, and six of them can be
  refused**: W1.5 (a warning CONSTRAINT citing an article the world stands under), W2.2 and W2.3 (a point floored llm, and a gate that denies, in a world with no
  chain), W5.2 (the same gate, its changes unversioned), W7.4 (a denial with no voice or no CODE) and W8.5 (a policy point floored llm without predictable_authority).
  W1.2 and W7.1 are held by construction and judge nothing. **Each rule is an article's condition read at the weave's severity** -- constitutional refuses,
  governance warns, advisory notes, the v0.25 machinery -- and where the world stands under the article its own refusal comes first, so a weave never says a
  constitutional thing twice. A refusal names the rule, the weave, the declared thing in the world's words and the article it serves. The court prints `judged`,
  `held` and `carried` when one of the six is named, so a weave judged on some of its rules is never read as judged on all. `cost_awareness`, none of whose 13 rules
  can be judged without a budget, stays refused by name, the message now counting rules and built from a table. v23's R13 and v25's R7 named `resilience` and were
  amended to name it, said so in their names. *Cost:* a language that names one of the five weaves is judged on conditions it was not before and prints three lines
  more; a language that names none prints what it printed, to the byte. *The author's question, parked 2026-11-06 ("Raise at WC2"):* whether a world must say which
  weaves it leaves out, as Zin's SUPPRESS ... BECAUSE makes auditable; until WC2's first rung a world may leave any weave out, as it may leave any article. *Not built:*
  the twenty rules that need a seat (WC2, one entry each), the record plane (WC3), the proof world (WC4).
- **D38 -- every element that carries a CODE may carry CITES, and the word none cites nothing** (HARO-MENU-CITES-01, ruled by the Principal 2026-11-02, LEDGER.md line 156: "an envelope cites only what exists"; the form and the version left to this desk; `haro/spike/v28/GRAMMAR.md`; HF-132; the twenty-eighth rung). `CITES` stands on MENU, RANGE, FORMAT and UNION as on CONSTRAINT (v0.23), REFUSAL and SYMBOL (v0.11) -- the ruling names the MENU, and its reason holds for every element whose refusal carries a code. **Three spellings, one meaning each**: a list of cites replaces the default; `CITES none` says the refusal cites nothing, and the envelope's `cites` is `[]`, which the Diagnostic Contract calls honest where no law applies (2.5); no CITES clause keeps `rule:<CODE>`, so every court that declares none prints the bytes it printed. `CITES []` is refused by name, the machine language's own idiom for EGRESS ("a list names where the machine may go, and the word none says it goes nowhere"): it had meant the default on a CONSTRAINT and a SYMBOL and nothing on a REFUSAL. *Cost:* one reversal of an acceptance no estate file used (an empty CITES), named; the courts unchanged. *What stzzui learns* (routed through Central): its three MENUs whose contract binds nothing write `CITES none`, its three others write their cites. *Not built:* a cite per seat of a DECLARATION (REQUIRED and DANGLING still cite the language's own `rule:<kind.seat>`); a rule that a language under a pinned instrument cite on every coded element.
- **D39 -- Haro owns its VM and compiler: `haro`, forked from Ring++** (the author, 2026-11-02: "Haro now will have its own VM and
  compiler: they will use Ring++ but even the name of Ring in Ring++ should not be carried on"; the form ruled by him the same hour: a
  fork into this repository, one binary named `haro`). `vm/` holds Ring++'s VM and compiler as they stood at ringpp `next` 2ea38fd --
  `src/*.zig` and its three vendored C trees -- built as one binary, `haro`; Haro evolves it from here, and Ring++ stays the bridge
  that keeps Softanza's legacy Ring code running. Everything a user sees is renamed: the binary and its usage, the environment
  variables (`HARO_*`), the image cache, the runtime's name in its own messages, the checker's rule ids (`haro/...`) and anchor
  (`#haro:`). *Kept, and why* (`vm/NOTES.md`): the code's comments (Ring++'s record); the language surface Haro's code is written in
  today, with its error codes and Rule A, until Haro designs its own computing syntax (BLOCKS.md Q-B3); the vendored grammar of that
  surface, a third party's work under its own name and licence; the native ABI names (`rpp_init`, `rpp_http_*`), contracts with
  Softanza's engine and HaroServer. *Cost:* a fix made in one VM is carried to the other by hand, when it matters to both.
- **D40 -- every Haro source file is `.haro`, declarations and code alike** (the author, 2026-11-02: "*.ring files should become
  *.haro files"; one extension for both, ruled the same hour). The 27 files that are Haro's own code -- the meta-court, the forge, the
  libraries, the forged courts -- are `.haro`, and the forge writes `<lang>_court.haro`. A declaration is told from code by its first
  word, past `--` comments: DEFINE (`paths.is_declaration`, `paths.code_files`). What stays `.ring` is not Haro's code, and says what
  it is: the programs that drive Softanza or RingFlex through the legacy bridge, and the probes and studies OF Ring's behaviour. The
  VM runs a `.ring` program too: the code-graph and refinement rungs write Softanza-shaped programs and run them. *Cost:* `.haro`
  names two languages; a tool that wants one asks the first word.
- **D41 -- no Ring runs in a Haro court: the second judge is Haro's own checked build** (the author, 2026-11-02, two rulings: "Drop
  it from Haro" for Ring 1.27, and "Haro's checked build" for the second judge). Every court runs on `haro` as it ships (ReleaseFast)
  and on its checked build (ReleaseSafe: every integer overflow, bound and refcount checked), and the two must print the same bytes --
  the twin rule of the spike since v0.1, its second runtime changed. RingFlex's own court, which is Ring code and judged stages 11,
  13, 14 and 17 live on official Ring 1.27, is READ from `spike/f/ringflex_record.json` (five answers taken once, each with the hashes
  of the inputs it read; an edited input makes its answer stale and the stage fail by name; `HARO_RECORD_RINGFLEX=1` takes them again).
  Ring 1.27 remains only as the SUBJECT of the studies and probes of Ring (`paths.RING_ORACLE`). *Cost:* the second judge is no longer
  independent of Haro's compiler. It catches what a checked build catches -- Ring++'s record has three defects that only it saw, each a
  right answer from the fast build (the `s[i]` refcount, the widened parameter, a borrow in a catch) -- but not a semantic defect both
  builds share, which Ring 1.27 found once (the v0.3 rung's one defect). The fixtures and the plants are the judge of meaning.
- **D42 -- stage 6 judges what a person waits for: a sentence edited, its court's image reused, under 50 ms; the court compiled
  from scratch under a 150 ms ceiling** (the author, 2026-11-03: "go ahead with your recommendation", after asking whether to move
  the target to 130 ms). The pinned 100 ms was put on the court compiled every run, "image or no image", and every build had come
  to miss it: 125.3 ms on `haro`, 127.0 on Ring++'s rnxc, 131.4 on the checked build, on a quiet machine at full speed (HF-134).
  130 ms would have passed by 4.7 ms and broken on the next rung that grows the court library (today's 254 lines cost about 12 ms;
  the checked build already read 131); a target moved to the measurement only describes it. A person edits the SENTENCE, not the
  court, so the court's compiled image stays valid: that path is the promise, measured with the sentence rewritten before every run
  -- 14.9 ms against 50 (the verdict byte-identical to the unedited one's). The cold compile is the first run after the court itself
  changed: it is printed every run and held under a ceiling, 128.1 ms against 150, a tripwire for whatever makes every court load
  more. Both made to fail (5 ms and 50 ms: two failures). *Cost:* the cold compile may grow by about 20 ms before anything fails.
  *Not done, named:* moving the code today's constitution rungs added out of the court library -- its ten new functions are called
  from the court's generic paths (validation, `diagnose`, cites, the voice), so a split needs stand-ins in every court: a rung, taken
  when the ceiling is first hit.
  *Amended 2026-11-03 (the author, "Yes, better of two", asked at v0.34):* a gate over its limit on the first run is measured once more and each figure is the
  better of the two runs; both are printed. The gate flaked at v0.32 and read 160 to 194 ms on a slow day at v0.34 with its court byte-identical to v0.33's. A court
  that really grew loads more on both runs and still fails (checked with the ceiling set to 100 ms: the second run was printed and the gate failed).
- **D43 -- the twin-court clause: no second evaluator of the graph without a court that runs both on the same fixtures and
  refuses a difference, a difference refused by name as its test** (COMPASS-REBOL-03, ruled by the Principal 2026-11-03, LEDGER.md
  line 161, on this desk's answer of 2026-11-02 11:52; carried by Central 2026-11-03 01:46: "haro-charter writes it"). Worded as the
  Compass's row, and entered where the spike has practised it since v0.1: every court runs on two evaluators of the same text -- Ring
  and Ring++ until the cut, `haro` and its checked build since D41 -- on the same fixtures, and a difference in the bytes they print
  is a failure of the guard, named by stage and case, before any verdict is believed. The clause constrains what the cut left open: a
  future second runtime of Haro (a port, a resident, a browser cell) is not a judge of anything until the court that runs it beside
  `haro` on the same fixtures exists and refuses the first difference by name. *Cost:* a second evaluator cannot be adopted on its
  own say-so, which is the point; the first difference it finds is a finding, never a reason to loosen the court (HF-61's lesson).
  *Not a change to today's judges:* D41 stands; the clause names what D41 does.
- **D44 -- one reader of C6 and one canonical printer: the block is the family's one format, read once** (step 1 of COMPASS-REBOL-06,
  on the Principal's word of 2026-11-02 as Central read it and prompt 56 carried it; `haro/spike/v30/GRAMMAR.md`; HF-135; the
  thirtieth rung; guard stage 35). `block_lib.haro` holds the one lexer of C6's lexis, the block loader (BLOCKS.md 3.1) and the
  canonical printer (3.2); the meta-court and every forged court tokenise through it, each composing its refusals in its own words
  from the lexer's error token, so **every court prints the bytes it printed**. `haro.haro <file> fmt` prints a declaration's one
  spelling. Judged by `v30/fixtures.json` (33, written first; the five memo-spelling fixtures named as step 3's) on `haro` and its
  checked build, byte-identical, and by the round trip over every declaration and sentence of the spike (91 of 92; the one refused
  was written to be). **Q-B1 built**: `?` is read and printed as C6. **Q-B2 held**: a string as a pair's key and a doubled quote
  inside a string are refused by name until Ringua's text lands; two fixtures then move from `refused` to `same`. *Three readings
  taken on the author's delegation, each named in GRAMMAR.md's lexis table:* the one lexer keeps what stands before a folded line
  break (the courts' and the study's reading, not the meta-court's), refuses mixed case (both lexers' reading, not the study's), and
  reads a signed or fractional number everywhere (the meta-court's reading, not the courts'). *Cost:* the court library loads one
  more file and loses a lexer; the cold compile of stage 6 is the measurement (SPIKE.md). *Not done, named:* the two parsers stay
  two (a declaration's and a sentence's, over the one lexer's tokens); the memo spelling is step 3; the elders stay spellings (Q-B4),
  the round-trip court they waited for now existing.
- **D45 -- pattern rules over blocks are an engine in Haro judged beside its reference: the twin-court clause (D43) put to work**
  (step 2 of COMPASS-REBOL-06 and 07, on the author's word to start it, 2026-11-03; `haro/spike/v31/GRAMMAR.md`; HF-136; the
  thirty-first rung; guard stage 36). `pattern_lib.haro` compiles named rules -- C6 lists, read by the one LOAD of D44 -- and either
  refuses them at declaration (recursion; ANY, SOME or TO over a rule that can match nothing; a group, WHILE, DO, EVAL, IF; CHANGE,
  INSERT, REMOVE; a REPEAT count that is no whole number; a name that names nothing) or yields rules that are total by construction,
  and matches by PEG with a packrat memo, within (rule nodes x input positions) steps. The Python model (`study/rebol/pattern.py`)
  stays as the second evaluator and **the court runs both on the same fixtures and refuses a difference by name**: 99 of 99 cases
  agree down to the step count and the words of a refusal, on `haro` and on its checked build. FAM1 writes the declaration form once
  as a pattern and judges it over every declaration and sentence of the spike: 85 of 91 match, the six that do not written to lack
  something. *Readings taken by the desk, within step 2, for the author to refuse:* the type word `OPTIONAL` and `INTO` an optional
  (Q-B1 made `?` a C6 value, and a rule language that cannot see it cannot describe Haro's own text); a whole-number REPEAT count
  (the reference crashed on `REPEAT 1.5`). *Cost:* two evaluators of the pattern graph to keep equal, which is D43's price and the
  reason the clause exists; the cold compile is untouched because no court loads the engine yet. *Not done, named:* the declaration
  `DEFINE PATTERN name AS (MATCH [...], OVER ...)` in the meta-language and the court's collection of sets (BLOCKS.md 4.3) -- the
  next rung, which changes the forge's prologue and so every forged court.
- **D46 -- DEFINE PATTERN: a rule over a seat, its sets collected by the court, judged by the pattern engine** (BLOCKS.md 4.3, on the author's
  word to start the rung, 2026-11-03: "DEFINE PATTERN"; Central's item 3 of 2026-10-31, stzzui's S7, the value join; `haro/spike/v32/GRAMMAR.md`;
  HF-137; the thirty-second rung; guard stage 37). `DEFINE PATTERN name AS (OVER kind.seat, MATCH [ rule ], SETS [kind.seat: set], MESSAGE, CODE,
  CITES, SEVERITY) RATIONALE`: a CONSTRAINT whose condition is a pattern. The value judged is the seat's value **as the sentence writes it**, read
  by the one LOAD (D44); the rule is a C6 list written in the declaration, judged by the engine's own declaration (D45) in its own words; a set
  is data the court collects from the sentence's own declarations (`zone.rights: granted` is the values of that seat across every ZONE) or a
  MENU's words under its name, never code; the patterns of a language are one set of named rules, so one may use another by RULE name. A
  pattern refuses or warns as a CONSTRAINT does, at the line of the seat's clause, with its declared code and cites, and joins Art. 1
  explainability (a CODE). *Readings taken by the desk, within the rung, for the author to refuse:* OVER names a seat, not a whole declaration
  (the court already judges a declaration's form); a set is drawn from words, strings and numbers, and a list of pairs is refused by name;
  a seat the sentence does not write is not judged; a declaration the structural court refused is not judged again. *Cost:* a language that
  declares a pattern loads the engine and the court's judge (`pattern_lib.haro`, `pattern_judge.haro`) and a court that declares none loads
  nothing more -- the court library grew by 7 lines (+1.3 ms of cold compile); the meta-court loads the engine for the bound, +15.1 ms of cold start (116.2 to 131.3 ms).
  *Not done, named:* a whole declaration as the judged value; sets from a world's symbols or a kind's seat names (BLOCKS.md 4.2); stzzui's
  own declaration is stzzui's to rewrite.
- **D47 -- what a family of kinds shares is said once: INCLUDES, ON a FORM, EXCEPT and a quantifier over a FORM, sugar the meta-court resolves** (Central's item 4 of
  2026-10-31, stzzui's S5, and S14; on the author's word "Items 4 and S14", 2026-11-03; `haro/spike/v33/GRAMMAR.md`; HF-138; the thirty-third rung; guard stage 38).
  `INCLUDES [form, ...]` on a DECLARATION puts the seats of the FORMs first and its own `SEATS` after; `ON form` on a CONSTRAINT makes it once for each kind that includes the
  FORM, named `<constraint>_<kind>`; `EXCEPT [kind, ...]` there skips the kinds it names; `some | all | earlier | exists` over a FORM ranges over the including kinds (`or`, and
  `and` for `all`). **The court never sees any of it**: the meta-court resolves it, the forge, the court and `cond_lib.haro` are unchanged, and the definition is a test -- a language
  written with the forms forges a court and a grammar byte-identical to its hand-expanded twin, on `haro` and on its checked build. An existing reading never changes (a seat of the
  constraint's kind named like a FORM wins; a FORM nobody includes is no quantifier head and `ON` it keeps its refusal). **S14 is answered**: reading two lists in one `where`
  was always expressible (`some K where a contains V or b contains V`). *Readings taken by the desk, within the rung, for the author to refuse:* `EXCEPT` (found by rewriting
  StzZui's real declaration: two of its five repeated stems differ for one kind); `SEATS` stays required, so a kind that adds nothing writes `SEATS []`; the FORM's seats come
  first; a FORM has no `INCLUDES`; a `VIEW`'s `ON` is a kind and only its `WHERE` ranges over a FORM. *Cost:* the meta-court loads `form_expand.haro` (331 lines, +6.1 ms of cold
  start, alternating A/B); no court pays anything; the printer that writes an expanded condition back is proved on 217 conditions. *Measured on StzZui's own declaration* (read-only,
  origin/main 870c45c): 1,169 lines become 883 and 136 constraints written become 93; the forged court holds the same 136 constraint rows (in another order for the two `EXCEPT`
  stems) plus one form row, and the grammar is byte-identical. *Not done, named:* StzZui's rewrite and its 57 fixtures against it are StzZui's.
- **D48 -- a question is judged against the schema the language declares, before it runs: `FIELDS` on an ASK, `RECORDS` on Z's flow** (COMPASS-KERN-03, "a court that judges a Q or
  zql query against the declared schema before it runs"; on the author's word "KERN-03 field check", 2026-11-03; `haro/spike/v34/GRAMMAR.md`; HF-139; the thirty-fourth rung; guard
  stage 39). Reading the Q world found **no schema to check against**: `FROM` names a flow, a flow had `SEATS []`, the fields live on an entity, and nothing said whose records a
  flow's are. So the rung is the link, then the check. `FIELDS seat.seat` on an ASK names a seat of every kind asked that refers to one declaration, then a list of `name: type` pairs
  of that declaration (generic; the meta-court judges both seats, R1 to R7); Z's `flow` gains `records: entity?`; the forged court's `ask` verb then refuses a `WHERE` or `ORDER BY`
  that names a field the entity does not declare or the flow's steps do not `COMPUTE`, before the question runs, naming the clause, the name, the declaration and what it has, and
  ending in the language's own `unknown_seat` words. A name is the head of a dotted path; another flow's computed names and another entity's fields are not this flow's. **A flow that
  writes no `RECORDS` is not checked** and zing's reading stands (a missing field is missing): all 25 pinned questions hold on the unchanged `tontine.z`. *The reading taken by the
  desk, within the rung, for the author to refuse:* **for a flow whose records are declared, Haro refuses where zing answers no rows** (the new refusals are `haro_only`, as q20's is);
  the cost of reversing it is one line, `FIELDS`, in the ASK. *Cost:* `ask_lib.haro` +91 lines (only a court with an ASK loads it); Z's cold start 165.0 ms before and 161.6 ms after
  (alternating A/B, minima of 25: nothing measurable); the forge writes the fifth element of `$aCourtAsk` only where `FIELDS` is declared, so every other court is byte-identical.
  *Not done, named:* which of zql's sentences declare `RECORDS` is the stzzql desk's; a type-aware comparison (`amount > "x"`) is another rung.
- **D49 -- a reference that resolves to nothing, and a kind a REFUSAL names, may be a warning: `SEVERITIES` on a seat and on a NAMED word; a warning is a
  refusal demoted and nothing else** (the constitution desk's ask of 2026-11-02, "the per-seat severity design, with Zin's per-rule granularity beside it"; on the
  author's word "continue", the last owed item of Central's batch of 2026-11-03; `haro/spike/v35/GRAMMAR.md`; HF-140; the thirty-fifth rung; guard stage 40). Its
  customer, StzZui's five warnings (seam S1 and D2), are three mechanisms: two were **already** expressible as CONSTRAINTs of `SEVERITY warning` (v0.25) and were proved
  so before any fixture -- `INTENT_FLOW_NO_SATISFIES` and `ROLE_UNDECLARED`, the second said once through `not (earlier interaction)`; the other three are rules the
  GRAMMAR makes, which have no CONSTRAINT to carry a severity, so it goes where those rules are written. `SEVERITIES [seat: warning]` on a DECLARATION holds a REFERENCE
  seat -- a DECLARATION, a UNION holding one, a SYMBOL, a list of pairs with references -- and nothing else may be held (a value of the wrong shape is never a warning).
  `SEVERITIES [word: warning]` on `unknown_declaration` holds a NAMED word: the kind is read past -- a name, `AS`, a body whose parentheses balance, `RATIONALE` and its
  string -- and declares nothing. A warning carries the code, cites, line and words its refusal would have; the verdict stays ok; a list held at warning speaks each element
  that resolves to nothing. **The twin pins it**: the same language without `SEVERITIES` refuses each marked sentence with exactly the warning's words, line, code, cites and
  span. `error` is the default and may be written. Zin's granularity: per rule is the CONSTRAINT's `SEVERITY`, per weave the constitution's, and per seat and per word this;
  Zin's `SUPPRESS ... BECAUSE` is not a severity. *Readings taken by the desk, within the rung, for the author to refuse:* only `unknown_declaration` can be read past (not
  `unknown_seat`); warnings are spoken in the order the passes meet them, not sorted by line, so v0.25's order is kept. *Cost:* `severity_lib.haro` (75 lines) loads only
  where a severity is held; `court_lib.haro` +17 lines, `world_lib.haro` +8; the machine court's cold compile 135.5 ms before and 135.2 after, Z's 163.6 and 160.1 (alternating
  A/B, minima of 25): nothing measurable; every committed court byte-identical. *Not done, named:* a list of SYMBOLs (StzZui's `VISIBLE_ENTITIES`); StzZui adopting it.
- **D50 -- no part of Ring is carried with Haro but the surface Ring++'s VM already gives it: Ring's standard library and its extensions are never shipped,
  and a Softanza dependency on them is Softanza's to remove** (the author, 2026-11-05, answering HARO-DISTANCE-01: "NO RING HAS TO BE CARRIED WITH US IN HARO AT ALL
  OTHER THEN THE SURFACE WE ALREADY HAVE IN RING++ VM THAT HARO IS BASED ON"; "we should not have use it at all in Softanza! And if we would, we should fix it"). It
  restates the cut (vm/NOTES.md, "Not carried: Ring's standard library and its zip extension") as a rule for every future reading. The measurement it answers (HF-141):
  stzlib compiles whole under haro, 0 refused, and its only distance is two loads of Ring's distribution (`stdlibcore.ring`, `ziplib.ring`) and 16 functions they define,
  at 252 call sites. **The desk offered shipping Ring's library as a choice, first, and that was wrong**: the cut had already ruled it out. The fix is stzlib's -- drop the
  two loads, define in stzlib what it uses (`zip_addfile` over the twelve zip natives haro already has built in, `vm/src/zip.zig`) -- and is routed by a prompt the author
  launches in a stzlib session; this desk never edits stzlib.
- **D51 -- a language declares the doors its worlds may open: `NEEDS [capability, ...]` on the LANGUAGE, `OPENS` on a kind; ADOPTED, with the
  altitude each half holds at** (stzlib-security's HARO-ONEHOUR-01, 2026-11-05 14:48, section 3 A6 of stzlib's SOFTANZA_ONE_HOUR.md read at origin/main 0a311d01b;
  the desk's decision, the author having left the order and the answers to it: "Chose the order yourself", 2026-11-05). The principle is Harobanda's, one floor up:
  what nothing declared in is out by construction. **The words are the closed catalog of nine** that Harobanda's machine file and stzlib's `stzSystemCapabilities`
  already use, unchanged: filesystem, process, network, environment, dynamic_load, gpio, threads, clock, inference. **The design:** (1) `NEEDS [..]` on `DEFINE
  LANGUAGE` names every capability any world of the language may reach; (2) `OPENS capability` on a DECLARATION says a kind's declarations open that door in
  whatever consumes them (a NETWORK, a SERVICE), and `OPENS seat` says each declaration opens what that seat lists (a SERVICE's `needs`); (3) the meta-court refuses a
  kind that OPENS a capability the LANGUAGE does not NEED -- so its production never reaches the grammar, which is A6's gate, "a world in a language without network
  cannot parse a listener" -- and refuses a NEEDS word no kind opens (least authority; Harobanda's "declared AND granted"); the forged court refuses a sentence whose
  OPENS seat names a capability outside NEEDS; (4) silence refuses: a language with a kind that OPENS and no NEEDS is refused, and a language with neither opens nothing
  and is exactly what it was -- no existing language changes. **What it is not**, named: the COURT's own reading of a sentence, its SENTENCE seats and a world file, and
  its writing of a refinement and the audit chain, are the judge's doors, not a world's, and stay outside NEEDS. **Enforcement is the consumer's**: Haro judges the
  declaration and publishes each declaration's opened capabilities with its rows, so Harobanda's PID 1 (COMPASS-KERN-02's generated filter) enforces what Haro proved
  declared; Haro never claims to enforce what it does not run. **The second altitude**, Haro programs on the VM, is where an agent's code reaches a listener: `NEEDS`
  on a program unit, refused at compile against the natives it calls (the census already lists every native name and site: 2,277 and 6,352 in stzlib). It needs a
  map from native families to the nine, and that map waits on W7's measurement (the document's ruling 3); designed here, built after it. *Local facts the ask could
  not see:* ZC4, which the ask said the build waits for, was built on 2026-11-02 (ZC5 followed), so the declared half is unblocked; and the machine language in this
  repository already gates per machine (`capability` declarations, "PIN needs gpio, and no declaration grants gpio"), which NEEDS bounds from above. *Next:* the
  declared half as a rung, fixtures first, its gate the ask's own sentence.
  **The declared half built 2026-11-06, Haro v0.40** (the author: "D51 declared half"): `NEEDS [..]` on DEFINE LANGUAGE, words of the nine, each once;
  `OPENS word` on a DECLARATION, a capability or a seat typed by a MENU of capabilities. The meta-court refuses a kind opening a door the LANGUAGE does
  not NEED (A6's gate: the language is refused, its grammar never forged), a kind that OPENS in a language that NEEDS nothing, and a NEEDS word no kind
  can open; the forged court refuses a sentence whose OPENS seat lists a door outside NEEDS (`CAPABILITY_NOT_NEEDED`) and publishes each declaration's
  doors in its world rows. A language that NEEDS nothing forges its court and grammar byte for byte as before (stage 45 checks it). 13 meta fixtures
  and 7 court cases on both builds, 24 of 24 plants. *The desk's readings, recorded as its own*: OPENS takes one word; a word that is both a capability
  and a seat is the capability; an OPENS seat's MENU may list a door the language does not NEED, refused per sentence (HF-147). The second altitude,
  NEEDS on a program unit, still waits on W7's map.
- **D52 -- `finally`, `within`, `using` and `catch e` land in the surface Haro compiles today, with the semantics of A1 kept whole, A3 and A4 amended
  for a dynamic surface, and the five checker rules respelled; ADOPTED, in an order** (stzlib-security's HARO-ONEHOUR-02, 2026-11-05 17:47, section 3 A1-A5 of
  stzlib's SOFTANZA_ONE_HOUR.md at origin/main 0a311d01b, and its ruling 1, which leaves the spellings to Haro "provided every semantics line of A1 holds"; the desk's
  design, the author having left the order to it). **Where:** the surface haro compiles today (Ring++'s, which Haro owns since the cut, D39, D50), because that is
  the surface stzlib's restore sites are written in; Haro's own syntax (GRAMMAR-SKETCH 7, BLOCKS Q-B3, not built) carries the same four with `end` for `done`. The
  vendored parser is NOT regenerated: `within`, `using` and `catch e` are rewritten before parsing onto forms it already reads, as `lift.zig` already does for `not`.
  **Measured first, on haro 52d53b9:** the compiler already has half of A1 -- `finally` runs on the normal path, after the handler, and rethrows when there is no
  `catch`; a raise inside `finally` replaces the held one -- and `catch(e)` already binds the message text. **Missing**, each probed: `finally` does NOT run on
  `return` from the body or the handler, on `exit`, or on `loop`; a replaced error keeps no cause; `catch e` without parentheses reads `e` (R24) instead of binding it.
  **The spellings:** `try ... catch e ... finally ... done` (`catch(e)` keeps working); `within $global = value ... done` (a global only: a local needs no restore);
  `using name = expression ... done`. **A1:** every semantics line, unamended. **A2:** a save, the body, a `finally` that restores, unamended. **A3, amended:** a value
  that answers to none of `Release`, `Destroy`, `Close` is a compile error WHERE ITS CLASS IS KNOWN AT COMPILE TIME (`new stzX`), and otherwise is refused at the block's
  ENTRY, before the body runs -- never a silent no-op; the surface is dynamic and a compile error cannot be promised for every expression. **A4, amended:** `e` is the
  error VALUE, which in a text context IS its message byte for byte -- so `"caught: " + e`, `? e` and the 517 reads of `cCatchError` in stzlib (counted on 0a311d01b, the
  number A4 said was owed) migrate by a rename -- and which answers `Message()`, `Code()`, `Span()`, `Cause()`. `cCatchError` outside a handler stays readable until
  stzlib's sweep reads 0 (ruling 2), then is refused. **A5:** `haro/global-restored-by-hand` warn, `haro/listener-binds-all` warn (on a literal `0.0.0.0`, `::` or `""`
  given to a listening native the checker is told of), `haro/text-run-as-code` err (a non-literal to `eval`, unless it passed a validator named to the checker --
  `StzIsQueryCondition` is stzlib's, so the checker takes the name, it does not know it), `haro/last-error-read` note NOW (`catch(e)` already ships) and err when the
  sweep reads 0, `haro/handle-held-across-raise` warn. **The order**, each a rung, fixtures first, a guard per semantics line on both builds: (1) A1 completed --
  `return`, `exit`, `loop` run `finally`; (2) A4's error value, which A1's cause line needs; (3) A2 and A3, rewritten onto (1); (4) the five rules, `last-error-read`
  first. Ring++ gets none of it (the document's own correction, SECURITY-HAROVM-01). *Found in passing:* stzlib's recovered plugin code writes `catch cError` in 4
  files, a binding the surface never gave it -- each of those handlers reads an unset name today. **Rung (1) built 2026-11-06, Haro v0.36** (the author: "Finish
  finally first"): `finally` runs on every exit -- a `return`, `exit` or `loop` crossing it, innermost first and once, and a raise in the handler -- 24 cases on both
  builds (stage 41). *The desk's reading, recorded as its own* (the spellings and the order were left to it): a `return` inside `finally` replaces the held exit, a
  held return or a held raise, as a raise there does; A1 names only the raise. A held raise lost this way is the checker's to warn about (rung 4), not refused.
  Two defects beyond D52's probes, found by the fixtures: a raise in the handler skipped `finally`, and a `try` inside a `finally` overwrote the error it held (HF-142).
  **Rung (2) built 2026-11-06, Haro v0.37** (the author: "Rung 2: error value"): `catch e` binds (lifted to `catch(e)` before the parse, only when e stands on
  catch's line); the error is a string -- its message in every text use -- whose header indexes a record answering `Message()`, `Code()`, `Span()`, `Cause()`;
  a raise in a `finally` that held an error carries it as its cause; `haro fmt` prints `catch(e)`. 31 cases on both builds (stage 42). *The desk's readings,
  recorded as its own*: `raise(e)` of an error value is a rethrow and keeps its origin; `Code()` is Ring's code of a VM error and "" for `raise()`; `Span()` is
  a list with :file and :line. *Corrected*: "`catch cError` in 4 recovered plugin files" above was 10 sites in 4 files, and 3 of them are in stzlib's CORE
  (`core/system/stkPointer.ring`), which `max/stzMax.ring` loads -- each handler raised R24 on its own first line, so two fallbacks never ran; under haro they
  now run as written, under Ring++ they still raise (HF-143).
  **Rung (3) built 2026-11-06, Haro v0.38** (the author: "Rung 3: within, using"): the lift rewrites `within $g = v ... done` and `using name = v ... done`,
  on their own lines, to a `try` whose `finally` the compiler fills wherever rung (1) compiles it -- the global saved before the value and written back,
  or the first of Release, Destroy, Close the value answers called -- and the compiler refuses by name a `within` of a name without `$` (Rule A makes
  every global one), `new K` of a class of the unit answering none of the three, a using name rebound in its block, a block without its `done` or its
  `= value`, and a block with a catch. A value answering none is raised at the entry, before the body. 33 cases on both builds (stage 43), 25 of 25
  plants. *The desk's readings, recorded as its own*: the value is computed after the save, so it may read the global; a global with no value is R24
  at the `within` line; the using name cannot be rebound in its block (rebound, its end would release the new value and leak the old); only `new K` is
  judged at compile time, a literal at the entry like any other value; the refusal at the entry is the VM's error, not a raise() (HF-145).
  **Rung (4) built 2026-11-06, Haro v0.39** (the author: "Rung 4: checker rules"): A5's five rules in `haro check` -- `haro/last-error-read` note,
  every read of cCatchError; `haro/text-run-as-code` error, `eval` of non-literal text unless a validator named with `--validators=` is called in the
  same body; `haro/listener-binds-all` warn, a literal 0.0.0.0, :: or "" given to a listener named with `--listeners=`; `haro/global-restored-by-hand`
  warn; `haro/handle-held-across-raise` warn. The checker reads the LIFTED tree, what the compiler reads, each finding at the file's own column --
  which ends v0.37's and v0.38's misreading of `catch e`, `within` and `done` as names nothing assigns. 24 cases on both builds (stage 44), 29 of 29
  plants. *The desk's readings, recorded as its own*: a read of cCatchError in its handler is reported too (ruling 2's sweep counts every read);
  "passed a validator" is a validator called in the same body, as stzlib's own rule reads it; a by-hand restore a catch also makes is still reported;
  A5's name pattern for a handle is kept as written, though on stzlib it catches 4 values that are not handles (HF-146).
- **D54 -- the extension of a file says how it is read: a `.haro` file by Haro's rules, a `.ring` file by Ring's; ADOPTED** (HARO-SURFACE-01,
  the desk's design under the author's two rulings of 2026-11-06, given in the session after `aNd`, a variable of v0.40, was read as the keyword `and`:
  "I don't the aNd error to happen in Haro so fix it by design. don't feel constrained by Ring heritage since we cut wit it, and hence we are not obliged
  to opt forcase inceseniftvity if you find the inverse moure useful and more robust to Haro langyage"; and "the same thing applies to the use of : in
  :key = value turning it to a list and the special undocumented case (in ring) of using :str and turning str to lowercase!!! i saw some code embracing
  this but we should not be obliged to do so!!"; `spike/v41/GRAMMAR.md`; HF-148; the forty-first rung). **In a `.haro` file** a keyword is spelled in
  lowercase, exactly -- `aNd`, `oK`, `If`, `NULL` are names; Haro's block words `within`, `using`, `done` too -- a symbol keeps its spelling (`:Name` is
  "Name"), and `:key = value` is refused by name (write `[:key, value]`), in a list and as an expression. **In a `.ring` file** Softanza's code reads
  as it did: keywords in any case, symbols lowered, the pair. An eval reads by the rules of the program's root file; each loaded file by its own; `haro
  fmt` by the file's, printing a name as written. **Built** in the grammar (`keyword()` is the lowercase word: one spelling, 22.1 MB of parser to 19.4),
  in `lift.parse` (a `.ring` file's keyword-shaped words outside strings and comments lowered, the same length, before its one parse), in every reader,
  and in the compiler (a `.haro` node keeps its symbol and refuses the pair). Haro's own code followed: 293 `NULL` in 31 files. *The desk's readings,
  recorded as its own*: lowercase only, not lowercase-or-UPPER; NAMES stay case-insensitive (`aNd` and `AND` are one name, which can never be written
  `and`) -- making them case-sensitive would change how a `.haro` program reaches Softanza's functions and is not done here; an eval follows the root
  file, not the line that runs it; a refusal quoting a `.ring` file's text quotes the lowered text. 17 cases on both builds (stage 46), 15 of 15 plants;
  7,125 of 7,126 stzlib files read the same tree (the other fails to parse on both). **Amended in advance, the author's ruling of 2026-11-07**
  (TYPES.md decision (e)): a keyword written in another case in a `.haro` file is refused, as principle 2.2 reads it, not a name -- in v0.42, with
  case-exact names; v0.41 diverged from 2.2 without saying so, found the day after it was built.
- **D55 -- Haro's types: no coercion, a checked letter per exact type, a real boolean, exact numbers, no null in every type, judged types;
  RULED by the author 2026-11-07** (`TYPES.md`; his words, all four quoted there: on case "what do you advise? Keep in mind that we are making a
  language that is mainly executed by agents"; "I want Haro to be cprecise in using an expressive letter for each of it's exact types"; "Haro holds
  no bolean type which was one of my strong critics to ring! ... redeesign a good correct typesystem for Haro"; and on the desk's proposal "Yes
  as recommended, but think of an other letter for list"). T1 no value changes type unasked; T2 a name's first letter is its type, checked, the
  full type written at parameters, returns and attributes; T3 `boolean`, and only a boolean decides; T4 `integer`, `decimal` (a literal with a
  point), `float` (asked for, compared by `near`); T5 `none` in no type, `maybe T` resolved where it lands; T6 vector, map, record, object,
  error; T7 a sentence of a declared language is a value only its court makes, text from a door is `unjudged`, a handle names its door. The
  letters: b i d f n t x k v m r o e h s -- `v` for `vector of T`, not `l`, which a person reads as `1` (the desk's reading under his
  delegation). Builds PRINCIPLES 1.1, 2.1, 2.4, 4.1 and 4.3, ruled in v0.1 and never built. The rungs: v0.42 case-exact names, then v0.43 to
  v0.48. Nothing of it is built at this entry. **Rung v0.42 built 2026-11-07** (`spike/v42/GRAMMAR.md`, HF-149, stage 47): in a `.haro` file a
  name is spelled where it is used as where it is declared -- local, parameter, global, function, class, attribute, method -- and any other
  spelling is refused, naming the declared spelling and its line; a second spelling in one scope is that refusal, never a second name; two
  functions differing only by case are refused at a call of either; a keyword of the grammar in another case is no name (decision (e)); a
  native is spelled in lowercase, as the VM registers it -- **the author's ruling of 2026-11-07**, asked with the count (433 calls of Haro's
  code not in lowercase): "Lowercase (Recommended)". Resolution stays Ring's, so a `.ring` file folds case as it did. *The desk's readings,
  recorded as its own*: Haro's block words `within` and `using` are contextual, no keywords in principle 2.2's sense (v0.38's B03), so v41's
  S14 stands; a `.ring` declaration is spelled as Ring reads it, lowered when keyword-shaped (`o.see()`, not `o.See()`); a method on a receiver
  of unknown class is accepted when some class declares that spelling. 19 cases on both builds, 16 of 16 plants. **Rung v0.43 built 2026-11-08** (`spike/v43/GRAMMAR.md`, HF-150, stage 48): T1 and T3 in a `.haro` file -- `true` and `false` booleans, a comparison and the logic answering one, a condition taking one (BOOLEAN_EXPECTED; a literal condition refused when compiling), no coercion (NO_COERCION, TYPE_MISMATCH), an integer exact to 64 bits (INTEGER_OVERFLOW); a `.ring` file reads as Ring reads and a boolean is 1 or 0 to it. *The desk's readings*: the error codes are names in capitals; Ring's F-98 (a number + nl is text) is a coercion and is not kept; a `.ring` function's 1 is refused in a `.haro` condition, the conversion at a b-name waiting for v0.44. 24 cases on both builds, 26 of 26 plants.
  **Rung v0.47 built 2026-11-09** (`spike/v47/GRAMMAR.md`, HF-153, stage 51), the scope asked with the measurement and ruled by the author 2026-11-08: "Yes, as recommended" -- T2 in a `.haro` file: a value's name (local, parameter, global, attribute) begins with one of the sixteen letters or `a`, Softanza's list until v0.50; no letter, Softanza's `c` (its todo `t`), and a single letter outside a `for` counter or a `catch` name are refused when compiling; the letters whose types exist (b i n f t v o h) are checked -- a literal of another type when compiling, any other value where it is given (a statement, a parameter on entry, a for-in counter), raising TYPE_LETTER; the empty text passes any letter until v0.49; a `.ring` file is untouched. Haro's own code re-lettered by a tool (a11646b, listed apart for stage 24). *The desk's readings, recorded as its own*: `n` on a local stays accepted until v0.48 (renamed once); functions, methods and classes are not lettered; `cCatchError` is read, never declared, and keeps its name; a name spelled other than its declaration is that fault before its letter's. 16 cases on both builds, 15 of 15 plants.
- **D58 -- a built-in is spelled as Softanza writes a name in a `.haro` file; RULED by the Principal 2026-11-09, BUILT the same day as v0.48** (`spike/v48/GRAMMAR.md`, HF-154, stage 52). Their words, reading `parentclassname`: "for a human reader it's better to be ParentClassName or at least parent_class_name"; asked with their 2026-11-07 ruling ("Lowercase (Recommended)", v0.42's N4) and three options, they chose "ParentClassName". It REVISES v0.42's N4. One spelling per built-in, Ring's 258 and the VM's 19, from `study/v48/builtin_names.py`'s table (the desk's, under the Principal's "I let you decide"): words capitalised, a digit in place, a C name's parts as words (`FOpen`), Ring's prefixes as words and no underscore (`RingStateNew`); any other spelling refused naming it; a `.ring` file reads every spelling. 9 cases on both builds, 5 of 5 plants; Haro's 2,172 calls re-spelled by a tool (20fc236).
- **D62 -- Haro has contracts: `requires`, `ensures`, `invariant`, written in the closed condition language, RULED 2026-11-10 ON THE AUTHOR'S DELEGATION** (his words: "I let you decide onmy behalf", answering HARO-CONTRACT-01, which stzlib-testoor raised as HARO-PROOF-01 (b); delegated, not his own reading). (a) **They exist**, in a `.haro` file only: `requires <condition>` and `ensures <condition>` stand after a definition's signature and its intent clause, before its body, one clause a line; `invariant <condition>` stands first in a loop's body. `result` names the answer inside `ensures`. (b) **The condition is written in the condition language CONSTRAINT already speaks** (v0.2, v0.3: `and`, `or`, `not`, the comparisons, `contains`, `absent`, `empty`, `some ... where`, `all ... where`), widened only by what a value needs -- arithmetic, `Len`, a parameter, an attribute, `result` -- and kept CLOSED AND TOTAL: no assignment, no `eval`, no loop but a quantifier over a list it is given, and a call only to a built-in that answers without effect or, once the facts carry it, to a function recorded pure and total. So a contract always ends and changes nothing, and the specification language is itself judged, as HARO-PROOF-01 (b) asked. The intent clause stays prose and is never compared; a contract is the part a machine reads. (c) **A contract is checked when the program runs** -- a failed one raises CONTRACT_REQUIRES, CONTRACT_ENSURES or CONTRACT_INVARIANT naming the definition, the clause and its line -- until a prover discharges it; `haro check --facts` records each clause (its text and line) and, from the discharge rung on, its certificate. (d) **Placed** after judged types: contracts v0.56, their discharge (the closed language to an SMT solver) v0.57; the proof profile's name is asked when D56's first rung is built (HARO-PROOF-01 (c)), the words `requires`, `ensures`, `invariant` and `result` being ruled here. A `.ring` file has none.
- **D78 -- Haro's numbers, RULED and built 2026-11-12 as v0.66** (`NUMBERS.md`, `spike/v66/GRAMMAR.md`, HARO-NUMBERS-CORE-01). The Principal's words: "Haro should not reproduce the wrong design of [the retired language] changing the decimals globally ... What led us to leave [it] should not be in front of us in our own language!!"; "if we need the decimals(10.257) we get a list [2, 5, 7], if we want the decimal part we say DecimalPart(10.257) and we get 0.257. Look at how we designed this in Softanza number staff ... learn from the best desigend languges"; and, on `NUMBERS.md`, "Build it as proposed". In a `.haro` file no setting for places reaches the code: a float is written as its shortest exact text; places are asked per value -- `Text(x, iPlaces)`, `Round(x[, iPlaces])`, half to even, a float rounded from its exact value; `IntegerPart`, `DecimalPart`, `Decimals` and `Digits`; `Abs`, `Sign`, `Clamp`; `FromHex`. `Decimals(n)` as a setting, `FAbs` and `Dec` are refused, each naming what to write; a `.ring` file keeps its names. The desk left `Truncate` out, said so: it answers what `IntegerPart` answers. **Maps are v0.67, judged types v0.68, contracts v0.69 and their discharge v0.70.**
- **D77 -- in .ring code a decimal is Ring's number, built 2026-11-12 as v0.65** (`spike/v65/GRAMMAR.md`, HARO-RINGBOUNDARY-DECIMAL-OUT-01, from stzlib-haroport: stzPattern's decimal positions reached a `.ring` guard unformatted by `decimals(4)`). The desk's reading, first StzLib's (a), a conversion where a decimal crosses into `.ring` code, amended before any code when StzLib found its decimals were list items two levels deep: wherever a decimal came from, `.ring` code prints it, joins it into text and `string()`s it as Ring writes a number, and `type()` answers NUMBER; nothing is converted at a boundary, so a decimal through `.ring` code comes back to `.haro` exact. **Maps are v0.66, judged types v0.67, contracts v0.68 and their discharge v0.69.**
- **D76 -- records, built 2026-11-12 as v0.64** (`spike/v64/GRAMMAR.md`, HARO-RECORD-01), TYPES.md T6 with the Principal's spelling of 2026-11-12, **"Declared, built in order"**: `record User` with lettered fields, one per line, ended by `end`; `User("ada", 36)`. The desk's readings: a record holds no method; the number of values is checked when compiling and each value against its field's letter where given; a field the record lacks is refused when compiling where the record is proven, naming the nearest field within two edits, and is NO_FIELD when running elsewhere; `r` holds a record and nothing else, `o` an object and no record; a record is a value, copied when assigned; `new User` is refused; a `.ring` file is untouched; the refusal of `:key = value` names the record.
- **D75 -- a .ring number crossing into .haro is an exact decimal, built 2026-11-12 as v0.63** (`spike/v63/GRAMMAR.md`, HARO-RINGBOUNDARY-NUMBER-01, from stzlib-haroport: a `.ring` caller's 0.25 met stzPattern's `pxCycles <= 0` as a float, NUMBER_MIX, holding stzlib's module 3). TYPES.md section 6 (D55) rules that a value crossing from `.ring` code into a `.haro` name is checked at that binding; the desk's reading, the first of the two StzLib named: a fraction crossing from `.ring` into `.haro` -- a `.ring` caller's argument at a `.haro` parameter, a `.ring` function's answer to a `.haro` caller -- is the exact decimal of its shortest text, a whole number an integer. A float stays where `.haro` code asks for one (an `f` parameter, `0.25f`), where it has no decimal, between `.ring` functions and in a list. **Records are v0.64, maps v0.65, judged types v0.66, contracts v0.67 and their discharge v0.68.**
- **D74 -- two silent defects, built 2026-11-12 as v0.62** (`spike/v62/GRAMMAR.md`). HARO-NATIVE-BOOL-01 (stzlib-haroport): a boolean crosses to a native as the number 1 or 0, an argument and an item of a list the native reads -- it crossed as nothing, read as 0, and a case-sensitive replace ran case-insensitive. HARO-THISCHAIN-01 (stzlib-security): the count of Ring's named holders walks each live frame only up to where the next begins -- a callee's frame begins inside its caller's, a temporary in the overlap was taken off twice, and `oU = Pointer2Object(h)` copied an object it should have shared, so a capability revocation was lost; `.ring` and `.haro` alike, a defect and no change of rule.
- **D73 -- structure, its letters, built 2026-11-12 as v0.61** (`spike/v61/GRAMMAR.md`, HARO-STRUCTURE-01), TYPES.md T6 (D55), on the Principal's "Start structure". The desk's readings on his delegation: T6 is built in three rungs -- its letters (this one), records, maps -- because records and maps are new kinds of value and the letters are not. In a `.haro` file `a`, kept by T2 "until structure", is no type's letter: a name lettered `a` is refused, naming `v` (a vector) and `x` (any value), a parameter keeping its p mark; `e` is checked, an error -- the value a catch binds -- and nothing else. A `.ring` file is untouched. Haro's own 451 `a` names moved by a tool (5c2ce49: 118 to v, those the tree gives only list literals; 333 to x); haroport's rule A does the same for a ported tree (6d05f74). **StzLib's HARO-NATIVE-BOOL-01 takes v0.62** (a .haro boolean reaching an engine native arrived as 0, silently), **so records are v0.63, maps v0.64, judged types v0.65, contracts v0.66 and their discharge v0.67.**
- **D72 -- symbols compared by name, built 2026-11-12 as v0.60** (`spike/v60/GRAMMAR.md`, HARO-SYMBOL-01), from stzlib-haroport's HARO-SYMBOL-KEYWORD-01 and HARO-SYMBOL-TEXT-EQ-01, on principle 4 (a symbol is data, keeps its text, and compares ignoring case). The desk's readings on the Principal's delegation: a symbol's word is no keyword; where one side of `=` or `!=` is a symbol written in the code, the other side is compared with the symbol's name by its text, case ignored, and a value that is not a text is never the symbol -- false, no error, because a named-parameter list may hold any value first. A `.ring` file reads its symbols as Ring does. **This takes v0.60, so structure (T6) is v0.61, judged types v0.62, contracts v0.63 and their discharge v0.64.**
- **D71 -- `null` leaves Haro, built 2026-11-12 as v0.59** (`spike/v59/GRAMMAR.md`, HARO-NULL-01), TYPES.md T5 (D55): Ring's NULL was the empty text and is gone. The Principal's: the order ("Right after absence", 2026-11-11) and the test's name, chosen among three on 2026-11-12: "IsEmpty(x)". The desk's readings: `null` is refused in a `.haro` file, naming `""` and `none`; `IsNull` is refused, naming `IsEmpty`; `IsEmpty(x)` is true for the empty text only (the text "NULL" is a text; a list, a number, an object is no empty text). Haro's own 302 `null` became `""` and its 384 `IsNull` became `IsEmpty`, by a tool. A `.ring` file keeps Ring's `null` and `isnull`.
- **D70 -- absence, built 2026-11-11 as v0.58** (`spike/v58/GRAMMAR.md`, HARO-ABSENCE-01), TYPES.md T5 ruled in D55, with the Principal's spelling of 2026-11-11 (`maybe` a trailing word, `func Find(kId) maybe`, `oParent = none maybe`; `x = E else D`). The desk's readings on his delegation: `none` stands only where a maybe is declared -- returned by a maybe function, given to a maybe attribute; a maybe (a call of a maybe function or method, a read of a maybe attribute) stands where it lands -- the left of `E else D`, the value a maybe function returns, or a statement of its own -- and is refused anywhere else, naming it; `E else D` is D when E is none, and D may raise; `else` is written after `=`, `return` or `print`, and an `else` that begins its line or follows an if opened on its line is the if's; a maybe function that ends without a return gives none; `else` after a value that is never none is refused. `none` is a nil with a mark, so a slot nothing assigned still raises R24. A `.ring` file has neither word.
- **D69 -- one way to print: `print`, and `?` its shortcut, RULED 2026-11-11, built as v0.57** (`spike/v57/GRAMMAR.md`, HARO-PRINT-01). The Principal's words: "I don't want Haro to enherit the Ring pathology of having serveral laternative to the same fauture like 'see', 'print' and '?'. Although, one could accept a unique keyword (print for example) along with a useful shortuct like '?'." His own: one keyword and one shortcut. The desk's reading on his "i let you decide": `print` and `?` are the same statement -- the value, then the end of the line, as `?` always wrote it; `see` and `put` are refused in a `.haro` file, naming `print`; output that ends no line goes through the stream, `FWrite(stdout, tText)`. No grammar change: the lift writes the keyword as `?` in place, and a `.ring` file keeps Ring's `see`, `put`, `?` and its own `print(...)` function.
- **D68 -- every definition ends with `end`, in any order; `func` a function, `def` a method, RULED 2026-11-11, built as v0.56** (`spike/v56/GRAMMAR.md`, HARO-DEFINITIONS-01). The Principal's words, in this desk's chat: "the ring's style of positioning classes at the end etc, shloud not be adopted by haro. it was one of the things that let agents suffer most (including you) and waste token to remind them tat each time! aloso, i would like to keep func for functions and def for methods so they are clearley separate", and "i let you decide" for the rest. His own: no position rule, and `func` and `def` apart. The desk's readings on his delegation: (G1) **a definition is a block like every other and ends with `end`** -- func, def, class, package -- which replaces D67's F2; a definition without it, an `end` that closes nothing, a body on its header's line or an end word in another spelling refuses the program at its first statement, so nothing runs; (G2) `func` inside a class and `def` outside one are refused, each naming the other, which replaces D67's `func` for methods; (G3) **any order**: a class, a function and the program's statements stand where the writer puts them, every statement at the top level is the program's, run in the order written; (G5) **a chain across lines continues with its dot at the start of the next line**, a dot that ends a line refused (HARO-PORTTOOL-CHAINDOT-01, from stzlib-haroport). The structure is read from the tokens, not the grammar: a `.haro` file's definitions are handed to the parser in braces, so the grammar shared with the classic Ring surface is unchanged and a `.ring` file reads as before.
- **D67 -- one form for each construct, RULED 2026-11-11 ON THE AUTHOR'S DELEGATION, built as v0.55** (`spike/v55/GRAMMAR.md`, HARO-ONEFORM-01). His words, in this desk's chat: "Ring uses different keywords to end a block (ok, end, }, off, done...). I want Hero to end this chao and do not enherit it. Opt for a strict one form. Try to identify any simular issue and solve it." The choice of each form is the desk's on that delegation, not his own reading: the word that says what the construct does, and among equals the one Haro's own code already writes. In a .haro file: (F1) **every block ends with `end`** -- if, while, for, switch, try, and v0.38's within and using (which ended with `done`) -- never ok, next, off, done, endif, endwhile, endfor, endswitch, endtry, and never braces; (F2) **a definition -- func, class, package -- has no end word**: it ends where the next definition begins, never end, endfunc, endfunction, endclass, endpackage, never braces; (F3) **one word each**: func (never def, function), elseif (never but), else (never other, in a switch too), case (never on), for (never foreach), see (never put), give (never get), exit (never break), loop (never continue), and, or, not (never &&, ||, !), from (never `:` or `<` before a class's parent), `#` for a line's comment (never //), `this` for the method's object (`self` only inside a brace object, where it is that object); (F4) **a definition's parameters stand in parentheses**, `func Add(iA, iB)`, and a definition without parameters has none, `func Main`; (F5) **a statement has no trailing period**. Kept, each a different construct: `?` (prints a line) beside `see` (prints, ending no line), the three quote marks (each lets the other two stand inside), /* */ (a comment across lines), `do ... again` (a loop whose condition stands at its end). A .ring file reads every spelling as it always has; haroport's rule O writes a ported tree in the one forms, and Haro's own code was rewritten by it (a tool commit).
- **D66 -- the p mark and a vector's element letter, built 2026-11-11 as v0.54** (`spike/v54/GRAMMAR.md`, HF-160, stage 59), HARO-LETTER-SOFTANZA-01 from stzlib-haroport, carrying the Principal's HAROPORT-SPELLINGS-02 (a) "Keep p as a mark", (c) "v + second letter" and (d) "Keep constants in caps" (stzlib 18608e029); the order -- these letters before absence -- is the Principal's in this desk's chat (2026-11-11, "Letters first"). In a .haro file `p` + a type letter + a capital names a parameter and is checked by its letter (`ptName`), Softanza's `pc` refused with `pt` as its todo; a `p` name that is no parameter of its function is refused naming the function, because the mark would say something false (the desk's reading); `v` + an element letter + a capital (`viPos`, `pvtNames`) is a vector each of whose items holds the element's type, checked where a value is given, a vector literal included, the first item that does not named with its place (the desk's reading: the element letter is checked as every checked letter is). A constant -- its letter, then capitals and underscores -- holds as it did. **Ruled with it, for the next rungs** (the same chat, 2026-11-11): absence writes `maybe` as a trailing word -- `func Find kId maybe`, `oParent = none maybe` -- and resolves with `x = E else D`; and right after absence, Haro's own `null` and `IsNull` are migrated and `null` is refused in a .haro file.
- **D65 -- the classic Ring surface's 1 and 0 cross into a .haro file as false and true, built 2026-11-10 as v0.53** (`spike/v53/GRAMMAR.md`, HF-159, stage 57), TYPES.md section 6 (ruled in D55) on HARO-RINGBOUNDARY-BOOL-01 from stzlib-haroport; the desk's reading: where a boolean is wanted -- a b name given with =, a condition, an operand of not, and, or -- the answer of a call the compiler cannot prove is Haro's (a .ring function, an engine native, a method dispatched by name) has its 1 or 0 made true or false, and anything else stays for the check that stood; a function of a .haro file, a built-in and a method through `this` stay strict. **With it, haroport** (`port/haroport.py`, stage 58, HARO-PORTTOOL-01): a tree of the classic Ring surface ported to .haro mechanically -- keywords, built-in spellings, Softanza's c and v, bare locals lettered, `_name_` unwrapped -- every rename landing on a keyword, a name already there or a class's attribute refused and listed; plan writes nothing.
- **D64 -- numbers, built 2026-11-10 as v0.52** (`spike/v52/GRAMMAR.md`, HF-158, stage 56), D55 T4 on the author's "start the next type rung"; the readings inside T4 are the desk's: a decimal keeps the digits written after its point (`12.50`), `+ -` keep the larger scale and `*` adds them; `/` on integers and decimals is the exact decimal in the fewest digits or DECIMAL_INEXACT, so a .haro file's `7 / 2` is the decimal 3.5, and `Divide(a, b, iPlaces)` rounds half to even; a float mixes with no other number, an integer included; 64 bits of coefficient and 18 digits of scale, DECIMAL_OVERFLOW past them; `Float`, `Decimal`, `Integer`, `Divide`, `Near` are Haro's own and a .haro file's only; `Type()` says DECIMAL for a decimal and keeps NUMBER for an integer and a float. A .ring file reads its numbers as it always has, and a decimal is a double in .ring code and to the engine.
- **The surface's name, RULED by the author 2026-11-10** (his words: "You can say \"class Ring surface\"", answering the desk's proposal of a neutral name for HARO-RINGTEXT-01): the surface on which Haro reads Softanza's existing code is called **the classic Ring surface** in prose -- the desk's reading of "class" as "classic", to be corrected if he meant another word. The `.ring` extension and the vendored grammar's name stay, each with its reason; the rest of HARO-RINGTEXT-01 follows CENTRAL-NORING-SCOPE-01.
- **D63 -- Haro's release: MIT, Mansour Ayouni, a public releases repository, RULED 2026-11-10 ON THE AUTHOR'S DELEGATION** (the same words, answering HARO-RELEASE-ADOPT-01 (a) and (d), routed by central 2026-11-09 16:15; delegated, not his own reading). (a) **The licence is MIT**, "Copyright (c) 2020-<year> Mansour Ayouni", the end year computed when the archive is built (PRINCIPAL-COPYRIGHTYEARS-01, as stzlib's LICENSE reads), carried in every archive beside THIRD-PARTY-NOTICES.txt. It covers the release's binaries; this repository and its source stay PRIVATE. (b) **The public place is the releases page of a public repository, `mayouni/haro-releases`**, holding the archives, their SHA-256 sums and one short page -- nothing of Haro's source. Its text states what Haro is and does (PRINCIPAL-AFFIRM-01) and names no other language (PRINCIPAL-HAROINDEPENDENT-01), and release/build_release.py refuses a page that does either. (c) **Only an accepted build is published**: windows-x86_64 and linux-x86_64 (Radar's guard and feed check, from a fresh clone); macos-aarch64 joins when it is accepted on a Mac. (d) Publishing is the outward act and waits on the author's yes, asked once. **Published 2026-11-10 on his "Yes, publish"**: https://github.com/mayouni/haro-releases/releases/tag/v0.51-269f15a, the windows and linux archives and SHA256SUMS, each sum checked on a fresh download. **(b) AMENDED THE SAME NIGHT BY THE AUTHOR HIMSELF**: "you should have proposed to make Haro public and I would agree! remove this haro-releases and work on one repo" -- the desk had kept this repository private by its CLAUDE.md and made a second one without saying why. `mayouni/haro` is PUBLIC, its history whole (scanned for secrets first, none found; his "Public now, clean after" for the Ring wording it carries), and the release is https://github.com/mayouni/haro/releases/tag/v0.51-269f15a, tagged at 269f15a, each sum checked on a fresh download. `mayouni/haro-releases` was deleted the same night on his "delete mayouni/haro-releases onmy behalf", once he granted the delete_repo scope.
- **D61 -- `haro check --facts`, 2026-11-10, as v0.51** (`spike/v51/GRAMMAR.md`, HF-157, stage 55), HARO-FACTS-01 answering HARO-PROOF-01 (a), delegated to this desk (the author: "I let you decide"). One JSON record per unit, format "haro-check-facts/1": the checker's commit (the last that touched vm/, "+uncommitted" when vm/ held changes at the build), each file's sha256 of the bytes read and its surface, every function's lines, findings, calls (static, dynamic, late), first direct impurity, whether the compiler finished it and why not, and the rules that did not look. A field for a fact not established is absent, never false; `total`, `uses` and profiles join with their rungs. The record is what the checker and the compiler establish, not a proof: the grade it earns is Testoor's to set.
- **D60 -- a program that serves another, 2026-11-09, as v0.50** (`spike/v50/GRAMMAR.md`, HF-156, stage 54), on HARO-STDIOFLUSH-01 from the Radar desk, delegated to this desk (the author: "I let you decide"). `give` sends the program's output before it waits and reads a line whole; `stdin`, `stdout`, `stderr` are C's streams as Ring's file handles, `fflush(stdout)` sends the output, a write through `stdout` keeps its place; `feof(stdin)` is 1 once a read met the end of input, a boolean in a .haro file. No new name: the three streams and `feof` are Ring's. Named divergences: Ring's give cuts a line at 255 bytes, Haro's reads it whole in a .ring file too; Ring flushes after every `see`, Haro sends at a read, a flush, a command, the end or 64 KB.
- **D59 -- ZIP is Softanza's engine's, not Haro's VM's; zip.zig retired, 2026-11-09, as v0.49** (`spike/v49/GRAMMAR.md`, HF-155, stage 53), on the author's words of 2026-11-08 ("we have zip covered by the engine!!"; "only Haro will remain") once stzlib's port had moved stzZipFile onto stz_compress (stzlib cb6f5de65). A zip_ call is Ring's R3, as Ring with its extension not loaded; stzlib's zip guard 305 of 305 on haro.exe without zip.zig. v0.44's zip cases and plants retire with it.
- **D56 -- the system grain is a profile a `.haro` unit declares, and its seats are D55's, amended; RULED by the author 2026-11-07**
  (HARO-TYPES-SYSTEM-01, COMPASS-SYSLANG-02; `SG1.md`, the desk's draft at c780692 on syslang-sg0's memo of 2026-11-07 13:09; his words, asked
  with the draft's nine parts in section 10: "Yes, as recommended"). (a) Every seat is Haro's in every `.haro` file; `PROFILE system` only
  refuses what C cannot hold without a runtime -- a managed value outside a region, `eval`, an unresolved call, an undeclared door. (b) Two
  whole-number families: `i` integer, overflow raised, widths `i8` to `u64`, `integer` alone `i64`; `w` word, unsigned, wrapping by
  definition, `w8` to `w64`, the only type the bit operators take -- the sixteenth letter. (c) `bytes` of a length fixed when made, `bytes of
  N` fixed when compiling, an element a `w8`; `DEFINE LAYOUT` with widths, byte order and padding written, no native order. (d) One
  second-class rule: `ref` (written at the call too), a region's values and a scoped door handle pass down and are never stored, returned or
  captured. (e) Reference counting by default, regions on v0.38's `using` in the profile, no manual free. (f) `uses [door]` on a function from
  D51's nine, pure without it, the call closure checked; a native outside W7's map refused in the profile until the map lands. (g) `personal`,
  the dual of `unjudged`, reaching a door only under D37's `SAFEGUARDS`, built with the constitution desk. (h) `total` on a function; `budget`
  in W6's form, checked at run time. (i) The C door is `DEFINE FOREIGN` under `uses [dynamic_load]`; the engine's ABI v1 untouched. Amends
  D55 as T4a-c, T6a-b, T8 and T9 (`SG1.md` section 9). The rungs are `SG1.md` section 11, after D55's number rung; the first takes SG0's
  seven X1/X2/X7 GAP tasks, written without their workarounds, as its acceptance set. Nothing of it is built at this entry.
- **D57 -- the four ported defects are fixed in Haro, Ring 1.27 the specification of a `.ring` file's surface, with two divergences named; under the author's Haro-first ruling** (PRINCIPAL-HAROFIRST-01, LEDGER line 207, 2026-11-08: "the fixes and enhancements should go into Haro and not Ring++"; HARO-PORTED-FINDINGS-01, carried by Central 08:18; the order, "Yes, that order"). Built as v0.44 (`spike/v44/GRAMMAR.md`, HF-151, stage 49): a math native outside its domain raises R51 as Ring's does; a NaN is unordered; `s[i] = c` writes a letter of a local text in a `.ring` file as Ring does (R7, R2, a number as its byte) and a `.haro` file refuses it (TEXT_IN_PLACE); `zip_openfile(f, "a")` on no archive answers Ring's NULL and leaves the file; `zip_extract_allfiles` writes every entry, the last of a name winning. **The divergences from Ring, the desk's, recorded so**: (1) a letter of a text held by a global, an attribute or a list item is refused in a `.ring` file by name, where Ring writes it, until the compiler writes the new text back to its holder -- allowed now it would be a wrong answer with no error; (2) an archive entry whose name leaves the extraction folder (absolute, a drive, a `..` part) is not written, where Ring 1.27 writes it (zip slip) -- least authority over parity. 14 cases on both builds, every `.ring` expectation read off Ring 1.27; 20 of 20 plants.
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
