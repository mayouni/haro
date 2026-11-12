"""Every protection of v0.66 (Haro's numbers; HARO-NUMBERS-CORE-01, D78) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig, lift.zig), built into runtime/v66/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v66/plants.py            all plants (about two minutes each)
  python spike/v66/plants.py P1 P3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v66', 'plant-build')
COURT = os.path.join(HERE, 'numbers_court.py')

PLANTS = [
    ('P1', 'U01', 'print writes a .haro float through the setting', MAIN,
     [('                self.say_haro = strict_say;', '                self.say_haro = strict_say and pv.tag == .int;')]),
    ('P2', 'U01', 'String writes a .haro float through the setting', MAIN,
     [('                            if (v.tag == .num and self.strictAt(pc)) {', '                            if (v.tag == .num and v.tag == .int) {')]),
    ('P3', 'U03', 'Text neither rounds nor pads a decimal', MAIN,
     [('                    else => decimal.round(decOf(x), pl) catch {', '                    else => decimal.round(decOf(x), 99) catch {')]),
    ('P4', 'U04', 'a float\'s tie rounds up', MAIN,
     [('        if (d > 0.5) r = fl + 1 else if (d == 0.5) r = if (@mod(fl, 2) == 0) fl else fl + 1;', '        if (d >= 0.5) r = fl + 1;')]),
    ('P5', 'U04', 'a float is rounded from its shortest text', MAIN,
     [('                        break :blk (decimal.parse(fmtPlaces(&fb, x.p.d, pl)) catch null) orelse {',
       '                        _ = &fb;\n                        break :blk (decimal.fromF64Opt(x.p.d, pl) catch null) orelse {')]),
    ('P6', 'U06', 'IntegerPart rounds down, not toward zero', MAIN,
     [('                .dec => return Value.int(@divTrunc(x.p.i, @as(i64, @intCast(decimal.pow10(x._r))))),', '                .dec => return Value.int(@divFloor(x.p.i, @as(i64, @intCast(decimal.pow10(x._r))))),')]),
    ('P7', 'U06', 'DecimalPart loses its sign', MAIN,
     [('                .dec => return Value.dec(@rem(x.p.i, @as(i64, @intCast(decimal.pow10(x._r)))), x._r),', '                .dec => return Value.dec(@mod(x.p.i, @as(i64, @intCast(decimal.pow10(x._r)))), x._r),')]),
    ('P8', 'U07', 'Decimals takes every digit', MAIN,
     [('                    const t = decimal.text(.{ .c = x.p.i, .s = x._r }, &buf);\n                    const dot = std.mem.indexOfScalar(u8, t, \'.\') orelse return self.digitVec("");\n                    return self.digitVec(t[dot + 1 ..]);',
       '                    const t = decimal.text(.{ .c = x.p.i, .s = x._r }, &buf);\n                    return self.digitVec(t);')]),
    ('P9', 'U07', 'Digits of a decimal is empty', MAIN,
     [('                .dec => return self.digitVec(decimal.text(.{ .c = x.p.i, .s = x._r }, &buf)),', '                .dec => return self.digitVec(""),')]),
    ('P10', 'U08', 'Abs of an integer keeps its sign', MAIN,
     [('                    return Value.int(if (x.p.i < 0) -x.p.i else x.p.i);', '                    return x;')]),
    ('P11', 'U08', 'Sign turns negative to 1', MAIN,
     [('                    .int, .dec => if (x.p.i < 0) -1 else if (x.p.i > 0) 1 else 0,', '                    .int, .dec => if (x.p.i < 0) 1 else if (x.p.i > 0) 1 else 0,')]),
    ('P12', 'U08', 'Clamp lets a value past its top through', MAIN,
     [('                if (valCmp(x, hi) > 0) return hi;\n', '')]),
    ('P13', 'U09', 'FromHex is no built-in', COMP,
     [('    .{ .name = "fromhex", .id = .fromhex1, .argc = 1 },\n', '')]),
    ('P14', 'U10', 'Decimals(n) as a setting is let through', COMP,
     [('            if (self.spellIn(n.namedChild(0).text()))\n                self.spellSet(n.namedChild(0).text(), "there is no setting',
       '            if (self.spellIn(n.namedChild(0).text()) and n.namedChildCount() == 99)\n                self.spellSet(n.namedChild(0).text(), "there is no setting')]),
    ('P15', 'U11', 'FAbs is let through', COMP,
     [('        if (self.haroNode(n) and (std.ascii.eqlIgnoreCase(callee, "fabs") or std.ascii.eqlIgnoreCase(callee, "dec"))) {',
       '        if (self.haroNode(n) and (std.ascii.eqlIgnoreCase(callee, "dec"))) {')]),
    ('P16', 'U12', 'Dec is let through', COMP,
     [('        if (self.haroNode(n) and (std.ascii.eqlIgnoreCase(callee, "fabs") or std.ascii.eqlIgnoreCase(callee, "dec"))) {',
       '        if (self.haroNode(n) and (std.ascii.eqlIgnoreCase(callee, "fabs"))) {')]),
    ('P17', 'U07', 'Decimals(x) in a .haro file is the classic setter', COMP,
     [('    .{ .name = "decimals", .id = .decimals1h, .argc = 1 },\n', '')]),
    ('P18', 'U13', 'a .ring file\'s fabs and dec are refused too', COMP,
     [('        if (self.haroNode(n) and (std.ascii.eqlIgnoreCase(callee, "fabs") or std.ascii.eqlIgnoreCase(callee, "dec"))) {',
       '        if ((std.ascii.eqlIgnoreCase(callee, "fabs") or std.ascii.eqlIgnoreCase(callee, "dec"))) {')]),
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
