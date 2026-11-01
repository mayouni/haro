"""The web comparison's Python server (webbench.py): the standard library's ThreadingHTTPServer, a thread a
connection. Production Python serves through uvicorn or gunicorn, which are not installed here; this is what
Python itself ships. The same three answers, byte for byte, as every server measured."""
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8703
P = ' '.join(['the quick brown fox jumps over the lazy dog'] * 20)


def text():
    words = P.split(' ')
    return P.upper() + '\n' + str(len(words)) + '\n' + ' '.join(reversed(words))


# the primes below 20,000 by a sieve over a plain list, as the other servers do with their own lists
def primes():
    n = 20000
    sieve = [0] * n
    count = 0
    for i in range(2, n):
        if sieve[i] == 0:
            count += 1
            for j in range(i * i, n, i):
                sieve[j] = 1
    return str(count)


ROUTES = {'/bench/hello': lambda: 'hello', '/bench/text': text, '/bench/primes': primes}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        f = ROUTES.get(self.path.split('?')[0])
        if not f:
            self.send_response(404)
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        body = f().encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


ThreadingHTTPServer.daemon_threads = True
ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
