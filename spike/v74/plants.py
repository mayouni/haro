"""Every protection of v0.74 (a folder made and a run answered whole) switched off in turn: the court must fail, for the fixture that
protection exists for. A plant is text substitutions in one file of vm/src; it is built into runtime/v74/plant-build (ReleaseFast,
-j2, one build at a time, and only when the machine has 8 GB free) and its fixture's case run on that build alone. Every file is
restored byte for byte, verified by its digest, and restored even when a build fails or the script is stopped; what a plant lets a
case make is taken away after each.

  python spike/v74/plants.py            all plants (about two minutes each)
  python spike/v74/plants.py K1 K3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMPILE = os.path.join(VM_DIR, 'src', 'compile.zig')
BUILTINS = os.path.join(VM_DIR, 'src', 'builtins.zig')
SYSCMD = os.path.join(VM_DIR, 'src', 'syscmd.zig')
OUT = os.path.join(ROOT, 'runtime', 'v74', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v74', 'plant-cache')
COURT = os.path.join(HERE, 'made_court.py')
NEED_GB = 8.0

DOOR = '                    .readf, .fexists, .direxists, .dir, .writef, .removefile, .makedir1 => if (in.c > 0 and isPlace(regs[A])) {'
PLANTS = [
    ('K1', 'W02', 'MakeDir does not take a place', MAIN,
     [(DOOR, DOOR.replace(', .makedir1 =>', ' =>'))]),
    ('K2', 'W02', 'MakeDir asks read', MAIN,
     [('                            .makedir1 => "write",', '                            .makedir1 => "read",')]),
    ('K3', 'W04', 'a folder that cannot be made is passed over', MAIN,
     [('                        std.fs.cwd().makePath(p) catch {\n'
       '                            self.pending = self.haroMsg("Error (FOLDER_NOT_MADE) : the folder `{s}` could not be made", .{p});\n'
       '                            continue :dispatch .raise;\n'
       '                        };\n',
       '                        std.fs.cwd().makePath(p) catch {};\n')]),
    ('K4', 'W05', 'MakeDir takes what is no text', MAIN,
     [('                    .makedir1 => {\n                        if (regs[A].tag != .str) {', '                    .makedir1 => {\n                        if (regs[A].tag == .nil) {')]),
    ('K5', 'W07', 'MakeDir is a built-in of a .ring file too', COMPILE,
     [('        .makedir1 => true,\n', '')]),
    ('K6', 'W08', 'the door beneath Run does not take an invocation', MAIN,
     [('                if (in.c == 1 and isInvocation(regs[base + in.b]) and std.ascii.eqlIgnoreCase(nm, "systemrun")) {',
       '                if (in.c == 1000 and isInvocation(regs[base + in.b]) and std.ascii.eqlIgnoreCase(nm, "systemrun")) {')]),
    ('K7', 'W08', 'a run answered whole does not answer the exit code', MAIN,
     [('                    .Exited => |c| @intCast(c),\n                    else => -1,\n                }), false);',
       '                    .Exited => 0,\n                    else => -1,\n                }), false);')]),
    ('K8', 'W08', 'the last line end of what the child wrote is kept', MAIN,
     [('                self.vecPushB(wv, Value.str(self.newStr(dropLineEnd(res.stdout))), true);', '                self.vecPushB(wv, Value.str(self.newStr(res.stdout)), true);')]),
    ('K9', 'W08', 'the last line end of the child\'s errors is kept', MAIN,
     [('                self.vecPushB(wv, Value.str(self.newStr(dropLineEnd(res.stderr))), true);', '                self.vecPushB(wv, Value.str(self.newStr(res.stderr)), true);')]),
    ('K10', 'W08', 'a run answered whole writes the child\'s errors out as well', MAIN,
     [('            if (mode == .whole) {\n', '            if (mode == .whole) {\n                std.debug.print("{s}", .{res.stderr});\n')]),
    ('K11', 'W11', 'the door beneath Run is written in any program', COMPILE,
     [('        if (std.ascii.eqlIgnoreCase(callee, "systemrun") and self.spellIn(n.text())) {', '        if (std.ascii.eqlIgnoreCase(callee, "systemrun-off") and self.spellIn(n.text())) {')]),
    ('K12', 'W12', 'the door beneath Run, given no invocation, answers nothing', SYSCMD,
     [('    retStr(out, "Error (RUN_TAKES_INVOCATION) : a run is asked of an invocation -- hCall.Run()");\n    return 1;\n', '    retStr(out, "");\n    return 0;\n')]),
    ('K13', 'W01', 'the checker does not know MakeDir', BUILTINS,
     [('pub const own = [_][]const u8{ "systemcmd", "systemrun", "makedir" };', 'pub const own = [_][]const u8{ "systemcmd", "systemrun" };')]),
    ('K14', 'W12', 'the checker does not know the door beneath Run', BUILTINS,
     [('pub const own = [_][]const u8{ "systemcmd", "systemrun", "makedir" };', 'pub const own = [_][]const u8{ "systemcmd", "makedir" };')]),
    ('K15', 'W13', 'MakeDir has no spelling in a .haro file', BUILTINS,
     [('    .{ "makedir", "MakeDir" },\n', '')]),
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


def cases_again():
    subprocess.run([sys.executable, os.path.join(HERE, 'gen_fixtures.py')], capture_output=True, timeout=120)
    for stray in (os.path.join(HERE, 'cases', 'data', 'new'), os.path.join(HERE, 'cases', 'outside', 'new'), os.path.join(HERE, 'cases', 'made')):
        shutil.rmtree(stray, ignore_errors=True)


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMPILE, BUILTINS, SYSCMD)}

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
            cache = os.path.join(CACHE, pid)
            shutil.rmtree(cache, ignore_errors=True)
            env = dict(os.environ)
            env['HARO_CACHE'] = os.path.join(cache, 'images')
            r = subprocess.run([sys.executable, COURT, '--vm', exe, '--only', fixture], capture_output=True, timeout=900, env=env)
            restore()
            cases_again()
            shutil.rmtree(cache, ignore_errors=True)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
        cases_again()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
