"""Every protection of D52 rung (3) switched off in turn: the block court must fail, for the fixture that protection exists for (the W discipline).

Each plant is one or more text substitutions in one of vm/src/compile.zig, lift.zig, fmt.zig. The VM is built with the plant into
runtime/v38/plant-build (ReleaseFast, -j2, one build at a time: the machine's rule), the block court is run on that build alone, and every file is
restored byte for byte before the next plant -- verified by its digest, and restored even when a build fails or the script is stopped. zig-out and
zig-out-safe are never touched. A substitution that removes a line keeps every name it leaves still used: Zig refuses an unused one (v36 P4, P6).

Printed is CAUGHT with the fixtures that failed, or MISSED: a protection no fixture pins, and the answer to it is a fixture.

Removed, not planted: P11 (a copy of the saved value: the VM copies a shared list before writing it) and P20 (the class check skipped in an
eval: there the compiler's class table is empty and findClass answers null) MISSED on their first run -- nothing depended on them, so they went.

Not planted, named: `blockSite`'s refusal of a site with no `finally` is unreachable through the grammar (a try needs a catch or a finally, and a
catch is refused first); it guards a hand-written `try within ... catch ... done` from compiling with no restore.

  python spike/v38/plants.py            all plants (about a minute each)
  python spike/v38/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
OUT = os.path.join(ROOT, 'runtime', 'v38', 'plant-build')
COURT = os.path.join(HERE, 'block_court.py')

PLANTS = [
    # ---- the lift
    ('P1', 'W01', 'lift.zig', 'the blocks are not rewritten', [
        ('    const bl = blocks(alloc, parser, tree_in, src_in);', '    const bl: Lifted = .{ .tree = tree_in, .src = src_in };')]),
    ('P2', 'U01', 'lift.zig', 'the header is looked for among the siblings only', [
        ('''        const p = cur.parent();
        if (p.isNull()) return null;
        cur = p;''', '''        _ = &cur;
        return null;''')]),
    ('P3', 'B01', 'lift.zig', 'a `done` the grammar read as a try\'s end closes nothing', [
        ('} else if (eq(k, "done") or ((eq(k, "end")', '} else if (false or ((eq(k, "end")')]),
    ('P4', 'B01', 'lift.zig', 'a `try` opens nothing', [
        ('} else if (eq(k, "try")) {', '} else if (eq(k, "try_never")) {')]),
    ('P5', 'B10', 'lift.zig', 'a try\'s other ends close nothing', [
        ('(eq(k, "end") or eq(k, "endtry") or eq(k, "}"))', '(eq(k, "endtry") or eq(k, "}"))')]),
    ('P6', 'B08', 'lift.zig', 'a header on a later line counts', [
        ('n.start().row != marker.start().row', 'n.start().row < marker.start().row')]),
    ('P7', 'W01', 'lift.zig', 'a bare `done` closes nothing', [
        ('            if (isBareDone(ch)) {', '            if (isBareDone(ch) and false) {')]),
    # ---- within
    ('P8', 'W01', 'compile.zig', 'the global is not restored', [
        ('            } else _ = try self.emit(.gset, b.save, 0, 0, b.slot);', '            }')]),
    ('P9', 'W06', 'compile.zig', 'the value is assigned before the global is saved', [
        ('''            if (!b.using) {
                b.slot = try self.globalSlot(b.name.text());''', '''            if (!b.using) try self.stmt(n.namedChild(1));
            if (!b.using) {
                b.slot = try self.globalSlot(b.name.text());'''),
        ('''            try self.stmt(n.namedChild(1));
            if (b.using) try self.usingVerb(b.*, false);''', '''            if (b.using) try self.stmt(n.namedChild(1));
            if (b.using) try self.usingVerb(b.*, false);''')]),
    ('P10', 'W09', 'compile.zig', 'a local may be a within\'s name', [
        ("            if (!(t.len > 1 and t[0] == '$')) return self.nopeKind(name, R_GLOBAL);", "            _ = t;")]),
    # ---- using
    ('P12', 'U11', 'compile.zig', 'the header runs inside the handler, so a value that raises is released', [
        ('''            try self.stmt(n.namedChild(1));
            if (b.using) try self.usingVerb(b.*, false);
        }
        const arm = try self.emit(.ptry, errl.reg, 0, 0, 0);''', '''        }
        const arm = try self.emit(.ptry, errl.reg, 0, 0, 0);
        if (site) |*b| {
            try self.stmt(n.namedChild(1));
            if (b.using) try self.usingVerb(b.*, false);
        }''')]),
    ('P13', 'U06', 'compile.zig', '`new K` of a class with none of the three is not refused', [
        ('                if (!answers) return self.nopeKind(cn, R_CLASS);', '                if (!answers and false) return self.nopeKind(cn, R_CLASS);')]),
    ('P14', 'U09', 'compile.zig', 'the using name may be rebound', [
        ('            if (rebinds(n.namedChild(k), name.text())) |at| return self.nopeKind(at, R_REBIND);', '            _ = rebinds(n.namedChild(k), name.text());')]),
    ('P15', 'U07', 'compile.zig', 'nothing is checked at the entry', [
        ('            if (b.using) try self.usingVerb(b.*, false);\n', '')]),
    ('P16', 'U07', 'compile.zig', 'a value that is not an object is asked for its methods', [
        ('const not_obj = try self.emit(.jfalsy, t, 0, 0, 0);', 'const not_obj = try self.emit(.jfalsy, v, 0, 0, 0);')]),
    ('P17', 'U02', 'compile.zig', 'the verbs are tried in another order', [
        ('const USING_VERBS = [_][]const u8{ "release", "destroy", "close" };', 'const USING_VERBS = [_][]const u8{ "close", "destroy", "release" };')]),
    ('P18', 'U10', 'compile.zig', 'a value answering none is passed over in silence', [
        ('''Close", .{b.name.text()}) catch
            return Error.OutOfMemory;
        _ = try self.emit(.loadk, t, 0, 0, try self.konstIndex(msg));
        _ = try self.emit(.trap, t, 0, 0, 0);''', '''Close", .{b.name.text()}) catch
            return Error.OutOfMemory;
        _ = try self.emit(.loadk, t, 0, 0, try self.konstIndex(msg));''')]),
    ('P19', 'U12', 'compile.zig', 'an eval must name every verb', [
        ('                if (self.eval != null) continue;\n', '')]),
    # ---- every exit
    ('P21', 'W03', 'compile.zig', 'a jump out of a block runs its finally without the restore or the release', [
        ('        try self.finBody(r.node, r.site);', '        try self.finBody(r.node, null);')]),
    ('P22', 'W02', 'compile.zig', 'a raise out of a block runs its finally without the restore or the release', [
        ('''            defer borrowed = self.try_borrows.pop().?;
            try self.finBody(f, site);''', '''            defer borrowed = self.try_borrows.pop().?;
            try self.finBody(f, null);
            _ = site;''')]),
    ('P23', 'W01', 'compile.zig', 'the normal end of a block runs its finally without the restore or the release', [
        ('        if (fc) |f| try self.finBody(f, site);', '        if (fc) |f| try self.finBody(f, null);')]),
    # ---- the refusals of a block without its parts
    ('P24', 'B04', 'compile.zig', 'a bare word is compiled as the name it reads', [
        ('''        if (lift.isMarker(n)) {
            self.atNode(n);
            return self.nopeKind(lift.blockWord(n).?, R_BARE);
        }''', '')]),
    ('P25', 'B06', 'compile.zig', 'a block may have a catch of its own', [
        ('            if (std.mem.eql(u8, ch.kind(), "catch_clause")) return self.nopeKind(ch.child(0), R_CLAUSE);\n', '')]),
    ('P26', 'B07', 'compile.zig', 'a bare word on the line after a try is taken for the try\'s block', [
        ('        if (m.start().row != n.start().row) return null;\n', '')]),
    # ---- the printer
    ('P27', 'K01', 'fmt.zig', '`haro fmt` prints a block as the try it was made into', [
        ('''            g.op = if (lowerIs(sp.head[0].kids[0].text, "within")) "within" else "using";''', '''            g.op = null;''')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    files = {f: os.path.join(VM_DIR, 'src', f) for f in ('compile.zig', 'lift.zig', 'fmt.zig')}
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
            failed = re.findall(r'^  FAIL ([WUBK]\d+)', out, re.M)
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
