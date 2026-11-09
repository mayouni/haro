"""Haro v0.36, D52 rung (1): A1 completed -- `finally` runs on EVERY exit of a `try`. Written FIRST, before the compiler is touched.

A1's semantics lines (stzlib SOFTANZA_ONE_HOUR.md section 3, at origin/main 0a311d01b), each pinned by the cases that name it:

  S1  the `finally` block runs exactly once per entry of the `try`
  S2  a `return` inside the body or the handler is held, the block runs, then the held exit resumes
  S3  a raise inside the body or the handler is held, the block runs, then the held exit resumes
  S4  a raise inside `finally` replaces a held one                (the CAUSE half is rung (2): it needs the error value)
  S5  `exit` and `loop` crossing a `try` run its `finally` first

Measured on haro 52d53b9 before this rung (runtime/v36/p, runtime/v36/q): the normal path, the caught raise, the uncaught raise and S4 already
hold; S2 (body and handler), S3 for a raise in the HANDLER, and S5 do not; and a `try` inside a `finally` overwrote the error the `finally`
holds (q2: "outer caught: inner"), because nested handlers were named by the depth of open CATCHES and a `finally` is compiled outside its
catch. Each case is a program and the exact bytes it prints; the court runs it on haro and on its checked build.

Not covered here, named: the cause of a replaced error (rung 2); `catch e` without parentheses (rung 2); `bye` inside a `try` (A1 does not
list it: it ends the process); a function whose locals share registers (window overflow, shareFunction) -- no case is that large.

  python spike/v36/gen_fixtures.py      writes v36/cases/*.haro and v36/fixtures.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

CASES = [
    # v0.48 RE-SPELLED, 2026-11-09, AFTER THIS COURT SPOKE (the Principal's ruling, "ParentClassName"): a .haro program's calls of
    # built-ins are spelled as Softanza writes a name (Len, IsNull, SubStr), by study/v48/respell.py, ported here by
    # study/v47/port_cases.py --respell. A report still names a built-in as the VM registers it. Each case asks what it asked.
    # v0.47 RE-LETTERED, 2026-11-08, AFTER THIS COURT SPOKE (D55 T2, the author's scope "Yes, as recommended"): every name of these
    # .haro programs carries its type's letter, by study/v47/reletter.py's rules (c -> t, a single letter or a word by what it holds),
    # ported here by study/v47/port_cases.py; an output that names a renamed variable names its new name. Each case asks what it asked.
    ('F01', 'S1', 'the normal path: the body, the finally, then on', [
        'try', T + '? "body"', 'catch', T + '? "handler"', 'finally', T + '? "finally"', 'done', '? "after"'],
     ['body', 'finally', 'after']),
    ('F02', 'S3', 'a raise in the body, caught: the handler, then the finally', [
        'try', T + 'Raise("boom")', T + '? "not reached"', 'catch', T + '? "handler: " + cCatchError', 'finally', T + '? "finally"', 'done',
        '? "after"'],
     ['handler: boom', 'finally', 'after']),
    ('F03', 'S3', 'a raise in the body with no catch: the finally, then the raise resumes outward', [
        'try', T + 'try', T * 2 + 'Raise("only")', T + 'finally', T * 2 + '? "finally"', T + 'done', T + '? "not reached"', 'catch',
        T + '? "outer: " + cCatchError', 'done'],
     ['finally', 'outer: only']),
    ('F04', 'S2', 'a return in the body: the value is taken, the finally runs (computing as it likes), the value returned is the one taken', [
        '? f()', '? "after"', 'func f', T + 'nN = 1', T + 'try', T * 2 + 'return nN', T + 'finally', T * 2 + '? "finally " + String(nN) + " " + Upper("x")',
        T * 2 + 'nN = 2', T + 'done', T + 'return 99'],
     ['finally 1 X', '1', 'after']),
    ('F05', 'S2', 'a return in the handler: the finally runs, then the return resumes', [
        '? g()', 'func g', T + 'try', T * 2 + 'Raise("in g")', T + 'catch', T * 2 + 'return "from handler"', T + 'finally', T * 2 + '? "finally"',
        T + 'done', T + 'return "fell through"'],
     ['finally', 'from handler']),
    ('F06', 'S3', 'a raise in the handler: the finally runs, then the raise resumes outward', [
        'try', T + 'try', T * 2 + 'Raise("in body")', T + 'catch', T * 2 + 'Raise("in handler")', T + 'finally',
        T * 2 + '? "finally after handler raise"', T + 'done', 'catch', T + '? "outer: " + cCatchError', 'done'],
     ['finally after handler raise', 'outer: in handler']),
    ('F07', 'S5', '`exit` crossing a try in a for loop runs its finally first', [
        'for i = 1 to 3', T + 'try', T * 2 + 'if i = 2 exit ok', T * 2 + '? "body " + String(i)', T + 'finally', T * 2 + '? "finally " + String(i)', T + 'done',
        'next', '? "after"'],
     ['body 1', 'finally 1', 'finally 2', 'after']),
    ('F08', 'S5', '`loop` crossing a try in a for loop runs its finally first, and the loop goes on', [
        'for i = 1 to 3', T + 'try', T * 2 + 'if i = 2 loop ok', T * 2 + '? "body " + String(i)', T + 'finally', T * 2 + '? "finally " + String(i)', T + 'done',
        T + '? "end " + String(i)', 'next'],
     ['body 1', 'finally 1', 'end 1', 'finally 2', 'body 3', 'finally 3', 'end 3']),
    ('F09', 'S5', '`exit` crossing a try with a catch, in a while loop', [
        'w()', 'func w', T + 'nN = 0', T + 'while true', T * 2 + 'nN++', T * 2 + 'try', T * 3 + 'if nN = 3 exit ok', T * 2 + 'catch',
        T * 3 + '? "no"', T * 2 + 'finally', T * 3 + '? "finally " + String(nN)', T * 2 + 'done', T + 'end', T + '? "after " + String(nN)'],
     ['finally 1', 'finally 2', 'finally 3', 'after 3']),
    ('F10', 'S2', 'a return crossing two trys runs the inner finally, then the outer', [
        '? h()', 'func h', T + 'try', T * 2 + 'try', T * 3 + 'return "value"', T * 2 + 'finally', T * 3 + '? "inner finally"', T * 2 + 'done',
        T + 'finally', T * 2 + '? "outer finally"', T + 'done'],
     ['inner finally', 'outer finally', 'value']),
    ('F11', 'S5', '`exit 2` crossing two loops and two trys runs both finallys, inner first, once each', [
        'for i = 1 to 2', T + 'try', T * 2 + 'for j = 1 to 2', T * 3 + 'try', T * 4 + 'exit 2', T * 3 + 'finally', T * 4 + '? "inner " + String(i) + String(j)',
        T * 3 + 'done', T * 2 + 'next', T + 'finally', T * 2 + '? "outer " + String(i)', T + 'done', 'next', '? "after"'],
     ['inner 11', 'outer 1', 'after']),
    ('F12', 'S1', 'a raise in the finally on the return path goes outward: the finally does not run twice', [
        'try', T + '? k()', 'catch', T + '? "caught: " + cCatchError', 'done', 'func k', T + 'try', T * 2 + 'return "value"', T + 'finally',
        T * 2 + '? "finally"', T * 2 + 'Raise("from finally")', T + 'done'],
     ['finally', 'caught: from finally']),
    ('F13', 'S1', 'a raise in the finally on the exit path never lands in the same try\'s catch', [
        'try', T + 'for i = 1 to 3', T * 2 + 'try', T * 3 + 'exit', T * 2 + 'catch', T * 3 + '? "own catch: " + cCatchError', T * 2 + 'finally',
        T * 3 + '? "finally " + String(i)', T * 3 + 'Raise("from finally")', T * 2 + 'done', T + 'next', 'catch', T + '? "outer: " + cCatchError', 'done'],
     ['finally 1', 'outer: from finally']),
    ('F14', 'S3', 'a try inside the finally does not overwrite the error the finally holds', [
        'try', T + 'try', T * 2 + 'Raise("outer")', T + 'finally', T * 2 + 'try', T * 3 + 'Raise("inner")', T * 2 + 'catch', T * 2 + 'done',
        T + 'done', 'catch', T + '? "outer caught: " + cCatchError', 'done'],
     ['outer caught: outer']),
    ('F15', 'S4', 'a return in the finally replaces a held return', [
        '? m()', 'func m', T + 'try', T * 2 + 'return "from body"', T + 'finally', T * 2 + 'return "from finally"', T + 'done'],
     ['from finally']),
    ('F16', 'S4', 'a return in the finally replaces a held raise', [
        '? m2()', 'func m2', T + 'try', T * 2 + 'Raise("dropped")', T + 'finally', T * 2 + 'return "from finally"', T + 'done'],
     ['from finally']),
    ('F17', 'S5', '`exit` crossing a try in a for-in loop', [
        'for x in [1, 2, 3]', T + 'try', T * 2 + 'if x = 2 exit ok', T + 'finally', T * 2 + '? "finally " + String(x)', T + 'done', 'next', '? "after"'],
     ['finally 1', 'finally 2', 'after']),
    ('F18', 'S5', '`loop` crossing a try in a do-again loop', [
        'd()', 'func d', T + 'nN = 0', T + 'do', T * 2 + 'nN++', T * 2 + 'try', T * 3 + 'if nN = 2 loop ok', T * 3 + '? "body " + String(nN)', T * 2 + 'finally',
        T * 3 + '? "finally " + String(nN)', T * 2 + 'done', T + 'again nN < 3'],
     ['body 1', 'finally 1', 'finally 2', 'body 3', 'finally 3']),
    ('F19', 'S2', 'a return from a loop inside the try body runs the finally once', [
        '? r()', 'func r', T + 'try', T * 2 + 'for i = 1 to 5', T * 3 + 'if i = 2 return "at " + String(i) ok', T * 2 + 'next', T + 'finally',
        T * 2 + '? "finally once"', T + 'done'],
     ['finally once', 'at 2']),
    ('F20', 'S2', 'a return crossing a try without finally inside one with: both handlers are left, and a later raise lands where it is raised', [
        '? s()', 'try', T + 'Raise("later")', 'catch', T + '? "later caught at top: " + cCatchError', 'done', 'func s', T + 'try', T * 2 + 'try',
        T * 3 + 'return "v"', T * 2 + 'catch', T * 3 + '? "no"', T * 2 + 'done', T + 'finally', T * 2 + '? "finally"', T + 'done'],
     ['finally', 'v', 'later caught at top: later']),
    ('F21', 'S5', '`loop` from the handler crosses the finally', [
        'for i = 1 to 2', T + 'try', T * 2 + 'Raise("e" + String(i))', T + 'catch', T * 2 + '? "caught " + cCatchError', T * 2 + 'loop', T + 'finally',
        T * 2 + '? "finally " + String(i)', T + 'done', T + '? "not reached " + i', 'next'],
     ['caught e1', 'finally 1', 'caught e2', 'finally 2']),
    ('F22', 'S2', 'a return from a `catch(e)` handler uses e, then the finally runs before it resumes', [
        '? t()', 'func t', T + 'try', T * 2 + 'Raise("why")', T + 'catch(e)', T * 2 + 'return "handled " + e', T + 'finally', T * 2 + '? "finally"',
        T + 'done'],
     ['finally', 'handled why']),
    ('F23', 'S2', 'a return in an eval string runs the finally of the eval\'s try', [
        '? Eval("try" + nl + "return 6" + nl + "finally" + nl + "? :f" + nl + "done")'],
     ['f', '6']),
    # F24 was written AFTER the compiler change, found by designing the plants (plants.py P9): no case had a loop INSIDE a try body, so a loop
    # that forgot which regions were open at its entry would have run the enclosing finally at every exit, and no fixture would have said so.
    ('F24', 'S1', '`exit` from a loop inside the try body stays inside it: the finally runs once, at the end of the try', [
        'try', T + 'for i = 1 to 3', T * 2 + 'if i = 2 exit ok', T * 2 + '? "body " + String(i)', T + 'next', T + '? "after loop"', 'finally',
        T + '? "finally"', 'done'],
     ['body 1', 'after loop', 'finally']),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for cid, line, why, prog, want in CASES:
    name = f'cases/{cid}.haro'
    with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(prog) + '\n')
    out.append({'id': cid, 'line': line, 'why': why, 'file': name, 'stdout': '\n'.join(want) + '\n'})
doc = {'rung': 'v0.36', 'decision': 'D52 rung (1): A1 completed',
       'lines': {'S1': 'finally runs exactly once per entry of the try',
                 'S2': 'a return inside the body or the handler is held, the block runs, then the held exit resumes',
                 'S3': 'a raise inside the body or the handler is held, the block runs, then the held exit resumes',
                 'S4': 'a raise (or a return) inside finally replaces a held exit',
                 'S5': 'exit and loop crossing a try run its finally first'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
