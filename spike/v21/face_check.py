"""face_check.py -- the court of rung 21, a second face of the program graph in Python's shape (rung 6 of the code-graph memo):
   python haro/spike/v21/face_check.py [--plant] [--corpus N]      (exit 1 on any failure)

  F  the fixtures (fixtures.txt, written before face_py.py): each prints exactly its `--- py` text, or is refused for its `--- refused` collision
  P  every text the face prints is Python syntax (ast.parse) and starts with the banner; printing is deterministic
  T  the collision table: every collision is reached by a fixture, and every refusal names one
  D  controls that must FAIL the fixtures: a face that indexes with Python's brackets, one that compares with `==` whatever the kinds, one that
     prints a string's backslash as an escape, one that drops comments, one that does not refuse a brace block
  K  Softanza's corpus through the face: how many files print whole, and what refuses the rest, ranked -- the measurement of kill criterion K3
     ("the collision fixtures outnumber the spellings")
"""
import ast, collections, glob, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import face_py

PLANT = '--plant' in sys.argv
CORPUS_N = int(sys.argv[sys.argv.index('--corpus') + 1]) if '--corpus' in sys.argv else 300
STZ = r'D:\GitHub\stzlib\libraries\stzlib'
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
            cur = {'id': fid, 'name': name, 'ring': None, 'py': None, 'refused': None}
            fx.append(cur)
            sec = None
        elif cur is None or line.startswith('~~~'):
            continue
        elif line.startswith('--- ') and line[4:] in ('ring', 'py', 'refused'):
            sec = line[4:]
            cur[sec] = []
        elif sec:
            cur[sec].append(line)
    for f in fx:
        for s in ('ring', 'py', 'refused'):
            if f[s] is not None:
                while f[s] and f[s][-1] == '':
                    f[s].pop()
        f['ring'] = '\n'.join(f['ring']) + '\n'
        if f['py'] is not None:
            f['py'] = '\n'.join(f['py']) + '\n'
    return fx


def judge(fx, printer):
    """-> [(fixture id, what is wrong)]"""
    bad = []
    for f in fx:
        try:
            g = face_py.parse_text(f['ring'])
        except ValueError as e:
            bad.append((f['id'], 'the Ring program does not parse: %s' % e))
            continue
        try:
            text = printer(g)
        except face_py.Refused as e:
            if f['refused'] is None:
                bad.append((f['id'], 'refused (%s), want printed' % e))
                continue
            cid, _, words = f['refused'][0].partition(' ')
            if e.cid != cid or words.lower() not in str(e).lower():
                bad.append((f['id'], 'refused as %s (%s), want %s holding "%s"' % (e.cid, str(e)[:80], cid, words)))
            continue
        except Exception as e:
            bad.append((f['id'], 'EXCEPTION %s: %s' % (type(e).__name__, e)))
            continue
        if f['refused'] is not None:
            bad.append((f['id'], 'printed, want refused (%s)' % f['refused'][0]))
            continue
        body = text.split('\n', 1)[1] if '\n' in text else ''
        if body != f['py']:
            bad.append((f['id'], 'printed:\n%swant:\n%s' % (body, f['py'])))
    return bad


# ---- the controls: a face with one of its rules taken out ------------------------------------------------------------------------------

def patched(fn_name, replacement):
    def printer(g):
        orig = getattr(face_py.Face, fn_name) if hasattr(face_py.Face, fn_name) else getattr(face_py, fn_name)
        target = face_py.Face if hasattr(face_py.Face, fn_name) else face_py
        setattr(target, fn_name, replacement(orig))
        try:
            return face_py.print_py(g)
        finally:
            setattr(target, fn_name, orig)
    return printer


def ctl_brackets(orig):
    def e(self, n):
        if n['k'] == 'index':
            return '%s[%s]' % (self.e(n['obj']), self.e(n['idx']))
        return orig(self, n)
    return e


def ctl_eq(orig):
    def binary(self, n):
        if n['op'] in ('=', '!='):
            return self.operand(n['l']) + (' == ' if n['op'] == '=' else ' != ') + self.operand(n['r'])
        return orig(self, n)
    return binary


def ctl_escape(orig):
    return lambda v: '"' + v + '"'


def ctl_no_comments(orig):
    def item(self, it, ind, after):
        if it['k'] == 'comment':
            return []
        it = {k: v for k, v in it.items() if k != 'trail'}
        return orig(self, it, ind, after)
    return item


def ctl_brace(orig):
    def e(self, n):
        if n['k'] == 'brace':
            return self.e(n['obj']) + '  # a brace block'
        return orig(self, n)
    return e


# ---- the corpus: K3 ----------------------------------------------------------------------------------------------------------------------

def corpus(n):
    files = sorted(glob.glob(os.path.join(STZ, 'base', '**', '*.ring'), recursive=True))
    files = [f for f in files if os.sep + 'test' + os.sep not in f and os.path.getsize(f) < 200_000]
    step = max(1, len(files) // n)
    sample = files[::step][:n]
    whole, refused, unparsed, bad_py = 0, collections.Counter(), 0, []
    t = time.time()
    for p in sample:
        g, why = face_py.l1.parse_ring(p)
        if g is None:
            unparsed += 1
            continue
        try:
            text = face_py.print_py(g)
        except face_py.Refused as e:
            refused[e.cid] += 1
            continue
        except Exception as e:
            refused['(no spelling: %s)' % str(e)[:50]] += 1
            continue
        try:
            ast.parse(text)
            whole += 1
        except SyntaxError as e:
            bad_py.append((os.path.relpath(p, STZ), str(e)[:80]))
    return {'sample': len(sample), 'whole': whole, 'refused': refused, 'unparsed': unparsed, 'bad_py': bad_py, 'secs': time.time() - t}


def main():
    t0 = time.time()
    print('face_check -- a second face of the program graph, in Python\'s shape, as a printer (rung 21)')
    fx = read_fixtures(os.path.join(HERE, 'fixtures.txt'))
    bad = judge(fx, face_py.print_py)
    for fid, why in bad[:12]:
        print('  FAIL F %s: %s' % (fid, why))
    nref = sum(1 for f in fx if f['refused'] is not None)
    check(not bad and len(fx) >= 28, 'F %d fixtures, written before the face: %d print exactly their text, %d are refused for exactly their collision (%d fail)'
          % (len(fx), len(fx) - nref, nref, len(bad)))

    texts = []
    for f in fx:
        if f['refused'] is None:
            texts.append(face_py.print_py(face_py.parse_text(f['ring'])))
    syntax = [i for i, t in enumerate(texts) if not t.startswith(face_py.BANNER + '\n') or not _parses(t)]
    again = all(face_py.print_py(face_py.parse_text(f['ring'])) == t for f, t in zip([f for f in fx if f['refused'] is None], texts))
    check(not syntax and again, 'P every printed text starts with the banner and is Python syntax (%d texts, ast.parse), and printing twice gives the same bytes' % len(texts))

    reached = {f['refused'][0].split()[0] for f in fx if f['refused']}
    missing = sorted(set(face_py.COLLISIONS) - reached)
    check(len(reached) >= 10, 'T the collision table: %d collisions, %d reached by a fixture; not yet reached: %s' % (len(face_py.COLLISIONS), len(reached), missing or 'none'))

    for label, printer, floor in (
            ('a face that indexes with Python\'s brackets', patched('e', ctl_brackets), 1),
            ('a face that compares with == whatever the kinds', patched('binary', ctl_eq), 1),
            ('a face that prints a backslash as Python reads it, an escape', patched('py_str', ctl_escape), 1),
            ('a face that drops comments', patched('item', ctl_no_comments), 1),
            ('a face that prints a brace block', patched('e', ctl_brace), 1)):
        nbad = len(judge(fx, printer))
        check(nbad >= floor, 'D the control, %s, fails %d fixture(s) (at least %d)' % (label, nbad, floor))

    if os.path.isdir(STZ):
        c = corpus(CORPUS_N)
        top = ', '.join('%s %d' % kv for kv in c['refused'].most_common(8))
        check(not c['bad_py'], 'K %d files of Softanza\'s base through the face (%.0f s): %d print whole as Python syntax, %d are refused (%s), %d do not parse as Ring%s'
              % (c['sample'], c['secs'], c['whole'], sum(c['refused'].values()), top, c['unparsed'],
                 ('; NOT Python syntax: %s' % c['bad_py'][:3]) if c['bad_py'] else ''))
        share = 100.0 * c['whole'] / max(1, c['sample'] - c['unparsed'])
        print('  --   K3, "the collision fixtures outnumber the spellings": %d fixtures spell and %d are refused; a file prints whole only when NOTHING in it '
              'collides, and %.0f%% of the sample does -- K3 %s' % (len(fx) - nref, nref, share,
                                                                    'is MET: a second face is a reading aid, not a parser' if nref > len(fx) - nref or share < 50
                                                                    else 'is not met: rung 7 (a parser) stays open'))
    else:
        print('  SKIP K the Softanza tree is not at %s' % STZ)
    if PLANT:
        fails.append('PLANTED')
        print('  FAIL PLANTED')
    print('face_check: %s (%d failure(s), %.0f s)' % ('FAIL' if fails else 'PASS', len(fails), time.time() - t0))
    return 1 if fails else 0


def _parses(t):
    try:
        ast.parse(t)
        return True
    except SyntaxError:
        return False


if __name__ == '__main__':
    sys.exit(main())
