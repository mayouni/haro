"""Haro v0.44, the ported defects (HARO-PORTED-FINDINGS-01): every case of v44/fixtures.json on haro and on its checked build, each run in a
fresh folder of its own (the zip cases write files). A case passes when both builds print exactly the bytes the fixture says, exit as it
says (0 unless it names another), and print the same bytes as each other (D41).

  python spike/v44/ported_court.py              haro and the checked build, as paths.py finds them
  python spike/v44/ported_court.py --vm X.exe   one build only (the plants)
  python spike/v44/ported_court.py --ring R.exe Ring 1.27, the subject the .ring cases were read off (never a judge: it prints, it decides nothing)
  python spike/v44/ported_court.py --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
RING = os.path.abspath(sys.argv[sys.argv.index('--ring') + 1]) if '--ring' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths


def run(exe, case):
    src = os.path.join(HERE, case['file'])
    with tempfile.TemporaryDirectory() as td:
        shutil.copy(src, td)
        env = dict(os.environ)
        env['HARO_NOCACHE'] = '1'
        try:
            r = subprocess.run([exe, os.path.basename(src)], capture_output=True, env=env, timeout=30, cwd=td)
        except subprocess.TimeoutExpired:
            return 'TIMEOUT', -1
        return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if RING:
        for c in doc['cases']:
            if not c['file'].endswith('.ring'):
                continue
            o, rc = run(RING, c)
            print(f'  {"same" if o == c["stdout"] else "DIFFERS"} {c["id"]} on Ring 1.27 (exit {rc}): {o!r}')
        return 0
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        want = c['stdout'] + ('doctored\n' if PLANT and c['id'] == 'Q05' else '')
        got = [run(exe, c) for _, exe in builds]
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
    print(f'PORTED COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
