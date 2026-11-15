"""Every protection of v0.77 (three findings of the desks) switched off in turn: the court must fail, for the fixture that protection
exists for. A plant is text substitutions in one file of vm/src; it is built into runtime/v77/plant-build (ReleaseFast, -j2, one
build at a time, and only when the machine has 8 GB free) and its fixture's case run on that build alone. Every file is restored
byte for byte, verified by its digest, and restored even when a build fails or the script is stopped.

  python spike/v77/plants.py            all plants (about two minutes each)
  python spike/v77/plants.py K1 K3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
COMPILE = os.path.join(VM_DIR, 'src', 'compile.zig')
GRAPH = os.path.join(VM_DIR, 'src', 'graph.zig')
OUT = os.path.join(ROOT, 'runtime', 'v77', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v77', 'plant-cache')
COURT = os.path.join(HERE, 'findings_court.py')
NEED_GB = 8.0

PLANTS = [
    ('K1', 'F01', 'a statement after a header on its line is let through', LIFT,
     [("                if (h < last and src[h] != '{') {\n", "                if (h < last and src[h] == 0) {\n")]),
    ('K2', 'F03', 'a method\'s header is not read', LIFT,
     [('            if (!rec and ne > k and (eq(w, "func") or eq(w, "def"))) {', '            if (!rec and ne > k and eq(w, "func")) {')]),
    ('K3', 'F04', 'a parameter list its line does not close is let through', LIFT,
     [('                    if (!closed) {\n', '                    if (!closed and depth == 99) {\n')]),
    ('K4', 'F05', '`maybe` after a header is read as a statement', LIFT,
     [('                if (h + 5 <= last and eq(src[h .. h + 5], "maybe") and (h + 5 == last or !wordByte(src[h + 5]))) h += 5;\n', '')]),
    ('K5', 'F06', 'a program served from its image does not say which surface it is read by', HARO,
     [('    lift.haro_root = lift.isHaro(root_as_typed);\n', '')]),
    ('K6', 'F09', 'a call by a built name is not counted', COMPILE,
     [('        self.cur.late_calls += 1;\n', '')]),
    ('K7', 'F09', 'the graph does not print a call by a built name', GRAPH,
     [('        if (f.late_calls > 0) {\n', '        if (f.late_calls > 99) {\n')]),
    ('K8', 'F09', 'the count of a function\'s calls by a built name is kept from one pass to the next', COMPILE,
     [('    for (c.funcs.items[c.prefix_funcs..]) |*f| {\n        f.poisoned = false;\n        f.late_calls = 0;\n',
       '    for (c.funcs.items[c.prefix_funcs..]) |*f| {\n        f.poisoned = false;\n')]),
    ('K9', 'F11', 'a name is read as letters, digits and underscores, so one that holds `@` ends early', LIFT,
     [('            while (ne < last and nameByte(src[ne])) ne += 1;\n', '            while (ne < last and wordByte(src[ne])) ne += 1;\n')]),
    ('K10', 'F13', 'the refusal writes the name to its first `@`', LIFT,
     [('fault = .{ .why = R_ONELINE, .word = src[k..ne], .row = row };', 'fault = .{ .why = R_ONELINE, .word = src[k..e], .row = row };')]),
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
    originals = {p: open(p, 'rb').read() for p in (LIFT, HARO, COMPILE, GRAPH)}

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
            cache = os.path.join(CACHE, 'v77-' + pid)
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
