"""haroport -- a tree of the classic Ring surface ported to .haro, mechanically (HARO-PORTTOOL-01, stzlib-haroport 2026-11-10).

  python port/haroport.py plan  ROOT [--json]       what it would do, file by file; writes nothing
  python port/haroport.py apply ROOT --out DIR      the ported tree in DIR: each .ring file as .haro, each load rewritten to it

THE REWRITES, in this order, each on code only (a string, a comment, a symbol's name are never touched):
  K  a keyword in any case is written in lowercase -- the keywords are vm/src/lift.zig's ring_keywords, read from there
  U  Softanza's method-local spelling _name_ is unwrapped to name
  C  Softanza's c (text) is t and its v (any value) is x: cName -> tName, $cX -> $tX, @cX -> @tX -- one decision for the whole tree
  L  a bare name declared in a function (assigned, a parameter) is lettered by what it holds: n a number, t a text, a a list, o an object,
     x anything else or two kinds -- never at the top level or in a class body, never a name the class declares as an attribute
  B  a built-in called by name is written in its one spelling (study/v48/builtin_names.py), unless the tree defines a function of that name
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
                new = core
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
                if line_start and k == 'id' and v in attrs and rhs_text(toks, i) is not None and (nm, v) not in refused_here:
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
                renames.append(('C', v, c_map[v]))
    # B: a built-in called by name, in its one spelling
    for i, (k, v) in enumerate(toks):
        if k != 'id' or v.startswith(('$', '@')) or is_member(toks, i) or is_symbol(toks, i):
            continue
        j = sig(toks, i, 1)
        if j is None or toks[j][1] != '(' or v.lower() in tree_funcs:
            continue
        want = SPELL.get(v.lower().replace('_', ''))
        if want and want != v:
            toks[i][1] = want
            renames.append(('B', v, want))
    return ''.join(v for _, v in toks), renames


def files_of(root):
    out = []
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(('.ring', '.haro')):
                out.append(os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/'))
    return sorted(out)


def port_tree(root):
    rels = files_of(root)
    srcs = {r: open(os.path.join(root, r), 'rb').read().decode('utf-8', 'surrogateescape').replace('\r\n', '\n') for r in rels}
    tree_funcs = set()
    tree_names = set()
    for src in srcs.values():
        tree_funcs |= {m.group(1).lower() for m in re.finditer(r'(?mi)^\s*(?:func|def)\s+(\w+)', src)}
        tree_names |= {v for k, v in tokens(src) if k == 'id'}
    refused = []
    c_map = {}
    for name in sorted(tree_names):
        core = name.lstrip('$@')
        pre = name[:len(name) - len(core)]
        if len(core) >= 2 and core[1].isupper() and core[0] in 'cv' and name != 'cCatchError':
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


def haro_name(rel):
    return rel[:-5] + '.haro' if rel.endswith('.ring') else rel


def loads_to_haro(text):
    return re.sub(r'(?m)^(\s*load\s+["\'][^"\'\n]*?)\.ring(["\'])', r'\1.haro\2', text)


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ('plan', 'apply'):
        sys.exit(__doc__)
    root = os.path.abspath(a[1])
    rels, out, renames, refused = port_tree(root)
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
