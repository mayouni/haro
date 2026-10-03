# Phase 1.5 -- the exemplar extension study, run

**Run 2026-10-03, on the author's instruction ("run the Phase 1.5 study"), by the haro-charter session.**
The study is defined in `ringua/docs/mission.md` section 6 and `ringua/docs/roadmap.md` (Phase 1.5); this
document is its result. Everything it cites is a measurement made by a program in this folder, or a line of
source read and anchored, and each says which.

    python haro/study/phase15/study_run.py        # E3, E1, E2, E4: every fact below, 3 of 3 groups, ~16 s warm
    python haro/study/phase15/study_run.py --plant  # the planted failure: must exit 1

## 1. The result in one page

**The gate** (roadmap): *the composed exemplar answers domain questions asked in at least two human languages,
without the answer path leaving the closed surfaces.*

| | measured | where |
|---|---|---|
| the tontine, with a knowledge graph | 19 facts and 1 law in stzKnowledgeGraph, shipped as a 25-line plain-text artifact that reloads to the same 19 facts | E1 |
| a natural-language surface over it | 74 questions in English and French, compiled by `stzNatural`'s architecture with its compile target changed | E4 |
| two human languages, one meaning | 17 of 17 questions asked in both languages compile to the **same** closed query | E4 G2 |
| answers right | 14 graph questions, 4 plans, 29 ledger questions: each equal to what was composed by hand; each ledger answer equal across the court on two runtimes, an independent evaluation and zing live | E4 G1 |
| answers out, in the language asked | 18 sentences as composed by hand; 22 ledger answers in the voice of the question's language | E4 G6 |
| nothing the question says is run | 16 attacks (brackets, calls, quotes, a second statement, a range, raw ZQL, a Ring global, full-width brackets) all refused; the canary called **0** times; and called **1** time when the gate is removed | E4 G3 |
| understands or refuses, never guesses | 31 questions the language cannot understand, each refused by name in its own language | E4 G4 |
| the same bytes on the reference VM | the whole compile stage, 111 lines, identical on official Ring 1.27 with the author's engine and on Ring++ | E4 G7 |

**The gate's condition is met on these measurements. Its qualification is the finding that matters most:**
the closure holds **because of a lexical gate in front of an engine that is not itself closed.** `stzNatural`'s
shipped tokenizer evaluates any bracketed section of the question as Ring, in a dry run (E2d). The architecture
composes; the shipped front end needs a gate (built here) or a two-site change in the author's tree (named, not
made).

**The engine choice** (mission section 4, "provisional verdict: the `stzNatural` architecture, with its compile
target changed per rule 2"): **confirmed on the architecture, corrected on two claims** (section 3).

## 2. The experiments

### E3 -- NaturalLib 1.27 as shipped (`e3_naturallib.ring`, `e3_run.py`; 9 of 9 facts)

Run on the official 1.27 install, which is the library's own runtime and a named reach outside this repository
(the subject *is* that library).

* **Its answer path is `eval(prepareCode(cString))`** (`naturallanguage.ring:243-244`, read): the user's text is
  pasted into a Ring source string and evaluated, under `changeringkeyword` masking. *Measured:* a question
  followed by a line `? "ESCAPED: this line ran as Ring"` **printed it** (E3d). Keywords are masked, so `see`
  did not run; the `?` statement did.
* **It can be retargeted at the command level** (E3a, E3b): commands whose functions return a ZQL string instead
  of executing, in English and in French (a second language is a second set of commands: the words are the class
  name). So rule 2 fails on NaturalLib's **input** side, not its target side.
* **It accepts what it does not understand, in silence** (E3c): `show me the deposits please` and `show deposits
  over lots` produce no query and no error. There is no refusal channel to answer in the domain's jargon.
* **It does not run on Ring++** (measured): Ring++ refuses the library's own source (Rule A, its `C_NATLIB_*`
  constants are bare globals) before running a line; beneath that, none of `changeringkeyword`,
  `changeringoperator`, `braceexpreval`, `braceerror` appears in `src/*.zig` (0 mentions), and the library's
  `BraceError` reads Ring's own R24 message with `substr(cError,45)` (`naturalbase.ring:127`, read). It cannot be
  vendored into a produced binary.

### E2 -- stzNatural as shipped, then with the tontine vocabulary as data (`e2_stznatural.ring`; 5 checks)

* **As shipped it refuses a tontine question** (E2a): `Unsupported object type!`, English and French. Its
  vocabulary is strings, lists and numbers (read from `stzNatural.ring` and `stzNaturalLangData.ring`); it has no
  vocabulary for deposits, members or rounds.
* **Strict mode names what it did not understand** (E2b): `not understood: 'deposits' 'over' (did you mean
  'power'?) '5000'` -- a real refusal channel NaturalLib lacks, but its suggestions come from a lexicon of string
  verbs, so the domain's jargon is not what it guesses from.
* **The front half retargets with data alone** (E2c): two packs registered through `StzAddNaturalLanguage`
  (English 24 word mappings and 19 ignorable words, French 25 and 21; **the same 11 semantic ids**) give **one
  semantic form** for 3 of 3 questions asked in both languages, e.g. `Q_SHOW ENT_DEPOSIT CMP_GT literal:5000`.
  `Analyze` plus `Tokens()` produce it without generating or running code.
* **The front end is not closed** (E2d): the tokenizer evaluates a bracketed `[ ... ]` section of the question
  (`stzNatural.ring:739` and `:1120`, read), and `LooksEvalSafeList` checks only that the text starts with
  `[` and ends with `]`. *Measured:* `show deposits over [ Marker() ]` called `Marker()` **during `Analyze`**, the
  dry run, and its return value became the literal (`[ 5000 ]`). A quoted `"Marker()"` stayed inert text.

### E1 -- the tontine's knowledge graph (`e1_graph.ring`, `data/tontine.zknw`; 12 checks)

Built with `stzKnowledgeGraph`, on the Ring++ package: 6 members, 3 rounds, 2 roles; `received_pot_in`,
`guarantees`, `holds_role`.

* **It composes.** A triple pattern is a closed query that is *data*: `["?x", "received_pot_in", "round2"]`
  answers `moussa`. The artifact is plain, diffable text (`knowledge "tontine"` / `facts` / `ontology`, 654 bytes,
  25 lines) that reloads to the same 19 facts and answers the same, **and carries its law** (`received_pot_in |
  unique`) in an `ontology` section.
* **A law judges a fact** (E1b): a second pot for Fatima is refused with its reason.
* **What resists**, each measured:
  * `:Unique` is the subject's side only: a second beneficiary for round 3 is **admitted** (E1b). "One beneficiary
    per round" cannot be said.
  * **Laws are enforced when a fact is admitted, not when a world is loaded** (E1g): an artifact that breaks its
    own `:Unique` law loads, both facts, no refusal.
  * **A node property does not survive the artifact** (E1e): the ledger's spelling `Moussa` lived on the live
    graph and was gone after reload. Node ids are lowercased and space-free.
  * **No join** (E1f): `QueryPath` with a shared variable answered the first pattern only (`fatima`; the joined
    answer, `zeinab`, never came).

### E4 -- the composed exemplar (`nlq.ring`, `e4_pipeline.ring`, `e4_run.py`; 13 checks)

`stzNatural`'s architecture -- language packs as data, tokens as semantic ids, one core under many skins -- with
the generate-Ring-and-eval stage **not used**. `nlq.ring` is 322 lines of Ring (257 of code), the driver 61, plus
74 fixtures.

    question ──gate──> tokens ──frames──> closed target ──┬─ ZQL text ──> the ledger's court (Haro Z `ask`) ──> rows ──> the language's voice
    (any language)     (Analyze,          (a table, data)  ├─ triple ─────> the knowledge graph (Query) ────────> ids ──> a sentence
                        no codegen)                         ├─ plan: a triple, then a ZQL built from its answer
                                                            └─ refusal, naming the word / character / shape, in the question's language

* **The gate** (`NlqGate`) is an allow-list: letters, digits, space and `- ' ? , .`; any byte >= 128 (UTF-8
  letters); everything Ring or ZQL reads as syntax is refused before the tokenizer sees it.
* **Names never come from the question.** The lexicon is generated from the graph's facts (every member and role
  is a word); a ZQL string holds the question's text only as a digit string or as a member spelled from the graph.
  `show deposits of Mallory` is refused: Mallory is not in the world.
* **Frames** (12) are `[id, token kinds, kind, target template]`: `Q_SHOW ENT_DEPOSIT CMP_GT NUM` ->
  `SELECT * FROM collect WHERE amount > {NUM}`. A shape no frame has is refused.

**The 74 fixtures** (`mk_fixtures.py`, composed by hand from the domain): 17 pairs in both languages (9 ledger, 6
graph, 2 plans), 9 variants (synonyms, case, a trailing `?`), 15 questions to refuse, 16 attacks.

| gate | what it checks | result |
|---|---|---|
| G1 | the target each question compiles to is the one composed by hand; graph and plan answers likewise; each of 29 ledger answers equal across **the court on rnxc, the court on the oracle, an independent evaluation in Python, and zing live** | 43/43, 18/18, 29/29 |
| G2 | a question in two languages compiles to the same target | 17/17 |
| G3 | 16 attacks refused, canary 0; code holds no eval/system/LoadLib/execute/call/write/fopen/sysget | holds |
| G3 control | the same bracket attack **with the gate removed** calls the canary | 1 call: the canary can fire |
| G4 | 31 refusals each name what was not understood, in the question's language | 31/31 |
| G5 | the court refuses 4 of 4 tampered targets (`; DROP TABLE`, `OR 1=1`, `SELECT member`) | 4/4 |
| G6 | graph sentences as composed by hand; ledger answers in the language's voice, equal to a narration composed by rule from the independent evaluation, on both runtimes | 18/18, 22/22 |
| G7 | the compile stage's 111 lines identical on official Ring 1.27 + the author's engine and on Ring++ | 0 differ |

## 3. The engine choice

| | NaturalLib 1.27 | `stzNatural` as shipped | the retargeted pipeline (E4) |
|---|---|---|---|
| the text of a question is | Ring source, evaluated (E3d) | tokenized; **bracketed sections evaluated** (E2d) | gated, then tokenized: never evaluated (G3) |
| text it does not understand | silently accepted (E3c) | refused in strict mode, with suggestions (E2b) | refused, by name, in the question's language (G4) |
| a second language | duplicate command definitions (E3b) | a pack of data (E2c) | a pack of data: 25 words + 21 ignorable (G2) |
| compile target | a command function: any (E3a) | Ring source from `$aSemanticOperations`, then `eval` (read) | ZQL text or a triple pattern, judged by a court (G1, G5) |
| runs on Ring++ | **no** (E3) | yes (E2, E4) | yes, and the same bytes as the reference VM (G7) |

**The author's analysis (`stznatural-vs-ring-naturallib.md`) is confirmed where it argues architecture:** data-driven
packs, config-only multilingualism, deferred and auditable processing (`Tokens()` is the auditable form) -- each
measured above. **It is corrected on two points the mission had inherited from it:**

1. *"A closed semantic dictionary" is closed for words, not for brackets.* The tokenizer is an open door (E2d).
   Closure needs the gate, or the two `eval` sites replaced by a data parser. Those sites are in the author's
   tree; this study did not touch it.
2. *"Closure applied to natural language" is not refusal by default.* The refusal channel exists (strict mode) but
   its vocabulary is the library's own, not the domain's, so its suggestions are wrong for the tontine (`over` ->
   `power`). The domain pack must supply the vocabulary the refusals speak from.

## 4. What composes

* A knowledge graph for the domain, as data, with a law, reloadable, in 25 lines (E1).
* One semantic core under two languages by data alone; the same 11 ids (E2c, G2).
* A closed compile target on each side: ZQL, judged by the Z court; a triple pattern, judged by the graph (G1, G5).
* A lexicon generated from the world, so names resolve through the ontology and cannot be smuggled (G3, N04).
* The ledger's court as the judge of the query, and **zing as an independent witness of its answers** (G1): a
  composition across two Ringua languages that the study did not have to build.
* Haro v0.16's `NARRATE` as the answer's voice, in English as shipped and in French as a second declaration (G6).
* The same pipeline on two VMs with the same bytes (G7).

## 5. What resists

1. The shipped tokenizer evaluates brackets (E2d). *Worked around by a gate; not fixed.*
2. **Identity across surfaces.** The graph says `moussa`, the ledger `Moussa`, and a node property does not survive
   the artifact (E1e). The study bound them by convention (`upper(first letter)`): true for 6 of 6 names, true in no
   general sense, and the ledger already holds an `amina` row.
3. **Laws.** One-per-round is not expressible; laws are not judged on load (E1b, E1g).
4. **Questions across surfaces.** `QueryPath` is first-pattern-only (E1f) and ZQL has no join, so the composite
   question ("the deposits of the beneficiary of round 2") needed a plan the study invented (`pattern => ZQL`).
5. **One voice per language.** A second human language is a second Haro declaration (`zfr`, built in
   `voices.py`); and the voice's events cover a ledger answer, not a graph answer, so graph answers are told by a
   separate template table (`NlqSayTemplates`).
6. **The shipped packs do not help.** `stzlib` ships English, Hausa, French, Arabic and Turkish packs (read), all
   for string and list verbs. The tontine's vocabulary had to be authored, per language, as data.
7. **The suggestion lexicon is not the domain's** (section 3).
8. **Numbers.** Digits only: a decimal, a sign, a number longer than 12 digits and a spelled-out number are all
   refused (N08-N10).
9. **No multi-clause questions.** `... and delete everything` is refused whole (N14), correctly; but there is no way
   to ask two things at once either.

## 6. What the kit must provide (parts 3.4-3.5)

Each requirement traces to a finding above, as the mission's discipline asks: no API before the pattern.

| | the kit must provide | traced to |
|---|---|---|
| K1 | a **world artifact** (facts and laws) **judged when loaded** by a court, with laws that can say one-per-round, and identity carried in the artifact | E1b, E1e, E1g |
| K2 | **identity across surfaces**: a declared binding of the world's ids to each surface's spellings; best, a surface field *typed by* the world's class (Haro already has reference seats resolved against declared names) | E1e, resist 2 |
| K3 | a **pack format** and a generator of the lexicon from the world; domain vocabulary per language as data; a coverage report of the words a language does not understand | E2c, E4, resist 6 |
| K4 | a **tokenizer with no eval path**, or the gate as part of the contract, with closure a *tested* property: a canary and a negative control | E2d, G3 |
| K5 | a **frame language**: token shapes to closed targets, as data, exact-match, refusing the rest | E4 (12 frames), resist 9 |
| K6 | a **closed plan grammar** for a question across surfaces: steps, an answer bound to a slot of the next query, judged | E1f, resist 4 |
| K7 | **several voices per language declaration**, selected by the question's language; graph answers as events beside ledger answers | G6, resist 5 |
| K8 | **refusals as first-class**: typed, localised, speaking the domain's words; the C2 envelope (Haro v0.11) is the carrier and was **not wired** in this study | G4, section 3 |
| K9 | a **numeric sublanguage** per language | resist 8 |
| K10 | a **question conformance format**: (text, language) to (closed target, answer), with the pair-across-languages invariance as the multilingual test and an independent witness | `fixtures/questions.json`, G1, G2 |

## 7. Honest boundaries

* **Two languages, authored by a model.** English and French; the French has had no speaker's review. The Hausa
  and Arabic packs `stzlib` ships were not tested; right-to-left input was tested only as a refusal (N13).
* **A small closed domain.** 12 frames, a fixed question set. This measures that the architecture *composes* and
  *refuses*, not recall on free questions, which would be low by design. Precision is what the study measures.
* **The graph's facts are constructed** for the study (who received which pot, who guarantees whom, who holds a
  role); the ledger is zing's bedrock-query example, with its replayed duplicates and an `amina` row.
* **The closure is evidence, not proof.** The gate is an allow-list and an argument from reading the tokenizer (its
  two `eval` sites are reached only by `[...]` and `a:b` shapes); 16 attacks and a canary with a negative control
  support it. If `stzlib` changes, G3 must be re-run.
* **No produced binary was built.** The mission accepts vendoring `stzlib`'s natural and graph modules into the
  artifact; their size and start-up in that form are unmeasured. Cold, Softanza compiles in about 9 s here.
* **The oracle cannot host Softanza without the official install** (F-96): G7 uses official Ring 1.27 and the
  author's engine build, run from inside his tree, read-only. No source file of his tree changed during the study
  (checked by modification time; one engine DLL did, which a study that only loads it does not write, and the
  semantic-ops cache is unchanged since 2 October).
* **Not measured:** latency, memory, throughput of the answer path.
* **The `survey` facts** about `stzlib` (the shipped languages and their counts, the `QueryPath` comment, the
  `eval` line numbers outside `stzNatural`) were read from source by a read-only survey; those that the study
  cites as measured say so, the rest are marked *read*.

## 8. Mistakes made on the way, each caught before this was written

1. `split(s, char(9))` splits on **all** whitespace (both runtimes), so every question reached the compiler as its
   first word. Found because every shape read as one token.
2. In a Ring file, statements after a `func` belong to that function: a probe printed nothing and exited 0.
3. **Fixture N02 was composed before the `ledger-all` frame existed.** With it, "show me the deposits please" is a
   lawful question; it moved to V09 *after* the first run, for that stated reason (`mk_fixtures.py`). That is an
   expectation changed after seeing output, and is recorded as one.
4. The French role word came from the first matching entry, so an answer said `tresorier`; the hand-composed
   sentence caught it, and the canonical spelling now comes first.
5. A control character in a refusal message split an output line and two attacks went uncounted (70 of 72); the
   count caught it, and control characters are named by code now.
6. E1's first run admitted a second beneficiary into the artifact (20 facts); the probe now runs after the
   artifact is written.
7. **Attack X16 did not test what it said it tested** (found 2026-10-03, while reading the results to draw the N
   API). It was meant to show that full-width brackets (bytes the gate lets through) are never read as a
   bracketed section, but it had `Marker()` inside, so the gate refused it at the parenthesis and the lookalike
   never reached the tokenizer. The fixture is now `show deposits over ［ 5000 ］` and is refused as the unknown
   word `［`, which is the claim. The study's numbers did not change (74 questions, 16 attacks); what was
   overstated was one attack's coverage.

## 9. What is not decided here

Whether this study closes the gate for N is **the author's reading** (the roadmap's gate is stated for the study;
D13 in `haro/CHARTER.md` held it). **No N API has been drawn**: section 6 is the input to one, not one. Three
things need the author: reading section 6; the two `eval` sites in `stzNatural`'s tokenizer (his tree: replace
bracket evaluation with a data parser, or accept the gate as the contract); and a speaker for the French, Hausa
and Arabic skins.

## Files

    e1_graph.ring  e2_stznatural.ring  e3_naturallib.ring  e3_probe_rnx.ring   the experiments
    nlq.ring  e4_pipeline.ring                                                    the retargeted pipeline
    e3_run.py  e12_run.py  e4_run.py  study_run.py  voices.py  mk_fixtures.py     the judges
    fixtures/questions.json  data/tontine.zknw                                    the questions, and the world as data
    e3_result.txt  e4_result.txt                                                  the recorded runs
