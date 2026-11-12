"""Every protection of v0.60 (symbols compared by name; HARO-SYMBOL-01, D72) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (compile.zig, lift.zig), built into runtime/v60/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v60/plants.py            all plants (about two minutes each)
  python spike/v60/plants.py N1 N3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v60', 'plant-build')
COURT = os.path.join(HERE, 'symbol_court.py')

PLANTS = [
    ('S1', 'Y01', 'a symbol word is read as a keyword', COMP,
     [('        if (std.mem.eql(u8, k, "symbol")) return;\n', '')]),
    ('S2', 'Y02', 'a symbol compares as a text, case kept', COMP,
     [('        if (std.mem.eql(u8, n.namedChild(1).kind(), "symbol")) return 1;\n        if (std.mem.eql(u8, n.namedChild(0).kind(), "symbol")) return 0;\n', '')]),
    ('S3', 'Y03', 'a value that is not text is compared as text', COMP,
     [('                    try out.append(self.scratch, try self.emit(.jfalsy, s, 0, 0, 0));\n                    _ = try self.emit(.bcall, t, t, 1, @intFromEnum(vm.Builtin.lower));',
       '                    _ = try self.emit(.bcall, t, t, 1, @intFromEnum(vm.Builtin.lower));')]),
    ('S4', 'Y04', 'the text is not lowered', COMP,
     [('                    try out.append(self.scratch, try self.emit(.jfalsy, s, 0, 0, 0));\n                    _ = try self.emit(.bcall, t, t, 1, @intFromEnum(vm.Builtin.lower));\n                    try out.append(self.scratch, try self.emit(.jne, t, kr, 0, 0));',
       '                    try out.append(self.scratch, try self.emit(.jfalsy, s, 0, 0, 0));\n                    try out.append(self.scratch, try self.emit(.jne, t, kr, 0, 0));')]),
    ('S5', 'Y02', 'a symbol comparison as a value takes cmpv', COMP,
     [('            if ((self.classOf(ln) == .ref or self.classOf(rn) == .ref) and self.symbolSide(n) == null) {',
       '            if (self.classOf(ln) == .ref or self.classOf(rn) == .ref) {')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMP, LIFT)}

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
