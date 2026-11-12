# Haro v0.59 -- `null` leaves Haro: `""` the empty text, `none` absence, `IsEmpty` the test

HARO-NULL-01. TYPES.md T5 (D55): "Ring's NULL, which was the empty string, is gone with the global it lived in: `""` is a text of length 0
and nothing else." The order is the Principal's (2026-11-11, "Right after absence"); the test's name is his too, chosen on 2026-11-12 among
three: "IsEmpty(x)". The rest is the desk's reading (D71).

Fixtures first (60d2a95: 5 cases, 4 failing before the code; U05, a `.ring` file, holds). Code 862d426; Haro's code rewritten a45b9c2 (a tool commit).

| line | what | cases |
|---|---|---|
| N1 | `IsEmpty(x)` is true for the empty text and false for any other value or type -- the text "NULL" is a text, a list, a number or an object is no empty text; it answers a condition | U01, U02 |
| N2 | `null` is refused in a `.haro` file, naming `""` and `none`; `IsNull` is refused, naming `IsEmpty` | U03, U04 |
| N3 | a `.ring` file keeps Ring's `null` (the empty text) and `isnull`, true for it and for the text "NULL" | U05 |

## How it is built

- `main.zig`: the built-in `IsEmpty` (`isempty1`), Haro's own and a `.haro` file's only, as v0.52's `Near`; the image format is version 7.
- `compile.zig`: the statement walk refuses `null` and a call of `IsNull`; `IsEmpty` answers a boolean.

## Haro's code, and haroport

`study/v59/nullfree.py` rewrote Haro's own code (a tool commit): 302 `null` written `""`, the value each always was, and 384 `IsNull`
written `IsEmpty`, in 38 files. haroport's rule N does the same for a ported tree (H35, plant T56; H02 expects `IsEmpty` by the ruling).

## Measured

- The court: 5 of 5 on haro and its checked build; plants Z1-Z4 caught.
