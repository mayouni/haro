"""Memory: the K4 paragraph of rung7-reader-resume.md, a new note on Softanza's local models, and the two index lines."""
import io, os

MEM = r'C:\Users\ASUS V3607V CORE 5\.claude\projects\D--GitHub-ringpp\memory'
LF, CR = chr(10), chr(13)


def rw(name, fn):
    p = os.path.join(MEM, name)
    raw = io.open(p, encoding='utf-8', newline='').read()
    nl = CR + LF if CR + LF in raw else LF
    s = fn(raw.replace(CR + LF, LF))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
    print('edited', name)


def k4(s):
    a = s.index('**K4 MEASURED 2026-10-20')
    new = ('**K4 MEASURED, TWICE. Cloud models 2026-10-20 (f7d1f69): the face does no better than Ring (Claude haiku/sonnet, 16 runs, ~3.7M tokens).** He then asked whether a cloud model is sustainable when small local models are first class '
           'in Softanza -- it is a tool, never a foundation (cost, cannot be pinned or run offline in the guard) -- and that was not the regime, so the consequences were withdrawn (76a5068).\n\n'
           '**LOCAL REGIME MEASURED 2026-10-21 (cf2b69c, `haro/spike/v22/k4/K4.md` "The local rounds", HF-112..115): MET AGAIN.** SmolLM2-135M, Qwen2.5-Coder-0.5B and -1.5B, Ring++ and the face, engine decoder on/off, greedy, 20 tasks, '
           'right on shown AND hidden data: 135M 0; 0.5B at most 1 (13 of its 15 shown-only programs print a literal answer); 1.5B Ring++ 5 on / 6 off, face 3 / 3. Size decides; the SAME tasks pass with and without the decoder (it buys shape, not meaning); '
           'the face does not beat Ring++ at any size; the shapes fail differently (Ring++ by not ending, the face by vocabulary the reader refuses). Both grammars are built (`face_gbnf.py`, `ringpp_gbnf.py`, court = Haro guard stage 27, '
           'no model loaded). The first six hours were VOID: the engine keeps only the last 512 tokens of a fresh prompt (`local/void-tail512/`).\n\n'
           'The user\'s baseline correction: K4 compares against Ring++ on rnxc, NEVER Ring 1.27 on the oracle (a retired language; I lapsed once and he caught it). The oracle only guards that the references agree. See [[softanza-local-models]].\n\n'
           'Left: nothing owed on K4. 3B/7B models, sampling with a repetition remedy, per-model primers could move the numbers; not run. Related: [[block-kind-resume]], [[rung5-resume]], [[softanza-method-reference-style]], [[haro-not-ring-habits]].\n')
    s = s[:a] + new
    s = s.replace('K4 MEASURED the same day and MET (the face is a reading aid, not a write surface); the code-graph memo is closed"', 'K4 MEASURED and MET in both regimes, cloud 2026-10-20 and local 2026-10-21 (the face is a reading aid, not a write surface)"')
    return s


NOTE = '''---
name: softanza-local-models
description: "Softanza's local generative models (Qwen2.5-Coder 0.5B/1.5B added 2026-10-21) and the three engine limits that govern using them: 512-token prompt window, a memory pool too small for the 1.5B, no termination remedy"
metadata:
  node_type: memory
  type: project
---

**Where:** `D:\\GitHub\\stzlib\\libraries\\stzlib\\models\\` (`*.gguf` is git-ignored: local assets). Record: `haro/spike/v22/k4/MODELS.md` in ringpp (source, size, sha256). He said yes to the download and asked that the models become Softanza
assets once Haro was done with them; I moved (renamed) them in 2026-10-21. The Ring++ package skips files over 256 MB, so it ships neither Qwen file.

**Why Qwen2.5-Coder-1.5B-Instruct (q8_0, 1.89 GB):** the first of SmolLM2-135M / Qwen 0.5B / Qwen 1.5B that writes working programs under the engine's decoder (K4: 5-6 of 20 right on hidden data). The engine's own header names Qwen2.5 as its target family.

**Three engine limits (his tree, reported in `haro/spike/v22/k4/ENGINE_NOTES.md`, NOT applied there):**
1. `neural_gen.zig` keeps only the last 512 tokens of a fresh prompt, SILENTLY (the head, i.e. the system message, is lost: survives at 506, gone at 514). Count with `StzEngineNeuralGenTokenize`.
2. `forwardDecode`'s memory-pool formula is a few hundred KB short for the 1.5B, so it cannot load. The Ring++ copy (`runtime/engine-copy`) has +25 percent and the package's `stz_neural.dll` is that build (original kept as `.orig-20261020`); `bench/engine_copy.py` re-copies his source over the patch.
3. The decoder guarantees a valid shape, not an end; small models loop to the token cap, and the sampler has no repetition penalty.

**Using one:** the engine has ONE model slot; `StzAutoLoadNeuralModel()` takes the first `*.gguf` in dir() order (on Windows the embedding model all-MiniLM, unchanged by the Qwen files), so load explicitly: `StzNeuralModelQ(path)`.
The local K4 harness is `haro/spike/v22/k4/k4_local.py` (resumable: work dirs under `runtime/k4work/`, a power cut costs one job); results under `k4/local/`, `RESULTS_LOCAL.md`.

**The machine:** the CPU was firmware-throttled to 20-57 percent for much of this work (`python bench/heartbeat.py`); he said to forget the charger, so do not raise it again, and do not quote timings from throttled runs.
'''


def index(s):
    old = [l for l in s.split(LF) if l.startswith('- [Rung 7 and K4]')]
    assert len(old) == 1
    s = s.replace(old[0], '- [Rung 7 and K4](rung7-reader-resume.md) — reader BUILT 2026-10-20 (stage 26); K4 MEASURED and MET in both regimes (cloud 2026-10-20, local 2026-10-21, HF-110..115): the face is a reading aid, not a write surface; baseline is Ring++ on rnxc, never Ring 1.27; grammars built (stage 27).')
    if '[Softanza local models]' not in s:
        s = s.rstrip(LF) + LF + '- [Softanza local models](softanza-local-models.md) — Qwen2.5-Coder 0.5B/1.5B now in stzlib models/ (git-ignored; MODELS.md in ringpp); the 1.5B is the code model; three engine limits (512-token window, pool too small, no termination remedy) reported to him.' + LF
    return s


rw('rung7-reader-resume.md', k4)
io.open(os.path.join(MEM, 'softanza-local-models.md'), 'w', encoding='utf-8', newline='').write(NOTE)
print('wrote softanza-local-models.md')
rw('MEMORY.md', index)
