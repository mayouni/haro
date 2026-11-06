"""Every protection of D52 rung (2) switched off in turn: the error court must fail, for the fixture that protection exists for (the W discipline).

Each plant is one text substitution in one of vm/src/main.zig, compile.zig, lift.zig, fmt.zig. The VM is built with the plant into
runtime/v37/plant-build (ReleaseFast, -j2, one build at a time: the machine's rule), the error court is run on that build alone, and every file is
restored byte for byte before the next plant -- verified by its digest, and restored even when a build fails or the script is stopped. zig-out and
zig-out-safe are never touched. A substitution that removes a line keeps every name it leaves still used: Zig refuses an unused one (v36 P4, P6).

Printed is CAUGHT with the fixtures that failed, or MISSED: a protection no fixture pins, and the answer to it is a fixture.

  python spike/v37/plants.py            all plants (about 1.5 minutes each)
  python spike/v37/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
OUT = os.path.join(ROOT, 'runtime', 'v37', 'plant-build')
COURT = os.path.join(HERE, 'error_court.py')

PLANTS = [
    ('P1', 'G01', 'lift.zig', '`catch e` is not lifted: e stays a statement',
     '''                    try out.append(alloc, .{ .pos = id.?.startByte(), .close = false });
                    try out.append(alloc, .{ .pos = id.?.endByte(), .close = true });
''', ''),
    ('P2', 'G03', 'lift.zig', 'a name on the line after `catch` is lifted too',
     'st.start().row == kw.start().row', 'st.start().row >= kw.start().row'),
    ('P3', 'G27', 'main.zig', 'a string someone else holds is marked as the error in place',
     'const sp = if (err.p.s.rc == 0) err.p.s else self.newStr(strOf(err));', 'const sp = err.p.s;'),
    ('P4', 'G14', 'main.zig', 'a rethrown error is made a new error, losing its origin',
     '        if (err.tag != .str or err.p.s.err != 0) return err;\n        const sp', '        if (err.tag != .str) return err;\n        const sp'),
    ('P5', 'G15', 'main.zig', 'a raise in a finally that held an error is given no cause',
     'const err = if (in.d > 0) self.withCause(regs[base + in.a], regs[base + @as(u32, @intCast(in.d - 1))]) else regs[base + in.a];',
     'const err = regs[base + in.a];'),
    ('P6', 'G28', 'main.zig', 'a cause may point back at its own error',
     '''        var k = held;
        while (k.tag == .str and k.p.s.err != 0) : (k = self.errs.items[k.p.s.err - 1].cause) {
            if (k.p.s == new.p.s) return new;
        }
''', ''),
    ('P7', 'G29', 'main.zig', 'the methods answer whatever arguments they are given',
     'rv.p.s.err == 0 or argc != 0 or name < 0', 'rv.p.s.err == 0 or argc == 255 or name < 0'),
    ('P8', 'G08', 'main.zig', 'Code() is not cut to Ring\'s code',
     'code = msg[7..close];', 'code = msg[0..close];'),
    ('P9', 'G24', 'main.zig', 'Message() returns the error itself, not a plain string',
     '''        if (std.ascii.eqlIgnoreCase(nm, "message")) {
            out = Value.str(self.newStr(msg));''', '''        if (std.ascii.eqlIgnoreCase(nm, "message")) {
            out = rv;'''),
    ('P10', 'G10', 'main.zig', 'the method names are matched in one case only',
     'if (std.ascii.eqlIgnoreCase(nm, "message")) {', 'if (std.mem.eql(u8, nm, "Message")) {'),
    ('P11', 'G18', 'main.zig', 'Cause() of an error with none is nothing at all, not an empty string',
     'out = if (info.cause.tag == .nil) Value.str(self.newStr("")) else info.cause;', 'out = info.cause;'),
    ('P12', 'G30', 'main.zig', 'a rethrow reports as raise() whatever made the error',
     'const rz = if (err.tag == .str and err.p.s.err != 0) self.errs.items[err.p.s.err - 1].raised else in.b == 1;', 'const rz = in.b == 1;'),
    ('P13', 'G22', 'compile.zig', 'the handler of an error path\'s finally is not counted open, so a return from that finally leaves it armed',
     '''            self.try_open += 1;
            defer self.try_open -= 1;
            try self.try_borrows.append(self.alloc, .{ 0, 0, 0, 0 });
            defer borrowed = self.try_borrows.pop().?;
            try self.body(f, 0);
        }
        _ = try self.emit(.pend, 0, 0, 0, 0);
        _ = try self.emit(.trap, held, 1, 0, 0);''',
     '''            try self.try_borrows.append(self.alloc, .{ 0, 0, 0, 0 });
            defer borrowed = self.try_borrows.pop().?;
            try self.body(f, 0);
        }
        _ = try self.emit(.pend, 0, 0, 0, 0);
        _ = try self.emit(.trap, held, 1, 0, 0);'''),
    ('P14', 'K01', 'fmt.zig', '`haro fmt` prints `catch e` as a statement on the next line',
     '''                    cg.name = try leaf(rest[0].kids[0]);
                    rest = tail(rest, 1);
''', ''),
    ('P15', 'K01', 'fmt.zig', '`haro fmt` binds a name on the line after `catch` too',
     ' and self.line(rest[0].start) == self.line(cl.kids[0].start))', ')'),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    files = {f: os.path.join(VM_DIR, 'src', f) for f in ('main.zig', 'compile.zig', 'lift.zig', 'fmt.zig')}
    original = {f: open(p, 'rb').read() for f, p in files.items()}

    def restore():
        for f, p in files.items():
            open(p, 'wb').write(original[f])
            assert digest(open(p, 'rb').read()) == digest(original[f])

    results = []
    try:
        for pid, fixture, f, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            text = original[f].decode('utf-8')
            if text.count(old) != 1:
                print(f'{pid} STALE: its text is in {f} {text.count(old)} times')
                results.append((pid, 'STALE'))
                continue
            open(files[f], 'wb').write(text.replace(old, new).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}')
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([GK]\d+)', out, re.M)
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
