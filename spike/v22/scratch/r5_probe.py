"""Probe: one refinement task through rung 5's gate, by hand -- the program, the lift (the FROM the sentence must carry), the sentence, the outcome, the program after, its output on rnxc."""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V20 = os.path.abspath(os.path.join(HERE, '..', '..', 'v20'))
sys.path.insert(0, V20)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'v18')))
import refine

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
RNXC = os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')

PROGRAM = '''nN = 5
? SumTo(nN)

# <R:BLOCK name="sumto" calls="">
func SumTo(n)
'''

m = refine.Model(PROGRAM, {})
print('canonical text equal to the program:', m.text() == PROGRAM)
print('lift:', m.lift()['points'][0]['name'], m.lift()['points'][0]['kind'], repr(m.lift()['points'][0]['value']), m.lift()['points'][0]['attrs'])
frm = m.lift()['points'][0]['value']
body = "nS = 0 for i = 1 to n nS += i next return nS"
sent = 'DEFINE REFINE write_sumto AS ( TARGET "sumto", KIND block, FROM "%s", TO "%s", AUTHOR "mansour", POSTURE trusted, REASON "sum to n" )' % (frm, body)
out = m.refine(sent)
print('admitted:', out.admitted, 'status:', out.status, 'stage:', out.stage, 'why:', out.why)
print(m.text())
d = tempfile.mkdtemp(prefix='r5_')
p = os.path.join(d, 'p.ring')
open(p, 'w').write(m.text())
r = subprocess.run([RNXC, p], capture_output=True, timeout=30)
print('rnxc says:', r.stdout.decode('latin-1').strip(), r.stderr.decode('latin-1').strip()[:200])
# a forbidden call and a comment, to see the stages
for label, b in (('forbidden call', "return floor(n)"), ('double quote', 'return "x"'), ('a func', 'func X() return 1')):
    m2 = refine.Model(PROGRAM, {})
    o2 = m2.refine('DEFINE REFINE w AS ( TARGET "sumto", KIND block, FROM "%s", TO "%s", AUTHOR "mansour", POSTURE trusted, REASON "r" )' % (frm, b))
    print(label, '->', o2.status, o2.stage, (o2.why or '')[:90])
