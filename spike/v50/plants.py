"""Every protection of v0.50 (a program that serves another, HARO-STDIOFLUSH-01) switched off in turn: the court must fail, for the
fixture that protection exists for. Each plant is text substitutions in vm/src/main.zig or vm/src/compile.zig, built into
runtime/v50/plant-build (ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte --
verified by their digests, and restored even when a build fails or the script is stopped.

  python spike/v50/plants.py            all plants (about two minutes each)
  python spike/v50/plants.py F1 F3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v50', 'plant-build')
COURT = os.path.join(HERE, 'stdio_court.py')
NL = chr(10)

PLANTS = [
    ('F1', 'D01', 'give waits without sending the output', MAIN,
     [('                        outFlush();' + NL + '                        var line: std.ArrayListUnmanaged(u8) = .{};',
       '                        var line: std.ArrayListUnmanaged(u8) = .{};')]),
    ('F2', 'D03', 'fflush(stdout) leaves what see holds', MAIN,
     [('                                if (fp == cStream(1)) outFlush();', '                                if (false) outFlush();')]),
    ('F3', 'D05', 'a write through stdout goes before what see holds', MAIN,
     [('                        if (to_out) outFlush();', '                        if (false) outFlush();')]),
    ('F4', 'D05', 'a write through stdout waits in C\'s buffer, and the next see passes it', MAIN,
     [('                        defer if (to_out) {', '                        defer if (false) {')]),
    ('F5', 'D08', 'a line is cut at 4,096 bytes again', MAIN,
     [('                            line.append(self.alloc, one[0]) catch @panic("oom");',
       '                            if (line.items.len < 4096) line.append(self.alloc, one[0]) catch @panic("oom");')]),
    ('F6', 'D10', 'give does not remember the end of input', MAIN,
     [('                                stdin_ended = true;', '                                stdin_ended = false;')]),
    ('F7', 'D12', 'FEOF answers a number in a .haro file', COMP,
     [('"iswindows64", "isxdigit", "fexists", "direxists", "feof" };', '"iswindows64", "isxdigit", "fexists", "direxists" };')]),
    ('F8', 'D05', 'the three streams are not defined', COMP,
     [('            if (if (haro) std.mem.eql(u8, nm, w) else std.ascii.eqlIgnoreCase(nm, w)) return id;',
       '            if (false and (if (haro) std.mem.eql(u8, nm, w) else std.ascii.eqlIgnoreCase(nm, w))) return id;')]),
    # F9 MISSED on its first run: D07 read the program's `stdout` at the top level only, where the main chunk finds its own name before
    # the stream is asked. D07 was changed after the code (said so) to read it from a function, and F9 is caught.
    ('F9', 'D07', 'a program\'s own global named stdout is not its own', COMP,
     [('                if (self.knownGlobal(nm)) |slot|' + NL + '                    _ = try self.emit(.gorc, dst, 0, 0, slot);' + NL
       + '                return;' + NL + '            }' + NL + '            // Inside `obj',
       '                return;' + NL + '            }' + NL + '            // Inside `obj')]),
    ('F10', 'D14', 'a .haro file reads the streams in any case', COMP,
     [('            if (if (haro) std.mem.eql(u8, nm, w) else std.ascii.eqlIgnoreCase(nm, w)) return id;',
       '            if (if (haro) std.ascii.eqlIgnoreCase(nm, w) else std.ascii.eqlIgnoreCase(nm, w)) return id;')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMP)}

    def restore():
        for p, b in originals.items():
            open(p, 'wb').write(b)
            assert digest(open(p, 'rb').read()) == digest(b)

    results = []
    try:
        for pid, fixture, why, path, subs in PLANTS:
            if want and pid not in want:
                continue
            raw = originals[path].decode('utf-8')
            crlf = (chr(13) + NL) in raw
            text = raw.replace(chr(13) + NL, NL)
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r} ({text.count(stale[0])} found)', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(path, 'wb').write((planted.replace(NL, chr(13) + NL) if crlf else planted).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=900)
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
