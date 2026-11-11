"""Haro's own code with every definition ended by `end`, `func` for a function and `def` for a method (v0.56, D68, HARO-DEFINITIONS-01):
haroport's `def_ends` over every tracked .haro file of code. A declaration (a file that opens a DEFINE) is no code and is left; v0.55's and
v0.56's cases are written by their generators. An `end` takes the blank line after its definition when there is one, so the lines after
keep their numbers; else it takes a line of its own, and the lines after move down one: each file's moves are written to
runtime/v56/linemap.json, for the fixtures that name a line.

  python study/v56/defends.py          rewrite, and print what changed
  python study/v56/defends.py --plan   print only
"""
import collections, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'port'))
import haroport as H

SKIP = ('spike/v55/cases/', 'spike/v56/cases/')


def linemap(old, new):
    """old line number -> new line number, for the lines that kept their text (ends are added lines)"""
    a, b = old.split('\n'), new.split('\n')
    m, j = {}, 0
    for i, line in enumerate(a):
        while j < len(b) and b[j] != line and b[j].strip() == 'end':
            j += 1
        if j < len(b) and b[j] == line:
            m[i + 1] = j + 1
            j += 1
        else:
            m[i + 1] = j + 1
            j += 1
    return m


def main():
    plan = '--plan' in sys.argv
    files = subprocess.run(['git', 'ls-files', '*.haro'], capture_output=True, text=True, cwd=ROOT).stdout.split()
    total = collections.Counter()
    changed = moved = 0
    maps = {}
    for rel in files:
        if rel.startswith(SKIP):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, 'rb').read().decode('utf-8')
        if re.search(r'(?m)^\s*DEFINE\b', src):
            continue
        renames = []
        new = ''.join(v for _, v in H.def_ends(H.tokens(src), renames))
        if new == src:
            continue
        changed += 1
        for _, old, nw in renames:
            total[old + ' -> ' + nw] += 1
        if new.count('\n') != src.count('\n'):
            moved += 1
            m = linemap(src, new)
            maps[rel] = {k: v for k, v in m.items() if k != v}
        if not plan:
            open(path, 'wb').write(new.encode('utf-8'))
    for k, n in total.most_common():
        print(f'{n:6}  {k}')
    print(f'{changed} files {"to change" if plan else "changed"}; {moved} with lines moved')
    if not plan:
        os.makedirs(os.path.join(ROOT, 'runtime', 'v56'), exist_ok=True)
        json.dump(maps, open(os.path.join(ROOT, 'runtime', 'v56', 'linemap.json'), 'w'), indent=0)


if __name__ == '__main__':
    main()
