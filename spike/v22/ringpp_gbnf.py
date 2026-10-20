"""ringpp_gbnf.py -- the Ring++-shaped counterpart of face_gbnf.py: a GBNF for the texts a model may write when it writes Ring++ (the baseline K4 compares the face against), in the same
dialect and under the same decoder (gbnf_machine.zig, contract C9), so that BOTH shapes are measured with a grammar.

    ringpp_grammar(sentinel=END, indent=True) -> the grammar text      python haro/spike/v22/ringpp_gbnf.py     prints it and its rule count

It is the canonical spelling `rnxc fmt` prints for the core of the language -- `if ... but ... else ... ok`, `for i = 1 to n ... next`, `for x in list ... next`, `while ... end`, `try ... catch ... done`,
`func`, `class` with attributes then methods, `?`, `new K` and `new K(args)`, `$global`, `@attribute`, `This.x` -- over the constructs the K4 tasks and ordinary programs use. What it leaves out
(braces, `switch`, `do ... again`, lambdas, `eval`, `load`, `import`, `call`, `:symbols`, `loop N` / `exit N`, statements in a class body) has no production; the court (grammar_court.py) names the
fixtures it does not accept.

What it says for SHAPE, as the face grammar does: the module's order (statements, then functions, then classes -- in Ring a statement written after a `func` belongs to that function, HF-73, so the
grammar gives it to the function and never offers it at the top level again), an expression statement is a call, `not` takes one comparison, an `if` is closed by `ok`, a loop by `end` or `next`.

INDENTATION. Ring ignores it, so a block could be `stmt+` with no counting, to any depth. Two forms, both here:
  indent=True   (the default) the canonical form `rnxc fmt` prints: a tab a level, counted by named rules exactly as the face's four spaces are, to DEPTH levels. Deterministic for the decoder.
  indent=False  FLAT: no tabs at all, a recursive block. Measured by the court: it is accepted by the decoder and the K4 programs go through it, but a model must then write code with no
                indentation, which no model was trained to do.
What does not work, found by the court: a TAB-OPTIONAL grammar (`"\\t"*` at the head of every line, no counting). Every closer (`ok`, `next`, ...) may then belong to any enclosing block, the number of parse
stacks the decoder keeps grows with the nesting, and the decoder rejects a program of three levels that the flat and the counted forms accept. A grammar's ambiguity is the decoder's problem, not only the reader's.

The decoder holds at most 128 rules (every group and every repeat counts, scoped.py); the count is checked here and by the court. A program ends with the sentinel line `<<END>>` (see face_gbnf.py).
"""
import re, sys

END = '<<END>>'
DEPTH = 4           # levels of indentation a statement may have below the top (the indented form)


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t') + '"'


def ringpp_grammar(sentinel=END, indent=True, depth=DEPTH):
    R = []

    def rule(name, body):
        R.append('%s ::= %s' % (name, body))

    NL = '"\\n"'
    # -- names, numbers, strings (Ring has no escapes: a string runs to its closing quote)
    rule('name', '[A-Za-z_] [A-Za-z0-9_]*')
    rule('pname', '[$@]? name')
    rule('num', '[0-9]+ ("." [0-9]+)?')
    rule('str', '"\\"" [^"\\n]* "\\"" | "\'" [^\'\\n]* "\'"')
    # -- expressions: Ring's precedence, `not` over one comparison chain, `and` and `or` below it
    rule('expr', 'andx (" or " andx)*')
    rule('andx', 'notx (" and " notx)*')
    rule('notx', '"not " eqx | eqx')
    rule('eqx', 'cmp ((" = " | " != ") cmp)*')
    rule('cmp', 'arith (cmpop arith)?')
    rule('cmpop', '" <= " | " >= " | " < " | " > "')
    rule('arith', 'term (addop term)*')
    rule('addop', '" + " | " - "')
    rule('term', 'factor (mulop factor)*')
    rule('mulop', '" * " | " / " | " % "')
    rule('factor', '"-" factor | atom')
    rule('atom', 'num | str | "new " name ("(" args? ")")? | chain | "[" args? "]" | "(" expr ")"')
    rule('chain', 'pname trailer*')
    rule('trailer', '"." name | "(" args? ")" | "[" expr "]"')
    rule('args', 'expr (", " expr)*')
    # -- simple statements: an expression statement is a call
    rule('target', 'pname ("." name | "[" expr "]")*')
    rule('call', 'pname ("." name | "[" expr "]")* "(" args? ")"')
    rule('simple', 'target " = " expr | target augop expr | target "++" | target "--" | "return" (" " expr)? | "exit" | "loop" | "? " expr | call')
    rule('augop', '" += " | " -= " | " *= " | " /= "')
    rule('params', 'name (", " name)*')
    rule('comment', '"#" [^\\n]* ' + NL)
    if indent:
        # statements by depth: a line at depth d is d tabs in, its block d+1
        for d in range(1, depth + 1):
            rule('i%d' % d, '"\\t"' if d == 1 else 'i%d "\\t"' % (d - 1))
        for d in range(0, depth + 1):
            pre = 'i%d ' % d if d else ''
            if d < depth:
                nxt = 'b%d' % (d + 1)
                rule('s%d' % d,
                     pre + 'simple ' + NL +
                     ' | ' + pre + 'comment' +
                     ' | ' + NL +
                     ' | ' + pre + '"if " expr ' + NL + ' ' + nxt + ' (' + pre + '"but " expr ' + NL + ' ' + nxt + ')* (' + pre + '"else" ' + NL + ' ' + nxt + ')? ' + pre + '"ok" ' + NL +
                     ' | ' + pre + '"while " expr ' + NL + ' ' + nxt + ' ' + pre + '"end" ' + NL +
                     ' | ' + pre + '"for " name " = " expr " to " expr (" step " expr)? ' + NL + ' ' + nxt + ' ' + pre + '"next" ' + NL +
                     ' | ' + pre + '"for " name " in " expr ' + NL + ' ' + nxt + ' ' + pre + '"next" ' + NL +
                     ' | ' + pre + '"try" ' + NL + ' ' + nxt + ' ' + pre + '"catch" ' + NL + ' ' + nxt + ' ' + pre + '"done" ' + NL)
                rule('b%d' % (d + 1), '(s%d)+' % (d + 1))
            else:
                rule('s%d' % d, pre + 'simple ' + NL + ' | ' + pre + 'comment | ' + NL)
        rule('fdef', '"func " name "(" params? ")" ' + NL + ' b1')
        rule('attr', 'i1 name " = " expr ' + NL + ' | ' + NL)
        rule('mdef', 'i1 "func " name "(" params? ")" ' + NL + ' b2 | ' + NL)
        rule('cdef', '"class " name (" from " name)? ' + NL + ' attr* mdef*')
        root = 'root ::= s0* fdef* cdef* ' + lit(sentinel + '\n')
        return root + '\n' + '\n'.join(R)
    # FLAT: no indentation at all, a recursive block
    rule('stmt', 'simple ' + NL +
         ' | comment' +
         ' | ' + NL +
         ' | "if " expr ' + NL + ' blk ("but " expr ' + NL + ' blk)* ("else" ' + NL + ' blk)? "ok" ' + NL +
         ' | "while " expr ' + NL + ' blk "end" ' + NL +
         ' | "for " name " = " expr " to " expr (" step " expr)? ' + NL + ' blk "next" ' + NL +
         ' | "for " name " in " expr ' + NL + ' blk "next" ' + NL +
         ' | "try" ' + NL + ' blk "catch" ' + NL + ' blk "done" ' + NL)
    rule('blk', 'stmt+')
    rule('fdef', '"func " name "(" params? ")" ' + NL + ' stmt*')
    rule('attr', 'name " = " expr ' + NL + ' | ' + NL)
    rule('mdef', '"func " name "(" params? ")" ' + NL + ' stmt*')
    rule('cdef', '"class " name (" from " name)? ' + NL + ' attr* mdef*')
    root = 'root ::= stmt* fdef* cdef* ' + lit(sentinel + '\n')
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
    g = ringpp_grammar(indent='--flat' not in sys.argv)
    print(g)
    print('\n# %d named rules, about %d by the decoder\'s count' % (len(re.findall(r'^\w+ ::=', g, re.M)), rule_count(g)), file=sys.stderr)
