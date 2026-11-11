# Haro v0.54 -- the p mark and a vector's element letter

HARO-LETTER-SOFTANZA-01, from stzlib-haroport (2026-11-11 06:00), carrying the Principal's ruling of HAROPORT-SPELLINGS-02 (2026-11-11 05:59,
recorded at stzlib 18608e029, `base/doc/design/HAROPORT_SPELLINGS.md` section 0). Of its six parts, three reach Haro's letter rule (TYPES.md
T2, "a lowercase type letter followed by a capital"): (a) "Keep p as a mark" -- a parameter is `p` + its type letter + a capital,
`ptSubStr`, as `$` and `@` stand before a letter; (c) "v + second letter" -- a vector keeps its element's letter after `v`, `viPos`;
(d) "Keep constants in caps" -- `$iMAX_NUMBER_SIZE`, `@tNL`. The order, these letters before absence, is the Principal's in this desk's
chat (2026-11-11, "Letters first").

Fixtures first (3187354: 13 cases, 10 failing before the code; L10, L11, L13 hold and guard). Code a5c83c9.

| line | what | cases |
|---|---|---|
| E1 | a parameter `p` + letter + capital is accepted and checked by the letter after `p`, where it is given; it may be given a new value in its body; Softanza's `pc` is refused with `pt` as its todo | L01, L02, L03, L12 |
| E2 | a `p` name that is no parameter of its function is refused, naming the function | L04 |
| E3 | `v` + element letter + capital: a vector each of whose items holds the element's type, checked where it is given -- a vector literal included; a parameter `p` + `v` + element letter too; the first item that does not is named with its place | L05, L06, L07, L08, L09 |
| E4 | a constant is its letter and capitals and underscores, held already (a letter then a capital) | L11 |
| E5 | a plain `v` name holds any vector; a `.ring` file reads its names as it did | L10, L13 |

## The desk's readings (D66)

- **The `p` mark names a parameter.** Read with `$` and `@`: a mark before the letter, the letter checked as any. A `p` name that is no
  parameter of its function is refused, because the mark would then say something false.
- **The element letter is checked**, as every checked letter is where a value is given: the value is a vector, and each item holds the
  element's type. A vector literal settles `v` when compiling, never its items, so a name with an element letter keeps its check. The
  check walks the items once per binding.

## How it is built

- `compile.zig`: `letterParts` reads a name as an optional `p` mark, its letter, and after `v` an element letter; `letterOf` and the faults
  read through it; `isParam` answers whether a name is a parameter of the function being compiled; `emitLetterCheck` carries the element
  letter in the check's `c`.
- `main.zig`: `lchk` with `c` set checks each item by `letterHolds`, naming the item's place and type; `letterPlural` words the vector.

## haroport's third round, beside the rung (HARO-PORTTOOL-ROUND3-01)

`port/haroport.py` applies SPELLINGS-02's renames: a parameter keeps its `p` mark (`pc` -> `pt`, `pa` + element -> `pv` + element);
Softanza's list letters are `v` and the element's (`an`, `ac`, `ao`, `aa` -> `vi`, `vt`, `vo`, `vv`); an ALL_CAPS name and an
`@Capitalised` attribute the tree assigns take their letter by what they hold -- 1 or 0 alone and never counted is a boolean; a `b` name
given 1 or 0 and a condition on a literal 1 or 0 are on `true` or `false`. Fixtures first (06cebf0: H23-H27), the tool 23e8617, 27 of 27,
plants T1-T32 caught.

## Named

- A `p` parameter's value given when the function is called is checked at the call's entry, as every parameter's; a `p` parameter given a
  new value in its body is checked there too.
- The element check runs per binding: a vector of n items costs n checks where it is given.
