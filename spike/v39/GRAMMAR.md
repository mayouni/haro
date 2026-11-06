# Haro v0.39 -- A5's five checker rules, in `haro check` (D52 rung 4)

stzlib-security's A5, as D52 respelled it: five rules in the checker programmers already run. Fixtures first (`fixtures.json`, `cases/`, the court
`rule_court.py`: 5383b89), then the checker (`vm/src/check.zig`, `types.zig`), the loader (`haro.zig`) and the lift (`lift.zig`).

## What a programmer sees

    haro check app.haro [--listeners=Serve,Listen] [--validators=IsSafe,StzIsQueryCondition]

| rule | tier | fires on | cases |
|---|---|---|---|
| `haro/last-error-read` | note | every read of `cCatchError` -- worded for a read in its handler (bind the error: `catch e`) and outside one (whoever raised last); a member, a write and a binding of that name are not reads | L01-L05 |
| `haro/text-run-as-code` | error | `eval()` of text that is not literal (a string, or a `+` of strings), unless a validator the checker was told of is called in the same body | T01-T05 |
| `haro/listener-binds-all` | warn | a literal `"0.0.0.0"`, `"::"` or `""` given directly to a listening native the checker was told of; told of none, a closing line says so | N01-N03 |
| `haro/global-restored-by-hand` | warn | a body that saves a `$global` in a local and later writes it back from that local (a plain `=`), outside any `finally` -- worded for whether a raise between leaves it set, or a catch restores it too | G01-G05 |
| `haro/handle-held-across-raise` | warn | a local assigned an engine handle (a call `StzEngine...Create` or `StzEngine...Hold`) that no `finally` of its body releases (a call naming Release, Destroy or Close with it) and that the body does not return; a `$global`, an `@attribute` and an attribute the class declares are the program's or the object's | H01-H06 |

`last-error-read` is note until stzlib's sweep reads 0, then error (ruling 2 of SOFTANZA_ONE_HOUR.md). A rule told of nothing looks at nothing
and says so -- for `listener-binds-all`, in words that are not "NOT checked", which `v20/refine.py` reads as a checker shut.

## How it is built

- **The checker reads the lifted tree** -- the one the loader made, what the compiler reads -- instead of parsing each file's raw text again.
  It is why the rules see `catch e` as a binding and a `within` block as a try. **It also ends a defect of v0.37 and v0.38**: the raw text's
  `e` (of `catch e`), `within` and `done` were reported by `haro/uninitialized-variable` as names nothing assigns. The write collector of
  `types.zig` now counts a catch's binding, and the word of a block is no read.
- **Columns stay the file's.** The lift keeps every row and now records every byte it puts in (`lift.Insert`, composed across its passes into
  the file's coordinates); `checkLifted` maps each finding's column back with them (L05: 14, not the lifted text's 18).
- **A body is the definition and the statements after it, up to the next definition**, and a class runs on past where the grammar ended it.
  The grammar can end a `function_definition` after one statement and a `class_definition` after one attribute and leave the rest as top-level
  siblings; the compiler, as Ring does, reads them as the function's or the class's (G01, H06 -- stzlib's `stzCancelToken.ring`).

## Measured on stzlib

`haro check max/stzMax.ring` on origin/main f77486b5a (git archive, read-only), 765 files:

| | before (v0.38, 5383b89) | after |
|---|---|---|
| the checker's other findings | 9,180 (13 error, 24 warn, 1,690 perf, 7,453 note) | the same 9,180, line for line: file, position, message |
| `last-error-read` | -- | 41 notes |
| `text-run-as-code` | -- | 115 errors; 112 told `--validators=StzIsQueryCondition,StzIsPlainIdentifier` (84 run a name, 23 text built with `+`; 37 files, most in stzObject.ring 20 and stzFuncs.ring 12) |
| `global-restored-by-hand` | -- | 9 saves: 3 with nothing on a raise (stzPIAgent.ring's `$cStzCaller` and `$nStzActiveAgentWorkbench`, stzModelsReport.ring), 6 restored in a catch too (stzVision.ring) |
| `handle-held-across-raise` | -- | 4, none a handle: a status code (stzSequence.ring, stzGridNav.ring twice) and a registry slot (stzAgentHost.ring); 14 before the attribute exemption |
| `listener-binds-all` | -- | not looked at: no listener named |

## The desk's readings, recorded as its own

- A read of `cCatchError` in its handler is reported too: ruling 2's sweep counts every read until it reads 0.
- "Passed a validator" is a validator called anywhere in the same body, as stzlib's own rule reads it; a helper whose callers validate is
  reported (T05), so `_StzWCheckedPositions` is among the 112.
- `""` is a bind address only when given to a listener; only a literal given directly is seen (N03).
- A by-hand restore a catch also makes is still reported: A2 makes the old shape a finding, and `within` is that shape written once (G02).
- A5's name pattern for a handle is kept as written; on stzlib it catches 4 values that are not handles, which only the pattern's owner can narrow.

## Not covered, named

- A validator in the caller is not followed into the callee; an address passed through a variable is not followed to the listener.
- A handle whose class inherits its attribute from a parent class declared elsewhere is not seen as the object's.
- `last-error-read` at error tier waits on stzlib's sweep reading 0.
