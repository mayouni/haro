"""Does a grammar accept each of several texts? usage: gc_text.py ringpp|face  (texts on stdin separated by a line holding only ===; the sentinel is added)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import grammar_court as gc

shape = sys.argv[1]
g = gc.ringpp_gbnf.ringpp_grammar() if shape == 'ringpp' else gc.face_gbnf.face_grammar()
texts = sys.stdin.read().split('\n===\n')
jobs = [('t%d' % i, 'x', g, gc.with_end(t)) for i, t in enumerate(texts)]
for (lab, _, _, s), (r, a) in zip(jobs, gc.run_batch(jobs)):
    print('ACCEPT' if a else 'no    ', repr(texts[int(lab[1:])][:90]), r)
