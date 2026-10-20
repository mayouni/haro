"""grammar_court.py -- the court of the two write-surface grammars (face_gbnf.py, ringpp_gbnf.py): does the engine's constrained decoder HOLD each, ACCEPT what each shape's own printer prints,
REJECT what the shape excludes, and does the court itself have teeth?

    python haro/spike/v22/grammar_court.py            ~15 s; needs the Ring++ package (runtime/package/ringpp-win64) and zig-out/bin/rnxc.exe; no model is loaded

It asks the decoder itself -- StzGrammarRefusal and StzGrammarAccepts, in one batch on the package (the v20 driver gbnf_batch.ring) -- so a rule count or a dialect fault is the engine's own verdict.
  held        the decoder holds the grammar (no refusal), and its rule count is under the decoder's 128
  gold        the twenty K4 programs, each as the shape's own printer writes it (the face by face_py.print_py, Ring++ by `rnxc fmt`), ending in the sentinel: ALL accepted
  fixtures    the printer's text for every v21 fixture the shape can print: the count accepted, each miss NAMED (a miss is a construct outside the grammar's core, not a failure, but it is said)
  excluded    texts the shape excludes: ALL rejected
  controls    a grammar broken on purpose must FAIL a gold text, and a grammar loosened on purpose must ACCEPT an excluded one -- or the court proves nothing
No model is loaded, so this runs in the guard. It judges SHAPE; the reader (face_read.py) and rnxc judge the rest.
"""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'v21'))
sys.path.insert(0, os.path.join(HERE, 'k4'))
import face_gbnf, ringpp_gbnf, face_py, face_check
import tasks as K4TASKS

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PACKAGE = os.environ.get('PKG_RNXC') or os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
BATCH = os.path.join(ROOT, 'haro', 'spike', 'v20', 'probes', 'gbnf_batch.ring')
END = face_gbnf.END
LIMIT = 128


def with_data(task, which='a'):
    return '\n'.join(task[which]) + '\n' + task['ref']


def fmt_ring(text):
    """The canonical Ring++ text `rnxc fmt` prints for a program, or None when the formatter refuses it."""
    d = tempfile.mkdtemp(prefix='gc_')
    p = os.path.join(d, 'p.ring')
    open(p, 'wb').write(text.encode('latin-1', 'replace'))
    r = subprocess.run([RNXC, 'fmt', '--write', p], capture_output=True, stdin=subprocess.DEVNULL, timeout=60)
    if r.returncode != 0:
        return None
    return open(p, 'rb').read().decode('latin-1').replace('\r\n', '\n')


def face_text(ring):
    return face_py.print_py(face_py.parse_text(ring))


def with_end(text):
    return text.rstrip('\n') + '\n' + END + '\n'


# -- what each shape excludes: (id, text) -----------------------------------------------------------------------------------------------------------------
FACE_EXCLUDED = [
    ('subscript', 'x = a[1]\n'),
    ('lambda', 'f = lambda x: x\n'),
    ('import', 'import os\n'),
    ('f-string', 'say(f"a{b}")\n'),
    ('class before a statement', 'class K:\n    def M(self):\n        return 1\nx = 1\n'),
    ('def before a statement', 'def f():\n    return 1\nx = 1\n'),
    ('method without self', 'class K:\n    def M():\n        return 1\n'),
    ('else on a loop', 'for i in span(1, 3):\n    say(i)\nelse:\n    say(0)\n'),
    ('a bare name as a statement', 'x\n'),
    ('conditional expression', 'x = 1 if a else 2\n'),
    ('keyword argument', 'say(end="")\n'),
    ('plain except', 'try:\n    f()\nexcept:\n    g()\n'),
    ('tab indentation', 'if x:\n\tsay(1)\n'),
    ('no sentinel', None),     # handled below: a gold text without its sentinel
]
RING_EXCLUDED = [
    ('if without ok', 'if x\n\t? 1\n'),
    ('loop closed by the wrong word', 'for i = 1 to 3\n\t? i\nend\n'),
    ('Python def', 'def f(x):\n    return x\n'),
    ('print without parentheses', 'print x\n'),
    ('unbalanced bracket', 'x = [1, 2\n'),
    ('a bare name as a statement', 'x\n'),
    ('then', 'if x then\n\t? 1\nok\n'),
    ('a statement in a class body', 'class K\n\t? 1\n'),
    ('indentation deeper than the grammar counts', 'if a\n\tif b\n\t\tif c\n\t\t\tif d\n\t\t\t\tif e\n\t\t\t\t\t? 1\n\t\t\t\tok\n\t\t\tok\n\t\tok\n\tok\nok\n'),
    ('Python comparison chain with ==', 'if x == 1\n\t? 1\nok\n'),
    ('no sentinel', None),
]


def jobs_for(shape, gold, fixtures, excluded, grammar_text, broken, loosened):
    """-> [(label, kind, grammar text, sentence text)]"""
    out = []
    for gid, t in gold:
        out.append(('%s/gold/%s' % (shape, gid), 'gold', grammar_text, with_end(t)))
    for fid, t in fixtures:
        out.append(('%s/fixture/%s' % (shape, fid), 'fixture', grammar_text, with_end(t)))
    for xid, t in excluded:
        if t is None:
            t = gold[0][1].rstrip('\n') + '\n'            # a gold text with no sentinel: the decoder has not been told it is finished
            out.append(('%s/excluded/%s' % (shape, xid), 'excluded', grammar_text, t))
        else:
            out.append(('%s/excluded/%s' % (shape, xid), 'excluded', grammar_text, with_end(t)))
    # controls: the broken grammar must reject a gold text, the loosened one must accept an excluded text
    out.append(('%s/control/broken' % shape, 'control-reject', broken, with_end(gold[2][1])))
    out.append(('%s/control/loosened' % shape, 'control-accept', loosened[0], with_end(loosened[1])))
    return out


def run_batch(jobs):
    d = tempfile.mkdtemp(prefix='gcourt_')
    man, gfiles = [], {}
    for i, (label, kind, g, s) in enumerate(jobs):
        gi = gfiles.setdefault(g, 'g%d.gbnf' % len(gfiles))
        if not os.path.exists(os.path.join(d, gi)):
            open(os.path.join(d, gi), 'wb').write(g.encode('latin-1'))
        open(os.path.join(d, 's%d.txt' % i), 'wb').write(s.encode('latin-1', 'replace'))
        man.append('%s|s%d.txt' % (gi, i))
    open(os.path.join(d, 'm.txt'), 'wb').write('\n'.join(man).encode('latin-1'))
    r = subprocess.run([PACKAGE, BATCH, os.path.join(d, 'm.txt'), d], capture_output=True, cwd=ROOT, timeout=1800)
    res = {}
    for ln in r.stdout.decode('latin-1').replace('\r\n', '\n').split('\n'):
        if ln.startswith('J|'):
            _, j, refusal, a = (ln.split('|', 3) + ['', ''])[:4]
            res[int(j) - 1] = (refusal, a.strip() == '1')
    if len(res) != len(jobs):
        raise SystemExit('the batch answered %d of %d jobs; stderr: %s' % (len(res), len(jobs), r.stderr.decode('latin-1')[:300]))
    return [res[i] for i in range(len(jobs))]


def main():
    face_g, rpp_g = face_gbnf.face_grammar(), ringpp_gbnf.ringpp_grammar()
    # the controls' grammars
    face_broken = face_g.replace('"for "', '"fr "')
    face_loose = re.sub(r'^trailer ::= (.*)$', lambda m: 'trailer ::= ' + m.group(1) + ' | "[" expr "]"', face_g, flags=re.M)
    rpp_broken = rpp_g.replace('"for "', '"fr "')
    rpp_loose = rpp_g.replace('" ok" ', '"ok"').replace('"ok"', '("ok" | "end")')
    assert face_loose != face_g and rpp_loose != rpp_g and face_broken != face_g and rpp_broken != rpp_g

    face_gold, rpp_gold, face_fx, rpp_fx, rpp_skipped = [], [], [], [], []
    hint = {}
    for t in K4TASKS.TASKS:
        face_gold.append((t['id'], face_text(with_data(t))))
        f = fmt_ring(with_data(t))
        if f is None:
            raise SystemExit('rnxc fmt refuses the reference of %s' % t['id'])
        rpp_gold.append((t['id'], f))
    for f in face_check.read_fixtures(os.path.join(HERE, '..', 'v21', 'fixtures.txt')):
        if f['refused'] is not None:
            continue
        face_fx.append((f['id'], face_text(f['ring'])))
        hint[str(f['id'])] = re.sub(r'\s+', ' ', f['ring'])[:44]
        g = fmt_ring(f['ring'])
        if g is None:
            rpp_skipped.append(f['id'])
        else:
            rpp_fx.append((f['id'], g))

    jobs = (jobs_for('face', face_gold, face_fx, FACE_EXCLUDED, face_g, face_broken, (face_loose, 'x = a[1]\n'))
            + jobs_for('ringpp', rpp_gold, rpp_fx, RING_EXCLUDED, rpp_g, rpp_broken, (rpp_loose, 'if x\n\t? 1\nend\n')))
    results = run_batch(jobs)

    bad = 0
    print('grammars: face %d named rules (about %d by the decoder\'s count), Ring++ %d (about %d); the decoder\'s limit is %d'
          % (len(re.findall(r'^\w+ ::=', face_g, re.M)), face_gbnf.rule_count(face_g), len(re.findall(r'^\w+ ::=', rpp_g, re.M)), ringpp_gbnf.rule_count(rpp_g), LIMIT))
    for shape, g in (('face', face_g), ('ringpp', rpp_g)):
        count = (face_gbnf if shape == 'face' else ringpp_gbnf).rule_count(g)
        refused = [r for (lab, kind, gg, s), (r, a) in zip(jobs, results) if lab.startswith(shape + '/') and gg == g and r]
        ok = not refused and count <= LIMIT
        print('  %s held: %s' % (shape, 'yes' if ok else 'NO -- %s' % (refused[:1] or ['rule count %d over %d' % (count, LIMIT)])))
        bad += 0 if ok else 1
        mine = [(lab, kind, a, r) for (lab, kind, gg, s), (r, a) in zip(jobs, results) if lab.startswith(shape + '/')]
        for kind, want, what in (('gold', True, 'K4 gold texts accepted'), ('excluded', False, 'excluded texts rejected')):
            rows = [m for m in mine if m[1] == kind]
            good = [m for m in rows if m[2] == want and not m[3]]
            ok = len(good) == len(rows)
            print('  %s %s: %d of %d%s' % (shape, what, len(good), len(rows), '' if ok else '   MISSED: ' + ', '.join(m[0].split('/', 2)[2] for m in rows if m not in good)))
            bad += 0 if ok else 1
        rows = [m for m in mine if m[1] == 'fixture']
        acc = [m for m in rows if m[2] and not m[3]]
        print('  %s v21 fixtures accepted: %d of %d printed' % (shape, len(acc), len(rows)))
        for m in rows:
            if m not in acc:
                print('      not accepted: %-4s %s' % (m[0].split('/', 2)[2], hint.get(m[0].split('/', 2)[2], '')))
        if shape == 'ringpp' and rpp_skipped:
            print('  ringpp fixtures `rnxc fmt` refuses (not counted): %s' % ', '.join(rpp_skipped))
        for kind, want, what in (('control-reject', False, 'broken grammar fails a gold text'), ('control-accept', True, 'loosened grammar accepts an excluded text')):
            rows = [m for m in mine if m[1] == kind]
            ok = all(m[2] == want and not m[3] for m in rows)
            print('  %s control, %s: %s' % (shape, what, 'ok' if ok else 'FAIL -- the court has no teeth here'))
            bad += 0 if ok else 1
    print('GRAMMAR COURT %s' % ('PASSED' if not bad else 'FAILED (%d)' % bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
