"""probes/mutate.py -- is the court load-bearing? Defects of known kinds put into the engine (v20/refine.py), one at a time, and the fast court (refine_check.py --fx: the
fixtures, the commutation pool, the small checks; 4 seconds) asked whether it notices.

    python haro/spike/v20/probes/mutate.py [--limit N] [--seed S] [--full-survivors]

A mutant is ONE token of ONE line changed, in the functions that decide something (the gate, the constraint and governance stages, the lowering, the lift, the
sentence reader, the cascade, the primitives): a comparison flipped (`<` and `<=`, `>` and `>=`, `==` and `!=`), `and` and `or` swapped, `in` and `not in` swapped,
`is None` and `is not None` swapped, a `not` dropped, a stage name in a refusal exchanged for another, a case fold removed. The fast court KILLS a mutant when it
fails (or times out); what survives is printed with its line, to be read -- a survivor is either an equivalent mutant (the change alters nothing a program can see) or a
fixture still to be written. With --full-survivors the survivors are put to the whole court (about two minutes each), which also has the live gate, the scoped grammar,
the sweep and the corpus.
The mutated module is loaded in place of refine.py through REFINE_SRC, with its HERE pointed back at the real directory.
"""
import os, random, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
V20 = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(V20, '..', '..', '..'))
SRC = os.path.join(V20, 'refine.py')
SCRATCH = os.path.join(V20, 'scratch', 'mut')
FUNCS = ('lift', 'resolve_target', 'own_rule_error', 'parse_tag', 'tag_set', 'tag_del', 'tag_insert', 'parse_sentence', 'cascade', 'apply_prim', 'lower', 'lower_pipeline',
         'lower_attr', 'is_widening', 'rules_violated', 'evaluate', 'constraint', 'governance', 'footprint', 'commutes', 'same_value', 'to_literal', 'literal_node', 'literal_text')
STAGES = ('structural', 'constraint', 'governance', 'trust', 'derivation')

OPS = [
    (re.compile(r'(?<![<>=!-])>=(?!=)'), '>'), (re.compile(r'(?<![<>=!-])<=(?!=)'), '<'),
    (re.compile(r'(?<![<>=!-])>(?![>=])'), '>='), (re.compile(r'(?<![<>=!-])<(?![<=])'), '<='),
    (re.compile(r'=='), '!='), (re.compile(r'!='), '=='),
    (re.compile(r' and '), ' or '), (re.compile(r' or '), ' and '),
    (re.compile(r' not in '), ' in '), (re.compile(r'(?<!not)(?<!for \w)(?<! for) in (?=[\w(\[\'"{])'), ' not in '),
    (re.compile(r' is not None'), ' is None'), (re.compile(r' is None'), ' is not None'),
    (re.compile(r'\bif not '), 'if '), (re.compile(r'\.lower\(\)'), ''),
]


def functions(src):
    """{function name: (first line, last line)} of the module's top-level defs, 1-based."""
    lines = src.split('\n')
    out, name, start = {}, None, 0
    for i, ln in enumerate(lines, 1):
        m = re.match(r'^def (\w+)\(', ln)
        if m or re.match(r'^(class |# ----)', ln):
            if name:
                out[name] = (start, i - 1)
            name, start = (m.group(1) if m else None), i
    if name:
        out[name] = (start, len(lines))
    return out


def mutants(src):
    lines = src.split('\n')
    fn = functions(src)
    out = []
    for name in FUNCS:
        if name not in fn:
            continue
        a, b = fn[name]
        in_doc = False
        for n in range(a, b + 1):
            ln = lines[n - 1]
            code = ln
            if ln.count('"""') % 2 == 1:
                in_doc = not in_doc
                continue
            if in_doc or ln.strip().startswith('#') or '"""' in ln:
                continue
            code = ln.split('  # ')[0] if '  # ' in ln else ln
            for pat, rep in OPS:
                for m in pat.finditer(code):
                    # not inside a string literal: an even number of quotes before the match
                    before = code[:m.start()]
                    if before.count("'") % 2 or before.count('"') % 2:
                        continue
                    if rep == ' not in ' and re.search(r'\bfor\b', before):
                        continue                    # a loop's own `in`
                    out.append((n, name, pat.pattern, code[:m.start()] + rep + code[m.end():] + ln[len(code):]))
            m = re.search(r"reject\('(\w+)'", code)
            if m and m.group(1) in STAGES:
                other = STAGES[(STAGES.index(m.group(1)) + 1) % len(STAGES)]
                out.append((n, name, 'stage ' + m.group(1) + '->' + other, code.replace("reject('%s'" % m.group(1), "reject('%s'" % other, 1) + ln[len(code):]))
    return out


def run_mutant(text, full=False):
    os.makedirs(SCRATCH, exist_ok=True)
    path = os.path.join(SCRATCH, 'refine.py')
    open(path, 'w', encoding='utf-8', newline='').write(text.replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = %r" % V20, 1))
    env = dict(os.environ, REFINE_SRC=path)
    cmd = [sys.executable, os.path.join(V20, 'refine_check.py')] + ([] if full else ['--fx'])
    try:
        p = subprocess.run(cmd, capture_output=True, cwd=ROOT, env=env, timeout=600 if full else 90)
    except subprocess.TimeoutExpired:
        return True, 'timed out'
    out = p.stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        first = next((ln.strip() for ln in out.split('\n') if 'FAIL' in ln), 'exit %d' % p.returncode)
        return True, first[:110]
    return False, ''


def main():
    limit = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 1
    src = open(SRC, encoding='utf-8', newline='').read()
    ms = mutants(src)
    print('%d mutants of %d functions' % (len(ms), len(FUNCS)))
    if '--only' in sys.argv:
        # --only <log>: the survivors a previous run printed, regenerated (refine.py unchanged, so the same line, operator and mutated text); for
        # judging fixtures written from those survivors without the whole study again. Several mutants can share a line and an operator, so the
        # mutated text is part of the match
        log = open(sys.argv[sys.argv.index('--only') + 1], encoding='utf-8', errors='replace').read().split('\n')
        want = set()
        for i, ln in enumerate(log):
            m = re.match(r'^SURVIVES (\w+) line (\d+) \[(.*)\]$', ln)
            if m and i + 2 < len(log) and log[i + 2].startswith('    now: '):
                want.add((int(m.group(2)), m.group(1), m.group(3), log[i + 2][9:]))
        ms = [x for x in ms if (x[0], x[1], x[2], x[3].strip()[:150]) in want]
        print('--only: %d of the %d survivors listed regenerated' % (len(ms), len(want)))
        if len(ms) != len(want):
            raise SystemExit('some survivors could not be regenerated: has refine.py changed since that run?')
    if limit and limit < len(ms):
        random.Random(seed).shuffle(ms)
        ms = sorted(ms[:limit])
    lines = src.split('\n')
    killed, survivors, t0 = 0, [], time.time()
    for k, (n, name, what, newline) in enumerate(ms, 1):
        text = '\n'.join(lines[:n - 1] + [newline] + lines[n:])
        dead, why = run_mutant(text)
        if dead:
            killed += 1
        else:
            survivors.append((n, name, what, lines[n - 1].strip(), newline.strip(), text))
        if k % 20 == 0:
            print('  %d/%d: %d killed, %d survive, %.0f s' % (k, len(ms), killed, len(survivors), time.time() - t0), flush=True)
    print('%d mutants: %d killed by the fast court (%.1f%%), %d survive, %.0f s' % (len(ms), killed, 100.0 * killed / max(1, len(ms)), len(survivors), time.time() - t0))
    still = []
    for n, name, what, old, new, text in survivors:
        verdict = ''
        if '--full-survivors' in sys.argv:
            dead, why = run_mutant(text, full=True)
            verdict = '  [the whole court kills it: %s]' % why if dead else '  [the whole court does not notice either]'
            if not dead:
                still.append((n, name))
        print('SURVIVES %s line %d [%s]%s\n    was: %s\n    now: %s' % (name, n, what, verdict, old[:150], new[:150]))
    if '--full-survivors' in sys.argv:
        print('%d of the %d survivors are not noticed by the whole court either' % (len(still), len(survivors)))


if __name__ == '__main__':
    main()
