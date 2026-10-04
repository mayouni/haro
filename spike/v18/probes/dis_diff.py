import os, sys, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import l1, l1_check as ck

want = sys.argv[1]
fx = {f['id']: f for f in ck.read_fixtures(os.path.join(os.path.dirname(HERE), 'fixtures.txt'))}[want]
g, why = ck.to_l1(fx['ring'], 'dd.ring')
canon = l1.print_ring(g)
a = ck.dis(fx['ring'], 'dd_o.ring')
b = ck.dis(canon, 'dd_k.ring')
print('rc', a[0], b[0])
for line in difflib.unified_diff(a[1].split('\n'), b[1].split('\n'), 'original', 'canonical', lineterm='', n=2):
    print(line[:160])
print('---- canonical text:')
print(canon)
