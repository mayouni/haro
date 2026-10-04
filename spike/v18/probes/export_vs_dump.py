# -*- coding: utf-8 -*-
"""Does the graph change when the tree comes from `rnxc dump --json` instead of the text dump?

    python haro/spike/v18/probes/export_vs_dump.py [--stride=N | --all]

Rung 18 read the parse through `rnxc dump` and recovered what the dump loses by walking the leaves against the source (cst.recover).
Rung 3 of the code-graph memo gave rnxc an export that loses nothing (src/dumpjson.zig), and `cst.recover_export` reads it. The
abstraction is the same code either way; only its input differs, so this asks the one question the swap raises: for each file, the
graph, and the canonical text printed from it, are they the same? A difference is a place where the heuristic recovery was wrong, or
where the real tree says something the recovery could not -- each is printed, and each has to be read, not counted away.
"""
import glob, os, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
V18 = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(V18, '..', '..', '..'))
sys.path.insert(0, V18)
import cst, l1

STZ = r'D:\GitHub\stzlib\libraries\stzlib'


def corpus(stride):
    files = sorted(glob.glob(os.path.join(ROOT, 'bench', 'exec', '*.ring')))
    files += sorted(glob.glob(os.path.join(ROOT, 'vendor', 'ring-stdlib', '**', '*.ring'), recursive=True))
    files += sorted(glob.glob(os.path.join(ROOT, 'haro', 'spike', '*.ring')))
    if os.path.isdir(STZ):
        stz = sorted(glob.glob(os.path.join(STZ, '**', '*.ring'), recursive=True))
        files += [p for p in stz[::stride] if os.path.getsize(p) <= 400_000]
    return files


def graph(path, export):
    os.environ['CST_EXPORT'] = '1' if export else '0'
    try:
        g, why = l1.parse_ring(path)
    except Exception as e:                      # a shape the abstraction does not know: that is an answer too
        return None, 'raised ' + type(e).__name__ + ': ' + str(e)[:60]
    if g is None:
        return None, why
    try:
        return l1.print_ring(g), None
    except Exception as e:
        return None, 'print raised ' + type(e).__name__ + ': ' + str(e)[:60]


def main():
    stride = 7
    for a in sys.argv[1:]:
        if a == '--all':
            stride = 1
        elif a.startswith('--stride='):
            stride = int(a[9:])
    files = corpus(stride)
    same = both_none = differ = 0
    rows = []
    for i, p in enumerate(files):
        a, wa = graph(p, False)
        b, wb = graph(p, True)
        if a is None and b is None:
            both_none += 1
        elif a == b:
            same += 1
        else:
            differ += 1
            rows.append((p, a is None, b is None, wa, wb, a, b))
        if i % 200 == 199:
            print('  ...', i + 1, 'of', len(files), flush=True)
    for p, an, bn, wa, wb, a, b in rows[:40]:
        kind = 'dump-only fails' if an and not bn else 'export-only fails' if bn and not an else 'text differs'
        line = ''
        if a is not None and b is not None:
            la, lb = a.split('\n'), b.split('\n')
            k = next((k for k in range(min(len(la), len(lb))) if la[k] != lb[k]), min(len(la), len(lb)))
            line = ' at line %d: dump %r | export %r' % (k + 1, la[k][:70] if k < len(la) else None, lb[k][:70] if k < len(lb) else None)
        print('  DIFF', os.path.relpath(p, ROOT) if p.startswith(ROOT) else p, '--', kind, (wa or wb or '')[:80], line)
    print(f'{len(files)} file(s): {same} print the same, {differ} differ, {both_none} neither reader abstracts')
    return 0


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    threading.stack_size(128 * 1024 * 1024)
    t = threading.Thread(target=lambda: sys.exit(main()))
    t.start()
    t.join()
