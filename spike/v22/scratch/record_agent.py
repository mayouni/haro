"""Record rung 5 with a model as the agent: v20/agent/AGENT.md (the results table is read from results.json), HF-116 and HF-117, the v20 grammar document, CODEGRAPH, SPIKE and the charter's 6.2."""
import io, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
AG = os.path.join(ROOT, 'haro', 'spike', 'v20', 'agent')
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


MODELS = [('smollm2-135m', 'SmolLM2-135M-Instruct'), ('qwen25c-0.5b', 'Qwen2.5-Coder-0.5B'), ('qwen25c-1.5b', 'Qwen2.5-Coder-1.5B')]
ARMS = [('free', 'one line, free'), ('scoped', 'one line, scoped grammar'), ('lines', 'lines, free'), ('lines-scoped', 'lines, scoped grammar')]
rows = []
S = {}
for tag, label in MODELS:
    d = json.load(open(os.path.join(AG, 'local', tag, 'results.json')))
    for arm, alabel in ARMS:
        s = d['summary'][arm]
        S[(tag, arm)] = s
        rows.append('| %s | %s | %d | %d | %d | %d | **%d** |' % (label, alabel, s['shape'], s['admitted'], s['runs'], s['shown'], s['both']))
TABLE = '\n'.join(['| model | the body written as | gate can read it | admitted | runs | right on shown | **right on both** |', '|---|---|---|---|---|---|---|'] + rows)
assert S[('qwen25c-1.5b', 'free')]['both'] == 3 and S[('qwen25c-1.5b', 'lines-scoped')]['both'] == 10 and S[('qwen25c-0.5b', 'lines-scoped')]['both'] == 3

AGENT = '''# Rung 5 with a model as the agent -- measured 2026-10-21

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

''' + TABLE + '''

## What it shows

- **A one-line body is the wrong thing to ask a model to write, and the harness should flatten.** Qwen2.5-Coder-1.5B gets 3 of 16 right on a one-line body, with or without a grammar, and **7 of 16 when it writes lines**
  that the harness joins into the sentence's TO (10 under the lines grammar). Its natural output is lines: asked for one, it glues `ok`, `next` and `return` into the identifiers around them and loops. The gate
  sees the same body either way, so this costs the gate nothing.
- **The scoped grammar earns its place once the shape is natural.** On one line it raises what the gate can read and not what is right (1.5B: 8 -> 11 readable, right 3 -> 3). On lines it raises both: **1.5B 7 -> 10 right**
  (9 -> 14 readable, admitted 8 -> 13), **0.5B 2 -> 3**. This is the first measurement in this work in which the decoder improved correctness and not only shape (K4's decoder did not).
- **Size still decides.** SmolLM2-135M gets 0-1 of 16 in every arm, the 0.5B 0-3, the 1.5B 3-10. The 1.5B on lines under the grammar gets **10 of 16** and every program right on the shown data is right on the other.
- **What is left, for the 1.5B on lines under the grammar** (six of sixteen): **three do not end** -- one line repeated to the token cap, and twice `oknextreturn...` glued into an identifier, which the grammar allows
  because a GBNF cannot say "an identifier that is not a keyword" -- one body the compiler's own check refused (`derivation`: a name that nothing assigns), two admitted and wrong at run time (a function body that
  used the call site's variable names, `cA + '-' + cB`, although the prompt lists the parameters; `aL[len(aL) - 1]` for the last item, 0-based). The first run of every arm lacked the parameter list in the prompt of a function that does not exist yet
  (`local/v1-no-params/`, kept): that was the prompt's defect and all arms were re-run.

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
'''

FIND = [
    "| HF-117 | **A grammar cannot tell an identifier from a keyword, and a small model uses the gap to stop writing.** Under the lines grammar Qwen2.5-Coder-1.5B left 3 of 16 bodies without an end: one repeated a line to the token cap, two glued the closers into an identifier (`oknextreturnf *= i`, valid because `id` is `[A-Za-z_][A-Za-z0-9_]*`) and went on. A GBNF has no negation, so \"an identifier that is not a keyword\" is not sayable; Softanza's naming convention (nName, cName, aName, oName, bName) would exclude it by shape and is the option to measure. The sampler's missing termination remedy (HF-115) is the other half. | measured, `v20/agent/AGENT.md`, `local/qwen25c-1.5b/results.json` | ringpp/haro; stzlib (his engine), reported |",
    "| HF-116 | **A model as the agent of rung 5: a one-line body is the wrong thing to ask for, lines are right, and the scoped grammar earns its place on lines.** Sixteen refinement tasks (a BLOCK or FUNCTION point, its allowlists, two data sets), the gate as judge, rnxc running the refined program; the harness proven on gold answers first (guard stage 28). Right on both data sets, 1.5B / 0.5B / SmolLM2: one line free 3 / 0 / 1 (rung 5's write surface as it stands: `qbody`); one line under the point's grammar 3 / 0 / 1; lines free 7 / 2 / 0; **lines under the point's grammar 10 / 3 / 0**. The agent writes the body and the harness the sentence; the lines are flattened into TO, so the gate sees the same body. The first run lacked a function point's parameters in the prompt (my defect; re-run, kept as v1). For BODY kinds the charter's 6.2 \"only write surface is a sentence\" becomes \"the body under the point's grammar\" (`scoped.body_lines_gbnf`). | measured, `v20/agent/AGENT.md`, guard stage 28 | ringpp/haro (decision for the author's reading, 2026-10-21) |",
]


def findings(s):
    marker = '| HF-115 |'
    assert s.count(marker) == 1
    return s.replace(marker, '\n'.join(FIND) + '\n' + marker)


def v20(s):
    s = rep(s, '| the kind `method`: an agent proposes a method of a class that is not there yet, or the body of one that is | **built** (2026-10-20) | section 14 |',
            '| the kind `method`: an agent proposes a method of a class that is not there yet, or the body of one that is | **built** (2026-10-20) | section 14 |\n| **a local model as the agent**, on sixteen tasks (the body free or under its point\'s grammar, one line or lines) | **measured** (2026-10-21): 1.5B 3 of 16 on one line, **10 of 16 on lines under the grammar** (HF-116) | `agent/AGENT.md` |\n| the agent\'s write surface for a body: the lines grammar of the point, `scoped.body_lines_gbnf` | **built** (2026-10-21), guard stage 28 | `agent/body_gbnf.py` |')
    return s


def codegraph(s):
    return rep(s, '**Not built:** the kinds `type`, `custom`; a body kind on a library file (HF-103) | haro-charter, Refine |',
               '**A local model as the agent, measured 2026-10-21** (16 tasks: Qwen2.5-Coder-1.5B 3 right on a one-line body, **10 on lines under the point\'s own grammar**; HF-116, HF-117; the body\'s write surface `scoped.body_lines_gbnf`, guard stage 28). **Not built:** the kinds `type`, `custom`; a body kind on a library file (HF-103) | haro-charter, Refine |')


def spike(s):
    return rep(s, '(HF-100 to HF-103); open: the kinds `type` and `custom`, a body kind\n   on a library file (HF-103), and a write surface for a program larger than the decoder holds (HF-87).',
               '(HF-100 to HF-103); **a local model put in the loop as the agent 2026-10-21** (HF-116, HF-117: 10 of 16 tasks on lines under the point\'s grammar, 3 of 16 on the one-line body rung 5 leaves free; guard stage 28); open: the kinds `type` and `custom`, a body kind\n   on a library file (HF-103), and a write surface for a program larger than the decoder holds (HF-87).')


def charter(s):
    a = 'the charter\'s 6.2'
    return s


edit(os.path.join(AG, 'AGENT.md'), lambda s: AGENT) if os.path.exists(os.path.join(AG, 'AGENT.md')) else io.open(os.path.join(AG, 'AGENT.md'), 'w', encoding='utf-8', newline='').write(AGENT)
edit(os.path.join(ROOT, 'haro', 'FINDINGS.md'), findings)
edit(os.path.join(ROOT, 'haro', 'spike', 'v20', 'GRAMMAR.md'), v20)
edit(os.path.join(ROOT, 'haro', 'CODEGRAPH.md'), codegraph)
edit(os.path.join(ROOT, 'haro', 'SPIKE.md'), spike)
print('done')
