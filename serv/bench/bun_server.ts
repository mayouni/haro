// The web comparison's Bun server (webbench.py): Bun.serve, one process, one event loop.
// The same three answers, byte for byte, as every server measured: /bench/hello, /bench/text, /bench/primes.
const port = Number(process.argv[2] || 8702);
const P = Array(20).fill('the quick brown fox jumps over the lazy dog').join(' ');

function text(): string {
  const words = P.split(' ');
  return P.toUpperCase() + '\n' + words.length + '\n' + words.slice().reverse().join(' ');
}

// the primes below 20,000 by a sieve over a plain array, as the other servers do with their own lists
function primes(): string {
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

const routes: Record<string, () => string> = { '/bench/hello': () => 'hello', '/bench/text': text, '/bench/primes': primes };

Bun.serve({
  port,
  hostname: '127.0.0.1',
  fetch(req) {
    const u = req.url, at = u.indexOf('/', u.indexOf('//') + 2), q = u.indexOf('?', at);
    const f = routes[q < 0 ? u.slice(at) : u.slice(at, q)];
    if (!f) return new Response('', { status: 404 });
    return new Response(f(), { headers: { 'Content-Type': 'text/plain' } });
  },
});
