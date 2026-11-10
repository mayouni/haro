"""Every protection of v0.52 (numbers, D55 T4) switched off in turn: the court must fail, for the fixture that protection exists for. Each
plant is text substitutions in vm/src (main.zig, compile.zig, decimal.zig, image.zig), built into runtime/v52/plant-build (ReleaseFast,
-j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests, and restored
even when a build fails or the script is stopped.

  python spike/v52/plants.py            all plants (about two minutes each)
  python spike/v52/plants.py P1 P3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
SRC = os.path.join(VM_DIR, 'src')
MAIN = os.path.join(SRC, 'main.zig')
COMP = os.path.join(SRC, 'compile.zig')
DEC = os.path.join(SRC, 'decimal.zig')
IMG = os.path.join(SRC, 'image.zig')
OUT = os.path.join(ROOT, 'runtime', 'v52', 'plant-build')
COURT = os.path.join(HERE, 'num_court.py')
NL = chr(10)

PLANTS = [
    ('P1', 'N01', 'a literal with a point is a double', COMP,
     [('            if (self.haroNode(n)) {' + NL + '                if (try haroNumber(self, t, false)) |ki| {',
       '            if (false and self.haroNode(n)) {' + NL + '                if (try haroNumber(self, t, false)) |ki| {')]),
    ('P2', 'N04', 'two integers divide as doubles', MAIN,
     [('                if (isNum(x) and isNum(y) and self.strictAt(pc)) {', '                if (false and isNum(x) and isNum(y) and self.strictAt(pc)) {')]),
    ('P3', 'N05', 'a quotient with no end is answered anyway', DEC,
     [('    if (d != 1) return error.inexact;', '    if (false and d != 1) return error.inexact;')]),
    ('P4', 'N06', 'Divide rounds half up', DEC,
     [('    if (twice > d or (twice == d and q % 2 == 1)) return q + 1;', '    if (twice >= d) return q + 1;')]),
    ('P5', 'N09', 'a decimal and a float mix', MAIN,
     [('            if (x.tag != .num or y.tag != .num) return .{ .err = self.mixErr(sym, x, y) };',
       '            if (false and (x.tag != .num or y.tag != .num)) return .{ .err = self.mixErr(sym, x, y) };')]),
    ('P6', 'N12', 'two floats are claimed equal', MAIN,
     [('        if (x.tag == .num and y.tag == .num) {' + NL + '            if (!self.strictAt(pc)) return null;',
       '        if (false and x.tag == .num and y.tag == .num) {' + NL + '            if (!self.strictAt(pc)) return null;')]),
    ('P7', 'N11', 'a decimal is ordered against a float', MAIN,
     [('        if (x.tag != y.tag and (x.tag == .num or y.tag == .num) and isNum(x) and isNum(y) and self.strictAt(pc)) return self.mixErr(op, x, y);',
       '        if (false and x.tag != y.tag and (x.tag == .num or y.tag == .num) and isNum(x) and isNum(y) and self.strictAt(pc)) return self.mixErr(op, x, y);')]),
    ('P8', 'N24', 'a float\'s whole result is narrowed to an integer', MAIN,
     [('            return .{ .val = Value.num(r) };', '            return .{ .val = narrow(r) };')]),
    ('P9', 'N02', '* keeps the larger scale', DEC,
     [('    const s = a.s + b.s;', '    const s = @max(a.s, b.s);')]),
    ('P10', 'N25', 'decimals are equal as doubles', MAIN,
     [('        if ((a.tag == .dec or b.tag == .dec) and a.tag != .num and b.tag != .num and isNum(a) and isNum(b)) return decimal.cmp(decOf(a), decOf(b)) == 0;',
       '        if (false and (a.tag == .dec or b.tag == .dec) and a.tag != .num and b.tag != .num and isNum(a) and isNum(b)) return decimal.cmp(decOf(a), decOf(b)) == 0;')]),
    ('P11', 'N25', 'decimals are ordered as doubles', MAIN,
     [('        if ((a.tag == .dec or b.tag == .dec) and a.tag != .num and b.tag != .num and isNum(a) and isNum(b)) return decimal.cmp(decOf(a), decOf(b));',
       '        if (false and (a.tag == .dec or b.tag == .dec) and a.tag != .num and b.tag != .num and isNum(a) and isNum(b)) return decimal.cmp(decOf(a), decOf(b));')]),
    ('P12', 'N15', 'Decimal rounds to one place more than asked', MAIN,
     [('                        const rv = if (places) |pl| decimal.round(dv, pl) catch {',
       '                        const rv = if (places) |pl| decimal.round(dv, pl + 1) catch {')]),
    ('P13', 'N16', 'a float becomes a decimal without the places said', MAIN,
     [('.num => if (places) |pl| decimal.fromF64Opt(v.p.d, pl) else null,', '.num => if (places) |pl| decimal.fromF64Opt(v.p.d, pl) else decimal.fromF64Opt(v.p.d, 2),')]),
    ('P14', 'N17', 'Integer truncates a decimal that is not whole', MAIN,
     [('                            .dec => out = Value.int(decimal.whole(decOf(v)) orelse {',
       '                            .dec => out = Value.int(@as(?i64, asInt(v)) orelse {')]),
    ('P15', 'N18', 'a d name takes anything', MAIN,
     [("                    'd' => v.tag == .dec,", "                    'd' => true,")]),
    ('P16', 'N19', 'a literal with a point is an integer to the letters', COMP,
     [("            _ = std.fmt.parseInt(i64, s, 10) catch return 'd';", "            _ = std.fmt.parseInt(i64, s, 10) catch return 'i';")]),
    ('P17', 'N20', 'a decimal is 0 to .ring code', MAIN,
     [('            .dec => decimal.toF64(.{ .c = x.p.i, .s = x._r }),' + NL, '            .dec => 0,' + NL)]),
    ('P18', 'N26', 'a .ring file gets Haro\'s number built-ins', COMP,
     [('            if (haroOnlyBuiltin(bi.id) and !self.haroNode(n)) continue;', '            if (false and haroOnlyBuiltin(bi.id) and !self.haroNode(n)) continue;')]),
    ('P19', 'N21', 'a product past 64 bits is cut, not refused', DEC,
     [('    return .{ .c = try fit(@as(i128, a.c) * @as(i128, b.c)), .s = s };', '    return .{ .c = @truncate(@as(i128, a.c) * @as(i128, b.c)), .s = s };')]),
    ('P20', 'N22', 'a decimal\'s text is Ring\'s two places', MAIN,
     [('        if (v.tag == .dec) return decimal.text(.{ .c = v.p.i, .s = v._r }, buf);', '        if (false and v.tag == .dec) return decimal.text(.{ .c = v.p.i, .s = v._r }, buf);')]),
    ('P21', 'N04', 'a decimal prints as a double', MAIN,
     [('                outPrint("{s}{s}", .{ decimal.text(.{ .c = v.p.i, .s = v._r }, &db), end });',
       '                outPrint("{s}{s}", .{ numText(Value.num(asF64(v)), &db), end });')]),
    ('P22', 'N10', 'a constant on the left folds beside a float', COMP,
     [(' and !may_obj_r and !(haro_num and self.classOf(rn) != .int)) {', ' and !may_obj_r) {')]),
    ('P23', 'N27', 'a constant on the right folds beside a float', COMP,
     [(' and !(haro_num and self.classOf(ln) != .int)) {', ') {')]),
    ('P24', 'N27', 'a float is negated as 0 minus it', MAIN,
     [('        if (unary and y.tag == .num) return .{ .val = Value.num(-y.p.d) };', '        if (false and unary and y.tag == .num) return .{ .val = Value.num(-y.p.d) };')]),
    ('P25', 'N28', '% on decimals subtracts', MAIN,
     [('            else => decimal.rem(a, b),', '            else => decimal.sub(a, b),')]),
    ('P26', 'N14', 'Near is strict at the tolerance', MAIN,
     [('<= asF64(regs[A + 2])));', '< asF64(regs[A + 2])));')]),
    ('P27', 'N29', 'the image drops a decimal\'s scale', IMG,
     [('._r = if (tag == .dec) ents[i].len else 0 };', '._r = 0 };')]),
    ('P28', 'N30', 'an f name takes an integer', MAIN,
     [("                    'f' => v.tag == .num,", "                    'f' => v.tag == .num or v.tag == .int,")]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMP, DEC, IMG)}

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
