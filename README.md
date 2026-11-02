# Haro

Haro is the foundational language of the Softanza project: a closed, judged family of grammars in which a world is declared,
constrained, asked, moved, stepped and spoken to. Every sentence is judged by a court generated from its declaration, and every
refusal is named and cited. It runs on the Ring++ VM.

**This repository is private.** Nothing in it is published until its author says so.

## This repository, and the Ring++ it runs on

Haro grew inside Ring++, in the folder `haro/` on branch `next` of github.com/mayouni/rnx-spike, from 2026-09-26. It moved here on
2026-11-02 with its history: a file that was `haro/X` there is `X` here, and records written before the move still name it that way.
Its courts are Ring code. Each runs on `rnxc` (Ring++) and on the oracle (Ring++'s own build of Ring 1.27's VM), and the two must print
the same bytes. Both binaries come from a Ring++ checkout beside this one (`..\ringpp`).

    python spike/haro_forge.py             the guard: every rung's court, on both runtimes (34 stages)
    python spike/haro_forge.py --stage=N   one stage
    python spike/haro_forge.py --plant     must FAIL: a check that cannot fail is not a check

STANDALONE.md explains how this checkout finds Ring++, and what still has to change for it to do so.

## Where to read

    CHARTER.md       the charter: the alphabet, the decisions (D1-D38), the amendments
    PRINCIPLES.md    the founding principles;  GRAMMAR-SKETCH.md  the first grammar
    SPIKE.md         every rung, one section each, and what comes next
    FINDINGS.md      HF-1 to HF-133, each one measured
    CODEGRAPH.md     the code-graph memo;  BLOCKS.md  one format and pattern rules (REBOL-06/07)
    FROM-RINGPP.md   what Ring++ handed over
    spike/           the meta-court, the forge, the courts, each rung's fixtures (written first) and grammar
    study/           the measurements behind the memos
