"""body_court.py -- the court of the two scoped body grammars (body_gbnf.py): does the engine's decoder HOLD each, ACCEPT every gold body of the sixteen tasks under its own point's calls and
writes, REJECT what the gate would refuse for the shape, and does the court have teeth? No model is loaded.

    python haro/spike/v20/agent/body_court.py

`one-line` is the shape of the sentence's TO; `lines` is the same body as an agent writes it naturally (a statement a line, a tab a level, a closing sentinel line), which the harness
flattens into the one-line TO.
"""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V22 = os.path.abspath(os.path.join(HERE, '..', '..', 'v22'))
sys.path.insert(0, HERE)
sys.path.insert(0, V22)
import body_gbnf, tasks as T, r5_agent as A
import grammar_court as gc        # the decoder batch driver of the v22 court

LIMIT = 128
BY_ID = {t['id']: t for t in T.TASKS}
ONE_EXCLUDED = [
    ('a call the point does not allow', 'R01', 'return floor(n)\n'),
    ('a function defined inside', 'R01', 'func X() return 1\n'),
    ('a double quote', 'R01', 'return "x"\n'),
    ('a comment', 'R01', 'return n # fast\n'),
    ('a line break', 'R01', 'nS = 0\nreturn nS\n'),
    ('a global written without leave', 'R01', '$nX = 1 return n\n'),
    ('a call by name', 'R01', 'call F()\n'),
    ('a brace block', 'R01', 'return n { x }\n'),
    ('a write to a global the point does not name', 'R16', '$nOther = 1\n'),
    ('no newline at the end', 'R01', 'return xN'),
]
LINES_EXCLUDED = [
    ('a call the point does not allow', 'R01', 'return floor(n)\n<<END>>\n'),
    ('a function defined inside', 'R01', 'func X()\n\treturn 1\n<<END>>\n'),
    ('a double quote', 'R01', 'return "x"\n<<END>>\n'),
    ('a comment', 'R01', '# fast\nreturn n\n<<END>>\n'),
    ('a write to a global the point does not name', 'R16', '$nOther = 1\n<<END>>\n'),
    ('no sentinel', 'R01', 'return nN\n'),
    ('a blank line', 'R01', 'nS = 0\n\nreturn nS\n<<END>>\n'),
    ('indentation deeper than the grammar counts', 'R01', 'if a\n\tif b\n\t\tif c\n\t\t\tif d\n\t\t\t\treturn 1\n\t\t\tok\n\t\tok\n\tok\nok\n<<END>>\n'),
    ('a block closed by the wrong word', 'R01', 'for i = 1 to n\n\tnS += i\nend\n<<END>>\n'),
]


def run_plain(jobs):
    """The v22 court's batch driver, with the sentences as written."""
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


def main():
    jobs = []
    for shape, gram, excluded, gold in (('one-line', body_gbnf.body_grammar, ONE_EXCLUDED, lambda t: t['gold'] + '\n'),
                                        ('lines', body_gbnf.lines_grammar, LINES_EXCLUDED, lambda t: A.multiline_gold(t))):
        for t in T.TASKS:
            jobs.append((shape, 'gold/%s' % t['id'], 'gold', gram(t['calls'], t['writes']), gold(t)))
        for label, tid, text in excluded:
            t = BY_ID[tid]
            jobs.append((shape, 'excluded/%s' % label, 'excluded', gram(t['calls'], t['writes']), text))
        t6 = BY_ID['R06']
        jobs.append((shape, 'control/broken', 'control-reject', gram(t6['calls'], t6['writes']).replace('"for "', '"fr "'), gold(t6)))
        jobs.append((shape, 'control/loosened', 'control-accept', gram('floor', ''), 'return floor(n)\n' + ('<<END>>\n' if shape == 'lines' else '')))
    res = run_plain([(lab, k, g, s) for (shape, lab, k, g, s) in jobs])
    bad = 0
    for shape, gram in (('one-line', body_gbnf.body_grammar), ('lines', body_gbnf.lines_grammar)):
        counts = [body_gbnf.rule_count(gram(t['calls'], t['writes'])) for t in T.TASKS]
        print('%s grammar: about %d to %d rules by the decoder\'s count (limit %d)' % (shape, min(counts), max(counts), LIMIT))
        mine = [(lab, k, r, a) for (sh, lab, k, g, s), (r, a) in zip(jobs, res) if sh == shape]
        held = [lab for lab, k, r, a in mine if r]
        ok = not held and max(counts) <= LIMIT
        print('  %s held by the decoder: %s' % (shape, 'yes' if ok else 'NO -- %s' % (held[:1] or 'rule count')))
        bad += 0 if ok else 1
        for kind, want, what in (('gold', True, 'gold bodies accepted'), ('excluded', False, 'excluded bodies rejected')):
            rows = [(lab, a) for lab, k, r, a in mine if k == kind]
            good = [lab for lab, a in rows if a == want]
            print('  %s %s: %d of %d%s' % (shape, what, len(good), len(rows), '' if len(good) == len(rows) else '   MISSED: ' + ', '.join(lab for lab, a in rows if a != want)))
            bad += 0 if len(good) == len(rows) else 1
        for kind, want, what in (('control-reject', False, 'broken grammar fails a gold body'), ('control-accept', True, 'loosened grammar accepts a forbidden call')):
            rows = [a for lab, k, r, a in mine if k == kind]
            good = all(a == want for a in rows)
            print('  %s control, %s: %s' % (shape, what, 'ok' if good else 'FAIL -- the court has no teeth here'))
            bad += 0 if good else 1
    # the grammar the harness uses is the one derived from the program's own point (scoped.body_lines_gbnf), not a copy built from the task's fields
    import refine, scoped
    same = sum(1 for t in T.TASKS if scoped.body_lines_gbnf(refine.Model(T.program(t, 'a'), {}), t['name']) == body_gbnf.lines_grammar(t['calls'], t['writes']))
    print('  the lines grammar derived from each program\'s own point (scoped.body_lines_gbnf): %d of %d identical to the task-built one%s' % (same, len(T.TASKS), '' if same == len(T.TASKS) else '   MISSED'))
    bad += 0 if same == len(T.TASKS) else 1
    print('BODY COURT %s' % ('PASSED' if not bad else 'FAILED (%d)' % bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
