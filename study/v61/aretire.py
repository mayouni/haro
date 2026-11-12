"""Haro's own code without the `a` letter (v0.61, D73, TYPES.md T6): each name lettered `a` -- a global ($a), a local, a parameter (pa)
-- takes `v` when every value the tree gives it is a list literal, and `x` otherwise; one decision per name for the whole tree, so a
global read in many files stays one name. A global named inside a text (the forge writes `$aCourtAsk = ...` into the courts it makes)
follows it. A local's rename that lands on a name already in its function is refused and listed, unless OVERRIDE names it; a global's,
on a name anywhere in the tree. v0.61's cases, which write `a` on purpose, are left; a rung's fixtures.json follows its cases' renames
(a name in an expected message), the new name being as long as the old, so no column moves.

  python study/v61/aretire.py --plan              print only
  python study/v61/aretire.py                     rewrite
  python study/v61/aretire.py --root DIR [--plan] another tree's .haro files, in place (stzlib's landed modules); its refusals
                                                  are listed for its own desk to name, and no fixture follows
"""
import collections, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'port'))
import haroport as H

SKIP = ('spike/v61/cases/',)
A_NAME = re.compile(r'^([$@]?)(p?)a([A-Z]\w*)$')
# a local whose v or x name is already in its function: the name it takes there, chosen by reading the function
OVERRIDE = {
    ('spike/cond_lib.haro', 1021, 'aV'): 'xView',   # CondViewIn's answer, a row or empty; xV is the path's scalar
    ('spike/cond_lib.haro', 1547, 'aR'): 'vR',      # begun [] and grown by Insert; xR is one range
    ('spike/pattern_lib.haro', 153, 'aX'): 'xItem', # PatItem's answer; xX is a literal item
}


def code_files(root=None):
    if root:
        files = [os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/') for d, _, fs in os.walk(root) for f in fs if f.endswith('.haro')]
    else:
        files = subprocess.run(['git', 'ls-files', '*.haro'], capture_output=True, text=True, cwd=ROOT).stdout.split()
    out = {}
    for rel in files:
        if rel.startswith(SKIP) and not root:
            continue
        src = open(os.path.join(root or ROOT, rel), 'rb').read().decode('utf-8')
        if re.search(r'(?m)^\s*DEFINE\b', src):
            continue
        out[rel] = src
    return out


def segments(toks):
    """the function each token is in: a count that grows at each `func` or `def` beginning a line, and the line it begins at"""
    seg, line, ls = 0, 1, True
    out, starts = [], {0: 1}
    for k, v in toks:
        if k == 'nl':
            line += 1
            ls = True
        elif k not in ('ws', 'cm'):
            if ls and k == 'id' and v in ('func', 'def'):
                seg += 1
                starts[seg] = line
            ls = False
        out.append(seg)
    return out, starts


def main():
    plan = '--plan' in sys.argv
    other = os.path.abspath(sys.argv[sys.argv.index('--root') + 1]) if '--root' in sys.argv else None
    srcs = code_files(other)
    base = other or ROOT
    kinds = collections.defaultdict(set)
    names, every = set(), set()
    for rel, src in srcs.items():
        toks = H.tokens(src)
        for i, (k, v) in enumerate(toks):
            if k != 'id':
                continue
            every.add(v)
            if H.is_symbol(toks, i) or not A_NAME.match(v) or v.lower() in H.KW:   # aNd is the keyword in another case, a case of its own
                continue
            names.add(v)
            j = H.sig(toks, i, 1)
            if j is not None and toks[j][1] == '=' and not (j + 1 < len(toks) and toks[j + 1][1] == '='):
                r = H.sig(toks, j, 1)
                kinds[v].add('v' if r is not None and toks[r][1] == '[' else '?')
    rename = {}
    for v in sorted(names):
        m = A_NAME.match(v)
        letter = 'v' if kinds[v] and kinds[v] <= {'v'} else 'x'
        rename[v] = f'{m.group(1)}{m.group(2)}{letter}{m.group(3)}'
    refused = [(v, n) for v, n in rename.items() if v[0] in '$@' and n in every]
    for v, _ in refused:
        del rename[v]
    counts = collections.Counter()
    changed, fixtures = {}, collections.defaultdict(dict)
    text_re = re.compile(r'[$@]p?a[A-Z]\w*')
    for rel, src in srcs.items():
        toks = H.tokens(src)
        seg, starts = segments(toks)
        ids = collections.defaultdict(set)
        for i, (k, v) in enumerate(toks):
            if k == 'id' and not H.is_symbol(toks, i):
                ids[seg[i]].add(v)
        for i, (k, v) in enumerate(toks):
            if k == 'id' and v in rename and not H.is_symbol(toks, i):
                j = H.sig(toks, i, 1)
                if j is not None and toks[j][1] == '(' and v[0] not in '$@':
                    continue    # a call, never the variable
                new = rename[v]
                if v[0] not in '$@' and new in ids[seg[i]]:
                    key = (rel, starts[seg[i]], v)
                    if other or key not in OVERRIDE:
                        refused.append((f'{rel}:{starts[seg[i]]} {v}', new))
                        continue
                    new = OVERRIDE[key]
                toks[i][1] = new
                counts['name'] += 1
                if '/cases/' in rel and not other:
                    fixtures[rel.split('/cases/')[0]][v] = new
            elif k == 'st':
                t = text_re.sub(lambda g: rename.get(g.group(0), g.group(0)), v)
                if t != v:
                    toks[i][1] = t
                    counts['in a text'] += 1
        out = ''.join(v for _, v in toks)
        if out != src:
            changed[rel] = out
    lv = collections.Counter(n.lstrip('$@')[1 if n.lstrip('$@')[0] == 'p' else 0] for n in rename.values())
    print(f'{len(rename)} names: {lv["v"]} to v, {lv["x"]} to x; {sum(counts.values())} rewrites ({counts["in a text"]} inside a text)')
    print(f'{len(set(refused))} refused:', sorted(set(refused)))
    print(f'{len(changed)} files {"to change" if plan else "changed"}; fixtures of {len(fixtures)} rungs follow')
    if refused and not plan:
        sys.exit('refused renames: resolve them in OVERRIDE first')
    if plan:
        return
    for rel, out in changed.items():
        open(os.path.join(base, rel), 'wb').write(out.encode('utf-8'))
    for rung, ren in fixtures.items():
        for f in ('fixtures.json', 'gen_fixtures.py'):
            p = os.path.join(ROOT, rung, f)
            if not os.path.exists(p):
                continue
            t = open(p, 'rb').read().decode('utf-8')
            u = re.sub(r'(?<![\w$@])(' + '|'.join(sorted(map(re.escape, ren), key=len, reverse=True)) + r')(?!\w)',
                       lambda g: ren[g.group(1)], t)
            if u != t:
                open(p, 'wb').write(u.encode('utf-8'))
                print(f'  {rung}/{f} follows')


if __name__ == '__main__':
    main()
