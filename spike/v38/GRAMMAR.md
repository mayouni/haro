# Haro v0.38 -- `within` and `using`, onto `finally` (D52 rung 3)

stzlib-security's A2 and A3, as D52 decided them: A2 unamended, A3 amended for a dynamic surface. Fixtures first: `fixtures.json` and `cases/`
(4e9b2af), then the lift (`vm/src/lift.zig`), the compiler (`compile.zig`) and the printer (`fmt.zig`). No VM instruction is new: both blocks are
rung (1)'s `finally`, filled.

## What a program sees

    within $cCaller = "agent-x"     the global holds "agent-x" here and in everything called from here
        ...
    done                            and what it held before, after -- on every exit, a raise included

    using oKey = new SecretKey      oKey holds the value here
        ...
    done                            oKey.Release() -- or Destroy(), or Close(), the first it answers -- on every exit

| line | says | cases |
|---|---|---|
| W1 | inside `within` the global holds the value, in the body and in what it calls; after it, what it held before | W01 |
| W2 | restored on every exit -- a raise, a return, an exit or a loop crossing it, a callee's raise; a write by the body or a callee is undone | W02-W05, W11 |
| W3 | the global is saved FIRST, then the value computed (it may read the global); a value that raises changes nothing and the body never runs; a global with no value cannot be saved (R24 at the `within` line) | W06-W08 |
| W4 | `within` names a global, a `$` name (Rule A); a local or a parameter is refused at compile time | W09, W10 |
| U1 | at the end the first of Release, Destroy, Close the value answers is called, once -- in any case, an inherited one counting, in an eval too | U01, U02, U12 |
| U2 | called on every exit; a raise in it replaces a held raise, which becomes its cause (A1) | U03-U05 |
| U3 | `new K` of a class the unit defines, answering none, is refused at compile time; any other value answering none is raised at the block's entry, before the body, catchable; a value that raises releases nothing; a name a callee rebinds is raised at the exit | U06-U08, U10, U11 |
| U4 | the using name cannot be rebound inside its block: refused at compile time | U09 |
| B1 | the blocks nest with `try` in every shape the grammar misreads, and with each other; every line keeps its number | B01, B02, B10 |
| B2 | only the statement form is a block; a block with no `done`, no `= value` on its line, or a catch of its own is refused by name | B03-B08 |
| B3 | `haro fmt` prints both blocks as written | K01 |

## How it is built

- **The lift rewrites, on the same lines.** `within $g = v` becomes `try within $g = v`, and its `done` becomes `finally done`: a try whose
  body opens with the word and the header, and whose `finally` is empty. Every line keeps its number, so a report, `Span()` and the census name
  the line written (B02). The census counts the blocks (`lift.block_sites`).
- **The tokens say which `done` closes which block, because the tree cannot.** The grammar reads `within`, `using` and a `done` as bare names --
  except inside a try's catch or finally, where a `done` ends that try (B01). In document order, every `try` and every block opens; every `done`,
  keyword or bare name, and a try's other ends (`end`, `endtry`, `}`) close, innermost first. A word whose block never closes is left as it was.
- **The header is the next statement in document order**, not the next sibling: the grammar can end a function's body right after a bare word,
  and the header then stands one level up (U01 failed that way first).
- **The compiler recognises the try the lift made** (the word on the try's own line) and checks it before it emits anything: the refusals
  below. It then runs the header BEFORE the handler is armed, so a value that raises leaves nothing to restore or release (W07, U11):
  - `within` reads the global into a hidden local (`cWithin$d`; no copy is made -- the VM copies a shared list before it writes it, W11), then
    runs the header as written;
  - `using` runs the header, then tries the value at the entry.
- **The `finally` is filled wherever rung (1) compiles it** -- the normal end, a raise held, a return, exit or loop unwinding through it:
  `within` writes the saved value back to the global; `using` asks the value `isobject`, then `ismethod` for release, destroy, close in that
  order, and calls the first it answers. Answering none -- or not an object -- raises `using: <name> answers none of Release, Destroy, Close`:
  at the entry before the body, and at the exit only when a callee rebound a global name (U10). It is the VM's error, not a raise(), so an
  uncaught report names the block's line and no `raise()` (U08).
- **In an eval** a verb the program never names is skipped: no class can answer it (dispatch is by name), and an eval may not name it (U12).

### The refusals, each by name

    within needs a global (D52 A2)                                       `within x = ...` where x is not a `$` name
    using a class that answers none of Release, Destroy, Close (D52 A3)  `using o = new K`, K a class of the unit with none of the three
    using rebinds its name inside its block (D52 A3)                     an assignment to the name anywhere in the body
    within or using without its block (D52)                              a bare word: no `done`, or no `= value` on its line
    within or using with a catch of its own (D52)                        a block cannot catch; a `try` inside it can

## The desk's readings, recorded as its own

- The value is computed AFTER the save, so it may read the global (`within $depth = $depth + 1`, W06).
- A global with no value cannot be saved: R24 at the `within` line, as reading it is (A2: an ambient value "must exist").
- The name of a `using` cannot be rebound in its block. Rebound, its end would release the new value and leak the old: refused, not followed.
- Only `new K` is judged at compile time; a literal (`using n = 42`) is judged at the entry like any value whose class the compiler does not know.
- The verbs are matched in any case, an inherited method counting -- `ismethod` and the dispatch already do.
- A `finally` of the block's own can be written only by hand (`try within ... finally ... done`); it runs after the restore and is not refused.

## Not covered, named

- **A global rebound by a callee inside `using`** is raised at the exit, and the value the block began with is not released: the name is all the
  block holds. The checker's `haro/handle-held-across-raise` (rung 4) is where a held value is followed.
- **A class that gains Release by `addmethod` at run time** is refused at compile time when it had none of the three when compiled.
- **`blockSite`'s refusal of a site with no `finally`** is unreachable through the grammar (a try needs a catch or a finally, and a catch is refused
  first) and has no plant; it guards a hand-written `try within ... catch ... done` from compiling with no restore.
- **A rewrite that would break the parse is not made**: every word of that file is then refused by name, the blocks that were well formed with it.
