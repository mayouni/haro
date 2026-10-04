"""identity.py -- can a node keep its identity across a real edit, with nothing but a name and a content hash?

The Refine graph model (RCP 1.4) requires stable node identifiers: a refinement targets a node, and the node survives the
change. A face is edited as TEXT, so identity has to be recovered when the edited text is parsed again. This measures the
cheapest matcher there is -- a function by its qualified name, a statement by the hash of its tokens, statements in a matched
function aligned by longest common subsequence -- over the real history of real files: consecutive revisions, old against new.

  kept         an old statement with an identical statement in the matched function of the new revision
  changed      an old statement in a matched function with no identical counterpart (edited or deleted)
  lost         an old statement whose function has no namesake in the new revision (renamed, moved or deleted)
The share that is `kept` is the identity a name-and-hash matcher already gives for free; the rest is what a tree matcher
(or an id written into the text) would have to carry. History is read with `git show`; stzlib is read-only.

  python haro/study/codegraph/identity.py [--quick]
"""
import difflib, hashlib, os, subprocess, sys, json, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cst

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCRATCH = os.path.join(HERE, 'scratch')
STMT = {'expression_statement', 'return_statement', 'see_statement', 'give_statement', 'if_statement', 'for_statement',
        'while_statement', 'switch_statement', 'try_statement', 'do_again_statement', 'exit_statement', 'loop_statement',
        'bye_statement', 'load_statement', 'import_statement'}
SOURCES = [
    (ROOT, 'haro/spike/court_lib.ring'), (ROOT, 'haro/spike/haro_lib.ring'), (ROOT, 'haro/spike/forge.ring'),
    (ROOT, 'haro/spike/n_lib.ring'),
    (r'D:\GitHub\stzlib', 'libraries/stzlib/base/meta/stzCodeGraph.ring'),
    (r'D:\GitHub\stzlib', 'libraries/stzlib/base/refine/stzRefinableCode.ring'),
    (r'D:\GitHub\stzlib', 'libraries/stzlib/base/natural/stzNatural.ring'),
]
MAX_REVS = 12 if '--quick' not in sys.argv else 4


def tok_hash(node):
    h = hashlib.sha1()
    for lf in node.leaves():
        h.update((lf.kind + ':' + (lf.text or '') + ' ' + ' '.join(lf.hidden_before) + '\n').encode('latin-1', 'replace'))
    return h.hexdigest()[:12]


def name_of(fn):
    for k in fn.kids:
        if k.kind == 'identifier':
            return k.text
    return '?'


def units(root):
    """{qualified function name: [statement hashes]}; the script body and each class body are units too."""
    out = {}

    def stmts(node):
        # every statement at any depth, in order, a nested definition left to its own unit: an edit inside an `if` changes
        # the `if` and keeps the statements around it
        found = []

        def go(n):
            for k in n.kids:
                if k.kind in ('function_definition', 'class_definition'):
                    continue
                if k.kind in STMT:
                    found.append(tok_hash(k))
                go(k)
        go(node)
        return found

    def walk(node, cls):
        for k in node.kids:
            if k.kind == 'class_definition':
                cname = name_of(k)
                out.setdefault('<class ' + cname + '>', []).extend(stmts(k))
                walk(k, cname)
            elif k.kind == 'function_definition':
                q = (cls + '.' if cls else '') + name_of(k)
                out.setdefault(q, []).extend(stmts(k))
    out['<top>'] = stmts(root)
    walk(root, '')
    return out


def revisions(repo, path):
    r = subprocess.run(['git', '-C', repo, 'log', '--format=%h', '--follow', '--', path], capture_output=True, text=True)
    return list(reversed(r.stdout.split()))[-MAX_REVS:]


def fetch(repo, rev, path, i):
    os.makedirs(SCRATCH, exist_ok=True)
    data = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True).stdout
    p = os.path.join(SCRATCH, f'rev{i}.ring')
    open(p, 'wb').write(data)
    return p


def compare(old, new):
    kept = changed = lost = 0
    for name, hs in old.items():
        if name not in new:
            lost += len(hs)
            continue
        sm = difflib.SequenceMatcher(None, hs, new[name], autojunk=False)
        k = sum(b.size for b in sm.get_matching_blocks())
        kept += k
        changed += len(hs) - k
    return kept, changed, lost


if __name__ == '__main__':
    allpairs, rows = [], []
    for repo, path in SOURCES:
        revs = revisions(repo, path)
        trees = []
        for i, rv in enumerate(revs):
            p = fetch(repo, rv, path, i)
            root, src, rep = cst.recover(p)
            trees.append(units(root) if root is not None and not rep['error'] and not rep['bad'] else None)
        pairs = [(trees[i], trees[i + 1]) for i in range(len(trees) - 1) if trees[i] is not None and trees[i + 1] is not None]
        K = C = L = 0
        fr = []
        for a, b in pairs:
            k, c, l = compare(a, b)
            K += k
            C += c
            L += l
            if k + c + l:
                fr.append(k / (k + c + l))
        rows.append(dict(file=path, revisions=len(revs), pairs=len(pairs), kept=K, changed=C, lost=L, median_pair=statistics.median(fr) if fr else None,
                         pairs_95=sum(1 for f in fr if f >= 0.95), all=len(fr)))
        tot = K + C + L
        print(f'  {os.path.basename(path):24s} {len(revs):2d} revisions {len(pairs):2d} pairs: {tot:6d} old statements: '
              f'{100 * K / max(tot, 1):5.1f}% kept, {100 * C / max(tot, 1):4.1f}% changed, {100 * L / max(tot, 1):4.1f}% lost | '
              f'median pair keeps {100 * (statistics.median(fr) if fr else 0):5.1f}%, {sum(1 for f in fr if f >= 0.95)} of {len(fr)} pairs keep 95%+')
    K = sum(r['kept'] for r in rows)
    C = sum(r['changed'] for r in rows)
    L = sum(r['lost'] for r in rows)
    print(f'  all: {K + C + L} old statements over {sum(r["pairs"] for r in rows)} edits: {100 * K / (K + C + L):.1f}% kept by a name-and-hash matcher, '
          f'{100 * C / (K + C + L):.1f}% changed in place, {100 * L / (K + C + L):.1f}% lost with their function')
    json.dump(rows, open(os.path.join(HERE, 'identity.json'), 'w'), indent=1)
