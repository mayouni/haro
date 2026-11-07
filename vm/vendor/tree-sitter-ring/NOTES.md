# tree-sitter-ring, vendored

The Ring grammar: `ysdragon/tree-sitter-ring` by Youssef Saeed, MIT
(`LICENSE` travels with it). `tree-sitter.json` says 0.2.0, which is not the
release tag; the copy here postdates the v1.1.1 fix, as the re-measurement
below was made on it. It
is the front end of `rnxc` -- every Ring source file the compiler reads
goes through `src/parser.c` and `src/scanner.c` here.

`SHA256SUMS` records every file; `tests/run-all.ps1` checks it on every
run under the gate `vendored grammar`, needing no network and no compiler.

Grammar findings reported upstream and their outcome are in
[`upstream/tree-sitter-ring-notes.md`](../../upstream/tree-sitter-ring-notes.md):
issue #2 was fixed by Youssef in `287afffb`, shipped as v1.1.1, and
re-measured here (wrongly rejected files 18 -> 11 across 10,233).

**The grammar is a lens, never the judge.** It locates spans and structure;
whether a program is valid Ring is decided by the oracle running it.

## Haro's change: one spelling per keyword (2026-11-06, HARO-SURFACE-01)

Haro no longer carries the grammar as Ring has it in one respect: `keyword()` is the lowercase word, exactly, where it was `ci()`, every case. A
`.haro` file is read with that grammar as it stands; any other file is read as Ring reads it, because the Haro VM's lift lowers its keyword-shaped
words before the parse is kept (`vm/src/lift.zig`, `ring_keywords`). `src/` was regenerated with tree-sitter 0.25.10 -- the version that made the
copy before it, which regenerating the unchanged grammar reproduced byte for byte. The author's ruling and the measurements: `spike/v41/GRAMMAR.md`.
