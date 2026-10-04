"""Which alternative spellings of a construct compile to the same code on rnxc? Each pair is a program in the canonical spelling and
the same program in one alternative; `rnxc dis` is the judge, with the lambda's source-line name blanked."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import l1_check as ck

PAIRS = [
    ('func/def', 'func F()\n\treturn 1\n', 'def F()\n\treturn 1\n'),
    ('func/function', 'func F()\n\treturn 1\n', 'function F()\n\treturn 1\n'),
    ('func/FUNC', 'func F()\n\treturn 1\n', 'FUNC F()\n\treturn 1\n'),
    ('end/endfunc', 'func F()\n\treturn 1\nend\n', 'func F()\n\treturn 1\nendfunc\n'),
    ('ok/endif', 'if a\n\tb = 1\nok\n', 'if a\n\tb = 1\nendif\n'),
    ('ok/end', 'if a\n\tb = 1\nok\n', 'if a\n\tb = 1\nend\n'),
    ('if/IF', 'if a\n\tb = 1\nok\n', 'IF a\n\tb = 1\nOK\n'),
    ('but/elseif', 'if a\n\tb = 1\nbut c\n\tb = 2\nok\n', 'if a\n\tb = 1\nelseif c\n\tb = 2\nok\n'),
    ('else/other', 'if a\n\tb = 1\nelse\n\tb = 2\nok\n', 'if a\n\tb = 1\nother\n\tb = 2\nok\n'),
    ('?/see', '? x\n', 'see x\n'),
    ('?/put', '? x\n', 'put x\n'),
    ('give/get', 'give x\n', 'get x\n'),
    ('give/GIVE', 'give x\n', 'GIVE x\n'),
    ('exit/break', 'for i = 1 to 2\n\texit\nnext\n', 'for i = 1 to 2\n\tbreak\nnext\n'),
    ('loop/continue', 'for i = 1 to 2\n\tloop\nnext\n', 'for i = 1 to 2\n\tcontinue\nnext\n'),
    ('for/foreach', 'for i in x\n\t? i\nnext\n', 'foreach i in x\n\t? i\nnext\n'),
    ('next/endfor', 'for i in x\n\t? i\nnext\n', 'for i in x\n\t? i\nendfor\n'),
    ('next/end', 'for i in x\n\t? i\nnext\n', 'for i in x\n\t? i\nend\n'),
    ('while end/endwhile', 'while a\n\tb = 1\nend\n', 'while a\n\tb = 1\nendwhile\n'),
    ('while {}', 'while a\n\tb = 1\nend\n', 'while a { b = 1 }\n'),
    ('if {}', 'if a\n\tb = 1\nok\n', 'if a { b = 1 }\n'),
    ('for {}', 'for i = 1 to 2\n\t? i\nnext\n', 'for i = 1 to 2 { ? i }\n'),
    ('func {}', 'func F()\n\treturn 1\n', 'func F() { return 1 }\n'),
    ('switch off/end', 'switch a\n\ton 1\n\t\t? 1\noff\n', 'switch a\n\ton 1\n\t\t? 1\nend\n'),
    ('switch off/endswitch', 'switch a\n\ton 1\n\t\t? 1\noff\n', 'switch a\n\ton 1\n\t\t? 1\nendswitch\n'),
    ('on/case', 'switch a\n\ton 1\n\t\t? 1\noff\n', 'switch a\n\tcase 1\n\t\t? 1\noff\n'),
    ('other/else (switch)', 'switch a\n\ton 1\n\t\t? 1\n\tother\n\t\t? 2\noff\n', 'switch a\n\ton 1\n\t\t? 1\n\telse\n\t\t? 2\noff\n'),
    ('done/end', 'try\n\tf()\ncatch\n\tg()\ndone\n', 'try\n\tf()\ncatch\n\tg()\nend\n'),
    ('done/endtry', 'try\n\tf()\ncatch\n\tg()\ndone\n', 'try\n\tf()\ncatch\n\tg()\nendtry\n'),
    ('and/&&', 'x = a and b\n', 'x = a && b\n'),
    ('or/||', 'x = a or b\n', 'x = a || b\n'),
    ('not/!', 'x = not a\n', 'x = !a\n'),
    ('This/self', 'func F()\n\treturn This\n', 'func F()\n\treturn self\n'),
    ('This/this', 'func F()\n\treturn This\n', 'func F()\n\treturn this\n'),
    ('NULL/null', 'x = NULL\n', 'x = null\n'),
    ('true/TRUE', 'x = true\n', 'x = TRUE\n'),
    ('class from/:', 'class A from B\n\tx = 1\n', 'class A : B\n\tx = 1\n'),
    ('class from/<', 'class A from B\n\tx = 1\n', 'class A < B\n\tx = 1\n'),
    ('class {}', 'class A\n\tx = 1\n', 'class A { x = 1 }\n'),
    ('stmt sep ;', 'a = 1\nb = 2\n', 'a = 1; b = 2\n'),
    ('stmt sep ,', 'a = 1\nb = 2\n', 'a = 1, b = 2\n'),
    ('trailing period', 'Foo(1)\n', 'Foo(1).\n'),
    ('func no-paren params', 'func F(a, b)\n\treturn a\n', 'func F a, b\n\treturn a\n'),
    ('func empty parens', 'func F()\n\treturn 1\n', 'func F\n\treturn 1\n'),
    ('return / return(expr)', 'func F()\n\treturn 1\n', 'func F()\n\treturn (1)\n'),
]


def norm(text):
    return re.sub(r'@@lambda\d+', '@@lambdaN', text)


if __name__ == '__main__':
    bad = 0
    for name, a, b in PAIRS:
        ra, rb = ck.dis(a, 'syn_a.ring'), ck.dis(b, 'syn_b.ring')
        same = ra[0] == rb[0] and norm(ra[1]) == norm(rb[1])
        status = 'same' if same else ('DIFFERS' if ra[0] == rb[0] == 0 else f'rc {ra[0]}/{rb[0]}')
        bad += not same
        print(f'  {status:8s} {name}')
    print(bad, 'of', len(PAIRS), 'differ')
