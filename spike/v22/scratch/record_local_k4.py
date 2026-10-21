"""Record the local K4: K4.md's local section, HF-112..HF-115, and the places that said the local regime was unmeasured / the grammar owed. Line-ending aware, ASCII only."""
import io, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
K4 = os.path.join(ROOT, 'haro', 'spike', 'v22', 'k4')
CR, LF = chr(13), chr(10)


def edit(path, fn):
    raw = io.open(path, encoding='utf-8', newline='').read()
    nl = CR + LF if CR + LF in raw else LF
    s = fn(raw.replace(CR + LF, LF))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
    print('edited', os.path.relpath(path, ROOT))


def rep(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:90])
    return s.replace(a, b)


# ---- the numbers, read from the results ------------------------------------------------------------------------------------------------------------------
MODELS = [('smollm2-135m', 'SmolLM2-135M-Instruct (Q8_0, 0.14 GB; the model Softanza ships)'),
          ('qwen25c-0.5b', 'Qwen2.5-Coder-0.5B-Instruct (Q8_0, 0.68 GB)'),
          ('qwen25c-1.5b-on', 'Qwen2.5-Coder-1.5B-Instruct (Q8_0, 1.89 GB), decoder on'),
          ('qwen25c-1.5b-off', 'Qwen2.5-Coder-1.5B-Instruct (Q8_0, 1.89 GB), decoder off')]
rows = []
for tag, label in MODELS:
    d = json.load(open(os.path.join(K4, 'local', tag, 'results.json')))
    for key in ('ringpp/on', 'ringpp/off', 'face/on', 'face/off'):
        if key in d['summary']:
            s = d['summary'][key]
            shape, dec = key.split('/')
            rows.append('| %s | %s | decoder %s | %d | %d | %d | %d | %d | %d |' % (label.split(' (')[0] if tag != 'qwen25c-1.5b-on' and tag != 'qwen25c-1.5b-off' else 'Qwen2.5-Coder-1.5B',
                                                                                  'Ring++' if shape == 'ringpp' else 'the face', dec, s['valid'], s['ended'], s['reads'], s['runs'], s['shown'], s['pass']))
TABLE = '\n'.join(['| model | shape | decoder | in grammar | wrote the end marker | reads | runs | right on shown data | **right on both** |', '|---|---|---|---|---|---|---|---|---|'] + rows)

LOCAL = '''## The local rounds (2026-10-20/21): small models under the engine's decoder

**What was run.** `k4_local.py`: the same twenty tasks, Ring++ and the Python-shaped face, each with the engine's constrained decoder ON (the shape's grammar, enforced at the sampler: `ringpp_gbnf.py`,
`face_gbnf.py`, judged by `grammar_court.py` = guard stage 27) and OFF, three local models, greedy decoding, offline, on the Ring++ package. The prompt is ChatML: a compact primer, ONE worked example
(not among the twenty), the task with its data lines already written, and a closing line `<<END>>` the program must write. Every prompt is counted with the generator's own tokenizer and none is over 510 tokens.
Scores are taken at the floor, so a model that cannot pass still says how far it got: **in grammar**, **wrote the end marker**, **reads** (the face reader / rnxc accepts it), **runs** (no error on the shown data),
**right on the shown data**, and **right on both** (the K4 pass: the hidden data too, so a program that prints the shown answer fails). Models: SmolLM2-135M-Instruct, which Softanza ships, and
Qwen2.5-Coder-0.5B-Instruct and -1.5B-Instruct (Apache-2.0, `Qwen/*-GGUF`, q8_0, downloaded 2026-10-20 and checked against the published sizes and sha256 -- the engine's header names Qwen2.5 as its target).

**Two limits of the engine, found on the way, which voided the first six hours** (`ENGINE_NOTES.md`; HF-112, HF-113). The engine keeps only the LAST 512 TOKENS of a fresh prompt, silently: the first runs
sent a primer, three examples and the task (about 1,400 tokens) and the model saw the tail of the last example and the task. They read like a model that was never told the language, and they are kept in
`local/void-tail512/` with a README and are not results. The prompts were rewritten to fit, and the generator now refuses to run any over 510 tokens (a system message survives at 506 and is gone at 514).
And the engine's memory pool for the forward pass is too small for the 1.5B (short by 196 KB on a 40-token prompt), so the model cannot run at all; the Ring++ copy of the engine carries a 25 percent margin, his tree is untouched.

**The results** (20 tasks per row; `local/*/results.json`, `RESULTS_LOCAL.md`):

''' + TABLE + '''

## What it shows

- **Model size decides; the decoder and the shape do not.** Right on both inputs: 0 for SmolLM2-135M in every cell; at most 1 for the 0.5B, which had 15 programs (over its four cells) right on the shown data and wrong
  on the hidden: 13 print a literal answer (`fact = 720`) and two start a maximum at 0; 3 to 6 for the 1.5B, where all but one program right on the shown data (a face word-counter that counts spaces) was also
  right on the hidden data -- it computes. The 1.5B is the first of the three that writes working programs in either shape.
- **The decoder buys shape, not meaning.** At 1.5B the same tasks pass with it and without it (the face: 3, 6 and 18, both ways; Ring++: 1, 4, 8, 16 and 20, plus 18 with it off). It raises what is in the grammar
  (the face 3 -> 18 of 20, Ring++ 9 -> 12) and, for the weakest model, what the face reader accepts (SmolLM2: 11 -> 18 of 20), and it changes nothing about which tasks are solved. It also costs the END: with the
  grammar on the 1.5B wrote its end marker in 12 of 20 Ring++ programs, with it off in 19 -- the others repeated one line to the token cap (`break = false` 48 times). A grammar that may always take one more statement is
  always satisfied by one more; the sampler has no repetition penalty (`ENGINE_NOTES.md`, section 3; HF-115). K4's Ring++ numbers are therefore a floor.
- **The face does not beat Ring++ at any size tried.** Right on both, face against Ring++: 0 / 0 (135M), 1 / 0 (0.5B, decoder on), 3 / 5 (1.5B, on), 3 / 6 (1.5B, off). Three programs in twenty are inside the noise of
  this protocol, and the two shapes pass DIFFERENT tasks (the face solves 3, 6 and 18, Ring++ 1, 4, 8, 16 and 20, and 18 with the decoder off). The face's explicit `eq` is what carried task 3, which counts "01" and "1.0" as 1,
  where the Ring++ program reached for Python's `isnumeric` and `float`. They fail differently: Ring++ mostly by not ending (8 of its 15 failures at 1.5B, decoder on), the face by vocabulary the reader refuses
  (`cat` takes two arguments; two names that print as one: 5 of 17), by wrong output (5) and by errors (4). The face also costs prompt:
  its primer is longer, 426-503 tokens a prompt against 391-468, of a 512-token window.

## Limits, stated

Greedy decoding, one run per cell, twenty tasks and the primers written by the same author, and one worked example (the window allows one). The compact primers were written once and never tuned per model, where the cloud
rounds amended theirs twice. A difference of three programs in twenty is noise. Not measured, so not claimed: models above 1.5B; sampling instead of greedy; a repetition penalty or any other remedy for
non-termination; a per-model primer; more examples. Wall times are not reported: the machine's CPU was firmware-throttled for most of the runs (21-57 percent of nominal), which changes how long a run takes and
not what greedy decoding writes.

## Decisions (recorded 2026-10-21 for the author's reading; he has the last word)

1. **K4 is met in the local regime too.** At no model size tried does the face beat Ring++ as a write surface, and it spends more of a small window on its primer. The face stays what K4 left it: a reading aid,
   a lint and a respeller (the lenient reader, then the printer), and the graph's second spelling. It is not a required write surface.
2. **Both grammars stay**, built, held by the engine's decoder and judged by guard stage 27 with no model loaded. Whoever wants a decoder-held write surface has one in either shape; the Ring++ shape is the better
   default today (more passes, no indentation to count) once the engine has a termination remedy.
3. **The model for Softanza.** Qwen2.5-Coder-1.5B-Instruct (Q8_0, 1.89 GB, Apache-2.0) is the first that writes working programs (5-6 of 20 right on both inputs; the 0.5B hard-codes, SmolLM2 does nothing). It is
   the candidate code model; SmolLM2 stays the small chat model Softanza ships. It needs from the engine: the pool fix (without it the model does not run), a prompt window that does not drop the head
   (`ENGINE_NOTES.md` 1) and a termination remedy (3). Both Qwen files are kept as Softanza model assets after this study.
4. **Owed, and not claimed:** the measurements in the last paragraph above. Any of them could move the numbers; a 3B or 7B model is the obvious next rung.
'''

FINDING_ROWS = [
    "| HF-115 | **A constrained decoder guarantees a valid shape, not an end -- and its grammar can cost the end.** With the Ring++ grammar on, Qwen2.5-Coder-1.5B wrote the end marker in 12 of 20 programs; with it off, in 19 of 20: the others repeated one line to the token cap (`break = false` 48 times, `? \"out=0\"` 40). The face's counted-indentation grammar ended 18 of 20 (8 off). The sampler has no repetition penalty, and the grammar cannot tell a repeated line from a long program. The remedy is the sampler's (a penalty, a stop on N identical lines, a bias toward the end token when the grammar is complete); K4 used none, so its Ring++ numbers are a floor. | measured, `v22/k4/ENGINE_NOTES.md` section 3, `local/qwen25c-1.5b-*` | stzlib (his engine), reported |",
    "| HF-114 | **K4 in the local regime: model size decides, the decoder buys shape and not meaning, and the face does not beat Ring++ at any size tried.** Twenty tasks, both shapes, the engine's decoder on and off, SmolLM2-135M, Qwen2.5-Coder-0.5B and 1.5B, greedy, one worked example, prompts of at most 510 tokens, programs judged on the shown AND hidden data. Right on both inputs: 135M 0 in all four cells; 0.5B Ring++ 0 and 0, the face 1 (on) and 0 (off) -- of its 15 programs right on the shown data only, 13 print a literal answer; 1.5B Ring++ 5 (on) and 6 (off), the face 3 and 3, and all but one program right on the shown data right on the hidden data too. The same tasks pass with and without the decoder at 1.5B. The decoder raised what is in the grammar (the face 3 -> 18 of 20) and, for the weakest model, what the face reader accepts (11 -> 18), and nothing else. The shapes fail differently: Ring++ by not ending, the face by vocabulary the reader refuses and by wrong output. Three programs in twenty are inside the noise of the protocol. | measured, `v22/k4/K4.md`, `local/*/results.json`, `RESULTS_LOCAL.md` | ringpp/haro (decisions for the author's reading, 2026-10-21) |",
    "| HF-113 | **The engine's forward-pass memory pool is too small for Qwen2.5-Coder-1.5B, so the model cannot run at all.** `forwardDecode` sizes ggml's pool with a formula (`128 MB + kv_len*n_new*n_head*n_layer*24 + n_new*n_embd*n_layer*64`); for the 1.5B it is short by 196 KB on a 40-token prompt (needed 264,244,144, available 264,048,128) and by 16 MB on a 512-token one, and `GGML_ASSERT(obj_new)` ends the process. The 0.5B and SmolLM2 fit. A quarter more in the engine COPY (stz_neural rebuilt in 29 s, the original DLL kept beside it) runs the 1.5B; his tree is untouched. | measured, `v22/k4/ENGINE_NOTES.md` section 2 | stzlib (his engine), reported with the patch; ringpp (the copy patched) |",
    "| HF-112 | **The engine cuts a fresh prompt to its last 512 tokens, silently, and the head is lost.** `neural_gen.zig`: `const cap: usize = 512; ... prompt[prompt.len - cap ..]`. A secret word in a system message ahead of filler is remembered at 506 tokens and gone at 514 (SmolLM2-135M; counts by `StzEngineNeuralGenTokenize`); no error, no flag, only a wrong answer. The first local K4 runs sent about 1,400 tokens (a primer, three examples, the task), so the model saw the tail of the last example and the task: 120 runs voided and kept in `local/void-tail512/`. The generator counts every prompt now and refuses one over 510. Anything built on `StzGenerateXT` with a long system or few-shot prompt is exposed to the same loss. | measured, `v22/k4/ENGINE_NOTES.md` section 1, `k4_gen.ring` | stzlib (his engine), reported; ringpp/haro (the harness, fixed) |",
]


def findings(s):
    marker = '| HF-111 |'
    assert s.count(marker) == 1
    return s.replace(marker, '\n'.join(FINDING_ROWS) + '\n' + marker)


def k4md(s):
    s = rep(s, '# K4 -- does a model write a Python-shaped face better than Ring? Measured 2026-10-20', '# K4 -- does a model write a Python-shaped face better than Ring? Measured 2026-10-20 (cloud models) and 2026-10-21 (local models)')
    s = rep(s, '\n## The experiment\n', '\n**UPDATE 2026-10-21: the local regime is measured** (section "The local rounds", HF-112 to HF-115): K4 is met there too -- model size decides, the decoder buys shape and not meaning, and the face does not beat Ring++ at\nany size tried. The first sentence above, and decisions 2 to 4 below, describe the state before it.\n\n## The experiment\n')
    i = s.index('## The local rounds (what this directory now runs)')
    return s[:i] + LOCAL


def spike(s):
    return rep(s, 'the\n   small-local-model regime Softanza names is unmeasured and its grammar is owed.',
               'the\n   small-local-model regime was measured 2026-10-21 on three models and met as well (HF-112 to HF-115): size decides, the decoder buys shape and not meaning, the face does not beat Ring++; both grammars are built and held by guard stage 27.')


def codegraph(s):
    s = rep(s, '**Owed:** a GBNF for the face (drafted, `v22/face_gbnf.py`) and the small-local-model-under-a-decoder regime, which is Softanza\'s direction and untested |',
            '**The small-local-model regime, measured 2026-10-21** (SmolLM2-135M, Qwen2.5-Coder-0.5B and 1.5B under the engine\'s decoder, with a GBNF for each shape: `v22/face_gbnf.py`, `v22/ringpp_gbnf.py`): K4 is met there too -- size decides, the decoder buys shape and not meaning, the face does not beat Ring++ (HF-112 to HF-115) |')
    s = rep(s, '| guard stage 26 (`spike/v22/face_read_check.py`); `haro/FINDINGS.md` HF-104 to HF-109 |', '| guard stages 26 and 27 (`spike/v22/face_read_check.py`, `spike/v22/grammar_court.py`); `haro/FINDINGS.md` HF-104 to HF-115 |')
    return s


def gram21(s):
    return rep(s, 'for them the face is a reading aid and a respeller, not a write surface; small local models under a decoder are unmeasured.',
               'for them the face is a reading aid and a respeller, not a write surface; small local models under a decoder were measured 2026-10-21 and K4 is met there too (HF-112 to HF-115).')


def gram22(s):
    s = rep(s, '| **measured 2026-10-20: met for capable models** (Ring at ceiling, the face at best ties), `k4/K4.md`, HF-110, HF-111 |',
            '| **measured 2026-10-20 and 2026-10-21: met for capable models and for small local ones** (`k4/K4.md`, HF-110 to HF-115) |')
    s = rep(s, '**Not measured, and the regime Softanza names: a small local model under the decoder** -- so that consequence is not applied.',
            '**The regime Softanza names, a small local model under the decoder, was measured on 2026-10-21** (SmolLM2-135M, Qwen2.5-Coder-0.5B and 1.5B; the face does not beat Ring++ at any size, and the decoder buys shape and not meaning; HF-114) -- so the consequence holds there too.')
    a = s.index('- **A GBNF for the face: drafted, OWED.**')
    b = s.index('\n', a)
    s = s[:a] + ('- **A GBNF for the face: built 2026-10-21.** `face_gbnf.py` (about 93 of the decoder\'s 128 rules) accepts the twenty K4 programs and 39 of the 43 texts the printer prints for the v21 fixtures, rejects what the shape excludes, '
                 'and is judged with its Ring++ counterpart (`ringpp_gbnf.py`) by `grammar_court.py`, guard stage 27, with no model loaded; the four it does not accept are trailing comments, `next i` and `new @`.') + s[b:]
    return s


edit(os.path.join(ROOT, 'haro', 'FINDINGS.md'), findings)
edit(os.path.join(K4, 'K4.md'), k4md)
edit(os.path.join(ROOT, 'haro', 'SPIKE.md'), spike)
edit(os.path.join(ROOT, 'haro', 'CODEGRAPH.md'), codegraph)
edit(os.path.join(ROOT, 'haro', 'spike', 'v21', 'GRAMMAR.md'), gram21)
edit(os.path.join(ROOT, 'haro', 'spike', 'v22', 'GRAMMAR.md'), gram22)
print('done')
