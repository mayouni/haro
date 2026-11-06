"""Every protection of D52 rung (1) switched off in turn: the finally court must fail, for the fixture that protection exists for (the W discipline).

Each plant is one text substitution in vm/src/compile.zig. The VM is built with the plant into runtime/v36/plant-build (ReleaseFast, -j2, one build at a
time: the machine's rule), the finally court is run on that build alone, and compile.zig is restored byte for byte before the next plant -- verified by
its digest, and restored even when a build fails or the script is stopped. zig-out and zig-out-safe are never touched.

Printed is CAUGHT with the fixtures that failed, or MISSED: a protection no fixture pins, and the answer to it is a fixture.

  python spike/v36/plants.py            all plants (about 1.5 minutes each)
  python spike/v36/plants.py P3 P7      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
SRC = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v36', 'plant-build')
COURT = os.path.join(HERE, 'finally_court.py')

PLANTS = [
    ('P1', 'F04', 'a return leaves its trys without running their finally',
     '        self.floor = @max(self.floor, keep + 1);\n        try self.unwind(0, 0);',
     '        self.floor = @max(self.floor, keep + 1);\n        try self.leaveTries(self.try_open);'),
    ('P2', 'F07', 'an exit or loop leaves its trys without running their finally',
     '        try self.unwind(lt[lt.len - lv], self.loop_fin.items[self.loop_fin.items.len - lv]);',
     '        try self.leaveTries(self.try_open - lt[lt.len - lv]);'),
    ('P3', 'F06', 'a raise in the handler skips the finally',
     '                try self.body(f, 0);\n                _ = try self.emit(.trap, held.reg, 1, 0, 0);',
     '                _ = try self.emit(.trap, held.reg, 1, 0, 0);'),
    ('P4', 'F12', 'a crossed finally runs with its own handler still armed',
     '            try self.leaveTries(cur - r.try_level);\n            cur = r.try_level;\n',
     '            _ = &cur;\n'),
    ('P5', 'F10', 'the crossed finally blocks run outermost first',
     '''        var cur = self.try_open;
        var j = self.fin_regions.items.len;
        while (j > to_fin) {
            j -= 1;
            const r = self.fin_regions.items[j];
            try self.leaveTries(cur - r.try_level);
            cur = r.try_level;
            try self.inlineFinally(j, r);
        }
        try self.leaveTries(cur - to_try);''',
     '''        try self.leaveTries(self.try_open - to_try);
        var j = to_fin;
        while (j < self.fin_regions.items.len) : (j += 1) try self.inlineFinally(j, self.fin_regions.items[j]);'''),
    ('P6', 'F04', 'the finally compiled at a return may reuse the register holding the value',
     '        self.floor = @max(self.floor, keep + 1);\n', '        _ = keep;\n'),
    ('P7', 'F14', 'handlers are named by the open catches, so a try inside a finally shares its enclosing try\'s error',
     '        const depth = self.try_depth - 1;', '        const depth: u32 = @intCast(self.catch_regs.items.len);'),
    ('P8', 'F15', 'a finally compiled at a jump still counts itself open, so a jump inside it crosses it again',
     '        self.fin_regions.shrinkRetainingCapacity(j);\n', ''),
    ('P9', 'F24', 'a loop does not record the regions open at its entry, so an exit inside a try body runs that try\'s finally',
     '        try self.loop_fin.append(self.alloc, @intCast(self.fin_regions.items.len));',
     '        try self.loop_fin.append(self.alloc, 0);'),
    ('P10', 'F05', 'the handler of a try with a finally is not a region, so a return from it skips the finally',
     '''                    try self.fin_regions.append(self.alloc, .{ .node = f, .try_level = self.try_open, .catch_len = @intCast(self.catch_regs.items.len) });
                    defer _ = self.fin_regions.pop();
''', ''),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    original = open(SRC, 'rb').read()
    text = original.decode('utf-8')
    d0 = digest(original)
    results = []
    try:
        for pid, fixture, why, old, new in PLANTS:
            if want and pid not in want:
                continue
            n = text.count(old)
            if n < 1:
                print(f'{pid} STALE: its text is not in compile.zig')
                results.append((pid, 'STALE'))
                continue
            open(SRC, 'wb').write(text.replace(old, new).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            open(SRC, 'wb').write(original)
            assert digest(open(SRC, 'rb').read()) == d0
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-300:]}')
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=600)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL (F\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}; failed {", ".join(failed) or "none"}')
            results.append((pid, verdict))
    finally:
        open(SRC, 'wb').write(original)
        assert digest(open(SRC, 'rb').read()) == d0
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
