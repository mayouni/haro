# Haro v0.77 -- three findings of the desks

Three findings other desks routed to this one on 2026-11-15, each read first on the installed v0.74 as its desk reported it, and
closed together (D94).

| finding | from | what was wrong | now |
|---|---|---|---|
| HARO-SIGLINE-01 | stzlib-testoor | a statement on a definition's header line, and a header over two lines, were read as something else and said nothing | refused when the program is compiled, by name |
| HARO-IMAGE-EVAL-LENIENT-01 | stzlib-intelligence | a program served from its kept image let `Eval` take what a fresh compile of the same program refuses | one reading, kept image or fresh compile |
| HARO-GRAPH-LATECALL-01 | stzlib-testoor | `haro graph` printed no line for a call by a name built when the program runs | `CALL\|<caller>\|*\|late\|<n>` |

Fixtures first (6b90c8c: 10 cases, 3 of 10 before the code -- the three that say what stays). The code 966e123; the plants and
stage 82, ee5b871. Six cases were added after the court spoke: three for a name's bytes (f019780, fixed ee8416a), two for the older refusal of
parameters without parentheses (41978e1, 0867d4c, fixed 83d2d99), each before the fix it asked for, and one a plant asked for
(d50ae85). See "A name is read
to its end" and "The older refusal stays" below.

| line | what | cases |
|---|---|---|
| L1 | a definition's body starts on the line after its header: a statement after the header on its line is refused when the program is compiled, for a function and for a method, whatever bytes its name holds, and after a parameter list whatever follows | F01, F02, F03, F12, F13, F15, F16 |
| L2 | a definition's header is written on one line: a parameter list that runs on to the next line is refused when compiling | F04 |
| L3 | what a header holds stays: its parameters, `maybe`, a comment; a class and its parent; a function with no parameter; a name that holds `@` or starts with it; parameters written without parentheses keep the refusal that names them | F05, F11, F14 |
| L4 | a program run from its kept image is the program a fresh compile runs: what `Eval` refuses in one it refuses in the other, and what it takes in one it takes in the other | F06, F07, F08 |
| L5 | `haro graph` names a call by a name built when the program runs; a unit that holds none prints what it printed | F09, F10 |

## A definition's header (HARO-SIGLINE-01)

    func PageUtc(nMs) print "hit"        # refused: a definition's body starts on the line after its header
    func Label(tName,                    # refused: a definition's header is written on one line
        nNet)

- **What it was.** In a `.haro` file each definition reaches the parser in braces, and the brace that opens one went at the end of
  the header's line. With a statement on that line the brace went after the statement: on v0.74 a program that writes
  `func PageUtc(nMs) print "hit"` prints nothing at all and ends well. With a parameter list over two lines the brace went inside
  the list, and the body ran as the file's own statements.
- **The rule.** A function's or a method's header ends with its name, its parameter list and `maybe`. Anything else on its line
  is refused; a parameter list its line does not close is refused. A comment after the header stays.
- **The spelling of the second is this desk's** (D84): the grammar reads no parameter list across lines on either surface, and
  neither Haro's own code nor stzlib's `.haro` files write one.
- A brace after a header keeps the refusal that names it.

### A name is read to its end

The count of this rule on stzlib's landed `.haro` files showed a defect of the rule as first built (966e123): it ended a name at
its first byte that is no letter, digit or underscore. `func Stz@(tType, xP)` was then a header with a statement after it, and a
program that loads stzlib's `stzFuncs.haro` stopped at that line; a name that starts with `@` was not looked at. A name is now
read to its end by the grammar's own bytes, and the refusal writes it whole. F11 says what stays, F12 and F13 what is refused.
The defect stood in a private build only: the count is run before an install for this.

### The older refusal stays

`func f iA, iB` has had its own refusal since v0.55 -- a definition's parameters stand in parentheses -- said by the compiler
where the function is called. On the build of ee8416a the header's rule answered first, when the program is compiled and in other
words; the guard's stage 60 (O26) failed for it. A header with no parenthesised list whose rest is names with commas between, the
first no keyword, is left to the compiler's rule (F14). After a list in parentheses, names and commas are a statement on the
header's line and the header's rule answers (F15; F16 with no blank after the list, the case only that stop refuses).

## One reading, kept image or fresh compile (HARO-IMAGE-EVAL-LENIENT-01)

- **What it was.** `Eval` reads its text by the surface of the program's root file: a `.haro` program's by Haro's rules. A fresh
  load says which surface that is; a run served from the kept image said nothing, so `Eval` read the text by the other surface's
  rules -- a built-in in another case, `:key = value` -- and took what the first run of the same program had refused. A verdict
  depended on whether the image was kept.
- **The rule.** The image path says the root's surface as the load does. Three runs of a program -- the first compiled, the next
  two served from the image -- print the same bytes, in what `Eval` refuses and in what it takes.

## A call the graph cannot draw (HARO-GRAPH-LATECALL-01)

    CALL|Go|*|late|2        # Go makes two calls by a name built when the program runs

- A `call x()` names its target when the program runs, so no edge can be drawn for it. The graph said nothing, and a reader of
  its lines could not know the caller's edges had a hole.
- The compiler counts those calls where it compiles them, function by function, and `haro graph` prints one line for each
  function that holds any: the caller, `*` for the callee, `late`, and how many. The summary on the standard error says how many
  such calls and functions the unit holds, and says nothing for a unit that holds none: such a unit is summed up byte for byte as
  it was.
- The extra fields follow the protocol's rule: a reader that takes fields 2 and 3 reads a caller and `*`.

## Measured

- The court: 16 of 16 on both builds. One expectation was corrected before the code from the fresh run's own bytes; six
  cases were added after the court spoke, each before the fix it asked for. 12 plants in `vm/src`, each built and each caught
  by its fixture (`plants.py`). Two were missed first: one took out a reset nothing reads, one asked for a case that writes
  no blank after the list.
- The courts of v0.72 to v0.76 hold on the same builds.
- `haro check` of v0.75's build against v0.77's, file by file: on stzlib 2a5b3ca7f, 204 `.haro` files, 0 not read, errors 1562 -> 1562, 0 files change; on stzlib 1d63b0f97, 255 files, 0 not read, errors 4018 -> 4018, 0 files change -- the header's rule adds no refusal on stzlib. On 1d63b0f97 the 18 files that name `System` or `SystemCmd` hold 36 statements in 13 files that v0.75 refuses as a built command line, 30 of them in the security plane's 9 files (written as 28 when this was recorded on 2026-11-16: the list was right and its sum was not), and none in its general desk's files, whose 11 lines are converted. Counted again on stzlib 448013c92, 2026-11-17: 6 statements in 4 files, none in the security plane's; and its GPU guard's two are converted since (e28024800), which leaves 4 statements in 3 files
- The 82-stage guard on builds made from the commit: PASS, 0 failures, 1994.5 s on the builds of 83d2d99; its stage 6 read 139.1 ms cold and 15.6 ms for an edit with another desk's run beside it, 122.4 ms and 15.1 ms alone, under ceilings of 150 and 50

## What stands at its present size

- A header over two lines is refused; the grammar reads none.
- `haro graph` counts a call by a built name and draws no edge for it; `Eval` shows its function as unfinished, as it did.
- HARO-CALLCOUNT-01, a count of calls written when a program ends, is open; its desk no longer waits on it.
