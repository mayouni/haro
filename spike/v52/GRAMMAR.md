# Haro v0.52 -- numbers: three kinds, each saying whether it is exact

D55 T4 (`TYPES.md`, ruled by the author 2026-11-07, decision (c) "yes; measurement 2 before its rung"), started on his "start the next
type rung" (2026-11-10). In a `.haro` file:

| type | letter | written | exact |
|---|---|---|---|
| `integer` | `i` | `12` | whole, to 64 bits (v0.43) |
| `decimal` | `d` | `12.50` | to its digits: a 64-bit coefficient and up to 18 digits after the point |
| `float` | `f` | `0.5f`, `2f` | near, never exact |

`n` is any of the three. A `.ring` file reads its numbers as it always has, and a decimal reaching `.ring` code, or Softanza's engine, is
the double it is nearest.

Fixtures first (ce9a538: 23 cases, 19 failing before the code; N03, N07, N20, N23 held and guard). Code c5ed99a. **Changed after the
code, said so**: N22 gained `String(0.125)` -- Ring's two places print `12.50` too, so only a digit past them shows that `String` is the
decimal's own text; and N24 to N30 were added, each for a protection the plants found no case asking about. **Earlier rungs' fixtures
changed by this ruling, said so**: v0.43's B17 (`3 + 0.5` is `3.5`, no longer the double `3.50`), v0.44's Q04 (the NaN is ordered
against `0f`, and its `=` and `!=` lines go: two floats are never claimed equal now), v0.47's Y01 (`fX = 0.5f`; `nX = 2.5` prints `2.5`)
and Y12 ("this literal is a decimal"), and v0.47's plant L4 (an integer letter taking a decimal literal).

| line | what | cases |
|---|---|---|
| N1 | a literal with a point is a decimal: exact (`0.1 + 0.2 = 0.3`), printed as its digits (`12.50`), compared by value (`0.10 = 0.1`), exactly past a double's digits, `DECIMAL` to `Type()`; through the compiled image it keeps its digits | N01, N03, N22, N25, N29 |
| N2 | a literal ending in `f` is a float; a float's arithmetic stays a float | N08, N24 |
| N3 | `+ - * %` on decimals and integers are exact -- an integer joins a decimal; `+ -` keep the larger scale, `*` adds them, `%` has the dividend's sign; past 64 bits of digits, DECIMAL_OVERFLOW | N02, N21, N28 |
| N4 | `/` on integers and decimals is the exact decimal in the fewest digits (`7 / 2 = 3.5`, `10 / 5 = 2`), or DECIMAL_INEXACT when it has no end (`1 / 3`); `Divide(a, b, iPlaces)` rounds half to even; by zero, Ring's R1 | N04, N05, N06, N23 |
| N5 | a float mixes with neither a decimal nor an integer: NUMBER_MIX names the conversion; the operator named is the one written; a float is negated | N09, N10, N11, N27 |
| N6 | `=` and `!=` on two floats are refused, FLOAT_EQUALITY naming `Near`; the orderings stand | N12, N13 |
| N7 | `Near(fA, fB, fTolerance)`: the distance at most the tolerance | N14 |
| N8 | `Float(x)`, `Decimal(x)`, `Decimal(x, iPlaces)`, `Integer(x)` convert, each refusing what it cannot say exactly | N15, N16, N17 |
| N9 | the letters: `d` a decimal, `f` a float, `n` any number, each checked as a value is given | N18, N19, N30 |
| N10 | a `.ring` file reads as it did and has none of the five built-ins; a decimal is a double in `.ring` code | N07, N20, N26 |

## The desk's readings inside T4 (D64)

T4 rules the three kinds, the literal, the one widening, and float equality. What it leaves to the rung, read by the desk and judged above:

- **A decimal keeps the digits written**: `12.50` is not `12.5`, as an amount of money is not. `+` and `-` keep the larger scale, `*`
  adds the scales (`1.25 * 1.2 = 1.500`), and `=` compares values.
- **`/` is exact or refused**: on integers and decimals it answers the exact quotient in the fewest digits, so `7 / 2` is the decimal
  `3.5` -- a `.haro` file's division of two integers is no longer a float -- and a quotient with no end is DECIMAL_INEXACT, naming
  `Divide(a, b, iPlaces)` (half to even, the rounding that adds no bias) and `Float(a) / Float(b)`.
- **A float mixes with no other number**, an integer included: T4 widens only an integer into a decimal.
- **The width**: 64 bits of coefficient and 18 digits of scale -- every amount of money and every measure a world declares -- with
  DECIMAL_OVERFLOW past it, as INTEGER_OVERFLOW past 64 bits.
- **Five built-ins of Haro's own**, in a `.haro` file only: `Float`, `Decimal`, `Integer`, `Divide`, `Near`. `Type()` names a decimal
  `DECIMAL` and keeps `NUMBER` for an integer and a float, the word a `.ring` file shares.

## How it is built

- `vm/src/decimal.zig`: the decimal, pure -- add, subtract, multiply, the exact quotient (the reduced divisor must be 2^p 5^q), the
  rounded quotient, the remainder, comparison, text, parsing.
- `main.zig`: a tag `dec`, the coefficient in the value's payload and the scale in its spare 32 bits, so a decimal costs no allocation.
  Every arithmetic operator's number path asks once, `haroNum`, whether a decimal or a float meets it in Haro's code; Ring's code keeps
  its doubles. `/` asks it for two integers too. `=` and the orderings refuse in `preEq` and `preCmp`, where the `.haro` checks
  already stood; equality and ordering are exact between decimals and integers.
- `compile.zig`: a literal with a point is a decimal constant, one ending in `f` a float constant (a hex literal's `F` is a digit); the
  literal letters are `i`, `d`, `f`; a constant folds into an immediate operand only beside a proven integer, so a refusal names the
  operator written; the five built-ins are compiled in a `.haro` file only.
- The image and the prefix (VERSION 5) carry a decimal's scale in the length field only a string used; the engine boundary hands a
  decimal over as a double, in an argument and in a list.

## Measured

- **Measurement 2** (owed before the rung, TYPES.md section 8): Haro's own `.haro` code holds 15 literals with a point in 274 files, and
  a `.ring` file never reads a decimal, so stzMax -- a `.ring` program -- carries none: the cost of "a literal with a point is a decimal"
  falls on 15 literals.
- **The court**: 30 of 30 on haro and its checked build (stage 56).
- **Radar on it**: a fresh clone of stzradar (d39413d), `haro tools/guard.haro` 62 passed 0 failed, `haro tools/feed.haro check` problems 0.

## Named

- A decimal's coefficient is 64 bits: a quantity past nineteen significant digits is DECIMAL_OVERFLOW, not a wider number.
- `for` with a decimal step and a decimal as a list index read through the decimal's double; no case asks them yet.
- `haro check` judges no number rule: the rules are the compiler's and the VM's, and `haro check --facts` carries them through
  `compiled` and `refused` as before.
