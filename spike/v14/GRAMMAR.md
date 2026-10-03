# Haro v0.14 -- a court that collects

**Written after `multi_cases.json` and the five multi-defect sentences beside it, which are
the judge** (the W discipline: sentences and predictions first, prose second). v0.14 grows no
clause: the declaring altitude is v0.13's, unchanged, and refuses nothing it accepted. What
grows is what a forged court does with a sentence that is wrong in more than one place. The
Diagnostic Contract (C2 v1.2.0, `stzzui/doc/diagnostic-contract.md`) carries `diagnostics` as
an array and says nothing of its length; v0.11 filled it with at most one error, because every
court stopped at its first refusal. A person fixing a workflow wants all of them at once, and
the shipped court already gives them: RingFlex's `Check()` runs six passes (names, actors, step
bodies, references, reachability, unused) and returns every finding.

## What changes

```
<lang>_court.ring diagnose <file> [<world.json>]    every finding, in the order of the file
<lang>_court.ring check    <file> [<world.json>]    the first refusal, one line, to the byte -- unchanged
```

**The rule, in one sentence: a pass that meets a refusal notes it and goes on to the next
element.** Inside the court it is one function, `CtNote`, and a `try` at each site that raises:
out of collect mode `CtNote` raises the same string again with the same code and cites in the
same globals, so `check` and every other verb are what they were; in collect mode it records
`[code, cites, line, message]` and the pass resumes. `diagnose` sorts what was recorded by
line, ties in the order they were met, and answers it as the contract's one object.

| the pass | what it collects |
|---|---|
| one namespace | the first duplicate of each declaration |
| shapes | each clause with the wrong shape; the declaration is then **broken** and the passes that read its values say nothing more about it, as a condition that reads through an unresolved reference says nothing |
| required seats | each missing seat, with its own message and code |
| the WORLD's cardinality | each ONE kind not exactly once, and the FIRST kind not first |
| names, then local values | each declaration's name, then each clause that fails its menu, range, format or union |
| constraints | each declaration each constraint refuses |
| references | each reference that resolves to nothing |
| the algorithm's step tree, the FORMS | the first cycle; each family offering a form the FORMS does not declare |
| the symbols | each symbol seat the handed-in world does not hold |

**What stops the run, because there is nothing to resume from:** a sentence that does not
parse. An unknown verb, kind or clause, an unterminated string, an unexpected character and a
declaration with no RATIONALE are refused by the parser before any declaration exists to judge,
and RingFlex does the same (its parser raises; only `Check()` collects). That one finding is
the last and only one. A **SENTENCE seat** is judged by its own court, which does not collect
into the outer's findings: the seat is one finding, saying why.

## Measured

Five sentences with several defects, written with a hand prediction of what a court that
collects must say about each (`v14/multi/`, `v14/multi_cases.json`), each in two notations:
RingFlex's `.wflow` and the Commons' `.f` the forge reads. The guard's stage 17 runs
RingFlex's own court live under official Ring 1.27 on the `.wflow` (`rf_multi.ring`,
read-only), reads both files in Python to name the declaration each finding sits on, and
holds the forged court to the shipped one:

    predictions     4 of 5 were RingFlex's findings exactly; one was corrected after it
                    spoke: C14 is stated twice on a duplicated name, once per kind and once
                    per namespace (src/wflow.ring CheckNames) -- I predicted once
    pairs           the forged court reports every (code, declaration) pair RingFlex
                    reports and none it does not: 11 pairs over 5 sentences; it says 3 of
                    them more often (a missing TIMEOUT and a missing ON_TIMEOUT are two
                    seats under one law, C1) and never fewer times -- with one named
                    exception, C14, stated once for the one namespace
    no cascade      all 24 of RingFlex's original fixtures, every finding and not only the
                    first, give the same (code, declaration) pairs: collecting adds nothing
                    where RingFlex finds one thing
    check           unchanged: one line, the first refusal, one of the findings
    the same bytes  on rnxc and the oracle on every `diagnose` and `check` run

**What the new judge found that 24 single-defect fixtures could not.** A name declared twice
was `DUPLICATE_NAME` in the forged F court and C14 in RingFlex's: no original fixture
exercises C14, so the forged court had never been asked. F now declares that refusal with
RingFlex's code and cite (`f_v13.haro`), and the court passes the refusal's own cites rather
than none. Two more were the guard's own: stage 14 asserted exactly one error per refused
fixture, which was a statement about first-refusal courts and is now "every error carries
RingFlex's code"; and a family offering an undeclared form was refused twice, by the menu that
types the seat and by the FORMS pass behind it -- the second now says nothing the first said.

**What it cost, and how it was paid back.** The collecting sites added 112 lines to
`court_lib.ring`, which every court compiles on every run, and the machine court's cold start
went from 92-96 ms to 99-101 against its pinned 100. The lesson of HF-49 applied again:
`world_lib.ring` now holds the world's functions, loaded only where the language declares a
SYMBOL or a PUBLISH, and a 25-line `world_stub.ring` stands elsewhere -- 121 lines out of
`court_lib.ring` for 25 in. Two clean readings after the move: 95.4 and 95.1 ms.

## What it does not do, named

- **`check`, `narrate` and `refine` stop at the first refusal.** Only `diagnose` collects.
- **The first finding per site.** A seat that fails two ways is one finding; a declaration
  missing two seats is two, because each seat is its own site.
- **Order is the file's, not the passes'.** RingFlex's order is its pass order; C2 specifies
  none, and the file's is the one a person reads down.
- **The meta-court does not collect.** `haro_lib.ring` judges `.haro` files and raises at its
  first refusal; making a declaration's author see every defect at once is its own rung.
- **A broken declaration is silent past its shape.** A clause of the wrong shape ends what
  the value passes say about that declaration; fixing it can reveal findings behind it.
