"""k4_local.py -- K4 on a LOCAL model: the twenty tasks, both shapes (Ring++ and the Python-shaped face), each with the engine's constrained decoder ON (the shape's grammar, enforced at the
sampler) and OFF, a pinned gguf and a fixed seed, offline. Scores are taken at the FLOOR, so a model that cannot pass still says how far it got:

    valid    the text is in the shape's grammar (always true under the decoder -- that is what it is for; measured for the unconstrained runs)
    ended    the program wrote its sentinel line (`<<END>>`): it knew it was finished
    reads    the face: the lenient reader accepts the text; Ring++: rnxc compiles it (no statement refused)
    runs     it runs on the shown data without an error
    shown    it prints the right answer for the shown data
    pass     it prints the right answer on the shown data AND on the hidden data (k4.judge_one: the K4 pass)

    python k4_local.py run <model.gguf> <tag> [--tasks T01,T02] [--shapes ringpp,face] [--grammar on,off] [--seeds 0:0,1:0.7] [--max-tokens 320]
    python k4_local.py report                      the table of every run kept under local/

Ring++ is judged on rnxc (the product). The oracle -- Ring 1.27's VM -- is only the guard that the twenty references agree (k4.py build). The generation runs on the Ring++ package
(runtime/package/ringpp-win64), where Softanza's engine loads the model; nothing leaves the machine.

Each task is a few-shot chat in ChatML: the shape's primer as the system turn, three worked examples (not among the twenty) as user/assistant turns, then the task, with the task's data lines
already written at the head of the assistant's turn (the program must begin with them, as in the cloud rounds), so the grammar governs the continuation only. The examples are validated: each
runs on rnxc to its stated output, in both shapes, and the face's text is read back strictly.
"""
import json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
V22 = os.path.join(HERE, '..')
for p in (HERE, V22, os.path.join(V22, '..', 'v21')):
    sys.path.insert(0, os.path.abspath(p))
import k4, round2, face_py, face_read, face_gbnf, ringpp_gbnf
import grammar_court as gc
from k4 import TASKS

import paths                                   # on sys.path once k4 is imported
ROOT = paths.RINGPP
PACKAGE = os.environ.get('PKG_RNXC') or os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
GEN = os.path.join(HERE, 'k4_gen.ring')
BATCH = os.path.join(paths.SPIKE, 'v20', 'probes', 'gbnf_batch.ring')
LOCAL = os.path.join(HERE, 'local')
END = face_gbnf.END
BANNER = face_gbnf.BANNER_START

DEMOS = [
    {'id': 'D1', 'text': 'Print the sum of the items of the list as `total=<n>`.', 'a': ['aNums = [4, 5, 6]'],
     'ref': 'nTotal = 0\nfor x in aNums\n\tnTotal += x\nnext\n? "total=" + nTotal\n'},
    {'id': 'D2', 'text': 'Define a function Double that returns twice its argument, and print `d=<Double(n)>`.', 'a': ['n = 21'],
     'ref': '? "d=" + Double(n)\n\nfunc Double(x)\n\treturn x * 2\n'},
    {'id': 'D3', 'text': 'Define a class Box with an attribute v that starts at 0, a method Put(x) that stores x in it and a method Take() that returns it. Make one Box, call Put(nIn) and print `box=<Take()>`.',
     'a': ['nIn = 8'],
     'ref': 'o = new Box\no.Put(nIn)\n? "box=" + o.Take()\n\nclass Box\n\tv = 0\n\n\tfunc Put(x)\n\t\tThis.v = x\n\n\tfunc Take()\n\t\treturn This.v\n'},
]
DEMO_IDS = ('D1',)     # the engine keeps only the last 512 tokens of a prompt (k4_gen.ring): primer + examples + task must fit, so one example
SYSTEM_TAIL = ('\nReply with code only: the Start lines, then the rest, then a line holding only %s.' % END)

RPP_COMPACT = '''You write Ring++ programs (Ring with explicit scope).
- Print: ? expr    Join text and numbers with +    Strings "..." or '...', no escapes.
- Lists [1, 2, 3]: aList[1] is the first item, len(aList), add(aList, x). cText[i] is the i-th character.
- if c ... else ... ok    while c ... end    for i = 1 to n ... next    for x in aList ... next    % is the remainder, floor(x)
- Compare = != < > <= >=    and or not.  In a function a bare name is local, $x is a global, @x an attribute.
- After the statements: func Name(a) ... return x    class Name (n = 0) func Add() This.n = This.n + 1 ...; o = new Name; o.Add()
- try ... catch ... done  (the message is cCatchError)'''

FACE_COMPACT = '''You write programs in "the face": Python syntax standing for Ring++, with a fixed vocabulary.
- say(x) prints; cat(text, x) joins; at(a, i) is item or character i (from 1); len(a).
- Use == != < > <= >= and + only when both sides are plainly numbers or both plainly strings; else eq ne lt gt le ge and plus(a, b). "1" equals 1.
- mod(a, b); for i in span(1, n): (inclusive); for x in aList:; if/elif/else; while; both(a, b) either(a, b) negate(a).
- Order: statements, then def functions (return "" for nothing), then classes.
- Class: class C: def __region__(self): self.n = 0   def Add(self): ...; o = new_without_init(C); o.Add().
- try: ... except RingError as e: (str(e) is the message). No a[i], str(), int(), lambda, True/False, .get().'''


def shape_text(shape, ring):
    """The program as the shape's own printer writes it: Ring++ by `rnxc fmt`, the face by the printer, without its banner."""
    if shape == 'ringpp':
        t = gc.fmt_ring(ring)
        if t is None:
            raise SystemExit('haro fmt refuses a reference')
        return t
    t = face_py.print_py(face_py.parse_text(ring))
    lines = t.split('\n')
    if lines and lines[0].startswith(BANNER):
        lines = lines[1:]
    return '\n'.join(lines)


def with_data(t, which='a'):
    return '\n'.join(t[which]) + '\n' + t['ref']


def task_block(t, exp):
    return 'Task: %s\nStart:\n%s\nOutput:\n%s' % (t['text'], '\n'.join(t['a']), exp)


def run_full(text, exe=None, timeout=10):
    d = tempfile.mkdtemp(prefix='k4l_')
    p = os.path.join(d, 'p.ring')
    open(p, 'wb').write(text.encode('latin-1', 'replace'))
    try:
        r = subprocess.run([exe or k4.HARO_VM, p], capture_output=True, cwd=d, timeout=timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return '', 'timeout', 124
    return r.stdout.decode('latin-1').replace('\r\n', '\n')[:20000], r.stderr.decode('latin-1')[:2000], r.returncode


def demo_turns(shape):
    """-> [(user, assistant)], validated: each demo's program runs on rnxc to the output it states, and a face text reads back strictly."""
    turns = []
    for dm in [x for x in DEMOS if x['id'] in DEMO_IDS]:
        ring = with_data(dm)
        out = k4.norm(run_full(ring)[0])
        text = shape_text(shape, ring)
        if shape == 'face':
            back = face_read.read_ring(text, strict=True)
            if k4.norm(run_full(back)[0]) != out:
                raise SystemExit('demo %s: the face text prints something else' % dm['id'])
        else:
            if k4.norm(run_full(text)[0]) != out:
                raise SystemExit('demo %s: the formatted text prints something else' % dm['id'])
        turns.append((task_block(dm, out), text.rstrip('\n') + '\n' + END + '\n'))
    return turns


def primer(shape):
    return (RPP_COMPACT if shape == 'ringpp' else FACE_COMPACT) + SYSTEM_TAIL


def chat(shape, t, exp, demos):
    s = '<|im_start|>system\n' + primer(shape) + '<|im_end|>\n'
    for u, a in demos:
        s += '<|im_start|>user\n' + u + '<|im_end|>\n<|im_start|>assistant\n' + a + '<|im_end|>\n'
    prefill = '\n'.join(t['a']) + '\n'
    s += '<|im_start|>user\n' + task_block(t, exp) + '<|im_end|>\n<|im_start|>assistant\n' + prefill
    return s, prefill


def clean(out):
    """-> (body, ended): the generated text up to its sentinel, with any code fence or chat token dropped."""
    out = out.replace('\r\n', '\n')
    for stop in ('<|im_end|>', '<|endoftext|>'):
        if stop in out:
            out = out.split(stop)[0]
    ended = END in out
    if ended:
        out = out.split(END)[0]
    out = '\n'.join(l for l in out.split('\n') if not l.strip().startswith('```'))
    return out.rstrip('\n') + '\n' if out.strip() else '', ended


def put(path, data):
    """Write a file only when its bytes differ: a generator already running reads these files job by job, and must never meet one half rewritten."""
    if os.path.exists(path) and open(path, 'rb').read() == data:
        return
    open(path, 'wb').write(data)


def pairs(s):
    return [tuple(x.split(':')) for x in s.split(',')]


def run(model, tag, only=None, shapes=('ringpp', 'face'), grammars=('on', 'off'), seeds=(('0', '0'),), max_tokens=320, count_only=False, judge_only=False):
    exp = json.load(open(os.path.join(HERE, 'expected.json')))
    # a PERSISTENT work directory, so a run that a power cut stopped goes on where it was (k4_gen.ring skips a job whose .meta exists) -- but only when everything the
    # jobs were made from is the same: the key below hashes the model, the prompts, the grammars and the manifest, and a different key clears the finished jobs.
    work = os.path.join(paths.OUT, 'k4work', tag)
    os.makedirs(work, exist_ok=True)
    put(os.path.join(work, 'ringpp.gbnf'), ringpp_gbnf.ringpp_grammar().encode('latin-1'))
    put(os.path.join(work, 'face.gbnf'), face_gbnf.face_grammar().encode('latin-1'))
    man, meta = [], {}
    demo_by_shape = {shape: demo_turns(shape) for shape in shapes}
    for t in TASKS:                      # a task at a time, both shapes, so that a run stopped half way still compares the shapes on the tasks it reached
        if only and t['id'] not in only:
            continue
        for shape in shapes:
            prompt, prefill = chat(shape, t, exp[t['id']]['a'], demo_by_shape[shape])
            pf = 'p_%s_%s.txt' % (shape, t['id'])
            put(os.path.join(work, pf), prompt.encode('latin-1', 'replace'))
            for g in grammars:
                for seed, temp in seeds:
                    jid = '%s_%s_%s_s%s' % (shape, g, t['id'], seed)
                    man.append('%s|%s|%s|%s|%s|%s' % (jid, pf, (shape + '.gbnf') if g == 'on' else '-', seed, temp, max_tokens))
                    meta[jid] = {'shape': shape, 'grammar': g, 'task': t['id'], 'seed': seed, 'temp': temp, 'prefill': prefill}
    open(os.path.join(work, 'm.txt'), 'wb').write('\n'.join(man).encode('latin-1'))
    import hashlib
    h = hashlib.sha256(('%s|%d' % (os.path.basename(model), os.path.getsize(model))).encode())
    h.update('\n'.join(sorted(man)).encode())          # the jobs, not their order
    for fn in sorted(os.listdir(work)):
        if fn.startswith('p_') or fn.endswith('.gbnf'):
            if any(('|' + fn + '|') in ln or ln.endswith('|' + fn) for ln in man) or fn.endswith('.gbnf'):
                h.update(fn.encode())
                h.update(open(os.path.join(work, fn), 'rb').read())
    key = h.hexdigest()
    kf = os.path.join(work, '_key.txt')
    old = open(kf).read() if os.path.exists(kf) else None
    if old is not None and old != key:
        gone = [fn for fn in os.listdir(work) if fn.endswith('.out') or fn.endswith('.meta')]
        for fn in gone:
            os.remove(os.path.join(work, fn))
        print('the inputs changed since the last run in %s: %d finished files cleared' % (work, len(gone)))
    open(kf, 'w').write(key)
    done = len([fn for fn in os.listdir(work) if fn.endswith('.meta')])
    if done:
        print('resuming: %d of %d jobs already finished in %s' % (done, len(man), work))
    print('%d jobs on %s; working in %s' % (len(man), os.path.basename(model), work))
    t0 = time.time()
    if judge_only:
        # judge what has finished so far, generate nothing: the .meta files are the generator's own result lines
        for jid in list(meta):
            if not os.path.exists(os.path.join(work, jid + '.meta')):
                del meta[jid]
        so = '\n'.join(open(os.path.join(work, jid + '.meta')).read().strip() for jid in meta)
        print('judging %d of %d jobs (the rest have not finished)' % (len(meta), len(man)))
        r = None
    else:
        r = subprocess.run([PACKAGE, GEN, model, os.path.join(work, 'm.txt'), work] + (['count'] if count_only else []), capture_output=True, cwd=ROOT, timeout=6 * 3600)
        so = r.stdout.decode('latin-1').replace('\r\n', '\n')
    toks = {ln.split('|')[1]: int(ln.split('|')[2]) for ln in so.split('\n') if ln.startswith('T|')}
    if toks:
        for sh in sorted({k.split('_')[0] for k in toks}):
            v = {k: n for k, n in toks.items() if k.startswith(sh + '_')}
            print('prompt tokens, %s: min %d, max %d (limit 510, %d prompts); longest: %s' % (sh, min(v.values()), max(v.values()), len(v), ', '.join('%s %d' % (k.split('_')[2], n) for k, n in sorted(v.items(), key=lambda kv: -kv[1])[:4])))
    if count_only:
        return
    if r is not None and (r.returncode != 0 or 'ERR|' in so):
        print(so[:600], r.stderr.decode('latin-1')[:600])
        raise SystemExit('the generator failed')
    for ln in so.split('\n'):
        if ln.startswith('J|'):
            _, jid, sec, steps, judged, masked, stalled, complete = ln.split('|')
            meta[jid].update({'seconds': float(sec), 'tokens': int(steps), 'complete': complete.strip() == '1', 'stalled': int(stalled.strip() or 0)})
        elif ln.startswith('MODEL|'):
            print(ln)
    print('generated in %.0f s' % (time.time() - t0))
    if judge_only:
        tag = tag + '-partial'      # never the name of a finished run: others wait for that file
    outdir = os.path.join(LOCAL, tag, 'out')
    os.makedirs(outdir, exist_ok=True)
    for jid in meta:
        fp = os.path.join(work, jid + '.out')
        meta[jid]['raw'] = open(fp, 'rb').read().decode('latin-1') if os.path.exists(fp) else ''
        open(os.path.join(outdir, jid + '.txt'), 'wb').write(meta[jid]['raw'].encode('latin-1', 'replace'))
    judge_run(tag, meta, model, seeds, max_tokens)


def accepts(items):
    """items: [(grammar text, sentence)] -> [bool], by the engine's own decoder."""
    d = tempfile.mkdtemp(prefix='k4g_')
    man, gfiles = [], {}
    for i, (g, s) in enumerate(items):
        gi = gfiles.setdefault(g, 'g%d.gbnf' % len(gfiles))
        open(os.path.join(d, gi), 'wb').write(g.encode('latin-1'))
        open(os.path.join(d, 's%d.txt' % i), 'wb').write(s.encode('latin-1', 'replace'))
        man.append('%s|s%d.txt' % (gi, i))
    open(os.path.join(d, 'm.txt'), 'wb').write('\n'.join(man).encode('latin-1'))
    r = subprocess.run([PACKAGE, BATCH, os.path.join(d, 'm.txt'), d], capture_output=True, cwd=ROOT, timeout=3600)
    res = {}
    for ln in r.stdout.decode('latin-1').replace('\r\n', '\n').split('\n'):
        if ln.startswith('J|'):
            _, j, refusal, a = (ln.split('|', 3) + ['', ''])[:4]
            res[int(j) - 1] = (not refusal) and a.strip() == '1'
    return [res.get(i, False) for i in range(len(items))]


def judge_run(tag, meta, model, seeds, max_tokens):
    exp = json.load(open(os.path.join(HERE, 'expected.json')))
    tk = {t['id']: t for t in TASKS}
    grams = {'ringpp': ringpp_gbnf.ringpp_grammar(), 'face': face_gbnf.face_grammar()}
    items, order = [], []
    for jid, m in meta.items():
        m['body'], m['ended'] = clean(m['raw'])
        items.append((grams[m['shape']], m['body'] + END + '\n'))
        order.append(jid)
    for jid, ok in zip(order, accepts(items)):
        meta[jid]['valid'] = ok
    for jid, m in meta.items():
        t = tk[m['task']]
        program = m['prefill'] + m['body']
        m['program'] = program
        cond = 'R' if m['shape'] == 'ringpp' else 'F'
        e = exp[t['id']]
        text_a = k4.substitute(t, program, 'a')
        reads = runs = shown = False
        detail = ''
        if text_a is None:
            detail = 'does not begin with its data'
        elif m['shape'] == 'ringpp':
            out, err, code = run_full(text_a)
            both = out + err
            reads = 'did not compile' not in both and 'refused this statement' not in both
            runs = reads and code == 0 and 'Error (' not in both
            shown = k4.norm(out) == e['a']
            detail = (err or out)[-120:] if not runs else ''
        else:
            try:
                ring = face_read.read_ring(text_a, strict=False)
                reads = True
            except Exception as ex:
                detail = 'unreadable: ' + str(ex)[:100]
                ring = None
            if reads:
                out, err, code = run_full(ring)
                both = out + err
                runs = code == 0 and 'Error (' not in both
                shown = k4.norm(out) == e['a']
                detail = (err or out)[-120:] if not runs else ''
        verdict = k4.judge_one(t, cond, program, e) if text_a is not None else {'strict': 'format', 'lenient': 'format'}
        m.update({'reads': reads, 'runs': runs, 'shown': shown, 'pass': verdict['lenient'] == 'pass', 'strict': verdict['strict'] == 'pass', 'detail': detail})
    rows = {}
    for jid, m in meta.items():
        rows.setdefault((m['shape'], m['grammar']), []).append(m)
    summary = {}
    for key, ms in rows.items():
        n = len(ms)
        summary['%s/%s' % key] = {'n': n, 'valid': sum(x['valid'] for x in ms), 'ended': sum(x['ended'] for x in ms), 'reads': sum(x['reads'] for x in ms), 'runs': sum(x['runs'] for x in ms),
                                  'shown': sum(x['shown'] for x in ms), 'pass': sum(x['pass'] for x in ms), 'strict': sum(x['strict'] for x in ms),
                                  'tok_per_s': round(sum(x.get('tokens', 0) for x in ms) / max(1e-9, sum(x.get('seconds', 0) for x in ms)), 1)}
    keep = {jid: {k: v for k, v in m.items() if k not in ('raw',)} for jid, m in meta.items()}
    json.dump({'tag': tag, 'model': os.path.basename(model), 'seeds': seeds, 'max_tokens': max_tokens, 'summary': summary, 'jobs': keep},
              open(os.path.join(LOCAL, tag, 'results.json'), 'w'), indent=1)
    print_summary(tag, summary)


def print_summary(tag, summary):
    print('\n%s' % tag)
    print('  %-14s %3s %6s %6s %6s %6s %6s %6s %7s' % ('shape/grammar', 'n', 'valid', 'ended', 'reads', 'runs', 'shown', 'pass', 'tok/s'))
    for k in sorted(summary):
        s = summary[k]
        print('  %-14s %3d %6d %6d %6d %6d %6d %6d %7.1f' % (k, s['n'], s['valid'], s['ended'], s['reads'], s['runs'], s['shown'], s['pass'], s['tok_per_s']))


def report():
    out = ['# K4, local models -- results (regenerated by `k4_local.py report`)', '',
           'Twenty tasks, Ring++ and the Python-shaped face, the engine\'s constrained decoder on and off, a pinned gguf, greedy decoding unless the run says otherwise. `valid` = in the shape\'s grammar,',
           '`ended` = wrote its sentinel, `reads` = the face reader / haro accepts it, `runs` = no error on the shown data, `shown` = the right answer on the shown data, `pass` = right on the hidden data too.', '']
    for tag in sorted(os.listdir(LOCAL)) if os.path.isdir(LOCAL) else []:
        fp = os.path.join(LOCAL, tag, 'results.json')
        if not os.path.exists(fp):
            continue
        d = json.load(open(fp))
        out += ['## %s -- %s, seeds %s, max tokens %s' % (tag, d['model'], d['seeds'], d['max_tokens']), '',
                '| shape / decoder | n | valid | ended | reads | runs | shown | pass | tokens/s |', '|---|---|---|---|---|---|---|---|---|']
        for k in sorted(d['summary']):
            s = d['summary'][k]
            out.append('| %s | %d | %d | %d | %d | %d | %d | %d | %.1f |' % (k.replace('/on', ', decoder on').replace('/off', ', decoder off'), s['n'], s['valid'], s['ended'], s['reads'], s['runs'], s['shown'], s['pass'], s['tok_per_s']))
        out.append('')
    open(os.path.join(HERE, 'RESULTS_LOCAL.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print('\n'.join(out))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'report':
        report()
    elif a[0] in ('run', 'count', 'judge'):
        model, tag = a[1], a[2]
        opt = {}
        i = 3
        while i < len(a):
            opt[a[i]] = a[i + 1]
            i += 2
        run(model, tag, only=opt['--tasks'].split(',') if '--tasks' in opt else None, count_only=(a[0] == 'count'), judge_only=(a[0] == 'judge'), shapes=tuple(opt.get('--shapes', 'ringpp,face').split(',')),
            grammars=tuple(opt.get('--grammar', 'on,off').split(',')), seeds=tuple(pairs(opt.get('--seeds', '0:0'))), max_tokens=int(opt.get('--max-tokens', 320)))
    else:
        raise SystemExit(__doc__)
