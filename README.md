# Haro

Haro is the foundational language of the Softanza project: a closed, judged family of grammars in which a world is declared,
constrained, asked, moved, stepped and spoken to. Every sentence is judged by a court generated from its declaration, and every
refusal is named and cited. It runs on its own VM, `haro`.

**This repository is private.** Nothing in it is published until its author says so.

## Running it

    python paths.py                                       what this checkout runs on
    cd vm && zig build -Doptimize=ReleaseFast -j2                       the Haro VM            vm/zig-out/bin/haro.exe
    cd vm && zig build -Doptimize=ReleaseSafe -j2 -p zig-out-safe       its checked build      vm/zig-out-safe/bin/haro.exe
    python spike/haro_forge.py                            the guard: every rung's court on both builds (34 stages)
    python spike/haro_forge.py --stage=N                  one stage
    python spike/haro_forge.py --plant                    must FAIL: a check that cannot fail is not a check

Every court runs on the VM and on its checked build, and the two must print the same bytes. The few stages that drive Softanza's
library run it on Ring++'s package, the bridge that keeps Softanza's legacy code running; a Ring++ checkout beside this one
(`..\ringpp`, or `RINGPP=`) provides it.

## Where it came from

Haro grew inside Ring++, under `haro/` on branch `next` of github.com/mayouni/rnx-spike, from 2026-09-26. On 2026-11-02 it cut with
the Ring legacy: it moved here with its history, forked Ring++'s VM and compiler into `vm/` as its own, renamed every source file
`.haro`, and stopped running Ring in its courts. Records written before then still say `haro/X`, `X.ring`, `rnxc` and "the oracle".

## Where to read

    CLAUDE.md        the brief, and what is where
    CHARTER.md       the charter: the alphabet, the decisions (D1-D42), the amendments
    PRINCIPLES.md    the founding principles;  GRAMMAR-SKETCH.md  the first grammar
    SPIKE.md         every rung, one section each, the cut, and what comes next
    FINDINGS.md      HF-1 to HF-134, each one measured
    CODEGRAPH.md     the code-graph memo;  BLOCKS.md  one format and pattern rules (REBOL-06/07)
    FROM-RINGPP.md   what Ring++ handed over;  vm/NOTES.md  what the VM's fork kept and why
    spike/           the meta-court, the forge, the courts, each rung's fixtures (written first) and grammar
    study/           the measurements behind the memos
