"""Haro v0.46, stzlib's findings on haro.exe (HARO-KEYEDRELEASE-01, HARO-ARITY-RECEIVER-01, HARO-OBJECT2POINTER-01): every case of v46/fixtures.json on haro and on its checked build, each run in a
fresh folder of its own (the zip cases write files). A case passes when both builds print exactly the bytes the fixture says, exit as it
says (0 unless it names another), and print the same bytes as each other (D41).

  python spike/v46/finding_court.py              haro and the checked build, as paths.py finds them
  python spike/v46/finding_court.py --vm X.exe   one build only (the plants)
  python spike/v46/finding_court.py --ring R.exe Ring 1.27, the subject the .ring cases were read off (never a judge: it prints, it decides nothing)
  python spike/v46/finding_court.py --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
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

# K23 (HARO-PIPEWRITE-01): a `pipe` case runs its program into a pipe Git Bash makes -- `"$0" "$1" | cat` -- since the defect showed
# there, and a pipe Python or cmd.exe makes carried every line whole. On a machine without that bash the case is NOT RUN, named.
GIT_BASH = r'C:\Git\usr\bin\bash.exe'


def run(exe, case):
    src = os.path.join(HERE, case['file'])
    verb = ['check'] if case.get('kind') == 'check' else []
    with tempfile.TemporaryDirectory() as td:
        shutil.copy(src, td)
        env = dict(os.environ)
        env['HARO_NOCACHE'] = '1'
        cmd = [exe] + verb + [os.path.basename(src)]
        if case.get('pipe'):
            cmd = [GIT_BASH, '-c', '"$0" "$1" | cat', exe.replace(chr(92), '/'), os.path.basename(src)]
        try:
            r = subprocess.run(cmd, capture_output=True, env=env, timeout=60, cwd=td)
        except subprocess.TimeoutExpired:
            return 'TIMEOUT', -1
        return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if RING:
        for c in doc['cases']:
            if not c['file'].endswith('.ring') or c['kind'] != 'run':
                continue
            o, rc = run(RING, c)
            print(f'  {"same" if o == c["stdout"] else "DIFFERS"} {c["id"]} on Ring 1.27 (exit {rc}): {o!r}')
        return 0
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed, not_run = [], []
    for c in doc['cases']:
        if c.get('pipe') and not os.path.exists(GIT_BASH):
            not_run.append(c['id'])
            print(f'  NOT RUN {c["id"]} [{c["line"]}] {c["why"]}: Git Bash is not at {GIT_BASH}, and the pipe it makes is the case')
            continue
        got = [run(exe, c) for _, exe in builds]
        if c['kind'] == 'check':
            # a `haro check` case: the report must hold (has) or lack (not) a rule name; the plant asks the opposite of K03
            needle, must_have = (c['not'], False) if 'not' in c else (c['has'], True)
            if PLANT and c['id'] == 'K03':
                must_have = True
            want = ('must hold ' if must_have else 'must not hold ') + needle
            bad = [f'{label}: {o[-300:]!r}' for (label, _), (o, rc) in zip(builds, got) if (needle in o) != must_have]
            got = [(o if (needle in o) == must_have else 'x', rc) for o, rc in got]
        else:
            want = c['stdout'] + ('doctored\n' if PLANT and c['id'] == 'K01' else '')
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
    n = len(doc['cases']) - len(not_run)
    print(f'FINDING COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}' + (f'; failed: {", ".join(failed)}' if failed else '')
          + (f'; NOT RUN: {", ".join(not_run)}' if not_run else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
