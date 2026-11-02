# Standing alone -- the first task in this repository

Haro was carved out of Ring++ on 2026-11-02 (`git subtree split --prefix=haro`). Its scripts were written when they lived at
`ringpp/haro/...`, so most of them find Ring++ -- `rnxc`, the oracle, `runtime/`, `bench/` -- and Haro itself by climbing a fixed
number of directories: `ROOT = HERE/../..` from `spike/`, `HERE/../../..` from `spike/vNN/` and `study/x/`. Here, those climbs land in
`D:\GitHub`, not in Ring++. **Nothing in this repository runs correctly until that is fixed**, the guard included.

## The rule to implement

One small module, `paths.py` at the root (HaroServer has the same shape: `D:\GitHub\haroserver\paths.py`), and every script asks it:

    HARO     this repository's root (where this file is)
    RINGPP   env RINGPP, else a checkout beside this one (`<parent>\ringpp`), else stop and say which was looked for
    RNXC     env RNXC, else RINGPP\zig-out\bin\rnxc.exe
    RING     env RING, else RINGPP\runtime\win64\ring.exe      (the oracle; Ring++'s own build of Ring 1.27's VM)
    OUT      where generated files go: HARO\runtime\ (gitignored here) -- it was RINGPP\runtime\haro-forge-oracle

No silent fallback to the install (`D:\ringpp\ringpp-win64`): a court must say which compiler it ran on. A report that names a
build names it from `RNXC` (its path, and Ring++'s commit when RINGPP is a checkout) -- HaroServer's `rnxc_build()` is the model.

## The inventory, taken at the split (scratch folders left out)

The guard, `spike/haro_forge.py`: `ROOT = HERE/../..` (line 21); `RNXC`, `ORACLE` from it (22-23); `ROOT\runtime\haro-forge-oracle`
as its oracle work folder (seven sites); `ROOT\runtime\package\ringpp-win64\bin\rnxc.exe` (the package's rnxc, stage 6's engine
probe); `ROOT\runtime\stz_names.txt`; bench/exec as the oracle probe corpus (stage 26); and two absolute paths that are other
desks' binaries, `D:\GitHub\harobanda\zig-out\bin\harb.exe` and `D:\GitHub\zing\cli\zig-out\bin\zing.exe` (leave those, or route
them through env with the same default).

The others that climb to Ring++ or name `ROOT\haro\...` (each must take `paths`):

    spike/v17/n_check.py, probe_rejects.py
    spike/v18/l1_check.py, cst.py (an ABSOLUTE default D:\GitHub\ringpp\zig-out\bin\rnxc.exe), probes/closers.py, fall.py,
        export_vs_dump.py, refused58.py (a path relative to the CURRENT directory)
    spike/v19/ids_check.py
    spike/v20/refine.py, refine_check.py, probes/mutate.py, probes/library_softanza.py, agent/r5_agent.py (r5_local, r5_retry
        and lint_corpus take ROOT from it or climb themselves)
    spike/v22/grammar_court.py, face_read_check.py (bench/exec), ringpp_gbnf.py, k4/k4.py, k4/k4_local.py
    study/codegraph/corpus.py, cst.py (absolute default), identity.py, layout.py, spellings.py
    study/phase15/e3_run.py, e4_run.py, e12_run.py, voices.py   (`ROOT\haro\spike`)
    study/rebol/census.py, gen_fixtures.py                     (`D:\GitHub\ringpp\haro\spike` spelt out)

Find them again rather than trusting this list: `grep -rnE "ROOT|zig-out|runtime|'bench'|ringpp" --include=*.py spike study`.
Ring files: `spike/v18/scratch/*.ring` load `../../stzBase.ring` (scratch, never run by the guard; leave them).

## Done when

- `python spike/haro_forge.py` runs every one of its 34 stages from `D:\GitHub\haro` and passes, on both runtimes, with Ring++
  found beside it and again with `RINGPP=` pointing elsewhere; `--plant` fails it;
- a FRESH clone passes too (`git clone` into a new folder, then the guard). It does not today: HF-126 measured that a fresh
  checkout writes the spike's non-`.ring` files CRLF (`core.autocrlf` is true on this machine), and stage 20's `v17/n_check.py` then
  counts a fragment holding `\n` as absent. The working tree at D:\GitHub\haro was laid as a byte copy of the one that passed in
  Ring++, so it holds these files as they were; a clone does not. Decide the `.gitattributes` rule (or the reader's fix) and say which. The same decision answers
  the four forged `.gbnf` files that git holds CRLF and the forge writes LF;
- nothing under this repository climbs out of it except through `paths.py`;
- Ring++'s gate (in `D:\GitHub\ringpp`, `python bench/gate.py`) still finds Haro beside it: its `fmt` step reads `..\haro\spike\v18`
  (`HARO=` overrides) and SKIPs by name without it;
- the account says what moved, in FINDINGS (a new HF) and SPIKE.md, and the mailbox is told.
