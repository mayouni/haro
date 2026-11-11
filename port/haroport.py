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
            for i in range(s, e):
                k, v = toks[i]
                if k == 'nl':
                    line_start = True
                    first = False
                    continue
                if k in ('ws', 'cm'):
                    continue
                if k == 'id':
                    if first and v.lower() not in ('func', 'def') and v != nm:
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
