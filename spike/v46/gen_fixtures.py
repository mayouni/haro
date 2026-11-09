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
    # WRITTEN AFTER THE PLANTS: plant N6 (pointer2object takes a pointer of any kind) missed, because K07 passes a number, which is refused
    # before the kind is asked; K08 passes a file's pointer (Ring's answer read off Ring 1.27).
    ('K08', 'K3', 'pointer2object of a pointer of another kind is Bad parameter type', 'run', '.ring', [
        'fp = fopen("K08.txt", "w")', 'o = pointer2object(fp)', '? "after"'],
     {'stdout': '\nLine 2 Bad parameter type! \nIn pointer2object() in file K08.ring ', 'exit': 1}),
    # WRITTEN AFTER THE RUNG LANDED (haro 55c377d), on stzlib's second report of 2026-11-08, before any code: (1) the keyed-read fix held
    # only where the key was PROVEN a text (an `hget`, which counts); a key whose class the compiler cannot prove -- `"" + (anA[i] * 3 +
    # anB[i])` is a `ref`, its operands may be objects -- reads through `vget`, uncounted, and still freed the static empty text: plant N2's
    # change was load-bearing, and no case had reached it (K09, stzlib's haro_keyed_release_arith.ring whole). The desk had also reported
    # stzDataSet_defects 185 of 185 on stzlib c4f6f85ea, a ref OLDER than the guard that reaches this loop -- corrected in the records.
    # (2) HARO-PTRCMP-01: ptrcmp and pointercompare, and the short forms obj2ptr and ptr2obj, absent (K10-K12; Ring's answers read off it).
    ('K09', 'K1', 'a keyed read by a key the compiler cannot prove a text is counted too', 'run', '.ring', [
        'o = new K', '? o.Joint([ 1, 1, 2, 2 ], [ 1, 1, 2, 2 ])', '? "done"', 'class K', T + 'def Joint(anA, anB)', T * 2 + 'aAt = []',
        T * 2 + 'anN = []', T * 2 + 'nTotal = len(anA)', T * 2 + 'for i = 1 to nTotal', T * 3 + 'cPair = "" + (anA[i] * 3 + anB[i])',
        T * 3 + 'nAt = aAt[cPair]', T * 3 + 'if isNumber(nAt)', T * 4 + 'anN[nAt]++', T * 3 + 'else', T * 4 + 'anN + 1',
        T * 4 + 'aAt[cPair] = len(anN)', T * 3 + 'ok', T * 2 + 'next', T * 2 + 'return anN'],
     {'stdout': '2\n2\n\ndone\n'}),
    ('K10', 'K3', 'ptrcmp and pointercompare answer whether two pointers point at one thing', 'run', '.ring', [
        'o1 = new P', 'o2 = new P', 'p1 = object2pointer(o1)', 'p2 = object2pointer(o1)', 'p3 = object2pointer(o2)', '? ptrcmp(p1, p2)',
        '? ptrcmp(p1, p3)', '? pointercompare(p1, p2)', 'class P', T + 'x = 1'],
     {'stdout': '1\n0\n1\n'}),
    ('K11', 'K3', 'obj2ptr and ptr2obj are object2pointer and pointer2object', 'run', '.ring', [
        'o = new P', 'p = obj2ptr(o)', '? type(p)', 'o2 = ptr2obj(p)', 'o2.x = 7', '? o.x', 'class P', T + 'x = 1'],
     {'stdout': 'OBJECTPOINTER\n7\n'}),
    ('K12', 'K3', 'ptrcmp of no pointer is Bad parameter type, in its name', 'run', '.ring', [
        'o = new P', 'p = object2pointer(o)', '? ptrcmp(p, 5)', 'class P', T + 'x = 1'],
     {'stdout': '\nLine 3 Bad parameter type! \nIn ptrcmp() in file K12.ring ', 'exit': 1}),
    # WRITTEN BEFORE THE CODE, third round (HARO-CLONEDEEP-01): stzlib's stzObject guard crashed in Summary() and sometimes hung; reduced
    # by ddmin to one scenario, then to this, with no library: an error raised inside `$g + This.T()` and caught outside leaves the
    # caller's call-window register holding the global's list as an uncounted borrow -- the unwind clears only from the end of the
    # handler's frame, and a callee's frame starts inside it -- so the next store there releases the list while $g still holds it.
    ('K13', 'K4', 'an error raised inside an append to a global, caught outside, leaves the global whole', 'run', '.ring', [
        '$aTV = []', '$bOn = 1', 'oA = new O', 'oA.Add()', 'oA.Add()', '? len(oA.Vals())', '$bOn = 0', 'for i = 1 to 3', T + 'try',
        T * 2 + 'oA.Add()', T + 'catch', T * 2 + '? "caught"', T + 'done', 'next', '? len(oA.Vals())', 's = "banana"', 'aCopy = oA.Vals()',
        '? len(aCopy)', '$aTV + 5', '? len($aTV)', '? "done"', 'class O', T + 'def Add()', T * 2 + '$aTV + This.T()', T + 'def T()',
        T * 2 + 'if $bOn = 0', T * 3 + 'raise("off")', T * 2 + 'ok', T * 2 + 'return 1', T + 'def Vals()', T * 2 + 'return $aTV'],
     {'stdout': '2\ncaught\ncaught\ncaught\n2\n2\n3\ndone\n'}),
    # FOURTH ROUND, 2026-11-09, written before the code: HARO-ARITY-RECEIVER-02 (stzlib-haroport, stzlib bb0cd0fa8,
    # security/stzResponsePlan.ring 445). When the method before ends in `return ... > 0`, the grammar cuts a chained call that is a
    # method's LAST statement: the lone `.` ends that statement INSIDE the definition, and `LockAccount(...)` lands as the definition's
    # next sibling -- so the `.` is the last LEAF of the statement before, not its last child, which is all K03's fix looked at.
    ('K14', 'K2', 'a receiver call cut after a method\'s last statement is no unqualified call: no arity error', 'check', '.ring', [
        'class Plan', T + 'def Owns(pcVerb)', T * 2 + 'return ring_find([ "lockaccount" ], lower("" + pcVerb)) > 0', '',
        T + 'def LockAccount(pcTarget)', T * 2 + 'This._Auth().LockAccount("" + pcTarget, "locked")', '', T + 'def RevokeSession(pcTarget)',
        T * 2 + 'if pcTarget = "" return 0 ok', T * 2 + 'return 1'],
     {'not': 'haro/type-arity'}),
    ('K15', 'K2', 'stzlib\'s probe whole (haroport_probes/haro_arity_receiver2.ring, bb0cd0fa8), its unclosed `if` kept', 'check', '.ring', [
        T * 2 + 'return ring_find([ "lockaccount", "revokesession" ], StzLower("" + pcVerb)) > 0', T + 'def LockAccount(pcTarget)',
        T * 2 + 'This._Auth().LockAccount("" + pcTarget, "locked by a containment plan")', T * 2 + 'if _i_ = 0'],
     {'not': 'haro/type-arity'}),
    # FIFTH ROUND, 2026-11-09, written before the code: HARO-PARENTCLASSNAME-01 (stzlib-haroport, stzlib 44103f717,
    # sound_mu3_narrated.ring 329): parentclassname() was absent (R3). Ring 1.27's meta_e.c, ring_vm_refmeta_parentclassname: one
    # argument; an object answers its class's parent as Ring stores it (folded), "" when it has none; anything else Bad parameter type.
    ('K16', 'K5', 'parentclassname answers the parent folded, the empty text with no parent, through a chain the nearest', 'run', '.ring', [
        '? parentclassname(new B)', '? "[" + parentclassname(new A) + "]"', '? parentclassname(new C)', 'class A', 'class B from A',
        'class C from B'],
     {'stdout': 'a\n[]\nb\n'}),
    ('K17', 'K5', 'parentclassname of no object is Bad parameter type, in its name', 'run', '.ring', ['? parentclassname(5)'],
     {'stdout': '\nLine 1 Bad parameter type! \nIn parentclassname() in file K17.ring ', 'exit': 1}),
    # SIXTH ROUND, 2026-11-09, written before the code: HARO-SYSTEMCMD-01 (lookout, 2026-11-08 13:20, carried by central 22:33).
    # (a) systemcmd() raised R3: it is Ring's LIBRARY code (stdlibcore.ring: System(cmd + "> " + tempname()), read the file, drop a last
    # "\n"), and Haro carries no part of Ring's library (D50) -- so Haro gives it as its own native, C's popen as Ring's system() runs the
    # shell. The desk's named divergence: the whole last line end goes ("\r\n" on Windows), where Ring's leaves the "\r".
    # (b) `a == b` gave R24 naming an EMPTY variable: the parser's recovery put a MISSING identifier between the two `=`, and the
    # compiler read it as a name. A statement holding a missing node is refused, and `==` named.
    ('K18', 'K6', 'systemcmd answers what the command writes, its last line end dropped', 'run', '.ring', [
        '? systemcmd("echo hello")', '? "[" + systemcmd("echo hello") + "]"'],
     {'stdout': 'hello\n[hello]\n'}),
    ('K19', 'K6', 'systemcmd of no text is Bad parameter type, in its name', 'run', '.ring', ['? systemcmd(5)'],
     {'stdout': '\nLine 1 Bad parameter type! \nIn systemcmd() in file K19.ring ', 'exit': 1}),
    ('K20', 'K7', '`a == b` is refused naming `==`, not read as a variable with no name', 'run', '.ring', [
        '? "before"', 'a = 1', 'b = 1', '? a == b'],
     {'stdout': "before\n\nLine 4 Haro refused this statement (`==` is no operator: equality is `=`; written `a == b`, line 4 of K20.ring) "
                "and did not compile it -- running past it would give a wrong answer \nin file K20.ring ", 'exit': 1}),
    ('K21', 'K7', 'and in a .haro file', 'run', '.haro', [
        '? "before"', 'f()', 'func f', T + 'nA = 1', T + '? nA == 1'],
     {'stdout': "before\n\nLine 5 Haro refused this statement (`==` is no operator: equality is `=`; written `nA == 1`, line 5 of K21.haro) "
                "and did not compile it -- running past it would give a wrong answer \nIn function f() in file K21.haro\n\nCalled from line 2 "
                "in file K21.haro ", 'exit': 1}),
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
                 'K3': 'object2pointer and pointer2object as Ring\'s', 'K4': 'an unwound call leaves no uncounted borrow behind'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
