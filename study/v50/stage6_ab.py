"""v0.50: stage 6's cold compile, the VM before the rung (A, built from 1f1ad87's vm/) against the VM of the rung (B), on the same court
sources, alternating A B A B so a machine shared with other sessions loads both alike. Minima of N runs per round, as stage 6 takes them.

  python study/v47/stage6_ab.py [rounds] [n]
"""
import os, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPIKE = os.path.join(ROOT, 'spike')
A = os.path.join(ROOT, 'runtime', 'v50', 'oldvm', 'vm', 'zig-out', 'bin', 'haro.exe')
B = os.path.join(ROOT, 'vm', 'zig-out', 'bin', 'haro.exe')
MAKEEN = r'D:\GitHub\harobanda\machines\makeen_box.machine'
rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 4
n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
env = dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1')


def cold(vm):
    ts = []
    for _ in range(n):
        t0 = time.perf_counter()
        subprocess.run([vm, 'machine_court.haro', 'check', MAKEEN], capture_output=True, env=env, cwd=SPIKE, timeout=120)
        ts.append(time.perf_counter() - t0)
    return min(ts) * 1000


ra, rb = [], []
for r in range(rounds):
    a = cold(A)
    b = cold(B)
    ra.append(a); rb.append(b)
    print(f'round {r + 1}: A (1f1ad87) {a:6.1f} ms   B (v0.50) {b:6.1f} ms   B-A {b - a:+6.1f} ms', flush=True)
print(f'minima over {rounds} rounds of {n}: A {min(ra):.1f} ms, B {min(rb):.1f} ms, B-A {min(rb) - min(ra):+.1f} ms')
