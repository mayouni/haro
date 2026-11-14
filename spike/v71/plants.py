"""Every protection of v0.71 (the literal and `of`; TYPES.md T7, D83) switched off in turn: the court must fail, for the fixture that
protection exists for. A plant is text substitutions in one file. In vm/src it is built into runtime/v71/plant-build (ReleaseFast,
-j2, one build at a time) and the court run on that build alone; in the judging library nothing is built -- the court runs on the base
build, runtime/v71/build, which reads the planted library. Every file is restored byte for byte, verified by its digest, and restored
even when a build fails or the script is stopped.

  python spike/v71/plants.py            all plants (about two minutes each for those that build)
  python spike/v71/plants.py P1 P3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
LIFT = os.path.join(VM_DIR, 'src', 'lift.zig')
JLIB = os.path.join(SPIKE, 'judge_lib.haro')
OUT = os.path.join(ROOT, 'runtime', 'v71', 'plant-build')
BASE = os.path.join(ROOT, 'runtime', 'v71', 'build', 'bin', 'haro.exe')
COURT = os.path.join(HERE, 'literal_court.py')

PLANTS = [
    ('P1', 'Q01', 'a language\'s name with a text after it is not read as a literal', HARO,
     [("            if (lang != null and e < src.len and (src[e] == '\"' or src[e] == '\\'' or src[e] == '`')) {",
       "            if (lang != null and e == 0 and e < src.len and (src[e] == '\"' or src[e] == '\\'' or src[e] == '`')) {")]),
    ('P2', 'Q03', 'a literal is not judged when the program is compiled', HARO,
     [('                if (fault == null) if (judgeLiteral(alloc, lang.?, src[e + 1 .. q])) |refusal| {',
       '                if (fault != null) if (judgeLiteral(alloc, lang.?, src[e + 1 .. q])) |refusal| {')]),
    ('P3', 'Q04', '`of` before a language is not taken from the header', HARO,
     [('                } else if (is_lang) {\n', '                } else if (is_lang and named.len == 0) {\n')]),
    ('P4', 'Q10', '`of` before a word that is no language is let through', HARO,
     [('                    if (fault == null) fault = .{ .why = "`of` names a language this file loads; written"',
       '                    if (fault != null) fault = .{ .why = "`of` names a language this file loads; written"')]),
    ('P5', 'Q14', '`of` away from a header is let through', HARO,
     [("                    if (fault == null) fault = .{ .why = \"`of` stands on a definition's header",
       "                    if (fault != null) fault = .{ .why = \"`of` stands on a definition's header")]),
    ('P6', 'Q12', 'what the loader put in is not counted when a column is named', HARO,
     [('    if (mine.len == 0) return theirs;\n', '    if (mine.len < 1000000) return theirs;\n')]),
    ('P7', 'Q05', 'a parameter\'s check is not written', LIFT,
     [('                if (!eq(ch.kind(), "{")) continue;\n                const text = try std.fmt.allocPrint(alloc, " HaroOfGiven(',
       '                if (!eq(ch.kind(), "{{")) continue;\n                const text = try std.fmt.allocPrint(alloc, " HaroOfGiven(')]),
    ('P8', 'Q08', 'an answer\'s check is not written', LIFT,
     [('                try ofReturns(alloc, n, true, m.lang, fname, out);\n', '                if (m.lang.len == 0) try ofReturns(alloc, n, true, m.lang, fname, out);\n')]),
    ('P9', 'Q05', 'a parameter takes a sentence of any language', JLIB,
     [('\t\tif pxValue.Language() != ptLanguage\n\t\t\tRaise("Error (SENTENCE_OF_ANOTHER) : `" + ptName + "` is a sentence of ',
       '\t\tif pxValue.Language() = ""\n\t\t\tRaise("Error (SENTENCE_OF_ANOTHER) : `" + ptName + "` is a sentence of ')]),
    ('P10', 'Q08', 'a definition answers a sentence of any language', JLIB,
     [('\t\tif pxValue.Language() != ptLanguage\n\t\t\tRaise("Error (SENTENCE_OF_ANOTHER) : `" + ptName + "` answers a sentence of ',
       '\t\tif pxValue.Language() = ""\n\t\t\tRaise("Error (SENTENCE_OF_ANOTHER) : `" + ptName + "` answers a sentence of ')]),
    ('P11', 'Q09', 'a definition of a language answers a text', JLIB,
     [('\t\tRaise("Error (SENTENCE_EXPECTED) : `" + ptName + "` answers a sentence of " + ptLanguage + ", and answers a text")\n',
       '\t\treturn pxValue\n')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (HARO, LIFT, JLIB)}

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
            crlf = '\r\n' in raw
            text = raw.replace('\r\n', '\n')
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r} ({text.count(stale[0])} found)', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(path, 'wb').write((planted.replace('\n', '\r\n') if crlf else planted).encode('utf-8'))
            exe = BASE
            if path.endswith('.zig'):
                b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=1800)
                restore()
                if b.returncode != 0:
                    print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                    results.append((pid, 'BUILD FAILED'))
                    continue
                exe = os.path.join(OUT, 'bin', 'haro.exe')
            r = subprocess.run([sys.executable, COURT, '--vm', exe], capture_output=True, timeout=900)
            restore()
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
