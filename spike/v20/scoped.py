"""scoped.py -- the write surface of rung 20: the GBNF of the sentences an agent may write against ONE program, as it stands (charter 6.2: the
refinement sentence's grammar is the agent's write surface; v0.1's scoped hole, with the names in scope inlined).

    scoped_gbnf(model, ctx, posture)     the grammar, in the dialect the forge emits and the engine's constrained decoder (gbnf_machine.zig) reads

Each point of the program is an alternative of its own, so what the gate would refuse for the SHAPE or the IDENTITY of a proposal the grammar does not let
be written: the point's name, its kind, the id of its statement (AT), the value the sentence expects to find (FROM is the point's current text), the
readers of its name (CASCADE), the options TO may take where the point has them, a governance that exists, a number where a number is wanted.
`posture` fixes the origin the harness stands for: an agent run under :llm cannot write :trusted; `author` the actor it acts as.
What no context-free grammar says stays the gate's: a number inside its bounds, an actor's authority, a rule over two points, a callee that exists, a
list of options without a duplicate, a revert (REVERTS names an event of the log, and the harness writes those: Model.revert).
"""
import refine

DQ = '"\\""'                         # a double quote, as a GBNF literal


def lit(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def alt(words):
    return '(' + ' | '.join(lit(w) for w in words) + ')'


def quoted(body):
    return DQ + ' ' + body + ' ' + DQ if body else DQ + ' ' + DQ


NUM = '("-")? [0-9]+ ("." [0-9]+)?'


def scoped_gbnf(model, ctx=None, posture=None, author=None):
    ctx = model.ctx if ctx is None else ctx
    L = model.lift()
    post = lit(posture) if posture else alt(list(refine.POSTURES))
    who = lit('"%s"' % author) if author else 'word'
    govs = sorted(ctx)
    cases, tails = [], []
    for n, p in enumerate(L['points']):
        if not p['built']:
            continue
        a = p['attrs']
        opts = a['options'].split('|') if a.get('options') else None
        c = refine.cascade(model.g, p)
        reads = ','.join(str(i) for i in sorted(set(i for i, _ in c['reads'])))
        tails.append('tail%d ::= ", AUTHOR " who ", POSTURE " post ", REASON " word (", AT " %s)?' % (n, lit('"%d"' % p['id'])))
        tails.append('vtail%d ::= tail%d (", CASCADE " %s)?' % (n, n, lit('"%s"' % reads)))
        shapes = []                                   # (target text, the text FROM must be, the rule for TO, whether the sentence is about the value)
        if p['form'] in ('num', 'neg'):
            shapes.append((p['name'], p['value'], quoted('(' + NUM + ')'), True))
            for k in ('min', 'max'):
                shapes.append((p['name'] + '.' + k, a.get(k, ''), quoted('(' + NUM + ')?'), False))
        elif p['form'] == 'str':
            shapes.append((p['name'], p['value'], quoted(alt(opts) if opts else '[^"\\n|]*'), True))
        elif p['form'] == 'call':
            shapes.append((p['name'], p['value'], quoted(alt(opts) if opts else '[A-Za-z_] [A-Za-z0-9_]*'), True))
        else:
            shapes.append((p['name'], p['value'], quoted('(' + alt(opts) + ' ("|" ' + alt(opts) + ')*)?'), True))
        if p['kind'] in ('algo', 'pipeline'):
            shapes.append((p['name'] + '.options', a.get('options', ''), quoted('[A-Za-z0-9_]+ ("|" [A-Za-z0-9_]+)*'), False))
        shapes.append((p['name'] + '.risk', a.get('risk', ''), quoted('("1" | "2" | "3" | "4")?'), False))
        shapes.append((p['name'] + '.floor', a.get('floor', ''), quoted('(' + ' | '.join(lit(x) for x in refine.POSTURES) + ')?'), False))
        shapes.append((p['name'] + '.governed_by', a.get('governed_by', ''), quoted('(' + ' | '.join(lit(x) for x in govs) + ')?' if govs else ''), False))
        for target, frm, to, is_value in shapes:
            cases.append('(' + lit('TARGET "%s", KIND %s, FROM "%s", TO ' % (target, p['kind'], frm)) + ' ' + to + ' ' + ('vtail%d' if is_value else 'tail%d') % n + ')')
    body = ' | '.join(cases) if cases else lit('TARGET "-"')
    rules = [
        'root ::= "DEFINE REFINE " id " AS ( " body " )"',
        'id ::= [a-z] [a-z0-9_]*',
        'word ::= ' + DQ + ' [^"\\n ] [^"\\n]* ' + DQ,
        'who ::= ' + who,
        'post ::= ' + post,
    ] + tails + ['body ::= ' + body]
    return '\n'.join(rules) + '\n'
