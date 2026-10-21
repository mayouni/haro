# Two limits of Softanza's generative engine, found by the local K4 (2026-10-20)

For Mansour. Both are in `libraries/stzlib/engine/src/neural_gen.zig` (his tree); nothing there was touched. The Ring++ engine copy (`runtime/engine-copy`) carries the second fix so that the
1.5B model can run at all; the first is measured around, not patched, so that the K4 measures the engine as it is.

## 1. A fresh prompt is cut to its LAST 512 tokens, silently -- the head (system message, first examples) is lost

`neural_gen_start`, line 904: `const cap: usize = 512; ... if (reset != 0 and prompt.len > cap) prompt = prompt[prompt.len - cap ..];`

**Measured** (smollm2-135m; a system message "The secret word is PINEAPPLE ... answer with exactly that word", then filler, then "What is the secret word?"; token counts by
`StzEngineNeuralGenTokenize`, the generator's own tokenizer):

    prompt of 490 / 498 / 506 tokens   -> "The secret word is PINEAPPLE. ..."
    prompt of 514 tokens               -> "OK."
    prompt of 522 / 538 tokens         -> "The answer is: ..." / nothing

So the cap is exact (512 counting the leading BOS) and nothing says it happened: no error, no flag, the answer is merely wrong. It cost the first six hours of the local K4: prompts of about 1,400 tokens
(a primer, three worked examples, the task) reached the model as the tail of the last example and the task, and the results read like a model that was never told what language to write. They are
kept in `local/void-tail512/` with a README, and are not results.

Why it matters beyond K4: a ChatML conversation whose system message and first turns come first is exactly what a cap of this shape removes. Anything Softanza builds on `StzGenerateXT` with a long
system prompt, a few-shot prompt or a retrieved context is affected, and fails soft.

Options, cheapest first (his call): (a) raise a catchable error, or set a flag the Ring side can read (`StzLastGenerationTruncated()`), when the cap bites; (b) cut the MIDDLE and keep the head and the tail;
(c) lift the cap by prefilling in chunks of 256 -- the append path (`reset == 0`) already exists for chat turns, and the memory estimate below is quadratic in `n_new`, so chunks are also what keeps a
larger model inside its pool.

## 2. The forward pass's memory pool is too small for Qwen2.5-Coder-1.5B: the model cannot run at all

`forwardDecode`, line 445: `const mem_size: usize = 128 * 1024 * 1024 + kv_len * n_new * n_head * n_layer * 24 + n_new * n_embd * n_layer * 64;`

**Measured**, `qwen2.5-coder-1.5b-instruct-q8_0.gguf` (1,894,532,160 bytes, sha256 507de590...bc47), engine as it is:

    a 40-token prompt     ggml_new_object: not enough space in the context's memory pool (needed 264244144, available 264048128)
    a 512-token prompt    ... (needed 3673525360, available 3657433088)       -> GGML_ASSERT(obj_new) failed, the process ends

Short by 196 KB at 40 tokens and by 16 MB at 512: the estimate under-counts something that grows with the model (12 heads, 28 layers, n_embd 1536, n_ff 8960 against the 0.5B's 14, 24, 896, 4864,
which fits). The 0.5B and smollm2 are fine; the 1.5B never loads a single prompt.

**The copy's fix** (`runtime/engine-copy/src/neural_gen.zig`, stz_neural rebuilt in 29 s, installed in the Ring++ package; the original DLL kept beside it as `stz_neural.dll.orig-20261020`):

    const mem_size_est: usize = 128 * 1024 * 1024 + kv_len * n_new * n_head * n_layer * 24 + n_new * n_embd * n_layer * 64;
    const mem_size: usize = mem_size_est + mem_size_est / 4 + 1024 * 1024 * 1024;

With it the 1.5B answers PINEAPPLE for the 40-token prompt and for the same prompt with 35 and 45 sentences of filler between the system message and the question (about 400 and 500 tokens). **A quarter more was not enough, and the first version of this fix was wrong for short prompts:** a 368-token prompt on the 1.5B (the rung 5 agent tasks) failed with a quarter more by 1.1 MB (`needed 2800125616, available 2799001600`), because the estimate under-counts something that does not grow with the prompt, so a percentage margin only works for long ones; the copy carries a constant gigabyte as well. A pool that is not touched is address space, not memory (`no_alloc = false` commits what the graph uses); the
proper fix is to size the pool from the graph (`ggml_graph_overhead` + the tensors it allocates) rather than from a formula.

Not in his tree: this is a note, not a commit. The Ring++ package's DLL is a derived file and `bench/engine_copy.py` re-copies his source over the patch the next time it runs.

## 3. The constrained decoder guarantees a valid shape, not an END -- and a small model loops inside the grammar

Not a defect of `gbnf_machine.zig`: a grammar that may always take one more statement is always satisfied by one more statement. **Measured** (greedy, the decoder on, 20 tasks a shape): Qwen2.5-Coder-1.5B left 8 of its 20 Ring++ programs without their end marker, running to the 320-token cap on one repeated line (`break = false` 48 times, `? "out=0"` 40, `endif = 0` 32 and 27 in two others, `shift = end` 32); the Python-shaped face, whose grammar counts indentation, did it in 2 of 20. The 0.5B did it in 4 of 20 for each shape, smollm2-135m in 4 of 20 for each shape and each decoder setting.
The decoder cannot tell a repeated line from a long program.

The cheap remedies are the sampler's, not the grammar's: a repetition penalty (`StzGenerateXT` has temperature, top-p, top-k and a seed, and no penalty), a stop when the same line has been produced N times, or a bias
toward the grammar's end token whenever the grammar is complete. K4 used none of them, so its Ring++ numbers are a floor for the shape, not a ceiling.
