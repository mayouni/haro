"""Every protection of v0.46 (stzlib's findings on haro.exe) switched off in turn: the finding court must fail, for the fixture
that protection exists for.

Each plant is one text substitution in vm/src/main.zig, compile.zig or zip.zig, written so that no name is left unused (Zig refuses one).
The VM is built with the plant into runtime/v44/plant-build (ReleaseFast, -j2, one build at a time), the court is run on that build alone,
and the file is restored byte for byte before the next plant -- verified by its digest, and restored even when a build fails or the
script is stopped.

A file with CRLF line ends (zip.zig, HF-135) is matched and planted on its LF-normalised text and written back with its own ends: the
first run read raw bytes, and four zip plants stood 0 times (STALE) though their text was there.

Removed after planting, named: Z6 and Z8, the NaN check of `jle` and `jge`. The compiler emits an ordering jump only inverted (c = 1, from
cond()), and for these two a NaN's valCmp of 0 already makes `<=` and `>=` hold, so the jump fires and the comparison reads false, as IEEE
says; switched off, no case moved, and none can. The checks are removed from the VM; `jlt` and `jgt` keep theirs (Z5, Z7).

N2 RESTORED, second round: removed once as idle because no case reached it, it is load-bearing for a key of class ref (K09). Removed after
planting, named: N2 (FIRST ROUND), the keyed read's vget counted when the element is unboxed -- the class of the read (N1) is what stops
the crash, since the move into the counted register retains; switched off, nothing moved, and the change is taken out. N4, a lone `.` as
the sibling of the receiver call's statement -- the grammar puts it at the end of the statement before (N3), never there; taken out.
N6 missed first: K07 passes a number, refused before the kind is asked, so K08 (a file's pointer) was written after the plants.

  python spike/v46/plants.py            all plants (about a minute each)
  python spike/v46/plants.py Z3 Z7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
TYPES = os.path.join(VM_DIR, 'src', 'types.zig')
OUT = os.path.join(ROOT, 'runtime', 'v46', 'plant-build')
COURT = os.path.join(HERE, 'finding_court.py')

PLANTS = [
    ('N1', 'K01', COMP, 'a keyed read takes the element class',
     '                    .list => if (idx_is_int) l.elem else Class.join(l.elem, .str),', '                    .list => if (idx_is_int or true) l.elem else Class.join(l.elem, .str),'),
    ('N2', 'K09', COMP, 'a keyed read by an unproven key is an uncounted vget when the element is unboxed',
     '.list => _ = try self.emit(.vget, dst, base, idx, if (ec.boxed() or self.classOf(n.namedChild(1)) != .int) 1 else 0),',
     '.list => _ = try self.emit(.vget, dst, base, idx, if (ec.boxed() or (false and self.classOf(n.namedChild(1)) != .int)) 1 else 0),'),
    ('N10', 'K12', MAIN, 'ptrcmp takes anything', '                        if (pa.tag != .cptr or pb.tag != .cptr) {',
     '                        if (false and (pa.tag != .cptr or pb.tag != .cptr)) {'),
    ('N11', 'K10', MAIN, 'ptrcmp answers 1 for any two pointers', '                        out = Value.int(if (cptrOf(pa) == cptrOf(pb)) 1 else 0);',
     '                        out = Value.int(if (true or cptrOf(pa) == cptrOf(pb)) 1 else 0);'),
    ('N12', 'K11', COMP, 'obj2ptr is no name the compiler knows', '    .{ .name = "obj2ptr", .id = .obj2ptr, .argc = 1 },', '    .{ .name = "obj2ptr_unknown", .id = .obj2ptr, .argc = 1 },'),
    ('N3', 'K03', TYPES, 'the lone `.` ending the statement before is not looked for',
     '                if (cnt > 0 and std.mem.eql(u8, before.child(cnt - 1).kind(), ".")) return;',
     '                if (false and cnt > 0 and std.mem.eql(u8, before.child(cnt - 1).kind(), ".")) return;'),
    ('N5', 'K06', MAIN, 'object2pointer takes anything',
     '                        if (ov.tag != .obj) {\n                            self.pending = BADPARAM;\n                            continue :dispatch .raise;\n                        }\n                        retain(ov);',
     '                        if (false and ov.tag != .obj) {\n                            self.pending = BADPARAM;\n                            continue :dispatch .raise;\n                        }\n                        retain(ov);'),
    ('N6', 'K08', MAIN, 'pointer2object takes anything that is a pointer of any kind',
     '                        const raw = if (kind_ok) cptrOf(pv) else null;', '                        const raw = if (kind_ok or pv.tag == .cptr) cptrOf(pv) else null;'),
    ('N7', 'K05', MAIN, 'pointer2object answers the object unshared', '                        if (o.rref == 0) o.rref = 1;', '                        if (false and o.rref == 0) o.rref = 1;'),
    ('N8', 'K05', MAIN, 'two pointers to one object are unequal',
     '        if (a.tag == .cptr and b.tag == .cptr) return cptrOf(a) == cptrOf(b);', '        if (false and a.tag == .cptr and b.tag == .cptr) return cptrOf(a) == cptrOf(b);'),
    ('N9', 'K05', MAIN, 'the pointer kind is not OBJECTPOINTER', 'out = self.newCptr(@ptrCast(ov.p.o), "OBJECTPOINTER");', 'out = self.newCptr(@ptrCast(ov.p.o), "POINTER");'),
]


def nan_plant(text, op):
    """the unordered check of one ordering jump, switched off: `if (unordered(...))` of the block that opens `.op => {`"""
    at = text.index(f'            .{op} => {{\n')
    key = '                if (unordered(regs[base + in.a], regs[base + in.b])) {'
    k = text.index(key, at)
    return text[:k] + key.replace('if (unordered(', 'if (false and unordered(') + text[k + len(key):]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {f: open(f, 'rb').read() for f in (MAIN, COMP, TYPES)}

    def restore():
        for f, b in originals.items():
            open(f, 'wb').write(b)
            assert digest(open(f, 'rb').read()) == digest(b)

    results = []
    try:
        for pid, fixture, src, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            raw_text = originals[src].decode('utf-8')
            crlf = (chr(13) + chr(10)) in raw_text
            text = raw_text.replace(chr(13) + chr(10), chr(10))
            if old is None:
                planted = nan_plant(text, new)
            else:
                if text.count(old) != 1:
                    print(f'{pid} STALE: the text stands {text.count(old)} times: {old[:70]!r}', flush=True)
                    results.append((pid, 'STALE'))
                    continue
                planted = text.replace(old, new)
            open(src, 'wb').write((planted.replace(chr(10), chr(13) + chr(10)) if crlf else planted).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL (K\d+)', out, re.M)
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
