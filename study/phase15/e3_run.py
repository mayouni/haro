"""Phase 1.5, E3: NaturalLib 1.27 as shipped. Runs e3_naturallib.ring on the official Ring
install -- the library's own runtime, a deliberate and named reach outside this repository: the
study's subject IS that library as shipped -- and asks Ring++ to load it, then records the facts
the study cites. Prints PASS/FAIL per fact; exits 1 on any FAIL. Writes e3_result.txt.

Usage: python haro/study/phase15/e3_run.py
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
RING_OFFICIAL = r'D:\ring127\bin\ring.exe'
NATLIB = r'D:\ring127\libraries\naturallib'
RNXC = paths.HARO_VM
EXP = os.path.join(HERE, 'e3_naturallib.ring')


def run(exe, args, cwd):
    p = subprocess.run([exe] + args, capture_output=True, cwd=cwd, timeout=180)
    return p.returncode, p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), p.stderr.decode('utf-8', 'replace').replace('\r\n', '\n')


def main():
    facts = []

    def fact(ok, text):
        facts.append((ok, text))
        print(('PASS ' if ok else 'FAIL ') + text)
    if not os.path.exists(RING_OFFICIAL) or not os.path.isdir(NATLIB):
        print('SKIP: the official Ring 1.27 install is not at D:\\ring127; E3 measures NaturalLib as shipped')
        return 0
    rc, out, err = run(RING_OFFICIAL, [EXP], HERE)
    open(os.path.join(HERE, 'e3_result.txt'), 'w', encoding='utf-8', newline='').write(out)
    line = {m.group(1): m.group(2) for m in re.finditer(r'^(E3[a-d]\d?) (.*)$', out, re.M)}
    fact(rc == 0 and len(line) == 5, f'official Ring 1.27 runs the experiment: exit {rc}, {len(line)} of 5 result lines')
    fact('query=<SELECT * FROM collect WHERE amount > 5000>' in line.get('E3a', ''),
         'E3a retargeting works at the command level: "show deposits over 5000" -> a ZQL string, nothing executed')
    fact('query=<SELECT * FROM collect WHERE amount > 5000>' in line.get('E3b', ''),
         'E3b a second language works, as a second set of commands: "montre les depots au dessus de 5000" -> the same ZQL')
    fact('query=<>' in line.get('E3c1', '') and 'error=<>' in line.get('E3c1', ''),
         'E3c1 an argument the vocabulary cannot read ("lots") is silently dropped: no query, no error')
    fact('query=<>' in line.get('E3c2', '') and 'error=<>' in line.get('E3c2', ''),
         'E3c2 prose the vocabulary does not know is silently accepted: no query, no error, no refusal')
    fact('ESCAPED: this line ran as Ring' in out.split('E3d')[0].splitlines()[-1] if 'E3d' in out else False,
         'E3d the question carried a Ring statement and it RAN: the natural-language surface is the host language')
    # the library's own answer path, quoted from its source
    src = open(os.path.join(NATLIB, 'common', 'naturallanguage.ring'), encoding='utf-8').read().splitlines()
    fact('eval(prepareCode(cString))' in src[243].replace('\t', '') or 'eval(prepareCode(cString))' in src[243],
         'naturallanguage.ring:244 RunString is eval(prepareCode(cString)): the text is pasted into Ring source and evaluated')
    # Ring++ : the library as shipped
    rc, out, err = run(RNXC, [os.path.join(HERE, 'e3_probe_rnx.ring')], HERE) if os.path.exists(os.path.join(HERE, 'e3_probe_rnx.ring')) else (None, '', '')
    if rc is not None:
        fact(rc != 0 and 'Rule A' in out + err, 'Ring++ refuses NaturalLib\'s own source before running a line of it (Rule A: its C_NATLIB_* constants are bare globals)')
    names = ('changeringkeyword', 'changeringoperator', 'braceexpreval', 'braceerror')
    hits = 0
    for f in os.listdir(os.path.join(ROOT, 'src')):
        if f.endswith('.zig'):
            t = open(os.path.join(ROOT, 'src', f), encoding='utf-8', errors='replace').read().lower()
            hits += sum(t.count(n) for n in names)
    fact(hits == 0, f'Ring++ implements none of {", ".join(names)} (0 mentions in src/*.zig): they are what NaturalLib stands on')
    bad = [t for ok, t in facts if not ok]
    print(f'e3: {len(facts) - len(bad)} of {len(facts)} facts hold')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
