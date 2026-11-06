"""Every protection of D52 rung (4) switched off in turn: the rule court must fail, for the fixture that protection exists for (the W discipline).

Each plant is one or more text substitutions in one of vm/src/check.zig, types.zig, lift.zig, haro.zig. The VM is built with the plant into
runtime/v39/plant-build (ReleaseFast, -j2, one build at a time: the machine's rule), the rule court is run on that build alone, and every file is
restored byte for byte before the next plant -- verified by its digest, and restored even when a build fails or the script is stopped. zig-out and
zig-out-safe are never touched. A substitution that removes a line keeps every name it leaves still used: Zig refuses an unused one.

Printed is CAUGHT with the fixtures that failed, or MISSED: a protection no fixture pins, and the answer to it is a fixture.

  python spike/v39/plants.py            all plants (about a minute each)
  python spike/v39/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
OUT = os.path.join(ROOT, 'runtime', 'v39', 'plant-build')
COURT = os.path.join(HERE, 'rule_court.py')

PLANTS = [
    # ---- R1 last-error-read
    ('P1', 'L03', 'check.zig', 'a member named cCatchError is read as the name', [
        ('            if (std.mem.eql(u8, pk, "member_expression") and par.namedChildCount() > 0 and par.namedChild(0).startByte() != n.startByte()) return;\n', '')]),
    ('P2', 'L03', 'check.zig', 'a write of cCatchError is read as a read', [
        ('            if (std.mem.eql(u8, pk, "assignment_expression") and par.namedChildCount() > 0 and par.namedChild(0).startByte() == n.startByte()) return;\n', '')]),
    ('P3', 'L03', 'check.zig', 'a catch binding named cCatchError is read as a read', [
        ('            if (std.mem.eql(u8, pk, "catch_clause")) return;\n', '')]),
    ('P4', 'L01', 'check.zig', 'a read in its handler is worded as one outside', [
        ('        const in_handler = hasAncestor(n, "catch_clause");', '        const in_handler = hasAncestor(n, "catch_clause_never");')]),
    # ---- R2 text-run-as-code
    ('P5', 'T02', 'check.zig', 'literal text is judged too', [
        ('        if (literalText(arg)) return;\n', '        _ = literalText(arg);\n')]),
    ('P6', 'T02', 'check.zig', 'a `+` of literals is not literal text', [
        ('            if (std.mem.eql(u8, ch.kind(), "+")) plus = true else return false;', '            if (std.mem.eql(u8, ch.kind(), "++")) plus = true else return false;')]),
    ('P7', 'T03', 'check.zig', 'a validator in the body clears nothing', [
        ('                if (callsAny(b, self.validators)) return;', '                _ = callsAny(b, self.validators);')]),
    ('P8', 'T05', 'check.zig', 'a validator anywhere in the file clears the eval', [
        ('''            if (ownerOf(n)) |f| {
                try bodyNodes(self.gpa, f, &body);
            } else {''', '''            if (ownerOf(n)) |f| {
                _ = f;
                var top0 = n;
                while (!top0.parent().isNull()) top0 = top0.parent();
                try body.append(self.gpa, top0);
            } else {''')]),
    # ---- R3 listener-binds-all
    ('P9', 'N01', 'check.zig', '"" is no bind address', [
        ('std.mem.eql(u8, v, "::") or v.len == 0) {', 'std.mem.eql(u8, v, "::") or v.len == 99) {')]),
    ('P10', 'N03', 'check.zig', 'every call is a listener', [
        ('        if (callee.len == 0 or !inNames(callee, self.listeners)) return;', '        if (callee.len == 0) return;')]),
    ('P11', 'N02', 'haro.zig', 'told of no listener, the checker says nothing', [
        ('        if (listeners.items.len == 0) try w.print("  listener-binds-all: no listening native named (--listeners=), so no call was looked at\\n", .{});\n', '')]),
    # ---- R4 global-restored-by-hand
    ('P12', 'G03', 'check.zig', 'a restore in a finally is by hand too', [
        ('            if (in_finally) continue;', '            if (in_finally and false) continue;')]),
    ('P13', 'G02', 'check.zig', 'a restore in a catch is worded as none', [
        ('                if (hasAncestor(b, "catch_clause")) in_catch = true;', '                if (hasAncestor(b, "catch_clause_never")) in_catch = true;')]),
    ('P14', 'G05', 'check.zig', 'a write-back before its save counts', [
        ('                if (b.startByte() <= s.startByte()) continue;\n', '')]),
    ('P15', 'G05', 'check.zig', 'any two names saved and written back count, `$` or not', [
        ("            if (!(local.len > 0 and local[0] != '$' and local[0] != '@' and g.len > 1 and g[0] == '$')) continue;\n", '')]),
    ('P16', 'G05', 'check.zig', 'a compound write is a write-back', [
        ('''            if (std.mem.eql(u8, n.child(i).kind(), "=")) plain = true;''', '''            if (n.child(i).kind().len > 0) plain = true;''')]),
    ('P17', 'G01', 'check.zig', 'a body is the definition alone, not the statements the grammar left after it', [
        ('''    try out.append(gpa, f);
    var s = f.nextNamedSibling();
    while (!s.isNull()) : (s = s.nextNamedSibling()) {
        const k = s.kind();
        if (std.mem.eql(u8, k, "function_definition") or std.mem.eql(u8, k, "class_definition")) break;
        try out.append(gpa, s);
    }''', '''    try out.append(gpa, f);''')]),
    # ---- R5 handle-held-across-raise
    ('P18', 'H03', 'check.zig', 'a handle the body returns is held', [
        ('                if (returns(b, local) or releasedInFinally(b, local)) kept = true;', '                if (releasedInFinally(b, local)) kept = true;')]),
    ('P19', 'H02', 'check.zig', 'a release in a finally does not count', [
        ('                if (returns(b, local) or releasedInFinally(b, local)) kept = true;', '                if (returns(b, local)) kept = true;')]),
    ('P20', 'H02', 'check.zig', 'Destroy is no release', [
        ('std.ascii.indexOfIgnoreCase(c, "release") != null or std.ascii.indexOfIgnoreCase(c, "destroy") != null or',
         'std.ascii.indexOfIgnoreCase(c, "release") != null or std.ascii.indexOfIgnoreCase(c, "destroy_never") != null or')]),
    ('P21', 'H03', 'check.zig', 'a handle in a global is the body\'s', [
        ("            if (local.len == 0 or local[0] == '$' or local[0] == '@') continue;\n            if (classDeclares", "            if (local.len == 0) continue;\n            if (classDeclares")]),
    ('P22', 'H04', 'check.zig', 'any Create is an engine handle', [
        ('std.ascii.startsWithIgnoreCase(callee, "stzengine") and', 'std.ascii.startsWithIgnoreCase(callee, "") and')]),
    ('P23', 'H05', 'check.zig', 'an attribute the class declares is a local', [
        ('            if (classDeclares(f, local)) continue;\n', '')]),
    ('P24', 'H06', 'check.zig', 'a method the grammar left after its class has no class', [
        ('''        cls = f.prevNamedSibling();
        while (!cls.isNull() and !std.mem.eql(u8, cls.kind(), "class_definition")) cls = cls.prevNamedSibling();
        if (cls.isNull()) return false;''', '''        return false;''')]),
    ('P25', 'H06', 'check.zig', 'a class\'s statements end where the grammar ended the class', [
        ('''    var s = cls.nextNamedSibling();
    while (!s.isNull()) : (s = s.nextNamedSibling()) {
        if (std.mem.eql(u8, s.kind(), "function_definition") or std.mem.eql(u8, s.kind(), "class_definition")) return false;
        if (declares(s, name)) return true;
    }
    return false;''', '''    return false;''')]),
    # ---- reading the lifted tree
    ('P26', 'L05', 'check.zig', 'a finding on a rewritten line is named at the lifted text\'s column', [
        ('''        const at = lift.fileByte(inserts, ls + f.col - 1);
        f.col = at - lift.fileByte(inserts, ls) + 1;''', '''        _ = lift.fileByte(inserts, ls + f.col - 1);''')]),
    ('P27', 'L03', 'types.zig', 'a catch binding is no write', [
        ('''                std.mem.eql(u8, k, "postfix_expression") or
                std.mem.eql(u8, k, "catch_clause"))''', '''                std.mem.eql(u8, k, "postfix_expression"))''')]),
    ('P28', 'G03', 'types.zig', 'a block\'s word is read as a variable', [
        ('''        if (!par.isNull() and lift.blockWord(par) != null and !par.parent().isNull() and std.mem.eql(u8, par.parent().kind(), "try_statement")) return;\n''', '')]),
    ('P29', 'L03', 'haro.zig', 'the checker reads the file\'s raw text, not the lifted tree', [
        ('            check.checkLifted(alloc, r, path, &report, ctx, opts, unit.inserts.items[i]) catch continue;',
         '            _ = r;\n            check.checkSourceCtx(alloc, parser, path, unit.origs.items[i], &report, ctx) catch continue;\n            _ = opts;')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    files = {f: os.path.join(VM_DIR, 'src', f) for f in ('check.zig', 'types.zig', 'lift.zig', 'haro.zig')}
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
            failed = re.findall(r'^  FAIL ([LTNGH]\d+)', out, re.M)
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
