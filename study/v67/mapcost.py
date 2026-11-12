"""A map read's cost against its size: 200,000 reads of the last key, minimum of 5 runs, minus the same loop without the read."""
import os, subprocess, sys, time

EXE = sys.argv[1]
DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'runtime', 'v67', 'mapcost')
os.makedirs(DIR, exist_ok=True)
READS = 200000


def prog(n, read):
    body = '\tiV = mX[' + str(n) + '] else 0\n' if read else '\tiV = ' + str(n) + '\n'
    return ('mX = [:]\nfor i = 1 to ' + str(n) + '\n\tmX[i] = i\nend\niV = 0\nfor j = 1 to ' + str(READS) + '\n' + body + 'end\n'
            'print iV\n')


def best(path):
    t = []
    for _ in range(5):
        t0 = time.perf_counter()
        r = subprocess.run([EXE, path], capture_output=True)
        t.append(time.perf_counter() - t0)
        assert r.returncode == 0, r.stdout + r.stderr
    return min(t)


for n in (1, 10, 100, 1000):
    times = []
    for read in (False, True):
        p = os.path.join(DIR, f'm{n}_{int(read)}.haro')
        open(p, 'w', newline='\n').write(prog(n, read))
        times.append(best(p))
    per = (times[1] - times[0]) / READS * 1e9
    print(f'size {n:>5}: {per:8.0f} ns per read  (loop {times[0]*1e3:.0f} ms, with reads {times[1]*1e3:.0f} ms)')
