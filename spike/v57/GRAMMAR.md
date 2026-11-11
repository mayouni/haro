# Haro v0.57 -- one way to print: `print`, and `?` its shortcut

HARO-PRINT-01. The Principal, 2026-11-11, in this desk's chat: "I don't want Haro to enherit the Ring pathology of having serveral
laternative to the same fauture like 'see', 'print' and '?'. Although, one could accept a unique keyword (print for example) along with a
useful shortuct like '?'." His own: one keyword, `print`, and the shortcut `?`. The desk's reading (D69), on his "i let you decide":
`print` and `?` are the same statement -- the value written, then the end of the line, as `?` always wrote it; `see` and `put` are refused
in a `.haro` file, naming `print`; output that ends no line goes through the stream, `FWrite(stdout, tText)` (v0.50).

Fixtures first (69bbef6: 7 cases, 5 failing before the code; R02, `?` itself, and R07, a `.ring` file, hold). Code cddf919; haroport cdf968e; Haro's code rewritten 61bffdf (a tool commit).

| line | what | cases |
|---|---|---|
| P1 | `print v` writes v and ends the line; `?` is its shortcut and writes the same bytes (a list: its items, then an empty line) | R01-R03 |
| P2 | `see` and `put` are refused, naming `print` | R04, R05 |
| P3 | output that ends no line: `FWrite(stdout, ...)` | R06 |
| P4 | a `.ring` file reads `see`, `put`, `?` and its `print(...)` calls as Ring reads them | R07 |

## How it is built

- No grammar change: the grammar is shared with the classic Ring surface, and a `.ring` file calls a function `print` (stzlib does, at 48
  places or more). In a `.haro` file the lift's token pass (v0.56, `bracesText`) writes each keyword `print` as `?    ` in place -- five
  bytes for five, no column moves -- so the parser reads the `?` statement.
- `compile.zig`: `see` and `put` in a see statement are refused by the one-form walk, naming `print`.

## Haro's code, and haroport

`study/v57/printing.py` rewrote Haro's own code (a tool commit): `see E + nl` is `print E` (11 lines), a `see` that ends no line is
`FWrite(stdout, E)` (3 lines). v0.55's O17 names `print`, its O28 writes through the stream, and v0.39's L04 reads its column 18 where the
rewritten line holds the name, each by the ruling. haroport's rule O writes the same: a statement's expression is read to the line's end,
to the next statement word, or to a bracket around it (H34; H01, H28, H29, H32 by the ruling); plants T52-T55.
