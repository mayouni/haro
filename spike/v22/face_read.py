"""face_read.py -- the READER of the Python-shaped face (rung 7 of the code-graph memo; Haro v0.22).

    read_py(text, strict=True) -> graph       the L1 graph (rung 18) of a text in the face v21 prints, or raises ReadRefused / face_py.Refused
    read_ring(text, strict=True) -> text      the canonical Ring text of that graph
    python haro/spike/v22/face_read.py file.py [--lenient]

THE RULE. The reader accepts exactly the printer's image: it builds the graph from the text with Python's own parser, prints the graph back with v21's printer,
and the two must be the same Python up to layout, comments, quotes, parentheses and the three things the face writes out (a trailing `return ""`, the `main()`
call, `pass`). So a text is read only when it is the face's own spelling of one Ring meaning, and what a reader could take two ways is decided once, here:
  `x += 1` is `x++`; `x = plus(x, y)` stays `x = x + y`; `self.x` is `This.x` in a method and the bare region name in `__region__`; `self.at_x` is `@x`;
  `at_Foo` is `@Foo`; a catch has a binding only if the handler uses the name other than as `str(e)`; `return ""` is a bare return; `_switch` followed by a chain of
  `eq(_switch, v)` is a switch, and `while True:` ending in `if not (c): break` is `do ... again c`; the three kinds of comment are `#`.
A construct Python has and the face has no word for is refused by name (`construct`), a face word used as the face does not use it is `word`, a definition out of
Ring's order is `order`, a text that is not the face's spelling is `not-canonical` (with the line the face writes), and a text the printer would refuse is
refused for the printer's collision. The reader never gives a spelling Python's meaning (CODEGRAPH 3.2).
"""
import ast, copy, io, keyword, os, re, sys, tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v21'))
sys.path.insert(0, os.path.join(HERE, '..', 'v18'))
import face_py
import l1
from l1 import mk

READ_REFUSALS = {
    'syntax':        'the text is not Python',
    'construct':     'Python the face has no word for',
    'word':          'a face word used as the face does not use it',
    'order':         'a definition\'s place is semantic on Ring (F-21, HF-73)',
    'not-canonical': 'a spelling the face does not print for that graph',
}


class ReadRefused(Exception):
    def __init__(self, cid, detail):
        self.cid = cid
        super().__init__('%s: %s -- %s' % (cid, READ_REFUSALS[cid], detail))


def refuse(cid, node, detail):
    line = getattr(node, 'lineno', None)
    raise ReadRefused(cid, ('line %d: ' % line if line else '') + detail)


FACE_WORDS = face_py.FACE_WORDS
STATEMENT_WORDS = {'say', 'see', 'give', 'load', 'bye', 'setat'}
COMPARE = {'eq': '=', 'ne': '!=', 'lt': '<', 'gt': '>', 'le': '<=', 'ge': '>='}
BINOPS = {ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/', ast.Pow: '**', ast.Mod: '%', ast.BitOr: '|', ast.BitXor: '^', ast.BitAnd: '&',
          ast.LShift: '<<', ast.RShift: '>>'}
CMPOPS = {ast.Eq: '=', ast.NotEq: '!=', ast.Lt: '<', ast.LtE: '<=', ast.Gt: '>', ast.GtE: '>='}
NUMBER = re.compile(r'^(0[xX][0-9a-fA-F_]+|[0-9][0-9_]*(\.[0-9_]*)?([eE][+-]?[0-9]+)?|\.[0-9]+)$')    # Ring and Python both take `_` between digits
CONSTRUCTS = {
    ast.Lambda: 'lambda: a Ring lambda is a value whose free names are read when it runs (C-14)',
    ast.ListComp: 'comprehension', ast.GeneratorExp: 'comprehension', ast.SetComp: 'comprehension', ast.DictComp: 'comprehension',
    ast.Tuple: 'tuple: the face has lists', ast.Dict: 'dict: the face has lists of pairs', ast.Set: 'set',
    ast.IfExp: 'conditional expression: write an if statement', ast.NamedExpr: 'assignment expression',
    ast.Yield: 'yield', ast.YieldFrom: 'yield', ast.Await: 'await', ast.Slice: 'slice', ast.Starred: 'starred expression',
    ast.JoinedStr: 'f-string: Ring has no formatting, join with cat() and plus()',
    ast.Subscript: 'subscript: an index is 1-based on Ring, write at(a, i) or setat(a, i, v)',
    ast.Import: 'import: Ring loads files, write load("file.ring")', ast.ImportFrom: 'import',
    ast.Raise: 'raise: Ring raises with the function raise("message")', ast.Assert: 'assert', ast.Delete: 'del statement: Ring\'s del() is a function',
    ast.Global: 'global statement: a Ring global is G.x', ast.Nonlocal: 'nonlocal', ast.With: 'with', ast.AsyncWith: 'async with', ast.AsyncFor: 'async for',
    ast.AsyncFunctionDef: 'async def', ast.Match: 'match', ast.AnnAssign: 'annotation', ast.TypeAlias: 'type alias',
}


def unident(t):
    """The Ring name a Python name spells (the inverse of face_py.ident): a trailing `_` after a keyword or a face word, `_` before a digit, `at_` for `@`."""
    if t.endswith('_') and len(t) > 1 and t != 'at_' and (keyword.iskeyword(t[:-1]) or t[:-1] in FACE_WORDS):
        return t[:-1]
    if t[:1] == '_' and t[1:2].isdigit():
        return t[1:]
    t = t.replace('__at__', '@')
    if t.startswith('at_'):
        t = '@' + t[3:]
    return t


def ring_literal(node, value):
    for q in ('"', "'", '`'):
        if q not in value:
            return q + value + q
    refuse('construct', node, 'a string holding all three of Ring\'s quotes cannot be written (F-55)')


def wrap(n):
    """A graph read from text has no parenthesis nodes, because Python's AST does not keep them and both printers parenthesize from the tree -- with one exception:
    a `not` that is the operand of a comparison, of arithmetic or of a unary sign. Ring binds `not` looser than those and the grammar's tree binds it tighter, so the
    graph says which was meant with a parenthesis, and the Ring that is written has it (`(not a) = b`)."""
    return mk('paren', e=n) if n['k'] == 'un' and n['op'] == 'not' else n


def sub_blocks(s):
    """The blocks of statements a statement holds, in source order."""
    if isinstance(s, ast.If):
        return [s.body, s.orelse]
    if isinstance(s, (ast.For, ast.While, ast.AsyncFor)):
        return [s.body, s.orelse]
    if isinstance(s, ast.Try):
        return [s.body] + [h.body for h in s.handlers] + [s.orelse, s.finalbody]
    if isinstance(s, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.With)):
        return [s.body]
    return []


def statements(body):
    """Every statement under a block, pre-order, with the blocks it holds."""
    for s in body:
        yield s
        for b in sub_blocks(s):
            yield from statements(b)


class Reader:
    def __init__(self, text):
        self.text = text.replace('\r\n', '\n')
        self.lines = self.text.split('\n')
        try:
            self.tree = ast.parse(self.text)
        except SyntaxError as e:
            raise ReadRefused('syntax', 'line %s: %s' % (e.lineno, e.msg))
        except ValueError as e:
            raise ReadRefused('syntax', str(e))
        self.catch = []                     # the handlers we are inside: the name each binds, or None
        self.region = None                  # the attributes a class region assigns, while it is read
        self.skip = set()                   # statements the face writes and Ring does not (`return ""`, `main()`, `super().__region__()`, a do-again's test)
        self.slots = {}                     # id(block) -> [(position in the block, (row, col, text))]: the comments that stand between its statements
        self.trails = {}                    # id(statement) -> the comment that follows it on its line
        self.place_comments()

    # -- comments ---------------------------------------------------------------------------------------------------------------------
    def place_comments(self):
        try:
            toks = [t for t in tokenize.generate_tokens(io.StringIO(self.text).readline) if t.type == tokenize.COMMENT]
        except (tokenize.TokenError, IndentationError) as e:
            raise ReadRefused('syntax', str(e))
        for t in toks:
            row, col = t.start
            text = t.string.rstrip()
            if row == 1 and text == face_py.BANNER:
                continue
            if self.lines[row - 1][:col].strip() == '':
                self.place(self.tree.body, (row, col, text))
            else:
                self.trail((row, col, text))

    def place(self, block, c):
        row, col, text = c
        before = [s for s in block if s.lineno < row]
        if before and col > before[-1].col_offset:
            prev = before[-1]
            blocks = [b for b in sub_blocks(prev) if b]
            inner = [b for b in blocks if b[0].lineno < row]
            if inner:
                k = blocks.index(inner[-1])
                if k + 1 < len(blocks) and self.header_between(prev, inner[-1][-1].end_lineno, row):
                    return self.place(blocks[k + 1], c)     # after `else:`, `except ...:` or `finally:` and before its first statement
                return self.place(inner[-1], c)
            if blocks and row <= prev.end_lineno:
                return self.place(blocks[0], c)              # before the first statement of the first block
        self.slots.setdefault(id(block), []).append((len(before), c))

    def header_between(self, stmt, lo, hi):
        """Is there a line between rows lo and hi that opens the next block of stmt: `else`, `elif`, `except`, `finally`, at stmt's own indentation?"""
        for r in range(lo + 1, hi):
            line = self.lines[r - 1]
            if len(line) - len(line.lstrip()) == stmt.col_offset and line.lstrip().startswith(('else', 'elif', 'except', 'finally')):
                return True
        return False

    def trail(self, c):
        """A comment after code on its line: it follows the deepest statement that ends on that line. On a header line (`else:  # note`) it opens the block."""
        row = c[0]
        best = None
        for s in statements(self.tree.body):
            if s.end_lineno == row:
                best = s
        if best is not None:
            self.trails[id(best)] = c
            return
        for s in statements(self.tree.body):
            if s.lineno <= row <= s.end_lineno:
                for b in sub_blocks(s):
                    if b and b[0].lineno > row:
                        self.slots.setdefault(id(b), []).append((0, c))
                        return
        self.place(self.tree.body, (row, 0, c[2]))

    def entries(self, block):
        slots = sorted(self.slots.get(id(block), []), key=lambda p: (p[0], p[1][0]))
        out, k = [], 0
        for i in range(len(block) + 1):
            while k < len(slots) and slots[k][0] == i:
                out.append(('comment', slots[k][1]))
                k += 1
            if i < len(block):
                out.append(('stmt', block[i]))
        return out

    # -- the graph ----------------------------------------------------------------------------------------------------------------------
    def graph(self):
        body = self.tree.body
        funcs = {s.name.lower() for s in body if isinstance(s, ast.FunctionDef)}
        last = body[-1] if body else None
        if (isinstance(last, ast.Expr) and isinstance(last.value, ast.Call) and isinstance(last.value.func, ast.Name) and last.value.func.id.lower() == 'main'
                and not last.value.args and not last.value.keywords and 'main' in funcs):
            self.skip.add(id(last))         # Ring calls Main() after the top level (F-60): the face calls it too, so that a Python reader sees it run
        seen_def = seen_class = False
        for s in body:
            if id(s) in self.skip:
                continue
            if isinstance(s, ast.FunctionDef):
                if seen_class:
                    refuse('order', s, 'a function after a class is a method of that class on Ring (F-21): functions come before classes')
                seen_def = True
            elif isinstance(s, ast.ClassDef):
                seen_class = seen_def = True
            elif seen_def:
                refuse('order', s, 'a statement after a definition belongs to the last function on Ring (HF-73): the top level comes first')
        return mk('file', items=self.block(body, 'top'))

    def block(self, body, kind):
        out = []
        ents = self.entries(body)
        i = 0
        while i < len(ents):
            tag, x = ents[i]
            if tag == 'comment':
                out.append(self.comment(x, kind))
                i += 1
                continue
            if kind != 'class' and self.switch_head(x) and i + 1 < len(ents) and ents[i + 1][0] == 'stmt':
                sw = self.switch(x, ents[i + 1][1])
                if sw is not None:
                    out.extend(self.with_trail([sw], ents[i + 1][1]))
                    i += 2
                    continue
            out.extend(self.with_trail(self.statement(x, kind), x))
            i += 1
        return out

    def comment(self, c, kind):
        if kind == 'class' and c[2] == face_py.PRIVATE_COMMENT:
            return mk('private')
        return l1.comment(c[2])

    def with_trail(self, items, node):
        c = self.trails.get(id(node))
        if c is None or not items:
            return items
        tgt = items[-1]
        if tgt['k'] in l1.CARRIERS and 'trail' not in tgt:
            tgt['trail'] = l1.comment(c[2])
            return items
        return items + [l1.comment(c[2])]

    # -- statements -----------------------------------------------------------------------------------------------------------------------
    def statement(self, s, kind):
        if id(s) in self.skip:
            return []
        t = type(s)
        if t in CONSTRUCTS:
            refuse('construct', s, CONSTRUCTS[t])
        if t is ast.Expr:
            return [self.expr_statement(s)]
        if t is ast.Assign:
            return [self.assign(s)]
        if t is ast.AugAssign:
            return [self.augassign(s)]
        if t is ast.If:
            return [self.if_statement(s, kind)]
        if t is ast.While:
            return [self.while_statement(s, kind)]
        if t is ast.For:
            return [self.for_statement(s, kind)]
        if t is ast.Try:
            return [self.try_statement(s, kind)]
        if t is ast.Return:
            if s.value is None or (isinstance(s.value, ast.Constant) and s.value.value == '' and isinstance(s.value.value, str)):
                return [] if id(s) in self.skip else [mk('return')]
            return [mk('return', e=self.expression(s.value))]
        if t is ast.Break:
            return [mk('exit')]
        if t is ast.Continue:
            return [mk('loop')]
        if t is ast.Pass:
            return []
        if t is ast.FunctionDef:
            if kind != 'top':
                refuse('construct', s, 'a definition inside a block: Ring has no nested functions, and a function after a function ends it')
            return [self.function(s, method=False)]
        if t is ast.ClassDef:
            if kind != 'top':
                refuse('construct', s, 'a class inside a block')
            return [self.klass(s)]
        refuse('construct', s, t.__name__)

    def expr_statement(self, s):
        v = s.value
        if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id in STATEMENT_WORDS and not v.keywords:
            name, args = v.func.id, v.args
            if name in ('say', 'see'):
                self.arity(v, name, args, 1)
                return mk(name, e=self.expression(args[0]))
            if name == 'bye':
                self.arity(v, name, args, 0)
                return mk('bye')
            if name == 'load':
                self.arity(v, name, args, 1)
                if not (isinstance(args[0], ast.Constant) and isinstance(args[0].value, str)):
                    refuse('word', v, '`load` takes the file name as a string')
                return mk('load', path=mk('str', text=ring_literal(v, args[0].value)))
            if name == 'setat':
                self.arity(v, name, args, 3)
                return mk('expr', e=mk('assign', op='=', l=mk('index', obj=self.expression(args[0]), idx=self.expression(args[1])), r=self.expression(args[2])))
            refuse('word', v, '`%s` is read as the right side of an assignment: `x = give()`' % name)
        return mk('expr', e=self.expression(v))

    def arity(self, node, name, args, n):
        if len(args) != n:
            refuse('word', node, '`%s` takes %d argument(s), the text gives %d' % (name, n, len(args)))

    def target(self, t):
        if isinstance(t, ast.Name):
            if t.id in FACE_WORDS and t.id != 'self':
                refuse('word', t, '`%s` is a word of the face' % t.id)
            return mk('id', text=unident(t.id))
        if isinstance(t, ast.Attribute):
            return self.attribute(t, call=False)
        if isinstance(t, ast.Subscript):
            refuse('construct', t, 'a subscript target: write setat(a, i, v)')
        if isinstance(t, (ast.Tuple, ast.List)):
            refuse('construct', t, 'tuple target: Ring assigns one name')
        refuse('construct', t, type(t).__name__)

    def assign(self, s):
        if len(s.targets) != 1:
            refuse('construct', s, 'two targets: `a = b = 1` compares on Ring (F-59)')
        tgt = s.targets[0]
        v = s.value
        if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == 'give' and not v.args and not v.keywords:
            return mk('give', target=self.target(tgt))
        return mk('expr', e=mk('assign', op='=', l=self.target(tgt), r=self.expression(v)))

    def augassign(self, s):
        op = {ast.Add: '+=', ast.Sub: '-=', ast.Mult: '*=', ast.Div: '/='}.get(type(s.op))
        if op is None:
            refuse('construct', s, 'the augmented operator %s: write %s' % (type(s.op).__name__, 'mod(x, y) for %' if isinstance(s.op, ast.Mod) else 'the assignment'))
        tgt = self.target(s.target)
        v = s.value
        if op in ('+=', '-=') and isinstance(v, ast.Constant) and type(v.value) is int and ast.get_source_segment(self.text, v) == '1':
            return mk('expr', e=mk('post', op='++' if op == '+=' else '--', e=tgt))
        return mk('expr', e=mk('assign', op=op, l=tgt, r=self.expression(v)))

    def if_statement(self, s, kind):
        cond, then = self.expression(s.test), self.block(s.body, 'body')
        elifs, els, cur = [], None, s
        while cur.orelse:
            if len(cur.orelse) == 1 and isinstance(cur.orelse[0], ast.If) and id(cur.orelse) not in self.slots:
                nxt = cur.orelse[0]
                elifs.append(mk('elif', cond=self.expression(nxt.test), items=self.block(nxt.body, 'body')))
                cur = nxt
            else:
                els = self.block(cur.orelse, 'body')
                break
        return mk('if', cond=cond, then=then, elifs=elifs, **{'else': els})

    def while_statement(self, s, kind):
        if s.orelse:
            refuse('construct', s, 'else on a loop')
        if isinstance(s.test, ast.Constant) and s.test.value is True:
            last = s.body[-1] if s.body else None
            if (isinstance(last, ast.If) and isinstance(last.test, ast.UnaryOp) and isinstance(last.test.op, ast.Not) and not last.orelse
                    and len(last.body) == 1 and isinstance(last.body[0], ast.Break)):
                self.skip.add(id(last))
                items = self.block(s.body, 'body')
                node = mk('dowhile', items=items, cond=self.expression(last.test.operand))
                c = self.trails.get(id(last))
                if c is not None and id(s) not in self.trails:
                    self.trails[id(s)] = c
                return node
            refuse('construct', s, 'while True: the face\'s only `while True:` is `do ... again c`, its body ending in `if not (c): break`')
        return mk('while', cond=self.expression(s.test), items=self.block(s.body, 'body'))

    def for_statement(self, s, kind):
        if s.orelse:
            refuse('construct', s, 'else on a loop')
        var = self.target(s.target)
        if var['k'] != 'id':
            refuse('construct', s, 'a loop variable is a name')
        it = s.iter
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == 'span':
            if it.keywords or not 2 <= len(it.args) <= 3:
                refuse('word', it, '`span` takes a start, an end and optionally a step')
            a, b = self.expression(it.args[0]), self.expression(it.args[1])
            step = self.expression(it.args[2]) if len(it.args) == 3 else None
            return mk('for', var=var['text'], kind='to', a=a, b=b, step=step, items=self.block(s.body, 'body'))
        return mk('for', var=var['text'], kind='in', a=self.expression(it), items=self.block(s.body, 'body'))

    def try_statement(self, s, kind):
        if s.orelse:
            refuse('construct', s, 'try ... else')
        if len(s.handlers) > 1:
            refuse('construct', s, 'several except clauses: Ring has one catch')
        catch = None
        if s.handlers:
            h = s.handlers[0]
            if not (isinstance(h.type, ast.Name) and h.type.id == 'RingError'):
                refuse('construct', h, 'the handler is `except RingError as e:`')
            name = h.name
            via_str = set()
            for st in h.body:
                for n in ast.walk(st):
                    if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'str' and len(n.args) == 1
                            and isinstance(n.args[0], ast.Name) and n.args[0].id == name):
                        via_str.add(id(n.args[0]))
            bare = name is not None and any(isinstance(n, ast.Name) and n.id == name and id(n) not in via_str for st in h.body for n in ast.walk(st))
            self.catch.append(name)
            try:
                items = self.block(h.body, 'body')
            finally:
                self.catch.pop()
            catch = mk('catch', binding=unident(name) if bare else None, items=items)
        return mk('try', items=self.block(s.body, 'body'), catch=catch, **{'finally': self.block(s.finalbody, 'body') if s.finalbody else None})

    def switch_head(self, s):
        return isinstance(s, ast.Assign) and len(s.targets) == 1 and isinstance(s.targets[0], ast.Name) and s.targets[0].id == '_switch'

    def switch_values(self, test):
        """The values of a case: `eq(_switch, v)`, or several joined by `or`."""
        def one(n):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'eq' and len(n.args) == 2 and not n.keywords
                    and isinstance(n.args[0], ast.Name) and n.args[0].id == '_switch'):
                return n.args[1]
            return None
        if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
            vs = [one(v) for v in test.values]
            return None if any(v is None for v in vs) else vs
        v = one(test)
        return None if v is None else [v]

    def switch(self, head, first):
        """`_switch = subject` and the chain of `eq(_switch, v)` after it, as the printer writes a switch."""
        if not isinstance(first, ast.If):
            return None
        chain, other, cur = [], None, first
        if isinstance(first.test, ast.Constant) and first.test.value is True and not first.orelse:
            other = first.body
        else:
            while True:
                vals = self.switch_values(cur.test)
                if vals is None:
                    return None
                chain.append((vals, cur.body))
                if not cur.orelse:
                    break
                nxt = cur.orelse[0] if len(cur.orelse) == 1 and isinstance(cur.orelse[0], ast.If) and id(cur.orelse) not in self.slots else None
                if nxt is not None and self.switch_values(nxt.test) is not None:
                    cur = nxt
                    continue
                other = cur.orelse
                break
        cases = [mk('case', values=[self.expression(v) for v in vals], items=self.block(body, 'body')) for vals, body in chain]
        return mk('switch', subject=self.expression(head.value), cases=cases, other=self.block(other, 'body') if other is not None else None)

    # -- definitions --------------------------------------------------------------------------------------------------------------------------
    def function(self, s, method):
        if s.decorator_list:
            refuse('construct', s, 'decorator')
        a = s.args
        if a.vararg or a.kwarg or a.kwonlyargs or a.posonlyargs:
            refuse('construct', s, '*args, **kwargs, keyword-only and positional-only parameters: Ring has plain parameters')
        if a.defaults:
            refuse('construct', s, 'default parameter: Ring has none')
        if s.returns or any(x.annotation for x in a.args):
            refuse('construct', s, 'annotation')
        names = [x.arg for x in a.args]
        if method:
            if not names or names[0] != 'self':
                refuse('construct', s, 'a method\'s first parameter is self')
            names = names[1:]
        last = s.body[-1] if s.body else None
        if (isinstance(last, ast.Return) and isinstance(last.value, ast.Constant) and last.value.value == '' and isinstance(last.value.value, str)
                and id(last) not in self.trails):
            self.skip.add(id(last))         # the face writes the NULL a function returns when it returns nothing; a comment on it would go with it, so it stays
        items = self.block(s.body, 'func')
        return mk('func', name=unident(s.name), params=[mk('param', name=unident(n)) for n in names], items=items)

    def klass(self, s):
        if s.decorator_list or s.keywords:
            refuse('construct', s, 'decorator or class keyword')
        if len(s.bases) > 1:
            refuse('construct', s, 'several base classes: Ring has one parent')
        parent = None
        if s.bases:
            parent = self.qualified(s.bases[0], 'a base class is a name')
        items = []
        for tag, x in self.entries(s.body):
            if tag == 'comment':
                items.append(self.comment(x, 'class'))
                continue
            if isinstance(x, ast.Pass):
                continue
            if isinstance(x, ast.FunctionDef):
                if x.name == face_py.REGION:
                    items.extend(self.with_trail(self.region_def(x, parent is not None), x))
                else:
                    items.extend(self.with_trail([self.function(x, method=True)], x))
                continue
            refuse('construct', x, 'a class body holds methods and `def __region__(self):`, not %s' % type(x).__name__)
        return mk('class', name=unident(s.name), parent=parent, items=items)

    def region_def(self, s, has_parent):
        names = [x.arg for x in s.args.args]
        if names != ['self'] or s.decorator_list or s.args.defaults:
            refuse('construct', s, '`def __region__(self):` takes self and nothing else')
        assigned = set()
        for st in s.body:
            for n in ast.walk(st):
                tg = []
                if isinstance(n, ast.Assign):
                    tg = n.targets
                elif isinstance(n, (ast.AugAssign, ast.AnnAssign)):
                    tg = [n.target]
                elif isinstance(n, ast.For):
                    tg = [n.target]
                for t in tg:
                    if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == 'self' and not t.attr.startswith('at_'):
                        assigned.add(t.attr)
        first = s.body[0] if s.body else None
        if (has_parent and isinstance(first, ast.Expr) and isinstance(first.value, ast.Call) and isinstance(first.value.func, ast.Attribute)
                and first.value.func.attr == face_py.REGION and isinstance(first.value.func.value, ast.Call)
                and isinstance(first.value.func.value.func, ast.Name) and first.value.func.value.func.id == 'super'):
            self.skip.add(id(first))
        saved, self.region = self.region, assigned
        try:
            return self.block(s.body, 'region')
        finally:
            self.region = saved

    def qualified(self, n, why):
        if isinstance(n, ast.Name):
            return [unident(n.id)]
        if isinstance(n, ast.Attribute):
            return self.qualified(n.value, why) + [unident(n.attr)]
        refuse('word', n, why)

    # -- expressions -----------------------------------------------------------------------------------------------------------------------------
    def condition(self, n):
        return self.expression(n)

    def expression(self, n):
        t = type(n)
        if t in CONSTRUCTS:
            refuse('construct', n, CONSTRUCTS[t])
        if t is ast.Constant:
            return self.constant(n)
        if t is ast.Name:
            if n.id == 'self':
                return mk('self')
            if n.id in FACE_WORDS:
                refuse('word', n, '`%s` is a word of the face and is read where the face uses it' % n.id + (' (`G.x` is the global $x)' if n.id == 'G' else ''))
            return mk('id', text=unident(n.id))
        if t is ast.Attribute:
            return self.attribute(n, call=False)
        if t is ast.Call:
            return self.call(n)
        if t is ast.BinOp:
            op = BINOPS.get(type(n.op))
            if op is None:
                refuse('construct', n, 'the operator %s' % ('//' if isinstance(n.op, ast.FloorDiv) else type(n.op).__name__))
            return mk('bin', op=op, l=wrap(self.expression(n.left)), r=wrap(self.expression(n.right)))
        if t is ast.BoolOp:
            op = 'and' if isinstance(n.op, ast.And) else 'or'
            acc = self.expression(n.values[0])
            for v in n.values[1:]:
                acc = mk('bin', op=op, l=acc, r=self.expression(v))
            return acc
        if t is ast.Compare:
            if len(n.ops) != 1:
                refuse('construct', n, 'a chained comparison: Ring compares two values')
            op = CMPOPS.get(type(n.ops[0]))
            if op is None:
                refuse('construct', n, '`%s` (the face compares with == != < <= > >=, or eq lt gt ...)' % type(n.ops[0]).__name__.lower().replace('not', 'not ').strip())
            return mk('bin', op=op, l=wrap(self.expression(n.left)), r=wrap(self.expression(n.comparators[0])))
        if t is ast.UnaryOp:
            op = {ast.USub: '-', ast.UAdd: '+', ast.Not: 'not'}.get(type(n.op))
            if op is None:
                refuse('construct', n, 'the operator ~')
            return mk('un', op=op, e=self.expression(n.operand) if op == 'not' else wrap(self.expression(n.operand)))
        if t is ast.List:
            return mk('list', items=[self.expression(x) for x in n.elts])
        refuse('construct', n, t.__name__)

    def constant(self, n):
        v = n.value
        if v is True or v is False:
            refuse('construct', n, '`%s` is Python\'s: the face writes 1 and 0' % v)
        if v is None:
            refuse('construct', n, '`None` is Python\'s: the face writes ""')
        if isinstance(v, (bytes, complex)) or v is Ellipsis:
            refuse('construct', n, type(v).__name__)
        if isinstance(v, str):
            return mk('str', text=ring_literal(n, v))
        seg = ast.get_source_segment(self.text, n) or str(v)
        if not NUMBER.match(seg):
            refuse('construct', n, 'the number %s (Ring has digits, a point, an exponent and 0x)' % seg)
        if re.match(r'^[0-9]+\.0$', seg) and int(seg[:-2]) > 2 ** 53:
            seg = seg[:-2]                   # the face writes a number past 2^53 as the double it is (F-75)
        return mk('num', text=seg)

    def attribute(self, n, call):
        v, attr = n.value, n.attr
        if isinstance(v, ast.Name) and v.id == 'G':
            return mk('id', text='$' + unident(attr))
        if isinstance(v, ast.Name) and v.id == 'self':
            if not call:
                if attr.startswith('at_'):
                    return mk('id', text=unident(attr))
                if self.region is not None and attr in self.region:
                    return mk('id', text=unident(attr))
            return mk('member', obj=mk('self'), prop=mk('id', text=unident(attr)))
        return mk('member', obj=wrap(self.expression(v)), prop=mk('id', text=unident(attr)))

    def call(self, n):
        if n.keywords:
            refuse('construct', n, 'keyword argument: Ring\'s named arguments are lists, :name = value (F-59)')
        if any(isinstance(a, ast.Starred) for a in n.args):
            refuse('construct', n, 'starred argument')
        f, args = n.func, n.args
        if isinstance(f, ast.Name):
            w = f.id
            if w == 'super' and not args:
                return mk('super')
            if w == 'at':
                self.arity(n, w, args, 2)
                return mk('index', obj=wrap(self.expression(args[0])), idx=self.expression(args[1]))
            if w in COMPARE:
                self.arity(n, w, args, 2)
                return mk('bin', op=COMPARE[w], l=wrap(self.expression(args[0])), r=wrap(self.expression(args[1])))
            if w in ('cat', 'plus', 'mod', 'rng', 'both', 'either'):
                self.arity(n, w, args, 2)
                op = {'cat': '+', 'plus': '+', 'mod': '%', 'rng': ':', 'both': 'and', 'either': 'or'}[w]
                if w in ('both', 'either'):
                    return mk('bin', op=op, l=self.expression(args[0]), r=self.expression(args[1]))
                return mk('bin', op=op, l=wrap(self.expression(args[0])), r=wrap(self.expression(args[1])))
            if w == 'negate':
                self.arity(n, w, args, 1)
                return mk('un', op='not', e=wrap(self.expression(args[0])))
            if w == 'new':
                if not args:
                    refuse('word', n, '`new(K, ...)` names the class first')
                return mk('new', name=self.qualified(args[0], '`new` names a class'), args=[self.expression(a) for a in args[1:]])
            if w == 'new_without_init':
                self.arity(n, w, args, 1)
                return mk('new', name=self.qualified(args[0], '`new_without_init` names a class'))
            if w == 'str':
                self.arity(n, w, args, 1)
                if not (self.catch and self.catch[-1] and isinstance(args[0], ast.Name) and args[0].id == self.catch[-1]):
                    refuse('word', n, '`str(e)` is the message of the handler\'s error, read inside `except RingError as e:` and nowhere else')
                return mk('id', text='cCatchError')
            if w in STATEMENT_WORDS:
                refuse('word', n, '`%s` is a statement%s' % (w, ', not a value' if w in ('say', 'see', 'bye', 'load', 'setat') else ''))
            if w == 'span':
                refuse('word', n, '`span` is the bound of a numeric loop: `for i in span(a, b):`')
            if w in FACE_WORDS and w != 'self':
                refuse('word', n, '`%s` is a word of the face' % w)
            callee = mk('id', text=unident(w))
        elif isinstance(f, ast.Attribute):
            callee = self.attribute(f, call=True)
        else:
            callee = wrap(self.expression(f))
        return mk('call', callee=callee, args=[self.expression(a) for a in args])


# ---- canonicity: the text must be the face's own spelling of its graph -----------------------------------------------------------------------

class Normal(ast.NodeTransformer):
    """What the face writes and Ring does not say, and what Python's parser does not keep: dropped from both sides before they are compared."""
    def visit_FunctionDef(self, n):
        self.generic_visit(n)
        if n.body and isinstance(n.body[-1], ast.Return) and isinstance(n.body[-1].value, ast.Constant) and n.body[-1].value.value == '':
            n.body = n.body[:-1]
        n.body = [s for s in n.body if not isinstance(s, ast.Pass)]
        return n

    def visit_Module(self, n):
        self.generic_visit(n)
        if (n.body and isinstance(n.body[-1], ast.Expr) and isinstance(n.body[-1].value, ast.Call) and isinstance(n.body[-1].value.func, ast.Name)
                and n.body[-1].value.func.id.lower() == 'main' and not n.body[-1].value.args):
            n.body = n.body[:-1]
        n.body = [s for s in n.body if not isinstance(s, ast.Pass)]
        return n

    def visit_BoolOp(self, n):
        self.generic_visit(n)
        flat = []
        for v in n.values:
            if isinstance(v, ast.BoolOp) and type(v.op) is type(n.op):
                flat.extend(v.values)
            else:
                flat.append(v)
        n.values = flat
        return n

    def generic_visit(self, n):
        super().generic_visit(n)
        for f in ('body', 'orelse', 'finalbody'):
            b = getattr(n, f, None)
            if isinstance(b, list) and b and all(isinstance(s, ast.stmt) for s in b):
                kept = [s for s in b if not isinstance(s, ast.Pass)]
                setattr(n, f, kept)
        return n


def normal(text):
    return Normal().visit(ast.parse(text))


def head(s):
    c = copy.copy(s)
    for f in ('body', 'orelse', 'finalbody', 'handlers'):
        if hasattr(c, f):
            setattr(c, f, [])
    return ast.dump(c)


def flat(tree):
    out = []

    def go(body):
        for s in body:
            out.append(s)
            if isinstance(s, ast.Try):
                go(s.body)
                for h in s.handlers:
                    out.append(h)
                    go(h.body)
                go(s.orelse)
                go(s.finalbody)
            else:
                for f in ('body', 'orelse'):
                    b = getattr(s, f, None)
                    if isinstance(b, list):
                        go(b)
    go(tree.body)
    return out


def difference(text, canon):
    """None when the text is the face's spelling, else the first line that is not."""
    a, b = normal(text), normal(canon)
    if ast.dump(a) == ast.dump(b):
        return None
    ta, tb = text.split('\n'), canon.split('\n')
    sa, sb = flat(a), flat(b)
    for x, y in zip(sa, sb):
        if head(x) != head(y):
            return 'line %d: the text has `%s`, the face writes `%s`' % (x.lineno, ta[x.lineno - 1].strip(), tb[y.lineno - 1].strip())
    if len(sa) != len(sb):
        longer, lines, who = (sb, tb, 'the face writes') if len(sb) > len(sa) else (sa, ta, 'the text has')
        s = longer[min(len(sa), len(sb))]
        return '%s a statement more: `%s`' % (who, lines[s.lineno - 1].strip())
    return 'the text differs from the face\'s spelling of its graph'


def read_py(text, strict=True):
    """The graph of a text in the face. strict: refuse a spelling the face does not print. The printer's collisions are refused either way."""
    text = text.replace('\r\n', '\n')
    r = Reader(text)
    g = r.graph()
    canon = face_py.print_py(g)             # raises face_py.Refused for a collision (for-after, name-clash, ...)
    if strict:
        why = difference(text, canon)
        if why:
            raise ReadRefused('not-canonical', why)
    return g


def ring_of(g):
    """The canonical Ring text of a graph: parentheses by Ring's precedence."""
    return l1.print_ring(g)


def read_ring(text, strict=True):
    return ring_of(read_py(text, strict))


def main(argv):
    lenient = '--lenient' in argv
    argv = [a for a in argv if a != '--lenient']
    if len(argv) != 1:
        print(__doc__)
        return 2
    text = open(argv[0], 'rb').read().decode('utf-8')
    try:
        sys.stdout.write(read_ring(text, strict=not lenient))
    except (ReadRefused, face_py.Refused) as e:
        print('refused -- ' + str(e))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
