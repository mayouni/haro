# Haro v0.58 -- absence: `none`, `maybe`, resolved where it lands

HARO-ABSENCE-01, TYPES.md T5 (ruled in D55, 2026-11-07): "`none` belongs to no type. A function that may find nothing returns `maybe T`,
and its caller resolves it where it lands ... A `maybe` never travels in a local ... Only a return and an attribute may be declared
`maybe`." The spelling is the Principal's, in this desk's chat on 2026-11-11: `maybe` a trailing word -- `func Find(kId) maybe`,
`oParent = none maybe` -- and the resolution `x = E else D`. The rest is the desk's reading (D70), on his "i let you decide".

Fixtures first (b681f73: 16 cases, 13 failing before the code; M11, M12 and M16 hold and guard). Code 64c0f87.

| line | what | cases |
|---|---|---|
| A1 | a maybe function or method, resolved where it lands: `x = E else D`, `return E else D`, `print E else D`; D is taken when E is none, and may raise; a maybe function that ends without a return gives none; a maybe function may return another maybe as it is | M01-M03, M13-M15 |
| A2 | `none` stands only where a maybe is declared: returned by a maybe function, given to a maybe attribute | M06, M07 |
| A3 | a maybe anywhere else -- given to a local, passed as an argument -- is refused, naming it | M04, M05 |
| A4 | an attribute declared `maybe` starts as none and is read only where it is resolved | M08, M09 |
| A5 | `else` after a value that is never none is refused; an `else` that follows an if opened on its line, or begins its line, is the if's; `""` is a text of length 0 | M10-M12 |
| A6 | a `.ring` file: `none` and `maybe` are names | M16 |

## How it is built

- **No grammar change.** The lift's token pass (v0.56, `bracesText`) reads a `.haro` file's `maybe` at the end of a line -- a header or an
  attribute's declaration -- and blanks it, and reads an `else` that resolves a maybe and gives it to the parser as `or`, four bytes for
  four; it keeps both places (`lift.marks`), and the compiler reads them back.
- `main.zig`: `none` is a nil value with a mark (`Value.none`), so a slot nothing ever assigned still raises R24 when read and a maybe
  attribute holding none does not; two instructions, `ldnone` and `jnone`; the image format is version 6.
- `compile.zig`: a function's `maybe` flag and the maybe attributes are read from the marks; the statement walk refuses `none` and an
  unresolved maybe where T5 does not allow them (`absenceForm`); `E else D` compiles to E, a jump when it holds none, and D.

## Measured

- The court: 16 of 16 on haro and its checked build (M06 changed after the code, said so: its first form called g from f and named one caller); plants A1-A12 caught.

## With it: HARO-CHAIN-COMMENT-01

stzlib-haroport found the last structural refusal after rule O: a comment line before a call whose bracket spans lines, inside a block, made the grammar cut the chain at its dot, and the trailing-period refusal (v0.55) stood before the re-read that joins it. A dot is now a trailing period only when it ends its line (v0.56's E23, plant C1); stzTreeCanvas compiles whole.

## With it: HARO-RINGBOUNDARY-BOOL-02

stzlib-haroport's move stopped on its first module: a `.ring` caller passes 1 or 0 to a `.haro` function's `b` parameter, and the parameter's check refused it. TYPES.md section 6 says the crossing converts; v0.53 built it for a call's answer only. The parameter's check at its function's entry now converts an integer 0 or 1 to false or true when the caller's code is a `.ring` file, and a `.haro` caller's 1 stays refused (M17, M18, plants B1-B3).

## Stage 6

The first build of the absence walk asked every node for its parent, which tree-sitter finds by walking down from the root, and looked each call up in every function: stage 6 read about 30 ms over v0.57 (alternating A/B, `study/v58/stage6_ab.py`, minima of 15 runs). Carried down the walk and looked up by name, the minima read 156.4 against 159.0 ms, on a machine then loaded by other desks.
