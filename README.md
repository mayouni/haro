# Haro

Haro is the foundational language of the Softanza project: a closed, judged family of grammars in which a world is declared,
constrained, asked, moved, stepped and spoken to. Every sentence is judged by a court generated from its declaration, and every
refusal is named and cited. It runs on its own VM, `haro`.

## Download and use

Release builds for Windows and Linux are on this repository's releases page: https://github.com/mayouni/haro/releases. Each
archive holds the `haro` binary, its LICENSE (MIT) and THIRD-PARTY-NOTICES.txt, with a SHA-256 sum for every archive.

    haro prog.haro                    runs a program
    haro check prog.haro              checks it without running it
    haro check --facts prog.haro      prints what the checker establishes, per function, as JSON

## Building it

    python paths.py                                                     what this checkout runs on
    cd vm && zig build -Doptimize=ReleaseFast -j2                       the Haro VM            vm/zig-out/bin/haro.exe
    cd vm && zig build -Doptimize=ReleaseSafe -j2 -p zig-out-safe       its checked build      vm/zig-out-safe/bin/haro.exe
    python spike/haro_forge.py                                          the guard: every rung's court on both builds (55 stages)
    python spike/haro_forge.py --stage=N                                one stage
    python spike/haro_forge.py --plant                                  must FAIL: a check that cannot fail is no check
    python release/build_release.py windows | linux | macos             a release archive

Every court runs on the VM and on its checked build, and the two must print the same bytes. Every rung's fixtures are written
before its code, and every protection is switched off in turn to show the court fails without it.

## Where to read

    CLAUDE.md        the brief, and what is where
    CHARTER.md       the charter: the alphabet, the decisions (D1-D63), the amendments
    PRINCIPLES.md    the founding principles;  GRAMMAR-SKETCH.md  the first grammar
    TYPES.md         Haro's types, rung by rung
    SPIKE.md         every rung, one section each, and what comes next
    FINDINGS.md      HF-1 to HF-157, each one measured
    CODEGRAPH.md     the code-graph memo;  BLOCKS.md  one format and pattern rules
    vm/NOTES.md      the VM and its compiler
    spike/           the meta-court, the forge, the courts, each rung's fixtures and grammar
    study/           the measurements behind the memos
    release/         the release builds, their licence and their acceptance

Haro is a Softanza project: https://mayouni.github.io/stzsite/
