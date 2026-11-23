"""Every protection of v0.78 (three findings of the desks) switched off in turn: the court must fail, for the fixture that protection
exists for. A plant is text substitutions in one file -- vm/src/haro.zig, vm/src/main.zig, or the judging library spike/judge_lib.haro
-- built into runtime/v78/plant-build (ReleaseFast, -j2, one build at a time, and only when the machine has 8 GB free) and its
fixture's case run on that build alone. Every file is restored byte for byte, verified by its digest, and restored even when a
build fails or the script is stopped.

  python spike/v78/plants.py            all plants (about two minutes each)
  python spike/v78/plants.py K1 K3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
JUDGE = os.path.join(SPIKE, 'judge_lib.haro')
OUT = os.path.join(ROOT, 'runtime', 'v78', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v78', 'plant-cache')
COURT = os.path.join(HERE, 'desks_court.py')
NEED_GB = 8.0

RETURNS = '            co.reportFailure(e);\n            return;\n'
PLANTS = [
    ('K1', 'X01', 'a compile that fails ends with 0', HARO,
     [('    co.reportFailure(e);\n    vm.outFlush();\n    std.process.exit(1);\n', '    co.reportFailure(e);\n    vm.outFlush();\n    std.process.exit(0);\n')]),
    ('K2', 'X01', 'the run alone reports its failed compile and returns', HARO,
     [('            break :blk co.compileLenient(alloc, unit.roots.items) catch |e| {\n                compileFailed(e);\n            };\n        };\n        if (from_kept) {',
       '            break :blk co.compileLenient(alloc, unit.roots.items) catch |e| {\n                co.reportFailure(e);\n                return;\n            };\n        };\n        if (from_kept) {')]),
    ('K3', 'X03', '`haro dis` alone reports its failed compile and returns', HARO,
     [('        const prog = co.compileLenient(alloc, unit.roots.items) catch |e| {\n            compileFailed(e);\n        };\n        try disasm(prog, w);',
       '        const prog = co.compileLenient(alloc, unit.roots.items) catch |e| {\n' + RETURNS + '        };\n        try disasm(prog, w);')]),
    ('K4', 'X04', 'a check whose compiler stopped ends with 0', HARO,
     [('        if (compiler_silent) std.process.exit(1);\n', '')]),
    ('K5', 'L01', 'a run from its kept image does not say so', HARO,
     [('                pathSay("kept image", .{});\n', '')]),
    ('K6', 'L01', 'a run on the kept library says it was compiled whole', HARO,
     [('                    from_kept = true;\n', '')]),
    ('K7', 'L06', 'the name that stopped the kept library is not kept', HARO,
     [('                    blocked = alloc.dupe(u8, if (co.prefix_blocked_by.len > 0) co.prefix_blocked_by else "its own reason") catch "";\n', '')]),
    ('K8', 'L07', 'a kept library that was there and not taken is not called stale', HARO,
     [('            prefix_stale = true;\n', '            prefix_stale = false;\n')]),
    ('K9', 'L08', 'HARO_NOIMAGE is not asked where a root\'s image is used and written', HARO,
     [('        img_path = if (no_image) null else image.pathFor(vmheap, root_abs);\n', '        img_path = image.pathFor(vmheap, root_abs);\n')]),
    ('K10', 'L10', 'HARO_NOIMAGE is not asked, with no kept library', HARO,
     [('        img_path = if (no_image) null else image.pathFor(vmheap, root_abs);\n', '        img_path = image.pathFor(vmheap, root_abs);\n')]),
    ('K11', 'L11', 'the path is said without being asked for', HARO,
     [('    if (say_path) std.debug.print("path: " ++ text ++ "\\n", args);\n', '    std.debug.print("path: " ++ text ++ "\\n", args);\n')]),
    ('K12', 'L13', 'the usage text does not name `prefix`', HARO,
     [('        std.debug.print("       haro prefix <library.haro>    compile a library once and keep it: a program whose first statement loads it\\n", .{});\n', '')]),
    ('K13', 'R02', 'the place\'s own door is not asked: its path is taken as it is', MAIN,
     [('        const pv = self.placeDoor(input, "read") orelse return null;\n        const path = strOf(pv);\n',
       '        const path = strOf(input.p.o.slots[2]);\n')]),
    ('K14', 'R03', 'what is given is not asked to be a place', MAIN,
     [('        if (!isPlace(input)) {\n            self.pending = self.haroMsg("Error (RUN_INPUT)', '        if (input.tag == .nil) {\n            self.pending = self.haroMsg("Error (RUN_INPUT)')]),
    ('K15', 'R04', 'a file that could not be read is no refusal', MAIN,
     [('            self.pending = self.haroMsg("Error (INPUT_NOT_READ) : the command `{s}` reads `{s}` as its standard input, which could not be read", .{ name, path });\n            return null;\n',
       '            return Value.vec(self.newVec(3));\n')]),
    ('K16', 'R05', 'the child is fed before its output is read, by the thread that reads it', MAIN,
     [('        const feeder: ?std.Thread = std.Thread.spawn(.{}, Feeder.feed, .{ to_child, bytes }) catch null;\n', '        const feeder: ?std.Thread = null;\n')]),
    ('K17', 'R01', 'the judging library runs the child without what it reads', JUDGE,
     [('\t\tvGot = SystemRun(this, pxInput)\n', '\t\tvGot = SystemRun(this)\n')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def free_gb():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong), ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong), ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong), ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
    if os.name != 'nt':
        return 99.0
    st = MEMORYSTATUSEX()
    st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st)):
        return 99.0
    return st.ullAvailPhys / (1024.0 ** 3)


def headroom(pid):
    """a build waits for the machine: up to twenty minutes, said every minute"""
    for k in range(60):
        g = free_gb()
        if g >= NEED_GB:
            return True
        if k % 3 == 0:
            print(f'{pid} waits: {g:.1f} GB free, a build needs {NEED_GB:.0f}', flush=True)
        time.sleep(20)
    return False


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (HARO, MAIN, JUDGE)}

    def restore():
        for p, b in originals.items():
            if open(p, 'rb').read() != b:
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
            if not headroom(pid):
                print(f'{pid} NOT RUN: the machine never had {NEED_GB:.0f} GB free', flush=True)
                results.append((pid, 'NOT RUN'))
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
            exe = os.path.join(OUT, 'bin', 'haro.exe')
            cache = os.path.join(CACHE, 'v78-' + pid)
            shutil.rmtree(cache, ignore_errors=True)
            env = dict(os.environ)
            env['HARO_CACHE'] = os.path.join(cache, 'images')
            r = subprocess.run([sys.executable, COURT, '--vm', exe, '--only', fixture], capture_output=True, timeout=900, env=env)
            restore()
            shutil.rmtree(cache, ignore_errors=True)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
