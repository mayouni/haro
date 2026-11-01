// The web comparison's Node.js server (webbench.py): node's own http module, one process, one event loop.
// The same three answers, byte for byte, as every server measured: /bench/hello, /bench/text, /bench/primes.
import http from 'node:http';

const port = Number(process.argv[2] || 8701);
const P = Array(20).fill('the quick brown fox jumps over the lazy dog').join(' ');

function text() {
  const words = P.split(' ');
  return P.toUpperCase() + '\n' + words.length + '\n' + words.slice().reverse().join(' ');
}

// the primes below 20,000 by a sieve over a plain array, as the other servers do with their own lists
function primes() {
  const n = 20000, sieve = new Array(n).fill(0);
  let count = 0;
  for (let i = 2; i < n; i++) {
    if (sieve[i] === 0) {
      count++;
      for (let j = i * i; j < n; j += i) sieve[j] = 1;
    }
  }
  return String(count);
}

const routes = { '/bench/hello': () => 'hello', '/bench/text': text, '/bench/primes': primes };

http.createServer((req, res) => {
  const f = routes[req.url.split('?')[0]];
  if (!f) { res.writeHead(404, { 'Content-Length': 0 }); res.end(); return; }
  const body = f();
  res.writeHead(200, { 'Content-Type': 'text/plain', 'Content-Length': Buffer.byteLength(body) });
  res.end(body);
}).listen(port, '127.0.0.1');
