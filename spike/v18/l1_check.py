"""Judges rung 18, the structure level of the computing altitude, for the Ring++ face:
   python haro/spike/v18/l1_check.py [--plant] [--quick]      (exit 1 on any failure)

  F  the fixtures (v18/fixtures.txt, composed before the code): each Ring program abstracts to the graph its fixture says; the printer,
     given that hand-written graph, prints the text its fixture says; the printed text parses back to the same graph; printing that graph
     again gives the same text (the formatter is idempotent); and original and canonical text compile to the same code (`rnxc dis`) --
     or, where the answer is a printed line (`see`, `put`, a bare `return`), print the same output on the oracle
  C  two controls that must FAIL: an abstraction that drops a `for`'s step (both passes lose it, so only the compiled code can say so),
     and a printer that drops comments
  K  a corpus: Ring files of the spike, Ring++'s probes, Ring's standard library and a sample of Softanza (read-only), through the same
     four checks; the floor is the share that round-trips, never fewer files than the pinned count
The graph is the reference implementation of v18/GRAMMAR.md; `rnxc` is the second one, and the fixtures judge both.
"""
import glob, os, re, subprocess, sys, tempfile, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(SP, '..', '..'))
sys.path.insert(0, HERE)
import cst, l1

PLANT = '--plant' in sys.argv
QUICK = '--quick' in sys.argv
SCRATCH = os.path.join(HERE, 'scratch')
ORACLE = os.environ.get('RING') or os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
STZ = r'D:\GitHub\stzlib\libraries\stzlib\base'
FIXTURE_FLOOR, CORPUS_FLOOR = 20, 24
fails = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def write(name, text):
    os.makedirs(SCRATCH, exist_ok=True)
    p = os.path.join(SCRATCH, name)
    open(p, 'wb').write(text.encode('latin-1'))
    return p


def read_text(path):
    return open(path, 'rb').read().decode('latin-1')


def read_fixtures(path):
    fx, cur, sec = [], None, None
    for line in read_text(path).replace('\r\n', '\n').split('\n'):          # a checkout with autocrlf hands the file back with CRLF
        if line.startswith('=== '):
            num, _, name = line[4:].partition(' ')
            cur = {'id': num, 'name': name, 'notes': [], 'ring': None, 'l1': None, 'out': None}
            fx.append(cur)
            sec = None
        elif cur is None:
            continue
        elif line.startswith('~~~'):
            cur['notes'].append(line[4:])
        elif line in ('--- ring', '--- l1', '--- out'):
            sec = line[4:]
            cur[sec] = []
        elif sec is not None:
            cur[sec].append(line)
    for f in fx:
        for s in ('ring', 'l1', 'out'):
            if f[s] is not None:
                lines = f[s]
                while lines and lines[-1] == '':
                    lines.pop()
                f[s] = '\n'.join(lines) + '\n'
        f['dis'] = any(n.strip() == 'dis: yes' for n in f['notes'])
        f['run'] = any(n.strip() == 'run: yes' for n in f['notes'])
    return fx


def dis(text, name):
    p = write(name, text)
    # RNXC_LINES_STATIC: since F-110 (2026-10-12) rnxc puts a LINE into the code where Ring carries one past an `ok` -- and only when the
    # `ok` stands on its own line -- so two layouts of one program compile to different code there; this judge compares no line
    r = subprocess.run([cst.RNXC, 'dis', p], capture_output=True, timeout=300,
                       env=dict(os.environ, RNXC_NOCACHE='1', RNXC_LINES_STATIC='1'))
    out = r.stdout.decode('latin-1')
    # a lambda is named after its source LINE (`@@lambda62`): layout leaks into a function's name, and a formatter moves it
    out = re.sub(r'@@lambda\d+', '@@lambdaN', out)
    # one thing rnxc does that is not a result, measured (HF-74): it types a method's return from the parse (a `return x` the parser cut
    # from its value reads `ret=str` beside `ret=ref` for the same program -- the answers are the same, probed). It also read `put` and a
    # capitalised `See`/`SEE` as `?` until 2026-10-04, and this judge normalised the `say` flag to hide it; that is gone, so a regression
    # shows here again
    out = re.sub(r' ret=\w+', '', out)
    # `vnew`'s d is the capacity the list is created with, counted off the tree's children (blank lines in a literal change it); the
    # elements are the `vpush` instructions after it, which stay compared
    out = re.sub(r'(\bvnew\s+a=\d+\s+b=\d+\s+c=\d+\s+d=)\d+', r'\1_', out)
    return r.returncode, out


def run(text, name):
    """The program's output on the oracle: what Ring itself does, for the places where rnxc does not read Ring."""
    p = write(name, text)
    r = subprocess.run([ORACLE, p], capture_output=True, timeout=120)
    return r.returncode, r.stdout.decode('latin-1'), r.stderr.decode('latin-1').replace(p, '<file>')


def to_l1(text, name='x.ring'):
    g, why = l1.parse_ring(write(name, text))
    return g, why


def first_diff(a, b):
    sa, sb = l1.sexp_write(a), l1.sexp_write(b)
    i = next((i for i in range(min(len(sa), len(sb))) if sa[i] != sb[i]), min(len(sa), len(sb)))
    return f'at {i}: ...{sa[max(0, i - 40):i + 60]!r} / ...{sb[max(0, i - 40):i + 60]!r}'


def ring_refuses(path):
    """Does Ring itself refuse to read the file? `-norun` parses and loads without running a statement."""
    r = subprocess.run([ORACLE, path, '-norun'], capture_output=True, timeout=120, cwd=os.path.dirname(path))
    out = r.stdout.decode('latin-1') + r.stderr.decode('latin-1')
    return r.returncode != 0 or 'Error' in out


LOAD_LINE = re.compile(r'(?im)^(?:\xef\xbb\xbf)?[ \t]*(?:load|import)\b[^\n]*$')          # a byte-order mark may open the file


def strip_loads(text):
    """The text with its `load` and `import` lines blanked (every line kept): a copy compiled elsewhere cannot resolve what it loads, and
    the same blanking of the original and of the canonical text leaves the rest of the program to be compared."""
    return LOAD_LINE.sub('', text)


def refusals(text, name):
    """How many statements rnxc refuses in the text (`rnxc census`): a refused statement compiles to a trap, so the code of a text that has
    one says nothing about the graph -- the canonical text of such a file often compiles where the original does not."""
    p = write(name, text)
    r = subprocess.run([cst.RNXC, 'census', p], capture_output=True, timeout=300, env=dict(os.environ, RNXC_NOCACHE='1'))
    m = re.search(r'statements \d+: \d+ compiled \(\d+%\), (\d+) refused', r.stdout.decode('latin-1'))
    return int(m.group(1)) if m else 0


def round_trip_(text, name, with_dis=True):
    """The four checks on one program; -> (None, ...) when it holds, else a reason."""
    g, why = to_l1(text, name + '.ring')
    if g is None:
        return 'unparsed', why
    canon = l1.print_ring(g)
    g2, why2 = to_l1(canon, name + '_c.ring')
    if g2 is None:
        return 'the canonical text does not parse', why2
    if g2 != g:
        return 'graph differs after the round trip', first_diff(g, g2)
    if l1.print_ring(g2) != canon:
        return 'the formatter is not idempotent', ''
    if with_dis:
        a, b = dis(strip_loads(text), name + '_o.ring'), dis(strip_loads(canon), name + '_k.ring')
        if a[0] != 0 or b[0] != 0:
            return 'skipped', 'does not compile'          # not a failure: nothing to compare
        if a != b and refusals(strip_loads(text), name + '_r.ring'):
            return 'skipped', 'rnxc refuses part of the original'
        if a != b:
            i = next((i for i in range(min(len(a[1]), len(b[1]))) if a[1][i] != b[1][i]), 0)
            return 'compiled code differs', f'at {i}: {a[1][max(0, i - 60):i + 80]!r} / {b[1][max(0, i - 60):i + 80]!r}'
    return None, None


def round_trip(text, name, with_dis=True, path=None):
    """round_trip_ and, for a file that fails it, the question that decides whether the failure counts: does Ring itself refuse the file?
    (An unclosed comment, a literal not closed: the parser reads them as something, and no graph of that something is a program.)"""
    st, why = round_trip_(text, name, with_dis)
    if st not in (None, 'skipped') and path is not None and ring_refuses(path):
        return 'skipped', 'Ring itself refuses it'
    return st, why


def main():
    t0 = time.time()
    print('l1_check -- the structure level of the computing altitude, Ring++ face (rung 18)')
    fx = read_fixtures(os.path.join(HERE, 'fixtures.txt'))
    check(len(fx) >= FIXTURE_FLOOR, f'F the fixtures hold {len(fx)} programs, at or above the pinned floor of {FIXTURE_FLOOR}')
    bad = []
    for f in fx:
        want = l1.norm(l1.sexp_read(f['l1']))
        if f['ring'] is not None:
            got, why = to_l1(f['ring'], 'f' + f['id'] + '.ring')
            if got is None:
                bad.append((f['id'], 'unparsed: ' + str(why)))
                continue
            if got != want:
                bad.append((f['id'], 'abstracts to another graph ' + first_diff(want, got)))
                continue
        printed = l1.print_ring(want)
        if printed != f['out']:
            i = next((i for i in range(min(len(printed), len(f['out']))) if printed[i] != f['out'][i]), min(len(printed), len(f['out'])))
            bad.append((f['id'], f'prints other text, at {i}: {printed[max(0, i - 30):i + 40]!r} / {f["out"][max(0, i - 30):i + 40]!r}'))
            continue
        g2, why = to_l1(printed, 'f' + f['id'] + '_c.ring')
        if g2 is None:
            bad.append((f['id'], 'the printed text does not parse: ' + str(why)))
            continue
        same = (g2 == want) if f['ring'] is not None else (l1.norm(l1.strip_parens(g2)) == l1.norm(l1.strip_parens(want)))
        if not same:
            bad.append((f['id'], 'the printed text reads as another graph ' + first_diff(want, g2)))
            continue
        if l1.print_ring(g2) != printed:
            bad.append((f['id'], 'the formatter is not idempotent'))
            continue
        if f['dis'] and f['ring'] is not None:
            a, b = dis(f['ring'], 'f' + f['id'] + '_o.ring'), dis(printed, 'f' + f['id'] + '_k.ring')
            if a[0] != 0 or b[0] != 0 or a[1] != b[1]:
                bad.append((f['id'], 'original and canonical text compile to different code' if a[0] == b[0] == 0 else 'one of them does not compile'))
        if f['run'] and f['ring'] is not None:
            a, b = run(f['ring'], 'f' + f['id'] + '_ro.ring'), run(printed, 'f' + f['id'] + '_rk.ring')
            if a != b or a[0] != 0:
                bad.append((f['id'], f'original and canonical text print different output on the oracle: {a!r} / {b!r}'))
    for fid, why in bad[:6]:
        print(f'  FAIL F{fid}: {why[:420]}')
    fails.extend(f'F{fid}' for fid, _ in bad)
    check(not bad, f'F {len(fx)} fixtures: each program abstracts to its graph, the graph prints its text, the text parses back to the graph, '
                   f'printing is idempotent, original and canonical compile alike ({len(bad)} fail)')

    # ---- controls ------------------------------------------------------------------------------------------------------------------
    f6 = next(f for f in fx if f['id'] == '06')
    saved = l1.Abstract.s_for_statement

    def no_step(self, n):
        node = saved(self, n)
        node.pop('step', None)
        return node
    l1.Abstract.s_for_statement = no_step
    try:
        st, why = round_trip(f6['ring'], 'ctl1')
    finally:
        l1.Abstract.s_for_statement = saved
    check(st == 'compiled code differs', f"C the control, an abstraction that drops a `for`'s step, round-trips as a graph and is caught only by the compiled code: {st}")
    real = l1.Printer.item

    def no_comments(self, it, ind):
        return [] if it['k'] == 'comment' else real(self, it, ind)
    l1.Printer.item = no_comments
    try:
        st, why = round_trip(next(f for f in fx if f['id'] == '11')['ring'], 'ctl2', with_dis=False)
    finally:
        l1.Printer.item = real
    check(st == 'graph differs after the round trip', f'C the control, a printer that drops comments, is caught by the round trip: {st}')

    # ---- the corpus ---------------------------------------------------------------------------------------------------------------
    files = corpus()
    n_ok = n_skip = 0
    counts, failing = {}, []
    for p in files:
        try:
            st, why = round_trip(read_text(p), 'corpus', path=p)
        except Exception as e:                                  # a crash of the tool is a failure, never a skip
            st, why = 'tool', repr(e)[:160]
        counts[st] = counts.get(st, 0) + 1
        if st is None or st == 'skipped':
            n_ok += st is None
            n_skip += st == 'skipped'
        else:
            failing.append((os.path.relpath(p, ROOT) if p.startswith(ROOT) else p, st, why))
    if PLANT:
        failing.append(('PLANTED', 'plant', ''))
    for p, st, why in failing[:8]:
        print(f'  FAIL K {p}: {st} {str(why)[:300]}')
    fails.extend(f'K {p}' for p, _, _ in failing)
    check(not failing and len(files) >= CORPUS_FLOOR,
          f'K {len(files)} Ring files of four corpora: {n_ok} round-trip exactly (graph and compiled code, their `load` lines blanked), '
          f'{n_skip} round-trip as graphs only (Ring refuses the file, or rnxc refuses part of it, or it does not compile alone), '
          f'{len(failing)} fail; floor {CORPUS_FLOOR} files')
    print(f'l1_check: {"FAIL" if fails else "PASS"} ({len(fails)} failure(s), {time.time() - t0:.0f} s)')
    return 1 if fails else 0


def has_loads(path):
    """A file that loads others compiles against its neighbours; the canonical copy lives elsewhere, so its code is not compared."""
    t = read_text(path).lower()
    return '\nload ' in '\n' + t or '\nimport ' in '\n' + t


def corpus():
    spike = [p for p in sorted(glob.glob(os.path.join(SP, '*.ring'))) if 'GENERATED by forge.ring' not in read_text(p)[:400]]
    probes = sorted(glob.glob(os.path.join(ROOT, 'bench', '*.ring')) + glob.glob(os.path.join(ROOT, 'tests', '*.ring')))
    stdlib = sorted(glob.glob(os.path.join(ROOT, 'vendor', 'ring-stdlib', '**', '*.ring'), recursive=True))
    stz = sorted(glob.glob(os.path.join(STZ, '**', '*.ring'), recursive=True))
    stz = [p for p in stz[::97] if os.path.getsize(p) <= 40_000]
    small = lambda ps, k: [p for p in ps if 300 < os.path.getsize(p) <= 40_000][::k]
    c = small(spike, 3) + small(probes, 9) + small(stdlib, 7) + stz
    return c[:12] if QUICK else c


if __name__ == '__main__':
    sys.setrecursionlimit(200_000)
    threading.stack_size(128 * 1024 * 1024)
    rc = []
    t = threading.Thread(target=lambda: rc.append(main()))
    t.start()
    t.join()
    sys.exit(rc[0] if rc else 1)
