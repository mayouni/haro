"""Every protection of v0.67 (maps; HARO-MAP-01, D79) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig, lift.zig), built into runtime/v67/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v67/plants.py            all plants (about two minutes each)
  python spike/v67/plants.py H1 H3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v67', 'plant-build')
COURT = os.path.join(HERE, 'map_court.py')

PLANTS = [
    ('H1', 'G01', "a map literal's colon is not given as a comma", LIFT,
     [("        text[e + shift] = ',';\n", "        text[e + shift] = ':';\n")]),
    ('H2', 'G01', "the empty map's colon is not blanked", LIFT,
     [("    for (map_blanks.items) |e| {\n        var shift: usize = 0;\n        for (heads.items) |h| {\n            if (h <= e) shift += 2;\n        }\n        text[e + shift] = ' ';", "    for (map_blanks.items) |e| {\n        var shift: usize = 0;\n        for (heads.items) |h| {\n            if (h <= e) shift += 2;\n        }\n        text[e + shift] = ':';")]),
    ('H3', 'G01', 'a map literal stays a list', COMP,
     [('            if (lit_map) {', '            if (lit_map and n.namedChildCount() > 9999) {')]),
    ('H4', 'G02', 'a map read is no maybe', COMP,
     [('        if (self.mapRead(n)) return n.text();\n', '')]),
    ('H5', 'G01', 'a text key reads a map as a pair list', MAIN,
     [('                if (cv.p.v.map and self.strictAt(pc)) {\n                    const got = self.mapRead(cv.p.v, kv) orelse continue :dispatch .raise;', '                if (cv.p.v.map and cv.p.v.len == 99999) {\n                    const got = self.mapRead(cv.p.v, kv) orelse continue :dispatch .raise;')]),
    ('H6', 'G03', 'an integer key reads a map by position', MAIN,
     [('                if (cv.tag == .vec and cv.p.v.map and self.strictAt(pc)) {\n                    const got = self.mapRead(cv.p.v, iv) orelse continue :dispatch .raise;', '                if (cv.tag == .vec and cv.p.v.map and cv.p.v.len == 99999) {\n                    const got = self.mapRead(cv.p.v, iv) orelse continue :dispatch .raise;')]),
    ('H7', 'G15', 'a text key writes a map as a pair list', MAIN,
     [('                if (cv.p.v.map and self.strictAt(pc)) {\n                    if (!self.mapWrite(self.cowFor(base + in.a, cv), kv, regs[base + in.c])) continue :dispatch .raise;', '                if (cv.p.v.map and cv.p.v.len == 99999) {\n                    if (!self.mapWrite(self.cowFor(base + in.a, cv), kv, regs[base + in.c])) continue :dispatch .raise;')]),
    ('H8', 'G15', 'an integer key writes a map by position', MAIN,
     [('                if (vv.tag == .vec and vv.p.v.map and self.strictAt(pc)) {\n                    if (!self.mapWrite(', '                if (vv.tag == .vec and vv.p.v.map and vv.p.v.len == 99999) {\n                    if (!self.mapWrite(')]),
    ('H9', 'G06', 'Keys answers the values', MAIN,
     [('m.ptr[i].p.v.ptr[if (which == .keys1) 0 else 1]', 'm.ptr[i].p.v.ptr[if (which == .keys1) 1 else 0]')]),
    ('H10', 'G06', 'HasKey answers the other way', MAIN,
     [('                return Value.int(@intFromBool(mapFind(m, a[1]) != null));', '                return Value.int(@intFromBool(mapFind(m, a[1]) == null));')]),
    ('H11', 'G06', 'Del of a map deletes by position', MAIN,
     [('                if (cv.p.v.map and self.strictAt(pc)) {\n                    if (!self.mapDel(', '                if (cv.p.v.map and cv.p.v.len == 99999) {\n                    if (!self.mapDel(')]),
    ('H12', 'G04', 'a decimal key is let through', MAIN,
     [('        if (k.tag == .str or k.tag == .int) return null;\n        return self.haroMsg("Error (KEY_TYPE)', '        if (k.tag == .str or k.tag == .int or k.tag == .dec) return null;\n        return self.haroMsg("Error (KEY_TYPE)')]),
    ('H13', 'G05', "a literal's repeated key is let through", MAIN,
     [('            while (i + 1 < src.len) : (i += 2) {\n                const k = src.ptr[i];\n                if (self.mapKeyFault(k)) |e| {\n                    self.pending = e;\n                    return null;\n                }\n                if (mapFind(m, k) != null) {', '            while (i + 1 < src.len) : (i += 2) {\n                const k = src.ptr[i];\n                if (self.mapKeyFault(k)) |e| {\n                    self.pending = e;\n                    return null;\n                }\n                if (mapFind(m, k) != null and i == 99999) {')]),
    ('H14', 'G07', 'm is not a checked letter', COMP,
     [('    const CHECKED = "bidntfvoherm";', '    const CHECKED = "bidntfvoher";')]),
    ('H15', 'G08', 'a v name holds a map', MAIN,
     [("                    'v' => v.tag == .vec and !v.p.v.closure and !v.p.v.map,\n                    'm'", "                    'v' => v.tag == .vec and !v.p.v.closure,\n                    'm'")]),
    ('H16', 'G16', "a map literal is a vector's literal", COMP,
     [('        const lit: u8 = if (std.mem.eql(u8, rhs.kind(), "list_literal") and self.mapAt(rhs)) \'m\' else literalLetter(rhs) orelse return false;', '        const lit: u8 = if (std.mem.eql(u8, rhs.kind(), "list_literal") and self.mapAt(rhs) and rhs.namedChildCount() > 9999) \'m\' else literalLetter(rhs) orelse return false;')]),
    ('H17', 'G09', 'a copy is no map', MAIN,
     [('                c.closure = src.closure;\n                c.map = src.map;', '                c.closure = src.closure;\n                c.map = false;')]),
    ('H18', 'G10', 'a map is printed as a list', MAIN,
     [('                if (v.p.v.map and self.say_haro) {', '                if (v.p.v.map and self.say_haro and v.p.v.len == 99999) {')]),
    ('H19', 'G12', "a .ring caller's pair list is no map", MAIN,
     [("                if (in.c == 1 and in.b == 'm' and v.tag == .vec and !v.p.v.map and fsp > 0", "                if (in.c == 1 and in.b == 'm' and v.tag == .vec and !v.p.v.map and fsp > 9999")]),
    ('H20', 'G14', 'the pair refusal does not name the map', COMP,
     [('write [\\"key\\": value] for a map, [:key, value] for a pair, or declare', 'write [:key, value] for a pair, or declare')]),
    ('H21', 'G02', 'a map read refused in the words of a maybe call', COMP,
     [('                if (self.mapRead(n)) return self.spellSet(n.text(), "a map\'s read may find nothing', '                if (self.mapRead(n) and n.namedChildCount() > 9999) return self.spellSet(n.text(), "a map\'s read may find nothing')]),
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
