"""Every protection of v0.47 (the letters, D55 T2) switched off in turn: the court named must fail, for the fixture that protection
exists for.

Each plant is one text substitution in vm/src/compile.zig or main.zig, written so that no name is left unused (Zig refuses one). The
VM is built with the plant into runtime/v47/plant-build (ReleaseFast, -j2, one build at a time), the court is run on that build alone,
and the file is restored byte for byte before the next plant -- verified by its digest, and restored even when a build fails or the
script is stopped. L12 MISSED on its first run (Y11 gave its checked name only a literal, settled when compiling): Y16 was written
after the plants and L12 points at it. L14 is judged by v42's name court: the spelling fault speaking first is a v42 case's question (N03, N19).

  python spike/v47/plants.py            all plants (about a minute each)
  python spike/v47/plants.py L3 L7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v47', 'plant-build')
LETTER = os.path.join(HERE, 'letter_court.py')
NAME = os.path.join(ROOT, 'spike', 'v42', 'name_court.py')

PLANTS = [
    ('L1', 'Y02', LETTER, COMP, 'a name with no letter passes',
     '        if (l == 0 or std.mem.indexOfScalar(u8, LETTERS, l) == null)', '        if (false and (l == 0 or std.mem.indexOfScalar(u8, LETTERS, l) == null))'),
    ('L2', 'Y03', LETTER, COMP, "Softanza's c is refused as any unknown letter, its todo lost", "        if (l == 'c')", "        if (false and l == 'c')"),
    ('L3', 'Y04', LETTER, COMP, 'a literal of another type is accepted', '        if (letterTakes(l, lit)) return true;', '        if (true or letterTakes(l, lit)) return true;'),
    ('L4', 'Y12', LETTER, COMP, 'an integer letter takes a number with a point', "            else => lit == l,", "            else => lit == l or (l == 'i' and lit == 'n'),"),
    ('L5', 'Y10', LETTER, COMP, 'null is a text literal like any other', "        if (lit == '0') return true;", "        if (false and lit == '0') return true;"),
    ('L6', 'Y05', LETTER, MAIN, 'lchk lets any value through', '                if (!ok) {\n                    const nm = konst[@intCast(in.d)];',
     '                if (false and !ok) {\n                    const nm = konst[@intCast(in.d)];'),
    ('L7', 'Y05', LETTER, COMP, "the check reports Ring's F-114 row, the next token's", "        // the statement's own line: Ring's F-114 row (the next token's, after a statement's last call) is not a .haro statement's\n        self.atNodeStart(n);",
     "        // the statement's own line: Ring's F-114 row (the next token's, after a statement's last call) is not a .haro statement's\n        if (false) self.atNodeStart(n);"),
    ('L8', 'Y06', LETTER, COMP, 'a parameter is not checked on entry', '                if (c.lookup(p)) |lp| try c.emitLetterCheck(lp.reg, pl, p);',
     '                if (false) if (c.lookup(p)) |lp| try c.emitLetterCheck(lp.reg, pl, p);'),
    ('L9', 'Y15', LETTER, COMP, "a parameter's shape is not judged", '                if (c.entry_fault == null) if (c.letterFault(p, false)) |why| {',
     '                if (false and c.entry_fault == null) if (c.letterFault(p, false)) |why| {'),
    ('L10', 'Y14', LETTER, COMP, 'a for-in counter is not checked',
     '                if (std.mem.indexOfScalar(u8, CHECKED, vl) != null) try self.emitLetterCheck(xr, vl, vname);',
     '                if (false and std.mem.indexOfScalar(u8, CHECKED, vl) != null) try self.emitLetterCheck(xr, vl, vname);'),
    ('L11', 'Y07', LETTER, COMP, 'a single letter is refused as a for counter too',
     '        if (self.spell_on and self.eval == null and self.letterShape(vname, true)) {', '        if (self.spell_on and self.eval == null and self.letterShape(vname, false)) {'),
    ('L12', 'Y16', LETTER, COMP, 'the checks reach a .ring file',
     '        const named: ?[]const u8 = if (self.eval != null or !self.spell_on) null else', '        const named: ?[]const u8 = if (self.eval != null) null else'),
    ('L15', 'Y16', LETTER, COMP, "a .ring function's lettered parameters are checked on entry",
     '        if (!f.is_main and c.eval == null and f.params.len > 0 and c.haroNode(f.node)) {',
     '        if (!f.is_main and c.eval == null and f.params.len > 0 and (true or c.haroNode(f.node))) {'),
    ('L13', 'Y13', LETTER, COMP, 'an attribute through This and a bare one are not lettered',
     '        else if (std.mem.eql(u8, lhs.kind(), "member_expression") and self.isThis(lhs.namedChild(0)))\n            lhs.namedChild(1).text()\n        else\n            null;\n        const use = named orelse return self.assignBody(n);',
     '        else if (std.mem.eql(u8, lhs.kind(), "member_expression") and self.isThis(lhs.namedChild(0)))\n            lhs.namedChild(1).text()\n        else\n            null;\n        const use = (if (self.cur.owner != null) null else named) orelse return self.assignBody(n);'),
    ('L14', 'N03', NAME, COMP, 'the letter fault speaks before the spelling fault', '            if (self.spell_fault == null) self.spellSet(use, why);', '            self.spellSet(use, why);'),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {f: open(f, 'rb').read() for f in (MAIN, COMP)}

    def restore():
        for f, b in originals.items():
            open(f, 'wb').write(b)
            assert digest(open(f, 'rb').read()) == digest(b)

    results = []
    try:
        for pid, fixture, court, src, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            raw_text = originals[src].decode('utf-8')
            crlf = (chr(13) + chr(10)) in raw_text
            text = raw_text.replace(chr(13) + chr(10), chr(10))
            if text.count(old) != 1:
                print(f'{pid} STALE: the text stands {text.count(old)} times: {old[:70]!r}', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text.replace(old, new)
            open(src, 'wb').write((planted.replace(chr(10), chr(13) + chr(10)) if crlf else planted).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, court, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
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
