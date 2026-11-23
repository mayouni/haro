# Haro v0.78 -- three findings of the desks: the exit code, the kept library, a run that reads

D95. Three desks sent what they met on the installed runtime, and each was read there before a case was typed. The Principal
started the rung with "Start v0.78" (2026-11-23). The spellings below are this desk's, chosen with the fixtures under D84.

## A compile that fails ends with 1 (HARO-COMPILE-EXIT-01)

stzlib-security measured it in the OS boundary's guards: a haro.exe whose compile ran out of memory printed
`compile failed: OutOfMemory` and ended with 0, so a supervisor read success from a program that never ran. The ruling, given
for the Principal on his delegation of 2026-11-17: a compile that fails, for memory or for any other reason, ends haro.exe with a
non-zero exit code.

- Every command that compiles -- a run, `dis`, `graph`, `prefix`, `census`, `poison`, `usable`, `attrs`, `shadows`, `migrate`,
  `call`, `time`, `bench` -- reports through one way out, which prints the report as before and ends with **1**. It is the code
  every other way a program does not complete already has: a raise, a refused statement, a file that does not scan, a load
  that names no file.
- `haro check` whose compiler stopped before the unit's end prints its report, with the line that says refused forms were not
  checked, and ends with **1**: a gate that reads 0 from a check reads a whole check.
- The cases run a program of 6,000 functions under a Windows job that limits what a process may commit, down a ladder of
  limits. Where a run says the words, its code is 1; a ladder on which no rung says them fails, since it asked nothing.

## The kept library (HARO-LIBIMAGE-01)

An image is kept for one root file. A corpus of many small programs that load one library -- stzlib's 2,334 test files --
compiles the library once for every root. The VM holds the other half since the fork: `haro prefix <library>` writes the
compiler's state after the library, and a root whose **first statement** loads that library is compiled on top of it. No stage
held that path. stzlib-general found the cost, ran its corpus on the kept library, and asked for what a sweep needs.

    haro prefix lib.haro          compile the library once and keep it (one file in the cache folder, never retired by the cap)
    HARO_PATH=1 haro root.haro    the run says the path it took, on its standard error, in one line
    HARO_NOIMAGE=1                the root's own image is neither used nor written; the kept library is taken as before

The path is said after the compile, once the compiler has decided, and before the program's first statement:

| line | when |
|---|---|
| `path: kept image` | the root ran from its own kept image |
| `path: kept library` | the root was compiled on top of a kept library |
| `path: whole` | the unit was compiled whole: no kept library is there for what the root loads first, or its first statement is no load |
| `path: whole, the kept library does not apply (Name)` | a kept library was read and the root may not stand on it: it defines `Name`, which the library defines or called without finding. The root's own definition answers, as in every whole compile |
| `path: whole, the kept library is stale` | a kept library is there and was not taken: a file of the library, or haro.exe, changed since it was kept |

Without `HARO_PATH` a run writes nothing of its path. `HARO_IMAGE=1` keeps its own text, which says what was read and is
printed before the compiler decides.

`HARO_NOIMAGE=1` is the shape a corpus wants: the library compiled once, each root compiled on it and thrown away. A root's
image holds the whole library again, so a sweep without the setting writes one per root through a cache that retires them
as fast.

The usage text names `haro prefix <library.haro>`.

## A run that reads its standard input from a place (HARO-INVOCATION-STDIN-01)

stzradar met it at the install of v0.77: `ssh-keygen -Y verify` reads the message on its standard input and takes no file's
name, and an invocation has no shell to write `< file` for it.

    load "doors.haro"
    sDoors = doors'DEFINE ROOT feed AS (AT "feed", ALLOWS [read]) RATIONALE "what is checked"
    DEFINE COMMAND verify AS (RUNS "ssh-keygen", TAKES [option, option, place, option, word, option, word, option, place]) RATIONALE "a signature checked"'
    hCall = sDoors.Invocation("verify", [...])
    rRun = hCall.RunReading(sDoors.Place("feed", tName))

`RunReading` answers what `Run` answers -- `rRun.iCode`, `rRun.tOutput`, `rRun.tErrors` -- and the child's standard input is
the bytes of the file at the place. The declaration of a COMMAND does not change.

| refusal | when |
|---|---|
| `RUN_INPUT` | what is given is no place: "a run reads its standard input from a place -- <doors>.Place(root, text); given a text" |
| `PLACE_NOT_ALLOWED` | the place's root does not allow read |
| `PLACE_ESCAPES` | the place's path leads out of its root's folder, by a link |
| `INPUT_NOT_READ` | the place names a file that could not be read |

Each is raised before the child is started. The bytes are written to the child by a thread of their own while the run reads
what the child writes, so a child that writes much before it has read all does not stop on a full pipe.

## The cases

| line | cases | what |
|---|---|---|
| L1 | L01 to L04 | a root on the kept library prints what its whole compile prints and ends with its code: a root that runs, one that dies part-way, one that catches an error, one that runs text as code |
| L2 | L05 to L07 | the roots that are compiled whole beside a kept library, and what the path says of each |
| L3 | L08 to L10 | `HARO_NOIMAGE`, with a kept library and without; and what stays without it |
| L4 | L11 to L13 | the silence without `HARO_PATH`; `haro prefix`; the usage text |
| L5 | X01 to X05 | the exit code of a failed compile: a run, `dis`, `check`; and what stays |
| L6 | R01 to R06 | `RunReading`, its refusals, a large input with a large output; and what stays of `Run` |

## What stays

- A program with the memory it needs, a whole check, a raise, a refused statement: the codes they had.
- A run without `HARO_PATH` and `HARO_NOIMAGE` reads, keeps and prints what it did.
- `Run` gives its child no standard input.
- The rung refuses no form that runs today.
