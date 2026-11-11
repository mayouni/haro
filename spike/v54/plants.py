"""Every protection of v0.54 (the p mark and a vector's element letter, HARO-LETTER-SOFTANZA-01, D66) switched off in turn: the court must fail, for the
fixture that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig), built into runtime/v54/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v54/plants.py            all plants (about two minutes each)
  python spike/v54/plants.py Q1 Q3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v54', 'plant-build')
COURT = os.path.join(HERE, 'letter2_court.py')
NL = chr(10)

PLANTS = [
    ('M1', 'L01', 'the p mark is read as a letter', COMP,
     [("        if (core.len >= 3 and core[0] == 'p' and std.ascii.isLower(core[1]) and",
       "        if (false and core.len >= 3 and core[0] == 'p' and std.ascii.isLower(core[1]) and")]),
    ('M2', 'L02', 'a p parameter is checked by p, no letter', COMP,
     [('            p = true;' + NL + '            core = core[1..];', '            p = true;' + NL + '            core = core[0..];')]),
    ('M3', 'L04', 'a p name that is no parameter passes', COMP,
     [('        if (marked and !self.isParam(use)) {', '        if (false and marked and !self.isParam(use)) {')]),
    ('M4', 'L03', 'no name is a parameter', COMP,
     [('            if (std.mem.eql(u8, pm, name)) return true;', '            if (std.mem.eql(u8, pm, name)) return false;')]),
    ('M5', 'L06', 'the VM checks no item', MAIN,
     [('                if (in.c != 0 and v.tag == .vec and !v.p.v.closure) {', '                if (false and in.c != 0 and v.tag == .vec and !v.p.v.closure) {')]),
    ('M6', 'L06', 'the compiler sends no element letter', COMP,
     [("        const e: u8 = if (letterParts(use)) |pp| (if (pp.e != 0 and std.mem.indexOfScalar(u8, CHECKED, pp.e) != null) pp.e else 0) else 0;",
       "        const e: u8 = if (letterParts(use)) |pp| (if (false and pp.e != 0) pp.e else 0) else 0;")]),
    ('M7', 'L06', 'a vector literal settles the items too', COMP,
     [('                if (pp.e != 0) settled = false;', '                if (pp.e != 0 and false) settled = false;')]),
    ('M8', 'L07', 'a value that is no vector is named as for a plain v', MAIN,
     [('                    if (in.c != 0) {' + NL + '                        self.pending = self.haroMsg("Error (TYPE_LETTER) : `{s}` is lettered v{c}, a vector of {s}, and is given {s}"',
       '                    if (false) {' + NL + '                        self.pending = self.haroMsg("Error (TYPE_LETTER) : `{s}` is lettered v{c}, a vector of {s}, and is given {s}"')]),
    ('M9', 'L12', 'the c todo drops the p mark', COMP,
     [('            if (marked) return std.fmt.allocPrint(self.alloc, "`c` is Softanza\'s letter and no type\'s -- text is t: pt{s}; written"',
       '            if (false and marked) return std.fmt.allocPrint(self.alloc, "`c` is Softanza\'s letter and no type\'s -- text is t: pt{s}; written"')]),
    ('M10', 'L09', 'an item of a vector of vectors may be anything', MAIN,
     [("            't' => v.tag == .str," + NL + "            'v' => v.tag == .vec and !v.p.v.closure," + NL + "            'o' => v.tag == .obj," + NL +
       "            'h' => v.tag == .cptr or v.tag == .dll," + NL + "            else => true," + NL + "        };" + NL + "    }" + NL + "    /// v0.54: a checked letter's type in the plural",
       "            't' => v.tag == .str," + NL + "            'v' => true," + NL + "            'o' => v.tag == .obj," + NL +
       "            'h' => v.tag == .cptr or v.tag == .dll," + NL + "            else => true," + NL + "        };" + NL + "    }" + NL + "    /// v0.54: a checked letter's type in the plural")]),
    ('M11', 'L08', 'a p parameter with an element letter is not read', COMP,
     [("(std.ascii.isUpper(core[2]) or (core[1] == 'v' and core.len >= 4 and std.ascii.isLower(core[2]) and std.ascii.isUpper(core[3]))))",
       "(std.ascii.isUpper(core[2]) or (false and core[1] == 'v' and core.len >= 4 and std.ascii.isLower(core[2]) and std.ascii.isUpper(core[3]))))")]),
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
            crlf = (chr(13) + NL) in raw
            text = raw.replace(chr(13) + NL, NL)
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r} ({text.count(stale[0])} found)', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(path, 'wb').write((planted.replace(NL, chr(13) + NL) if crlf else planted).encode('utf-8'))
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
