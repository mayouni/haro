# Haro v0.7 -- the Q letter: ASK, a declared world's own question grammar

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second), and after `q_cases.json`, which is zing's. v0.7 is the declaring
altitude of Haro grown by one kind, so that a declared WORLD answers questions in one
closed grammar forged from its declaration -- the `ASK` row of `haro/CHARTER.md` section
3, "the language's own closed query grammar (the Q letter)", and 06-ALPHABET's route 3,
"then Q (smallest new grammar: ZQL's SELECT extracted)". v0.7 refuses nothing v0.6
accepted (fixture A4 is v0.6's A4, unchanged).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `ASK` | `FROM [kinds]` the kinds a question may name after FROM; `WHERE expression` the EXPRESSION a condition is written in; `CLAUSES [where, order, limit]` the optional clauses the question admits | ZQL's one READ verb (StzZql `GRAMMAR.md` 6; zing `cli/src/zql.zig` parseQuery): `SELECT * FROM name [WHERE expr] [ORDER BY field [ASC \| DESC]] [LIMIT n]`. The grammar is fixed, as W's is; the declaration says what it ranges over and what it admits. FROM names DECLARATIONs (R1) and at least one (R6); WHERE names an EXPRESSION (R2); CLAUSES is the closed menu where, order, limit (R3); a question that admits where names its expression (R4), and an expression no clause admits is unexpressible (R7); a language asks in one grammar (R5) |
| `ABSENT missing` on an `EXPRESSION` | a third word beside `zero` and `refuse` | zing's `.missing` (zql.zig resolveCtx, asNum, asStr, orderValues): a reference to nothing is 0 to arithmetic, the empty text to a comparison, and first in an order. v0.6's `zero` read it as 0 everywhere, which the 16 tontine cases could not tell apart (every record carried every field) and which `WHERE round = 1` on a record with no round does tell: `""` is not `1`, and `0 >= 0` would have been true where zing's `"" >= "0"` is false (HF-50). Z declares `missing` since v0.7 (A3, R8) |

## Grammar (EBNF), the v0.6 text with these additions

```
ASK:         FROM name_list, WHERE IDENT, CLAUSES name_list

a question of the declared language (the ask verb):
question     = "SELECT" "*" "FROM" IDENT [ "WHERE" expr ]
               [ "ORDER" "BY" field [ "ASC" | "DESC" ] ] [ "LIMIT" NUMBER ] ;
field        = IDENT { "." IDENT } ;
```

The keywords are the upper-case words, as zing reads them; a lower-case `order` is a
field. A clause out of its place is "Unexpected 'ORDER' after the question", zing's own
words; a clause the ASK does not admit is refused by name.

## What the forge makes of it

A language that declares an ASK gets `<lang>_ask.gbnf`, its question grammar for the
decoder -- the frame, then only the clauses it admits, over its WHERE expression's own
grammar -- and its sentence court loads `ask_lib.ring` and gains the verb:

```
<lang>_court.ring ask <file> "<question>" <rows json>     the matching records, a JSON list
```

The rows are the harness's: the declared altitude holds no store (CHARTER section 3,
"never a mutable runtime store"), so the records that walked the FROM declaration are
handed in, as zing hands its ledger's committed records. FROM must name a declaration of
one of the ASK's kinds -- a name that resolves to nothing is refused, where zing lists
nothing (HF-51, the one divergence, recorded and kept). WHERE must be a CONDITION: a
comparison, and, or, not, a flag; an arithmetic node, a reference or a text has no truth
(zql.zig evalExpr; zing refuses `WHERE amount` too), and the same rule now judges a
WALK's guards and the `eval` verb. ORDER BY orders by a field: numeric when both values
can be numbers, by bytes otherwise, a missing field first, ties in the records' own
order. LIMIT keeps the first n; `LIMIT 0` keeps none. A question never writes.

## Measured

`z_v07.haro` is `z_v06.haro` plus the ASK and `ABSENT missing`; the sixth rung's 16 cases
pass on it unchanged, and the eight flow cases answer identically with every STEP
declared in reverse (HF-52). `q_cases.json` holds 25 questions and zing's own answers to
them, captured on a scratch copy of zing's `examples/bedrock-query` -- its ledger of 6
committed deposits plus 4 replayed through `zing flow` (a numeric text amount, a record
with no round, a tie, a lowercase name) -- and the guard's stage 10 re-runs zing live on
the same replay when it is built here: zing agrees with the file on 24 of 24 judged
questions, and the forged `ask` verb answers 25 of 25 on `rnxc` and the oracle,
byte-identical. The 25th, `SELECT * FROM nowhere`, is the divergence above. Pinned at
25. The machine court 117 of 120, the fleet court 32 of 32 and W 29 of 29 unchanged.

## What it found

- **HF-50**, ABSENT zero was not zql's missing (above).
- **HF-51**, zing does not resolve a question's FROM against the declaration: `SELECT *
  FROM nowhere` lists nothing. The declared altitude refuses a name that resolves to
  nothing, as it does a step's FLOW; a proposal for zing.
- **HF-52**, Ring's `insert(list, i, x)` puts x AFTER position i. The stable sort behind
  ORDER BY and the walk's ordering of steps both inserted "before j" at j, and the head
  never moved: eight ORDER BY questions failed on the first run, every one with the first
  record stuck in place, while the sixth rung's walk had passed because the tontine's
  steps are declared in order. Both insert at j-1 now, and stage 9 walks the sentence
  with its steps reversed.
