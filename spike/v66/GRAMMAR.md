# Haro v0.66 -- Haro's numbers

HARO-NUMBERS-CORE-01, on the Principal's ruling of 2026-11-12 -- no process-wide setting for places, `Decimals(10.257)` is `[2, 5, 7]`,
`DecimalPart(10.257)` is `0.257`, Softanza's names, the best-designed languages as the model -- and his "Build it as proposed" on
`NUMBERS.md` (ad4d0a5). The desk's readings are D78.

**One departure, said so**: `NUMBERS.md` listed `Truncate(x)` beside `IntegerPart(x)`. Both answer the integer toward zero, and one
thing with two names is what D67 and D69 refuse, so `IntegerPart` is built and `Truncate` is not.

Fixtures first (5c79c5e: 13 cases, 11 failing before the code; U05 held -- `Floor` and `Ceil` already answered integers -- and U13, a
`.ring` file). Code 44dc55c.

| line | what | cases |
|---|---|---|
| L1 | a float is written as the shortest text that reads back the same (`print`, `String`, a list's join); a `.ring` file's `decimals(n)` never reaches `.haro` code | U01, U02 |
| L2 | `Text(x, iPlaces)`: exactly iPlaces after the point, the last rounded half to even | U03 |
| L3 | `Round(x)` the nearest integer, a tie to the even one; `Round(x, iPlaces)` the same kind; a float rounded from its exact value (`Round(2.675f, 2)` is 2.67, as it holds 2.67499...); `Floor`, `Ceil` an integer | U04, U05 |
| L4 | `IntegerPart` toward zero, `DecimalPart` the same kind and sign; `Decimals` and `Digits`, vectors of integers | U06, U07 |
| L5 | `Abs` the same kind, `Sign` -1, 0 or 1, `Clamp(x, lo, hi)` (a float mixes with no other number there either) | U08 |
| L6 | `FromHex(t)` beside `Hex(i)` | U09 |
| L7 | refused, naming what to write: `Decimals(n)` standing as a statement (a setting), `FAbs`, `Dec` | U10-U12 |
| L8 | a `.ring` file keeps its own names: `decimals(n)`, `fabs`, `dec` | U13 |

## How it is built

- `compile.zig`: the new built-ins are a `.haro` file's only (`haroOnlyBuiltin`); `Decimals(x)` of a `.haro` file stands ahead of the
  classic setter in the table, so a `.haro` file never reaches the setter. `FAbs` and `Dec` are refused where a built-in is chosen;
  `Decimals(...)` standing as a statement is refused where the statement is compiled, unless the program defines a function of that
  name.
- `main.zig`: `numBuiltin`, one helper out of the run loop for all eleven; `floatText`, the shortest text; `fmtPlaces`, the exact
  half-to-even rounding the printer always used, at the places asked for. The print op says whether `.haro` code prints (`say_haro`).
  The run loop's compile-time branch quota is raised to 4000: its inline calls reached Zig's default of 1000.
- `image.zig`: version 8.

## With it: haroport

`fabs` is `Abs`, `dec` is `FromHex`; a `decimals(n)` statement is listed for its writer, who moves the places to the values written
(H41, plants T66-T67).

## Changed by the ruling, said so

- v0.52's N27 and N28: a `.haro` float printed with the setting's two places (`-0.50`, `1.50`) is written `-0.5`, `1.5`.

## Measured

- The court: 13 of 13 on both builds; plants P1-P18.
- stzlib origin/main ef99cd947, 181 landed `.haro` files under `haro check --facts`: 5 functions refused, all `Decimals(n)` as a
  setting -- `Round` (core/common/stkNumberCommons), `ring_decimals` (core/common/stkRingFuncs), `RoundedTo`, `SRoundedTo` and
  `SFractPart` (core/number/stkNumber) -- holding 23 such statements; no `FAbs`, no `Dec`.
