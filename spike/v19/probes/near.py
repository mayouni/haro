"""The identity claimed nearest the threshold: the old and the new text of the items the matcher kept by similarity alone, lowest first.
   python haro/spike/v19/probes/near.py [N]        a claim you would not make is a defect of the threshold, not of the history"""
import copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import ids_check as ck, ids, l1
sys.setrecursionlimit(100000)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
pairs = []
for repo, path in ck.hand_written():
    revs = ck.revisions(repo, path, 7)
    gs = [ck.graph_at(repo, r, pth) for r, pth in revs]
    for a, b in zip(gs, gs[1:]):
        if a is None or b is None:
            continue
        og, ng = copy.deepcopy(a), copy.deepcopy(b)
        ids.number(og)
        rep = ids.carry(og, ng)
        for s, o, nn in rep['sim_pairs']:
            pairs.append((s, os.path.basename(path), ids.strip(o), ids.strip(nn)))
pairs.sort(key=lambda t: t[0])


def text(it):
    return l1.sexp_write(it)[:170]


print(len(pairs), 'kept by similarity; the', n, 'nearest the threshold:')
for s, f, o, nn in pairs[:n]:
    print(f'\n  {s:.2f}  {f}\n    was  {text(o)}\n    now  {text(nn)}')
