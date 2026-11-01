"""THE WEB COMPARISON: HaroServer serving Softanza, against the servers the mainstream languages ship with.

    python haro/serv/bench/webbench.py [--quick] [--conc=1,8] [--only=node,java]

Every server answers the same three paths with the same bytes -- /bench/hello (five bytes: the server alone),
/bench/text (a 180-word text upper-cased, counted, reversed: 1.8 KB), /bench/primes (the primes below 20,000 by a
sieve: the language computing) -- and every answer is checked BYTE FOR BYTE against the expected one before a
single timing is taken (this project's rule: no speed number for a wrong answer).

The servers, each with its language's own library and nothing downloaded:
    HaroServer + Softanza   haro/serv/host.ring on rnxc resident, the lab in its base, Softanza's library admitted
    HaroServer, plain Ring  the same server, the text answered with Ring++'s own builtins instead of Softanza
    Node.js                 node's http module                     Bun        Bun.serve
    Python                  http.server's ThreadingHTTPServer       Java       the JDK's com.sun.net.httpserver
The client is runtime/lab/loadgen.exe (loadgen.zig, built here when missing): one connection per request
(`Connection: close`, the one way HaroServer serves, so every server speaks the same protocol), N threads, the
best of three runs of three seconds after half a second of warm-up. bench/heartbeat.py's CPU reading is taken
first and written with the figures, since a throttled CPU makes every number here a different measurement.

Writes haro/serv/lab/results.json, which the lab's page shows (GET /lab/results), and a dated copy under
runtime/lab/.
"""
import json, os, re, socket, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LAB = os.path.join(ROOT, 'haro', 'serv', 'lab')
sys.path.insert(0, LAB)
import lab  # noqa: E402

LOADGEN = os.path.join(ROOT, 'runtime', 'lab', 'loadgen.exe')
QUICK = '--quick' in sys.argv
DUR, WARM, REPS = (1.0, 0.3, 1) if QUICK else (3.0, 0.5, 3)
# before a server is timed, each of its paths is loaded this long, unrecorded: Node, Bun and Java compile while
# they run, and a figure taken while they still interpret describes their start, not their speed
PRIME = 0.5 if QUICK else 2.0
CONC = [1, 8]
ONLY = None
for a in sys.argv[1:]:
    if a.startswith('--conc='):
        CONC = [int(x) for x in a.split('=', 1)[1].split(',')]
    if a.startswith('--only='):
        ONLY = set(a.split('=', 1)[1].split(','))

P = ' '.join(['the quick brown fox jumps over the lazy dog'] * 20)


def _primes(n=20000):
    s, c = [0] * n, 0
    for i in range(2, n):
        if s[i] == 0:
            c += 1
            for j in range(i * i, n, i):
                s[j] = 1
    return str(c)


EXPECT = {
    'hello': b'hello',
    'text': (P.upper() + '\n' + str(len(P.split(' '))) + '\n' + ' '.join(reversed(P.split(' ')))).encode(),
    'primes': _primes().encode(),
}
WORKLOADS = [
    {'id': 'hello', 'label': 'hello', 'desc': 'five bytes: the server and its request handling alone'},
    {'id': 'text', 'label': 'text', 'desc': 'a 180-word text upper-cased, its words counted and reversed: 1.8 KB'},
    {'id': 'primes', 'label': 'primes', 'desc': 'the primes below 20,000 counted by a sieve: the language computing'},
]
SERVERS = [
    {'id': 'haroserver', 'label': 'HaroServer + Softanza', 'ours': True,
     'paths': {'hello': '/bench/hello', 'text': '/bench/text', 'primes': '/bench/primes'},
     'arch': 'one Ring++ program (rnxc resident) on one thread, one request at a time; the text through Softanza'},
    {'id': 'haroring', 'label': 'HaroServer, plain Ring', 'ours': True, 'paths': {'text': '/bench/textring'},
     'arch': 'the same server and process; the text with Ring++\'s own string builtins, without Softanza'},
    {'id': 'node', 'label': 'Node.js', 'cmd': ['node', 'node_server.mjs'],
     'paths': {'hello': '/bench/hello', 'text': '/bench/text', 'primes': '/bench/primes'},
     'arch': 'node\'s http module: one process, one event loop; JavaScript compiled at run time (V8)'},
    {'id': 'bun', 'label': 'Bun', 'cmd': ['bun', 'bun_server.ts'],
     'paths': {'hello': '/bench/hello', 'text': '/bench/text', 'primes': '/bench/primes'},
     'arch': 'Bun.serve: one process, one event loop; JavaScript compiled at run time (JavaScriptCore)'},
    {'id': 'python', 'label': 'Python', 'cmd': [sys.executable, 'py_server.py'],
     'paths': {'hello': '/bench/hello', 'text': '/bench/text', 'primes': '/bench/primes'},
     'arch': 'the standard library\'s ThreadingHTTPServer: a thread a connection, one interpreter lock (CPython)'},
    # Java 17 on Windows opens its selector's pipe as a Unix-domain socket in the temp folder, and fails when that
    # path holds spaces ("Unable to establish loopback connection"): the socket goes under runtime/ instead
    {'id': 'java', 'label': 'Java', 'cmd': ['java', '-Djdk.net.unixdomain.tmpdir=' + os.path.join(ROOT, 'runtime', 'lab', 'jtmp').replace(os.sep, '/'), 'JavaServer.java'],
     'paths': {'hello': '/bench/hello', 'text': '/bench/text', 'primes': '/bench/primes'},
     'arch': 'the JDK\'s com.sun.net.httpserver: a pool of one thread a core; compiled at run time (HotSpot)'},
]


def version(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return ((r.stdout or '') + (r.stderr or '')).strip().split('\n')[0]
    except OSError:
        return 'not found'


def cpu_name():
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DESCRIPTION\System\CentralProcessor\0')
        return winreg.QueryValueEx(k, 'ProcessorNameString')[0].strip()
    except Exception:
        import platform
        return platform.processor()


def cpu_speed():
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'bench', 'heartbeat.py')], capture_output=True, text=True)
    m = re.search(r'cpu (\d+)%', r.stdout + r.stderr)
    return int(m.group(1)) if m else -1


def ensure_loadgen():
    src = os.path.join(HERE, 'loadgen.zig')
    if os.path.exists(LOADGEN) and os.path.getmtime(LOADGEN) >= os.path.getmtime(src):
        return
    os.makedirs(os.path.dirname(LOADGEN), exist_ok=True)
    r = subprocess.run(['zig', 'build-exe', '-OReleaseFast', '-lc', src, '-femit-bin=' + LOADGEN], cwd=HERE,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('webbench: loadgen did not build\n' + r.stderr)


def get(port, path):
    try:
        return lab.req(port, 'GET', path, timeout=10)
    except OSError:
        return 0, b''


def wait_up(port, proc, secs=60):
    t = time.time()
    while time.time() - t < secs:
        if proc.poll() is not None:
            return False
        if get(port, '/bench/hello')[0] == 200:
            return True
        time.sleep(0.1)
    return False


def load(port, path, c, secs=None):
    secs = secs or DUR
    r = subprocess.run([LOADGEN, str(port), path, str(c), str(secs), str(WARM)], capture_output=True, text=True,
                       timeout=secs + WARM + 120)
    if r.returncode != 0:
        raise SystemExit('webbench: loadgen failed: ' + r.stderr[-500:])
    return json.loads(r.stdout)


def main():
    ensure_loadgen()
    os.makedirs(os.path.join(ROOT, 'runtime', 'lab', 'jtmp'), exist_ok=True)
    speed = cpu_speed()
    print('webbench: CPU at %d%% of its rated speed%s' % (speed, '' if speed >= 100 else ' -- THROTTLED: these numbers describe a slowed machine'))
    rows, identical, versions = [], {w['id']: True for w in WORKLOADS}, {}
    haro = None
    try:
        for s in SERVERS:
            if ONLY and s['id'] not in ONLY:
                continue
            port, proc = None, None
            if s['id'] in ('haroserver', 'haroring'):
                if haro is None:
                    hp = lab.free_port()
                    hproc = lab.start(hp, wait_softanza=True, say=lambda m: print('   ' + m))
                    haro = (hp, hproc)
                port = haro[0]
                git = subprocess.run(['git', '-C', ROOT, 'log', '-1', '--format=%h %cs'], capture_output=True, text=True).stdout.strip()
                dirty = subprocess.run(['git', '-C', ROOT, 'diff', '--quiet', '--', 'src'], capture_output=True).returncode != 0
                pkg = open(os.path.join(lab.STZ_TREE, '..', '..', 'PACKAGE.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(lab.STZ_TREE, '..', '..', 'PACKAGE.txt')) else ''
                stz = (re.search(r'Softanza\s+(stzlib \S+)', pkg) or [None, 'Softanza'])[1]
                s['version'] = 'rnxc %s%s, %s' % (git, ' + uncommitted source' if dirty else '', stz)
            else:
                port = lab.free_port()
                proc = subprocess.Popen(s['cmd'] + [str(port)], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if not wait_up(port, proc):
                    print('webbench: %s did not answer; left out' % s['label'])
                    proc.kill()
                    s['version'] = 'did not start'
                    continue
                s['version'] = {'node': lambda: 'Node.js ' + version(['node', '--version']),
                                'bun': lambda: 'Bun ' + version(['bun', '--version']),
                                'python': lambda: version([sys.executable, '--version']),
                                'java': lambda: version(['java', '-version'])}[s['id']]()
            print('%s (%s) on %d' % (s['label'], s['version'], port))
            for w in WORKLOADS:
                path = s['paths'].get(w['id'])
                if not path:
                    continue
                st, body = get(port, path)
                if st != 200 or body != EXPECT[w['id']]:
                    identical[w['id']] = False
                    print('   %-7s DIFFERENT ANSWER (%d, %d bytes, want %d) -- not timed' % (w['id'], st, len(body), len(EXPECT[w['id']])))
                    continue
                load(port, path, max(CONC), secs=PRIME)
                for c in CONC:
                    best = None
                    for _ in range(REPS):
                        r = load(port, path, c)
                        if best is None or r['rps'] > best['rps']:
                            best = r
                    best.update(server=s['id'], workload=w['id'], c=c)
                    rows.append(best)
                    print('   %-7s c=%d  %9.0f req/s   p50 %6.2f ms  p99 %7.2f ms  errors %d' % (
                        w['id'], c, best['rps'], best['p50_us'] / 1000, best['p99_us'] / 1000, best['errors'] + best['non200']))
            if proc:
                proc.kill()
                proc.wait(timeout=20)
    finally:
        if haro:
            try:
                lab.req(haro[0], 'POST', '/stop', timeout=5)
                haro[1].wait(timeout=30)
            except Exception:
                haro[1].kill()
    servers = [{k: s[k] for k in ('id', 'label', 'arch', 'version')} | {'ours': s.get('ours', False)}
               for s in SERVERS if s.get('version') and s['version'] != 'did not start' and any(r['server'] == s['id'] for r in rows)]
    out = {
        'taken': time.strftime('%Y-%m-%d %H:%M'),
        'machine': {'cpu': cpu_name(), 'cores': os.cpu_count(), 'cpu_speed_pct': speed, 'os': 'Windows' if os.name == 'nt' else os.uname().sysname},
        'duration_s': DUR, 'warmup_s': WARM, 'reps': REPS, 'prime_s': PRIME, 'quick': QUICK,
        'client': 'runtime/lab/loadgen.exe (haro/serv/bench/loadgen.zig) on the same machine, over loopback: one connection a request (Connection: close), as many threads as connections',
        'servers': servers, 'workloads': WORKLOADS, 'rows': rows, 'identical': identical,
        'notes': [
            'HaroServer serves one request at a time, on one thread, with one connection per request: it has no keep-alive. Every server here was measured the same way (Connection: close); Node, Bun, Java and Python can also keep a connection open and serve more requests a second that way, which this comparison does not show.',
            'With eight connections at once, Java uses a pool of threads across every core, Python a thread per connection under one interpreter lock, Node and Bun one event loop each, and HaroServer one thread: what it gains from eight is only the overlap of the client\'s own work.',
            'primes is computing in the language itself: V8 (Node), JavaScriptCore (Bun) and HotSpot (Java) compile the loop to machine code while it runs; Ring++ and CPython interpret bytecode. That row shows the cost of an interpreter, not of a server.',
            'text through Softanza makes objects and calls its engine (Zig) for every operation; HaroServer, plain Ring answers the same bytes with Ring++\'s builtins. The difference between the two rows is what Softanza\'s layer costs on this request.',
            'One machine, loopback only: no network latency, tiny answers, the client sharing the CPU with the server. The CPU reading above is part of the measurement.',
            'Not measured, because each needs a download first: Express, Fastify (npm), FastAPI with uvicorn, Flask (PyPI), Spring Boot (Maven), ASP.NET Core (the .NET SDK) and Go\'s net/http (the Go toolchain).',
        ],
    }
    path = os.path.join(LAB, 'results.json')
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1)
    hist = os.path.join(ROOT, 'runtime', 'lab', 'results-%s.json' % time.strftime('%Y%m%d-%H%M'))
    json.dump(out, open(hist, 'w', encoding='utf-8'), indent=1)
    print('webbench: wrote %s (and %s)' % (path, hist))
    if not all(identical.values()):
        sys.exit(1)


main()
