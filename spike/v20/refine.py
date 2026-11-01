"""refine.py -- refinement over the program graph of rung 18 (Haro v0.20, the twentieth rung).

    text --l1--> graph (rung 18) --ids--> graph with ids (rung 19)
         --lift--> the refinement points the program declares (a `<R:KIND ...>` tag in a comment: the lift for foreign code, charter 6.1)
    a SENTENCE (rfn's shape: TARGET KIND FROM TO AUTHOR POSTURE REASON, and the optional AT CASCADE REVERTS)
         --gate--> structural, constraint, governance, trust, derivation (stzRefinableCode's order); the first stage to fail ends it
         --lower--> a transaction of RCP's twelve primitives over the graph, each with the inverse captured BEFORE it lands
         --apply--> a new graph, whose canonical text is the new program; the diff is the printer's: print(old) against print(new)

The agent never edits text: its only write surface is a sentence against a point, and the only way a sentence changes a program is through
the gate. A refinement answers for the rules of the point it touched -- its own bounds and options, and every RULE that names it -- and for
nothing else, so a program a text edit left inconsistent can be repaired by a refinement, and refined elsewhere meanwhile. A human edit made as TEXT is read back (`audit`) as the refinements it amounts to and judged by the same gate.

    Model(text, ctx, unit)     a program, its ids, its event log; `unit` names the program that loads it, for a library (D32)
    Model.refine(sentence)     one proposal through the gate; the outcome is also an event in the log
    Model.edit(text)           a human edit as text: ids carried by rung 19's matcher, an event in the log
    Model.revert(n, ...)       a refinement with REVERTS n, which is how a revert is written: its own event, gated like any other
    lift(g)                    the points, the rules and the faults of a graph
    apply_tx(g, tx)            atomic: all the primitives or none; -> (new graph, the inverse transaction)
    audit(model, text, ...)    what a text edit amounts to, each refinement judged
    replay(text, log, ctx)     the log run again from the base text: the same verdicts, the same final text
    commutes(model, s1, s2)    RCP's predicate over the two sentences' footprints
The ten pieces of the model that are not in the graph (governance tables, the posture ranks) are CONTEXT, passed in; what is in the text is the
point, its bounds, its options, its risk tier, its trust floor and the governance it is under -- all of it refinable, and all of it versioned.
"""
import copy, difflib, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v18'))
sys.path.insert(0, os.path.join(HERE, '..', 'v19'))
import l1, ids

SCRATCH = os.path.join(HERE, 'scratch')

POSTURES = {'trusted': 3, 'external': 2, 'sandboxed': 1, 'llm': 0}          # StzRefinableCodeQ()._PostureRank
LEVELS = {'advisory': 1, 'delegated': 2, 'autonomous': 3, 'emergencyoverride': 4}   # StzGovernanceQ()._AuthLevel
KINDS = ('param', 'algo', 'pipeline', 'rule', 'lib', 'block', 'function', 'method', 'type', 'custom')
BUILT = ('param', 'algo', 'pipeline', 'block', 'function', 'method')  # the kinds this rung builds; the others are declared and refused when proposed against
RULE_ATTRS = ('min', 'max', 'options', 'risk', 'floor', 'governed_by', 'calls', 'writes', 'reads')   # calls, writes, reads: a body point's allowlists
BLOCK_ATTRS = ('calls', 'writes', 'reads', 'risk', 'floor', 'governed_by')   # what a BLOCK point declares besides its name
FUNCTION_ATTRS = ('params',) + BLOCK_ATTRS                         # and a FUNCTION point: the signature is declared too
BODY_KINDS = ('block', 'function', 'method')    # the kinds whose value is a function's body
DECLARING = ('function', 'method')              # ...and those that DECLARE the function, which may not be there yet
MUTATORS = ('add', 'insert', 'del', 'swap')     # the builtins that write into their first argument
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
STAGES = ('structural', 'constraint', 'governance', 'trust', 'derivation')
RULE_FLOOR = 'trusted'                          # the posture a refinement of a point's own RULES must come from, whatever the point's floor says
WIDEN_TIER = 4                                  # widening a rule is the heaviest act there is
SEATS = ('TARGET', 'KIND', 'FROM', 'TO', 'AUTHOR', 'POSTURE', 'REASON', 'AT', 'CASCADE', 'REVERTS')
REQUIRED = ('TARGET', 'KIND', 'FROM', 'TO', 'AUTHOR', 'POSTURE', 'REASON')
NUM_RE = re.compile(r'^-?[0-9]+(\.[0-9]+)?$')
IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
NAME_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_-]*$')

# switches the controls of the court turn (a gate that skips a stage, an apply that edits in place), never the real thing
SKIP_STAGES = set()
INPLACE = False


class TxError(Exception):
    pass


class Unreadable(Exception):
    pass


# ---- text and graph -------------------------------------------------------------------------------------------------------------------

_n = [0]
_READ = {}


def parse_text(text):
    """Ring text (latin-1: one char a byte) to its graph, through the compiler's own parser. Raises Unreadable."""
    key = hashlib.sha256(text.encode('latin-1')).hexdigest()
    if key in _READ:
        return copy.deepcopy(_READ[key])
    os.makedirs(SCRATCH, exist_ok=True)
    _n[0] += 1
    p = os.path.join(SCRATCH, 'r%d_%d.ring' % (os.getpid(), _n[0]))
    open(p, 'wb').write(text.encode('latin-1'))
    try:
        g, why = l1.parse_ring(p)
    finally:
        try:
            os.remove(p)
        except OSError:
            pass
    if g is None:
        raise Unreadable(why)
    _READ[key] = copy.deepcopy(g)
    return g


def new_graph(text):
    g = parse_text(text)
    ids.number(g)
    return g


def text_of(g):
    return l1.print_ring(g)


def digest(text):
    return hashlib.sha256(text.encode('latin-1')).hexdigest()[:16]


def get_path(node, path):
    for p in path:
        node = node[p]
    return node


def walk_items(g):
    """Every item with where it stands: (item, parent item or None, path of its block inside the parent, its list, its index, owner)."""
    out = []

    def go(lst, parent, bpath, owner, in_class):
        for i, it in enumerate(lst):
            out.append((it, parent, bpath, lst, i, owner))
            o2, c2 = owner, in_class
            k = it['k']
            if k == 'class':
                o2, c2 = ids.def_name(it), True
            elif k == 'func':
                o2 = (owner + '.' + ids.def_name(it)) if in_class else ids.def_name(it)
            for path, b in ids.blocks(it):
                go(b, it, path, o2, c2)
    go(g['items'], None, ('items',), '<top>', False)
    return out


def find_item(g, ident):
    for it, parent, bpath, lst, i, owner in walk_items(g):
        if it.get('_id') == ident:
            return it, parent, bpath, lst, i
    raise TxError('no item %s' % ident)


# ---- tags ---------------------------------------------------------------------------------------------------------------------------

_KIND_RE = re.compile(r'<R:([A-Za-z]+)')
_ATTR_RE = re.compile(r'(\s+)([A-Za-z_][A-Za-z0-9_]*)="([^"]*)"')
_CLOSE_RE = re.compile(r'\s*>')


def parse_tag(text):
    """The first `<R:KIND key="value" ...>` in a comment: None when there is none, an error string when it is malformed, else a dict with the
    spans of every attribute, so an edit changes those bytes and no others."""
    i = text.find('<R:')
    if i < 0:
        return None
    m = _KIND_RE.match(text, i)
    if not m:
        return 'malformed tag: no kind'
    pos, attrs, seen = m.end(), [], set()
    while True:
        m2 = _ATTR_RE.match(text, pos)
        if not m2:
            break
        key = m2.group(2)
        if key != key.lower():
            return "malformed tag: key '%s' -- a key is written in lower case" % key
        if key in seen:
            return 'malformed tag: attribute %s twice' % key
        seen.add(key)
        attrs.append({'key': key, 'val': m2.group(3), 'start': m2.start(), 'end': m2.end(), 'vstart': m2.start(3), 'vend': m2.end(3)})
        pos = m2.end()
    if not _CLOSE_RE.match(text, pos):
        return 'malformed tag: not closed'
    if m.group(1) != m.group(1).upper():
        return "malformed tag: kind '%s' -- a kind is written in upper case" % m.group(1)
    return {'kind': m.group(1).lower(), 'attrs': attrs, 'attrs_end': pos}


def tag_get(text, key):
    t = parse_tag(text)
    if not isinstance(t, dict):
        return None
    for a in t['attrs']:
        if a['key'] == key:
            return a['val']
    return None


def tag_set(text, key, val):
    """The comment with `key` set to `val`: in place when it is there, before the closing `>` when it is not."""
    t = parse_tag(text)
    for a in t['attrs']:
        if a['key'] == key:
            return text[:a['vstart']] + val + text[a['vend']:]
    return text[:t['attrs_end']] + ' %s="%s"' % (key, val) + text[t['attrs_end']:]


def tag_del(text, key):
    t = parse_tag(text)
    for a in t['attrs']:
        if a['key'] == key:
            return text[:a['start']] + text[a['end']:]
    return text


def tag_index(text, key):
    t = parse_tag(text)
    for n, a in enumerate(t['attrs']):
        if a['key'] == key:
            return n
    return None


def tag_insert(text, key, val, index):
    """`key="val"` placed as the index-th attribute (the end when index is None or too large): what a delete's inverse needs to restore the bytes."""
    t = parse_tag(text)
    attrs = t['attrs']
    if index is None or index >= len(attrs):
        return text[:t['attrs_end']] + ' %s="%s"' % (key, val) + text[t['attrs_end']:]
    at = attrs[index]['start']
    return text[:at] + ' %s="%s"' % (key, val) + text[at:]


# ---- literals ---------------------------------------------------------------------------------------------------------------------------

def to_literal(value):
    """The text of a Ring string holding `value`, or None. Ring has no string escapes (F-55), so the quote must be one the value does not hold."""
    if '\n' in value or '\r' in value:
        return None
    for q in ('"', "'", '`'):
        if q not in value:
            return q + value + q
    return None


def unquote(lit):
    return lit[1:-1]


def literal_node(text):
    """A literal's text -- a number, a signed number or a quoted string -- as a graph node."""
    if text[:1] in ('"', "'", '`'):
        return {'k': 'str', 'text': text}
    if text.startswith('-'):
        return {'k': 'un', 'op': '-', 'e': {'k': 'num', 'text': text[1:]}}
    return {'k': 'num', 'text': text}


def literal_text(node):
    if node['k'] == 'num':
        return node['text']
    if node['k'] == 'un' and node.get('op') == '-' and node['e']['k'] == 'num':
        return '-' + node['e']['text']
    if node['k'] == 'str':
        return node['text']
    return None


def num(s):
    return float(s)


# ---- the lift -----------------------------------------------------------------------------------------------------------------------------

def resolve_target(kind, it):
    """What a point of this kind is attached to inside the statement it stands on: (form, path, value) or an error text."""
    k = it['k']
    if kind == 'lib':
        if k == 'load' and it.get('path') and it['path']['k'] == 'str':
            return 'load', ['path'], unquote(it['path']['text'])
        return 'the statement is not a load'
    if kind == 'pipeline':
        if k == 'expr' and it['e']['k'] == 'assign' and it['e'].get('op') == '=' and it['e']['r']['k'] == 'list':
            lst = it['e']['r']
            if all(x['k'] == 'str' for x in lst.get('items', [])):
                return 'list', ['e', 'r'], '|'.join(unquote(x['text']) for x in lst.get('items', []))
            return 'a stage of the list is not a string literal'
        return 'is not a list of string literals'
    if kind in ('param', 'algo'):
        if k == 'expr' and it['e']['k'] == 'assign' and it['e'].get('op') == '=':
            r = it['e']['r']
            lt = literal_text(r)
            if lt is not None:
                if r['k'] == 'str':
                    return 'str', ['e', 'r'], unquote(lt)
                if kind == 'param':
                    return ('neg' if lt.startswith('-') else 'num'), ['e', 'r'], lt
            if kind == 'algo' and r['k'] == 'call' and r['callee']['k'] == 'id':
                return 'call', ['e', 'r'], r['callee']['text']
        if kind == 'algo' and k == 'expr' and it['e']['k'] == 'call' and it['e']['callee']['k'] == 'id':
            return 'call', ['e'], it['e']['callee']['text']
        return 'target is not a literal' if kind == 'param' else 'target is neither a string literal nor a call'
    if kind == 'block':
        if k == 'func':
            return 'block', ['items'], block_digest(body_text(it.get('items', [])))
        return 'is not on a function'
    return 'kind is not built'


def own_rule_error(p):
    """Does the point's value satisfy the point's own rules? None, or what is wrong."""
    v, a = p['value'], p['attrs']
    if p['kind'] == 'param' and p['form'] in ('num', 'neg'):
        if any(k in a and not NUM_RE.match(a[k]) for k in ('min', 'max')):
            return None             # reported on its own: the bounds are not numbers
        if 'min' in a and num(v) < num(a['min']):
            return "point '%s' value %s is below its own min %s" % (p['name'], v, a['min'])
        if 'max' in a and num(v) > num(a['max']):
            return "point '%s' value %s is above its own max %s" % (p['name'], v, a['max'])
    if p['kind'] == 'algo' and 'options' in a:
        if v not in a['options'].split('|'):
            return "point '%s' value '%s' is not in its own options %s" % (p['name'], v, a['options'])
    if p['kind'] == 'pipeline':
        stages = v.split('|') if v else []
        opts = a.get('options', '').split('|')
        for s in stages:
            if s not in opts:
                return "point '%s' stage '%s' is not in its own options %s" % (p['name'], s, a['options'])
        for s in set(stages):
            if stages.count(s) > 1:
                return "point '%s' stage '%s' appears twice" % (p['name'], s)
    return None


def lift(g):
    """The refinement points a program declares: {'points': [...], 'rules': [...], 'errors': [...]}. A fault is an error. A declaration that cannot be read
    (a tag with no name, a duplicate, an orphan, a rule over an unknown point) stops the gate: it fails closed. An error flagged `own` -- a value outside
    its own bounds or options -- is a state, not a fault, and does not."""
    points, rules, errors = [], [], []
    by_item = {}

    def err(msg, own=False):
        errors.append({'msg': msg, 'own': own})

    def carriers():
        for it, parent, bpath, lst, i, owner in walk_items(g):
            if it['k'] == 'comment':
                if it.get('kind') == 'tag':
                    yield it, {'id': it['_id'], 'path': []}, it['text'], lst, i, parent
            elif it.get('trail') and it['trail'].get('kind') == 'tag':
                yield it, {'id': it['_id'], 'path': ['trail']}, it['trail']['text'], None, None, parent

    for holder, carrier, text, lst, i, parent in carriers():
        t = parse_tag(text)
        if isinstance(t, str):
            err(t)
            continue
        kind = t['kind']
        attrs = {a['key']: a['val'] for a in t['attrs']}
        if kind not in KINDS:
            err("unknown kind '%s'" % kind)
            continue
        name = attrs.get('name')
        if not name or not NAME_RE.match(name):
            err('malformed tag: no name' if not name else "malformed tag: name '%s'" % name)
            continue
        if kind == 'rule':
            if 'expr' not in attrs:
                err("rule '%s' has no expr" % name)
                continue
            rules.append({'name': name, 'expr': attrs['expr'], 'message': attrs.get('message', ''), 'carrier': carrier})
            continue
        if kind in DECLARING:
            # a FUNCTION or METHOD point is attached to nothing: it DECLARES a function, which may not be there yet, so it is carried by its own comment
            faults, fatal, existing = function_faults(g, name, kind, t['attrs'], lst, parent)
            for f in faults:
                err(f)
            if fatal:
                continue
            points.append({'name': name, 'kind': kind, 'id': carrier['id'], 'carrier': carrier,
                           'attrs': {k: v for k, v in attrs.items() if k != 'name'}, 'order': [a['key'] for a in t['attrs'] if a['key'] != 'name'],
                           'form': kind, 'path': [],
                           'value': block_digest(body_text(existing.get('items', []))) if existing is not None else 'absent', 'built': True})
            continue
        # the statement a point is attached to
        if lst is None:
            target = holder
        else:
            j = i + 1
            while j < len(lst) and lst[j]['k'] == 'comment':
                j += 1
            if j >= len(lst):
                err("orphan tag '%s'" % name)
                continue
            target = lst[j]
        r = resolve_target(kind, target)
        if isinstance(r, str):
            if kind in BUILT or kind == 'lib':
                err("point '%s' %s" % (name, r))
                continue
            form, path, value = kind, [], ''
        else:
            form, path, value = r
        pt = {'name': name, 'kind': kind, 'id': target['_id'], 'carrier': carrier, 'attrs': {k: v for k, v in attrs.items() if k != 'name'},
              'order': [a['key'] for a in t['attrs'] if a['key'] != 'name'], 'form': form, 'path': path, 'value': value, 'built': kind in BUILT}
        points.append(pt)

    seen, folded = {}, {}
    for p in points:
        if p['name'] in seen:
            err("duplicate point '%s'" % p['name'])
        elif p['name'].lower() in folded:
            err("look-alike points '%s' and '%s': names differ only in case" % (folded[p['name'].lower()], p['name']))
        seen[p['name']] = p
        folded.setdefault(p['name'].lower(), p['name'])
    per = {}
    for p in points:
        per.setdefault(p['id'], []).append(p)
    for ident, ps in per.items():
        if len(ps) > 1:
            err('statement @%d carries %d points' % (ident, len(ps)))
    for p in points:
        a = p['attrs']
        if p['kind'] in ('algo', 'pipeline') and not a.get('options'):
            err("point '%s' needs options" % p['name'])
        for key in ('min', 'max'):
            if key in a:
                if p['kind'] != 'param' or p['form'] not in ('num', 'neg'):
                    err("point '%s' bounds apply to numeric points only" % p['name'])
                    break
                if not NUM_RE.match(a[key]):
                    err("point '%s' %s '%s' is not a number" % (p['name'], key, a[key]))
        if 'min' in a and 'max' in a and NUM_RE.match(a['min']) and NUM_RE.match(a['max']) and num(a['min']) > num(a['max']):
            err("point '%s' min %s is above its max %s" % (p['name'], a['min'], a['max']))
        if 'risk' in a and a['risk'] not in ('1', '2', '3', '4'):
            err("point '%s' risk '%s' is not a tier from 1 to 4" % (p['name'], a['risk']))
        if 'floor' in a and a['floor'] not in POSTURES:
            err("point '%s' floor '%s' is not a posture" % (p['name'], a['floor']))
        if p['kind'] in BODY_KINDS:
            for e in block_decl_errors(g, p):
                err(e)
            why = body_own_error(g, p)
            if why:
                err("point '%s' body is outside its own rule: %s" % (p['name'], why), own=True)
        if p['built']:
            e = own_rule_error(p)
            if e and not any(x['msg'].startswith("point '%s' bounds" % p['name']) for x in errors):
                err(e, own=True)
    names = {p['name']: p for p in points}
    for r in rules:
        parts = r['expr'].split()
        if len(parts) != 3 or parts[1] not in ('>=', '<=', '!=', '>', '<', '='):
            err("rule '%s' expr '%s' is not <operand> <op> <operand>" % (r['name'], r['expr']))
            continue
        r['left'], r['op'], r['right'] = parts
        for side in (parts[0], parts[2]):
            if NUM_RE.match(side):
                continue
            q = names.get(side)
            if q is None:
                err("rule '%s' names unknown point '%s'%s" % (r['name'], side, near(names, side)))
            elif r['op'] != '=' and r['op'] != '!=' and not (q['kind'] == 'param' and q['form'] in ('num', 'neg')):
                err("rule '%s' orders the non-numeric point '%s'" % (r['name'], side))
    return {'points': points, 'rules': rules, 'errors': errors}


def same_value(p, a, b):
    """Two spellings of a point's value: numbers by value, a callee by Ring's case-folded name, everything else exactly."""
    if p['form'] in ('num', 'neg') and NUM_RE.match(a) and NUM_RE.match(b):
        return num(a) == num(b)
    return a == b


def point_named(L, name):
    for p in L['points']:
        if p['name'] == name:
            return p
    return None


def near(names, name):
    """The hint a refusal of a name gives when the name is a declared one in another case: names are exact (D24), and saying which was meant is cheap."""
    hit = [n for n in names if n.lower() == name.lower() and n != name]
    return " (names are exact: '%s' is declared)" % hit[0] if hit else ''


def show_lift(L):
    """The lift as the lines the fixtures spell it in."""
    out = []
    for p in L['points']:
        extra = ''.join(' %s=%s' % (k, p['attrs'][k]) for k in p['order'])
        out.append('%s %s @%d = %s%s' % (p['name'], p['kind'], p['id'], p['value'], extra))
    for r in L['rules']:
        out.append('rule %s "%s" -- %s' % (r['name'], r['expr'], r['message']))
    for e in L['errors']:
        out.append('error ' + e['msg'])
    return out


# ---- the sentence -----------------------------------------------------------------------------------------------------------------

class Bad(Exception):
    pass


def _scan_string(s, i):
    q = s[i]
    j = s.find(q, i + 1)
    if j < 0:
        raise Bad('a string is not closed')
    return s[i + 1:j], j + 1


def parse_sentence(text):
    """`DEFINE REFINE id AS ( SEAT value, ... ) [RATIONALE "..."]` -> (dict of its seats, None), or (None, why) for a sentence that is not one."""
    try:
        s = text.strip()
        m = re.match(r'DEFINE\s+REFINE\s+([A-Za-z_][A-Za-z0-9_-]*)\s+AS\s*\(', s)
        if not m:
            raise Bad('not a DEFINE REFINE sentence')
        i = m.end()
        seats = {}
        while True:
            while i < len(s) and s[i].isspace():
                i += 1
            if i < len(s) and s[i] == ')':
                i += 1
                break
            m2 = re.match(r'([A-Z]+)\s*', s[i:])
            if not m2:
                raise Bad('a seat name was expected')
            name = m2.group(1)
            if name not in SEATS:
                raise Bad('unknown seat %s' % name)
            if name in seats:
                raise Bad('seat %s twice' % name)
            i += m2.end()
            if i >= len(s):
                raise Bad('the sentence ends inside its seats')
            if s[i] in ('"', "'", '`'):
                val, i = _scan_string(s, i)
            else:
                m3 = re.match(r'[A-Za-z0-9_.-]+', s[i:])
                if not m3:
                    raise Bad('seat %s has no value' % name)
                val, i = m3.group(0), i + m3.end()
            seats[name] = val
            while i < len(s) and s[i].isspace():
                i += 1
            if i < len(s) and s[i] == ',':
                i += 1
        rest = s[i:].strip()
        if rest:
            m4 = re.match(r'RATIONALE\s+', rest)
            if not m4 or rest[m4.end():m4.end() + 1] not in ('"', "'", '`'):
                raise Bad('only a RATIONALE may follow the seats')
            _, j = _scan_string(rest, m4.end())
            if rest[j:].strip():
                raise Bad('text after the RATIONALE')
        for r in REQUIRED:
            if r not in seats:
                raise Bad('missing seat %s' % r)
        for r in ('TARGET', 'AUTHOR', 'REASON'):
            if not seats[r].strip():
                raise Bad('seat %s is empty' % r)
        if seats['KIND'] not in KINDS:
            raise Bad("unknown kind '%s'" % seats['KIND'])
        if seats['POSTURE'] not in POSTURES:
            raise Bad("unknown posture '%s'" % seats['POSTURE'])
        for key in ('AT', 'REVERTS'):
            if key in seats and not re.match(r'^[0-9]+$', seats[key]):
                raise Bad('seat %s is not an id' % key)
        if 'CASCADE' in seats and seats['CASCADE'].strip() and not re.match(r'^[0-9]+(\s*,\s*[0-9]+)*$', seats['CASCADE'].strip()):
            raise Bad('seat CASCADE is not a list of ids')
    except Bad as e:
        return None, 'malformed sentence: %s' % e
    out = {'id': m.group(1), 'target': seats['TARGET'], 'kind': seats['KIND'], 'from': seats['FROM'], 'to': seats['TO'], 'author': seats['AUTHOR'],
           'posture': seats['POSTURE'], 'reason': seats['REASON'], 'text': text.strip()}
    if 'AT' in seats:
        out['at'] = int(seats['AT'])
    if 'REVERTS' in seats:
        out['reverts'] = int(seats['REVERTS'])
    if 'CASCADE' in seats:
        out['cascade'] = [int(x) for x in seats['CASCADE'].replace(' ', '').split(',') if x]
    base, _, attr = out['target'].partition('.')
    out['base'], out['attr'] = base, (attr or None)
    return out, None


def quote_seat(v):
    for q in ('"', "'", '`'):
        if q not in v:
            return q + v + q
    raise Bad('a seat value holds all three quotes')


def sentence_text(sid, target, kind, frm, to, author, posture, reason, at=None, cascade=None, reverts=None):
    seats = ['TARGET %s' % quote_seat(target), 'KIND %s' % kind, 'FROM %s' % quote_seat(frm), 'TO %s' % quote_seat(to),
             'AUTHOR %s' % quote_seat(author), 'POSTURE %s' % posture, 'REASON %s' % quote_seat(reason)]
    if at is not None:
        seats.append('AT %s' % quote_seat(str(at)))
    if cascade is not None:
        seats.append('CASCADE %s' % quote_seat(','.join(str(c) for c in cascade)))
    if reverts is not None:
        seats.append('REVERTS %s' % quote_seat(str(reverts)))
    return 'DEFINE REFINE %s AS ( %s )' % (sid, ', '.join(seats))


def parse_context(text):
    """The governance tables: `governance NAME` and, one tab in, `actor NAME LEVEL may POINT ...`. -> {governance: {actor: {'level', 'name', 'may'}}}"""
    ctx, cur = {}, None
    for line in text.replace('\r\n', '\n').split('\n'):
        if not line.strip():
            continue
        if not line.startswith(('\t', ' ')):
            parts = line.split()
            if len(parts) != 2 or parts[0] != 'governance':
                raise ValueError('context line: ' + line)
            cur = ctx.setdefault(parts[1], {})
        else:
            parts = line.split()
            if len(parts) < 4 or parts[0] != 'actor' or parts[3] != 'may' or parts[2] not in LEVELS or cur is None:
                raise ValueError('context line: ' + line)
            cur[parts[1]] = {'level': LEVELS[parts[2]], 'name': parts[2], 'may': set(parts[4:])}
    return ctx


# ---- the cascade --------------------------------------------------------------------------------------------------------------------

def _expr_ids(node, out):
    """Every identifier an item's own expressions name, its nested blocks and its trailing comment left out (they are items, or text)."""
    if isinstance(node, dict):
        if node.get('k') == 'id':
            out.append(node['text'].lower())
        for f, v in node.items():
            if f == 'trail' or f.startswith('_') or ids.is_block(node, f, v):
                continue
            if isinstance(v, (dict, list)):
                _expr_ids(v, out)
    elif isinstance(node, list):
        for x in node:
            _expr_ids(x, out)


def cascade(g, p):
    """What a change to a point's literal touches: the statements that read the name, and the other places that write it. The scan is by Ring's
    case-folded name and sees the whole file, so it is an over-approximation across scopes, and says so by the owner it prints."""
    items = walk_items(g)
    tgt = next(it for it, *_ in items if it['_id'] == p['id'])
    e = tgt.get('e') if tgt['k'] == 'expr' else None
    if not e or e['k'] != 'assign' or e['l']['k'] != 'id':
        return {'reads': [], 'writes': []}
    name = e['l']['text'].lower()
    reads, writes = [], []
    for it, parent, bpath, lst, i, owner in items:
        if it['_id'] == p['id']:
            continue
        used, wrote, k = [], False, it['k']
        x = it.get('e') if k == 'expr' else None
        if x is not None and x['k'] == 'assign' and x['l']['k'] == 'id' and x['l']['text'].lower() == name:
            wrote = True
            _expr_ids(x['r'], used)
            if x.get('op') != '=':
                used.append(name)
        elif x is not None and x['k'] == 'post' and x['e']['k'] == 'id' and x['e']['text'].lower() == name:
            wrote = True
            used.append(name)
        else:
            _expr_ids({f: v for f, v in it.items() if f != 'trail' and not f.startswith('_')}, used)
            if k == 'for' and str(it.get('var', '')).lower() == name:
                wrote = True
        if name in used:
            reads.append((it['_id'], owner))
        if wrote:
            writes.append((it['_id'], owner))
    return {'reads': reads, 'writes': writes}


# ---- the primitives -----------------------------------------------------------------------------------------------------------------

def _point(work, name):
    L = lift(work)
    p = point_named(L, name)
    if p is None:
        raise TxError("no refinement point '%s'" % name)
    return p


def _comment_node(work, p):
    it = find_item(work, p['carrier']['id'])[0]
    return get_path(it, p['carrier']['path'])


def _block_list(work, parent, block):
    if parent is None:
        holder, path = work, ['items']
    else:
        holder = find_item(work, parent)[0]
        path = [block] if isinstance(block, str) else list(block)
    h = get_path(holder, path[:-1])
    if path[-1] not in h and path[-1] in l1.FIELDS.get(h.get('k'), ()):
        h[path[-1]] = []        # an empty body has no list in the graph until something goes in it (a function declared, its body to come)
    return h[path[-1]]


def _renumber(work, node):
    """Fresh ids for the items of a node that holds none; the ones it holds are kept (a delete's inverse restores them)."""
    seen = set(it['_id'] for it, *_ in walk_items(work) if '_id' in it)
    tmp = {'k': 'file', 'items': [node]}
    for it in ids.preorder(tmp):
        if '_id' in it:
            if it['_id'] in seen:
                raise TxError('id %s is already in use' % it['_id'])
        else:
            it['_id'] = work['_next']
            work['_next'] += 1


def apply_prim(work, p):
    """One RCP primitive on `work`, in place; -> the inverse primitive, captured before the change landed."""
    op = p['op']
    if op == 'node.update_property':
        it = find_item(work, p['target']['id'])[0]
        node = get_path(it, p['target']['path'])
        prop = p['prop']
        if prop not in node:
            raise TxError('the node has no property %s' % prop)
        old = node[prop]
        if 'expect' in p and old != p['expect']:
            raise TxError('conflict: the property is now %r, the change this undoes left it at %r' % (old, p['expect']))
        node[prop] = p['value']
        return {'op': op, 'target': p['target'], 'prop': prop, 'value': old, 'expect': p['value']}
    if op == 'node.create':
        lst = _block_list(work, p['parent'], p['block'])
        node = copy.deepcopy(p['node'])
        _renumber(work, node)
        idx = p['index'] if p.get('index') is not None else len(lst)
        if idx < 0 or idx > len(lst):
            raise TxError('index %s is outside the block' % idx)
        lst.insert(idx, node)
        return {'op': 'node.delete', 'id': node['_id']}
    if op == 'node.delete':
        it, parent, bpath, lst, i = find_item(work, p['id'])
        lst.pop(i)
        return {'op': 'node.create', 'parent': parent['_id'] if parent else None, 'block': list(bpath) if parent else 'items', 'index': i, 'node': it}
    if op in ('edge.create', 'edge.delete', 'edge.retarget') and p['edge'] == 'governed_by':
        pt = _point(work, p['src'])
        node = _comment_node(work, pt)
        cur = tag_get(node['text'], 'governed_by')
        if op == 'edge.create':
            if cur is not None:
                raise TxError("'%s' is already governed by '%s'" % (p['src'], cur))
            node['text'] = tag_insert(node['text'], 'governed_by', p['dst'], p.get('pos'))
            return {'op': 'edge.delete', 'edge': 'governed_by', 'src': p['src'], 'dst': p['dst']}
        if op == 'edge.delete':
            if cur != p['dst']:
                raise TxError("'%s' is governed by '%s', not '%s'" % (p['src'], cur, p['dst']))
            pos = tag_index(node['text'], 'governed_by')
            node['text'] = tag_del(node['text'], 'governed_by')
            return {'op': 'edge.create', 'edge': 'governed_by', 'src': p['src'], 'dst': p['dst'], 'pos': pos}
        if cur != p['from']:
            raise TxError("'%s' is governed by '%s', not '%s'" % (p['src'], cur, p['from']))
        node['text'] = tag_set(node['text'], 'governed_by', p['to'])
        return {'op': op, 'edge': 'governed_by', 'src': p['src'], 'from': p['to'], 'to': p['from']}
    if op == 'edge.retarget' and p['edge'] == 'calls':
        it = find_item(work, p['src']['id'])[0]
        node = get_path(it, p['src']['path'])
        if node.get('k') != 'call' or node['callee']['k'] != 'id':
            raise TxError('the edge is not a call to a named function')
        old = node['callee']['text']
        if old != p['from']:
            raise TxError("the call goes to '%s', not '%s'" % (old, p['from']))
        node['callee']['text'] = p['to']
        return {'op': op, 'edge': 'calls', 'src': p['src'], 'from': p['to'], 'to': old}
    if op == 'refinement.set_value':
        pt = _point(work, p['point'])
        if pt['form'] not in ('num', 'neg', 'str'):
            raise TxError("'%s' is not a literal point: use the primitive of its form" % p['point'])
        it = find_item(work, pt['id'])[0]
        holder = get_path(it, pt['path'][:-1])
        old = holder[pt['path'][-1]]
        if 'expect' in p and literal_text(old) != p['expect']:
            raise TxError("conflict: '%s' is now %s, the change this undoes left it at %s" % (p['point'], literal_text(old), p['expect']))
        lit = p.get('literal') or (to_literal(p['value']) if pt['form'] == 'str' else p['value'])
        if lit is None:
            raise TxError('the value cannot be written as a literal')
        holder[pt['path'][-1]] = literal_node(lit)
        return {'op': op, 'point': p['point'], 'value': pt['value'], 'literal': literal_text(old), 'expect': lit}
    if op in ('refinement.add_option', 'refinement.remove_option'):
        pt = _point(work, p['point'])
        node = _comment_node(work, pt)
        cur = tag_get(node['text'], 'options')
        opts = cur.split('|') if cur else []
        if op == 'refinement.add_option':
            if p['option'] in opts:
                raise TxError("'%s' is already an option" % p['option'])
            idx = p.get('index')
            idx = len(opts) if idx is None or idx > len(opts) else idx
            opts.insert(idx, p['option'])
            node['text'] = tag_set(node['text'], 'options', '|'.join(opts))
            return {'op': 'refinement.remove_option', 'point': p['point'], 'option': p['option']}
        if p['option'] not in opts:
            raise TxError("'%s' is not an option" % p['option'])
        idx = opts.index(p['option'])
        opts.pop(idx)
        node['text'] = tag_set(node['text'], 'options', '|'.join(opts))
        return {'op': 'refinement.add_option', 'point': p['point'], 'option': p['option'], 'index': idx}
    if op in ('pipeline.insert_stage', 'pipeline.remove_stage', 'pipeline.reorder_stages'):
        pt = _point(work, p['point'])
        if pt['form'] != 'list':
            raise TxError("'%s' is not a pipeline" % p['point'])
        it = find_item(work, pt['id'])[0]
        lst = get_path(it, pt['path'])['items']
        stages = [unquote(x['text']) for x in lst]
        if op == 'pipeline.insert_stage':
            lit = p.get('literal') or to_literal(p['stage'])
            if lit is None:
                raise TxError('the stage cannot be written as a string')
            idx = p.get('index')
            idx = len(lst) if idx is None or idx > len(lst) else idx
            lst.insert(idx, {'k': 'str', 'text': lit})
            return {'op': 'pipeline.remove_stage', 'point': p['point'], 'stage': p['stage'], 'index': idx}
        if op == 'pipeline.remove_stage':
            idx = p.get('index')
            if idx is None:
                if p['stage'] not in stages:
                    raise TxError("'%s' is not a stage" % p['stage'])
                idx = stages.index(p['stage'])
            if idx >= len(lst) or stages[idx] != p['stage']:
                raise TxError("stage %s is not '%s'" % (idx, p['stage']))
            old = lst.pop(idx)
            return {'op': 'pipeline.insert_stage', 'point': p['point'], 'stage': p['stage'], 'index': idx, 'literal': old['text']}
        order = p['order']
        if sorted(order) != sorted(stages):
            raise TxError('the order is not a permutation of the stages')
        pool = list(lst)
        new = []
        for s in order:
            for n, x in enumerate(pool):
                if unquote(x['text']) == s:
                    new.append(pool.pop(n))
                    break
        lst[:] = new
        return {'op': op, 'point': p['point'], 'order': stages}
    raise TxError('unknown primitive %s' % op)


def apply_tx(g, tx, inplace=None):
    """All the primitives or none. -> (the new graph, the inverse transaction): the inverse undoes it, last primitive first."""
    work = g if (INPLACE if inplace is None else inplace) else copy.deepcopy(g)
    inv = []
    try:
        for p in tx:
            inv.append(apply_prim(work, p))
    except TxError:
        if work is g:
            for q in reversed(inv):
                apply_prim(work, q)
        raise
    return work, list(reversed(inv))


# ---- lowering: a sentence to primitives -------------------------------------------------------------------------------------------

def lower_pipeline(cur, to):
    """Remove what is not wanted; insert what is missing at its place in the new order; reorder what is left if it is still out of order."""
    tx, now = [], list(cur)
    for s in cur:
        if s not in to:
            tx.append({'op': 'pipeline.remove_stage', 'point': None, 'stage': s})
            now.remove(s)
    for n, s in enumerate(to):
        if s not in now:
            idx = min(n, len(now))
            tx.append({'op': 'pipeline.insert_stage', 'point': None, 'stage': s, 'index': idx})
            now.insert(idx, s)
    if now != to:
        tx.append({'op': 'pipeline.reorder_stages', 'point': None, 'order': list(to)})
    return tx


def lower(p, s):
    """The transaction a sentence means against point p."""
    attr = s['attr']
    if attr is None:
        if p['form'] in ('num', 'neg'):
            return [{'op': 'refinement.set_value', 'point': p['name'], 'value': s['to']}]
        if p['form'] == 'str':
            return [{'op': 'refinement.set_value', 'point': p['name'], 'value': s['to'], 'literal': to_literal(s['to'])}]
        if p['form'] == 'call':
            return [{'op': 'edge.retarget', 'edge': 'calls', 'src': {'id': p['id'], 'path': p['path']}, 'from': p['value'], 'to': s['to']}]
        cur = p['value'].split('|') if p['value'] else []
        want = s['to'].split('|') if s['to'] else []
        tx = lower_pipeline(cur, want)
        for q in tx:
            q['point'] = p['name']
        return tx
    cur = p['attrs'].get(attr, '')
    to = s['to']
    car = p['carrier']
    if attr == 'options':
        have = cur.split('|') if cur else []
        want = to.split('|') if to else []
        tx, now = [], list(have)
        for o in have:
            if o not in want:
                tx.append({'op': 'refinement.remove_option', 'point': p['name'], 'option': o})
                now.remove(o)
        for n, o in enumerate(want):
            if o not in now:
                idx = min(n, len(now))
                tx.append({'op': 'refinement.add_option', 'point': p['name'], 'option': o, 'index': idx})
                now.insert(idx, o)
        return tx
    if attr == 'governed_by':
        if cur and to:
            return [{'op': 'edge.retarget', 'edge': 'governed_by', 'src': p['name'], 'from': cur, 'to': to}]
        if cur:
            return [{'op': 'edge.delete', 'edge': 'governed_by', 'src': p['name'], 'dst': cur}]
        return [{'op': 'edge.create', 'edge': 'governed_by', 'src': p['name'], 'dst': to}]
    return None   # min, max, risk, floor: the tag text changes (node.update_property), which needs the graph: see `lower_attr`


def lower_attr(work, p, s):
    node = _comment_node(work, p)
    text = node['text']
    to = s['to']
    new = tag_del(text, s['attr']) if to == '' else tag_set(text, s['attr'], to)
    return [{'op': 'node.update_property', 'target': dict(p['carrier']), 'prop': 'text', 'value': new}]


def is_widening(p, attr, frm, to):
    """Does the refinement of a rule loosen it? Widening is the heaviest act, whatever the point's own risk tier."""
    if attr == 'max':
        return frm != '' and (to == '' or num(to) > num(frm))
    if attr == 'min':
        return frm != '' and (to == '' or num(to) < num(frm))
    if attr == 'options':
        have = set(frm.split('|')) if frm else set()
        return bool(set(to.split('|') if to else []) - have)
    if attr == 'risk':
        return frm != '' and (to == '' or int(to) < int(frm))
    if attr == 'floor':
        return frm != '' and (to == '' or POSTURES[to] < POSTURES[frm])
    if attr == 'governed_by':
        return frm != ''
    if attr in ('calls', 'writes', 'reads'):
        return bool(set(names_of(to)) - set(names_of(frm)))             # a name the list did not have: the body may do more than it could
    return False


# ---- the rules ----------------------------------------------------------------------------------------------------------------------------

def rule_value(L, side):
    if NUM_RE.match(side):
        return side
    return point_named(L, side)['value']


def rules_violated(L, only=None):
    """The first rule the state breaks; with `only`, the first of the rules that name that point (a refinement answers for the rules of what it touched)."""
    for r in L['rules']:
        if only and only not in (r['left'], r['right']):
            continue
        a, b = rule_value(L, r['left']), rule_value(L, r['right'])
        both = NUM_RE.match(a) and NUM_RE.match(b)
        x, y = (num(a), num(b)) if both else (a, b)
        op = r['op']
        ok = {'>=': lambda: x >= y, '<=': lambda: x <= y, '>': lambda: x > y, '<': lambda: x < y, '=': lambda: x == y, '!=': lambda: x != y}[op]()
        if not ok:
            return r
    return None


# ---- the BLOCK kind: the body of a function whose signature a human declared -------------------------------------------------------------
# The point is a function's BODY; its value is the body's canonical text, named by its digest. The agent proposes a new body on one line; the gate
# reads it with the compiler's parser, refuses what it could not follow (definitions, loads, eval, `call` by name, braces, comments), holds it to
# the calls and writes its point names (least authority: what is not named is refused), and asks the compiler at derivation (`rnxc check`).
# The lowering keeps every statement that stays, with its id and its comments; the rest is node.delete and node.create.

_BUILTINS = []
_CHECK = {}
DIGEST_RE = re.compile(r'^sha:[0-9a-f]{12}$')


def body_text(items):
    """A body's canonical text: the printer's, each statement at the body's own level, a line each."""
    return l1.print_ring({'k': 'file', 'items': ids.strip(items)}) if items else ''


def block_digest(text):
    return 'sha:' + hashlib.sha256(text.encode('latin-1')).hexdigest()[:12]


def builtins():
    """Ring's builtin names, as rnxc's checker has them (src/builtins.zig)."""
    if not _BUILTINS:
        src = open(os.path.join(ROOT, 'src', 'builtins.zig'), encoding='utf-8').read()
        _BUILTINS.extend(re.findall(r'"([^"]+)"', src.split('pub const names', 1)[1].split('};', 1)[0]))
    return _BUILTINS


def names_of(v):
    return v.split('|') if v else []


def all_nodes(x):
    if isinstance(x, dict):
        yield x
        for f, v in x.items():
            if not f.startswith('_'):
                yield from all_nodes(v)
    elif isinstance(x, list):
        for v in x:
            yield from all_nodes(v)


def _text(x):
    return x['text'] if isinstance(x, dict) else x


# Names Ring's parser takes as identifiers. A keyword is a name only where ring_parser_processkeywords turns it into one: by context for TO IN FROM STEP BUT
# OK ON CASE OFF CATCH DONE AGAIN ELSE OTHER (when no statement of theirs is open, which a definition's head never is), always for THIS SELF SUPER MAIN INIT
# OPERATOR, the brace hooks and the RINGVM ones (vendor/ring-vm/src/parser.c:161-190). Every other keyword is refused (C6): GET, PUT, GIVE, SEE, NEXT, IF...
# tree-sitter-ring, the compiler's parser, takes them all without a word, so the gate asks the vendored scanner and parser what Ring does (HF-101).
NAME_KEYWORDS = {'to', 'in', 'from', 'step', 'but', 'ok', 'on', 'case', 'off', 'catch', 'done', 'again', 'else', 'other', 'this', 'self', 'super',
                 'ringvm_see', 'ringvm_give', 'ringvm_errorhandler', 'main', 'init', 'operator', 'bracestart', 'braceend', 'braceexpreval',
                 'braceerror', 'bracenewline'}
# methods Ring calls itself (F-69, and the brace hooks of a brace block), whatever the class does with them
CALLED_BY_RING = {'operator': 'the method Ring calls for every operator (F-69)', 'bracestart': 'a hook Ring calls on a brace block',
                  'braceend': 'a hook Ring calls on a brace block', 'braceerror': 'a hook Ring calls on a brace block',
                  'braceexpreval': 'a hook Ring calls on a brace block', 'bracenewline': 'a hook Ring calls on a brace block'}
_KEYWORDS = []


def ring_keywords():
    """Ring's keywords, lower case, read from the vendored scanner (vendor/ring-vm/include/scanner.h)."""
    if not _KEYWORDS:
        src = open(os.path.join(ROOT, 'vendor', 'ring-vm', 'include', 'scanner.h'), encoding='utf-8', errors='replace').read()
        block = src.split('RING_KEYWORDS[] = {', 1)[1].split('};', 1)[0]
        _KEYWORDS.extend(w.lower() for w in re.findall(r'"([A-Za-z_]+)"', block))
    return _KEYWORDS


def not_a_name(word):
    """Is `word` a keyword Ring's parser will not take as the name of a function, a method or a parameter?"""
    w = word.lower()
    return w in set(ring_keywords()) and w not in NAME_KEYWORDS


def function_faults(g, name, kind, tag_attrs, lst, parent):
    """What is wrong with a FUNCTION or METHOD tag, and the function it stands for. -> (faults, fatal, that function or None). Fatal faults leave no point to
    speak of: a tag in the wrong place, a name that is no function's, a class or a look-alike in the way. The others are faults and the point stays, so a
    refinement answers for the rest. A FUNCTION is declared at the top level and looked for there; a METHOD among the members of the class its tag stands in."""
    faults = []
    attrs = {a['key']: a['val'] for a in tag_attrs}
    order = [a['key'] for a in tag_attrs if a['key'] != 'name']
    word = 'function' if kind == 'function' else 'method'
    if lst is None:
        return ["point '%s' is a trailing comment; a %s tag stands alone on its line" % (name, kind.upper())], True, None
    if kind == 'function' and parent is not None:
        return ["point '%s' stands inside another definition; a function is declared at the top level, among the statements" % name], True, None
    if kind == 'method':
        if parent is None:
            return ["point '%s' stands outside a class; a METHOD tag stands among its class's members, with a member below it (after the last member it leaves the class)" % name], True, None
        if parent['k'] == 'func':
            return ["point '%s' stands inside a function; a method is declared among its class's members" % name], True, None
        if parent['k'] != 'class':
            return ["point '%s' stands inside another definition; a method is declared among its class's members" % name], True, None
    if not IDENT_RE.match(name):
        return ["point '%s' is not a %s name" % (name, word)], True, None
    if not_a_name(name):
        faults.append("'%s' is a Ring keyword: Ring's parser does not take it as a name (C6)" % name)
    if kind == 'function':
        if name.lower() in set(builtins()):
            faults.append("'%s' is a Ring builtin" % name)
        if name.lower() == 'main':
            faults.append("'%s' is the function Ring calls after the top level (F-60)" % name)
    else:
        low = name.lower()
        if low in CALLED_BY_RING:
            faults.append("'%s' is called by Ring itself: %s" % (name, CALLED_BY_RING[low]))
        for it in parent['items']:
            if it['k'] == 'expr' and it['e'].get('k') == 'assign' and it['e']['l'].get('k') == 'id':
                attr = it['e']['l']['text']
                if low in ('get' + attr.lower(), 'set' + attr.lower()):
                    faults.append("'%s' is called by Ring itself: the %s of the attribute '%s' (F-73)" % (name, 'getter' if low.startswith('get') else 'setter', attr))
                    break
        if low in set(builtins()):
            faults.append("'%s' shadows the builtin: inside the class's methods a bare call goes to the class's own method first" % name)
        for it, par, *_ in walk_items(g):
            if par is None and it['k'] == 'func' and ids.def_name(it).lower() == low:
                faults.append("'%s' shadows the function '%s': inside the class's methods a bare call goes to the class's own method first" % (name, ids.def_name(it)))
                break
    for key in order:
        if key not in FUNCTION_ATTRS:
            faults.append("'%s' is not an attribute of a %s point" % (key, kind.upper()))
    declared = names_of(attrs.get('params'))
    seen = set()
    for q in declared:
        if not IDENT_RE.match(q):
            faults.append("'%s' in params of '%s' is not a parameter name" % (q, name))
        elif not_a_name(q):
            faults.append("'%s' in params of '%s' is a Ring keyword: Ring's parser does not take it as a name" % (q, name))
        elif q.lower() in seen:
            faults.append("params of '%s' repeat '%s'" % (name, q))
        seen.add(q.lower())
    existing = None
    if kind == 'function':
        for it, par, *_ in walk_items(g):
            if par is not None or it['k'] not in ('func', 'class') or ids.def_name(it).lower() != name.lower():
                continue
            if it['k'] == 'class':
                return faults + ["'%s' is declared as a class" % name], True, None
            if ids.def_name(it) != name:
                return faults + ["the function is declared '%s', the point names '%s' (names are exact, D24)" % (ids.def_name(it), name)], True, None
            existing = it
    else:
        for it in parent['items']:
            if it['k'] != 'func' or ids.def_name(it).lower() != name.lower():
                continue
            if ids.def_name(it) != name:
                return faults + ["the method is declared '%s', the point names '%s' (names are exact, D24)" % (ids.def_name(it), name)], True, None
            existing = it
    if existing is not None:
        have = [q['name'] for q in existing.get('params', [])]
        if have != declared:
            faults.append("'%s' takes (%s), the point declares (%s)" % (name, ', '.join(have), ', '.join(declared)))
    return faults, False, existing


def point_function(g, p):
    """The function a BLOCK or FUNCTION point stands for: the func under a BLOCK tag, the top-level func a FUNCTION point names -- None while it is not
    there."""
    if p['kind'] == 'block':
        return find_item(g, p['id'])[0]
    if p['kind'] == 'method':
        cls = find_item(g, p['carrier']['id'])[1]                   # the class the tag stands in
        return next((m for m in cls['items'] if m['k'] == 'func' and ids.def_name(m) == p['name']), None)
    for it, par, *_ in walk_items(g):
        if par is None and it['k'] == 'func' and ids.def_name(it) == p['name']:
            return it
    return None


def create_function(g, p, items):
    """The one node.create of a function that is not there: the signature the point declares, the body proposed. It goes AFTER the last function and
    BEFORE the first class (F-21), never beside the tag: Ring ends a function at the next function or class and nowhere else, so a function written among
    the top-level statements would swallow every statement after it (HF-73)."""
    head = parse_text('func %s(%s)\n' % (p['name'], ', '.join(names_of(p['attrs'].get('params')))))
    fn = ids.strip(head['items'][0])
    fn['items'] = [ids.strip(st) for st in items]
    if p['kind'] == 'method':
        # into the class the tag stands in, after its last member and BEFORE `private`: the marker is flat in the graph, and a method after it is private
        cls = find_item(g, p['carrier']['id'])[1]
        members = cls['items']
        idx = next((i for i, it in enumerate(members) if it['k'] == 'private'), len(members))
        return {'op': 'node.create', 'parent': cls['_id'], 'block': ['items'], 'index': idx, 'node': fn}
    top = g['items']
    idx = next((i for i, it in enumerate(top) if it['k'] == 'class'), len(top))
    return {'op': 'node.create', 'parent': None, 'block': 'items', 'index': idx, 'node': fn}


def body_params(g, p):
    """The parameters of the function a BLOCK or FUNCTION point stands for, and its name: a BLOCK point's from the function under its tag, a FUNCTION
    point's as the tag declares them (the lift has already checked that a function that exists takes exactly these)."""
    if p['kind'] == 'block':
        fn = find_item(g, p['id'])[0]
        return [q['name'] for q in fn.get('params', [])], ids.def_name(fn)
    return names_of(p['attrs'].get('params')), p['name']


_UNIT_NAMES = [None]   # what the unit of the model being judged defines beyond its own file (D32); None for a program asked about alone
_UNIT_CACHE = {}


def unit_names(unit):
    """What the program that loads a library defines -- its functions and classes as `rnxc graph` reads them, spelt as each file declares them -- and
    the natives the engine's list names: the names a library's point may call (D32). The library file's own names come from its graph, so the unit's
    are read from the files on disk. Cached by the unit."""
    key = (unit['root'], unit.get('natives'))
    if key in _UNIT_CACHE:
        return _UNIT_CACHE[key]
    import subprocess
    r = subprocess.run([RNXC, 'graph', unit['root']], capture_output=True, timeout=600)
    names = set()
    for ln in r.stdout.decode('utf-8', 'replace').split('\n'):
        f = ln.strip().split('|')
        if f[0] in ('FUNC', 'CLASS') and len(f) > 1 and f[1]:
            names.add(f[1])
    if unit.get('natives'):
        names |= set(open(unit['natives'], 'rb').read().decode('latin-1').split())
    _UNIT_CACHE[key] = names
    return names


class InUnit:
    """`with InUnit(model.unit):` -- the lift's name check sees the unit's names for the duration."""

    def __init__(self, unit):
        self.names = unit_names(unit) if unit else None

    def __enter__(self):
        self.prev = _UNIT_NAMES[0]
        _UNIT_NAMES[0] = self.names

    def __exit__(self, *exc):
        _UNIT_NAMES[0] = self.prev


def name_list_errors(g, p, attr, names):
    """What is wrong with a list of names as the `calls` or `writes` of a point: a call must be a function, class or builtin the program has, a write a
    global, an attribute or a parameter of the function -- each spelt as declared (D24)."""
    out = []
    params, owner = body_params(g, p)
    if attr == 'calls':
        fns = {ids.def_name(it) for it, *_ in walk_items(g) if it['k'] in ('func', 'class')}
        if p['kind'] in DECLARING:
            fns.add(p['name'])                                      # a function the point declares is a function, there or not
        fns |= _UNIT_NAMES[0] or set()                              # a library's: what the program that loads it defines (D32)
        bis = set(builtins())
        for nm in names:
            if nm in fns or nm in bis:
                continue
            hit = sorted(x for x in fns if x.lower() == nm.lower())
            bhit = sorted(x for x in bis if x.lower() == nm.lower())
            if hit:
                out.append("calls of '%s' names '%s'; the function is declared '%s'" % (p['name'], nm, hit[0]))
            elif bhit:
                out.append("calls of '%s' names '%s'; the builtin is spelt '%s'" % (p['name'], nm, bhit[0]))
            else:
                out.append("'%s' in calls of '%s' is no function and no builtin" % (nm, p['name']))
    elif attr == 'reads':
        for nm in names:                                            # a parameter is the function's own: reading it is not governed
            if not (nm.startswith('$') or nm.startswith('@')):
                out.append("'%s' in reads of '%s' is no global and no attribute (a parameter is the function's own)" % (nm, p['name']))
    else:
        for nm in names:
            if not (nm.startswith('$') or nm.startswith('@') or nm in params):
                out.append("'%s' in writes of '%s' is no global, no attribute and no parameter of %s()" % (nm, p['name'], owner))
    return out


def allowlist_error(g, p, attr, to):
    """Is TO a list the program can honour as the `calls` or `writes` of point p? None, or why not. "" is a list: the body then calls nothing, or writes
    its own locals only."""
    names, seen = names_of(to), set()
    for nm in names:
        if not nm:
            return 'an empty name'
        if nm in seen:
            return "'%s' repeats" % nm
        seen.add(nm)
    errs = name_list_errors(g, p, attr, names)
    return errs[0] if errs else None


def body_own_error(g, p):
    """Is the body that is there inside its own point's rule -- calls and writes only what the point names? None, or what it does that it may not. A
    function that is not there yet has no body to judge."""
    fn = point_function(g, p)
    if fn is None or not fn.get('items'):
        return None
    return block_constraint(p, fn, fn['items'], g)


def block_decl_errors(g, p):
    """What a BLOCK or FUNCTION point's tag may say about its body: calls of what the program defines or Ring builds in, spelt as declared (D24); writes
    of a global, an attribute or a parameter of its function."""
    out, a = [], p['attrs']
    if p['kind'] == 'block':
        for key in p['order']:
            if key not in BLOCK_ATTRS:
                out.append("'%s' is not an attribute of a BLOCK point" % key)
    for attr in ('calls', 'writes', 'reads'):                       # a FUNCTION tag's other attributes were read by function_faults
        out += name_list_errors(g, p, attr, names_of(a.get(attr)))
    return out


def body_shape_error(body):
    """A body is a statement list the gate can read, and nothing else."""
    for it in body['items']:
        k = it['k']
        if k in ('func', 'class', 'package'):
            return 'a body defines nothing, and TO holds a %s' % ('function' if k == 'func' else k)
        if k in ('load', 'import'):
            return 'a body loads nothing, and TO holds a %s' % k
    for n in all_nodes(body['items']):
        k = n.get('k')
        if k == 'comment' or n.get('trail'):
            return 'a comment in TO: the gate does not judge prose, and a comment can mislead the reader of the diff'
        if k == 'call' and n['callee'].get('k') == 'id' and n['callee']['text'].lower() == 'eval':
            return 'TO calls eval, which runs code the gate cannot read'
        if k == 'callkw':
            return 'TO calls a function by name (`call`), which the gate cannot follow'
        if k == 'brace':
            return 'TO holds a brace block, whose hooks and bare calls the gate cannot follow'
        if k == 'scanner':
            return 'TO changes the language under the text'
        if k == 'bye':
            return 'TO ends the program (bye): a body returns, it does not stop the program'
    return None


def body_calls(items):
    """Every name a body calls: a function, a method (`x.M()` is a call of M), a class it makes (`new K`)."""
    out = []
    for n in all_nodes(items):
        k = n.get('k')
        if k == 'call':
            c = n['callee']
            if c.get('k') == 'id':
                out.append(c['text'])
            elif c.get('k') == 'member':
                out.append(_text(c['prop']))
        elif k == 'new':
            nm = n.get('name')
            out.append('.'.join(_text(x) for x in nm) if isinstance(nm, list) else _text(nm))
    return out


def body_writes(items, params):
    """Every write a body makes outside its own frame: ('global', '$x'), ('attr', '@x'), ('param', name) -- writing INTO what a parameter holds,
    since the caller holds it too; assigning the parameter itself only rebinds a local (C-29)."""
    out = []
    alias = {}      # a for-in variable is a REFERENCE into the list it walks (Ring and Ring++ agree): writing through it writes the list's owner's contents

    def root(e):
        while isinstance(e, dict) and e.get('k') in ('index', 'member', 'paren'):
            e = e.get('e') if e.get('k') == 'paren' else e.get('obj')
        return e.get('text') if isinstance(e, dict) and e.get('k') == 'id' else None

    def owner(name):
        if name is None:
            return None
        if name.startswith('$'):
            return ('global', name)
        if name.startswith('@'):
            return ('attr', name)
        if name.lower() in alias:
            return alias[name.lower()]
        if name.lower() in params:
            return ('param', params[name.lower()])
        return None

    for n in all_nodes(items):                                      # source order, outer loops first
        if n.get('k') == 'for' and n.get('kind') == 'in' and n.get('var'):
            o = owner(root(n.get('a')))
            if o:
                alias[str(n['var']).lower()] = o

    def into(r, chain=None):
        if r.get('k') == 'id':
            t = r['text']
            if t.lower() in alias and t[:1] not in ('$', '@'):
                out.append(alias[t.lower()])
            elif t.startswith('$'):
                out.append(('global', t))
            elif t.startswith('@'):
                out.append(('attr', t))
            elif t.lower() in params and chain is not None:
                out.append(('param', params[t.lower()]))
        elif r.get('k') == 'self' and chain is not None and chain.get('k') == 'member':
            out.append(('attr', '@' + _text(chain['prop'])))

    def target(l):
        if l.get('k') in ('index', 'member'):
            chain = l
            while chain['obj'].get('k') in ('index', 'member'):
                chain = chain['obj']
            into(chain['obj'], chain)
        else:
            into(l)

    for n in all_nodes(items):
        k = n.get('k')
        if k == 'assign':
            target(n['l'])
        elif k == 'post':
            target(n['e'])
        elif k == 'for' and str(n.get('var') or '')[:1] in ('$', '@'):   # `for $x = ...` and `for $x in ...` write the variable on every turn
            into({'k': 'id', 'text': str(n['var'])})
        elif k == 'give' and isinstance(n.get('target'), dict):     # `give $x` reads a line of input INTO the variable
            target(n['target'])
        elif k == 'catch' and n.get('binding'):                     # `catch($x)` binds the error to the variable
            into({'k': 'id', 'text': str(n['binding'])})
        elif k == 'call' and n['callee'].get('k') == 'id' and n['callee']['text'].lower() in MUTATORS and n.get('args'):
            a0 = n['args'][0]
            if a0.get('k') == 'id':
                into(a0, a0)
            else:
                target(a0)
    return out


def body_reads(items):
    """Every global and attribute a body READS: `$x`, `@x`, and `This.x` (an attribute of the object), wherever they stand -- except where a name is only WRITTEN, which is the writes' business:
    the target of a plain `=`, a loop variable, a `give` target, a `catch` binding. A compound assignment, `x++` and the root of an indexed or member target read what they write.
    -> [name]"""
    nodes = list(all_nodes(items))
    pure = {id(n['callee']) for n in nodes if n.get('k') == 'call' and isinstance(n.get('callee'), dict)}      # `This.Size()` is a call of Size, not a read of an attribute
    for n in nodes:
        k = n.get('k')
        if k == 'assign' and n.get('op') == '=' and isinstance(n.get('l'), dict):
            pure.add(id(n['l']))
        elif k == 'give' and isinstance(n.get('target'), dict):
            pure.add(id(n['target']))
    out = []
    for n in nodes:
        k = n.get('k')
        if k == 'id' and id(n) not in pure and str(n.get('text', ''))[:1] in ('$', '@'):
            out.append(n['text'])
        elif k == 'member' and id(n) not in pure and isinstance(n.get('obj'), dict) and n['obj'].get('k') in ('self', 'this'):
            out.append('@' + _text(n['prop']))
    return out


def accessors(g):
    """The methods the program's classes declare that Ring runs by itself when code reads or assigns a member: get<name> and set<name> (F-73). -> {lower name: declared name}."""
    out = {}
    for it, parent, bpath, lst, i, owner in walk_items(g):
        if it.get('k') == 'func' and parent is not None and parent.get('k') == 'class':
            nm = ids.def_name(it)
            if nm.lower().startswith(('get', 'set')) and len(nm) > 3:
                out.setdefault(nm.lower(), nm)
    return out


def body_accessors(items):
    """Every get<name> / set<name> a body can run by touching a member: a member that is not the callee of a call is an attribute access, read (getter), assigned (setter)
    or both (`+=`, `++`). `This.x` and `self.x` are exempt, as they are on Ring. -> [(accessor lower name, the member's name as written, 'reads' | 'assigns')]"""
    nodes = list(all_nodes(items))
    callee = {id(n['callee']) for n in nodes if n.get('k') == 'call' and isinstance(n.get('callee'), dict)}
    role = {}
    for n in nodes:
        if n.get('k') == 'assign' and isinstance(n.get('l'), dict) and n['l'].get('k') == 'member':
            role[id(n['l'])] = 'set' if n.get('op') == '=' else 'both'
        elif n.get('k') == 'post' and isinstance(n.get('e'), dict) and n['e'].get('k') == 'member':
            role[id(n['e'])] = 'both'
    out = []
    for n in nodes:
        if n.get('k') != 'member' or id(n) in callee or n.get('obj', {}).get('k') in ('self', 'this'):
            continue
        prop = _text(n['prop'])
        r = role.get(id(n))
        if r in (None, 'both'):
            out.append(('get' + prop.lower(), prop, 'reads'))
        if r in ('set', 'both'):
            out.append(('set' + prop.lower(), prop, 'assigns'))
    return out


def block_constraint(p, fn, items, g=None):
    a = p['attrs']
    allowed = names_of(a.get('calls'))
    for nm in body_calls(items):
        if nm in allowed:
            continue
        hit = [x for x in allowed if x.lower() == nm.lower()]
        if hit:
            return "'%s' is not a call '%s' allows (the declared spelling is '%s')" % (nm, p['name'], hit[0])
        return "'%s' is not a call '%s' allows" % (nm, p['name'])
    if g is not None:                                       # a member read or assignment is a CALL when a class declares get<name> / set<name>
        acc = accessors(g)
        for low, prop, what in body_accessors(items):
            decl = acc.get(low)
            if decl and decl not in allowed:
                return "%s .%s, which runs %s() (Ring calls a class's get<name> and set<name> by itself), and '%s' does not allow it" % (what, prop, decl, p['name'])
    params = {q['name'].lower(): q['name'] for q in fn.get('params', [])}
    may = names_of(a.get('writes'))
    for what, nm in body_writes(items, params):
        if nm in may:
            continue
        if what == 'param':
            return "writes into '%s', which the caller holds, and '%s' does not allow it" % (nm, p['name'])
        return "writes %s, which '%s' does not allow" % (nm, p['name'])
    readable = set(names_of(a.get('reads'))) | set(may)           # what a body may write it may read: `$n += 1` reads $n
    for nm in body_reads(items):
        if nm not in readable:
            hit = [x for x in readable if x.lower() == nm.lower()]
            return "reads %s, which '%s' does not allow%s" % (nm, p['name'], " (the declared spelling is '%s')" % hit[0] if hit else '')
    return None


def _stmt_key(it):
    one = ids.strip(it)
    one.pop('trail', None)
    return l1.print_ring({'k': 'file', 'items': [one]})


def lower_block(fn, new_items):
    """The transaction that makes fn's body new_items: statements matched on their canonical text (difflib's longest matching blocks); a statement
    that stays keeps its id and the comments attached to it (rung 18: a comment belongs to the next statement); the rest is node.delete, deletes first,
    then node.create at its place, a fresh id each."""
    units, pending = [], []
    for it in fn.get('items', []):
        if it['k'] == 'comment':
            pending.append(it)
        else:
            units.append((pending, it))
            pending = []
    tail = pending
    old_keys = [_stmt_key(st) for _, st in units]
    new_keys = [_stmt_key(st) for st in new_items]
    kept_old, kept_new = {}, {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old_keys, new_keys, autojunk=False).get_opcodes():
        if tag == 'equal':
            for d in range(i2 - i1):
                kept_old[i1 + d] = j1 + d
                kept_new[j1 + d] = i1 + d
    tx = []
    for i, (cmts, st) in enumerate(units):
        if i not in kept_old:
            for c in cmts:
                tx.append({'op': 'node.delete', 'id': c['_id']})
            tx.append({'op': 'node.delete', 'id': st['_id']})
    sim = []
    for i, (cmts, st) in enumerate(units):
        if i in kept_old:
            sim += [c['_id'] for c in cmts] + [st['_id']]
    sim += [c['_id'] for c in tail]
    pos = 0
    for j, st in enumerate(new_items):
        if j in kept_new:
            pos = sim.index(units[kept_new[j]][1]['_id']) + 1
            continue
        tx.append({'op': 'node.create', 'parent': fn['_id'], 'block': ['items'], 'index': pos, 'node': ids.strip(st)})
        sim.insert(pos, None)
        pos += 1
    return tx


def rnxc_findings(text, unit=None):
    """What `rnxc check --closed` says of a program: ([(severity, rule, message)], [the rules it says it did NOT check, and why]).

    CLOSED (D32): the gate's question is whether the unit DEFINES every name a body uses, not Ring's whether the line errs when it runs. So a file
    that runs nothing is asked about, and eval, loadlib and an admission do not shut the absence rules -- a name only one of them could make is
    absent, because the gate cannot see what it calls (D28). `unit` -- {'root', 'file', 'natives'} -- asks it of a LIBRARY file inside the program
    that loads it: the root's unit is checked with the file's text replaced by `text` (`--subst`, the file on disk untouched), and a native counts
    when the engine's own list (`natives`, one name a line) names it. A file the unit cannot read or parse still shuts the check."""
    key = hashlib.sha256(text.encode('latin-1') + repr(sorted((unit or {}).items())).encode()).hexdigest()
    if key in _CHECK:
        return _CHECK[key]
    os.makedirs(SCRATCH, exist_ok=True)
    _n[0] += 1
    path = os.path.join(SCRATCH, 'chk%d_%d.ring' % (os.getpid(), _n[0]))
    open(path, 'wb').write(text.encode('latin-1'))
    if unit:
        cmd = [RNXC, 'check', unit['root'], '--closed', '--subst=%s=%s' % (unit['file'], path)]
    else:
        cmd = [RNXC, 'check', path, '--closed']
    if unit and unit.get('natives'):
        cmd.append('--natives=%s' % unit['natives'])
    import subprocess
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=600)
        lines = (r.stdout + r.stderr).decode('utf-8', 'replace').replace('\r\n', '\n').split('\n')
    except (OSError, subprocess.TimeoutExpired) as e:
        lines = ['  NOT checked -- rnxc check did not run: %s' % e]
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
    finds, shut = [], []
    for i, line in enumerate(lines):
        m = re.match(r'^\s+\d+:\d+\s+(error|warn|perf|note)\s+(\S+)\s*$', line)
        if m:
            finds.append((m.group(1), m.group(2), lines[i + 1].strip() if i + 1 < len(lines) else ''))
        elif 'NOT checked --' in line:
            shut.append(line.strip())
    _CHECK[key] = (finds, shut)
    return finds, shut


def evaluate_block(model, s, ctx, out, p):
    """A sentence against a BLOCK point, through the same five stages."""
    g = model.g
    frm, to = s['from'], s['to']
    fn = point_function(g, p)        # a BLOCK point's function is always there; a FUNCTION point's may not be
    revert = None
    if 'reverts' in s:
        revert = model.event(s['reverts'])
        if revert is None:
            return out.reject('structural', 'no event %d' % s['reverts'])
        if not revert['admitted'] or revert['kind'] != 'refine':
            return out.reject('structural', 'event %d was not admitted' % s['reverts'])
        if revert.get('reverted_by'):
            return out.reject('structural', 'event %d is already reverted by event %d' % (s['reverts'], revert['reverted_by']))
        if revert['target'] != s['target']:
            return out.reject('structural', 'event %d refined %s, not %s' % (s['reverts'], revert['target'], s['target']))
    if frm != p['value']:
        return out.reject('structural', "stale: '%s' is %s now, not %s" % (p['name'], p['value'], frm))
    items = None
    if revert is not None:
        if to != revert['value_from']:
            return out.reject('structural', "TO is not the prior state of event %d, which is '%s'" % (s['reverts'], revert['value_from']))
        if p['value'] != revert['value_to']:
            return out.reject('structural', "conflict: '%s' is %s now, event %d left it at %s" % (p['name'], p['value'], s['reverts'], revert['value_to']))
        tx = copy.deepcopy(revert['inverse'])
    else:
        if p['kind'] in DECLARING and to.strip() == 'absent':
            return out.reject('structural', "a refinement does not delete a function: 'absent' is the state before one is made, and a revert of its creation is the way back")
        if DIGEST_RE.match(to):
            return out.reject('structural', "TO is a digest, which only a revert's TO is: a body is proposed as its statements")
        try:
            body = parse_text(to + '\n') if to.strip() else {'k': 'file', 'items': []}
        except Unreadable as e:
            return out.reject('structural', 'TO does not parse as a body: %s' % e)
        why = body_shape_error(body)
        if why:
            return out.reject('structural', why)
        items = body['items']
        tx = [create_function(g, p, items)] if fn is None else lower_block(fn, items)
        if not tx:
            return out.reject('structural', "nothing to refine: '%s' is %s already" % (p['name'], p['value']))
    out.passed('structural')
    if revert is not None or 'constraint' in SKIP_STAGES:
        out.skipped('constraint')
    else:
        sig = fn if fn is not None else {'params': [{'name': q} for q in names_of(p['attrs'].get('params'))]}
        why = block_constraint(p, sig, items, g)
        if why:
            return out.reject('constraint', why)
        out.passed('constraint')
    try:
        new, inv = apply_tx(g, tx)
    except TxError as e:
        return out.reject('structural', 'the change cannot be applied: %s' % e)
    try:
        back = parse_text(text_of(new))
    except Unreadable as e:
        return out.reject('structural', 'the refined program does not parse: %s' % e)
    if l1.norm(ids.strip(back)) != l1.norm(ids.strip(new)):
        return out.reject('structural', 'the refined program does not read back as itself')
    out.tx, out.inverse = tx, inv
    out.value_from = p['value']
    after = point_named(lift(new), p['name'])
    out.value_to = after['value'] if after else ''
    gname = p['attrs'].get('governed_by')
    if 'governance' in SKIP_STAGES or not gname:
        out.skipped('governance')
    else:
        why = governance(ctx, gname, s['author'], p, None)
        if why:
            return out.reject('governance', why)
        out.passed('governance')
    floor = p['attrs'].get('floor')
    if 'trust' in SKIP_STAGES:
        out.skipped('trust')
    elif floor and POSTURES[s['posture']] < POSTURES[floor]:
        return out.reject('trust', "posture :%s below the required floor for '%s'" % (s['posture'], p['name']))
    else:
        out.passed('trust')
    if 'derivation' in SKIP_STAGES:
        out.skipped('derivation')
    else:
        bad = [e for e in lift(new)['errors'] if not e['own']]
        if bad:
            return out.reject('derivation', 'the declarations no longer lift: ' + bad[0]['msg'])
        f0, _ = rnxc_findings(text_of(g), model.unit)
        f1, shut = rnxc_findings(text_of(new), model.unit)
        if shut:
            return out.reject('derivation', 'rnxc check does not check this program: ' + shut[0])
        seen = {}
        for sev, rule, msg in f0:
            k = (rule, re.sub(r'[0-9]+', '#', msg))
            seen[k] = seen.get(k, 0) + 1
        for sev, rule, msg in f1:
            k = (rule, re.sub(r'[0-9]+', '#', msg))
            if seen.get(k):
                seen[k] -= 1
            elif sev in ('error', 'warn'):
                return out.reject('derivation', 'rnxc check: %s (%s)' % (msg, rule))
        if 'cascade' in s and s['cascade']:
            return out.reject('derivation', "cascade stated %s but a body has callers, not readers" % sorted(set(s['cascade'])))
        out.passed('derivation')
    out.cascade = {'reads': [], 'writes': []}
    out.status, out.stage, out.graph = 'admitted', 'all', new
    out.why = "admitted: '%s' %s -> %s [:%s]" % (s['target'], out.value_from, out.value_to, s['posture'])
    out.diff = diff_lines(text_of(g), text_of(new))
    return out


# ---- the gate ---------------------------------------------------------------------------------------------------------------------------

class Outcome:
    def __init__(self, sentence):
        self.sentence = sentence
        self.status = 'rejected'
        self.stage = None
        self.why = ''
        self.stages = []        # (stage, 'pass' | 'fail' | 'skip')
        self.tx = []
        self.inverse = []
        self.graph = None
        self.cascade = None
        self.warnings = []
        self.diff = []
        self.value_from = self.value_to = None
        self.point = None

    @property
    def admitted(self):
        return self.status in ('admitted', 'flagged')

    def reject(self, stage, why):
        self.status, self.stage, self.why = 'rejected', stage, why
        self.stages.append((stage, 'fail'))
        return self

    def passed(self, stage):
        self.stages.append((stage, 'pass'))

    def skipped(self, stage):
        self.stages.append((stage, 'skip'))


def evaluate(model, s, ctx, readback=True):
    """One sentence through the gate against a model. The model is not changed: the outcome carries the new graph for the caller to keep."""
    out = Outcome(s)
    if s is None:
        return out
    g = model.g
    L = lift(g)
    # ---------------------------------------------------------------- structural: the language itself is asked
    blocking = [e for e in L['errors'] if not e['own']]
    if blocking:        # a declaration that cannot be read stops everything; a value outside its own bounds does not (it can be repaired)
        return out.reject('structural', 'declarations do not lift: ' + blocking[0]['msg'])
    p = point_named(L, s['base'])
    if p is None:
        return out.reject('structural', "no refinement point '%s'%s" % (s['base'], near([q['name'] for q in L['points']], s['base'])))
    out.point = p
    if s['kind'] != p['kind']:
        return out.reject('structural', "kind '%s' does not match point '%s', which is declared %s" % (s['kind'], p['name'], p['kind']))
    if not p['built']:
        return out.reject('structural', "kind '%s' is declared but not built at this rung" % p['kind'])
    if 'at' in s and s['at'] != p['id']:
        return out.reject('structural', "stale: '%s' is at id %d, not %d" % (p['name'], p['id'], s['at']))
    attr = s['attr']
    if attr is not None and attr not in RULE_ATTRS:
        return out.reject('structural', "'%s' is not an attribute of a point's rule (%s)" % (attr, ', '.join(RULE_ATTRS)))
    if p['kind'] in BODY_KINDS and attr is None:
        return evaluate_block(model, s, ctx, out, p)
    frm, to = s['from'], s['to']
    revert = None
    if 'reverts' in s:
        revert = model.event(s['reverts'])
        if revert is None:
            return out.reject('structural', 'no event %d' % s['reverts'])
        if not revert['admitted'] or revert['kind'] != 'refine':
            return out.reject('structural', 'event %d was not admitted' % s['reverts'])
        if revert.get('reverted_by'):
            return out.reject('structural', 'event %d is already reverted by event %d' % (s['reverts'], revert['reverted_by']))
        if revert['target'] != s['target']:
            return out.reject('structural', 'event %d refined %s, not %s' % (s['reverts'], revert['target'], s['target']))
    cur = p['attrs'].get(attr, '') if attr else p['value']
    if attr in ('min', 'max'):
        same = frm == cur or (frm and cur and NUM_RE.match(frm) and NUM_RE.match(cur) and num(frm) == num(cur))
    else:
        same = same_value(p, frm, cur) if attr is None else frm == cur
    if not same:
        return out.reject('structural', "stale: '%s' is %s now, not %s" % (s['target'], cur, frm))
    if to == cur:
        return out.reject('structural', "nothing to refine: '%s' is %s already" % (s['target'], cur if cur != '' else 'unset'))
    if revert is not None:
        if not (to == revert['value_from'] or (attr is None and same_value(p, to, revert['value_from']))):
            return out.reject('structural', "TO is not the prior state of event %d, which is '%s'" % (s['reverts'], revert['value_from']))
        if not (cur == revert['value_to'] or (attr is None and same_value(p, cur, revert['value_to']))):
            return out.reject('structural', "conflict: '%s' is %s now, event %d left it at %s" % (s['target'], cur, s['reverts'], revert['value_to']))
    # the shape of TO
    form = p['form']
    if attr is None:
        if form in ('num', 'neg'):
            if not NUM_RE.match(to):
                return out.reject('structural', "TO '%s' is not a number" % to)
        elif form == 'str':
            if to_literal(to) is None:
                return out.reject('structural', 'TO cannot be written as a Ring string')
        elif form == 'call':
            if not IDENT_RE.match(to):
                return out.reject('structural', "TO '%s' is not a function name" % to)
            fns = [it for it, par, bp, lst, i, own in walk_items(g) if it['k'] == 'func' and par is None]
            fn = [it for it in fns if ids.def_name(it) == to]
            if not fn:
                hint = [ids.def_name(it) for it in fns if ids.def_name(it).lower() == to.lower()]
                return out.reject('structural', "no function '%s' in this program%s" % (to, " (names are exact: '%s' is declared)" % hint[0] if hint else ''))
            it = find_item(g, p['id'])[0]
            call = get_path(it, p['path'])
            want, have = len(fn[0].get('params', [])), len(call.get('args', []))
            if want != have:
                return out.reject('structural', "'%s' takes %d argument(s), the call passes %d" % (ids.def_name(fn[0]), want, have))
        else:
            for st in (to.split('|') if to else []):
                if not st:
                    return out.reject('structural', 'TO holds an empty stage name')
                if to_literal(st) is None:
                    return out.reject('structural', "stage '%s' cannot be written as a Ring string" % st)
    else:
        if attr in ('calls', 'writes', 'reads'):
            if p['kind'] not in BODY_KINDS:
                return out.reject('structural', "%s apply to BLOCK and FUNCTION points only, and '%s' is a %s" % (attr, p['name'], p['kind']))
            why = allowlist_error(g, p, attr, to)
            if why:
                return out.reject('structural', 'TO is not an allowlist of this program: ' + why)
        if attr in ('min', 'max') and not (p['kind'] == 'param' and form in ('num', 'neg')):
            return out.reject('structural', "bounds apply to numeric points only, and '%s' is not one" % p['name'])
        if attr == 'options' and p['kind'] not in ('algo', 'pipeline'):
            return out.reject('structural', "options apply to algo and pipeline points, and '%s' is a %s" % (p['name'], p['kind']))
        if attr in ('min', 'max') and to and not NUM_RE.match(to):
            return out.reject('structural', "TO '%s' is not a number" % to)
        if attr == 'risk' and to not in ('', '1', '2', '3', '4'):
            return out.reject('structural', "TO '%s' is not a risk tier from 1 to 4" % to)
        if attr == 'floor' and to != '' and to not in POSTURES:
            return out.reject('structural', "TO '%s' is not a posture" % to)
        if attr == 'options':
            parts = to.split('|') if to else []
            if not parts or any(not x for x in parts) or len(set(parts)) != len(parts):
                return out.reject('structural', "TO '%s' is not a list of distinct options" % to)
        if attr == 'governed_by' and to != '':
            if not NAME_RE.match(to):
                return out.reject('structural', "TO '%s' is not a governance name" % to)
            if to not in ctx:
                return out.reject('structural', "no governance '%s'" % to)
    out.passed('structural')
    out.value_from, out.value_to = frm, to
    # ---------------------------------------------------------------- constraint: the point's bounds and options, on the value proposed
    if revert is not None or 'constraint' in SKIP_STAGES:
        out.skipped('constraint')
    else:
        why = constraint(p, attr, frm, to)
        if why:
            return out.reject('constraint', why)
        out.passed('constraint')
    # the candidate: lower the sentence, apply it, and ask the language whether the result is still a program (a structural fact, asked once the
    # proposal is within its bounds: a value outside them may not be a change that can be made at all)
    try:
        if revert is not None:
            tx = copy.deepcopy(revert['inverse'])
        elif attr in ('min', 'max', 'risk', 'floor', 'calls', 'writes', 'reads'):
            tx = lower_attr(g, p, s)
        else:
            tx = lower(p, s)
        new, inv = apply_tx(g, tx)
    except TxError as e:
        return out.reject('structural', 'the change cannot be applied: %s' % e)
    if readback:
        text = text_of(new)
        try:
            back = parse_text(text)
        except Unreadable as e:
            return out.reject('structural', 'the refined program does not parse: %s' % e)
        if l1.norm(ids.strip(back)) != l1.norm(ids.strip(new)):
            return out.reject('structural', 'the refined program does not read back as itself')
    out.tx, out.inverse = tx, inv
    # ---------------------------------------------------------------- governance: before any change lands
    gname = p['attrs'].get('governed_by')
    if 'governance' in SKIP_STAGES or not gname:
        out.skipped('governance')
    else:
        tier = WIDEN_TIER if (attr and is_widening(p, attr, frm, to) and revert is None) else None
        why = governance(ctx, gname, s['author'], p, tier)
        if why:
            return out.reject('governance', why)
        out.passed('governance')
    # ---------------------------------------------------------------- trust: origin is not identity
    floor = p['attrs'].get('floor')
    need = POSTURES[floor] if floor else -1
    if attr:
        need = max(need, POSTURES[RULE_FLOOR])
    if 'trust' in SKIP_STAGES:
        out.skipped('trust')
    elif need >= 0 and POSTURES[s['posture']] < need:
        if attr:
            return out.reject('trust', "posture :%s below the required floor (%s) for rule refinements of '%s'" % (s['posture'], RULE_FLOOR, p['name']))
        return out.reject('trust', "posture :%s below the required floor for '%s'" % (s['posture'], p['name']))
    else:
        out.passed('trust')
    # ---------------------------------------------------------------- derivation: the state the change would leave
    if 'derivation' in SKIP_STAGES:
        out.skipped('derivation')
    else:
        L2 = lift(new)
        mine = "point '%s' " % p['name']
        bad2 = [e for e in L2['errors'] if not e['own'] or e['msg'].startswith(mine)]
        if bad2:
            e = bad2[0]
            return out.reject('derivation', ('own rule violated: ' if e['own'] else 'the declarations no longer lift: ') + e['msg'])
        r = rules_violated(L2, p['name'])
        if r:
            return out.reject('derivation', "rule '%s' violated -- %s" % (r['name'], r['message']))
        c = cascade(g, p) if attr is None and revert is None else {'reads': [], 'writes': []}
        out.cascade = c
        if 'cascade' in s:
            got = sorted(set(i for i, _ in c['reads']))
            if sorted(set(s['cascade'])) != got:
                return out.reject('derivation', "cascade stated %s but '%s' is read by %s" % (sorted(set(s['cascade'])), p['name'], got))
        out.passed('derivation')
    out.warnings = ['also assigned at id %d (%s)' % (i, o) for i, o in (out.cascade or {'writes': []})['writes']]
    out.status = 'flagged' if out.warnings else 'admitted'
    out.stage = 'all'
    out.graph = new
    out.why = "admitted: '%s' %s -> %s [:%s]" % (s['target'], frm, to, s['posture'])
    out.diff = diff_lines(text_of(g), text_of(new))
    return out


def constraint(p, attr, frm, to):
    if attr is None:
        if p['kind'] == 'param':
            a = p['attrs']
            if p['form'] in ('num', 'neg'):
                if 'min' in a and num(to) < num(a['min']):
                    return '%s below min %s' % (to, a['min'])
                if 'max' in a and num(to) > num(a['max']):
                    return '%s above max %s' % (to, a['max'])
            return None
        opts = p['attrs'].get('options', '')
        if p['kind'] == 'algo':
            if to not in opts.split('|'):
                return "'%s' not in options %s" % (to, opts)
            return None
        stages = to.split('|') if to else []
        if not stages:
            return 'pipeline would be empty'
        for st in stages:
            if st not in opts.split('|'):
                return "'%s' not in options %s" % (st, opts)
        for st in stages:
            if stages.count(st) > 1:
                return "'%s' appears twice" % st
        return None
    if attr in ('min', 'max'):
        other = p['attrs'].get('max' if attr == 'min' else 'min')
        if to and other:
            lo, hi = (to, other) if attr == 'min' else (other, to)
            if num(lo) > num(hi):
                return 'min %s would be above max %s' % (lo, hi)
    return None


def governance(ctx, gname, actor, p, tier):
    """StzGovernanceQ().MayProceed over the action `refine-<point>`: a declared risk tier, a permission, an authority that covers the tier."""
    gov = ctx.get(gname)
    action = 'refine-' + p['name']
    if gov is None:
        return "governance '%s' is not configured" % gname
    risk = p['attrs'].get('risk')
    if not risk:
        return "refused: '%s' has NO declared risk tier (undeclared actions never proceed)" % action
    need = tier or int(risk)
    who = gov.get(actor)
    if who is None or p['name'] not in who['may']:
        return "refused: '%s' lacks PERMISSION (can) for '%s'" % (actor, action)
    if who['level'] < need:
        return "refused: '%s' holds '%s' authority (level %d) but '%s' is risk tier %d (SHOULD does not cover it)" % (actor, who['name'], who['level'], action, need)
    return None


def diff_lines(a, b):
    return list(difflib.unified_diff(a.split('\n'), b.split('\n'), lineterm='', n=0))[2:]


# ---- the model: a program, its ids, its event log ------------------------------------------------------------------------------------

class Model:
    def __init__(self, text, ctx=None, unit=None):
        self.g = new_graph(text)
        self.ctx = ctx or {}
        # a LIBRARY file is refined through the program that loads it: {'root': its path, 'file': this file's path, 'natives': a list or None}
        self.unit = unit
        self.log = []
        self.base = text_of(self.g)

    def text(self):
        return text_of(self.g)

    def hash(self):
        return digest(self.text())

    def lift(self):
        with InUnit(self.unit):
            return lift(self.g)

    def event(self, seq):
        return self.log[seq - 1] if 1 <= seq <= len(self.log) else None

    def edit(self, text):
        """A human edit, made as text: the new graph gets the ids it keeps (rung 19); the edit is an event."""
        ng = parse_text(text)
        old = text_of(self.g)
        ids.carry(self.g, ng)
        self.g = ng
        self.log.append({'seq': len(self.log) + 1, 'kind': 'edit', 'admitted': True, 'text': text, 'pre': digest(old), 'post': self.hash()})

    def refine(self, sentence, ctx=None):
        s, why = parse_sentence(sentence) if isinstance(sentence, str) else (sentence, None)
        pre = self.hash()
        if s is None:
            out = Outcome(None)
            out.reject('structural', why)
            self.log.append({'seq': len(self.log) + 1, 'kind': 'refine', 'admitted': False, 'sentence': sentence, 'status': 'rejected', 'stage': 'structural',
                             'why': why, 'target': '', 'pre': pre, 'post': pre})
            return out
        with InUnit(self.unit):
            out = evaluate(self, s, self.ctx if ctx is None else ctx)
        ev = {'seq': len(self.log) + 1, 'kind': 'refine', 'admitted': out.admitted, 'sentence': s['text'], 'status': out.status, 'stage': out.stage,
              'why': out.why, 'target': s['target'], 'author': s['author'], 'posture': s['posture'], 'pre': pre}
        if out.admitted:
            self.g = out.graph
            ev.update({'tx': out.tx, 'inverse': out.inverse, 'value_from': out.value_from, 'value_to': out.value_to, 'point': s['base'], 'attr': s['attr']})
            if 'reverts' in s:
                ev['reverts'] = s['reverts']
                self.log[s['reverts'] - 1]['reverted_by'] = ev['seq']
        ev['post'] = self.hash()
        self.log.append(ev)
        out.event = ev
        return out

    def revert(self, n, author, posture='trusted', reason='a revert'):
        ev = self.event(n)
        s = sentence_text('revert_%d' % n, ev['target'], self.kind_of(ev), ev['value_to'], ev['value_from'], author, posture, reason, reverts=n)
        return self.refine(s)

    def kind_of(self, ev):
        p = point_named(self.lift(), ev['point'])
        return p['kind'] if p else 'param'

    def admitted(self):
        return [e for e in self.log if e['kind'] == 'refine' and e['admitted']]


def replay(text, log, ctx, unit=None):
    """The log run again from the base text, through the gate: the same verdicts and the same final text. -> (model, list of differences)"""
    m = Model(text, ctx, unit)
    bad = []
    for ev in log:
        if ev['kind'] == 'edit':
            m.edit(ev['text'])
            continue
        out = m.refine(ev['sentence'])
        if out.status != ev['status'] or out.stage != ev['stage'] or m.log[-1]['post'] != ev['post']:
            bad.append((ev['seq'], ev['status'], out.status))
    return m, bad


def replay_tx(text, log):
    """The same log without the gate: the transactions of the admitted events, applied in order. The engine alone is deterministic."""
    g = new_graph(text)
    for ev in log:
        if ev['kind'] == 'refine' and ev['admitted']:
            g, _ = apply_tx(g, ev['tx'], inplace=False)
    return g


# ---- commutation ------------------------------------------------------------------------------------------------------------------------

def footprint(model, s):
    """(reads, writes) of a sentence over the pieces of the model: the value of a point, its declaration (its rules), and -- because a derivation rule
    reads the post-state -- the value of every point that shares a rule with it."""
    with InUnit(model.unit):
        return _footprint(model, s)


def _footprint(model, s):
    L = model.lift()
    base = s['base']
    partners = set()
    for r in L['rules']:
        sides = {x for x in (r['left'], r['right']) if not NUM_RE.match(x)}
        if base in sides:
            partners |= sides
    partners.discard(base)
    if s['attr']:
        return ({('value', base)}, {('decl', base)})
    return ({('decl', base)} | {('value', q) for q in partners}, {('value', base)})


def commutes(model, s1, s2):
    r1, w1 = footprint(model, s1)
    r2, w2 = footprint(model, s2)
    return not (w1 & (r2 | w2) or w2 & r1)


# ---- the audit of a human edit ------------------------------------------------------------------------------------------------------

def audit(model, new_text, posture='trusted', author='text-edit'):
    """What an edit made as text amounts to. Each point whose value or tag changed is read back as the sentence that would have made the same change
    and judged by the gate on the OLD program; every other change is raw. -> (list of (sentence, outcome), the number of raw edits, the faults)"""
    with InUnit(model.unit):
        return _audit(model, new_text, posture, author)


def _audit(model, new_text, posture='trusted', author='text-edit'):
    ng = parse_text(new_text)
    og = copy.deepcopy(model.g)
    ids.carry(og, ng)
    L0, L1 = lift(model.g), lift(ng)
    faults = [e['msg'] for e in L1['errors'] if not e['own']]
    if faults:
        return [], None, faults     # a value outside its own bounds is exactly what the audit exists to judge; a tag that does not lift is not
    by_id = {p['id']: p for p in L1['points']}
    sentences, undone = [], copy.deepcopy(ng)
    for p in L0['points']:
        q = by_id.get(p['id'])
        if q is None or q['kind'] != p['kind'] or q['name'] != p['name']:
            continue
        if q['value'] != p['value'] and p['kind'] not in BODY_KINDS:   # a body edited by hand is the human's: a raw edit, not a sentence's
            sentences.append((p['name'], p['kind'], p['value'], q['value']))
        for k in set(p['attrs']) | set(q['attrs']):
            if k in RULE_ATTRS and p['attrs'].get(k, '') != q['attrs'].get(k, ''):
                sentences.append((p['name'] + '.' + k, p['kind'], p['attrs'].get(k, ''), q['attrs'].get(k, '')))
    # the raw edits: an item of the new program that is not the old one once the point changes are undone
    old_by_id = {it['_id']: it for it, *_ in walk_items(og)}
    for p in L0['points']:
        q = by_id.get(p['id'])
        if q is None:
            continue
        item = find_item(undone, p['id'])[0]
        if p['form'] in ('num', 'neg', 'str'):
            holder = get_path(item, p['path'][:-1])
            holder[p['path'][-1]] = copy.deepcopy(get_path(old_by_id[p['id']], p['path']))
        elif p['form'] == 'list':
            holder = get_path(item, p['path'][:-1])
            holder[p['path'][-1]] = copy.deepcopy(get_path(old_by_id[p['id']], p['path']))
        elif p['form'] == 'call':
            get_path(item, p['path'])['callee'] = copy.deepcopy(get_path(old_by_id[p['id']], p['path'])['callee'])
        car = p['carrier']
        cn = get_path(find_item(undone, car['id'])[0], car['path'])
        cn['text'] = get_path(old_by_id[car['id']], car['path'])['text']
        cn['kind'] = get_path(old_by_id[car['id']], car['path']).get('kind', cn.get('kind'))
    raw = 0
    now = {it['_id']: it for it, *_ in walk_items(undone)}
    for ident, it in old_by_id.items():
        n = now.get(ident)
        if n is None:
            raw += 1
        elif ids.strip(shallow(it)) != ids.strip(shallow(n)):
            raw += 1
    raw += sum(1 for ident in now if ident not in old_by_id)
    results = []
    for tgt, kind, frm, to in sentences:
        sent = sentence_text('audit', tgt, kind, frm, to, author, posture, 'a text edit, read back')
        s, why = parse_sentence(sent)
        results.append((tgt, frm, to, evaluate(model, s, model.ctx) if s else None))
    return results, raw, []


def shallow(it):
    """An item without the blocks inside it: the audit compares an item's own text; the items it holds are compared as items."""
    d = copy.deepcopy(it)
    for path, b in ids.blocks(d):
        get_path(d, path[:-1])[path[-1]] = []
    return d


# ---- the command line: `haro refine` at this rung -----------------------------------------------------------------------------------------------

def split_sentences(text):
    """The sentences of a .rfn-shaped file: each begins with DEFINE REFINE at the start of a line and runs to the next; `--` lines are comments."""
    out, cur = [], None
    for line in text.replace('\r\n', '\n').split('\n'):
        if line.startswith('--'):
            continue
        if line.startswith('DEFINE REFINE'):
            if cur is not None:
                out.append('\n'.join(cur))
            cur = [line]
        elif cur is not None:
            cur.append(line)
    if cur is not None:
        out.append('\n'.join(cur))
    return out


def main(argv):
    """python refine.py <program.ring> <sentences.rfn> [--ctx governance.txt] [--unit root.ring [--natives names.txt]] [--write]
    Each sentence goes through the gate in order, against what the earlier ones left. Prints the verdict, the primitives and the diff of each; exit 0 when every
    sentence was admitted, 1 when one was refused, 2 when the command could not run. `--write` replaces the program with the canonical text of the result --
    and refuses to when the program is not already its own canonical text, because the diff would then carry layout the refinement did not make (rnxc fmt
    --write first; never on a tree that is not yours to reformat). `--unit` refines a LIBRARY file through the program that loads it (D32): the
    derivation checks that program's unit with the file's text replaced, and `--natives` lists the names its native libraries register."""
    args = [a for a in argv if not a.startswith('--')]
    write = '--write' in argv
    ctxfile = None
    if '--ctx' in argv:
        ctxfile = argv[argv.index('--ctx') + 1]
        args = [a for a in args if a != ctxfile]
    unit = None
    if '--unit' in argv:
        root = argv[argv.index('--unit') + 1]
        args = [a for a in args if a != root]
        nat = None
        if '--natives' in argv:
            nat = argv[argv.index('--natives') + 1]
            args = [a for a in args if a != nat]
            nat = os.path.abspath(nat)
        unit = {'root': os.path.abspath(root), 'file': os.path.abspath(args[0]) if args else '', 'natives': nat}
    if len(args) != 2:
        print(main.__doc__)
        return 2
    prog = open(args[0], 'rb').read().decode('latin-1')
    try:
        m = Model(prog, parse_context(open(ctxfile, 'rb').read().decode('latin-1')) if ctxfile else {}, unit)
    except Unreadable as e:
        print('the program does not parse: %s' % e)
        return 2
    if write and m.text() != prog.replace('\r\n', '\n'):
        print('refused: %s is not its own canonical text, so a written result would carry layout changes no refinement made; run `rnxc fmt --write` on it first' % args[0])
        return 2
    sents = split_sentences(open(args[1], 'rb').read().decode('latin-1'))
    if not sents:
        print('no sentence in %s' % args[1])
        return 2
    rc = 0
    for text in sents:
        o = m.refine(text)
        print('%s %s' % (o.status, ('' if o.status != 'rejected' else o.stage + ': ') + o.why))
        if o.admitted:
            print('  lowered to: ' + ', '.join(p['op'] for p in o.tx))
            for w in o.warnings:
                print('  warning: ' + w)
            for ln in o.diff:
                print('  ' + ln)
        else:
            rc = 1
    if write and m.admitted():
        open(args[0], 'wb').write(m.text().encode('latin-1'))
        print('wrote %s (%d event(s))' % (args[0], len(m.admitted())))
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
