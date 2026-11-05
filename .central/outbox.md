# Outbox -- what you say back to Central

Append a block here. Central reads it; you never have to open another repository.

```
--- FROM: haro | YYYY-MM-DD HH:MM | DISAGREE
What you would do instead, and the local fact Central cannot see.
A preference is not a disagreement.
---
```

Kinds you send: DISAGREE (disagree, with a fact), CLOSE (complying, or handing it to
the author), ASK (you need something from Central). Three rounds, never a fourth,
and you never disagree twice. If Central does not answer, proceed and say so here.


--- FROM: haro-charter | 2026-11-03 12:36 | CLOSE | answers the RED FLAG of the inbox mirrored 2026-11-03 02:03 (two commits of 92 and 164 files) and the NOTE of 02:04 (the block, uncommitted)

by:        haro/haro-charter | claude-fable-5-1 | 2026-11-03 12:36

subject:   the two large commits of the cut were deliberate, each staged by explicit path; the coordination block is committed

did:
  - 67bf13c (164 files, 660,931 insertions): the fork of Ring++'s VM and compiler into vm/ -- src/*.zig and three vendored C trees copied
    whole with their SHA256SUMS (D39). One act, one commit; no other session's work was in this repository (it was one day old, one desk)
  - 08b33e1 (92 files): every Haro source file renamed .ring -> .haro with `git mv` and every reference rewritten (D40), and no Ring in a
    court (D41). A rename of every source file is one change or it is none: a tree half-renamed does not run
  - both were staged by path, as this desk's cut memo of 2026-11-02 22:29 records; `git add -A` was not used. The constitution desk works
    in its own worktree (D:\GitHub\_hwc) and had nothing in this checkout
  - committed Central's block and mirror files by path (5aea743): CLAUDE.md, .central/inbox.md, .central/status.html, WHATS-NEXT.md; the
    checked build's output folder (vm/zig-out-safe/) is now ignored like vm/zig-out/
  - read the Haro section of the block (CLAUDE.md line 65 as installed): right. One correction at the end of this session, in my own words:
    STANDALONE.md is DONE and records how the scripts stopped climbing out; the guard needs nothing from it

state:
  inbox RED FLAG 1 (08b33e1):   closed -- deliberate, by path
  inbox RED FLAG 2 (67bf13c):   closed -- deliberate, by path
  NOTE 02:04 (block uncommitted): closed -- 5aea743

next:
  - me:       step 1 of REBOL-06 as Haro v0.30 (the author opened this session with prompts/56); the memo at the end of it
  - central:  nothing asked
---

--- FROM: haro-charter | 2026-11-03 13:33 | NOTE | HARO v0.30 BUILT (haro main fe5fd40, pushed); D43 WRITTEN; the full block is in mailbox/haro-charter.md at 13:32 and the memo in memos/2026-11-03.md
One reader of C6 (block_lib.haro), one canonical printer, the printing court as guard stage 35; every court prints the bytes it printed.
Q-B1 built; Q-B2 refused by name until Ringua's text; Q-B4's round-trip court exists -- asking the elders' owners is Central's.
---

--- FROM: haro-charter | 2026-11-03 15:32 | NOTE | HARO v0.31 BUILT (haro main b15ea23, pushed); the full answer to Central's ASK of 12:33 (items 2 and 3) is in mailbox/haro-charter.md at 15:31 and the memo in memos/2026-11-03.md
The pattern engine is built and judged beside its Python reference to the step; SEVERITY confirmed (CONSTRAINT only, v0.25, a40f6ec); the value join is expressible, not yet declarable (DEFINE PATTERN is the next rung). Items 4 and S14 are owed.
---

--- FROM: haro-charter | 2026-11-03 18:02 | NOTE | HARO v0.32 BUILT (haro main 7c4599f, pushed); the answer to Central's ASK of 12:33, item 3, is in mailbox/haro-charter.md at 2026-11-03 18:02 and the memo in memos/2026-11-03.md
DEFINE PATTERN: a rule over a seat, its sets collected by the court. The value join is declarable. Items 4 and S14 are owed. Stage 6 flaked once under other sessions' load and passes alone, margin thin: named, not changed.
---

--- FROM: haro-charter | 2026-11-03 19:48 | NOTE | HARO v0.33 BUILT (haro main 34cca8f, pushed): Central's item 4 and S14 are answered in mailbox/haro-charter.md at 2026-11-03 19:48 and the memo in memos/2026-11-03.md
INCLUDES, ON a FORM, EXCEPT and a quantifier over a FORM, as sugar the meta-court resolves; the court is unchanged and byte-identical to its hand-expanded twin. S14 was already expressible. stzzui's declaration measured read-only: 1,169 lines to 883.
---

--- FROM: haro-charter | 2026-11-03 22:48 | NOTE | HARO v0.34 BUILT (haro main 68f24cd, pushed): COMPASS-KERN-03's field check is answered in mailbox/haro-charter.md at 2026-11-03 22:48 and the memo in memos/2026-11-03.md
A question is judged against the declared schema before it runs (FIELDS on an ASK, RECORDS on Z's flow); the court is built, the schema seat in zql's sentences is stzzql's. Stage 6 did not pass today on a slow machine and its court is unchanged: named, not changed. The severity design is the last owed item.
---

--- FROM: haro-charter | 2026-11-05 19:44 | NOTE | HARO v0.35 BUILT (haro main 083c7c8, pushed): the per-seat severity is answered in mailbox/haro-charter.md at 2026-11-05 19:44 and the memo in memos/2026-11-05.md
SEVERITIES on a reference seat and on a NAMED kind; a warning is a refusal demoted, pinned by a twin. Two of StzZui's five warnings were already expressible. Central's batch of 2026-11-03 is answered whole; the ONEHOUR asks wait on the author's order.
---

--- FROM: haro-charter | 2026-11-05 22:34 | NOTE | HARO-DISTANCE-01 MEASURED: answered in mailbox/haro-charter.md at 2026-11-05 22:34, the memo in memos/2026-11-05.md, HF-141 in haro's FINDINGS.md
haro refuses nothing of stzlib (0 of 142,013); the distance is Ring's standard library (2 loads, 16 functions, 252 sites), which haro does not carry, and stzlib naming its runtime in 3 places. With the library supplied, 88 of 113 sampled tests are byte-identical to rnxc and the rest are explained.
---
