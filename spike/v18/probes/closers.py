import subprocess, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
SCRATCH = os.path.join(HERE, '..', 'scratch')
os.makedirs(SCRATCH, exist_ok=True)
ORACLE = paths.RING
RNXC = paths.RNXC
def run(exe, text):
    open(os.path.join(SCRATCH, 'cl.ring'), 'w').write(text)
    args = [exe, os.path.join(SCRATCH, 'cl.ring')] if exe == ORACLE else [exe, 'exec', os.path.join(SCRATCH, 'cl.ring')]
    r = subprocess.run(args, capture_output=True, timeout=60)
    out = r.stdout.decode('latin-1').replace('\r', '')
    out = [l for l in out.split('\n') if l and not l.startswith(('files ', 'running', 'TOP LEVEL'))]
    return ' / '.join(out)
for closer in ['end', 'endfunc', 'endclass', 'ok', 'next', 'done', 'off', 'endif', '}']:
    body = '\t? "in F"\n' + closer + '\n? "after"\n'
    if closer == '}':
        body = '{\n\t? "in F"\n}\n? "after"\n'
        text = '? "top1"\nF()\nF()\nfunc F()' + (' ' if closer == '}' else '\n') + body
    else:
        text = '? "top1"\nF()\nF()\nfunc F()\n' + body
    print(f'{closer:9s} oracle: {run(ORACLE, text):60s} rnxc: {run(RNXC, text)}')
