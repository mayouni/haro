"""The condition printer's court (Haro v0.33), standalone: born here, run by guard stage 38.

The meta-court prints a condition back (form_expand.haro, CondPrint) only where it has expanded a quantifier over a FORM. A printer that loses meaning there would
change what a constraint says, silently, in a court nobody re-reads. So the printer is proved on EVERY condition the repository holds -- each CONSTRAINT's WHEN and THEN
and each VIEW's WHERE in every committed declaration, in every meta fixture of every rung, and in the grants and medium worlds:

  parse -> print -> parse gives the same tree, and print -> parse -> print the same text (so a printed condition is its own canonical form);

and the nodes the corpus does not reach are pinned by hand-written conditions, one for each node kind of the grammar and each precedence the printer parenthesises.
On haro and on its checked build, the two printing the same bytes (D41).

  python spike/v33/cond_court.py [--plant]
"""
import glob, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
import paths

HARO_VM, TWIN = paths.need_bins()
CWD = SPIKE                                       # where cond_rt.haro runs; plants.py points it at a planted copy
PLANT = '--plant' in sys.argv
CLAUSE = re.compile(r'\b(?:WHEN|THEN|WHERE)\s+"([^"]*)"')

# every node kind of the grammar, and every precedence the printer parenthesises: written by hand because no committed condition may reach them all
HAND = [
    'a = b', 'a != b', 'a > 5', 'a < 5', 'a = 5', "a = 'two words'", 'a = this.b', 'a = b.c.d', 'a present', 'a absent', 'a empty', 'a nonempty', 'a unique', 'a distinct',
    'a contains x', "a contains 'two words'", 'a contains 7', 'a within b', "a within 'x'", 'a host_of b.c', 'a under b', 'a covers b', 'a cyclic', 'a matches shape',
    'self is v', 'self reachable', 'self referenced', 'a keyed_by b', "a keyed_by 'k'", 'exists d',
    'not a present', 'not not a present', 'not (a present and b present)', 'not (a present or b present)',
    'a present and b present or c present', 'a present and (b present or c present)', '(a present or b present) and c present', 'a present or b present and c present',
    '(a present and b present) and c present', 'a present and (b present and c present)', '(a present or b present) or c present', 'a present or (b present or c present)',
    'some d', 'some d where a present', 'all d where a = x', 'earlier d where a present', 'some d named this', 'some d named x where a present',
    "some d named 'x y' where a present", 'some d named this.n where a present', 'some a.b where c present', 'some d where a present or b present',
    'some d where (some e where c present)', '(some d where a present) and (some e where b present)', 'not (some d where a present)',
    'x = print and (some d where a contains zoom or b contains zoom)', 'a present and some d where b present',
]


def corpus():
    seen, out = set(), []

    def add(text):
        c = ' '.join(text.split())
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    for p in sorted(glob.glob(os.path.join(SPIKE, '**', '*.haro'), recursive=True)):
        if os.sep + 'scratch' + os.sep in p or os.path.basename(p).startswith('zz_'):
            continue
        for m in CLAUSE.finditer(open(p, encoding='utf-8', errors='replace').read()):
            add(m.group(1))
    for p in sorted(glob.glob(os.path.join(SPIKE, 'v*', '*.json'))):
        try:
            doc = json.load(open(p, encoding='utf-8'))
        except ValueError:
            continue
        for case in (doc.get('accepts', []) + doc.get('rejects', [])) if isinstance(doc, dict) else []:
            for m in CLAUSE.finditer(case.get('source', '')):
                add(m.group(1))
    return out, len(out)


def run(exe, path):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    r = subprocess.run([exe, 'cond_rt.haro', path], capture_output=True, env=env, timeout=600, cwd=CWD)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def judge(conds, hand_from, builds=(('haro', None), ('checked', None)), quiet=False):
    """Returns (failures, the conditions that failed)."""
    builds = [(l, e or (HARO_VM if l == 'haro' else TWIN)) for l, e in builds]
    say = (lambda *a: None) if quiet else print
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'conds.txt')
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(conds) + '\n')
        outs = {label: run(exe, p) for label, exe in builds}
    lines = {l: o.split('\n') for l, o in outs.items()}
    first = builds[0][0]
    failures, bad = 0, []
    unreadable = 0
    ok_n = 0
    for n, c in enumerate(conds):
        got = lines[first][n] if n < len(lines[first]) else 'NO OUTPUT'
        if got.startswith('ok '):
            ok_n += 1
        elif got.startswith('unreadable ') and n < hand_from:
            unreadable += 1                                   # a corpus condition written to be refused by the condition language
        else:
            failures += 1
            bad.append(c)
            say(f'  FAIL {c[:100]} -- {got[:160]}')
    if PLANT:
        failures += 1
        say('  FAIL the condition printer -- PLANTED')
    if len(builds) > 1:
        if outs[builds[0][0]] != outs[builds[1][0]]:
            failures += 1
            say('  FAIL haro and its checked build differ on the condition printer')
        else:
            say('  ok   haro and its checked build print the same bytes on all %d conditions' % len(conds))
    say(f'CONDITION PRINTER: {ok_n} of {len(conds)} conditions print and read back to the same tree and the same text ({hand_from} from the repository, {len(conds) - hand_from} by hand; '
        f'{unreadable} of the repository\'s are written to be refused by the condition language)')
    return failures, bad


def court():
    print('condition printer court -- Haro v0.33: CondPrint judged on every condition the repository holds, on haro and its checked build')
    rep, _ = corpus()
    conds = rep + HAND
    if len(rep) < 150:
        print(f'  FAIL only {len(rep)} conditions found in the repository (floor 150): the extraction is broken')
        return 1
    return judge(conds, len(rep))[0]


if __name__ == '__main__':
    n = court()
    print(f'cond_court: {"FAIL" if n else "PASS"} ({n} failure(s))')
    sys.exit(1 if n else 0)
