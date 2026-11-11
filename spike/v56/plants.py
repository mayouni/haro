"""Every protection of v0.56 (every definition ends with end, in any order; func a function, def a method; HARO-DEFINITIONS-01, D68) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (compile.zig, lift.zig), built into runtime/v56/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v56/plants.py            all plants (about two minutes each)
  python spike/v56/plants.py N1 N3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v56', 'plant-build')
COURT = os.path.join(HERE, 'def_court.py')

PLANTS = [
    ('D1', 'E02', 'a .haro file\'s pieces are placed by position, as Ring places them', COMP,
     [('        const by_tree = c.haroNode(p.node);', '        const by_tree = false;')]),
    ('D2', 'E03', 'the top level after the first definition is dropped', COMP,
     [('    const haro_file = ri < load_paths.len and lift.isHaro(load_paths[ri]);', '    const haro_file = false;')]),
    ('D4', 'E10', 'func in a class passes', COMP,
     [('                    if (method and !std.mem.eql(u8, t, "def")) return .{ R_METHOD, ch.text() };',
       '                    if (false and method and !std.mem.eql(u8, t, "def")) return .{ R_METHOD, ch.text() };')]),
    ('D5', 'E11', 'def outside a class passes', COMP,
     [('                    if (!method and !std.mem.eql(u8, t, "func")) return .{ R_FUNCTION, ch.text() };',
       '                    if (false and !method and !std.mem.eql(u8, t, "func")) return .{ R_FUNCTION, ch.text() };')]),
    ('D7', 'E05', 'a statement in a class region is the program\'s', COMP,
     [('                if (ci.node.startByte() == a.startByte() and ci.node.src.ptr == a.src.ptr) return .{ .func = null, .class = ci.id };',
       '                if (false) return .{ .func = null, .class = ci.id };')]),
    ('D9', 'E06', 'a fault the lift found does not refuse the program', COMP,
     [('            c.file_fault = .{ f.why, wordAt(root.src, f.row, f.word) };', '            if (false) c.file_fault = .{ f.why, wordAt(root.src, f.row, f.word) };')]),
    ('D10', 'E14', 'a dot that ends a line passes', COMP,
     [('                    n.child(i + 1).start().row > ch.start().row) return self.spellSet(ch.text(), R_CHAIN);',
       '                    false) return self.spellSet(ch.text(), R_CHAIN);')]),
    # the lift's reading of a definition's structure
    ('L1', 'E15', 'the definitions are given to the parser as written, without braces', LIFT,
     [('fn bracesText(alloc: std.mem.Allocator, src: []const u8, name: []const u8) ?Braced {',
       'fn bracesText(alloc: std.mem.Allocator, src: []const u8, name: []const u8) ?Braced {\n    if (src.len < 1 << 40) return null;')]),
    ('L2', 'E06', 'a definition left open is no fault', LIFT,
     [('            fault = .{ .why = R_NOEND, .word = o.name, .row = o.row };', '            if (false) fault = .{ .why = R_NOEND, .word = o.name, .row = o.row };')]),
    ('L3', 'E08', 'an end word in another spelling is no fault', LIFT,
     [('            if (fault == null) fault = .{ .why = R_ENDWORD, .word = w, .row = row };', '            if (false) fault = .{ .why = R_ENDWORD, .word = w, .row = row };')]),
    ('L4', 'E16', 'an end that closes nothing is no fault', LIFT,
     [('                if (fault == null) fault = .{ .why = R_STRAY, .word = w, .row = row };', '                if (false) fault = .{ .why = R_STRAY, .word = w, .row = row };')]),
    ('L5', 'E17', 'a body on its header\'s line is no fault', LIFT,
     [('                if (o.row == row) {', '                if (false) {')]),
    ('L6', 'E18', 'a block\'s other end word closes nothing', LIFT,
     [('            if (stack.items.len > 0 and !stack.items[stack.items.len - 1].def) _ = stack.pop();\n            continue;',
       '            continue;')]),
    ('L7', 'E19', 'a block\'s closing brace closes nothing', LIFT,
     [('                if (stack.items.len > 0 and stack.items[stack.items.len - 1].braced) _ = stack.pop();', '                {}')]),
    ('L8', 'E04', 'within opens no block in the scan', LIFT,
     [('            if (e > k and q < n and src[q] == \'=\' and !(q + 1 < n and src[q + 1] == \'=\'))', '            if (false)')]),
    ('L9', 'E20', 'an end an eval span gave away closes no block', LIFT,
     [('    if (!eq(parent, "function_definition") and !eq(parent, "class_definition") and !eq(parent, "package_definition") and !eq(parent, "ERROR"))',
       '    if (parent.len < 1000000)')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (COMP, LIFT)}

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
