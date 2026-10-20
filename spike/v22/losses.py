"""losses.py -- what the Python-shaped face does not keep, written down as one function (rung 7 of the code-graph memo; Haro v0.22).

    declared(graph) -> graph      the graph with the face's NAMED LOSSES erased

The memo's round-trip court says: across faces, L1 to face to L1 is exact. It is exact up to these, and only these; a difference the function does not erase is a
loss nobody named, and the court fails on it. Every entry is a spelling, never a meaning: the oracle judges meaning (the S step), and a loss that changed meaning
would be a collision and be refused by the printer instead. Each entry can be switched off (ON), so the court can show that each one is needed.

  case         names: Ring folds case (F-18), the face writes every use as the first spelling
  parens       the face prints Python's precedence, not the author's parentheses
  strings      a Ring string is its value: quotes are the face's choice; `:Name` is "name", NULL is "", true is 1
  pairs        `:name = value`, in a list or as an argument, is the list ["name", value] (F-59); a string key before `=` in a list is a comparison (F-93)
  assign       `x += v`, `x -= v`, `x++` and `x = x + v` are one statement for the face; `&&` is `and`, `||` is `or`, `exit 1` is `exit`
  returns      a function that runs off its end, a bare `return` and `return ""` are one NULL (F-66)
  comments     the three kinds are `#`, one line a comment
  trails       a comment after a statement stands on its last line: on the deepest statement that ends there
  elif         an else holding only an if is an elif
  classes      the region first, then the methods; a bare name the region assigns, `This.x` and `x` in it are one attribute; `This.@x` is `@x`; `self` and `This` agree
  catch        a binding is kept only if the handler uses the name
  numbers      a number past 2^53 is written as the double it is (F-75)
"""
import copy, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v21'))
sys.path.insert(0, os.path.join(HERE, '..', 'v18'))
import face_py
import l1

ALL = ('case', 'parens', 'strings', 'pairs', 'assign', 'returns', 'comments', 'trails', 'elif', 'classes', 'catch', 'numbers')
ON = set(ALL)
LOGIC = {'and': 'and', '&&': 'and', 'or': 'or', '||': 'or'}
LISTS = ('items', 'then', 'else', 'other', 'finally')


def low(t):
    return t.lower() if 'case' in ON else t


def string(value):
    return {'k': 'str', 'value': value}


def comments_of(text):
    if 'comments' not in ON:
        return [{'k': 'comment', 'text': text}]
    return [{'k': 'comment', 'text': line} for line in face_py.py_comment(text)]


def uses(n, name):
    if isinstance(n, dict):
        if n.get('k') == 'id' and n['text'].lower() == name:
            return True
        return any(uses(v, name) for v in n.values())
    if isinstance(n, list):
        return any(uses(v, name) for v in n)
    return False


def fold(n):
    if isinstance(n, list):
        return [fold(x) for x in n]
    if not isinstance(n, dict):
        return n
    k = n['k']
    n = dict(n)
    for f, v in list(n.items()):
        if isinstance(v, (dict, list)):
            n[f] = fold(v)
    if k == 'paren':
        return n['e'] if 'e' in n and 'parens' in ON else n
    if k == 'id':
        n['text'] = low(n['text'])
        return n
    if 'strings' in ON:
        if k == 'str':
            return n if 'value' in n else string(n['text'][1:-1])
        if k == 'sym':
            return string(n['text'][1:].strip().lower())
        if k == 'null':
            return string('')
        if k == 'bool':
            return {'k': 'num', 'text': '1' if n['value'] else '0'}
    if k == 'num':
        t = n['text']
        if 'numbers' in ON and re.match(r'^[0-9]+\.0$', t) and int(t[:-2]) > 2 ** 53:
            t = t[:-2]
        return {'k': 'num', 'text': t.lower()}
    if k == 'self':
        return {'k': 'self'} if 'classes' in ON else n
    if k == 'bin':
        if 'assign' in ON and n['op'] in LOGIC:
            n['op'] = LOGIC[n['op']]
        return n
    if k == 'member':
        if 'classes' in ON and n['obj'].get('k') == 'self' and n['prop'].get('k') == 'id' and n['prop']['text'].startswith('@'):
            return n['prop']                       # This.@x is @x
        return n
    if k == 'new':
        n['name'] = [low(x) for x in n['name']]
        return n
    if k in ('func', 'param'):
        n['name'] = low(n['name'])
        n.pop('type', None)
        return n
    if k == 'class':
        n['name'] = low(n['name'])
        if 'parent' in n:
            n['parent'] = [low(x) for x in n['parent']]
        return n
    if k == 'for':
        n['var'] = low(n['var'])
        return n
    if k in ('exit', 'loop'):
        if 'assign' in ON and 'e' in n and n['e'] == {'k': 'num', 'text': '1'}:
            del n['e']
        return n
    if k == 'return':
        n.pop('amp', None)
        if 'returns' in ON and n.get('e') == string(''):
            del n['e']
        return n
    return n


def pairs(n):
    """`:name = value` and the pair node: the list [\"name\", value]; a pair keyed by anything else is a comparison."""
    if isinstance(n, list):
        return [pairs(x) for x in n]
    if not isinstance(n, dict):
        return n
    n = {f: pairs(v) if isinstance(v, (dict, list)) else v for f, v in n.items()}
    if n['k'] == 'pair':
        if n['key'].get('k') == 'sym':
            return {'k': 'list', 'items': [string(n['key']['text'][1:].strip().lower()), n['value']]}
        return {'k': 'bin', 'op': '=', 'l': n['key'], 'r': n['value']}
    if n['k'] == 'bin' and n['op'] == '=' and n['l'].get('k') == 'sym':
        return {'k': 'list', 'items': [string(n['l']['text'][1:].strip().lower()), n['r']]}
    return n


def statements(items):
    """A block: comments split to one line each, the compound assignments and ++ written out."""
    out = []
    for it in items:
        if it['k'] == 'comment':
            out.extend(comments_of(it['text']))
            continue
        it = dict(it)
        if 'trail' in it and 'comments' in ON:
            it['trail'] = {'k': 'comment', 'text': ' '.join(face_py.py_comment(it['trail']['text']))}
        if it['k'] == 'expr' and 'assign' in ON:
            e = it['e']
            if e['k'] == 'post':
                it['e'] = {'k': 'assign', 'op': '=', 'l': e['e'], 'r': {'k': 'bin', 'op': e['op'][0], 'l': e['e'], 'r': {'k': 'num', 'text': '1'}}}
            elif e['k'] == 'assign' and e['op'] != '=':
                it['e'] = {'k': 'assign', 'op': '=', 'l': e['l'], 'r': {'k': 'bin', 'op': e['op'][:-1], 'l': e['l'], 'r': e['r']}}
        out.append(it)
    return out


def walk(n):
    if isinstance(n, dict):
        yield n
        for v in n.values():
            yield from walk(v)
    elif isinstance(n, list):
        for x in n:
            yield from walk(x)


def attribute(n, assigned):
    """In a class region a bare name the region assigns, and `This.x`, are one attribute: written `This.x`."""
    if isinstance(n, list):
        return [attribute(x, assigned) for x in n]
    if not isinstance(n, dict):
        return n
    if n.get('k') == 'id' and n['text'] in assigned:
        return {'k': 'member', 'obj': {'k': 'self'}, 'prop': n}
    return {f: attribute(v, assigned) if isinstance(v, (dict, list)) else v for f, v in n.items()}


def shape(n):
    """The structure: blocks normalized, classes in the face's order, catch bindings, else-if."""
    if isinstance(n, list):
        return [shape(x) for x in n]
    if not isinstance(n, dict):
        return n
    n = {f: shape(v) if isinstance(v, (dict, list)) else v for f, v in n.items()}
    for f in LISTS:
        if f in n and isinstance(n[f], list) and (not n[f] or isinstance(n[f][0], dict) and 'k' in n[f][0]):
            n[f] = statements(n[f])
    k = n['k']
    if k == 'func' and 'returns' in ON:
        it = n.get('items', [])
        if it and it[-1]['k'] == 'return' and 'e' not in it[-1] and 'trail' not in it[-1]:
            it = it[:-1]                                     # a function that runs off its end returns NULL: a final bare return says nothing
        n['items'] = it
    if k == 'if' and 'elif' in ON:
        while n.get('else') is not None and len(n['else']) == 1 and n['else'][0]['k'] == 'if' and 'trail' not in n['else'][0]:
            inner = n['else'][0]
            n['elifs'] = list(n.get('elifs', [])) + [{'k': 'elif', 'cond': inner['cond'], 'items': inner.get('then', [])}] + list(inner.get('elifs', []))
            if 'else' in inner:
                n['else'] = inner['else']
            else:
                del n['else']
    if k == 'try' and 'catch' in n and 'binding' in n['catch'] and 'catch' in ON:
        b = n['catch']['binding'].lower()
        if not uses(n['catch'].get('items', []), b):
            n['catch'] = {f: v for f, v in n['catch'].items() if f != 'binding'}
        else:
            n['catch'] = dict(n['catch'], binding=b)
    if k == 'class' and 'classes' in ON:
        items = n.get('items', [])
        region = [x for x in items if x['k'] not in ('func', 'private')]
        rest = [x for x in items if x['k'] in ('func', 'private')]
        assigned = set()
        for x in walk(region):
            if x.get('k') == 'assign':
                lv = x['l']
                if lv['k'] == 'id' and not lv['text'].startswith(('@', '$')):
                    assigned.add(lv['text'])
                elif lv['k'] == 'member' and lv['obj'].get('k') == 'self' and lv['prop'].get('k') == 'id':
                    assigned.add(lv['prop']['text'].lower())
        n['items'] = attribute(region, assigned) + rest
    return n


def last_block(n):
    """The block whose last statement ends the statement n on its last line, or None."""
    k = n['k']
    if k == 'if':
        if n.get('else') is not None:
            return n['else']
        if n.get('elifs'):
            return n['elifs'][-1].get('items', [])
        return n.get('then', [])
    if k == 'try':
        if n.get('finally'):
            return n['finally']
        if 'catch' in n:
            return n['catch'].get('items', [])
        return n.get('items', [])
    if k == 'switch':
        if n.get('other') is not None:
            return n['other']
        return n['cases'][-1].get('items', []) if n.get('cases') else None
    if k in ('while', 'for', 'dowhile', 'func', 'class'):
        return n.get('items', [])
    return None


def lower_trails(n):
    """A comment after a statement on its line stands on the statement's last line, which is the last line of the deepest statement that ends there."""
    if isinstance(n, list):
        for x in n:
            lower_trails(x)
        return
    if not isinstance(n, dict):
        return
    for v in n.values():
        if isinstance(v, (dict, list)):
            lower_trails(v)
    if 'trail' in n and n['k'] != 'comment':
        tgt = n
        while True:
            blk = last_block(tgt)
            if not blk or blk[-1]['k'] == 'comment' or 'trail' in blk[-1]:
                break
            tgt = blk[-1]
        if tgt is not n:
            tgt['trail'] = n.pop('trail')


def declared(g):
    g = copy.deepcopy(g)
    if 'pairs' in ON:
        g = pairs(g)
    g = fold(g)
    g = shape(g)
    if 'trails' in ON:
        lower_trails(g)
    return g


def first_difference(a, b, path='graph'):
    """Where two declared graphs part, as a path and the two things found there."""
    if type(a) != type(b):
        return '%s: %s against %s' % (path, str(a)[:70], str(b)[:70])
    if isinstance(a, dict):
        for f in sorted(set(a) | set(b)):
            if f not in a:
                return '%s.%s only in the reading: %s' % (path, f, str(b[f])[:80])
            if f not in b:
                return '%s.%s only in the original: %s' % (path, f, str(a[f])[:80])
            d = first_difference(a[f], b[f], path + '.' + f + ('<%s>' % a.get('k') if f == 'items' else ''))
            if d:
                return d
        return None
    if isinstance(a, list):
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_difference(x, y, '%s[%d]' % (path, i))
            if d:
                return d
        if len(a) != len(b):
            longer, who = (a, 'original') if len(a) > len(b) else (b, 'reading')
            return '%s: the %s has %d more item(s), the first %s' % (path, who, abs(len(a) - len(b)), str(longer[min(len(a), len(b))])[:90])
        return None
    return None if a == b else '%s: %r against %r' % (path, a, b)
