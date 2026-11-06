"""Haro v0.39, D52 rung (4): every case of v39/fixtures.json on haro and on its checked build. A `check` case runs `haro check <file> <args>`.
A case passes when both builds print the pinned lines exactly, exit 0, and print the same bytes as each other in full (D41).

The pinned lines are every line of the report but the detail paragraph under a finding -- the prose that explains it, which may be reworded:
the file line, each finding's `row:col  severity  rule` line and its message line, the blank lines, the counts and the closing lines.

  python spike/v39/rule_court.py              haro and the checked build, as paths.py finds them
  python spike/v39/rule_court.py --vm X.exe   one build only (the plants)
  python spike/v39/rule_court.py --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths

FINDING = re.compile(r'^  \d+:\d+  ')


def pinned(text):
    """every line but a finding's detail paragraph: after a finding's line and its message, the 10-space lines that follow"""
    out, lines, i = [], text.split('\n'), 0
    while i < len(lines):
        out.append(lines[i])
        if FINDING.match(lines[i]) and i + 1 < len(lines):
            out.append(lines[i + 1])
            i += 2
            while i < len(lines) and lines[i].startswith(' ' * 10):
                i += 1
            continue
        i += 1
    return '\n'.join(out)


def run(exe, path, args):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([exe, 'check', os.path.basename(path)] + args, capture_output=True, env=env, timeout=60, cwd=os.path.dirname(path))
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', -1
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        want = c['stdout'] + ('doctored\n' if PLANT and c['id'] == 'L01' else '')
        path = os.path.join(HERE, c['file'])
        got = [run(exe, path, c['args']) for _, exe in builds]
        bad = [f'{label}: {pinned(o)!r} (exit {rc})' for (label, _), (o, rc) in zip(builds, got) if pinned(o) != want or rc != 0]
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
    n = len(doc['cases'])
    print(f'RULE COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
