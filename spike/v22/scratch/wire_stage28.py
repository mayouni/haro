"""Wire stage 28 (the body-grammar court of rung 5's agent) into haro_forge.py, preserving the file's line endings."""
import io, os

p = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'haro_forge.py'))
raw = io.open(p, encoding='utf-8', newline='').read()
CR, LF = chr(13), chr(10)
nl = CR + LF if CR + LF in raw else LF
s = raw.replace(CR + LF, LF)


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)


rep('''def stage6(lang, court=None, n=15):''', '''# ---- stage 28: the agent's body grammar (rung 5, a model as the agent; v20/agent/AGENT.md)

BODY_COURT = os.path.join(HERE, 'v20', 'agent', 'body_court.py')
AGENT_SELFTEST = os.path.join(HERE, 'v20', 'agent', 'r5_agent.py')


def stage28():
    """The write surface of a body, scoped to its point (v20/agent/body_gbnf.py), and the tasks a model is measured on (v20/agent/tasks.py): the sixteen gold bodies each admitted by the gate and
    right on both data sets (rnxc and the oracle agreeing), a body that returns the shown answer admitted and wrong on the other, four forbidden shapes refused at their stage; the one-line and the
    lines grammar each held by the engine's decoder with every gold body accepted, what the gate would refuse for the shape rejected, a broken and a loosened grammar caught, and the grammar derived
    from a program's own point identical to the task-built one. No model is loaded: the model runs (r5_local.py) are measurements, not guards."""
    print('stage 28 -- the agent's body grammar: v20/agent/r5_agent.py selftest and v20/agent/body_court.py (no model loaded)')
    failures = 0
    for label, script, args in (('selftest', AGENT_SELFTEST, ['selftest']), ('body court', BODY_COURT, [])):
        p = subprocess.run([sys.executable, script] + args, capture_output=True, cwd=ROOT, timeout=3600)
        out = p.stdout.decode('utf-8', 'replace').replace(chr(13) + chr(10), chr(10))
        for line in out.splitlines():
            if line.startswith('  ') or line.startswith('r5_agent selftest') or line.startswith('BODY COURT') or 'grammar:' in line:
                print(line)
        if p.returncode != 0:
            failures += 1
            print(f'  FAIL {label} exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the agent's body grammar -- PLANTED')
    return failures


def stage6(lang, court=None, n=15):''')
rep('''    if stage in (None, 27) and os.path.exists(GRAMMAR_COURT):
        failures += stage27()
''', '''    if stage in (None, 27) and os.path.exists(GRAMMAR_COURT):
        failures += stage27()
    if stage in (None, 28) and os.path.exists(BODY_COURT):
        failures += stage28()
''')
io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
print('stage 28 wired into', p)
