# Haro v0.79 -- `haro check` says what the run will refuse, and a reply carries only the head it writes

Fixtures first (`gen_fixtures.py`, `fixtures.json`, `cases/`), this note second, the code third. The court is `court.py`.

## What the desks found on v0.78

| family | found by | on v0.78 | from v0.79 |
|---|---|---|---|
| H | marbooha | `rpp_http_reply(iStatus, tType, tBody)` wrote `tType` into the reply's head as given: a type holding CR, LF or both wrote a header of its own (`X-Injected: yes` in the court's reply), and a type over 200 bytes was cut | the type is refused with `HEADER_VALUE`; nothing is sent; the request stays open and the program answers it again |
| B | marbooha | `check` called `Divide` and every `rpp_http_*` undefined, while haro.exe ran them: it knew 258 names of the older runtime and three of Haro's | `check` knows every name haro.exe answers: its compiler's built-ins and the natives it publishes when it starts |
| T | stzlib-gpu, marbooha | text + a number, a decimal + a float, a float + an integer: refused by the run (`NO_COERCION`, `NUMBER_MIX`), passed by `check` | `check` names them where a literal or a type letter shows both sides |
| Q | stzlib-gpu | `1 / 3` (no exact decimal) and any quotient given to an `i` name, even `10 / 5`: refused by the run, passed by `check` | `check` names them: `DECIMAL_INEXACT` for two integer literals, `TYPE_LETTER` for a quotient given to an `i` name |
| N | stzlib-gpu | a `.haro` file's top-level `nL = 5` replaced the line end every older file of the program reads: `"x" + nl + "y"` printed `x5y`, and nothing said so | a top-level assignment to `nl`, `tab`, `cr`, `stdin`, `stdout` or `stderr`, in any case, is refused when compiling, `NAME_RESERVED` |
| I | marbooha | a list indexed by a decimal or a float stopped with `Bad parameter type!` | `INDEX_NOT_INTEGER`, naming the value; `check` names it where a literal or a `d` or `f` name is the index |
| C | this rung's own sweep | `Add()`, `Add(x)` and `Len()` crashed the compiler -- a segmentation fault, exit 3 -- in `check` and in a run | refused by name, as every other built-in called with a wrong count is |
| E | stzlib-testoor | `haro graph` printed nothing for `Eval`, whose text may call any function | an `Eval` no function of the unit answers counts with the late calls, `CALL|<caller>|*|late|<n>` |
| L | iris | `haro check` of a 6-line file whose first statement loads stzBase (stzlib 5bb8697d2) took 596 s, 1,307 MB at its peak, printed nothing until the end and then 9,670 findings in 623 files -- none in the file named | `check <file>` reports the named file's folder and below; a file loaded from elsewhere is read for its names, not reported, and counted in one line; `--all` reports every file; the compile stands on a kept library where there is one, and `HARO_PATH=1` says the path |

## The spellings, chosen under D84 (delegated)

- `HEADER_VALUE` -- a reply's type holds CR or LF, or is over 200 bytes.
- `INDEX_NOT_INTEGER` -- a list's index in a `.haro` file is a decimal or a float.
- `NAME_RESERVED` -- a `.haro` top-level assignment to one of the six names every older file reads as built in. A function's
  local of that name is its own and stays allowed: a local replaces nothing.
- `check`'s new rules are named after the run's code each foresees, and each says that code in its words:
  `haro/no-coercion`, `haro/number-mix`, `haro/decimal-inexact`, `haro/type-letter`, `haro/index-not-integer`.
  A refusal made when compiling (`NAME_RESERVED`, a wrong count of arguments) is `haro/refused-form`, as since v0.69.
- `check --all` -- every file of the unit reported, as v0.78 reported. Without it, the line
  `<n> file(s) loaded from outside its folder: read for their names, not reported (--all reports them)`.

## The court

`court.py` judges five kinds: `check` (findings by line and rule, words said and not said, and the file's run where the
fixture has one), `http` (a real request on 127.0.0.1 and the reply's bytes whole), `graph`, and `scope` (the L family). A
`check` or a run that crashes -- exit 3, a segmentation fault, a panic -- fails its case whatever it printed: B05 passed its
first run on v0.78 because `check` died on `Add(x)` before printing anything, and that is how C was found.

On the installed v0.78, before any code: 16 of 52 cases pass -- the cases that say what stays, and H01 and H06, the replies
v0.78 already sends right. Every other case fails for the reason its fixture names.

## What a side's type is, for `check`

A side shows its type by a literal (`"text"`, `3`, `1.5`, `2.0f`), by a name's type letter (`t`, `i`, `d`, `f`), or by a call
whose answer has one type (`String`, `Float`, `Integer`). A name lettered `x`, or a value the run alone can know, shows none:
`check` says nothing there and the run still refuses (T04, Q05, I05 hold this).

## What stays

- A `.ring` file reads as it did: its own `nl = "|"` replaces its line end, as it always has (N06).
- `Eval`, `LoadLib` and the calls that admit code while a program runs switch the undefined-function rule off for their file.
- An integer `1` held in a `.haro` list and used as a condition is refused by the run, `BOOLEAN_EXPECTED`: only the run can know
  the value (stzlib-gpu's fourth reading, corrected by its desk on 2026-11-27).
