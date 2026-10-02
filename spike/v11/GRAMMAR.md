# Haro v0.11 -- the Diagnostic Contract: CODE, CODES and CITES

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.11 is the declaring altitude of Haro grown by what the family's
Diagnostic Contract asks of a court that wants to speak it -- C2 v1.2.0,
`stzzui/doc/diagnostic-contract.md`: six fields never omitted or renamed (`code`,
`severity`, `message`, `span`, `cites`, `language`), one object carrying `diagnostics`,
codes the court's own stable identifiers, cites by the pinned instrument's identifier and
empty where no law applies, no bare `true`, `false` or `null` anywhere -- and by nothing
else. v0.10's record said the envelope "is a decision for the family's courts together,
not this one's alone"; the family took it in C2, and RingFlex's court already speaks it.
v0.11 refuses nothing v0.10 accepted (fixture A3 is v0.10's A1, unchanged).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `CODE` on a `CONSTRAINT`, a `UNION`, a `MENU`, a `RANGE`, a `FORMAT`, a `SYMBOL` or a `REFUSAL` | the stable identifier the court's refusal carries when that element refuses: `CODE "C7"`, `CODE "UNRESOLVED_FLOW"`, `CODE "PARSE"` | C2 2.1: "stable identifiers the consumer can branch on, never the message"; the format is the contract's, `[A-Z][A-Z0-9]*` with `_` or `-` between parts (R1). An element without a CODE refuses under a default of its kind -- `CONSTRAINT`, `UNION`, `MENU`, `RANGE`, `FORMAT`, `UNRESOLVED`, `REQUIRED`, `DANGLING` -- cited as `rule:<element name>`, so no refusal ever leaves without an identifier (A1) |
| `CODES` on a `DECLARATION` | `[seat: "CODE", ...]`, a code per seat beside `MESSAGES`: the code a missing or dangling seat refuses under | RingFlex's C1, C2, C4, C9 to C12 are each a seat's law: a required TIMEOUT is C1 on a human task and C2 on an event wait, the same seat under two codes, so the code belongs to the seat on the declaration, where MESSAGES already put the words (A2); CODES name a seat (R2) |
| `CODES` on a `REFUSAL` | `[word: "CODE", ...]`, a code per `NAMED` word | RingFlex refuses the word `FLOW` as `FLOW_IS_ZQL` and `INVOKED_BY` as `SEAM_UPWARD`, both under `unknown_declaration`; the word is the law (A2); CODES name a NAMED word (R4) |
| `CITES` on a `SYMBOL` or a `REFUSAL` | `["kind:value", ...]`, the pinned instruments the refusal cites | C2 2.5: a cite is `kind:value`, kind in `rule`, `article`, `right`, `pattern`, "empty where no law applies, never omitted" (R3). The seam refusals cite `article:placement-3`, the resolution ones `article:placement-3.2`, exactly as RingFlex's do; a grammar refusal (`PARSE`) cites nothing, by the contract's own reading |

## Grammar (EBNF), the v0.10 text with these additions

```
CONSTRAINT:  ON IDENT, WHEN string, THEN string, MESSAGE string, CODE string
UNION:       OF type_list, MESSAGE string, CODE string
MENU:        WORDS name_list, MESSAGE string, CODE string
RANGE:       MIN number, MAX number, MESSAGE string, CODE string
FORMAT:      SHAPE IDENT, FOLD IDENT, MESSAGE string, CODE string
SYMBOL:      KIND string, REF string, MESSAGE string, CODE string, CITES string_list
REFUSAL:     MESSAGE string, NAMED message_list, CODE string, CODES message_list,
             CITES string_list
DECLARATION: VERB string, SEATS seat_list, NAMES IDENT, MESSAGES message_list,
             CODES message_list
string_list  = "[" STRING { "," STRING } [ "," ] "]" ;
```

## What the forge makes of it

Every forged court gains one verb, and no court loses a byte of what it printed before:

```
<lang>_court.ring diagnose <file> [<world.json>]
```

The same court, the same passes, the same first refusal -- answered as the family's one
object. A refusal is one `error` carrying the code and cites of the element that refused:
a CONSTRAINT's CODE on the declaration's line, a seat's CODES on a required or dangling
seat, a MENU's or FORMAT's or UNION's CODE where the value fails it, a SYMBOL's CODE and
CITES where the world lacks the name, a REFUSAL's CODES per NAMED word on an unknown
declaration. A refusal no element owns -- the grammar's own, a duplicate name, the WORLD's
cardinality -- is `PARSE`, `DUPLICATE_NAME`, `WORLD_ONE`, `WORLD_FIRST`, `SENTENCE` or
`CYCLE` (the A runner's), with no cites where the contract says a grammar diagnostic
enforces no pinned instrument. A sentence with SYMBOL seats and no world is one `warning`,
`NO_WORLD`, at line 0, citing what the SYMBOL cites (RingFlex's reading, kept). A clean
sentence is `{"diagnostics": []}`, which a consumer can tell from no output at all. The
`language` is the court's own name; the `span` is the file as given and the refusing
line; `col` is not emitted, which the contract permits.

Inside the court the change is one function: every refusal that enforces a declared
element goes through `CtFailC(line, code, cites, message)`, which records the code and
cites in two globals the `diagnose` verb reads after the catch, and then raises exactly
the one-line refusal `check` prints. A typed check that returns its text instead of
raising records the code before returning (`CtSetCode`). `check` is unchanged to the
byte on every fixture of every rung.

## Measured

`f_v11.haro` is `f_v10.haro` with RingFlex's own codes declared where its court raises
them: `CODES` per seat on actor, invocation, human task, event wait, decision and
suspension (C1, C2, C4, C9 to C12), `CODE` on the sixteen constraints (C6, C7, C8, C15,
C3 ...), on the two unions (C5, C10), on the flow SYMBOL (`UNRESOLVED_FLOW`, citing
`article:placement-3.2`), and on the two `unknown_declaration` refusals -- `FLOW_IS_ZQL`
and `SEAM_UPWARD` per NAMED word, `PARSE` for the deleted forms, citing
`article:placement-3`. The 27 F fixtures, the 16 + 25 Z cases, the 35 A cases and the
world's nine checks are unchanged on it.

The guard's stage 14 judges the envelope three ways. The contract's shape, by hand
against the schema's rules (no `jsonschema` module here), on every diagnostic every
forged court emits over its fixtures -- 27 F fixtures, Z's `tontine.z`, A's `w_in_a.a`,
the machine's `qemu_hello.machine`, an unknown verb and a cyclic algorithm. Then the
codes: every F fixture's error carries the code its `-- EXPECT:` line names, the cite
RingFlex gives it (`rule:Cn`, `article:placement-3`, nothing for PARSE), on a line of the
file; the resolution against RingFlex's world fixtures gives `UNRESOLVED_FLOW` citing
`article:placement-3.2` on the step's line and `NO_WORLD` a warning at line 0. Then
RingFlex's court itself, run live under official Ring 1.27 on its 24 original fixtures and
four worlds through `rf_diag.ring` (read-only): the same first code, the same cites and
the same severities as the forged court on the re-expressed fixtures, all 28. The same
bytes on `rnxc` and the oracle on every `diagnose` run, first run of the codes.

## What it does not do, named

- `col` is not emitted; the court knows lines, not columns.
- One error per run: the court stops at its first refusal, as every rung before, so
  `diagnostics` holds at most one error and at most one warning. The contract allows
  many; a court that collects is a later rung.
- `why`, `todo` and `frames`, the extensions v0.1's trust refusal carries, are not in
  this envelope: v0.11 emits the six fields the contract requires and nothing beside
  them.
- The W, Q and A verbs (`eval`, `walk`, `ask`, `run`) keep their own answers; `diagnose`
  judges the sentence, not a run of it.
