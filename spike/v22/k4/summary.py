"""summary.py -- K4's results: every answer file judged, grouped by condition and model, and the respelling check.

    python haro/spike/v22/k4/summary.py          prints the table and writes RESULTS.md

For the face: `strict` is the reader's own spelling (a lint), `lenient` reads the text for its meaning, and `respelled` takes each answer that reads leniently, lets the printer write it
(print of the reading: the formatter) and reads THAT strictly and runs it -- the pipeline the face is meant for, which needs nothing of the model but the meaning.
"""
import collections, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import k4
from k4 import face_read, face_py, TASKS

COND_LANG = {'R': 'R', 'R0': 'R', 'F': 'F', 'F2': 'F', 'F3': 'F'}
LABEL = {'R': 'Ring, a primer of Ring\'s facts', 'R0': 'Ring, no primer', 'F': 'the face, round-1 primer', 'F2': 'the face, primer amended (order, no str(), explicit words are always right)',
         'F3': 'the face, F2 plus new vs new_without_init'}


def respell(program, task, exp):
    """The answer, read leniently, printed by the formatter, read strictly and run on both inputs: 'pass', or why not."""
    for which in ('a', 'b'):
        text = k4.substitute(task, program, which)
        if text is None:
            return 'format'
        try:
            canon = face_py.print_py(face_read.read_py(text, strict=False))
            ring = face_read.read_ring(canon, strict=True)
        except Exception as e:
            return 'unreadable: %s' % str(e)[:80]
        if k4.ring_output(ring) != exp[which]:
            return 'wrong'
    return 'pass'


def main():
    exp = json.load(open(os.path.join(HERE, 'expected.json')))
    rows = collections.defaultdict(list)             # (cond, model) -> [per-file results]
    paired = collections.defaultdict(dict)           # (cond) -> {(model, rep, task): lenient pass}
    for f in sorted(glob.glob(os.path.join(HERE, 'answers', '*.md'))):
        m = re.match(r'(\w+?)_(F3|F2|F|R0|R)_(\d+)\.md', os.path.basename(f))
        if not m:
            continue
        model, cond, rep = m.group(1), m.group(2), m.group(3)
        answers = k4.parse_answers(open(f, encoding='utf-8', errors='replace').read())
        res = {'strict': 0, 'lenient': 0, 'respelled': 0, 'fails': []}
        for t in TASKS:
            prog = answers.get(t['id'])
            if prog is None:
                res['fails'].append((t['id'], 'missing'))
                paired[cond][(model, rep, t['id'])] = False
                continue
            r = k4.judge_one(t, COND_LANG[cond], prog, exp[t['id']])
            res['strict'] += r['strict'] == 'pass'
            res['lenient'] += r['lenient'] == 'pass'
            paired[cond][(model, rep, t['id'])] = r['lenient'] == 'pass'
            if COND_LANG[cond] == 'F' and r['lenient'] == 'pass':
                res['respelled'] += respell(prog, t, exp[t['id']]) == 'pass'
            elif COND_LANG[cond] == 'R':
                res['respelled'] += r['strict'] == 'pass'
            if r['lenient'] != 'pass':
                res['fails'].append((t['id'], r['lenient']))
        rows[(cond, model)].append((rep, res))
    out = ['# K4 -- results', '', 'Twenty tasks, two inputs each (the shown data and hidden data), one attempt per task; the models are Claude haiku and Claude sonnet, run as sub-agents that read one prompt file and '
           'wrote one answer file (two tool calls each). Ring is judged on the oracle; the face is read by the reader (strict: the face\'s own spelling; lenient: its meaning) and run on the oracle.', '',
           '| condition | model | runs | strict | lenient | respelled by the printer then strict |', '|---|---|---|---|---|---|']
    for cond in ('R', 'R0', 'F', 'F2', 'F3'):
        for model in ('haiku', 'sonnet'):
            rs = rows.get((cond, model))
            if not rs:
                continue
            n = len(rs)
            out.append('| %s | %s | %d | %s | %s | %s |' % (LABEL[cond], model, n, ', '.join('%d/20' % r['strict'] for _, r in rs), ', '.join('%d/20' % r['lenient'] for _, r in rs),
                                                            ', '.join('%d/20' % r['respelled'] for _, r in rs)))
    out += ['', '## What failed (lenient)', '']
    for (cond, model), rs in sorted(rows.items()):
        fails = collections.Counter(tid + ' ' + why for _, r in rs for tid, why in r['fails'])
        out.append('- %s / %s: %s' % (cond, model, ', '.join('%s x%d' % kv for kv in sorted(fails.items())) or 'nothing'))
    text = '\n'.join(out) + '\n'
    open(os.path.join(HERE, 'RESULTS.md'), 'w', encoding='utf-8', newline='\n').write(text)
    print(text)


if __name__ == '__main__':
    main()
