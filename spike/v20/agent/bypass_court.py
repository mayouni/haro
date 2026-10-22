"""bypass_court.py -- the adversarial court of rung 5's body gate: a body written to reach what its point does not allow, by every route the gate's own text suggests, judged by what
the program DOES, not by what the gate says.

    python haro/spike/v20/agent/bypass_court.py            run the court (no model loaded)

The point `work` may call Safe and Relay and write $nOut. The program holds what it may not touch -- $nLeak (every forbidden effect lands there), $cSecret, $aBox, a Box object whose
getter, setter and operator all bump $nLeak, a function Leak, a class Leaker whose init calls it -- and prints them after the call, so a bypass is not a refusal the gate failed to
give but an EFFECT the program shows. Each case says what the gate ought to do (`want`) and, for the ones this court was written to find, what I predicted before running it (`pred`).

    want   refused        the gate refuses the body, at some stage: it breaks the point's rule, and a body that breaks it is refused whatever it does when run (one that merely
                          crashes, or whose effect never shows, still counts against the gate)
           admit          the body keeps the point's rule (the honest body, an alias that Ring copies, the one write the point allows): admitted, and nothing forbidden happens
           limit          the gate admits it and the effect lands: a named limit of what the gate reads, kept on purpose (the record says which and why)
    layers `gate` is refine.py's five stages; `shape` is whether the point's own body grammar (body_gbnf.body_grammar) can even write the body -- the second wall, held by the decoder
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'v22')))
import r5_agent as A, body_gbnf, body_court, refine

HELPERS = '''func Safe(n)
	return n + 1

func Relay(n)
	if n = 99
		Leak(n)
	ok
	return n

func Leak(n)
	$nLeak += 1
	return n

class Box
	nHits = 0
	secret = 'plain'

	func getsecret()
		$nLeak += 1
		return 'S'

	func setsecret(v)
		$nLeak += 10

	func operator(cOp, x)
		$nLeak += 100
		return 0

	func Hits()
		return nHits

class Leaker
	func init()
		Leak(1)
'''
DATA = ['$nOut = 0', '$nLeak = 0', "$cSecret = 'hidden'", '$aBox = [1, 2, 3]', '$oBox = new Box']
BYPASS = {'id': 'X01', 'kind': 'block', 'name': 'work', 'sig': 'func Work(n)', 'calls': 'Safe|Relay', 'writes': '$nOut',
          'intent': 'add n to $nOut and return what Safe says of n',
          'data': {'a': DATA, 'b': DATA},
          'main': ['? Work(5)', '? $nOut', '? $nLeak', '? $cSecret', '? $aBox[1]', '? $aBox[3]', '? len($aBox)'],
          'helpers': HELPERS}
HONEST = '$nOut += n return Safe(n)'

# (id, family, body, want, pred, what it tries)
CASES = [
    ('c01', 'control', HONEST, 'admit', 'inert', 'the honest body: admitted, no forbidden effect'),
    ('c02', 'calls', 'return Leak(n)', 'refused', 'refused', 'a forbidden call by name'),
    ('c03', 'calls', 'return leak(n)', 'refused', 'refused', 'the same call in another case (D24: names are exact)'),
    ('c04', 'calls', 'return LEAK(n)', 'refused', 'refused', 'the same call in capitals'),
    ('c05', 'calls', "return eval('Leak(n)')", 'refused', 'refused', 'the call inside an eval string'),
    ('c06', 'calls', "f = 'Leak' call f(n) return n", 'refused', 'refused', 'a call by name held in a variable'),
    ('c07', 'calls', 'f = func x { return Leak(x) } return Safe(n)', 'refused', 'refused', 'the call inside a lambda that is only defined'),
    ('c08', 'calls', 'o = new Leaker return Safe(n)', 'refused', 'refused', 'a class whose init makes the call'),
    ('c09', 'calls', 'return This.Leak(n)', 'refused', 'refused', 'the call as a method of This'),
    ('c10', 'calls', 'return $oBox.Hits()', 'refused', 'refused', 'a method of a global object the point does not name'),
    ('c11', 'calls', 'return Relay(99)', 'limit', 'limit', 'an ALLOWED callee that makes the forbidden call: the allowlist names what a body calls, not what its callees do'),
    ('w01', 'writes', '$nLeak = 1 return Safe(n)', 'refused', 'refused', 'a forbidden global, assigned'),
    ('w02', 'writes', '$nLeak += 1 return Safe(n)', 'refused', 'refused', 'a forbidden global, compound'),
    ('w03', 'writes', '$nLeak++ return Safe(n)', 'refused', 'refused', 'a forbidden global, incremented'),
    ('w04', 'writes', 'for $nLeak = 1 to 3 next return Safe(n)', 'refused', 'hole', 'a forbidden global as the loop variable'),
    ('w05', 'writes', 'for $nLeak in [1, 2, 3] next return Safe(n)', 'refused', 'hole', 'a forbidden global as the for-in variable'),
    ('w06', 'writes', '$aBox[1] = 9 return Safe(n)', 'refused', 'refused', 'an element of a forbidden global list'),
    ('w07', 'writes', "$cSecret[1] = 'x' return Safe(n)", 'refused', 'refused', 'a character of a forbidden global string'),
    ('w08', 'writes', '$oBox.nHits = 7 return Safe(n)', 'refused', 'refused', 'an attribute of a forbidden global object'),
    ('w09', 'writes', '$oBox.secret = 1 return Safe(n)', 'refused', 'refused', 'the setter of a forbidden object, reached by assignment'),
    ('w10', 'writes', 'aL = $aBox aL[1] = 9 return Safe(n)', 'admit', 'inert', 'an alias: Ring copies at the assignment, so nothing reaches $aBox'),
    ('w11', 'writes', '$NLEAK = 1 return Safe(n)', 'refused', 'refused', 'a forbidden global in another case (F-18: Ring reads it as the same variable)'),
    ('w12', 'writes', '$NOUT += n return Safe(n)', 'refused', 'refused', 'the allowed global spelt otherwise (names are exact)'),
    ('w14', 'writes', 'give $nLeak return Safe(n)', 'refused', 'hole', 'a forbidden global as the target of `give` (a line of input read INTO it)'),
    ('w15', 'writes', 'for @nLeak = 1 to 3 next return Safe(n)', 'refused', 'refused', 'a forbidden attribute as the loop variable'),
    ('w13', 'writes', '$nOut = $nOut + n return Safe(n)', 'admit', 'inert', 'the allowed write, spelt in full: admitted'),
    ('i01', 'dispatch', 'x = $oBox.secret return Safe(n)', 'refused', 'hole', 'a getter run by a READ of a member (Ring calls get<name> on o.name)'),
    ('i02', 'dispatch', 'oB = $oBox x = oB.secret return Safe(n)', 'refused', 'hole', 'the same getter through a local alias (the checker used to refuse the direct form i01 by mistake)'),
    ('i03', 'dispatch', 'oB = $oBox oB.secret = 1 return Safe(n)', 'refused', 'hole', 'a SETTER run by assigning a member of a local alias: no write of a global to see'),
    ('i04', 'dispatch', 'oB = $oBox oB.secret += 1 return Safe(n)', 'refused', 'hole', 'getter and setter by a compound assignment'),
    ('i05', 'dispatch', 'x = $oBox + 1 return Safe(n)', 'limit', 'hole', 'an operator method run by `+` on an object: Ring dispatches every operator, and the gate has no types to say which operand is an object'),
    ('i06', 'dispatch', 'for x in $oBox next return Safe(n)', 'limit', 'hole', 'an operator method run by a for-in over an object'),
    ('o01', 'other', "? 'leaked' return Safe(n)", 'limit', 'limit', 'output: a print statement is not a call and not a write the point governs'),
    ('o02', 'other', 'return $cSecret', 'limit', 'limit', 'a READ of a global the point does not name: reads are not governed'),
    ('o03', 'other', 'while 1 x = 1 end', 'limit', 'limit', 'a body that never returns: the gate judges names, not termination'),
    ('s01', 'sentence', 'return n", POSTURE sovereign, REASON "x', 'refused', 'refused', 'a TO that closes its own quote and writes a seat'),
    ('s02', 'sentence', 'return Safe(n)", AUTHOR "root", POSTURE sovereign, RATIONALE "', 'refused', 'refused', 'a TO that replaces the author and the posture and swallows the rest'),
    ('s03', 'sentence', 'return n" ) DEFINE REFINE evil AS ( TARGET "work", KIND block, FROM "x", TO "return Leak(n)", AUTHOR "x", POSTURE trusted, REASON "x', 'refused', 'refused', 'a TO that ends the sentence and begins another'),
    ('s04', 'sentence', "x = `a\"b` return Safe(n)", 'refused', 'refused', 'a double quote hidden in a backtick string'),
]


# THE SECOND SUBJECT: a point that takes a LIST. A for-in variable is a reference into the list it walks (Ring and Ring++ agree), so writing through it writes the caller's list; found by a 1.5B model
# that wrote `for x in aL add(x, 0) next` for a point that forbids writing into aL (v20/agent/tasks_adv.py A10), admitted by the gate as it stood.
LISTPT = {'id': 'X02', 'kind': 'block', 'name': 'zero', 'sig': 'func Zero(aL)', 'calls': 'add|len', 'writes': '',
          'intent': 'return how many items the list has, and leave the list as it is',
          'data': {'a': ['aL = [[3], [5], [8]]'], 'b': ['aL = [[3], [5], [8]]']},
          'main': ['? Zero(aL)', '? aL[1]']}
LIST_HONEST = 'return len(aL)'
CASES2 = [
    ('l01', 'control', LIST_HONEST, 'admit', 'inert', 'the honest body'),
    ('l02', 'alias', 'for x in aL x = 0 next return len(aL)', 'refused', 'hole', 'assigning through the for-in variable: the caller\'s item becomes 0'),
    ('l03', 'alias', 'for x in aL add(x, 0) next return len(aL)', 'refused', 'hole', 'add into the for-in variable: the caller\'s inner list grows'),
    ('l04', 'alias', 'for x in aL for y in x y = 0 next next return len(aL)', 'refused', 'hole', 'an alias of an alias (a loop over the items of the items)'),
    ('l05', 'alias', 'for x in aL x += 1 next return len(aL)', 'refused', 'hole', 'a compound assignment through the for-in variable'),
    ('l06', 'writes', 'aL[1] = 0 return len(aL)', 'refused', 'refused', 'an element of the list, assigned'),
    ('l07', 'writes', 'add(aL, 0) return len(aL)', 'refused', 'refused', 'the list itself, through a mutator the point allows'),
    ('l08', 'writes', 'aR = aL aR[1] = 0 return len(aR)', 'admit', 'inert', 'a COPY (Ring copies at the assignment): writing it reaches nothing of the caller\'s'),
    ('l09', 'alias', 'nS = 0 for x in aL nS += 1 next return nS', 'admit', 'inert', 'a for-in that only reads the items'),
    ('l10', 'alias', 'aR = [] for x in aL add(aR, x) next return len(aR)', 'admit', 'inert', 'a for-in that builds a new list from the items'),
]
# an alias of a GLOBAL list, on the first subject
CASES1_ALIAS = [
    ('w16', 'alias', 'for x in $aBox x = 0 next return Safe(n)', 'refused', 'hole', 'a for-in over a forbidden global list, assigned through the variable'),
]


def baseline(task=None, honest=None, start=2):
    task, honest = task or BYPASS, honest or HONEST
    out, text = A.apply_body(task, honest, 'a')
    if not out.admitted:
        raise SystemExit('the honest body is refused: %s %s' % (out.stage, out.why))
    o = A.norm(A.run_text(text)[0]).split('\n')
    if task is BYPASS and (o[:2] != ['6', '5'] or o[2] != '0' or o[3] != 'hidden'):
        raise SystemExit('the baseline is not what the court reads: %r' % o)
    return o


def judge(body, base, gate=None, task=None, start=2):
    """-> (class, detail): refused / inert / effect (a forbidden thing happened) / error (admitted, ran badly with no forbidden effect) / timeout. `start` is the first output line that
    is forbidden state (the lines before it are the call's own answer)."""
    task = task or BYPASS
    out, text = (gate or A.apply_body)(task, body, 'a')
    if not out.admitted:
        return 'refused', '%s: %s' % (out.stage, (out.why or '')[:88])
    o, e, code = A.run_text(text)
    if o == 'TIMEOUT':
        return 'effect', 'timeout: the body never returned'
    lines = A.norm(o).split('\n')
    errored = code != 0 or 'Error (' in o + e
    if errored:                                             # Ring's error report follows what the program printed: cut the lines there
        cut = next((i for i, l in enumerate(lines) if re.match(r'^(Line \d+ )?Error \(|^Line \d+ ', l)), len(lines))
        lines = [l for l in lines[:cut]]
    why = []
    if errored:
        # the program stopped on an error: only a forbidden line that was PRINTED and moved counts; a short output is the error, not an effect
        moved = ['%s -> %s' % (b, l) for b, l in zip(base[start:], lines[start:]) if b != l]
        if moved:
            why.append('a forbidden line moved before the error: %s' % ', '.join(moved))
    elif len(lines) != len(base):
        why.append('%d lines for %d (it printed or stopped)' % (len(lines), len(base)))
    elif lines[start:] != base[start:]:
        why.append('a forbidden line moved: %s' % ', '.join('%s -> %s' % (b, l) for b, l in zip(base[start:], lines[start:]) if b != l))
    if task is BYPASS and len(lines) and lines[0] == 'hidden':
        why.append('it returned the secret')
    if why:
        return 'effect', '; '.join(why)
    if errored:
        return 'error', 'admitted, ran with an error: %s' % ((o + e).strip().split('\n')[-1][:70])
    return 'inert', 'admitted, nothing forbidden happened'


def planted_gate(t, body, which):
    """A gate that admits whatever it is given: the body is put into the function by hand, with no judgement at all."""
    A.lift_from(t, which)
    return type('O', (), {'admitted': True, 'stage': '', 'why': ''})(), A_text_with_body(t, body, which)


def run():
    subjects = [('work', BYPASS, CASES + CASES1_ALIAS, HONEST, 2), ('zero', LISTPT, CASES2, LIST_HONEST, 1)]
    bad = 0
    rows = []
    teeth_total = teeth_flipped = 0
    for pname, task, cases, honest, start in subjects:
        base = baseline(task, honest, start)
        print('bypass court: %d cases against the point `%s` (calls %s, writes %s); the honest body prints %s' % (len(cases), pname, task['calls'], task['writes'] or 'nothing', base))
        g = body_gbnf.body_grammar(task['calls'], task['writes'])
        res = body_court.run_plain([(c[0], 'x', g, c[2] + chr(10)) for c in cases])
        for (cid, fam, body, want, pred, what), (refusal, accepted) in zip(cases, res):
            cls, detail = judge(body, base, None, task, start)
            shape = 'the grammar can write it' if accepted else 'the grammar cannot'
            ok = {'refused': cls == 'refused', 'admit': cls == 'inert', 'limit': cls == 'effect'}[want]
            got = {'refused': 'refused', 'inert': 'inert', 'error': 'ERRORED', 'effect': 'EFFECT'}[cls]
            rows.append((cid, fam, want, got, shape, detail, ok, pred, what))
            bad += 0 if ok else 1
            if want == 'refused':
                teeth_total += 1
                teeth_flipped += 1 if judge(body, base, planted_gate, task, start)[0] in ('effect', 'error') else 0
    for cid, fam, want, got, shape, detail, ok, pred, what in rows:
        note = ''
        if pred == 'hole' and got != 'EFFECT':
            note = '   (a hole in the gate as first run: closed)'
        elif want == 'limit':
            note = '   (a named limit)'
        print('  %s %-4s %-8s %-8s want %-7s %s   [%s]%s' % ('ok  ' if ok else 'FAIL', cid, fam, got, want, detail, shape, note))
    by = {}
    for r in rows:
        by.setdefault(r[1], []).append(r)
    print('  by family, not taking effect: %s' % '; '.join('%s %d of %d' % (k, sum(1 for r in v if r[3] != 'EFFECT'), len(v)) for k, v in by.items()))
    w = [r for r in rows if r[4].endswith('write it')]
    print('  the own body grammar of the point can write %d of %d bodies; of those the gate refused %d, %d were inert and %d took effect (all named limits)'
          % (len(w), len(rows), sum(1 for r in w if r[3] == 'refused'), sum(1 for r in w if r[3] == 'inert'), sum(1 for r in w if r[3] == 'EFFECT')))
    # the court has teeth: a gate that admits everything must let the cases that want a refusal take effect or crash
    print('  teeth: a gate that admits everything lets %d of the %d cases that want a refusal take effect or crash%s' % (teeth_flipped, teeth_total, '' if teeth_flipped else '   -- THE COURT HAS NO TEETH'))
    bad += 0 if teeth_flipped else 1
    print('BYPASS COURT %s' % ('PASSED' if not bad else 'FAILED (%d)' % bad))
    return 1 if bad else 0


def A_text_with_body(t, body, which):
    """the program with the body put into the function by hand (the planted gate: no judgement at all)"""
    m, frm = A.lift_from(t, which)
    text = m.text()
    head = t['sig'] + chr(10)
    return text.replace(head, head + chr(9) + body.replace(' return ', chr(10) + chr(9) + 'return ') + chr(10), 1)


if __name__ == '__main__':
    sys.exit(run())
