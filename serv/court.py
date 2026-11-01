"""HAROSERVER'S COURT -- the host loop (haro/serv/host.ring) booted on the resident VM and driven over HTTP, every answer
checked, the costs measured.

    python haro/serv/court.py               RNXC=<path> for another build
    python haro/serv/court.py --softanza    and an app that loads Softanza's library, run from the install's tree
    python haro/serv/court.py --platform=linux     the Linux rnxc under WSL (the client stays on Windows: WSL forwards
                                                   localhost)

What it asks, in order, of ONE server process:
  deploy     an app admitted while the server runs, its route answering at once; the same app twice, refused; an app
             Rule A refuses, refused whole -- its route never appears
  state      an app holding an object; REPLACED while it runs -- the object and its tally kept, the new code answering;
             replaced again with an attribute added -- admitted, the running object takes it (rung 7); one dropped -- refused
  failure    a handler that raises answers 500 and the server goes on; a new class admitted after the first file; a
             handler that makes objects of a class an app deployed after it brings -- R11 until then, the class
             found by name once it is (rung 8)
  load       sequential requests to one route: requests a second, and latency
  per request  code admitted with every request (RingServ's eval-per-request shape): what an admission costs while
             the server runs, and what the program and the process grow by -- the question the resident VM's fifth
             rung left open: must code admitted per request be RELEASED?
  release    code that comes with a request and leaves with it (POST /run, rung 6): admitted, called, released; the
             same code again; a raising run released too; thousands of runs, each answering with a literal of its own
             released code, and the process's memory flat across them
  stop       the loop ends on request, the process exits 0, and wrote nothing to stderr

A part that cannot run is named, never passed in silence."""
import ctypes, os, socket, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
APPS = os.path.join(HERE, 'apps')
LINUX = '--platform=linux' in sys.argv
SOFTANZA = '--softanza' in sys.argv
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out-linux' if LINUX else 'zig-out', 'bin', 'rnxc' if LINUX else 'rnxc.exe')
STZ_TREE = os.environ.get('HAROSERV_STZ') or r'D:\ringpp\ringpp-win64\libraries\stzlib'
DISTRO = os.environ.get('RPP_WSL_DISTRO', 'Ubuntu')
N_LOAD = int(os.environ.get('HAROSERV_LOAD', '2000'))
N_PER_REQUEST = int(os.environ.get('HAROSERV_PER_REQUEST', '300'))
fails, passed = [], []


def say(ok, what):
    print(('ok    ' if ok else 'FAIL  ') + what, flush=True)
    (passed if ok else fails).append(what)


def free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def wsl_path(p):
    p = os.path.abspath(p).replace(chr(92), '/')
    return '/mnt/' + p[0].lower() + p[2:]


PORT = free_port()


def req(method, path, body=b''):
    """One request on a connection of its own, the request in ONE send, read to the server's close. A raw, BLOCKING socket:
    measured 2026-10-31, http.client -- and then a raw socket given a timeout, which waits through select() -- spent a
    Windows timer tick (~15 ms) on every request against a server that answers in ~0.2 ms. The court was timing itself."""
    if isinstance(body, str):
        body = body.encode('utf-8')
    t = time.perf_counter()
    # BLOCKING, no timeout: a socket with a timeout waits through select(), which cost a Windows timer tick too
    s = socket.create_connection(('127.0.0.1', PORT))
    s.sendall(('%s %s HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Length: %d\r\nConnection: close\r\n\r\n' % (method, path, len(body))).encode('ascii') + body)
    data = b''
    while True:
        b = s.recv(65536)
        if not b:
            break
        data += b
    s.close()
    ms = (time.perf_counter() - t) * 1000
    head, _, payload = data.partition(b'\r\n\r\n')
    status = int(head.split(b' ', 2)[1]) if head.startswith(b'HTTP/') else 0
    return status, payload.decode('utf-8', 'replace'), ms


def app(name):
    return open(os.path.join(APPS, name), encoding='utf-8').read()


# ---- the process's memory, from outside
class PMC(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong), ('PeakWorkingSetSize', ctypes.c_size_t),
                ('WorkingSetSize', ctypes.c_size_t), ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t),
                ('PeakPagefileUsage', ctypes.c_size_t), ('PrivateUsage', ctypes.c_size_t)]


def private_mb(proc):
    """The server's private bytes (Windows), in MB; None where it cannot be read (under WSL)."""
    if LINUX or os.name != 'nt':
        return None
    h = ctypes.windll.kernel32.OpenProcess(0x0400 | 0x0010, False, proc.pid)
    if not h:
        return None
    pmc = PMC()
    pmc.cb = ctypes.sizeof(PMC)
    ok = ctypes.windll.psapi.GetProcessMemoryInfo(h, ctypes.byref(pmc), pmc.cb)
    ctypes.windll.kernel32.CloseHandle(h)
    return pmc.PrivateUsage / (1 << 20) if ok else None


def start():
    host = os.path.join(HERE, 'host.ring')
    cwd = STZ_TREE if SOFTANZA else HERE
    if LINUX:
        cmd = ['wsl.exe', '-d', DISTRO, '--cd', wsl_path(cwd), '--', 'env', 'HAROSERV_PORT=%d' % PORT, wsl_path(RNXC), 'resident', wsl_path(host)]
        env = None
    else:
        cmd = [RNXC, 'resident', host]
        env = dict(os.environ)
        env['HAROSERV_PORT'] = str(PORT)
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t = time.time()
    while time.time() - t < 120:
        if proc.poll() is not None:
            break
        try:
            st, _, _ = req('GET', '/stats')
            if st == 200:
                return proc, (time.time() - t) * 1000
        except OSError:
            time.sleep(0.05)
    out, err = proc.communicate(timeout=10) if proc.poll() is not None else (b'', b'')
    raise SystemExit('FAIL haroserv did not come up on port %d: %s %s' % (PORT, out.decode('utf-8', 'replace')[-300:], err.decode('utf-8', 'replace')[-300:]))


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))]


def main():
    if not os.path.exists(RNXC):
        print('no rnxc at ' + RNXC)
        return 1
    proc, boot_ms = start()
    print('haroserv up on 127.0.0.1:%d in %.0f ms (%s%s)' % (PORT, boot_ms, 'Linux, ' if LINUX else '', RNXC))
    mem0 = private_mb(proc)

    # ---- deploy
    st, body, _ = req('GET', '/hello')
    say(st == 404, 'before the app: GET /hello is 404')
    st, body, t_admit = req('POST', '/admit/hello', app('hello.ring'))
    say(st == 201, 'deploy: hello admitted while the server runs (%d, %.1f ms)' % (st, t_admit))
    st, body, _ = req('GET', '/hello')
    say(st == 200 and body == 'hello from HaroServer', 'deploy: its route answers at once: %r' % body)
    st, body, _ = req('POST', '/admit/hello', app('hello.ring'))
    say(st == 422 and 'already defined' in body, 'deploy: the same app twice is refused (%d): %s' % (st, body[:90]))
    st, body, _ = req('GET', '/hello')
    say(st == 200, 'deploy: after the refusal the first is still served')
    st, body, _ = req('POST', '/admit/bad', app('bad.ring'))
    say(st == 422 and 'Rule A' in body, 'deploy: Rule A refuses an app whole (%d): %s' % (st, body[:90]))
    st, body, _ = req('GET', '/bad')
    say(st == 404, 'deploy: the refused app\'s route never appears')

    # ---- state, and a live redeploy
    st, _, _ = req('POST', '/admit/tally', app('tally.ring'))
    a = req('POST', '/tally', '5')
    b = req('POST', '/tally', '7')
    say(st == 201 and a[1] == '5' and b[1] == '12', 'state: the tally app holds an object: 5, then 12')
    st, body, t_repl = req('POST', '/replace/tally', app('tally_v2.ring'))
    say(st == 201, 'redeploy: tally replaced while it runs (%d, %.1f ms)' % (st, t_repl))
    st, body, _ = req('GET', '/tally')
    say(st == 200 and body == 'tally 12 (v2)', 'redeploy: the same object, the new code: %r' % body)
    st, body, _ = req('POST', '/tally', '1')
    st2, body2, _ = req('GET', '/tally')
    say(body == '13' and body2 == 'tally 13 (v2)', 'redeploy: the handler v2 left alone still runs, on the kept object: %r, %r' % (body, body2))
    st, body, _ = req('POST', '/replace/tally', app('tally_v3.ring'))
    say(st == 201, 'redeploy: an attribute added to the live class is admitted (%d)%s' % (st, '' if st == 201 else ': ' + body[:100]))
    st, body, _ = req('GET', '/tally')
    say(body == 'tally 13 in 0 add(s)', 'redeploy: the running object takes it, starting as declared, its total kept: %r' % body)
    st, body, _ = req('POST', '/tally', '2')
    st2, body2, _ = req('GET', '/tally')
    say(body == '15' and body2 == 'tally 15 in 1 add(s)', 'redeploy: and the new code counts in it: %r, %r' % (body, body2))
    st, body, _ = req('POST', '/replace/tally', app('tally_v4.ring'))
    say(st == 422 and 'keeps the attributes' in body, 'redeploy: an attribute dropped from the live class is refused (%d): %s' % (st, body[:100]))
    st, body, _ = req('GET', '/tally')
    say(body == 'tally 15 in 1 add(s)', 'redeploy: after the refusal the server answers as before: %r' % body)

    # ---- failure, and a class after the first file
    req('POST', '/admit/boom', app('boom.ring'))
    st, body, _ = req('GET', '/boom')
    say(st == 500 and 'the boom app said no' in body, 'failure: a raising handler answers 500 (%s)' % body.strip()[:60])
    st, body, _ = req('GET', '/hello')
    say(st == 200, 'failure: and the server goes on')
    # a client that sends half a request and leaves, and one that connects and says nothing: one loop serves
    # everything, so neither may stop it -- the second holds it at most the receive timeout (10 s)
    s = socket.create_connection(('127.0.0.1', PORT))
    s.sendall(b'GET /hel')
    s.close()
    st, body, _ = req('GET', '/hello')
    say(st == 200, 'failure: a client that sent half a request and left does not stop the loop')
    idle = socket.create_connection(('127.0.0.1', PORT))
    t = time.perf_counter()
    st, body, _ = req('GET', '/hello')
    held = time.perf_counter() - t
    idle.close()
    say(st == 200 and held < 15, 'failure: a client that says nothing holds the loop %.1f s, then it serves again' % held)
    st, _, _ = req('POST', '/admit/echo', app('echo.ring'))
    st2, body, _ = req('POST', '/echo', 'abc')
    say(st == 201 and body == 'echo 3 byte(s): abc', 'class: an app with a class admitted while serving: %r' % body)
    # rung 8: a handler that makes objects of a class an app deployed AFTER it brings
    st, _, _ = req('POST', '/admit/ledger', app('ledger.ring'))
    st2, body, _ = req('GET', '/ledger')
    say(st == 201 and st2 == 500 and 'class not found: entry.entry' in body,
        'late new: a handler making a class no app has brought yet answers 500, R11 (%d): %s' % (st2, body.strip()[:70]))
    st, _, _ = req('POST', '/admit/entry?Entry', app('entry.ring'))
    st2, body, _ = req('GET', '/ledger')
    say(st == 201 and st2 == 200 and body == 'rent: 40',
        'late new: once the app bringing it is deployed, the same handler makes its objects: %r' % body)

    # D31: every app a namespace of its own -- the same names in two apps, and another app's function through its exports
    sa, _, _ = req('POST', '/admit/twin_a', app('twin_a.ring'))
    sb, _, _ = req('POST', '/admit/twin_b', app('twin_b.ring'))
    _, ba, _ = req('GET', '/twin_a')
    _, bb, _ = req('GET', '/twin_b')
    say(sa == 201 and sb == 201 and ba == 'twin a answers' and bb == 'twin b answers',
        'namespaces: two apps define the same functions, each answers its own: %r, %r' % (ba, bb))
    s1, _, _ = req('POST', '/admit/sum?Sum', app('sum.ring'))
    s2, _, _ = req('POST', '/admit/calc', app('calc.ring'))
    c1, b1, _ = req('GET', '/calc')
    c2, b2, _ = req('GET', '/peek')
    say(s1 == 201 and s2 == 201 and c1 == 200 and b1 == '2 + 3 = 5' and c2 == 500 and 'sum.secret' in b2,
        'namespaces: an app reaches another\'s exported function (%r) and not what it keeps (%d)' % (b1, c2))
    s3, b3, _ = req('POST', '/admit/nope?Missing', app('sum.ring'))
    say(s3 == 422 and 'exports Missing' in b3, 'namespaces: an export naming nothing the app defines is refused (%d)' % s3)

    # ---- load: one route, sequential
    lat = []
    t0 = time.perf_counter()
    for _ in range(N_LOAD):
        st, body, ms = req('GET', '/hello')
        if st != 200:
            break
        lat.append(ms)
    dt = time.perf_counter() - t0
    say(len(lat) == N_LOAD, 'load: %d requests to GET /hello all answered' % N_LOAD)
    print('      %.0f requests/s sequential, one connection each; latency p50 %.2f ms, p95 %.2f, max %.2f'
          % (len(lat) / dt, pct(lat, 0.5), pct(lat, 0.95), max(lat)))
    mem1 = private_mb(proc)

    # ---- per request: code admitted with every request
    adm, call = [], []
    for i in range(1, N_PER_REQUEST + 1):
        src = 'Route("GET", "/f%d", "PerRequest%d")\nfunc PerRequest%d cBody\n\treturn "f%d"\n' % (i, i, i, i)
        st, _, ms = req('POST', '/admit/f%d' % i, src)
        st2, body, ms2 = req('GET', '/f%d' % i)
        if st != 201 or body != 'f%d' % i:
            say(False, 'per request: admission %d answered %d %r' % (i, st2, body))
            break
        adm.append(ms)
        call.append(ms2)
    say(len(adm) == N_PER_REQUEST, 'per request: %d functions admitted with their requests, each answering at once' % N_PER_REQUEST)
    mem2 = private_mb(proc)
    if adm:
        print('      an admission over HTTP: p50 %.2f ms, p95 %.2f (first %.2f, last %.2f); the call after it p50 %.2f ms'
              % (pct(adm, 0.5), pct(adm, 0.95), adm[0], adm[-1], pct(call, 0.5)))
    if mem0 is not None and mem2 is not None:
        print('      private memory: %.1f MB at boot, %.1f after the load, %.1f after %d admissions -- %.1f KB an admission'
              % (mem0, mem1, mem2, len(adm), (mem2 - mem1) * 1024 / max(1, len(adm))))
    lat2 = [req('GET', '/hello')[2] for _ in range(300)]
    print('      GET /hello after them: p50 %.2f ms (the host routes by a list: %d routes now)' % (pct(lat2, 0.5), 5 + len(adm)))

    # ---- release (rung 6): code that comes with a request and leaves with it
    def stats():
        return dict(l.rsplit(' ', 1) for l in req('GET', '/stats')[1].split('\n') if ' ' in l)
    f0 = stats().get('functions')
    run_src = 'func Run cInput\n\treturn "run on " + cInput\n'
    st, body, _ = req('POST', '/run?ring', run_src)
    st2, body2, _ = req('POST', '/run?again', run_src)
    say(st == 200 and body == 'run on ring' and st2 == 200 and body2 == 'run on again',
        'release: a run admitted, called and released, and the same code again -- Run is free once released: %r, %r' % (body, body2))
    s1 = stats()
    say(s1.get('functions') == f0 and s1.get('runs released') == '2', 'release: after them the program holds %s function(s), as before (%s)' % (s1.get('functions'), f0))
    st, body, _ = req('POST', '/run', 'func Run cInput\n\traise("the run said no")\n')
    st2, body2, _ = req('POST', '/run?after', run_src)
    say(st == 500 and 'the run said no' in body and st2 == 200 and body2 == 'run on after',
        'release: a run that raises answers 500, is released, and the next run works: %r' % body2)
    st, body, _ = req('POST', '/run', 'zTop = 1\nfunc Run cInput\n\treturn zTop\n')
    say(st == 422 and 'Rule A' in body, 'release: a run Rule A refuses is never admitted (%d): %s' % (st, body[:80]))
    # what Run returns is the reply, sent AFTER the release: a literal of the released code outlives it
    big = ''.join(chr(97 + (i * 7) % 26) for i in range(16000))
    run_big = 'func Run cInput\n\treturn "%s"\n' % big
    # The memory is BOUNDED, not flat: a released run's source and compile stay in the program's arena until the arena
    # is compacted (past twice its size plus 16 MB, under a millisecond here), so it rises and falls. Measured 2026-10-31:
    # 36-50 MB over 14,000 runs; without the release's compaction, +17 KB a run for good. So the high-water mark of the
    # second half of the runs is held to the first half's -- each half spans more than one compaction
    runs, lat_run = int(os.environ.get('HAROSERV_RUNS', '3000')), []
    mem = []
    for i in range(1, runs + 1):
        st, body, ms = req('POST', '/run?%d' % i, run_big)
        if st != 200 or body != big:
            say(False, 'release: run %d answered %d, %d byte(s)%s' % (i, st, len(body), '' if body == big else ' -- not the literal'))
            break
        lat_run.append(ms)
        if i % 50 == 0:
            mem.append(private_mb(proc))
    say(len(lat_run) == runs, 'release: %d runs, each returning a 16 KB literal of its own code, answered with it after its release' % runs)
    say(stats().get('functions') == f0, 'release: and the program holds %s function(s), as before' % f0)
    if lat_run:
        print('      a run over HTTP (admit, call, release, reply): p50 %.2f ms, p95 %.2f' % (pct(lat_run, 0.5), pct(lat_run, 0.95)))
    if runs < 3000:
        print('      private memory: %d runs do not span a compaction in each half (it takes ~1,000) -- the bounded-memory check is NOT measured' % runs)
    elif mem and None not in mem and len(mem) >= 8:
        half = len(mem) // 2
        hi1, hi2 = max(mem[2:half]), max(mem[half:])
        say(hi2 - hi1 < 6, 'release: private memory bounded -- high-water %.1f MB over runs %d-%d, %.1f over %d-%d (low %.1f)'
            % (hi1, 150, half * 50, hi2, half * 50, len(mem) * 50, min(mem[2:])))
    else:
        print('      private memory: not read on this platform -- the bounded-memory check is NOT measured here')

    if SOFTANZA:
        st, body, ms = req('POST', '/base/stz', 'load "stzlib.ring"\n')
        say(st == 201, 'softanza: Softanza\'s library admitted into the base while serving (%d, %.0f ms)%s' % (st, ms, '' if st == 201 else ': ' + body[:300]))
        src = 'Route("POST", "/upper", "UpperApp")\nfunc UpperApp cBody\n\treturn StzStringQ(cBody).Uppercased()\n'
        st, body, _ = req('POST', '/admit/upper', src)
        say(st == 201, 'softanza: an app reading the base\'s library admitted (%d)%s' % (st, '' if st == 201 else ': ' + body[:300]))
        st, body, _ = req('POST', '/upper', 'ring++')
        say(st == 200 and body == 'RING++', 'softanza: its route answers through Softanza: %r' % body)
        adm2 = []
        for i in range(1, 51):
            src = 'Route("GET", "/s%d", "PerRequestStz%d")\nfunc PerRequestStz%d cBody\n\treturn StzStringQ("s%d").Uppercased()\n' % (i, i, i, i)
            st, _, ms = req('POST', '/admit/s%d' % i, src)
            st2, body, _ = req('GET', '/s%d' % i)
            if st != 201 or body != 'S%d' % i:
                say(False, 'softanza: admission %d answered %d %r' % (i, st2, body))
                break
            adm2.append(ms)
        say(len(adm2) == 50, 'softanza: 50 more functions admitted with their requests into the program holding the library')
        if adm2:
            print('      an admission at Softanza\'s size, over HTTP: p50 %.2f ms, p95 %.2f; private memory %s MB'
                  % (pct(adm2, 0.5), pct(adm2, 0.95), ('%.0f' % private_mb(proc)) if private_mb(proc) else '?'))

    st, body, _ = req('GET', '/stats')
    print('      ' + body.replace('\n', ', '))
    # ---- stop
    st, body, _ = req('POST', '/stop')
    try:
        out, err = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    out = out.decode('utf-8', 'replace').replace('\r', '')
    err = err.decode('utf-8', 'replace').strip()
    say(st == 200 and proc.returncode == 0 and 'haroserv: stopped after' in out, 'stop: the loop ended on request and the process exited %s' % proc.returncode)
    say(not err, 'stop: nothing on stderr' + ('' if not err else ': ' + err[:120]))
    summary = [l for l in out.split('\n') if l.startswith('resident:')]
    if summary:
        print('      ' + summary[0])
    print()
    if fails:
        print('HAROSERV FAILED -- %d of %d: %s' % (len(fails), len(fails) + len(passed), fails[0]))
        return 1
    print('HAROSERV OK -- %d checks' % len(passed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
