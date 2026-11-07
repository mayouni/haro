"""Every protection of HARO-SURFACE-01 switched off in turn: the surface court must fail, for the fixture that protection exists for.

Each plant is one or more text substitutions in vm/src/lift.zig, compile.zig, haro.zig or fmt.zig. The VM is built with the plant into
runtime/v41/plant-build (ReleaseFast, -j2, one build at a time), the surface court is run on that build alone, and every file is restored byte for
byte before the next plant -- verified by its digest, and restored even when a build fails or the script is stopped.

Not planted, named: the grammar itself (a plant would regenerate a 19 MB parser; S01 and S02 are what a case-insensitive grammar fails); the two
dumps printing the file's own bytes (no court reads `haro dump`; spike/v18's printer does, and its stage runs in the guard); fmt lowering a re-read
piece of a .ring file (no case is re-read); comments skipped by the lowering (a comment lowered changes nothing a program does).

  python spike/v41/plants.py            all plants (about a minute each)
  python spike/v41/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
OUT = os.path.join(ROOT, 'runtime', 'v41', 'plant-build')
COURT = os.path.join(HERE, 'surface_court.py')

PLANTS = [
    ('P1', 'S03', 'lift.zig', 'a .ring file is not lowered', [('    if (haro) return .{ .tree = parser.parse(src) orelse return null, .src = src };', '    if (haro or true) return .{ .tree = parser.parse(src) orelse return null, .src = src };')]),
    ('P2', 'S02', 'lift.zig', 'no file is a .haro file', [('    return std.mem.endsWith(u8, path, ".haro");', '    return std.mem.endsWith(u8, path, ".never");')]),
    ('P3', 'S03', 'lift.zig', 'every file is a .haro file', [('    return std.mem.endsWith(u8, path, ".haro");', '    return std.mem.endsWith(u8, path, "");')]),
    ('P4', 'S12', 'lift.zig', 'a .ring file\'s strings are lowered too', [("        if (ch == '\"' or ch == '\\'' or ch == '`') {", '        if (false) {')]),
    ('P5', 'S04', 'compile.zig', 'a .haro symbol is lowered', [('        for (t, 0..) |ch, i| buf[i] = if (keep) ch else std.ascii.toLower(ch);',
                                                               '        _ = keep;\n        for (t, 0..) |ch, i| buf[i] = std.ascii.toLower(ch);')]),
    ('P6', 'S09', 'compile.zig', 'an eval is read by Ring\'s rules whatever the root', [('        if (self.eval != null) return lift.haro_root;', '        if (self.eval != null) return false;')]),
    ('P7', 'S06', 'compile.zig', 'a .haro list may hold `:key = value`', [('                    if (self.haroNode(el)) return self.nopeKind(el, R_PAIR);\n', '')]),
    ('P8', 'S13', 'compile.zig', 'a .haro expression may be `:key = value`', [('            if (self.haroNode(n)) return self.nopeKind(n, R_PAIR);\n', '')]),
    ('P9', 'S14', 'lift.zig', 'Haro\'s block words in any case', [('    return if (std.mem.eql(u8, id.text(), "within") or std.mem.eql(u8, id.text(), "using")) id else null;',
                                                                   '    return if (std.ascii.eqlIgnoreCase(id.text(), "within") or std.ascii.eqlIgnoreCase(id.text(), "using")) id else null;')]),
    ('P10', 'K02', 'fmt.zig', '`haro fmt` reads every file by Haro\'s rules', [('    const pl = lift.parse(a, parser, src, haro) orelse {', '    const pl = lift.parse(a, parser, src, true) orelse {')]),
    ('P11', 'K02', 'fmt.zig', '`haro fmt` prints the lowered text, not the file\'s', [('    var ab = try Abs.init(a, parser, if (lb.src.len == src.len) src else lb.src);', '    var ab = try Abs.init(a, parser, lb.src);')]),
    ('P12', 'S11', 'haro.zig', 'every loaded file is read by the root\'s rules', [('        const pl = lift.parse(alloc, parser, src, lift.isHaro(p)) orelse continue;', '        const pl = lift.parse(alloc, parser, src, lift.haro_root) orelse continue;')]),
    ('P13', 'S09', 'haro.zig', 'the root\'s rules are never recorded', [('        if (qi == 0) lift.haro_root = lift.isHaro(p);', '        if (qi == 0) lift.haro_root = false;')]),
    ('P14', 'KEYWORDS', 'lift.zig', 'the lift lowers one keyword fewer than the grammar has', [(' "not",', '')]),
    ('P15', 'S10', 'compile.zig', 'an eval in a .ring program is read by Haro\'s rules', [('snippet, lift.haro_root) orelse return Error.Unsupported).tree;', 'snippet, true) orelse return Error.Unsupported).tree;')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    files = {f: os.path.join(VM_DIR, 'src', f) for f in ('lift.zig', 'compile.zig', 'haro.zig', 'fmt.zig')}
    original = {f: open(p, 'rb').read() for f, p in files.items()}

    def restore():
        for f, p in files.items():
            open(p, 'wb').write(original[f])
            assert digest(open(p, 'rb').read()) == digest(original[f])

    results = []
    try:
        for pid, fixture, f, why, subs in PLANTS:
            if want and pid not in want:
                continue
            text = original[f].decode('utf-8')
            stale = [old for old, _ in subs if text.count(old) != 1]
            if stale:
                print(f'{pid} STALE: a text is in {f} {text.count(stale[0])} times: {stale[0][:60]!r}', flush=True)
                results.append((pid, 'STALE'))
                continue
            for old, new in subs:
                text = text.replace(old, new)
            open(files[f], 'wb').write(text.encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([SK]\d+)', out, re.M) + (['KEYWORDS'] if 'FAIL the lift' in out else [])
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
