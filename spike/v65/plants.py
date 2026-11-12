"""Every protection of v0.65 (in .ring code a decimal is Ring's number; HARO-RINGBOUNDARY-DECIMAL-OUT-01, D77) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig, lift.zig), built into runtime/v65/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v65/plants.py            all plants (about two minutes each)
  python spike/v65/plants.py G1 G3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v65', 'plant-build')
COURT = os.path.join(HERE, 'decout_court.py')

PLANTS = [
    ('G1', 'O01', 'print in .ring code writes a decimal\'s digits', MAIN,
     [('                self.say_ring = (pv.tag == .dec or pv.tag == .vec or pv.tag == .obj) and !self.strictAt(pc);',
       '                self.say_ring = (pv.tag == .dec or pv.tag == .vec or pv.tag == .obj) and pv.tag == .int and !self.strictAt(pc);')]),
    ('G2', 'O01', 'the printer ignores the reading', MAIN,
     [('                if (self.say_ring) return self.sayValue(Value.num(asF64(v)), nl);', '                if (self.say_ring and v.tag == .int) return self.sayValue(Value.num(asF64(v)), nl);')]),
    ('G3', 'O01', 'type() says DECIMAL in .ring code', MAIN,
     [('                            .dec => if (self.strictAt(pc)) "DECIMAL" else "NUMBER",', '                            .dec => "DECIMAL",')]),
    ('G4', 'O05', 'text and a decimal joined in .ring code keep the digits', MAIN,
     [('        if (mixed and (x.tag == .dec or y.tag == .dec))', '        if (mixed and x.tag == .dec and y.tag == .dec)')]),
    ('G5', 'O05', 'string() in .ring code writes a decimal\'s digits', MAIN,
     [('                            out = Value.str(self.newStr(numText(self.ringNum(v, pc), &buf)));', '                            out = Value.str(self.newStr(numText(v, &buf)));')]),
    ('G6', 'O06', 'a printed list keeps its decimals\' digits', MAIN,
     [('(pv.tag == .dec or pv.tag == .vec or pv.tag == .obj) and !self.strictAt(pc);', '(pv.tag == .dec or pv.tag == .obj) and !self.strictAt(pc);')]),
    ('G7', 'O03', 'the reading reaches .haro code too', MAIN,
     [('        return if (v.tag == .dec and !self.strictAt(pc)) Value.num(asF64(v)) else v;', '        return if (v.tag == .dec and (!self.strictAt(pc) or v.tag == .dec)) Value.num(asF64(v)) else v;')]),
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
