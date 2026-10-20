"""k4.py -- the K4 harness (kill criterion K4 of the code-graph memo: does a model do no better writing a Python-shaped face than a Ring-shaped one?)

    python haro/spike/v22/k4/k4.py build                 validate the tasks, write prompts/R.md, prompts/F.md and expected.json
    python haro/spike/v22/k4/k4.py judge R|F file...     judge answer files (each holds `### T01` ... blocks) and print the scores

THE EXPERIMENT. Twenty tasks (tasks.py), one attempt each, two conditions that differ only in the language and its primer: R, Ring, with a primer of Ring's facts; F, the
Python-shaped face, with a primer of its words. A program is judged on TWO inputs -- the data the statement shows and data the checker substitutes -- so printing the shown
answer fails. R: run on the oracle (runtime/win64/ring.exe, our own build of Ring 1.27's VM). F: read by the reader (face_read.py) STRICTLY -- only the face's own spelling --
and the Ring that comes out is run on the oracle; read LENIENTLY too (a text that is not the face's spelling but means something), which is how often a model needed correcting.
The build step proves the harness: every reference solution passes on the oracle on both inputs, and its printed face text is read back strictly to the same output.
"""
import glob, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import face_read
from face_read import face_py, l1, ReadRefused
from tasks import TASKS

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
ORACLE = os.environ.get('RING') or os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
SCRATCH = tempfile.mkdtemp(prefix='k4_')

RING_PRIMER = '''You write programs in Ring (version 1.27), a small dynamic language. Facts about it:
- Print with `? expression` (prints the value, then a newline). Comments start with #.
- Variables need no declaration; names are case-insensitive. Strings are "..." or '...' and have NO escape sequences. `+` joins a string with anything ("n=" + 5 is "n=5") and adds two
  numbers; a string that looks like a number is equal to that number under `=`.
- Lists are written [1, 2, 3]; items are numbered from 1: aList[1]; len(aList) is the length; add(aList, x) appends. A string is indexed the same way: cText[1] is its first character.
- if cond ... else ... ok      while cond ... end      for i = 1 to n ... next (the bound is inclusive; for i = 10 to 1 step -1 counts down)      for x in aList ... next
  Comparison: = != < > <= >=      logic: and or not      % is the remainder      floor(x) rounds down.
- Functions: func Name(a, b) ... return x. Put function and class definitions AFTER the statements that use them (whatever follows a func belongs to that func).
- Classes: class Name, attributes assigned in the class body (n = 0), methods func Method() ... ; This.n is an attribute; make an object with o = new Name; call o.Method().
- Errors: try ... catch ... done ; the message is in cCatchError.
- Do not load libraries.'''

FACE_PRIMER = '''You write programs in "the face": Python syntax with a fixed vocabulary, standing for the language Ring. It has ONE meaning, Ring's, and the text is read by a strict reader that
accepts only the face's own spelling. Rules:
- Statements are Python's: indentation, if/elif/else, while, for, def, class, try/except. Print one line with say(x).
- Positions start at 1: at(a, i) reads item i of a list or character i of a string; setat(a, i, v) writes it. Never a[i].
- Write == != < > <= >= and + ONLY when both sides are plainly numbers or both plainly strings (a literal, len(...), a name that is only ever assigned numbers, or only strings).
  Otherwise use eq(a, b) ne lt gt le ge for comparisons, and cat(a, b) when the left side is a string or plus(a, b) otherwise, for +. Ring calls a string that looks like a number equal to
  that number: eq("1", 1) is true.
- mod(a, b) is the remainder. for i in span(first, last): is inclusive; span(10, 1, -1) counts down; for x in aList: iterates the items.
- both(a, b), either(a, b), negate(a) give 1 or 0 as values; and/or/not are used only inside an if or while condition. Use 1 and 0, never True/False/None.
- Strings have no escapes. A function ends with return (return "" for nothing). Globals are G.name. An object: class Name: with def __region__(self): self.n = 0 holding its attributes
  and def Method(self): ... for methods; make one with new(Name); call o.Method().
- try: ... except RingError as e: ... ; str(e) is the message. floor(x) rounds down.
- There are no lambdas, comprehensions, dicts, tuples, a[i] subscripts, f-strings, imports, //, conditional expressions (x if c else y), `is` or `in`.'''


def run(path):
    p = subprocess.run([ORACLE, path], capture_output=True, cwd=os.path.dirname(path), timeout=30, stdin=subprocess.DEVNULL)
    return (p.stdout.decode('latin-1')).replace('\r\n', '\n')


def norm(s):
    return '\n'.join(line.rstrip() for line in s.replace('\r\n', '\n').split('\n')).rstrip('\n')


def with_data(task, which):
    """The reference program with its preamble set to the data of variant `a` or `b`."""
    return '\n'.join(task[which]) + '\n' + task['ref']


def ring_output(text):
    p = os.path.join(SCRATCH, 'p.ring')
    open(p, 'wb').write(text.encode('latin-1'))
    return norm(run(p))


def expected():
    out = {}
    for t in TASKS:
        out[t['id']] = {v: ring_output(with_data(t, v)) for v in ('a', 'b')}
    return out


def build():
    exp = expected()
    bad = []
    for t in TASKS:
        a, b = exp[t['id']]['a'], exp[t['id']]['b']
        if not a or not b or a == b:
            bad.append('%s: the two inputs must give two different non-empty outputs (%r, %r)' % (t['id'], a, b))
        # the gold face text: the reference, printed through the face, read back strictly, run
        for v in ('a', 'b'):
            try:
                g = face_py.parse_text(with_data(t, v))
                text = face_py.print_py(g)
                back = face_read.read_ring(text, strict=True)
            except Exception as e:
                bad.append('%s/%s: the face cannot say the reference: %s' % (t['id'], v, str(e)[:160]))
                continue
            if ring_output(back) != exp[t['id']][v]:
                bad.append('%s/%s: the face text of the reference prints %r, the reference prints %r' % (t['id'], v, ring_output(back), exp[t['id']][v]))
    os.makedirs(os.path.join(HERE, 'prompts'), exist_ok=True)
    for cond, primer, lang in (('R', RING_PRIMER, 'Ring'), ('F', FACE_PRIMER, 'the face')):
        lines = [primer, '', 'TASKS. For each task write one complete program in %s. Every program must BEGIN with exactly the line(s) shown for its task (they hold its data; the checker will '
                 'run your program on other values of the same shape, so compute the answer, never print it from the example). Nothing may be read from the keyboard or from a file. '
                 'Reply with one block per task, in this exact form, and nothing else:' % lang, '', '### T01', '```', '<the program>', '```', '']
        for t in TASKS:
            lines += ['### %s' % t['id'], t['text'], 'The program begins with:'] + ['    ' + l for l in t['a']]
            lines += ['For that data it prints:'] + ['    ' + l for l in exp[t['id']]['a'].split('\n')] + ['']
        open(os.path.join(HERE, 'prompts', cond + '.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    json.dump(exp, open(os.path.join(HERE, 'expected.json'), 'w'), indent=1)
    print('k4 build: %d tasks, %d problem(s)' % (len(TASKS), len(bad)))
    for b in bad:
        print('  PROBLEM', b)
    return 1 if bad else 0


# ---- judging --------------------------------------------------------------------------------------------------------------------------------

def parse_answers(text):
    """`### T01` then a fenced block: {task id: program text}."""
    out = {}
    for m in re.finditer(r'###\s*(T\d\d)[^\n]*\n(.*?)(?=\n###\s*T\d\d|\Z)', text, re.S):
        body = m.group(2)
        f = re.search(r'```[A-Za-z]*\n(.*?)```', body, re.S)
        out[m.group(1)] = (f.group(1) if f else body).strip('\n') + '\n'
    return out


def substitute(task, program, which):
    """The program with its first lines (after blanks, comments and the face's banner) replaced by variant `which`; None when it does not begin with the shown data."""
    lines = program.replace('\r\n', '\n').split('\n')
    k = 0
    while k < len(lines) and (not lines[k].strip() or lines[k].strip().startswith('#')):
        k += 1
    shown = task['a']
    got = [l.strip() for l in lines[k:k + len(shown)]]
    if [re.sub(r'\s+', '', x) for x in got] != [re.sub(r'\s+', '', x) for x in shown]:
        return None
    return '\n'.join(lines[:k] + task[which] + lines[k + len(shown):]) + '\n'


def judge_one(task, cond, program, exp):
    """-> (verdict, detail). verdicts: pass, wrong, error, format (does not begin with its data), refused (F only: the reader said no), plus `lenient` for F."""
    res = {}
    for which in ('a', 'b'):
        text = substitute(task, program, which)
        if text is None:
            return {'strict': 'format', 'lenient': 'format', 'detail': 'does not begin with the shown data'}
        if cond == 'R':
            got = ring_output(text)
            res[which] = ('pass' if got == exp[which] else 'wrong', got)
        else:
            row = {}
            for mode in ('strict', 'lenient'):
                try:
                    ring = face_read.read_ring(text, strict=(mode == 'strict'))
                except (ReadRefused, face_py.Refused) as e:
                    row[mode] = ('refused', str(e)[:200])
                    continue
                except Exception as e:
                    row[mode] = ('refused', 'EXCEPTION %s: %s' % (type(e).__name__, e))
                    continue
                got = ring_output(ring)
                row[mode] = ('pass' if got == exp[which] else 'wrong', got)
            res[which] = row
    if cond == 'R':
        ok = all(res[w][0] == 'pass' for w in res)
        first = next((res[w] for w in res if res[w][0] != 'pass'), ('pass', ''))
        return {'strict': 'pass' if ok else first[0], 'lenient': 'pass' if ok else first[0], 'detail': first[1][:120]}
    out = {}
    for mode in ('strict', 'lenient'):
        vs = [res[w][mode] for w in res]
        if all(v[0] == 'pass' for v in vs):
            out[mode] = 'pass'
        else:
            out[mode] = next(v[0] for v in vs if v[0] != 'pass')
            out['detail_' + mode] = next(v[1] for v in vs if v[0] != 'pass')[:200]
    out['detail'] = out.get('detail_strict', '')
    return out


def judge(cond, files):
    exp = json.load(open(os.path.join(HERE, 'expected.json')))
    total = {}
    for f in files:
        answers = parse_answers(open(f, encoding='utf-8', errors='replace').read())
        row = {}
        for t in TASKS:
            if t['id'] not in answers:
                row[t['id']] = {'strict': 'missing', 'lenient': 'missing', 'detail': ''}
                continue
            row[t['id']] = judge_one(t, cond, answers[t['id']], exp[t['id']])
        total[f] = row
        n = len(TASKS)
        ps = sum(1 for r in row.values() if r['strict'] == 'pass')
        pl = sum(1 for r in row.values() if r['lenient'] == 'pass')
        print('%s  %-40s strict %2d/%d  lenient %2d/%d' % (cond, os.path.basename(f), ps, n, pl, n))
        for tid, r in row.items():
            if r['strict'] != 'pass':
                print('     %s strict=%s lenient=%s  %s' % (tid, r['strict'], r['lenient'], r.get('detail', '')[:150]))
    return total


def selftest():
    """Gold answers (the references; their face texts) must score every task in both conditions; answers that print the shown output must score none; an index in Python's
    brackets and a True must be refused in F."""
    exp = json.load(open(os.path.join(HERE, 'expected.json')))
    d = tempfile.mkdtemp(prefix='k4_self_')
    files = {}
    for name, make in (('gold_R', lambda t: t['ref']),
                       ('gold_F', lambda t: face_py.print_py(face_py.parse_text(with_data(t, 'a')))),
                       ('hard_R', lambda t: '\n'.join(t['a']) + '\n' + ''.join('? "%s"\n' % l for l in exp[t['id']]['a'].split('\n'))),
                       ('hard_F', lambda t: '\n'.join(t['a']) + '\n' + ''.join('say("%s")\n' % l for l in exp[t['id']]['a'].split('\n')))):
        body = []
        for t in TASKS:
            text = make(t)
            if name == 'gold_R':
                text = '\n'.join(t['a']) + '\n' + t['ref']
            body.append('### %s\n```\n%s```\n' % (t['id'], text))
        files[name] = os.path.join(d, name + '.md')
        open(files[name], 'w', encoding='utf-8').write('\n'.join(body))
    bad = 0
    for name, want in (('gold_R', 20), ('gold_F', 20), ('hard_R', 0), ('hard_F', 0)):
        cond = name[-1]
        row = judge(cond, [files[name]])[files[name]]
        got = sum(1 for r in row.values() if r['strict'] == 'pass')
        ok = got == want
        print('  %s %s: %d of %d pass, want %d' % ('ok  ' if ok else 'FAIL', name, got, len(TASKS), want))
        bad += 0 if ok else 1
    # two defects a model could make, each refused for its reason in F
    t = TASKS[1]
    for label, text, want in (('Python subscript', '\n'.join(t['a']) + '\nsay(aList[2])\n', 'refused'), ('True', '\n'.join(t['a']) + '\nx = True\nsay(x)\n', 'refused')):
        r = judge_one(t, 'F', text, exp[t['id']])
        ok = r['strict'] == want
        print('  %s F %s -> %s' % ('ok  ' if ok else 'FAIL', label, r['strict']))
        bad += 0 if ok else 1
    return 1 if bad else 0


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'selftest':
        sys.exit(selftest())
    if len(sys.argv) >= 2 and sys.argv[1] == 'build':
        sys.exit(build())
    if len(sys.argv) >= 4 and sys.argv[1] == 'judge':
        files = []
        for a in sys.argv[3:]:
            files += glob.glob(a)
        judge(sys.argv[2], files)
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
