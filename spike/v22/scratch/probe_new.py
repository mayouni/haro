"""`new K()` on a class with no init, and `new K` against `new K()` on a class with one: the oracle (Ring 1.27) against rnxc (Ring++)."""
import os, subprocess, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
ORACLE = os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
RNXC = os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
d = tempfile.mkdtemp()
PROGS = {
    'no init, new K()': 'o = new K()\n? "made"\n\nclass K\n\tn = 0\n',
    'no init, new K': 'o = new K\n? "made"\n\nclass K\n\tn = 0\n',
    'init, new K': 'o = new K\n? "after"\n\nclass K\n\tfunc init()\n\t\t? "init ran"\n',
    'init, new K()': 'o = new K()\n? "after"\n\nclass K\n\tfunc init()\n\t\t? "init ran"\n',
    'init(a), new K(1)': 'o = new K(1)\n? "after"\n\nclass K\n\tfunc init(a)\n\t\t? "init " + a\n',
}
for label, src in PROGS.items():
    p = os.path.join(d, 'p.ring')
    open(p, 'w').write(src)
    res = []
    for exe in (ORACLE, RNXC):
        r = subprocess.run([exe, p], capture_output=True, stdin=subprocess.DEVNULL)
        res.append((r.stdout + r.stderr).decode('latin-1').strip().replace('\r\n', ' | ').replace(p, '<f>')[:70])
    print('%-20s oracle %-42s rnxc %-30s %s' % (label, res[0], res[1], '' if res[0] == res[1] else '<-- DIFFERENT'))
