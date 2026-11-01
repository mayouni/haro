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

**BUILT, the first rung, 2026-10-30 (83ce489), at the author's word.** `rnxc resident <file.ring>...` holds one program
and admits files into it, each whole or not at all. The state between admissions is the compiler's as bytes, so a refused
file costs its own arena and nothing else. A function an admitted file already calls is reached once a later file defines
it. The four refusals are: a statement that does not compile, a function already defined, a class after the first file,
and a new global an admitted function reads as an unassigned local. Measured on the test bed as promised, RingServ's 14
files in its host's order:

- as written, 5 are admitted and 9 refused for their bare globals (Rule A), the program unchanged after each;
- migrated, 14 of 14 are admitted, its own load check passes, and its library prints what Ring prints;
- Softanza's whole library admits as the first file, and a small file after it takes about 150 ms.

The full record is in CLAUDE.md, "THE RESIDENT VM, FIRST RUNG".

**BUILT, the second rung, 2026-10-30 (93d3cab), at the author's word: admission from inside the running program.**
`admitfile(cPath)` and `admitcode(cName, cSource)` take in a file, or source the program built, and the program calls
what they define at once. Code compiled before that function existed reaches it. A refusal raises an error the host
catches, with the program as it was. An admitted top level runs above the caller and its error comes back to the call,
as eval's does. The second rung is the shape of HaroServer's host loop: one live program fed new code by itself.

- Measured: a host program's transcript is pinned, and every line it shares in meaning with Ring's eval(read()) is Ring's.
- Cost: nothing at run time. An admission costs about 2 ms in a small program and about 143 ms with Softanza's
  library inside, so a host that admits per deployment pays it once and one that admits per request pays it each time.

The record is in CLAUDE.md, "THE RESIDENT VM, RUNG 2".

**BUILT, the third rung, 2026-10-30 (0f3eb0b), at the author's word: a running function replaced.** `replacefile(cPath)`,
`replacecode(cName, cSource)` and `rnxc resident --replace <file>`. Every call from then on runs the new body, and the
frames already in the old body finish it. The old body stays in the code, so a running frame is safe. Its call sites, the
running code's included, and its by-name lookups are pointed at the new one.
- Refused: a replacement that changes the parameter count, and one that replaces nothing.
- Redeploy: a file the program holds can be replaced by its path.
- Ring has no answer to compare with (a function defined twice is C22 there), so the transcripts are golden. Four plants
  show each part is needed.
- Cost: none measurable on a plain program. A resident program no longer types a caller from its callee's return, which
  costs 1 to 3%; without that rule a replacement answering another type is unsound.

The record is in CLAUDE.md, "THE RESIDENT VM, RUNG 3".

**BUILT, the fourth rung, 2026-10-31 (d539d05), at the author's word: classes after the first file.**
- **New classes:** a class new to the program is admitted at any time, from a class admitted before it too.
- **Replacing a class:** a class the program holds can be replaced by name. Its objects keep their class and answer with
  the new methods, a `super.M()` included. New objects get the new initial values; old objects keep theirs.
- **Refused:** a replacement that changes what the objects were made for (their attributes, parent, code at `new`, init,
  a parameter count), and a class redefined without the replace verbs (C26).
- **Ring's answer:** it agrees on every line before the first replacement.
- **Cost:** nothing at run time; the VM is unchanged.
- **Not built:** a `new K` compiled before K existed stays R11. A host reaches a later class through eval or a factory
  function.

The record is in CLAUDE.md, "THE RESIDENT VM, RUNG 4".

**BUILT, the fifth rung, 2026-10-31 (148557d), at the author's word: the compiler kept alive between admissions.**
- **What changed:** the program stays in one compiler between admissions instead of being saved to bytes and restored. A
  refused admission is undone in place. The VM's tables grow by what each admission adds instead of being rebuilt.
- **Measured:** a small admission into Softanza's library (49,009 functions) takes 0.6 to 1.4 ms, against about 150 to
  200 ms before, so a host can admit code per request.
- **Proved two ways, on every transcript of the guard:**
  - a refused admission leaves the program byte for byte as it was, and an admitted one leaves the VM the tables a whole
    build gives;
  - the old saved-bytes path prints the same.
  - Eight plants show each part is needed.
- **Cost:** nothing for a plain program (176 programs compile to the same bytes).
- **Still paid per admission:** a new class (its tables rebuilt, about 90 ms at that size), a replacement (every earlier
  call site walked), and about a millisecond per new global. **Made cheap the same day** (4d533d7): the class tables grow
  in place, about 1 ms a class and 2 ms a class replacement; a function replacement about 1.3 ms; such a global about
  1 ms. A method `addmethod` attached at run time now survives later class admissions. The resident VM runs on Linux:
  its guard passes 18 of 18 there. The install and both packages carry it (2f34bea).

The record is in CLAUDE.md, "THE RESIDENT VM, RUNG 5". **Next on this road:** HaroServer's host loop itself, on these five
rungs. Running it will show what is still missing rather than guessing:
- whether code admitted per request must also be released (a program only grows today);
- whether objects must move to a class's new layout when an app adds an attribute while it runs.

**BUILT, HaroServer's first build, 2026-10-31 (bd38342), at the author's word: the host loop on the resident VM**
(`haro/serv/`, with its README).
- **What it is:** the loop is the program's own, under `rnxc resident`. It waits for a request, routes it to the
  function an app registered, and answers. A deployment is a request too (`POST /admit/<app>`, `POST /replace/<app>`).
  The socket under it is eight rnxc natives (`src/httpd.zig`), part of the one binary.
- **Its court:** 22 checks (23 with Softanza's library loaded into the running server), on Windows and Linux; in the
  gate.
- **Measured:** about 5,000 to 7,800 requests a second, a new connection each, p50 0.12-0.18 ms. Code admitted with a
  request costs 0.3 ms in a small program and 0.9 ms with Softanza inside.
- **What running it answered:**
  - Code admitted per request is never released: about 22 KB a function, for good.
  - Every app shares one namespace: Softanza's `echo` refused an app's `Echo`.
  - An attribute added to a live class is refused, and a real app wants it.
  - A large deployment blocks the loop while it compiles (Softanza's library: 13.8 s).

**Next on this road:** RELEASE -- an admission whose functions are dropped when the request that brought them is done,
or a request's code compiled and run without being admitted. It is the one finding that grows without bound; the
namespace question is Haro's language decision (packages), and moving objects to a new layout waits for an app that
needs it.

**BUILT, rung 6 of the resident VM, 2026-10-31 (71dd019), at the author's word ("go ahead with release"): RELEASE.**
- **What it is:** `releasefile` / `releasecode` (and the driver's `--release`) undo the program's LAST admission -- its
  functions, globals, constants, names and code -- leaving the program byte for byte as it was before it. A stack: only
  the last. Refused: code that defined a class or a lambda, a replacement, a function a class reaches through
  `addmethod`, and while a frame of it runs. What the host kept from it (a reply, a literal) outlives it.
- **HaroServer's `POST /run`:** a request's code admitted, called and released before the reply. 3,000 runs each
  answering with a 16 KB literal of its own released code: the program keeps its size, private memory stays between
  36 and 53 MB, p50 0.6-0.7 ms a run. At Softanza's size a release costs at most 0.01 ms.
- **Found on the way and fixed:** a global admitted after a release read the released one's value; an `addmethod` cell
  for a released name answered for the next name at its index; the arena's 64 MB slack let a small server climb 64 MB
  before compacting (now 16 MB).

**Next on this road:** objects moved to a class's new layout -- an app that adds an attribute to a live class
(`tally_v3.ring`) is the last refusal a running app meets in the court. The namespace question stays the author's
language decision (packages), and a large deployment blocking the loop waits for a server that deploys at that size.

**BUILT, rung 7, 2026-10-31 (16920ec), at the author's word: a class gains attributes while its objects exist.**
- **What it is:** a replacement may add attributes after the ones the class's objects hold. Each object made before
  takes them at its first access past its own slots, starting as declared (a constant; a list a list of its own). The
  replacement walks nothing; an object's first access costs about 55 ns more, once.
- **Refused, with the reason:** an attribute dropped or reordered, a starting value that runs code, region code that
  uses the added attribute, and a class another class the program holds inherits from.
- **HaroServer:** `tally_v3.ring` is admitted now; the running tally keeps its total and counts the new attribute from 0.

**Next on this road:** a `new K` compiled before K was admitted reaching K once it is -- the late link rung 1 gave
functions, given to classes. Today a host can make an admitted class's objects only through a function the class's file
defines, the one friction every HaroServer app still meets. The namespace question stays the author's language decision.

**BUILT, rung 8, 2026-11-01 (1c35218), at the author's word: the late `new`.**
- **What it is:** a `new K` compiled before any admission defined K finds K by name once one does, as Ring does: R11
  naming it until then, then its initial values, `init` with its arguments, a brace, a class replaced since (its new
  initial values) -- in a resident program; a plain one compiles exactly as before.
- **One divergence, loud:** in `new K { ... }` of a class not yet held, a bare name the class lacks is R12, where Ring
  makes a variable.
- **HaroServer:** `apps/ledger.ring`'s handler makes `new Entry(...)` before `apps/entry.ring` is deployed: 500 and R11
  until then, 200 after, from the same handler.

**Next on this road:** the install and both packages carry rungs 1-5 only (2f34bea) -- rungs 6-8 and HaroServer's natives
reach the desks with a re-lay, at the author's word. The namespace question stays his language decision.
**RE-LAID 2026-11-01 at his word:** `D:\ringpp\ringpp-win64` and both packages carry 1c35218 -- every resident rung and
HaroServer's natives; the fingerprint `D:\rpp-pkgtest\prog\resident_fp2.ring` tells them from the build before.
**PUBLISHED the same day as release v2.0.8** (public main be4575f): the downloads carry `rnxc resident` and the
`rpp_http_*` natives, both archives tested as shipped. The notes describe them without naming Haro.

**DECIDED 2026-11-01, on the author's delegation: the namespace question (D31).** Each app admitted into HaroServer is a
namespace of its own -- its names first, then the base, and another app only through what it exports, spelt
`ledger.Entry`. **BUILT the same day** ("go ahead with building D31"): `admitapp(cApp, cSource, aExports)` and
`replaceapp`; HaroServer deploys every app into its own namespace and shared code into the base (`POST /base/<name>`).
Limits named: an app's top level, lambdas and eval resolve a name given by string as the base does; an app's admission
is not released.

**BUILT 2026-11-01, rung 9 of the resident VM, at the author's word ("go ahead with the large deployment blocking the
loop"): an admission compiled in the background.** `admitstart(cVerb, ...)` starts any of the six admission verbs'
compile on a thread of its own and returns; `admitstate([nWaitMs])` says "compiling" or "compiled"; `admitfinish()`
installs it where the call stands -- the same admission the verb makes, refused as it would refuse. HaroServer deploys
everything that way: Softanza's library compiled while the loop answered 67,760 requests, the longest waiting 114 ms
(the install and the library's top level, on the program's thread), where the whole 13.8 s compile was a pause before.
One compiles at a time; HaroServer queues the rest and answers `/run` 503 meanwhile.

**The alternative, if the author prefers the language side first:** the library derivation of rung 5 (body kinds refine a
program, not a library, HF-103), or opening Z's route 3 (a runtime for a declared world, CHARTER section 3, HF-45). Both
are recorded where they were found.
