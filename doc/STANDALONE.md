# Standing alone -- DONE, 2026-11-02

This file was the first task's brief when Haro was carved out of Ring++: its scripts reached Ring++ by climbing `../..`, which from
this repository lands in `D:\GitHub`. It is done, and the work grew into the cut (SPIKE.md "The cut"; CHARTER D39-D41; HF-134):

- **`paths.py`** is the one place for where things are. Every script asks it, and none climbs out of the repository: the guard and
  about 35 scripts were moved to it. It names the Haro VM (`HARO_VM`), its checked build (`TWIN`), the run output (`OUT`), Ring++ for
  the bridge to Softanza (`RINGPP`), and Ring 1.27 only as the subject of the studies of Ring (`RING_ORACLE`).
- **A fresh clone passes.** `* text=auto eol=lf` makes every checkout LF, as stored (HF-126).
- **Ring++'s gate still finds Haro beside it.** Its `fmt` step reads `..\haro\spike\v18` (`HARO=` overrides) and hands Haro's
  reference Ring++'s own compiler and oracle (`HARO_VM`, `HARO_TWIN`). Its `fmt` and `dump --json` corpora read Haro's code as `.haro`.

The inventory that was here (which scripts climbed, and how) is in git's history of this file.
