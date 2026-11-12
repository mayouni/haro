# Haro v0.63 -- a .ring number crossing into .haro is an exact decimal

HARO-RINGBOUNDARY-NUMBER-01, from stzlib-haroport (2026-11-12): the guard sound_mu3 (`.ring`) calls `oPattern.Off(0.25)` on stzPattern
(`.haro`), and `pxCycles <= 0` stopped with NUMBER_MIX (float <= integer). Ring has one number type, so every `.ring` caller's fraction
reached a `.haro` library as a float, and the library's integer literals refused it -- the shape of Softanza's whole library. It held
base/common, stzlib's module 3.

TYPES.md section 6 (D55): "A value crossing from .ring code into a .haro name is checked at that binding." The desk's reading (D75), the
first of the two StzLib named: a fraction crossing from `.ring` code into `.haro` -- a `.ring` caller's argument at a `.haro` function's
parameter, a `.ring` function's answer to a `.haro` caller -- is the exact decimal of its shortest text (0.25 is 0.25, 0.1 is 0.1). A whole
number is already an integer. Decimals and integers mix (v0.52), so the library's literals hold. A float stays a float where `.haro` code
asks for one (an `f` parameter, a `.haro` caller's `0.25f`), where it has no decimal (a NaN, an infinity, past 64 bits of digits), between
`.ring` functions, and as an item of a list.

Fixtures first (260389b: 7 cases, 3 failing before the code; fc6c261: M08 and M09, written after the code was edited and before it was
built or run, said so).

| line | what | cases |
|---|---|---|
| D1 | a `.ring` caller's fraction at a `.haro` parameter is an exact decimal, its shortest text | M01, M02 |
| D2 | a `.ring` caller's whole number is the integer it was | M03 |
| D3 | a `.ring` function's answer to a `.haro` caller: a fraction is an exact decimal, a whole number an integer | M04, M05 |
| D4 | a float `.haro` code asks for is not converted: a `.haro` caller's `0.25f`, an `f` parameter | M06, M08 |
| D5 | a `.ring` file reads its own numbers as it did, and a `.ring` caller of a `.ring` function too | M07, M09 |

## How it is built

- `compile.zig`: every parameter of a `.haro` function is checked at the entry (`lchk` with c = 1), an unchecked letter's too -- its check
  only converts; an `f` parameter is left. A `return` in a `.ring` function says so (`ret` with b = 1).
- `main.zig`: `ringDec` -- the shortest text of the double, read as a decimal. At a parameter's entry check, a float from a caller whose
  code is `.ring` becomes it; at a `.ring` function's return, a float answered to a caller whose code is `.haro` becomes it.
