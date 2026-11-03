"""Pattern rules over blocks of typed values (COMPASS-REBOL-07): a reference model, judged by pattern_fixtures.json (written
first). A rule is C6 text -- a list -- read by block.load, so a grammar is data. Declaring a set of rules either refuses it,
naming why, or yields rules that are TOTAL by construction:

  no recursion           the named rules form a DAG (a RULE reference is followed at declaration time)
  every repetition moves  ANY, SOME and TO over a rule that can match nothing are refused (nullable analysis), so each turn of
                          a repetition consumes a value of a finite input: Parse's documented infinite loop cannot be written
  no host                 a group in a rule (Parse's paren!), WHILE and DO are refused; so are the editing words -- a pattern
                          judges and never edits
  INTO descends           into a strictly smaller value, so depth is bounded by the input's

Matching is PEG (ordered choice that commits, greedy repetition) with a packrat memo, so a match costs at most
O(input values x rule nodes) steps; the model counts its steps and checks that bound on every fixture.

  python pattern.py            runs pattern_fixtures.json
  python pattern.py --plant=<n> switches off protection n and runs it again (the plants must fail it)
"""
import json, os, sys
from block import load, pv, Refused

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = {'WORD': 'word', 'STRING': 'str', 'NUMBER': 'num', 'KEYWORD': 'kw', 'PATH': 'path', 'PAIR': 'pair',
         'LIST': 'list', 'GROUP': 'group', 'ROW': 'row', 'OPTIONAL': 'opt', 'SKIP': None}   # OPTIONAL: Haro's `?` mark, a value of its own kind (v0.31)
UNARY = ('OPT', 'ANY', 'SOME', 'NOT', 'AHEAD', 'INTO', 'TO', 'THRU', 'COLLECT', 'KEEP')
REFUSED_WORDS = {
    'WHILE': 'WHILE is refused: a pattern rule is total, and WHILE is how Parse loops without consuming',
    'DO': 'DO is refused: a pattern rule runs nothing',
    'EVAL': 'EVAL is refused: a pattern rule runs nothing',
    'IF': 'IF is refused: a condition is a rule, never host code',
    'CHANGE': 'CHANGE is refused: a pattern judges and never edits',
    'INSERT': 'INSERT is refused: a pattern judges and never edits',
    'REMOVE': 'REMOVE is refused: a pattern judges and never edits',
}
PLANT = 0


def flat(items):
    out = []
    for it in items:
        if it[0] == 'row':
            out.extend(it[1])
        elif it[0] != 'comment':
            out.append(it)
    return out


def compile_rule(text, where):
    vals = [v for v in load(text) if v[0] != 'comment']
    if len(vals) != 1 or vals[0][0] != 'list':
        raise Refused(f'pattern {where} is not a list: a rule is written [ ... ]')
    return alt(flat(vals[0][1]), where)


def alt(seq, where):
    branches, cur = [], []
    for v in seq:
        if v == ('kw', 'OR'):
            branches.append(cur); cur = []
        else:
            cur.append(v)
    branches.append(cur)
    if len(branches) > 1 and any(not b for b in branches):
        raise Refused(f'pattern {where}: OR needs a rule on each side')
    nodes = [sequence(b, where) for b in branches]
    return nodes[0] if len(nodes) == 1 else ('alt', nodes)


def sequence(seq, where):
    out, pos = [], [0]

    def item():
        if pos[0] >= len(seq):
            return None
        v = seq[pos[0]]; pos[0] += 1
        k = v[0]
        if k == 'kw':
            w = v[1]
            if w in TYPES:
                return ('type', TYPES[w])
            if w == 'END':
                return ('end',)
            if w in REFUSED_WORDS:
                raise Refused(f'pattern {where}: {REFUSED_WORDS[w]}')
            if w in UNARY:
                x = item()
                if x is None:
                    raise Refused(f'pattern {where}: {w} takes a rule')
                return (w.lower(), x)
            if w == 'REPEAT':
                if pos[0] >= len(seq) or seq[pos[0]][0] != 'num':
                    raise Refused(f'pattern {where}: REPEAT takes a count, then a rule')
                n = count(seq[pos[0]][1], where); pos[0] += 1; m = n
                if pos[0] < len(seq) and seq[pos[0]][0] == 'num':
                    m = count(seq[pos[0]][1], where); pos[0] += 1
                if m < n:
                    raise Refused(f'pattern {where}: REPEAT {n} {m}: its minimum is above its maximum')
                x = item()
                if x is None:
                    raise Refused(f'pattern {where}: REPEAT takes a count, then a rule')
                return ('repeat', n, m, x)
            if w in ('RULE', 'MEMBER'):
                if pos[0] >= len(seq) or seq[pos[0]][0] != 'word':
                    raise Refused(f'pattern {where}: {w} takes a name')
                name = seq[pos[0]][1]; pos[0] += 1
                return ('ref' if w == 'RULE' else 'member', name)
            if w == 'LIT':
                if pos[0] >= len(seq):
                    raise Refused(f'pattern {where}: LIT takes a value')
                x = seq[pos[0]]; pos[0] += 1
                return ('lit', x)
            raise Refused(f'pattern {where}: {w} is not a pattern word')
        if k == 'list':
            return ('sub', alt(flat(v[1]), where))
        if k == 'group':
            raise Refused(f"pattern {where}: ( ) in a rule would run the host (Parse's paren!): refused")
        return ('lit', v)

    while True:
        x = item()
        if x is None:
            break
        out.append(x)
    return ('seq', out)


def count(text, where):
    """A REPEAT count: digits only. 1.5 and -1 are refused by name (v0.31, X29, X30); int() of '1.5' was an uncaught ValueError."""
    if not text.isdigit():
        raise Refused(f'pattern {where}: REPEAT takes a whole count of zero or more, found {text}')
    return int(text)


def children(n):
    k = n[0]
    if k in ('seq',):
        return n[1]
    if k == 'alt':
        return n[1]
    if k == 'sub':
        return [n[1]]
    if k == 'repeat':
        return [n[3]]
    if k in tuple(u.lower() for u in UNARY):
        return [n[1]]
    return []


def refs(n):
    out = [n[1]] if n[0] == 'ref' else []
    for c in children(n):
        out += refs(c)
    return out


def members(n):
    out = [n[1]] if n[0] == 'member' else []
    for c in children(n):
        out += members(c)
    return out


def declare(rules_text, sets):
    """Rules as text -> compiled rules, or Refused. The bound is checked here, once, never at match time."""
    rules = {name: compile_rule(text, name) for name, text in rules_text.items()}
    for name, r in rules.items():
        for ref in refs(r):
            if ref not in rules:
                raise Refused(f'pattern {name}: RULE {ref} names no pattern')
        for s in members(r):
            if s not in sets:
                raise Refused(f'pattern {name}: MEMBER {s} names no set')
    # no recursion: depth-first over RULE references
    state = {}

    def visit(name, path):
        if state.get(name) == 1:
            cyc = path[path.index(name):] + [name]
            raise Refused(f"pattern {cyc[0]} is recursive ({' -> '.join(cyc)}): a pattern rule refers only to rules that end")
        if state.get(name) == 2:
            return
        state[name] = 1
        for r in refs(rules[name]):
            visit(r, path + [name])
        state[name] = 2

    if PLANT != 1:
        for name in rules:
            visit(name, [])
    memo = {}

    def nullable(n):
        k = n[0]
        if k in ('type', 'lit', 'member', 'into'):
            return False
        if k in ('end', 'opt', 'any', 'not', 'ahead', 'to'):
            return True
        if k in ('some', 'thru', 'collect', 'keep', 'sub'):
            return nullable(n[1])
        if k == 'repeat':
            return n[1] == 0 or nullable(n[3])
        if k == 'seq':
            return all(nullable(c) for c in n[1])
        if k == 'alt':
            return any(nullable(c) for c in n[1])
        if k == 'ref':
            if n[1] not in memo:
                memo[n[1]] = nullable(rules[n[1]])
            return memo[n[1]]
        raise ValueError(k)

    def check(n, name):
        k = n[0]
        if k in ('any', 'some', 'to') and nullable(n[1]) and PLANT != 2:
            raise Refused(f'pattern {name}: {k.upper()} over a rule that can match nothing: it would never move, so it is refused')
        for c in children(n):
            check(c, name)

    for name, r in rules.items():
        check(r, name)
    return rules


class Matcher:
    def __init__(self, rules, sets):
        self.rules, self.steps, self.memo, self.inner = rules, 0, {}, {}
        self.sets = {k: set(v) for k, v in sets.items()}

    def m(self, n, seq, i):
        key = (id(n), id(seq), i)
        if key in self.memo:
            return self.memo[key]
        self.steps += 1
        r = self._m(n, seq, i)
        self.memo[key] = r
        return r

    def _m(self, n, seq, i):
        k, N = n[0], len(seq)
        if k == 'type':
            return (True, i + 1, ()) if i < N and (n[1] is None or seq[i][0] == n[1]) else (False, i, ())
        if k == 'lit':
            return (True, i + 1, ()) if i < N and seq[i] == n[1] else (False, i, ())
        if k == 'member':
            if i < N and seq[i][0] in ('word', 'str', 'kw', 'num') and seq[i][1] in self.sets[n[1]]:
                return (True, i + 1, ())
            return (False, i, ())
        if k == 'end':
            return (i == N, i, ())
        if k == 'seq':
            kept, j = (), i
            for c in n[1]:
                ok, j, kk = self.m(c, seq, j)
                if not ok:
                    return (False, i, ())
                kept += kk
            return (True, j, kept)
        if k == 'alt':
            for c in n[1]:
                r = self.m(c, seq, i)
                if r[0]:
                    return r
            return (False, i, ())
        if k == 'sub':
            return self.m(n[1], seq, i)
        if k == 'ref':
            return self.m(self.rules[n[1]], seq, i)
        if k == 'opt':
            r = self.m(n[1], seq, i)
            return r if r[0] else (True, i, ())
        if k in ('any', 'some'):
            kept, j, count = (), i, 0
            while True:
                ok, j2, kk = self.m(n[1], seq, j)
                if not ok or j2 == j:
                    break
                kept += kk; j = j2; count += 1
            if k == 'some' and count == 0:
                return (False, i, ())
            return (True, j, kept)
        if k == 'repeat':
            kept, j, count = (), i, 0
            while count < n[2]:
                ok, j2, kk = self.m(n[3], seq, j)
                if not ok:
                    break
                kept += kk; j = j2; count += 1
            return (True, j, kept) if count >= n[1] else (False, i, ())
        if k == 'not':
            return (False, i, ()) if self.m(n[1], seq, i)[0] else (True, i, ())
        if k == 'ahead':
            return (True, i, ()) if self.m(n[1], seq, i)[0] else (False, i, ())
        if k == 'into':
            if i >= N:
                return (False, i, ())
            v = seq[i]
            if v[0] in ('list', 'group'):
                inner = tuple(x for x in v[1] if x[0] != 'comment')
            elif v[0] == 'row':
                inner = tuple(v[1])
            elif v[0] == 'pair':
                inner = (v[1], v[2])
            elif v[0] == 'opt':
                inner = (v[1],)                 # the value an optional mark makes optional (v0.31)
            else:
                return (False, i, ())
            inner = self.inner.setdefault(id(v), inner)   # one object per value, so the memo's id() key is stable
            ok, j, kk = self.m(n[1], inner, 0)
            return (True, i + 1, kk) if ok and j == len(inner) else (False, i, ())
        if k in ('to', 'thru'):
            for p in range(i, N + 1):
                ok, j, kk = self.m(n[1], seq, p)
                if ok:
                    return (True, p, ()) if k == 'to' else (True, j, kk)
            return (False, i, ())
        if k == 'keep':
            ok, j, kk = self.m(n[1], seq, i)
            return (True, j, tuple(seq[i:j])) if ok else (False, i, ())
        if k == 'collect':
            ok, j, kk = self.m(n[1], seq, i)
            return (True, j, (('list', list(kk)),)) if ok else (False, i, ())
        raise ValueError(k)


def run(rules_text, sets, start, text):
    rules = declare(rules_text, sets)
    vals = tuple(v for v in load(text) if v[0] != 'comment')
    mt = Matcher(rules, sets)
    ok, j, kept = mt.m(rules[start], vals, 0)
    whole = ok and j == len(vals)
    # Parse returns the collected block when the rule is one top-level COLLECT; KEEP outside any COLLECT keeps into the result
    body = rules[start][1] if rules[start][0] == 'seq' else []
    if whole and len(body) == 1 and body[0][0] == 'collect' and len(kept) == 1:
        kept = tuple(kept[0][1])
    # packrat: each (rule node, sequence, position) is computed once, so the steps are at most nodes x positions, where the
    # positions are those of the input and of every sequence INTO can enter
    bound = count_nodes(rules) * positions(vals)
    return whole, [pv(v) for v in kept], mt.steps, bound


def count_nodes(rules):
    def c(n):
        return 1 + sum(c(x) for x in children(n))
    return sum(c(r) for r in rules.values())


def positions(vals):
    vals = [v for v in vals if v[0] != 'comment']
    total = len(vals) + 1
    for v in vals:
        if v[0] in ('list', 'group', 'row'):
            total += positions(v[1])
        elif v[0] == 'pair':
            total += positions([v[1], v[2]])
        elif v[0] == 'opt':
            total += positions([v[1]])
    return total


def court(path=os.path.join(HERE, 'pattern_fixtures.json')):
    doc = json.load(open(path, encoding='utf-8'))
    ok = bad = 0
    worst = 0.0
    for f in doc['matches']:
        try:
            whole, kept, steps, bound = run(f['rules'], f.get('sets', {}), f['start'], f['input'])
            e = f['expect']
            good = whole == e['match'] and ('kept' not in e or kept == e['kept']) and steps <= bound
            worst = max(worst, steps / bound)
            why = f'match {whole} kept {kept} steps {steps} bound {bound}'
        except Refused as ex:
            good, why = False, 'refused: ' + str(ex)
        ok += good; bad += not good
        if not good:
            print(f'  FAIL {f["id"]}: {f["name"][:80]} -- {why}')
    for f in doc['refusals']:
        try:
            declare(f['rules'], f.get('sets', {}))
            good, why = False, 'declared, must be refused'
        except Refused as ex:
            good, why = f['refusal'] in str(ex), str(ex)
        ok += good; bad += not good
        if not good:
            print(f'  FAIL {f["id"]}: {f["name"][:80]} -- {why}')
    print(f'PATTERN COURT: {ok} of {ok + bad} fixtures hold; the most a match spent was {worst:.0%} of its step bound')
    return bad


if __name__ == '__main__':
    for a in sys.argv[1:]:
        if a.startswith('--plant='):
            PLANT = int(a.split('=')[1])
    sys.exit(1 if court() else 0)
