# Haro v0.5 -- an expression language forged whole: CONTEXTS on an EXPRESSION

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.5 is the declaring altitude of Haro grown by one clause, so that a
language that is only an expression -- stz's W, the alphabet's W letter: `@item > 2`,
`2*@item`, `@accumulator + @item` -- can be declared and forged whole, its court AND its
evaluator, from its declaration, and judged by its own 29 fixtures unadapted
(`haro/SPIKE.md`, the fifth rung). v0.5 refuses nothing v0.4 accepted (fixture A3 is v0.4's
A6, unchanged).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `CONTEXTS` on an `EXPRESSION` | `[seat: [variables], ...]` | the seats a host offers the expression and which of its `VARIABLES` each admits: `map: [item]`, `reduce: [accumulator, item]`, `eval: []`. W's own rule -- "the variables an expression may use are FIXED BY ITS SEAT; an unknown `@name` is refused at compile time, by name, never silently nil" -- was a sentence of its prose and a table in its Luau; it is a clause now. A context names only `VARIABLES` (R1), needs them (R2), and is named once (R3). Without `CONTEXTS` every seat admits every variable, as v0.1 read it (A2) |

The `EXPRESSION` kind itself is v0.1's, unchanged: `OPERATORS` and `OPERANDS` from the
closed menus (`or and not cmp contains add sub mul div mod round neg`; `number text flag
ref var agg`), `AGGREGATES`, `VARIABLES`, and the coherence rules both ways. An operator
the menu lacks is still unexpressible, not forbidden (R4).

## Grammar (EBNF), the v0.4 text with one addition

```
EXPRESSION:  OPERATORS name_list, OPERANDS name_list, AGGREGATES name_list,
             VARIABLES name_list, CONTEXTS context_list
context_list = "[" context { "," context } [ "," ] "]" ;
context      = IDENT ":" name_list ;
```

## What the forge makes of it

A language whose declaration holds an `EXPRESSION` is forged into `<lang>_expr.ring`, a
court and an evaluator over `expr_lib.ring`: `check <seat> "<expr>"` answers `ok` or
`refused: why`; `eval <seat> "<expr>" [input] [init]` answers the value as JSON. The
grammar the evaluator reads is W's, the one expression shape the estate declares --
`or < and < not < comparison < additive < multiplicative < unary < primary` -- and the
declaration gates it: an operator outside the menu is refused by name
(`'*' is not an operator of w`), an operand kind outside the menu likewise, a variable
outside the seat as W refuses it (`unknown variable @nosuch in this seat`). The seats a
host gives a list expression -- `eval`, `map`, `filter`, `count`, `partition`, `groupby`,
`reduce`, `reduce_noinit` -- are the harness's operations (stz's list face,
`experiment/run_w.luau`), implemented once in `expr_lib.ring` so the forged evaluator is
judged by W's own fixtures and nothing else. A language with declarations AND an
expression gets both courts; one with only an expression gets the expression court alone.

The grammar for the decoder (`<lang>_expr.gbnf`) is emitted from the menus: a rule per
precedence level, present when the declaration admits its operators, the operands it
admits, and the variables by name. A word operator is set off by at least one space in
the grammar, because `not1` and `@itemand` are one word to the tokenizer -- the first
sample of 200 derivations found 165 of them glued that way.

## Semantics the evaluator keeps from W's text

Numbers are the host's numbers; `/` is real division, `%` the mathematical modulo; `=` is
equality, `!=` and `<>` one operator, comparison non-associative. A comparison answers 1
or 0; `and`, `or` and `not` take the truth of their operands, where a number is true when
it is not 0 and a string is always true (the Luau host's rule). A number and a string are
never equal, whatever the host's own `=` would say. Values print as JSON: a whole number
without a point, `7 / 2` as `3.5`, a string quoted, a list bracketed, a group as
`["1", [1, 3, 5]]` with its key as text.

## What v0.5 still cannot say, named

`contains`, `round` and the aggregates (`sum count avg min max`) are in the menus and not
in the evaluator: W v0.1 admits none of them, so no fixture asks. A second EXPRESSION in
one declaration is accepted by the meta-court and ignored by the forge, which emits the
first. The seats' operations belong to the harness, not to the declaration: a host that
offers an expression a seat the eight do not name gets `check` for it, and `eval` with no
variable bound.
