import subprocess
import os
HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
SCRATCH = os.path.join(HERE, '..', 'scratch')
os.makedirs(SCRATCH, exist_ok=True)
ORACLE = paths.RING_ORACLE
RNXC = paths.HARO_VM
def run(exe, text):
    open(os.path.join(SCRATCH, 'fl.ring'), 'w').write(text)
    args = [exe, os.path.join(SCRATCH, 'fl.ring')] if exe == ORACLE else [exe, 'exec', os.path.join(SCRATCH, 'fl.ring')]
    r = subprocess.run(args, capture_output=True, timeout=60)
    out = r.stdout.decode('latin-1').replace('\r', '')
    out = [l for l in out.split('\n') if l and not l.startswith(('files ', 'running', 'TOP LEVEL'))]
    return ' / '.join(out)
cases = {
 'class braces, method falls off, stmt after class': '? "top1"\no = new A\no.F()\no.F()\nclass A {\n\tfunc F() {\n\t\t? "in F"\n\t}\n}\n? "after class"\n',
 'class end, method falls off, stmt after': '? "top1"\no = new A\no.F()\nclass A\n\tfunc F()\n\t\t? "in F"\n\tend\nend\n? "after class"\n',
 'class no end, stmt after method': '? "top1"\no = new A\no.F()\nclass A\n\tfunc F()\n\t\t? "in F"\n? "after method"\n',
 'two funcs, stmt between': '? "top1"\nF()\nG()\nfunc F()\n\t? "in F"\n? "between"\nfunc G()\n\t? "in G"\n? "tail"\n',
 'func then class then stmt': '? "top1"\nF()\nfunc F()\n\t? "in F"\nclass K\n\tx = 1\n? "after K"\n',
}
for k, t in cases.items():
    print(f'{k}\n   oracle: {run(ORACLE, t)}\n   rnxc  : {run(RNXC, t)}')
