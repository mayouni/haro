# Haro v0.73 -- the command and the invocation

`doc/DOORS.md`, its second rung (D88 (d), D90): a program declares the programs it runs, once, in the same sentence of doors that
declares its folders; the arguments are judged by their declared shapes into an invocation; and the two doors that run a program
take an invocation and start the program from its vector, with no shell.

    load "doors.haro"
    sDoors = doors'DEFINE COMMAND check AS (RUNS "haro", TAKES [word, place], IN src) RATIONALE "the checker, run as a child"
                   DEFINE ROOT src AS (AT "src", ALLOWS [read]) RATIONALE "the files this program checks"'
    hCall = sDoors.Invocation("check", ["check", sDoors.Place("src", tGiven)])     # judged, or refused by name
    print SystemCmd(hCall)                                                         # no shell: the program and its arguments

Fixtures first (7ad48a4: 18 cases, 0 of 18 before the code; 9f58151: a nineteenth, still before the code). The judge in Haro
a731feb; the VM, the compiler, the loader and the checker c459605; what stzlib's own lines asked for -- IN, the wider QUIET -- with
the cases it changed and added, the plants and stage 78, 115dc85.

| line | what | cases |
|---|---|---|
| L1 | a sentence of doors declares commands; `sDoors.Invocation(command, vArguments)` answers an invocation: its command, its arguments as texts; it prints as its command and arguments; the letter `h` holds it; a sentence of another language judges none (INVOCATION_NO_DOORS) | V01, V17 |
| L2 | `SystemCmd(hCall)` runs the program with no shell and answers what it wrote: an argument arrives as one argument, byte for byte, whatever a shell would read in it | V02 |
| L3 | `System(hCall)` runs it and answers its exit code; what the child writes passes through, after what the program wrote first | V03 |
| L4 | each argument is judged by its declared shape, or INVOCATION_SHAPE; the count is the declaration's, or INVOCATION_COUNT; `words` stands once in a command, or COMMAND_WORDS | V04, V05, V06, V19 |
| L5 | a command the sentence does not declare is COMMAND_UNKNOWN, and the refusal names the ones it does | V07 |
| L6 | no shell: a command that runs a shell, or a file a shell reads, is COMMAND_SHELL | V08 |
| L7 | the declaration's court: a command that runs nothing (COMMAND_NOTHING), one that says RUNS and ITSELF (COMMAND_TWICE), a shape outside the six (UNKNOWN_SHAPE) -- each refused when the program is compiled, its verdict the standalone court's | V09 |
| L8 | ITSELF yes runs this haro; RUNS names a program found as the platform finds one; a program that cannot be started is COMMAND_NOT_STARTED | V02, V10, V11 |
| L9 | an invocation is made by its judge alone, and is not written into (INVOCATION_FIXED) | V12, V13 |
| L10 | QUIET yes: nothing the child writes reaches the program's output -- `SystemCmd` still answers what it wrote, `System` answers its exit code alone; without it the child's standard error passes through, and under `System` its standard output too | V14, V15 |
| L11 | a door still takes text as it did, a built command line included: the rung refuses nothing that ran | V16 |
| L12 | a forged court's folder is named by which haro forged it too: another haro at the same place forges its own | V18 |
| L13 | a command runs IN a root: the child stands in the root's folder, and a place it is given is given whole; a root that is not declared is the court's DANGLING, a root with no folder COMMAND_IN | V20, V21 |

## The spellings (this desk's, under D84)

- **The kind COMMAND** of the language of doors: `RUNS "program"` names the program, found as the platform finds one; `ITSELF yes`
  says it is this haro; `TAKES [...]` gives the shape of each argument, in order; `IN root` names the root whose folder the
  child stands in; `QUIET yes` keeps everything the child writes from the program's output.
- **The six shapes**:

  | shape | what it takes | given to the program as |
  |---|---|---|
  | `word` | a text of letters, digits and `_ - . , =`, with no blank and no dash first | itself |
  | `option` | one or two dashes, then a word: `-x`, `--deep`, `-Doptimize=ReleaseFast` | itself |
  | `number` | a number -- never a text that reads as one | its text |
  | `place` | a place, judged by `Place` | its path; whole, when the command runs IN a root |
  | `text` | any text with no control byte and no dash first | itself, as one argument |
  | `words` | one or more words; once in a command | one argument each |

- **The judge `Invocation(command, vArguments)`**, a method of a sentence of doors. Its answer is an invocation: `Command()`,
  `Program()`, `Arguments()`, `Quiet()`, `In()`; printed, it is its command's name and its arguments, one in quotes where it is empty or
  holds a blank or a quote.
- **The doors are the two that run a program today.** `SystemCmd(hCall)` answers what the child wrote to its standard output,
  the last line end dropped as the text form drops it; `System(hCall)` lets the child write where the program writes and answers
  its exit code.
- **The letter `h`** holds an invocation: T7's handle of the process door, held before the door is opened.

## No shell

- A door given an invocation starts the program from the invocation's vector: the program, then each argument as it is. No line is
  made and no shell reads one, so an ampersand, a bar, an angle bracket, a percent or dollar name, a quote and a backquote in an
  argument are bytes of that argument (V02).
- **COMMAND_SHELL**: a command whose program is a shell by its name -- `cmd`, `command`, `powershell`, `pwsh`, `sh`, `bash`, `zsh`,
  `dash`, `ksh`, `csh`, `tcsh`, `fish`, with or without a folder and an extension -- or a file a shell reads by its kind -- `.bat`,
  `.cmd`, `.ps1`, `.sh`. A command is a program and its arguments.
- **No argument is read as an option unless the declaration says an option stands there**: a word and a text do not begin with a
  dash.

## How it is built

- **The declaration** (`spike/doors.haro`): the kind COMMAND, the menu of shapes, two constraints; the language NEEDS process beside
  filesystem, and a COMMAND OPENS process, so the sentence's world rows say which programs a program runs.
- **The judge is Haro code** (`judge_lib.haro`, `HaroInvocationOf`): it reads the commands the sentence declares through the
  sentence's own court, judges each argument, and makes a `HaroInvocation` -- the command's name, whether it is quiet, the line it
  prints as, the vector. The reading of a sentence's declarations is one function, the place's judge using it too.
- **The VM knows an invocation by its class**, as it knows a sentence and a place: it prints as its line, the letter `h` holds it, a
  write into it is INVOCATION_FIXED, and `new` of one is refused by the compiler outside the judging library.
- **At the door** the VM writes out what the program wrote first, then starts the child from the vector. Under `System` the child
  inherits the program's standard output; under `SystemCmd` its output is read whole. The child stands in the invocation's
  folder when the command names one. A program that cannot be started is COMMAND_NOT_STARTED, at either door. Given a text,
  both doors do what they did.
- **A forged court's folder** is named by the declaration, by where haro stands, by the forge's files, and now by haro's own file's
  size and time: a haro put where another stood forges its own folder (HF-178 (9), closed).
- **The checker knows `SystemCmd`**, Haro's own native; it read an undefined function there.

## The desk's readings (D90, under D84)

- **This rung builds the invocation and refuses nothing.** D88 (d) refuses, in `.haro` code, a command line built as text once
  invocations are built. That refusal is the next step, with its own number: stzlib's landed `.haro` files hold 10 such lines, and
  they are converted against an installed invocation, their list sent first.
- **The doors are the existing two.** A door takes the program's own text or a judged value (D88 (a)); the judged value of the
  process door is the invocation, so `System` and `SystemCmd` take one, as `Read` takes a place.
- **A shell is refused by the judge, by name and by kind**, in one place.
- **IN and the wider QUIET came from stzlib's own lines**, read before the install: of its 10 lines that build a command line, 6
  change folder first and 7 want the exit code with everything the child writes sent away. A root says where a child may stand,
  as it says where a file may be opened; and QUIET has one meaning at both doors -- nothing the child writes reaches the
  program's output.
- **Haro's own run of a program is converted with the refusal.** `n_lib.haro` builds one command line as text; that library is
  loaded by courts, and a court that loads the judging library does not judge (`court_lib.haro`, `CtMain`), so its conversion goes
  with the step that reworks that switch.

## What the rung found

- **The court passed on the first build**, 19 of 19 as it then stood, the hostile arguments among them.
- **stzlib's lines were read after the court spoke**, and asked for IN and the wider QUIET: four cases changed or added before
  the install, each said in the generator (V03, V15, V20, V21).
- **The plants sharpened two cases**, said in the generator. One door passing the child's standard error through hid the other
  dropping it, so the case counts the line twice (V14); a number given where a word, an option or a text stands had no line of
  its own (V05).
- **A plant runs its own case alone** (`--only`): the 30 plants that build nothing ran in the time one ran before.
- **The checker read `SystemCmd` as an undefined function**; the case that a door still takes text found it (V16).

## Measured

- The court: 21 of 21 on both builds. 53 plants, each caught by its fixture: K1-K19 in `vm/src`, each built; J1-J30 in the judge
  and M1-M4 in the declaration of doors, where nothing is built (`plants.py`).
- The courts of v0.70, v0.71 and v0.72 hold on v0.73's builds: 15 of 15, 14 of 14, 18 of 18.
- stzlib origin/main 2a5b3ca7f, its 204 landed `.haro` files, `haro check` of each alone, v0.72 against v0.73: 1,498 errors before and after, no file changes -- 202 read in a run beside another desk's sweep, the 2 that timed out there read alone after it (61 errors each, before and after). The count is of the checker on standalone files; a `.ring` program that loads stzBase and runs is not in it
- The 78-stage guard on builds made from the commit: 77 stages green in the full run, 3,036 s; stage 6, the cold-load timing, read 156.8 ms there on a machine that read throttled and ran another desk's sweep (the native court beside it read 11.8 ms where it reads 9.7) and, run again alone once the machine read fit to measure and alternated twice, 146.4 and 138.4 ms on v0.73 against 134.5 and 137.7 on v0.72, under the 150 ms ceiling

## What stands at its present size

- `Invocation` reads the sentence's commands through its court at each call.
- A door given a text runs it through the shell, as it did: the refusal of a command line built as text is the next step.
- `SystemCmd` of an invocation reads the child's output whole before it answers; `System` lets it pass as it is written.
- One run answers its exit code (`System`) or what it wrote (`SystemCmd`), not both. Of stzlib's 10 lines that build a
  command line, 6 are written as invocations today; 1 reads the exit code and the output of one run, 2 make a folder with the
  shell's `mkdir`, and 1 is a wrapper that takes any command line. A run that answers both, and a built-in that makes a
  folder, come before the refusal.
- A program is found as the platform finds one; where it is found is not judged.
- An argument that is one word of a MENU, and a place of a named root, are shapes for a later step.
- PEER and the endpoint are DOORS.md's rung 3.
