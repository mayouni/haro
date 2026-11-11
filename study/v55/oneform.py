"""Haro's own code written in one form (v0.55, D67, HARO-ONEFORM-01): haroport's rule O over every tracked .haro file of code -- a
declaration (a file that opens a DEFINE) is no code and is left, and so are v0.55's cases, which write the other forms on purpose. A
definition's end word goes and leaves its line, so every line keeps its number.

  python study/v55/oneform.py          rewrite, and print what changed
  python study/v55/oneform.py --plan   print only
"""
import collections, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'port'))
import haroport as H

SKIP = ('spike/v55/cases/',)


def main():
    plan = '--plan' in sys.argv
    files = subprocess.run(['git', 'ls-files', '*.haro'], capture_output=True, text=True, cwd=ROOT).stdout.split()
    total = collections.Counter()
    changed = 0
    for rel in files:
        if rel.startswith(SKIP):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, 'rb').read().decode('utf-8')
        if re.search(r'(?m)^\s*DEFINE\b', src):
            continue
        renames = []
        new = ''.join(v for _, v in H.one_form(H.tokens(src), renames))
        if new == src:
            continue
        changed += 1
        for _, old, nw in renames:
            total[(old if len(old) < 12 else old[:12]) + ' -> ' + (nw or '(none)')] += 1
        if not plan:
            open(path, 'wb').write(new.encode('utf-8'))
    for k, n in total.most_common():
        print(f'{n:6}  {k}')
    print(f'{changed} files {"to change" if plan else "changed"}')


if __name__ == '__main__':
    main()
