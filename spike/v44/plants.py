"""Every protection of v0.44 (the ported defects, HARO-PORTED-FINDINGS-01) switched off in turn: the ported court must fail, for the fixture
that protection exists for.

Each plant is one text substitution in vm/src/main.zig, compile.zig or zip.zig, written so that no name is left unused (Zig refuses one).
The VM is built with the plant into runtime/v44/plant-build (ReleaseFast, -j2, one build at a time), the court is run on that build alone,
and the file is restored byte for byte before the next plant -- verified by its digest, and restored even when a build fails or the
script is stopped.

  python spike/v44/plants.py            all plants (about a minute each)
  python spike/v44/plants.py Z3 Z7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
ZIP = os.path.join(VM_DIR, 'src', 'zip.zig')
OUT = os.path.join(ROOT, 'runtime', 'v44', 'plant-build')
COURT = os.path.join(HERE, 'ported_court.py')

PLANTS = [
    ('Z1', 'Q01', MAIN, 'sqrt of a negative is not refused', '                            .sqrt => dx < 0,', '                            .sqrt => false,'),
    ('Z2', 'Q02', MAIN, 'log and log10 at or below zero are not refused', '                            .log, .log10 => dx <= 0,', '                            .log, .log10 => false,'),
    ('Z3', 'Q02', MAIN, 'asin and acos beyond 1 are not refused', '                            .asin, .acos => dx > 1 or dx < -1,', '                            .asin, .acos => false,'),
    ('Z4', 'Q02', MAIN, 'pow outside its domain is not refused',
     '                            if ((px < 0 and py != @trunc(py)) or (px == 0 and py < 0)) {',
     '                            if (false and ((px < 0 and py != @trunc(py)) or (px == 0 and py < 0))) {'),
    ('Z5', 'Q03', MAIN, 'a NaN is ordered by `jlt`', None, 'jlt'),
    ('Z6', 'Q03', MAIN, 'a NaN is ordered by `jle`', None, 'jle'),
    ('Z7', 'Q03', MAIN, 'a NaN is ordered by `jgt`', None, 'jgt'),
    ('Z8', 'Q03', MAIN, 'a NaN is ordered by `jge`', None, 'jge'),
    ('Z9', 'Q13', MAIN, 'a NaN is ordered by cmpv', '                    t = if (unordered(x, y)) false else switch (k) {',
     '                    t = if (false and unordered(x, y)) false else switch (k) {'),
    ('Z10', 'Q09', MAIN, 'a .haro file writes a letter in place',
     '        if (self.strictAt(pc)) return "Error (TEXT_IN_PLACE)', '        if (false and self.strictAt(pc)) return "Error (TEXT_IN_PLACE)'),
    ('Z11', 'Q08', MAIN, 'a letter of a global\'s text is written into a register nobody reads back',
     '        if (!local) return "Haro: a letter', '        if (false and !local) return "Haro: a letter'),
    ('Z12', 'Q06', MAIN, 'more than one character is not R7', '            if (t.len != 1) return R7;', '            if (t.len == 0) return R7;'),
    ('Z13', 'Q07', MAIN, 'an index past the end is not R2', '        if (idx < 1 or idx > s.len) return R2;', '        if (idx < 1 or idx > s.len + 1) return R2;'),
    ('Z14', 'Q05', MAIN, 'the letter is written into the text another name holds',
     '        const buf = self.alloc.alloc(u8, s.len) catch @panic("oom");\n        @memcpy(buf, s);',
     '        const buf = @constCast(s);'),
    ('Z15', 'Q05', COMP, 'the compiler does not say the container is a local',
     '                const own: i32 = if (depth == 1 and borrowed.items.len == 0) 2 else 0;',
     '                const own: i32 = if (false and depth == 1 and borrowed.items.len == 0) 2 else 0;'),
    ('Z16', 'Q05', MAIN, 'a number is not taken as its byte',
     '        } else if (isNum(nv)) @truncate(@as(u64, @bitCast(asInt(nv)))) else return BADPARAM;',
     '        } else if (false and isNum(nv)) @truncate(@as(u64, @bitCast(asInt(nv)))) else return BADPARAM;'),
    ('Z17', 'Q10', ZIP, 'append reads a file that is no archive as an empty one',
     '                readNames(path, &names) catch {\n                    a.deinit();\n                    retStr(out, ""); // Ring\'s NULL',
     '                readNames(path, &names) catch if (false) {\n                    a.deinit();\n                    retStr(out, ""); // Ring\'s NULL'),
    ('Z18', 'Q10', ZIP, 'a call on the null archive is refused instead of doing nothing',
     '    if (argc != 1) return 1;\n    if (nullArchive(args, argc)) return noop(out);\n    const a = argArchive(args, 0) orelse return 1;\n    if (a.open_name) |name| {',
     '    if (argc != 1) return 1;\n    if (false and nullArchive(args, argc)) return noop(out);\n    const a = argArchive(args, 0) orelse return 1;\n    if (a.open_name) |name| {'),
    ('Z19', 'Q10', ZIP, 'the null archive is the integer 0, which isnull() does not see',
     '                retStr(out, ""); // Ring\'s NULL\n                    return 0;', '                out.* = RppVal.handle(null);\n                    return 0;'),
    ('Z20', 'Q11', ZIP, 'extraction reads an entry by its name, the first of a name twice',
     '        const raw = (readEntryAt(path, name, pos) catch continue) orelse continue;',
     '        const raw = (readEntryAt(path, name, if (false) pos else null) catch continue) orelse continue;'),
    ('Z21', 'Q11', ZIP, 'extraction answers 0, not nothing', '    retStr(out, "");\n    std.fs.cwd().makePath(folder) catch {};',
     '    out.* = RppVal.int(0);\n    std.fs.cwd().makePath(folder) catch {};'),
    ('Z22', 'Q14', ZIP, 'a name that leaves the folder is written', '        if (!safeName(name)) continue;', '        if (false and !safeName(name)) continue;'),
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
    originals = {f: open(f, 'rb').read() for f in (MAIN, COMP, ZIP)}

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
            if old is None:
                planted = nan_plant(text, new)
            else:
                if text.count(old) != 1:
                    print(f'{pid} STALE: the text stands {text.count(old)} times: {old[:70]!r}', flush=True)
                    results.append((pid, 'STALE'))
                    continue
                planted = text.replace(old, new)
            open(src, 'wb').write(planted.encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL (Q\d+)', out, re.M)
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
