"""census_comments.py -- how much of what a Ring file SAYS lives in its comments.   python census_comments.py

A code graph that drops comments as layout would drop promises. Two comment conventions of the estate carry meaning:
  `#-->`   a narrated guard's PROMISE: the run of the file checks it (stzlib's narrated tests, ringpp's clock)
  `<R:`    a Refine refinement-point tag: stzRefinableCode reads it out of a comment (CHARTER section 6)
and the intent clause of a method (`#--` / `#-` lines are NOT counted: only what a tool reads is counted here).
Read-only. One scan of each tree, one at a time.
"""
import os, re, sys, json

ROOTS = {
    'softanza base': r'D:\GitHub\stzlib\libraries\stzlib\base',
    'softanza core': r'D:\GitHub\stzlib\libraries\stzlib\core',
    'ringpp haro spike': r'D:\GitHub\ringpp\haro\spike',
    'ringpp bench+tests': None,
}
COMMENT = re.compile(r'^\s*(#|//)')
PROMISE = re.compile(r'#-->')
TAG = re.compile(r'<R:[A-Z]+')


def scan(files):
    n = dict(files=0, lines=0, comment_lines=0, promise_lines=0, tag_lines=0, bytes=0, comment_bytes=0, promise_files=0)
    for p in files:
        try:
            data = open(p, 'rb').read().decode('latin-1')
        except OSError:
            continue
        n['files'] += 1
        n['bytes'] += len(data)
        had = False
        for line in data.split('\n'):
            n['lines'] += 1
            if COMMENT.match(line):
                n['comment_lines'] += 1
                n['comment_bytes'] += len(line) + 1
            if PROMISE.search(line):
                n['promise_lines'] += 1
                had = True
            if TAG.search(line):
                n['tag_lines'] += 1
        n['promise_files'] += had
    return n


def ring_files(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.ring'):
                yield os.path.join(d, f)


if __name__ == '__main__':
    out = {}
    for name, root in ROOTS.items():
        if root is None:
            base = r'D:\GitHub\ringpp'
            files = [os.path.join(base, d, f) for d in ('bench', 'tests') for f in os.listdir(os.path.join(base, d)) if f.endswith('.ring')]
        elif os.path.isdir(root):
            files = list(ring_files(root))
        else:
            print(f'  {name}: not there ({root})')
            continue
        r = scan(files)
        out[name] = r
        print(f'  {name:20s} {r["files"]:5d} files {r["lines"]:8d} lines | comment lines {r["comment_lines"]:7d} '
              f'({100 * r["comment_lines"] / max(r["lines"], 1):4.1f}% of lines, {100 * r["comment_bytes"] / max(r["bytes"], 1):4.1f}% of bytes) | '
              f'#--> promises {r["promise_lines"]:6d} in {r["promise_files"]:4d} files | <R: tags {r["tag_lines"]:4d}')
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'census_comments.json'), 'w'), indent=1)
