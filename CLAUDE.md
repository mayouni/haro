# Haro

**Haro is the foundational language of the Softanza project: the language of languages** (Ringua realised) -- a closed, judged
grammar family in which a world is declared, constrained, asked, moved, stepped and spoken to (the alphabet Z W Q F A N), every
sentence judged by a court the forge emits from its declaration, every refusal named and cited, refinement the change model at
every altitude. It runs on the Ring++ VM. This file is the whole brief for an AI session working here; `CHARTER.md` is the law.

**PRIVATE.** This repository (`github.com/mayouni/haro`, private) is never made public, and nothing of it is published, until the
author says so. Haro's announcement is his to write and send.

---

## Where it came from -- 2026-11-02

Haro grew inside Ring++'s repository, under `haro/` on branch `next` (pushed only to `mayouni/rnx-spike`), from the charter's v0.1
(2026-09-26) to v0.28 (2026-11-02). At the author's word it moved here, its history kept (`git subtree split --prefix=haro`), so the
files that were `haro/X` in Ring++ are `X` here. **Every path in the records written before the move says `haro/...`; read it as this
repository's root.** Ring++ keeps no copy: its gate reads Haro from a checkout beside it (`../haro`, or `HARO=`).

## The repositories around it

| | where | what Haro takes from it |
|---|---|---|
| **Ring++** | `D:\GitHub\ringpp`, branch `next`, remote `private` = `mayouni/rnx-spike` | `rnxc` (`zig-out\bin\rnxc.exe`), the ORACLE (`runtime\win64\ring.exe`, Ring 1.27's VM built from vendored source), the probes in `bench\exec`. Ring++'s `CLAUDE.md` is its brief |
| **the install** | `D:\ringpp\ringpp-win64` | a released `rnxc` with Softanza and its engine laid beside it |
| **HaroServer** | `D:\GitHub\haroserver`, `mayouni/haroserver` (private) | nothing: it runs on Ring++'s resident VM and is Haro's server counterpart |
| **Softanza** | `D:\GitHub\stzlib` (and worktrees under `D:\GitHub\_w*`) | the estate courts are judged against, read-only unless the author says otherwise |
| **the journal** | `D:\GitHub\softanza` | `mailbox/haro-charter.md` (this desk's mailbox: read it first, answer in it), `memos/<date>.md` (every substantive answer filed as a yaml memo) |

## The records

- `CHARTER.md` -- the charter (v0.2 ratified 2026-10-01; section 13 the decisions, D1 to D38; section 15 the v0.3 amendments).
- `PRINCIPLES.md`, `GRAMMAR-SKETCH.md` -- the founding design.
- `FINDINGS.md` -- HF-1 to HF-133, each measured.
- `SPIKE.md` -- every rung, one section each, and "Next, in the order the charter gives".
- `CODEGRAPH.md` -- the code-graph memo (rungs 1 to 7 built). `BLOCKS.md` -- the one-format and pattern-rules memo (REBOL-06 and 07, 2026-11-02).
- `FROM-RINGPP.md` -- what Ring++ handed over.
- `spike/` -- the meta-court (`haro.ring`, `haro_lib.ring`), the forge (`forge.ring`), the forged courts and grammars, the letters'
  declarations (`*_vNN.haro`) and sentences, and `vNN/` per rung: `fixtures.json` (written FIRST), `GRAMMAR.md` (prose second),
  court cases. `spike/haro_forge.py` is THE GUARD: 34 stages, `--stage=N` runs one, `--plant` must fail it.
- `study/` -- measurements behind design memos (codegraph, phase15, rebol).

## How work is done here

- **Fixtures first, prose second.** A rung's fixtures are committed before any court code; a fixture changed after the court spoke
  is said so in the account (and in the fixture's name), never silently.
- **Every protection load-bearing.** Switch each one off in turn; the guard must fail for the fixture it exists for.
- **Both runtimes.** A court is Ring code, run on rnxc AND the oracle; the two must print the same bytes (the twin-court rule).
- **One exact spelling, least authority, refuse loudly** -- and name what is refused. A divergence is a decision, recorded as a D-entry.
- **Decisions**: the author rules; on his delegation the desk rules and records it as delegated. Never present a delegated
  reading as his own.
- **Measure, never assert**; two significant figures; minima over repetitions; state the pattern a change hurts.
- **The machine**: one heavy job at a time; `python <ringpp>\bench\heartbeat.py` before any timing (a throttled CPU reads 20%); a
  long run gets a heartbeat, never a silent watch; power cuts are routine -- commit often.
- **Tools**: write scripts with the Write tool -- Bash heredocs strip backslashes; never round-trip text through PowerShell
  Get-Content/Set-Content; detect a file's own line ending and keep it; commit explicit paths, never `git add -A`.
- **Other desks**: the constitution desk works on Haro too (Zin's articles; v0.23 to v0.27); take the next free version number and
  say so. Never push to another desk's branch; never merge for anyone.

## Where it stands -- 2026-11-02

- v0.28 is the latest rung (CITES on every coded element, `CITES none`; D38, HF-132; guard stage 34).
- `BLOCKS.md` waits on the author: Q-B1 (`AS` and `?` vs C6), Q-B2 (two C6 amendments), Q-B3 (programs as blocks), Q-B4 (the elders).
  Step 1 of REBOL-06 (one C6 reader and a canonical printer, under the printing court) is next on his word.
- Owed to Central (mailbox, 2026-11-02): items 3 and 4 of 2026-10-31 (a value join, a seat shared by ten kinds), COMPASS-KERN-03's
  field check (in `ask_lib.ring`), and REBOL-03's clause (the author's).
- **FIRST, before any of that: make this repository stand alone.** It was carved out of Ring++, and its scripts still reach Ring++
  by climbing directories that are no longer there. `STANDALONE.md` lists every site, the rule (`paths.py`) and when it is done.
