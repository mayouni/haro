"""Haro v0.35 -- the per-seat severity: a reference that resolves to nothing, and a kind a REFUSAL names, may be a WARNING. Fixtures first.

Writes, BEFORE any code reads a SEVERITIES clause: fixtures.json (the meta-court's), panel_v35.haro (a language that declares all five of StzZui's warnings),
v35/panel_errors.haro (the same language with every SEVERITIES line removed: its twin), the sentences under panel/, panel/world.json, and court_cases.json.

THE ASK. The constitution desk's, routed 2026-11-02 (mailbox/constitution.md, WC0): "the per-seat severity design, with Zin's per-rule granularity beside it". Its customer
is StzZui's seam S1: five diagnostics are warnings in zane.js and the court can only refuse, so zane.stzu leaves them undeclared rather than over-refuse. Read against
violations.json (stzzui origin/main ff5d1c5, read-only), the five are three mechanisms, and only one of them is a seat:

  INTENT_FLOW_NO_SATISFIES  an INTENT_FLOW declares no intents        ALREADY: a CONSTRAINT `satisfies absent or satisfies empty`, SEVERITY warning (v0.25)
  ROLE_UNDECLARED           interactions, and none has a role          ALREADY: ON interaction, `not (earlier interaction) and (all interaction where role absent)`,
                                                                       SEVERITY warning -- said once per sentence, on its first interaction
  UNRESOLVED_INTENT_FLOW    a reference names no declared flow         NEW: SEVERITIES [intent_flow: warning] on the kind -- the per-seat severity
  UNRESOLVED_ENTITY         a name resolves to no entity in the world  NEW: the same, on a SYMBOL seat resolved against a world
  UNSPECIFIED_DECLARATION   WIDGET and USER, kinds the language lacks  NEW: SEVERITIES [widget: warning] on unknown_declaration -- the NAMED kind is read past, and said

The two ALREADY were proved on a scratch language before any fixture was written, and are judged here by P1 to P4.

ZIN'S GRANULARITY, BESIDE IT. Zin sets severity per RULE (WEAVE_POLICY); Haro already does: a CONSTRAINT is a rule, and its SEVERITY is v0.25's. The weave sets it per
WEAVE (v0.25's constitutional, governance, advisory). What neither carried is the rule the GRAMMAR makes -- a reference must resolve, a kind must be declared: those have
no CONSTRAINT to carry a SEVERITY, so the severity goes where the rule is written: on the SEAT (beside its MESSAGES and CODES) and on the NAMED word (beside its message and
code). Same two words, error and warning, at every grain.

WHAT A WARNING IS. A refusal demoted, and nothing else: the same code, the same cites, the same line, the same words; the verdict stays ok and the warning is spoken after
it, as a constraint's is. The twin pins it: panel_errors.haro, the same language without SEVERITIES, must refuse each sentence with exactly the text the warning carries.
Only a reference that resolves to nothing may be a warning: a value of the wrong shape is never one (a menu seat, a number seat). A NAMED kind read past is not declared --
it counts nowhere, and a reference to it dangles.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(s)


# ---- the meta-court's fixtures ----------------------------------------------------------------------------------------------------------------
LANG = 'DEFINE LANGUAGE q AS (VERSION "0.35", GRAMMAR "0.35", COURT "x", EXTENSION ".q") RATIONALE "x"\n'
COMMON = ('DEFINE MENU roles AS (WORDS [primary, secondary], MESSAGE "a role") RATIONALE "x"\n'
          'DEFINE SYMBOL entity AS (KIND "entity", MESSAGE "x") RATIONALE "x"\n'
          'DEFINE UNION target AS (OF [flow, form]) RATIONALE "x"\n'
          'DEFINE DECLARATION flow AS (VERB "FLOW", SEATS []) RATIONALE "x"\n')
SEATS = 'SEATS [flow: flow?, flows: [flow]?, role: roles?, entity: entity?, target: target?, title: text?]'


def form(extra=''):
    return f'DEFINE DECLARATION form AS (VERB "FORM", {SEATS}{extra}) RATIONALE "x"\n'


def refusal(cat='unknown_declaration', extra=', NAMED [widget: "w", user: "u"]'):
    return f'DEFINE REFUSAL {cat} AS (MESSAGE "x"{extra}) RATIONALE "x"\n'


def accept(id_, name, src, **counts):
    return {'id': id_, 'name': name, 'source': src, 'expect': {'language': 'q', 'counts': counts}}


def reject(id_, name, src, refusal_):
    return {'id': id_, 'name': name, 'source': src, 'refusal': refusal_}


B = LANG + COMMON
accepts = [
    accept('A1', 'a reference to a declaration at warning', B + form(', SEVERITIES [flow: warning]'), declarations=2),
    accept('A2', 'a list of references at warning', B + form(', SEVERITIES [flows: warning]'), declarations=2),
    accept('A3', 'a UNION of declarations at warning', B + form(', SEVERITIES [target: warning]'), declarations=2),
    accept('A4', 'a SYMBOL at warning: resolved against a world', B + form(', SEVERITIES [entity: warning]'), declarations=2, symbols=1),
    accept('A5', 'error written out is the default, accepted as SEVERITY error is on a CONSTRAINT', B + form(', SEVERITIES [flow: error, flows: warning]'), declarations=2),
    accept('A6', 'a NAMED kind at warning', B + form() + refusal(extra=', NAMED [widget: "w", user: "u"], SEVERITIES [widget: warning]'), refusals=1),
    accept('A7', 'without SEVERITIES nothing changes', B + form() + refusal(), declarations=2, refusals=1),
    accept('A8', 'beside MESSAGES and CODES, in any order', B + form(', SEVERITIES [flow: warning], MESSAGES [flow: "m {value}"], CODES [flow: "NO_FLOW"]'), declarations=2),
]
rejects = [
    reject('R1', 'SEVERITIES names a seat the kind lacks', B + form(', SEVERITIES [ghost: warning]'), "SEVERITIES: no seat 'ghost' on form"),
    reject('R2', 'a severity is error or warning', B + form(', SEVERITIES [flow: loud]'), "'loud' is not a SEVERITY of a seat: error or warning"),
    reject('R3', 'a MENU seat is no reference: a wrong word is never a warning', B + form(', SEVERITIES [role: warning]'),
           "SEVERITIES: 'role' of form is not a reference: only a reference that resolves to nothing may be a warning"),
    reject('R4', 'a plain value is no reference', B + form(', SEVERITIES [title: warning]'), "SEVERITIES: 'title' of form is not a reference"),
    reject('R5', 'a seat is named once', B + form(', SEVERITIES [flow: warning, flow: error]'), "'flow' is named twice in SEVERITIES"),
    reject('R6', 'a REFUSAL\'s SEVERITIES belongs to unknown_declaration', B + form() + refusal('unknown_seat', ', NAMED [widget: "w"], SEVERITIES [widget: warning]'),
           "SEVERITIES belongs to unknown_declaration: a NAMED kind can be read past and said; 'unknown_seat' cannot be a warning"),
    reject('R7', 'the word is a NAMED word', B + form() + refusal(extra=', NAMED [widget: "w"], SEVERITIES [gadget: warning]'), "SEVERITIES: 'gadget' is not a NAMED word of unknown_declaration"),
    reject('R8', 'without NAMED there is no word to name', B + form() + refusal(extra=', SEVERITIES [widget: warning]'), "SEVERITIES: 'widget' is not a NAMED word of unknown_declaration"),
    reject('R9', 'a NAMED word\'s severity is error or warning', B + form() + refusal(extra=', NAMED [widget: "w"], SEVERITIES [widget: soft]'),
           "'soft' is not a SEVERITY of a NAMED word: error or warning"),
    reject('R10', 'a word is named once', B + form() + refusal(extra=', NAMED [widget: "w"], SEVERITIES [widget: warning, widget: warning]'), "'widget' is named twice in SEVERITIES"),
    reject('R11', 'unknown_verb cannot be a warning either: an unknown verb stops the parse', B + form() + refusal('unknown_verb', ', SEVERITIES [widget: warning]'),
           "SEVERITIES belongs to unknown_declaration"),
]
wr(os.path.join(HERE, 'fixtures.json'), json.dumps({
    'grammar': 'haro', 'version': '0.35',
    'comment': ('Written BEFORE any code reads SEVERITIES (the W discipline). v0.35 is the per-seat severity: SEVERITIES [seat: warning] on a DECLARATION, for a seat whose value is '
                'a reference (a DECLARATION, a UNION of declarations, a SYMBOL); SEVERITIES [word: warning] on unknown_declaration, for a NAMED word. A1-A8 accept; R1-R11 refuse, each '
                'by the fragment of why. A7 pins that nothing existing changes. The module docstring of gen_fixtures.py states the ask, the five warnings and Zin\'s granularity.'),
    'accepts': accepts, 'rejects': rejects}, indent=1, ensure_ascii=False) + '\n')

# ---- the panel world: all five of StzZui's warnings, declared -----------------------------------------------------------------------------------
PANEL = '''-- panel_v35.haro -- a small surface language that declares all five of StzZui's warnings (Haro v0.35, the per-seat severity). Not StzZui's language: its
-- shape, cut to what the five need. Two are constraints of SEVERITY warning (v0.25, already expressible); two are reference seats held at warning by
-- SEVERITIES (one to a declaration, one to a SYMBOL the world resolves); one is a NAMED kind held at warning, read past and said. Beside each warning
-- seat stands one that is NOT held, so a sentence shows the grain: per seat, per word. v35/panel_errors.haro is this file with the SEVERITIES lines removed.

DEFINE LANGUAGE panel AS (
  VERSION "0.35", GRAMMAR "0.35",
  COURT "spike/v35/court_cases.json",
  EXTENSION ".panel"
) RATIONALE "What a person is doing on a surface, declared before it is drawn: flows of intents, forms that walk them, views of the world's entities, interactions with roles"

DEFINE MENU intents AS (
  WORDS [read, act, undo],
  MESSAGE "An intent is read, act or undo",
  CODE "UNKNOWN_INTENT"
) RATIONALE "Three verbs are enough to show a flow that has some and one that has none"

DEFINE MENU roles AS (
  WORDS [primary, secondary],
  MESSAGE "A role is primary or secondary",
  CODE "UNKNOWN_ROLE"
) RATIONALE "What an interaction is to the person: the act they came for, or one beside it"

DEFINE SYMBOL entity AS (
  KIND "entity",
  MESSAGE "WORLD_VIEW {name} shows the entity '{value}', and the world declares no entity:{value}",
  CODE "UNRESOLVED_ENTITY"
) RATIONALE "The entities a view shows are the host world's; a view never declares one"

DEFINE DECLARATION intent_flow AS (
  VERB "INTENT_FLOW",
  SEATS [satisfies: [intents]?]
) RATIONALE "The intents a surface serves, in the order a person meets them"

DEFINE DECLARATION form AS (
  VERB "FORM",
  SEATS [satisfies: [intents]?, intent_flow: intent_flow?, next: intent_flow?],
  MESSAGES [intent_flow: "FORM {name} walks the INTENT_FLOW '{value}', and no flow of that name is declared", next: "FORM {name} hands on to '{value}', and no flow of that name is declared"],
  CODES [intent_flow: "UNRESOLVED_INTENT_FLOW", next: "UNRESOLVED_NEXT"],
  SEVERITIES [intent_flow: warning]
) RATIONALE "A form walks a flow, which may be declared in another pillar (a warning when it is not here), and hands on to a flow that must be here (an error)"

DEFINE DECLARATION world_view AS (
  VERB "WORLD_VIEW",
  SEATS [shows: entity?, flows: [intent_flow]?],
  MESSAGES [flows: "WORLD_VIEW {name} lists the INTENT_FLOW '{value}', and no flow of that name is declared"],
  CODES [flows: "UNRESOLVED_FLOWS"],
  SEVERITIES [shows: warning]
) RATIONALE "A view shows an entity of the host world (a warning when the world lacks it) and lists flows of this sentence (an error when one is missing)"

DEFINE DECLARATION interaction AS (
  VERB "INTERACTION",
  SEATS [role: roles?]
) RATIONALE "One thing a person can do on the surface"

DEFINE CONSTRAINT no_satisfies AS (
  ON intent_flow, WHEN "satisfies absent or satisfies empty",
  MESSAGE "INTENT_FLOW {name} declares no intents",
  CODE "INTENT_FLOW_NO_SATISFIES",
  SEVERITY warning
) RATIONALE "A flow with no intents serves nobody; said, never refused (violations.json, level 2)"

DEFINE CONSTRAINT role_undeclared AS (
  ON interaction, WHEN "not (earlier interaction) and (all interaction where role absent)",
  MESSAGE "the surface declares interactions and gives none of them a role",
  CODE "ROLE_UNDECLARED",
  SEVERITY warning
) RATIONALE "Said once for the sentence, on its first interaction: the counter-check of an expression without intent, reported and never refusing"

DEFINE REFUSAL unknown_declaration AS (
  MESSAGE "The kinds are INTENT_FLOW, FORM, WORLD_VIEW and INTERACTION.",
  NAMED [widget: "WIDGET names a rendering, and a declaration that needs to say card has stopped describing intent", user: "USER is not a kind this language defines", gadget: "GADGET was retired: say what the person does, with an INTERACTION"],
  CODES [widget: "UNSPECIFIED_DECLARATION", user: "UNSPECIFIED_DECLARATION", gadget: "RETIRED_KIND"],
  SEVERITIES [widget: warning, user: warning],
  CITES ["article:intent"]
) RATIONALE "WIDGET and USER are kinds another implementation reads, so they are said and read past; GADGET was this language's and is refused"
'''
wr(os.path.join(SPIKE, 'panel_v35.haro'), PANEL)
twin = '\n'.join(l for l in PANEL.split('\n') if not l.strip().startswith('SEVERITIES ['))
twin = twin.replace('CODES [intent_flow: "UNRESOLVED_INTENT_FLOW", next: "UNRESOLVED_NEXT"],', 'CODES [intent_flow: "UNRESOLVED_INTENT_FLOW", next: "UNRESOLVED_NEXT"]')
twin = twin.replace('CODES [flows: "UNRESOLVED_FLOWS"],', 'CODES [flows: "UNRESOLVED_FLOWS"]')
twin = twin.replace('-- panel_v35.haro -- a small', '-- panel_errors.haro -- THE TWIN: panel_v35.haro with every SEVERITIES line removed, so every warning there is the refusal it was. Generated by\n-- v35/gen_fixtures.py; never edited by hand.\n-- panel_v35.haro -- a small')
wr(os.path.join(HERE, 'panel_errors.haro'), twin)

# ---- the sentences -------------------------------------------------------------------------------------------------------------------------------
S = {
    'clean': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW browse, NEXT browse) RATIONALE "x"\n'
             'DEFINE WORLD_VIEW members AS (SHOWS member, FLOWS [browse]) RATIONALE "x"\nDEFINE INTERACTION go AS (ROLE primary) RATIONALE "x"\n',
    'flow_elsewhere': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW checkout, NEXT browse) RATIONALE "x"\n',
    'next_missing': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW browse, NEXT checkout) RATIONALE "x"\n',
    'both_missing': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW checkout, NEXT payment) RATIONALE "x"\n',
    'two_forms': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW checkout) RATIONALE "x"\n'
                 'DEFINE FORM pay AS (INTENT_FLOW payment) RATIONALE "x"\n',
    'flows_missing': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE WORLD_VIEW members AS (SHOWS member, FLOWS [browse, checkout]) RATIONALE "x"\n',
    'entity_missing': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE WORLD_VIEW members AS (SHOWS ghost, FLOWS [browse]) RATIONALE "x"\n',
    'widget': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE WIDGET card AS (TITLE "a card", ITEMS [a, b, (c)]) RATIONALE "x"\n'
              'DEFINE INTERACTION go AS (ROLE primary) RATIONALE "x"\n',
    'widget_user': 'DEFINE WIDGET card AS () RATIONALE "x"\nDEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE USER ana AS (NAME "Ana") RATIONALE "x"\n',
    'gadget': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE GADGET knob AS () RATIONALE "x"\n',
    'widget_referenced': 'DEFINE WIDGET checkout AS () RATIONALE "x"\nDEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW browse, NEXT checkout) RATIONALE "x"\n',
    'widget_unclosed': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE WIDGET card AS (TITLE "a card" RATIONALE "x"\n',
    'widget_no_rationale': 'DEFINE INTENT_FLOW browse AS (SATISFIES [read]) RATIONALE "x"\nDEFINE WIDGET card AS ()\nDEFINE INTERACTION go AS (ROLE primary) RATIONALE "x"\n',
    'only_widget': 'DEFINE WIDGET card AS () RATIONALE "x"\n',
    'no_satisfies': 'DEFINE INTENT_FLOW browse AS () RATIONALE "x"\nDEFINE INTENT_FLOW idle AS (SATISFIES []) RATIONALE "x"\nDEFINE INTENT_FLOW work AS (SATISFIES [act]) RATIONALE "x"\n',
    'no_roles': 'DEFINE INTERACTION a AS () RATIONALE "x"\nDEFINE INTERACTION b AS () RATIONALE "x"\nDEFINE INTERACTION c AS () RATIONALE "x"\n',
    'one_role': 'DEFINE INTERACTION a AS () RATIONALE "x"\nDEFINE INTERACTION b AS (ROLE secondary) RATIONALE "x"\n',
    'all_five': 'DEFINE INTENT_FLOW idle AS () RATIONALE "x"\nDEFINE FORM search AS (INTENT_FLOW checkout, NEXT idle) RATIONALE "x"\n'
                'DEFINE WORLD_VIEW members AS (SHOWS ghost, FLOWS [idle]) RATIONALE "x"\nDEFINE WIDGET card AS () RATIONALE "x"\nDEFINE INTERACTION go AS () RATIONALE "x"\n',
    'wrong_role': 'DEFINE INTERACTION a AS (ROLE loud) RATIONALE "x"\n',
}
for k, v in S.items():
    wr(os.path.join(SPIKE, 'panel', k + '.panel'), v)
wr(os.path.join(SPIKE, 'panel', 'world.json'), json.dumps({'symbols': [{'kind': 'entity', 'name': 'member'}]}, indent=1) + '\n')

# ---- the cases ------------------------------------------------------------------------------------------------------------------------------------
W = 'panel/world.json'


def case(id_, name, file_, verb='check', world=True, first='ok', contains=(), lacks=(), counts=None, diagnose=None, twin=None):
    c = {'id': id_, 'name': name, 'verb': verb, 'args': ['panel/' + file_ + '.panel'] + ([W] if world else [])}
    if first is not None:
        c['first'] = first
    if contains:
        c['contains'] = list(contains)
    if lacks:
        c['lacks'] = list(lacks)
    if counts:
        c['counts'] = counts
    if diagnose:
        c['diagnose'] = diagnose
    if twin is not None:
        c['twin'] = twin
    return c


UIF = "warning UNRESOLVED_INTENT_FLOW: FORM search walks the INTENT_FLOW 'checkout', and no flow of that name is declared (line 2)"
cases = [
    case('P1', 'a clean sentence: no warning at all', 'clean', lacks=['warning']),
    # the per-seat severity, on a reference to a declaration
    case('P2', 'a FORM walks a flow declared elsewhere: ok, and the warning in the seat\'s own MESSAGES and CODES', 'flow_elsewhere', contains=[UIF], twin='UNRESOLVED_INTENT_FLOW'),
    case('P3', 'the seat beside it is not held: a missing NEXT is refused as it always was', 'next_missing', first="panel (line 2): FORM search hands on to 'checkout', and no flow of that name is declared"),
    case('P4', 'both: the error refuses, and a refused sentence speaks no warning', 'both_missing', first="panel (line 2): FORM search hands on to 'payment'", lacks=['warning']),
    case('P5', 'two forms, two warnings, in the order of the sentence', 'two_forms',
         contains=["warning UNRESOLVED_INTENT_FLOW: FORM search walks the INTENT_FLOW 'checkout'", "warning UNRESOLVED_INTENT_FLOW: FORM pay walks the INTENT_FLOW 'payment'"]),
    case('P6', 'a list seat not held: refused by its first missing element', 'flows_missing', first="panel (line 2): WORLD_VIEW members lists the INTENT_FLOW 'checkout'"),
    case('P7', 'the warning in the envelope: severity warning, the seat\'s code, cited as the code it would have refused with', 'flow_elsewhere', verb='diagnose', first=None,
         diagnose={'code': 'UNRESOLVED_INTENT_FLOW', 'severity': 'warning', 'line': 2}),
    # the per-seat severity, on a SYMBOL against a world
    case('P8', 'a view shows an entity the world lacks: ok, and the warning in the SYMBOL\'s words and code', 'entity_missing',
         contains=["warning UNRESOLVED_ENTITY: WORLD_VIEW members shows the entity 'ghost', and the world declares no entity:ghost (line 2)"], twin='UNRESOLVED_ENTITY'),
    case('P9', 'without a world the entity is NO_WORLD, as before: not resolved, so not a warning of its own', 'entity_missing', world=False,
         contains=['warning NO_WORLD'], lacks=['UNRESOLVED_ENTITY']),
    case('P10', 'the entity the world has: clean', 'clean', contains=['ok'], lacks=['warning']),
    # the NAMED kind held at warning
    case('P11', 'WIDGET is read past and said: ok, counted nowhere, the warning in the NAMED words and code', 'widget',
         contains=['warning UNSPECIFIED_DECLARATION: WIDGET names a rendering, and a declaration that needs to say card has stopped describing intent (line 2)'],
         counts={'INTENT_FLOW': 1, 'INTERACTION': 1}, twin='UNSPECIFIED_DECLARATION'),
    case('P12', 'WIDGET and USER, each said, in order; what follows a skipped kind is read', 'widget_user',
         contains=['warning UNSPECIFIED_DECLARATION: WIDGET names a rendering', 'warning UNSPECIFIED_DECLARATION: USER is not a kind this language defines (line 3)'], counts={'INTENT_FLOW': 1}),
    case('P13', 'GADGET is NAMED and not held: refused, as it always was', 'gadget', first='panel (line 2): GADGET was retired'),
    case('P14', 'a kind read past is not declared: a reference to it dangles', 'widget_referenced', first="panel (line 3): FORM search hands on to 'checkout', and no flow of that name is declared"),
    case('P15', 'what is read past must still be a declaration: an unclosed body is refused', 'widget_unclosed', first='panel (line 2)', lacks=['warning']),
    case('P16', 'and it carries its RATIONALE', 'widget_no_rationale', first='panel (line 3)', lacks=['warning UNSPECIFIED']),
    case('P17', 'a sentence of nothing but a kind read past declares nothing', 'only_widget', first='panel (line 1)'),
    case('P18', 'the NAMED warning in the envelope, with the refusal\'s cites', 'widget', verb='diagnose', first=None,
         diagnose={'code': 'UNSPECIFIED_DECLARATION', 'severity': 'warning', 'line': 2, 'cites': ['article:intent']}),
    # the two that were already expressible (v0.25)
    case('P19', 'INTENT_FLOW_NO_SATISFIES: absent and empty each said, the flow with intents not', 'no_satisfies',
         contains=['warning INTENT_FLOW_NO_SATISFIES: INTENT_FLOW browse declares no intents (line 1)', 'warning INTENT_FLOW_NO_SATISFIES: INTENT_FLOW idle declares no intents (line 2)'],
         lacks=['INTENT_FLOW work']),
    case('P20', 'ROLE_UNDECLARED: said once, on the first interaction', 'no_roles', contains=['warning ROLE_UNDECLARED: the surface declares interactions and gives none of them a role (line 1)'],
         lacks=['(line 2)', '(line 3)']),
    case('P21', 'one role is enough', 'one_role', lacks=['warning']),
    case('P22', 'all five in one sentence, and one error-free verdict', 'all_five',
         contains=['ok', 'warning UNSPECIFIED_DECLARATION', 'warning INTENT_FLOW_NO_SATISFIES', 'warning ROLE_UNDECLARED', 'warning UNRESOLVED_INTENT_FLOW', 'warning UNRESOLVED_ENTITY']),
    case('P23', 'a wrong word in a seat is never a warning', 'wrong_role', first='panel (line 1)', lacks=['warning']),
]
wr(os.path.join(HERE, 'court_cases.json'), json.dumps({
    'grammar': 'panel', 'version': '0.35',
    'comment': ('Written BEFORE any code reads SEVERITIES. Each case runs the court forged from panel_v35.haro on a sentence of panel/ (with panel/world.json unless world is false). '
                'first: a fragment of the first line; contains / lacks: fragments of the whole output; counts: the verdict\'s counts per verb; diagnose: the first warning of the '
                'envelope. twin: the code of a warning the TWIN (v35/panel_errors.haro, the same language without SEVERITIES) must refuse with, in exactly the words the warning carries.'),
    'cases': cases}, indent=1, ensure_ascii=False) + '\n')
print(f'{len(accepts)} accepts, {len(rejects)} rejects; {len(cases)} cases over {len(S)} sentences; panel_v35.haro and its twin')
