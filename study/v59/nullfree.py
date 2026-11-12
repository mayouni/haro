"""Haro's own code without null (v0.59, D71): `null` is `""` -- the value it always was -- and `IsNull(x)` is `IsEmpty(x)`, over every
tracked .haro file of code but v0.59's cases, which write both on purpose.

  python study/v59/nullfree.py          rewrite, and print the counts
"""
import collections, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'port'))
import haroport as H

SKIP = ('spike/v59/cases/',)


def rewrite(src, counts):
    toks = H.tokens(src)
    for i, (k, v) in enumerate(toks):
        if k != 'id' or H.is_member(toks, i) or H.is_symbol(toks, i):
            continue
        if v == 'null':
            toks[i] = ['st', '""']
            counts['null -> ""'] += 1
        elif v == 'IsNull':
            j = H.sig(toks, i, 1)
            if j is not None and toks[j][1] == '(':
                toks[i][1] = 'IsEmpty'
                counts['IsNull -> IsEmpty'] += 1
    return ''.join(v for _, v in toks)


def main():
    files = subprocess.run(['git', 'ls-files', '*.haro'], capture_output=True, text=True, cwd=ROOT).stdout.split()
    counts = collections.Counter()
    changed = 0
    for rel in files:
        if rel.startswith(SKIP):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, 'rb').read().decode('utf-8')
        if re.search(r'(?m)^\s*DEFINE\b', src):
            continue
        new = rewrite(src, counts)
        if new != src:
            changed += 1
            open(path, 'wb').write(new.encode('utf-8'))
    for k, n in counts.items():
        print(f'{n:6}  {k}')
    print(f'{changed} files changed')


if __name__ == '__main__':
    main()
