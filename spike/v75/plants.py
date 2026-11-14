"""Every protection of v0.75 (a command line is not built as text; D88 (d)) switched off in turn: the court must fail, for the
fixture that protection exists for. A plant is text substitutions in one file. In vm/src it is built into runtime/v75/plant-build
(ReleaseFast, -j2, one build at a time, and only when the machine has 8 GB free) and its fixture's case run on that build alone; in
the libraries of spike/ nothing is built -- the case runs on the base build, runtime/v75/build, which reads the planted file. Every
file is restored byte for byte, verified by its digest, and restored even when a build fails or the script is stopped.

  python spike/v75/plants.py            all plants (about two minutes each for those that build)
  python spike/v75/plants.py K1 J1      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMPILE = os.path.join(VM_DIR, 'src', 'compile.zig')
JLIB = os.path.join(SPIKE, 'judge_lib.haro')
CLIB = os.path.join(SPIKE, 'court_lib.haro')
NLIB = os.path.join(SPIKE, 'n_lib.haro')
OUT = os.path.join(ROOT, 'runtime', 'v75', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v75', 'plant-cache')
BASE = os.path.join(ROOT, 'runtime', 'v75', 'build', 'bin', 'haro.exe')
COURT = os.path.join(HERE, 'line_court.py')
NEED_GB = 8.0

BUILT_SYSTEM = ('                    .built => {\n'
                '                        if (self.spellIn(a.text())) self.spellSet(a.text(), LINE_WHY);\n'
                '                        _ = try self.emit(.loadk, dst, 0, 0, try self.konstIndex("\\"\\""));\n'
                '                        return;\n'
                '                    },\n'
                '                    .other => guarded = true,\n')
BUILT_CMD = ('                .built => {\n'
             '                    if (self.spellIn(a.text())) self.spellSet(a.text(), LINE_WHY);\n'
             '                    _ = try self.emit(.loadk, dst, 0, 0, try self.konstIndex("\\"\\""));\n'
             '                    return;\n'
             '                },\n'
             '                .other => guarded3 = true,\n')
PLANTS = [
    # the compiler
    ('K1', 'X02', 'System takes a command line built as text when compiling', COMPILE,
     [(BUILT_SYSTEM, '                    .built => guarded = true,\n                    .other => guarded = true,\n')]),
    ('K2', 'X03', 'SystemCmd takes a command line built as text when compiling', COMPILE,
     [(BUILT_CMD, '                .built => guarded3 = true,\n                .other => guarded3 = true,\n')]),
    ('K3', 'X05', 'System has no guard where the program runs', COMPILE,
     [('                    .other => guarded = true,\n', '                    .other => guarded = false,\n')]),
    ('K4', 'X05', 'SystemCmd has no guard where the program runs', COMPILE,
     [('                .other => guarded3 = true,\n', '                .other => guarded3 = false,\n')]),
    ('K5', 'X04', 'a name lettered as a text is not read as a text', COMPILE,
     [("            if (l == 't') return .built;", "            if (l == 'z') return .built;")]),
    ('K6', 'X02', 'a text joined with a name is not read as built', COMPILE,
     [('        return .built;\n    }\n    if (std.mem.eql(u8, k, "identifier")) {', '        return .other;\n    }\n    if (std.mem.eql(u8, k, "identifier")) {')]),
    ('K7', 'X01', 'literals joined are read as built', COMPILE,
     [('        if (lineForm(e.namedChild(0)) == .written and lineForm(e.namedChild(1)) == .written) return .written;\n', '')]),
    ('K8', 'X07', 'System in a .ring file is read by the rule', COMPILE,
     [('            if (bi.id == .system and argc == 1 and self.haroNode(n)) {', '            if (bi.id == .system and argc == 1) {')]),
    ('K9', 'X07', 'SystemCmd in a .ring file is read by the rule', COMPILE,
     [('        if (std.ascii.eqlIgnoreCase(callee, "systemcmd") and argc == 1 and self.haroNode(n)) {', '        if (std.ascii.eqlIgnoreCase(callee, "systemcmd") and argc == 1) {')]),
    # the VM
    ('K10', 'X05', 'the guard lets a text through', MAIN,
     [('                        if (regs[A].tag == .str) {\n                            self.pending = "Error (COMMAND_LINE_BUILT)',
       '                        if (regs[A].tag == .nil) {\n                            self.pending = "Error (COMMAND_LINE_BUILT)')]),
    # the libraries
    ('J1', 'X10', 'a sentence of doors is read at each call', JLIB,
     [('\t\tif $vHaroDoorsRead[i][1] = tText return $vHaroDoorsRead[i][2] end\n', '')]),
    ('C1', 'X09', 'no court is the program: a court whose library holds a sentence has no main', CLIB,
     [('\treturn Lower(tGiven) = Lower($vCourtLangs[1][1]) + "_court.haro"\n', '\treturn false\n')]),
    ('C2', 'X06', 'every court is the program: a court a program loads runs its main', CLIB,
     [('\treturn Lower(tGiven) = Lower($vCourtLangs[1][1]) + "_court.haro"\n', '\treturn true\n')]),
    ('N1', 'X09', 'the library\'s sentence is read while its court judges', NLIB,
     [('HaroDoorsDeclared($sNatDoors)\n\n', '\n')]),
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
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMPILE, JLIB, CLIB, NLIB)}

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
            exe = BASE
            if path.endswith('.zig') and not headroom(pid):
                print(f'{pid} NOT RUN: the machine never had {NEED_GB:.0f} GB free', flush=True)
                results.append((pid, 'NOT RUN'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(path, 'wb').write((planted.replace('\n', '\r\n') if crlf else planted).encode('utf-8'))
            if path.endswith('.zig'):
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
