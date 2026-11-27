"""Every protection of v0.79 switched off in turn: the court must fail, for the fixture that protection exists for. A plant is text
substitutions in one file of vm/src, built into runtime/v79/plant-build (ReleaseFast, -j2, one build at a time, and only when the
machine has 8 GB free), and its fixture's case run on that build alone. Every file is restored byte for byte, verified by its digest,
and restored even when a build fails or the script is stopped.

  python spike/v79/plants.py            all plants
  python spike/v79/plants.py P1 P3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
SRC = os.path.join(VM_DIR, 'src')
HTTPD = os.path.join(SRC, 'httpd.zig')
BUILTINS = os.path.join(SRC, 'builtins.zig')
COMPILE = os.path.join(SRC, 'compile.zig')
HARO = os.path.join(SRC, 'haro.zig')
MAIN = os.path.join(SRC, 'main.zig')
TYPES = os.path.join(SRC, 'types.zig')
OUT = os.path.join(ROOT, 'runtime', 'v79', 'plant-build')
COURT = os.path.join(HERE, 'court.py')
NEED_GB = 8.0


def report_off(rule):
    """the line of types.zig that reports `rule`, made to report nothing"""
    return ('try self.report.add(self.gpa, self.file, ', f'"{rule}", ')


PLANTS = [
    ('P1', 'H02', 'a type holding CR or LF goes into the head', HTTPD,
     [('    if (std.mem.indexOfAny(u8, ctype, "\\r\\n") != null or ctype.len > 200) {', '    if (ctype.len > 200) {')]),
    ('P2', 'H05', 'a type over 200 bytes goes into the head', HTTPD,
     [('    if (std.mem.indexOfAny(u8, ctype, "\\r\\n") != null or ctype.len > 200) {', '    if (std.mem.indexOfAny(u8, ctype, "\\r\\n") != null) {')]),
    ('P3', 'B01', '`check` does not ask the compiler\'s table', BUILTINS,
     [('    if (@import("compile.zig").isIntrinsic(lowname)) return true;\n', '')]),
    ('P4', 'B05', '`check` does not know the underscored spellings', BUILTINS,
     [('        if (std.ascii.eqlIgnoreCase(e[1], lowname)) return true;\n    }\n    if (@import("native.zig")', '    }\n    if (@import("native.zig")')]),
    ('P5', 'B02', '`check` does not ask the natives published at start-up', BUILTINS,
     [('    if (@import("native.zig").find(lowname) != null) return true;\n', '')]),
    ('P6', 'C03', 'Len is not counted', COMPILE,
     [('        if ((std.ascii.eqlIgnoreCase(callee, "len") and argc != 1) or (std.ascii.eqlIgnoreCase(callee, "add") and argc < 2))',
       '        if (std.ascii.eqlIgnoreCase(callee, "add") and argc < 2)')]),
    ('P7', 'C01', 'Add is not counted', COMPILE,
     [('        if ((std.ascii.eqlIgnoreCase(callee, "len") and argc != 1) or (std.ascii.eqlIgnoreCase(callee, "add") and argc < 2))',
       '        if (std.ascii.eqlIgnoreCase(callee, "len") and argc != 1)')]),
    ('P8', 'E01', 'an Eval is no late call', COMPILE,
     [('        if (std.ascii.eqlIgnoreCase(callee, "eval")) self.cur.late_calls += 1;\n', '')]),
    ('P9', 'N01', 'a top-level nL is not refused', COMPILE,
     [('            for ([_][]const u8{ "nl", "tab", "cr", "stdin", "stdout", "stderr" }) |r| {', '            for ([_][]const u8{}) |r| {')]),
    ('P10', 'I05', 'the run does not name a decimal index', MAIN,
     [('        if (!self.strictAt(pc) or (iv.tag != .dec and iv.tag != .num)) return BADPARAM;', '        _ = pc;\n        if (true) return BADPARAM;')]),
    ('P11', 'T01', '`check` does not name text + a number', TYPES,
     [('try self.report.add(self.gpa, self.file, n, .err, "haro/no-coercion"', 'if (false) try self.report.add(self.gpa, self.file, n, .err, "haro/no-coercion"')]),
    ('P12', 'T05', '`check` does not name a float mixed with a decimal', TYPES,
     [('try self.report.add(self.gpa, self.file, n, .err, "haro/number-mix"', 'if (false) try self.report.add(self.gpa, self.file, n, .err, "haro/number-mix"')]),
    ('P13', 'Q01', '`check` does not name a quotient with no exact decimal', TYPES,
     [('try self.report.add(self.gpa, self.file, n, .err, "haro/decimal-inexact"', 'if (false) try self.report.add(self.gpa, self.file, n, .err, "haro/decimal-inexact"')]),
    ('P14', 'Q03', '`check` does not name a quotient given to an i name', TYPES,
     [('try self.report.add(self.gpa, self.file, rhs, .err, "haro/type-letter"', 'if (false) try self.report.add(self.gpa, self.file, rhs, .err, "haro/type-letter"')]),
    ('P15', 'I01', '`check` does not name a decimal index', TYPES,
     [('try self.report.add(self.gpa, self.file, ix, .err, "haro/index-not-integer"', 'if (false) try self.report.add(self.gpa, self.file, ix, .err, "haro/index-not-integer"')]),
    ('P16', 'T02', 'a name\'s type letter shows no type to `check`', TYPES,
     [("            const l = Comp.letterOf(n.text()) orelse return null;\n", "            const l: u8 = 0;\n")]),
    ('P17', 'L01', '`check` reports every file of the unit', HARO,
     [('            in_scope[i] = check_all or (i >= pre_start and blk: {', '            in_scope[i] = true or (i >= pre_start and blk: {')]),
    ('P18', 'L03', '`check` never stands on the kept library', HARO,
     [('    if ((std.mem.eql(u8, argv[1], "exec") or check_on_kept) and image.enabled(alloc)) {', '    if (std.mem.eql(u8, argv[1], "exec") and check_on_kept == check_on_kept and image.enabled(alloc)) {')]),
    ('P19', 'L03', 'the kept library\'s names are not given to `check`', HARO,
     [('            try uni.addNatives(alloc, lib_names.items);\n', '')]),
    ('P20', 'L01', 'a file outside the folder does not claim its own refusals', HARO,
     [('                    try addRefused(alloc, &unseen, r, unit.paths.items[i], unit.inserts.items[i], trapped, placed);\n',
       '                    _ = &unseen;\n')]),
    ('P21', 'L06', 'the name that stopped the kept library is not said', HARO,
     [('                check_blocked = alloc.dupe(u8, if (co.prefix_blocked_by.len > 0) co.prefix_blocked_by else "its own reason") catch "";\n',
       '                check_blocked = "";\n')]),
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
    for k in range(90):
        g = free_gb()
        if g >= NEED_GB:
            return True
        if k % 3 == 0:
            print(f'{pid} waits: {g:.1f} GB free, a build needs {NEED_GB:.0f}', flush=True)
        time.sleep(20)
    return False


def main():
    want = set(sys.argv[1:])
    files = {p for _, _, _, p, _ in PLANTS}
    originals = {p: open(p, 'rb').read() for p in files}

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
            t0 = time.time()
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=3600)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            exe = os.path.join(OUT, 'bin', 'haro.exe')
            r = subprocess.run([sys.executable, COURT, '--vm', exe, '--only', fixture], capture_output=True, timeout=900)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}; built in {time.time() - t0:.0f} s', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
