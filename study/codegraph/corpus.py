"""corpus.py -- the round trip over four corpora, with controls that can fail.   python haro/study/codegraph/corpus.py [--quick]

  spike     haro/spike/*.ring                       the Haro spike's own Ring (the courts, the forge, the libraries)
  stdlib    vendor/ring-stdlib/**/*.ring            Ring's standard library as Ring ships it
  ringpp    bench/*.ring, tests/*.ring              Ring++'s probes and benchmarks
  softanza  every 38th file of stzlib's base layer  (read-only; a sample, named as one)

For each file: text -> tree -> canonical text -> tree, compared exactly but for layout (round.py). Two controls are run
first and must FAIL: a printer that puts a space before every `(` and `[` (the scanner reads those differently, so files
with calls must differ), and a printer that drops comments (every file with a comment must differ).
Results go to results.json; the report prints counts, failure classes by first difference, and what layout cost.
"""
import glob, json, os, sys, time, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cst, printer, round as rt

sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
STZ = r'D:\GitHub\stzlib\libraries\stzlib\base'
QUICK = '--quick' in sys.argv


def corpora():
    spike = sorted(glob.glob(os.path.join(paths.SPIKE, '*.ring')))
    stdlib = sorted(glob.glob(os.path.join(ROOT, 'vendor', 'ring-stdlib', '**', '*.ring'), recursive=True))
    ringpp = sorted(glob.glob(os.path.join(ROOT, 'bench', '*.ring')) + glob.glob(os.path.join(ROOT, 'tests', '*.ring')))
    stz = sorted(glob.glob(os.path.join(STZ, '**', '*.ring'), recursive=True))
    stz = [p for p in stz[::38] if os.path.getsize(p) <= 400_000]
    c = {'spike': spike, 'stdlib': stdlib, 'ringpp': ringpp, 'softanza': stz}
    if QUICK:
        c = {k: v[:12] for k, v in c.items()}
    return c


def control(name, mutate):
    """Run the round trip with a deliberately broken printer on files that should expose it; the control passes when it fails."""
    real = printer.print_ring
    printer.print_ring = mutate(real)
    try:
        hits, n = 0, 0
        for p in sample_for_controls():
            n += 1
            st, _ = rt.one(p)
            hits += st != 'same'
        return hits, n
    finally:
        printer.print_ring = real


def sample_for_controls():
    return sorted(glob.glob(os.path.join(paths.SPIKE, '*.ring')))[:8]


def glue_everything(real):
    """A printer that puts a space before every ( and [ : the scanner reads `f (x)` and `a [1]` differently from `f(x)`."""
    def p(root):
        t = real(root)
        return t.replace('(', ' (').replace('[', ' [')
    return p


def drop_comments(real):
    def p(root):
        return '\n'.join(l for l in real(root).split('\n') if not l.lstrip().startswith(('#', '//', '/*'))) + '\n'
    return p


if __name__ == '__main__':
    t0 = time.time()
    print('codegraph corpus -- text -> tree -> canonical text -> tree')
    for name, mut in (('a printer that spaces every ( and [', glue_everything), ('a printer that drops comments', drop_comments)):
        hits, n = control(name, mut)
        print(f'  control: {name}: {hits} of {n} files differ' + ('' if hits else '   <-- THE CONTROL DID NOT FAIL'))
        if not hits:
            sys.exit(1)
    results, classes = {}, collections.Counter()
    tot = collections.Counter()
    for group, files in corpora().items():
        c = collections.Counter()
        for p in files:
            try:
                st, det = rt.one(p)
            except Exception as e:                       # a crash of the tool is counted, never hidden
                st, det = 'tool', repr(e)[:120]
            c[st] += 1
            size = os.path.getsize(p)
            results[p] = {'group': group, 'status': st, 'bytes': size, 'detail': det}
            if st == 'differs' and det:
                key = det[0] if det[0] not in ('shape', 'leaf') else (det[0], str(det[2][-1] if det[0] == 'shape' else det[2][:2])[:60])
                classes[(group, str(key))] += 1
        tot.update(c)
        print(f'  {group:9s} {len(files):4d} files: {c["same"]:4d} same, {c["differs"]:3d} differ, {c["error"]:3d} parse errors, {c["unplaced"]:3d} unplaced, {c["tool"]:3d} tool')
    json.dump(results, open(os.path.join(HERE, 'results.json'), 'w'), indent=1, default=str)
    measured = tot['same'] + tot['differs']
    print(f'  all       {sum(tot.values()):4d} files: {tot["same"]} same of {measured} measured ({100 * tot["same"] / max(measured, 1):.1f}%), '
          f'{tot["error"]} not measured (the parser reports an error), {tot["unplaced"]} unplaced, {tot["tool"]} tool failures')
    for (g, k), n in classes.most_common(8):
        print(f'    differs {n:3d}  {g}: {k}')
    print(f'  {time.time() - t0:.0f} s')
