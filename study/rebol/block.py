"""The one LOAD (COMPASS-REBOL-06): C6 text and the memo spelling read into one block of typed values, and the canonical
printing of a block in each spelling. A reference model in Python, judged by printing_fixtures.json (written first).

A value is a tuple:
  ('word', 'tones')   ('kw', 'DEFINE')   ('str', 'text')   ('num', '3')   ('path', ('a', 'b'))
  ('pair', key, value)        key a word, a keyword, a path, or a string (a memo key that is no C6 identifier)
  ('list', [items])  ('group', [items])  ('row', [values])  ('comment', 'text')  ('opt', value) -- Haro's `?`, a seat
  that may be absent (`name?`, `[intents]?`), which C6's lexis does not have
A list or group holds ITEMS separated by commas: an item of one value is that value, an item of several is a ROW.
Comments are values in the sequence that holds them; a comment inside a row is moved after the row (the one named loss
besides layout).

  python block.py            runs printing_fixtures.json and prints a verdict per fixture
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


class Refused(Exception):
    pass


# a proposed C6 amendment, measured and not adopted: a doubled quote inside a string is one quote (SQL's and CSV's
# convention, no backslash). Off, a string holding a quote has no C6 printing, as C6 v1.0 says.
DOUBLED_QUOTE = False


# ---- C6: tokens -----------------------------------------------------------------------------------------------------

IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
NUMBER = re.compile(r'-?[0-9]+(\.[0-9]+)?')


def is_keyword(w):
    return any(c.isupper() for c in w) and not any(c.islower() for c in w)


def tokens(text):
    """C6's lexis (ringua/docs/commons.md 3.1-3.6): -- comments, double-quoted strings folding their continuation indent,
    numbers, identifiers and keywords, paths, and the punctuation of lists, groups and pairs."""
    s = text.replace('\r\n', '\n').replace('\r', '\n')
    out, i, n, line = [], 0, len(s), 1
    while i < n:
        c = s[i]
        if c == '\n':
            line += 1; i += 1; continue
        if c in ' \t﻿':
            i += 1; continue
        if s.startswith('--', i):
            j = s.find('\n', i)
            j = n if j < 0 else j
            out.append(('comment', s[i + 2:j].strip(), line)); i = j; continue
        if c == '"':
            j = s.find('"', i + 1)
            while DOUBLED_QUOTE and j >= 0 and j + 1 < n and s[j + 1] == '"':
                j = s.find('"', j + 2)
            if j < 0:
                raise Refused(f'line {line}: a string not closed')
            raw = s[i + 1:j]
            if DOUBLED_QUOTE:
                raw = raw.replace('""', '"')
            line += raw.count('\n')
            out.append(('str', re.sub(r'\n[ \t]*', ' ', raw), line)); i = j + 1; continue
        if c == "'":
            raise Refused(f"line {line}: a single quote; C6 strings are double-quoted (.zql's D-ZQL-1 is a divergence)")
        mnum = NUMBER.match(s, i)
        if mnum and (c != '-' or (i + 1 < n and s[i + 1].isdigit())):
            out.append(('num', mnum.group(0), line)); i = mnum.end(); continue
        mid = IDENT.match(s, i)
        if mid:
            parts, j = [mid.group(0)], mid.end()
            while j < n and s[j] == '.' and IDENT.match(s, j + 1):
                m2 = IDENT.match(s, j + 1); parts.append(m2.group(0)); j = m2.end()
            if len(parts) > 1:
                out.append(('path', tuple(parts), line))
            else:
                w = parts[0]
                out.append(('kw' if is_keyword(w) else 'word', w, line))
            i = j; continue
        if c in '[](),:?':
            out.append((c, c, line)); i += 1; continue
        raise Refused(f"line {line}: unexpected '{c}'")
    return out


# ---- C6: the block ----------------------------------------------------------------------------------------------------

def load(text):
    """C6 text -> the top-level sequence of values."""
    toks = tokens(text)
    pos = [0]

    def peek(k=0):
        j = pos[0] + k
        return toks[j] if j < len(toks) else ('eof', '', toks[-1][2] if toks else 1)

    def value():
        v = value1()
        while peek()[0] == '?':
            pos[0] += 1
            v = ('opt', v)
        return v

    def value1():
        t = peek()
        if t[0] in ('word', 'kw', 'path', 'str') and peek(1)[0] == ':':
            pos[0] += 2
            key = (t[0], t[1])
            if peek()[0] in (',', ')', ']', 'eof'):
                raise Refused(f'line {t[2]}: a pair with no value after {t[1]}:')
            return ('pair', key, value())
        pos[0] += 1
        if t[0] in ('word', 'kw', 'str', 'num', 'path'):
            return (t[0], t[1])
        if t[0] in ('[', '('):
            close = ']' if t[0] == '[' else ')'
            return ('list' if t[0] == '[' else 'group', container(close, t[2]))
        if t[0] == ',':
            raise Refused(f'line {t[2]}: a comma outside a list or a group')
        if t[0] == 'eof':
            raise Refused(f'line {t[2]}: the text ends inside a value')
        raise Refused(f"line {t[2]}: unexpected '{t[1]}'")

    def container(close, line0):
        items, seg = [], []

        def flush():
            vals = [v for v in seg if v[0] != 'comment']
            lead, trail, seen = [], [], False
            for v in seg:
                if v[0] == 'comment':
                    (trail if seen else lead).append(v)
                else:
                    seen = True
            items.extend(lead)
            if len(vals) == 1:
                items.append(vals[0])
            elif vals:
                items.append(('row', vals))
            items.extend(trail)
            seg.clear()

        while True:
            t = peek()
            if t[0] == 'eof':
                raise Refused(f"line {line0}: a {'list' if close == ']' else 'group'} not closed")
            if t[0] == close:
                pos[0] += 1; flush(); return items
            if t[0] == ',':
                pos[0] += 1
                if not [v for v in seg if v[0] != 'comment']:
                    raise Refused(f'line {t[2]}: an empty item before a comma')
                flush(); continue
            if t[0] == 'comment':
                pos[0] += 1; seg.append(('comment', t[1])); continue
            seg.append(value())

    out = []
    while peek()[0] != 'eof':
        if peek()[0] == 'comment':
            out.append(('comment', peek()[1])); pos[0] += 1; continue
        out.append(value())
    return out


# ---- C6: the canonical printing ---------------------------------------------------------------------------------------

def pv(v, ind=0):
    k = v[0]
    if k in ('word', 'kw', 'num'):
        return v[1]
    if k == 'str':
        if '"' in v[1] and DOUBLED_QUOTE:
            return '"' + v[1].replace('"', '""') + '"'
        if '"' in v[1]:
            raise Refused('a string holding a double quote has no C6 printing (C6 strings have no escape)')
        return '"' + v[1] + '"'
    if k == 'path':
        return '.'.join(v[1])
    if k == 'pair':
        key = v[1]
        return (pv(key) if key[0] != 'path' else '.'.join(key[1])) + ': ' + pv(v[2], ind)
    if k == 'row':
        return ' '.join(pv(x, ind) for x in v[1])
    if k == 'opt':
        return pv(v[1], ind) + '?'
    if k == 'comment':
        return '-- ' + v[1] if v[1] else '--'
    if k == 'list':
        if not v[1]:
            return '[]'
        if any(x[0] in ('comment', 'group') for x in v[1]):
            return '[' + block_lines(v[1], ind) + ']'
        return '[' + ', '.join(pv(x, ind) for x in v[1]) + ']'
    if k == 'group':
        return '()' if not v[1] else '(' + block_lines(v[1], ind) + ')'
    raise ValueError(k)


def block_lines(items, ind):
    pad = ' ' * (ind + 2)
    real = [j for j, x in enumerate(items) if x[0] != 'comment']
    lines = []
    for j, x in enumerate(items):
        comma = ',' if x[0] != 'comment' and j != real[-1] else ''
        lines.append(pad + pv(x, ind + 2) + comma)
    return '\n' + '\n'.join(lines) + '\n' + ' ' * ind


def print_c6(vals):
    """One spelling per block: a declaration (DEFINE ...) per paragraph, a blank line between; anything else a line."""
    paras, cur = [], []
    for v in vals:
        if v == ('kw', 'DEFINE') and cur:
            paras.append(cur); cur = []
        if v[0] == 'comment':
            # a comment ends its line: it never shares one with what follows it
            if cur:
                paras.append(cur); cur = []
            paras.append([v]); continue
        cur.append(v)
    if cur:
        paras.append(cur)
    return '\n'.join(' '.join(pv(v) for v in p) + '\n' for p in paras)


# ---- the memo spelling: _StzOutputParseMemo, ported line for line --------------------------------------------------------

def _colon_at(line):
    at = line.find(':')
    if at < 1:
        return -1
    key = line[:at]
    if ' ' in key or '/' in key:
        return -1
    if len(line) > at + 1 and line[at + 1] != ' ':
        return -1
    return at


def _unquote(v):
    c = v.strip()
    if len(c) >= 2 and ((c[0] == '"' and c[-1] == '"') or (c[0] == "'" and c[-1] == "'")):
        return c[1:-1]
    return c


C6_IDENT = re.compile(r'[a-z_][a-z0-9_]*\Z')


def _key(k):
    if C6_IDENT.match(k):
        return ('word', k)
    if re.fullmatch(r'[A-Z][A-Z0-9_]*', k):
        return ('kw', k)
    return ('str', k)


def _colon_at_house(line):
    """The house memo's field: the text before the first colon that a space or the line's end follows; it may hold spaces
    (`the page: version 1`), which C9's reader refuses."""
    for at, c in enumerate(line):
        if c == ':' and (at + 1 == len(line) or line[at + 1] == ' '):
            return at if line[:at].strip() and not line.startswith('- ') else -1
    return -1


def _fold(L):
    """The house memo's continuation: a line deeper than a line that holds a scalar, which is not a list item, continues
    that scalar -- except under a list element's first field (`- name: x`), where a deeper `key: value` is its next field."""
    out = []
    for n, t in L:
        if out and n > out[-1][0] and not (t.startswith('- ') or t == '-'):
            pn, pt = out[-1]
            if pt.startswith('- '):
                rest = pt[2:].strip()
                at = _colon_at(rest)
                holds = at < 0 or rest[at + 1:].strip() != ''
                sibling = at >= 0 and _colon_at(t) >= 0
            else:
                at = _colon_at_house(pt)
                holds = at >= 0 and pt[at + 1:].strip() != ''
                sibling = False
            if holds and not sibling:
                out[-1] = (pn, pt + ' ' + t)
                continue
        out.append((n, t))
    return out


def load_memo(text, house=False):
    """The memo spelling -> one group of pairs (a map), as _StzOutputParseMemo reads it: every scalar a string."""
    L = []
    for ln in text.replace('\r', '').split('\n'):
        ln = ln.replace('\t', '    ')
        t = ln.strip()
        if not t or t.startswith('#') or t.startswith('```'):
            continue
        L.append((len(ln) - len(ln.lstrip(' ')), t))
    if house:
        L = _fold(L)
    if not L:
        raise Refused('the memo says nothing readable')
    if L[0][1].startswith('- '):
        raise Refused('the memo is a bare list; a structure must open with named fields')

    def mmap(i, ind):
        out = []
        while i < len(L):
            n, ln = L[i]
            if n < ind:
                break
            if n > ind:
                raise Refused(f"unexpected indentation before '{ln}'")
            if ln.startswith('- ') or ln == '-':
                break
            at = _colon_at_house(ln) if house else _colon_at(ln)
            if at < 0:
                raise Refused(f"'{ln}' is not a 'field: value' line")
            key, val = ln[:at].strip(), ln[at + 1:].strip()
            if val:
                out.append(('pair', _key(key), ('str', _unquote(val)))); i += 1; continue
            if i == len(L) - 1 or L[i + 1][0] <= ind:
                out.append(('pair', _key(key), ('str', ''))); i += 1; continue
            deep = L[i + 1][0]
            first = L[i + 1][1]
            if house and not (first.startswith('- ') or first == '-') and _colon_at_house(first) < 0:
                # the house memo's prose block: a deeper paragraph under `key:` is the key's text
                j, text = i + 1, []
                while j < len(L) and L[j][0] > ind:
                    text.append(L[j][1]); j += 1
                out.append(('pair', _key(key), ('str', ' '.join(text)))); i = j; continue
            if L[i + 1][1].startswith('- ') or L[i + 1][1] == '-':
                sub, i = mlist(i + 1, deep)
            else:
                sub, i = mmap(i + 1, deep)
                sub = ('group', sub)
            out.append(('pair', _key(key), sub))
        return out, i

    def mlist(i, ind):
        out = []
        while i < len(L):
            n, ln = L[i]
            if n < ind:
                break
            if n > ind:
                raise Refused(f"unexpected indentation before '{ln}'")
            if not (ln.startswith('- ') or ln == '-'):
                break
            rest = '' if ln == '-' else ln[2:].strip()
            i += 1
            at = _colon_at(rest) if rest else -1
            if rest and at < 0:
                out.append(('str', _unquote(rest))); continue
            elem = []
            if at >= 0:
                elem.append(('pair', _key(rest[:at].strip()), ('str', _unquote(rest[at + 1:].strip()))))
            if i < len(L) and L[i][0] > ind:
                more, i = mmap(i, L[i][0])
                elem.extend(more)
            if not elem:
                raise Refused('a list item is empty')
            out.append(('group', elem))
        return ('list', out), i

    vals, i = mmap(0, L[0][0])
    if i < len(L):
        raise Refused(f"unexpected '{L[i][1]}'")
    return [('group', vals)]


def print_memo(vals):
    """A group of pairs in the memo spelling: key: value; key: then a deeper block; - for a list item."""
    if len(vals) != 1 or vals[0][0] != 'group':
        raise Refused('only a group of pairs has a memo printing')
    out = []

    def scalar(v, in_list=False):
        if v[0] != 'str':
            raise Refused(f'a {v[0]} has no memo printing: every memo scalar is a string')
        s = v[1]
        if s != s.strip() or (s[:1] in '"\'' and s[-1:] in '"\'' and len(s) >= 2) or (in_list and _colon_at(s) >= 0) or s.startswith('- ') \
                or s.startswith('#') or s.startswith('```') or s == '-':
            return '"' + s + '"'
        return s

    def keytext(k):
        return k[1] if k[0] in ('word', 'kw', 'str') else '.'.join(k[1])

    def pairs(items, ind):
        for p in items:
            if p[0] != 'pair':
                raise Refused(f'a {p[0]} inside a map has no memo printing')
            k, v = keytext(p[1]), p[2]
            if v[0] == 'str':
                out.append(' ' * ind + k + ':' + (' ' + scalar(v) if v[1] != '' else ''))
            elif v[0] == 'group':
                if not v[1]:
                    raise Refused('an empty map has no memo printing')
                out.append(' ' * ind + k + ':'); pairs(v[1], ind + 2)
            elif v[0] == 'list':
                if not v[1]:
                    raise Refused('an empty list has no memo printing')
                out.append(' ' * ind + k + ':'); items_(v[1], ind + 2)
            else:
                raise Refused(f'a {v[0]} has no memo printing')

    def items_(items, ind):
        for it in items:
            if it[0] == 'group':
                if not it[1]:
                    raise Refused('an empty list item has no memo printing')
                first, rest = it[1][0], it[1][1:]
                if first[0] != 'pair' or first[2][0] != 'str':
                    raise Refused('a list item that opens with a block has no memo printing')
                out.append(' ' * ind + '- ' + keytext(first[1]) + ':' + (' ' + scalar(first[2]) if first[2][1] != '' else ''))
                pairs(rest, ind + 2)
            else:
                out.append(' ' * ind + '- ' + scalar(it, True))

    pairs(vals[0][1], 0)
    return '\n'.join(out) + '\n'


def load_as(text, spelling):
    if spelling in ('memo', 'house'):
        return load_memo(text, spelling == 'house')
    return load(text)


# ---- the court of the printing fixtures -----------------------------------------------------------------------------------

def court(path=os.path.join(HERE, 'printing_fixtures.json')):
    doc = json.load(open(path, encoding='utf-8'))
    ok = bad = 0

    def verdict(fid, good, why=''):
        nonlocal ok, bad
        if good:
            ok += 1
        else:
            bad += 1
        print(('  ok   ' + fid) if good else ('  FAIL ' + fid + (' -- ' + why if why else '')))

    for f in doc['same']:
        try:
            a, b = load_as(f['a'], f.get('a_spelling', 'c6')), load_as(f['b'], f.get('b_spelling', 'c6'))
            verdict(f['id'], a == b, '' if a == b else f'{a} != {b}')
        except Refused as e:
            verdict(f['id'], False, 'refused: ' + str(e))
    for f in doc['differ']:
        try:
            a, b = load_as(f['a'], f.get('a_spelling', 'c6')), load_as(f['b'], f.get('b_spelling', 'c6'))
            verdict(f['id'], a != b, 'loaded equal')
        except Refused as e:
            verdict(f['id'], False, 'refused: ' + str(e))
    for f in doc['canonical']:
        try:
            vals = load(f['text'])
            got = print_memo(vals) if f.get('spelling') == 'memo' else print_c6(vals)
            verdict(f['id'], got == f['canonical'], repr(got))
        except Refused as e:
            verdict(f['id'], False, 'refused: ' + str(e))
    for f in doc['refused']:
        try:
            load_as(f['text'], f.get('spelling', 'c6'))
            verdict(f['id'], False, 'accepted, must refuse')
        except Refused as e:
            verdict(f['id'], f['why'] in str(e), str(e))
    print(f'PRINTING COURT: {ok} of {ok + bad} fixtures hold')
    return bad


if __name__ == '__main__':
    sys.exit(1 if court() else 0)
