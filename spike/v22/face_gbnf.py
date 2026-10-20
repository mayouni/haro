"""DRAFT, NOT WIRED, OWED. K4 (v22/k4/K4.md) found that capable cloud models do no better writing the face than Ring; the regime this grammar is for -- small local models under the decoder, Softanza's direction -- is unmeasured. Measured on the way: the engine's
decoder HOLDS this grammar (no refusal, 42 named rules, about 53 by its count of 128) and accepts 27 of the 43 texts the printer prints for the v21 fixtures; the 16 it does not accept fail on
blank lines between definitions, comments, and method bodies richer than the draft allows. Finish it for that regime (K4.md, decision 4).

face_gbnf.py -- the write surface of the Python-shaped face (rung 7 of the code-graph memo; Haro v0.22): a GBNF for the texts a model may write, in the dialect the forge
emits and the engine's constrained decoder (gbnf_machine.zig, contract C9) reads.

    face_grammar() -> the grammar text            python haro/spike/v22/face_gbnf.py            prints it and its rule count

What a context-free grammar can say of the face, it says, so that a decoder CANNOT write what the reader would refuse for its SHAPE:
  - the module's order, which Ring makes semantic (F-21, HF-73): statements, then functions, then classes (the reader's `order`)
  - no subscript, lambda, comprehension, tuple, dict, set, f-string, conditional expression, chained comparison, `is`, `in`, `//`, keyword or default argument, `*args`,
    decorator, import, raise, with, assert, del, global, else on a loop, a class body that is not methods, a method without self: none has a production
  - a handler is `except RingError as e:`; a loop's `else` and a try's `else` do not exist; `while True:` is not a statement of the grammar (a do-again is spelt, rarely)
What no context-free grammar says stays the reader's: which operator may be Python's (`==` where both kinds are known, `eq` otherwise -- the kinds are a flow fact), the
face's words used right (`at` takes two arguments), a name that is a Python keyword or a face word, a name defined, a loop variable read after its loop, and the 23
collisions. So the grammar is a SUPERSET of the face -- every text the printer prints is in it -- and the reader is the judge of the rest.

The decoder holds at most 128 rules and makes every `( ... )` and every repeat a rule of its own (scoped.py), so the grammar is written for that count: statements
are held to DEPTH levels of nesting (indentation is counted by named rules, the one thing a GBNF cannot count), and the count is checked here.
"""
import os, re, sys

DEPTH = 4           # levels of indentation a statement may have below the top: 0 .. DEPTH
BANNER_START = '# Ring++ in Python shape'


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def face_grammar(depth=DEPTH):
    R = []                                        # the rules, in order

    def rule(name, body):
        R.append('%s ::= %s' % (name, body))

    ind = lambda d: 'i%d' % d
    # indentation: i1 is four spaces, i2 two of them ...
    for d in range(1, depth + 2):
        rule(ind(d), ' '.join(['"    "'] * d) if d <= 1 else ind(d - 1) + ' "    "')

    NL = '"\\n"'
    # -- names, numbers, strings
    rule('name', '[A-Za-z_] [A-Za-z0-9_]*')
    rule('num', '[0-9]+ ("." [0-9]+)?')
    rule('str', '"\\"" [^"\\n]* "\\"" | "\'" [^\'\\n]* "\'" | "r\\"" [^"\\n]* "\\""')
    # -- expressions: Python's precedence, no subscript, no lambda, one comparison at most
    rule('expr', 'andx (" or " andx)*')
    rule('andx', 'notx (" and " notx)*')
    rule('notx', '"not " notx | cmp')
    rule('cmp', 'arith (cmpop arith)?')
    rule('cmpop', '" == " | " != " | " <= " | " >= " | " < " | " > "')
    rule('arith', 'term (addop term)*')
    rule('addop', '" + " | " - "')
    rule('term', 'factor (mulop factor)*')
    rule('mulop', '" * " | " / "')
    rule('factor', '"-" factor | power')
    rule('power', 'atom (" ** " factor)?')
    rule('atom', 'num | str | chain | "[" args? "]" | "(" expr ")"')
    rule('chain', 'name trailer*')
    rule('trailer', '"." name | "(" args? ")"')
    rule('args', 'expr (", " expr)*')
    # -- simple statements
    rule('target', 'name ("." name)*')
    rule('simple', 'target " = " expr | target augop expr | "return" (" " expr)? | "break" | "continue" | "pass" | expr')
    rule('augop', '" += " | " -= " | " *= " | " /= "')
    rule('params', 'name (", " name)*')
    # -- compound statements, by depth: a statement at depth d is indented by d levels and its blocks by d+1
    for d in range(0, depth + 1):
        pre = ind(d) + ' ' if d else ''
        nxt = d + 1
        if d < depth:
            blk = 'b%d' % nxt
            rule('s%d' % d,
                 pre + 'simple ' + NL +
                 ' | ' + pre + '"if " expr ":" ' + NL + ' ' + blk + ' (' + (ind(d) + ' ' if d else '') + '"elif " expr ":" ' + NL + ' ' + blk + ')* ('
                 + (ind(d) + ' ' if d else '') + '"else:" ' + NL + ' ' + blk + ')?'
                 ' | ' + pre + '"while " expr ":" ' + NL + ' ' + blk +
                 ' | ' + pre + '"for " name " in " expr ":" ' + NL + ' ' + blk +
                 ' | ' + pre + '"try:" ' + NL + ' ' + blk + ' ' + (ind(d) + ' ' if d else '') + '"except RingError as " name ":" ' + NL + ' ' + blk + ' ('
                 + (ind(d) + ' ' if d else '') + '"finally:" ' + NL + ' ' + blk + ')?')
            rule('b%d' % nxt, '(s%d)+' % nxt)
        else:
            rule('s%d' % d, pre + 'simple ' + NL)
    # a block at depth `depth` holds simple statements only; b<depth> is defined above as (s<depth>)+
    # -- functions and classes: a function's body is a block at depth 1, a method's at depth 2 (indented under the class)
    rule('fdef', '"def " name "(" params? "):" ' + NL + ' b1')
    rule('mdef', ind(1) + ' "def " name "(self" (", " name)* "):" ' + NL + ' ' + 'mb')
    rule('mb', '(' + ind(2) + ' simple ' + NL + ' | ' + ind(2) + ' "if " expr ":" ' + NL + ' (' + ind(3) + ' simple ' + NL + ')+)+')
    rule('cdef', '"class " name ("(" name ")")? ":" ' + NL + ' (mdef)+')
    rule('banner', lit(BANNER_START) + ' [^\\n]* ' + NL)
    rule('root', 'banner? s0* fdef* cdef*')
    # name the first rule `root` for the decoder
    return 'root ::= banner? s0* fdef* cdef*\n' + '\n'.join(r for r in R if not r.startswith('root ::='))


def rule_count(text):
    """The decoder's count: named rules, plus every group and every repeat."""
    named = len(re.findall(r'^\w+ ::=', text, re.M))
    body = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    body = re.sub(r'\[(?:[^\]\\]|\\.)*\]', 'C', body)
    groups = body.count('(')
    repeats = len(re.findall(r'[\)\w"\]C][*+?]', body))
    return named + groups + repeats


if __name__ == '__main__':
    g = face_grammar()
    print(g)
    print('\n# %d named rules, about %d by the decoder\'s count' % (len(re.findall(r'^\w+ ::=', g, re.M)), rule_count(g)), file=sys.stderr)
