# Haro v0.41 -- a .haro file is read by Haro's rules, a .ring file by Ring's (HARO-SURFACE-01)

The author's two rulings of 2026-11-06, given in the session after a variable named `aNd` was read as the keyword `and`:

> "I don't the aNd error to happen in Haro so fix it by design. don't feel constrained by Ring heritage since we cut wit it, and hence we are not
> obliged to opt forcase inceseniftvity if you find the inverse moure useful and more robust to Haro langyage"

> "the same thing applies to the use of : in :key = value turning it to a list and the special undocumented case (in ring) of using :str and
> turning str to lowercase!!! i saw some code embracing this but we should not be obliged to do so!!"

The desk's decision under them: **the extension of a file says how it is read.** Fixtures first (`fixtures.json`, `cases/`, `surface_court.py`:
dc5b731), then the grammar (`vm/vendor/tree-sitter-ring`), the lift, the loader, the compiler, the printer and the dump.

| line | in a `.haro` file | in a `.ring` file | cases |
|---|---|---|---|
| S1/S2 | a keyword is spelled in lowercase, exactly; `aNd`, `oK`, `If`, `NULL` are names | a keyword is Ring's, in any case (`oK = ...` is the keyword `ok`, as on Ring) | S01-S03 |
| S3 | a symbol keeps its spelling: `:Name` is `"Name"` | a symbol is lowered: `:Name` is `"name"` | S04, S05 |
| S4 | `:key = value` is refused by name; `[:key, value]` says it | `:key = value` is Ring's pair | S06-S08 |
| S5 | an eval reads its text by the rules of the program's root file | | S09, S10 |
| S6 | a program may load files of both kinds: each is read by its own rules | | S11 |
| S7 | `haro fmt` reads each file by its rules, and prints a name as written | | K01-K03 |

## How it is built

- **One grammar, one spelling.** `keyword()` in `grammar.js` is the lowercase word exactly (it was `ci()`, every case). The parser was regenerated
  with tree-sitter 0.25.10, the version that made the old one, after regenerating the OLD grammar reproduced the vendored parser byte for byte.
  `parser.c` went from 22.1 MB to 19.4 MB.
- **A `.ring` file is lowered before its one parse** (`lift.parse`): every word outside strings and comments that is a Ring keyword written in
  another case is lowered -- the same length, so every offset and column stays the file's -- and the lowered text is what is parsed. The words are
  found LEXICALLY: a first version took them from the leaves of a first parse and missed three `NOT (` in stzlib's stzListFunc.ring, where the
  lowercase-only grammar's error recovery had misjudged a string; the stzlib A/B found it as three extra native calls. That version also parsed
  every such file twice, 17 s against 7.7 s for a `dump` of one stzlib test with its loads; parsed once, 6.1 s against 5.7 s. A quote or a `/*`
  that is never closed is no string or comment to the grammar, and the scan reads what follows as code too (stzlib's
  datetime/48_custom_format_strings.ring opens a `/*` it never closes).
- **Every reader goes through it**: the loader (`haro run`, `check`, `census` ...), the prefix path, the load scan, an eval, `haro fmt` and its
  re-reads, `haro dump` and `dump --json` -- the two dumps print the file's own bytes by span, so a lossless export stays lossless.
- **`haro fmt` prints the file's own bytes.** The lowering reaches a `.ring` file's names spelled like keywords -- a method `Get`, a member `See`
  -- which the grammar reads as names; fmt's tree took its leaves from the lowered text and printed `o.get()`. Its leaves, and those of a re-read
  piece, now read the file's own bytes under the same spans. Found by plant P11 MISSING, pinned by K03, written after the code.
- **The compiler** asks of a node whether its file is a `.haro` one (an eval: the root's): `konstSymbol` keeps the spelling there, and the two places
  that build a pair from `:key = value` -- a list's element and an expression -- refuse it there.
- **Haro's block words** (`within`, `using`, a bare `done`) are lowercase in every file: they are Haro's, and no `.ring` file writes them.
- **Haro's own code** followed: 293 keywords lowered in 31 `.haro` files (293 `NULL`) and the forge's court templates, each file verified to read
  the same tree before and after; v37's G04 (`Catch err`) now spells `catch err`, said so in its generator.

## Measured

- stzlib origin/main f77486b5a, 7,126 `.ring` files (`runtime/v41/surface_scan.py`): keywords 79.6% lowercase, 16.2% Capital, 4.0% UPPER, 0.2% in
  no single case; 23,754 `:key = value` pairs in 1,689 files; 25,914 symbols with a capital. **All of it reads as it did**: see the A/B below.
- **Every file, one at a time** (`runtime/v41/all_trees.py`, `haro dump --json` on the VM before the rung and after it, every byte lowered): **7,125
  of 7,126 files read the same tree.** The one that does not, future/doc/stzappserver.ring, fails to parse on both: `def NotFound(cMessage = "Not
  Found")` is an ERROR, and inside that error the old grammar read the `Not` of the string as the keyword `not`; the scan leaves a string's words as
  written (S12), so the error runs three bytes further and the function ends 24 bytes later. Four nodes of 2,487 differ, all in that function.
- `haro census max/stzMax.ring` (765 files) before and after: the same statements, refusals, instructions, natives and names; `haro check` the same
  findings, but 4 messages that quote a symbol key lowered (`'class'` for `:Class`), the key's value on Ring.
- The 980 sites where Softanza names an object `oN`, `oK` or `oR` are read as keywords by Ring and Ring++ themselves, and by Haro in a `.ring` file;
  in a `.haro` file they are names.

## The protections, each switched off (`plants.py`)

15 plants over lift.zig, compile.zig, haro.zig and fmt.zig, each built and judged alone: **15 of 15 caught**, each by the fixture it exists for. Two
missed on the first run and were repaired, not removed: P11 (fmt printing the lowered text) had no case that showed it, and K03 is that case; P14
(the lift's keyword list one word short) planted a source that the harness restored before the court read it, so a check that reads the source
now runs with its plant in place.

## The desk's readings, recorded as its own

- One exact spelling: lowercase only, not "lowercase or UPPER" -- `NULL` was Haro's only habit otherwise, and it was mechanical to change.
- Names stay case-insensitive: `aNd` and `AND` in a `.haro` file are one name, which can never be written `and`. Making names case-sensitive would
  change how a `.haro` program reaches Softanza's functions (`StzRaise`, `stzraise`) and is not done here.
- An eval follows the root file's rules, not the file of the line that runs it.
- A refusal or a checker message that quotes a `.ring` file's text quotes the lowered text.

## Not covered, named

- A `.ring` file's keyword-shaped words inside a string that is code (`eval("If ...")`) are lowered when the eval runs, by the root's rules (S5):
  a `.haro` program evaluating Ring text written with capitals reads it by Haro's rules.
- Other extensions (the courts' sentence files, `.stzu`) are read by Ring's rules, as any non-`.haro` file is.
