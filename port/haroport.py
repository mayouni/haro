"""haroport -- a tree of the classic Ring surface ported to .haro, mechanically (HARO-PORTTOOL-01, stzlib-haroport 2026-11-10).

  python port/haroport.py plan  ROOT [--json]       what it would do, file by file; writes nothing
  python port/haroport.py apply ROOT --out DIR      the ported tree in DIR: each .ring file as .haro, each load rewritten to it
  ... --unit FILE                                   the functions a call can reach read from FILE and what it loads (B, D)

THE REWRITES, in this order, each on code only (a string, a comment, a symbol's name are never touched):
  K  a keyword in any case is written in lowercase -- the keywords are vm/src/lift.zig's ring_keywords, read from there
  U  Softanza's method-local spelling _name_ is unwrapped to name
  C  Softanza's c (text) is t and its v (any value) is x: cName -> tName, $cX -> $tX, @cX -> @tX -- one decision for the whole tree
  L  a bare name declared in a function (assigned, a parameter) is lettered by what it holds: n a number, t a text, a a list, o an object,
     x anything else or two kinds -- never at the top level or in a class body, never a name the class declares as an attribute
  G  a library-internal global $_name is $name -- one decision for the whole tree
  B  a built-in called by name is written in its one spelling (study/v48/builtin_names.py), unless the tree defines a function of that name
  D  a call to a function the tree declares at a file's top level is written as it is declared; a name declared in two spellings is refused
  P  `:key = value` is the pair [:key, value] (HARO-SURFACE-01), the value read to the comma or closing bracket at its own depth
  R  (the Principal's HAROPORT-SPELLINGS-02, 2026-11-11) a parameter keeps its p mark (pc -> pt, pa + element -> pv + element); a list
     letter is v and the element's (an/ac/ao/aa -> vi/vt/vo/vv); an ALL_CAPS name and an @Capitalised attribute take their letter by what
     they hold (1 or 0 alone and never counted: a boolean)
  Y  a b name given 1 or 0 is given true or false, and a condition on a literal 1 or 0 is on true or false
  N  (D71) `null` is `""` and `isnull(x)` is `IsEmpty(x)`
  O  (D69) see and put: `see E + nl` is `print E`, any other is `FWrite(stdout, E)`
  O  (D67, HARO-ONEFORM-01) one form for each construct: every block ends with `end` (never ok, next, off, done, endX, braces), a
     definition has no end word, one word each (func, elseif, else, case, for, see, give, exit, loop, and, or, not, from), `#` for a
     comment, `this` outside a brace object, parameters in parentheses and none without, no period after a call ending a statement
A RENAME IS REFUSED, and listed, when its new name is a keyword in any case, is already a name in its scope (for C: anywhere in the tree),
or is in a method an attribute its class declares (a bare assignment to one writes the attribute in Ring; a local would change the
program). The name is then left as it was written.
"""
import json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'study', 'v48'))
import builtin_names  # noqa: E402

TOK = re.compile(r'''(?P<cm>\#[^\n]*|//[^\n]*|/\*.*?\*/)|(?P<st>"[^"]*"|'[^']*'|`[^`]*`)|(?P<id>[$@]?[A-Za-z_][A-Za-z0-9_]*)|(?P<num>\d+(?:\.\d+)?)|(?P<nl>\n)|(?P<ws>[ \t\r]+)|(?P<op>.)''', re.S)


def keywords():
    """lift.zig's ring_keywords: the one list Haro reads keywords by"""
    src = open(os.path.join(ROOT, 'vm', 'src', 'lift.zig'), encoding='utf-8').read()
    block = src[src.index('pub const ring_keywords'):]
    block = block[:block.index('};')]
    return set(re.findall(r'"([a-z]+)"', block))


# and the three the grammar's scanner reads for a `for` (to, in, step): v0.41's one spelling does not reach them yet (HF-159), so the tool
# writes them lowercase as every other keyword
KW = keywords() | {'to', 'in', 'step'}
SPELL = {k.replace('_', ''): v for k, v in builtin_names.table().items()}
NUM_CALLS = ('len', 'ascii', 'number', 'floor', 'ceil', 'round', 'abs', 'fabs', 'sqrt', 'pow', 'exp', 'log', 'clock', 'random', 'find',
             'max', 'min', 'decimals')
TEXT_CALLS = ('char', 'substr', 'upper', 'lower', 'trim', 'string', 'left', 'right', 'copy', 'hex', 'read', 'date', 'time')


def tokens(src):
    return [[m.lastgroup, m.group()] for m in TOK.finditer(src)]


def sig(toks, i, step):
    j = i + step
    while 0 <= j < len(toks) and toks[j][0] in ('ws', 'cm'):
        j += step
    return j if 0 <= j < len(toks) else None


def is_symbol(toks, i):
    return i > 0 and toks[i - 1][0] == 'op' and toks[i - 1][1] == ':'


def is_member(toks, i):
    j = sig(toks, i, -1)
    return j is not None and toks[j][1] == '.'


def scopes(toks):
    """[(start, end, kind, name, cls)]: the top level, each class body, each function -- a function after `class X` is X's method, as Ring
    reads it, until the next class"""
    marks = [(0, 'top', '@main', None)]
    cls = None
    line_start = True
    for i, (k, v) in enumerate(toks):
        if k == 'nl':
            line_start = True
            continue
        if k in ('ws', 'cm'):
            continue
        if line_start and k == 'id' and v.lower() in ('func', 'def', 'class'):
            j = sig(toks, i, 1)
            nm = toks[j][1] if j is not None else '?'
            if v.lower() == 'class':
                cls = nm
                marks.append((i, 'class', nm, nm))
            else:
                marks.append((i, 'method' if cls else 'func', nm, cls))
        line_start = False
    out = []
    for n, (s, kind, nm, c) in enumerate(marks):
        e = marks[n + 1][0] if n + 1 < len(marks) else len(toks)
        out.append((s, e, kind, nm, c))
    return out


def unwrapped(v):
    return v[1:-1] if len(v) > 2 and v[0] == '_' and v[-1] == '_' and v[1] != '_' and re.fullmatch(r'_[A-Za-z]\w*_', v) else None


def kind_of(rhs):
    r = rhs.strip()
    if not r or r.lower() == 'null':
        return None
    low = r.lower()
    if re.fullmatch(r'-?\d+(\.\d+)?', r) or any(low.startswith(c + '(') for c in NUM_CALLS):
        return 'n'
    if r[0] in '"\'`' or any(low.startswith(c + '(') for c in TEXT_CALLS):
        return 't'
    if r.startswith('['):
        return 'a'
    if low.startswith('new '):
        return 'o'
    return 'x'


def rhs_text(toks, i):
    j = sig(toks, i, 1)
    if j is None or toks[j][1] != '=':
        return None
    k = sig(toks, j, 1)
    if k is not None and toks[k][1] == '=':
        return None
    parts = []
    j += 1
    while j < len(toks) and toks[j][0] != 'nl':
        parts.append(toks[j][1])
        j += 1
    return ''.join(parts).strip()


def letter_word(core):
    """a bare name with no letter: one lowercase word or one lowercase letter"""
    return re.fullmatch(r'[a-z][a-z0-9_]*', core) is not None and not (len(core) >= 2 and core[1].isupper())


def lettered(letter, core):
    return letter + core[0].upper() + core[1:]


def port_file(rel, src, tree_funcs, tree_names, c_map, refused):
    # tree_funcs: lowercase name -> the spellings the tree (or the unit) declares it in, at a file's top level
    """(new text, [renames]) for one file"""
    toks = tokens(src)
    renames = []
    # K: keywords lowered, everywhere in code but a symbol's name
    for i, (k, v) in enumerate(toks):
        if k == 'id' and v.lower() in KW and v != v.lower() and not is_symbol(toks, i):
            toks[i][1] = v.lower()
            renames.append(('K', v, v.lower()))
    # the scopes once, and each class's declared attributes (names assigned in its body) once: asked per method, they made a file
    # of thousands of methods quadratic (stzlib's sweep ran past ten minutes)
    scs = scopes(toks)
    class_attrs = {}
    for s2, e2, k2, n2, c2 in scs:
        if k2 != 'class':
            continue
        found = class_attrs.setdefault(n2, set())
        line_start = True
        for i in range(s2, e2):
            if toks[i][0] == 'nl':
                line_start = True
                continue
            if toks[i][0] in ('ws', 'cm'):
                continue
            if line_start and toks[i][0] == 'id' and rhs_text(toks, i) is not None:
                found.add(toks[i][1])
            line_start = False
    refused_here = set()
    for s, e, kind, nm, cls in scs:
        idents = {toks[i][1] for i in range(s, e) if toks[i][0] == 'id'}
        attrs = class_attrs.get(cls, set()) if kind == 'method' else set()
        # U then L: the declared bare names of a function or a method
        decl = {}
        if kind in ('func', 'method'):
            line_start = True
            first = True
            closed = False  # the header's parameter list ended: a body on the definition's line is no parameter (v0.56, H31)
            for i in range(s, e):
                k, v = toks[i]
                if k == 'nl':
                    line_start = True
                    first = False
                    continue
                if k in ('ws', 'cm'):
                    continue
                if first and k == 'op' and v == ')':
                    closed = True
                if k == 'id':
                    if first and not closed and v.lower() not in KW and v != nm:
                        decl.setdefault(v, set()).add('x')  # a parameter
                    elif line_start and not first:
                        r = rhs_text(toks, i)
                        if r is not None:
                            decl.setdefault(v, set()).add(kind_of(r))
                line_start = False
        plan = {}
        for i in range(s, e):
            k, v = toks[i]
            if k != 'id' or is_member(toks, i) or is_symbol(toks, i) or v in plan:
                continue
            core = unwrapped(v)
            base = core if core else v
            new = None
            if (v in decl or base in decl) and letter_word(base) and v not in attrs and base not in attrs:
                kinds = {x for x in decl.get(v, decl.get(base, set())) if x}
                letter = kinds.pop() if len(kinds) == 1 else 'x'
                new = lettered(letter, base)
            elif core:
                # an unwrapped name takes Softanza's c and v rule as well: _cPath_ -> tPath
                new = core
                if len(core) >= 2 and core[1].isupper() and core[0] in 'cv':
                    new = ('t' if core[0] == 'c' else 'x') + core[1:]
            if new is None or new == v:
                continue
            why = None
            if new.lower() in KW:
                why = 'keyword: `%s` is a keyword' % new.lower()
            elif new in idents:
                why = 'already: `%s` is a name in %s' % (new, nm)
            elif kind == 'method' and (new in attrs or v in attrs):
                why = 'attribute: `%s` is an attribute of class %s' % (v, cls)
            if why:
                refused.append({'file': rel, 'scope': nm, 'old': v, 'new': new, 'why': why})
                refused_here.add((nm, v))
                plan[v] = v
            else:
                plan[v] = new
        if kind == 'method':
            # a method's bare assignment to an attribute: named, never made a local
            line_start = True
            for i in range(s, e):
                k, v = toks[i]
                if k == 'nl':
                    line_start = True
                    continue
                if k in ('ws', 'cm'):
                    continue
                if line_start and k == 'id' and not v.startswith('@') and v in attrs and rhs_text(toks, i) is not None and (nm, v) not in refused_here:
                    refused_here.add((nm, v))
                    refused.append({'file': rel, 'scope': nm, 'old': v, 'new': v,
                                    'why': 'attribute: `%s` is an attribute of class %s, written bare -- write @%s' % (v, cls, v)})
                line_start = False
        for i in range(s, e):
            k, v = toks[i]
            if k != 'id' or is_symbol(toks, i):
                continue
            if not is_member(toks, i) and v in plan and plan[v] != v:
                toks[i][1] = plan[v]
                renames.append(('L' if not unwrapped(v) else 'U', v, plan[v]))
            elif v in c_map:
                toks[i][1] = c_map[v]
                renames.append(('G' if v.startswith('$_') else 'C', v, c_map[v]))
    # B: a built-in called by name, in its one spelling
    for i, (k, v) in enumerate(toks):
        if k != 'id' or v.startswith(('$', '@')) or is_member(toks, i) or is_symbol(toks, i):
            continue
        j = sig(toks, i, 1)
        if j is None or toks[j][1] != '(':
            continue
        if v.lower() in tree_funcs:
            # D: a call to a function the tree declares, as it is declared; two spellings refused
            spellings = tree_funcs[v.lower()]
            if len(spellings) > 1:
                if (rel, v) not in refused_here:
                    refused_here.add((rel, v))
                    refused.append({'file': rel, 'scope': '-', 'old': v, 'new': v,
                                    'why': 'two spellings: the tree declares %s' % ', '.join(sorted(spellings))})
            else:
                want = next(iter(spellings))
                if want != v:
                    toks[i][1] = want
                    renames.append(('D', v, want))
            continue
        want = SPELL.get(v.lower().replace('_', ''))
        if want and want != v:
            toks[i][1] = want
            renames.append(('B', v, want))
    bool_literals(toks, renames)
    toks, pairs = pair_lists(toks)
    renames.extend(('P', ':' + k, '[:' + k + ', ...]') for k in pairs)
    toks = one_form(toks, renames)
    toks = def_ends(toks, renames)
    toks = printing(toks, renames)
    toks = null_free(toks, renames)
    return ''.join(v for _, v in toks), renames


def pair_lists(toks):
    """P (HARO-SURFACE-01): `:key = value` is the pair [:key, value] -- the value read to the comma or the closing bracket at its own depth,
    or the line's end"""
    out = []
    pairs = []
    i = 0
    n = len(toks)
    while i < n:
        k, v = toks[i]
        if k == 'op' and v == ':' and i + 1 < n and toks[i + 1][0] == 'id':
            j = sig(toks, i + 1, 1)
            jn = sig(toks, j, 1) if j is not None else None
            if j is not None and toks[j][1] == '=' and (jn is None or toks[jn][1] != '='):
                # the value: from after `=` to its end at depth 0
                depth = 0
                e = j + 1
                last = None
                while e < n:
                    ke, ve = toks[e]
                    # a line ending in an operator goes on, as Ring reads it: `"a" + "|" +` then the next line
                    if ke == 'nl' and depth == 0 and not (last is not None and (
                            (toks[last][0] == 'op' and toks[last][1] in '+-*/%&|^=<>!') or toks[last][1].lower() in ('and', 'or', 'not'))):
                        break
                    if ke == 'op' and ve in '([{':
                        depth += 1
                    elif ke == 'op' and ve in ')]}':
                        if depth == 0:
                            break
                        depth -= 1
                    elif ke == 'op' and ve == ',' and depth == 0:
                        break
                    if ke not in ('ws', 'cm', 'nl'):
                        last = e
                    e += 1
                if last is not None:
                    pairs.append(toks[i + 1][1])
                    out.append(['op', '['])
                    out.append(toks[i])
                    out.append(toks[i + 1])
                    out.append(['op', ','])
                    # what stood between `=` and the value (its spaces), then the value
                    rest = toks[j + 1:last + 1]
                    while rest and rest[0][0] == 'ws':
                        rest = rest[1:]
                    out.append(['ws', ' '])
                    out.extend(rest)
                    out.append(['op', ']'])
                    i = last + 1
                    continue
        out.append(toks[i])
        i += 1
    return out, pairs


def files_of(root):
    out = []
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(('.ring', '.haro')):
                out.append(os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/'))
    return sorted(out)


def loaded(root, rels, srcs, unit):
    """the files `unit` loads, itself and transitively: a load resolved from the loading file's folder, as Ring resolves it"""
    have = set(rels)
    seen = set()
    todo = [unit]
    while todo:
        r = todo.pop()
        if r in seen or r not in have:
            continue
        seen.add(r)
        for m in re.finditer(r'(?mi)^\ufeff?\s*load\s+["\']([^"\'\n]+)["\']', srcs[r]):
            target = os.path.normpath(os.path.join(os.path.dirname(r), m.group(1))).replace(os.sep, '/')
            todo.append(target)
    return seen


def top_funcs(src):
    """the functions a file declares at its top level, before any class, as written"""
    return [nm for s, e, kind, nm, cls in scopes(tokens(src)) if kind == 'func']


def port_tree(root, unit=None):
    rels = files_of(root)
    srcs = {r: open(os.path.join(root, r), 'rb').read().decode('utf-8', 'surrogateescape').replace('\r\n', '\n') for r in rels}
    # the functions a call can reach: the unit's files when one is named, else the whole tree -- lowercase name -> its spellings
    reach = loaded(root, rels, srcs, unit) if unit else set(rels)
    tree_funcs = {}
    for r in reach:
        for nm in top_funcs(srcs[r]):
            tree_funcs.setdefault(nm.lower(), set()).add(nm)
    tree_names = set()
    for src in srcs.values():
        tree_names |= {v for k, v in tokens(src) if k == 'id'}
    letters = holds(srcs)
    refused = []
    c_map = {}
    for name in sorted(tree_names):
        # G (NEXT-01 (a)): $_name, a library-internal global, is $name
        g = name
        if name.startswith('$_') and len(name) > 2 and name[2] != '_' and not name.endswith('_'):
            g = '$' + name[2:]
            if g in tree_names:
                refused.append({'file': '*', 'scope': 'tree', 'old': name, 'new': g, 'why': 'already: `%s` is a name in the tree' % g})
                continue
        core = g.lstrip('$@')
        pre = g[:len(g) - len(core)]
        r3 = round3(pre, core, letters)
        if r3 and r3 != g:
            if r3.lower() in KW:
                refused.append({'file': '*', 'scope': 'tree', 'old': name, 'new': r3, 'why': 'keyword: `%s` is a keyword' % r3.lower()})
            elif r3 in tree_names:
                refused.append({'file': '*', 'scope': 'tree', 'old': name, 'new': r3, 'why': 'already: `%s` is a name in the tree' % r3})
            else:
                c_map[name] = r3
            continue
        if not (len(core) >= 2 and core[1].isupper() and core[0] in 'cv' and g != 'cCatchError'):
            if g != name:
                c_map[name] = g
            continue
        if True:
            new = pre + ('t' if core[0] == 'c' else 'x') + core[1:]
            if new.lower() in KW:
                refused.append({'file': '*', 'scope': 'tree', 'old': name, 'new': new, 'why': 'keyword: `%s` is a keyword' % new.lower()})
            elif new in tree_names:
                refused.append({'file': '*', 'scope': 'tree', 'old': name, 'new': new, 'why': 'already: `%s` is a name in the tree' % new})
            else:
                c_map[name] = new
    out = {}
    renames = {}
    for r in rels:
        out[r], renames[r] = port_file(r, srcs[r], tree_funcs, tree_names, c_map, refused)
    return rels, out, renames, refused


LIST_LETTER = {'n': 'i', 'c': 't', 'o': 'o', 'a': 'v'}


def holds(srcs):
    """R3 (d): for each name, what every assignment of it gives -- one letter, or None -- and whether it is ever counted (++, +=, -=)"""
    kinds = {}
    counted = set()
    for src in srcs.values():
        toks = tokens(src)
        line_start = True
        for i, (k, v) in enumerate(toks):
            if k == 'nl':
                line_start = True
                continue
            if k in ('ws', 'cm'):
                continue
            if k == 'id':
                j = sig(toks, i, 1)
                if j is not None and toks[j][1] in ('+', '-'):
                    jj = sig(toks, j, 1)
                    if jj is not None and toks[jj][1] in ('+', '-', '='):
                        counted.add(v)
                if line_start:
                    r = rhs_text(toks, i)
                    if r is not None:
                        kinds.setdefault(v, set()).add(literal_kind(r))
            line_start = False
    out = {}
    for name, ks in kinds.items():
        if name in counted:
            out[name] = 'n'
        elif ks == {'01'}:
            out[name] = 'b'
        elif ks <= {'i', '01'}:
            out[name] = 'i'
        elif ks <= {'i', '01', 'd'}:
            out[name] = 'd' if ks == {'d'} else 'n'
        elif len(ks) == 1 and None not in ks:
            out[name] = ks.pop()
        else:
            out[name] = 'x'
    return out


def literal_kind(r):
    r = r.strip()
    if r in ('0', '1'):
        return '01'
    if re.fullmatch(r'-?\d+', r):
        return 'i'
    if re.fullmatch(r'-?\d+\.\d+', r):
        return 'd'
    if r[:1] in ('"', "'", '`'):
        return 't'
    if r.startswith('['):
        return 'v'
    if r.lower().startswith('new '):
        return 'o'
    if r.lower() in ('true', 'false'):
        return 'b'
    return None


def round3(pre, core, letters):
    """the third round's tree-wide name for pre+core, or None (SPELLINGS-02): (a) pc -> pt, pa + element -> pv + element;
    (c) an/ac/ao/aa -> vi/vt/vo/vv; (d) an ALL_CAPS name and an @Capitalised attribute take their letter by what they hold"""
    if re.fullmatch(r'pc[A-Z]\w*', core):
        return pre + 'pt' + core[2:]
    if re.fullmatch(r'pa[ncoa][A-Z]\w*', core):
        return pre + 'pv' + LIST_LETTER[core[2]] + core[3:]
    if re.fullmatch(r'a[ncoa][A-Z]\w*', core):
        return pre + 'v' + LIST_LETTER[core[1]] + core[2:]
    # only a name the tree assigns holds a value: a call written in capitals is no constant
    if re.fullmatch(r'[A-Z][A-Z0-9_]+', core) and (pre + core) in letters:
        return pre + letters[pre + core] + core
    if pre == '@' and re.fullmatch(r'[A-Z][a-z]\w*', core) and (pre + core) in letters:
        return pre + letters[pre + core] + core
    return None


def bool_literals(toks, renames):
    """(b): a b name given 1 or 0 is given true or false; a condition (if, elseif, while) on a 1 or 0 literal is on true or false"""
    for i, (k, v) in enumerate(toks):
        if k != 'num' or v not in ('0', '1'):
            continue
        after = sig(toks, i, 1)
        if after is not None and toks[after][0] != 'nl':
            continue
        before = sig(toks, i, -1)
        if before is None:
            continue
        word = 'true' if v == '1' else 'false'
        if toks[before][0] == 'id' and toks[before][1].lower() in ('if', 'elseif', 'while'):
            toks[i][1] = word
            renames.append(('Y', v, word))
            continue
        if toks[before][1] != '=':
            continue
        name_at = sig(toks, before, -1)
        if name_at is None or toks[name_at][0] != 'id':
            continue
        core = toks[name_at][1].lstrip('$@')
        if core.startswith('p') and len(core) >= 3 and core[2:3].isupper():
            core = core[1:]
        if len(core) >= 2 and core[0] == 'b' and core[1].isupper():
            toks[i][1] = word
            renames.append(('Y', v, word))


ONE_WORD = {'but': 'elseif', 'other': 'else', 'on': 'case', 'foreach': 'for', 'get': 'give', 'break': 'exit',
            'continue': 'loop'}
OPENS = ('if', 'while', 'for', 'foreach', 'switch', 'try', 'do')
CLOSES = ('ok', 'next', 'off', 'done', 'endif', 'endwhile', 'endfor', 'endswitch', 'endtry', 'end')
DEF_ENDS = ('end', 'endfunc', 'endfunction', 'endclass', 'endpackage')


def one_form(toks, renames):
    """O (D67): one form for each construct. A block's end word, or its closing brace, is `end`, and its opening brace goes; a
    definition's end word goes (the line is kept, so every line keeps its number); one word each (ONE_WORD; &&, ||, ! are and, or, not);
    `from` before a class's parent; `#` for a line's comment; `this` for `self` outside a brace object; a definition's parameters in
    parentheses and none without; no period after a call that ends a statement. Blocks are matched lexically: in document order every
    block word opens (if, while, for, switch, try, do, and within/using before a header), every end word or block brace closes, and an end
    word with no block open is a definition's."""
    out = [list(x) for x in toks]
    stack = []          # 'blk', 'brace' (a block opened by `{`), 'do'
    obj = 0             # depth of brace objects, where self is the object
    header = False      # a block word opened on this line, and no brace yet
    line_start = True

    def put(i, new, why='O'):
        if out[i][1] != new:
            renames.append((why, out[i][1], new))
            out[i][1] = new

    i = 0
    while i < len(out):
        k, v = out[i]
        if k == 'nl':
            line_start = True
            header = False
            i += 1
            continue
        if k == 'ws':
            i += 1
            continue
        if k == 'cm':
            if v.startswith('//'):
                put(i, '#' + v[2:])
            i += 1
            continue
        low = v  # exact: a .ring file's keywords are lowered first (K), and in a .haro file `oN` is a name
        word = k == 'id' and not is_member(out, i) and not is_symbol(out, i)
        if word and line_start and low in ('func', 'def', 'function', 'class', 'package'):
            stack = []
            if low != 'package':
                j = sig(out, i, 1)
                # a name that starts with a digit: its digits are a number token, its rest a name (HARO-PORTTOOL-DIGITNAME-01)
                if j is not None and out[j][0] == 'num' and j + 1 < len(out) and out[j + 1][0] == 'id':
                    j += 1
                if j is not None and out[j][0] == 'id':
                    if low == 'class':
                        jj = sig(out, j, 1)
                        if jj is not None and out[jj][1] in (':', '<'):
                            put(jj, 'from')
                            if jj > 0 and out[jj - 1][0] != 'ws':
                                out.insert(jj, ['ws', ' '])
                    else:
                        params(out, j, renames)
            line_start = False
            i += 1
            continue
        if word and low in OPENS:
            stack.append('do' if low == 'do' else 'blk')
            header = low != 'do'
            if low == 'foreach':
                put(i, 'for')
        elif word and low in ('within', 'using') and line_start:
            j = sig(out, i, 1)
            jj = sig(out, j, 1) if j is not None else None
            if j is not None and out[j][0] == 'id' and jj is not None and out[jj][1] == '=':
                stack.append('blk')
        elif word and low == 'again':
            if stack:
                stack.pop()
        elif word and low in CLOSES:
            if stack and stack[-1] == 'blk':
                stack.pop()
                put(i, 'end')
            elif not stack and low in DEF_ENDS:
                put(i, '')
            elif stack:
                stack.pop()
                put(i, 'end')
        elif word and low in DEF_ENDS:
            if not stack:
                put(i, '')
        elif word and low in ONE_WORD:
            put(i, ONE_WORD[low])
        elif word and low == 'self' and obj == 0:
            put(i, 'this')
        elif k == 'op' and v == '{':
            if header:
                stack[-1] = 'brace'
                put(i, '')
                header = False
            else:
                obj += 1
        elif k == 'op' and v == '}':
            if stack and stack[-1] == 'brace' and obj == 0:
                stack.pop()
                put(i, 'end')
            elif obj:
                obj -= 1
        elif k == 'op' and v in ('&', '|') and i + 1 < len(out) and out[i + 1][1] == v:
            put(i, 'and' if v == '&' else 'or')
            out[i + 1][1] = ''
            spaced(out, i)
        elif k == 'op' and v == '!' and not (i + 1 < len(out) and out[i + 1][1] == '='):
            put(i, 'not')
            spaced(out, i)
        elif k == 'op' and v == '.':
            j = sig(out, i, 1)
            b = sig(out, i, -1)
            if (j is None or out[j][0] == 'nl') and b is not None and (out[b][1] == ')' or out[b][0] == 'id'):
                # a dot that ends a line: before a name the chain goes on there, and the dot starts that line (D68,
                # HARO-PORTTOOL-CHAINDOT-01); before anything else it is a call's trailing period, and goes
                n = j
                while n is not None and n < len(out) and out[n][0] in ('nl', 'ws', 'cm'):
                    n += 1
                if n is not None and n < len(out) and out[n][0] == 'id' and out[n][1].lower() not in KW:
                    put(i, '')
                    out[n][1] = '.' + out[n][1]
                    renames.append(('O', 'a dot ending a line', 'a dot starting the next'))
                elif out[b][1] == ')':
                    put(i, '')
        line_start = False
        i += 1
    # a word taken out takes the blank before it when nothing but a blank or the line's end follows
    for i in range(1, len(out)):
        if out[i][1] == '' and out[i][0] != 'nl' and out[i - 1][0] == 'ws':
            j = i + 1
            while j < len(out) and out[j][1] == '' and out[j][0] != 'nl':
                j += 1
            if j == len(out) or out[j][0] in ('nl', 'ws'):
                out[i - 1][1] = ''
    return [x for x in out if x[1] != '' or x[0] == 'nl']


# the words that end a `see`'s expression on its line: the next statement, or the end of the block around it
STMT_WORDS = {'if', 'elseif', 'else', 'end', 'case', 'while', 'for', 'switch', 'try', 'catch', 'finally', 'return', 'see', 'put', 'print',
              'give', 'exit', 'loop', 'func', 'def', 'class', 'ok', 'next', 'off', 'done', 'but', 'other', 'on'}


def printing(toks, renames):
    """O (D69): `see E + nl` and `put E + nl` are `print E`; any other `see E` or `put E` is `FWrite(stdout, E)` -- the expression read to
    the line's end or to the next statement word, outside brackets"""
    out = [list(x) for x in toks]
    i = 0
    while i < len(out):
        k, v = out[i]
        if not (k == 'id' and v in ('see', 'put') and not is_member(out, i) and not is_symbol(out, i)):
            i += 1
            continue
        # the expression: from the next token to the line's end or a statement word at depth 0
        j = i + 1
        depth = 0
        last = None
        while j < len(out):
            kj, vj = out[j]
            if kj == 'nl' or (kj == 'cm' and depth == 0):
                break
            if kj == 'op' and vj in '([{':
                depth += 1
            elif kj == 'op' and vj in ')]}':
                if depth == 0:
                    break   # it closes what holds the statement (a brace object's `}`)
                depth -= 1
            elif kj in ('id', 'op') and depth == 0 and vj.lower() in STMT_WORDS and last is not None:
                # a word rule O wrote over an operator (a block's `}` is `end`) keeps the operator's kind
                break
            if kj != 'ws':
                last = j
            j += 1
        if last is None:
            i += 1
            continue
        # `... + nl` at its end: the line is print's
        a = last
        b = sig(out, a, -1)
        if out[a][0] == 'id' and out[a][1].lower() == 'nl' and b is not None and out[b][1] == '+':
            for x in range(b, a + 1):
                out[x][1] = ''
            # the blank before the `+` goes too
            y = b - 1
            while y > i and out[y][0] == 'ws':
                out[y][1] = ''
                y -= 1
            renames.append(('O', v + ' ... + nl', 'print'))
            out[i][1] = 'print'
        else:
            n = sig(out, i, 1)
            for x in range(i + 1, n):
                out[x][1] = ''
            out[i][1] = 'FWrite(stdout,'
            out[n][1] = ' ' + out[n][1]
            out[last][1] = out[last][1] + ')'
            renames.append(('O', v, 'FWrite(stdout, ...)'))
        i = j
    return [x for x in out if x[1] != '' or x[0] == 'nl']


def null_free(toks, renames):
    """N (D71): `null` is `""`, the value it always was, and `isnull(x)` (respelled IsNull by B) is `IsEmpty(x)`"""
    out = [list(x) for x in toks]
    for i, (k, v) in enumerate(out):
        if k != 'id' or is_member(out, i) or is_symbol(out, i):
            continue
        if v.lower() == 'null':
            out[i] = ['st', '""']
            renames.append(('N', v, '""'))
        elif v.lower() == 'isnull':
            j = sig(out, i, 1)
            if j is not None and out[j][1] == '(':
                out[i][1] = 'IsEmpty'
                renames.append(('N', v, 'IsEmpty'))
    return out


def body_on_own_line(out, j, b, renames):
    """a definition named at out[j] whose header ends at out[b]: a body on the same line goes to a line of its own, one level in"""
    c = sig(out, b, 1)
    if c is None or out[c][0] == 'nl':
        return
    x = j
    while x > 0 and out[x - 1][0] != 'nl':
        x -= 1
    indent = out[x][1] if out[x][0] == 'ws' else ''
    for y in range(b + 1, c):
        out[y][1] = ''
    out[c][1] = '\n' + indent + '\t' + out[c][1]
    renames.append(('O', 'a body on its definition\'s line', 'on its own line'))


DEF_WORDS = ('func', 'def', 'function', 'class', 'package', 'private')


def def_ends(toks, renames):
    """O (D68): every definition ends with `end`; a definition after a class is that class's method, as the classic surface reads it, and is
    written `def`, one before any class `func`. Each `end` goes after the definition's last line of code, at its header's indentation, on
    the blank line that follows when there is one (so the lines after keep their numbers), else on a line of its own."""
    out = [list(x) for x in toks]
    # the lines: [first token, last token] and whether a line holds code
    lines = []
    s = 0
    for i, (k, v) in enumerate(out):
        if k == 'nl':
            lines.append((s, i))
            s = i + 1
    lines.append((s, len(out)))

    def code(ln):
        a, e = lines[ln]
        return any(out[x][0] not in ('ws', 'cm', 'nl') and out[x][1] != '' for x in range(a, e))

    def first(ln):
        a, e = lines[ln]
        for x in range(a, e):
            if out[x][0] not in ('ws',) and out[x][1] != '':
                return x
        return None

    def indent(ln):
        a, e = lines[ln]
        return out[a][1] if a < e and out[a][0] == 'ws' else ''

    heads = []
    for ln in range(len(lines)):
        x = first(ln)
        if x is not None and out[x][0] == 'id' and out[x][1] in DEF_WORDS and not is_member(out, x) and not is_symbol(out, x):
            heads.append((ln, x, out[x][1]))
    if not heads:
        return out
    fills = {}      # line -> text that replaces a blank line
    after = {}      # token index -> text appended after it

    def close(head_ln, upto, ind):
        """close the definition headed at head_ln, whose region ends before line `upto`"""
        last = head_ln
        for ln in range(head_ln, upto):
            if code(ln):
                last = ln
        nxt = last + 1
        while nxt in fills:
            nxt += 1
        if nxt < upto and not code(nxt) and lines[nxt][0] < len(out) and all(out[y][0] in ('ws', 'nl') or out[y][1] == ''
                                                                              for y in range(*lines[nxt])):
            fills[nxt] = ind + 'end'
        else:
            a, e = lines[last]
            tail = e - 1
            while tail > a and out[tail][1] == '':
                tail -= 1
            after[tail] = after.get(tail, '') + '\n' + ind + 'end'
        renames.append(('O', 'a definition', 'ends with end'))

    open_def = None     # (line, indent)
    open_class = None
    open_pkg = None
    for n, (ln, x, w) in enumerate(heads):
        if w in ('func', 'def', 'function'):
            if open_def:
                close(open_def[0], ln, open_def[1])
            want = 'def' if open_class else 'func'
            if w != want:
                renames.append(('O', w, want))
                out[x][1] = want
            open_def = (ln, indent(ln))
        elif w == 'private':
            # the class's private section: the method before it ends there
            if open_def and open_class:
                close(open_def[0], ln, open_def[1])
                open_def = None
        elif w == 'class':
            if open_def:
                close(open_def[0], ln, open_def[1])
                open_def = None
            if open_class:
                close(open_class[0], ln, open_class[1])
            open_class = (ln, indent(ln))
        else:
            for o in (open_def, open_class, open_pkg):
                if o:
                    close(o[0], ln, o[1])
            open_def = open_class = None
            open_pkg = (ln, indent(ln))
    end = len(lines)
    for o in (open_def, open_class, open_pkg):
        if o:
            close(o[0], end, o[1])
    for ln, txt in fills.items():
        a, e = lines[ln]
        ws = [y for y in range(a, e) if out[y][0] == 'ws']
        if ws:
            out[ws[0]][1] = txt
            for y in ws[1:]:
                out[y][1] = ''
        else:
            # an empty line: the end stands after the newline before it
            out[a - 1][1] = out[a - 1][1] + txt
    # each end its own tokens -- a newline, its indentation, the word -- so a later rule reads the token before it unchanged
    res = []
    for x, tok in enumerate(out):
        res.append(tok)
        for part in after.get(x, '').split('\n')[1:]:
            res.append(['nl', '\n'])
            ind = part[:len(part) - len(part.lstrip())]
            if ind:
                res.append(['ws', ind])
            res.append(['id', part.lstrip()])
    return res


def spaced(out, i):
    """a word made of an operator stands apart from its neighbours"""
    if i + 1 < len(out) and out[i + 1][0] not in ('ws', 'nl') and out[i + 1][1] != '':
        out.insert(i + 1, ['ws', ' '])
    elif i + 2 < len(out) and out[i + 1][1] == '' and out[i + 2][0] not in ('ws', 'nl'):
        out.insert(i + 2, ['ws', ' '])
    if i > 0 and out[i - 1][0] not in ('ws', 'nl') and out[i - 1][1] not in ('(', '['):
        out.insert(i, ['ws', ' '])


def params(out, j, renames):
    """a definition named at out[j]: `name()` loses its parentheses, `name a, b` gains them"""
    a = sig(out, j, 1)
    if a is None or out[a][0] == 'nl':
        return
    if out[a][1] == '(':
        b = sig(out, a, 1)
        if b is not None and out[b][1] == ')':
            renames.append(('O', out[j][1] + '()', out[j][1]))
            for x in range(j + 1, b + 1):
                out[x][1] = ''
            body_on_own_line(out, j, b, renames)
        return
    # bare parameters: up to the line's end, before a comment
    end = a
    x = a
    while x < len(out) and out[x][0] != 'nl':
        if out[x][0] not in ('ws', 'cm'):
            end = x
        x += 1
    renames.append(('O', out[j][1] + ' ' + out[a][1], out[j][1] + '(' + out[a][1]))
    out[end][1] = out[end][1] + ')'
    for x in range(j + 1, a):
        out[x][1] = ''
    out[a][1] = '(' + out[a][1]


def haro_name(rel):
    return rel[:-5] + '.haro' if rel.endswith('.ring') else rel


def loads_to_haro(text):
    # a first line may begin with a byte order mark (BOM-01)
    return re.sub(r'(?m)^(\ufeff?\s*load\s+["\'][^"\'\n]*?)\.ring(["\'])', r'\1.haro\2', text)


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ('plan', 'apply'):
        sys.exit(__doc__)
    root = os.path.abspath(a[1])
    unit = a[a.index('--unit') + 1].replace(os.sep, '/') if '--unit' in a else None
    rels, out, renames, refused = port_tree(root, unit)
    counts = {}
    for r in rels:
        for kind, _, _ in renames[r]:
            counts[kind] = counts.get(kind, 0) + 1
    if a[0] == 'plan':
        if '--json' in a:
            print(json.dumps({'files': len(rels), 'counts': counts, 'refused': refused,
                              'renames': {r: [list(x) for x in renames[r]] for r in rels}}, indent=1))
            return 0
        for r in rels:
            if renames[r]:
                print(f'{r}: {len(renames[r])} rewrite(s)')
        for x in refused:
            print(f'REFUSED {x["file"]} {x["scope"]}: {x["old"]} -> {x["new"]} ({x["why"]})')
        print(f'{len(rels)} file(s); rewrites {counts}; {len(refused)} refused')
        return 0
    if '--out' not in a:
        sys.exit('apply needs --out DIR: the ported tree is written beside the original, never over it')
    dst = os.path.abspath(a[a.index('--out') + 1])
    if os.path.exists(dst) and os.listdir(dst):
        sys.exit(f'{dst} is not empty')
    for r in rels:
        p = os.path.join(dst, haro_name(r))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(loads_to_haro(out[r]).encode('utf-8', 'surrogateescape'))
    print(f'{len(rels)} file(s) written to {dst}; rewrites {counts}; {len(refused)} refused')
    return 0


if __name__ == '__main__':
    sys.exit(main())
