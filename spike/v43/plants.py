"""Every protection of v0.43 (a real boolean and no coercion, D55 T1 and T3) switched off in turn: the boolean court must fail, for the fixture
that protection exists for.

Each plant is one text substitution in vm/src/main.zig or vm/src/compile.zig. The VM is built with the plant into runtime/v43/plant-build
(ReleaseFast, -j2, one build at a time), the boolean court is run on that build alone, and the file is restored byte for byte before the next
plant -- verified by its digest, and restored even when a build fails or the script is stopped.

Removed after planting, named:
  - P8, the boolean constant of a .haro file's true and false (constOf): its one caller outside constOf is the resident VM's gained
    attribute, which no case of this rung runs; switched off, nothing moved. Kept, as a boolean constant (konstBool) -- the first version
    returned no constant there, which would have refused `bReady = true` in a replaced .haro class; found by asking why P8 missed.
  - P19, a boolean against an integer immediate (jeqi, jnei, jgti): the compiler never emits those three, only the VM's built-in bench
    programs do, so the check guarded nothing a .haro file reaches; the check is removed from the VM.

  python spike/v43/plants.py            all plants (about a minute each)
  python spike/v43/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v43', 'plant-build')
COURT = os.path.join(HERE, 'bool_court.py')

PLANTS = [
    # the VM: conditions and truth
    ('P1', 'B04', MAIN, 'a condition is not judged (jfalsy)',
     '            .jfalsy => {\n                const in = code[pc];\n                if (in.c == 1 and regs[base + in.a].tag != .boolean) {',
     '            .jfalsy => {\n                const in = code[pc];\n                if (false) {'),
    ('P2', 'B23', MAIN, 'the left of `or` is not judged (jtruthy)',
     '            .jtruthy => {\n                const in = code[pc];\n                if (in.c == 1 and regs[base + in.a].tag != .boolean) {',
     '            .jtruthy => {\n                const in = code[pc];\n                if (false) {'),
    ('P3', 'B07', MAIN, 'the right of `and` is not judged (truth)',
     '            .truth => {\n                const in = code[pc];\n                if (in.c == 1 and regs[base + in.b].tag != .boolean) {',
     '            .truth => {\n                const in = code[pc];\n                if (false) {'),
    ('P4', 'B06', MAIN, 'the operand of `not` is not judged (lnot)',
     '            .lnot => {\n                const in = code[pc];\n                if (in.c == 1 and regs[base + in.b].tag != .boolean) {',
     '            .lnot => {\n                const in = code[pc];\n                if (false) {'),
    ('P5', 'B02', MAIN, 'truth makes Ring\'s 1 or 0, not a boolean',
     '                    self.setRegB(base + in.a, Value.boolean(truthy(regs[base + in.b])), false);',
     '                    self.setRegB(base + in.a, Value.int(if (truthy(regs[base + in.b])) 1 else 0), false);'),
    ('P6', 'B02', MAIN, '`not` makes Ring\'s 1 or 0, not a boolean',
     '                    self.setRegB(base + in.a, Value.boolean(!truthy(regs[base + in.b])), false);',
     '                    self.setRegB(base + in.a, Value.int(if (truthy(regs[base + in.b])) 0 else 1), false);'),
    # the compiler: where booleans are made, and conditions flagged
    ('P7', 'B01', COMP, 'true and false load as Ring\'s 1 and 0',
     '            if (self.haroNode(n)) _ = try self.emit(.truth, dst, dst, 2, 0);\n            return;\n        }\n        if (std.mem.eql(u8, k, "null")) {',
     '            return;\n        }\n        if (std.mem.eql(u8, k, "null")) {'),
    ('P9', 'B02', COMP, 'a comparison as a value is Ring\'s 1 or 0',
     '            self.land(done);\n            if (self.haroNode(n)) _ = try self.emit(.truth, dst, dst, 2, 0);\n            return;',
     '            self.land(done);\n            return;'),
    ('P10', 'B03', COMP, 'a literal condition is not refused when compiling',
     '            if (lit) |what| {\n                self.spellSet(', '            if (lit) |what| {\n                if (what.len > 0) {} else self.spellSet('),
    ('P11', 'B04', COMP, 'a condition is not flagged to be judged',
     '        try out.append(self.scratch, try self.emit(.jfalsy, t, 0, if (hc) 1 else 0, 0));',
     '        try out.append(self.scratch, try self.emit(.jfalsy, t, 0, 0, 0));'),
    ('P12', 'B08', COMP, 'a yes-or-no native answers Ring\'s 1 or 0',
     '            if (self.yesNoNative(n) and self.haroNode(n)) _ = try self.emit(.truth, dst, dst, 2, 0);\n', ''),
    ('P13', 'B07', COMP, '`and` as a value does not judge its operands',
     '            const hb: u8 = if (self.haroNode(n)) 1 else 0;', '            const hb: u8 = 0;'),
    ('P14', 'B06', COMP, '`not` does not judge its operand',
     '            _ = try self.emit(.lnot, dst, t, if (self.haroNode(n)) 1 else 0, 0);', '            _ = try self.emit(.lnot, dst, t, 0, 0);'),
    # the VM: no coercion
    ('P15', 'B11', MAIN, 'text + number is not refused', '        if (self.strictAt(pc)) return self.coerceErr("+", x, y);',
     '        if (false and self.strictAt(pc)) return self.coerceErr("+", x, y);'),
    ('P16', 'B13', MAIN, 'arithmetic on a text is not refused', '        if (self.strictAt(pc)) return self.coerceErr(arithSym(op), x, y);',
     '        if (false and self.strictAt(pc)) return self.coerceErr(arithSym(op), x, y);'),
    ('P17', 'B14', MAIN, '= between two types is not refused',
     '        if (isNum(x) and isNum(y)) return null;\n        if (!self.strictAt(pc)) return null;\n        return self.mismatchErr(op, x, y);\n    }\n    /// The orderings',
     '        if (isNum(x) and isNum(y)) return null;\n        if (!self.strictAt(pc) or true) return null;\n        return self.mismatchErr(op, x, y);\n    }\n    /// The orderings'),
    ('P18', 'B15', MAIN, 'an ordering between two types is not refused',
     '        if (same) return null;\n        if (!self.strictAt(pc)) return null;', '        if (same or true) return null;\n        if (!self.strictAt(pc)) return null;'),
    ('P20', 'B19', MAIN, 'an integer past Ring\'s exact range becomes a float in Haro\'s code too',
     '    fn intStrict(self: *VM, pc: u32, x: i64, y: i64, comptime op: u8) ?Value {\n        if (!self.strictAt(pc)) return null;',
     '    fn intStrict(self: *VM, pc: u32, x: i64, y: i64, comptime op: u8) ?Value {\n        if (!self.strictAt(pc) or true) return null;'),
    ('P21', 'B18', COMP, 'a .haro integer literal past 32 bits is a float constant',
     '                if (self.haroNode(n)) {\n                    _ = try self.emit(.loadk, dst, 0, 0, try self.konstInt(v));',
     '                if (false) {\n                    _ = try self.emit(.loadk, dst, 0, 0, try self.konstInt(v));'),
    ('P22', 'B21', MAIN, 'every file is held to Haro\'s rules',
     '        return std.mem.endsWith(u8, self.file_names[fi], ".haro");', '        return true;'),
    ('P23', 'B22', MAIN, 'a boolean reaching Ring\'s + is not read as 1 or 0',
     '        if (isNum(a) and isNum(b)) {\n            self.setRegB(dst, narrow(asF64(a) + asF64(b)), false);\n            return ARITH_DONE;\n        }\n',
     ''),
    ('P24', 'B10', MAIN, 'string() of a boolean is not its word',
     '                        } else if (v.tag == .boolean) {\n                            out = Value.str(self.newStr(if (v.p.i != 0) "true" else "false"));\n', ''),
    ('P25', 'B01', MAIN, 'a boolean is printed as a number',
     '            .boolean => outPrint("{s}{s}", .{ if (v.p.i != 0) "true" else "false", end }),', '            .boolean => outPrint("{d}{s}", .{ v.p.i, end }),'),
    ('P26', 'B01', MAIN, 'type() of a boolean is NUMBER', '                            .boolean => "BOOLEAN",', '                            .boolean => "NUMBER",'),
    ('P27', 'B09', MAIN, 'the `+ constant` path reports Haro\'s error without its line',
     '                                if (self.strictAt(pc)) self.dieRing(e, pc, fsp);\n', ''),
    ('P28', 'B24', MAIN, 'a comparison with an object\'s operand (cmpv) is not judged',
     '                if (strict) {\n                    if (if (k < 2) self.preEq(pc, x, y, names[k]) else self.preCmp(pc, x, y, names[k])) |e| {',
     '                if (false) {\n                    if (if (k < 2) self.preEq(pc, x, y, names[k]) else self.preCmp(pc, x, y, names[k])) |e| {'),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {MAIN: open(MAIN, 'rb').read(), COMP: open(COMP, 'rb').read()}

    def restore():
        for f, b in originals.items():
            open(f, 'wb').write(b)
            assert digest(open(f, 'rb').read()) == digest(b)

    results = []
    try:
        for pid, fixture, src, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            text = originals[src].decode('utf-8')
            if text.count(old) != 1:
                print(f'{pid} STALE: the text stands {text.count(old)} times: {old[:70]!r}', flush=True)
                results.append((pid, 'STALE'))
                continue
            open(src, 'wb').write(text.replace(old, new).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL (B\d+)', out, re.M)
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
