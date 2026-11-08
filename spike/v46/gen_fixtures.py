"""Haro v0.46 -- three defects stzlib's port found running on haro.exe (HARO-KEYEDRELEASE-01, HARO-ARITY-RECEIVER-01,
HARO-OBJECT2POINTER-01), fixed in Haro under the author's Haro-first ruling. Written FIRST, before the VM or the compiler is touched.

THE RULING. The author, 2026-11-08 (PRINCIPAL-HAROFIRST-01): "the fixes and enhancements should go into Haro and not Ring++"; and "Ring++
will be retired as Ring and all it's libraries, only Haro will remain."

THE LINES. Ring 1.27 is the specification of a .ring file's surface; every run case's expected answer was read off it (ported_court --ring).
  K1  a read by a key that is not proven a whole number answers the element OR the empty text of a missing key, so the compiler may never
      hold it as an uncounted integer: a missing key's empty text, released from such a register, freed static memory (a segfault)
  K2  `haro check` resolves an unqualified call inside a class to its own method -- but `x.M()` and `This.F().M()` call M on a receiver,
      which is no unqualified call; the arity of the class's own M is not theirs
  K3  object2pointer(o) is an OBJECTPOINTER (isPointer 1); pointer2object(p) is that same object, shared, not a copy; two pointers to one
      object are equal; anything else is "Bad parameter type!" in the function's name, as Ring's

MEASURED before the rung, on haro 1dc5795: stzlib's haro_keyed_release.ring segfaults in release() (static empty_str freed); haro check
reports haro/type-arity on haro_arity_receiver.ring 4:32; object2pointer is R3, implemented nowhere (its name only in builtins.zig).

  python spike/v46/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

CASES = [
    ('K01', 'K1', 'a keyed read of missing keys in a loop answers as Ring, never freeing the empty text', 'run', '.ring', [
        'o = new K', '? o.Ids([ "a", "a", "b", "b" ])', '? "done"', 'class K', T + 'def Ids(aData)', T * 2 + 'aSeen = []', T * 2 + 'anCounts = []',
        T * 2 + 'nLen = len(aData)', T * 2 + 'for i = 1 to nLen', T * 3 + 'cKey = "" + aData[i]', T * 3 + 'nId = aSeen[cKey]',
        T * 3 + 'if isNumber(nId)', T * 4 + 'anCounts[nId]++', T * 3 + 'else', T * 4 + 'anCounts + 1', T * 4 + 'nId = len(anCounts)',
        T * 4 + 'aSeen[cKey] = nId', T * 3 + 'ok', T * 2 + 'next', T * 2 + 'return anCounts'],
     {'stdout': '2\n2\n\ndone\n'}),
    ('K02', 'K1', 'a missing key\'s answer is the empty text, and the name holding it is a text until it is set again', 'run', '.ring', [
        'f()', 'func f', T + 'aSeen = []', T + 'aSeen["a"] = 1', T + 'for i = 1 to 3', T * 2 + 'x = aSeen["b"]', T * 2 + '? isString(x) + len(x)',
        T * 2 + 'x = 5', T * 2 + '? x', T + 'next', T + '? aSeen["a"]'],
     {'stdout': '1\n5\n1\n5\n1\n5\n1\n'}),
    # K03 is stzlib's probe whole (haroport_probes/haro_arity_receiver.ring): its first form defined ScoreOf, so the checker saw the
    # receiver's class and the case held before any code -- rewritten before the code, said so.
    ('K03', 'K2', 'a method called on a receiver is not the class\'s own: no arity error', 'check', '.ring', [
        'class stzMusic', T + '@oUniverse = NULL       # MU4: the universe In() chose', T + 'def ToSound(pcNotes)',
        T * 2 + 'return This.ScoreOf(pcNotes).ToSound()'],
     {'not': 'haro/type-arity'}),
    ('K04', 'K2', 'an unqualified call of the class\'s own method with the wrong arity is still reported (must not move)', 'check', '.ring', [
        'class stzMusic', T + 'def ToSound(pcNotes)', T * 2 + 'return 1', T + 'def Play', T * 2 + 'return ToSound()'],
     {'has': 'haro/type-arity'}),
    ('K05', 'K3', 'object2pointer and pointer2object as Ring\'s: one object, shared, pointers equal', 'run', '.ring', [
        'oP = new Point', 'p = object2pointer(oP)', '? type(p)', '? isPointer(p)', 'o2 = pointer2object(p)', 'o2.x = 5', '? oP.x', '? type(o2)',
        'p2 = object2pointer(oP)', '? p = p2', '? isNull(p)', 'class Point', T + 'x = 1'],
     {'stdout': 'OBJECTPOINTER\n1\n5\nOBJECT\n1\n0\n'}),
    ('K06', 'K3', 'object2pointer of no object is Bad parameter type, in its name', 'run', '.ring', ['? object2pointer(5)'],
     {'stdout': '\nLine 1 Bad parameter type! \nIn object2pointer() in file K06.ring ', 'exit': 1}),
    ('K07', 'K3', 'pointer2object of no pointer is Bad parameter type, in its name', 'run', '.ring', ['p = pointer2object(5)', '? "after"'],
     {'stdout': '\nLine 1 Bad parameter type! \nIn pointer2object() in file K07.ring ', 'exit': 1}),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for cid, line, why, kind, ext, prog, want in CASES:
    name = f'cases/{cid}{ext}'
    with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(prog) + '\n')
    case = {'id': cid, 'kind': kind, 'line': line, 'why': why, 'file': name}
    case.update(want)
    out.append(case)
doc = {'rung': 'v0.46', 'decision': 'stzlib\'s three findings on haro.exe, fixed in Haro; Ring 1.27 the specification of a .ring file',
       'class': 'run: exact stdout and exit code on haro and its checked build, the same bytes; check: the report holds (has) or lacks (not) a rule name',
       'lines': {'K1': 'a keyed read is never an uncounted integer', 'K2': 'a call on a receiver is no unqualified call',
                 'K3': 'object2pointer and pointer2object as Ring\'s'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
