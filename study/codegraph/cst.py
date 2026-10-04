"""cst.py -- a lossless concrete syntax tree of a Ring file, recovered from `rnxc dump` and the source.

`rnxc dump` prints the tree-sitter parse of a file, one node a line, and it is LOSSY in four ways this module
measures and repairs: a leaf's text is shown only up to 40 bytes, a newline inside a leaf is shown as a backslash, an
interior node has no text and no position, and a few tokens the grammar hides (the `(` of a parameter list among them)
are not nodes at all. The tree is recovered by walking the leaves in source order against the source bytes: a long leaf
is read off the source by its kind, and what lies between two leaves is either layout (whitespace and `;`, which the
grammar declares extras) or a HIDDEN token, recorded with the leaf it follows. Everything is read as latin-1, so one
character is one byte and positions are byte positions.

The module reports what it could not place: a gap that is neither layout nor a recognised hidden token, a leaf it
could not find in the source. A file with one is not measured; it is counted and named.
"""
import os, re, subprocess

RNXC = os.environ.get('RNXC', r'D:\GitHub\ringpp\zig-out\bin\rnxc.exe')
LINE = re.compile(r"^( *)(\S+)(?:  '(.*)')?$")
LAYOUT = ' \t\r\n;'
WORD = re.compile(r"[^\s;\"'`#+*/%.,()=<>!\[\]{}:&|~^?-]+")


class Node:
    __slots__ = ('kind', 'text', 'kids', 'parent', 'start', 'end', 'hidden_before')

    def __init__(self, kind, text, parent):
        self.kind, self.text, self.kids, self.parent = kind, text, [], parent
        self.start = self.end = -1
        self.hidden_before = []          # hidden tokens (text) between the previous leaf and this one

    def leaves(self):
        if not self.kids:
            yield self
        for k in self.kids:
            yield from k.leaves()


def read_bytes(path):
    return open(path, 'rb').read().decode('latin-1')


def parse_dump(dump):
    root, stack, has_error = None, [], False
    for raw in dump.split('\n'):
        if not raw.strip():
            continue
        m = LINE.match(raw)
        if not m:
            raise ValueError('cannot read a dump line: ' + repr(raw[:60]))
        depth = len(m.group(1)) // 2
        node = Node(m.group(2), m.group(3), None)
        if node.kind in ('ERROR', 'MISSING'):
            has_error = True
        del stack[depth:]
        if stack:
            node.parent = stack[-1]
            stack[-1].kids.append(node)
        else:
            root = node
        stack.append(node)
    return root, has_error


def scan_long(src, kind, pos):
    """The text of a leaf the dump did not show, read off the source: the first token of its kind at or after pos."""
    if kind == 'string':
        m = re.compile(r"[\"'`]").search(src, pos)
        if m:
            end = src.find(m.group(0), m.end())
            if end >= 0:
                return m.start(), end + 1
    if kind == 'comment':
        for m in re.compile(r'#|//|/\*').finditer(src, pos):
            if m.group(0) == '/*':
                end = src.find('*/', m.end())
                return (m.start(), end + 2) if end >= 0 else None
            eol = re.compile(r'[\r\n]').search(src, m.end())
            return m.start(), (eol.start() if eol else len(src))
    m = WORD.search(src, pos)
    return (m.start(), m.end()) if m else None


def locate(src, leaf, pos):
    """(start, end) of a leaf at or after pos, or None."""
    t = leaf.text
    if t is None:
        return scan_long(src, leaf.kind, pos)
    if '\\' in t:                          # a backslash in a dump may be a folded newline
        pat = re.compile(''.join('[\\\\\r\n]' if c == '\\' else re.escape(c) for c in t))
        m = pat.search(src, pos)
        return (m.start(), m.end()) if m else None
    i = src.find(t, pos)
    return (i, i + len(t)) if i >= 0 else None


def recover(path):
    """-> (root, src, report). The report names what could not be placed; an empty `bad` is a measured file."""
    src = read_bytes(path)
    r = subprocess.run([RNXC, 'dump', path], capture_output=True, timeout=300, env=dict(os.environ, RNXC_NOCACHE='1'))
    root, has_error = parse_dump(r.stdout.decode('latin-1'))
    rep = {'error': has_error, 'bad': [], 'leaves': 0, 'hidden': {}}
    if root is None or has_error:
        return root, src, rep
    pos = 0
    for leaf in root.leaves():
        rep['leaves'] += 1
        loc = locate(src, leaf, pos)
        if loc is None:
            rep['bad'].append(('leaf not found', leaf.kind, (leaf.text or '')[:20], pos))
            return root, src, rep
        s, e = loc
        # the string content between the quotes of a string that has children is verbatim, not layout
        gap = src[pos:s]
        inside_string = leaf.parent is not None and leaf.parent.kind == 'string' and leaf.parent.kids and leaf is leaf.parent.kids[-1]
        if inside_string:
            leaf.hidden_before = [gap] if gap else []
            if gap:
                rep['hidden']['<string content>'] = rep['hidden'].get('<string content>', 0) + 1
        else:
            for tok in re.findall(r'[^\s;]+', gap):
                leaf.hidden_before.append(tok)
                rep['hidden'][tok] = rep['hidden'].get(tok, 0) + 1
        leaf.start, leaf.end = s, e
        leaf.text = src[s:e]
        pos = e
    tail = src[pos:]
    if tail.strip(LAYOUT):
        rep['bad'].append(('text after the last leaf', tail.strip()[:30], '', pos))
    return root, src, rep


if __name__ == '__main__':
    import sys, json
    root, src, rep = recover(sys.argv[1])
    print(json.dumps({k: v for k, v in rep.items() if k != 'bad'}, indent=1)[:600], rep['bad'][:3])
