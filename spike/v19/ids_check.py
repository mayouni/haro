"""Judges rung 19, node identity on the program graph of rung 18, for the Ring++ face:
   python haro/spike/v19/ids_check.py [--plant] [--quick] [--wide]      (exit 1 on any failure)

  F  the fixtures (v19/fixtures.txt, composed before the code): an edit as an old Ring program and a new one, and the ids the new
     program must hold -- which old id each of its items kept, which are new, and which old ids are gone
  C  two controls that must FAIL: a matcher that pairs items by position, and one that keeps nothing. Each must fail a third of the
     fixtures, and the first must fall under the retention floor on real history
  H  Haro's own history: every hand-written Ring file of haro/spike, consecutive revisions read with `git show`, each old statement a
     refinement TARGET -- does it still resolve in the next revision? The floors: 95 percent (below it, CODEGRAPH 3.7 moves to option C)
     and the number of pairs and statements the sample must hold. K2 (90 percent) is printed beside it.
  W  with --wide, the memo's seven files of 4.4 as well, three of them stzlib's (read-only): the baseline 98.1 percent
The matcher is v19/ids.py; the graph it works on is rung 18's.
"""
import copy, glob, hashlib, json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.HARO                              # the repository whose history H reads
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'v18'))
import ids, l1

PLANT = '--plant' in sys.argv
QUICK = '--quick' in sys.argv
WIDE = '--wide' in sys.argv
SCRATCH = os.path.join(HERE, 'scratch')
FIXTURE_FLOOR = 20
RETENTION_FLOOR = 0.95          # CODEGRAPH 3.7: below it, ids move into a sidecar (option C)
K2 = 0.90                       # CODEGRAPH section 6, K2: below it, ids must live in the text
PAIRS_FLOOR, STATEMENTS_FLOOR = 20, 8000
MAX_REVS = 4 if QUICK else 7
fails = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def write(name, data):
    os.makedirs(SCRATCH, exist_ok=True)
    p = os.path.join(SCRATCH, name)
    open(p, 'wb').write(data if isinstance(data, bytes) else data.encode('latin-1'))
    return p


def graph_of(text, name):
    g, why = l1.parse_ring(write(name, text))
    return g


# ---- the fixtures ---------------------------------------------------------------------------------------------------------------------

def read_fixtures(path):
    fx, cur, sec = [], None, None
    raw = open(path, 'rb').read().decode('latin-1').replace('\r\n', '\n')
    for line in raw.split('\n'):
        if line.startswith('=== '):
            num, _, name = line[4:].partition(' ')
            cur = {'id': num, 'name': name, 'old': None, 'new': None, 'ids': None, 'lost': None}
            fx.append(cur)
            sec = None
        elif cur is None or line.startswith('~~~'):
            continue
        elif line in ('--- old', '--- new', '--- ids', '--- lost'):
            sec = line[4:]
            cur[sec] = []
        elif sec is not None:
            cur[sec].append(line)
    for f in fx:
        for s in ('old', 'new'):
            lines = f[s]
            while lines and lines[-1] == '':
                lines.pop()
            f[s] = '\n'.join(lines) + '\n'
        f['ids'] = ' '.join(f['ids']).split()
        f['lost'] = ' '.join(f['lost']).split()
    return fx


def run_fixture(f):
    """-> (the new items' ids as the fixture writes them, the lost ids), or (None, why)."""
    og = graph_of(f['old'], 'o%s.ring' % f['id'])
    ng = graph_of(f['new'], 'n%s.ring' % f['id'])
    if og is None or ng is None:
        return None, 'unparsed'
    ids.number(og)
    first_fresh = og['_next']
    rep = ids.carry(og, ng)
    got = ['*' if it['_id'] >= first_fresh else str(it['_id']) for it in ids.preorder(ng)]
    lost = [str(i) for i in sorted(rep['lost_ids'])] or ['-']
    return (got, lost), None


def judge_fixtures(fx):
    bad = []
    for f in fx:
        res, why = run_fixture(f)
        if res is None:
            bad.append((f['id'], why))
            continue
        got, lost = res
        want_lost = f['lost'] or ['-']
        if got != f['ids'] or lost != want_lost:
            bad.append((f['id'], f"ids {' '.join(got)} / want {' '.join(f['ids'])}; lost {' '.join(lost)} / want {' '.join(want_lost)}"))
    return bad


def sanity(fx):
    """Whatever the edit: ids are unique, and carrying a graph onto itself changes nothing."""
    bad = []
    for f in fx:
        og = graph_of(f['old'], 's%s.ring' % f['id'])
        ng = graph_of(f['new'], 't%s.ring' % f['id'])
        ids.number(og)
        ids.carry(og, ng)
        seen = ids.ids_of(ng)
        if len(seen) != len(set(seen)):
            bad.append((f['id'], 'an id appears twice'))
        again = copy.deepcopy(ng)
        twin = ids.strip(ng)
        ids.carry(ng, twin)
        if ids.ids_of(twin) != ids.ids_of(ng):
            bad.append((f['id'], 'the same graph carried onto itself moved an id'))
    return bad


# ---- the controls ---------------------------------------------------------------------------------------------------------------------

def positional(self, olds, news, params=False):
    for o, n in zip(olds, news):
        if o['k'] == n['k']:
            self.pair(o, n, 'position')
            for path, nl in dict(ids.blocks(n)).items():
                ol = dict(ids.blocks(o)).get(path)
                if ol is not None:
                    self.match_block(ol, nl)


def nothing(self, olds, news, params=False):
    return None


def with_matcher(fn, body):
    saved = ids.Run.match_block
    ids.Run.match_block = fn
    try:
        return body()
    finally:
        ids.Run.match_block = saved


# ---- history ---------------------------------------------------------------------------------------------------------------------------

def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True)


def hand_written():
    out = [p for p in git(ROOT, 'ls-files', 'spike/*.haro').stdout.decode().split() if not paths.is_declaration(os.path.join(ROOT, p))]
    keep = []
    for p in sorted(out):
        head = open(os.path.join(ROOT, p), 'rb').read(400)
        if b'GENERATED by forge.haro' in head:
            continue
        keep.append((ROOT, p))
    return keep


MEMO_SEVEN = [
    (ROOT, 'spike/court_lib.haro'), (ROOT, 'spike/haro_lib.haro'), (ROOT, 'spike/forge.haro'), (ROOT, 'spike/n_lib.haro'),
    (r'D:\GitHub\stzlib', 'libraries/stzlib/base/meta/stzCodeGraph.ring'),
    (r'D:\GitHub\stzlib', 'libraries/stzlib/base/refine/stzRefinableCode.ring'),
    (r'D:\GitHub\stzlib', 'libraries/stzlib/base/natural/stzNatural.ring'),
]


def revisions(repo, path, n):
    """(revision, the file's path AT that revision), oldest first, the last n: `--follow` crosses a rename (stzu.ring became haro.haro)."""
    lines = git(repo, 'log', '--follow', '--name-only', '--format=%H', '--', path).stdout.decode().split('\n')
    out, rev = [], None
    for ln in lines:
        ln = ln.strip()
        if len(ln) == 40 and all(c in '0123456789abcdef' for c in ln):
            rev = ln
        elif ln and rev:
            out.append((rev, ln))
            rev = None
    return list(reversed(out))[-n:]


def graph_at(repo, rev, path):
    """The L1 graph of a file at a revision, cached by blob: None when the revision does not parse."""
    os.makedirs(SCRATCH, exist_ok=True)
    blob = git(repo, 'rev-parse', '%s:%s' % (rev, path)).stdout.decode().strip()
    cache = os.path.join(SCRATCH, 'g_%s.json' % blob)
    if os.path.exists(cache):
        return json.load(open(cache))
    data = git(repo, 'show', '%s:%s' % (rev, path)).stdout
    g, _ = l1.parse_ring(write('b_%s.ring' % blob, data))
    json.dump(g, open(cache, 'w'))
    return g


TOOL_COMMITS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'v20', 'tool_commits.txt')


def tool_commits():
    """The commits a tool made, not a person (the author's "Exclude tool commits", 2026-11-08, ruled for stage 24's history and read here
    by this stage's own words: "after the next HUMAN edit"). Applied here 2026-11-09, when v0.47 and v0.48's renames, made in place by a
    tool, let the position control keep 96.6% of a history it must keep less than 95% of."""
    if not os.path.exists(TOOL_COMMITS):
        return set()
    return {ln.split()[0] for ln in open(TOOL_COMMITS, encoding='utf-8') if ln.strip() and not ln.startswith('#')}


TOOLS = tool_commits()


def replay(sources, n):
    """Old statements as refinement targets over every consecutive pair of revisions: -> totals and the per-pass diagnostics. A pair
    whose later revision is a tool's commit is no human edit: left out, and counted in `tool`."""
    tot = {'pairs': 0, 'skipped': 0, 'tool': 0, 'total': {}, 'same': {}, 'edited': {}, 'lost': {}, 'how': {}, 'sims': [], 'files': 0}
    for repo, path in sources:
        revs = revisions(repo, path, n)
        gs = []
        for rv, pth in revs:
            try:
                gs.append(graph_at(repo, rv, pth))
            except Exception:
                gs.append(None)
        used = False
        for (a, b), (rv_b, _) in zip(zip(gs, gs[1:]), revs[1:]):
            if rv_b in TOOLS:
                tot['tool'] += 1
                continue
            if a is None or b is None:
                tot['skipped'] += 1
                continue
            og, ng = copy.deepcopy(a), copy.deepcopy(b)
            ids.number(og)
            rep = ids.carry(og, ng)
            tot['pairs'] += 1
            used = True
            for key in ('total', 'same', 'edited', 'lost', 'how'):
                for k, v in rep[key].items():
                    tot[key][k] = tot[key].get(k, 0) + v
            tot['sims'].extend(rep['sims'])
        tot['files'] += used
    return tot


def share(tot, cls='statement'):
    t = tot['total'].get(cls, 0)
    if not t:
        return 0.0, 0.0
    same, edited = tot['same'].get(cls, 0), tot['edited'].get(cls, 0)
    return (same + edited) / t, same / t


# ---- the court -------------------------------------------------------------------------------------------------------------------------

def main():
    t0 = time.time()
    print('ids_check -- node identity on the program graph, Ring++ face (rung 19)')
    fx = read_fixtures(os.path.join(HERE, 'fixtures.txt'))
    check(len(fx) >= FIXTURE_FLOOR, f'F the fixtures hold {len(fx)} edits, at or above the pinned floor of {FIXTURE_FLOOR}')
    bad = judge_fixtures(fx)
    for fid, why in bad[:8]:
        print(f'  FAIL F{fid}: {why[:300]}')
    fails.extend(f'F{fid}' for fid, _ in bad)
    check(not bad, f'F {len(fx)} edits: each item of the new program holds the id the fixture says, and the lost ids are the ones it says ({len(bad)} fail)')
    sb = sanity(fx)
    for fid, why in sb[:4]:
        print(f'  FAIL F{fid}: {why}')
    fails.extend(f'F{fid} sanity' for fid, _ in sb)
    check(not sb, f'F every id is unique, and a graph carried onto itself moves none ({len(sb)} fail)')

    # controls, on the fixtures first
    for name, fn in (('pairs items by position', positional), ('keeps nothing', nothing)):
        nbad = len(with_matcher(fn, lambda: judge_fixtures(fx)))
        check(nbad * 3 >= len(fx), f'C the control, a matcher that {name}, fails {nbad} of {len(fx)} fixtures (a third is the floor)')

    # every pass of the matcher is the one thing that finds something: switched off, a fixture must fail
    for label, kw in (('the move pass (C)', {'USE_MOVE': False}), ('the function pool (D)', {'USE_POOL': False}),
                      ('similarity (B)', {'SIM_MIN': 1.01}), ('the rename pass', {'RENAME_MIN': 1.01})):
        saved = {k: getattr(ids, k) for k in kw}
        for k, v in kw.items():
            setattr(ids, k, v)
        try:
            nbad = len(judge_fixtures(fx))
        finally:
            for k, v in saved.items():
                setattr(ids, k, v)
        check(nbad >= 1, f'C with {label} switched off, {nbad} fixture(s) fail: it is load-bearing')

    # history
    srcs = hand_written()
    check(len(srcs) >= 10, f'H Haro holds {len(srcs)} hand-written Ring files in haro/spike (floor 10)')
    tot = replay(srcs, MAX_REVS)
    ret, same = share(tot)
    nst = tot['total'].get('statement', 0)
    print(f"  --   {tot['pairs']} pairs of consecutive revisions over {tot['files']} files, {nst} old statements ({tot['skipped']} pairs skipped: a revision that does not parse; "
          f"{tot['tool']} end at one of the {len(TOOLS)} commits a tool made, v20/tool_commits.txt: no human edit, left out)")
    print(f"  --   statements: {same*100:.1f}% kept with the same text (the memo's measure, 98.1% on its seven files), {ret*100:.1f}% keep their id; "
          f"definitions {share(tot, 'definition')[0]*100:.1f}%, comments {share(tot, 'comment')[0]*100:.1f}%")
    how = ', '.join(f'{k} {v}' for k, v in sorted(tot['how'].items(), key=lambda kv: -kv[1]))
    print(f'  --   matched by: {how}')
    near = sum(1 for s, k in tot['sims'] if s < 0.7)
    print(f"  --   {len(tot['sims'])} items kept by similarity, {near} of them under 0.7: the identity claimed nearest the threshold")
    check(tot['pairs'] >= PAIRS_FLOOR and nst >= STATEMENTS_FLOOR,
          f"H the sample is not shrinking: {tot['pairs']} pairs (floor {PAIRS_FLOOR}), {nst} statements (floor {STATEMENTS_FLOOR})")
    check(ret >= RETENTION_FLOOR, f'H {ret*100:.1f}% of the statements a refinement could have targeted still resolve after the next human edit; '
                                  f'the floor is {RETENTION_FLOOR*100:.0f}% (CODEGRAPH 3.7), and K2 fires below {K2*100:.0f}%')
    check(ret >= same, 'H identity keeps at least what the same text keeps: an edited statement is a kept id, never a lost one')
    # the position control, on history
    ptot = with_matcher(positional, lambda: replay(srcs, MAX_REVS))
    pret, _ = share(ptot)
    check(pret < RETENTION_FLOOR, f'C the control, a matcher that pairs items by position, keeps {pret*100:.1f}% on the same history: under the floor, as it must')

    if WIDE:
        wtot = replay(MEMO_SEVEN, 12)
        wret, wsame = share(wtot)
        print(f"  --   the memo's seven files, up to 12 revisions: {wtot['pairs']} pairs, {wtot['total'].get('statement', 0)} statements, "
              f'{wsame*100:.1f}% kept with the same text (memo: 98.1%), {wret*100:.1f}% keep their id')
    if PLANT:
        fails.append('PLANTED')
        print('  FAIL PLANTED')
    print(f'ids_check: {"FAIL" if fails else "PASS"} ({len(fails)} failure(s), {time.time() - t0:.0f} s)')
    return 1 if fails else 0


if __name__ == '__main__':
    import threading
    sys.setrecursionlimit(200_000)
    threading.stack_size(128 * 1024 * 1024)
    rc = []
    t = threading.Thread(target=lambda: rc.append(main()))
    t.start()
    t.join()
    sys.exit(rc[0] if rc else 1)
