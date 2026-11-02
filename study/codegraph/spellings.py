"""spellings.py -- which spelling of each construct the code actually uses.   python spellings.py

The Ring grammar accepts several spellings of one construct (`func`, `function`, `def`; `ok`, `end`, `endif`; `see`, `put`, `?`;
`and`, `&&`; a keyword block or a `{ }` block ...) and reads keywords case-insensitively. A face prints ONE (principle 2), and
the one is decided by the corpus, not by taste: the count is by the leaf's node kind (which is the keyword, lower-cased) under its
parent, and the original text is kept to count the case. Corpora: the Haro spike, Ring's standard library, Ring++'s probes, and
the thirty smallest Softanza files (the library's own habit, without the cost of the big ones).
"""
import collections, glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cst

sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
STZ = r'D:\GitHub\stzlib\libraries\stzlib\base'


def files():
    spike = sorted(glob.glob(os.path.join(paths.SPIKE, '*.ring')))
    stdlib = sorted(glob.glob(os.path.join(ROOT, 'vendor', 'ring-stdlib', '**', '*.ring'), recursive=True))
    ringpp = sorted(glob.glob(os.path.join(ROOT, 'bench', '*.ring')) + glob.glob(os.path.join(ROOT, 'tests', '*.ring')))
    stz = sorted(glob.glob(os.path.join(STZ, '**', '*.ring'), recursive=True), key=os.path.getsize)[:30]
    return spike + stdlib + ringpp + stz


if __name__ == '__main__':
    count = collections.Counter()
    variants = collections.Counter()
    case = collections.Counter()
    n = 0
    for p in files():
        r = subprocess.run([cst.RNXC, 'dump', p], capture_output=True, timeout=300)
        try:
            root, err = cst.parse_dump(r.stdout.decode('latin-1'))
        except ValueError:
            continue
        if err or root is None:
            continue
        n += 1
        stack = [root]
        while stack:
            node = stack.pop()
            if not node.kids and node.parent is not None and node.kind not in ('identifier', 'number', 'string', 'comment', 'symbol'):
                count[(node.parent.kind, node.kind)] += 1
                if node.text is not None and node.kind[:1].isalpha():
                    case['differs from the lower-case keyword' if node.text != node.kind else 'is the lower-case keyword'] += 1
            if node.kind in ('self', 'super', 'boolean', 'null') and node.text is not None:
                variants[(node.kind, node.text)] += 1
            stack.extend(node.kids)
    keys = ['function_definition', 'if_statement', 'elseif_clause', 'else_clause', 'while_statement', 'for_statement', 'switch_statement',
            'case_clause', 'other_clause', 'try_statement', 'see_statement', 'give_statement', 'exit_statement', 'loop_statement',
            'class_definition', 'class_parent', 'binary_expression', 'unary_expression', 'self', 'anonymous_function', 'return_statement']
    out = {}
    print(f'  {n} files')
    for par in keys:
        items = sorted(((v, k) for (p, k), v in count.items() if p == par), reverse=True)
        if items:
            tot = sum(v for v, _ in items)
            print(f'  {par:20s} ' + '  '.join(f'{k} {v} ({100 * v / tot:.0f}%)' for v, k in items[:9]))
            out[par] = {k: v for v, k in items}
    print('  keyword case:', dict(case))
    print('  the four literals, as written:', dict(sorted(variants.items(), key=lambda kv: -kv[1])))
    out['literals'] = {f'{k}:{t}': v for (k, t), v in variants.items()}
    json.dump({'files': n, 'spellings': out, 'case': dict(case)}, open(os.path.join(HERE, 'spellings.json'), 'w'), indent=1)
