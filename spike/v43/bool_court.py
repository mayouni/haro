"""Haro v0.43, a real boolean and no coercion (D55 T1, T3): every case of v43/fixtures.json on haro and on its checked build. A `run` case runs the program, a `fmt` case runs
`haro fmt` on it. A case passes when both builds print exactly the bytes the fixture says, exit as it says (0 unless it names another), and print the same bytes as each other (D41).

  python spike/v43/bool_court.py              haro and the checked build, as paths.py finds them
  python spike/v43/bool_court.py --vm X.exe   one build only (the plants)
  python spike/v43/bool_court.py --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
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


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        want = c['stdout'] + ('doctored\n' if PLANT and c["id"] == "B04" else '')
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
    n = len(doc['cases'])
    print(f'BOOLEAN COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
