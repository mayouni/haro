# Haro v0.69 -- `haro check` names what the run refuses

HARO-CHECKRUN-01, from stzlib-security through Central (2026-11-12): `haro check` passed three forms the run refused in one file --
`func F()` with no parameters, `but`, and `[:key = value]` -- so check read "0 error" on a library that did not load.

The desk's reading (D82), under the delegation: **a form the run refuses is an error of `haro check`, at the same line and in the same
words.** Not three forms: every form. Check asked the compiler nothing, so thirteen forms tried were thirteen refused by the run and
thirteen passed by check. The rule is `haro/refused-form`.

Fixtures first (3401b67: 22 cases, 20 failing before the code; N02 and T03 held). Code eb4b47f. W01 was written after the code, and
the generator says so.

| line | what | cases |
|---|---|---|
| L1 | a form the run refuses is an error of check, at the run's line and in the run's words | S01-S13 |
| L2 | check names every refused form of a file; the run names the first it reaches | M01 |
| L3 | the unit: a refused form in a loaded file is named under that file | U01 |
| L4 | a program with no refused form has no such error | N01 |
| L5 | a `.ring` file keeps its own reading: the same forms are no error there | N02 |
| L6 | `check --facts` carries each one, in its function or at the file's top | G01 |
| L7 | in a `.haro` file a definition closed by `end` holds nothing after it: the statements after it are the program's | T01, T02 |
| L8 | a `.ring` definition holds what follows it, as before | T03 |
| L9 | the facts give a closed function its own lines | T04 |
| L10 | a trap the compiler rolled back is no refusal | W01 |

The thirteen forms of L1: a definition or a method with empty parentheses, `but`, `:key = value`, `see`, `null`, a block closed with
`ok` or `next`, `==`, a name in another spelling, a definition in braces, the letter `c`, `IsNull`.

L7 to L9 were found while probing and built in this rung, said so. Since v0.56 a `.haro` definition ends at its `end` and a program's
statements may follow it; check still read those statements as the definition's own. A program written definitions first was called
a library ("nothing in this unit runs"), so none of its calls was looked at, and the facts gave the function the lines after it.

## The court

`checkrun_court.py` runs each case, checks it, and reads **the law off the run's own output**: where the run prints
`Haro refused this statement (WORDS, line N of FILE)`, check must hold a `haro/refused-form` error at FILE, line N, whose message is
WORDS. The fixture pins the same line and words, typed in the generator before the code.

## How it is built

- `compile.zig`: `refusalTrap`, which writes the trap a refused statement compiles to, records what it says -- its reason, the text it
  quotes, its line, the source it sits in, and the constant that holds its message (`Trapped`). `factsData` keeps the records whose
  trap stands in the final code: a `loadk` of that constant followed by a `trap`.
- `haro.zig`: `check` asks the compiler once (a lenient compile; nothing runs) and adds each record to the report as an error, in its
  own file after that file's other findings, in line order, one a statement. The column is the quoted text's on its line, in the
  file's own columns. A record in text no file of the unit holds is named under the unit's first file.
- `ts.zig`, `closedByEnd`: a definition whose last child is `end`, or the closing brace the lift writes in place of a `.haro`
  definition's `end` -- the tree the checker reads. `universe.zig`: such a definition does not make the statements after it its own.
  `facts.zig`: such a function ends there.
- `check` prints `refused-form: NOT checked` with its reason when the compiler stops before the unit's end. Its exit code is what it
  was: a gate reads the count line.

## Measured

- The court: 23 of 23 on both builds. Twelve plants, K1-K12, each caught by its fixture (`plants.py`). T03 has no plant: a `.ring`
  definition holds what follows it by the grammar, and with every definition read as closed the court still passed.
- **A trap rolled back.** Counting on stzlib first showed 63 errors in one function of `graph/stzDiagram.ring` that the run does not
  refuse: its locals pass the register window, the compiler compiles it a second time with shared registers, and the first attempt's
  traps were thrown away with its code while their records stayed. With the standing-trap test the base library reads 12, the number
  the compiler's own census gives (141,015 statements, 12 refused).
- **stzlib origin/main 8221cdcfd, its 195 landed `.haro` files, each checked alone, v0.68 against v0.69**: check's errors go from 810
  to 1,120, every one of the 310 a refused form, in 31 files. The base library holds 12 (a file that loads it reads 49 before and 61
  after): 7 `StzChar` where the class is declared `stzChar` (`data/stzCharData.haro`), 1 `StzListOfChars` and 4 `Dec` on hex text
  (`data/stzUnicodeData.haro`). The others: `core/test` (stkNumberTest 39, stkPointerTest 17, stkListTest 8, five more files), the three
  `-copy` files of `core/system` (50, 24, 7), four haroport probes, three single files, and the engine's loaders checked alone
  (`$tEngineDir` never assigned -- the run says the same of them alone). No run changes.
- **Haro's own guard held 24 such files.** The five-rules court's cases (v0.39) were written before a file's extension said how it
  is read, and held about 75 forms a `.haro` file refuses today; stage 44 read 0 of 24 on v0.69. They are the classic surface, so
  they are `.ring` files now, and read as they did: 24 of 24 on v0.68 and on v0.69.
- Stages 44, 45, 50 and 55 (the five rules, the declared doors, the findings, the facts) hold on v0.69's builds. The 74-stage guard
  on builds made from the commit: 0 failures, 2,227 s, stage 6 at 141.0 ms cold.
- **What it costs.** Check now pays a compile. On stzlib's base (724 files) `haro check` takes 77 to 82 s where it took 36 to 44 s
  (two runs each, alternated); the census times the same compile at 27 s. The pattern it costs is the check of a large unit. A small
  file is unchanged: the court's 23 cases, run and checked on both builds, take 2.4 s.
