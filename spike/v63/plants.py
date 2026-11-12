"""Every protection of v0.63 (a .ring number crossing into .haro is an exact decimal; HARO-RINGBOUNDARY-NUMBER-01, D75) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig), built into runtime/v63/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v63/plants.py            all plants (about two minutes each)
  python spike/v63/plants.py Q1 Q3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v63', 'plant-build')
COURT = os.path.join(HERE, 'number_court.py')

PLANTS = [
    ('Q1', 'M01', 'a parameter given a .ring float keeps it', MAIN,
     [("        if (in.c == 1 and v.tag == .num and in.b != 'f' and fsp > 0 and", "        if (in.c == 1 and v.tag == .num and in.b != 'f' and fsp > 0 and fsp == 0 and")]),
    ('Q2', 'M01', 'an unchecked parameter gets no check at the entry', COMP,
     [("                    if (pl != 'f') _ = try c.emit(.lchk, lp.reg, pl, 1, try c.konstIndex(p));", "                    if (pl == 0) _ = try c.emit(.lchk, lp.reg, pl, 1, try c.konstIndex(p));")]),
    ('Q3', 'M04', 'a .ring function\'s float answered to .haro stays a float', MAIN,
     [("                if (in.b == 1 and result.tag == .num and self.strictAt(fr.ret_pc -| 1)) {", "                if (in.b == 7 and result.tag == .num and self.strictAt(fr.ret_pc -| 1)) {")]),
    ('Q4', 'M04', 'a .ring function\'s return does not say so', COMP,
     [("            const ring_ret: u8 = if (self.haroNode(n)) 0 else 1;", "            const ring_ret: u8 = if (self.haroNode(n)) 0 else 0;")]),
    ('Q5', 'M02', 'the decimal is not the shortest text', MAIN,
     [('        const s = std.fmt.bufPrint(&buf, "{d}", .{d}) catch return null;', '        const s = std.fmt.bufPrint(&buf, "{d:.20}", .{d}) catch return null;')]),
    ('Q6', 'M06', 'a .haro caller\'s float is converted too', MAIN,
     [("in.b != 'f' and fsp > 0 and !self.strictAt(self.frames[fsp - 1].ret_pc -| 1)) {", "in.b != 'f' and fsp > 0) {")]),
    ('Q7', 'M08', 'an f parameter is converted too', MAIN,
     [("        if (in.c == 1 and v.tag == .num and in.b != 'f' and fsp > 0 and", "        if (in.c == 1 and v.tag == .num and fsp > 0 and")]),
    ('Q8', 'M09', 'a .ring function\'s float answered to a .ring caller is converted', MAIN,
     [("                if (in.b == 1 and result.tag == .num and self.strictAt(fr.ret_pc -| 1)) {", "                if (in.b == 1 and result.tag == .num) {")]),
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
