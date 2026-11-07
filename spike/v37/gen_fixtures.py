"""Haro v0.37, D52 rung (2): A4's error value, `catch e`, and A1's cause. Written FIRST, before the VM or the compiler is touched.

What D52 decided (CHARTER.md D52, A4 amended): `e` is the error VALUE, which in a text context IS its message byte for byte -- so `"caught: " + e`, `? e`
and every read of `cCatchError` keep working -- and which answers `Message()`, `Code()`, `Span()` and `Cause()`. A1's line the last rung left open: a
raise inside `finally` replaces a held error, and the replaced error is attached as its CAUSE. And `catch e`, without parentheses, binds.

The lines this rung pins, each by the cases that name it:

  E1  `catch e` binds e, as `catch(e)` does -- and only when e is on the line of `catch`: a name on the next line is a statement, as it always was
  E2  in a text context the error is its message, byte for byte: concatenation, `?`, len, type, comparison, isString
  E3  e.Message() is the message as a plain string; e.Code() is Ring's code (R2, R14 ...) of an error the VM raised, "" for raise()
  E4  e.Span() is where it was raised: a list with :file and :line; a rethrow keeps the origin it had
  E5  e.Cause() is the error a raise in `finally` replaced -- a held raise of the body or of the handler -- and "" when nothing was held
  E6  the methods belong to the error and nothing else: a plain string, and any string made FROM an error, still refuses a method
  E7  `haro fmt` prints `catch e` as `catch(e)`: it read the name as a statement on its own line, which now changes what the program means

Measured on haro 3d47200 before this rung (runtime/v37/q): `catch e` reads e (R24); `? s.Message()` on a string is "Bad parameter type!"; an index
past the end is "Error (R2) : Array Access (Index out of range)"; 1 / 0 is "Error (R1) : Can't divide by zero"; `haro fmt` turns `catch e` into
`catch` and a statement `e` on the next line.

The desk's readings, written here before the code so the cases can hold them: raise(e) of an error value is a RETHROW -- it keeps e's origin (E4);
Message() returns a plain string, so it answers no method itself (E6); an error crossing an eval string arrives as its message (named, not covered).

  python spike/v37/gen_fixtures.py      writes v37/cases/*.haro and v37/fixtures.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

CASES = [
    ('G01', 'E1', '`catch e` binds the error to e', [
        'try', T + 'raise("x1")', 'catch e', T + '? "e=" + e', 'done'],
     ['e=x1']),
    ('G02', 'E1', '`catch e` with a finally; cCatchError still reads the same error', [
        'try', T + 'raise("x2")', 'catch e', T + '? e', T + '? cCatchError', 'finally', T + '? "f"', 'done'],
     ['x2', 'x2', 'f']),
    ('G03', 'E1', 'a name on the line AFTER `catch` stays a statement: it does not bind', [
        'f()', 'func f', T + 'e = "outer"', T + 'try', T * 2 + 'raise("z")', T + 'catch', T * 2 + 'e', T * 2 + '? "e is still " + e', T + 'done'],
     ['e is still outer']),
    # G04 CHANGED after the court spoke (v0.41, HARO-SURFACE-01): in a .haro file a keyword is lowercase, so `Catch` is a name -- the case
    # was `Catch err` and now spells the keyword as Haro does; what it pins (a comment after the binding) is unchanged.
    ('G04', 'E1', '`catch err` with a comment after it binds', [
        'try', T + 'raise("x4")', 'catch err   # the error', T + '? "err=" + err', 'done'],
     ['err=x4']),
    ('G05', 'E1', 'the shape of stzlib\'s recovered plugin code: `catch cError` in a function binds cError', [
        'p()', 'func p', T + 'try', T * 2 + 'raise("plugin failed")', T + 'catch cError', T * 2 + '? "handled: " + cError', T + 'done'],
     ['handled: plugin failed']),
    ('G06', 'E2', 'in a text context the error is its message, byte for byte', [
        'try', T + 'raise("boom")', 'catch e', T + '? "caught: " + e', T + '? e + "!"', T + '? len(e)', T + '? type(e)', T + '? e = "boom"',
        T + '? isString(e)', 'done'],
     ['caught: boom', 'boom!', '4', 'STRING', '1', '1']),
    ('G07', 'E3', 'Message() is the message, a plain string', [
        'try', T + 'raise("boom")', 'catch e', T + '? e.Message()', T + '? type(e.Message())', T + '? e.Message() = e', 'done'],
     ['boom', 'STRING', '1']),
    ('G08', 'E3', 'Code() of an error the VM raised is Ring\'s code', [
        'g()', 'func g', T + 'aL = [1]', T + 'try', T * 2 + '? aL[5]', T + 'catch e', T * 2 + '? e.Code()', T * 2 + '? e', T + 'done', T + 'try',
        T * 2 + 'x = 1 / 0', T + 'catch e2', T * 2 + '? e2.Code()', T + 'done'],
     ['R2', 'Error (R2) : Array Access (Index out of range)', 'R1']),
    ('G09', 'E3', 'Code() of a raise() is empty', [
        'try', T + 'raise("mine")', 'catch e', T + '? "[" + e.Code() + "]"', 'done'],
     ['[]']),
    ('G10', 'E3', 'the four names are Ring names: any case reaches them', [
        'try', T + 'raise("cased")', 'catch e', T + '? e.MESSAGE()', T + '? e.message()', T + '? "[" + e.code() + "]"', 'done'],
     ['cased', 'cased', '[]']),
    ('G11', 'E4', 'Span() is the file and the line where the error was raised', [
        'h()', 'func h', T + 'try', T * 2 + 'x = 1', T * 2 + 'raise("here")', T + 'catch e', T * 2 + 's = e.Span()', T * 2 + '? s[:line]',
        T * 2 + '? s[:file]', T + 'done'],
     ['5', 'G11.haro']),
    ('G12', 'E4', 'Span() of a VM error inside a called function is the line of the fault', [
        'h()', 'func h', T + 'try', T * 2 + 'deep()', T + 'catch e', T * 2 + '? e.Span()[:line]', T + 'done', 'func deep', T + 'aL = []',
        T + '? aL[1]'],
     ['10']),
    ('G13', 'E4', 'a finally with no catch raises the held error again, and its Span is still where it began', [
        'h()', 'func h', T + 'try', T * 2 + 'try', T * 3 + 'raise("origin")', T * 2 + 'finally', T * 3 + '? "cleanup"', T * 2 + 'done', T + 'catch e',
        T * 2 + '? e.Span()[:line]', T + 'done'],
     ['cleanup', '5']),
    ('G14', 'E4', 'raise(e) of an error value is a rethrow: it keeps the origin it had', [
        'h()', 'func h', T + 'try', T * 2 + 'try', T * 3 + 'raise("orig")', T * 2 + 'catch e', T * 3 + 'raise(e)', T * 2 + 'done', T + 'catch e2',
        T * 2 + '? e2 + " " + e2.Span()[:line]', T + 'done'],
     ['orig 5']),
    ('G15', 'E5', 'a raise in finally replaces the held raise of the body, which is its cause', [
        'try', T + 'try', T * 2 + 'raise("first")', T + 'finally', T * 2 + 'raise("second")', T + 'done', 'catch e', T + '? e', T + '? e.Cause()',
        T + '? e.Cause().Message()', 'done'],
     ['second', 'first', 'first']),
    ('G16', 'E5', 'a raise in finally replaces the held raise of the HANDLER, which is its cause', [
        'try', T + 'try', T * 2 + 'raise("body")', T + 'catch', T * 2 + 'raise("handler")', T + 'finally', T * 2 + 'raise("cleanup")', T + 'done',
        'catch e', T + '? e', T + '? e.Cause()', 'done'],
     ['cleanup', 'handler']),
    ('G17', 'E5', 'causes chain: each finally that replaces an error holds the one before', [
        'try', T + 'try', T * 2 + 'try', T * 3 + 'raise("a")', T * 2 + 'finally', T * 3 + 'raise("b")', T * 2 + 'done', T + 'finally',
        T * 2 + 'raise("c")', T + 'done', 'catch e', T + '? e + " <- " + e.Cause() + " <- " + e.Cause().Cause()', 'done'],
     ['c <- b <- a']),
    ('G18', 'E5', 'a raise in finally on the normal path has no cause: nothing was held', [
        'try', T + 'try', T * 2 + '? "ok"', T + 'finally', T * 2 + 'raise("late")', T + 'done', 'catch e', T + '? e', T + '? "[" + e.Cause() + "]"',
        'done'],
     ['ok', 'late', '[]']),
    ('G19', 'E5', 'an error the handler HANDLED is not a cause', [
        'try', T + 'try', T * 2 + 'raise("handled")', T + 'catch', T * 2 + '? "handled it"', T + 'finally', T * 2 + 'raise("after")', T + 'done',
        'catch e', T + '? e', T + '? "[" + e.Cause() + "]"', 'done'],
     ['handled it', 'after', '[]']),
    ('G20', 'E5', 'a raise in finally replacing a held RETURN has no cause', [
        'try', T + '? k()', 'catch e', T + '? e', T + '? "[" + e.Cause() + "]"', 'done', 'func k', T + 'try', T * 2 + 'return "value"', T + 'finally',
        T * 2 + 'raise("instead")', T + 'done'],
     ['instead', '[]']),
    ('G21', 'E5', 'a VM error in finally replaces the held raise too, and the cause is a whole error value', [
        'h()', 'func h', T + 'aL = []', T + 'try', T * 2 + 'try', T * 3 + 'raise("held")', T * 2 + 'finally', T * 3 + '? aL[3]', T * 2 + 'done',
        T + 'catch e', T * 2 + '? e.Code()', T * 2 + '? e.Cause() + " " + e.Cause().Span()[:line]', T + 'done'],
     ['R2', 'held 6']),
    # G22 CHANGED after the court spoke: plant P13 left the finally's handler armed at a return and this case still passed, because its later raise
    # sat inside a newer try. It now returns 300 times from that finally -- past the VM's 256 handlers, so a handler left armed each time overflows.
    ('G22', 'E5', 'a return from the finally of an error path leaves its handler: 300 of them leave none armed', [
        'for i = 1 to 300', T + 'm()', 'next', '? "300 returns from a finally"', 'try', T + 'raise("later")', 'catch e',
        T + '? "later caught at top: " + e', 'done', 'func m', T + 'try', T * 2 + 'raise("dropped")', T + 'finally', T * 2 + 'return "from finally"',
        T + 'done'],
     ['300 returns from a finally', 'later caught at top: later']),
    ('G23', 'E6', 'a plain string refuses a method, as it did', [
        'g()', 'func g', T + 'try', T * 2 + 's = "abc"', T * 2 + '? s.Message()', T + 'catch e', T * 2 + '? e', T + 'done'],
     ['Bad parameter type!']),
    ('G24', 'E6', 'a string made from an error is a plain string', [
        'g()', 'func g', T + 'try', T * 2 + 'raise("orig")', T + 'catch e', T * 2 + 't = e + ""', T * 2 + 'try', T * 3 + '? t.Message()', T * 2 + 'catch e2',
        T * 3 + '? e2', T * 2 + 'done', T * 2 + 'try', T * 3 + '? e.Message().Message()', T * 2 + 'catch e3', T * 3 + '? e3', T * 2 + 'done', T + 'done'],
     ['Bad parameter type!', 'Bad parameter type!']),
    ('G25', 'E2', 'the error value is assigned, passed and returned as itself', [
        'g()', 'func g', T + 'try', T * 2 + 'raise("travels")', T + 'catch e', T * 2 + 'f = e', T * 2 + '? f.Message()', T * 2 + '? show(e)', T + 'done',
        'func show x', T + 'return x.Message() + " from " + x.Span()[:line]'],
     ['travels', 'travels from 4']),
    ('G26', 'E2', 'cCatchError read after the handler is the last error, still its message', [
        'try', T + 'raise("last one")', 'catch e', 'done', '? cCatchError'],
     ['last one']),
    # G27-G30 were written AFTER the VM change, found by designing the plants (plants.py): no case raised a string a variable still held, made a
    # cause point back at its own error, called a method with an argument, or let a rethrown VM error go uncaught.
    ('G27', 'E6', 'raising a variable\'s string makes the ERROR, not the variable, answer the methods', [
        'g()', 'func g', T + 'm = "held"', T + 'try', T * 2 + 'raise(m)', T + 'catch e', T * 2 + '? e.Message()', T + 'done', T + 'try',
        T * 2 + '? m.Message()', T + 'catch e2', T * 2 + '? e2', T + 'done'],
     ['held', 'Bad parameter type!']),
    ('G28', 'E5', 'a finally that raises the held error again gives it no cause: a cause never points back at its own error', [
        'try', T + 'try', T * 2 + 'raise("a")', T + 'finally', T * 2 + 'raise(cCatchError)', T + 'done', 'catch e', T + '? e',
        T + '? "[" + e.Cause() + "]"', 'done'],
     ['a', '[]']),
    ('G29', 'E3', 'the four methods take no argument: given one, the error refuses as a string does', [
        'g()', 'func g', T + 'try', T * 2 + 'raise("x")', T + 'catch e', T * 2 + 'try', T * 3 + '? e.Message(1)', T * 2 + 'catch e2', T * 3 + '? e2',
        T * 2 + 'done', T + 'done'],
     ['Bad parameter type!']),
    ('G30', 'E4', 'a VM error a finally raises again, uncaught, is reported as the VM error it is -- not as a raise()', [
        'h()', 'func h', T + 'aL = []', T + 'try', T * 2 + '? aL[2]', T + 'finally', T * 2 + '? "cleanup"', T + 'done'],
     ['cleanup', '', 'Line 7 Error (R2) : Array Access (Index out of range) ', 'In function h() in file G30.haro', '',
      'Called from line 1 in file G30.haro '], 1),
]

FMT = [
    ('K01', 'E7', '`haro fmt` prints `catch e` as `catch(e)`, and a name on the next line as a statement', [
        'try', T + 'raise("x")', 'catch e', T + '? e', 'done', 'try', T + 'raise("y")', 'catch', T + 'e', 'done'],
     ['try', T + 'raise("x")', 'catch(e)', T + '? e', 'done', 'try', T + 'raise("y")', 'catch', T + 'e', 'done']),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for kind, rows in (('run', CASES), ('fmt', FMT)):
    for row in rows:
        cid, line, why, prog, want = row[:5]
        name = f'cases/{cid}.haro'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(prog) + '\n')
        case = {'id': cid, 'kind': kind, 'line': line, 'why': why, 'file': name, 'stdout': '\n'.join(want) + '\n'}
        if len(row) > 5:
            # an uncaught report: its last line ends without a newline, and the exit is the one named
            case['stdout'] = '\n'.join(want)
            case['exit'] = row[5]
        out.append(case)
doc = {'rung': 'v0.37', 'decision': 'D52 rung (2): A4 the error value, catch e, A1 the cause',
       'lines': {'E1': '`catch e` binds e, only when e is on the line of catch',
                 'E2': 'in a text context the error is its message, byte for byte',
                 'E3': 'Message() is the plain message; Code() is Ring\'s code of a VM error, "" for raise()',
                 'E4': 'Span() is the file and line where it was raised; a rethrow keeps its origin',
                 'E5': 'Cause() is the held error a raise in finally replaced, "" when nothing was held',
                 'E6': 'the methods belong to the error: a plain string, or one made from an error, refuses them',
                 'E7': 'haro fmt prints catch e as catch(e)'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
