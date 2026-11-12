# Haro v0.60 -- symbols: data that keeps its text, compared by its name

HARO-SYMBOL-01, from stzlib-haroport (2026-11-12): Softanza's named parameters compare an item with a symbol (`pvList[1] = :To`), 3,829
times in 330 files of base/. Two findings stopped its module 3: `kA = :And` was refused as a keyword in another case
(HARO-SYMBOL-KEYWORD-01); and `vL[1] = :To` answered false, with no error, when `vL[1]` was the text "to" -- which is what a `.ring`
caller's `:to` is, Ring lowering it (HARO-SYMBOL-TEXT-EQ-01). Principle 4 and v0.41 (S3): a symbol is data and keeps its text, and its
comparison ignores case. The readings are the desk's (D72), on the Principal's "i let you decide".

Fixtures first (6637442 and 0f6de3d: 6 cases, 5 failing before the code; Y06, a `.ring` file, holds). Code a963f89.

| line | what | cases |
|---|---|---|
| K1 | a symbol's word is no keyword: `:And`, `:To`, `:End` are symbols | Y01 |
| K2 | where one side of `=` or `!=` is a symbol written in the code, the other side is compared with the symbol's name by its text, case ignored; a value that is not a text is never the symbol, and no error | Y02-Y04 |
| K3 | a `.ring` caller's lowered `:to` reaches a `.haro` comparison and holds | Y05 |
| K4 | a `.ring` file reads its symbols as Ring does | Y06 |

## How it is built

- `compile.zig`: the statement walk stops at a symbol; a comparison with a symbol on either side (`symbolSide`) compiles to: the other
  side, `IsString` of it (not text: not equal), `Lower` of it, and a jump against the symbol's name lowered at compile time -- in a
  condition and as a value alike.

## Measured

- The court: 6 of 6 on haro and its checked build; plants S1-S5 caught (S4 points at Y04, the case whose text has capitals, after it
  missed Y02, whose text is lowercase).

## With it: haroport

stzlib-haroport's HARO-PORTTOOL-CALLNAME-01 (a parameter named like a built-in was lettered, and the built-in's call renamed with it) and
-NAMETEXT-01 (a global named in a text or as a symbol kept its old name while its uses were renamed): c64fecb, H36, H37, plants T57-T59.
