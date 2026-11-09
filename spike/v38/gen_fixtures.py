"""Haro v0.38, D52 rung (3): A2 `within` and A3 `using`, rewritten onto rung (1)'s `finally`. Written FIRST, before the lift, the compiler or the
printer is touched.

What D52 decided (CHARTER.md D52): `within $global = value ... done` -- a global only, a local needs no restore -- compiles to a save, the body, and a
`finally` that restores (A2, unamended). `using name = expression ... done` calls the first of `Release`, `Destroy`, `Close` the value answers to, on
every exit (A3); a value that answers none is refused at compile time WHERE ITS CLASS IS KNOWN THERE (`new K`), and otherwise at the block's ENTRY,
before the body runs -- never a silent no-op (A3, amended for a dynamic surface). The vendored parser is not regenerated: both are rewritten before the
parse onto forms it already reads, as `not` and `catch e` are.

The lines this rung pins, each by the cases that name it:

  W1  inside `within`, the global holds the value -- in the body and in everything the body calls -- and after the block it holds what it held before
  W2  the global is restored on EVERY exit: a raise, a return, an exit or a loop crossing the block, a raise in a function it calls; a write the body
      or a callee makes to the global is undone
  W3  the old value is saved FIRST, then the value is computed (it may read the global), then the body runs; if the value raises, the global is
      unchanged and the body never runs; a global with no value yet cannot be saved (R24 at the `within` line)
  W4  `within` names a global (`$name`); a local or a parameter is refused at compile time
  U1  inside `using`, the name holds the value; at the end the first of Release, Destroy, Close the value answers to is called, once -- in any
      case of the name, and an inherited method counts
  U2  it is called on EVERY exit: a raise, a return, an exit, a loop; a raise in it replaces a held raise, which becomes its cause (A1)
  U3  `new K` of a class the unit defines, answering none of the three, is refused at compile time; any other value answering none -- an object or
      not an object -- is raised at the block's entry, before the body, and can be caught; a value rebound by a callee is raised at the exit
  U4  the name of a `using` cannot be rebound inside its block: refused at compile time
  B1  the blocks nest with `try` in every shape the grammar mis-reads (inside a try body, inside a catch clause, around a try) and with each other,
      and every line keeps its number
  B2  only the statement form is a block: `within` or `using` assigned, called or read as a name is what it was; a block with no `done`, no
      `= value` on its line, or a `catch` of its own is refused at compile time
  B3  `haro fmt` prints both blocks, the header on one line and the body a level in: before this rung it printed them as flat statements, which
      would now change what the program means

Measured on haro 00e0794 before this rung (runtime/v38): `within $g = 2` reads `within` as a variable and raises R24 ("Using uninitialized
variable: within") at its line; the census compiles all six statements of that program and refuses none; the parser reads `within`, `using` and a
`done` outside a try's clauses as bare identifiers, and reads a `done` INSIDE a try's catch clause as that try's end.

The desk's readings, written here before the code so the cases can hold them: the value is computed after the save, so it may read the global
(W3); a global with no value cannot be saved and is R24, as reading it is (A2: an ambient value "must exist"); the using name cannot be rebound in
its block -- a rebound name would release the new value and leak the old, so it is refused, not followed (U4); a literal (`using n = 42`) is
judged at entry like any value whose class the compiler does not know (U3); the refusal at entry is the VM's error, not a raise(), so its report
names no raise().

  python spike/v38/gen_fixtures.py      writes v38/cases/*.haro and v38/fixtures.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

RES = ['class Res', T + 'tName = ""', T + 'func init tN', T * 2 + 'tName = tN', T + 'func release', T * 2 + '? "release " + tName']
PLAIN = ['class Plain', T + 'nX = 1']
REFUSED = 'and did not compile it -- running past it would give a wrong answer '


def refused(cid, line, why, text, at, called):
    """the report of a refused statement in f(), called from line `called`; the trap is at the statement's line `line`, the refusal at `at`"""
    return ['before', '', f'Line {line} Haro refused this statement ({why} `{text}`, line {at} of {cid}.haro) ' + REFUSED,
            f'In function f() in file {cid}.haro', '', f'Called from line {called} in file {cid}.haro ']


R_GLOBAL = 'within needs a global (D52 A2)'
R_BARE = 'within or using without its block (D52)'
# CHANGED after the court spoke: it read "with a catch or finally of its own" until a finally of the block's own -- which only a hand-written
# `try within` can have -- was let run after the restore instead of refused; B06's bytes changed with it.
R_CLAUSE = 'within or using with a catch of its own (D52)'
R_CLASS = 'using a class that answers none of Release, Destroy, Close (D52 A3)'
R_REBIND = 'using rebinds its name inside its block (D52 A3)'

CASES = [
    # v0.48 RE-SPELLED, 2026-11-09, AFTER THIS COURT SPOKE (the Principal's ruling, "ParentClassName"): a .haro program's calls of
    # built-ins are spelled as Softanza writes a name (Len, IsNull, SubStr), by study/v48/respell.py, ported here by
    # study/v47/port_cases.py --respell. A report still names a built-in as the VM registers it. Each case asks what it asked.
    # v0.47 RE-LETTERED, 2026-11-08, AFTER THIS COURT SPOKE (D55 T2, the author's scope "Yes, as recommended"): every name of these
    # .haro programs carries its type's letter, by study/v47/reletter.py's rules (c -> t, a single letter or a word by what it holds),
    # ported here by study/v47/port_cases.py; an output that names a renamed variable names its new name. Each case asks what it asked.
    # By hand: Res's init takes a text (tN), Plain's attribute is nX, U12's eval strings say oRes and $tG, K01's fmt text follows its
    # program, W08's R24 names $nnever as R24 folds a name; B03 moved to the Ring surface (cases/B03.ring), its program as it was, since
    # a .haro name always carries a letter and so is never `within` or `using`.
    ('W01', 'W1', 'the global holds the value in the body and in what the body calls; after the block, what it held before', [
        '$tCaller = "nobody"', 'within $tCaller = "agent-x"', T + '? "in: " + $tCaller', T + 'who()', 'done', '? "after: " + $tCaller',
        'func who', T + '? "who: " + $tCaller'],
     ['in: agent-x', 'who: agent-x', 'after: nobody']),
    ('W02', 'W2', 'a raise out of the block restores the global before the handler runs', [
        '$nG = 1', 'try', T + 'within $nG = 2', T * 2 + '? $nG', T * 2 + 'Raise("boom")', T + 'done', 'catch e', T + '? "caught " + e + ", g=" + String($nG)',
        'done'],
     ['2', 'caught boom, g=1']),
    ('W03', 'W2', 'a return out of the block restores the global; the value returned was computed inside it', [
        '$tG = "a"', '? f()', '? $tG', 'func f', T + 'within $tG = "b"', T * 2 + 'return "returned " + $tG', T + 'done'],
     ['returned b', 'a']),
    ('W04', 'W2', 'a loop and an exit crossing the block restore the global', [
        '$nG = 0', 'for i = 1 to 3', T + '? "top g=" + String($nG)', T + 'within $nG = i * 10', T * 2 + 'if i = 1 loop ok', T * 2 + '? "i=" + String(i) + " g=" + String($nG)',
        T * 2 + 'if i = 2 exit ok', T + 'done', 'next', '? "g=" + String($nG)'],
     ['top g=0', 'top g=0', 'i=2 g=20', 'g=0']),
    ('W05', 'W2', 'a write by the body and by a callee is undone; a callee\'s raise restores too', [
        '$tG = "start"', 'try', T + 'within $tG = "mid"', T * 2 + '$tG = "changed in body"', T * 2 + 'setG()', T + 'done', 'catch e', T + '? e', 'done',
        '? $tG', 'func setG', T + '$tG = "changed by callee"', T + 'Raise("from callee " + $tG)'],
     ['from callee changed by callee', 'start']),
    ('W06', 'W3', 'the value may read the global: a depth that counts its own recursion and ends where it began', [
        '$xDepth = 0', 'nest(3)', '? "depth after: " + String($xDepth)', 'func nest nN', T + 'within $xDepth = $xDepth + 1', T * 2 + '? "depth " + String($xDepth)',
        T * 2 + 'if nN > 1 nest(nN - 1) ok', T + 'done'],
     ['depth 1', 'depth 2', 'depth 3', 'depth after: 0']),
    ('W07', 'W3', 'a value that raises leaves the global unchanged and the body unrun', [
        '$tG = "kept"', 'try', T + 'within $tG = boom()', T * 2 + '? "body ran"', T + 'done', 'catch e', T + '? "caught " + e', 'done', '? $tG',
        'func boom', T + 'Raise("no value")'],
     ['caught no value', 'kept']),
    ('W08', 'W3', 'a global with no value yet cannot be saved: R24 at the within line, the body unrun', [
        '? "before"', 'f()', 'func f', T + 'within $nNever = 1', T * 2 + '? "body ran"', T + 'done'],
     ['before', '', 'Line 4 Error (R24) : Using uninitialized variable: $nnever ', 'In function f() in file W08.haro', '',
      'Called from line 2 in file W08.haro '], 1),
    ('W09', 'W4', 'a local is refused: it needs no restore', [
        '? "before"', 'f()', 'func f', T + 'nX = 1', T + 'within nX = 2', T * 2 + '? nX', T + 'done'],
     refused('W09', 5, R_GLOBAL, 'nX', 5, 2), 1),
    ('W10', 'W4', 'a parameter is refused', [
        '? "before"', 'f(1)', 'func f xP', T + 'within xP = 2', T * 2 + '? xP', T + 'done'],
     refused('W10', 4, R_GLOBAL, 'xP', 4, 2), 1),
    ('W11', 'W2', 'a list global grown in place inside the block is the old list after it', [
        '$aL = [1, 2]', 'within $aL = $aL', T + 'Add($aL, 3)', T + '? Len($aL)', 'done', '? Len($aL)'],
     ['3', '2']),

    ('U01', 'U1', 'the name holds the value in the body; Release at the end, once', [
        'f()', 'func f', T + 'using oO = new Res("a")', T * 2 + '? "in: " + oO.tName', T + 'done', T + '? "after"'] + RES,
     ['in: a', 'release a', 'after']),
    ('U02', 'U1', 'the first of Release, Destroy, Close the value answers to, in any case, an inherited one counting', [
        'f()', 'func f', T + 'using oA = new OnlyClose', T * 2 + '? "body a"', T + 'done', T + 'using oB = new DestroyAndClose', T * 2 + '? "body b"',
        T + 'done', T + 'using oC = new Child', T * 2 + '? "body c"', T + 'done', T + 'using oD = new All', T * 2 + '? "body d"', T + 'done',
        'class OnlyClose', T + 'func close', T * 2 + '? "close"',
        'class DestroyAndClose', T + 'func Close', T * 2 + '? "close (wrong)"', T + 'func DESTROY', T * 2 + '? "destroy"',
        'class Base', T + 'func release', T * 2 + '? "release (inherited)"',
        'class Child from Base', T + 'func close', T * 2 + '? "close (wrong)"',
        'class All', T + 'func close', T * 2 + '? "close (wrong)"', T + 'func destroy', T * 2 + '? "destroy (wrong)"', T + 'func Release',
        T * 2 + '? "release"'],
     ['body a', 'close', 'body b', 'destroy', 'body c', 'release (inherited)', 'body d', 'release']),
    ('U03', 'U2', 'a raise out of the block releases before the handler runs', [
        'f()', 'func f', T + 'try', T * 2 + 'using oO = new Res("r")', T * 3 + 'Raise("boom")', T * 2 + 'done', T + 'catch e',
        T * 2 + '? "caught " + e', T + 'done'] + RES,
     ['release r', 'caught boom']),
    ('U04', 'U2', 'a return, a loop and an exit release, once each', [
        '? g()', 'h()', '? "end"', 'func g', T + 'using oO = new Res("g")', T * 2 + 'return "returned " + oO.tName', T + 'done', 'func h',
        T + 'for i = 1 to 3', T * 2 + 'using oO = new Res("i" + String(i))', T * 3 + 'if i = 1 loop ok', T * 3 + 'if i = 3 exit ok', T * 3 + '? "body " + String(i)',
        T * 2 + 'done', T + 'next'] + RES,
     ['release g', 'returned g', 'release i1', 'body 2', 'release i2', 'release i3', 'end']),
    ('U05', 'U2', 'a raise in the release replaces the held raise, which is its cause', [
        'f()', 'func f', T + 'try', T * 2 + 'using oO = new Bad', T * 3 + 'Raise("in body")', T * 2 + 'done', T + 'catch e',
        T * 2 + '? "caught " + e', T * 2 + '? "cause " + e.Cause()', T + 'done', 'class Bad', T + 'func release', T * 2 + 'Raise("in release")'],
     ['caught in release', 'cause in body']),
    ('U06', 'U3', '`new K` of a class the unit defines with none of the three is refused at compile time', [
        '? "before"', 'f()', 'func f', T + 'using oO = new Plain', T * 2 + '? "body"', T + 'done'] + PLAIN,
     refused('U06', 4, R_CLASS, 'Plain', 4, 2), 1),
    ('U07', 'U3', 'any other value with none -- an object, a number -- is raised at entry, before the body, and caught', [
        'f()', 'func f', T + 'try', T * 2 + 'using xO = make()', T * 3 + '? "body ran"', T * 2 + 'done', T + 'catch e', T * 2 + '? "caught: " + e',
        T * 2 + '? "line " + String(e.Span()[:line]) + ", code [" + e.Code() + "]"', T + 'done', T + 'try', T * 2 + 'using nN = 42', T * 3 + '? "body ran"',
        T * 2 + 'done', T + 'catch e', T * 2 + '? "caught: " + e', T + 'done', 'func make', T + 'return new Plain'] + PLAIN,
     ['caught: using: xO answers none of Release, Destroy, Close', 'line 4, code []', 'caught: using: nN answers none of Release, Destroy, Close']),
    ('U08', 'U3', 'uncaught, the refusal at entry is reported at the using line, and names no raise()', [
        '? "before"', 'f()', 'func f', T + 'using xO = make()', T * 2 + '? "body"', T + 'done', 'func make', T + 'return new Plain'] + PLAIN,
     ['before', '', 'Line 4 using: xO answers none of Release, Destroy, Close ', 'In function f() in file U08.haro', '',
      'Called from line 2 in file U08.haro '], 1),
    ('U09', 'U4', 'the name rebound in the block is refused at compile time', [
        '? "before"', 'f()', 'func f', T + 'using oO = new Res("a")', T * 2 + 'oO = new Res("b")', T + 'done'] + RES,
     refused('U09', 4, R_REBIND, 'oO = new Res("b")', 5, 2), 1),
    ('U10', 'U3', 'a global using name a callee rebinds to a value with none is raised at the exit', [
        'f()', 'func f', T + 'try', T * 2 + 'using $xR = new Res("a")', T * 3 + 'swap()', T * 2 + 'done', T + 'catch e', T * 2 + '? "caught: " + e',
        T + 'done', 'func swap', T + '$xR = 5'] + RES,
     ['caught: using: $xR answers none of Release, Destroy, Close']),

    ('B01', 'B1', 'within inside a try body, inside a catch clause, inside itself; a try inside within', [
        '$nG = 0', 'try', T + 'within $nG = 1', T * 2 + 'within $nG = 2', T * 3 + '? "inner " + String($nG)', T * 2 + 'done', T * 2 + '? "outer " + String($nG)', T + 'done',
        T + 'Raise("go")', 'catch', T + 'within $nG = 3', T * 2 + 'try', T * 3 + '? "in catch " + String($nG)', T * 3 + 'Raise("again")', T * 2 + 'catch',
        T * 3 + '? "nested catch " + String($nG)', T * 2 + 'done', T + 'done', T + '? "after catch block " + String($nG)', 'done', '? "end " + String($nG)'],
     ['inner 2', 'outer 1', 'in catch 3', 'nested catch 3', 'after catch block 0', 'end 0']),
    ('B02', 'B1', 'using inside within, a try inside both; a raise keeps its own line', [
        '$tG = "a"', 'f()', 'func f', T + 'within $tG = "b"', T * 2 + 'using oO = new Res("r")', T * 3 + 'try', T * 4 + 'Raise("x")', T * 3 + 'catch e',
        T * 4 + '? "span line " + String(e.Span()[:line])', T * 3 + 'done', T * 3 + '? "g " + $tG', T * 2 + 'done', T + 'done', T + '? "g " + $tG'] + RES,
     ['span line 7', 'g b', 'release r', 'g a']),
    ('B03', 'B2', '`within` and `using` assigned, called, or an attribute, are what they were', [
        'f()', 'func f', T + 'within = "a word"', T + 'using = 2', T + '? within + " " + string(using)', T + 'o = new App', T + '? o.Within', T + 'Using(5)',
        'func Using n', T + '? "Using called with " + string(n)', 'class App', T + 'Within = "attribute"'],
     ['a word 2', 'attribute', 'Using called with 5']),
    ('B04', 'B2', 'a block with no `done` is refused', [
        '? "before"', 'f()', 'func f', T + 'within $nG = 1', T * 2 + '? "body"'],
     refused('B04', 4, R_BARE, 'within', 4, 2), 1),
    ('B05', 'B2', 'a block with no `= value` on its line is refused', [
        '? "before"', 'f()', 'func f', T + 'within $g', T * 2 + '? "body"', T + 'done'],
     refused('B05', 4, R_BARE, 'within', 4, 2), 1),
    ('B06', 'B2', 'a block with a catch of its own is refused', [
        '? "before"', 'f()', 'func f', T + 'within $nG = 1', T * 2 + '? "body"', T + 'catch', T * 2 + '? "c"', T + 'done'],
     refused('B06', 4, R_CLAUSE, 'catch', 6, 2), 1),

    # WRITTEN AFTER THE CODE, each found by designing a plant that no case above could catch: a using whose value raises has nothing to release
    # (the header is compiled before the handler is armed); both blocks in an eval string (the release failed there: an eval may not name a
    # verb the program never names); a try closed by `end` inside a block (the other ends of a try close too); a header on the line after its
    # word, and a bare word as a try's first statement (each refused as a block without its parts, and not as a try's own catch).
    ('U11', 'U3', 'a using whose value raises releases nothing: the raise is the one caught', [
        'f()', 'func f', T + 'try', T * 2 + 'using xO = boom()', T * 3 + '? "body ran"', T * 2 + 'done', T + 'catch e', T * 2 + '? "caught " + e',
        T + 'done', 'func boom', T + 'Raise("no value")'],
     ['caught no value']),
    ('U12', 'U1', 'both blocks inside an eval string: the release runs, though the program never names Destroy or Close', [
        'f()', 'func f', T + 'Eval("using oRes = new Res(" + Char(34) + "e" + Char(34) + ")" + nl + "? " + Char(34) + "in eval " + Char(34) + " + oRes.tName" + nl + "done")',
        T + '$tG = "a"', T + 'Eval("within $tG = " + Char(34) + "b" + Char(34) + nl + "? $tG" + nl + "done")', T + '? $tG'] + RES,
     ['in eval e', 'release e', 'b', 'a']),
    ('B07', 'B2', 'a bare word as the first statement of a try, its block unclosed, is refused as a block without its parts', [
        '? "before"', 'f()', 'func f', T + 'try', T * 2 + 'within $nG = 1', T * 2 + '? "x"', T + 'catch', T + 'done'],
     refused('B07', 5, R_BARE, 'within', 5, 2), 1),
    ('B08', 'B2', 'a header on the line after its word is no header', [
        '? "before"', 'f()', 'func f', T + 'within', T * 2 + '$nG = 1', T * 2 + '? "body"', T + 'done'],
     refused('B08', 4, R_BARE, 'within', 4, 2), 1),
    ('B10', 'B1', 'a try closed by `end` inside a block', [
        '$tG = "a"', 'within $tG = "b"', T + 'try', T * 2 + 'Raise("x")', T + 'catch', T * 2 + '? "caught in " + $tG', T + 'end', 'done', '? $tG'],
     ['caught in b', 'a']),
]

FMT = [
    ('K01', 'B3', '`haro fmt` prints both blocks, the header on one line and the body a level in, inside a try and its catch', [
        'within $nG = 1', '? $nG', 'done', 'try', 'within $nH = 2', '$nX = 1', 'done', 'catch', 'using $oO   =   new K', '? $oO', 'done', 'done'],
     ['within $nG = 1', T + '? $nG', 'done', 'try', T + 'within $nH = 2', T * 2 + '$nX = 1', T + 'done', 'catch', T + 'using $oO = new K', T * 2 + '? $oO',
      T + 'done', 'done']),
]

RING_SURFACE = {'B03'}
os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for kind, rows in (('run', CASES), ('fmt', FMT)):
    for row in rows:
        cid, line, why, prog, want = row[:5]
        # v0.47: B03's names have no letter, so it is read on the Ring surface (a .haro name always carries one)
        name = f'cases/{cid}.ring' if cid in RING_SURFACE else f'cases/{cid}.haro'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(prog) + '\n')
        case = {'id': cid, 'kind': kind, 'line': line, 'why': why, 'file': name, 'stdout': '\n'.join(want) + '\n'}
        if len(row) > 5:
            # an uncaught report: its last line ends without a newline, and the exit is the one named
            case['stdout'] = '\n'.join(want)
            case['exit'] = row[5]
        out.append(case)
doc = {'rung': 'v0.38', 'decision': 'D52 rung (3): A2 within and A3 using, rewritten onto finally',
       'lines': {'W1': 'inside within the global holds the value, in the body and its callees; after it, what it held before',
                 'W2': 'the global is restored on every exit, and a write by the body or a callee is undone',
                 'W3': 'saved first, then the value computed (it may read the global); a raising value changes nothing; no value yet is R24',
                 'W4': 'within names a global: a local or a parameter is refused at compile time',
                 'U1': 'the first of Release, Destroy, Close the value answers to is called at the end, once, in any case, inherited',
                 'U2': 'it is called on every exit; a raise in it replaces a held raise, which becomes its cause',
                 'U3': 'none of the three: refused at compile time for new K of a known class, else raised at entry (or at exit if rebound by a callee)',
                 'U4': 'the using name cannot be rebound inside its block',
                 'B1': 'the blocks nest with try in every shape, and every line keeps its number',
                 'B2': 'only the statement form is a block; no done, no = value, or a catch of its own is refused',
                 'B3': 'haro fmt prints both blocks'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
