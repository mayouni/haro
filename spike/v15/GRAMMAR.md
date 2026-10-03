# Haro v0.15 -- the meta-court collects

**Written after `multi_cases.json` and the five hand-made files beside it, which are the
judge of what it must say** (the W discipline: findings first, prose second). v0.15 grows no
clause. v0.14 made every forged court's `diagnose` answer every finding; the court that
judges a LANGUAGE -- `haro.ring`, the meta-court every `.haro` file passes through -- still
stopped at its first refusal, so an author who had mistyped a clause, forgotten a RATIONALE
and named a type that nothing declares learned it one build at a time. v0.15 refuses nothing
v0.14 accepted, and `haro.ring <file>` prints exactly what it printed.

## What changes

```
rnxc haro.ring <file.haro>         the first refusal, one line      -- unchanged to the byte
rnxc haro.ring <file.haro> all     every defect, one line each, in the order of the file
```

`all` prints `haro (line N): message` for each, sorted by line, ties in the order they were
met; a declaration with no defect prints what the default prints, `ok` and its fields. The
rule is one function, `StzuNote`, and a `try` at each element of the declaration loop and of
every whole-file pass: out of collect mode it raises the same string again, so every earlier
verdict is what it was; in collect mode it records the finding and the run goes on to the
next element.

## Three phases, and a barrier

The meta-court does three kinds of work, and the order is the design.

| phase | what it judges | a finding here... |
|---|---|---|
| 1. read and register | each DEFINE parsed, its name entered in the one namespace | is collected; a declaration that did not parse is **broken**, and the court resumes at the next DEFINE |
| 2. resolve | every seat's type, the list forms, the unions' shapes, the CODES and MESSAGES seats, the voice and the forms | is collected, except what is an echo (below) |
| 3. relate | sentences, views, constraints, walks, the ask, the run, the refinement points, the world | is judged **only if phases 1 and 2 found nothing** |

**The barrier is the point.** A relation between declarations is undefined while one of them
is not there to relate: a view that reads through a seat whose type resolved to nothing, a
constraint on a declaration that did not read, a walk over steps one of which was refused --
what the court would say of each is an echo of the defect already found, not a second defect.
Collected naively these were 49 of the first 70 mutation runs: one unknown clause on one
declaration drew eight further findings from the views and constraints that named it. The
parser and the checker of RingFlex stand on the same barrier (its parser raises; `Check()`
collects only after it), and so does every compiler that refuses to report type errors on a
file it could not parse. The cost is that an author sees the relational defects after the
first two phases are clean -- one round later, which is what they cost today.

**Inside the first two phases, the same principle at the grain of a seat.** A finding is an
echo, and says nothing, when it is about something already refused:

- it **quotes the name of a declaration that did not read** (`seat type 'a' resolves to nothing`
  when `a` had an unknown clause);
- it is about a **declaration whose own seat types did not resolve** (MESSAGES on a seat whose
  type is nowhere is neither a reference seat nor a plain one -- the court has not yet said
  what it is);
- it is about a **seat typed by a FORM whose own seats did not resolve** (the list-of-a-FORM
  check, the MESSAGES check). A seat typed by a declaration that did not READ needs no check
  of its own: that name is not declared, so the finding about the seat quotes it and falls
  under the first bullet.

A name declared twice is the one refusal that breaks nothing: the first declaration of that
name is sound, and the second is simply refused.

## Measured

The judge is the court's own first refusal, one defect at a time (`haro_mutate.py`). Five
operators put a defect of a known kind into a sound declaration without moving a line: an
unknown clause, a missing RATIONALE, a name taken by an earlier declaration, a seat typed by
a name nothing declares, a constraint on a kind nothing declares. The law:

    one defect         the court that collects gives exactly the one line the default
                       gives for it -- nothing echoing it
    several defects    on different declarations, exactly the union of their single lines;
                       when any defect of phase 1 or 2 is present, the relational ones wait
    a sound file       prints what the default prints

Applied to the real declarations of the letters -- F, Z, A, the machine, the forms, W and the
fleet -- over ten seeds in exploration with eight mutations per operator, **zero differences**
on the final code; before the protections above, 49 in the first pass and still 5 after the
barrier. Stage 18 pins one seed at eight per operator on both runtimes -- 183 single defects
and 116 combinations of two to four, floors pinned at 165 and 100 so a stage that checks
nothing cannot pass -- plus five files whose findings were written by hand (`multi_cases.json`: an unknown clause, a seat typed by nothing,
a missing RATIONALE and a name twice, with a seat typed by the broken declaration saying
nothing; one defect with a form, a seat, a constraint and a sound declaration all naming it,
saying nothing; the barrier; two relational defects both reported; a sound file).

**Each protection was proved load-bearing by switching it off** under the stage's own sampling
-- the stage fails, naming what echoed. Six are: the barrier, the memory of a declaration whose
types did not resolve, the quote-based silence, the seat check on a FORM that did not
resolve, the memory of that FORM, and the MESSAGES-pass skip. **Two were not, and were
removed**: registering a broken name as declared -- the first thought, which no law needed
once the findings that quote it are silent -- and the seat check for a declaration that did
not read, which mattered only while the first existed. The seeds were chosen for it: at four
mutations per operator the second never mattered in eight seeds, at eight per operator seed 1
makes all six matter.

**Two findings that are not the court's.** `haro.ring`'s own top level named a variable `cErr`,
and on the oracle a bare assignment in a function to a name that exists as a global writes
the GLOBAL -- so `StzuDeclare`'s own `cErr` leaked into the top level's and the oracle printed
a finding twice that `rnxc` printed once. The branch is a function now, with names no
script-level variable has: C-2's own trap, met from the other side, and found only because the
stage runs both runtimes. And a mutation helper's pattern, written in a heredoc, held two
backspace characters where `\b` was meant, so the relational operator matched nothing and the
exploration reported "0 problems" over a population with no relational defects in it -- the
list of operators it printed beside the count is what gave it away.

## What it does not do, named

- **The tokenizer is not resumable.** An unterminated string or a character the grammar does
  not have is refused before any declaration exists, and ends the run, as in RingFlex.
- **The first declaration unreadable ends the run.** With no LANGUAGE there is nothing to
  judge the rest by.
- **A SENTENCE seat's file is judged by its own meta-court run,** which does not collect into
  this file's findings; the seat is one finding, and it is a phase-3 one.
- **The echo rules are textual in one place:** a finding that quotes a broken name in single
  quotes. A message that mentions the name any other way would not be silenced -- no
  mutation in the sample found one, and the stage is what would.
