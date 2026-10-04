"""round.py -- the round trip on the Ring face: text -> tree -> canonical text -> tree, and the two trees compared.

  python haro/study/codegraph/round.py <file.ring> ...      one line a file
The comparison is exact on everything but layout: the same nodes in the same shape, the same token texts, the same
comments, the same hidden tokens. A file the parser reports an error for, or that cst.py cannot place, is counted and
named, never measured.
"""
import os, sys, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cst, printer

SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratch')


def signature(root):
    """Pre-order (depth, kind) of every node, then every leaf's text and hidden tokens: what the tree SAYS, no layout."""
    shape, leaves = [], []

    def walk(n, d):
        shape.append((d, n.kind))
        if not n.kids:
            leaves.append((n.kind, n.text, tuple(n.hidden_before)))
        for k in n.kids:
            walk(k, d + 1)
    walk(root, 0)
    return shape, leaves


def first_difference(a, b):
    sa, la = signature(a)
    sb, lb = signature(b)
    for i in range(min(len(sa), len(sb))):
        if sa[i] != sb[i]:
            return ('shape', i, sa[max(0, i - 2):i + 2], sb[max(0, i - 2):i + 2])
    if len(sa) != len(sb):
        return ('shape length', len(sa), len(sb))
    for i in range(len(la)):
        if la[i] != lb[i]:
            return ('leaf', i, la[i], lb[i])
    return None


def one(path):
    """-> (status, detail). status in: same, differs, error, unplaced."""
    a, src, rep = cst.recover(path)
    if rep['error']:
        return 'error', 'the parser reports an error'
    if rep['bad']:
        return 'unplaced', rep['bad'][0]
    text = printer.print_ring(a)
    os.makedirs(SCRATCH, exist_ok=True)
    tmp = os.path.join(SCRATCH, 'rt.ring')
    open(tmp, 'wb').write(text.encode('latin-1'))
    b, _, repb = cst.recover(tmp)
    if repb['error']:
        return 'differs', ('the printed text does not parse', None)
    if repb['bad']:
        return 'differs', ('the printed text cannot be placed', repb['bad'][0])
    d = first_difference(a, b)
    return ('same', None) if d is None else ('differs', d)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        st, det = one(p)
        print(st, os.path.basename(p), json.dumps(det, default=str)[:300] if det else '')
