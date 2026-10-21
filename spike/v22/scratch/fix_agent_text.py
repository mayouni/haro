"""Correct the account of the six failures of the 1.5B on lines under the grammar: three never end (R02 glued the closers into an identifier, R06 repeated a line, R05 ran an identifier on and the compiler's own check refused it),
two were admitted and errored when run (R07 wrote `/ next` for a downward step, R15 used the call site's names), one admitted and wrong (R14, 0-based)."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
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


def agent(s):
    a = s.index('- **What is left, for the 1.5B on lines under the grammar**')
    b = s.index('\n\n## Limits, stated')
    new = ("- **What is left, for the 1.5B on lines under the grammar** (six of sixteen): **three never end** -- R02 glued its closers into an identifier (`oknextreturnf *= i`) and repeated it to the token cap, which the grammar allows "
           "because a GBNF cannot say \"an identifier that is not a keyword\"; R06 repeated a line; R05 ran an identifier on (`minmaxmax...`) until the compiler's own check refused it (`derivation`: a name nothing assigns). "
           "**Two were admitted and errored when run**: R07 wrote `/ next` where a downward loop needs `step -1`, and R15 used the call site's variable names (`cA + '-' + cB`) although the prompt lists the function's parameters. "
           "**One was admitted and wrong**: R14 took `aL[len(aL) - 1]`, a 0-based index in a 1-based language. The first run of every arm lacked the parameter list in the prompt of a function that does not exist yet "
           "(`local/v1-no-params/`, kept): that was the prompt's defect and all arms were re-run.")
    return s[:a] + new + s[b:]


def findings(s):
    return rep(s, 'Under the lines grammar Qwen2.5-Coder-1.5B left 3 of 16 bodies without an end: one repeated a line to the token cap, two glued the closers into an identifier (`oknextreturnf *= i`, valid because `id` is `[A-Za-z_][A-Za-z0-9_]*`) and went on.',
               'Under the lines grammar Qwen2.5-Coder-1.5B left 3 of 16 bodies without an end: one glued its closers into an identifier (`oknextreturnf *= i`, valid because `id` is `[A-Za-z_][A-Za-z0-9_]*`) and repeated it to the token cap, one repeated a line, one ran an identifier on (`minmaxmax...`) until the compiler\'s own check refused it.')


edit(os.path.join(ROOT, 'haro', 'spike', 'v20', 'agent', 'AGENT.md'), agent)
edit(os.path.join(ROOT, 'haro', 'FINDINGS.md'), findings)
