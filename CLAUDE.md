# Haro

**Haro is the foundational language of the Softanza project: the language of languages** (Ringua realised) -- a closed, judged
grammar family in which a world is declared, constrained, asked, moved, stepped and spoken to (the alphabet Z W Q F A N), every
sentence judged by a court the forge emits from its declaration, every refusal named and cited, refinement the change model at
every altitude. It runs on its own VM, `haro`. This file is the whole brief for an AI session working here; `CHARTER.md` is the law.

**PRIVATE.** This repository (`github.com/mayouni/haro`, private) is never made public, and nothing of it is published, until the
author says so. Haro's announcement is his to write and send.

---

## The cut -- 2026-11-02

Haro grew inside Ring++'s repository (under `haro/` on its private branch `next`) from the charter's v0.1 (2026-09-26) to v0.28. On
2026-11-02, at the author's word, it **cut with the Ring legacy**:

- **its own repository**, this one, its 152 commits of history kept (`git subtree split`);
- **its own VM and compiler**, `haro`, in `vm/` -- forked from Ring++'s technology at ringpp 2ea38fd, Haro's from then (D39);
- **every source file `.haro`**, declarations and code alike; a declaration's first word is DEFINE (D40);
- **no Ring in its courts**: every court runs on `haro` and on its own CHECKED build, and the two must print the same bytes (D41).

Ring++ (`D:\GitHub\ringpp`) is now only the **bridge** that keeps Softanza's legacy Ring code running. Haro reaches it for one thing:
what drives Softanza (its library, its engine, the local models) runs on Ring++'s package, named as such. **Records written before
the cut say `haro/X`, `X.ring`, `rnxc` and "the oracle"**: read them as this repository's `X`, `X.haro`, `haro`, and -- for a judge
-- "the checked build". `SPIKE.md`'s section "The cut" has the proof.

## What is where -- `python paths.py` says it for this checkout

    paths.py         one place for where things are; every script asks it, none climbs out of the repository
    vm/              the Haro VM and compiler: zig build -Doptimize=ReleaseFast -j2              -> vm/zig-out/bin/haro.exe
                     and its checked build:  zig build -Doptimize=ReleaseSafe -j2 -p zig-out-safe -> vm/zig-out-safe/bin/haro.exe
                     (one heavy job each: the grammar's parser is 21 MB of C). vm/NOTES.md: what the fork kept and why
    spike/           the meta-court (haro.haro, haro_lib.haro), the forge (forge.haro), the libraries, the forged courts and grammars,
                     the letters' declarations (*_vNN.haro) and sentences, and vNN/ per rung: fixtures.json (written FIRST),
                     GRAMMAR.md (prose second), court cases. spike/haro_forge.py is THE GUARD: 34 stages, --stage=N runs one,
                     --plant must fail it. spike/f/ringflex_record.json: RingFlex's own court's answers, recorded (D41)
    study/           the measurements behind design memos (codegraph, phase15, rebol). Studies and probes OF Ring keep Ring 1.27 as
                     their subject (paths.RING_ORACLE), never as a judge
    runtime/         gitignored: what runs write (the second judge's forge folder, scratch)

The records: `CHARTER.md` (section 13 the decisions, D1 to D41; section 15 the v0.3 amendments), `PRINCIPLES.md`,
`GRAMMAR-SKETCH.md`, `FINDINGS.md` (HF-1 to HF-134, each measured), `SPIKE.md` (every rung, one section each, and "Next"),
`CODEGRAPH.md` (the code-graph memo), `BLOCKS.md` (one format and pattern rules, REBOL-06/07: its four questions RULED 2026-11-02),
`FROM-RINGPP.md`.

## The neighbours

| | where | what Haro takes from it |
|---|---|---|
| **Ring++** | `D:\GitHub\ringpp` (branch `next`, remote `private` = mayouni/rnx-spike) | the bridge to Softanza's legacy code: its package (`runtime\package\ringpp-win64`) runs what loads Softanza. Its gate reads Haro's v18 printer from THIS checkout (`..\haro`): never move `spike\v18` |
| **Softanza** | `D:\GitHub\stzlib` (worktrees `D:\GitHub\_w*`) | the estate courts are judged against; read-only unless the author says otherwise |
| **HaroServer** | `D:\GitHub\haroserver` (private) | nothing: Haro's server counterpart, on Ring++'s resident VM today |
| **the journal** | `D:\GitHub\softanza` | `mailbox/haro-charter.md` (this desk's mailbox: read it first, answer in it), `memos/<date>.md` (every substantive answer filed as a yaml memo) |
| **the constitution desk** | its own worktree of THIS repository, `D:\GitHub\_hwc`, branch `constitution` | works on Haro too (Zin's articles and weaves; v0.23 to v0.27, and v0.29). The two desks never work in one checkout; fetch and rebase before landing |

## How work is done here

- **Fixtures first, prose second.** A rung's fixtures are committed before any court code; a fixture changed after the court spoke
  is said so in the account, never silently.
- **Every protection load-bearing.** Switch each one off in turn; the guard must fail for the fixture it exists for.
- **Both builds, the same bytes.** A court runs on `haro` and on its checked build; any difference fails the guard.
- **One exact spelling, least authority, refuse loudly** -- and name what is refused. A divergence is a decision, recorded as a D-entry.
- **Decisions**: the author rules; on his delegation the desk rules and records it as delegated. Never present a delegated
  reading as his own.
- **Measure, never assert**; two significant figures; minima over repetitions; state the pattern a change hurts.
- **The machine**: one heavy job at a time; `python D:\GitHub\ringpp\bench\heartbeat.py` before any timing (the CPU is often held at
  20-80% of its rated speed, and stage 6's 100 ms target then fails for every build alike); a long run gets a heartbeat, never a
  silent watch; power cuts are routine -- commit often.
- **Tools**: write scripts with the Write tool -- Bash heredocs strip backslashes; never round-trip text through PowerShell
  Get-Content/Set-Content; every checkout is LF (`.gitattributes`); commit explicit paths, never `git add -A`.
- **Versions**: take the next free version number and say so -- the constitution desk takes them too (it holds v0.29).

## Where it stands -- 2026-11-02, after the cut

- The cut is done and proved (SPIKE.md "The cut"; D39-D41; HF-134).
- **Next, on the author's word as Central relayed it: step 1 of REBOL-06, as v0.30** -- one reader of C6 and a canonical printer,
  under the printing court, as a guard stage (BLOCKS.md section 5; study/rebol/block.py the reference, printing_fixtures.json the
  start). The four questions are ruled: Q-B1 `AS` and `?` recorded in C6 (Ringua writes them); Q-B2 both C6 amendments, yes
  (Ringua writes them; refuse them until its text lands); Q-B3 the block export now, the syntax later; Q-B4 the elders wait for the
  round-trip court.
- Owed (mailbox): Central's items 3 and 4 of 2026-10-31 (a value join -- a case of REBOL-07 -- and a seat shared by ten kinds),
  COMPASS-KERN-03's field check (`spike/ask_lib.haro`), and the constitution desk's ask for a per-seat severity design.
