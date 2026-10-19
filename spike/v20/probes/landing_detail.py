"""probes/landing_detail.py -- the literal assignments a refinement drafted at one revision could NOT land on at the next, one by one (refine_check's H count,
opened): what the old statement said, and what the next revision says of the same variable.   python haro/spike/v20/probes/landing_detail.py [revisions]"""
import copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'v19'))
import refine, ids, l1, ids_check

n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rows = []
for repo, path in ids_check.hand_written():
    revs = ids_check.revisions(repo, path, n)
    gs = []
    for rv, pth in revs:
        try:
            gs.append(ids_check.graph_at(repo, rv, pth))
        except Exception:
            gs.append(None)
    for k, (a, b) in enumerate(zip(gs, gs[1:])):
        if a is None or b is None:
            continue
        og, ng = copy.deepcopy(a), copy.deepcopy(b)
        ids.number(og)
        ids.carry(og, ng)
        now = {it['_id']: it for it, *_ in refine.walk_items(ng)}
        lits_new = {}
        for it, *_ in refine.walk_items(ng):
            if it['k'] == 'expr' and it['e']['k'] == 'assign' and it['e'].get('op') == '=' and it['e']['l']['k'] == 'id':
                lits_new.setdefault(it['e']['l']['text'].lower(), []).append(l1.print_ring({'k': 'file', 'items': [ids.strip(it)]}).strip())
        for it, *_ in refine.walk_items(og):
            if it['k'] == 'expr' and it['e']['k'] == 'assign' and it['e'].get('op') == '=' and it['e']['l']['k'] == 'id' and refine.literal_text(it['e']['r']) is not None:
                n2 = now.get(it['_id'])
                lhs = it['e']['l']['text'].lower()
                old = l1.print_ring({'k': 'file', 'items': [ids.strip(it)]}).strip()
                if n2 is None:
                    rows.append((os.path.basename(path), k, 'gone', old, lits_new.get(lhs, [])[:2]))
                elif not (n2['k'] == 'expr' and n2['e']['k'] == 'assign' and n2['e']['l']['k'] == 'id' and n2['e']['l']['text'].lower() == lhs):
                    rows.append((os.path.basename(path), k, 'other', old, [l1.print_ring({'k': 'file', 'items': [ids.strip(n2)]}).strip()[:70]]))
for r in rows:
    print('%-22s #%d %-6s %-44s -> %s' % r)
print(len(rows), 'did not land')
