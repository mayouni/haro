"""layout.py -- what the canonical text costs and saves: bytes, tokens, nodes, and the share that was layout.
python haro/study/codegraph/layout.py        (a sample; read-only on stzlib)
"""
import glob, os, sys, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cst, printer

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STZ = r'D:\GitHub\stzlib\libraries\stzlib\base'


def sample():
    spike = sorted(glob.glob(os.path.join(ROOT, 'haro', 'spike', '*.ring')))[:20]
    stdlib = sorted(glob.glob(os.path.join(ROOT, 'vendor', 'ring-stdlib', '**', '*.ring'), recursive=True))[::5]
    stz = sorted(glob.glob(os.path.join(STZ, '**', '*.ring'), recursive=True))[::190]
    stz = [p for p in stz if os.path.getsize(p) <= 300_000]
    return {'spike': spike, 'stdlib': stdlib, 'softanza': stz}


def count(n):
    return 1 + sum(count(k) for k in n.kids)


if __name__ == '__main__':
    tot = {}
    for g, files in sample().items():
        orig = printed = leaves = nodes = hidden = comments = comment_bytes = 0
        t0 = time.time()
        for p in files:
            root, src, rep = cst.recover(p)
            if rep['error'] or rep['bad']:
                continue
            text = printer.print_ring(root)
            orig += len(src)
            printed += len(text)
            leaves += rep['leaves']
            nodes += count(root)
            hidden += sum(rep['hidden'].values())
            for lf in root.leaves():
                if lf.kind == 'comment':
                    comments += 1
                    comment_bytes += len(lf.text)
        tot[g] = dict(files=len(files), orig=orig, printed=printed, leaves=leaves, nodes=nodes, hidden=hidden, comments=comments, comment_bytes=comment_bytes)
        print(f'  {g:9s} {len(files):3d} files {orig / 1024:8.0f} KB -> {printed / 1024:8.0f} KB canonical ({100 * (1 - printed / orig):4.1f}% was layout) | '
              f'{leaves / (orig / 1024):5.0f} tokens/KB, {nodes / (orig / 1024):5.0f} nodes/KB | comments {100 * comment_bytes / printed:4.1f}% of the canonical text | {time.time() - t0:.0f} s')
    json.dump(tot, open(os.path.join(HERE, 'layout.json'), 'w'), indent=1)
