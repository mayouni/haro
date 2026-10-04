"""ids.py -- node identity on the program graph of rung 18 (Haro v0.19, the nineteenth rung).

A refinement targets a node, and the node must survive a change: the Refine graph model (RCP) wants a stable identifier. A face is edited
as TEXT, so identity has to be RECOVERED when the edited text is parsed again -- and this is the matcher that does it, from nothing but
the two graphs: the one that was (its items carry ids) and the one that is (its items carry none).

    number(g)            the first graph: every item gets an id, 1, 2, 3 ... in pre-order; g['_next'] is the next one
    carry(old, new)      the edit: `new` gets the ids of what it keeps from `old`, a fresh id for what is new; -> a report
    strip(g)             a copy without ids, which is what L1 equality, printing and hashing are done on
    resolve(g, id)       the item holding an id, or None: does a refinement's target still resolve?

WHAT HAS AN ID. An ITEM: a statement, a definition, a comment, a parameter -- whatever stands in a block (`items`, `then`, `else`, `other`,
`finally`, `params`), at any depth, a lambda's or a brace's body included. An expression holds none: a node inside one is named by the
statement it stands in and its path.

HOW IT MATCHES, in this order, inside one list of items (v19/IDENTITY.md has the reasons, v19/fixtures.txt the rows):
  1. a DEFINITION by its name (kind, name, occurrence), wherever it stands: reordering functions moves no id
  2. the rest, by the hash of the WHOLE text: the longest common run (A), then what is left in each gap between runs by SIMILARITY of 0.6
     on its tokens, in order (B): an edit keeps its id, a replacement does not -- identity is a claim, and `b = 2` becoming `foo(bar)`
     is not the same statement
  3. what is still unmatched, by identical text anywhere in the list: a move (C)
  4. a renamed definition by the share of its body that is unchanged (0.6), after the names have had their say
  and then, for a matched pair, the same inside each of its blocks, found by their path; and for a matched FUNCTION, one more pass over
  everything still unmatched in it, by identical text: a statement wrapped in an `if`, or taken out of one, keeps its id (D).
A statement moved to ANOTHER function is lost, on purpose: `return 0` is everywhere, and the same text is not the same statement.
"""
import difflib, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v18'))
import l1

BLOCK_FIELDS = ('items', 'then', 'else', 'other', 'finally', 'params')
DEFS = l1.DEFS
SIM_MIN = 0.6               # similarity two tokenised items need to be one edited item
RENAME_MIN = 0.6            # the share of a body that must be unchanged for a renamed definition to be the same one
USE_MOVE, USE_POOL = True, True      # the two passes that find a moved statement; switched off only by probes/sweep.py, to price them
GAP_CAP = 90000             # old x new items in one gap beyond which no similarity is computed (a whole-file rewrite)


# ---- the shape ---------------------------------------------------------------------------------------------------------------------

def is_block(node, field, value):
    return field in BLOCK_FIELDS and isinstance(value, list) and not (node.get('k') == 'list' and field == 'items')


def blocks(node):
    """(path, list of items) for each block directly inside `node`, expressions looked through, in field order."""
    out = []

    def walk(x, path):
        if isinstance(x, dict):
            for f, v in x.items():
                if f == 'k' or f.startswith('_'):
                    continue
                if is_block(x, f, v):
                    out.append((path + (f,), v))
                elif isinstance(v, (dict, list)):
                    walk(v, path + (f,))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, (dict, list)):
                    walk(v, path + (i,))
    walk(node, ())
    return out


def preorder(g):
    """Every item of the graph, in pre-order: an item, then the items of its blocks in field order."""
    out = []

    def go(items):
        for it in items:
            out.append(it)
            for _, b in blocks(it):
                go(b)
    go(g['items'])
    return out


def strip(x):
    if isinstance(x, dict):
        return {f: strip(v) for f, v in x.items() if not f.startswith('_')}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def def_name(it):
    n = it.get('name')
    return '.'.join(n) if isinstance(n, list) else n


# ---- numbering and lookup -----------------------------------------------------------------------------------------------------------

def number(g, start=1):
    n = start
    for it in preorder(g):
        it['_id'] = n
        n += 1
    g['_next'] = n
    return g


def resolve(g, ident):
    for it in preorder(g):
        if it.get('_id') == ident:
            return it
    return None


def ids_of(g):
    return [it.get('_id') for it in preorder(g)]


# ---- hashes and tokens ----------------------------------------------------------------------------------------------------------------

class Memo:
    def __init__(self):
        self.deep, self.toks = {}, {}

    def dh(self, x):
        """The hash of the whole text of an item (or of anything inside one): ids and nothing else are left out."""
        if isinstance(x, dict):
            key = id(x)
            h = self.deep.get(key)
            if h is None:
                parts = [f + '=' + self.dh(v) for f, v in x.items() if not f.startswith('_')]
                h = hashlib.sha1(('{' + ','.join(parts) + '}').encode('utf-8', 'replace')).hexdigest()[:16]
                self.deep[key] = h
            return h
        if isinstance(x, list):
            return hashlib.sha1(('[' + ','.join(self.dh(v) for v in x) + ']').encode('utf-8', 'replace')).hexdigest()[:16]
        return repr(x)

    def tokens(self, it):
        """The item's kind and the values in its header (names, operators, literals), its bodies set aside; a comment is its words."""
        key = id(it)
        t = self.toks.get(key)
        if t is None:
            t = [it['k']]

            def go(x):
                if isinstance(x, dict):
                    if x.get('k') == 'comment':
                        t.extend(str(x.get('text', '')).split())
                        return
                    for f, v in x.items():
                        if f == 'k' or f.startswith('_') or is_block(x, f, v):
                            continue
                        go(v)
                elif isinstance(x, list):
                    for v in x:
                        go(v)
                else:
                    t.append(str(x))
            if it['k'] == 'comment':
                t.extend(str(it.get('text', '')).split())
            else:
                go(it)
            self.toks[key] = t
        return t

    def sim(self, a, b):
        if a['k'] != b['k']:
            return 0.0
        ta, tb = self.tokens(a), self.tokens(b)
        return difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()


# ---- the matcher -----------------------------------------------------------------------------------------------------------------------

class Run:
    """One carry: the memo, the items already paired, and why each was (the diagnostics the report reads)."""

    def __init__(self):
        self.m = Memo()
        self.paired_old = set()          # id() of old items that found their new one
        self.how = {}                    # old id -> the pass that matched it
        self.sims = []                   # (similarity, old kind) of every B pairing: how near the threshold identity was claimed
        self.sim_pairs = []              # the items themselves, for a reader who wants to look at the nearest claims

    def pair(self, o, n, how):
        n['_id'] = o['_id']
        self.paired_old.add(id(o))
        self.how[o['_id']] = how

    def copy_ids(self, o, n, how):
        """o and n are the same text: every item inside gets its counterpart's id."""
        self.pair(o, n, how)
        ob, nb = dict(blocks(o)), dict(blocks(n))
        for path, nl in nb.items():
            ol = ob.get(path)
            if ol is not None and len(ol) == len(nl):
                for a, b in zip(ol, nl):
                    self.copy_ids(a, b, how)

    def descend(self, o, n):
        ob, nb = dict(blocks(o)), dict(blocks(n))
        for path, nl in nb.items():
            ol = ob.get(path)
            if ol is not None:
                self.match_block(ol, nl, params=path[-1] == 'params')
        if n['k'] == 'func' and USE_POOL:
            self.function_pool(o, n)

    # -- one list of items
    def match_block(self, olds, news, params=False):
        if params:
            return self.match_params(olds, news)
        m = self.m
        # 1. definitions by name
        okeys, nkeys = {}, {}
        for i, it in enumerate(olds):
            if it['k'] in DEFS:
                okeys.setdefault((it['k'], def_name(it)), []).append(i)
        for j, it in enumerate(news):
            if it['k'] in DEFS:
                nkeys.setdefault((it['k'], def_name(it)), []).append(j)
        pairs = []
        for key, oi in okeys.items():
            for i, j in zip(oi, nkeys.get(key, [])):
                pairs.append((i, j))
        done_o = {i for i, _ in pairs}
        done_n = {j for _, j in pairs}
        for i, j in sorted(pairs):
            self.pair(olds[i], news[j], 'name')
            self.descend(olds[i], news[j])
        # 2. the rest, in order: A (the whole text), B (similarity)
        orest = [i for i, it in enumerate(olds) if it['k'] not in DEFS]
        nrest = [j for j, it in enumerate(news) if it['k'] not in DEFS]
        oh = [m.dh(olds[i]) for i in orest]
        nh = [m.dh(news[j]) for j in nrest]
        sm = difflib.SequenceMatcher(None, oh, nh, autojunk=False)
        mp = []                                      # (index into orest, index into nrest), whole-text matches
        for a, b, size in sm.get_matching_blocks():
            for t in range(size):
                mp.append((a + t, b + t))
        matched = {}                                 # orest idx -> (nrest idx, how)
        for a, b in mp:
            matched[a] = (b, 'text')
        used_n = {b for a, (b, _) in matched.items()}

        def gaps():
            prev_a, prev_b = -1, -1
            for a in sorted(list(matched) + [len(orest)]):
                b = matched[a][0] if a < len(orest) else len(nrest)
                yield (range(prev_a + 1, a), range(prev_b + 1, b))
                prev_a, prev_b = a, b
        # B: similar enough, in order
        for ga, gb in list(gaps()):
            if not ga or not gb or len(ga) * len(gb) > GAP_CAP:
                continue
            w = [[m.sim(olds[orest[a]], news[nrest[b]]) for b in gb] for a in ga]
            n_, m_ = len(ga), len(gb)
            dp = [[0.0] * (m_ + 1) for _ in range(n_ + 1)]
            for i in range(n_ - 1, -1, -1):
                for j in range(m_ - 1, -1, -1):
                    best = max(dp[i + 1][j], dp[i][j + 1])
                    if w[i][j] >= SIM_MIN:
                        best = max(best, dp[i + 1][j + 1] + w[i][j])
                    dp[i][j] = best
            i = j = 0
            while i < n_ and j < m_:
                if w[i][j] >= SIM_MIN and abs(dp[i][j] - (dp[i + 1][j + 1] + w[i][j])) < 1e-12:
                    matched[ga[i]] = (gb[j], 'similar')
                    used_n.add(gb[j])
                    self.sims.append((w[i][j], olds[orest[ga[i]]]['k']))
                    self.sim_pairs.append((w[i][j], olds[orest[ga[i]]], news[nrest[gb[j]]]))
                    i += 1
                    j += 1
                elif dp[i + 1][j] >= dp[i][j + 1]:
                    i += 1
                else:
                    j += 1
        # C: a move inside the list, by identical text
        left_o = [a for a in range(len(orest)) if a not in matched]
        left_n = [b for b in range(len(nrest)) if b not in used_n]
        by_hash = {}
        for b in left_n:
            by_hash.setdefault(nh[b], []).append(b)
        for a in left_o if USE_MOVE else ():
            q = by_hash.get(oh[a])
            if q:
                matched[a] = (q.pop(0), 'move')
        for a, (b, how) in sorted(matched.items()):
            o, n = olds[orest[a]], news[nrest[b]]
            if how in ('text', 'move'):
                self.copy_ids(o, n, how)
            else:
                self.pair(o, n, how)
                self.descend(o, n)
        # 4. a renamed definition: what is left of the definitions, by the share of the body that did not change
        lo = [i for i, it in enumerate(olds) if it['k'] in DEFS and i not in done_o]
        ln = [j for j, it in enumerate(news) if it['k'] in DEFS and j not in done_n]
        cands = []
        for i in lo:
            for j in ln:
                if olds[i]['k'] == news[j]['k']:
                    s = self.body_share(olds[i], news[j])
                    if s >= RENAME_MIN:
                        cands.append((-s, i, j))
        used_i, used_j = set(), set()
        for s, i, j in sorted(cands):
            if i in used_i or j in used_j:
                continue
            used_i.add(i)
            used_j.add(j)
            self.pair(olds[i], news[j], 'rename')
            self.descend(olds[i], news[j])

    def match_params(self, olds, news):
        by = {}
        for i, it in enumerate(olds):
            by.setdefault(it.get('name'), []).append(i)
        for n in news:
            q = by.get(n.get('name'))
            if q:
                self.pair(olds[q.pop(0)], n, 'name')

    def body_share(self, o, n):
        """The share of a definition's body, at every depth, that is the same text in both."""
        def bag(d):
            c = {}
            for _, b in blocks(d):
                stack = list(b)
                while stack:
                    it = stack.pop()
                    if it['k'] == 'param':
                        continue
                    h = self.m.dh(it)
                    c[h] = c.get(h, 0) + 1
                    for _, bb in blocks(it):
                        stack.extend(bb)
            return c
        bo, bn = bag(o), bag(n)
        tot = max(sum(bo.values()), sum(bn.values()))
        if tot == 0:
            return 0.0
        return sum(min(c, bn.get(h, 0)) for h, c in bo.items()) / tot

    def function_pool(self, o, n):
        """D: what is left unmatched in a matched function, old and new, at any depth: the same text is the same statement."""
        def pool(f, fresh):
            out = []
            stack = []
            for _, b in blocks(f):
                stack.extend(b)
            while stack:
                it = stack.pop(0)
                if it['k'] != 'param' and ((fresh and '_id' not in it) or (not fresh and id(it) not in self.paired_old)):
                    out.append(it)
                for _, b in blocks(it):
                    stack.extend(b)
            return out

        def size(it):
            return 1 + sum(size(x) for _, b in blocks(it) for x in b)
        po, pn = pool(o, False), pool(n, True)
        if not po or not pn:
            return
        by = {}
        for it in po:
            by.setdefault(self.m.dh(it), []).append(it)
        for it in sorted(pn, key=lambda x: -size(x)):
            if '_id' in it:
                continue                 # inside something already paired
            q = by.get(self.m.dh(it))
            while q and id(q[0]) in self.paired_old:
                q.pop(0)
            if q:
                self.copy_ids(q.pop(0), it, 'pool')


def carry(old, new):
    """`new` gets the ids it keeps from `old` and fresh ones for what is new. `old` must carry ids (see `number`)."""
    run = Run()
    run.match_block(old['items'], new['items'])
    nxt = old.get('_next') or (max([it.get('_id', 0) for it in preorder(old)] + [0]) + 1)
    for it in preorder(new):
        if '_id' not in it:
            it['_id'] = nxt
            nxt += 1
    new['_next'] = nxt
    return report(old, new, run)


# ---- what happened ---------------------------------------------------------------------------------------------------------------------

def kind_class(it):
    k = it['k']
    if k in DEFS:
        return 'definition'
    if k == 'comment':
        return 'comment'
    if k == 'param':
        return 'parameter'
    return 'statement'


def report(old, new, run=None):
    """For every item of `old`: gone, kept (the same text), or kept and edited -- by kind class, and by the pass that matched it."""
    m = run.m if run else Memo()
    now = {it['_id']: it for it in preorder(new)}
    rep = {'total': {}, 'same': {}, 'edited': {}, 'lost': {}, 'how': {}, 'lost_ids': [], 'sims': list(run.sims) if run else [], 'sim_pairs': list(run.sim_pairs) if run else []}
    for it in preorder(old):
        c = kind_class(it)
        rep['total'][c] = rep['total'].get(c, 0) + 1
        n = now.get(it['_id'])
        if n is None:
            rep['lost'][c] = rep['lost'].get(c, 0) + 1
            rep['lost_ids'].append(it['_id'])
        elif m.dh(it) == m.dh(n):
            rep['same'][c] = rep['same'].get(c, 0) + 1
        else:
            rep['edited'][c] = rep['edited'].get(c, 0) + 1
        if n is not None and run:
            h = run.how.get(it['_id'])
            rep['how'][h] = rep['how'].get(h, 0) + 1
    return rep
