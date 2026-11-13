"""Every protection of v0.69 (`haro check` names what the run refuses; HARO-CHECKRUN-01) switched off in turn: the court must fail, for
the fixture that protection exists for. Each plant is text substitutions in vm/src, built into runtime/v69/plant-build (ReleaseFast, -j2,
one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests, and restored even
when a build fails or the script is stopped.

  python spike/v69/plants.py            all plants (about two minutes each)
  python spike/v69/plants.py K1 K3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
UNI = os.path.join(VM_DIR, 'src', 'universe.zig')
FACTS = os.path.join(VM_DIR, 'src', 'facts.zig')
TS = os.path.join(VM_DIR, 'src', 'ts.zig')
OUT = os.path.join(ROOT, 'runtime', 'v69', 'plant-build')
COURT = os.path.join(HERE, 'checkrun_court.py')

PLANTS = [
    ('K1', 'S01', 'check asks the compiler and keeps none of its answers', HARO,
     [('const trapped: []const co.Trapped = if (fdata) |d| d.trapped else &.{};', 'const trapped: []const co.Trapped = if (fdata) |d| d.trapped[0..0] else &.{};')]),
    ('K2', 'U01', 'a refused form is not placed in its own file, so it falls under the unit\'s first', HARO,
     [('        if (placed[k] or t.src != root.src.ptr) continue;\n        placed[k] = true;\n        var twice = false;',
       '        if (placed[k] or t.src != root.src.ptr or t.row > 0) continue;\n        placed[k] = true;\n        var twice = false;')]),
    ('K3', 'M01', 'a file\'s refused forms in the compiler\'s order, not the file\'s', HARO,
     [('    std.mem.sort(usize, mine.items, trapped, byRow);\n', '    _ = byRow;\n')]),
    ('K4', 'S01', 'a statement the compiler traps twice is named twice', HARO,
     [('        if (!twice) try mine.append(alloc, k);', '        if (!twice or t.row > 0) try mine.append(alloc, k);')]),
    ('K5', 'W01', 'a trap the compiler rolled back is kept', COMP,
     [('        if (standing.contains(t.konst)) try kept.append(alloc, t);', '        if (standing.contains(t.konst) or t.row > 0) try kept.append(alloc, t);')]),
    ('K6', 'T01', 'a closed function holds the statements after it', UNI,
     [('            if (!c.closedByEnd()) seen_def = true;', '            seen_def = true;')]),
    ('K7', 'T02', 'a closed class holds the statements after it', UNI,
     [('            if (!c.closedByEnd()) {\n                seen_def = true;\n                seen_class = true;\n            }',
       '            {\n                seen_def = true;\n                seen_class = true;\n            }')]),
    ('K8', 'T04', 'the facts run a closed function to the next definition', FACTS,
     [('        if (f.node.closedByEnd()) end = f.node.endByte();\n', '')]),
    ('K9', 'N01', 'the brace the lift writes for a definition\'s `end` is not read as its end', TS,
     [('        return std.mem.eql(u8, k, "end") or std.mem.eql(u8, k, "}");', '        return std.mem.eql(u8, k, "end");')]),
    ('K10', 'S02', 'the finding gives the reason without what was written', HARO,
     [('        .message = if (t.named) try std.fmt.allocPrint(a, "{s} `{s}`", .{ t.kind, t.text }) else try a.dupe(u8, t.kind),',
       '        .message = try a.dupe(u8, t.kind),')]),
    ('K11', 'S01', 'a refused form is a warning', HARO,
     [('        .severity = .err,\n        .rule = "haro/refused-form",', '        .severity = .warn,\n        .rule = "haro/refused-form",')]),
    ('K12', 'T03', 'every definition is read as closed, a .ring file\'s too', TS,
     [('        return std.mem.eql(u8, k, "end") or std.mem.eql(u8, k, "}");', '        return k.len > 0;')]),
    ('K13', 'S01', 'the record keeps the line after the trap\'s', COMP,
     [('        .row = row,\n        .src = c.last_fail_src orelse st.src.ptr,', '        .row = row + 1,\n        .src = c.last_fail_src orelse st.src.ptr,')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (HARO, COMP, UNI, FACTS, TS)}

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
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=1800)
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
