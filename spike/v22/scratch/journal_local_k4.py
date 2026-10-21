"""Journal: the local K4 memo (appended to the softanza memo of the day), the CONCLUSIONS line, and the memory notes. Append-only for the shared journal files: other sessions write to them too."""
import io, os

MEMO = r'D:\GitHub\softanza\memos\2026-10-21.md'
CONC = r'D:\GitHub\softanza\dashboard\CONCLUSIONS.md'
MEM = r'C:\Users\ASUS V3607V CORE 5\.claude\projects\D--GitHub-ringpp\memory'
LF, CR = chr(10), chr(13)

memo = '''
## ringpp — Haro K4 in the local regime: measured and met; two engine limits and a missing termination remedy for the author; the Qwen2.5-Coder models are Softanza assets

```yaml
by:        ringpp · claude-sonnet-5-5 · 2026-10-21
subject:   the twenty K4 tasks written by SmolLM2-135M, Qwen2.5-Coder-0.5B and -1.5B under the engine's constrained decoder, in Ring++ and in the Python-shaped face, decoder on and off
why:       the author asked whether a cloud model is a sustainable basis when small local models are first class in Softanza, and told me to choose a larger local model

did:
  - finished the two write-surface grammars (face_gbnf.py, ringpp_gbnf.py) and a court for them with controls (grammar_court.py = Haro guard stage 27, no model loaded; the decoder holds both, 20 of 20 K4 programs accepted)
  - built the local harness (k4_local.py, k4_gen.ring): counted prompts, resumable after a power cut, floor-aware scores; moved the K4 baseline to Ring++ on rnxc (the first cloud rounds had been judged as Ring 1.27 on the oracle: my lapse, recorded)
  - downloaded Qwen2.5-Coder-0.5B and 1.5B Instruct (q8_0, Apache-2.0) with the author's yes, sha256 checked, and moved them into libraries/stzlib/models/ when done (untracked: *.gguf is ignored); record in ringpp haro/spike/v22/k4/MODELS.md

found:
  - K4 is met in the local regime too: right on both inputs, SmolLM2 0 of 20 in every cell, the 0.5B at most 1, the 1.5B 5 (on) and 6 (off) in Ring++ and 3 and 3 in the face; the same tasks pass with and without the decoder, so the decoder buys shape and not meaning; size decides (HF-114)
  - YOUR ENGINE, three things (haro/spike/v22/k4/ENGINE_NOTES.md): (1) neural_gen.zig keeps only the last 512 tokens of a fresh prompt and drops the head, silently -- a system message survives at 506 tokens and is gone at 514; it voided my first 120 runs; (2) forwardDecode's memory-pool formula is short by 196 KB on a 40-token prompt for Qwen2.5-Coder-1.5B, so the model cannot run at all (a quarter more in a COPY fixes it; the line is in the notes); (3) the decoder guarantees a valid shape, not an end: with the Ring++ grammar the 1.5B wrote its end marker in 12 of 20 programs and 19 of 20 without it, the rest repeating one line to the token cap -- the sampler has no repetition penalty
  - Ring++ itself: new K() on a class with no init makes the object where Ring raises R3 (F-131)

waiting:
  - the author: apply (2) in stzlib (without it the 1.5B does not load), decide (1) and (3); whether the Ring++ package should offer the Qwen models as an optional download (it skips every file over 256 MB, so it ships neither); whether Softanza wants a helper to choose a model by name -- the engine has one model slot and StzAutoLoadNeuralModel() takes the first .gguf, which on Windows stays the embedding model

next:
  - me:      nothing owed on K4. A 3B or 7B model, sampling with a repetition remedy and a primer tuned per model are the measurements that could move the numbers; not run
  - author:  the three engine decisions above
```
'''
conc = ('2026-10-21 | ringpp | HARO K4 LOCAL MEASURED, MET (HF-112 to HF-115): SmolLM2-135M, Qwen2.5-Coder-0.5B and -1.5B under the decoder, Ring++ and the face, decoder on and off -- size decides, the decoder buys shape not meaning, the face does not beat Ring++; '
        'YOUR ENGINE: neural_gen.zig drops the head of a prompt over 512 tokens silently, its memory pool is too small for the 1.5B (it cannot load), and the decoder cannot end a looping program (ringpp haro/spike/v22/k4/ENGINE_NOTES.md); the Qwen models are in libraries/stzlib/models/')


def append(path, text, one_line):
    raw = io.open(path, 'rb').read()
    # the file's own line ending, read from its last complete line
    crlf = raw.rstrip(b'\r\n').rfind(b'\n') > 0 and raw.rstrip(b'\r\n')[raw.rstrip(b'\r\n').rfind(b'\n') - 1:raw.rstrip(b'\r\n').rfind(b'\n')] == b'\r'
    nl = (CR + LF) if crlf else LF
    body = text if one_line else text.lstrip(LF)
    out = (b'' if raw.endswith(b'\n') else nl.encode()) + (b'' if one_line else nl.encode()) + body.replace(LF, nl).encode('utf-8') + (nl.encode() if not body.endswith(LF) else b'')
    with io.open(path, 'ab') as f:
        f.write(out)
    print('appended to', path, '(CRLF)' if crlf else '(LF)')


append(MEMO, memo, False)
append(CONC, conc, True)
