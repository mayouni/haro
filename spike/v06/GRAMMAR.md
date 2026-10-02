# Haro v0.6 -- a WORLD forged whole: pairs, an expression's semantics, and WALK

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.6 is the declaring altitude of Haro grown by what a declared
WORLD needs to be forged whole -- its court AND its runtime -- from its declaration, so
that Z, the alphabet's Z letter (ZQL, canonical in StzZql, pinned by zing's 16 tontine
cases), can be declared in Haro and its sentence can be judged, evaluated and WALKED by
what the forge emits (`haro/SPIKE.md`, the sixth rung). v0.6 refuses nothing v0.5
accepted (fixture A5 is v0.5's A1, unchanged), and nothing the pinned v0.1 judge accepts.

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| a list of a `FORM` that is a name and a scalar | `fields: [field]` with `FORM field AS (SEATS [name: name, type: name])` is written `FIELDS [id: uuid, amount: currency, status: deposit_status]` | an entity's fields are name: type pairs in every ZQL program; the Commons had no pair in a list. The rule is narrow on purpose: a FORM of exactly two seats, the first a `name`, the second a scalar (a primitive, a MENU, a RANGE, a FORMAT) is written as pairs (A1); a pair cannot hold a reference (R8); EVERY OTHER FORM keeps v0.1's reading -- its items follow its first seat -- because the pinned v0.1 judge lists a six-seat FORM (`[step]`) and v0.6 refuses nothing it accepts (HF-48) |
| `ABSENT`, `DIVISION`, `EQUALITY` on an `EXPRESSION` | `ABSENT zero`, `missing` (since v0.7) or `refuse`; `DIVISION calm` or `refuse`; `EQUALITY kind` or `value` | the three places where two correct evaluators of one grammar disagree, declared instead of assumed. ZQL (zql.zig, zql.js): a reference to nothing counts as 0, a division by zero yields 0, a numeric text and its number are one value (`"7500" > 0`). W: a number and a text are never equal. Each takes a closed word (R1, R2, R3); undeclared, the evaluator keeps W's rules |
| a seat typed by an `EXPRESSION` | `rule: zexpr`, `validate: zexpr?`, `formula: zexpr?` | v0.1 admitted the type; v0.6's court PARSES the seat's text with the expression's own menus when it judges the sentence (A3): `RULE "amount >> 0"` is refused at `check`, not at the first record |
| `WALK` | `OF` the walked kind, `STEPS` the steps' kind, `THROUGH` the step's reference to its walk, `ORDER` its rank, `GUARDS` the expression seats that must hold (a path reads through a reference: `enforcing.rule`), `COMPUTE` and `FORMULA` the computed field and its expression, `FAIL` the seat naming the failure | the one kinetic declaration: a record walks a flow's steps in order, and each step's guards must hold. What ZQL's runner hard-codes (steps run in order; VALIDATE, then the ENFORCING norm's RULE; FORMULA first, its result joining the record for this step and every later one; a failed guard halts the flow at that step with its ON_FAIL) is a declaration now, and the forge emits the walker. `OF` and `STEPS` name declarations (R4); `THROUGH` is a seat of the steps' kind that refers to the walked kind (R5); every guard is an expression seat, directly or through one reference (R6); a kind is walked once (R7); `COMPUTE` and `FORMULA` go together (R9) |

The expression grammar is W's, grown where the menus admit it: a bare name is a reference
into the record (`ref`; `a.b` a path), `SUM(path)` and its kin an aggregate (`agg`, over
the `AGGREGATES` menu), `ROUND(x)` an operator, `CONTAINS` a comparison, `true` and
`false` flags. A word's meaning is fixed by the menus and by what follows it, never by its
case: `AND` and `and` are one word, `COUNT(` is a call. A language whose menu has no `ref`
still refuses a bare name by name, as W does.

## Grammar (EBNF), the v0.5 text with these additions

```
EXPRESSION:  OPERATORS name_list, OPERANDS name_list, AGGREGATES name_list,
             VARIABLES name_list, CONTEXTS context_list,
             ABSENT IDENT, DIVISION IDENT, EQUALITY IDENT
WALK:        OF IDENT, STEPS IDENT, THROUGH IDENT, ORDER IDENT, GUARDS path_list,
             COMPUTE IDENT, FORMULA IDENT, FAIL IDENT
path_list    = "[" path { "," path } [ "," ] "]" ;
path         = IDENT { "." IDENT } ;

in a SENTENCE of the declared language:
pair_list    = "[" pair { "," pair } [ "," ] "]" ;
pair         = IDENT ":" ( IDENT | STRING | NUMBER ) ;
```

## What the forge makes of it

A language with declarations is forged into `<lang>_court.ring` and `<lang>.gbnf` as
before; when it also declares an EXPRESSION, the court loads `expr_lib.ring` (and only
then: a court carries what its language says, and the machine court's edit-to-verdict
stayed under its 100 ms target only once the load was conditional, HF-49), its record
carries the expression's tables and its WALKs, and `<lang>_expr.ring` and
`<lang>_expr.gbnf` are emitted beside it. The sentence court gains two verbs:

```
<lang>_court.ring eval <file> <decl> <seat> <json>    true | false
<lang>_court.ring walk <file> <name> <json>           {"status": "complete", "computed": {...}}
                                                      {"status": "failed", "at": step, "code": ..., "reason": ...}
```

`eval` evaluates one expression seat of one declaration on a record (a JSON object). `walk`
takes the WALK of the named declaration's kind, collects every step whose THROUGH seat
names it, orders them by ORDER, and at each: computes the FORMULA into the COMPUTE seat's
name first (an overlay the references read before the record, as zing's runner does),
then evaluates each GUARD in the WALK's order; the first that does not hold stops the
walk, naming the step, the FAIL seat's value when written, and a reason -- `VALIDATE
failed` for a direct seat, the referenced declaration's `message` seat for a guard read
through a reference. The grammar for the decoder gains `pairlist` (emitted when a kind
writes one), `reference`, `aggregate`, `flag`, `ROUND` and `CONTAINS` where the menus
admit them.

## Semantics the evaluator keeps, and which declaration chose them

Under `EQUALITY value` a comparison is numeric when both sides can be numbers (a number,
a numeric text, a flag) and by text otherwise, byte by byte -- by hand, because Ring's own
`<` on two strings is R41 (HF-30); `CONTAINS` is a case-blind substring test; arithmetic
reads a value that is not a number as 0. Under `ABSENT zero` a reference to nothing reads
as 0 and an aggregate over no list answers 0; under `refuse` the evaluation is refused by
name. Under `DIVISION calm` a division by zero is 0; under `refuse` it is refused;
undeclared, it is the host's (R1 on both runtimes). `ROUND` rounds half away from zero.
Numbers print as JSON (`84`, not `84.00`); an object as `{"k": v}`; `true` and `false`
are read as 1 and 0.

## Measured

`z_v06.haro` declares Z in the Commons' shape and `tontine.z` is zing's fixture source
re-expressed in it (HF-47); the guard's stage 9 judges the 16 cases on the forged court
unadapted: 4 norms on records (`eval`), 8 flows on records with their computed fields
(`walk`; a step is lower_snake here where ZQL names it UPPER, so `at` is compared
case-blind), 4 destructive rejects (`check`). 16 of 16 on `rnxc` and on the oracle,
byte-identical, on the first run; the four artefacts byte-identical on both runtimes;
W's 29 unchanged under the grown tokenizer; the machine court 117 of 120 and the fleet
court 32 of 32 unchanged. Pinned at 16.
