"""Haro v0.39, D52 rung (4): A5's five checker rules in `haro check`. Written FIRST, before the checker is touched.

What D52 decided (CHARTER.md D52, A5 respelled): `haro/global-restored-by-hand` warn; `haro/listener-binds-all` warn, on a literal `0.0.0.0`, `::` or
`""` given to a listening native the checker is told of; `haro/text-run-as-code` err, a non-literal to `eval` unless it passed a validator named to
the checker; `haro/last-error-read` note now (`catch e` shipped in v0.37) and err when stzlib's sweep reads 0; `haro/handle-held-across-raise` warn.
`last-error-read` first.

The lines this rung pins, each by the cases that name it:

  R1  last-error-read: every read of `cCatchError` is a note -- in its handler (bind the error: `catch e`) and outside one (the last error of
      whoever raised); a binding, a write and a member of that name are not reads
  R2  text-run-as-code: `eval` of anything but literal text is an error, unless a validator the checker was told of (`--validators=`) is called
      in the same body; literal text, a `+` of literals included, is not
  R3  listener-binds-all: a literal "0.0.0.0", "::" or "" given directly to a listening native the checker was told of (`--listeners=`) is a
      warning; told of none, the checker says so on a line of its own -- and not with the words "NOT checked", which a gate reads as a checker shut
  R4  global-restored-by-hand: a body that saves a `$global` in a local and later writes it back from that local, outside a `finally`, is a
      warning at the save -- worded for whether a raise between leaves the global set, or a catch restores it by hand too; `within` and a
      restore in a `finally` are not
  R5  handle-held-across-raise: a local assigned an engine handle (a call named StzEngine...Create or StzEngine...Hold) that no `finally` of
      its body releases (a call naming Release, Destroy or Close with it), and that the body does not return, is a warning; a handle held
      in a `$global` is the program's, not the body's

Measured on haro 4e9e6e7 before this rung (runtime/v39): `haro check` reports none of the five; it exits 0 whatever it finds, and an eval in the
unit prints two "NOT checked" lines for the absence rules.

A `check` case runs `haro check <file> <args>` and pins every line but the detail paragraph under a finding -- the prose that explains it --
which may be reworded without a case changing: the file line, each finding's `row:col  severity  rule` line and its message line, the blank lines
and the count lines.

The desk's readings, written here before the code: a read of cCatchError IN its handler is reported too, because ruling 2's sweep counts every
read until it reads 0 (R1); "passed a validator" is a validator called anywhere in the same body, as stzlib's own rule reads it, so a helper whose
callers validate is reported (R2, T05); "" is a bind address only when given to a listener (R3); a by-hand restore that a catch also makes is
still reported, as A2 says the old shape is a finding (R4).

  python spike/v39/gen_fixtures.py      writes v39/cases/*.haro and v39/fixtures.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

M_IN = 'cCatchError read in its handler -- bind the error instead (`catch e`) and read e'
M_OUT = 'cCatchError read outside a handler -- it is the last error of whoever raised, not this code\'s'
M_EVAL = 'eval() runs text that is not a literal, and nothing in this body passed it to a validator'
NO_LISTEN = '  listener-binds-all: no listening native named (--listeners=), so no call was looked at'
# CHANGED after the court spoke: SHUT held a second line, `uninitialized-variable: NOT checked`, which `eval("x = " + c)` never prints -- the
# universe reads the eval's target from its literal prefix. Taken from a probe whose eval was opaque (`eval(c)`); T01-T05 changed with it.
SHUT = ['  undefined-function, unknown-class/-package: NOT checked -- the unit calls loadlib() or eval()']


def listen(name, lit):
    return f'{name}() given "{lit}" -- a listener bound to every interface'


def by_hand(g, local, line, catch):
    if catch:
        return f'{g} is saved in {local} here and written back by hand at line {line}, in a catch too -- `within {g} = ...` is this shape, written once'
    return f'{g} is saved in {local} here and written back by hand at line {line}, and a raise between leaves it set -- write `within {g} = ...`'


def held(local, call):
    return f'{local} holds an engine handle from {call}() and no finally releases it -- a raise between leaves it held'


def report(cid, findings, counts, tail):
    """the pinned lines of `haro check`: the file, each finding's two lines, the counts and the closing lines"""
    out = []
    if findings:
        out.append(f'{cid}.haro')
        for rc, sev, rule, msg in findings:
            out.append(f'  {rc}  {sev: <5}  {rule}')
            out.append(f'          {msg}')
    out.append('')
    e, w, n = counts
    out.append(f'  {e} error, {w} warn, 0 perf, {n} note   in 1 file(s)')
    return out + tail


CASES = [
    # ---- R1 last-error-read
    ('L01', 'R1', 'a read of cCatchError in its handler is a note', [
        'f()', 'func f', T + 'try', T * 2 + 'raise("x")', T + 'catch', T * 2 + '? cCatchError', T + 'done'], [],
     lambda c: report(c, [('6:5', 'note', 'haro/last-error-read', M_IN)], (0, 0, 1), [NO_LISTEN])),
    ('L02', 'R1', 'a read of cCatchError outside a handler is a note, worded for it', [
        'f()', 'func f', T + 'try', T * 2 + 'raise("x")', T + 'catch', T * 2 + 'c = 1', T + 'done', T + '? cCatchError'], [],
     lambda c: report(c, [('8:4', 'note', 'haro/last-error-read', M_OUT)], (0, 0, 1), [NO_LISTEN])),
    ('L03', 'R1', 'a binding, a write and a member of that name are not reads; `catch e` reads e', [
        'f()', 'func f', T + 'try', T * 2 + 'raise("x")', T + 'catch e', T * 2 + '? e', T + 'done', T + 'try', T * 2 + 'raise("y")',
        T + 'catch cCatchError', T * 2 + '? "bound"', T + 'done', T + 'cCatchError = ""', T + 'o = new K', T + '? o.cCatchError',
        'class K', T + 'cCatchError = "an attribute"'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    ('L04', 'R1', 'every read is counted: two reads in one handler are two notes', [
        'f()', 'func f', T + 'try', T * 2 + 'raise("x")', T + 'catch', T * 2 + '? cCatchError + "!"', T * 2 + 'see cCatchError', T + 'done'], [],
     lambda c: report(c, [('6:5', 'note', 'haro/last-error-read', M_IN), ('7:7', 'note', 'haro/last-error-read', M_IN)], (0, 0, 2), [NO_LISTEN])),
    # WRITTEN AFTER THE CODE (a plant of the column mapping found no case on a line the lift rewrote): `within` gains `try ` on its line,
    # and the note must still name the file's column, 14, not the lifted text's, 18.
    ('L05', 'R1', 'a read on a line the lift rewrote is named at the file\'s own column', [
        '$g = ""', 'f()', 'func f', T + 'within $g = cCatchError', T * 2 + '? $g', T + 'done'], [],
     lambda c: report(c, [('4:14', 'note', 'haro/last-error-read', M_OUT)], (0, 0, 1), [NO_LISTEN])),

    # ---- R2 text-run-as-code
    ('T01', 'R2', 'eval of text built at run time is an error', [
        'f("1")', 'func f c', T + 'x = 0', T + 'eval("x = " + c)'], [],
     lambda c: report(c, [('4:2', 'error', 'haro/text-run-as-code', M_EVAL)], (1, 0, 0), SHUT + [NO_LISTEN])),
    ('T02', 'R2', 'eval of literal text, a `+` of literals included, is not', [
        'f()', 'func f', T + 'x = 0', T + 'eval("x = 1")', T + 'eval("x = " + "2")'], [],
     lambda c: report(c, [], (0, 0, 0), SHUT + [NO_LISTEN])),
    ('T03', 'R2', 'a validator the checker was told of, called in the same body, clears it', [
        'f("1")', 'func f c', T + 'x = 0', T + 'if IsSafe(c)', T * 2 + 'eval("x = " + c)', T + 'ok', 'func IsSafe c', T + 'return 1'],
     ['--validators=IsSafe'],
     lambda c: report(c, [], (0, 0, 0), SHUT + [NO_LISTEN])),
    ('T04', 'R2', 'the same body, the checker told of no validator: an error', [
        'f("1")', 'func f c', T + 'x = 0', T + 'if IsSafe(c)', T * 2 + 'eval("x = " + c)', T + 'ok', 'func IsSafe c', T + 'return 1'], [],
     lambda c: report(c, [('5:3', 'error', 'haro/text-run-as-code', M_EVAL)], (1, 0, 0), SHUT + [NO_LISTEN])),
    ('T05', 'R2', 'a validator called in the caller does not clear the helper\'s eval', [
        'f("1")', 'func f c', T + 'if IsSafe(c) g(c) ok', 'func g c', T + 'x = 0', T + 'eval("x = " + c)', 'func IsSafe c', T + 'return 1'],
     ['--validators=IsSafe'],
     lambda c: report(c, [('6:2', 'error', 'haro/text-run-as-code', M_EVAL)], (1, 0, 0), SHUT + [NO_LISTEN])),

    # ---- R3 listener-binds-all
    ('N01', 'R3', '"0.0.0.0", "::" and "" given to a listener the checker was told of are warnings; 127.0.0.1 is not', [
        'Serve("0.0.0.0", 80)', 'Serve("::", 80)', 'Serve("", 80)', 'Serve("127.0.0.1", 80)', 'func Serve cHost, nPort', T + 'return 0'],
     ['--listeners=Serve'],
     lambda c: report(c, [('1:7', 'warn', 'haro/listener-binds-all', listen('Serve', '0.0.0.0')),
                          ('2:7', 'warn', 'haro/listener-binds-all', listen('Serve', '::')),
                          ('3:7', 'warn', 'haro/listener-binds-all', listen('Serve', ''))], (0, 3, 0), [])),
    ('N02', 'R3', 'told of no listener, the checker looks at none and says so', [
        'Serve("0.0.0.0", 80)', 'func Serve cHost, nPort', T + 'return 0'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    ('N03', 'R3', 'only a literal given directly: an address through a variable, or to another call, is not followed', [
        '$cHost = "0.0.0.0"', 'Serve($cHost, 80)', 'Other("0.0.0.0")', 'func Serve cHost, nPort', T + 'return 0', 'func Other c', T + 'return 0'],
     ['--listeners=Serve'],
     lambda c: report(c, [], (0, 0, 0), [])),

    # ---- R4 global-restored-by-hand
    ('G01', 'R4', 'saved, set, and written back by hand with nothing on a raise: a warning at the save', [
        '$g = "a"', 'f()', 'func f', T + 'cOld = $g', T + '$g = "b"', T + 'work()', T + '$g = cOld', 'func work', T + 'return 0'], [],
     lambda c: report(c, [('4:2', 'warn', 'haro/global-restored-by-hand', by_hand('$g', 'cOld', 7, False))], (0, 1, 0), [NO_LISTEN])),
    ('G02', 'R4', 'written back in a catch and after it: still by hand, worded for it', [
        '$g = "a"', 'f()', 'func f', T + 'cOld = $g', T + '$g = "b"', T + 'try', T * 2 + 'work()', T + 'catch e', T * 2 + '$g = cOld',
        T * 2 + 'raise(e)', T + 'done', T + '$g = cOld', 'func work', T + 'return 0'], [],
     lambda c: report(c, [('4:2', 'warn', 'haro/global-restored-by-hand', by_hand('$g', 'cOld', 9, True))], (0, 1, 0), [NO_LISTEN])),
    ('G03', 'R4', 'written back in a finally, or with within: not by hand', [
        '$g = "a"', 'f()', 'func f', T + 'cOld = $g', T + 'try', T * 2 + '$g = "b"', T + 'finally', T * 2 + '$g = cOld', T + 'done',
        T + 'within $g = "c"', T * 2 + '? $g', T + 'done'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    ('G04', 'R4', 'a global read into a local and never written back from it is no save', [
        '$g = "a"', 'f()', 'func f', T + 'x = $g', T + '$g = "b"', T + '$g = x + "!"', T + 'y = $g', T + '$g = "c"'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    # WRITTEN AFTER THE CODE (plants of R4's order, its `=` and its `$` found no case): a write-back before the save is no restore, nor is
    # a compound write, and two locals swapped are no global.
    ('G05', 'R4', 'a write-back before its save, a compound write, and two locals swapped, are no restore', [
        '$g = "a"', 'f()', 'func f', T + 'cOld = "x"', T + '$g = cOld', T + 'cOld = $g', T + '$g += cOld', T + 'a = 1', T + 'b = a', T + 'a = b'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),

    # ---- R5 handle-held-across-raise
    ('H01', 'R5', 'a handle released on the normal path only: a warning where it is taken', [
        'f()', 'func f', T + 'nH = StzEngineSecretHold("k")', T + 'use(nH)', T + 'StzEngineSecretRelease(nH)',
        'func StzEngineSecretHold c', T + 'return 1', 'func StzEngineSecretRelease n', T + 'return 0', 'func use n', T + 'return 0'], [],
     lambda c: report(c, [('3:2', 'warn', 'haro/handle-held-across-raise', held('nH', 'StzEngineSecretHold'))], (0, 1, 0), [NO_LISTEN])),
    ('H02', 'R5', 'a handle a finally releases is not held across a raise', [
        'f()', 'func f', T + 'nH = StzEngineCacheCreate(8)', T + 'try', T * 2 + 'use(nH)', T + 'finally', T * 2 + 'StzEngineCacheDestroy(nH)', T + 'done',
        'func StzEngineCacheCreate n', T + 'return 1', 'func StzEngineCacheDestroy n', T + 'return 0', 'func use n', T + 'return 0'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    ('H03', 'R5', 'a handle the body returns, or holds in a global, is not this body\'s to release', [
        'f()', 'g()', 'func f', T + 'nH = StzEngineCacheCreate(8)', T + 'return nH', 'func g', T + '$nCache = StzEngineCacheCreate(8)',
        'func StzEngineCacheCreate n', T + 'return 1'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    ('H04', 'R5', 'a handle never released is held too; a Create that is not the engine\'s is no handle', [
        'f()', 'func f', T + 'nH = StzEngineCacheCreate(8)', T + 'use(nH)', T + 'nX = MakeCreate()', 'func StzEngineCacheCreate n', T + 'return 1',
        'func MakeCreate', T + 'return 1', 'func use n', T + 'return 0'], [],
     lambda c: report(c, [('3:2', 'warn', 'haro/handle-held-across-raise', held('nH', 'StzEngineCacheCreate'))], (0, 1, 0), [NO_LISTEN])),

    # WRITTEN AFTER THE CODE: found on stzlib f77486b5a, where 9 of the rule's first 14 findings were a method writing a handle into its
    # class's declared attribute -- the object's, kept on purpose for its Release().
    ('H05', 'R5', 'a method writing a handle into an attribute its class declares holds it in the object, not a local', [
        '$o = new Token', '$o.Open()', 'func StzEngineCancelCreate', T + 'return 1', 'func StzEngineCancelDestroy n', T + 'return 0',
        'class Token', T + 'pHandle = 0', T + 'func Open', T * 2 + 'pHandle = StzEngineCancelCreate()', T + 'func Release',
        T * 2 + 'StzEngineCancelDestroy(pHandle)'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
    # WRITTEN AFTER THE CODE: stzlib's stzCancelToken.ring, where the grammar ends the class after its first attribute (a comment line follows
    # it) and leaves the next attribute and every method at the top level, which the compiler reads as the class's.
    ('H06', 'R5', 'the same, where the grammar ends the class early and its methods stand at the top level', [
        '$o = MakeToken()', '$o.Open()', 'func StzEngineCancelCreate', T + 'return 1', 'func StzEngineCancelDestroy n', T + 'return 0',
        'func MakeToken()', T + 'return new Token()', '', '# the shape of stzCancelToken.ring: a function returning the new object, a comment, the class',
        '', 'class Token', '', T + 'nOther = 0', T + '# a comment line after an attribute', T + 'pHandle = 0', '', T + 'def Open()',
        T * 2 + 'pHandle = StzEngineCancelCreate()', '', T + 'def Release()', T * 2 + 'StzEngineCancelDestroy(pHandle)'], [],
     lambda c: report(c, [], (0, 0, 0), [NO_LISTEN])),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for cid, line, why, prog, args, want in CASES:
    name = f'cases/{cid}.haro'
    with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(prog) + '\n')
    out.append({'id': cid, 'kind': 'check', 'line': line, 'why': why, 'file': name, 'args': args, 'stdout': '\n'.join(want(cid)) + '\n'})
doc = {'rung': 'v0.39', 'decision': 'D52 rung (4): A5, the five checker rules',
       'lines': {'R1': 'last-error-read: every read of cCatchError is a note, worded in its handler or outside one',
                 'R2': 'text-run-as-code: eval of non-literal text is an error unless a named validator is called in the same body',
                 'R3': 'listener-binds-all: a literal 0.0.0.0, :: or "" given to a named listener is a warning; told of none, it says so',
                 'R4': 'global-restored-by-hand: a $global saved in a local and written back from it outside a finally is a warning',
                 'R5': 'handle-held-across-raise: a local engine handle no finally releases, and the body does not return, is a warning'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
