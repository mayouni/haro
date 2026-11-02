"""Which of Softanza's Ring files does `rnxc fmt` refuse (the parser reports an error in them), and where do they live? HF-80. Run it from the
repository root; RNXC= names the compiler. Then ask Ring itself: `ring file -norun` raises an error on each (45 an unclosed comment, S2)."""
import glob, os, subprocess, collections
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
import paths
RN = paths.RNXC
STZ = r'D:\GitHub\stzlib\libraries\stzlib'
stz = sorted(p for p in glob.glob(os.path.join(STZ, '**', '*.ring'), recursive=True) if os.path.getsize(p) <= 400000)
ref = []
for i in range(0, len(stz), 200):
    r = subprocess.run([RN, 'fmt', '--check'] + stz[i:i + 200], capture_output=True)
    for line in r.stderr.decode('latin-1').splitlines():
        if 'nothing printed' in line:
            ref.append(line.split(': the parser')[0].replace('rnxc fmt: ', ''))
by = collections.Counter()
lib = []
for p in ref:
    rel = os.path.relpath(p, STZ).replace(chr(92), '/')
    if '/archive/' in rel:
        by['archive'] += 1
    elif '/test/' in rel:
        by['test'] += 1
    else:
        by['library'] += 1
        lib.append(rel)
print(len(ref), dict(by))
print(lib)
