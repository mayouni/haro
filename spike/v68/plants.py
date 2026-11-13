"""Every protection of v0.68 (in .ring code a boolean is the number 1 or 0; HARO-RINGBOUNDARY-BOOL-OUT-01, D80) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig), built into runtime/v68/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v68/plants.py            all plants (about two minutes each)
  python spike/v68/plants.py K1 K3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v68', 'plant-build')
COURT = os.path.join(HERE, 'boolout_court.py')

PLANTS = [
    ('K1', 'B01', 'a boolean prints its word in .ring code', MAIN,
     [('.boolean => if (self.say_ring) outPrint(', '.boolean => if (self.say_ring and v.p.i == 99) outPrint(')]),
    ('K2', 'B01', "the print op does not flag a boolean as .ring code's", MAIN,
     [('const wide = pv.tag == .dec or pv.tag == .num or pv.tag == .vec or pv.tag == .obj or pv.tag == .boolean;', 'const wide = pv.tag == .dec or pv.tag == .num or pv.tag == .vec or pv.tag == .obj;')]),
    ('K3', 'B03', 'type() says BOOLEAN in .ring code', MAIN,
     [('.boolean => if (self.strictAt(pc)) "BOOLEAN" else "NUMBER",', '.boolean => if (self.strictAt(pc)) "BOOLEAN" else "BOOLEAN",')]),
    ('K4', 'B03', 'isNumber is 0 in .ring code', MAIN,
     [('(regs[A].tag == .boolean and !self.strictAt(pc))) 1 else 0),', '(regs[A].tag == .boolean and pc == 0xFFFFFFFF)) 1 else 0),')]),
    ('K5', 'B04', 'string() writes the word in .ring code', MAIN,
     [('(if (v.p.i != 0) "1" else "0")', '(if (v.p.i != 0) "true" else "false")')]),
    ('K6', 'B04', 'number() refuses a boolean', MAIN,
     [('!(regs[A].tag == .boolean and !self.strictAt(pc))) {', '!(regs[A].tag == .boolean and pc == 0xFFFFFFFF)) {')]),
    ('K7', 'B04', 'list2str drops a boolean', MAIN,
     [('} else if (e.tag == .boolean and !self.strictAt(pc)) {', '} else if (e.tag == .boolean and pc == 0xFFFFFFFF) {')]),
    ('K8', 'B06', 'find() keeps a boolean apart from its number in .ring code', MAIN,
     [('                        const ring = !self.strictAt(pc);\n                        var found: i64 = 0;', '                        const ring = pc == 0xFFFFFFFF;\n                        var found: i64 = 0;')]),
    ('K9', 'B06', 'sort() keeps a boolean apart from its number in .ring code', MAIN,
     [('.ring = !self.strictAt(pc) }, sortLess);', '.ring = pc == 0xFFFFFFFF }, sortLess);')]),
    ('K10', 'B11', 'a boolean does not find a boolean', MAIN,
     [('        if (a.tag == .boolean and b.tag == .boolean) return a.p.i == b.p.i;\n', '')]),
    ('K11', 'B09', '.haro code prints a boolean as 1 or 0', MAIN,
     [('self.say_ring = wide and pv.tag != .num and !strict_say;', 'self.say_ring = wide and pv.tag != .num;')]),
    ('K12', 'B09', 'String() writes 1 or 0 in .haro code', MAIN,
     [('out = Value.str(self.newStr(if (!self.strictAt(pc)) (if (v.p.i != 0) "1"', 'out = Value.str(self.newStr(if (!(pc == 0xFFFFFFFF)) (if (v.p.i != 0) "1"')]),
    ('K13', 'B09', 'Type() says NUMBER in .haro code', MAIN,
     [('.boolean => if (self.strictAt(pc)) "BOOLEAN" else "NUMBER",', '.boolean => if (pc == 0xFFFFFFFF) "BOOLEAN" else "NUMBER",')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN,)}

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
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=1800)
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
