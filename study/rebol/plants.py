"""Each protection of the two courts switched off in turn: the court must fail, for the fixture that protection exists for.
Each plant is a text substitution in a copy of block.py run in memory, or pattern.py's PLANT switch; no file is changed."""
import importlib.util, io, os, sys, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
NL, BS = chr(10), chr(92)
BLOCK_PLANTS = [
    ('a string folds its continuation indent',
     "re.sub(r'" + BS + "n[ " + BS + "t]*', ' ', raw)", 'raw'),
    ('a comment inside a list or a group is kept',
     "                pos[0] += 1; seg.append(('comment', t[1])); continue", "                pos[0] += 1; continue"),
    ('a trailing comma is layout',
     "            if t[0] == close:" + NL + "                pos[0] += 1; flush(); return items",
     "            if t[0] == close:" + NL + "                if items and not seg: raise Refused('a trailing comma')" + NL + "                pos[0] += 1; flush(); return items"),
    ('an empty item between commas is refused',
     "                if not [v for v in seg if v[0] != 'comment']:" + NL +
     "                    raise Refused(f'line {t[2]}: an empty item before a comma')" + NL + "                flush(); continue",
     "                flush(); continue"),
    ('a memo scalar is a string',
     "out.append(('pair', _key(key), ('str', _unquote(val)))); i += 1; continue",
     "out.append(('pair', _key(key), ('word', _unquote(val)))); i += 1; continue"),
    ('a blank line between declarations',
     "    return '" + BS + "n'.join(' '.join(pv(v) for v in p) + '" + BS + "n' for p in paras)",
     "    return ''.join(' '.join(pv(v) for v in p) + '" + BS + "n' for p in paras)"),
    ('CRLF is LF',
     "    s = text.replace('" + BS + "r" + BS + "n', '" + BS + "n').replace('" + BS + "r', '" + BS + "n')", "    s = text"),
]


def module(name, src):
    spec = importlib.util.spec_from_loader(name, loader=None)
    m = importlib.util.module_from_spec(spec)
    m.__file__ = os.path.join(HERE, name + '.py')
    exec(compile(src, name, 'exec'), m.__dict__)
    return m


def run(fn):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        bad = fn()
    return bad, [l.split()[1].rstrip(':') for l in buf.getvalue().splitlines() if l.startswith('  FAIL')]


src = open(os.path.join(HERE, 'block.py'), encoding='utf-8').read()
caught = 0
for what, a, b in BLOCK_PLANTS:
    assert src.count(a) == 1, (what, src.count(a))
    m = module('block_planted', src.replace(a, b))
    bad, fails = run(lambda: m.court(os.path.join(HERE, 'printing_fixtures.json')))
    caught += bool(bad)
    print(('CAUGHT ' if bad else 'MISSED ') + what + (' -- ' + ', '.join(fails) if fails else ''))
import pattern
for n, what in ((1, 'no recursion'), (2, 'every repetition moves')):
    pattern.PLANT = n
    bad, fails = run(pattern.court)
    caught += bool(bad)
    print(('CAUGHT ' if bad else 'MISSED ') + what + (' -- ' + ', '.join(fails) if fails else ''))
pattern.PLANT = 0
total = len(BLOCK_PLANTS) + 2
print(f'{caught} of {total} plants caught; no file changed')
sys.exit(0 if caught == total else 1)
