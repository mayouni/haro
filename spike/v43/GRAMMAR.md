# Haro v0.43 -- a real boolean, and no coercion (D55 T1, T3)

The author's words of 2026-11-07, given in the session (all quoted whole in `TYPES.md` and `CHARTER.md` D55):

> "Ok but I noticed Haro holds no bolean type which was one of my strong critics to ring! Think of this widely and redeesign a good correct
> typesystem for Haro that is relevant to it's nature and core mission as a language of languages, and a governed languge of the agentic age"

> on TYPES.md's eight decisions: "Yes as recommended, but think of an other letter for list ..."

This rung builds T1 (no value changes type unasked) and T3 (`boolean` is its own type, and only a boolean decides), in a `.haro` file. A `.ring`
file reads as Ring reads (D54). Fixtures first (`fixtures.json`, `cases/`, `gen_fixtures.py`: 503de5c, 22 cases, 1 holding before the code --
B21, the `.ring` case that must not move), then the VM and the compiler.

| line | in a `.haro` file | cases |
|---|---|---|
| B1 | `true` and `false` are the booleans: printed `true` and `false`, `type()` BOOLEAN | B01 |
| B2 | a comparison and `and`, `or`, `not` answer a boolean | B02, B17 |
| B3 | a condition, and an operand of `and`, `or`, `not`, takes a boolean: a literal of another type is refused when compiling, any other value raises BOOLEAN_EXPECTED naming its type and what may have been meant | B03-B07, B23 |
| B4 | the natives that answer yes or no (`isnull`, `isstring`, ..., `fexists`, `direxists`) answer a boolean | B08 |
| B5 | a boolean is no number: in arithmetic it raises NO_COERCION; `string()` of it is `true` or `false` | B09, B10 |
| B6 | no coercion: text with a number under `+ - * / %`, and a numeric text used as a number, raise NO_COERCION; `=`, `!=` and the orderings between two types raise TYPE_MISMATCH; an integer and a number with a point are one kind of number until v0.45 | B11-B17, B20, B24 |
| B7 | an integer stays an integer to 64 bits, its literals included, and raises INTEGER_OVERFLOW past them | B18, B19 |
| B8 | a `.ring` file reads as Ring reads; a boolean reaching `.ring` code is 1 or 0 there; a `.ring` function's 1 is an integer to a `.haro` condition | B21, B22 |

The errors' words:

    Error (BOOLEAN_EXPECTED) : a condition takes a boolean, and this is an integer -- say what is meant: x != 0
    Error (NO_COERCION) : text + integer -- a value changes type only when asked: string(x) or number(x)
    Error (NO_COERCION) : boolean + integer -- a value changes type only when asked: a comparison, or string(b)
    Error (TYPE_MISMATCH) : integer = text -- = compares two values of one type
    Error (INTEGER_OVERFLOW) : integer + integer leaves 64 bits
    Haro refused this statement (a condition takes a boolean -- this literal is an integer; written `1`, line 4 of B03.haro) ...

A caught one answers its name from `Code()`: `NO_COERCION`.

## How it is built

- **A ninth tag, `boolean`** (`vm/src/main.zig`, `Tag`), its payload 1 or 0 so that every path of Ring's that reads `p.i` reads Ring's
  value. Only Haro's code makes one; Ring's truth (`truthy`) reads it as its payload, Ring's equality and ordering read it as an integer
  (`unb`), and Ring's `+` and arithmetic compute it as 1 or 0 (`preAdd`, `preArith`). It prints `true` or `false` wherever it is printed.
- **Which code is Haro's** is decided twice, each where it costs nothing. A condition the program wrote carries a flag from the compiler
  (`c = 1` on `jfalsy`, `jtruthy`, `truth`, `lnot`), set when the node stands in a `.haro` file (`haroNode`): Ring's truth tests pay one
  compare of a field they already load. Every other check asks the file of the instruction (`strictAt`: `files[pc]`, the name ending
  `.haro`), and only on a path that is slow already: a `+` that is not number with number, an `=` between two tags, an ordering between two
  kinds, an integer past Ring's exact range.
- **Where booleans are made**: the literals (`truth dst dst c = 2`, a boolean from Ring's truth with no check), a comparison as a value, the
  shortcut of `and` and `or`, `not`, and the yes-or-no natives, all in the compiler; `cmpv` (a comparison whose operand may be an object) in
  the VM, judged as a jump is.
- **Integers**: a `.haro` literal past 32 bits is an integer constant (`konstInt`), not a double; `+ - *` past 2^53 go to `intStrict`,
  exact to 64 bits by the overflow builtins, INTEGER_OVERFLOW past them. Ring's code still turns to a double past 2^53.
- **A literal condition** (`while 1`, `if "x"`, `if [1]`) is refused when compiling through v0.42's statement refusal (`spellSet`).
- **The `+ constant` path** (`addi`) reported an uncaught error as `Error: ...` with no line, where every other path prints Ring's line
  report. Haro's code now reports as every path does; Ring's keeps the older form, unchanged (HF-150).

## Measured

- **Before the rung** (`study/v43/`): 2,931 conditions in Haro's 35 code files, 2,429 already comparisons or logic; a census build of the VM
  over the 47-stage guard found 131 lines of coercion in Haro's code, every one `+` between a text and a number, and no condition of another
  type, no comparison between two types, no arithmetic on a text.
- **The migration** (`study/v43/migrate.py`, by rule, on the census's lines only): 117 lines -- `"" + x` to `string(x)`, `0 + x` to
  `number(x)`, a number in a text chain to `string(x)` -- one by hand (v38's B03, a variable named `using` holding 2), and ten `while 1` to
  `while true`. 41 of the lines are earlier rungs' case programs (v36's F cases, v38's B, U and W cases): their generators carry the same change,
  regenerating gives the same bytes, and no expected output moved.
- **The second migration** (`study/v43/migrate_bool.py`), found by a run of the guard with a locator built into a scratch VM (every Haro
  error written with its file and line, caught or not -- removed before the commit): a b-name assigned 1 or 0, a b-name compared with 1 or
  0, the predicates (every function a candidate, dropped while a return is not boolean-shaped: a greatest fixed point, so `PatNullable`,
  which calls itself, stays one), a literal 1 or 0 passed to a b-parameter, a success tuple `[1, value]` / `[0, 0]` in a function whose
  every returned list starts with one (so `PatItem`'s `[node, pos]` is left alone), the forge's templates. About 560 lines in all. By hand:
  `ExTruthy` and `ExBool`, the refinement grammar's seat table, `CtSeatPasses`, `n_lib`'s answered slot, one boolean used as an index
  (`aP[bRefs + 1]`), and `pattern.haro`'s `bInput`, which held 0, 1 or 2 and is `nInput` now.
- **One wrong answer with no error, which is the class to fear**: W's `ExTruthy` read a value as true when it was a nonzero number, a text or
  a list; `ExCompareValue` now answers a boolean, `isnumber(true)` is false, and a norm that holds read as violated. Stage 9 caught it as a
  wrong verdict, not as an error.
- **Four earlier fixtures print `true` where they printed `1`** (v37 G06 and G07, v41 S04, v42 N01), by the author's ruling; each generator
  says so.
- **Stage 6, the court compiled from scratch**: 156 ms on the first clean run, over its 150 ms ceiling, where v0.42 read 144 ms. The compiler
  asked which file a node stands in for every call before asking whether the call was a yes-or-no native at all; the cheap question first,
  141 and 143 ms on two runs, on a machine the heartbeat called fit.

- **Stage 24, a history measure**, read 94.9% against its 95% floor: a refinement drafted at one revision must land after the next human
  edit, and every lost target stood in the pairs ending at this rung's migration commit, which a tool made. The author: "Exclude tool
  commits". `v20/tool_commits.txt` lists such a commit; its pairs are counted apart and both figures print every run (99.8% on human edits,
  90 pairs; 94.9% with the tool's).

## The protections, each switched off (`plants.py`)

**26 of 26 caught**, each a text substitution in `vm/src/main.zig` or `compile.zig`, built into its own folder and judged by the court alone;
21 on haro 3752c05, and P10, P15, P16, P17 and P28 again after they were rewritten (the first four left a name unused, which Zig refuses, and
did not build; P28 missed). The conditions and their flag (P1-P4, P11, P13, P14), where booleans are made (P5-P7, P9, P12), no coercion
(P15-P18, P28), integers (P20, P21), which file is Haro's (P22), Ring's reading of a boolean (P23), printing and `type()` and `string()`
(P24-P26), the line of the `+ constant` path's error (P27), the literal condition (P10).

Removed after planting, named:
- **P8**, the boolean constant of a `.haro` file's `true` and `false` in `constOf`: its one caller is the resident VM's gained attribute, which
  no case runs. Asking why it missed found that its first version returned no constant there -- which would have refused `bReady = true`
  in a replaced `.haro` class as code that runs. It is a boolean constant now (`konstBool`).
- **P19**, a boolean against an integer immediate (`jeqi`, `jnei`, `jgti`): the compiler never emits those three; only the VM's built-in
  bench programs do. The check guarded nothing a `.haro` file reaches, and is removed from the VM.

B24 was rewritten after the plants: a call's answer is compared by a jump, so its first form never reached `cmpv`; a global's value may be
an object, and its comparison does (read off `haro dis`).

## The desk's readings, recorded as its own

- The error codes are names in capitals, as TYPES.md spells them, where Ring's are R-numbers.
- The type names in a message: boolean, integer, number (a value with a point until v0.45 names it decimal or float), text, vector, function,
  object, none, handle.
- Ring's F-98 exception (a number + nl is text) is a coercion and is not kept in a `.haro` file: `string(n) + nl`.
- A boolean prints its word wherever it is printed, `.ring` code included; in `.ring` arithmetic and truth it is 1 or 0.
- A `.ring` function's 1 or 0 entering a `.haro` condition is refused, not converted: the conversion at a `b` name is v0.44's (TYPES.md
  section 6).

## Not covered, named

- An eval in a `.haro` program is half judged: its conditions are flagged (the compiler reads an eval as its root's file), but the VM's
  other checks ask the file of the instruction, and an eval's instructions have none, so its coercions read as Ring's.
- A boolean as an index (`v[true]`) reads as 1 in either file.
- **No native asks whether a value is a boolean**: `isnumber`, `isstring` and their kin exist, `isboolean` does not, and Haro's own code asks
  `type(v) = "BOOLEAN"` (`ExTruthy`). Owed with v0.44, where the letters are checked.
- `!`, `&&` and `||` are compiled as `not`, `and` and `or` are; no case names them.
