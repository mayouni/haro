"""Bisect a text the grammar does not accept: which prefix (by lines) is the longest the decoder accepts as a COMPLETE program? usage: gc_probe.py ringpp|face <task id or fixture id>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import grammar_court as gc

shape, which = sys.argv[1], sys.argv[2]
if which.startswith('T'):
    t = next(t for t in gc.K4TASKS.TASKS if t['id'] == which)
    ring = gc.with_data(t)
else:
    f = next(f for f in gc.face_check.read_fixtures(os.path.join(HERE, '..', '..', 'v21', 'fixtures.txt')) if str(f['id']) == which)
    ring = f['ring']
text = gc.fmt_ring(ring) if shape == 'ringpp' else gc.face_text(ring)
g = gc.ringpp_gbnf.ringpp_grammar() if shape == 'ringpp' else gc.face_gbnf.face_grammar()
print(text)
lines = text.split('\n')
jobs = [('p%d' % n, 'x', g, gc.with_end('\n'.join(lines[:n]))) for n in range(1, len(lines) + 1)]
res = gc.run_batch(jobs)
for (lab, _, _, _), (r, a) in zip(jobs, res):
    print(lab, 'ACCEPT' if a else 'no', r)
