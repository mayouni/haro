"""haroport (HARO-PORTTOOL-01): the cases, written FIRST, before port/haroport.py.

THE ASK. stzlib-haroport (2026-11-10 04:12), for stzlib's move to .haro (CENTRAL-NORING-SCOPE-01 (2)): "your keyword lowering,
study/v48/respell.py and study/v47/reletter.py as one command (or script) that takes a tree root, with reletter's conflict check and a plan
mode" -- its scratch scripts had no collision check, and unwrapping _x_ landed 15 locals on keywords (_new_ -> new, _try_ -> try).

THE TOOL (the desk's design, judged below):
  python port/haroport.py plan  ROOT              what it would do, file by file; writes nothing
  python port/haroport.py apply ROOT --out DIR    the ported tree in DIR, each .ring file as .haro and each load rewritten to it
THE REWRITES, each mechanical and each refused where it would land on something already there:
  K  a keyword in any case is written in lowercase (lift.zig's ring_keywords, read from there); a symbol (:Name), a string, a comment
     are never touched
  B  a built-in called by name is written in its one spelling (study/v48/builtin_names.py); a name the tree defines as its own
     function is the program's, not the built-in, and is left
  C  Softanza's c (text) is t and its v (any value) is x: cName -> tName, $cX -> $tX, @cX -> @tX, everywhere the token is so spelled
  L  a bare name declared in a function -- assigned, a parameter -- is lettered by what it holds (reletter's R3): n, t, a, o or x;
     never at the top level or in a class body, never a name the class declares as an attribute (in a method a bare assignment to one
     writes the attribute, and a local would change the program)
  U  Softanza's method-local spelling _name_ is unwrapped to name, then lettered by L where L letters; where it stands bare (the top
     level) and is a keyword in any case, the rename is refused -- the collision stzlib's scratch scripts did not check
A rename is REFUSED, and listed in the plan, when the new name is a keyword in any case, is already a name in that scope, or is an
attribute the class declares; the tree is then written without it.

  python port/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

# each case: a small tree, the command's answer judged by asserts on the plan (a JSON report: --json) and on the applied files
CASES = [
    ('H01', 'K', 'a keyword in another case is lowered; a symbol, a string and a comment are not', {
        'main.ring': ['If 1 = 1 See "If" Ok   # If stays in a comment', 'x = :Next', 'For i = 1 To 2 Next']},
     [("applied['main.haro']", 'if 1 = 1 see "If" ok   # If stays in a comment\nx = :Next\nfor i = 1 to 2 next\n')]),
    ('H02', 'B', 'a built-in is spelled as Haro writes it; a function the tree defines is left as written', {
        'main.ring': ['? len("ab")', '? upper("a")', '? isnull(1)', 'func f', T + '? trim(" a ")'],
        'lib.ring': ['func trim x', T + 'return x']},
     [("'? Len(\"ab\")' in applied['main.haro']", True), ("'? Upper(\"a\")' in applied['main.haro']", True),
      ("'? IsNull(1)' in applied['main.haro']", True), ("'? trim(\" a \")' in applied['main.haro']", True)]),
    ('H03', 'C', 'Softanza\'s c is t and its v is x, the same in every file', {
        'main.ring': ['load "lib.ring"', '$cTitle = "a"', 'vAny = 1', '? Shout($cTitle)'],
        'lib.ring': ['func Shout cWord', T + 'return cWord + $cTitle']},
     [("'$tTitle = \"a\"' in applied['main.haro']", True), ("'xAny = 1' in applied['main.haro']", True),
      ("'func Shout tWord' in applied['lib.haro']", True), ("'return tWord + $tTitle' in applied['lib.haro']", True)]),
    ('H04', 'L', 'a bare name in a function is lettered by what it holds; the top level and a class body are not', {
        'main.ring': ['count = 1', 'func f', T + 'count = 3', T + 'name = "a"', T + 'items = [1, 2]', T + 'o = new P', T + '? count + 1',
                      'class P', T + 'size = 2']},
     [("applied['main.haro'].splitlines()[0]", 'count = 1'),
      ("'nCount = 3' in applied['main.haro'] and 'tName = \"a\"' in applied['main.haro'] and 'aItems = [1, 2]' in applied['main.haro']", True),
      ("'oO = new P' in applied['main.haro'] and '? nCount + 1' in applied['main.haro']", True),
      ("applied['main.haro'].splitlines()[-1]", '\tsize = 2')]),
    ('H05', 'L', 'a method\'s bare assignment to an attribute of its class is not made a local: refused, named', {
        'main.ring': ['class P', T + 'count = 0', T + 'func Bump', T + T + 'count = count + 1']},
     [("'\\t\\tcount = count + 1' in applied['main.haro']", True),
      ("any(r['old'] == 'count' and 'attribute' in r['why'] for r in plan['refused'])", True)]),
    ('H06', 'L', 'a rename landing on a name already in the scope is refused, named', {
        'main.ring': ['func f', T + 'cName = "a"', T + 'tName = "b"', T + '? cName + tName']},
     [("'cName = \"a\"' in applied['main.haro']", True),
      ("any(r['old'] == 'cName' and r['new'] == 'tName' and 'already' in r['why'] for r in plan['refused'])", True)]),
    ('H07', 'U', 'Softanza\'s method-local _name_ is unwrapped and lettered as any local', {
        'main.ring': ['func f', T + '_count_ = 1', T + '_new_ = "a"', T + '? _count_ + 1', T + '? _new_']},
     [("'nCount = 1' in applied['main.haro'] and 'tNew = \"a\"' in applied['main.haro']", True),
      ("'? nCount + 1' in applied['main.haro'] and '? tNew' in applied['main.haro']", True)]),
    ('H08', 'U', 'an unwrapped name that stands bare and is a keyword in any case is refused, named (the _new_ -> new kind)', {
        'main.ring': ['_new_ = 1', '_Try_ = 2', '_size_ = 3', '? _new_ + _Try_ + _size_']},
     [("'_new_ = 1' in applied['main.haro'] and '_Try_ = 2' in applied['main.haro']", True),
      ("'size = 3' in applied['main.haro']", True),
      ("sorted(r['old'] for r in plan['refused'] if 'keyword' in r['why'])", ['_Try_', '_new_'])]),
    ('H09', 'C', 'a c name whose t name is a keyword-free word is renamed: tAnd is no keyword', {
        'main.ring': ['func f', T + 'cAnd = 1', T + '? cAnd']},
     [("'tAnd = 1' in applied['main.haro']", True)]),
    ('H10', '-', 'plan writes nothing; apply writes every .ring as .haro, and rewrites its loads', {
        'main.ring': ['load "lib.ring"', '? Half(4)'], 'lib.ring': ['func Half n', T + 'return n / 2']},
     [("sorted(applied)", ['lib.haro', 'main.haro']), ("applied['main.haro'].splitlines()[0]", 'load "lib.haro"'),
      ("plan_wrote", False), ("plan['files']", 2)]),
    ('H11', '-', 'the ported tree runs on haro and prints what the classic Ring surface printed', {
        'main.ring': ['load "lib.ring"', 'cName = Greet("ada")', '? cName', '? Len(cName)'],
        'lib.ring': ['func Greet cWho', T + 'cOut = "hi " + cWho', T + 'return cOut']},
     [("ran['main.haro']", "hi ada\n6\n"), ("ran_ring['main.ring']", "hi ada\n6\n")]),
]


def main():
    out = []
    for cid, line, why, tree, asserts in CASES:
        folder = os.path.join(HERE, 'cases', cid)
        os.makedirs(folder, exist_ok=True)
        for name, lines in tree.items():
            with open(os.path.join(folder, name), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(lines) + '\n')
        out.append({'id': cid, 'line': line, 'why': why, 'folder': 'cases/' + cid, 'files': sorted(tree),
                    'asserts': [[e, v] for e, v in asserts]})
    doc = {'tool': 'port/haroport.py', 'ask': 'HARO-PORTTOOL-01 (stzlib-haroport, 2026-11-10)',
           'class': 'each case: `plan ROOT --json` read as `plan` (and `plan_wrote`: whether it wrote any file), `apply ROOT --out DIR` read '
                    'as `applied` (published name -> text); for H11 each tree run on haro: `ran` (the ported) and `ran_ring` (the original)',
           'cases': out}
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
