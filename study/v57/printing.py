"""Haro's own code printing one way (v0.57, D69): `see X + nl` is `print X`, a `see X` that ends no line is `FWrite(stdout, X)`. Over every
tracked .haro file of code but the cases of v0.55 and v0.57, which write `see` and `put` on purpose (their generators hold them).

  python study/v57/printing.py          rewrite, and print each change
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP = ('spike/v55/cases/', 'spike/v57/cases/')
NL = re.compile(r'^(\s*)see (.+?) \+ nl\s*$')
BARE = re.compile(r'^(\s*)see (.+?)\s*$')


def main():
    files = subprocess.run(['git', 'ls-files', '*.haro'], capture_output=True, text=True, cwd=ROOT).stdout.split()
    n = 0
    for rel in files:
        if rel.startswith(SKIP):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, 'rb').read().decode('utf-8')
        if re.search(r'(?m)^\s*DEFINE\b', src) or not re.search(r'(?m)^\s*see ', src):
            continue
        out = []
        for line in src.split('\n'):
            m = NL.match(line) or None
            if m:
                new = f'{m.group(1)}print {m.group(2)}'
            else:
                m = BARE.match(line)
                new = f'{m.group(1)}FWrite(stdout, {m.group(2)})' if m else line
            if new != line:
                n += 1
                print(f'{rel}: {line.strip()}  ->  {new.strip()}')
            out.append(new)
        open(path, 'wb').write('\n'.join(out).encode('utf-8'))
    print(f'{n} lines')


if __name__ == '__main__':
    main()
