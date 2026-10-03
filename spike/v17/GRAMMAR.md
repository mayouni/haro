# N, built -- the natural letter's API (Haro v0.17, the seventeenth rung)

**Drawn from Ringua's Phase 1.5 study** (`haro/study/phase15/STUDY.md`, section 6, K1-K10), on the author's
"draw the N API from the study" (commit `20d6851`), and **built** on his "build rung 17": the `UNDERSTAND` meta-clause,
the forged court's five verbs and fifteen rules, judged against the drawing's own fixtures. **Written after** the fixtures in `fixtures.json` and the sentence
`n/tontine.n` (the W discipline: fixtures first, prose second) -- and after the study's own 74 questions, which are
the judge of whether the drawing loses anything.

**What this is, in one line.** N is a letter of Haro whose sentences declare how a human language reaches the
closed questions of a declared world: *tongues* (the languages), *meanings* (what a question can mean, with its words
as a column per tongue), *surfaces* (where a question ends), *frames* (the shapes of a question) and *examples* (the
sentence's own conformance). A question is understood by exact shape or refused by name; nothing it says is
evaluated; a name in it is never passed on. **N asks. It never declares.**

## 0. What exists, and what does not

| | status | where |
|---|---|---|
| the letter: eight kinds, five menus, four forms | **built.** Accepted by the meta-court on rnxc and the oracle, byte for byte, using **no new meta-vocabulary** | `n_v17.haro` |
| the forged court: `check` and `diagnose` on sentences of N | **built.** Judges the 17 defects of section 4a and the rules of section 4b. (The court's usage line lists `refine`, `eval` and `walk` too: those answer only for a letter that declares the kind they read, and N declares none.) | `n_court.ring`, forged from the letter |
| a sentence of N: the tontine's natural door | **built.** 85 declarations, English and French | `n/tontine.n` |
| the rules the existing vocabulary cannot say | **built.** 15 codes, 21 fixtures; the v0.16 court said `ok` to the first 20, each of the 15 rules switched off in turn fails its fixtures | `n_lib.ring` (`NatRules`), `v17/n_model.py` (`rules`, the reference) |
| `understand`, `ask`, `tokens`, `vocabulary`, `examples` | **built.** The forged court reproduces the study on 74 of 74 questions and agrees with the model field for field | `n_lib.ring` (`NatMain`) |
| the meta-clause that makes the forge emit them: `UNDERSTAND` | **built (section 8).** The meta-court checks it (12 fixtures, `v17/meta_fixtures.json`, stage 1); the forge emits the court's loads and globals | `haro_lib.ring`, `forge.ring` |
| `propose` (N drafts a sentence of another letter) | **reserved, not drawn.** The study did not measure it (section 10) | -- |

`python haro/spike/v17/n_check.py` judges all of it; `--plant` fails it. **The model is no longer the court, and
is kept as its reference.** It is a second implementation of the same behaviour, read from the sentence alone, sharing
no code with the study's pipeline nor with the court's: the court and the model are compared field for field on every
question, which is how a defect of the port, or of the drawing, is told apart.

## 1. What is ratified, and what the drawing keeps to

* *"Natural language asks; it never declares."* (Ringua rule 1; 06-ALPHABET, ratified 2026-09-27.) **No kind of N can
  declare a world, a fact or a rule**; a sentence that tries is refused by the letter's own `unknown_declaration`
  (fixture C09).
* *"The engine compiles to the language's own closed query grammar, never to host code."* (rule 2.) A question ends as
  a query a **surface's court** judges. Nothing of the question is evaluated.
* *"N may DRAFT declarations ... a draft enters the world only as a proposal judged by the court; N proposes, the
  court decides, the human ratifies."* Ratified, **reserved here**: section 10.
* *Closed, plain text, judged.* A sentence is plain text; `check` judges it, including its own examples.

## 2. The shape of it

    a question, in a tongue
         |  gate        the characters the court allows; anything else is refused before anything reads it
         |  tokens      each word is ignored, a word of a meaning, a name the world knows, or digits
         |  frame       the meanings, in order, are exactly one frame's SHAPE -- or the question is refused
         |  query       the frame's template, its slots filled: digits, and entities spelled the surface's way
         v
    a surface (a court)  judges the query, runs it
         |  answer       rows or entities, as data
         v
    told, in the tongue  by the surface's voice, else by the frame's own template

## 3. The sentence: eight kinds

`DEFINE KIND name AS (CLAUSE value, ...) RATIONALE "..."`, as every sentence of Haro. A seat ending in `?` is optional.

| kind | seats | what it declares |
|---|---|---|
| `TONGUE` | `CODE text`, `IGNORES text`, `ALLOWS text?`, `DIGITS digit_sets?`, `NAMES spellings?`, `REFUSES [kind: text]` | a human language: the words that mean nothing, the punctuation it allows (only from the court's safe set), how it writes a name in an answer, how it says each of five refusals |
| `MEANING` | `SLOT slots`, `OF name?`, `FROM surface?`, `WORDS [tongue: text]?` | one thing a question can mean. `SLOT none`: words per tongue. `SLOT number`: digits. `SLOT entity`: an entity of kind `OF` that surface `FROM` enumerates; its words are generated |
| `ALIAS` | `MEANING meaning`, `ENTITY text`, `WORDS [tongue: text]` | words for one entity, per tongue; **the first word of a tongue is the one an answer is told in** |
| `SURFACE` | `KIND query\|pattern`, `GRAMMAR text`, `COURT text`, `WORLD text?`, `ENTITIES [word]?`, `SPELLS [kind: how]?`, `TELLS [tongue]?` | a closed place a question ends: its grammar, the court that judges and runs it, the versioned world it reads, what it enumerates, how it spells it, the tongues it can tell an answer in |
| `STEP` | `TARGET surface`, `QUERY text`, `BINDS name?` | one query of a plan; `BINDS` names the slot its one answer fills for the steps after it |
| `FRAME` | `SHAPE [meaning]`, then `TARGET`+`QUERY` **or** `STEPS [step]`, `ANSWERS [tongue: text]?`, `EMPTY [tongue: text]?` | one shape of question, exact |
| `EXAMPLE` | `MEANS frame`, `ASKING [tongue: text]` | what the sentence promises to understand, in each tongue |
| `COUNTEREXAMPLE` | `ASKING [tongue: text]`, `REFUSED refusal_kind` | what the sentence promises **not** to understand, and how it is refused |

Menus: `slots` (none, number, entity), `surface_kinds` (query, pattern), `spellings` (as_is, upper_first),
`refusal_kinds` (character, word, shape, ambiguous, surface), `digit_sets` (ascii).

Placeholders in a template are `{slot}`: a slot is the name of a `number` or `entity` meaning in the frame's SHAPE
(`{num}`, `{member}`, `{role}`), plus `{answer}` in `ANSWERS`, plus a slot a step BINDS. `{what}` is the thing not
understood, in a tongue's `REFUSES`. **A QUERY uses single quotes**: a Haro string cannot hold a double quote, and
ZQL reads both (measured).

A frame, whole (`n/tontine.n`):

    DEFINE FRAME graph_pot AS (
      SHAPE [who, received, round, num], TARGET graph, QUERY "?x received_pot_in round{num}",
      ANSWERS [english: "{answer} received the pot in round {num}.", french: "{answer} a reçu la cagnotte au tour {num}."],
      EMPTY [english: "Nobody received the pot in round {num}.", french: "Personne n'a reçu la cagnotte au tour {num}."]
    ) RATIONALE "Who received the pot of a round"

## 4. Rules

### 4a. Enforced today, by the forged court, with the existing meta-vocabulary (17 fixtures, `B`)

Every reference resolves (a tongue, a meaning, a surface, a step, a frame: `DANGLING_TONGUE`, `DANGLING_MEANING`,
`DANGLING_SURFACE`, `DANGLING_STEP`, `DANGLING_FRAME`); a column keyed by an undeclared tongue; every seat typed by its
menu (`SLOT text` is refused: **there is no free-text slot**); `SLOT`, `COURT` required (`MEANING_INCOMPLETE`,
`SURFACE_INCOMPLETE`); one namespace; a RATIONALE on every declaration; **and rule 1 as a refusal**: a kind N does not
have is refused with *"N asks; it never declares the world, the facts or a rule"*.

### 4b. Enforced by the forged court since the seventeenth rung (21 fixtures, `C`)

Each is a sentence the **v0.16 court called `ok`** (recorded in HF-68, before the rung); the forged court now answers
the code, in `diagnose` as a C2 envelope citing `rule:<code>` in lower case, and the model answers the same codes. Each
rule is switched off in turn **in the court** (a copy with the one `NatAdd` for that code muted) and its fixtures stop
being caught: 15 of 15 hold. A rule reads a sentence whose references resolve: a sentence that already has a finding of
section 4a is not read by them, and `check` stops at the first finding, by line and then by code.

| code | the rule | traced to |
|---|---|---|
| `N_SLOT_UNKNOWN` | every `{placeholder}` of a QUERY, a step, ANSWERS or EMPTY is a slot of the shape (or `{answer}`, or a bound slot) | K5 |
| `N_SLOT_REPEATED` | a slot meaning appears at most once in a SHAPE | K5 |
| `N_FRAME_TARGET` | a frame has a TARGET and a QUERY, or STEPS: not both, not neither | K6 |
| `N_QUERY_REFUSED` | **each QUERY, with sample slots, is judged by its surface** (`surface-check`) when the sentence is checked: the ledger's own court for ZQL, three terms for a pattern. A frame its surface refuses is a sentence error, not a runtime surprise | K5, G5 |
| `N_TONGUE_UNCOVERED` | every `SLOT none` meaning has words in every declared tongue | K3 |
| `N_TELL_UNCOVERED` | every frame can be told in every tongue: by its own template (ANSWERS, with an EMPTY) or by the surface's voice | K7 |
| `N_REFUSAL_UNCOVERED` | every tongue says all five kinds of refusal | K8 |
| `N_GATE_WIDENED` | a tongue's ALLOWS is a subset of the court's safe set `- ' ? , .` | K4 |
| `N_WORD_AMBIGUOUS` | a word means one thing in a tongue | K3 |
| `N_WORD_IGNORED` | a word is not both ignored and meaningful | K3 |
| `N_ENTITY_UNKNOWN` | an entity meaning is `OF` a kind its `FROM` surface enumerates | K2 |
| `N_EXAMPLE_FAILED` | each EXAMPLE text, in each tongue, is understood as the frame it MEANS | K10 |
| `N_EXAMPLE_DIVERGES` | the tongues of one example compile to the **same** query (the multilingual invariance, G2, as a law of the sentence) | K10 |
| `N_COUNTEREXAMPLE_FAILED` | each COUNTEREXAMPLE is refused, as the kind it names | K10 |
| `N_WORLD_UNREAD` | a SURFACE's WORLD is a file the court can read, from the sentence's own folder. **Found by building**: the drawing's model crashed on a missing world, and a court that cannot read a world cannot judge a single example | K1 |

## 5. The court's verbs

`<n>_court.ring <verb> <sentence.n> ...`; every answer is JSON on stdout, one object.

**One name is shared.** The Q letter's court already has an `ask` verb, `ask <file> <question> <rows json>`, which takes a *query* and *rows*. N's `ask <file> <tongue> <text>` takes a *tongue* and a *human text*. They are different courts and different arguments; an N sentence's surfaces call the Q-shaped one (`surface-run`). The name is kept because the alphabet says N asks, and is named here so nobody mistakes the one for the other.

| verb | status | arguments | answers |
|---|---|---|---|
| `check` | built | `<file> [surfaces]` | `ok` and the counts, or the first refusal; **runs 4b**. `surfaces` also asks each surface's own court to judge its queries (D-N18) |
| `diagnose` | built | `<file> [surfaces]` | the C2 envelope of every finding |
| `tokens` | built | `<file> <tongue> <text>` | the semantic form, below |
| `understand` | built | `<file> <tongue> <text>` | the frame, the surface, the closed query, the slots; or a refusal |
| `ask` | built | `<file> <tongue> <text>` | `understand`, run on the surfaces, and told |
| `vocabulary` | built | `<file> <tongue>` | the words by meaning, the entities, the aliases, the ignored words; and what is uncovered |
| `examples` | built | `<file>` | the sentence's own conformance: how many understood, diverging, refused, failing |
| `propose` | **reserved** | -- | section 10 |

A tongue is named as the sentence names it (`english`, `french`); a text is one argument. The court refuses a sentence
that has a finding, so a question is only ever asked of a sentence that has passed `check`.

**`tokens`** -- the auditable intermediate, the one thing a reader can check a question against:

    {"tongue": "english", "tokens": [{"meaning": "show", "word": "show"}, {"meaning": "deposit", "word": "deposits"},
       {"meaning": "member", "word": "Aminata", "slot": "aminata"}, {"meaning": "over", "word": "over"},
       {"meaning": "num", "word": "4000", "slot": "4000"}], "ignored": ["me", "the", "of"]}

**`understand`**

    {"frame": "ledger_over", "surface": "ledger", "query": "SELECT * FROM collect WHERE amount > 5000", "slots": {"num": "5000"}}

    a plan:  {"frame": "beneficiary_deposits", "surface": "plan", "slots": {"num": "2"},
              "steps": [{"surface": "graph", "query": "?x received_pot_in round2", "binds": "member"},
                        {"surface": "ledger", "query": "SELECT * FROM collect WHERE member = '{member}'"}]}

**`ask`** adds what the surfaces answered and how it is told. **It runs only a `pattern` surface** (a triple pattern
over the facts of the surface's world); a `query` surface -- the ledger -- is **not run by N** (D-N17): `ask` answers its
closed query and a `run` hint the host performs, `"run": [{"surface": "ledger", "court": "z_court.ring ask", "world":
"../tontine.z", "query": "SELECT * FROM collect WHERE amount > 5000"}]`, because the rows are the host's, not the
sentence's. A plan whose first step is a pattern runs it, binds the one entity, and answers the second query filled
(`query2`) and its `run` hint:

    {"frame": "graph_guarantor", "surface": "graph", "query": "?x guarantees sanda", "answer": ["boubacar"], "told": "Boubacar guarantees Sanda."}
    a ledger question: "rows": [...], "told": <the ledger's voice, in the tongue>

A plan runs its steps in order. **A step that binds needs exactly one entity**: none, and the plan stops and the frame's
`EMPTY` is told; several, and it is refused as `ambiguous`. The first step is told by the frame's `ANSWERS`, the last by
the last surface's voice.

**A refusal**, the same shape from every verb:

    {"refused": {"kind": "word", "code": "N_WORD", "what": "Mallory", "tongue": "french",
                 "message": "le mot « Mallory » ne fait pas partie du vocabulaire de la tontine"}}

Five kinds, five codes: `N_CHARACTER`, `N_WORD`, `N_SHAPE`, `N_AMBIGUOUS`, `N_SURFACE`. The message is the tongue's own
text for the kind (`REFUSES`) with `{what}` filled. Mapped to the C2 envelope for tooling (`code`, `message`, severity
`error`, `language`); **not wired here**: a question has no source line for C2's `span`.

## 6. The surface protocol

A surface is a **protocol**, never a library. N knows no ZQL and no `stzKnowledgeGraph`; it asks a court that offers:

| verb | the contract | the ledger today | the graph |
|---|---|---|---|
| `surface-check <query>` | judge a query of the grammar **without data**: lawful, or a refusal | the Z court's `ask` over no rows answers `[]` or refuses (measured: this is how `N_QUERY_REFUSED` is judged) | exactly three terms |
| `surface-run <query>` | answer as data: rows, or entities | `ask` | `Query([s, p, o])`, `?x` a variable |
| `surface-entities <kind>` | the ids of an entity kind, to generate a lexicon | -- (the ledger enumerates none) | the facts `x | is-a | <kind>` of the world artifact |
| `surface-tell <tongue> <answer>` | optional: the surface's own voice | `narrate-ask`: English as shipped, French as a second declaration | none: the frame's `ANSWERS` tell |

Implemented as written, with one convention: a surface whose `COURT` is `<file>.ring <verb>` is asked as
`<runtime> <file>.ring <verb> <world> "<query>" []`, in the court's own folder, and judges a query lawful when its stdout
is a JSON list; `triples` is judged by the court itself (exactly three terms). Only the first line of a refusal is
kept, and the nested runtime's own stderr is not an answer. The ledger needs **no change** to serve this. The graph's court does not exist as a Haro court: until the knowledge tier
(K1) provides one, an adapter over `stzKnowledgeGraph` serves the protocol, as in the study.

## 7. The gate

Before anything reads a question, each character must be: an ASCII letter or digit, the space, **any byte of 128 or
more** (the letters of other scripts), or a character of the tongue's `ALLOWS`. Anything else is refused as `character`,
naming it (a control character by its code, never printed). **`ALLOWS` can only narrow the court's safe set** `- ' ? , .`
(`N_GATE_WIDENED`): **a tongue cannot widen the gate** (K4). Of the safe set, `' ? , .` separate words and `-` joins them.

What it guarantees: **nothing a question says is evaluated.** In the study, `stzNatural`'s shipped tokenizer evaluated
bracketed text, so the gate -- not the engine -- was the closure; 16 attacks refused and a canary at 0, and at 1 with
the gate removed (STUDY E4 G3). This is **evidence, not proof**: it is an allow-list plus an argument from reading the
tokenizer, and it must be re-run if the tokenizer changes. The letter makes it a *contract of the court*, so it is no
longer an author's choice.

## 8. The one growth the rung needs: `UNDERSTAND`

The forge emits a court from a letter's meta-clauses (`ASK` gave Q its verb, `RUN` gave A its runner, `NARRATE` its
voice). N needs one, which names the kinds that play the roles:

    DEFINE UNDERSTAND n AS (
      TONGUE [tongue], MEANING [meaning], ALIAS [alias], SURFACE [surface],
      STEP [step], FRAME [frame], EXAMPLE [example], COUNTEREXAMPLE [counterexample]
    ) RATIONALE "What the forge emits tokens, understand, ask, vocabulary and examples for, and the checks of section 4b"

**Built.** The meta-court takes `UNDERSTAND` as a kind (at most one; each of the eight role clauses names exactly one
`DECLARATION`; no declaration plays two roles; each has the seats the court reads, which is how a letter that plays
the roles with other declarations is understood the same way) and reports `understands 1`. The forge adds the
language record's 23rd element, `load "n_lib.ring"` and the two globals every court now carries (`$aCourtUnderstand`,
`$bNSurfaces`); every committed court was re-forged. It is the only growth of the meta-vocabulary the drawing asked for.
The algorithm of `understand` is the model's, ported (`n_lib.ring`): gate; separators; case folding; each token ignored,
a word of a meaning, a generated entity or alias word, or digits (1 to 12); the meanings, in order, against each
frame's SHAPE; the template filled. **Found by building:** a tongue needs a `JOINS` seat (the word that joins the last
of several names in an answer: `and`, `et`) -- the drawing had put French's `et` in code.

## 9. The decisions, and what each costs

Taken on the author's standing delegation, each reversible by naming it.

| | decision | the cost |
|---|---|---|
| D-N1 | N is a **letter of Haro**: a `.haro` declaration forged to a court; its sentences are `.n` | it inherits Haro's one-voice-per-language rule (R3 of v0.13), which the study found to resist |
| D-N2 | A sentence **asks**: eight kinds, none able to declare the world, the facts or a rule | none: it is the ratified rule |
| D-N3 | **One meaning, many tongues**: a tongue is a column of each meaning; adding one is adding pairs, never code | every `SLOT none` meaning needs words in every tongue (`N_TONGUE_UNCOVERED`); a language with no word for a thing needs a decision |
| D-N4 | **Frames are exact**: a question is one frame or it is refused; nothing is guessed | **recall is low by design**, and a question with two requests in it is refused whole (STUDY resist 9) |
| D-N5 | **Names come from the world, numbers from digits**: slots are none, number or entity; **no text slot** | a name the world does not know is refused as an unknown *word*; no free-text search |
| D-N6 | **The gate is the court's**, not the author's: an allow-list that `ALLOWS` can only narrow | a language whose punctuation is outside the safe set cannot be asked in until the court widens it, in the open |
| D-N7 | **Surfaces are protocol**: N depends on no query grammar and no graph library | the graph surface has no Haro court yet: an adapter stands in |
| D-N8 | **A frame is judged by its surface when the sentence is checked** | `check` needs the surface's court to run: the ledger's court is called with sample slots -- **on `check ... surfaces` only** (D-N18); `triples` is judged always |
| D-N9 | An answer is told by the surface's voice or the frame's template; **every tongue must be coverable** | a second language is a second voice declaration for a surface that has one (the French Z court) |
| D-N10 | **Examples are part of the sentence** and `check` runs them | a sentence's check costs a run of its own conformance |
| D-N11 | **Five refusal kinds**, each said per tongue | a tongue authors five messages |
| D-N12 | **Digits only, up to 12**: a decimal, a sign, a spelled-out number or other digits are refused | `ascii` is the only `DIGITS` today; the menu is where more would go (K9) |
| D-N13 | **A plan binds exactly one entity or stops** | no plan over a set; the several-answers case is refused, not iterated |
| D-N14 | **Spelling is declared per surface** (`SPELLS`): the ledger says Moussa, the graph moussa | **a convention, not identity** (K2): it held for 6 of 6 names and fails the first name that is not `upper_first` |
| D-N15 | **The drafting half is reserved**, not drawn from a study that did not measure it | N cannot yet propose a sentence: section 10 |
| D-N16 | **Case is folded for ASCII and Latin-1 only** (the court works on bytes: U+00C0 to U+00DE except U+00D7, and A-Z) | a tongue whose script has case (Greek, Cyrillic, Turkish dotted i) is not folded until the court learns it, in the open; the model folds the same way, so the two cannot drift |
| D-N17 | **N never runs a `query` surface**: `ask` answers its closed query and a `run` hint | a host that wants the ledger's rows performs the hint itself; the told sentence of a ledger answer is the ledger's voice, not N's |
| D-N18 | **`check` asks the surfaces' own courts only on `surfaces`** (`check <file> surfaces`) | the default `check` is 0.7 s; with `surfaces` it shells out once per ledger query (rnxc 0.8 s, the oracle 2.7 s for the tontine). Without it a query the ledger refuses is not caught until the flag is given |

## 10. What is not drawn, on purpose

* **`propose`** -- N drafts a sentence of Z, W, Q, F or A, a proposal the court judges and a human ratifies; the
  ratified guard (PRINCIPLES 8) is "a fixture where N drafts a Z sentence, the court judges it, and the draft is refused
  when it names a thing the world does not declare". The study measured asking; **nothing here is derived for drafting**.
  What can be said without inventing it: the verb is reserved; its answer is a *sentence of another letter*, never
  applied; the target's own court judges it; and it must meet the same gate and the same closure. Its frames would have
  a target of kind `sentence`. That is a design for a second study.
* **The knowledge tier** (K1, K2): laws judged on load, `:Unique` from both sides, identity carried in the artifact.
  N asks a surface for entities; where they come from is not N's.
* **Hausa, Arabic** and other scripts: the menus and columns are ready; no skin was authored or tested.
* **Spelled numbers, decimals, signs, other digits**: the menu (D-N12), not the words.
* **Several requests in one question, a plan over a set, negation, a question about a question**.
* **A produced binary** and the cost of shipping `stzlib`'s tokenizer inside it: the drawing is engine-independent, and
  the model shows it, but the study's engine is still the only one measured end to end.

## 11. Traceability: the study's ten requirements

| | the study asked for | the drawing |
|---|---|---|
| K1 | a world artifact judged on load, laws that can say one-per-round | **not N's**; N asks a surface for entities (section 6, 10) |
| K2 | identity across surfaces | `SPELLS` as a **declared convention** (D-N14), `N_ENTITY_UNKNOWN`; the real fix stays the kit's |
| K3 | a pack format, a lexicon generated from the world, a coverage report | `MEANING` + `ALIAS` + generated entity words; `vocabulary`; `N_TONGUE_UNCOVERED`, `N_WORD_AMBIGUOUS`, `N_WORD_IGNORED` |
| K4 | a tokenizer with no eval path, or the gate as the contract | the gate as the **court's** (section 7); `N_GATE_WIDENED` |
| K5 | a frame language: shapes to closed targets as data, refusing the rest | `FRAME`; `N_SLOT_*`; `N_QUERY_REFUSED`; refusal as `shape` |
| K6 | a closed plan grammar | `STEP` with `BINDS`; `STEPS` on a frame; `ambiguous`; `N_FRAME_TARGET` |
| K7 | several voices per language declaration, graph answers beside ledger answers | `TELLS` on a surface, `ANSWERS`/`EMPTY` on a frame; `N_TELL_UNCOVERED` |
| K8 | refusals first-class: typed, localised, in the domain's words | `REFUSES` per tongue; five kinds and codes; `N_REFUSAL_UNCOVERED` |
| K9 | a numeric sublanguage per language | `DIGITS` menu (ascii only) |
| K10 | a question conformance format | `EXAMPLE` and `COUNTEREXAMPLE` inside the sentence; `examples`; `N_EXAMPLE_*` |

## 12. How it was judged

`python haro/spike/v17/n_check.py` (about 95 s; `--plant` fails it; guard stage 20):

    A  n_v17.haro accepted by the meta-court (its UNDERSTAND included), the forge forges N, n/tontine.n accepted by the
       forged court -- `check`, and `check ... surfaces` -- and `examples` run: both runtimes, the same bytes
    B  17 defects the declaration's own vocabulary catches: each refused with the message and the code the letter declares
    C  21 defects a rule must catch: the forged court answers the declared code as a C2 envelope citing its rule, the model
       answers the same codes, `check` refuses and the runtimes agree; the unmutated sentence has no finding, every
       ledger query judged by the ledger's own court
    C' each of the 15 codes switched off in the court in turn: its fixtures stop being caught
    D  the REAL court, asked the study's 74 questions, reproduces the study -- the closed query, the graph answer, the
       sentence told, the kind of every refusal -- one meaning sequence in both tongues of 17 of 17 pairs; the court and
       the model agree field for field on `ask` and `tokens` for all 74, and on `vocabulary` and `examples`; 19 of the
       asks, one in four, are byte-identical on the oracle
    E  the check can fail: a court without its gate is refused by the sentence's own counterexamples, and with the rules
       off too it disagrees with the study on 13 of 16 attacks

**What D does and does not show.** The sentence was derived from the study's data, so D shows the drawing can *express*
everything the study used, and that the behaviour is specifiable without `stzNatural`. It does not show that N
generalises beyond 74 questions, and it judges my own design. The court now passes the same fixtures the drawing was
judged by (the real test the drawing named); what is left is the author's reading of section 9, and a second sentence
(another domain, another language) -- the generality is still unmeasured.

## Files

    n_v17.haro  n_court.ring  n.gbnf        the letter, and the court forged from it
    n/tontine.n                              the sentence: the tontine's natural door
    n_lib.ring                               the court's dynamic half: tokens, understand, ask, vocabulary, examples, the rules
    v17/fixtures.json  v17/mk_fixtures.py    17 court cases and 21 rule cases
    v17/meta_fixtures.json  v17/mk_meta_fixtures.py   the 12 fixtures of the UNDERSTAND meta-clause (stage 1)
    v17/n_model.py                           the reference model: parse, rules, understand, ask, tokens, vocabulary, examples
    v17/n_check.py                           the judge (guard stage 20)
    v17/n_check.py  v17/probe_rejects.py     the judge; the exploration that preceded the fixtures
