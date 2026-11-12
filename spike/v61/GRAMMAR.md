# Haro v0.61 -- structure, its letters: `a` retires, `e` is checked

HARO-STRUCTURE-01, on the Principal's "Start structure" (2026-11-12). TYPES.md T6 names the structured values and their letters: a vector
`v`, a map `m`, a record `r`, an object `o`, an error `e`. T2 kept Softanza's list letter `a` "until structure". The desk's readings are
D73: T6 is built in three rungs -- its letters (this one), records (v0.62), maps (v0.63) -- because records and maps are new kinds of value
and the letters are not.

Fixtures first (a77f467: 6 cases, 3 failing before the code; Q03, Q04, Q06 hold).

| line | what | cases |
|---|---|---|
| S1 | `a` is no type's letter: a name lettered `a` is refused, naming `v` (a vector) and `x` (any value); a parameter keeps its p mark in the todo (`pvItems or pxItems`) | Q01-Q03 |
| S2 | `e` is checked: an error -- the value a catch binds -- and nothing else | Q04, Q05 |
| S3 | a `.ring` file reads its names as it did | Q06 |

## How it is built

- `compile.zig`: `letterFault` refuses `a` before the letter table, naming both names it can become; `e` joins the checked letters.
- `main.zig`: `e` holds a text that carries an error's record (`err != 0`) -- what `catch eErr` binds -- checked where a value is given.

## Haro's own code

`study/v61/aretire.py` (a tool commit, listed in `spike/v20/tool_commits.txt`): each of Haro's 451 `a` names takes `v` when every value the
tree gives it is a list literal (118) and `x` otherwise (333); one decision per name for the whole tree, a global named inside a text
following it (67), a local's collision checked in its own function, three resolved by reading the function (`OVERRIDE`). The keyword in
another case (`aNd`, v0.41's and v0.42's cases) is a case of its own and keeps its spelling. Five rungs' generators follow their cases.
The same tool takes another tree: `python study/v61/aretire.py --root DIR [--plan]`.

## With it: haroport

Rule A: a name Softanza lettered `a` (`aList`, `$aRows`, `paItems`) is `v` when the tree gives it only list literals and `x` otherwise, a
parameter keeping its p mark; refused and listed when the new name is in the tree or is another rename's new name (`vResult -> xResult`
beside `aResult`). Rule L letters a list `v`. H38 and H39 before the code; H04, H19, H21, H23 and H25 changed by the ruling, said so.
