"""A corpus the lint's author did not compose: the REASON seats of the refinement court's fixtures and the leading comments of Softanza's base library, run through the lint with an empty point
(calls nothing, writes nothing). Prose written for other purposes by other hands: every finding is a candidate false positive, read one by one."""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import task_lint as TL

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
texts = []
for fp in glob.glob(os.path.join(ROOT, 'haro', 'spike', 'v20', 'fixtures*.txt')):
    s = open(fp, encoding='utf-8', errors='replace').read()
    texts += [('reason', os.path.basename(fp), m) for m in re.findall(r'REASON "([^"]+)"', s)]
lib = r'D:\GitHub\stzlib\libraries\stzlib\base'
n = 0
for fp in glob.glob(os.path.join(lib, 'list', '*.ring'))[:40] + glob.glob(os.path.join(lib, 'string', '*.ring'))[:40]:
    try:
        lines = open(fp, encoding='utf-8', errors='replace').read().split('\n')
    except OSError:
        continue
    for i, l in enumerate(lines):
        if re.match(r'\s*(def|func)\s', l) and i > 0 and lines[i - 1].strip().startswith('#') and len(lines[i - 1].strip()) > 30:
            texts.append(('comment', os.path.basename(fp), lines[i - 1].strip().lstrip('# ').strip()))
            n += 1
flagged = []
for kind, src, t in texts:
    f = TL.lint(t, calls='', writes='', own=(), params=('aL', 'cText', 'n'), defined=())
    if f:
        flagged.append((kind, src, t, [str(x)[:110] for x in f]))
print('%d texts (%d reasons, %d comments); %d flagged' % (len(texts), len([x for x in texts if x[0] == 'reason']), n, len(flagged)))
for kind, src, t, f in flagged[:40]:
    print('  [%s %s] %s\n      -> %s' % (kind, src, t[:110], f[0]))
