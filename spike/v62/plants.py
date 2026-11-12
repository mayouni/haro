"""Every protection of v0.62 (a boolean reaches a native as 1 or 0, and an object reached by a pointer is that object; HARO-NATIVE-BOOL-01, HARO-THISCHAIN-01, D74) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig), built into runtime/v62/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v62/plants.py            all plants (about two minutes each)
  python spike/v62/plants.py P1 P3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v62', 'plant-build')
COURT = os.path.join(HERE, 'native_court.py')

PLANTS = [
    ('P1', 'B01', 'a boolean argument crosses as nothing', MAIN,
     [('                        .int, .boolean => native.RppVal.int(v.p.i),', '                        .int => native.RppVal.int(v.p.i),')]),
    ('P2', 'B05', 'a boolean list item reads as 0', MAIN,
     [('        .int, .boolean => @floatFromInt(it.p.i),', '        .int => @floatFromInt(it.p.i),')]),
    ('P3', 'B05', 'a boolean list item is no number to a native', MAIN,
     [('        .int, .boolean => native.Tag.int,', '        .int => native.Tag.int,')]),
    ('P4', 'C02', 'a frame is walked whole, over its callee\'s', MAIN,
     [('                if (next > own and next - own < size) size = next - own;', '                if (next > own and next - own < size and next == 0) size = next - own;')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMP)}

    def restore():
        for p, b in originals.items():
            open(p, 'wb').write(b)
            assert digest(open(p, 'rb').read()) == digest(b)

    results = []
    try:
        for pid, fixture, why, path, subs in PLANTS:
            if want and pid not in want:
                continue
            raw = originals[path].decode('utf-8')
            crlf = '\r\n' in raw
            text = raw.replace('\r\n', '\n')
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r} ({text.count(stale[0])} found)', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(path, 'wb').write((planted.replace('\n', '\r\n') if crlf else planted).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=900)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}; failed {", ".join(failed) or "none"}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
