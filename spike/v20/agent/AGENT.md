# Rung 5 with a model as the agent -- measured 2026-10-21

**The question.** Rung 5 (Haro v0.20) lets an agent change a program only through a refinement against a point a human declared, judged by a gate of five stages. For the BLOCK, FUNCTION and METHOD kinds the
agent writes a function's body. Every one of the 147 fixtures that judge this was written by hand, and the court's "agent" is a harness: **no model had ever been put in the loop.** Does a local
model, as the agent, get its bodies admitted by the gate and right when the program runs -- and does the write surface rung 5 gives it (the decoder fixes the sentence around a body and leaves
TO as one line of free text, `qbody`) help?

## The experiment

Sixteen tasks (`tasks.py`): a small Ring++ program with ONE point, its allowlist of calls (and writes) in the tag, the function's signature a human's, the body the agent's: twelve BLOCK points
(empty bodies: sum to n, factorial, even, larger of two, clamp, vowels, reverse, average, gross plus tax through an allowed helper, fizz, digit sum, round) and four more that need a global write or a function
that is not there yet (FUNCTION kind: square, last item, dash-join; BLOCK with a `writes` allowlist: a counter). Each runs on TWO data sets -- the one the prompt shows and one the checker substitutes -- so a body that
returns the shown answer fails (K4's rule). **The harness was proven on gold answers before any model was asked** (`r5_agent.py selftest`, guard stage 28): the sixteen gold bodies are admitted
by the gate and right on both data sets with rnxc and the oracle agreeing; a hard-coded body is admitted and right on the shown data only; a call the point does not allow, a function defined inside, a double quote and
a comment are refused at their stages.

The agent writes the BODY; the harness writes the sentence around it (TARGET, KIND, FROM, AUTHOR, POSTURE, REASON -- an agent cannot write a stronger posture, charter 6.2), puts it through
`refine.Model.refine`, and runs the refined program on rnxc. **Four ways of asking for the body, the same prompt otherwise** (a primer, one worked example, the program with its tag, the point's
allowlists, the parameters of a function that does not exist yet, the task, what the program prints on the shown data; counted with the generator's own tokenizer, none over 433 tokens):

| arm | what the model writes | what the decoder is told |
|---|---|---|
| `free` | one line | nothing -- the harness takes its first line: **rung 5's write surface as `scoped.py` leaves it** (`qbody` is one line of free text) |
| `scoped` | one line | the point's body grammar, `body_gbnf.body_grammar`: one line, a statement list, only the point's calls, writes only to the point's names |
| `lines` | a statement a line, a tab a level, a closing line `<<END>>` | nothing; the harness flattens the lines into the one-line TO |
| `lines-scoped` | the same | the same body as lines, `body_gbnf.lines_grammar` (84-88 rules, held by the engine's decoder, 16 of 16 gold bodies accepted, `body_court.py`); derived from the program's own point by `scoped.body_lines_gbnf` |

Scores at the floor, as K4's: **gate can read it** (the structural stage), **admitted** (every stage), **runs**, **right on shown**, **right on both**. Greedy decoding, one run per cell, three models,
`runtime/k4work/r5-*` is resumable after a power cut (a job whose `.meta` exists is finished).

## The results (16 tasks per row; `local/*/results.json`, `RESULTS_LOCAL.md`)

| model | the body written as | gate can read it | admitted | runs | right on shown | **right on both** |
|---|---|---|---|---|---|---|
| SmolLM2-135M-Instruct | one line, free | 12 | 12 | 6 | 1 | **1** |
| SmolLM2-135M-Instruct | one line, scoped grammar | 16 | 16 | 7 | 1 | **1** |
| SmolLM2-135M-Instruct | lines, free | 12 | 12 | 3 | 0 | **0** |
| SmolLM2-135M-Instruct | lines, scoped grammar | 14 | 14 | 2 | 0 | **0** |
| Qwen2.5-Coder-0.5B | one line, free | 11 | 9 | 1 | 0 | **0** |
| Qwen2.5-Coder-0.5B | one line, scoped grammar | 14 | 14 | 1 | 0 | **0** |
| Qwen2.5-Coder-0.5B | lines, free | 10 | 10 | 3 | 2 | **2** |
| Qwen2.5-Coder-0.5B | lines, scoped grammar | 14 | 14 | 6 | 3 | **3** |
| Qwen2.5-Coder-1.5B | one line, free | 8 | 8 | 6 | 3 | **3** |
| Qwen2.5-Coder-1.5B | one line, scoped grammar | 11 | 11 | 4 | 3 | **3** |
| Qwen2.5-Coder-1.5B | lines, free | 9 | 8 | 8 | 7 | **7** |
| Qwen2.5-Coder-1.5B | lines, scoped grammar | 14 | 13 | 11 | 10 | **10** |

## What it shows

- **A one-line body is the wrong thing to ask a model to write, and the harness should flatten.** Qwen2.5-Coder-1.5B gets 3 of 16 right on a one-line body, with or without a grammar, and **7 of 16 when it writes lines**
  that the harness joins into the sentence's TO (10 under the lines grammar). Its natural output is lines: asked for one, it glues `ok`, `next` and `return` into the identifiers around them and loops. The gate
  sees the same body either way, so this costs the gate nothing.
- **The scoped grammar earns its place once the shape is natural.** On one line it raises what the gate can read and not what is right (1.5B: 8 -> 11 readable, right 3 -> 3). On lines it raises both: **1.5B 7 -> 10 right**
  (9 -> 14 readable, admitted 8 -> 13), **0.5B 2 -> 3**. This is the first measurement in this work in which the decoder improved correctness and not only shape (K4's decoder did not).
- **Size still decides.** SmolLM2-135M gets 0-1 of 16 in every arm, the 0.5B 0-3, the 1.5B 3-10. The 1.5B on lines under the grammar gets **10 of 16** and every program right on the shown data is right on the other.
- **What is left, for the 1.5B on lines under the grammar** (six of sixteen): **three never end** -- R02 glued its closers into an identifier (`oknextreturnf *= i`) and repeated it to the token cap, which the grammar allows because a GBNF cannot say "an identifier that is not a keyword"; R06 repeated a line; R05 ran an identifier on (`minmaxmax...`) until the compiler's own check refused it (`derivation`: a name nothing assigns). **Two were admitted and errored when run**: R07 wrote `/ next` where a downward loop needs `step -1`, and R15 used the call site's variable names (`cA + '-' + cB`) although the prompt lists the function's parameters. **One was admitted and wrong**: R14 took `aL[len(aL) - 1]`, a 0-based index in a 1-based language. The first run of every arm lacked the parameter list in the prompt of a function that does not exist yet (`local/v1-no-params/`, kept): that was the prompt's defect and all arms were re-run.

## Limits, stated

Sixteen tasks I wrote, one worked example, greedy, one run per cell, small bodies (a gold body is 15-60 tokens), three models. Ten of sixteen is a count, not a rate: a difference of one or two tasks is noise, and the
larger gaps (3 -> 7 -> 10) are what the table can carry. The gate's constraint and derivation stages bound rarely here (three refusals in all); a task designed to tempt a forbidden call would test them. `free` stands for
`qbody`'s constraint (one line of text) but is not the decoder's own: with a grammar that only forbids a quote and a newline the result could differ a little. Nothing here exercises a METHOD point, a point of a larger program,
or an agent that proposes a second refinement after the first. The machine's CPU was firmware-throttled for most of the runs, which changes how long they took and not what greedy decoding writes.

## Decisions (recorded 2026-10-21 for the author's reading; he has the last word)

1. **For a body kind the agent's write surface is the body, as lines, under the point's own grammar; the sentence is the harness's.** This amends the charter's 6.2 ("the agent's only write surface is a sentence") for BODY kinds only: the
   sentence stays the record the gate judges, and `scoped.body_lines_gbnf(model, name)` is the agent's surface. `scoped_gbnf`'s `qbody` stays for a sentence written by something that is not a model.
2. **Flatten in the harness, never ask the model for a line.** Nothing the gate judges changes.
3. **A termination remedy is owed to the engine, and a keyword-aware identifier to the grammar.** Three of the six failures are a body that does not end; the decoder cannot tell a repeated line from a long program
   (`v22/k4/ENGINE_NOTES.md` section 3). Softanza's own naming convention (nName, cName, aName, oName, bName) would make `oknextreturn` an impossible identifier -- a grammar option to measure, not yet measured.
4. **Not measured, so not claimed:** models above 1.5B, sampling, a per-model primer, more than one example, a METHOD point, a larger program, a tempting forbidden call.
