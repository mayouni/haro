"""kinds.py -- which constructs of the Ring face a second face would have to spell, and how often the code uses them.
python haro/study/codegraph/kinds.py     (the corpora of corpus.py; no alignment, only the parse)

The grammar names 59 kinds of node. A face is a spelling of them, and a spelling is only a spelling when the meaning is the
same: a kind whose Ring meaning differs from what the same shape means in Python or JavaScript is a COLLISION, and a face
must refuse it or spell it unmistakably. This counts every kind over the corpora so that the table in the design memo
is ranked by use, not by taste.
"""
import collections, glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cst
import corpus

if __name__ == '__main__':
    kinds = collections.Counter()
    files = 0
    feat = collections.Counter()
    for group, paths in corpus.corpora().items():
        for p in paths:
            r = subprocess.run([cst.RNXC, 'dump', p], capture_output=True, timeout=300)
            try:
                root, err = cst.parse_dump(r.stdout.decode('latin-1'))
            except ValueError:
                continue
            if err:
                continue
            files += 1
            stack = [root]
            while stack:
                n = stack.pop()
                kinds[n.kind] += 1
                if n.kind == 'for_statement':
                    ks = [k.kind for k in n.kids]
                    feat['for ... step'] += 'step' in ks
                    feat['for ... in'] += 'in' in ks
                    feat['for i = a to b'] += 'to' in ks
                if n.kind == 'call_expression' and n.kids and n.kids[0].kind == 'identifier' and n.kids[0].text and n.kids[0].text.lower() == 'eval':
                    feat['eval(...) calls'] += 1
                stack.extend(n.kids)
    # the grammar's own list of named kinds: a kind is named if node-types.json says so, never by how its name looks
    nt = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'vendor', 'tree-sitter-ring', 'src', 'node-types.json'), encoding='utf-8'))
    grammar_named = {x['type'] for x in nt if x.get('named')}
    named = {k: v for k, v in kinds.items() if k in grammar_named}
    total = sum(named.values())
    print(f'  {files} files; {total} named nodes of {len(named)} of {len(grammar_named)} grammar kinds; never seen: {sorted(grammar_named - set(named))}')
    for k, v in sorted(named.items(), key=lambda kv: -kv[1]):
        print(f'    {k:28s} {v:8d} {100 * v / total:5.1f}%')
    print('  features:', dict(feat))
    json.dump({'files': files, 'named': named, 'features': dict(feat)}, open(os.path.join(HERE, 'kinds.json'), 'w'), indent=1)
