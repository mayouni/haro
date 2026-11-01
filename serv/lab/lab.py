"""THE SOFTANZA LAB, started: HaroServer with the lab in its base and Softanza's library compiling behind it.

    python haro/serv/lab/lab.py [--port=8642]       then open http://127.0.0.1:8642/lab ; Ctrl+C stops it

The server runs from the installed library's folder (D:\\ringpp\\ringpp-win64\\libraries\\stzlib, or STZ_TREE), where
`load "stzlib.ring"` resolves and Softanza finds its engine, on zig-out's rnxc (or RNXC). The lab is deployed first, so
the page answers at once; Softanza's library follows into the base, compiled in the background (rung 9) while the
page polls GET /deploy/stz. The server's own output goes to runtime/lab/haroserv.log.

`start()` is what bench/webbench.py uses to stand the same server up for the comparison.
"""
import os, socket, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
STZ_TREE = os.environ.get('STZ_TREE') or r'D:\ringpp\ringpp-win64\libraries\stzlib'
HOST = os.path.join(ROOT, 'haro', 'serv', 'host.ring')


def req(port, method, path, body=b'', timeout=60):
    """One request on a blocking socket (a Python socket with a timeout waits through select(), a Windows timer
    tick a request: haro/serv/court.py). Returns (status, body bytes)."""
    if isinstance(body, str):
        body = body.encode('utf-8')
    c = socket.create_connection(('127.0.0.1', port), timeout=timeout)
    c.settimeout(None)
    c.sendall(('%s %s HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Length: %d\r\nConnection: close\r\n\r\n'
               % (method, path, len(body))).encode() + body)
    d = b''
    while True:
        b = c.recv(65536)
        if not b:
            break
        d += b
    c.close()
    head, _, pay = d.partition(b'\r\n\r\n')
    return int(head.split(b' ')[1]), pay


def free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def start(port, softanza=True, log=None, wait_softanza=False, say=print):
    """HaroServer up on `port` with the lab in its base; Softanza's library deploying (or deployed, with
    wait_softanza). Returns the process."""
    os.makedirs(os.path.join(ROOT, 'runtime', 'lab'), exist_ok=True)
    log = log or os.path.join(ROOT, 'runtime', 'lab', 'haroserv.log')
    env = dict(os.environ, HAROSERV_PORT=str(port))
    out = open(log, 'wb')
    proc = subprocess.Popen([RNXC, 'resident', HOST], cwd=STZ_TREE, env=env, stdout=out, stderr=subprocess.STDOUT)
    for _ in range(400):
        try:
            if req(port, 'GET', '/stats', timeout=2)[0] == 200:
                break
        except OSError:
            time.sleep(0.05)
    else:
        proc.kill()
        raise SystemExit('lab: the server did not answer on %d (see %s)' % (port, log))
    src = '$cLabDir = "%s"\n' % HERE.replace(os.sep, '/') + open(os.path.join(HERE, 'lab.ring'), encoding='utf-8').read()
    st, body = req(port, 'POST', '/base/lab', src)
    if st == 202:
        while st == 202:
            time.sleep(0.05)
            st, body = req(port, 'GET', '/deploy/lab')
    if st not in (200, 201):
        proc.kill()
        raise SystemExit('lab: the lab was refused: %s' % body.decode('utf-8', 'replace'))
    say('lab: the page answers at http://127.0.0.1:%d/lab' % port)
    if softanza:
        t = time.perf_counter()
        st, body = req(port, 'POST', '/base/stz', 'load "stzlib.ring"\n')
        say('lab: Softanza\'s library is compiling in the background (%d %s)' % (st, body.decode('utf-8', 'replace')))
        if wait_softanza:
            while st == 202:
                time.sleep(0.2)
                st, body = req(port, 'GET', '/deploy/stz')
            if st not in (200, 201):
                proc.kill()
                raise SystemExit('lab: Softanza was refused: %s' % body.decode('utf-8', 'replace'))
            say('lab: Softanza admitted in %.1f s' % (time.perf_counter() - t))
    return proc


def main():
    port = 8642
    for a in sys.argv[1:]:
        if a.startswith('--port='):
            port = int(a.split('=', 1)[1])
    proc = start(port)
    print('lab: Ctrl+C stops the server')
    try:
        proc.wait()
    except KeyboardInterrupt:
        try:
            req(port, 'POST', '/stop', timeout=5)
        except OSError:
            pass
        proc.wait(timeout=20)


if __name__ == '__main__':
    main()
