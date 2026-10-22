"""tasks.py -- sixteen refinement tasks for an AGENT that writes the body of one function against a point (rung 5, the BLOCK and FUNCTION kinds).

Each task is a small Ring++ program with ONE point: the function's signature is a human's, its allowlist of calls (and writes) is declared in the tag, and the agent
writes the body as ONE line (statements separated by single spaces; no double quote, no comment) -- the `TO` of a refinement sentence. The program prints the result of
calling it, on TWO data sets: the one the task shows and one the checker substitutes, so a body that returns the shown answer is admitted by the gate and fails the
second (a self-test proves it, as K4's did).

    kind      block     the function is declared with an empty body: the agent writes the body (FROM is the empty body's digest)
              function  the function is not there yet: the tag declares its name, parameters and calls; the agent writes the body (FROM is `absent`)
    name      the point's name; for a function point it is the function's own name (D24: exact)
    calls     what the body may call (the point's allowlist); builtins count; `writes` what it may write beyond its own locals
    data      the data lines the program begins with: 'a' shown to the agent, 'b' substituted by the checker
    main      the statements that call the function and print
    gold      the reference body, one line: it must be admitted by the gate and print the right answer on both data sets
    helpers   functions the program defines beside the point (text, canonical)
"""

TASKS = [
    {'id': 'R01', 'kind': 'block', 'name': 'sumto', 'sig': 'func SumTo(n)', 'calls': '', 'writes': '',
     'intent': 'return the sum of the integers from 1 to n, inclusive',
     'data': {'a': ['nN = 5'], 'b': ['nN = 9']}, 'main': ['? SumTo(nN)'],
     'gold': 'nS = 0 for i = 1 to n nS += i next return nS'},
    {'id': 'R02', 'kind': 'block', 'name': 'fact', 'sig': 'func Fact(n)', 'calls': '', 'writes': '',
     'intent': 'return the factorial of n',
     'data': {'a': ['nN = 5'], 'b': ['nN = 6']}, 'main': ['? Fact(nN)'],
     'gold': 'nF = 1 for i = 2 to n nF *= i next return nF'},
    {'id': 'R03', 'kind': 'block', 'name': 'iseven', 'sig': 'func IsEven(n)', 'calls': '', 'writes': '',
     'intent': 'return 1 when n is even and 0 when it is odd',
     'data': {'a': ['nN = 10'], 'b': ['nN = 7']}, 'main': ['? IsEven(nN)'],
     'gold': 'if n % 2 = 0 return 1 ok return 0'},
    {'id': 'R04', 'kind': 'block', 'name': 'larger', 'sig': 'func Larger(a, b)', 'calls': '', 'writes': '',
     'intent': 'return the larger of the two numbers',
     'data': {'a': ['nA = 3', 'nB = 8'], 'b': ['nA = 9', 'nB = 4']}, 'main': ['? Larger(nA, nB)'],
     'gold': 'if a > b return a ok return b'},
    {'id': 'R05', 'kind': 'block', 'name': 'clamp', 'sig': 'func Clamp(n, nLo, nHi)', 'calls': '', 'writes': '',
     'intent': 'return n, but no lower than nLo and no higher than nHi',
     'data': {'a': ['nN = 15', 'nLo = 0', 'nHi = 10'], 'b': ['nN = -3', 'nLo = 0', 'nHi = 10']}, 'main': ['? Clamp(nN, nLo, nHi)'],
     'gold': 'if n < nLo return nLo ok if n > nHi return nHi ok return n'},
    {'id': 'R06', 'kind': 'block', 'name': 'vowels', 'sig': 'func Vowels(cText)', 'calls': 'len', 'writes': '',
     'intent': 'return how many of the characters a, e, i, o, u the lower-case text holds',
     'data': {'a': ['cT = "education"'], 'b': ['cT = "strengths"']}, 'main': ['? Vowels(cT)'],
     'gold': "nC = 0 for i = 1 to len(cText) if cText[i] = 'a' or cText[i] = 'e' or cText[i] = 'i' or cText[i] = 'o' or cText[i] = 'u' nC++ ok next return nC"},
    {'id': 'R07', 'kind': 'block', 'name': 'rev', 'sig': 'func Rev(cText)', 'calls': 'len', 'writes': '',
     'intent': 'return the text reversed',
     'data': {'a': ['cT = "ring"'], 'b': ['cT = "softanza"']}, 'main': ['? Rev(cT)'],
     'gold': "cR = '' for i = len(cText) to 1 step -1 cR += cText[i] next return cR"},
    {'id': 'R08', 'kind': 'block', 'name': 'avg', 'sig': 'func Avg(aL)', 'calls': 'len', 'writes': '',
     'intent': 'return the average of the numbers in the list',
     'data': {'a': ['aL = [2, 4, 6]'], 'b': ['aL = [1, 2, 3, 4]']}, 'main': ['? Avg(aL)'],
     'gold': 'nS = 0 for x in aL nS += x next return nS / len(aL)'},
    {'id': 'R09', 'kind': 'block', 'name': 'gross', 'sig': 'func Gross(nNet)', 'calls': 'Tax', 'writes': '',
     'intent': 'return the net amount plus its tax',
     'data': {'a': ['nN = 100'], 'b': ['nN = 50']}, 'main': ['? Gross(nN)'],
     'helpers': 'func Tax(n)\n\treturn n * 0.2\n',
     'gold': 'return nNet + Tax(nNet)'},
    {'id': 'R10', 'kind': 'block', 'name': 'fizz', 'sig': 'func Fizz(n)', 'calls': '', 'writes': '',
     'intent': "return the text fizz when n is divisible by 3, otherwise n itself",
     'data': {'a': ['nN = 9'], 'b': ['nN = 7']}, 'main': ['? Fizz(nN)'],
     'gold': "if n % 3 = 0 return 'fizz' ok return n"},
    {'id': 'R11', 'kind': 'block', 'name': 'digitsum', 'sig': 'func DigitSum(n)', 'calls': 'floor', 'writes': '',
     'intent': 'return the sum of the decimal digits of the non-negative integer n',
     'data': {'a': ['nN = 123'], 'b': ['nN = 4057']}, 'main': ['? DigitSum(nN)'],
     'gold': 'nS = 0 while n > 0 nS += n % 10 n = floor(n / 10) end return nS'},
    {'id': 'R12', 'kind': 'block', 'name': 'whole', 'sig': 'func Whole(n)', 'calls': 'floor', 'writes': '',
     'intent': 'round n to the nearest integer, halves going up',
     'data': {'a': ['nN = 3.6'], 'b': ['nN = 7.2']}, 'main': ['? Whole(nN)'],
     'gold': 'return floor(n + 0.5)'},
    {'id': 'R13', 'kind': 'function', 'name': 'Square', 'params': 'n', 'calls': '', 'writes': '',
     'intent': 'a function Square(n) that returns n times n',
     'data': {'a': ['nN = 7'], 'b': ['nN = 12']}, 'main': ['? Square(nN)'],
     'gold': 'return n * n'},
    {'id': 'R14', 'kind': 'function', 'name': 'Last', 'params': 'aL', 'calls': 'len', 'writes': '',
     'intent': 'a function Last(aL) that returns the last item of the list',
     'data': {'a': ['aL = [3, 5, 8]'], 'b': ['aL = [4, 1]']}, 'main': ['? Last(aL)'],
     'gold': 'return aL[len(aL)]'},
    {'id': 'R15', 'kind': 'function', 'name': 'Dash', 'params': 'a|b|c', 'calls': '', 'writes': '',
     'intent': 'a function Dash(a, b, c) that returns the three texts joined with a dash between them',
     'data': {'a': ['cA = "x"', 'cB = "y"', 'cC = "z"'], 'b': ['cA = "p"', 'cB = "q"', 'cC = "r"']}, 'main': ['? Dash(cA, cB, cC)'],
     'gold': "return a + '-' + b + '-' + c"},
    {'id': 'R16', 'kind': 'block', 'name': 'bump', 'sig': 'func Bump()', 'calls': '', 'writes': '$nCount',
     'intent': 'add one to the global $nCount',
     'data': {'a': ['$nCount = 0'], 'b': ['$nCount = 10']}, 'main': ['Bump()', 'Bump()', '? $nCount'],
     'gold': '$nCount += 1'},
]


BASE = TASKS
SET = ''


def use(name):
    """Switch the task set every harness reads: '' is the sixteen, 'adv' the adversarial eleven (tasks_adv.py). Read at call time, never at import."""
    global TASKS, SET
    if name == 'adv':
        import tasks_adv
        TASKS, SET = tasks_adv.TASKS, 'adv'
    elif name in ('', None):
        TASKS, SET = BASE, ''
    else:
        raise SystemExit('unknown task set %r' % name)


def program(t, which='a'):
    """The task's program text, in the canonical form the gate expects (the self-test checks that it is): the point's tag, the signature (or nothing, for a
    function that is not there yet), the data on top."""
    data = '\n'.join(t['data'][which])
    main = '\n'.join(t['main'])
    if t['kind'] == 'function':
        tag = '# <R:FUNCTION name="%s" params="%s" calls="%s"%s>' % (t['name'], t['params'], t['calls'], (' writes="%s"' % t['writes']) if t['writes'] else '')
        return tag + '\n' + data + '\n' + main + '\n'
    tag = '# <R:BLOCK name="%s" calls="%s"%s>' % (t['name'], t['calls'], (' writes="%s"' % t['writes']) if t['writes'] else '')
    text = data + '\n' + main + '\n\n' + tag + '\n' + t['sig'] + '\n'
    if t.get('helpers'):
        text += '\n' + t['helpers']
    return text


def sentence(t, body, frm):
    """The refinement sentence an agent's body becomes: the point, FROM what the lift shows, TO the body on one line."""
    return ('DEFINE REFINE write_%s AS ( TARGET "%s", KIND %s, FROM "%s", TO "%s", AUTHOR "mansour", POSTURE trusted, REASON "%s" )'
            % (t['id'].lower(), t['name'], t['kind'], frm, body, t['intent'].replace('"', "'")[:60]))
