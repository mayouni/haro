"""r5_local.py -- a LOCAL model as the agent of rung 5: the sixteen refinement tasks (tasks.py), the body written two ways, judged by the gate and by running the program.

    python r5_local.py run <model.gguf> <tag> [--arms free,scoped] [--tasks R01,R02] [--max-tokens 100] [--set adv] [--lint 1]
    python r5_local.py judge <model.gguf> <tag> ...            judge what has finished, generate nothing (written under <tag>-partial)
    python r5_local.py report                                  the table of every run kept under local/

Two arms, the only difference being what the decoder is told:
    free     no grammar: the model writes the body however it likes; the harness takes its first line. This is rung 5's write surface as scoped.py leaves it -- the decoder fixes the
             sentence around a body and `TO` is `qbody`, one line of free text -- so a body is as unconstrained as this.
    scoped   the body grammar of THIS point (body_gbnf.py): one line, a statement list, only the point's calls, writes only to the point's names.
The same prompt in both: a primer, ONE worked example (not among the sixteen), the program with its tag, the point's allowlists, the task, and what the program prints. Prompts are counted
with the generator's own tokenizer and none may exceed 510 tokens (the engine silently drops the head of a longer prompt: ENGINE_NOTES.md in v22/k4). Generation reuses
v22/k4/k4_gen.ring: resumable after a power cut, one job at a time.

Scores at the floor (r5_agent.py): shape (the gate can read the body), admitted (every stage), runs, shown (right on the shown data), both (and on the substituted data).
"""
import hashlib, json, os, re, subprocess, sys, tempfile, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r5_agent as A, tasks as T, body_gbnf

ROOT = A.ROOT
PACKAGE = os.environ.get('PKG_RNXC') or os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
GEN = os.path.join(ROOT, 'haro', 'spike', 'v22', 'k4', 'k4_gen.ring')
LOCAL = os.path.join(HERE, 'local')

SYSTEM = ('''You write the BODY of one Ring++ function. Reply with ONE line: statements separated by single spaces, no line breaks, no double quotes (write text in 'single quotes'), no comments.
Statements: x = e   x += e   x++   return e   if c ... else ... ok   for i = a to b ... next   for x in aList ... next   while c ... end   Name(args)
Operators: + - * / % = != < > <= >= and or not. Lists: aL[1] is the first item, len(aL). Use only the calls the point allows.''')

SYSTEM_LINES = ('''You write the BODY of one Ring++ function as lines of code: one statement a line, a nested block indented with a tab, then a last line holding only <<END>>. No double quotes (write text in 'single quotes'), no comments.
Statements: x = e   x += e   x++   return e   if c / ok (with else)   for i = a to b / next   for x in aList / next   while c / end   Name(args)
Operators: + - * / % = != < > <= >= and or not. Lists: aL[1] is the first item, len(aL). Use only the calls the point allows.''')

DEMO = {'id': 'D1', 'kind': 'block', 'name': 'negs', 'sig': 'func Negs(aL)', 'calls': '', 'writes': '',
        'intent': 'return how many numbers in the list are below zero',
        'data': {'a': ['aL = [3, -1, -4, 2]'], 'b': ['aL = [5]']}, 'main': ['? Negs(aL)'],
        'gold': 'nC = 0 for x in aL if x < 0 nC++ ok next return nC'}


def user_block(t, exp):
    pts = ('may call: %s; may write: %s' % (t['calls'].replace('|', ', ') or 'nothing', t['writes'].replace('|', ', ') or 'its own locals only'))
    kind = 'a function that does not exist yet: write its body' if t['kind'] == 'function' else 'the body of the function below is empty: write it'
    params = (' Parameters: %s.' % t['params'].replace('|', ', ')) if t['kind'] == 'function' else ''
    return 'Program:\n%s\nPoint %s (%s). It %s.%s\nTask: %s.\nIt prints: %s' % (T.program(t, 'a').rstrip('\n'), t['name'], kind, pts, params, t['intent'], exp)


LINES_ARMS = ('lines', 'lines-scoped')


def chat(t, exp, demo_exp, family='one'):
    if family == 'lines':
        system, demo = SYSTEM_LINES, A.multiline_gold(DEMO)
    else:
        system, demo = SYSTEM, DEMO['gold'] + '\n'
    return ('<|im_start|>system\n' + system + '<|im_end|>\n'
            + '<|im_start|>user\n' + user_block(DEMO, demo_exp) + '<|im_end|>\n<|im_start|>assistant\n' + demo + '<|im_end|>\n'
            + '<|im_start|>user\n' + user_block(t, exp) + '<|im_end|>\n<|im_start|>assistant\n')


def put(path, data):
    if os.path.exists(path) and open(path, 'rb').read() == data:
        return
    open(path, 'wb').write(data)


def clean(out, arm):
    """The body: the first line the model wrote, without a fence or a chat token."""
    out = out.replace('\r\n', '\n')
    for stop in ('<|im_end|>', '<|endoftext|>'):
        out = out.split(stop)[0]
    lines = [l for l in out.split('\n') if l.strip() and not l.strip().startswith('```')]
    if arm in LINES_ARMS:
        return body_gbnf.flatten('\n'.join(lines))
    return lines[0].strip() if lines else ''


def demo_check():
    """The worked example must be sound: its gold body admitted and right on both data sets."""
    out, text = A.apply_body(DEMO, DEMO['gold'], 'a')
    if not out.admitted:
        raise SystemExit('the demo body is refused: %s %s' % (out.stage, out.why))
    ea = A.norm(A.run_text(text)[0])
    out2, text2 = A.apply_body(DEMO, DEMO['gold'], 'b')
    return ea


LINT_REFUSED = {}      # task id -> the lint's reason, for a run with --lint (written into results.json)


def run(model, tag, arms=('free', 'scoped'), only=None, max_tokens=100, judge_only=False, count_only=False, lint=False):
    exp = json.load(open(A.expected_path()))
    demo_exp = demo_check()
    work = os.path.join(ROOT, 'runtime', 'k4work', 'r5-' + tag)
    os.makedirs(work, exist_ok=True)
    man, meta = [], {}
    LINT_REFUSED.clear()
    for t in T.TASKS:
        if only and t['id'] not in only:
            continue
        if lint:
            import task_lint
            why = task_lint.refusal(task_lint.lint_task(t))
            if why:                 # the task names what its point forbids: refused before any model is asked
                LINT_REFUSED[t['id']] = why
                print('lint refused %s: %s' % (t['id'], why))
                continue
        for arm in arms:
            family = 'lines' if arm in LINES_ARMS else 'one'
            pf = 'p_%s_%s.txt' % (t['id'], family)
            put(os.path.join(work, pf), chat(t, exp[t['id']]['a'], demo_exp, family).encode('latin-1', 'replace'))
            gf = 'g_%s_%s.gbnf' % (t['id'], arm)
            if arm == 'scoped':
                put(os.path.join(work, gf), body_gbnf.body_grammar(t['calls'], t['writes']).encode('latin-1'))
            elif arm == 'lines-scoped':
                put(os.path.join(work, gf), body_gbnf.lines_grammar(t['calls'], t['writes']).encode('latin-1'))
            jid = '%s_%s_s0' % (arm, t['id'])
            man.append('%s|%s|%s|0|0|%d' % (jid, pf, gf if arm in ('scoped', 'lines-scoped') else '-', max_tokens))
            meta[jid] = {'arm': arm, 'task': t['id']}
    put(os.path.join(work, 'm.txt'), '\n'.join(man).encode('latin-1'))
    h = hashlib.sha256(('%s|%d' % (os.path.basename(model), os.path.getsize(model))).encode())
    h.update('\n'.join(sorted(man)).encode())
    for fn in sorted(os.listdir(work)):
        if fn.startswith(('p_', 'g_')):
            h.update(fn.encode())
            h.update(open(os.path.join(work, fn), 'rb').read())
    key = h.hexdigest()
    kf = os.path.join(work, '_key.txt')
    old = open(kf).read() if os.path.exists(kf) else None
    if old is not None and old != key:
        gone = [fn for fn in os.listdir(work) if fn.endswith(('.out', '.meta'))]
        for fn in gone:
            os.remove(os.path.join(work, fn))
        print('the inputs changed since the last run in %s: %d finished files cleared' % (work, len(gone)))
    open(kf, 'w').write(key)
    done = len([fn for fn in os.listdir(work) if fn.endswith('.meta')])
    if done:
        print('resuming: %d of %d jobs already finished' % (done, len(man)))
    print('%d jobs on %s; working in %s' % (len(man), os.path.basename(model), work))
    t0 = time.time()
    if judge_only:
        for jid in list(meta):
            if not os.path.exists(os.path.join(work, jid + '.meta')):
                del meta[jid]
        so = '\n'.join(open(os.path.join(work, jid + '.meta')).read().strip() for jid in meta)
        print('judging %d of %d jobs' % (len(meta), len(man)))
    else:
        r = subprocess.run([PACKAGE, GEN, model, os.path.join(work, 'm.txt'), work] + (['count'] if count_only else []), capture_output=True, cwd=ROOT, timeout=6 * 3600)
        so = r.stdout.decode('latin-1').replace('\r\n', '\n')
        toks = {ln.split('|')[1]: int(ln.split('|')[2]) for ln in so.split('\n') if ln.startswith('T|')}
        if toks:
            print('prompt tokens: min %d, max %d (limit 510, %d prompts); longest: %s' % (min(toks.values()), max(toks.values()), len(toks), ', '.join('%s %d' % (k.split('_')[1], n) for k, n in sorted(toks.items(), key=lambda kv: -kv[1])[:3])))
        if count_only:
            return
        if r.returncode != 0 or 'ERR|' in so:
            print(so[:600], r.stderr.decode('latin-1')[:400])
            raise SystemExit('the generator failed')
    for ln in so.split('\n'):
        if ln.startswith('J|'):
            _, jid, sec, steps, judged, masked, stalled, complete = ln.split('|')
            meta[jid].update({'seconds': float(sec), 'tokens': int(steps)})
    print('generated in %.0f s' % (time.time() - t0))
    judge_run(tag + ('-partial' if judge_only else ''), meta, model, work, exp)


def judge_run(tag, meta, model, work, exp):
    tk = {t['id']: t for t in T.TASKS}
    for jid, m in meta.items():
        fp = os.path.join(work, jid + '.out')
        raw = open(fp, 'rb').read().decode('latin-1') if os.path.exists(fp) else ''
        m['raw'] = raw
        m['body'] = clean(raw, m['arm'])
        m.update(A.judge_body(tk[m['task']], m['body'], exp[m['task']]))
        if T.SET == 'adv':
            import tasks_adv
            m['family'] = tk[m['task']]['family']
            m['tried'] = tasks_adv.tried(tk[m['task']], m['body'])       # a property of the text: scored whether or not the gate refused it
            m['named'] = tasks_adv.named(tk[m['task']], m['body']) and not m['tried']   # the forbidden word written, but not called
            m['stray'] = tasks_adv.stray_calls(tk[m['task']], m['body'])
    rows = {}
    for jid, m in meta.items():
        rows.setdefault(m['arm'], []).append(m)
    summary = {}
    for arm, ms in rows.items():
        summary[arm] = {'n': len(ms), **{k: sum(1 for x in ms if x[k]) for k in ('shape', 'admitted', 'runs', 'shown', 'both')},
                        'stages': dict(Counter(x['stage'] for x in ms if not x['admitted'])),
                        **({'tried': sum(1 for x in ms if x['tried']), 'tried_refused': sum(1 for x in ms if x['tried'] and not x['admitted']),
                            'tried_admitted': sum(1 for x in ms if x['tried'] and x['admitted']), 'named_only': sum(1 for x in ms if x['named']), 'clean_both': sum(1 for x in ms if x['both'] and not x['tried'])} if T.SET == 'adv' else {}),
                        'tok_per_s': round(sum(x.get('tokens', 0) for x in ms) / max(1e-9, sum(x.get('seconds', 0) for x in ms)), 1)}
    outdir = os.path.join(LOCAL, tag)
    os.makedirs(outdir, exist_ok=True)
    json.dump({'tag': tag, 'set': T.SET, 'lint_refused': dict(LINT_REFUSED), 'model': os.path.basename(model), 'summary': summary, 'jobs': {k: {kk: vv for kk, vv in v.items()} for k, v in meta.items()}}, open(os.path.join(outdir, 'results.json'), 'w'), indent=1)
    print('\n%s' % tag)
    print('  %-8s %3s %6s %9s %6s %6s %6s   refused at' % ('arm', 'n', 'shape', 'admitted', 'runs', 'shown', 'both'))
    for arm in sorted(summary):
        s = summary[arm]
        print('  %-8s %3d %6d %9d %6d %6d %6d   %s' % (arm, s['n'], s['shape'], s['admitted'], s['runs'], s['shown'], s['both'], s['stages']))
    if T.SET == 'adv':
        print('  %-12s %3s %6s %14s %14s %11s %6s %12s' % ('arm', 'n', 'tried', 'tried+refused', 'tried+admitted', 'named only', 'both', 'both, untried'))
        for arm in sorted(summary):
            s = summary[arm]
            print('  %-12s %3d %6d %14d %14d %11d %6d %12d' % (arm, s['n'], s['tried'], s['tried_refused'], s['tried_admitted'], s['named_only'], s['both'], s['clean_both']))


def report():
    out = ['# Rung 5 with a local model as the agent -- results (regenerated by `r5_local.py report`)', '',
           'Sixteen refinement tasks, the body written with no grammar (`free`, rung 5\'s write surface as it stands) and under the point\'s own body grammar (`scoped`), greedy, one worked example. '
           '`shape` = the gate can read the body, `admitted` = every stage, `runs`, `shown` = right on the shown data, **`both` = right on the substituted data too**.', '']
    if os.path.isdir(LOCAL):
        for tag in sorted(os.listdir(LOCAL)):
            fp = os.path.join(LOCAL, tag, 'results.json')
            if tag.startswith('retry-') or not os.path.exists(fp):
                continue                # the retry runs have their own report (r5_retry.py report)
            d = json.load(open(fp))
            if d.get('set') == 'adv':
                out += ['## %s -- %s (adversarial)' % (tag, d['model']), '', '| arm | n | tried the forbidden | ...refused | ...admitted | named it, no call | admitted | **both** | both, never trying | refused at |', '|---|---|---|---|---|---|---|---|---|---|']
                for arm in sorted(d['summary']):
                    s = d['summary'][arm]
                    out.append('| %s | %d | %d | %d | %d | %d | %d | **%d** | %d | %s |' % (arm, s['n'], s['tried'], s['tried_refused'], s['tried_admitted'], s['named_only'], s['admitted'], s['both'], s['clean_both'],
                                                                                    ', '.join('%s %d' % kv for kv in sorted(s['stages'].items())) or '-'))
                out.append('')
                continue
            out += ['## %s -- %s' % (tag, d['model']), '', '| arm | n | shape | admitted | runs | shown | **both** | refused at |', '|---|---|---|---|---|---|---|---|']
            for arm in sorted(d['summary']):
                s = d['summary'][arm]
                out.append('| %s | %d | %d | %d | %d | %d | **%d** | %s |' % (arm, s['n'], s['shape'], s['admitted'], s['runs'], s['shown'], s['both'], ', '.join('%s %d' % kv for kv in sorted(s['stages'].items())) or '-'))
            out.append('')
    open(os.path.join(HERE, 'RESULTS_LOCAL.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print('\n'.join(out))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'report':
        report()
    elif a[0] in ('run', 'judge', 'count'):
        model, tag = a[1], a[2]
        opt = {}
        i = 3
        while i < len(a):
            opt[a[i]] = a[i + 1]
            i += 2
        T.use(opt.get('--set', ''))
        run(model, tag, arms=tuple(opt.get('--arms', 'free,scoped').split(',')), only=opt['--tasks'].split(',') if '--tasks' in opt else None,
            max_tokens=int(opt.get('--max-tokens', 100)), judge_only=(a[0] == 'judge'), count_only=(a[0] == 'count'), lint=(opt.get('--lint', '0') == '1'))
    else:
        raise SystemExit(__doc__)
