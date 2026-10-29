# From Ring++ to Haro -- the handoff of 2026-10-29

Ring++ was the bridge: carry Softanza and the customers on it off Ring, onto a runtime whose every decision sits in this
repository. On 2026-10-29 the last span of it was laid. This page says what Haro now stands on, what the bridge still owes,
and the first step I recommend for Haro. It rules nothing: the road is the author's.

## What Haro stands on, measured

    the runtime      rnx and rnxc, one Zig binary; the compiler is the checker; Ring 1.27 built from its own source stays in
                     ringpp as the reference only (the oracle), never shipped
    the estate       stzlib MAIN is written for Ring++ (Rule A, c08d12dd0, fast-forwarded 2026-10-29 under RINGPP-RULEA-01;
                     the three Linux load spellings 0950e246a): 136,346 statements in 697 files, every one compiled; 30 of its
                     narrated tests print the same before and after on Ring 1.27 itself (695 checks), so the move cost a program
                     still on Ring nothing
    the engine       main's own engine built for Ring++ (bench/engine_copy.py, runtime/engine-main): 89 domains on Windows, 87 on
                     Linux, every one ABI 3 (one handle table in the host, generation-checked)
    the release      Ring++ v2.0.5, both packages laid from main and tested as shipped (relocated, a bare PATH, an empty cache);
                     D:\ringpp\ringpp-win64 is that package, the copy every desk runs its guards with
    the tools Haro   rnxc graph (the resolved call graph), rnxc dump --json (the lossless tree), rnxc fmt (the canonical text),
      already uses   rnxc check, rnxc census, rnxc migrate (every Rule A site, n++ and add/insert/del included since today)
    the site         mayouni.github.io/ringpp says "the runtime that replaces Ring", with a page for moving a Ring program

What Ring is still used for, and why: RingServ, RingScript and MicroRing are hosts built on Ring's own VM, kept as test
beds and as the bases of Haro's server, browser and embedded runtimes (his decision of 2026-10-14); ringupstream is the
record of upstream. Everything else was handed to its own session on 2026-10-29: the Softanza site (its start page still
said "get Ring 1.27", its build ran examples with `ring`), the two books' runner, RingFace's pinned runtime; and through
central, stzlib's handoff notes and the `stz` experiment's engine build. The machine's PATH still holds D:\Ring127\bin --
a system setting, the author's to remove.

## What the bridge still owes -- done only when Softanza-shaped code meets it

Ring++ is not re-proved for its own sake (memory `ringpp-is-a-bridge-focus-haro`). These are named so that the day one of
them is met, it is a known item and not a hunt:

    F-140            `a and b = c` as a statement assigns on Ring, compares here -- no estate site
    `not o`          on an object Ring calls operator("not"); rnxc does not
    the readers      rnxc shadows / migrate / attrs still read F-138's misparsed assignment as a comparison
    the figure       the published parity (12,924 of 13,008) was measured on the BRANCH; main has not had the wide pass
    stzlib's build   main has not taken the Linux portability patch (bench/engine_linux_portability.patch) nor the libcurl
                     layout for Linux; 55 loads in its test folders name a file in another case (bench/load_case.py --tests)
    the clock copy   still carries ABI 2 libraries (clock34.py --copy takes the new ones)

## The step I recommend first: a resident VM that takes new definitions

**What it is.** rnx today compiles a whole program, freezes it and runs it; eval compiles a statement into the running
frame (F-72, F-107) but cannot add a function or a class. Haro needs the general form: a running program that accepts new
source -- functions, classes, globals -- into the program it already holds, checked by the compiler before it is admitted,
without a restart.

**Why it comes first.**
1. It is what HaroServer needs, measured rather than guessed: RingServ's design is exactly one resident VM fed new code
   (CLAUDE.md, "RINGSERV ON RING++": every app arrives as an eval that DEFINES functions and classes). The lesson is
   recorded; the capability is not built.
2. It closes rung 5's loop. Refinement admits a body through the gate (D27 to D30); today the admitted body is judged and
   then compiled into a fresh program. Admitted into the running one, a refinement becomes a change to a live system, which
   is what the charter's refinement model (section 6) describes.
3. Most of it is already in the VM: the eval compiler runs inside it against the caller's frame, `VM.dyn` holds names an
   eval makes, the image and the prefix already know how to carry a compiled library and compile a root on top of it.
   What is missing is growing the frozen tables -- functions, the dispatch table, classes -- and the checks that a new
   definition cannot change the meaning of code already running.
4. It is measurable from the first day: the RingServ test bed's 14 library files go in one by one and must define their
   functions; a refused definition must leave the running program exactly as it was.

**What it costs, named before it is started:** the frozen-table assumption is everywhere in the VM (a method's slot, a
class's layout, a function's index are fixed after the freeze), so the first rung should admit new FUNCTIONS only, and new
classes after; and every admission is a compile, so its time is the census's per-file time, not an eval's.

**The alternative, if the author prefers the language side first:** the library derivation of rung 5 (body kinds refine a
program, not a library, HF-103), or opening Z's route 3 (a runtime for a declared world, CHARTER section 3, HF-45). Both
are recorded where they were found.
