# Haro v0.67 -- maps

HARO-MAP-01. TYPES.md T6 (D55): a map is `m`, "a key to a value, keys unique; what Softanza's pair lists were used for when the keys
vary"; section 6: a list of pairs entering an `m` name is converted, refused if a key repeats. Asked how a map is written and what a
read of a missing key does, the Principal chose **"A literal with key: value"** and **"A maybe, resolved with else"** (2026-11-12):

    mAges = ["ada": 36, "bob": 41]
    mEmpty = [:]
    mAges["cyd"] = 29
    iAge = mAges["eve"] else 0

With it the third rung of T6 (letters v0.61, records v0.64, maps v0.67) is built. The desk's readings are D79. Fixtures first (5938689:
14 cases, 13 failing before the code; G13, a `.ring` file, holds). G15 and G16 were added after the code and before the plants, said so:
no case wrote a key in another case or an integer key, and none gave a map literal to a `v` name. Code 21b9d2f.

| line | what | cases |
|---|---|---|
| M1 | the literal and `[:]`; a read resolved with `else`; a write adds the key (in its exact case, or an integer) or replaces its value; `Len` | G01, G15 |
| M2 | a read left unresolved is refused when compiling | G02 |
| M3 | a key is a text in its exact case or an integer; any other key KEY_TYPE; a literal's repeated key DUPLICATE_KEY | G03-G05 |
| M4 | `Keys`, `Values`, `HasKey`, and `Del(mX, k)` (the list's `Del`, by key), in insertion order | G06 |
| M5 | an `m` name holds a map, a `v` name no map -- a literal refused when compiling, any other value where it is given | G07, G08, G16 |
| M6 | a map is a value: assigning it copies it | G09 |
| M7 | printed as written: `["ada": 36, "bob": 41]`, `[:]` | G10 |
| M8 | `for vP in mX` gives each [key, value] pair | G11 |
| M9 | a `.ring` caller's pair list at a `.haro` `m` parameter is a map | G12 |
| M10 | a `.ring` file reads its pair lists as it did | G13 |
| M11 | v0.41's refusal of `:key = value` names the map | G14 |

## How it is built

- `lift.zig`: inside a `[`, a `:` after a key (a text, a number, a name, `)` or `]`) is given to the parser as `,`, and the `:` of `[:]`
  as a blank -- byte for byte; the place of each map's `[` is kept in the file's marks.
- `compile.zig`: a list literal at a map's place is built as the flat list, then made a map (`mapof1`); a read of an `m` name by key is a
  maybe (`maybeName`), so `E else D` resolves it and an unresolved one is refused in its own words; `m` is a checked letter; `Keys`,
  `Values`, `HasKey` are a `.haro` file's own built-ins.
- `main.zig`: a map is a vector of [key, value] pairs with a flag (`Vec.map`), so a native and `.ring` code see the pair list Softanza
  has always used. In `.haro` code, `vget`, `dget`, `hget`, `vset`, `hset` and `vdel` read, write and delete it by key (`mapRead` answers
  none for a key not held); a copy keeps the flag; `m` holds a map, `v` no map; a `.ring` caller's pairs at an `m` parameter are made a
  map, a repeated key refused; `.haro` code prints a map as its literal.

## Changed by the ruling, said so

- v0.41's S06 and S13 and v0.64's R13: the refusal of `:key = value` now names `["key": value]` for a map.
- v0.47's Y09: `mIndex`, written to show a letter not yet built, is `kIndex` -- `m` is checked since v0.67.

## Measured

- The court: 16 of 16 on both builds; 21 plants, H1-H21, each caught by its fixture (`plants.py`).
- stzlib origin/main 0e32c4a34, its 190 landed `.haro` files under `haro check --facts`, v0.66 against v0.67: 71 functions refused
  before, 72 after. The one is `stkMemory.IsValidBufferId`, which calls `HasKey(@vBuffers[tBufferId])` with one argument -- its own
  comment marks it as the base layer's `HasKey`, which core does not load; with `HasKey(mX, k)` a built-in, the call is refused for its
  count. No `m`-lettered name and no map literal stood in the tree.
- A map is found by a walk over its pairs, so a read is linear in its size (`study/v67/mapcost.py`, 200,000 reads of the last
  integer key, the minimum of 5 runs less the same loop without the read): 13 ns at 1 pair, 51 ns at 10, 290 ns at 100, 2,600 ns at
  1,000 -- about 2.5 ns per pair held. A map of thousands of keys read in a loop pays for it; a hashed index is the change that
  answers it, and waits for a customer.
