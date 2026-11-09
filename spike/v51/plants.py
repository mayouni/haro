"""Every protection of v0.51 (`haro check --facts`, HARO-FACTS-01) switched off in turn: the court must fail, for the fixture that
protection exists for. Each plant is text substitutions in vm/ (facts.zig, haro.zig, compile.zig, build.zig), built into
runtime/v51/plant-build (ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte --
verified by their digests, and restored even when a build fails or the script is stopped.

A planted build is made while vm/ holds the plant, so its commit reads "+uncommitted" -- and so does the court's @COMMIT, read while
the plant stands: the court is run before the files are restored. Only G2 is about the commit.

  python spike/v51/plants.py            all plants (about two minutes each)
  python spike/v51/plants.py G1 G3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
SRC = os.path.join(VM_DIR, 'src')
FACTS = os.path.join(SRC, 'facts.zig')
HARO = os.path.join(SRC, 'haro.zig')
COMP = os.path.join(SRC, 'compile.zig')
BUILD = os.path.join(VM_DIR, 'build.zig')
OUT = os.path.join(ROOT, 'runtime', 'v51', 'plant-build')
COURT = os.path.join(HERE, 'facts_court.py')

PLANTS = [
    ('G1', 'X02', 'the flag before the file is read as the file', HARO,
     [('    if (argv.len >= 4 and std.mem.eql(u8, argv[1], "check") and std.mem.eql(u8, argv[2], "--facts")) {',
       '    if (false and argv.len >= 4 and std.mem.eql(u8, argv[1], "check") and std.mem.eql(u8, argv[2], "--facts")) {')]),
    ('G2', 'X01', 'the checker names no commit', BUILD,
     [('    opts.addOption([]const u8, "commit", vmCommit(b));', '    opts.addOption([]const u8, "commit", "unknown");')]),
    ('G3', 'X01', 'the sha256 is of the path, not the bytes read', FACTS,
     # G3 FAILED TO BUILD on its first run: hashing the path left `origs` unused, which Zig refuses; it still reads origs here
     [('        std.crypto.hash.sha2.Sha256.hash(origs[fi], &digest, .{});',
       '        std.crypto.hash.sha2.Sha256.hash(if (origs.len > 0) paths[fi] else origs[fi], &digest, .{});')]),
    ('G4', 'X10', 'every file reads as the Ring surface', FACTS,
     [('        try str(w, if (lift.isHaro(paths[fi])) "haro" else "ring");', '        try str(w, if (false) "haro" else "ring");')]),
    ('G5', 'X04', 'every finding goes to its file\'s top', FACTS,
     [('        if (fnAtRow(file_fns[fi], f.row)) |j|', '        if (@as(?usize, null)) |j|')]),
    ('G6', 'X03', 'a function runs to its file\'s end', FACTS,
     [('        for (defs[fi].items) |s| if (s > start) {', '        for (defs[fi].items) |s| if (false and s > start) {')]),
    ('G7', 'X03', 'a function\'s blank lines at its end are kept', FACTS,
     [('        while (end > start and std.ascii.isWhitespace(root.src[end - 1])) end -= 1;',
       '        while (false and end > start and std.ascii.isWhitespace(root.src[end - 1])) end -= 1;')]),
    # G8 MISSED on its first run, switching off the fold in the call lists alone: the lambda's call is one the compiler patched, folded
    # by the second loop. The protection is the pair; G8 switches both off.
    ('G8', 'X07', 'a lambda\'s calls are not its function\'s', FACTS,
     [('        const from = real(d.funcs, raw);', '        const from = if (false) real(d.funcs, raw) else raw;'),
      ('|n| try statics[real(d.funcs, fx.from)].append(a, n);', '|n| try statics[fx.from].append(a, n);')]),
    ('G9', 'X06', 'the calls the compiler patched are not read', FACTS,
     [('        if (try display(a, d, fx.fidx)) |n| try statics[real(d.funcs, fx.from)].append(a, n);',
       '        if (false) if (try display(a, d, fx.fidx)) |n| try statics[real(d.funcs, fx.from)].append(a, n);')]),
    ('G10', 'X06', 'a late call is not recorded', COMP,
     [('        try self.cur.calls_late.append(self.alloc, try self.nameIndex(callee));', '')]),
    ('G11', 'X08', 'the last impurity met wins, not the first', FACTS,
     [('                if (out[j] == null) out[j] = imp;', '                out[j] = imp;')]),
    ('G12', 'X08', 'the walk does not enter a node', FACTS,
     [('        if (ts.c.ts_tree_cursor_goto_first_child(&cur)) continue;', '        if (false and ts.c.ts_tree_cursor_goto_first_child(&cur)) continue;')]),
    ('G13', 'X10', 'a refused function says no why', FACTS,
     [('                if (@intFromPtr(r.src.ptr) != @intFromPtr(root.src.ptr) or r.byte < x.start or r.byte >= x.end) continue;',
       '                if (true or @intFromPtr(r.src.ptr) != @intFromPtr(root.src.ptr) or r.byte < x.start or r.byte >= x.end) continue;')]),
    ('G14', 'X10', 'a function refused itself also reaches the unfinished', FACTS,
     [('.{if (f.poisoned and !f.poisoned_own) "true" else "false"}', '.{if (f.poisoned) "true" else "false"}')]),
    ('G15', 'X13', 'the variable rule\'s silence is not said', HARO,
     [('            if (!uni.complete_vars) try nc.append(alloc, .{ .rules = &.{"haro/uninitialized-variable"}, .why = if (uni.reason.len > 0)',
       '            if (false and !uni.complete_vars) try nc.append(alloc, .{ .rules = &.{"haro/uninitialized-variable"}, .why = if (uni.reason.len > 0)')]),
]

NL = chr(10)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (FACTS, HARO, COMP, BUILD)}

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
            if b.returncode != 0:
                restore()
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            # the court reads @COMMIT while the plant stands, as the build did
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=900)
            restore()
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
