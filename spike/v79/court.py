"""Haro v0.79, where `haro check` and haro.exe disagree, and the reply's head: every case of v79/fixtures.json on haro and on its
checked build. A case passes when, on both builds:

  check   `haro check <file>` in a copy of the case's folder: each finding the fixture names is there, an error, at its line and
          under its rule; no rule or word the fixture says `never` is printed; each word of `says` is printed. Where the fixture
          has `run`, the file is also run in the copy: its bytes (`stdout` exactly, or each of `has`, and not `never`) and its
          exit code
          A `check` or a run that crashes (exit 3, a segmentation fault, a panic) fails its case whatever it printed
  http    the program is run with a free port of 127.0.0.1 written where `{PORT}` stands; the court sends one GET and reads the
          reply whole: its bytes are the fixture's (nothing at all, where the fixture's reply is empty), `never` is not in them,
          and the program prints the fixture's bytes (or `has`, and not `never_out`) and ends with its exit code
  graph   `haro graph <file>` in a copy: the fixture's bytes
  scope   a copy of cases/l with a cache of its own; `haro prefix` where the fixture names a library; `check` of the named file
          with the fixture's arguments and HARO_PATH=1: each [file, line, rule] printed under that file's heading, `never` and
          `says` as for check, and the path line the fixture's where it names one
  D41     the two builds answer the same

  python spike/v79/court.py                haro and the checked build, as paths.py finds them
  python spike/v79/court.py --vm X.exe      one build only (the plants)
  python spike/v79/court.py --only H02      one case alone
  python spike/v79/court.py --plant         the guard's own plant: one fixture's reply doctored, so the court must fail
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths

WORK = os.path.join(ROOT, 'runtime', 'v79', 'court')
FINDING = re.compile(r'^\s*(\d+):(\d+)\s+(error|warn|perf|note)\s+(\S+)', re.M)


def env_of(exe):
    env = dict(os.environ)
    for k in ('HARO_NOCACHE', 'HARO_NOIMAGE', 'HARO_PATH', 'HARO_IMAGE', 'HARO_CACHE'):
        env.pop(k, None)
    env['HARO_NOCACHE'] = '1'
    env['HARO_HOME'] = SPIKE
    env['PATH'] = os.path.dirname(exe) + os.pathsep + env.get('PATH', '')
    return env


def sh(exe, args, cwd, timeout=90):
    try:
        r = subprocess.run([exe] + args, capture_output=True, env=env_of(exe), timeout=timeout, cwd=cwd)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', '', -1
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.stderr.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def copy_of(c, label):
    sub = os.path.dirname(c['file'])
    dst = os.path.join(WORK, label, c['id'])
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(os.path.join(HERE, 'cases', sub), dst)
    return dst, os.path.basename(c['file'])


def bytes_bad(want, out, rc):
    bad = []
    if 'stdout' in want and out != want['stdout']:
        bad.append(f'prints {out[:300]!r}, not {want["stdout"]!r}')
    for h in want.get('has', []):
        if h not in out:
            bad.append(f'does not print {h!r}: {out.strip()[:240]!r}')
    if want.get('never') and want['never'] in out:
        bad.append(f'prints {want["never"]!r}')
    if rc != want['exit']:
        bad.append(f'ends with {rc}, not {want["exit"]}')
    return bad


def crashed(who, text, rc):
    """a crash is never a verdict: B05 passed on v0.78 because `check` died on Add(x) before it printed anything"""
    if rc == 3 or 'Segmentation fault' in text or 'panic:' in text:
        return [f'{who} CRASHED (exit {rc}): {text.strip()[:160]!r}']
    return []


def check(c, label, exe):
    d, f = copy_of(c, label)
    out, err, rc = sh(exe, ['check', f], d)
    text = out + err
    found = [(int(m.group(1)), m.group(3), m.group(4)) for m in FINDING.finditer(text)]
    bad = crashed('`check`', text, rc)
    for line, rule in c.get('rules', []):
        if (line, 'error', rule) not in found:
            bad.append(f'`check` names no error {rule} at line {line}; it names {found[:8]}')
    for w in c.get('never', []):
        if w in text:
            bad.append(f'`check` prints {w!r}: {[x for x in found if w in x[2]][:4] or text.strip()[:200]!r}')
    for w in c.get('says', []):
        if w not in text:
            bad.append(f'`check` does not say {w!r}')
    said = repr(sorted(found)) + '|' + '|'.join(w for w in c.get('says', []) if w in text)
    if 'run' in c:
        rout, rerr, rrc = sh(exe, [f], d)
        bad += crashed('the run', rout + rerr, rrc)
        bad += [f'the run {b}' for b in bytes_bad(c['run'], rout + rerr if 'has' in c['run'] else rout, rrc)]
        said += f'|{rout}|{rrc}'
    return bad, said


def scope(c, label, exe):
    """the L family: a copy of cases/l, with a cache of the case's own; `haro prefix` first where the case says; then `check` of
    the named file from its own folder, with HARO_PATH=1. A rule is [file, line, rule]: the finding is printed under that file's
    heading. The path line is the fixture's where it names one."""
    dst = os.path.join(WORK, label, c['id'])
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(os.path.join(HERE, 'cases', 'l'), dst)
    sub, f = os.path.split(c['file'][len('l/'):])
    d = os.path.join(dst, sub)
    cache = os.path.join(dst, '_cache')
    os.makedirs(cache)
    env = env_of(exe)
    env.pop('HARO_NOCACHE', None)
    env['HARO_CACHE'] = cache
    bad = []
    if c.get('prefix'):
        r = subprocess.run([exe, 'prefix', c['prefix']], cwd=d, env=env, capture_output=True, timeout=90)
        if r.returncode != 0:
            bad.append(f'`haro prefix` ends with {r.returncode}')
    env['HARO_PATH'] = '1'
    r = subprocess.run([exe, 'check', f] + c['args'], cwd=d, env=env, capture_output=True, timeout=90)
    out = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    err = r.stderr.decode('utf-8', 'replace').replace('\r\n', '\n')
    text = out + err
    bad += crashed('`check`', text, r.returncode)
    current, found = None, []
    for ln in text.split('\n'):
        if ln and not ln.startswith(' ') and ln.strip().endswith(('.haro', '.ring')):
            current = os.path.basename(ln.strip().replace('\\', '/'))
        m = FINDING.match(ln)
        if m:
            found.append((current, int(m.group(1)), m.group(3), m.group(4)))
    for fn, line, rule in c.get('rules', []):
        if (fn, line, 'error', rule) not in found:
            bad.append(f'`check` names no error {rule} at {fn}:{line}; it names {found[:8]}')
    for w in c.get('never', []):
        if w in text:
            bad.append(f'`check` prints {w!r}')
    for w in c.get('says', []):
        if w not in text:
            bad.append(f'`check` does not say {w!r}')
    paths_said = [ln for ln in err.split('\n') if ln.startswith('path:')]
    if c.get('path') and paths_said != [c['path']]:
        bad.append(f'the path line is {paths_said!r}, not {[c["path"]]!r}')
    if c.get('path_starts') and not (len(paths_said) == 1 and paths_said[0].startswith(c['path_starts'])):
        bad.append(f'the path line is {paths_said!r}, not one line beginning {c["path_starts"]!r}')
    return bad, repr(sorted(found, key=str)) + repr(paths_said)


def free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def http(c, label, exe):
    d, f = copy_of(c, label)
    port = free_port()
    p = os.path.join(d, f)
    src = open(p, encoding='utf-8').read().replace('{PORT}', str(port))
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(src)
    proc = subprocess.Popen([exe, f], cwd=d, env=env_of(exe), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    reply, bad = None, []
    t0 = time.time()
    while time.time() - t0 < 20 and reply is None:
        try:
            s = socket.create_connection(('127.0.0.1', port), timeout=2)
        except OSError:
            if proc.poll() is not None:
                break
            time.sleep(0.1)
            continue
        s.settimeout(20)
        s.sendall(b'GET / HTTP/1.1\r\nHost: court\r\n\r\n')
        got = b''
        try:
            while True:
                b = s.recv(65536)
                if not b:
                    break
                got += b
        except OSError:
            pass
        s.close()
        reply = got.decode('utf-8', 'replace')
    try:
        out, err = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        bad.append('the program did not end within 30 s of the reply')
    out = out.decode('utf-8', 'replace').replace('\r\n', '\n')
    err = err.decode('utf-8', 'replace').replace('\r\n', '\n')
    if reply is None:
        bad.append('no connection was taken within 20 s')
        reply = ''
    if reply != c['reply']:
        bad.append(f'the reply is {reply[:300]!r}, not {c["reply"]!r}')
    if c.get('never') and c['never'] in reply:
        bad.append(f'the reply carries {c["never"]!r}')
    want = {'exit': c['exit']}
    for k in ('stdout', 'has'):
        if k in c:
            want[k] = c[k]
    if c.get('never_out'):
        want['never'] = c['never_out']
    bad += [f'the program {b}' for b in bytes_bad(want, out + err if 'has' in c else out, proc.returncode)]
    return bad, f'{reply}|{out}|{proc.returncode}'


def graph(c, label, exe):
    d, f = copy_of(c, label)
    out, err, rc = sh(exe, ['graph', f], d)
    bad = [] if out == c['stdout'] else [f'`haro graph` prints {out[:400]!r}, not {c["stdout"]!r}']
    return bad, out


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    if ONLY:
        doc['cases'] = [c for c in doc['cases'] if c['id'] == ONLY]
    failed = []
    for c in doc['cases']:
        if PLANT and c['id'] == 'H01':
            c = json.loads(json.dumps(c))
            c['reply'] += 'doctored'
        judge = {'check': check, 'http': http, 'graph': graph, 'scope': scope}[c['kind']]
        res = [judge(c, label, exe) for label, exe in builds]
        bad = [f'{label}: {b}' for (label, _), (bs, _) in zip(builds, res) for b in bs]
        if len({o for _, o in res}) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
        print(f'  {"FAIL" if bad else "ok  "} {c["id"]} [{c["line"]}] {c["what"]}', flush=True)
        for b in bad:
            print(f'       {b}', flush=True)
    n = len(doc['cases'])
    print(f'V79 COURT {n - len(failed)} of {n} cases on ' + ' and '.join(label for label, _ in builds)
          + (f'; FAILED: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
