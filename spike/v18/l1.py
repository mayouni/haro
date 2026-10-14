"""l1.py -- the program graph of the Ring++ face (rung 18): its schema, its abstraction from the concrete tree, its canonical
printer, and the s-expressions the fixtures are written in.

    text --cst.recover--> L0 (every token, every comment, every gap)
         --abstract-----> L1 (names, literals, operators, structure; comments as nodes; no punctuation, no layout)
         --print_ring---> canonical text

What L1 keeps and what it drops is the whole of v18/GRAMMAR.md; in one breath: it keeps every identifier as written, every number and
string as its raw text, every comment, every parenthesis the author wrote, the order of everything; it drops layout, `;` and `,`
between statements, the grammar's alternative spellings of one construct (func/def/function, ok/end/endif, ? / put / see, ...),
keyword case, the shape the grammar gives `class` and `private` (they are greedy: the graph's classes are siblings), and the trailing
period of a call statement.

A node is a dict {'k': kind, field: value, ...}; a field whose value is its default is absent (`norm`), so two graphs are equal when
their dicts are equal.
"""
import json, os, re, sys, bisect, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cst

# ---- the schema ---------------------------------------------------------------------------------------------------------------

FIELDS = {
    'file': ['items'], 'package': ['name', 'items'], 'class': ['name', 'parent', 'items'], 'private': [],
    'func': ['name', 'params', 'items'], 'param': ['name', 'type'],
    'expr': ['e'], 'return': ['e', 'amp'], 'say': ['e'], 'see': ['e'], 'give': ['target'],
    'if': ['cond', 'then', 'elifs', 'else'], 'elif': ['cond', 'items'], 'while': ['cond', 'items'],
    'for': ['var', 'kind', 'a', 'b', 'step', 'items'], 'dowhile': ['items', 'cond'],
    'switch': ['subject', 'cases', 'other'], 'case': ['values', 'items'],
    'try': ['items', 'catch', 'finally'], 'catch': ['binding', 'items'],
    'load': ['mode', 'path'], 'import': ['name'], 'exit': ['e'], 'loop': ['e'], 'bye': [], 'scanner': ['text'],
    'comment': ['text'],
    'assign': ['op', 'l', 'r'], 'bin': ['op', 'l', 'r'], 'un': ['op', 'e'], 'post': ['op', 'e'],
    'call': ['callee', 'args'], 'callkw': ['e', 'items'], 'member': ['obj', 'prop'], 'index': ['obj', 'idx'],
    'brace': ['obj', 'items'], 'new': ['from', 'name', 'args', 'items'], 'lambda': ['params', 'items'],
    'paren': ['e'], 'list': ['items'], 'pair': ['key', 'value'],
    'id': ['text'], 'num': ['text'], 'str': ['text'], 'sym': ['text'], 'self': ['kw'], 'super': [], 'bool': ['value'], 'null': [],
}
# statements and definitions carry the comment after them on their line (`trail`); a comment inside an expression has nowhere to
# stay in a layout-free text, so the graph moves it to an item of its own after the statement it sat in
CARRIERS = {'package', 'class', 'private', 'func', 'expr', 'return', 'say', 'see', 'give', 'if', 'while', 'for', 'dowhile', 'switch', 'try',
            'load', 'import', 'exit', 'loop', 'bye', 'scanner'}
for _k in CARRIERS:
    FIELDS[_k] = FIELDS[_k] + ['trail']
DEFS = {'func', 'class', 'package'}
SUGAR = {'id': 'text', 'num': 'text', 'str': 'text', 'sym': 'text', 'comment': 'text', 'bool': 'value'}
LIST_FIELDS = {'items', 'then', 'elifs', 'params', 'args', 'cases', 'values'}


# ---- finish -------------------------------------------------------------------------------------------------------------------------
# Ring's flow, measured on the oracle (v18/probes/closers.py, fall.py): `end`, `endfunc` and `}` after a function are inert -- a statement
# written after a definition runs as part of the LAST FUNCTION's flow, up to the next definition -- and a `return` that ends its line is BARE
# (vendor/ring-vm/src/stmt.c:931: Ring looks at the very next token, finds the end of the line, and returns NULL), so what stands on a
# later row is a statement of its own that never runs. The parser's tree shows neither reliably (it closes a function at an `end`, hangs the
# next row's expression on a `return`, cuts a long expression at a `+`, and nests a stray statement in a class), so the graph is built
# from the tree and then settled by these rules, in this order. (The first version of this rung joined a bare `return` with the next
# row's statement because rnxc did; rnxc was wrong, and the oracle says so -- HF-74.)

STMT_LISTS = ('items', 'then', 'else', 'other', 'finally')


def tail_target(d):
    """Where the statements written after definition d run: the function at its physical end, else d itself."""
    if d['k'] == 'func':
        return d
    last = None
    for x in d.get('items', []):
        if x['k'] in DEFS:
            last = x
    return tail_target(last) if last is not None else d


def absorb(items):
    """Statements after a definition belong to the last function the definition holds, up to the next definition; the comments that head
    the next definition, or end the file, stay where they are."""
    out, i = [], 0
    while i < len(items):
        it = items[i]
        out.append(it)
        i += 1
        if it['k'] in DEFS:
            j = i
            while j < len(items) and items[j]['k'] not in DEFS and items[j]['k'] != 'private':
                j += 1
            run = items[i:j]
            n = len(run)
            while n > 0 and run[n - 1]['k'] == 'comment':
                n -= 1
            if n:
                tail_target(it).setdefault('items', []).extend(run[:n])
            out.extend(run[n:])
            i = j
    return out


def pop_comments(items):
    """A comment after the last statement of a definition is the parser's: it belongs to what holds the definition. Bottom up."""
    out = []
    for it in items:
        if it['k'] in DEFS:
            if it['k'] != 'func':
                it['items'] = pop_comments(it.get('items', []))
            tail = []
            while it.get('items') and it['items'][-1]['k'] == 'comment':
                tail.insert(0, it['items'].pop())
            out.append(it)
            out.extend(tail)
        else:
            out.append(it)
    return out


def settle_absorb(x):
    """Bottom up: a class settles what follows its own functions before the file settles what follows the class."""
    if isinstance(x, list):
        for v in x:
            settle_absorb(v)
    elif isinstance(x, dict):
        for v in list(x.values()):
            if isinstance(v, (list, dict)):
                settle_absorb(v)
        if x.get('k') in ('file', 'package', 'class'):
            x['items'] = absorb(x.get('items', []))


def lift_private(x):
    """`private` is a keyword on Ring, so a bare `private` the parser read as an expression (it does, after a comment that follows a
    top-level statement and precedes a class -- v18/probes/priv7.ring) is the marker, and what follows it is the class's, not the
    function's flow it was parked in."""
    if isinstance(x, list):
        for v in x:
            lift_private(v)
    elif isinstance(x, dict):
        for v in list(x.values()):
            if isinstance(v, (list, dict)):
                lift_private(v)
        if x.get('k') in ('file', 'package', 'class'):
            out = []
            for it in x.get('items', []):
                out.append(it)
                if it['k'] == 'func':
                    at = next((n for n, y in enumerate(it['items']) if y['k'] == 'private'), None) if it.get('items') else None
                    if at is not None:
                        out.extend(it['items'][at:])
                        it['items'] = it['items'][:at]
            x['items'] = out


def strip_pos(x):
    if isinstance(x, dict):
        x.pop('_pos', None)
        for v in x.values():
            strip_pos(v)
    elif isinstance(x, list):
        for v in x:
            strip_pos(v)
    return x


def push_trails(items):
    """A comment on the line where a definition ends trails the last statement that line holds, whichever node the parser hung it on."""
    for it in items:
        if it['k'] in DEFS:
            push_trails(it.get('items', []))
            if 'trail' in it:
                tgt = it
                while tgt['k'] in DEFS and tgt.get('items') and tgt['items'][-1]['k'] in CARRIERS:
                    tgt = tgt['items'][-1]
                if tgt is not it and 'trail' not in tgt:
                    tgt['trail'] = it.pop('trail')


def finish(g):
    lift_private(g)
    settle_absorb(g)
    g['items'] = pop_comments(g['items'])
    push_trails(g['items'])
    return g


def default_of(kind, field):
    if kind == 'new' and field in ('args', 'items'):
        return None
    if kind == 'callkw' and field == 'items':
        return None
    if field in ('amp', 'from'):
        return False
    if field in LIST_FIELDS:
        return []
    return None


def mk(_kind, /, **fields):
    n = {'k': _kind}
    for f, v in fields.items():
        if f in FIELDS[_kind] and v != default_of(_kind, f):
            n[f] = v
    return n


def norm(n):
    """The node with every default-valued field dropped, recursively (a graph is compared by this)."""
    if isinstance(n, dict):
        out = {'k': n['k']}
        if n['k'] == 'comment':
            out['kind'] = n.get('kind') or comment_kind(n['text'])
        for f in FIELDS[n['k']]:
            if f in n and n[f] != default_of(n['k'], f):
                v = norm(n[f])
                if v != default_of(n['k'], f):
                    out[f] = v
        return out
    if isinstance(n, list):
        return [norm(x) for x in n]
    return n


def comment_kind(text):
    if text.startswith('#-->'):
        return 'promise'
    if '<R:' in text:
        return 'tag'
    return 'note'


def comment(text):
    if (text[:1] != '/' or text[:2] == '//') and text.endswith('\r'):
        text = text[:-1]            # a line comment ends at the newline; on a CRLF file the carriage return is the line ending's, not the comment's
    return {'k': 'comment', 'kind': comment_kind(text), 'text': text}


# ---- s-expressions: how a fixture writes a graph -------------------------------------------------------------------------------

_TOK = re.compile(r'\s*(?:(\()|(\))|(\[)|(\])|(:[A-Za-z_]+)|("(?:[^"\\]|\\.)*")|([A-Za-z_][A-Za-z0-9_-]*))')


def sexp_read(text):
    toks, pos = [], 0
    while True:
        m = _TOK.match(text, pos)
        if not m:
            if text[pos:].strip():
                raise ValueError('cannot read the graph at: ' + text[pos:pos + 30].replace('\n', ' '))
            break
        toks.append(next((i, g) for i, g in enumerate(m.groups()) if g is not None))
        pos = m.end()
    i = 0

    def value():
        nonlocal i
        kind, tok = toks[i]
        if kind == 0:
            return node()
        if kind == 2:
            i += 1
            out = []
            while toks[i][0] != 3:
                out.append(value())
            i += 1
            return out
        if kind == 5:
            i += 1
            return json.loads(tok)
        if kind == 6:
            i += 1
            return {'nil': None, 'true': True, 'false': False}[tok]
        raise ValueError('unexpected token ' + tok)

    def node():
        nonlocal i
        i += 1
        k = toks[i][1]
        i += 1
        n = {'k': k}
        first = True
        while toks[i][0] != 1:
            if toks[i][0] == 4:
                f = toks[i][1][1:]
                i += 1
                n[f] = value()
            elif first and k in SUGAR:
                n[SUGAR[k]] = value()
            else:
                raise ValueError('a field of (' + k + ') must be keyed: ' + toks[i][1])
            first = False
        i += 1
        if k == 'comment':
            n['kind'] = comment_kind(n['text'])
        return n

    return value()


def sexp_write(n):
    """A readable single-line form of a graph, for a failure message. Equality never goes through text."""
    def atom(v):
        if v is None:
            return 'nil'
        if v is True:
            return 'true'
        if v is False:
            return 'false'
        return json.dumps(v, ensure_ascii=False)

    def one(v):
        if isinstance(v, dict):
            k = v['k']
            parts = [k]
            for f in FIELDS[k]:
                if f in v:
                    parts.append(atom(v[f]) if k in SUGAR and f == SUGAR[k] else ':' + f + ' ' + one(v[f]))
            return '(' + ' '.join(parts) + ')'
        if isinstance(v, list):
            return '[' + ' '.join(one(x) for x in v) + ']'
        return atom(v)
    return one(n)


def strip_parens(n):
    """The graph without its parenthesized nodes: what a refinement builds has none, and `(a + b) * c` and its builder's form agree here."""
    if isinstance(n, dict):
        if n['k'] == 'paren' and 'e' in n:
            return strip_parens(n['e'])
        return {f: strip_parens(v) for f, v in n.items()}
    if isinstance(n, list):
        return [strip_parens(x) for x in n]
    return n


# ---- abstraction: the concrete tree to the graph --------------------------------------------------------------------------------

# `!` and `not` compile to the same code on rnxc; `&&` and `||` do NOT compile like `and` and `or` (rnxc traps on them), so they keep
# their spelling: a spelling is normalized only where the compiler has been measured to read the two alike (probes/synonyms.py)
KEYWORD_OPS = {'!': 'not'}
REREAD_KINDS = {'return_statement', 'expression_statement', 'see_statement'}


def is_split_tail(n):
    """A statement the parser cut off the line above: an expression that begins, down its left spine, with a unary `+` or `-`."""
    if n.kind != 'expression_statement' or len(n.kids) != 1:
        return False
    e = n.kids[0]
    while e.kind == 'binary_expression' and e.kids:
        e = e.kids[0]
    return e.kind == 'unary_expression' and bool(e.kids) and e.kids[0].text in ('+', '-')


def term_end(ch):
    return ch.isalnum() or ch in "_\"'`)]}"


def leading_keyword(piece):
    """The length of the keyword a statement leads with when its payload is one expression: the statements the parser cuts at a `+`."""
    if piece[:1] == '?':
        return 1
    for kw in ('return', 'see', 'give'):
        if len(piece) > len(kw) and piece[:len(kw)].lower() == kw and piece[len(kw)] in ' \t':
            return len(kw)
    return None


STATEMENT_KINDS = {'expression_statement', 'return_statement', 'see_statement', 'give_statement', 'if_statement', 'for_statement',
                   'while_statement', 'switch_statement', 'try_statement', 'do_again_statement', 'exit_statement', 'loop_statement',
                   'bye_statement', 'load_statement', 'import_statement'}


def lift_statement_unary(e):
    """The grammar reads a statement that BEGINS with a unary `+` or `-` as that operator over the WHOLE rest whenever the rest holds a binary
    `+` or `-` -- `-a * b - c` is unary(((a * b) - c)) -- and Ring reads the unary as binding tighter than any binary operator, `((-a) * b) - c`
    (measured on the oracle and the official 1.27 with an object whose `operator` prints its name: v18/probes/unary_stmt.ring, fixture 23).
    Everywhere else the grammar agrees with Ring (`x = -a - b`, `? -a - b`, an argument), and so it does for `-a * b`; only a statement is
    cut this way, so only a statement is put right: the operator goes down the left spine of the binary chain to the leftmost operand.
    `!a - b` stays what the grammar says -- `not` is below the arithmetic on Ring too. rnxc still compiles the grammar's tree (HF-79)."""
    if e['k'] == 'un' and e.get('op') in ('+', '-') and e.get('e', {}).get('k') == 'bin':
        chain, parent, cur = e['e'], None, e['e']
        while cur['k'] == 'bin' and 'l' in cur:
            parent, cur = cur, cur['l']
        if parent is not None:
            parent['l'] = mk('un', op=e['op'], e=cur)
            return chain
    return e


class Abstract:
    def __init__(self, root, src):
        self.src = src
        self.nl = [i for i, c in enumerate(src) if c == '\n']
        self.inner = []
        self._spans(root)
        self.root = root

    # -- positions
    def _spans(self, root):
        if root.exact:
            return              # the export gives the parser's own spans, hidden tokens included
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack.extend(n.kids)
        for n in reversed(order):
            if n.kids:
                ks = [k for k in n.kids if k.start >= 0]
                if ks:
                    n.start, n.end = ks[0].start, ks[-1].end

    def line(self, pos):
        return bisect.bisect_left(self.nl, pos)

    def text(self, n):
        return self.src[n.start:n.end]

    # -- the file
    def file(self):
        items, _, _ = self.container(self.root.kids)
        return strip_pos(finish(mk('file', items=items)))

    # -- a list of statements, definitions and comments
    DEF_KINDS = ('function_definition', 'class_definition', 'package_definition')

    def tail_node(self, n):
        """The node whose flow the statements written after n continue: the function at n's physical end, else n."""
        if n.kind == 'function_definition':
            return n
        for k in reversed(n.kids):
            if k.kind in self.DEF_KINDS or k.kind == 'private_section':
                return self.tail_node(k)
        return n

    def fold_lambdas(self, kids):
        """`return func t { ... }`, one parameter and no parentheses, at the head of a function's own statement list: the grammar reads a BARE
        `return` and, on the same row, a FUNCTION DEFINITION named `t` (it cannot tell the two apart there; `return func(t) {`, `return func a, b {`
        and the same line inside an `if` it reads right). Ring reads a lambda. The definition is folded back into the return as the lambda it is
        (rnxc's compiler does the same, `Compiler.absorbed`), and what the grammar hung after its closing brace stays where the return is. The
        return is either the last statement of the function before it or, after an `if`, a statement the grammar left beside it: both are met."""
        out, i = [], 0
        while i < len(kids):
            cur = kids[i]
            out.append(cur)
            i += 1
            if i >= len(kids):
                break
            ret, owner = None, None
            if cur.kind == 'return_statement':
                ret = cur
            elif cur.kind == 'function_definition' and cur.kids and cur.kids[-1].kind == 'return_statement':
                ret, owner = cur.kids[-1], cur
            nxt = kids[i]
            if ret is None or not all(c.kind in ('return', '&') for c in ret.kids) or nxt.kind != 'function_definition' or len(nxt.kids) < 3:
                continue
            ident = nxt.kids[1]
            if ident.kind != 'identifier' or self.src[ident.end:].lstrip(' \t')[:1] != '{' or self.line(nxt.start) != self.line(max(ret.end - 1, 0)):
                continue
            close = max((n for n, c in enumerate(nxt.kids) if c.kind == '}'), default=None)
            if close is None:
                continue
            params = cst.Node('param_list', None, nxt)
            params.kids, params.start, params.end, params.exact = [ident], ident.start, ident.end, ident.exact
            lam = cst.Node('anonymous_function', None, ret)
            lam.kids = [nxt.kids[0], params] + nxt.kids[2:close + 1]
            lam.start, lam.end, lam.exact = nxt.start, nxt.kids[close].end, nxt.exact
            ret.kids = ret.kids + [lam]
            ret.end = max(ret.end, lam.end)
            rest = nxt.kids[close + 1:]
            if owner is not None:
                owner.kids = owner.kids + rest
                owner.end = max(owner.end, nxt.end)
            else:
                out.extend(rest)
            i += 1
        return out

    def absorb_kids(self, kids):
        """Ring's flow, in the tree. A statement written after a function runs as part of that function, up to the next definition; a
        function or a statement written after a class is the class's -- every `func` after the first `class` is a method of the latest one
        (F-21) -- and `end` and `}` close nothing (v18/probes/fall.py, nest.ring). The parser leaves them beside the definition, or
        hands them to the OUTER class of a nested pair, so they are moved into the definition before anything is read: which is also what
        lets a `return` and the tail the parser cut off it meet again."""
        kids = self.fold_lambdas(kids)
        out, i = [], 0
        while i < len(kids):
            k = kids[i]
            out.append(k)
            i += 1
            if k.kind not in self.DEF_KINDS:
                continue
            if k.kind == 'function_definition':
                stop = self.DEF_KINDS + ('private_section',)
            elif k.kind == 'class_definition':
                stop = ('class_definition', 'package_definition')
            else:
                stop = ('package_definition',)
            j = i
            while j < len(kids) and kids[j].kind not in stop:
                j += 1
            run = kids[i:j]
            n = len(run)
            while n > 0 and run[n - 1].kind == 'comment':
                n -= 1
            if n:
                k.kids = k.kids + run[:n]
                k.end = max(k.end, run[n - 1].end)
            if k.kind != 'function_definition':
                k.kids = self.absorb_kids(k.kids)
            out.extend(run[n:])
            i = j
        return out

    def container(self, kids, cls=False):
        """-> (items, where each ends, the classes the grammar nested inside this class's members: siblings in the graph)."""
        kids = self.absorb_kids(kids)
        out, ends, nested = [], [], []

        def add(item, end):
            out.append(item)
            ends.append(end)
        i = 0
        while i < len(kids):
            k = kids[i]
            kind = k.kind
            i += 1
            if kind == 'comment' and cls and nested:
                c = comment(self.text(k))          # after a nested class: between it and the next, so beside them, in order
                c['_pos'] = k.start
                nested.append(c)
            elif kind == 'comment':
                self.comment_into(out, ends, k)
            elif kind == 'class_definition':
                if cls:
                    nested.extend(self.class_def(k))
                else:
                    for it in self.class_def(k):
                        add(it, k.end)
            elif kind == 'private_section' and cls:
                add(mk('private'), k.start + 7)
                sub, sub_ends, sub_nested = self.container(k.kids[1:], cls=True)
                out.extend(sub)
                ends.extend(sub_ends)
                nested.extend(sub_nested)
            elif kind == 'package_definition':
                for it in self.package_def(k):
                    add(it, k.end)
            elif kind == 'function_definition':
                add(self.func_def(k), k.end)
            elif kind == 'expression_statement' and len(k.kids) == 1 and k.kids[0].kind == 'identifier' \
                    and k.kids[0].text.lower() == 'private':
                add(mk('private'), k.end)
            elif kind == 'expression_statement' and len(k.kids) == 1 and k.kids[0].kind == 'identifier' \
                    and k.kids[0].text.lower() in ('end', 'endfunc'):
                pass          # a closer the parser read as a name: on Ring `end` and `endfunc` after a function close nothing (closers.py)
            elif kind in REREAD_KINDS and self.reread(kids, i - 1) is not None:
                items, consumed = self.last_reread
                for it in items:
                    add(it, kids[i - 2 + consumed].end)
                i += consumed - 1
            elif kind in STATEMENT_KINDS:
                for it in self.stmts(k):
                    add(it, k.end)
            elif kind == 'scanner_command':
                add(mk('scanner', text=self.text(k)), k.end)
            # anything else is punctuation or a terminator: `,`, `end`, `ok`, `{`, `}` ...
        nested.sort(key=lambda it: it['_pos'])
        return out, ends, nested

    # -- a statement the parser cut where Ring does not, or did not cut where Ring does (the port of compile.zig's rereadSpan)
    def reread(self, kids, i):
        """Ring reads a line greedily: on one row `return E1 + E2` is one expression, and a line that begins with `+` or `-` after a finished
        term is a statement of its own. The parser does neither reliably, so the text of the statement and of every same-row tail it cut off
        is read again alone, in a function, where the parser keeps it whole. -> None when the tree already says what Ring says; else it sets
        self.last_reread = (items, statements consumed)."""
        st = kids[i]
        bare = st.kind == 'return_statement' and all(c.kind in ('return', '&') for c in st.kids)
        j = i + 1
        # a line that ends in `.` is unfinished on Ring, so the next statement, on any row, continues the chain the parser cut at the dot
        while j < len(kids) and kids[j].kind in ('expression_statement', 'see_statement') and (
                self.src[kids[j - 1].end - 1:kids[j - 1].end] == '.' or
                (self.line(kids[j].start) == self.line(max(kids[j - 1].end - 1, 0))
                 and (is_split_tail(kids[j]) or (j == i + 1 and bare)))):
            j += 1
        a, b = st.start, kids[j - 1].end
        text = self.src[a:b]
        hoisted = []
        comments = []
        stack = list(kids[i:j])
        while stack:
            n = stack.pop()
            if n.kind == 'comment':
                comments.append(n)
            else:
                stack.extend(n.kids)
        if comments and (j > i + 1 or '\n' in text):
            comments.sort(key=lambda c: c.start)
            buf = list(text)
            for c in comments:
                hoisted.append(comment(self.text(c)))
                for p in range(c.start - a, c.end - a):
                    if buf[p] not in '\r\n':
                        buf[p] = ' '
            text = ''.join(buf)
        else:
            comments = []
        starts, line_start = [0], 0
        for p, ch in enumerate(text):
            if ch != '\n':
                continue
            q = p
            while q > line_start and text[q - 1] in ' \t\r':
                q -= 1
            finished = q > line_start and term_end(text[q - 1])
            r = p + 1
            while r < len(text) and text[r] in ' \t\r':
                r += 1
            if finished and r < len(text) and text[r] in '+-':
                starts.append(r)
            line_start = p + 1
        if j == i + 1 and len(starts) == 1 and not comments:
            return None
        items = []
        for n, s0 in enumerate(starts):
            s1 = starts[n + 1] if n + 1 < len(starts) else len(text)
            piece = text[s0:s1].strip(' \t\r\n')
            if not piece:
                continue
            got = self.parse_piece(piece)
            if got is None:
                return None
            items.extend(got)
        self.last_reread = (items + hoisted, j - i)
        return self.last_reread

    def parse_piece(self, piece):
        """One statement's text alone -> its items, or None."""
        got = self.parse_snippet(piece)
        if got is not None:
            return got
        kw = leading_keyword(piece)
        if kw is not None:
            rest = piece[kw:].strip(' \t\r\n')
            if not rest:
                return None
            got = self.parse_snippet(piece[:kw] + ' (' + rest + ')')
            if got is None or got[0]['k'] not in ('return', 'say', 'see', 'give') or len(got) != 1:
                return None
            field = 'target' if got[0]['k'] == 'give' else 'e'
            if got[0].get(field, {}).get('k') == 'paren':
                got[0][field] = got[0][field]['e']
            return got
        got = self.parse_snippet('(' + piece + ')')
        if got is not None and len(got) == 1 and got[0]['k'] == 'expr' and got[0]['e']['k'] == 'paren' and got[0]['e']['e']['k'] == 'call':
            got[0]['e'] = got[0]['e']['e']
            return got
        return None

    def parse_snippet(self, piece):
        text = 'func __reread()\n' + piece + '\n'
        fd, path = tempfile.mkstemp(suffix='.ring')
        try:
            os.write(fd, text.encode('latin-1'))
            os.close(fd)
            root, src, rep = cst.recover_any(path)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass
        if rep['error'] or rep['bad'] or root is None:
            return None
        found = []
        for top in root.kids:
            if top.kind == 'function_definition':
                found.extend(c for c in top.kids[2:] if c.kind in STATEMENT_KINDS)
            elif top.kind in STATEMENT_KINDS:
                found.append(top)
        if not found:
            return None
        subabs = Abstract(root, src)
        want = len(text) - 1
        if found[0].end == want:
            return subabs.stmts(found[0])
        if len(found) == 2 and found[0].kind == 'return_statement' and all(c.kind in ('return', '&') for c in found[0].kids) \
                and found[1].kind == 'expression_statement' and found[1].end == want:
            ret, stray = subabs.stmts(found[0]), subabs.stmts(found[1])
            if subabs.line(found[1].start) != subabs.line(found[0].end - 1):
                return ret + stray                 # a later row: Ring's bare return, then a statement of its own
            e = stray[0]['e']
            if e['k'] == 'assign' and e['op'] == '=':
                e = mk('bin', op='=', l=e['l'], r=e['r'])          # the value of a return is an expression: its `=` compares
            joined = mk('return', e=e, amp=ret[0].get('amp', False))
            return [joined] + ret[1:] + stray[1:]
        return None

    def comment_into(self, out, ends, k):
        """A comment on the line where the previous item ends trails it; any other is an item where it stands."""
        c = comment(self.text(k))
        if out and out[-1]['k'] in CARRIERS and 'trail' not in out[-1] and self.line(k.start) == self.line(max(ends[-1] - 1, 0)):
            out[-1]['trail'] = c
        else:
            out.append(c)
            ends.append(k.end)

    # -- definitions
    def qname(self, n):
        return [k.text for k in n.kids if k.kind == 'identifier']

    def package_def(self, n):
        name = self.qname(n.kids[1])
        items = self.container(n.kids[2:])[0]
        flat = [it for it in items if it['k'] != 'package']
        nested = [it for it in items if it['k'] == 'package']          # a package the grammar nested is a sibling in the graph
        return [mk('package', name=name, items=flat)] + nested

    def class_def(self, n):
        name = n.kids[1].text
        parent, i = None, 2
        if i < len(n.kids) and n.kids[i].kind == 'class_parent':
            parent = self.qname(n.kids[i].kids[-1])
            i += 1
        items, _, nested = self.container(n.kids[i:], cls=True)
        node = mk('class', name=name, parent=parent, items=items)
        node['_pos'] = n.start          # the grammar nests a class in the one before it; the graph puts them side by side, in source order
        return [node] + nested

    def func_def(self, n):
        name = n.kids[1].text
        params, i = [], 2
        if i < len(n.kids) and n.kids[i].kind == 'param_list':
            params = self.params(n.kids[i])
            i += 1
        return mk('func', name=name, params=params, items=self.container(n.kids[i:])[0])

    def params(self, n):
        out = []
        for k in n.kids:
            if k.kind == 'identifier':
                out.append(mk('param', name=k.text))
            elif k.kind == 'typed_parameter':
                out.append(mk('param', name=k.kids[1].text, type=k.kids[0].text))
        return out

    # -- statements
    def stmts(self, n):
        """A statement and, after it, the comments that sat inside it (the graph keeps them, as items of their own)."""
        saved, self.inner = self.inner, []
        item = getattr(self, 's_' + n.kind)(n)
        hoisted, self.inner = self.inner, saved
        return (item if isinstance(item, list) else [item]) + hoisted

    def body(self, kids):
        return self.container(kids)[0]

    def ex(self, kids, i):
        """The expression at kids[i], skipping comments (they become the statement's inner comments); -> (graph, next index)."""
        while kids[i].kind == 'comment':
            self.inner.append(comment(self.text(kids[i])))
            i += 1
        return self.expr(kids[i]), i + 1

    def sections(self, kids, clause_kinds):
        """Split a statement's kids into the part before its first clause and one part per clause: a comment after a clause's last
        statement is a sibling of the clause in the tree, and belongs to the clause above it."""
        head, clauses = [], []
        for k in kids:
            if k.kind in clause_kinds:
                clauses.append((k, list(k.kids)))
            else:
                (clauses[-1][1] if clauses else head).append(k)
        return head, clauses

    def s_expression_statement(self, n):
        return mk('expr', e=lift_statement_unary(self.ex(n.kids, 0)[0]))

    def s_return_statement(self, n):
        amp = any(k.kind == '&' for k in n.kids)
        rest = [k for k in n.kids[1:] if k.kind != '&']
        first = next((k for k in rest if k.kind != 'comment'), None)
        if first is not None and self.line(first.start) > self.line(n.kids[0].end - 1):
            # the grammar reads a newline as an extra and hangs the NEXT row's expression on the `return`; Ring's `return` that ends its
            # line is bare, and that expression is a statement of its own, dead, which the graph keeps because the text has it
            for k in rest:
                if k.kind == 'comment':
                    self.inner.append(comment(self.text(k)))
            dead = self.parse_snippet(self.text(first))
            if dead is None:
                dead = [mk('expr', e=self.expr(first))]
            return [mk('return', amp=amp)] + dead
        e = self.ex(rest, 0)[0] if rest else None
        return mk('return', e=e, amp=amp)

    def s_see_statement(self, n):
        # measured on the oracle: `?` prints a line, `see` and `put` (any case) print without one. rnxc reads the keyword case-sensitively and
        # treats `put` as `?`, so the court judges this pair by running both texts on the oracle, not by `rnxc dis`
        return mk('say' if n.kids[0].text == '?' else 'see', e=self.ex(n.kids, 1)[0])

    def s_give_statement(self, n):
        return mk('give', target=self.ex(n.kids, 1)[0])

    def s_exit_statement(self, n):
        return mk('exit', e=self.ex(n.kids, 1)[0] if len(n.kids) > 1 else None)

    def s_loop_statement(self, n):
        return mk('loop', e=self.ex(n.kids, 1)[0] if len(n.kids) > 1 else None)

    def s_bye_statement(self, n):
        return mk('bye')

    def s_load_statement(self, n):
        mode, i = None, 1
        if n.kids[1].kind in ('package', 'again'):
            mode, i = n.kids[1].kind, 2
        return mk('load', mode=mode, path=mk('str', text=self.text(n.kids[i])))

    def s_import_statement(self, n):
        return mk('import', name=self.qname(n.kids[1]))

    def s_if_statement(self, n):
        cond, i = self.ex(n.kids, 1)
        head, clauses = self.sections(n.kids[i:], ('elseif_clause', 'else_clause'))
        elifs, els = [], None
        for k, kids in clauses:
            if k.kind == 'elseif_clause':
                c, j = self.ex(kids, 1)
                elifs.append(mk('elif', cond=c, items=self.body(kids[j:])))
            else:
                els = self.body(kids[1:])
        return mk('if', cond=cond, then=self.body(head), elifs=elifs, **{'else': els})

    def s_while_statement(self, n):
        cond, i = self.ex(n.kids, 1)
        return mk('while', cond=cond, items=self.body(n.kids[i:]))

    def s_for_statement(self, n):
        var, i = n.kids[1].text, 2
        kind, a, b, step = 'to', None, None, None
        if n.kids[i].kind == '=':
            a, i = self.ex(n.kids, i + 1)
            b, i = self.ex(n.kids, i + 1)            # past the `to`
        else:
            kind = 'in'
            a, i = self.ex(n.kids, i + 1)
        if i < len(n.kids) and n.kids[i].kind == 'step':
            step, i = self.ex(n.kids, i + 1)
        return mk('for', var=var, kind=kind, a=a, b=b, step=step, items=self.body(n.kids[i:]))

    def s_do_again_statement(self, n):
        again = max(i for i, k in enumerate(n.kids) if k.kind == 'again')
        cond, _ = self.ex(n.kids, again + 1)
        return mk('dowhile', items=self.body(n.kids[1:again]), cond=cond)

    def s_switch_statement(self, n):
        subject, i = self.ex(n.kids, 1)
        _, clauses = self.sections(n.kids[i:], ('case_clause', 'other_clause'))
        cases, other = [], None
        for k, kids in clauses:
            if k.kind == 'case_clause':
                cases.append(mk('case', values=self.exprs(kids[1].kids), items=self.body(kids[2:])))
            else:
                other = self.body(kids[1:])
        return mk('switch', subject=subject, cases=cases, other=other)

    def s_try_statement(self, n):
        head, clauses = self.sections(n.kids[1:], ('catch_clause', 'finally_clause'))
        catch = fin = None
        for k, kids in clauses:
            if k.kind == 'catch_clause':
                binding, rest = None, kids[1:]
                if rest and rest[0].kind == '(':
                    binding, rest = rest[1].text, rest[3:]
                catch = mk('catch', binding=binding, items=self.body(rest))
            else:
                fin = self.body(kids[1:])
        return mk('try', items=self.body(head), catch=catch, **{'finally': fin})

    # -- expressions
    def expr(self, n):
        return getattr(self, 'x_' + n.kind)(n)

    def exprs(self, kids):
        out = []
        for k in kids:
            if k.kind == 'comment':
                self.inner.append(comment(self.text(k)))
            elif k.kind != ',':
                out.append(self.expr(k))
        return out

    def x_identifier(self, n):
        return mk('id', text=n.text)

    def x_number(self, n):
        return mk('num', text=n.text)

    def x_string(self, n):
        return mk('str', text=self.text(n))

    def x_symbol(self, n):
        return mk('sym', text=self.text(n))

    def x_self(self, n):
        # `self` is kept as written: inside a brace it is the brace object and `This` the method's (ringpp F-124), so the two are not
        # one construct any more; `This` and `this` stay one spelling
        if self.text(n).strip().lower() == 'self':
            return mk('self', kw='self')
        return mk('self')

    def x_super(self, n):
        return mk('super')

    def x_boolean(self, n):
        return mk('bool', value=(self.text(n).lower() == 'true'))

    def x_null(self, n):
        return mk('null')

    def x_qualified_identifier(self, n):
        return mk('id', text='.'.join(self.qname(n)))

    def x_parenthesized_expression(self, n):
        e = None
        for k in n.kids:
            if k.kind == 'comment':
                self.inner.append(comment(self.text(k)))
            elif k.kind not in ('(', ')'):
                e = self.expr(k)
        return mk('paren', e=e)

    def x_assignment_expression(self, n):
        l, i = self.ex(n.kids, 0)
        op = n.kids[i].kind
        r, _ = self.ex(n.kids, i + 1)
        return mk('assign', op=op, l=l, r=r)

    def x_binary_expression(self, n):
        l, i = self.ex(n.kids, 0)
        op = KEYWORD_OPS.get(n.kids[i].kind, n.kids[i].kind)
        r, _ = self.ex(n.kids, i + 1)
        return mk('bin', op=op, l=l, r=r)

    def x_unary_expression(self, n):
        op = KEYWORD_OPS.get(n.kids[0].kind, n.kids[0].kind)
        return mk('un', op=op, e=self.ex(n.kids, 1)[0])

    def x_postfix_expression(self, n):
        e, i = self.ex(n.kids, 0)
        return mk('post', op=n.kids[i].kind, e=e)

    def x_call_expression(self, n):
        callee, i = self.ex(n.kids, 0)
        args = []
        for k in n.kids[i:]:
            if k.kind == 'arguments':
                args = self.exprs(k.kids)
            elif k.kind == 'comment':
                self.inner.append(comment(self.text(k)))
        return mk('call', callee=callee, args=args)

    def x_call_keyword_expression(self, n):
        k = n.kids[1]
        if k.kind == 'brace_block':
            return mk('callkw', items=self.body(k.kids))
        return mk('callkw', e=self.expr(k))

    def x_member_expression(self, n):
        obj, i = self.ex(n.kids, 0)
        prop, _ = self.ex(n.kids, i + 1)
        return mk('member', obj=obj, prop=prop)

    def x_subscript_expression(self, n):
        obj, i = self.ex(n.kids, 0)
        idx, _ = self.ex(n.kids, i)
        return mk('index', obj=obj, idx=idx)

    def x_brace_expression(self, n):
        obj, i = self.ex(n.kids, 0)
        items = self.body(n.kids[i:])
        if obj['k'] == 'assign' and obj['op'] == '=':
            # `o = F(x) { ... }`: the brace belongs to the value (Ring's parser attaches it to the factor), and the parser sometimes hangs
            # it on the whole assignment instead. An assignment's value is what it assigned, so the two do the same; the graph keeps the
            # first, which also prints as a statement of its own, where `(o = F(x)) { }` would join the call on the line above
            return mk('assign', op='=', l=obj['l'], r=mk('brace', obj=obj['r'], items=items))
        return mk('brace', obj=obj, items=items)

    def x_new_expression(self, n):
        frm = any(k.kind == 'from' for k in n.kids)
        q = next(k for k in n.kids if k.kind == 'qualified_identifier')
        args = items = None
        after = n.kids[n.kids.index(q) + 1:]
        if after and after[0].kind == '(':
            args = []
            for k in after:
                if k.kind == 'arguments':
                    args = self.exprs(k.kids)
        elif after and after[0].kind == '{':
            items = self.body(after)
        return mk('new', **{'from': frm, 'name': self.qname(q), 'args': args, 'items': items})

    x_new_with_parens = x_new_expression

    def x_anonymous_function(self, n):
        params = []
        for k in n.kids:
            if k.kind == 'param_list':
                params = self.params(k)
        return mk('lambda', params=params, items=self.body([k for k in n.kids if k.kind != 'param_list']))

    def x_list_literal(self, n):
        items = []
        for k in n.kids:
            if k.kind == 'comment':
                self.inner.append(comment(self.text(k)))
            elif k.kind == 'hash_pair':
                items.append(self.x_hash_pair(k))
            elif k.kind not in ('[', ']', ','):
                items.append(self.expr(k))
        return mk('list', items=items)

    def x_hash_pair(self, n):
        key, i = self.ex(n.kids, 0)
        value, _ = self.ex(n.kids, i + 1)
        return mk('pair', key=key, value=value)


def abstract_tree(root, src):
    return norm(Abstract(root, src).file())


def parse_ring(path):
    """A Ring file to its graph, or (None, why)."""
    root, src, rep = cst.recover_any(path)
    if rep['error']:
        return None, 'the parser reports an error'
    if rep['bad']:
        return None, 'the tree could not be placed: ' + str(rep['bad'][0])
    return abstract_tree(root, src), None


# ---- the printer ---------------------------------------------------------------------------------------------------------------------

BIN_PREC = {'or': 2, '||': 2, 'and': 3, '&&': 3, '=': 5, '!=': 5, '<': 6, '>': 6, '<=': 6, '>=': 6, '|': 7, '^': 7, '&': 9, '<<': 10, '>>': 10,
            '+': 11, '-': 11, '*': 12, '/': 12, '%': 12, '**': 12, '^^': 12, ':': 13}
UNARY_PREC, POSTFIX_PREC, ATOM_PREC = 14, 15, 99
TAB = '\t'


def prec_of(n):
    k = n['k']
    if k == 'bin':
        return BIN_PREC.get(n['op'], 11)
    if k == 'assign':
        return 1
    if k == 'un':
        return UNARY_PREC
    if k in ('post', 'call', 'member', 'index', 'brace', 'callkw'):
        return POSTFIX_PREC
    return ATOM_PREC


class Printer:
    # -- expressions; a block inside an expression prints its statements one level in from `ind`
    def e(self, n, ind):
        k = n['k']
        if k in ('id', 'num', 'str', 'sym'):
            return n['text']
        if k == 'self':
            return 'self' if n.get('kw') else 'This'
        if k == 'super':
            return 'super'
        if k == 'null':
            return 'NULL'
        if k == 'bool':
            return 'true' if n['value'] else 'false'
        if k == 'paren':
            return '(' + (self.e(n['e'], ind) if 'e' in n else '') + ')'
        if k == 'assign':
            return self.e(n['l'], ind) + ' ' + n['op'] + ' ' + self.e(n['r'], ind)
        if k == 'bin':
            p = BIN_PREC.get(n['op'], 11)
            l = self.operand(n['l'], p, False, ind)
            r = self.operand(n['r'], p, True, ind)
            return l + ':' + r if n['op'] == ':' else l + ' ' + n['op'] + ' ' + r
        if k == 'un':
            e = self.operand(n['e'], UNARY_PREC, False, ind)
            if n['op'] == 'not':
                return 'not ' + e
            if e[:1] in ('-', '+') and e[:1] == n['op']:
                return n['op'] + ' ' + e
            return n['op'] + e
        if k == 'post':
            return self.operand(n['e'], POSTFIX_PREC, False, ind) + n['op']
        if k == 'call':
            return self.operand(n['callee'], POSTFIX_PREC, False, ind) + '(' + ', '.join(self.e(a, ind) for a in n.get('args', [])) + ')'
        if k == 'callkw':
            return 'call ' + (self.block(n['items'], ind) if 'items' in n else self.e(n['e'], ind))
        if k == 'member':
            return self.operand(n['obj'], POSTFIX_PREC, False, ind) + '.' + self.e(n['prop'], ind)
        if k == 'index':
            return self.operand(n['obj'], POSTFIX_PREC, False, ind) + '[' + self.e(n['idx'], ind) + ']'
        if k == 'brace':
            return self.operand(n['obj'], POSTFIX_PREC, False, ind) + ' ' + self.block(n.get('items', []), ind)
        if k == 'new':
            s = 'new ' + ('from ' if n.get('from') else '') + '.'.join(n['name'])
            if 'args' in n:
                s += '(' + ', '.join(self.e(a, ind) for a in n['args']) + ')'
            elif 'items' in n:
                s += ' ' + self.block(n['items'], ind)
            return s
        if k == 'lambda':
            return 'func(' + self.params(n.get('params', [])) + ') ' + self.block(n.get('items', []), ind)
        if k == 'list':
            return '[' + ', '.join(self.e(i, ind) for i in n.get('items', [])) + ']'
        if k == 'pair':
            return self.e(n['key'], ind) + ' = ' + self.e(n['value'], ind)
        raise ValueError('cannot print an expression of kind ' + k)

    def operand(self, n, parent_prec, right, ind):
        """An operand, parenthesized when its own precedence would let the text read as another graph (operators associate left)."""
        s = self.e(n, ind)
        p = prec_of(n)
        if p < parent_prec or (p == parent_prec and right and n['k'] == 'bin'):
            return '(' + s + ')'
        return s

    def params(self, ps):
        return ', '.join((p['type'] + ' ' if 'type' in p else '') + p['name'] for p in ps)

    def block(self, items, ind):
        """`{ ... }` with its statements one level in from ind; the closing brace at ind."""
        lines = self.items(items, ind + TAB)
        return '{\n' + '\n'.join(lines) + ('\n' if lines else '') + ind + '}'

    # -- items
    def items(self, items, ind):
        """The lines of a list of items at indentation ind. A definition is set apart by a blank line; none is closed, because nothing
        closes one: `end` after a function is inert on Ring, and what follows a definition is its own (see `finish`)."""
        flags = [False] * len(items)
        for d, it in enumerate(items):
            if it['k'] in DEFS:
                j = d
                while j > 0 and items[j - 1]['k'] == 'comment':
                    j -= 1
                if j > 0:
                    flags[j] = True
                if d + 1 < len(items):
                    flags[d + 1] = True
        out = []
        for i, it in enumerate(items):
            if flags[i]:
                out.append('')
            out.extend(self.item(it, ind))
        return out

    def item(self, it, ind):
        k = it['k']
        if k == 'comment':
            return [ind + it['text']]
        lines = getattr(self, 'p_' + k)(it, ind)
        if 'trail' in it:
            lines[-1] = lines[-1] + '  ' + it['trail']['text']
        return lines

    def body(self, items, ind):
        return self.items(items, ind + TAB)

    def p_expr(self, it, ind):
        return (ind + self.e(it['e'], ind)).split('\n')

    def p_return(self, it, ind):
        if 'e' not in it:
            return [ind + 'return']
        return (ind + 'return ' + ('& ' if it.get('amp') else '') + self.e(it['e'], ind)).split('\n')

    def p_say(self, it, ind):
        return (ind + '? ' + self.e(it['e'], ind)).split('\n')

    def p_see(self, it, ind):
        return (ind + 'see ' + self.e(it['e'], ind)).split('\n')

    def p_give(self, it, ind):
        return (ind + 'give ' + self.e(it['target'], ind)).split('\n')

    def p_exit(self, it, ind):
        return (ind + 'exit' + (' ' + self.e(it['e'], ind) if 'e' in it else '')).split('\n')

    def p_loop(self, it, ind):
        return (ind + 'loop' + (' ' + self.e(it['e'], ind) if 'e' in it else '')).split('\n')

    def p_bye(self, it, ind):
        return [ind + 'bye']

    def p_scanner(self, it, ind):
        return [ind + it['text']]

    def p_load(self, it, ind):
        return [ind + 'load ' + (it['mode'] + ' ' if 'mode' in it else '') + it['path']['text']]

    def p_import(self, it, ind):
        return [ind + 'import ' + '.'.join(it['name'])]

    def p_private(self, it, ind):
        return [ind + 'private']

    def p_if(self, it, ind):
        out = [ind + 'if ' + self.e(it['cond'], ind)] + self.body(it.get('then', []), ind)
        for el in it.get('elifs', []):
            out.append(ind + 'but ' + self.e(el['cond'], ind))
            out += self.body(el.get('items', []), ind)
        if 'else' in it:
            out.append(ind + 'else')
            out += self.body(it['else'], ind)
        out.append(ind + 'ok')
        return out

    def p_while(self, it, ind):
        return [ind + 'while ' + self.e(it['cond'], ind)] + self.body(it.get('items', []), ind) + [ind + 'end']

    def p_for(self, it, ind):
        if it['kind'] == 'to':
            head = 'for ' + it['var'] + ' = ' + self.e(it['a'], ind) + ' to ' + self.e(it['b'], ind)
        else:
            head = 'for ' + it['var'] + ' in ' + self.e(it['a'], ind)
        if 'step' in it:
            head += ' step ' + self.e(it['step'], ind)
        return [ind + head] + self.body(it.get('items', []), ind) + [ind + 'next']

    def p_dowhile(self, it, ind):
        return [ind + 'do'] + self.body(it.get('items', []), ind) + [ind + 'again ' + self.e(it['cond'], ind)]

    def p_switch(self, it, ind):
        out = [ind + 'switch ' + self.e(it['subject'], ind)]
        for c in it.get('cases', []):
            out.append(ind + TAB + 'on ' + ', '.join(self.e(v, ind) for v in c.get('values', [])))
            out += self.items(c.get('items', []), ind + TAB + TAB)
        if 'other' in it:
            out.append(ind + TAB + 'other')
            out += self.items(it['other'], ind + TAB + TAB)
        out.append(ind + 'off')
        return out

    def p_try(self, it, ind):
        out = [ind + 'try'] + self.body(it.get('items', []), ind)
        if 'catch' in it:
            out.append(ind + 'catch' + ('(' + it['catch']['binding'] + ')' if 'binding' in it['catch'] else ''))
            out += self.body(it['catch'].get('items', []), ind)
        if 'finally' in it:
            out.append(ind + 'finally')
            out += self.body(it['finally'], ind)
        out.append(ind + 'done')
        return out

    def p_func(self, it, ind):
        return [ind + 'func ' + it['name'] + '(' + self.params(it.get('params', [])) + ')'] + self.body(it.get('items', []), ind)

    def p_class(self, it, ind):
        head = 'class ' + it['name'] + (' from ' + '.'.join(it['parent']) if 'parent' in it else '')
        return [ind + head] + self.body(it.get('items', []), ind)

    def p_package(self, it, ind):
        return [ind + 'package ' + '.'.join(it['name'])] + self.body(it.get('items', []), ind)


def print_ring(l1):
    """The canonical text of a graph: one spelling per construct, a tab a level, a statement a line."""
    lines = Printer().items(l1.get('items', []), '')
    return '\n'.join(lines) + '\n' if lines else ''
