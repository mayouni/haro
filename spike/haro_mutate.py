"""haro_mutate.py -- defects of known kinds, put into a language declaration that is sound.

The judge of the collecting meta-court (stage 18). The meta-court's own first-refusal path is
the oracle for what ONE defect looks like: a mutation is applied to a sound .haro file, the
court is run in its default mode, and the single refusal it gives is that defect's finding.
Then several mutations on different declarations are applied together, and the court that
collects must give exactly the union of the singles -- nothing more (no cascade), nothing less
(no defect hidden behind another). The law is metamorphic: it needs no expected text written
by anyone, only the court's own verdicts on one defect at a time.

Five operators, each preserving the line count so a finding keeps its line:

  clause    an unknown clause put in the declaration            (a parse refusal)
  rationale the RATIONALE taken off the declaration             (a parse refusal)
  dup       the declaration renamed to an earlier one's name    (a registration refusal)
  dangle    one seat's type renamed to a name nothing declares  (a resolution refusal)
  on        a CONSTRAINT made to apply ON a kind nothing declares (a RELATIONAL refusal)

Where a defect is found sets what it is judged against. The first three are found while the
declarations are READ and REGISTERED, the fourth while their types are RESOLVED, the fifth only
when the RELATIONS among declarations are judged -- and those are judged once every declaration
reads and every type resolves (the barrier, STAGE below). So the union law is stated by stage:
when any mutation of stage 1 or 2 is present, only those are reported; the relational ones wait.
"""
STAGE = {'clause': 1, 'rationale': 1, 'dup': 1, 'dangle': 2, 'on': 3}
import re

DEF_START = re.compile(r'^DEFINE\s+(\w+)\s+(\w+)\s+AS\b')
# kinds that carry no name of their own into the namespace, or that the rest of a file reads
# without naming: left alone, so a defect there is not judged by the union law
FIXED_KINDS = ('LANGUAGE', 'WORLD', 'REFINE')
# kinds a "dup" may point at: the ones that register a name
NAMED_KINDS = ('DECLARATION', 'FORM', 'MENU', 'RANGE', 'FORMAT', 'UNION', 'CONSTRAINT', 'REFUSAL', 'EXPRESSION',
               'SENTENCE', 'VIEW', 'WALK', 'ASK', 'RUN', 'SYMBOL', 'FORMS', 'NARRATE')
PRIMS = ('name', 'text', 'number', 'flag', 'ref', 'ident', 'string')


def split_statements(text):
    """[(kind, name, core, tail)] and a head: lines before the first DEFINE are the head; each
    statement is its DEFINE and the lines up to the next one, with trailing comment and blank
    lines kept apart as the tail, so a mutation never touches a comment."""
    lines = text.split('\n')
    head = []
    stmts = []
    cur = None
    for ln in lines:
        m = DEF_START.match(ln)
        if m:
            if cur is not None:
                stmts.append(cur)
            cur = {'kind': m.group(1), 'name': m.group(2), 'lines': [ln]}
        elif cur is None:
            head.append(ln)
        else:
            cur['lines'].append(ln)
    if cur is not None:
        stmts.append(cur)
    out = []
    for s in stmts:
        ls = s['lines']
        k = len(ls)
        while k > 1 and (ls[k - 1].strip() == '' or ls[k - 1].strip().startswith('--')):
            k -= 1
        out.append({'kind': s['kind'], 'name': s['name'], 'core': ls[:k], 'tail': ls[k:]})
    return head, out


def join_statements(head, stmts):
    lines = list(head)
    for s in stmts:
        lines += s['core'] + s['tail']
    return '\n'.join(lines)


def _no_inline_comment(core):
    """True when no line of the statement carries a -- comment outside a string."""
    for ln in core:
        inq = False
        for i, c in enumerate(ln):
            if c == '"':
                inq = not inq
            elif c == '-' and not inq and ln[i:i + 2] == '--':
                return False
    return True


def _references(text, name):
    return len(re.findall(r'\b' + re.escape(name) + r'\b', text))


def eligible(head, stmts, text):
    """The mutations this file can take: a list of dicts {op, at, ...}, in file order."""
    out = []
    for i, s in enumerate(stmts):
        if s['kind'] in FIXED_KINDS or not _no_inline_comment(s['core']):
            continue
        core = '\n'.join(s['core'])
        k = core.rfind('RATIONALE')
        if k < 0:
            continue
        # clause: a `)` before the RATIONALE closes the clause list
        close = core.rfind(')', 0, k)
        if close > 0:
            out.append({'op': 'clause', 'at': i})
        # rationale: a single-line string, taken off
        rm = re.search(r'RATIONALE\s+"[^"\n]*"\s*$', core)
        if rm:
            out.append({'op': 'rationale', 'at': i})
        # dangle: a seat typed by a declared name
        if s['kind'] in ('DECLARATION', 'FORM'):
            sm = re.search(r'SEATS\s*\[([^\]]*)\]', core)
            if sm:
                for pm in re.finditer(r'(\w+)\s*:\s*\[?\s*(\w+)\s*\]?\s*\??', sm.group(1)):
                    typ = pm.group(2)
                    if typ not in PRIMS and any(t['name'] == typ for t in stmts):
                        out.append({'op': 'dangle', 'at': i, 'seat': pm.group(1), 'type': typ})
                        break
        # on: a constraint whose ON names a declaration kind; made to name one nothing declares
        if s['kind'] == 'CONSTRAINT' and re.search(r'\bON\s+\w+', core):
            out.append({'op': 'on', 'at': i})
        # dup: nothing else in the file names this declaration, so renaming it loses no reference
        if s['kind'] in NAMED_KINDS and i > 1 and _references(text, s['name']) == 1:
            out.append({'op': 'dup', 'at': i})
    return out


def _first_named_before(stmts, i, avoid):
    for j in range(1, i):
        if stmts[j]['kind'] in NAMED_KINDS and j not in avoid:
            return j
    return None


def apply(text, muts):
    """The file with every mutation of `muts` applied, or None when two of them clash (the
    same declaration twice, or a dup pointing at a declaration that is itself mutated)."""
    head, stmts = split_statements(text)
    ats = [m['at'] for m in muts]
    if len(set(ats)) != len(ats):
        return None
    targets = set()
    for m in muts:
        if m['op'] == 'dup':
            j = _first_named_before(stmts, m['at'], set())
            if j is None or j in ats:
                return None
            targets.add(j)
    n_before = text.count('\n')
    for n, m in enumerate(muts):
        s = stmts[m['at']]
        core = '\n'.join(s['core'])
        k = core.rfind('RATIONALE')
        if m['op'] == 'clause':
            close = core.rfind(')', 0, k)
            core = core[:close] + ', BOGUS 1' + core[close:]
        elif m['op'] == 'rationale':
            core = re.sub(r'\s*RATIONALE\s+"[^"\n]*"\s*$', '', core)
        elif m['op'] == 'dangle':
            core = re.sub(r'(' + re.escape(m['seat']) + r'\s*:\s*\[?\s*)' + re.escape(m['type']) + r'\b',
                          r'\g<1>zz_nowhere_' + str(m['at']), core, count=1)
        elif m['op'] == 'on':
            core = re.sub(r'\bON\s+\w+', 'ON zz_nokind_' + str(m['at']), core, count=1)
        elif m['op'] == 'dup':
            j = _first_named_before(stmts, m['at'], set())
            core = re.sub(r'^(DEFINE\s+\w+\s+)' + re.escape(s['name']) + r'\b', r'\g<1>' + stmts[j]['name'], core, count=1)
        s['core'] = core.split('\n')
    out = join_statements(head, stmts)
    if out.count('\n') != n_before:
        return None
    return out
