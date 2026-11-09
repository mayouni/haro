# Haro v0.49 -- zip.zig retired: Softanza's engine carries ZIP (D59)

The author, 2026-11-08, of Haro carrying ziplib's natives: "why using "ziplib.ring" altogetjer! we have zip covered by the engine!!"; and
"Ring++ will be retired as Ring and all it's libraries, only Haro will remain." stzlib's port moved stzZipFile onto the engine's
stz_compress (stzlib cb6f5de65, 2026-11-09), and this desk verified with git grep at that ref that no zip_ call is left outside the
guard's own assertions. The twelve natives zip.zig published into every Haro program had no caller. Fixtures first (c526b58: 3 cases,
none holding; R02 rewritten before the code -- it called each name through eval(), which does not reach a native published at start-up,
so it held already and asked nothing).

| line | what | cases |
|---|---|---|
| Z1 | the twelve zip_ names are no longer the VM's: a call of one is what Ring answers with its zip extension not loaded -- R3, naming it, catchable, before the call runs | R01, R02, R03 |
| Z2 | ZIP is Softanza's engine's (stz_compress: StzEngineZipNames, Read, Crc, Write, ExtractAll, LastError), judged by stzlib's own guard -- a gate this desk does not own | named, not run here |

## How it is built

`vm/src/zip.zig` (620 lines) is removed, with its import and its registration in `haro.zig`; httpd.zig's comment that named it is
rewritten. v0.44's zip cases (Q10, Q11, Q12, Q14) and their six plants (Z17 to Z22) retire with the code they judged; v44's generator and
plant script say so.

## Measured

- **The court**: 3 of 3 on haro and its checked build; v0.44's court 10 of 10.
- **The engine carries it**: stzlib's `stzZipFile_defects_narrated.ring`, from a git archive of cb6f5de65 (base, core, the engine's
  .ring bridges), on haro.exe without zip.zig, with STZ_ENGINE_DIR=C:\haro-engine and its stz_compress rebuilt at cb6f5de65 (18 s):
  **305 assertions, 305 pass**. C:\haro-engine's other 91 domains stay at stzlib c4f6f85ea, written in its REF.txt.
- **No plant**: the rung removes code and adds no protection of its own; its three cases on both builds and the court's own `--plant`
  are what judge it.

## Named

- HARO-NEURALGEN-POOL-01: stzlib's neural_gen.zig sizes its pool from the graph since fe871d7e2, so build_engine.py's pool-size patch
  is not needed and the tool says so (d1db951). Whether the 1.5B model runs on Haro's engine at a ref past that is unmeasured: the
  stz_neural domain at C:\haro-engine is still c4f6f85ea's.
