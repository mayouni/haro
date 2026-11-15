"""Every protection of v0.76 (the peer and the endpoint; doc/DOORS.md rung 3) switched off in turn: the court must fail, for the
fixture that protection exists for. A plant is text substitutions in one file. In vm/src it is built into runtime/v77/plant-build
(ReleaseFast, -j2, one build at a time, and only when the machine has 8 GB free) and its fixture's case run on that build alone; in
the judging library and in the declaration of doors nothing is built -- the case runs on the base build, runtime/v77/build, which
reads the planted file. Every file is restored byte for byte, verified by its digest, and restored even when a build fails or the
script is stopped. (The builds stand in runtime/v77: v0.76's half in the VM was built together with v0.77.)

  python spike/v76/plants.py            all plants (about two minutes each for those that build)
  python spike/v76/plants.py K1 J3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMPILE = os.path.join(VM_DIR, 'src', 'compile.zig')
JLIB = os.path.join(SPIKE, 'judge_lib.haro')
DOORS = os.path.join(SPIKE, 'doors.haro')
OUT = os.path.join(ROOT, 'runtime', 'v77', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v77', 'plant-cache')
BASE = os.path.join(ROOT, 'runtime', 'v77', 'build', 'bin', 'haro.exe')
COURT = os.path.join(HERE, 'endpoint_court.py')
NEED_GB = 8.0

PLANTS = [
    # the VM
    ('K1', 'E01', 'an endpoint does not print as its address', MAIN,
     [('                if ((isSentence(v) or isPlace(v) or isInvocation(v) or isEndpoint(v)) and v.p.o.nslots > 2',
       '                if ((isSentence(v) or isPlace(v) or isInvocation(v)) and v.p.o.nslots > 2')]),
    ('K2', 'E10', 'an endpoint is written into', MAIN,
     [('                if (aop == .sattrn and endpointFixed(o)) {', '                if (aop == .sattrn and endpointFixed(o) and o.nslots == 0) {')]),
    ('K3', 'E01', 'the letter h does not hold an endpoint', MAIN,
     [("                    'h' => v.tag == .cptr or v.tag == .dll or isPlace(v) or isInvocation(v) or isEndpoint(v),",
       "                    'h' => v.tag == .cptr or v.tag == .dll or isPlace(v) or isInvocation(v),")]),
    ('K4', 'E09', '`new` of an endpoint is let through', COMPILE,
     [('        const an_endpoint = std.ascii.eqlIgnoreCase(ci.name, "haroendpoint");', '        const an_endpoint = ci.name.len == 0;')]),
    # the judge, in Haro
    ('J1', 'E11', 'a sentence of any language judges an endpoint', JLIB,
     [('\tif psDoors.Language() != "doors"\n\t\tRaise("Error (ENDPOINT_NO_DOORS)', '\tif psDoors.Language() = ""\n\t\tRaise("Error (ENDPOINT_NO_DOORS)')]),
    ('J2', 'E06', 'a peer the sentence does not declare is taken', JLIB,
     [('\tif not bFound\n\t\tRaise("Error (PEER_UNKNOWN)', '\tif not bFound and ptPeer = ""\n\t\tRaise("Error (PEER_UNKNOWN)')]),
    ('J3', 'E03', 'a blank or a control byte stands in an address', JLIB,
     [('\t\tif iByte < 33 or iByte > 126 or iByte = 92 Raise(tNo) end\n', '\t\tif iByte > 126 or iByte = 92 Raise(tNo) end\n')]),
    ('J4', 'E03', 'a byte past ASCII stands in an address', JLIB,
     [('\t\tif iByte < 33 or iByte > 126 or iByte = 92 Raise(tNo) end\n', '\t\tif iByte < 33 or iByte = 92 Raise(tNo) end\n')]),
    ('J5', 'E03', 'a backslash stands in an address', JLIB,
     [('\t\tif iByte < 33 or iByte > 126 or iByte = 92 Raise(tNo) end\n', '\t\tif iByte < 33 or iByte > 126 Raise(tNo) end\n')]),
    ('J6', 'E03', 'an address needs no scheme', JLIB,
     [('\tif iCut < 2 Raise(tNo) end\n', '\tif iCut < 2 Raise("Error (ENDPOINT_HOST) : planted") end\n')]),
    ('J7', 'E03', 'a scheme holds what is no letter', JLIB,
     [('\t\tif not IsAlpha(tScheme[i]) Raise(tNo) end\n', '')]),
    ('J8', 'E03', 'a name and a secret stand before the host', JLIB,
     [('\tif SubStr(tWhere, "@") > 0 or SubStr(tWhere, "[") > 0 or SubStr(tWhere, "]") > 0 Raise(tNo) end\n',
       '\tif SubStr(tWhere, "[") > 0 or SubStr(tWhere, "]") > 0 Raise(tNo) end\n')]),
    ('J9', 'E03', 'a bracket stands in the host', JLIB,
     [('\tif SubStr(tWhere, "@") > 0 or SubStr(tWhere, "[") > 0 or SubStr(tWhere, "]") > 0 Raise(tNo) end\n',
       '\tif SubStr(tWhere, "@") > 0 Raise(tNo) end\n')]),
    ('J10', 'E03', 'a port is no port', JLIB,
     [('\t\tif iPort < 1 or iPort > 65535 Raise(tNo) end\n', '')]),
    ('J11', 'E03', 'an address has no host', JLIB,
     [('\tif tName = "" Raise(tNo) end\n', '')]),
    ('J12', 'E05', 'a peer is reached by any scheme', JLIB,
     [('\tif not bReached\n', '\tif not bReached and tScheme = ""\n')]),
    ('J13', 'E04', 'any host is the peer\'s', JLIB,
     [('\telseif tName != tHost\n', '\telseif tName = ""\n')]),
    ('J14', 'E07', 'any address is in the network', JLIB,
     [('\t\tif not HaroInNet(tName, tNet)\n', '\t\tif not HaroInNet(tName, tNet) and tName = ""\n')]),
    ('J15', 'E07', 'a number begins with a zero', JLIB,
     [('\tif Len(ptDigits) > 1 and ptDigits[1] = "0" return -1 end\n', '')]),
    ('J16', 'E07', 'a part of an address is past 255', JLIB,
     [('\t\tif iPart < 0 or iPart > 255 or Len(tPart) > 3 return [] end\n', '\t\tif iPart < 0 return [] end\n')]),
    ('J17', 'E07', 'an address has any count of parts', JLIB,
     [('\tif Len(vNet) != 4 or Len(vOne) != 4 or iBits < 0 or iBits > 32 return false end\n',
       '\tif Len(vNet) != 4 or Len(vOne) < 3 or iBits < 0 or iBits > 32 return false end\n')]),
    ('J18', 'E07', 'the whole parts of the prefix are not compared', JLIB,
     [('\t\t\tif vOne[k] != vNet[k] return false end\n', '')]),
    ('J19', 'E05', 'a peer is reached at any port', JLIB,
     [('\tif iPort != iAllowed\n', '\tif iPort != iAllowed and iPort = 0\n')]),
    ('J20', 'E12', 'a peer with no port of any kind is reached', JLIB,
     [('\tif iAllowed = 0\n\t\tRaise(', '\tif iAllowed = -1\n\t\tRaise(')]),
    ('J21', 'E02', 'the scheme\'s own port is written', JLIB,
     [('\tif iPort != iOwn tUrl = tUrl + ":" + String(iPort) end\n', '\ttUrl = tUrl + ":" + String(iPort)\n')]),
    ('J22', 'E02', 'the host keeps its capitals', JLIB,
     [('\ttName = Lower(tName)\n', '')]),
    ('J23', 'E02', 'a peer that lists no scheme is reached by none', JLIB,
     [('\tif Len(vSchemes) = 0 vSchemes = ["https"] end\n', '')]),
    # the declaration of doors
    ('M1', 'E08', 'a peer with no host and no network is a sentence', DOORS,
     [('WHEN "net absent", THEN "host present"', 'WHEN "net absent", THEN "net absent"')]),
    ('M2', 'E08', 'a peer with a host and a network is a sentence', DOORS,
     [('WHEN "net present", THEN "host absent"', 'WHEN "net present", THEN "net present"')]),
    ('M3', 'E08', 'a peer is reached by a sixth scheme', DOORS,
     [('WORDS [https, http, wss, ws, tcp],', 'WORDS [https, http, wss, ws, tcp, gopher],')]),
    ('M4', 'E08', 'a host is any text', DOORS,
     [('SEATS [host: host_name?, net: net_prefix?,', 'SEATS [host: text?, net: net_prefix?,')]),
    ('M5', 'E08', 'a network is any text', DOORS,
     [('SEATS [host: host_name?, net: net_prefix?,', 'SEATS [host: host_name?, net: text?,')]),
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
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMPILE, JLIB, DOORS)}

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
            cache = os.path.join(CACHE, 'v76-' + pid)
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
