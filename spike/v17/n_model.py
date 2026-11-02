"""A reference MODEL of N's dynamic half, read from a sentence of N (n_v17.haro) -- a specification by
executable sketch, NOT the court. It exists so the drawing in GRAMMAR.md is precise and checkable now:

  rules(sentence)      the checks the forged court cannot yet make with the existing meta-vocabulary
                       (the v0.17 rung would add them): placeholders, coverage, the gate, a surface judging a query
  understand(...)      a question in a tongue -> the frame, the surface, the closed query, the slots; or a refusal
  ask(...)             a question answered on the graph surface, told in the tongue (the ledger is the Z court's)
  tokens(...)          the semantic form of a question: the auditable intermediate

It shares no code with the study's pipeline (nlq.ring, stzNatural): n_check.py judges it against the study's
74 questions. A second implementation of the same behaviour, from the sentence alone, is the evidence that the
drawing is complete and does not lean on any one engine.
"""
import os, re, subprocess

def fold(s):
    """Case folding, as the court does it: ASCII, and the Latin-1 letters U+00C0 to U+00DE (not U+00D7); no other
    script. A tongue whose script has case needs the court to learn it, in the open."""
    return ''.join(chr(ord(c) + 32) if 'A' <= c <= 'Z' or ('\u00c0' <= c <= '\u00de' and c != '\u00d7') else c for c in s)


def upper_first(s):
    return (chr(ord(s[0]) - 32) if s and 'a' <= s[0] <= 'z' else s[:1]) + s[1:]


def words(s):
    """Split on a space, a tab, a line feed or a carriage return -- the court splits on bytes, never on a Unicode space."""
    return [w for w in re.split(r'[ \t\r\n]+', s) if w]


SAFE_PUNCTUATION = "-'?,."          # the court's safe set: a tongue may allow a subset, never more
SEPARATORS = "'?,."                 # of these, all but the hyphen separate words
REFUSAL_KINDS = ('character', 'word', 'shape', 'ambiguous', 'surface')
MAX_DIGITS = 12


# ---- the sentence: a small parser (DEFINE KIND name AS ( CLAUSE value, ... ) RATIONALE "...") --------------------

class Decl:
    def __init__(self, kind, name, line):
        self.kind, self.name, self.line = kind, name, line
        self.clauses = {}
        self.rationale = None

    def get(self, key, default=None):
        return self.clauses.get(key, default)

    def pairs(self, key):
        """A pair list as an ordered list of (key, value)."""
        v = self.clauses.get(key)
        return [(i[1], i[2]) for i in v if isinstance(i, tuple)] if isinstance(v, list) else []

    def names(self, key):
        v = self.clauses.get(key)
        return [i for i in v if isinstance(i, str)] if isinstance(v, list) else []


_TOKEN = re.compile(r'\s*(?:(--[^\n]*)|("[^"]*")|([A-Za-z_][A-Za-z0-9_]*)|(-?\d+)|([()\[\],:]))')


def parse(text):
    toks, pos = [], 0
    while True:
        m = _TOKEN.match(text, pos)
        if not m:
            rest = text[pos:].strip()
            if rest:
                raise ValueError(f'line {text.count(chr(10), 0, pos) + 1}: cannot read {rest[:30]!r}')
            break
        ln = text.count('\n', 0, m.end(0) - len(m.group(0).lstrip())) + 1
        if m.group(1) is None:
            kind = 'str' if m.group(2) else 'id' if m.group(3) else 'num' if m.group(4) else 'p'
            val = m.group(2)[1:-1] if m.group(2) else (m.group(3) or m.group(4) or m.group(5))
            toks.append((kind, val, ln))
        pos = m.end()
    out, i = [], 0

    def expect(k, v=None):
        nonlocal i
        t = toks[i]
        if t[0] != k or (v is not None and t[1] != v):
            raise ValueError(f'line {t[2]}: expected {v or k}, found {t[1]!r}')
        i += 1
        return t

    def value():
        nonlocal i
        t = toks[i]
        if t[0] in ('str', 'id', 'num'):
            i += 1
            return t[1]
        expect('p', '[')
        items = []
        while not (toks[i][0] == 'p' and toks[i][1] == ']'):
            a = toks[i]
            if toks[i + 1][0] == 'p' and toks[i + 1][1] == ':':
                i += 2
                items.append(('pair', a[1], toks[i][1]))
                i += 1
            else:
                items.append(a[1])
                i += 1
            if toks[i][0] == 'p' and toks[i][1] == ',':
                i += 1
        expect('p', ']')
        return items

    while i < len(toks):
        expect('id', 'DEFINE')
        kind = expect('id')
        name = expect('id')
        d = Decl(kind[1], name[1], kind[2])
        expect('id', 'AS')
        expect('p', '(')
        while not (toks[i][0] == 'p' and toks[i][1] == ')'):
            key = expect('id')[1]
            d.clauses[key] = value() if not (toks[i][0] == 'p' and toks[i][1] in (',', ')')) else True
            if toks[i][0] == 'p' and toks[i][1] == ',':
                i += 1
        expect('p', ')')
        expect('id', 'RATIONALE')
        d.rationale = expect('str')[1]
        out.append(d)
    return out


# ---- the world: a surface's versioned artifact (.zknw: facts `s | p | o`, an ontology section) ----------------

def read_world(path):
    if not os.path.exists(path):
        return None                      # a world that is not there: the rules' N_WORLD_UNREAD
    triples, laws, section = [], [], None
    for raw in open(path, encoding='utf-8').read().splitlines():
        t = raw.strip()
        if t in ('facts', 'ontology'):
            section = t
        elif section == 'facts' and t.count('|') == 2:
            triples.append(tuple(x.strip() for x in t.split('|')))
        elif section == 'ontology' and t.count('|') == 1:
            laws.append(tuple(x.strip() for x in t.split('|')))
    return triples, laws


# ---- the sentence as a world to ask ----------------------------------------------------------------------------

class N:
    def __init__(self, text, base_dir, surface_check=None):
        self.decls = parse(text)
        self.by = {}
        for d in self.decls:
            self.by.setdefault(d.kind, {})[d.name] = d
        self.base = base_dir
        self.surface_check = surface_check or default_surface_check
        self._triples = {}
        self.tongues = list(self.by.get('TONGUE', {}))
        # the one meaning that captures digits: a question's own number is the only text of it a query may hold
        self.num = next((m.name for m in self.decls if m.kind == 'MEANING' and m.get('SLOT') == 'number'), None)

    def kinds(self, k):
        return list(self.by.get(k, {}).values())

    def world(self, surface):
        s = self.by['SURFACE'][surface]
        w = s.get('WORLD')
        if not w:
            return [], []
        if w not in self._triples:
            self._triples[w] = read_world(os.path.join(self.base, w))
        return self._triples[w] or ([], [])

    def world_read(self, surface):
        s = self.by['SURFACE'][surface]
        w = s.get('WORLD')
        self.world(surface)
        return not w or self._triples[w] is not None

    def entities(self, meaning):
        """The ids a surface enumerates for the entity kind a meaning is OF."""
        m = self.by['MEANING'][meaning]
        if m.get('SLOT') != 'entity' or m.get('FROM') not in self.by.get('SURFACE', {}) or not m.get('OF'):
            return []
        triples, _ = self.world(m.get('FROM'))
        return [s for s, p, o in triples if p == 'is-a' and o == m.get('OF')]

    # -- the lexicon of a tongue: words -> (meaning, entity id or None) -------------------------------------------
    def lexicon(self, tongue):
        t = self.by['TONGUE'][tongue]
        ignored = set(fold(w) for w in words(t.get('IGNORES', '')))
        lex, clashes = {}, []

        def add(word, meaning, ent=None):
            w = fold(word)
            if w in lex and lex[w] != (meaning, ent):
                clashes.append((w, lex[w][0], meaning))
            lex[w] = (meaning, ent)
        for m in self.kinds('MEANING'):
            for tg, txt in m.pairs('WORDS'):
                if tg == tongue:
                    for w in words(txt):
                        add(w, m.name)
            if m.get('SLOT') == 'entity':
                for ent in self.entities(m.name):
                    add(ent, m.name, ent)
        for a in self.kinds('ALIAS'):
            for tg, txt in a.pairs('WORDS'):
                if tg == tongue:
                    for w in words(txt):
                        add(w, a.get('MEANING'), a.get('ENTITY'))
        return ignored, lex, clashes

    def canonical(self, tongue, ent):
        """The word an answer is told in: an alias's first word, else the tongue's own spelling of a name."""
        for a in self.kinds('ALIAS'):
            if a.get('ENTITY') == ent:
                for tg, txt in a.pairs('WORDS'):
                    if tg == tongue and words(txt):
                        return words(txt)[0]
        return spell(ent, self.by['TONGUE'][tongue].get('NAMES', 'as_is'))

    # -- the gate and the tokens -----------------------------------------------------------------------------------------
    def gate(self, tongue, text):
        allows = self.by['TONGUE'][tongue].get('ALLOWS', '')
        for ch in text:
            o = ord(ch)
            if o >= 128 or ch == ' ' or ch.isascii() and ch.isalnum() or ch in allows:
                continue
            return f'(control character {o})' if o < 32 or o == 127 else ch
        return None

    def tokens(self, tongue, text):
        """The semantic form: [('show', None, 'show'), ('num', '5000', '5000'), ...] or a refusal."""
        bad = self.gate(tongue, text)
        if bad is not None:
            return None, ('character', bad)
        ignored, lex, _ = self.lexicon(tongue)
        norm = text
        for sep in SEPARATORS:
            norm = norm.replace(sep, ' ')
        out = []
        self._skipped = []
        for raw in words(norm):
            w = fold(raw)
            if w in ignored:
                self._skipped.append(raw)
                continue
            if w in lex:
                meaning, ent = lex[w]
                out.append((meaning, ent, raw))
            elif self.num and w.isascii() and w.isdigit() and len(w) <= MAX_DIGITS:
                out.append((self.num, w, raw))
            else:
                return None, ('word', raw)
        return out, None

    def tokens_full(self, tongue, text):
        """What the court's `tokens` answers: the tokens with their slots and the words that were ignored."""
        toks, ref = self.tokens(tongue, text)
        if ref:
            return {'refused': ref[0], 'what': ref[1]}
        return {'tongue': tongue, 'tokens': [dict({'meaning': m, 'word': raw}, **({'slot': ent} if ent else {})) for m, ent, raw in toks],
                'ignored': list(self._skipped)}

    def vocabulary(self, tongue):
        """What the court's `vocabulary` answers: the lexicon in order, what the tongue does not cover, the clashes."""
        ignored, wds, clashes = self.lexicon(tongue)
        ign = [fold(w) for w in words(self.by['TONGUE'][tongue].get('IGNORES', ''))]
        return {'tongue': tongue, 'ignored': ign,
                'words': [dict({'word': w, 'meaning': m}, **({'entity': e} if e else {})) for w, (m, e) in wds.items()],
                'uncovered': [m.name for m in self.kinds('MEANING') if m.get('SLOT') == 'none' and tongue not in {t for t, _ in m.pairs('WORDS')}],
                'clashes': [{'word': w, 'meanings': [a, b]} for w, a, b in clashes]}

    def examples_report(self):
        """What the court's `examples` answers: the sentence's own conformance, counted."""
        r = {'declared': 0, 'texts': 0, 'understood': 0, 'failed': 0, 'diverging': 0}
        for ex in self.kinds('EXAMPLE'):
            r['declared'] += 1
            seen = set()
            for tg, txt in ex.pairs('ASKING'):
                if tg not in self.by['TONGUE']:
                    continue
                r['texts'] += 1
                u = self.understand(tg, txt)
                if u.get('frame') == ex.get('MEANS'):
                    r['understood'] += 1
                    seen.add(u['surface'] + ' ' + u.get('query', '') + ''.join(' => ' + st[0] + ' ' + st[1] for st in u.get('steps', [])))
                else:
                    r['failed'] += 1
            r['diverging'] += len(seen) > 1
        c = {'declared': 0, 'texts': 0, 'refused': 0, 'failed': 0}
        for ce in self.kinds('COUNTEREXAMPLE'):
            c['declared'] += 1
            for tg, txt in ce.pairs('ASKING'):
                if tg not in self.by['TONGUE']:
                    continue
                c['texts'] += 1
                if self.understand(tg, txt).get('refused') == ce.get('REFUSED'):
                    c['refused'] += 1
                else:
                    c['failed'] += 1
        return {'examples': r, 'counterexamples': c}

    def refusal(self, tongue, kind, what):
        for k, txt in self.by['TONGUE'][tongue].pairs('REFUSES'):
            if k == kind:
                return txt.replace('{what}', what)
        return f'{kind}: {what}'

    # -- understand ---------------------------------------------------------------------------------------------------------
    def understand(self, tongue, text):
        toks, ref = self.tokens(tongue, text)
        if ref:
            kind, what = ref
            return {'refused': kind, 'what': what, 'message': self.refusal(tongue, kind, what)}
        shape = [m for m, _, _ in toks]
        for f in self.kinds('FRAME'):
            if f.names('SHAPE') == shape:
                slots = {}
                for m, ent, raw in toks:
                    if self.by['MEANING'][m].get('SLOT') in ('number', 'entity'):
                        slots[m] = ent
                r = {'frame': f.name, 'slots': slots}
                # a sentence under construction may name a surface or a step nobody declared: that is a finding of
                # the rules, never a crash of the model
                surfaces, steps = self.by.get('SURFACE', {}), self.by.get('STEP', {})
                if f.get('STEPS') is not None:
                    lawful = all(sn in steps and steps[sn].get('TARGET') in surfaces for sn in f.names('STEPS'))
                else:
                    lawful = f.get('TARGET') in surfaces and f.get('QUERY') is not None
                if not lawful:
                    return {'refused': 'surface', 'what': f.name, 'message': self.refusal(tongue, 'surface', f.name)}
                if f.get('STEPS') is not None:
                    r['surface'] = 'plan'
                    r['steps'] = [(self.by['STEP'][s].get('TARGET'), self.fill(self.by['STEP'][s].get('QUERY'), slots, self.by['STEP'][s].get('TARGET'), partial=True),
                                   self.by['STEP'][s].get('BINDS') or '') for s in f.names('STEPS')]
                    r['query'] = ' => '.join(q for _, q, _ in r['steps'])
                else:
                    r['surface'] = f.get('TARGET')
                    r['query'] = self.fill(f.get('QUERY'), slots, f.get('TARGET'))
                return r
        what = ' '.join(shape)
        return {'refused': 'shape', 'what': what, 'message': self.refusal(tongue, 'shape', what)}

    def fill(self, template, slots, surface, partial=False):
        out = template
        spells = dict(self.by['SURFACE'][surface].pairs('SPELLS'))
        for name, val in slots.items():
            m = self.by['MEANING'].get(name)
            if m is not None and m.get('SLOT') == 'entity':
                val = spell(val, spells.get(m.get('OF'), 'as_is'))
            out = out.replace('{' + name + '}', val)
        return out

    # -- ask: the graph surface answered, and told ------------------------------------------------------------------------
    def run_pattern(self, surface, query):
        triples, _ = self.world(surface)
        terms = words(query)
        if len(terms) != 3:
            return None                  # not a triple pattern: the surface refuses it
        ans = []
        for tr in triples:
            if all(q.startswith('?') or q == t for q, t in zip(terms, tr)):
                for q, t in zip(terms, tr):
                    if q.startswith('?'):
                        ans.append(t)
        return ans

    def ask(self, tongue, text):
        u = self.understand(tongue, text)
        if 'refused' in u:
            return u
        f = self.by['FRAME'][u['frame']]
        u['run'] = []
        if u['surface'] == 'plan':
            s1 = self.by['STEP'][f.names('STEPS')[0]]
            q1 = self.fill(s1.get('QUERY'), u['slots'], s1.get('TARGET'))
            if self.by['SURFACE'][s1.get('TARGET')].get('KIND') != 'pattern':
                u['run'].append(self.run_of(s1.get('TARGET'), q1))
                return u
            ans = self.run_pattern(s1.get('TARGET'), q1)
            if ans is None:
                return {'refused': 'surface', 'what': q1, 'message': self.refusal(tongue, 'surface', q1)}
            if len(ans) > 1:
                what = ' '.join(ans)
                return {'refused': 'ambiguous', 'what': what, 'message': self.refusal(tongue, 'ambiguous', what)}
            u['answer'] = ans
            u['told'] = self.tell(tongue, f, ans, u['slots'])
            if len(ans) == 1 and len(f.names('STEPS')) > 1:
                s2 = self.by['STEP'][f.names('STEPS')[1]]
                bound = dict(u['slots'], **({s1.get('BINDS'): ans[0]} if s1.get('BINDS') else {}))
                u['query2'] = self.fill(s2.get('QUERY'), bound, s2.get('TARGET'))
                if self.by['SURFACE'][s2.get('TARGET')].get('KIND') != 'pattern':
                    u['run'].append(self.run_of(s2.get('TARGET'), u['query2']))
            return u
        if self.by['SURFACE'][u['surface']].get('KIND') == 'pattern':
            ans = self.run_pattern(u['surface'], u['query'])
            if ans is None:
                return {'refused': 'surface', 'what': u['query'], 'message': self.refusal(tongue, 'surface', u['query'])}
            u['answer'] = ans
            u['told'] = self.tell(tongue, f, ans, u['slots'])
        else:
            u['run'].append(self.run_of(u['surface'], u['query']))
        return u

    def run_of(self, surface, query):
        s = self.by['SURFACE'][surface]
        return (surface, s.get('COURT') or '', s.get('WORLD') or '', query)

    def tell(self, tongue, frame, answer, slots):
        key = 'ANSWERS' if answer else 'EMPTY'
        tpl = dict(frame.pairs(key)).get(tongue)
        if tpl is None:
            return None
        names = [self.canonical(tongue, a) for a in answer]
        conj = ' ' + (self.by['TONGUE'][tongue].get('JOINS') or 'and') + ' '
        joined = names[0] if len(names) == 1 else (', '.join(names[:-1]) + conj + names[-1] if names else '')
        out = tpl.replace('{answer}', joined)
        for name, val in slots.items():
            m = self.by['MEANING'].get(name)
            if m is not None and m.get('SLOT') == 'entity':
                val = self.canonical(tongue, val)
            out = out.replace('{' + name + '}', val)
        return out


def spell(ent, how):
    return upper_first(ent) if how == 'upper_first' else ent


# ---- the rules the existing meta-vocabulary cannot say: the v0.17 court's added checks -----------------------------

PLACEHOLDER = re.compile(r'\{([A-Za-z0-9_\u0080-\U0010ffff]+)\}')


def court_is_sibling(name):
    """A surface's court that is a court file is a bare name ending in _court.haro, never a path: `check ... surfaces` runs it."""
    return name.endswith('_court.haro') and len(name) > len('_court.haro') and not any(c in name for c in '/\\:') and '..' not in name


def default_surface_check(surface, query, runner=None):
    """A surface judges a query of its grammar WITHOUT data. 'triples': exactly three terms. 'ZQL ASK': the Z
    court's `ask` over no rows answers [] for a lawful question and refuses the rest."""
    g = surface.get('GRAMMAR')
    if g == 'triples':
        return (len(words(query)) == 3, 'a triple pattern is three terms')
    court = words(surface.get('COURT') or '')
    if runner and len(court) >= 2 and court_is_sibling(court[0]) and surface.get('WORLD'):
        return runner(query)             # a surface whose court is a court file is asked as the Q letter's court is
    return (True, '')


def sample_fill(template, n, surface):
    """Fill a template's slots with values the surface's grammar can read, to ask it whether the SHAPE is lawful."""
    out = template
    for name in PLACEHOLDER.findall(template):
        m = n.by['MEANING'].get(name)
        if m is None:
            continue
        sv = {'number': '1', 'entity': 'Sample'}.get(m.get('SLOT'), 'x')
        out = out.replace('{' + name + '}', sv)
    return out


def rules(n, runner=None):
    """Every finding as (code, line, message). Empty for a lawful sentence."""
    f = []

    def add(code, d, msg):
        f.append((code, d.line, msg))
    meanings = n.by.get('MEANING', {})
    for sf in n.kinds('SURFACE'):
        cw = words(sf.get('COURT') or '')
        if cw and cw[0].endswith('.haro') and not court_is_sibling(cw[0]):
            add('N_SURFACE_COURT', sf, f"SURFACE {sf.name} names the court file '{cw[0]}': a surface's court is a court beside this one, a bare name ending in _court.haro and never a path, because `check ... surfaces` runs it")
        if sf.get('WORLD') and not n.world_read(sf.name):
            add('N_WORLD_UNREAD', sf, f"SURFACE {sf.name} reads the world '{sf.get('WORLD')}', which cannot be read from the sentence's folder")
    for fr in n.kinds('FRAME'):
        shape = fr.names('SHAPE')
        slots = [m for m in shape if meanings.get(m) and meanings[m].get('SLOT') in ('number', 'entity')]
        if len(slots) != len(set(slots)):
            add('N_SLOT_REPEATED', fr, f"FRAME {fr.name} names a slot meaning twice in its SHAPE: '{[s for s in slots if slots.count(s) > 1][0]}'")
        has_q = fr.get('TARGET') is not None and fr.get('QUERY') is not None
        has_s = fr.get('STEPS') is not None
        if has_q == has_s:
            add('N_FRAME_TARGET', fr, f'FRAME {fr.name} must have either a TARGET and a QUERY or STEPS, and not both nor neither')
        avail = set(slots)
        if has_s:
            for sn in fr.names('STEPS'):
                st = n.by['STEP'].get(sn)
                if st is None:
                    continue
                for ph in PLACEHOLDER.findall(st.get('QUERY', '')):
                    if ph not in avail:
                        add('N_SLOT_UNKNOWN', st, f"STEP {st.name} uses {{{ph}}}, which is neither a slot of FRAME {fr.name}'s SHAPE nor bound by an earlier step")
                if st.get('BINDS'):
                    avail.add(st.get('BINDS'))
        elif has_q:
            for ph in PLACEHOLDER.findall(fr.get('QUERY')):
                if ph not in avail:
                    add('N_SLOT_UNKNOWN', fr, f"FRAME {fr.name} QUERY uses {{{ph}}}, which is not a slot of its SHAPE")
        for key in ('ANSWERS', 'EMPTY'):
            for tg, txt in fr.pairs(key):
                for ph in PLACEHOLDER.findall(txt):
                    if ph not in slots and not (ph == 'answer' and key == 'ANSWERS') and ph not in avail:
                        add('N_SLOT_UNKNOWN', fr, f"FRAME {fr.name} {key} in {tg} uses {{{ph}}}, which is not a slot of its SHAPE")
        # the query is judged by its surface, here, without data
        targets = [(fr.get('TARGET'), fr.get('QUERY'))] if has_q else [(n.by['STEP'][s].get('TARGET'), n.by['STEP'][s].get('QUERY')) for s in fr.names('STEPS') if s in n.by['STEP']]
        for tgt, q in targets:
            sf = n.by['SURFACE'].get(tgt)
            if sf is None or not q:
                continue
            ok, why = default_surface_check(sf, sample_fill(q, n, tgt), runner)
            if not ok:
                add('N_QUERY_REFUSED', fr, f"FRAME {fr.name}: the surface '{tgt}' refuses the query '{q}': {why}")
        # every tongue can tell the answer: by the frame's template, or by the surface's own voice
        tgt = fr.get('TARGET') or (n.by['STEP'][fr.names('STEPS')[-1]].get('TARGET') if has_s and fr.names('STEPS') and fr.names('STEPS')[-1] in n.by['STEP'] else None)
        tells = n.by['SURFACE'][tgt].names('TELLS') if tgt in n.by['SURFACE'] else []
        have = {tg for tg, _ in fr.pairs('ANSWERS')}
        empty = {tg for tg, _ in fr.pairs('EMPTY')}
        for tn in n.tongues:
            if tn in have and tn not in empty:
                add('N_TELL_UNCOVERED', fr, f"FRAME {fr.name} has ANSWERS in {tn} but no EMPTY: an answer may be nobody")
            if has_s:
                if tn not in have:
                    add('N_TELL_UNCOVERED', fr, f"FRAME {fr.name} has no ANSWERS in {tn} for its first step")
                if tn not in tells:
                    add('N_TELL_UNCOVERED', fr, f"FRAME {fr.name} cannot tell its last step in {tn}: the surface '{tgt}' does not tell in {tn}")
            elif tn not in have and tn not in tells:
                add('N_TELL_UNCOVERED', fr, f"FRAME {fr.name} cannot be told in {tn}: no ANSWERS in {tn} and the surface '{tgt}' does not tell in {tn}")
    for t in n.kinds('TONGUE'):
        have = {k for k, _ in t.pairs('REFUSES')}
        miss = [k for k in REFUSAL_KINDS if k not in have]
        if miss:
            add('N_REFUSAL_UNCOVERED', t, f"TONGUE {t.name} does not say how it refuses: {', '.join(miss)}")
        extra = [c for c in t.get('ALLOWS', '') if c not in SAFE_PUNCTUATION]
        if extra:
            add('N_GATE_WIDENED', t, f"TONGUE {t.name} ALLOWS '{extra[0]}', outside the court's safe set {SAFE_PUNCTUATION}: a tongue cannot widen the gate")
        _, _, clashes = n.lexicon(t.name)
        for w, a, b in clashes:
            add('N_WORD_AMBIGUOUS', t, f"in {t.name} the word '{w}' means both {a} and {b}")
        ignored, lex, _ = n.lexicon(t.name)
        for w in sorted(ignored & set(lex)):
            add('N_WORD_IGNORED', t, f"in {t.name} the word '{w}' is both ignored and a word of {lex[w][0]}")
    for m in n.kinds('MEANING'):
        slot = m.get('SLOT')
        if slot == 'none':
            cols = {tg for tg, _ in m.pairs('WORDS')}
            for tn in n.tongues:
                if tn not in cols:
                    add('N_TONGUE_UNCOVERED', m, f"MEANING {m.name} has no words in {tn}")
        if slot == 'entity':
            sf = n.by['SURFACE'].get(m.get('FROM'))
            if m.get('OF') is None or m.get('FROM') is None:
                add('N_ENTITY_UNKNOWN', m, f'MEANING {m.name} is an entity and needs both OF and FROM')
            elif sf is not None and m.get('OF') not in sf.names('ENTITIES'):
                add('N_ENTITY_UNKNOWN', m, f"MEANING {m.name} is of '{m.get('OF')}', which the surface '{m.get('FROM')}' does not enumerate")
    for ex in n.kinds('EXAMPLE'):
        fr = n.by['FRAME'].get(ex.get('MEANS'))
        if fr is None:
            continue
        got = {}
        for tg, txt in ex.pairs('ASKING'):
            if tg not in n.by['TONGUE']:
                continue
            u = n.understand(tg, txt)
            if u.get('frame') != ex.get('MEANS'):
                add('N_EXAMPLE_FAILED', ex, f"EXAMPLE {ex.name} in {tg} ('{txt}') is {('understood as ' + u['frame']) if 'frame' in u else ('refused as ' + u['refused'])}, not as {ex.get('MEANS')}")
            else:
                got[tg] = u['query']
        if len(set(got.values())) > 1:
            add('N_EXAMPLE_DIVERGES', ex, f'EXAMPLE {ex.name} compiles to different queries in different tongues: {sorted(set(got.values()))}')
    for ce in n.kinds('COUNTEREXAMPLE'):
        for tg, txt in ce.pairs('ASKING'):
            if tg not in n.by['TONGUE']:
                continue
            u = n.understand(tg, txt)
            if u.get('refused') != ce.get('REFUSED'):
                add('N_COUNTEREXAMPLE_FAILED', ce, f"COUNTEREXAMPLE {ce.name} in {tg} ('{txt}') was {('understood as ' + u['frame']) if 'frame' in u else ('refused as ' + u['refused'])}, not refused as {ce.get('REFUSED')}")
    f.sort(key=lambda x: (x[1], x[0]))
    return f
