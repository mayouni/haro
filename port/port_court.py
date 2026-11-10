"""haroport's court (HARO-PORTTOOL-01): every case of port/fixtures.json. Each case's tree is copied to a fresh folder; `plan --json` is
read as `plan`, and whether it wrote any file as `plan_wrote`; `apply --out` is read as `applied` (each written file's text by its name);
for a case that asks, the ported tree and the original are each run on haro (`ran`, `ran_ring`). Every assert must hold.

  python port/port_court.py              haro as paths.py finds it, for the cases that run a tree
  python port/port_court.py --plant      the guard's own plant: one assert doctored, so the court must fail
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
TOOL = os.path.join(HERE, 'haroport.py')
sys.argv = [sys.argv[0]]
import paths


def listing(d):
    return sorted(os.path.relpath(os.path.join(a, f), d) for a, _, fs in os.walk(d) for f in fs)


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    haro, _ = paths.need_bins()
    env = dict(os.environ, HARO_NOCACHE='1')
    failed = []
    for c in doc['cases']:
        bad = []
        with tempfile.TemporaryDirectory() as td:
            src = os.path.join(td, 'tree')
            shutil.copytree(os.path.join(HERE, c['folder']), src)
            before = listing(src)
            p = subprocess.run([sys.executable, TOOL, 'plan', src, '--json'], capture_output=True)
            plan_wrote = listing(src) != before
            try:
                plan = json.loads(p.stdout.decode('utf-8'))
            except Exception:
                plan = None
                bad.append(f'plan is no JSON: {p.stdout[-300:]!r} {p.stderr[-300:]!r}')
            out = os.path.join(td, 'out')
            q = subprocess.run([sys.executable, TOOL, 'apply', src, '--out', out], capture_output=True)
            if q.returncode != 0:
                bad.append(f'apply exited {q.returncode}: {q.stderr[-300:]!r}')
            applied = {}
            if os.path.isdir(out):
                for rel in listing(out):
                    applied[rel.replace(os.sep, '/')] = open(os.path.join(out, rel), encoding='utf-8').read()
            ran, ran_ring = {}, {}
            if any('ran' in e for e, _ in c['asserts']):
                for rel in applied:
                    if rel == 'main.haro':
                        r = subprocess.run([haro, rel], capture_output=True, cwd=out, env=env)
                        ran[rel] = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
                r = subprocess.run([haro, 'main.ring'], capture_output=True, cwd=src, env=env)
                ran_ring['main.ring'] = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
            for i, (expr, want) in enumerate(c['asserts']):
                if PLANT and c['id'] == 'H01' and i == 0:
                    want = 'doctored'
                try:
                    got = eval(expr, {'plan': plan, 'plan_wrote': plan_wrote, 'applied': applied, 'ran': ran, 'ran_ring': ran_ring,
                                      'sorted': sorted, 'any': any})
                except Exception as e:
                    got = f'<{type(e).__name__}: {e}>'
                if got != want:
                    bad.append(f'{expr} is {got!r}, want {want!r}')
        if bad:
            failed.append(c['id'])
            print(f'  FAIL {c["id"]} [{c["line"]}] {c["why"]}')
            for b in bad:
                print(f'       {b[:600]}')
        else:
            print(f'  ok   {c["id"]} [{c["line"]}] {c["why"]}')
    n = len(doc['cases'])
    print(f'PORT COURT {n - len(failed)} of {n} cases' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
