"""face_py.py -- a second face of the program graph, in Python's shape, as a PRINTER (rung 6 of the code-graph memo; Haro v0.21).

    print_py(graph) -> text           the Python-shaped text of a Ring program's graph (rung 18), or raises Refused(collision, why)
    python haro/spike/v21/face_py.py file.ring

ONE MEANING, RING'S. The face spells the graph; it never gives it Python's meaning (CODEGRAPH 3.2). A Python reader must never take the program for
something else, so each construct is one of three things:
  - spelt plainly, where Python reads it as Ring means it (an assignment, a call, a numeric loop body, arithmetic on numbers);
  - spelt with an EXPLICIT WORD, where Ring means something a Python reader would not guess: `at`/`setat` (a 1-based index), `eq` and its kin (Ring's
    comparison: a numeric string equals its number), `cat`/`plus` (Ring's `+`; `add` is Ring's own list builtin), `span`/`rng` (inclusive), `say` (Ring's printing), `return ""` (NULL);
  - REFUSED by name, where no spelling cannot be misread (COLLISIONS below): a brace block, eval, an operator method, a getter, cCatchError outside its
    handler, a loop variable read after its loop, a for-in that writes through its variable, `exit 2`, a lambda, `call f()`, `n++` as a value,
    a setter, a `$x` parameter, a compound write whose target holds a call, a package, the scanner's commands -- sixteen.
Names keep their first spelling (Ring folds case, F-18, so `N` and `n` are one variable and the face writes it one way); `$x` is `G.x`, `@x` and
`This.x` are `self.x`; a Ring name that is not a Python name is spelt as one -- a keyword or one of the face's own words takes a trailing `_`, the
`@` that begins a Softanza function's name is `at_`, a leading digit takes `_`. What a reader still needs is in one banner line, which travels with every text (CODEGRAPH 5: "the table is the face's banner").
A light kind inference -- a name assigned only numbers is a number, only strings a string -- decides where an operator may be Python's.
"""
import keyword, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v18'))
import l1

BANNER = ('# Ring++ in Python shape -- one meaning, Ring\'s: at() and setat() are 1-based; eq() ne() lt() gt() le() ge() compare as Ring does; '
          'cat() and plus() are Ring\'s +; mod() is Ring\'s %; both() either() negate() are and/or/not as 1 or 0; span() and rng() are inclusive; '
          'G.x is the global $x; say() prints as Ring does; a function returns "" when it returns nothing')
IND = '    '

# the face's collision table: what it refuses, and why (each a Ring finding or correction already paid for)
COLLISIONS = {
    'brace':       ('obj { ... }', 'a brace block calls braceStart/braceEnd and makes a bare call the object\'s method first: it has no spelling'),
    'eval':        ('eval(s)', 'eval runs in its caller\'s scope and creates its variables there (F-72), and its string is a hole in the graph'),
    'operator':    ('func operator(cOp, x)', 'one method for every operator, the right side with an "r" (F-69): not __add__ and friends'),
    'getter':      ('o.x with getx() defined', 'a dot on the attribute calls the getter on every object but This (F-73)'),
    'setter':      ('o.x = v with setx() defined', 'an assignment to the attribute calls the setter (F-73)'),
    'catch-error': ('cCatchError outside a handler', 'the caught message is process-wide outside the handler (C-15)'),
    'for-after':   ('the variable of a numeric loop read after its loop', 'after the loop it holds the value that failed the test, not the last one'),
    'for-in-write': ('for x in list, x assigned in the body', 'the loop variable is the list\'s item by reference: writing it writes the list'),
    'exit-levels': ('exit N, loop N with N > 1', 'leaves or continues N loops at once, which break and continue cannot: two loops'),
    'increment-value': ('n++ as a value', 'yields the NEW value (F-64), which no Python spelling of n += 1 does'),
    'lambda':      ('func(x) { ... }', 'a Ring lambda is a value whose free names are read when it runs (C-14): not spelt in this rung'),
    'call-name':   ('call f()', 'calls the function a string names, by name at run time'),
    'package':     ('package, import', 'packages are not built (C-28)'),
    'scanner':     ('ChangeRingKeyword and its kin', 'the scanner commands change the language under the text (C-28)'),
    'index-twice': ('aL[f()] += v', 'Ring evaluates the target once; setat(aL, f(), plus(at(aL, f()), v)) would run it twice'),
    'dollar-param': ('func f($x)', 'a parameter spelt $x is the function\'s own local, not the global $x (F-91): G.x would be the global'),
    'name-char':   ('a Ring name with a character Python names lack', 'an `@` after the first character of a name would print as `_`, and no reader could tell it from one'),
    'name-clash':  ('two Ring names that print as one Python name', 'a reader of the face could not tell them apart: `del` is spelt `del_`, `@Foo` is `at_Foo`, and a name of Ring\'s that is already `del_` or `at_foo` is the same text'),
    'new-from':    ('new from name', 'makes an object of the class a string names, at run time: no spelling'),
    'param-type':  ('func f(string s)', 'a typed parameter would lose its type in the face'),
    'compound-nl': ('n += nl', '`x += nl` is R41 on Ring while `x = x + nl` joins the text (vmexpr.c:27, F-98), and the face writes both as x = plus(x, nl)'),
    'call-target': ('F() = v', 'the call runs, then Ring writes through its result or raises R34 (F-81): Python cannot assign to a call'),
}

FACE_WORDS = {'say', 'see', 'at', 'setat', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cat', 'plus', 'span', 'rng', 'mod', 'both', 'either', 'negate',
              'give', 'load', 'bye', 'G', 'RingError', 'str', 'self', 'super', 'new', 'new_without_init'}
PRIVATE_COMMENT = '# private: the methods below are private to the class'
MAIN_COMMENT = '# Ring calls main() after the top level (F-60)'
REGION = '__region__'


# Python's precedence of what the face prints (higher binds tighter); a call form such as eq(a, b) is an atom
PY_PREC = {'or': 1, '||': 1, 'and': 2, '&&': 2, '=': 4, '!=': 4, '<': 4, '>': 4, '<=': 4, '>=': 4,
           '|': 5, '^': 6, '&': 7, '<<': 8, '>>': 8, '+': 9, '-': 9, '*': 10, '/': 10, '%': 10, '**': 12}
NOT_PREC, UNARY_PREC, ATOM_PREC = 3, 11, 99
PRINTED = {}                             # a printed name folded -> the Ring name folded it came from, for the program being printed


def ident(t, function=False):
    """A Ring name as a Python name that reads as the same one. `@` is `at_` wherever it stands; a keyword or a face word takes a trailing `_`; a leading digit
    takes `_`. The map must be injective for a reader, so two Ring names that print as one are refused (name-clash)."""
    raw = t
    low = raw.lower()
    if low == 'at' or low.startswith('at_') or '__at__' in low or (raw[:1] == '_' and raw[1:2].isdigit()):
        raise Refused('name-clash', '`%s` is already spelt like one of the face\'s escapes (at_, __at__, a leading _ before a digit)' % low)
    if t.startswith('@'):
        t = 'at_' + t[1:]
    t = t.replace('@', '__at__')                  # an @ inside a name; a leading one is the sigil
    if re.search(r'[^A-Za-z0-9_]', t):
        raise Refused('name-char', low)
    if t[:1].isdigit():
        t = '_' + t
    if keyword.iskeyword(t) or t in FACE_WORDS:
        t += '_'
    elif not raw.startswith('@') and t.endswith('_') and (keyword.iskeyword(t.rstrip('_')) or t.rstrip('_') in FACE_WORDS):
        raise Refused('name-clash', '`%s` is already spelt like the face\'s own escape for a keyword or a face word' % low)
    was = PRINTED.setdefault(t.lower(), raw.lower())
    if was != raw.lower():
        raise Refused('name-clash', '`%s` and `%s` both print as %s' % (was, raw.lower(), t))
    return t


NUM_FUNCS = {'len', 'number', 'floor', 'ceil', 'fabs', 'round', 'sqrt', 'random', 'ascii', 'isnumber', 'isstring', 'islist', 'isnull', 'find', 'ring_find',
             'max', 'min', 'pow', 'exp', 'log', 'sin', 'cos', 'tan', 'clock'}
STR_FUNCS = {'string', 'upper', 'lower', 'trim', 'left', 'right', 'char', 'copy', 'hex', 'str2hex', 'date', 'time', 'type', 'classname', 'read'}


class Refused(Exception):
    def __init__(self, cid, detail=''):
        self.cid = cid
        construct, why = COLLISIONS[cid]
        super().__init__('%s: %s -- %s%s' % (cid, construct, why, (' (' + detail + ')') if detail else ''))


def parse_text(text):
    """Ring text to its graph (rung 18), or raises ValueError."""
    fd, p = tempfile.mkstemp(suffix='.ring')
    try:
        os.write(fd, text.encode('latin-1'))
        os.close(fd)
        g, why = l1.parse_ring(p)
    finally:
        try:
            os.remove(p)
        except OSError:
            pass
    if g is None:
        raise ValueError(why)
    return g


def walk(n):
    """Every node under n, in order (dicts only)."""
    if isinstance(n, dict):
        yield n
        for v in n.values():
            yield from walk(v)
    elif isinstance(n, list):
        for x in n:
            yield from walk(x)


def names_in(n):
    return {x['text'].lower() for x in walk(n) if x.get('k') == 'id'}


class Face:
    def __init__(self, g):
        self.g = g
        self.ctx = []                        # the enclosing blocks of the statement being printed: [items, position, loop body?, tail]
        self.spell = {}                     # a name folded -> its first spelling (F-18)
        for x in walk(g):
            k = x.get('k')
            for t in ([x['text']] if k == 'id' else [x['name']] if k in ('func', 'param') else [x['var']] if k == 'for' else []):
                self.spell.setdefault(t.lower(), t)
        PRINTED.clear()
        self.getters, self.setters = set(), set()
        for x in walk(g):
            if x.get('k') == 'class':
                for it in x.get('items', []):
                    if it.get('k') == 'func':
                        nm = it['name'].lower()
                        if nm.startswith('get') and len(nm) > 3:
                            self.getters.add(nm[3:])
                        if nm.startswith('set') and len(nm) > 3:
                            self.setters.add(nm[3:])
        self.catch = []                      # the handler bindings we are inside
        self.cond = False                    # printing a condition (and/or/not read as Python's there)
        self.kinds = {}
        self.region = set()                  # the attributes a class region assigns (bare names there are attributes)
        self.prec = ATOM_PREC                # the precedence of the expression printed last

    # -- names
    def name(self, t):
        t = self.spell.get(t.lower(), t)
        if t.startswith('$'):
            return 'G.' + ident(t[1:])
        if t.startswith('@'):
            return 'self.' + ident(t)
        if t.lower() in self.region:
            return 'self.' + ident(t)
        return ident(t)

    def fname(self, t):
        """A function's name, where `@` is part of the name (Softanza's `@IsCounter...`), not the attribute sigil."""
        return ident(self.spell.get(t.lower(), t), function=True)

    # -- the light kinds: 'num', 'str', 'list' or None
    def kind(self, n):
        k = n['k']
        if k in ('num', 'bool'):
            return 'num'
        if k in ('str', 'sym', 'null'):
            return 'str'
        if k == 'list':
            return 'list'
        if k == 'paren':
            return self.kind(n['e']) if 'e' in n else None
        if k == 'id':
            t = n['text'].lower()
            if t in self.kinds:
                return self.kinds[t]
            return 'str' if t in ('nl', 'cr', 'tab') else None       # Ring's predefined characters, unless the program assigned the name
        if k == 'un':
            return 'num'
        if k == 'bin':
            op = n['op']
            if op in ('-', '*', '/', '%', '**', '=', '!=', '<', '>', '<=', '>=', 'and', 'or', '&&', '||', '&', '|', '^', '<<', '>>'):
                return 'num'
            if op == ':':
                return 'list'
            if op == '+':
                kl, kr = self.kind(n['l']), self.kind(n['r'])
                if kl == 'str':
                    return 'str'
                if kl == 'num' and kr == 'num':
                    return 'num'
            return None
        if k == 'call' and n['callee']['k'] == 'id':
            c = n['callee']['text'].lower()
            return 'num' if c in NUM_FUNCS else 'str' if c in STR_FUNCS else None
        return None

    def infer(self, items, params=()):
        """The kinds of a scope's names: a name every assignment of which gives one known kind has it; a parameter has none; a numeric loop's
        variable is a number. Iterated, so `n = n + 1` after `n = 1` is a number."""
        assigns, loopvars = [], set()
        for x in walk(items):
            if x.get('k') in ('func', 'class', 'lambda'):
                continue
            if x.get('k') == 'assign' and x['l']['k'] == 'id':
                assigns.append(x)
            if x.get('k') == 'for' and x.get('kind') == 'to':
                loopvars.add(x['var'].lower())
        saved = dict(self.kinds)
        env = {}
        for _ in range(5):
            self.kinds = dict(saved, **env)
            for v in loopvars:
                self.kinds[v] = 'num'
            seen = {}
            for a in assigns:
                nm = a['l']['text'].lower()
                kr = self.kind(a['r']) if a['op'] == '=' else ('num' if a['op'] in ('-=', '*=', '/=') else
                                                              self.kind({'k': 'bin', 'op': '+', 'l': a['l'], 'r': a['r']}) if a['op'] == '+=' else None)
                seen.setdefault(nm, []).append(kr)
            new = {}
            for nm, ks in seen.items():
                known = [x for x in ks if x is not None]
                new[nm] = known[0] if known and len(set(known)) == 1 and (len(known) == len(ks) or _ == 0) else None
            for p in params:
                new[p.lower()] = None
            for v in loopvars:
                if v in new and new[v] not in (None, 'num'):
                    new[v] = None
            if new == env:
                break
            env = new
        self.kinds = dict(saved, **env)
        for v in loopvars:
            if env.get(v, 'num') == 'num':
                self.kinds[v] = 'num'

    # -- expressions
    def e(self, n):
        """`and`, `or` and `not` are Python's only in the condition itself, through parentheses and each other; whatever else stands in a condition -- a call's
        argument, an operand of a comparison, an item of a list -- is a value, and a value is Ring's 1 or 0 (rung 7 found the argument leaking). Leaves in
        `self.prec` the precedence of the text it returns."""
        k = n['k']
        keep = k == 'paren' or (k == 'bin' and n['op'] in ('and', '&&', 'or', '||')) or (k == 'un' and n['op'] == 'not')
        if self.cond and not keep:
            self.cond = False
            try:
                s = self.expression(n)
            finally:
                self.cond = True
        else:
            s = self.expression(n)
        if k == 'un':
            self.prec = NOT_PREC if s.startswith('not ') else UNARY_PREC if s[:1] in ('-', '+') else ATOM_PREC
        elif k in ('post', 'assign'):
            self.prec = 0
        elif k not in ('bin', 'paren', 'pair'):      # binary() leaves its own; a parenthesis is not printed, so the inner expression's stands
            self.prec = ATOM_PREC
        return s

    def operand(self, n, parent, op=None, side='left'):
        """An operand of an operator of precedence `parent`, in parentheses exactly where Python would otherwise read another tree: a looser operand; an equal one on
        the side the operator does not associate to (`**` associates right, the others left); any comparison inside a comparison, which Python chains; but a unary
        minus on the right of `**` (`a ** -b`) needs none."""
        s = self.e(n)
        p = self.prec
        if p == ATOM_PREC:
            return s
        need = p < parent
        if not need and p == parent:
            if parent == 4:
                need = True
            elif op == '**':
                need = side == 'left'
            elif op is not None:
                need = side == 'right'
        if op == '**' and side == 'right' and p == UNARY_PREC:
            need = False
        return '(' + s + ')' if need else s

    def atomic(self, n):
        """An expression as the object of a dot or the callee of a call: parenthesized unless it is an atom."""
        s = self.e(n)
        return s if self.prec == ATOM_PREC else '(' + s + ')'

    def expression(self, n):
        k = n['k']
        if k == 'num':
            t = n['text']
            if re.match(r'^[0-9]+$', t) and int(t) > 2 ** 53:
                return t + '.0'
            return t
        if k == 'str':
            return py_str(n['text'][1:-1])
        if k == 'sym':
            return py_str(n['text'][1:].strip().lower())
        if k == 'null':
            return '""'
        if k == 'bool':
            return '1' if n['value'] else '0'
        if k == 'id':
            if n['text'].lower() == 'ccatcherror':
                if not self.catch:
                    raise Refused('catch-error')
                return 'str(%s)' % self.catch[-1]
            return self.name(n['text'])
        if k == 'self':
            return 'self'
        if k == 'super':
            return 'super()'
        if k == 'paren':
            if 'e' in n:
                return self.e(n['e'])        # not printed: Python's precedence decides where a parenthesis stands
            self.prec = ATOM_PREC
            return '()'
        if k == 'list':
            return '[' + ', '.join(self.e(x) for x in n.get('items', [])) + ']'
        if k == 'pair':
            if n['key']['k'] != 'sym':
                # only `:symbol = value` builds a pair in a list literal (F-93); a string or a name before `=` is the comparison it looks like
                return self.binary({'k': 'bin', 'op': '=', 'l': n['key'], 'r': n['value']})
            self.prec = ATOM_PREC
            return '[' + py_str(n['key']['text'][1:].strip().lower()) + ', ' + self.e(n['value']) + ']'
        if k == 'un':
            if n['op'] == 'not':
                if self.cond:
                    return 'not ' + self.operand(n['e'], NOT_PREC)
                return 'negate(' + self.e(n['e']) + ')'
            return n['op'] + self.operand(n['e'], UNARY_PREC)
        if k == 'post':
            raise Refused('increment-value')
        if k == 'bin':
            return self.binary(n)
        if k == 'call':
            c = n['callee']
            if c['k'] == 'id' and c['text'].lower() == 'eval':
                raise Refused('eval')
            return (self.fname(c['text']) if c['k'] == 'id' else self.atomic(c)) + '(' + ', '.join(self.e(a) for a in n.get('args', [])) + ')'
        if k == 'callkw':
            raise Refused('call-name')
        if k == 'member':
            prop = n['prop']['text'] if n['prop']['k'] == 'id' else None
            if prop and prop.lower() in self.getters:
                raise Refused('getter', 'get' + prop)
            return self.atomic(n['obj']) + '.' + (ident(self.spell.get(prop.lower(), prop)) if prop else self.e(n['prop']))
        if k == 'index':
            return 'at(%s, %s)' % (self.e(n['obj']), self.e(n['idx']))
        if k == 'brace':
            raise Refused('brace')
        if k == 'new':
            if 'items' in n:
                raise Refused('brace', 'new K { ... }')
            if n.get('from'):
                raise Refused('new-from', 'new from ' + '.'.join(n['name']))
            word = 'new' if 'args' in n else 'new_without_init'          # `new K` does not call init; `new K()` does
            return word + '(' + ', '.join(['.'.join(ident(x) for x in n['name'])] + [self.e(a) for a in n.get('args', [])]) + ')'
        if k == 'lambda':
            raise Refused('lambda')
        if k == 'assign':
            raise Refused('increment-value', 'an assignment used as a value')
        raise ValueError('no spelling for an expression of kind ' + k)

    def binary(self, n):
        """The text of a binary expression, and in `self.prec` its precedence: a call form (`eq(a, b)`, `plus(a, b)`) is an atom, an infix form Python's."""
        op, l, r = n['op'], n['l'], n['r']
        if op == '=' and l['k'] == 'sym':
            # `:name = value` builds the list ["name", value] wherever a value is wanted (F-59), not a comparison
            self.prec = ATOM_PREC
            return '[' + py_str(l['text'][1:].strip().lower()) + ', ' + self.e(r) + ']'
        kl, kr = self.kind(l), self.kind(r)
        if op in ('and', '&&', 'or', '||'):
            word = 'and' if op in ('and', '&&') else 'or'
            if self.cond:
                pp = PY_PREC[op]
                text, prec = self.operand(l, pp, op, 'left') + ' ' + word + ' ' + self.operand(r, pp, op, 'right'), pp
            else:
                text, prec = '%s(%s, %s)' % ('both' if word == 'and' else 'either', self.e(l), self.e(r)), ATOM_PREC
            self.prec = prec
            return text
        inner, self.cond = self.cond, False
        try:
            if op == ':':
                text, prec = 'rng(%s, %s)' % (self.e(l), self.e(r)), ATOM_PREC
            elif op == '+' and not (kl == kr and kl in ('num', 'str')):
                text, prec = '%s(%s, %s)' % ('cat' if kl == 'str' else 'plus', self.e(l), self.e(r)), ATOM_PREC
            elif op in ('=', '!=') and not (kl == kr and kl in ('num', 'str')):
                text, prec = '%s(%s, %s)' % ('eq' if op == '=' else 'ne', self.e(l), self.e(r)), ATOM_PREC
            elif op in ('<', '>', '<=', '>=') and not (kl == 'num' and kr == 'num'):
                text, prec = '%s(%s, %s)' % ({'<': 'lt', '>': 'gt', '<=': 'le', '>=': 'ge'}[op], self.e(l), self.e(r)), ATOM_PREC
            elif op == '%':
                text, prec = 'mod(%s, %s)' % (self.e(l), self.e(r)), ATOM_PREC
            else:
                pp = PY_PREC.get(op, 9)
                shown = {'=': '==', '!=': '!='}.get(op, op)
                text, prec = self.operand(l, pp, op, 'left') + ' ' + shown + ' ' + self.operand(r, pp, op, 'right'), pp
        finally:
            self.cond = inner
        self.prec = prec
        return text

    def condition(self, n):
        self.cond = True
        try:
            return self.e(n)
        finally:
            self.cond = False

    # -- statements
    def items(self, items, ind, top=False, loop=False, tail=()):
        out = []
        frame = [items, 0, loop, list(tail)]
        self.ctx.append(frame)
        try:
            for i, it in enumerate(items):
                frame[1] = i
                if it['k'] in ('func', 'class') and out:
                    out += [''] * (2 if top else 1)
                elif out and i > 0 and items[i - 1]['k'] in ('func', 'class') and top:
                    out += ['', '']
                out += self.item(it, ind, items[i + 1:])
        finally:
            self.ctx.pop()
        return out

    def continuation(self):
        """What can run after the current statement, in order, to the end of its function: the rest of each enclosing block; for a loop body
        the body again from its start (the next turn, which reaches the statement itself again); for a try body its catch and finally."""
        out = []
        for items, i, loop, tail in reversed(self.ctx):
            out += items[i + 1:]
            if loop:
                out += items[:i + 1]
            out += tail
        return out

    def read_before_write(self, var, stmts):
        """Can stmts, run in order, read var before writing it for certain?"""
        return self.first(var.lower(), stmts, {'jumped': False}) == 'read'

    def first(self, v, stmts, state):
        """The first touch of v along stmts: 'read', 'write' (on every path), or None. Once an `exit` or `loop` may have jumped past what
        follows, no later write is certain (state['jumped']), and the scan goes on to the end for reads alone."""
        for st in stmts:
            r = self.touch(v, st, state)
            if r == 'read' or (r == 'write' and not state['jumped']):
                return r
        return None

    def touch(self, v, st, state):
        k = st.get('k')
        if k in ('func', 'class'):
            return 'read' if v.startswith('$') and v in names_in(st) else None   # another scope: a bare name there is not this one (Rule A)
        if k in ('exit', 'loop'):
            state['jumped'] = True
            return None
        if k == 'for':
            if v in names_in([st.get(x) for x in ('a', 'b', 'step') if x in st]):
                return 'read'
            if st['var'].lower() == v and st['kind'] == 'to':
                return 'write'               # a numeric loop sets its variable at entry, even when its body never runs
            return 'read' if self.first(v, st.get('items', []), state) == 'read' else None
        if k == 'while':
            if v in names_in(st['cond']):
                return 'read'
            return 'read' if self.first(v, st.get('items', []), state) == 'read' else None
        if k == 'dowhile':
            r = self.first(v, st.get('items', []), state)
            return r if r else ('read' if v in names_in(st['cond']) else None)
        if k == 'if':
            conds = [st['cond']] + [el['cond'] for el in st.get('elifs', [])]
            if v in names_in(conds):
                return 'read'
            branches = [st.get('then', [])] + [el.get('items', []) for el in st.get('elifs', [])] + ([st['else']] if 'else' in st else [])
            return self.branches(v, branches, 'else' in st, state)
        if k == 'switch':
            if v in names_in([st['subject']] + [c.get('values', []) for c in st.get('cases', [])]):
                return 'read'
            branches = [c.get('items', []) for c in st.get('cases', [])] + ([st['other']] if 'other' in st else [])
            return self.branches(v, branches, 'other' in st, state)
        if k == 'try':
            body = self.first(v, st.get('items', []), state)
            catch = self.first(v, st['catch'].get('items', []), state) if 'catch' in st else None
            fin = self.first(v, st.get('finally', []), state)
            if 'read' in (body, catch, fin):
                return 'read'
            return 'write' if fin == 'write' or (body == 'write' and ('catch' not in st or catch == 'write')) else None
        e = st.get('e') if k == 'expr' else None
        if e and e.get('k') == 'id':
            return None                      # `next i` leaves `i` as a statement: a read whose value is dropped changes nothing
        if e and e.get('k') == 'assign' and e['op'] == '=' and e['l'].get('k') == 'id' and e['l']['text'].lower() == v:
            return 'read' if v in names_in(e['r']) else 'write'
        return 'read' if v in names_in(st) else None

    def branches(self, v, branches, total, state):
        rs = [self.first(v, b, state) for b in branches]
        if 'read' in rs:
            return 'read'
        return 'write' if total and all(r == 'write' for r in rs) else None

    def item(self, it, ind, after):
        k = it['k']
        if k == 'comment':
            return [ind + line for line in py_comment(it['text'])]
        lines = getattr(self, 's_' + k)(it, ind, after)
        if 'trail' in it:
            lines[-1] += '  ' + ' '.join(py_comment(it['trail']['text']))
        return lines

    def block(self, items, ind, loop=False, tail=()):
        body = self.items(items, ind + IND, loop=loop, tail=tail)
        if all(it['k'] == 'comment' for it in items):
            body.append(ind + IND + 'pass')      # Ring allows a block of comments only; Python needs a statement
        return body

    def s_expr(self, it, ind, after):
        e = it['e']
        if e['k'] == 'post':
            if e['e']['k'] == 'index':
                return [ind + self.assign({'k': 'assign', 'op': e['op'][0] + '=', 'l': e['e'], 'r': {'k': 'num', 'text': '1'}})]
            return [ind + self.e(e['e']) + (' += 1' if e['op'] == '++' else ' -= 1')]
        if e['k'] == 'assign':
            return [ind + self.assign(e)]
        return [ind + self.e(e)]

    def assign(self, a):
        op, l, r = a['op'], a['l'], a['r']
        if l['k'] == 'call':
            raise Refused('call-target', self.e(l))
        if op == '+=' and r['k'] == 'id' and r['text'].lower() == 'nl' and self.kind(l) != 'str':
            raise Refused('compound-nl', 'nl')
        if l['k'] == 'index':
            obj, idx = self.e(l['obj']), self.e(l['idx'])
            if op == '=':
                return 'setat(%s, %s, %s)' % (obj, idx, self.e(r))
            if any(n.get('k') in ('call','callkw', 'post', 'assign', 'new', 'brace') for n in walk(l)):
                raise Refused('index-twice')
            return 'setat(%s, %s, %s)' % (obj, idx, self.e({'k': 'bin', 'op': op[0], 'l': l, 'r': r}))
        if l['k'] == 'member' and l['prop']['k'] == 'id' and l['prop']['text'].lower() in self.setters:
            raise Refused('setter', 'set' + l['prop']['text'])
        if l['k'] == 'member' and l['prop']['k'] == 'id' and l['prop']['text'].lower() in self.getters and op != '=':
            raise Refused('getter', 'get' + l['prop']['text'])
        target = self.e(l)
        if op == '=':
            return target + ' = ' + self.e(r)
        bop = op[:-1]
        if bop == '+':
            kl, kr = self.kind(l), self.kind(r)
            if kl == kr and kl in ('num', 'str'):
                return target + ' += ' + self.e(r)
            return target + ' = ' + ('cat' if kl == 'str' else 'plus') + '(%s, %s)' % (target, self.e(r))
        if bop == '%':
            return target + ' = mod(%s, %s)' % (target, self.e(r))
        return target + ' ' + op + ' ' + self.e(r)

    def s_say(self, it, ind, after):
        return [ind + 'say(%s)' % self.e(it['e'])]

    def s_see(self, it, ind, after):
        return [ind + 'see(%s)' % self.e(it['e'])]

    def s_give(self, it, ind, after):
        return [ind + '%s = give()' % self.e(it['target'])]

    def s_return(self, it, ind, after):
        return [ind + 'return ' + (self.e(it['e']) if 'e' in it else '""')]

    def s_exit(self, it, ind, after):
        return self.jump(it, ind, 'break')

    def s_loop(self, it, ind, after):
        return self.jump(it, ind, 'continue')

    def jump(self, it, ind, word):
        if 'e' in it and not (it['e']['k'] == 'num' and it['e']['text'] == '1'):
            raise Refused('exit-levels')
        return [ind + word]

    def s_bye(self, it, ind, after):
        return [ind + 'bye()']

    def s_load(self, it, ind, after):
        return [ind + 'load(%s)' % py_str(it['path']['text'][1:-1])]

    def s_import(self, it, ind, after):
        raise Refused('package')

    def s_package(self, it, ind, after):
        raise Refused('package')

    def s_scanner(self, it, ind, after):
        raise Refused('scanner')

    def s_private(self, it, ind, after):
        return [ind + PRIVATE_COMMENT]

    def s_if(self, it, ind, after):
        out = [ind + 'if ' + self.condition(it['cond']) + ':'] + self.block(it.get('then', []), ind)
        cur = it
        while True:
            for el in cur.get('elifs', []):
                out += [ind + 'elif ' + self.condition(el['cond']) + ':'] + self.block(el.get('items', []), ind)
            els = cur.get('else')
            if els is not None and len(els) == 1 and els[0]['k'] == 'if' and 'trail' not in els[0]:
                # an else holding only an if is an elif: Python's tree has no other reading (rung 7 found it)
                cur = els[0]
                out += [ind + 'elif ' + self.condition(cur['cond']) + ':'] + self.block(cur.get('then', []), ind)
                continue
            break
        if cur.get('else') is not None:
            out += [ind + 'else:'] + self.block(cur['else'], ind)
        return out

    def s_while(self, it, ind, after):
        return [ind + 'while ' + self.condition(it['cond']) + ':'] + self.block(it.get('items', []), ind, loop=True)

    def s_dowhile(self, it, ind, after):
        return ([ind + 'while True:'] + self.items(it.get('items', []), ind + IND, loop=True)
                + [ind + IND + 'if not (' + self.condition(it['cond']) + '):', ind + IND + IND + 'break'])

    def s_for(self, it, ind, after):
        var = it['var']
        if it['kind'] == 'to':
            if self.read_before_write(var, self.continuation()):
                raise Refused('for-after', var)
            head = 'for %s in span(%s, %s%s):' % (self.name(var), self.e(it['a']), self.e(it['b']), (', ' + self.e(it['step'])) if 'step' in it else '')
        else:
            for x in walk(it.get('items', [])):
                if (x.get('k') == 'assign' and x['l']['k'] == 'id' and x['l']['text'].lower() == var.lower()) or \
                        (x.get('k') == 'post' and x['e'].get('k') == 'id' and x['e']['text'].lower() == var.lower()):
                    raise Refused('for-in-write', var)
            if 'step' in it:
                raise Refused('for-in-write', 'a stepped for-in')
            head = 'for %s in %s:' % (self.name(var), self.e(it['a']))
        return [ind + head] + self.block(it.get('items', []), ind, loop=True)

    def s_switch(self, it, ind, after):
        out = [ind + '_switch = ' + self.e(it['subject'])]
        first = True
        for c in it.get('cases', []):
            test = ' or '.join('eq(_switch, %s)' % self.e(v) for v in c.get('values', []))
            out += [ind + ('if ' if first else 'elif ') + test + ':'] + self.block(c.get('items', []), ind)
            first = False
        if 'other' in it:
            out += [ind + ('else:' if not first else 'if True:')] + self.block(it['other'], ind)
        return out

    def s_try(self, it, ind, after):
        handler = (it['catch'].get('items', []) if 'catch' in it else []) + it.get('finally', [])
        out = [ind + 'try:'] + self.block(it.get('items', []), ind, tail=handler)
        if 'catch' in it:
            b = ident(it['catch'].get('binding', 'e'))
            out.append(ind + 'except RingError as %s:' % b)
            self.catch.append(b)
            try:
                out += self.block(it['catch'].get('items', []), ind, tail=it.get('finally', []))
            finally:
                self.catch.pop()
        if 'finally' in it:
            out += [ind + 'finally:'] + self.block(it['finally'], ind)
        return out

    def s_func(self, it, ind, after, method=False):
        if it['name'].lower() == 'operator' and method:
            raise Refused('operator')
        params = [p['name'] for p in it.get('params', [])]
        for p in it.get('params', []):
            if 'type' in p:
                raise Refused('param-type', p['type'] + ' ' + p['name'])
        for p in params:
            if p.startswith('$'):
                raise Refused('dollar-param', p)
        saved, saved_ctx = dict(self.kinds), self.ctx
        self.infer(it.get('items', []), params)
        self.ctx = []                        # a function is its own scope: what runs after a statement ends with it
        try:
            body = self.items(it.get('items', []), ind + IND)
            items = it.get('items', [])
            if not items or items[-1]['k'] != 'return':
                body.append(ind + IND + 'return ""')
        finally:
            self.kinds, self.ctx = saved, saved_ctx
        head = 'def %s(%s):' % (self.fname(it['name']), ', '.join((['self'] if method else []) + [self.name(p) for p in params]))
        return [ind + head] + body

    def s_class(self, it, ind, after):
        head = 'class %s%s:' % (ident(it['name']), ('(' + '.'.join(ident(x) for x in it['parent']) + ')') if 'parent' in it else '')
        region = [x for x in it.get('items', []) if x['k'] not in ('func', 'private')]
        methods = [x for x in it.get('items', []) if x['k'] in ('func', 'private')]
        assigned = set()                     # a name the region assigns -- bare, or through This -- is an attribute, and a bare read of it is self.x
        for x in walk(region):
            if x.get('k') == 'assign':
                lv = x['l']
                if lv['k'] == 'id':
                    assigned.add(lv['text'].lower())
                elif lv['k'] == 'member' and lv['obj'].get('k') == 'self' and lv['prop'].get('k') == 'id':
                    assigned.add(lv['prop']['text'].lower())
        out = [ind + head]
        saved_region, saved_ctx = self.region, self.ctx
        try:
            if region:
                self.region, self.ctx = assigned, []
                body = ([ind + IND + IND + 'super().%s()' % REGION] if 'parent' in it else []) + self.items(region, ind + IND + IND)
                self.ctx = saved_ctx
                out += [ind + IND + 'def %s(self):' % REGION] + body
            self.region = set()
            for m in methods:
                if len(out) > 1:
                    out.append('')
                if m['k'] == 'private':
                    out += self.item(m, ind + IND, [])
                    continue
                out += self.s_func(m, ind + IND, [], method=True)
        finally:
            self.region, self.ctx = saved_region, saved_ctx
        if len(out) == 1:
            out.append(ind + IND + 'pass')
        return out


def py_str(v):
    """A Ring string's value as a Python literal that reads as the same value: Ring has no escapes (F-55), so a backslash is printed raw."""
    if '\n' in v or '\r' in v:
        return repr(v)
    if '\\' in v:
        if '"' not in v and not v.endswith('\\'):
            return 'r"' + v + '"'
        return repr(v)
    if '"' not in v:
        return '"' + v + '"'
    if "'" not in v:
        return "'" + v + "'"
    return repr(v)


def py_comment(text):
    """A comment of any of Ring's three kinds, written with `#`."""
    t = text.rstrip()
    if t.startswith('#'):
        return [t]
    if t.startswith('//'):
        return ['#' + t[2:]]
    if t.startswith('/*'):
        body = t[2:-2] if t.endswith('*/') else t[2:]
        return [('#' + (' ' if line.strip() and not line.startswith(' ') else '') + line.rstrip()).rstrip() for line in body.split('\n')]
    return ['# ' + t]


def print_py(g):
    """The Python-shaped text of a graph: the banner, then the program. Raises Refused for a collision."""
    f = Face(g)
    items = g.get('items', [])
    f.infer([x for x in items if x['k'] not in ('func', 'class')])
    lines = f.items(items, '', top=True)
    if any(x['k'] == 'func' and x['name'].lower() == 'main' for x in items):
        lines += ['', '', 'main()  ' + MAIN_COMMENT]
    return BANNER + '\n' + '\n'.join(lines) + '\n'


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    text = open(argv[0], 'rb').read().decode('latin-1')
    try:
        sys.stdout.write(print_py(parse_text(text)))
    except Refused as e:
        print('refused -- ' + str(e))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
