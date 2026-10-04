import os, sys, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import l1, l1_check as ck
path = sys.argv[1]
text = ck.read_text(path)
g, why = ck.to_l1(text, 'fd.ring')
canon = l1.print_ring(g)
open(os.path.join(HERE, '..', 'scratch', 'fd_canon.ring'), 'w', encoding='latin-1', newline='').write(canon)
a = ck.dis(ck.strip_loads(text), "fd_o.ring"); b = ck.dis(ck.strip_loads(canon), "fd_k.ring")
print('rc', a[0], b[0])
n = 0
for line in difflib.unified_diff(a[1].split('\n'), b[1].split('\n'), 'original', 'canonical', lineterm='', n=1):
    print(line[:170]); n += 1
    if n > int(sys.argv[2] if len(sys.argv) > 2 else 40): break
