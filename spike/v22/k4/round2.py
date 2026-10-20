"""K4, round 2: the face primer amended for what round 1 showed was the PRIMER's fault, and a Ring baseline with no primer at all. Round 1's prompts (R.md, F.md) and answers stay as they were.

Round 1 (haiku and sonnet, two repetitions each, the primers of k4.py): Ring 20/20 in all four runs; the face 1/20 and 1/20 strict and 3/20 and 3/20 lenient for haiku (it wrote Python's str(x)
for a number, which the face refuses), 3/20 and 3/20 strict and 19/20 and 19/20 lenient for sonnet (the meaning right, the spelling over-explicit: plus(a, b) and eq(a, b) where the face
writes plain operators because both kinds are known); and T10 refused for all four face runs -- the class before the statements that use it, an order Ring does not allow and the primer
never said.

The F2 primer says the three things round 1 found missing: the order of a module, that there is no str() / int() and a number is joined to text with cat, and that the explicit words are
always right where the kinds are unsure (the formatter -- print of the reading -- respells them). R0 is Ring with the one line "you write Ring 1.27" and nothing else.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import k4

F2_EXTRA = '''- Order of a module: first the statements, then every `def` function, then every class; never a statement after a def or a class (Ring runs what follows a function as part of that function).
- There is no str(), int() or float(): join text and a number with cat(text, number), as in cat("n=", 5). str(e) exists only inside `except RingError as e:`.
- If you are not sure that both sides of an operator are plainly numbers (or plainly strings), use the words -- eq, ne, lt, gt, le, ge, plus, cat. They are always right; a formatter respells them to the plain operator when the kinds allow.'''

F2_PRIMER = k4.FACE_PRIMER + '\n' + F2_EXTRA
R0_PRIMER = 'You write programs in Ring (version 1.27).'


def emit():
    exp = __import__('json').load(open(os.path.join(HERE, 'expected.json')))
    for cond, primer, lang in (('F2', F2_PRIMER, 'the face'), ('R0', R0_PRIMER, 'Ring')):
        lines = [primer, '', 'TASKS. For each task write one complete program in %s. Every program must BEGIN with exactly the line(s) shown for its task (they hold its data; the checker will '
                 'run your program on other values of the same shape, so compute the answer, never print it from the example). Nothing may be read from the keyboard or from a file. '
                 'Reply with one block per task, in this exact form, and nothing else:' % lang, '', '### T01', '```', '<the program>', '```', '']
        for t in k4.TASKS:
            lines += ['### %s' % t['id'], t['text'], 'The program begins with:'] + ['    ' + l for l in t['a']]
            lines += ['For that data it prints:'] + ['    ' + l for l in exp[t['id']]['a'].split('\n')] + ['']
        open(os.path.join(HERE, 'prompts', cond + '.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('round 2 prompts written: F2, R0')


if __name__ == '__main__':
    emit()
