"""face_read_check.py -- the court of rung 22, the reader of the Python-shaped face (rung 7 of the code-graph memo):
   python haro/spike/v22/face_read_check.py [--plant] [--corpus N] [--quick]      (exit 1 on any failure)

  F  the fixtures (fixtures.txt, written before face_read.py): each text is read to exactly its Ring, or refused for exactly its id and words
  H  the fixtures are honest: every `py` is Python, every `ring` is canonical Ring, and v21's printer, given a fixture's Ring, prints its text wherever the text is
     the printer's own image
  R  the round trip, face to graph to face: every text the printer prints -- the fixtures of v21 and the corpus -- is read, and printing what was read gives the
     same text (a fixed point)
  S  the round trip, judged by the oracle: each of the runnable probes (bench/exec) that the face can spell, printed, read back and run, prints what the original
     printed
  D  controls that must FAIL the fixtures: a reader that takes Python's meaning for `==`, one that reads an index 0-based, one that keeps a binding the handler
     does not use, one that does not insist on the face's spelling, one that forgets the sigil
  K  Softanza's corpus: every file the printer prints whole is read back
  L  and it is read back to the SAME GRAPH, up to the named losses (losses.py: case, parentheses, strings, pairs, assignment, returns, comments, trails, else-if, classes,
     catch, numbers): across faces, L1 to face to L1 is exact; and each loss is needed, shown by taking it out (a control that must fail on the sample)
"""
import ast, collections, glob, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import face_read
import losses
from face_read import face_py, l1, ReadRefused

PLANT = '--plant' in sys.argv
QUICK = '--quick' in sys.argv
CORPUS_N = int(sys.argv[sys.argv.index('--corpus') + 1]) if '--corpus' in sys.argv else 300
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP                            # its bench/exec probes are run on the oracle
STZ = r'D:\GitHub\stzlib\libraries\stzlib'
ORACLE = paths.RING
fails = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def read_fixtures(path):
    fx, cur, sec = [], None, None
    for line in open(path, 'rb').read().decode('latin-1').replace('\r\n', '\n').split('\n'):
        if line.startswith('=== '):
            fid, _, name = line[4:].partition(' ')
            cur = {'id': fid, 'name': name, 'py': None, 'ring': None, 'refused': None, 'lenient': None}
            fx.append(cur)
            sec = None
        elif cur is None or line.startswith('~~~'):
            continue
        elif line.startswith('--- ') and line[4:] in ('py', 'ring', 'refused', 'lenient'):
            sec = line[4:]
            cur[sec] = []
        elif sec:
            cur[sec].append(line)
    for f in fx:
        for s in ('py', 'ring', 'refused', 'lenient'):
            if f[s] is not None:
                while f[s] and f[s][-1] == '':
                    f[s].pop()
        for s in ('py', 'ring', 'lenient'):
            if f[s] is not None:
                f[s] = '\n'.join(f[s]) + '\n'
    return fx


def with_banner(py):
    return face_py.BANNER + '\n' + py


def judge(fx, reader):
    """-> [(fixture id, what is wrong)]"""
    bad = []
    for f in fx:
        text = with_banner(f['py'])
        try:
            got = reader(text, True)
        except (ReadRefused, face_py.Refused) as e:
            if f['refused'] is None:
                bad.append((f['id'], 'refused (%s), want read' % str(e)[:200]))
                continue
            cid, _, words = f['refused'][0].partition(' ')
            if e.cid != cid or words.lower() not in str(e).lower():
                bad.append((f['id'], 'refused as %s (%s), want %s holding "%s"' % (e.cid, str(e)[:160], cid, words)))
                continue
            if f['lenient'] is not None:
                try:
                    lenient = reader(text, False)
                except (ReadRefused, face_py.Refused) as e2:
                    bad.append((f['id'], 'refused leniently too: %s' % str(e2)[:160]))
                    continue
                if lenient != f['lenient']:
                    bad.append((f['id'], 'lenient read:\n%swant:\n%s' % (lenient, f['lenient'])))
            continue
        except Exception as e:
            bad.append((f['id'], 'EXCEPTION %s: %s' % (type(e).__name__, e)))
            continue
        if f['refused'] is not None:
            bad.append((f['id'], 'read, want refused (%s)' % f['refused'][0]))
            continue
        if got != f['ring']:
            bad.append((f['id'], 'read:\n%swant:\n%s' % (got, f['ring'])))
    return bad


def strict_reader(text, strict):
    return face_read.read_ring(text, strict)


# ---- the controls: a reader with one of its rules taken out ------------------------------------------------------------------------------------

class patched:
    def __init__(self, obj, name, value):
        self.obj, self.name, self.value = obj, name, value

    def __enter__(self):
        self.saved = getattr(self.obj, self.name)
        setattr(self.obj, self.name, self.value)

    def __exit__(self, *a):
        setattr(self.obj, self.name, self.saved)


def ctl_zero_based(orig):
    def call(self, n):
        if isinstance(n.func, ast.Name) and n.func.id == 'at' and len(n.args) == 2:
            return face_read.mk('index', obj=face_read.wrap(self.expression(n.args[0])), idx=face_read.mk('bin', op='+', l=self.expression(n.args[1]), r=face_read.mk('num', text='1')))
        return orig(self, n)
    return call


def ctl_python_equality(orig):
    def expression(self, n):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'eq' and len(n.args) == 2:
            return face_read.mk('call', callee=face_read.mk('id', text='pyeq'), args=[self.expression(a) for a in n.args])
        return orig(self, n)
    return expression


def ctl_keep_binding(orig):
    def try_statement(self, s, kind):
        node = orig(self, s, kind)
        if 'catch' in node and 'binding' not in node['catch'] and s.handlers and s.handlers[0].name:
            node['catch']['binding'] = s.handlers[0].name
        return node
    return try_statement


def ctl_no_sigil(orig):
    def attribute(self, n, call):
        if isinstance(n.value, ast.Name) and n.value.id == 'self' and n.attr.startswith('at_') and not call:
            return face_read.mk('id', text=n.attr)
        return orig(self, n, call)
    return attribute


def lenient_reader(text, strict):
    return face_read.read_ring(text, False)


# ---- R: the round trip face -> graph -> face ---------------------------------------------------------------------------------------------------

def round_trip(g):
    """-> None when the printer's text is read and printing the reading gives the same text, else why not."""
    try:
        text = face_py.print_py(g)
    except face_py.Refused:
        return 'refused'
    try:
        g2 = face_read.read_py(text)
    except (ReadRefused, face_py.Refused) as e:
        return 'the printer\'s own text was refused: %s' % str(e)[:200]
    again = face_py.print_py(g2)
    if again != text:
        a, b = text.split('\n'), again.split('\n')
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return 'printing the reading gives another text at line %d: `%s` then `%s`' % (i + 1, x.strip(), y.strip())
        return 'printing the reading gives another length'
    return None


def corpus_files(n):
    files = sorted(glob.glob(os.path.join(STZ, 'base', '**', '*.ring'), recursive=True))
    files = [f for f in files if os.sep + 'test' + os.sep not in f and os.path.getsize(f) < 200_000]
    step = max(1, len(files) // n)
    return files[::step][:n]


def corpus(n):
    sample = corpus_files(n)
    read, refused, unparsed, bad, graphs = 0, collections.Counter(), 0, [], []
    t = time.time()
    for p in sample:
        g, why = l1.parse_ring(p)
        if g is None:
            unparsed += 1
            continue
        r = round_trip(g)
        if r == 'refused':
            refused['printer refuses'] += 1
        elif r is None:
            read += 1
            graphs.append((os.path.relpath(p, STZ), g, face_read.read_py(face_py.print_py(g))))
        else:
            bad.append((os.path.relpath(p, STZ), r))
    return {'sample': len(sample), 'read': read, 'refused': refused, 'unparsed': unparsed, 'bad': bad, 'secs': time.time() - t, 'graphs': graphs}


# ---- S: the oracle ------------------------------------------------------------------------------------------------------------------------------

def run_ring(path, cwd):
    pr = subprocess.run([ORACLE, path], capture_output=True, cwd=cwd, timeout=60, stdin=subprocess.DEVNULL)
    out = (pr.stdout + pr.stderr).decode('latin-1').replace(chr(13) + chr(10), chr(10))
    out = out.replace(path, '<file>').replace(os.path.basename(path), '<file>')
    out = re.sub(r'(?i)\bline \(?\d+\)?', 'Line #', out)       # the face prints the program again, so its lines move
    return pr.returncode, out


def probes():
    """Each runnable probe of bench/exec: its Ring through the face and back, run on the oracle both ways, from one path and one folder."""
    d = os.path.join(ROOT, 'bench', 'exec')
    files = sorted(f for f in glob.glob(os.path.join(d, '*.ring')))
    out = {'tried': 0, 'spelt': 0, 'same': 0, 'refused': collections.Counter(), 'bad': []}
    scratch = tempfile.mkdtemp(prefix='face_read_')
    for p in files:
        out['tried'] += 1
        try:
            g, why = l1.parse_ring(p)
        except Exception:
            g, why = None, 'error'
        if g is None:
            out['refused']['does not parse'] += 1
            continue
        if any(x['k'] == 'load' for x in face_py.walk(g)):
            out['refused']['loads a file'] += 1
            continue
        try:
            text = face_py.print_py(g)
        except face_py.Refused as e:
            out['refused'][e.cid] += 1
            continue
        except Exception:
            out['refused']['no spelling'] += 1
            continue
        out['spelt'] += 1
        try:
            back = face_read.read_ring(text)
        except (ReadRefused, face_py.Refused) as e:
            out['bad'].append((os.path.basename(p), 'refused its own text: %s' % str(e)[:200]))
            continue
        target = os.path.join(scratch, 'prog.ring')
        try:
            open(target, 'wb').write(open(p, 'rb').read())
            ra = run_ring(target, scratch)
            open(target, 'wb').write(back.encode('latin-1'))
            rb = run_ring(target, scratch)
        except subprocess.TimeoutExpired:
            out['bad'].append((os.path.basename(p), 'timed out'))
            continue
        if ra == rb:
            out['same'] += 1
        else:
            la, lb = ra[1].split(chr(10)), rb[1].split(chr(10))
            k = next((i for i, (x, y) in enumerate(zip(la, lb)) if x != y), min(len(la), len(lb)))
            out['bad'].append((os.path.basename(p), 'exit %s/%s, first difference at output line %d: the original `%s`, the reading `%s`' % (
                ra[0], rb[0], k + 1, (la[k] if k < len(la) else '')[:90], (lb[k] if k < len(lb) else '')[:90])))
    return out


def main():
    t0 = time.time()
    print('face_read_check -- the reader of the Python-shaped face (rung 22)')
    fx = read_fixtures(os.path.join(HERE, 'fixtures.txt'))
    bad = judge(fx, strict_reader)
    for fid, why in bad[:14]:
        print('  FAIL F %s: %s' % (fid, why))
    nref = sum(1 for f in fx if f['refused'] is not None)
    check(not bad and len(fx) >= 55, 'F %d fixtures, written before the reader: %d are read to exactly their Ring, %d are refused for exactly their id and words (%d fail)'
          % (len(fx), len(fx) - nref, nref, len(bad)))

    # H: the fixtures are honest
    problems = []
    for f in fx:
        try:
            ast.parse(f['py'])
        except SyntaxError:
            if f['id'] != 'X01':
                problems.append('%s: py is not Python' % f['id'])
        for key in ('ring', 'lenient'):
            if f[key] is not None:
                try:
                    if l1.print_ring(face_py.parse_text(f[key])) != f[key]:
                        problems.append('%s: %s is not canonical Ring' % (f['id'], key))
                except ValueError:
                    problems.append('%s: %s does not parse as Ring' % (f['id'], key))
    own = 0
    for f in fx:
        if f['ring'] is not None:
            try:
                if face_py.print_py(face_py.parse_text(f['ring'])).split('\n', 1)[1] == f['py']:
                    own += 1
            except Exception:
                pass
    check(not problems, 'H the fixtures are honest: every text is Python, every Ring is canonical Ring (%s); %d of the %d read texts are v21\'s own image of their Ring'
          % ('; '.join(problems[:3]) or 'none out of place', own, len(fx) - nref))

    # R on v21's fixtures
    v21 = []
    sys.path.insert(0, os.path.join(HERE, '..', 'v21'))
    import face_check
    for f in face_check.read_fixtures(os.path.join(HERE, '..', 'v21', 'fixtures.txt')):
        if f['refused'] is None:
            v21.append((f['id'], face_py.parse_text(f['ring'])))
    rt = [(i, round_trip(g)) for i, g in v21]
    badrt = [(i, r) for i, r in rt if r]
    for i, r in badrt[:8]:
        print('  FAIL R v21 fixture %s: %s' % (i, r))
    check(not badrt, 'R the %d fixtures v21 prints are read back from the printer\'s own text, and printing the reading gives the same text (%d fail)' % (len(v21), len(badrt)))

    for label, obj, name, wrap_fn, reader, floor in (
            ('a reader that takes Python\'s meaning for eq()', face_read.Reader, 'expression', ctl_python_equality, strict_reader, 1),
            ('a reader that reads an index 0-based', face_read.Reader, 'call', ctl_zero_based, strict_reader, 1),
            ('a reader that keeps a binding the handler does not use', face_read.Reader, 'try_statement', ctl_keep_binding, strict_reader, 1),
            ('a reader that does not insist on the face\'s spelling', None, None, None, lenient_reader, 1),
            ('a reader that forgets the sigil of at_', face_read.Reader, 'attribute', ctl_no_sigil, strict_reader, 1)):
        if obj is None:
            nbad = len(judge(fx, reader))
        else:
            with patched(obj, name, wrap_fn(getattr(obj, name))):
                nbad = len(judge(fx, reader))
        check(nbad >= floor, 'D the control, %s, fails %d fixture(s) (at least %d)' % (label, nbad, floor))

    if os.path.isdir(STZ):
        c = corpus(CORPUS_N)
        for p, r in c['bad'][:8]:
            print('  FAIL K %s: %s' % (p, r))
        check(not c['bad'], 'K %d files of Softanza\'s base (%.0f s): %d print whole and are read back from their own text to the same text, %d are refused by the printer, '
                            '%d do not parse as Ring (%d fail)' % (c['sample'], c['secs'], c['read'], sum(c['refused'].values()), c['unparsed'], len(c['bad'])))
        # L: the same graph, up to the declared losses
        graphs = list(c['graphs'])
        for text in ('x = 9007199254740993.0\n', 'try\n\tx = 1\ncatch(e)\n\t? cCatchError\ndone\n'):       # the two losses a sample of library files does not show
            g = face_py.parse_text(text)
            graphs.append(('synthetic: ' + text.split(chr(10))[0], g, face_read.read_py(face_py.print_py(g))))
        lossy = []
        for name, g, g2 in graphs:
            a, b = losses.declared(g), losses.declared(g2)
            if a != b:
                lossy.append((name, losses.first_difference(a, b)))
        for name, d in lossy[:8]:
            print('  FAIL L %s: %s' % (name, d))
        check(not lossy, 'L %d files and 2 synthetic: graph to face to graph is exact up to the %d declared losses (%d are not)' % (len(c['graphs']), len(losses.ALL), len(lossy)))
        needed = []
        for loss in losses.ALL:
            losses.ON.discard(loss)
            try:
                nbad = sum(1 for name, g, g2 in graphs if losses.declared(g) != losses.declared(g2))
            finally:
                losses.ON.add(loss)
            needed.append((loss, nbad))
        missing = [l for l, k in needed if k == 0]
        check(not missing, 'D the controls, each of the %d declared losses taken out in turn, fail on the sample (files that no longer compare equal): %s'
              % (len(losses.ALL), ', '.join('%s %d' % lk for lk in needed)))
    else:
        print('  SKIP K the Softanza tree is not at %s' % STZ)

    if os.path.exists(ORACLE) and not QUICK:
        s = probes()
        for p, r in s['bad'][:8]:
            print('  FAIL S %s: %s' % (p, r))
        top = ', '.join('%s %d' % kv for kv in s['refused'].most_common(6))
        check(not s['bad'] and s['spelt'] >= 20, 'S %d probes of bench/exec: %d spelt by the face (the rest refused: %s), each printed, read back and run on the oracle: %d print what the original '
                                                  'prints (%d differ)' % (s['tried'], s['spelt'], top, s['same'], len(s['bad'])))
    else:
        print('  SKIP S %s' % ('--quick' if QUICK else 'the oracle is not at %s' % ORACLE))

    if PLANT:
        fails.append('PLANTED')
        print('  FAIL PLANTED')
    print('face_read_check: %s (%d failure(s), %.0f s)' % ('FAIL' if fails else 'PASS', len(fails), time.time() - t0))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
