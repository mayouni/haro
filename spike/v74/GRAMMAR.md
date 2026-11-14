# Haro v0.74 -- a folder made, a run answered whole

The two debts v0.73 named (D90, HF-179) before D88 (d)'s refusal of a command line built as text, built together (D91): a built-in
that makes a folder, and a run that answers its exit code and what the child wrote in one value.

    MakeDir("out/reports/2026")                       # the folder and the folders above it; one that stands is left as it is
    MakeDir(sDoors.Place("out", tGiven))              # a place: its root allows write, and the door checks where it opens

    rRun = sDoors.Invocation("verify", ["check", hFile]).Run()     # no shell; nothing of the child's reaches the program's output
    if rRun.iCode != 0
        print rRun.tOutput
        print rRun.tErrors
    end

Fixtures first (ff8f939: 11 cases, 2 of 11 before the code -- the two that say an existing name reads as it did; 1ac20d5: a twelfth,
before any build). The code a221bdf; two cases the plants called for, a third for the shape stzlib has, the plants and stage 79
e3587d3.

| line | what | cases |
|---|---|---|
| L1 | `MakeDir(tPath)` makes the folder and the folders above it that are missing; a folder that stands is left as it is | W01 |
| L2 | `MakeDir(hPlace)` takes a place: its root allows write, or PLACE_NOT_ALLOWED and nothing is made | W02 |
| L3 | the door checks again where it opens: a place that leads out of its root through a link is PLACE_ESCAPES, and nothing is made | W03 |
| L4 | a folder that cannot be made is FOLDER_NOT_MADE; what is neither a text nor a place is a bad parameter | W04, W05 |
| L5 | a program's own function named MakeDir is the program's, wherever in the program it is defined; a `.ring` file reads the name as it did; in a `.haro` file the built-in has its one spelling | W06, W07, W13, W14 |
| L6 | `hCall.Run()` runs the invocation with no shell and answers a record: `iCode` the exit code, `tOutput` what the child wrote, `tErrors` what it wrote to its standard error, the last line end of each dropped; nothing of the child's reaches the program's output; the child stands where the command says | W08, W09 |
| L7 | a program that cannot be started is COMMAND_NOT_STARTED | W10 |
| L8 | the door beneath is the judging library's alone: `SystemRun` written in a program is refused when compiling, and given what is no invocation it says so (RUN_TAKES_INVOCATION) | W11, W12 |
| L9 | `haro check` reads no error where MakeDir and Run are written rightly, and knows the door's name | W01, W02, W08, W12 |

## The spellings (this desk's, under D84), chosen after reading the lines they serve

Read on stzlib origin/main 2a5b3ca7f before a word was chosen (HF-179 (9)):

- **`MakeDir`** is the name stzlib's own function bears (`core/common/stkRingStdFuncs.haro`: it runs the shell's `mkdir`, and its
  desk counts 108 calls of it, 92 in its tests). A program's own function of a built-in's name is the program's -- also when it
  is defined in a file loaded after the file that calls it (W14) -- so stzlib reads as it did; when its function is taken out, its
  `.haro` callers reach the built-in, with no shell. Its meaning is kept: the folders above are made too, and a folder that
  stands is no fault.
- **`Run()`** is a method of an invocation, and its answer a record, `HaroRun`, with lettered fields: `iCode`, `tOutput`,
  `tErrors`. One line of stzlib reads the exit code and the output of one run (`base/test/neural/_measure_screen_formats.haro`).
- **FOLDER_NOT_MADE**: `the folder ... could not be made` -- a file stands where a folder would, or the platform will not make it.

## How the three ways to run an invocation differ

| written | the child's standard output | its standard error | the answer |
|---|---|---|---|
| `System(hCall)` | passes through as it is written | passes through | the exit code |
| `SystemCmd(hCall)` | read whole | passes through | what it wrote |
| `hCall.Run()` | read whole | read whole | a record: the exit code, what it wrote, its errors |

QUIET on the command sends away what would pass through. Each starts the program from the invocation's vector, with no shell, in
the folder the command says.

## How it is built

- **`MakeDir` is a built-in of `.haro` code** (`compile.zig`'s table, `main.zig`): the platform makes the path whole; a refusal by
  the platform is FOLDER_NOT_MADE. It stands in the list of doors that take a place, asking `write`: what the root allows, the
  second check where the door opens -- the nearest folder above that stands is asked where it leads -- then the place's path.
- **`Run()` is Haro code** (`judge_lib.haro`): it calls the door beneath, `SystemRun`, and builds the record from the three values
  the door answers.
- **`SystemRun` is the VM's**, taken where a native is called, as `SystemCmd`'s door is: the same start from the vector, both
  streams read whole, the last line end of each dropped, nothing written by the VM. The compiler refuses the name in a `.haro` file
  that is not the judging library, so a run answered whole has one spelling; the native of that name, reached with what is no
  invocation, answers RUN_TAKES_INVOCATION.
- **The checker's table** knows `MakeDir` and `SystemRun`; `study/v48`'s table of spellings holds `MakeDir`.

## The desk's readings (D91, under D84)

- **`MakeDir` is Haro's own**: a built-in of `.haro` code alone. A `.ring` file reads the name as it did.
- **A folder that cannot be made is refused by name.** stzlib's function sent the shell's answer away and so could not fail; the
  built-in says what happened. For stzlib that is a new answer at its 108 calls on the day its function is taken out: a file in
  the way, or the platform refusing.
- **A run answered whole is asked of its invocation**, and has no form that takes a text: there is no shell beneath it.
- **The record is data**: `HaroRun(0, "", "")` may be written by any program. An invocation is made by its judge alone; what a run
  answered is a value like any other.

## Measured

- The court: 14 of 14 on both builds; 12 of 12 on the first build, with no expectation changed. 15 plants in `vm/src`, each
  built and each caught by its fixture (`plants.py`). Three plants first caught nothing: two cases were added for them (W13, and
  W12's check) and one table entry no case could fail was taken out.
- The courts of v0.72 and v0.73, and the court of the built-ins' spellings, hold on v0.74's builds: 18 of 18, 21 of 21, 9 of 9.
- stzlib origin/main 2a5b3ca7f, its 204 landed `.haro` files, `haro check` of each alone, v0.73 against v0.74: 1,498 errors before and after, no file changes, every file read (871 s, beside another desk's sweep, with a per-file limit of 900 s). The count is of the checker on standalone files; a `.ring` program that loads stzBase and runs is not in it
- The 79-stage guard on builds made from the commit: 79 stages green, 0 failures, 2,032 s; stage 6, the cold-load timing, read 135.3 ms, under the 150 ms ceiling, on a machine that read fit to measure

## What stands at its present size

- `Run()` reads both of the child's streams whole before it answers.
- `MakeDir` makes folders; taking one away, and the other built-ins of files (`FOpen`, `Rename`), take text as they did.
- A door given a text runs it through the shell, as it did: the refusal of a command line built as text is the next step. Each
  of stzlib's 10 such lines has its way out today: 6 declared commands, 1 `Run()`, 2 that go with its own `MakeDir`, and its
  `SystemCmd` wrapper, which its desk counted as having no caller.
- `n_lib.haro`, Haro's own run of a program through a command line, is converted with that step.
