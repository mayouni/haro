# Haro v0.8 -- the F letter: what a flow of work needs, and nothing else

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.8 is the declaring altitude of Haro grown by exactly what F --
the alphabet's F letter, RingFlex's `.wflow` v0 re-declared (`haro/SPIKE.md`, the eighth
rung) -- needs: nothing was added because it seemed useful, which is RingFlex's own
extraction rule. v0.8 refuses nothing v0.7 accepted (fixture A5 is v0.7's A1, unchanged);
it ADMITS two things earlier fixtures refused, and both are rewritten and recorded below.

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `NAMED` on a `REFUSAL` | `[word: "message", ...]` on `unknown_declaration` or `unknown_seat` (R1) | RingFlex refuses `FLOW`, `INVOKED_BY`, `FOREVER`, `CALLED_BY`, `VERDICT OF` and `DECISION OF` BY NAME: "an author who writes it is reaching for something real and deserves to be told which law they met, not that the declaration set is closed". A known trespasser's word gets its own message; the category's message speaks for the rest (A1) |
| a pair list keyed by a `MENU` or a `DECLARATION` | `FORM action AS (SEATS [verb: breach_actions, target: name])`, `FORM branch AS (SEATS [guard: guard, target: node])` | an escalation's actions are an ORDERED SEQUENCE whose verbs repeat (`NOTIFY x THEN NOTIFY y`): keyed by a MENU, keys may repeat; a routing's branches are keyed by GUARDs: keys resolve (C12). A key that is a name is a map: named twice is refused. A pair's value may be a reference -- a DECLARATION or a UNION of declarations -- since routes lead to targets (A2); never an EXPRESSION (R7, v0.6's R8 rewritten) |
| a `UNION` of `DECLARATION`s | `UNION node AS (OF [invocation, task, ..., terminal, suspended])` | an arrow's target is a step, a terminal or a suspension: one word, several kinds. DECLARATIONs share the shape "word" and are told apart by the name's resolution, in one namespace; the union's MESSAGE speaks when the word resolves to none (C5, C10). A DECLARATION beside a MENU is still refused -- a word would be either (R2; v0.3's R5 rewritten) |
| the shapes `duration`, `landmark`, `deadline` | `FORMAT deadline AS (SHAPE deadline, MESSAGE ...)` | RingFlex 5.4: `duration = number time-unit`, the one landmark form `the Nth working day of next month`; a deadline is either, and "no duration or landmark may read instance data" -- `2 working days after date_convenue` is not a deadline, and the FORMAT's own message says why (A3, R8) |
| `ENTRY` on the `WORLD` | `WORLD f AS (ONE [workflow], FIRST workflow, ENTRY [invocation, task, ...])` | "the entry step is the first STEP declared, by position": the first declaration of one of the ENTRY kinds is where a walk starts (A3, R4) |
| `self reachable`, `self referenced`, `pairs keyed_by names` | three closed relations, each a fixed line of the court | C6 and C7 (reachable from the entry, through the ENTRY kinds' reference seats -- an ending's seats are not arrows), C15 (named by some reference seat of the sentence), C8 (a pair list's keys are exactly a name list's words, `{other}` the first that is not). Each is total; each takes `self`, or a pair list and a name list, and nothing else (A4, R3, R5, R6) |

## Grammar (EBNF), the v0.7 text with these additions

```
REFUSAL:     MESSAGE string, NAMED message_list
WORLD:       ONE name_list, FIRST IDENT, ENTRY name_list
UNION:       OF type_list -- an alternative may be a DECLARATION
shape        = ... | "duration" | "landmark" | "deadline" ;
atom         = ... | "self" "reachable" | "self" "referenced" | path "keyed_by" path ;

in a sentence of the declared language:
pair         = IDENT ":" ( IDENT | STRING | NUMBER ) ;   -- the key a name, a MENU word or a declaration's name
duration     = NUMBER ( "seconds" | "minutes" | "hours" | "days" | "working" ( "day" | "days" ) ) ;
landmark     = "the" NUMBER ( "st" | "nd" | "rd" | "th" ) "working" "day" "of" "next" "month" ;
```

## What the forge makes of it

Nothing new in kind: `f_court.ring` and `f.gbnf` as every sentence language gets. The
court's references pass (v0.3: "the references, last") now judges every reference a
sentence can hold -- a scalar DECLARATION seat, a UNION of declarations, a list of
references, a pair list's keys and values -- and a pair list's local facts (a MENU key,
a scalar value, a name named twice) in the local pass before it. The tokenizer's one
refusal for a character the grammar lacks carries the language's `unexpected_character`
MESSAGE, so `GUARD g AS (NORM score > 5)` is told "there is no production that can parse
an operator" in RingFlex's words.

## F, re-declared, and what the re-expression is

`f_v08.haro` declares RingFlex's grammar-v0 in the Commons' shape: the eleven
declarations become thirteen kinds (a step is exactly one of six kinds, so each kind is a
declaration: INVOCATION, TASK, EVENT_WAIT, TIMER_WAIT, ROUTING, COMPENSATION), the arrows
are reference seats typed by the `node` union, `TIMEOUT 3 working days -> x` is two seats
(a deadline and a target), `IRREVERSIBLE` is a flag, an escalation's `ON BREACH` chain is
a MENU-keyed pair list, a routing's `WHEN` branches a GUARD-keyed one, a task's `ON
decision -> target` arms a name-keyed one. The fifteen rules of its structural court are:
required seats with MESSAGES (C1, C2, C4), the union's MESSAGE (C5, C10), reference seats
with MESSAGES (C9, C10, C11, C12), the Commons' own RATIONALE (C13) and one namespace
(C14), and CONSTRAINTs for C3, C6, C7, C8, C9 and C15 -- each message carrying its code,
which is what the judge reads. There are no expressions: the one EXPRESSION kind is
absent, and the grammar has no production that can parse an operator.

**What the re-expression costs, named**: RingFlex's ACTOR and GUARD carry no RATIONALE;
the Commons requires one on every declaration, so the fixtures in `f/` gain them. RingFlex
writes a step's kind by its first keyword; the Commons writes it as the declaration's
kind. `NOT_ON [REJECTED]` is `NOT_ON [rejected]`, `OUTCOME SUCCESS` is `OUTCOME success`.
Three refusals are refused by a different mechanism than RingFlex's parser and say
RingFlex's words through the declaration: the deleted guard forms, the upward seam, the
operator. Not expressed: `TRANSITION TO` an escalation's target is typed `name` where
RingFlex checks it resolves (C5) and `NOTIFY`/`REASSIGN TO` an actor (C11); no fixture
pins either, and a pair's value has one type.

## Measured

`haro/spike/f/` holds RingFlex's 24 one-defect fixtures and its two reference workflows
re-expressed in the Commons' shape, each keeping its first line -- `-- EXPECT: clean`,
`refuse Cn`, `parse-error <fragment>` -- as RingFlex's runner reads it. The guard's stage
11 judges the forged court against those lines: 26 of 26 on `rnxc` and the oracle,
byte-identical, on the first run; and RingFlex's own court (`src/wflow.ring` under
official Ring 1.27, read-only -- its runner loads Ring's full `stdlib.ring`, which the
oracle cannot) holds the same 26 expectations on the original files. Pinned at 26.

## What it reverses, and says so

- v0.3's R5 pinned "an alternative is a value type ... never a DECLARATION". v0.8 admits
  a DECLARATION, and the fixture now pins what is still refused: a DECLARATION beside a
  MENU.
- v0.6's R8 pinned "a pair cannot hold a reference". v0.8 admits one, and the fixture now
  pins what is still refused: a pair holding an EXPRESSION.

A later growth may reverse an earlier fixture; it may not do so silently. Both reversals
are recorded here, in `haro/FINDINGS.md` (HF-55), and in the fixtures' own names.
