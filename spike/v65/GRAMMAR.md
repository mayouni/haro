# Haro v0.65 -- in .ring code a decimal is Ring's number

HARO-RINGBOUNDARY-DECIMAL-OUT-01, from stzlib-haroport (2026-11-12), the outbound half of v0.63: stzPattern.haro's cycle positions,
decimals, reached the guard sound_mu3 (`.ring`) under `decimals(4)` and printed as 0.000000000000001 and 0.333333333333334 -- Ring's
`decimals(n)` formats a float, and a decimal stayed a decimal in `.ring` code. It held module 3 at 46 of 48.

The desk's reading (D77) was first StzLib's (a), a decimal converted to a float where it crosses into `.ring` code. StzLib then found
the decimals sound_mu3 reads are list items, two levels deep in a returned list, which converting a bare answer does not reach, and
walking every list a `.haro` function returns would cost each return its size. So the reading was amended before any code was written:
**in `.ring` code a decimal is Ring's number, wherever it came from** -- an answer, an argument, a list item, an attribute. It prints,
joins into text and `string()`s as Ring writes a number under `decimals(n)`, and `type()` answers NUMBER; Ring's arithmetic already read it
as a number. Nothing is converted at a boundary, so a decimal that passes through `.ring` code and back to `.haro` is still exact.

Fixtures first (c89d90a: 4 cases; db79e51: amended with the reading, E5-E7, 5 of 7 failing before the code). O06's expectation was
corrected after the court spoke (`?` ends a printed list with one more line), and O03's `String` line added before the plants, said so.

| line | what | cases |
|---|---|---|
| E1 | a `.haro` decimal printed by a `.ring` caller is formatted by `decimals(n)`, and `type()` is NUMBER | O01 |
| E2 | a `.haro` caller's decimal at a `.ring` function's parameter is Ring's number there | O02 |
| E3 | a `.haro` caller keeps its decimal | O03 |
| E4 | the round trip: a `.ring` fraction is a decimal in `.haro` (v0.63) and Ring's number again when it comes back | O04 |
| E5 | a decimal two levels deep in a returned list, joined into text by `.ring` code: StzLib's case | O05 |
| E6 | a list of decimals printed by `.ring` code | O06 |
| E7 | a decimal that passes through `.ring` code comes back to `.haro` exact | O07 |

## How it is built

- `main.zig`: `ringNum` -- a decimal, read by code at a `.ring` pc, is the float nearest it; used by `string()`, a list's items joined,
  and text joined with `+` (`preAdd`). `type()` answers NUMBER at a `.ring` pc. The print op says whether `.ring` code prints
  (`say_ring`), so a decimal printed there, alone or as an item of a list, is written as Ring writes a number.

## Measured

- The court: 7 of 7; plants G1-G7 caught (G7's first form left two parameters unused and did not build; rewritten, caught).
- stzlib origin/main 56d1cd4ad: no `.ring` or `.haro` file tests `type()` against "DECIMAL" (one "DECIMAL" is a COBOL type name in text).
