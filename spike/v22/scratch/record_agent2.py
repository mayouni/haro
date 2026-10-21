"""The charter paragraph, the journal memo and CONCLUSIONS line, and the memory notes for rung 5 with a model as the agent."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
MEMO = r'D:\GitHub\softanza\memos\2026-10-21.md'
CONC = r'D:\GitHub\softanza\dashboard\CONCLUSIONS.md'
MEM = r'C:\Users\ASUS V3607V CORE 5\.claude\projects\D--GitHub-ringpp\memory'
CR, LF = chr(13), chr(10)


def rw(path, fn):
    raw = io.open(path, encoding='utf-8', newline='').read()
    nl = CR + LF if CR + LF in raw else LF
    s = fn(raw.replace(CR + LF, LF))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
    print('edited', path)


CHARTER_PARA = ('**A local model as the agent of a refinement, measured, 2026-10-21, on the author\'s "decide on my behalf and start the work"** (`haro/spike/v20/agent/AGENT.md`; HF-116, HF-117). Rung 5\'s court had never put a model in the loop: its agent was a harness. '
                'Sixteen refinement tasks (a BLOCK or FUNCTION point, its allowlists, a function\'s body to write, two data sets), the gate as judge, rnxc running the refined program, the harness proven on gold answers first (guard stage 28). '
                'Qwen2.5-Coder-1.5B gets **3 of 16 right on both data sets when it writes the one-line TO that `scoped.py` leaves as free text, and 10 of 16 when it writes lines under the point\'s own grammar** and the harness flattens them into the TO; '
                'the 0.5B 0 and 3, SmolLM2-135M 1 and 0. **For a body kind the charter\'s 6.2 ("the agent\'s only write surface is a sentence") becomes: the agent writes the body, as lines, under a grammar scoped to its point '
                '(`scoped.body_lines_gbnf`), and the harness writes the sentence around it** -- a decision for the author\'s reading, not yet his. Three of the six failures are a body that does not end, and a GBNF cannot say "an identifier that is not a keyword" (HF-117).\n\n')


def charter(s):
    marker = '**A second face of the program graph, built, 2026-10-19, on the author\'s "go ahead with rung 6"**'
    assert s.count(marker) == 1, s.count(marker)
    return s.replace(marker, CHARTER_PARA + marker)


memo = '''
## ringpp — Haro rung 5 with a local model as the agent: a one-line body is the wrong ask; lines under the point's grammar take the 1.5B from 3 of 16 to 10 of 16

```yaml
by:        ringpp · claude-sonnet-5-5 · 2026-10-21
subject:   a real model, for the first time, as the agent of rung 5's refinement loop (the BLOCK and FUNCTION kinds): sixteen tasks, the gate as judge, the program run on shown and substituted data
why:       the author said "decide on my behalf and start the work" after asking what is next; the one thing rung 5 had never had was a model in the loop

did:
  - decided on his behalf: C-33 (new K() on a class with no init keeps making the object on Ring++; Haro's new(Name) is to refuse it loudly -- not built), the three engine fixes go ahead through prompt 55, v2.0.4 waits for his word (publishing is outward-facing; the wide pass has not been rerun on the `not` fix)
  - built haro/spike/v20/agent/: tasks.py (16 tasks), r5_agent.py (the harness, proven on gold answers), body_gbnf.py (the body grammar scoped to a point, one line and as lines, held by the decoder), body_court.py, r5_local.py (resumable runner), scoped.body_lines_gbnf (the grammar derived from a program's own point); guard stage 28 (no model loaded)
  - measured four ways of asking for the body on three models (3 x 4 x 16 jobs)

found:
  - right on both data sets, 1.5B / 0.5B / SmolLM2-135M: one line free (rung 5's write surface as it stands) 3 / 0 / 1; one line under the grammar 3 / 0 / 1; lines free 7 / 2 / 0; lines under the point's grammar 10 / 3 / 0 (HF-116)
  - the decoder-held grammar improved correctness for the first time in this work, but only once the shape was natural: the model writes lines, the harness flattens them into TO, the gate sees the same body
  - a GBNF cannot say "an identifier that is not a keyword"; three of the 1.5B's six failures are a body that never ends (HF-117, ENGINE_NOTES.md section 3)
  - the pool margin: +25% fails a 368-token prompt on the 1.5B by 1.1 MB; the engine copy now carries +25% and a constant gigabyte, and ENGINE_NOTES, K4, HF-113 and prompt 55 say so

waiting:
  - the author: the charter amendment for body kinds (the agent writes the body under the point's grammar; the sentence is the harness's) -- recorded as a decision for his reading in CHARTER, v20/agent/AGENT.md and HF-116; the engine decisions in prompt 55; whether to publish the `not` fix as v2.0.4

next:
  - me:      not run, and could move the numbers: a Softanza-naming identifier in the body grammar (nName, cName ... so `oknextreturn` cannot be written), a METHOD point, a tempting forbidden call, models above 1.5B, sampling with a repetition remedy
  - author:  the decisions above
```
'''
conc = ('2026-10-21 | ringpp | HARO RUNG 5 WITH A MODEL AS THE AGENT, MEASURED (HF-116, HF-117): Qwen2.5-Coder-1.5B writes 3 of 16 refinement bodies right as one line (rung 5\'s write surface today) and 10 of 16 as lines under the point\'s own grammar, flattened by the harness; '
        'the 0.5B 0 and 3; the decoder-held grammar improves correctness only once the shape is natural; a GBNF cannot exclude keywords from identifiers; guard stage 28; C-33 decided (new K() without init keeps making the object)')


def append(path, text, one_line):
    raw = io.open(path, 'rb').read()
    stripped = raw.rstrip(b'\r\n')
    k = stripped.rfind(b'\n')
    crlf = k > 0 and stripped[k - 1:k] == b'\r'
    nl = (CR + LF) if crlf else LF
    body = text if one_line else text.lstrip(LF)
    out = (b'' if raw.endswith(b'\n') else nl.encode()) + (b'' if one_line else nl.encode()) + body.replace(LF, nl).encode('utf-8') + (nl.encode() if not body.endswith(LF) else b'')
    with io.open(path, 'ab') as f:
        f.write(out)
    print('appended to', path)


NOTE = '''---
name: rung5-agent-with-model
description: "Haro rung 5 with a LOCAL MODEL as the agent (2026-10-21): the harness, the body grammars, the results (1.5B 3 of 16 on a one-line body, 10 of 16 on lines under the point's grammar), and what is open"
metadata:
  node_type: memory
  type: project
---

**Built 2026-10-21 on "decide on my behalf and start the work"** (private/next cb77bec..): `haro/spike/v20/agent/` -- tasks.py (16 refinement tasks, BLOCK + FUNCTION, two data sets), r5_agent.py (judge: the gate via `refine.Model.refine`, then rnxc on shown AND substituted
data), body_gbnf.py (body grammar scoped to a point: one line, or LINES with a closing `<<END>>`; `expr_rules` shared), body_court.py, r5_local.py (runner, resumable, `judge` for partial runs), `scoped.body_lines_gbnf(model, name)`, guard stage 28 (no model).

**Result (HF-116):** right on both data sets, 1.5B / 0.5B / SmolLM2: one line free 3/0/1 (rung 5's write surface as `qbody` leaves it), one line scoped 3/0/1, lines free 7/2/0, **lines scoped 10/3/0**. The model writes lines, the harness flattens into TO; the gate sees the same body.
Decision for his reading: for BODY kinds the agent writes the body under the point's grammar and the harness writes the sentence (amends charter 6.2; recorded in CHARTER, AGENT.md, HF-116).

**Open:** HF-117 (a GBNF cannot exclude keywords from identifiers; 3 of 6 failures never end -- try Softanza's nName/cName/aName naming convention as the identifier shape; and the engine's missing repetition penalty), a METHOD point, a tempting forbidden call, models above 1.5B, sampling.

**Lessons:** shell heredocs mangle backslashes AGAIN -- write script FILES with the Write tool; my first prompt omitted a function point's parameters (R13-R15 failed) -- keep `local/v1-no-params/`; the engine pool margin must be constant+percent (see [[softanza-local-models]]); other sessions' python processes (e.g. tools/intro_run.py) share this machine.
Related: [[rung7-reader-resume]], [[block-kind-resume]], [[rung5-resume]].
'''


def index(s):
    if '[Rung 5 with a model]' in s:
        return s
    return s.rstrip(LF) + LF + '- [Rung 5 with a model](rung5-agent-with-model.md) — 2026-10-21: a local model as the agent of rung 5; 1.5B 3/16 on a one-line body, 10/16 on lines under the point\'s grammar (HF-116/117); decision for his reading: for body kinds the agent writes the body, the harness the sentence.' + LF


rw(os.path.join(ROOT, 'haro', 'CHARTER.md'), charter)
append(MEMO, memo, False)
append(CONC, conc, True)
io.open(os.path.join(MEM, 'rung5-agent-with-model.md'), 'w', encoding='utf-8', newline='').write(NOTE)
rw(os.path.join(MEM, 'MEMORY.md'), index)
print('done')
