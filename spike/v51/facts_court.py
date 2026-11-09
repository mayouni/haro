"""Haro v0.51, `haro check --facts` (HARO-FACTS-01): every case of v51/fixtures.json on haro and on its checked build, each in a fresh copy
of its folder. A case passes when each build exits 0 and prints JSON, every assert holds on it, and the builds print the same bytes (D41).
@COMMIT reads the repository: the last commit that touched vm/, "+uncommitted" after it when vm/ holds changes now -- so run the court on
builds made from the tree as it is.

  python spike/v51/facts_court.py              haro and the checked build, as paths.py finds them
  python spike/v51/facts_court.py --vm X.exe   one build only (the plants)
  python spike/v51/facts_court.py --plant      the guard's own plant: one assert doctored, so the court must fail
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths


def commit():
    h = subprocess.run(['git', 'log', '-1', '--format=%H', '--', 'vm'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no', '--', 'vm'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return h + ('+uncommitted' if dirty else '')


def fn(d, name):
    for x in d['functions']:
        full = (x['class'] + '.' + x['name']) if x['class'] else x['name']
        if full == name:
            return x
    raise KeyError(name)


def run(exe, case, flag_first):
    src = os.path.join(HERE, case['folder'])
    with tempfile.TemporaryDirectory() as td:
        for f in os.listdir(src):
            shutil.copy(os.path.join(src, f), td)
        env = dict(os.environ, HARO_NOCACHE='1')
        args = ['check', '--facts', case['run']] if flag_first else ['check', case['run'], '--facts']
        r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=120, cwd=td)
        return r.stdout, r.returncode, r.stderr.decode('utf-8', 'replace')


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    builds = [('vm', VM)] if VM else list(zip(('haro', 'checked'), paths.need_bins()))
    want_commit = commit()
    failed = []
    for c in doc['cases']:
        bad = []
        outs = []
        for label, exe in builds:
            out, rc, err = run(exe, c, c['flag_first'])
            outs.append(out)
            if rc != 0:
                bad.append(f'{label}: exit {rc} {err[-300:]!r}')
                continue
            if c['same_as_flag_last']:
                last, _, _ = run(exe, c, False)
                if last != out:
                    bad.append(f'{label}: the flag first and the flag last print different bytes')
            try:
                d = json.loads(out.decode('utf-8'))
            except Exception as e:
                bad.append(f'{label}: not JSON ({e}): {out[:300]!r}')
                continue
            for i, (expr, want) in enumerate(c['asserts']):
                if want == '@COMMIT':
                    want = want_commit
                elif isinstance(want, str) and want.startswith('@SHA:'):
                    want = hashlib.sha256(open(os.path.join(HERE, c['folder'], want[5:]), 'rb').read()).hexdigest()
                if PLANT and c['id'] == 'X03' and i == 0:
                    want = 'doctored'
                try:
                    got = eval(expr, {'d': d, 'fn': fn, 'chr': chr, 'sorted': sorted, 'len': len, 'all': all})
                except Exception as e:
                    got = f'<{type(e).__name__}: {e}>'
                if isinstance(got, tuple):
                    got = list(got)
                if isinstance(got, list):
                    got = [list(x) if isinstance(x, tuple) else x for x in got]
                if got != want:
                    bad.append(f'{label}: {expr} is {got!r}, want {want!r}')
        if len(builds) > 1 and len(set(outs)) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
            print(f'  FAIL {c["id"]} [{c["line"]}] {c["why"]}')
            for b in bad:
                print(f'       {b[:700]}')
        else:
            print(f'  ok   {c["id"]} [{c["line"]}] {c["why"]}')
    n = len(doc['cases'])
    print(f'FACTS COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
