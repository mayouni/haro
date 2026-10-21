"""body_court.py -- the court of the scoped body grammar (body_gbnf.py): does the engine's decoder HOLD it, ACCEPT every gold body of the sixteen tasks under its own point's calls and
writes, REJECT what the gate would refuse for the shape, and does the court have teeth? No model is loaded.

    python haro/spike/v20/agent/body_court.py
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
V22 = os.path.abspath(os.path.join(HERE, '..', '..', 'v22'))
sys.path.insert(0, HERE)
sys.path.insert(0, V22)
import body_gbnf, tasks as T
import grammar_court as gc        # the decoder batch driver of the v22 court

LIMIT = 128
GOLD = [(t['id'], t, t['gold'] + '\n') for t in T.TASKS]
# what the shape excludes, each against a point that allows no call and no write (R01) unless it says
EXCLUDED = [
    ('a call the point does not allow', 'R01', 'return floor(n)\n'),
    ('a function defined inside', 'R01', 'func X() return 1\n'),
    ('a double quote', 'R01', 'return "x"\n'),
    ('a comment', 'R01', 'return n # fast\n'),
    ('a line break', 'R01', 'nS = 0\nreturn nS\n'),
    ('a global written without leave', 'R01', '$nX = 1 return n\n'),
    ('a call by name', 'R01', 'call F()\n'),
    ('a brace block', 'R01', 'return n { x }\n'),
    ('a write to a global the point does not name', 'R16', '$nOther = 1\n'),
    ('no newline at the end', 'R01', 'return n'),
]


def main():
    by_id = {t['id']: t for t in T.TASKS}
    jobs = []
    for tid, t, body in GOLD:
        g = body_gbnf.body_grammar(t['calls'], t['writes'])
        jobs.append(('gold/%s' % tid, 'gold', g, body))
    for label, tid, text in EXCLUDED:
        t = by_id[tid]
        jobs.append(('excluded/%s' % label, 'excluded', body_gbnf.body_grammar(t['calls'], t['writes']), text))
    g1 = body_gbnf.body_grammar(by_id['R06']['calls'], by_id['R06']['writes'])
    jobs.append(('control/broken', 'control-reject', g1.replace('"for "', '"fr "'), by_id['R06']['gold'] + '\n'))
    loose = body_gbnf.body_grammar('floor', '')
    jobs.append(('control/loosened', 'control-accept', loose, 'return floor(n)\n'))
    res = gc.run_batch_plain(jobs) if hasattr(gc, 'run_batch_plain') else None
    if res is None:
        # the v22 driver wants (label, kind, grammar, sentence) quadruples and appends the sentinel through with_end; use its lower-level call
        res = run_plain(jobs)
    bad = 0
    counts = [body_gbnf.rule_count(body_gbnf.body_grammar(t['calls'], t['writes'])) for t in T.TASKS]
    print('body grammar: about %d to %d rules by the decoder\'s count (limit %d)' % (min(counts), max(counts), LIMIT))
    held = [(lab, r) for (lab, k, g, s), (r, a) in zip(jobs, res) if r]
    ok = not held and max(counts) <= LIMIT
    print('  held by the decoder: %s' % ('yes' if ok else 'NO -- %s' % (held[:1] or 'rule count')))
    bad += 0 if ok else 1
    for kind, want, what in (('gold', True, 'gold bodies accepted'), ('excluded', False, 'excluded bodies rejected')):
        rows = [(lab, a) for (lab, k, g, s), (r, a) in zip(jobs, res) if k == kind]
        good = [lab for lab, a in rows if a == want]
        print('  %s: %d of %d%s' % (what, len(good), len(rows), '' if len(good) == len(rows) else '   MISSED: ' + ', '.join(lab for lab, a in rows if a != want)))
        bad += 0 if len(good) == len(rows) else 1
    for kind, want, what in (('control-reject', False, 'broken grammar fails a gold body'), ('control-accept', True, 'loosened grammar accepts a forbidden call')):
        rows = [a for (lab, k, g, s), (r, a) in zip(jobs, res) if k == kind]
        good = all(a == want for a in rows)
        print('  control, %s: %s' % (what, 'ok' if good else 'FAIL -- the court has no teeth here'))
        bad += 0 if good else 1
    print('BODY COURT %s' % ('PASSED' if not bad else 'FAILED (%d)' % bad))
    return 1 if bad else 0


def run_plain(jobs):
    """The v22 court's batch driver, with the sentences as written (no sentinel)."""
    import subprocess, tempfile
    d = tempfile.mkdtemp(prefix='bcourt_')
    man, gfiles = [], {}
    for i, (label, kind, g, s) in enumerate(jobs):
        gi = gfiles.setdefault(g, 'g%d.gbnf' % len(gfiles))
        open(os.path.join(d, gi), 'wb').write(g.encode('latin-1'))
        open(os.path.join(d, 's%d.txt' % i), 'wb').write(s.encode('latin-1', 'replace'))
        man.append('%s|s%d.txt' % (gi, i))
    open(os.path.join(d, 'm.txt'), 'wb').write('\n'.join(man).encode('latin-1'))
    r = subprocess.run([gc.PACKAGE, gc.BATCH, os.path.join(d, 'm.txt'), d], capture_output=True, cwd=gc.ROOT, timeout=1800)
    out = {}
    for ln in r.stdout.decode('latin-1').replace('\r\n', '\n').split('\n'):
        if ln.startswith('J|'):
            _, j, refusal, a = (ln.split('|', 3) + ['', ''])[:4]
            out[int(j) - 1] = (refusal, a.strip() == '1')
    if len(out) != len(jobs):
        raise SystemExit('the batch answered %d of %d jobs' % (len(out), len(jobs)))
    return [out[i] for i in range(len(jobs))]


if __name__ == '__main__':
    sys.exit(main())
