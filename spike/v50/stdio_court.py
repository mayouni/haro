"""Haro v0.50, a program that serves another (HARO-STDIOFLUSH-01): every case of v50/fixtures.json on haro and on its checked build, each
in a fresh folder of its own. A `run` case is given its input whole and must print exactly the fixture's bytes; a `dialog` case is driven
step by step on pipes -- `expect` waits at most WAIT seconds for the program's output so far to end with the text, `send` writes a line,
`touch` makes a file, `close` ends the input -- and its whole output must then be the fixture's. Both builds must print the same bytes (D41).

  python spike/v50/stdio_court.py              haro and the checked build, as paths.py finds them
  python spike/v50/stdio_court.py --vm X.exe   one build only (the plants)
  python spike/v50/stdio_court.py --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
"""
import json, os, shutil, subprocess, sys, tempfile, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths

WAIT = 10.0


def run(exe, case):
    """(stdout, exit code, why it stopped short or None)"""
    src = os.path.join(HERE, case['file'])
    with tempfile.TemporaryDirectory() as td:
        shutil.copy(src, td)
        env = dict(os.environ)
        env['HARO_NOCACHE'] = '1'
        cmd = [exe, os.path.basename(src)]
        if case['kind'] == 'run':
            try:
                r = subprocess.run(cmd, input=case['input'].encode('utf-8'), capture_output=True, env=env, timeout=60, cwd=td)
            except subprocess.TimeoutExpired:
                return '', -1, 'TIMEOUT'
            return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode, None
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, cwd=td, bufsize=0)
        got = bytearray()
        lock = threading.Lock()

        def pump():
            while True:
                b = p.stdout.read(1)
                if not b:
                    return
                with lock:
                    got.extend(b)

        th = threading.Thread(target=pump, daemon=True)
        th.start()

        def text():
            with lock:
                return bytes(got).decode('utf-8', 'replace').replace('\r\n', '\n')

        short = None
        for step in case['steps']:
            if step[0] == 'expect':
                end = time.monotonic() + WAIT
                while not text().endswith(step[1]) and time.monotonic() < end:
                    time.sleep(0.01)
                if not text().endswith(step[1]):
                    short = f'waited {WAIT:.0f} s for {step[1]!r}; had {text()[-200:]!r}'
                    break
            elif step[0] == 'send':
                p.stdin.write(step[1].encode('utf-8'))
                p.stdin.flush()
            elif step[0] == 'touch':
                open(os.path.join(td, step[1]), 'w').close()
            elif step[0] == 'close':
                p.stdin.close()
        if short:
            p.kill()
            p.wait()
            th.join(5)
            return text(), p.returncode, short
        try:
            rc = p.wait(timeout=60)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            return text(), -1, 'TIMEOUT after its last step'
        th.join(5)
        return text(), rc, None


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        got = [run(exe, c) for _, exe in builds]
        want = c['stdout'] + ('doctored\n' if PLANT and c['id'] == 'D01' else '')
        bad = [f'{label}: {short or ""} {o!r} (exit {rc})' for (label, _), (o, rc, short) in zip(builds, got)
               if short or o != want or rc != c.get('exit', 0)]
        if len({o for o, _, _ in got}) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
            print(f'  FAIL {c["id"]} [{c["line"]}] {c["why"]}')
            print(f'       want {want[:300]!r}')
            for b in bad:
                print(f'       {b[:600]}')
        else:
            print(f'  ok   {c["id"]} [{c["line"]}] {c["why"]}')
    n = len(doc['cases'])
    print(f'STDIO COURT {n - len(failed)} of {n} cases on {" and ".join(l for l, _ in builds)}'
          + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
