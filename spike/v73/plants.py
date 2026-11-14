"""Every protection of v0.73 (the command and the invocation; doc/DOORS.md rung 2, D88 (d)) switched off in turn: the court must fail,
for the fixture that protection exists for. A plant is text substitutions in one file. In vm/src it is built into
runtime/v73/plant-build (ReleaseFast, -j2, one build at a time, and only when the machine has 8 GB free) and its fixture's case run
on that build alone; in the judging library and in the declaration of doors nothing is built -- the case runs on the base build,
runtime/v73/build, which reads the planted file. Each plant forges into a cache of its own. Every file is restored byte for byte,
verified by its digest, and restored even when a build fails or the script is stopped; the cases' own files are written again
after each.

  python spike/v73/plants.py            all plants (about two minutes each for those that build)
  python spike/v73/plants.py K1 J3      some
"""
import ctypes, hashlib, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMPILE = os.path.join(VM_DIR, 'src', 'compile.zig')
BUILTINS = os.path.join(VM_DIR, 'src', 'builtins.zig')
JLIB = os.path.join(SPIKE, 'judge_lib.haro')
DOORS = os.path.join(SPIKE, 'doors.haro')
OUT = os.path.join(ROOT, 'runtime', 'v73', 'plant-build')
CACHE = os.path.join(ROOT, 'runtime', 'v73', 'plant-cache')
BASE = os.path.join(ROOT, 'runtime', 'v73', 'build', 'bin', 'haro.exe')
COURT = os.path.join(HERE, 'invocation_court.py')
NEED_GB = 8.0

NOT_STARTED = ('                self.pending = self.haroMsg("Error (COMMAND_NOT_STARTED) : the command `{s}` runs `{s}`, which could not be started", .{ name, argv.items[0] });\n'
               '                return null;\n')
NOT_STARTED_2 = NOT_STARTED.replace('                ', '            ')
PLANTS = [
    # the VM
    ('K1', 'V01', 'an invocation does not print as its line', MAIN,
     [('                if ((isSentence(v) or isPlace(v) or isInvocation(v)) and v.p.o.nslots > 2', '                if ((isSentence(v) or isPlace(v)) and v.p.o.nslots > 2')]),
    ('K2', 'V13', 'an invocation is written into', MAIN,
     [('                if (aop == .sattrn and invocationFixed(o)) {', '                if (aop == .sattrn and invocationFixed(o) and o.nslots == 0) {')]),
    ('K3', 'V01', 'the letter h does not hold an invocation', MAIN,
     [("                    'h' => v.tag == .cptr or v.tag == .dll or isPlace(v) or isInvocation(v),", "                    'h' => v.tag == .cptr or v.tag == .dll or isPlace(v),")]),
    ('K4', 'V03', 'System does not take an invocation', MAIN,
     [('                        if (isInvocation(regs[A])) {\n', '                        if (isInvocation(regs[A]) and in.c > 1000) {\n')]),
    ('K5', 'V02', 'SystemCmd does not take an invocation', MAIN,
     [('                if (in.c == 1 and isInvocation(regs[base + in.b]) and std.ascii.eqlIgnoreCase(nm, "systemcmd")) {',
       '                if (in.c == 1000 and isInvocation(regs[base + in.b]) and std.ascii.eqlIgnoreCase(nm, "systemcmd")) {')]),
    ('K6', 'V15', 'QUIET does not send away the standard error SystemCmd read', MAIN,
     [('            if (!quiet and res.stderr.len > 0) std.debug.print', '            if (res.stderr.len > 0) std.debug.print')]),
    ('K7', 'V15', 'QUIET does not send away the standard error under System', MAIN,
     [('        child.stderr_behavior = if (quiet) .Ignore else .Inherit;', '        child.stderr_behavior = .Inherit;')]),
    ('K8', 'V14', 'SystemCmd drops the standard error of a command that is not quiet', MAIN,
     [('            if (!quiet and res.stderr.len > 0) std.debug.print', '            if (!quiet and res.stderr.len > (1 << 40)) std.debug.print')]),
    ('K9', 'V11', 'SystemCmd answers nothing when the program cannot be started', MAIN,
     [('.max_output_bytes = 1 << 30 }) catch {\n' + NOT_STARTED, '.max_output_bytes = 1 << 30 }) catch {\n                return Value.str(self.newStr(""));\n')]),
    ('K10', 'V11', 'System answers -1 when the program cannot be started', MAIN,
     [('        const term = child.spawnAndWait() catch {\n' + NOT_STARTED_2, '        const term = child.spawnAndWait() catch {\n            return Value.int(-1);\n')]),
    ('K11', 'V02', 'the last line end of what the child wrote is kept', MAIN,
     [('            var s: []const u8 = res.stdout;\n            if (std.mem.endsWith(u8, s, "\\r\\n")) s = s[0 .. s.len - 2] else if (std.mem.endsWith(u8, s, "\\n")) s = s[0 .. s.len - 1];\n',
       '            const s: []const u8 = res.stdout;\n')]),
    ('K12', 'V03', 'the exit code is not answered', MAIN,
     [('            .Exited => |c| @intCast(c),\n            else => -1,\n        });\n    }\n\n    /// v0.72 (doc/DOORS.md): a place at a door.',
       '            .Exited => 0,\n            else => -1,\n        });\n    }\n\n    /// v0.72 (doc/DOORS.md): a place at a door.')]),
    ('K13', 'V03', 'what the program wrote first is not written before the child runs', MAIN,
     [('        outFlush();\n        if (capture) {\n', '        if (capture) {\n')]),
    ('K17', 'V15', 'QUIET does not send away what the child writes under System', MAIN,
     [('        child.stdout_behavior = if (quiet) .Ignore else .Inherit;', '        child.stdout_behavior = .Inherit;')]),
    ('K18', 'V20', 'the child SystemCmd starts does not stand in its folder', MAIN,
     [('.argv = argv.items, .cwd = folder, .max_output_bytes', '.argv = argv.items, .cwd = null, .max_output_bytes')]),
    ('K19', 'V20', 'the child System starts does not stand in its folder', MAIN,
     [('        child.cwd = folder;\n', '')]),
    ('K14', 'V12', '`new` of an invocation is let through', COMPILE,
     [('        const an_invocation = std.ascii.eqlIgnoreCase(ci.name, "haroinvocation");', '        const an_invocation = ci.name.len == 0;')]),
    ('K15', 'V18', 'a forged court\'s folder is named by where haro stands alone', HARO,
     [('    if (std.fs.cwd().statFile(self)) |st| {', '    if (std.fs.cwd().statFile("")) |st| {')]),
    ('K16', 'V16', 'the checker does not know SystemCmd', BUILTINS,
     [('pub const own = [_][]const u8{"systemcmd"};', 'pub const own = [_][]const u8{"systemcmd-unknown"};')]),
    # the judge, in Haro
    ('J1', 'V17', 'a sentence of any language judges an invocation', JLIB,
     [('\tif psDoors.Language() != "doors"\n\t\tRaise("Error (INVOCATION_NO_DOORS)', '\tif psDoors.Language() = ""\n\t\tRaise("Error (INVOCATION_NO_DOORS)')]),
    ('J2', 'V07', 'a command the sentence does not declare is taken', JLIB,
     [('\tif not bFound\n\t\tRaise("Error (COMMAND_UNKNOWN)', '\tif not bFound and ptCommand = ""\n\t\tRaise("Error (COMMAND_UNKNOWN)')]),
    ('J3', 'V08', 'a shell by its name is a command', JLIB,
     [('\t\tif tBase = vShells[i] bShell = true end\n', '')]),
    ('J4', 'V08', 'a file a shell reads is a command', JLIB,
     [('\t\tif tKind = vKinds[i] bShell = true end\n', '')]),
    ('J5', 'V08', 'a shell named with its folder is a command', JLIB,
     [('\t\tif tBase[i] = "/" or Ascii(tBase[i]) = 92\n', '\t\tif tBase[i] = "/" and Ascii(tBase[i]) = 92\n')]),
    ('J6', 'V19', 'a command takes words twice', JLIB,
     [('\tif iRuns > 1\n', '\tif iRuns > 100\n')]),
    ('J7', 'V05', 'the arguments are given as anything', JLIB,
     [('\tif not IsList(pxArguments)\n', '\tif not IsList(pxArguments) and iRuns > 100\n')]),
    ('J8', 'V06', 'any count of arguments is taken', JLIB,
     [('\tif iRuns = 0 and iGiven != iTakes\n', '\tif iRuns = 0 and iGiven > 1000\n')]),
    ('J9', 'V06', 'fewer arguments than the shapes are taken beside words', JLIB,
     [('\tif iRuns = 1 and iGiven < iTakes\n', '\tif iRuns = 1 and iGiven < 0\n')]),
    ('J10', 'V05', 'a text is a number', JLIB,
     [('\t\tif not IsNumber(pxValue) Raise(tNo + "number") end\n', '')]),
    ('J11', 'V05', 'a text is a place', JLIB,
     [('\t\tif not HaroIsPlace(pxValue) Raise(tNo + "place") end\n\t\treturn pxValue.Path()\n', '\t\tif not HaroIsPlace(pxValue) return pxValue end\n\t\treturn pxValue.Path()\n')]),
    ('J12', 'V05', 'any text is a word', JLIB,
     [('\t\tif not HaroIsWord(pxValue) Raise(tNo + "word") end\n', '')]),
    ('J13', 'V05', 'a word begins with a dash', JLIB,
     [('\tif ptWord[1] = "-" return false end\n', '')]),
    ('J14', 'V05', 'a word holds any byte', JLIB,
     [('\t\tif SubStr("_-.,=", ptWord[i]) > 0 loop end\n\t\treturn false\n', '\t\tif SubStr("_-.,=", ptWord[i]) > 0 loop end\n\t\tloop\n')]),
    ('J15', 'V05', 'nothing is a word', JLIB,
     [('\tif Len(ptWord) = 0 return false end\n\tif ptWord[1] = "-" return false end\n', '\tif Len(ptWord) = 0 return true end\n\tif ptWord[1] = "-" return false end\n')]),
    ('J16', 'V05', 'an option needs no dash', JLIB,
     [('\t\telse\n\t\t\tRaise(tNo + "option")\n\t\tend\n', '\t\tend\n')]),
    ('J17', 'V05', 'an option holds any text after its dash', JLIB,
     [('\t\tif not HaroIsWord(tRest) Raise(tNo + "option") end\n', '')]),
    ('J18', 'V05', 'a text begins with a dash', JLIB,
     [('\tif Left(pxValue, 1) = "-" Raise(tNo + "text") end\n', '')]),
    ('J19', 'V05', 'a text holds a control byte', JLIB,
     [('\t\tif iByte < 32 or iByte = 127 Raise(tNo + "text") end\n', '')]),
    ('J20', 'V05', 'a number is a text', JLIB,
     [('\tif not IsString(pxValue) Raise(tNo + "text") end\n', '\tif not IsString(pxValue) return "7" end\n')]),
    ('J21', 'V05', 'a number is a word', JLIB,
     [('\t\tif not IsString(pxValue) Raise(tNo + "word") end\n', '\t\tif not IsString(pxValue) return "7" end\n')]),
    ('J22', 'V05', 'a number is an option', JLIB,
     [('\t\tif not IsString(pxValue) Raise(tNo + "option") end\n', '\t\tif not IsString(pxValue) return "-7" end\n')]),
    ('J23', 'V02', 'ITSELF does not run this haro', JLIB,
     [('\tif bItself\n\t\ttProgram = ExeFileName()\n', '\tif bItself\n\t\ttProgram = "a-haro-that-is-not-there"\n')]),
    ('J24', 'V15', 'QUIET is not read', JLIB,
     [('\t\t\tif tKey = "quiet" bQuiet = (xClauses[k][3][2] = "yes") end\n', '')]),
    ('J25', 'V01', 'an argument with a blank prints bare', JLIB,
     [('\tif ptArgument = "" or SubStr(ptArgument, " ") > 0 or SubStr(ptArgument, tQuote) > 0\n', '\tif ptArgument = "never this"\n')]),
    ('J26', 'V04', 'words is one word', JLIB,
     [('\t\tif tShape = "words" iTimes = 1 + iGiven - iTakes end\n', '')]),
    ('J27', 'V10', 'RUNS is not read', JLIB,
     [('\t\t\tif tKey = "runs" tRuns = xClauses[k][3][2] end\n', '')]),
    ('J28', 'V20', 'IN is not read', JLIB,
     [('\t\t\tif tKey = "in" tIn = xClauses[k][3][2] end\n', '')]),
    ('J29', 'V21', 'a command runs in a root that has no folder', JLIB,
     [('\t\tif tFolder = ""\n\t\t\tRaise("Error (COMMAND_IN)', '\t\tif tFolder = "never this"\n\t\t\tRaise("Error (COMMAND_IN)')]),
    ('J30', 'V20', 'a child that stands elsewhere is given a place as this program reads it', JLIB,
     [('\t\t\tif tShape = "place" and tFolder != "" tArgument = HaroWholePath(tArgument) end\n', '')]),
    # the declaration of doors
    ('M1', 'V09', 'a command that runs nothing is a sentence', DOORS,
     [('WHEN "itself absent", THEN "runs present"', 'WHEN "itself absent", THEN "itself absent"')]),
    ('M2', 'V09', 'a command that says ITSELF and RUNS is a sentence', DOORS,
     [('WHEN "itself present", THEN "runs absent"', 'WHEN "itself present", THEN "itself present"')]),
    ('M3', 'V09', 'an argument has a seventh shape', DOORS,
     [('WORDS [word, option, number, place, text, words],', 'WORDS [word, option, number, place, text, words, line],')]),
    ('M4', 'V21', 'IN names anything', DOORS,
     [('quiet: flag?, in: root?],', 'quiet: flag?, in: name?],')]),
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
    stray = os.path.join(HERE, 'cases', 'out.txt')
    if os.path.exists(stray):
        os.remove(stray)


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (HARO, MAIN, COMPILE, BUILTINS, JLIB, DOORS)}

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
