"""Every protection of v0.57 (one way to print: print, and ? its shortcut; HARO-PRINT-01, D69) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (compile.zig, lift.zig), built into runtime/v57/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v57/plants.py            all plants (about two minutes each)
  python spike/v57/plants.py N1 N3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v57', 'plant-build')
COURT = os.path.join(HERE, 'print_court.py')

PLANTS = [
    ('P1', 'R01', 'print is not given to the parser as ?', LIFT,
     [('        @memcpy(text[e + shift .. e + shift + 5], "?    ");', '        _ = text[e + shift];')]),
    ('P2', 'R01', 'a file with print and no definition is not rewritten', LIFT,
     [('    if (heads.items.len == 0 and prints.items.len == 0) return null;', '    if (heads.items.len == 0) return null;')]),
    ('P3', 'R04', 'see passes', COMP,
     [('            .{ .w = "see", .p = "see_statement", .why = "one spelling: `print`; written" },', '')]),
    ('P4', 'R05', 'put passes', COMP,
     [('            .{ .w = "put", .p = "see_statement", .why = "one spelling: `print`; written" },', '')]),
    ('P5', 'R08', 'a definition named print is rewritten as ?', LIFT,
     [('            if (!after_def) prints.append(alloc, @intCast(s)) catch return null;', '            prints.append(alloc, @intCast(s)) catch return null;')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (COMP, LIFT)}

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
