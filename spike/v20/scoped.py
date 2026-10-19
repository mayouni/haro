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


def scoped_gbnf(model, ctx=None, posture=None, author=None, points=None):
    """The shapes TO takes are named rules SHARED by every point, and each point's sentence is a top-level alternative of `body`, not a group: the
    engine's decoder holds at most 128 rules (gbnf_machine.zig MAX_RULES) and makes every `( ... )` and every repeat a rule of its own, so the first
    form -- each point carrying its own copy of the number, the tier, the posture -- crossed the limit at five points (GBNF-M2, found by fixture 36,
    2026-10-19). What a point still costs is its own rule, its two tails and the option list it names; the language is the same.

    `points` (D26): the names of the points a TASK may refine -- the agent's write surface is what its task may change, nothing else; a name the program does
    not declare is refused here, by name. Without it every built point is in the grammar, which the decoder holds up to 10 or 11 points (HF-87)."""
    ctx = model.ctx if ctx is None else ctx
    L = model.lift()
    post = lit(posture) if posture else alt(list(refine.POSTURES))
    who = lit('"%s"' % author) if author else 'word'
    govs = sorted(ctx)
    cases, tails = [], []
    if points is not None:
        unknown = [x for x in points if not any(p['name'] == x for p in L['points'])]
        if unknown:
            raise ValueError('the task names points the program does not declare: %s' % ', '.join(unknown))
    for n, p in enumerate(L['points']):
        if not p['built'] or (points is not None and p['name'] not in points):
            continue
        a = p['attrs']
        opts = a['options'].split('|') if a.get('options') else None
        c = refine.cascade(model.g, p)
        reads = ','.join(str(i) for i in sorted(set(i for i, _ in c['reads'])))
        tails.append('tail%d ::= ", AUTHOR " who ", POSTURE " post ", REASON " word (", AT " %s)?' % (n, lit('"%d"' % p['id'])))
        tails.append('vtail%d ::= tail%d (", CASCADE " %s)?' % (n, n, lit('"%s"' % reads)))
        shapes = []                                   # (target text, the text FROM must be, the rule for TO, whether the sentence is about the value)
        if p['form'] in ('num', 'neg'):
            shapes.append((p['name'], p['value'], 'qnum', True))
            for k in ('min', 'max'):
                shapes.append((p['name'] + '.' + k, a.get(k, ''), 'qnumopt', False))
        elif p['form'] == 'str':
            shapes.append((p['name'], p['value'], quoted(alt(opts)) if opts else 'qtext', True))
        elif p['form'] == 'call':
            shapes.append((p['name'], p['value'], quoted(alt(opts)) if opts else 'qname', True))
        else:
            tails.append('stage%d ::= %s' % (n, alt(opts)))
            shapes.append((p['name'], p['value'], quoted('(stage%d ("|" stage%d)*)?' % (n, n)), True))
        if p['kind'] in ('algo', 'pipeline'):
            shapes.append((p['name'] + '.options', a.get('options', ''), 'qopts', False))
        shapes.append((p['name'] + '.risk', a.get('risk', ''), 'qtier', False))
        shapes.append((p['name'] + '.floor', a.get('floor', ''), 'qfloor', False))
        shapes.append((p['name'] + '.governed_by', a.get('governed_by', ''), 'qgov', False))
        # one rule per point: the decoder also holds at most 1024 elements in ONE rule (GBNF-M3), and every character of a literal is one, so the
        # points' sentences inlined in `body` crossed that at five points as the groups had crossed the rule count
        tails.append('point%d ::= ' % n + ' | '.join(
            lit('TARGET "%s", KIND %s, FROM "%s", TO ' % (target, p['kind'], frm)) + ' ' + to + ' ' + ('vtail%d' if is_value else 'tail%d') % n
            for target, frm, to, is_value in shapes))
        cases.append('point%d' % n)
    body = ' | '.join(cases) if cases else lit('TARGET "-"')
    rules = [
        'root ::= "DEFINE REFINE " id " AS ( " body " )"',
        'id ::= [a-z] [a-z0-9_]*',
        'word ::= ' + DQ + ' [^"\\n ] [^"\\n]* ' + DQ,
        'who ::= ' + who,
        'post ::= ' + post,
        'num ::= "-"? [0-9]+ ("." [0-9]+)?',
        'qnum ::= ' + quoted('num'),
        'qnumopt ::= ' + quoted('num?'),
        'qtext ::= ' + quoted('[^"\\n|]*'),
        'qname ::= ' + quoted('[A-Za-z_] [A-Za-z0-9_]*'),
        'qopts ::= ' + quoted('[A-Za-z0-9_]+ ("|" [A-Za-z0-9_]+)*'),
        'qtier ::= ' + quoted('("1" | "2" | "3" | "4")?'),
        'qfloor ::= ' + quoted('(' + ' | '.join(lit(x) for x in refine.POSTURES) + ')?'),
        'qgov ::= ' + (quoted('(' + ' | '.join(lit(x) for x in govs) + ')?') if govs else quoted('')),
    ] + tails + ['body ::= ' + body]
    return '\n'.join(rules) + '\n'
