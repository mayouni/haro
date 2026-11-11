"""v0.56: a case whose file gained an `end` line (study/v56/defends.py) names lines that moved. Each expected line number is mapped through
the file's own line map (runtime/v56/linemap.json, written by the migration); the mapped expectation is written only when it is exactly
what the build prints, so nothing is accepted that the map does not explain.

  python study/v56/remap.py spike/v42 N05 N06 ...      the cases of one rung's fixtures.json
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAP = json.load(open(os.path.join(ROOT, 'runtime', 'v56', 'linemap.json')))
PATTERNS = [r'([Ll]ine )(\d+)', r'(?m)^(\s+)(\d+)(?=:\d+ )', r'(?m)^()(\d+)(?=\n)']


def remap(text, m):
    """each number mapped once: every pattern's matches are found on the text as it was"""
    spans = []
    for pat in PATTERNS:
        for g in re.finditer(pat, text):
            spans.append((g.start(2), g.end(2)))
    out, at = [], 0
    for s, e in sorted(set(spans)):
        out.append(text[at:s])
        out.append(str(m.get(text[s:e], int(text[s:e]))))
        at = e
    out.append(text[at:])
    return ''.join(out)


def main():
    rung = sys.argv[1]
    ids = set(sys.argv[2:])
    fx = os.path.join(ROOT, rung, 'fixtures.json')
    doc = json.load(open(fx, encoding='utf-8'))
    exe = os.environ.get('HARO_VM')
    changed = []
    for c in doc['cases']:
        if c['id'] not in ids:
            continue
        rel = os.path.join(rung, c['file']).replace(os.sep, '/')
        m = MAP.get(rel)
        if not m:
            print(c['id'], 'no line map for', rel)
            continue
        want = remap(c['stdout'], m)
        path = os.path.join(ROOT, rel)
        kind = c.get('kind', 'run')
        args = [exe] + (['check'] if kind == 'check' else []) + [os.path.basename(path)]
        r = subprocess.run(args, capture_output=True, cwd=os.path.dirname(path), env=dict(os.environ, HARO_NOCACHE='1'))
        got = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
        if got == want:
            c['stdout'] = want
            changed.append(c['id'])
            print(c['id'], 'mapped: the build prints the mapped lines')
        else:
            print(c['id'], 'NOT explained by the map:')
            print('   want', repr(want[:300]))
            print('   got ', repr(got[:300]))
    if changed:
        json.dump(doc, open(fx, 'w', encoding='utf-8', newline='\n'), indent=1)
    print('changed:', ' '.join(changed) or 'none')


if __name__ == '__main__':
    main()
