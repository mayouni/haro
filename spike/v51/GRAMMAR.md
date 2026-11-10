# Haro v0.51 -- `haro check --facts`: what the checker establishes, per function, as one record

HARO-FACTS-01, answering stzlib-testoor's HARO-PROOF-01 (a) (2026-11-08 18:51, on the Principal's word): "can Haro's graph or `haro
check` export, per function, what the checker already establishes ... with the checker's version and the source hash? Testoor needs
nothing else to begin recording grade 5". This desk answered with the record's shape (2026-11-09 10:56); this rung builds it.

Fixtures first (a1e1f1f: 14 cases, all failing before the code). Code 6bd7e0f. **One fixture changed after the code**, said so: X13
held `eval("x = 1")`, which the checker reads, so the variable rule keeps looking past it -- the text report says the same; X13 now
evals text the checker cannot read, and X15 keeps the literal eval.

| line | what | cases |
|---|---|---|
| P1 | the record names its format, its checker's commit, and every file read by sha256 and surface; `haro check --facts <file>` is `haro check <file> --facts` | X01, X02 |
| P2 | every function and method of the unit, in file order, its class, its lines, the checker's findings inside it; a finding outside every function is its file's | X03, X04, X05, X12 |
| P3 | its calls: bound by the compiler (`calls_static`; a lambda's are its function's), dispatched by name (`calls_dynamic`), resolved when the program runs (`calls_late`: a native, or nothing) | X06, X07, X12 |
| P4 | its first direct impurity and its line, absent when none is seen | X08, X09 |
| P5 | whether the compiler finished its own body (`compiled`), why not and where (`refused`), and whether it calls a function that was not finished (`reaches_uncompiled`) | X10, X11 |
| P6 | the rules that did not look, and why, as the text report says them | X13, X14, X15 |

## The record

```
haro check --facts prog.haro          (or: haro check prog.haro --facts; --listeners= and --validators= as for haro check)

{"format": "haro-check-facts/1",
 "checker": {"name": "haro", "commit": "<the last commit that touched vm/>[+uncommitted]"},
 "files": [{"path", "sha256", "surface": "haro" | "ring", "top_findings": [...]}],
 "not_checked": [{"rules": [...], "why"}],
 "impurity": "<what the analysis is, in one sentence>",
 "functions": [{"file", "name", "class", "line", "end_line", "findings": [{"rule", "severity", "line", "col", "message"}],
                "impure": {"why", "line"}, "calls_static", "calls_dynamic", "calls_late",
                "compiled", "refused": {"why", "line"}, "reaches_uncompiled"}]}
```

- **A field for a fact not established is absent, never false.** `impure` appears only where the analysis saw one; `refused` only where
  the compiler stopped. `total`, `uses` and profiles (D55 T7, D56) are not built and are not in the record; each joins when its rung
  lands.
- **The checker's version is its source**: `build.zig` asks git for the last commit that touched `vm/` and bakes it in, with
  `+uncommitted` when `vm/` held changes as it was built, and `unknown` without git (a build from an archive). A commit of records
  alone does not change it. The build mode is no part of it: both builds print the same record (D41).
- **The sha256 is of the bytes read** -- a file's own bytes on disk, before any lift.
- **The impurity analysis is the checker's** (`haro/cache-impure`'s): writing a `$global`, printing, or calling one of sixteen named
  functions whose value moves on its own, in the function's own lines; calls are not followed. Silence is not purity, and the
  record's `impurity` sentence says so to every reader.
- **A function's lines** run from its definition to the next definition, as the checker reads a method (the grammar does not nest a
  method's body), blank lines at the end left out, comments kept.

## How it is built

- `src/facts.zig` prints the record from what `haro check` already holds -- the unit, the report's findings, the definition
  universe's silences -- and from a lenient compile with the census on (`compile.zig`, `factsData`), which gives each function's
  calls and each refusal's site. `Func.calls_late` is new: the name of each call compiled to be resolved when the program runs.
- `types.zig`: the checker's impurity test is split into the node's own test (`impurityDirect`) and its recursion, so the record and
  the checker share one definition.
- **One walk per file.** The first version walked the file's tree once per function, for its end and for its impurity; tree-sitter
  reaches a child, or a next sibling, by stepping from the first, so on stzlib it ran past ten minutes. Each file is now walked once
  with a tree cursor, each function's end read from the compiler's own list of definitions, each row found by bisection.

## Measured

- **The court**: 15 of 15 on haro and its checked build (stage 55), the same bytes from both. **The guard**: 55 stages on the committed tree (c7fd7d2), PASS, 0 failures, 1,517 s.
- **Plants**: G1 to G15, each one protection switched off: 15 of 15 caught (c7fd7d2). Two were rewritten after their first runs, said
  so: G3 did not build (hashing the path left `origs` unused, which Zig refuses); G8 MISSED, switching off one of two folds -- a
  lambda's call the compiler patched is folded by the second loop, so the protection is the pair, and G8 switches both off.
- **At Softanza's scale**: `haro check stzBase.ring --facts` on stzlib cb6f5de65 (a git archive in runtime/stzlib-cb6), heartbeat fit
  to measure: **26.6 s** for 720 files and 48,756 functions, a 14 MB record -- plain `haro check` 11.8 s and the compile (`haro graph`)
  15.1 s, the record about their sum. Every finding of the text report is placed once: 9,549 = 9,533 in functions + 16 at file tops.
  793 functions show a direct impurity; 5,380 late calls; all three absence rules and the variable rule did not look (the unit calls
  loadlib() or eval()), and the record says so.

## Named

- A `within` or `using` block is lifted with lines inserted (v0.38); a function's lines are the lifted tree's, which can stand below
  the file's own by the lines inserted. The findings are the file's own columns, as the checker maps them.
- `haro check` judges neither the letters (v0.47) nor the built-ins' spelling (v0.48) of a .haro file: those are the compiler's, and
  the record carries them through `compiled` and `refused`.
