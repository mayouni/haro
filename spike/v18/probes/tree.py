import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cst, l1_check as ck
text = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding='latin-1').read()
p = ck.write('tree_in.ring', text)
root, src, rep = cst.recover(p)
def show(n, d=0):
    t = '' if n.kids else ' ' + repr(src[n.start:n.end][:28])
    print('  ' * d + n.kind + t)
    for k in n.kids:
        show(k, d + 1)
show(root)
print(rep)
