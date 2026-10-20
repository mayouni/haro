"""face_gbnf.py -- the write surface of the Python-shaped face (rung 7 of the code-graph memo; Haro v0.22): a GBNF for the texts a model may write, in the dialect the forge
emits and the engine's constrained decoder (gbnf_machine.zig, contract C9) reads.

    face_grammar(sentinel=END) -> the grammar text        python haro/spike/v22/face_gbnf.py     prints it and its rule count

STATUS (2026-10-20): finished for the local rounds of K4 (v22/k4/K4.md), judged by v22/grammar_court.py -- every K4 gold text and every v21 fixture the printer prints is accepted,
the structural exclusions below are rejected, a planted break fails the court. It is the SHAPE only: the reader (face_read.py) stays the judge of the rest.

What a context-free grammar can say of the face, it says, so that a decoder CANNOT write what the reader would refuse for its SHAPE:
  - the module's order, which Ring makes semantic (F-21, HF-73): statements, then functions, then classes (the reader's `order`)
  - no subscript, lambda, comprehension, tuple, dict, set, f-string, conditional expression, chained comparison, `is`, `in` in an expression, `//`, keyword or default argument, `*args`,
    decorator, import, raise, with, assert, del, global, else on a loop, a class body that is not methods, a method without self: none has a production
  - a handler is `except RingError as e:`; a loop's `else` and a try's `else` do not exist; `while True:` is not a statement of the grammar (a do-again is spelt, rarely)
  - an expression statement is a CALL (`say(x)`, `o.Add()`): a bare name or literal alone on a line is not a statement
What no context-free grammar says stays the reader's: which operator may be Python's (`==` where both kinds are known, `eq` otherwise -- the kinds are a flow fact), the
face's words used right (`at` takes two arguments), a name that is a Python keyword or a face word, a name defined, a loop variable read after its loop, and the 23
collisions. So the grammar is a SUPERSET of the face -- every text the printer prints is in it -- and the reader is the judge of the rest.

The program ends with a SENTINEL line (`<<END>>`, a line no statement can begin with), so a decoder that has written a whole program has nothing left to write and stops: a grammar that
may always add one more statement never tells the decoder it is finished, and a small model then rambles to its token limit. The sentinel is stripped before the text is read.

The decoder holds at most 128 rules and makes every `( ... )` and every repeat a rule of its own (scoped.py), so the grammar is written for that count: statements
are held to DEPTH levels of nesting (indentation is counted by named rules, the one thing a GBNF cannot count), and the count is checked here and by the court.
"""
import os, re, sys

DEPTH = 4           # levels of indentation a statement may have below the top: 0 .. DEPTH
END = '<<END>>'
BANNER_START = '# Ring++ in Python shape'


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def face_grammar(depth=DEPTH, sentinel=END):
    R = []                                        # the rules, in order

    def rule(name, body):
        R.append('%s ::= %s' % (name, body))

    ind = lambda d: 'i%d' % d
    # indentation: i1 is four spaces, i2 two of them ...
    for d in range(1, depth + 1):
        rule(ind(d), '"    "' if d == 1 else ind(d - 1) + ' "    "')

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
    # -- simple statements: an expression statement is a call
    rule('target', 'name ("." name)*')
    rule('call', 'name ("." name)* "(" args? ")"')
    rule('simple', 'target " = " expr | target augop expr | "return" (" " expr)? | "break" | "continue" | "pass" | call')
    rule('augop', '" += " | " -= " | " *= " | " /= "')
    rule('params', 'name (", " name)*')
    rule('comment', '"#" [^\\n]* ' + NL)
    # -- compound statements, by depth: a statement at depth d is indented by d levels and its blocks by d+1.  A blank line is a statement at any depth.
    for d in range(0, depth + 1):
        pre = ind(d) + ' ' if d else ''
        nxt = d + 1
        if d < depth:
            blk = 'b%d' % nxt
            rule('s%d' % d,
                 pre + 'simple ' + NL +
                 ' | ' + pre + 'comment' +
                 ' | ' + NL +
                 ' | ' + pre + '"if " expr ":" ' + NL + ' ' + blk + ' (' + pre + '"elif " expr ":" ' + NL + ' ' + blk + ')* ('
                 + pre + '"else:" ' + NL + ' ' + blk + ')?'
                 ' | ' + pre + '"while " expr ":" ' + NL + ' ' + blk +
                 ' | ' + pre + '"for " name " in " expr ":" ' + NL + ' ' + blk +
                 ' | ' + pre + '"try:" ' + NL + ' ' + blk + ' ' + pre + '"except RingError as " name ":" ' + NL + ' ' + blk + ' ('
                 + pre + '"finally:" ' + NL + ' ' + blk + ')?')
            rule('b%d' % nxt, '(s%d)+' % nxt)
        else:
            rule('s%d' % d, pre + 'simple ' + NL + ' | ' + pre + 'comment | ' + NL)
    # -- functions and classes: a function's body is a block at depth 1, a method's at depth 2 (indented under the class)
    rule('fdef', '"def " name "(" params? "):" ' + NL + ' b1')
    rule('mdef', ind(1) + ' "def " name "(self" (", " name)* "):" ' + NL + ' b2')
    rule('cdef', '"class " name ("(" name ")")? ":" ' + NL + ' (mdef | ' + NL + ')+')
    rule('banner', lit(BANNER_START) + ' [^\\n]* ' + NL)
    root = 'root ::= banner? s0* fdef* cdef* ' + lit(sentinel + '\n')
    return root + '\n' + '\n'.join(R)


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
