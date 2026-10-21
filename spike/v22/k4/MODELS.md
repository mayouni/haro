# The generative models Softanza holds (`libraries/stzlib/models/`), as of 2026-10-21

`*.gguf` is ignored by git in stzlib, so these are local assets: this file is their record. The engine has ONE model slot (`StzEngineNeuralModelLoaded`): a program that needs an embedding model and a
generative one in turn loads them in turn.

| file | what | size | sha256 | licence | source |
|---|---|---|---|---|---|
| `all-MiniLM-L6-v2.Q8_0.gguf` | sentence embeddings | 25,008,064 | (not recorded) | not checked here | already in the tree |
| `jina-reranker-v1-turbo-en-Q8_0.gguf` | cross-encoder reranker | 41,719,968 | (not recorded) | not checked here | already in the tree |
| `smollm2-135m-instruct-q8_0.gguf` | chat, 135M; the small generative model Softanza has always had | 144,811,360 | (not recorded) | not checked here | already in the tree |
| `qwen2.5-coder-0.5b-instruct-q8_0.gguf` | code and chat, 0.5B | 675,710,848 | `e1a77721fa97d412f121878223eec81fb4ae6f271e18f922d746711f67b344d1` | Apache-2.0 | `huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct-GGUF` |
| `qwen2.5-coder-1.5b-instruct-q8_0.gguf` | code and chat, 1.5B; **the one that wrote working programs in K4** | 1,894,532,160 | `507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47` | Apache-2.0 | `huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF` |

The two Qwen files were downloaded on 2026-10-20 for the local K4 and moved here when it was done, with the author's yes; size and sha256 were checked against the publisher's listing after the download and again after
the move. The engine's own header names Qwen2.5 as the family its decoder targets (`neural_gen.zig`: llama, qwen2, qwen3, smollm architectures).

## What using them takes (K4.md, ENGINE_NOTES.md)

- **Load explicitly.** `StzAutoLoadNeuralModel()` takes the first `*.gguf` in `dir()` order, which on Windows is the embedding model; the Qwen files sort after the reranker and before SmolLM2, so nothing that auto-loads
  today changes. To generate with one: `StzNeuralModelQ("<path>/qwen2.5-coder-1.5b-instruct-q8_0.gguf")` then `StzGenerateXT(prompt, [[:MaxTokens, n], [:Temperature, 0], [:Grammar, g]])`.
- **The 1.5B does not run on the engine as it stands**: the forward pass's memory pool is a few hundred KB short (`ENGINE_NOTES.md` section 2). The Ring++ package carries a patched `stz_neural.dll` (the original beside it as
  `.orig-20261020`); the stzlib tree needs the one-line change.
- **A prompt must be under 512 tokens**: the engine drops the head of a longer one without a word (section 1). `StzEngineNeuralGenTokenize(text)` counts them.
- **Ring++ leaves them out of its package** (every file over 256 MB is skipped), so they are an optional download, not a shipped part.
- **Speed**, measured on a laptop whose CPU the firmware held at 20-57 percent of nominal for much of the time, with a prompt of 400-500 tokens and a short program: the 0.5B 24 seconds a job at best (80 jobs in 1,913 s), the 1.5B 77 seconds a job at best (40 jobs in 3,063 s) and about 12 minutes at worst. Not a figure to quote.
