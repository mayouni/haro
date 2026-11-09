"""Every protection of v0.48 (a built-in spelled as Softanza writes a name, in a .haro file) switched off in turn: the court must fail, for
the fixture that protection exists for. Each plant is one text substitution in vm/src/compile.zig, built into runtime/v48/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the file restored byte for byte -- verified by its digest,
and restored even when a build fails or the script is stopped.

  python spike/v48/plants.py            all plants (about a minute each)
  python spike/v48/plants.py B1 B3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v48', 'plant-build')
COURT = os.path.join(HERE, 'builtin_court.py')

PLANTS = [
    ('B1', 'P02', 'any spelling of a built-in passes', '        if (std.mem.eql(u8, use, want)) return;', '        if (true or std.mem.eql(u8, use, want)) return;'),
    ('B2', 'P05', 'a built-in registered with an underscore is not reached without it',
     '        if (self.spell_on) if (builtins.underscoreOf(callee)) |registered| {', '        if (false) if (builtins.underscoreOf(callee)) |registered| {'),
    ('B3', 'P09', 'the spelling is looked up by the name written, not the native the call resolved to',
     '        if (self.spell_on) self.spellNative(written, callee);', '        if (self.spell_on) self.spellNative(written, written);'),
    ('B4', 'P01', 'a yes-or-no built-in answers a boolean only in lowercase',
     '            if (std.ascii.eqlIgnoreCase(name, w)) return self.findFunc(name) == null;', '            if (std.mem.eql(u8, name, w)) return self.findFunc(name) == null;'),
    # B5 MISSED on its first run, switching off the guard inside spellNative alone: the call site asks `self.spell_on` first, so each
    # guard keeps a .ring file out without the other. The protection is the pair; B5 switches both off.
    ('B5', 'P06', 'the spelling is asked of a .ring file too',
     [('        if (!self.spellIn(use) or registered.len > 64) return;', '        if (registered.len > 64) return;'),
      ('        if (self.spell_on) self.spellNative(written, callee);', '        self.spellNative(written, callee);')], None),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    original = open(COMP, 'rb').read()

    def restore():
        open(COMP, 'wb').write(original)
        assert digest(open(COMP, 'rb').read()) == digest(original)

    results = []
    try:
        for pid, fixture, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            raw = original.decode('utf-8')
            crlf = (chr(13) + chr(10)) in raw
            text = raw.replace(chr(13) + chr(10), chr(10))
            subs = old if isinstance(old, list) else [(old, new)]
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r}', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(COMP, 'wb').write((planted.replace(chr(10), chr(13) + chr(10)) if crlf else planted).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
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
