"""Every protection of v0.42 (case-exact names, D55) switched off in turn: the name court must fail, for the fixture that protection exists for.

Each plant is one text substitution in vm/src/compile.zig. The VM is built with the plant into runtime/v42/plant-build (ReleaseFast, -j2, one
build at a time), the name court is run on that build alone, and the file is restored byte for byte before the next plant -- verified by its
digest, and restored even when a build fails or the script is stopped.

Removed after planting, named: P16, the check that a name stands in the statement's own text -- switched off, no case moved, and two probes
(a misspelling in a later statement; a .haro call of a .ring function whose body spells `NN` for its `nN`) read the same; v42/GRAMMAR.md.

Not planted, named: the census's report of a spelling refusal (no court reads the census; the migration of Haro's code was checked with it);
the refusal's text when a declaration's file cannot be named (no case declares a global in another file).

  python spike/v42/plants.py            all plants (about a minute each)
  python spike/v42/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
SRC = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v42', 'plant-build')
COURT = os.path.join(HERE, 'name_court.py')

PLANTS = [
    ('P1', 'N02', 'a local is not checked', '                if (self.spell_on) self.spellAt(name, l.name, "");\n', ''),
    ('P2', 'N05', 'a function is not checked', '        if (self.spell_on) self.spellFunc(name, f);\n', ''),
    ('P3', 'N06', 'two functions differing by case are not looked for',
     '        if (f.owner == null) for (self.funcs.items) |*g| {', '        if (false) for (self.funcs.items) |*g| {'),
    # P4 RE-POINTED 2026-11-09 (v0.48): the check names the native the call resolved to beside the spelling written
    ('P4', 'N07', 'a native is not checked', '        if (self.spell_on) self.spellNative(written, callee);\n',
     '        if (false) self.spellNative(written, callee);\n'),
    ('P5', 'N08', 'a class is not checked', '        if (self.spell_on) self.spellAt(name, ci.name, ci.node.src);\n', ''),
    ('P6', 'N09', 'a global read is not checked',
     '            scans[0] += 1;\n            if (std.ascii.eqlIgnoreCase(g, name)) {\n                if (self.spell_on) self.spellAt(name, g, "");\n',
     '            scans[0] += 1;\n            if (std.ascii.eqlIgnoreCase(g, name)) {\n'),
    ('P7', 'N19', 'a global written is not checked',
     '            scans[1] += 1;\n            if (std.ascii.eqlIgnoreCase(g, name)) {\n                if (self.spell_on) self.spellAt(name, g, "");\n',
     '            scans[1] += 1;\n            if (std.ascii.eqlIgnoreCase(g, name)) {\n'),
    ('P8', 'N10', 'an @attribute is not checked', '        if (self.spell_on) self.spellAttr(ci, name);\n        return slot;', '        return slot;'),
    ('P9', 'N15', 'a bare attribute is not checked', '                if (self.spell_on) self.spellAttr(pid, name);\n', ''),
    ('P10', 'N11', 'a method on a receiver is not checked', '        if (self.spell_on) self.spellMember(mname);\n', ''),
    ('P11', 'N12', 'a keyword in another case is not looked for', '            self.spellKeywords(what);\n', ''),
    ('P12', 'N13', 'every file is spelled as a .haro file', '        self.spell_on = self.haroNode(st);\n', '        self.spell_on = true;\n'),
    ('P13', 'N10', 'a re-read piece is not checked', '        self.spell_on = self.haroNode(st);\n',
     '        self.spell_on = self.reread_src == null and self.haroNode(st);\n'),
    ('P14', 'N05', 'the trap stands at the compiler\'s last row, not the fault\'s', '        self.cur_row = row;\n', ''),
    ('P15', 'N17', 'an eval is not checked', '    try c.stmtSpelled(s, s, false);\n}', '    try c.stmt(s);\n}'),
    ('P17', 'N14', 'a declaration in another file is not named',
     '            if (rowIn(decl_src, declared) != null) {', '            if (false) {'),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    original = open(SRC, 'rb').read()

    def restore():
        open(SRC, 'wb').write(original)
        assert digest(open(SRC, 'rb').read()) == digest(original)

    results = []
    try:
        for pid, fixture, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            text = original.decode('utf-8')
            if text.count(old) != 1:
                print(f'{pid} STALE: the text stands {text.count(old)} times: {old[:60]!r}', flush=True)
                results.append((pid, 'STALE'))
                continue
            open(SRC, 'wb').write(text.replace(old, new).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL (N\d+)', out, re.M)
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
