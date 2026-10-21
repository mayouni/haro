"""r5_agent.py -- a MODEL as the agent of rung 5: it writes the body of one function against a point, the gate judges it, the program runs.

    python r5_agent.py build        the expected outputs, and the proof that the harness is sound (gold bodies admitted and right on both data sets; a body that returns the
                                    shown answer admitted and wrong on the other; each rule of the gate refusing what it should)
    python r5_agent.py selftest     the same, without writing expected.json

(the model runs are added below `judge`.) The agent's whole output is the BODY: one line, statements separated by single spaces. The harness wraps it in the sentence
(TARGET, KIND, FROM, AUTHOR, POSTURE, REASON are the harness's: an agent run under a posture cannot write a stronger one, charter 6.2) and puts it through
refine.Model.refine -- the gate's five stages in stzRefinableCode's order -- and then runs the refined program on rnxc, on the shown data and on the checker's.

Scores, taken at the floor like K4's: SHAPE (the body is one line the gate can read: the structural stage), ADMITTED (every stage), RUNS (no error), SHOWN (the right answer
on the shown data), BOTH (and on the substituted data). Ring++ is the baseline and rnxc the judge; the oracle only guards that the gold answers agree.
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V20 = os.path.abspath(os.path.join(HERE, '..'))
for p in (V20, os.path.join(V20, '..', 'v18')):
    sys.path.insert(0, os.path.abspath(p))
import refine
import tasks as T

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
ORACLE = os.environ.get('RING') or os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
SCRATCH = tempfile.mkdtemp(prefix='r5a_')


def run_text(text, exe=None):
    p = os.path.join(SCRATCH, 'p.ring')
    open(p, 'wb').write(text.encode('latin-1', 'replace'))
    try:
        r = subprocess.run([exe or RNXC, p], capture_output=True, cwd=SCRATCH, timeout=15, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', 'timeout', 124
    return r.stdout.decode('latin-1').replace('\r\n', '\n'), r.stderr.decode('latin-1'), r.returncode


def norm(s):
    return '\n'.join(l.rstrip() for l in s.replace('\r\n', '\n').split('\n')).rstrip('\n')


def lift_from(t, which='a'):
    """The FROM the sentence must carry: what the lift shows for the task's point."""
    m = refine.Model(T.program(t, which), {})
    pts = m.lift()['points']
    return m, [p for p in pts if p['name'] == t['name']][0]['value']


def apply_body(t, body, which):
    """-> (outcome, program after or None): the body, as a sentence, through the gate on the task's program with data set `which`."""
    m, frm = lift_from(t, which)
    out = m.refine(T.sentence(t, body, frm))
    return out, (m.text() if out.admitted else None)


def expected():
    exp = {}
    for t in T.TASKS:
        exp[t['id']] = {}
        for w in ('a', 'b'):
            out, text = apply_body(t, t['gold'], w)
            if not out.admitted:
                raise SystemExit('%s/%s: the gate refuses the gold body: %s %s' % (t['id'], w, out.stage, out.why))
            got = norm(run_text(text)[0])
            if norm(run_text(text, ORACLE)[0]) != got:
                raise SystemExit('%s/%s: rnxc and the oracle disagree on the reference -- a finding, not a task' % (t['id'], w))
            exp[t['id']][w] = got
    return exp


def selftest(write=True):
    bad = []
    for t in T.TASKS:
        for w in ('a', 'b'):
            m = refine.Model(T.program(t, w), {})
            if m.text() != T.program(t, w):
                bad.append('%s/%s: the program is not its own canonical text' % (t['id'], w))
    if bad:
        for b in bad:
            print('  PROBLEM', b)
        return 1
    exp = expected()
    for t in T.TASKS:
        a, b = exp[t['id']]['a'], exp[t['id']]['b']
        if not a or not b or a == b:
            bad.append('%s: the two data sets must give two different non-empty answers (%r, %r)' % (t['id'], a, b))
    # a body that returns the shown answer: admitted, right on the shown data, wrong on the other
    hard = 0
    for t in T.TASKS:
        lit = exp[t['id']]['a']
        if t['writes']:
            body = '%s = %s' % (t['writes'], lit.split('\n')[-1])
        else:
            body = "return '%s'" % lit
        r = judge_body(t, body, exp[t['id']])
        if not (r['admitted'] and r['shown'] and not r['both']):
            bad.append('%s: a hard-coded body should be admitted and right on the shown data only: %s' % (t['id'], r))
        hard += 1 if r['both'] else 0
    # what the gate must refuse
    t = T.TASKS[0]
    for label, body, stage in (('a call the point does not allow', 'return floor(n)', 'constraint'),
                               ('a function defined inside', 'func X() return 1', 'structural'),
                               ('a double quote', 'return "x"', 'structural'),
                               ('a comment', 'return n # fast', 'structural')):
        out, _ = apply_body(t, body, 'a')
        ok = (not out.admitted) and out.stage == stage
        print('  %s %s -> %s' % ('ok  ' if ok else 'FAIL', label, out.stage))
        if not ok:
            bad.append('%s should be refused at %s, got %s %s' % (label, stage, out.status, out.stage))
    for b in bad:
        print('  PROBLEM', b)
    print('r5_agent selftest: %d tasks, %d problem(s)' % (len(T.TASKS), len(bad)))
    if write and not bad:
        json.dump(exp, open(os.path.join(HERE, 'expected.json'), 'w'), indent=1)
    return 1 if bad else 0


def judge_body(t, body, exp):
    """-> a dict of the floor scores for one body: shape, admitted, stage/why of a refusal, runs, shown, both."""
    r = {'shape': False, 'admitted': False, 'stage': '', 'why': '', 'runs': False, 'shown': False, 'both': False}
    body = body.strip()
    if not body or '\n' in body:
        r['stage'], r['why'] = 'structural', 'the body is empty or has a line break'
        return r
    out, text = apply_body(t, body, 'a')
    r['stage'], r['why'] = out.stage or '', (out.why or '')[:120]
    r['shape'] = out.stage not in ('structural',) or out.admitted
    if not out.admitted:
        return r
    r['admitted'] = True
    o, e, code = run_text(text)
    r['runs'] = code == 0 and 'Error (' not in o + e
    r['shown'] = norm(o) == exp['a']
    if r['shown']:
        out2, text2 = apply_body(t, body, 'b')
        r['both'] = out2.admitted and norm(run_text(text2)[0]) == exp['b']
    return r


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] in ('build', 'selftest'):
        sys.exit(selftest(write=(not a or a[0] == 'build')))
    raise SystemExit(__doc__)
