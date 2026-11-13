"""Every protection of v0.70 (a program judges; TYPES.md T7, D83) switched off in turn: the court must fail, for the fixture that
protection exists for. A plant is text substitutions in one file. In vm/src it is built into runtime/v70/plant-build (ReleaseFast,
-j2, one build at a time) and the court run on that build alone; in a library of spike/ nothing is built -- the court runs on the base
build, runtime/v70/build, which reads the planted library. Every file is restored byte for byte, verified by its digest, and restored
even when a build fails or the script is stopped.

A plant that caught nothing, kept here as what it found: a write into a sentence by its SLOT (the VM's `sattr`) was refused too, and
switching that off failed no case -- a write from outside the class goes by the attribute's name (`sattrn`, K10). The check was
taken out, and looking for what else reaches a sentence found `new HaroSentence` (J15, K15).

  python spike/v70/plants.py            all plants (about two minutes each for those that build)
  python spike/v70/plants.py K1 K3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
VM_DIR = os.path.join(ROOT, 'vm')
HARO = os.path.join(VM_DIR, 'src', 'haro.zig')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
JLIB = os.path.join(SPIKE, 'judge_lib.haro')
CLIB = os.path.join(SPIKE, 'court_lib.haro')
OUT = os.path.join(ROOT, 'runtime', 'v70', 'plant-build')
BASE = os.path.join(ROOT, 'runtime', 'v70', 'build', 'bin', 'haro.exe')
COURT = os.path.join(HERE, 'sentence_court.py')

PLANTS = [
    ('K1', 'J01', 'a loaded declaration is read as code, not forged', HARO,
     [('    return std.mem.startsWith(u8, src[i..], "DEFINE ") or std.mem.startsWith(u8, src[i..], "DEFINE\\t");',
       '    return src.len == 0 and std.mem.startsWith(u8, src[i..], "DEFINE ");')]),
    ('K2', 'J01', 'a language\'s name is not read as its language', HARO,
     [('            if (is_lang) {\n', '            if (is_lang and word.len == 0) {\n')]),
    ('K3', 'J02', 'the language\'s version is not read from its declaration', HARO,
     [('    return src[at + 1 .. e];\n}\n\n/// The forge\'s folder', '    return src[e..e];\n}\n\n/// The forge\'s folder')]),
    ('K4', 'J13', 'a declaration the meta-court refuses is loaded all the same', HARO,
     [('        if (!std.mem.startsWith(u8, line, "forged ")) {', '        if (line.len == 0 and !std.mem.startsWith(u8, line, "forged ")) {')]),
    ('K5', 'J13', 'the refusal of a declaration stands at its first line, not the meta-court\'s', HARO,
     [('.row = row -| 1 } };', '.row = 0 } };')]),
    ('K6', 'J14', 'a forged court is kept by its name alone, not by its declaration\'s bytes', HARO,
     [('    h.update(decl);\n', '')]),
    ('K7', 'J06', 'the compiler does not check the letter s', COMP,
     [('    const CHECKED = "bidntfvoherms";', '    const CHECKED = "bidntfvoherm";')]),
    ('K8', 'J07', 'the letter s takes any value when the program runs', MAIN,
     [("                    's' => isSentence(v),", "                    's' => true,")]),
    ('K9', 'J01', 'a sentence prints as an object\'s attributes', MAIN,
     [('                if (isSentence(v) and v.p.o.nslots > 2 and v.p.o.slots[2].tag == .str) {',
       '                if (isSentence(v) and v.p.o.nslots > 99 and v.p.o.slots[2].tag == .str) {')]),
    ('K10', 'J09', 'a write into a sentence by its attribute\'s name is taken', MAIN,
     [('                if (aop == .sattrn and sentenceFixed(o)) {', '                if (aop == .sattrn and sentenceFixed(o) and o.nslots > 99) {')]),
    ('K15', 'J15', 'a program makes a sentence itself, with new', COMP,
     [('            if (!own) {\n                if (self.spellIn(n.text())) self.spellSet(n.text(), "a sentence is made by its court',
       '            if (!own and ci.name.len == 0) {\n                if (self.spellIn(n.text())) self.spellSet(n.text(), "a sentence is made by its court')]),
    ('K11', 'J03', 'the court\'s refusal is raised without its code', JLIB,
     [('\tRaise("Error (" + ptCode + ") : " + ptMessage)\n', '\tRaise(ptMessage)\n')]),
    ('K12', 'J01', 'a court loaded by a program runs its main', CLIB,
     [('\tif IsGlobal("$bHaroJudges") return end\n', '')]),
    ('K13', 'J10', 'a language is judged with the tables of the last court loaded', JLIB,
     [('\t$vCourtLangs = vEntry[3]\n', '')]),
    ('K14', 'J09', 'a sentence is never fixed', JLIB,
     [('\t\tbFixed = true\n', '')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (HARO, MAIN, COMP, JLIB, CLIB)}

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
