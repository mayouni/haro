# Haro v0.75 -- a command line is not built as text

`doc/DOORS.md`, D88 (d), built (D92): in a `.haro` file the two doors that run a program take a text written at the call, or an
invocation. With it Haro's own run of a program is an invocation: `n_lib.haro` asks its sibling court with no shell.

    System("git status")                          # a text written at the call: as it was
    System("echo " + "joined")                    # literals joined: as it was
    System(sDoors.Invocation("check", [hFile]))   # an invocation: no shell

    System("del " + tName)                        # refused when the program is compiled
    System(tLine)                                 # refused when the program is compiled: a name lettered as a text
    System(Build())                               # COMMAND_LINE_BUILT when the program runs, if what arrives is a text

Fixtures first (bcb4350: 10 cases, 5 of 10 before the code -- the five that say what ran still runs). The Haro side 9af2567; the
compiler and the VM 55cabe9; one case made sharper, the plants and stage 80 in the commit after.

| line | what | cases |
|---|---|---|
| L1 | a text written at the call runs as it did: a literal, and literals joined | X01 |
| L2 | a command line built as text is refused when the program is compiled: a text joined with anything that is not written there, and a name lettered as a text -- at either door | X02, X03, X04 |
| L3 | a text that reaches the door another way -- a function's answer, a name that may hold anything -- is COMMAND_LINE_BUILT when the program runs, and can be caught | X05 |
| L4 | an invocation passes, by any way it reaches the door | X06 |
| L5 | a `.ring` file reads as it did, at either door; a program's own function named System or SystemCmd is the program's | X07, X08 |
| L6 | a court whose library holds a sentence of doors still judges, and runs its sibling court with no shell: what it answers is what it answered | X09 |
| L7 | a sentence of doors is read once: its judges answer from what was read | X10 |
| L8 | `haro check` lists the refused line, and reads no error where the door is given what it takes | X01 to X06 |

## The rule, and whose reading it is

D88, ruled by the Principal: (b) the program's own literals stay allowed at a door in an ordinary program; (d) in `.haro` code a
command line built as text is refused once invocations are built. This desk's reading of the two together, until `unjudged`
(DOORS.md rung 4) gives every text its origin:

- **The program's own text is what is written at the call.** A text literal, or text literals joined with `+`, in the door's own
  parentheses.
- **Built as text, seen when compiling**: a text joined with anything else, and a name lettered as a text. The statement is
  refused: `a command line is written at the call, or is an invocation of a declared COMMAND`.
- **Anything else is asked where the program runs**: a function's answer, a name lettered `x` or `h`, an item of a vector. An
  invocation goes on to the door; a text is COMMAND_LINE_BUILT -- `this text was made elsewhere`; any other value goes on, and the
  door says what it is, as it did.
- **A text a name holds is refused though the program wrote it.** `tLine = "dir"` then `System(tLine)` is refused, where the same
  literal at the call is taken: where a text came from is not yet known to the VM, and the rule takes only what it can see. When
  `unjudged` is built the line moves to where D88 (b) draws it -- outside text refused, the program's own taken wherever it is held.

## How it is built

- **The compiler reads the argument's form** (`compile.zig`, `lineForm`) where `System` (a built-in) and `SystemCmd` (a native) are
  compiled in a `.haro` file: `written`, `built`, or `other`. `built` refuses the statement. `other` puts a guard before the door.
- **The guard is a built-in with no name** (`main.zig`, `cmdguard1`): a text raises COMMAND_LINE_BUILT; anything else is left in
  its register for the door.
- **A program's own function of either name is never reached by the rule**: it is resolved as the program's function first.

## Haro's own run of a program

`n_lib.haro` ran a surface's own court by a command line it quoted and redirected by hand. It now holds a sentence of doors --
`DEFINE COMMAND sibling AS (ITSELF yes, TAKES [text, words, text, text, text], QUIET yes)` -- and asks through its invocation.
Two things stood in the way, and both are general:

- **A court that loads a declaration did not judge.** A program that judges set a flag, and every court's main read it and did
  nothing. A court's main now asks whether the court is the program: the file haro was given is the court's own,
  `<language>_court.haro`. A court loaded by a program, or by another court's library, has no main.
- **Reading a sentence of doors used the court's own tables**, so a court that asked for an invocation while judging would have
  lost its place. A sentence of doors is read once (`HaroDoorsDeclared`), when `n_lib.haro` is loaded and before the court that
  loads it sets its tables; `Place` and `Invocation` answer from what was read. v0.72's and v0.73's limit -- the sentence read at
  each call -- is gone with it.

## Measured

- The court: 10 of 10 on both builds, on the first build and with no expectation changed. 14 plants, each caught by its fixture:
  K1-K10 in `vm/src`, each built; J1, C1, C2 and N1 in the libraries of `spike/`, where nothing is built (`plants.py`).
- The courts of v0.72, v0.73 and v0.74 hold on v0.75's builds: 18 of 18, 21 of 21, 14 of 14. v0.73's case of a door that still
  takes text ran a built command line; it keeps the literal, and says so.
- The N court's own check (stage 20's judge) passes on both builds with `n_lib.haro` converted, on v0.74 as on v0.75.
- stzlib origin/main 2a5b3ca7f, its 204 landed `.haro` files, `haro check` of each alone, v0.74 against v0.75, every file read: 1,498 errors before and 1,562 after, 29 files change, and all 64 new findings are this refusal. 11 lines of stzlib build a command line -- 3 in models_check_narrated, 3 in policy_diff_narrated, 1 in _measure_screen_formats, 1 in prefix_cache_narrated, 3 in core/common/stkRingStdFuncs.haro, which most of the changed files load. Its desk has the list, with what each line becomes on the installed v0.74
- The 80-stage guard on builds made from the commit: 80 stages green, 0 failures, 2,211 s; stage 6, the cold-load timing, read 134.5 ms, under the 150 ms ceiling, on a machine that read fit to measure

## What stands at its present size

- A literal a name holds is refused at these two doors; the same literal at the call is taken. `unjudged` moves the line.
- The rule is these two doors'. `LoadLib`, the doors of files and the others take text as they did.
- QUIET on `n_lib.haro`'s command keeps what the redirection it replaces did; the sibling court writes nothing to its standard
  error in any case of this rung, so no case fails without it.
- The shared runtime is v0.74: this rung is installed when stzlib's 11 lines are converted, after its notice.
