# VOID: measured on prompts the engine had cut

These runs (smollm2-135m, all four cells; Qwen2.5-Coder-0.5B, decoder on) were taken on prompts of about 1,400 tokens. **Softanza's engine keeps only the last 512 tokens of a fresh prompt**
(`neural_gen.zig`: `const cap: usize = 512; ... prompt[prompt.len - cap ..]`), silently, so the model never saw the primer or the first examples: what was measured is a model shown the tail of one worked
example and the task. Found 2026-10-20 by a probe (a secret word in the system message was forgotten behind about 1,200 tokens of filler; it survives at 506 tokens and is gone at 514).

Nothing here may be quoted as a K4 result. They are kept as the record of the defect, and of what a tail-only prompt produces (the decoder still forced a valid shape: 16-17 of 20 programs in the grammar,
and still no program that was right on the hidden data). The measurements that count are in `../` (prompts counted by the generator's own tokenizer, none over 510 tokens).
