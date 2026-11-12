"""Every protection of v0.64 (records; HARO-RECORD-01, D76) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig, lift.zig), built into runtime/v64/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v64/plants.py            all plants (about two minutes each)
  python spike/v64/plants.py F1 F3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v64', 'plant-build')
COURT = os.path.join(HERE, 'record_court.py')

PLANTS = [
    ('F1', 'R01', 'record is not given to the parser as class', LIFT,
     [('        @memcpy(text[e + shift .. e + shift + 6], "class ");', '        @memcpy(text[e + shift .. e + shift + 6], "record");')]),
    ('F2', 'R10', 'a method in a record is let through', LIFT,
     [('            if (!rec and (eq(w, "def") or eq(w, "func"))) {', '            if (!rec and rec and (eq(w, "def") or eq(w, "func"))) {')]),
    ('F3', 'R02', 'the number of values is not checked', COMP,
     [('        if (argc != fields.len) {\n            if (self.spellIn(n.text())) {', '        if (argc != fields.len and argc > fields.len) {\n            if (self.spellIn(n.text())) {')]),
    ('F4', 'R03', 'a proven record\'s missing field is read by name', COMP,
     [('                if (self.classes.items[rcid].is_record and self.attrSlotOf(rcid, n.namedChild(1).text()) == null)',
       '                if (self.classes.items[rcid].is_record and rcid == 9999 and self.attrSlotOf(rcid, n.namedChild(1).text()) == null)')]),
    ('F5', 'R04', 'a proven record\'s missing field is written by name', COMP,
     [('                if (self.classes.items[rcid].is_record and self.attrSlotOf(rcid, aname) == null) self.noField(rcid, aname, lhs.text());',
       '                if (self.classes.items[rcid].is_record and rcid == 9999 and self.attrSlotOf(rcid, aname) == null) self.noField(rcid, aname, lhs.text());')]),
    ('F6', 'R05', 'a field\'s value is not checked against its letter', COMP,
     [('                if (std.mem.indexOfScalar(u8, Compiler.CHECKED, l) != null) try self.emitLetterCheck(t, l, f.name);',
       '                if (l == 0) try self.emitLetterCheck(t, l, f.name);')]),
    ('F7', 'R06', 'an r name holds any object', MAIN,
     [("                    'r' => v.tag == .obj and v.p.o.rec != 0,\n                    'h'", "                    'r' => v.tag == .obj,\n                    'h'")]),
    ('F8', 'R07', 'an o name holds a record', MAIN,
     [("                    'o' => v.tag == .obj and v.p.o.rec == 0,\n                    'r'", "                    'o' => v.tag == .obj,\n                    'r'")]),
    ('F9', 'R08', 'a copy loses the record', MAIN,
     [('.class = src.class, .rc = 0, .rec = src.rec };', '.class = src.class, .rc = 0, .rec = 0 };')]),
    ('F10', 'R09', 'new User is let through', COMP,
     [('        if (ci.is_record) {\n            if (self.spellIn(n.text())) {', '        if (ci.is_record and ci.id == 9999) {\n            if (self.spellIn(n.text())) {')]),
    ('F11', 'R11', 'a record\'s missing field is Ring\'s R12', MAIN,
     [('                    if (o.rec != 0) {\n                        self.pending = self.noField(o, nidx);', '                    if (o.rec == 9999) {\n                        self.pending = self.noField(o, nidx);')]),
    ('F12', 'R11', 'the nearest field is not named when running', MAIN,
     [('        var best_d: u32 = 3;\n        if (o.class + 1 < attr_from.len) {', '        var best_d: u32 = 0;\n        if (o.class + 1 < attr_from.len) {')]),
    ('F13', 'R03', 'the nearest field is not named when compiling', COMP,
     [('        var best_d: u32 = 3;\n        for (rc.attrs.items) |a| {', '        var best_d: u32 = 0;\n        for (rc.attrs.items) |a| {')]),
    ('F14', 'R13', 'the pair refusal does not name the record', COMP,
     [('write [:key, value] for a pair, or declare a record for named fields (HARO-SURFACE-01)";', 'write [:key, value] (HARO-SURFACE-01)";')]),
    ('F15', 'R09', 'new User is judged as an object literal first', COMP,
     [('            if (self.findClassQ(cn.text())) |ci| if (ci.is_record) return false;\n', '')]),
    ('F16', 'R03', 'User(...) proves no record', COMP,
     [('            return self.recordOf(n.namedChild(0).text());\n        }\n        if (std.mem.eql(u8, k, "identifier")) {',
       '            _ = self.recordOf(n.namedChild(0).text());\n            return null;\n        }\n        if (std.mem.eql(u8, k, "identifier")) {')]),
    ('F17', 'R01', 'a record built carries no mark', COMP,
     [('        _ = try self.emit(.newobj, objr, @intCast(mark & 0xFF), @intCast(mark >> 8), @intCast(rcid));',
       '        _ = mark;\n        _ = try self.emit(.newobj, objr, 0, 0, @intCast(rcid));')]),
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
