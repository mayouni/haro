"""Every protection of v0.55 (one form for each construct, HARO-ONEFORM-01, D67) switched off in turn: the court must fail, for the fixture
that protection exists for. Each plant is text substitutions in vm/src (compile.zig, lift.zig), built into runtime/v55/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

  python spike/v55/plants.py            all plants (about two minutes each)
  python spike/v55/plants.py N1 N3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
OUT = os.path.join(ROOT, 'runtime', 'v55', 'plant-build')
COURT = os.path.join(HERE, 'oneform_court.py')

PLANTS = [
    ('N1', 'O01', 'an old end word passes', COMP,
     [('                if (block and i + 1 == cnt and oldEnd(t)) return self.spellSet(ch.text(), R_END);',
       '                if (false and block and i + 1 == cnt and oldEnd(t)) return self.spellSet(ch.text(), R_END);')]),
    ('N2', 'O06', 'a block\'s braces pass', COMP,
     [('                if (block and (std.mem.eql(u8, t, "{") or std.mem.eql(u8, t, "}"))) return self.spellSet(ch.text(), R_BRACE);',
       '                if (false and block and (std.mem.eql(u8, t, "{") or std.mem.eql(u8, t, "}"))) return self.spellSet(ch.text(), R_BRACE);')]),
    ('N3', 'O13', 'no word has a one spelling', COMP,
     [('        for (table) |e| if (std.mem.eql(u8, k, e.w) and (e.p.len == 0 or std.mem.eql(u8, parent, e.p))) return e.why;',
       '        for (table) |e| if (false and std.mem.eql(u8, k, e.w) and (e.p.len == 0 or std.mem.eql(u8, parent, e.p))) return e.why;')]),
    ('N4', 'O28', 'self inside a brace object is refused too', COMP,
     [('                if (std.mem.eql(u8, n.text(), "self") and !self.brace_walk and self.braces.items.len == 0)',
       '                if (std.mem.eql(u8, n.text(), "self"))')]),
    ('N5', 'O24', 'self outside a brace passes', COMP,
     [('                if (std.mem.eql(u8, n.text(), "self") and !self.brace_walk and self.braces.items.len == 0)',
       '                if (false)')]),
    ('N6', 'O27', 'a trailing period passes', COMP,
     [('                if (std.mem.eql(u8, k, "expression_statement") and i + 1 == cnt and std.mem.eql(u8, t, "."))',
       '                if (false and std.mem.eql(u8, k, "expression_statement") and i + 1 == cnt and std.mem.eql(u8, t, "."))')]),
    ('N7', 'O09', 'a definition\'s end word passes', COMP,
     [('                    std.mem.eql(u8, t, "endclass") or std.mem.eql(u8, t, "endpackage")) return .{ R_DEF, ch.text() };',
       '                    std.mem.eql(u8, t, "endclass") or std.mem.eql(u8, t, "endpackage")) {}')]),
    ('N8', 'O26', 'bare parameters pass', COMP,
     [('                if (!p.isNull() and rparen == null) return .{ R_PARAMS, p.text() };',
       '                if (false and !p.isNull() and rparen == null) return .{ R_PARAMS, p.text() };')]),
    ('N9', 'O25', 'empty parentheses pass', COMP,
     [('                if (p.isNull()) if (rparen) |r| {', '                if (false) if (rparen) |r| {')]),
    ('N10', 'O22', 'a parent after : passes', COMP,
     [('                            if (!m.isNamed() and (std.mem.eql(u8, m.kind(), ":") or std.mem.eql(u8, m.kind(), "<")))',
       '                            if (false and !m.isNamed() and (std.mem.eql(u8, m.kind(), ":") or std.mem.eql(u8, m.kind(), "<")))')]),
    ('N11', 'O23', 'a comment beside the definition is not read', COMP,
     [('                while (!s.isNull() and std.mem.eql(u8, s.kind(), "comment")) : (s = s.nextNamedSibling())',
       '                while (false and !s.isNull() and std.mem.eql(u8, s.kind(), "comment")) : (s = s.nextNamedSibling())')]),
    ('N12', 'O11', 'a class around the method is not read', COMP,
     [('        while (!n.isNull()) : (n = n.parent()) {', '        while (!n.isNull() and std.mem.eql(u8, n.kind(), "function_definition")) : (n = n.parent()) {')]),
    ('N13', 'O12', 'a definition\'s words are never asked', COMP,
     [('        if (c.entry_fault == null and !f.is_main and c.eval == null and c.haroNode(f.node)) if (c.defForm(f.node)) |ff| {',
       '        if (false and c.entry_fault == null and !f.is_main and c.eval == null and c.haroNode(f.node)) if (c.defForm(f.node)) |ff| {')]),
    ('N14', 'O07', 'an end a definition took closes no within', LIFT,
     [('fn defEnd(parent: []const u8, k: []const u8) bool {', 'fn defEnd(parent: []const u8, k: []const u8) bool {\n    if (true) return false;')]),
    ('N15', 'O30', 'a block inside a within opens nothing', LIFT,
     [('        } else if (i == 0 and opensBlock(n.kind())) {', '        } else if (false and i == 0 and opensBlock(n.kind())) {')]),
    ('N16', 'O08', 'the statement walk is never asked', COMP,
     [('            self.oneForm(what);', '            if (false) self.oneForm(what);')]),
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
