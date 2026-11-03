"""Haro v0.33 -- INCLUDES, ON a FORM, and a quantifier over a FORM (Central's item 4, stzzui's S5), and S14 answered. Fixtures first.

Writes fixtures.json (the meta-court's), court_cases.json and the twelve sentences of spike/medium/ BEFORE any code reads INCLUDES. The world
medium_v33.haro (written with the new forms) and its hand-expanded twin v33/medium_expanded.haro are committed with them: the twin IS the definition,
and the guard compares the courts forged from the two byte for byte.

The design this file pins (the desk's, within the author's word "Items 4 and S14"; D47 records it for him to refuse):

  INCLUDES [form, ...]    a clause of DECLARATION. The seats of the named FORMs come first, in INCLUDES order, then the declaration's own SEATS (still required:
                          a kind that adds nothing writes `SEATS []`). A seat may come once. The court never sees the sugar: it is forged from the expanded seats
  ON form                 a CONSTRAINT written ON a FORM some DECLARATION includes is made once for each including kind, in declaration order, named <constraint>_<kind>,
                          the same condition, message, code, cites and severity
  some | all | earlier | exists FORM  in a condition (a CONSTRAINT's WHEN and THEN, a VIEW's WHERE) ranges over every kind that includes the FORM: the `or` of the
                          quantifier over each kind for some, earlier and exists, the `and` for all. A name that is already a seat of the constraint's kind keeps its meaning
  EXCEPT [kind, ...]      a clause of a CONSTRAINT written ON a FORM: the kinds it is not made for. Found by rewriting stzzui's real declaration: two of its five repeated stems are
                          identical for nine kinds and differ for INTERACTION alone, which has the extra seat ROLE; that kind keeps an explicit constraint of its own
  S14                     a verb guaranteed in either of two lists is ONE where: `some K where satisfies contains V or always_reachable contains V`, which the condition language
                          could always say; the answer to S14 is that, and the quantifier over a FORM that spares writing it once per kind

Run once; the files it writes are committed as they stand."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)

# ---- the sentences -------------------------------------------------------------------------------------------------------------
os.makedirs(os.path.join(SPIKE, 'medium'), exist_ok=True)


def sentence(fname, comment, decls):
    """decls: (VERB, name, [(CLAUSE, value)], rationale). Returns {verb name: its DEFINE line} and writes the file."""
    lines = ['-- ' + fname + ' -- a sentence of medium_v33.haro: ' + comment, '']
    at = {}
    for verb, name, clauses, why in decls:
        at[name] = len(lines) + 1
        lines.append(f'DEFINE {verb} {name} AS (')
        for k, (c, v) in enumerate(clauses):
            lines.append(f'  {c} {v}' + (',' if k < len(clauses) - 1 else ''))
        lines.append(f') RATIONALE "{why}"')
        lines.append('')
    with open(os.path.join(SPIKE, 'medium', fname), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines))
    return at


A = ('ACTOR', 'ops')
clean = sentence('clean.medium', 'three kinds that include the shared guarantees; nothing refused.', [
    ('SCREEN', 'home', [A, ('SATISFIES', '[read]')], 'The home screen reads'),
    ('VIBE', 'calm', [A, ('SATISFIES', '[confirm]'), ('ALWAYS_REACHABLE', '[cancel]'), ('SURFACE_AS', 'visual')], 'Confirm, with cancel always reachable'),
    ('PANEL', 'signup', [A, ('SATISFIES', '[read]')], 'A sign-up panel')])
nc_screen = sentence('no_cancel_screen.medium', 'ON a FORM reaches a SCREEN: it satisfies CONFIRM and keeps no CANCEL always reachable.', [
    ('SCREEN', 'home', [A, ('SATISFIES', '[confirm]')], 'A screen that confirms with no way out')])
nc_vibe = sentence('no_cancel_vibe.medium', 'ON a FORM reaches a VIBE.', [
    ('VIBE', 'calm', [A, ('SATISFIES', '[confirm]')], 'A vibe that confirms with no way out')])
nc_panel = sentence('no_cancel_panel.medium', 'ON a FORM reaches a PANEL.', [
    ('PANEL', 'signup', [A, ('SATISFIES', '[confirm]')], 'A panel that confirms with no way out')])
p_first = sentence('print_zoom_first.medium', 'S14, the first list: a VIBE on print while a SCREEN satisfies ZOOM.', [
    ('SCREEN', 'home', [A, ('SATISFIES', '[zoom]')], 'A screen that zooms'),
    ('VIBE', 'loud', [A, ('SATISFIES', '[read]'), ('SURFACE_AS', 'print')], 'A vibe on a medium that carries no zoom')])
p_second = sentence('print_zoom_second.medium', 'S14, the second list: a VIBE on print while a PANEL keeps ZOOM always reachable.', [
    ('PANEL', 'signup', [A, ('ALWAYS_REACHABLE', '[zoom]')], 'A panel that keeps zoom within reach'),
    ('VIBE', 'loud', [A, ('SATISFIES', '[read]'), ('SURFACE_AS', 'print')], 'A vibe on a medium that carries no zoom')])
sentence('print_no_zoom.medium', 'a VIBE on print and no declaration guarantees ZOOM: lawful.', [
    ('SCREEN', 'home', [A, ('SATISFIES', '[read]')], 'A screen that reads'),
    ('VIBE', 'loud', [A, ('SATISFIES', '[read]'), ('SURFACE_AS', 'print')], 'A vibe on print')])
sentence('visual_zoom.medium', 'a SCREEN satisfies ZOOM and the VIBE is on a visual surface, which carries it: lawful.', [
    ('SCREEN', 'home', [A, ('SATISFIES', '[zoom]')], 'A screen that zooms'),
    ('VIBE', 'calm', [A, ('SATISFIES', '[read]'), ('SURFACE_AS', 'visual')], 'A vibe on a visual surface')])
no_actor = sentence('no_actor.medium', 'a SCREEN names no actor: the sentence stands and the VIBE warns (ALL over a FORM).', [
    ('SCREEN', 'home', [('SATISFIES', '[read]')], 'A screen with no actor'),
    ('VIBE', 'calm', [A, ('SATISFIES', '[read]'), ('SURFACE_AS', 'visual')], 'A vibe')])
ns_screen = sentence('no_satisfies_screen.medium', 'EXCEPT: a SCREEN satisfies nothing, and the constraint ON the FORM, made for it, warns.', [
    ('SCREEN', 'home', [A], 'A screen with no reason')])
sentence('no_satisfies_panel.medium', 'EXCEPT [panel]: a PANEL satisfies nothing, and the constraint ON the FORM was not made for it, so nothing warns.', [
    ('PANEL', 'signup', [A], 'A panel bound to something else')])
ns_vibe = sentence('no_satisfies_vibe.medium', 'EXCEPT: a VIBE satisfies nothing, and the constraint is made for it too.', [
    ('VIBE', 'calm', [A, ('SURFACE_AS', 'visual')], 'A vibe with no reason')])
sentence('bad_intent.medium', 'an intent the menu lacks, in a seat a kind got from the FORM: refused by the seat\'s own MENU.', [
    ('SCREEN', 'home', [A, ('SATISFIES', '[dance]')], 'A screen that dances')])
sentence('own_seat.medium', 'a seat a kind adds to what it includes (SURFACE_AS) next to the included ones: lawful.', [
    ('VIBE', 'calm', [A, ('SATISFIES', '[read]'), ('SURFACE_AS', 'voice')], 'A vibe on voice')])
sentence('unknown_seat.medium', 'a seat no kind has: the expanded kinds are closed, as a hand-written one is (line 4).', [
    ('SCREEN', 'home', [A, ('DENSITY', 'high')], 'A screen with a seat it does not have')])

# ---- the court's cases -------------------------------------------------------------------------------------------------------
MC = 'satisfies CONFIRM and keeps no CANCEL always reachable'
cases = [
    {'id': 'M1', 'name': 'the clean sentence: three kinds that include the shared guarantees', 'verb': 'check', 'args': ['medium/clean.medium'], 'first': 'ok', 'counts': {'SCREEN': 1, 'VIBE': 1, 'PANEL': 1}},
    {'id': 'M2', 'name': 'the meta-court reads the world: three declarations, one form, seven constraints (ON a FORM made three, and ON a FORM EXCEPT one made two)', 'verb': 'meta', 'args': ['medium_v33.haro'], 'first': 'ok',
     'contains': ['declarations 3', 'forms 1', 'menus 2', 'constraints 7']},
    {'id': 'M3', 'name': 'ON a FORM, on a SCREEN: made once, enforced on the first kind that includes it', 'verb': 'check', 'args': ['medium/no_cancel_screen.medium'], 'refused': True,
     'contains': [f'medium (line {nc_screen["home"]}): home {MC}']},
    {'id': 'M4', 'name': 'ON a FORM, on a VIBE', 'verb': 'check', 'args': ['medium/no_cancel_vibe.medium'], 'refused': True, 'contains': [f'medium (line {nc_vibe["calm"]}): calm {MC}']},
    {'id': 'M5', 'name': 'ON a FORM, on a PANEL', 'verb': 'check', 'args': ['medium/no_cancel_panel.medium'], 'refused': True, 'contains': [f'medium (line {nc_panel["signup"]}): signup {MC}']},
    {'id': 'M6', 'name': 'the envelope of a constraint made ON a FORM: its code and its cite, as if written by hand', 'verb': 'diagnose', 'args': ['medium/no_cancel_panel.medium'],
     'diagnose': {'code': 'MISSING_CANCEL', 'cites': ['rule:cancel']}},
    {'id': 'M7', 'name': 'S14, the first list: a verb guaranteed in SATISFIES of any kind, read by a quantifier over the FORM', 'verb': 'check', 'args': ['medium/print_zoom_first.medium'], 'refused': True,
     'contains': [f'medium (line {p_first["loud"]}): VIBE loud puts the surface on print, which carries no ZOOM, and a declaration guarantees it']},
    {'id': 'M8', 'name': 'S14, the second list: the same verb in ALWAYS_REACHABLE of another kind, read by the same where', 'verb': 'check', 'args': ['medium/print_zoom_second.medium'], 'refused': True,
     'contains': [f'medium (line {p_second["loud"]}): VIBE loud puts the surface on print, which carries no ZOOM, and a declaration guarantees it']},
    {'id': 'M9', 'name': 'the envelope of S14: VERB_NOT_CARRIED, citing rule:medium', 'verb': 'diagnose', 'args': ['medium/print_zoom_second.medium'],
     'diagnose': {'code': 'VERB_NOT_CARRIED', 'cites': ['rule:medium']}},
    {'id': 'M10', 'name': 'on print and no declaration guarantees the verb: lawful', 'verb': 'check', 'args': ['medium/print_no_zoom.medium'], 'first': 'ok', 'counts': {'SCREEN': 1, 'VIBE': 1}},
    {'id': 'M11', 'name': 'the verb is guaranteed but the surface is visual, which carries it: lawful', 'verb': 'check', 'args': ['medium/visual_zoom.medium'], 'first': 'ok', 'counts': {'SCREEN': 1, 'VIBE': 1}},
    {'id': 'M12', 'name': 'ALL over a FORM: one kind names no actor, the sentence stands and the VIBE warns, at its own line', 'verb': 'check', 'args': ['medium/no_actor.medium'], 'first': 'ok',
     'contains': [f'warning NO_ACTOR: VIBE calm: some declaration of the sentence names no actor (line {no_actor["calm"]})']},
    {'id': 'M13', 'name': 'a seat a kind got from the FORM is checked by its own MENU, as a hand-written one is', 'verb': 'check', 'args': ['medium/bad_intent.medium'], 'refused': True,
     'contains': ["An intent is confirm, cancel, zoom or read, not 'dance'"]},
    {'id': 'M14', 'name': 'a seat the kind adds beside the included ones is lawful', 'verb': 'check', 'args': ['medium/own_seat.medium'], 'first': 'ok', 'counts': {'VIBE': 1}},
    {'id': 'M16', 'name': 'EXCEPT: the constraint ON the FORM is made for a SCREEN, which satisfies nothing, and warns at its own line', 'verb': 'check', 'args': ['medium/no_satisfies_screen.medium'],
     'first': 'ok', 'contains': [f'warning NO_SATISFIES: home satisfies nothing: a surface exists for a reason (line {ns_screen["home"]})']},
    {'id': 'M17', 'name': 'EXCEPT [panel]: the constraint was not made for a PANEL, so a panel that satisfies nothing is lawful and silent', 'verb': 'check', 'args': ['medium/no_satisfies_panel.medium'],
     'first': 'ok', 'lacks': ['NO_SATISFIES']},
    {'id': 'M18', 'name': 'EXCEPT leaves the other kinds: a VIBE that satisfies nothing warns', 'verb': 'check', 'args': ['medium/no_satisfies_vibe.medium'],
     'first': 'ok', 'contains': [f'warning NO_SATISFIES: calm satisfies nothing: a surface exists for a reason (line {ns_vibe["calm"]})']},
    {'id': 'M15', 'name': 'the expanded kinds are closed: a seat no kind has is refused', 'verb': 'check', 'args': ['medium/unknown_seat.medium'], 'refused': True, 'contains': ["DENSITY"]},
]
cdoc = {
    'name': 'the medium world -- sentence-level cases for Haro v0.33 (INCLUDES, ON a FORM, a quantifier over a FORM; Central\'s item 4, stzzui\'s S5; S14)',
    'comment': ('Written BEFORE any code reads INCLUDES. Each case runs the court forged from medium_v33.haro on haro AND on its checked build; the two must print the same '
                'bytes, and the guard also forges v33/medium_expanded.haro, the hand-expanded twin, and requires the same court byte for byte. The sentences are in medium/. '
                'M7 and M8 are S14: one where reads two lists. A constraint ON a FORM is enforced on every kind that includes it (M3, M4, M5), except the kinds it EXCEPTs (M16, M17, M18).'),
    'cases': cases,
}
with open(os.path.join(HERE, 'court_cases.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(cdoc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')

# ---- the meta-court's fixtures ------------------------------------------------------------------------------------------------
LANG = 'DEFINE LANGUAGE medium AS (VERSION "0.33", GRAMMAR "0.33", COURT "x", EXTENSION ".medium") RATIONALE "x"\n'
MENU = 'DEFINE MENU intents AS (WORDS [confirm, cancel, zoom, read], CODE "UNKNOWN_INTENT") RATIONALE "x"\n'
FORMG = 'DEFINE FORM guarantees AS (SEATS [satisfies: [intents]?, always_reachable: [intents]?, actor: name?]) RATIONALE "x"\n'


def decl(name, verb, incl='[guarantees]', seats='[]'):
    inc = f'INCLUDES {incl}, ' if incl else ''
    return f'DEFINE DECLARATION {name} AS (VERB "{verb}", {inc}SEATS {seats}) RATIONALE "x"\n'


BASE = LANG + MENU + FORMG + decl('screen', 'SCREEN') + decl('vibe', 'VIBE', seats='[density: name?]')


def con(name, on, when, extra='', exc=''):
    e = f'EXCEPT {exc}, ' if exc else ''
    return f'DEFINE CONSTRAINT {name} AS (ON {on}, {e}WHEN "{when}", MESSAGE "m"{extra}) RATIONALE "x"\n'


def accept(id_, name, src, **counts):
    return {'id': id_, 'name': name, 'source': src, 'expect': {'language': 'medium', 'counts': counts}}


def reject(id_, name, src, refusal):
    return {'id': id_, 'name': name, 'source': src, 'refusal': refusal}


accepts = [
    accept('A1', 'INCLUDES: two kinds take the seats of a FORM, and the declarations are two', BASE, declarations=2, forms=1, constraints=0),
    accept('A2', 'a seat an included FORM gives is a seat of the kind: a constraint ON the kind may read it (actor)', BASE + con('c', 'vibe', 'actor present'), constraints=1),
    accept('A3', 'ON a FORM is made once for each kind that includes it: two kinds, two constraints', BASE + con('c', 'guarantees', 'satisfies contains confirm'), constraints=2),
    accept('A4', 'some over a FORM ranges over the kinds that include it, two lists in one where (S14)',
           BASE + con('c', 'vibe', 'density = x and (some guarantees where satisfies contains zoom or always_reachable contains zoom)'), constraints=1),
    accept('A5', 'all, exists and earlier over a FORM', BASE + con('c1', 'vibe', 'not (all guarantees where actor present)') + con('c2', 'vibe', 'exists guarantees')
           + con('c3', 'vibe', 'earlier guarantees where actor present'), constraints=3),
    accept('A6', 'a kind adds its own seats beside the included ones, and includes two FORMs',
           LANG + MENU + FORMG + 'DEFINE FORM more AS (SEATS [note: name?]) RATIONALE "x"\n' + decl('screen', 'SCREEN', incl='[guarantees, more]', seats='[density: name?]'), declarations=1, forms=2),
    accept('A7', 'an existing reading never changes: a seat of the kind named like a FORM stays that seat, so `tag present` reads the quantified declaration\'s seat',
           LANG + MENU + FORMG + 'DEFINE DECLARATION step AS (VERB "STEP", SEATS [tag: name?]) RATIONALE "x"\n'
           + 'DEFINE DECLARATION screen AS (VERB "SCREEN", INCLUDES [guarantees], SEATS [guarantees: [step]?]) RATIONALE "x"\n'
           + con('c', 'screen', 'some guarantees where tag present'), constraints=1),
    accept('A8', 'a FORM no kind includes is still a FORM: ON still names a DECLARATION, as it did, and a kind without INCLUDES is the kind it was',
           LANG + MENU + FORMG + decl('screen', 'SCREEN', incl='', seats='[actor: name?]') + con('c', 'screen', 'actor present'), declarations=1, constraints=1),
    accept('A9', 'EXCEPT [kind]: a constraint ON a FORM is made for the including kinds but the ones it excepts', BASE + con('c', 'guarantees', 'actor present', exc='[vibe]'), constraints=1),
    accept('A10', 'the excepted kind has its own constraint beside the one made for the others: two constraints, no collision',
           BASE + con('c', 'guarantees', 'actor present', exc='[vibe]') + con('c_vibe', 'vibe', 'actor present and density present'), constraints=2),
    accept('A11', 'a quantifier over a FORM inside the where of another is expanded too (added after the code, found by planting it off)',
           BASE + con('c', 'vibe', 'some guarantees where (some guarantees where actor present)'), constraints=1),
    accept('A12', "a VIEW's WHERE may quantify over a FORM as a constraint's WHEN may (added after the code, found by planting it off)",
           BASE + 'DEFINE VIEW v AS (ONE "screen", WHERE "some guarantees where actor present") RATIONALE "x"\n', views=1),
]
rejects = [
    reject('R1', 'INCLUDES names nothing', BASE.replace('INCLUDES [guarantees], SEATS []', 'INCLUDES [ghost], SEATS []'), "INCLUDES: 'ghost' resolves to nothing in this declaration"),
    reject('R2', 'INCLUDES names something that is no FORM', BASE.replace('INCLUDES [guarantees], SEATS []', 'INCLUDES [intents], SEATS []'), "INCLUDES must name a FORM; 'intents' is a MENU"),
    reject('R3', 'INCLUDES names a FORM twice', BASE.replace('INCLUDES [guarantees], SEATS []', 'INCLUDES [guarantees, guarantees], SEATS []'), "INCLUDES names 'guarantees' twice"),
    reject('R4', 'a seat comes twice: from the FORM and from the kind\'s own SEATS',
           BASE.replace('SEATS []', 'SEATS [actor: name?]', 1), "seat 'actor' of screen comes twice: from the FORM 'guarantees' and from its own SEATS"),
    reject('R5', 'a seat comes twice: from two FORMs', LANG + MENU + FORMG + 'DEFINE FORM more AS (SEATS [actor: name?]) RATIONALE "x"\n' + decl('screen', 'SCREEN', incl='[guarantees, more]'),
           "seat 'actor' of screen comes twice: from the FORM 'guarantees' and from the FORM 'more'"),
    reject('R6', 'ON a FORM no kind includes keeps the refusal it had', LANG + MENU + FORMG + decl('screen', 'SCREEN', incl='', seats='[actor: name?]') + con('c', 'guarantees', 'actor present'),
           "ON must name a DECLARATION; 'guarantees' is a FORM"),
    reject('R7', 'ON a MENU keeps the refusal it had', BASE + con('c', 'intents', 'actor present'), "ON must name a DECLARATION; 'intents' is a MENU"),
    reject('R8', 'a where that reads a seat only some of the kinds have is refused, naming the kind that lacks it',
           BASE + con('c', 'vibe', 'some guarantees where density present'), "no seat 'density' on screen"),
    reject('R9', 'a FORM no kind includes is no quantifier head: the refusal it had', LANG + MENU + FORMG + decl('screen', 'SCREEN', incl='', seats='[actor: name?]') + con('c', 'screen', 'some guarantees where actor present'),
           "'guarantees' names neither a declaration kind nor a list of references"),
    reject('R10', 'a constraint made ON a FORM may not take the name of a declaration: one namespace', BASE + 'DEFINE DECLARATION c_screen AS (VERB "CS", SEATS []) RATIONALE "x"\n'
           + con('c', 'guarantees', 'actor present'), "the constraint 'c_screen' that ON guarantees makes for screen is already declared -- one namespace, one name, one meaning"),
    reject('R11', 'INCLUDES belongs to a DECLARATION: a FORM has no such clause', LANG + MENU + 'DEFINE FORM f AS (INCLUDES [g], SEATS [a: name]) RATIONALE "x"\n',
           "Unknown clause 'INCLUDES' in FORM -- allowed: SEATS"),
    reject('R12', 'SEATS is still required beside INCLUDES: a kind that adds nothing writes SEATS []', BASE.replace('INCLUDES [guarantees], SEATS []', 'INCLUDES [guarantees]'),
           'DECLARATION requires the SEATS clause'),
    reject('R13', 'a constraint made ON a FORM names its condition\'s seat for each kind: a seat the FORM does not give is refused where it is missing',
           BASE + con('c', 'guarantees', 'density present'), "no seat 'density' on screen"),
    reject('R14', 'EXCEPT belongs to a constraint ON a FORM: ON a kind has nothing to except', BASE + con('c', 'screen', 'actor present', exc='[vibe]'), "EXCEPT belongs to a constraint ON a FORM, and 'screen' is a DECLARATION"),
    reject('R15', 'EXCEPT names nothing', BASE + con('c', 'guarantees', 'actor present', exc='[ghost]'), "EXCEPT: 'ghost' resolves to nothing in this declaration"),
    reject('R16', 'EXCEPT names a kind that does not include the FORM', BASE + decl('plain', 'PLAIN', incl='', seats='[actor: name?]') + con('c', 'guarantees', 'actor present', exc='[plain]'),
           "EXCEPT names 'plain', which does not include the FORM 'guarantees'"),
    reject('R17', 'EXCEPT names a kind twice', BASE + con('c', 'guarantees', 'actor present', exc='[vibe, vibe]'), "EXCEPT names 'vibe' twice"),
    reject('R19', "an unreadable condition in a language that has forms is the validator's to speak of, quoting the text as written (added after the code, found by planting it off)",
           BASE + con('c', 'vibe', 'some guarantees where ('), "condition: expected a seat, found '' -- in 'some guarantees where ('"),
    reject('R18', 'EXCEPT may not leave the constraint without a kind', BASE + con('c', 'guarantees', 'actor present', exc='[screen, vibe]'), "EXCEPT leaves no kind for ON guarantees"),
]
doc = {
    'grammar': 'haro', 'version': '0.33',
    'comment': ('Written BEFORE any code reads INCLUDES (the W discipline). v0.33 answers Central\'s item 4 (stzzui\'s S5: four seats and 40 of 60 constraints written ten times) and S14. '
                'INCLUDES [form] on a DECLARATION; ON a FORM, and a quantifier (some, all, earlier, exists) over a FORM, expand over the kinds that include it. All of it is sugar '
                'the meta-court resolves: the court never sees it, which the guard proves by forging the hand-expanded twin and comparing the courts byte for byte. '
                'A1-A12 accept (A7 and A8 pin that no existing reading changes); R1-R19 refuse, each by the fragment of why. R6, R7 and R9 keep refusals the language already spoke.'),
    'accepts': accepts, 'rejects': rejects,
}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print(f'{len(accepts)} accepts, {len(rejects)} rejects; {len(cases)} court cases; 15 sentences')
