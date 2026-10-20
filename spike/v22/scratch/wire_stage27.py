"""Wire stage 27 (the grammar court) into haro_forge.py, preserving the file's line endings."""
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


rep('''def stage6(lang, court=None, n=15):''', '''# ---- stage 27: the write-surface grammars of the two shapes (rung 22, Haro v0.22; K4, v22/k4/K4.md)

GRAMMAR_COURT = os.path.join(HERE, 'v22', 'grammar_court.py')


def stage27():
    """The grammars a model writes under, for the Python-shaped face (v22/face_gbnf.py) and for Ring++ (v22/ringpp_gbnf.py): the engine's own decoder holds each (under its 128 rules), accepts
    the twenty K4 programs as each shape's printer writes them and every v21 fixture the grammar's core covers, rejects what the shape excludes, and a grammar broken or loosened on
    purpose is caught. No model is loaded: the court is SHAPE only, so it runs in the guard (the model runs -- k4_local.py -- do not)."""
    print('stage 27 -- the write-surface grammars: v22/grammar_court.py (held by the decoder, K4 gold accepted, exclusions rejected, controls with teeth)')
    failures = 0
    p = subprocess.run([sys.executable, GRAMMAR_COURT], capture_output=True, cwd=ROOT, timeout=3600)
    out = p.stdout.decode('utf-8', 'replace').replace(chr(13) + chr(10), chr(10))
    for line in out.splitlines():
        if (line.startswith('  ') and 'not accepted' not in line) or line.startswith('GRAMMAR COURT') or line.startswith('grammars:'):
            print(line)
    if p.returncode != 0:
        failures += 1
        print(f'  FAIL grammar_court.py exited {p.returncode}')
    if PLANT:
        failures += 1
        print('  FAIL the grammars -- PLANTED')
    return failures


def stage6(lang, court=None, n=15):''')
rep('''    if stage in (None, 26) and os.path.exists(FACE_READ_CHECK):
        failures += stage26()
''', '''    if stage in (None, 26) and os.path.exists(FACE_READ_CHECK):
        failures += stage26()
    if stage in (None, 27) and os.path.exists(GRAMMAR_COURT):
        failures += stage27()
''')
io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
print('stage 27 wired into', p)
