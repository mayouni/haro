"""Haro v0.41, HARO-SURFACE-01: every case of v41/fixtures.json on haro and on its checked build. A `run` case runs the program, a `fmt` case runs
`haro fmt` on it. A case passes when both builds print exactly the bytes the fixture says, exit as it says (0 unless it names another), and print the same bytes as each other (D41).

  python spike/v41/surface_court.py              haro and the checked build, as paths.py finds them
  python spike/v41/surface_court.py --vm X.exe   one build only (the plants)
  python spike/v41/surface_court.py --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths


def run(exe, path, kind='run'):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([exe] + (['fmt'] if kind == 'fmt' else []) + [os.path.basename(path)], capture_output=True, env=env, timeout=30, cwd=os.path.dirname(path))
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', -1
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def keyword_lists():
    """S2's list: the words the lift lowers in a .ring file (lift.zig, ring_keywords) are exactly the grammar's keyword() words -- a keyword
    the grammar gains and the list lacks would be read as a name in a .ring file, and the reverse would lower a name"""
    import re
    g = set(re.findall(r'keyword\("([a-z_]+)"\)', open(os.path.join(ROOT, 'vm', 'vendor', 'tree-sitter-ring', 'grammar.js'), encoding='utf-8').read()))
    src = open(os.path.join(ROOT, 'vm', 'src', 'lift.zig'), encoding='utf-8').read()
    m = re.search(r'ring_keywords = \[_\]\[\]const u8\{(.*?)\};', src, re.S)
    l = set(re.findall(r'"([a-z_]+)"', m.group(1))) if m else set()
    if g == l:
        print(f'  ok   the lift lowers exactly the grammar\'s {len(g)} keywords in a .ring file')
        return 0
    print(f'  FAIL the lift\'s ring_keywords and the grammar\'s keyword() differ: grammar only {sorted(g - l)[:8]}, lift only {sorted(l - g)[:8]}')
    return 1


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        want = c['stdout'] + ('doctored\n' if PLANT and c['id'] == 'S01' else '')
        path = os.path.join(HERE, c['file'])
        got = [run(exe, path, c['kind']) for _, exe in builds]
        bad = [f'{label}: {o!r} (exit {rc})' for (label, _), (o, rc) in zip(builds, got) if o != want or rc != c.get('exit', 0)]
        if len({o for o, _ in got}) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
            print(f'  FAIL {c["id"]} [{c["line"]}] {c["why"]}')
            print(f'       want {want!r}')
            for b in bad:
                print(f'       {b}')
        else:
            print(f'  ok   {c["id"]} [{c["line"]}] {c["why"]}')
    if keyword_lists():
        failed.append('KEYWORDS')
    n = len(doc['cases'])
    print(f'SURFACE COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
