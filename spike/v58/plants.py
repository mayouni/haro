"""Every protection of v0.58 (absence: none, maybe, resolved where it lands; HARO-ABSENCE-01, D70) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (compile.zig, lift.zig), built into runtime/v58/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v58/plants.py            all plants (about two minutes each)
  python spike/v58/plants.py N1 N3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v58', 'plant-build')
COURT = os.path.join(HERE, 'absence_court.py')

PLANTS = [
    ('A1', 'M01', 'an else that resolves a maybe is compiled as or', COMP,
     [('        if (self.haroNode(n) and self.isElse(n)) {\n            try self.expr(n.namedChild(0), dst);',
       '        if (false and self.haroNode(n) and self.isElse(n)) {\n            try self.expr(n.namedChild(0), dst);')]),
    ('A2', 'M02', 'a maybe function that ends without a return gives ""', COMP,
     [('            if (f.maybe) {\n                _ = try c.emit(.ldnone, tr, 0, 0, 0);',
       '            if (false and f.maybe) {\n                _ = try c.emit(.ldnone, tr, 0, 0, 0);')]),
    ('A3', 'M04', 'a maybe given to a local passes', COMP,
     [('            const assigned = std.mem.eql(u8, pk, "assignment_expression") and par.namedChild(0).startByte() == n.startByte();',
       '            const assigned = std.mem.eql(u8, pk, "assignment_expression");')]),
    ('A4', 'M05', 'a maybe passed as an argument passes', COMP,
     [('            if (!assigned and !returned and !alone) {', '            if (false and !assigned and !returned and !alone) {')]),
    ('A5', 'M06', 'none returned by a function not declared maybe passes', COMP,
     [('            const in_return = std.mem.eql(u8, pk, "return_statement") and self.cur.maybe;',
       '            const in_return = std.mem.eql(u8, pk, "return_statement");')]),
    ('A6', 'M07', 'none given to a local passes', COMP,
     [('            if (!in_return and !to_attr) self.spellSet(n.text(), R_NONE);', '            if (false and !in_return and !to_attr) self.spellSet(n.text(), R_NONE);')]),
    ('A7', 'M08', 'a maybe attribute is not recorded', COMP,
     [('                    if (declared.len > 0 and c.haroNode(p.node) and c.maybeRow(p.node)) try c.maybe_attrs.put(alloc, declared, {});', '')]),
    ('A8', 'M08', 'a none attribute raises R24 when read', MAIN,
     [('                if (av.tag == .nil and av.p.i != NONE_MARK) {', '                if (av.tag == .nil) {')]),
    ('A9', 'M10', 'else after a value that is never none passes', COMP,
     [('            if (self.maybeName(l) == null) return self.spellSet(l.text(), R_ELSE);', '')]),
    ('A10', 'M11', 'an if\'s else on its own line is read as a resolution', LIFT,
     [('            if (!top_here) {\n                const ls =', '            if (true or !top_here) {\n                const ls =')]),
    ('A11', 'M01', 'the VM never takes D', MAIN,
     [('                if (regs[base + in.a].tag == .nil) {\n                    pc = @intCast(in.d);',
       '                if (regs[base + in.a].tag == .nil and false) {\n                    pc = @intCast(in.d);')]),
    ('A12', 'M01', 'a maybe header is not blanked', LIFT,
     [('        @memcpy(text[e + shift .. e + shift + 5], "     ");', '        _ = text[e + shift];')]),
    ('B1', 'M17', 'the VM converts no .ring caller 1 or 0', MAIN,
     [("                if (in.c == 1 and in.b == 'b' and v.tag == .int and (v.p.i == 0 or v.p.i == 1) and fsp > 0 and",
       "                if (in.c == 9 and in.b == 'b' and v.tag == .int and (v.p.i == 0 or v.p.i == 1) and fsp > 0 and")]),
    ('B2', 'M17', 'the compiler marks no b parameter check', COMP,
     [("                    if (pl == 'b' and c.code.items[c.code.items.len - 1].c == 0) c.code.items[c.code.items.len - 1].c = 1;", "")]),
    ('B3', 'M18', 'a .haro caller 1 converts too', MAIN,
     [("                    !self.strictAt(self.frames[fsp - 1].ret_pc -| 1))", "                    self.frames[fsp - 1].ret_pc < 1 << 31)")]),
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
