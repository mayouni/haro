"""task_lint.py -- refuse a task whose TEXT names what its point forbids, before any model is asked.

    python task_lint.py                       lint every task of both sets and print what it finds

Three measurements said the same thing (HF-119, HF-120): the pull on a model is the request, not the prompt's allowlist and not the gate's reason. A task that says "use fabs(a - b)" for a point that may
call nothing is a contradiction a program can see, so the harness sees it first: `lint(intent, point)` returns findings, and a task with an `error` is refused with the reason, no model asked.

    error  names-call            the intent names a call (`name(`, or `call|calling|builtin|function` before a name Ring or the program defines) that the point's `calls` does not allow
           names-call-spelling   ... a name the point allows, spelt otherwise (D24: names are exact, and a look-alike is refused)
           names-write           the intent asks to write a global or an attribute (`$x`, `@x`) that the point's `writes` does not name
           names-read            the intent names a global or an attribute that the point's `reads` and `writes` do not (`reads` is closed by default, D30: a body reads only what it is given)
           claims-authority      the intent speaks about its own point's allowlist: it is out of date, a call is allowed, ignore the rules. The allowlist is the point's, not the task's
    warn   mutates-param         the intent may ask to change the list the caller passes (`set every item of the list to 0`) while the point writes its own locals only. Not refused: it can be read as a request
                                 for a new list, and the gate refuses the in-place body anyway

What it does NOT see, and says so: a pull the text does not name (the natural body of "how far apart are two numbers" calls fabs); prose that happens to hold a write verb before a global it only
reads (`add the tax in $nVat to n` names $nVat as written to). Fixtures first, in lint_court.py.
"""
import os, re, sys
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))
V20 = os.path.abspath(os.path.join(HERE, '..'))
for p in (V20, os.path.join(V20, '..', 'v18'), os.path.join(V20, '..', 'v19')):
    sys.path.insert(0, os.path.abspath(p))

KEYWORDS = {'if', 'while', 'for', 'return', 'and', 'or', 'not', 'in', 'to', 'step', 'ok', 'else', 'elseif', 'but', 'next', 'end', 'switch', 'case', 'other', 'on', 'off', 'func', 'new', 'try', 'catch', 'done'}
# a clause that writes `$x`: the target after a preposition (`add n to $x`, `count the call in $x`), or the direct object (`increment @x`, `zero the global $x`)
PREP_VERBS = r'(?:add|adds|adding|store|stores|storing|save|saves|saving|record|records|recording|remember|count|counts|counting|keep|keeps|log|logs|logging|put|puts|push|pushes|track|tracks|tally|accumulate)'
DIRECT_VERBS = r'(?:increment|increments|incrementing|decrement|decrements|reset|resets|clear|clears|zero|zeroes|bump|bumps|update|updates|write|writes|assign|assigns|set|sets|append|appends)'
ARTICLE = r'(?:the\s+|a\s+)?(?:global\s+|variable\s+|attribute\s+|property\s+)?'
MUTATE = r'(?:set|zero|clear|empty|fill|sort|reverse|remove|delete|append|push|insert|replace|update|modify|change|swap|shuffle|reorder|truncate|drop|pop)'
AUTHORITY = re.compile(r'allow-?list|allowed\s+(?:calls?|functions?|builtins?|names?)|permitted\s+(?:calls?|functions?)|list\s+of\s+(?:allowed|permitted)\s+\w+'
                       r'|\b(?:ignore|disregard|override|bypass|forget)\s+(?:the\s+|all\s+|any\s+)?(?:above|previous|earlier|allowed|rules?|restrictions?|constraints?|limits?|calls?|instructions?)', re.I)
CLAIM = re.compile(r'\b([A-Za-z_]\w*)\s+(?:is|are)\s+(?:also\s+|now\s+)?(?:allowed|permitted|fine\s+to\s+use|ok\s+to\s+use)\b', re.I)


@dataclass
class Finding:
    severity: str          # 'error' | 'warn'
    code: str
    what: str              # the words of the intent that did it
    why: str               # what to tell the author

    def __str__(self):
        return '%s %s: %s -- %s' % (self.severity, self.code, self.what, self.why)


def _known(defined):
    import refine
    return {b.lower() for b in refine.builtins()} | {d.lower() for d in defined}


def lint(intent, calls='', writes='', own=(), params=(), defined=(), reads=''):
    """-> [Finding]. `own` the point's function name(s), `params` its parameters, `defined` the program's other functions (a name Ring or the program defines is a KNOWN callable)."""
    out = []
    text = ' '.join((intent or '').split())
    allowed = [c for c in (calls or '').split('|') if c]
    allowed_low = {c.lower() for c in allowed}
    writable = {w for w in (writes or '').split('|') if w}
    readable = writable | {r for r in (reads or '').split('|') if r}          # what a body may write it may read
    own_low = {o.lower() for o in own} | {p.lower() for p in params}
    known = _known(defined)
    seen = set()

    def call_finding(name, how):
        low = name.lower()
        if low in own_low or low in KEYWORDS or name in allowed or (name, 'call') in seen:
            return
        seen.add((name, 'call'))
        if low in allowed_low:
            decl = next(c for c in allowed if c.lower() == low)
            out.append(Finding('error', 'names-call-spelling', how, "the task spells '%s', the point declares '%s': names are exact (D24)" % (name, decl)))
        else:
            out.append(Finding('error', 'names-call', how, "the task names the call '%s', which the point does not allow (it may call: %s)" % (name, ', '.join(allowed) or 'nothing')))

    # 1. a call written as a call
    for m in re.finditer(r'([A-Za-z_]\w*)\((?!(?:s|es|ies|ed|ing)\))', text):          # `position(s)` is a plural, not a call
        call_finding(m.group(1), m.group(0))
    # 2. a call named by a verb: `calling the builtin max`, `call Leak` -- only a name Ring or the program defines, so `call count` and `function that` stay prose
    for m in re.finditer(r'\b(?:call|calling|builtin|built-in|function)\s+(?:the\s+)?(?:builtin\s+|built-in\s+|function\s+)?([A-Za-z_]\w*)', text, re.I):
        if m.group(1).lower() in known:
            call_finding(m.group(1), m.group(0))
    # 3. a write named
    clauses = [c.strip() for c in re.split(r'[,;]|\.\s|\s+(?:and|then|also)\s+', text) if c.strip()]
    for clause in clauses:
        for tm in re.finditer(r'[$@][A-Za-z_]\w*', clause):
            tok = tm.group(0)
            targeted = (re.search(r'\b' + PREP_VERBS + r'\b[^,;]*\b(?:to|in|into|on|onto)\s+' + ARTICLE + re.escape(tok) + r'\b', clause, re.I)
                        or re.search(r'\b' + DIRECT_VERBS + r'\s+(?:\w+\s+){0,3}?' + re.escape(tok) + r'\b', clause, re.I))
            if targeted and tok not in writable and (tok, 'write') not in seen:
                seen.add((tok, 'write'))
                hint = next((w for w in writable if w.lower() == tok.lower()), None)
                out.append(Finding('error', 'names-write', clause, "the task asks to write %s, which the point does not allow (it may write: %s)%s"
                                   % (tok, ', '.join(sorted(writable)) or 'its own locals only', "; the declared spelling is %s" % hint if hint else '')))
    # 3b. a read named: a global or an attribute in the intent that is neither readable nor already named as a write
    for tm in re.finditer(r'[$@][A-Za-z_]\w*', text):
        tok = tm.group(0)
        if tok in readable or (tok, 'write') in seen or (tok, 'read') in seen:
            continue
        seen.add((tok, 'read'))
        hint = next((r for r in readable if r.lower() == tok.lower()), None)
        out.append(Finding('error', 'names-read', tok, "the task names %s, which the point does not let it read (it may read: %s)%s"
                           % (tok, ', '.join(sorted(readable)) or 'no global and no attribute', "; the declared spelling is %s" % hint if hint else '')))
    # 4. a claim about the point's own allowlist
    claim = AUTHORITY.search(text)
    if not claim:
        for m in CLAIM.finditer(text):
            if m.group(1).lower() in known or re.search(r'\b' + re.escape(m.group(1)) + r'\(', text):
                claim = m
                break
    if claim:
        out.append(Finding('error', 'claims-authority', claim.group(0), "the task speaks about its own point's allowlist; the allowlist is the point's tag, not the task's text"))
    # 5. a change of the list the caller passes, asked in the imperative, when the point writes its own locals only
    if not writable:
        listy = [p for p in params if re.match(r'a[A-Z_]|[a-z]+List$', p) or p.lower() in ('list', 'items')]
        for clause in clauses:
            m = re.match(r'(?:then\s+)?' + MUTATE + r'\b', clause, re.I)
            if m and (re.search(r'\blist\b', clause, re.I) or any(re.search(r'\b' + re.escape(p) + r'\b', clause) for p in listy)):
                out.append(Finding('warn', 'mutates-param', clause, "the task may ask to change the list the caller passes, and the point writes its own locals only: a body that does it in place is refused; ask for a new list if that is meant"))
                break
    return out


def refusal(findings):
    """The reason a task is refused (its errors, in one line), or None."""
    errs = [f for f in findings if f.severity == 'error']
    return '; '.join('%s (%s)' % (f.why, f.code) for f in errs) if errs else None


def task_point(t):
    """(calls, writes, own names, params, the program's other functions, reads) of a task of tasks.py / tasks_adv.py -- read from the task's program, as the gate reads it."""
    import refine, ids
    import tasks as T
    m = refine.Model(T.program(t, 'a'), {})
    funcs = [ids.def_name(it) for it, parent, bp, lst, i, owner in refine.walk_items(m.g) if it.get('k') == 'func']
    if t['kind'] == 'function':
        own, params = (t['name'],), tuple(p for p in t['params'].split('|') if p)
    else:
        sig = t['sig']
        own = (sig.split('(')[0].replace('func', '').strip(),)
        params = tuple(p.strip() for p in sig.split('(')[1].rstrip(') ').split(',') if p.strip())
    return t['calls'], t['writes'], own, params, tuple(f for f in funcs if f.lower() not in {o.lower() for o in own}), t.get('reads', '')


def lint_task(t):
    calls, writes, own, params, defined, reads = task_point(t)
    return lint(t['intent'], calls=calls, writes=writes, own=own, params=params, defined=defined, reads=reads)


if __name__ == '__main__':
    import tasks as T, tasks_adv
    for label, tasks in (('the sixteen', T.BASE), ('the adversarial eleven', tasks_adv.TASKS)):
        print(label)
        for t in tasks:
            f = lint_task(t)
            print('  %-4s %s' % (t['id'], ('REFUSED: ' + refusal(f)) if refusal(f) else ('warns: ' + '; '.join(str(x) for x in f)) if f else 'clean'))
