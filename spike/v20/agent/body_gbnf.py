"""body_gbnf.py -- the write surface of a BODY, scoped to its point: the GBNF of the one-line statement lists an agent may write for a BLOCK or FUNCTION point.

    body_grammar(calls, writes) -> the grammar text        python body_gbnf.py "len|floor" '$nCount'    prints it and its rule count

Rung 5's scoped grammar (`scoped.py`) fixes the sentence around a body -- the point, the kind, the digest FROM -- and leaves TO as `qbody`: one line of free text, "for the
compiler's parser and the gate's allowlists". So the decoder guaranteed the envelope and nothing about the body. This grammar says what a context-free grammar can say of the body
itself, and says it for THIS point:
  - one line: statements separated by single spaces, no line break, no double quote (a sentence has no escape, F-55: text is 'single-quoted'), no comment
  - a statement list and nothing else: assignment, `+=` `-=` `*=` `/=`, `++` `--`, `return`, `if ... else ... ok`, `for i = a to b [step c] ... next`, `for x in list ... next`,
    `while ... end`, a call -- no `func`, no `class`, no `load`, no brace, no `eval`, no `call` by name: none has a production
  - a call is one of the point's `calls`, spelt as declared (D24); with none declared the body has no call at all
  - a write outside the frame is one of the point's `writes`: an assignment target is a local name, an indexed element, or one of those global/attribute names
What no context-free grammar says stays the gate's: that a callee takes that many arguments, that a name is assigned before it is read, that the one-line text is read by Ring as the
statements it means (the gate reads it back through the compiler's parser and compares the graphs).

The decoder holds at most 128 rules and makes every group and every repeat a rule of its own; the count is checked here. A body ends with a newline, after which the grammar is complete.
"""
import re, sys


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def body_grammar(calls='', writes=''):
    cl = [c for c in (calls or '').split('|') if c]
    wl = [w for w in (writes or '').split('|') if w]
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
    # targets: a local, an element of one, or a name the point may write
    rule('tgt', 'lval' + (' | wtgt' if wl else ''))
    rule('lval', 'id ("[" expr "]")*')
    if wl:
        rule('wtgt', '(' + ' | '.join(lit(w) for w in wl) + ') ("[" expr "]")*')
    # expressions: Ring's precedence, `not` over one comparison chain
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
    rule('ref', '([$@]? id | wref) ("[" expr "]")*' if False else '[$@]? id ("[" expr "]")*')
    if cl:
        rule('call', '(' + ' | '.join(lit(c) for c in cl) + ') "(" args? ")"')
    rule('args', 'expr (", " expr)*')
    rule('id', '[A-Za-z_] [A-Za-z0-9_]*')
    rule('num', '[0-9]+ ("." [0-9]+)?')
    rule('str', "\"'\" [^'\"\\n]* \"'\"")
    return '\n'.join(R) + '\n'


def rule_count(text):
    named = len(re.findall(r'^\w+ ::=', text, re.M))
    body = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    body = re.sub(r'\[(?:[^\]\\]|\\.)*\]', 'C', body)
    return named + body.count('(') + len(re.findall(r'[\)\w"\]C][*+?]', body))


if __name__ == '__main__':
    g = body_grammar(*(sys.argv[1:3] + [''] * 2)[:2])
    print(g)
    print('# %d named rules, about %d by the decoder\'s count' % (len(re.findall(r'^\w+ ::=', g, re.M)), rule_count(g)), file=sys.stderr)
