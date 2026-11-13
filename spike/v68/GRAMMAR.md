# Haro v0.68 -- in .ring code a boolean is the number 1 or 0

HARO-RINGBOUNDARY-BOOL-OUT-01, from stzlib-haroport (2026-11-12), the boolean mirror of v0.65: stzObject's `b` attributes hold `true`
and `false` since its port, and `stzObject_defects_narrated.ring` lists an object's attribute values and formats each with
stzListShow.ring's FormatValue, which dispatches on isNumber / isString / isList / isObject. A boolean matched none and raised
"Unsupported value type". It held module 5 (base/object) at 30 of 35 guards.

The desk's reading (D80) is StzLib's (a), on v0.65's reading of a decimal: **in `.ring` code a boolean is the number 1 or 0, wherever
it came from** -- an answer, an argument, a list item, an attribute. Nothing is converted at a boundary, so a boolean that passes
through `.ring` code and back to `.haro` is still a boolean, and `.haro` code prints `true` and `false`.

Fixtures first (b7fb1bf: 11 cases, 8 failing before the code; B05, B09 and B10 held). Code 903213a.

| line | what | cases |
|---|---|---|
| L1 | `.ring` code prints a boolean as 1 or 0: alone, with `see`, as a list's item, as an object's attribute | B01, B02 |
| L2 | `type()` is NUMBER and `isNumber` is 1 | B03 |
| L3 | `string()`, `number()`, `list2str` and text joined with `+` read it as 1 or 0 | B04 |
| L4 | it compares with 1 and 0 as before | B05 |
| L5 | `find()` and `sort()` in `.ring` code take it as its number | B06 |
| L6 | StzLib's case: a dispatch on isNumber / isString over values a `.haro` function gave | B07 |
| L7 | a `.haro` caller's boolean at a `.ring` function's parameter is the number there | B08 |
| L8 | `.haro` code keeps `true` and `false`, and a boolean that passes through `.ring` code comes back a boolean | B09, B10 |
| L9 | `Find` in a `.haro` file finds a boolean, and a boolean meets no number there | B11 |

L9 was found while probing and built in this rung, said so: find's equality had no case for two booleans, so
`Find([true, false], false)` answered 0 in a `.haro` file.

## How it is built

- `main.zig`, each place asking whether the code is a `.ring` file's (`strictAt`): the print op flags a boolean, a list or an object
  printed by `.ring` code (`say_ring`), and `sayValue` then writes a boolean as its number, an item and an attribute too; `type()`
  answers NUMBER; `isNumber` 1; `string()` "1" or "0"; `number()` reads it; `list2str` joins it; `find()` compares the needle and each
  item as numbers (`ringBool`); `sort()` orders it as its number (`SortBy`). `strictEq` gains the case of two booleans.

## Measured

- The court: 11 of 11 on both builds; 13 plants, K1-K13, each caught by its fixture (`plants.py`).
- Stages 47, 48, 57, 70 and 72 (names, booleans, the 1/0 boundary inward, the decimal outward, maps) hold on v0.68's builds.
- stzlib origin/main 2d3cb7cca, its 194 landed `.haro` files under `haro check --facts`, v0.67 against v0.68: 80 functions refused
  before, 80 after, none newly refused -- the rung adds no refusal. No `.ring` file there tests `type()` against "BOOLEAN" (the three
  lines that write "BOOLEAN" are two database column type names and one parameter's documented type, in an archived file).
