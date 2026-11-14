"""Every protection of v0.72 (the language of doors and the place; doc/DOORS.md rung 1, D88) switched off in turn: the court must
fail, for the fixture that protection exists for. A plant is text substitutions in one file. In vm/src it is built into
runtime/v72/plant-build (ReleaseFast, -j2, one build at a time, and only when the machine has 8 GB free) and the court run on that
build alone; in the judging library and in the declaration of doors nothing is built -- the court runs on the base build,
runtime/v72/build, which reads the planted file. Each plant forges into a cache of its own, so no court forged before it is found.
Every file is restored byte for byte, verified by its digest, and restored even when a build fails or the script is stopped; the
cases' own files, which a plant may let a door write or remove, are written again after each.

  python spike/v72/plants.py            all plants (about two minutes each for those that build)
  python spike/v72/plants.py K1 J3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMPILE = os.path.join(VM_DIR, 'src', 'compile.zig')
JLIB = os.path.join(SPIKE, 'judge_lib.haro')
DOORS = os.path.join(SPIKE, 'doors.haro')
OUT = os.path.join(ROOT, 'runtime', 'v72', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v72', 'plant-cache')
BASE = os.path.join(ROOT, 'runtime', 'v72', 'build', 'bin', 'haro.exe')
COURT = os.path.join(HERE, 'place_court.py')
NEED_GB = 8.0

DOOR = '                    .readf, .fexists, .direxists, .dir, .writef, .removefile => if (in.c > 0 and isPlace(regs[A])) {'
PLANTS = [
    # the loader and the compiler
    ('K1', 'D01', "the loader does not look for a standard language in the forge's folder", HARO,
     [('            if (fileExists(at_home)) break :blk at_home;', '            if (at_home.len == 0) break :blk at_home;')]),
    ('K2', 'D01', 'the compiler does not look there', COMPILE,
     [('        if (forge_home.len > 0) {', '        if (forge_home.len > 1000000) {')]),
    ('K3', 'D01', "a forged court's libraries are forwarded for two alone", HARO,
     [('            const f = ln[6..q];\n',
       '            const f = ln[6..q];\n            if (!std.mem.eql(u8, f, "court_lib.haro") and !std.mem.eql(u8, f, "world_stub.haro")) continue;\n')]),
    ('K4', 'D12', 'a loaded declaration is scanned as code when a program is refused', HARO,
     [('    if (!is_root and lift.isHaro(path) and isDeclaration(src)) return false;',
       '    if (!is_root and lift.isHaro(path) and isDeclaration(src) and src.len == 0) return false;')]),
    # the VM
    ('K5', 'D09', 'a door does not ask what the root allows', MAIN,
     [('        if (!allowed) {', '        if (!allowed and need.len == 0) {')]),
    ('K6', 'D11', 'a door does not check again where it opens', MAIN,
     [('                    if (!inside) {', '                    if (!inside and r.len == 0) {')]),
    ('K7', 'D01', 'a place does not print as its path', MAIN,
     [('                if ((isSentence(v) or isPlace(v)) and v.p.o.nslots > 2', '                if (isSentence(v) and v.p.o.nslots > 2')]),
    ('K8', 'D13', 'a place is written into', MAIN,
     [('                if (aop == .sattrn and placeFixed(o)) {', '                if (aop == .sattrn and placeFixed(o) and o.nslots == 0) {')]),
    ('K9', 'D01', 'the letter h does not hold a place', MAIN,
     [("                    'h' => v.tag == .cptr or v.tag == .dll or isPlace(v),", "                    'h' => v.tag == .cptr or v.tag == .dll,")]),
    ('K10', 'D08', 'a door does not take a place', MAIN,
     [(DOOR, DOOR.replace('in.c > 0', 'in.c > 1000'))]),
    ('K11', 'D09', 'Write asks read', MAIN,
     [('                            .writef => "write",', '                            .writef => "read",')]),
    ('K12', 'D09', 'Remove asks read', MAIN,
     [('                            .removefile => "remove",', '                            .removefile => "read",')]),
    ('K13', 'D16', 'Dir asks read', MAIN,
     [('                            .dir => "list",', '                            .dir => "read",')]),
    ('K14', 'D12', '`new` of a place is let through', COMPILE,
     [('        const a_place = std.ascii.eqlIgnoreCase(ci.name, "haroplace");', '        const a_place = ci.name.len == 0;')]),
    # the judge, in Haro
    ('J1', 'D15', 'a sentence of any language judges a place', JLIB,
     [('\tif psDoors.Language() != "doors"\n', '\tif psDoors.Language() = ""\n')]),
    ('J2', 'D05', 'a root the sentence does not declare is taken', JLIB,
     [('\tif not bFound\n', '\tif not bFound and ptRoot = ""\n')]),
    ('J3', 'D03', 'a step back out of the root is taken', JLIB,
     [('\t\t\telseif not pbAnywhere\n', '\t\t\telseif not pbAnywhere and tSeg = ""\n')]),
    ('J4', 'D03', 'a drive is taken beneath a root', JLIB,
     [('\t\t# a drive\n\t\tif not pbAnywhere HaroEscapes(ptText, ptRoot) end\n', '\t\t# a drive\n')]),
    ('J5', 'D03', 'a rooted path and a share are taken beneath a root', JLIB,
     [('\t\t# a rooted path, a share\n\t\tif not pbAnywhere HaroEscapes(ptText, ptRoot) end\n', '\t\t# a rooted path, a share\n')]),
    ('J6', 'D03', 'a scheme is not read as leaving the root', JLIB,
     [('\tif SubStr(tAll, "://") > 0 and not pbAnywhere HaroEscapes(ptText, ptRoot) end\n', '')]),
    ('J7', 'D04', 'nothing is a name', JLIB,
     [('\tif ptText = "" HaroNoName(ptText) end\n', '')]),
    ('J8', 'D04', 'a control byte stands in a name', JLIB,
     [('\t\tif nByte < 32 or nByte = 127 HaroNoName(ptText) end\n', '')]),
    ('J9', 'D04', 'a name ends with a dot', JLIB,
     [('\tif tLast = "." or tLast = " " HaroNoName(ptText) end\n', '\tif tLast = " " HaroNoName(ptText) end\n')]),
    ('J10', 'D04', 'a name ends with a blank', JLIB,
     [('\tif tLast = "." or tLast = " " HaroNoName(ptText) end\n', '\tif tLast = "." HaroNoName(ptText) end\n')]),
    ('J11', 'D04', 'a colon stands in a name', JLIB,
     [('\t\tif SubStr(tBad, ptSeg[i]) > 0 HaroNoName(ptText) end\n', '')]),
    ('J12', 'D04', 'a device is a name', JLIB,
     [('\t\tif tBase = vDevices[i] HaroNoName(ptText) end\n', '')]),
    ('J13', 'D06', 'a root that lists nothing allows nothing', JLIB,
     [('\tif Len(vAllows) = 0 vAllows = ["read"] end\n', '')]),
    # the declaration of doors
    ('M1', 'D07', 'a root with no folder that does not say ANYWHERE is a sentence', DOORS,
     [('WHEN "anywhere absent", THEN "at present"', 'WHEN "anywhere absent", THEN "anywhere absent"')]),
    ('M2', 'D07', 'a root ANYWHERE with a folder is a sentence', DOORS,
     [('WHEN "anywhere present", THEN "at absent"', 'WHEN "anywhere present", THEN "anywhere present"')]),
    ('M3', 'D07', 'a root ANYWHERE that lists what it allows is a sentence', DOORS,
     [('WHEN "anywhere present", THEN "allows absent"', 'WHEN "anywhere present", THEN "anywhere present"')]),
    ('M4', 'D07', 'a root allows a fifth word', DOORS,
     [('WORDS [read, write, list, remove],', 'WORDS [read, write, list, remove, execute],')]),
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
    made = os.path.join(HERE, 'cases', 'out', 'made.txt')
    if os.path.exists(made):
        os.remove(made)


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (HARO, MAIN, COMPILE, JLIB, DOORS)}

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
            r = subprocess.run([sys.executable, COURT, '--vm', exe], capture_output=True, timeout=900, env=env)
            restore()
            cases_again()
            shutil.rmtree(cache, ignore_errors=True)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}; failed {", ".join(failed) or "none"}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
        cases_again()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
