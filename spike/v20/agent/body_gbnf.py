"""body_gbnf.py -- the write surface of a BODY, scoped to its point: the GBNF of the statement lists an agent may write for a BLOCK or FUNCTION point, in two shapes.

    body_grammar(calls, writes)   ONE line: statements separated by single spaces -- the shape of the sentence's TO
    lines_grammar(calls, writes)  the same body as an agent writes it naturally: a statement a line, blocks indented a tab a level, a closing sentinel line
                                  python body_gbnf.py "len|floor" '$nCount'    prints the one-line grammar and its rule count

Rung 5's scoped grammar (`scoped.py`) fixes the sentence around a body -- the point, the kind, the digest FROM -- and leaves TO as `qbody`: one line of free text, "for the
compiler's parser and the gate's allowlists". So the decoder guaranteed the envelope and nothing about the body. These grammars say what a context-free grammar can say of the body
itself, and say it for THIS point:
  - no double quote (a sentence has no escape, F-55: text is 'single-quoted'), no comment
  - a statement list and nothing else: assignment, `+=` `-=` `*=` `/=`, `++` `--`, `return`, `if ... else ... ok`, `for i = a to b [step c] ... next`, `for x in list ... next`,
    `while ... end`, a call -- no `func`, no `class`, no `load`, no brace, no `eval`, no `call` by name: none has a production
  - a call is one of the point's `calls`, spelt as declared (D24); with none declared the body has no call at all
  - a write outside the frame is one of the point's `writes`: an assignment target is a local name, an indexed element, or one of those global/attribute names
  - a READ of a global or an attribute is one of the point's `reads` or `writes` (what a body may write it may read): a `$x` or `@x` that is neither has no production
What no context-free grammar says stays the gate's: that a callee takes that many arguments, that a name is assigned before it is read, that the text is read by Ring as the
statements it means (the gate reads it back through the compiler's parser and compares the graphs).

The decoder holds at most 128 rules and makes every group and every repeat a rule of its own; the count is checked here. The one-line body ends with a newline, after which the grammar is
complete; the multi-line body ends with a sentinel line (a grammar that may always take one more statement never tells a small model it is finished).
"""
import re, sys


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def expr_rules(cl, rl=()):
    """The expression rules both shapes share: Ring's precedence, `not` over one comparison chain, the point's calls and nothing else that calls, and a global or an attribute only
    when it is one of `rl` (the point's reads and writes)."""
    R = []

    def rule(name, body):
        R.append('%s ::= %s' % (name, body))

    rule('expr', 'andx (" or " andx)*')
    rule('andx', 'notx (" and " notx)*')
    rule('notx', '"not " eqx | eqx')
    rule('eqx', 'cmp ((" = " | " != ") cmp)*')
    rule('cmp', 'arith ((" <= " | " >= " | " < " | " > ") arith)?')
    rule('arith', 'term ((" + " | " - ") term)*')
    rule('term', 'factor ((" * " | " / " | " % ") factor)*')
    rule('factor', '"-" factor | atom')
    atoms = ['num', 'str', 'ref', '"[" args? "]"', '"(" expr ")"']
    if cl:
        atoms.insert(2, 'call')
    rule('atom', ' | '.join(atoms))
    if rl:
        rule('ref', 'gref | id ("[" expr "]")*')
        rule('gref', '(' + ' | '.join(lit(r) for r in rl) + ') ("[" expr "]")*')
    else:
        rule('ref', 'id ("[" expr "]")*')
    if cl:
        rule('call', '(' + ' | '.join(lit(c) for c in cl) + ') "(" args? ")"')
    rule('args', 'expr (", " expr)*')
    rule('id', '[A-Za-z_] [A-Za-z0-9_]*')
    rule('num', '[0-9]+ ("." [0-9]+)?')
    rule('str', "\"'\" [^'\"\\n]* \"'\"")
    return R


def targets(wl):
    R = ['tgt ::= lval' + (' | wtgt' if wl else ''), 'lval ::= id ("[" expr "]")*']
    if wl:
        R.append('wtgt ::= (' + ' | '.join(lit(w) for w in wl) + ') ("[" expr "]")*')
    return R


def readable(writes='', reads=''):
    """What a body may read of the world outside its frame: its `reads` and its `writes`, each once, in the order declared."""
    out = []
    for n in [x for x in (reads or '').split('|') if x] + [x for x in (writes or '').split('|') if x]:
        if n[:1] in ('$', '@') and n not in out:
            out.append(n)
    return out


def body_grammar(calls='', writes='', reads=''):
    cl = [c for c in (calls or '').split('|') if c]
    wl = [w for w in (writes or '').split('|') if w]
    rl = readable(writes, reads)
    R = []

    def rule(name, body):
        R.append('%s ::= %s' % (name, body))

    rule('root', 'stmts "\\n"')
    rule('stmts', 'stmt (" " stmt)*')
    stmts = ['asg', 'aug', 'inc', 'ret', 'ifs', 'fors', 'forin', 'whl']
    if cl:
        stmts.append('call')
    rule('stmt', ' | '.join(stmts))
    rule('asg', 'tgt " = " expr')
    rule('aug', 'tgt (" += " | " -= " | " *= " | " /= ") expr')
    rule('inc', 'tgt ("++" | "--")')
    rule('ret', '"return" (" " expr)?')
    rule('ifs', '"if " expr " " stmts (" else " stmts)? " ok"')
    rule('fors', '"for " id " = " expr " to " expr (" step " expr)? " " stmts " next"')
    rule('forin', '"for " id " in " expr " " stmts " next"')
    rule('whl', '"while " expr " " stmts " end"')
    R.extend(targets(wl))
    R.extend(expr_rules(cl, rl))
    return '\n'.join(R) + '\n'


def lines_grammar(calls='', writes='', depth=3, sentinel='<<END>>', reads=''):
    """The same body as lines: a statement a line, a block indented a tab a level (counted by named rules, to `depth` levels below the top), then the sentinel line."""
    cl = [c for c in (calls or '').split('|') if c]
    wl = [w for w in (writes or '').split('|') if w]
    rl = readable(writes, reads)
    R = []

    def rule(name, body):
        R.append('%s ::= %s' % (name, body))

    NL = '"\\n"'
    rule('root', 's0+ ' + lit(sentinel + '\n'))
    for d in range(1, depth + 1):
        rule('i%d' % d, '"\\t"' if d == 1 else 'i%d "\\t"' % (d - 1))
    rule('simple', ' | '.join(['asg', 'aug', 'inc', 'ret'] + (['call'] if cl else [])))
    rule('asg', 'tgt " = " expr')
    rule('aug', 'tgt (" += " | " -= " | " *= " | " /= ") expr')
    rule('inc', 'tgt ("++" | "--")')
    rule('ret', '"return" (" " expr)?')
    for d in range(0, depth + 1):
        pre = ('i%d ' % d) if d else ''
        if d < depth:
            n = 'b%d' % (d + 1)
            rule('s%d' % d, pre + 'simple ' + NL +
                 ' | ' + pre + '"if " expr ' + NL + ' ' + n + ' (' + pre + '"else" ' + NL + ' ' + n + ')? ' + pre + '"ok" ' + NL +
                 ' | ' + pre + '"for " id " = " expr " to " expr (" step " expr)? ' + NL + ' ' + n + ' ' + pre + '"next" ' + NL +
                 ' | ' + pre + '"for " id " in " expr ' + NL + ' ' + n + ' ' + pre + '"next" ' + NL +
                 ' | ' + pre + '"while " expr ' + NL + ' ' + n + ' ' + pre + '"end" ' + NL)
            rule('b%d' % (d + 1), '(s%d)+' % (d + 1))
        else:
            rule('s%d' % d, pre + 'simple ' + NL)
    R.extend(targets(wl))
    R.extend(expr_rules(cl, rl))
    return '\n'.join(R) + '\n'


def flatten(text, sentinel='<<END>>'):
    """The lines an agent wrote, as the one line TO carries: the sentinel and anything after it dropped, each line stripped, joined with single spaces."""
    text = text.replace('\r\n', '\n')
    if sentinel in text:
        text = text.split(sentinel)[0]
    return ' '.join(l.strip() for l in text.split('\n') if l.strip())


def rule_count(text):
    named = len(re.findall(r'^\w+ ::=', text, re.M))
    body = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    body = re.sub(r'\[(?:[^\]\\]|\\.)*\]', 'C', body)
    return named + body.count('(') + len(re.findall(r'[\)\w"\]C][*+?]', body))


if __name__ == '__main__':
    g = body_grammar(*(sys.argv[1:3] + [''] * 2)[:2])
    print(g)
    print('# %d named rules, about %d by the decoder\'s count' % (len(re.findall(r'^\w+ ::=', g, re.M)), rule_count(g)), file=sys.stderr)
