"""Haro v0.40 -- D51's declared half: a language declares the doors its worlds may open. Fixtures first.

Writes, BEFORE any code reads NEEDS or OPENS: fixtures.json (the meta-court's), door_v40.haro (a language that NEEDS two doors, one kind opening a
door by name and one opening what its seat lists), the sentences under door/, and court_cases.json (the forged court's).

WHAT D51 DECIDED (CHARTER.md D51, stzlib-security's HARO-ONEHOUR-01, A6 of SOFTANZA_ONE_HOUR.md). The words are the closed catalog of nine that
Harobanda's machine file and stzlib's stzSystemCapabilities already use: filesystem, process, network, environment, dynamic_load, gpio, threads,
clock, inference.

  D1  NEEDS [capability, ...] on DEFINE LANGUAGE names every door any world of the language may open: words of the nine, each once
  D2  OPENS on a DECLARATION: a capability (the kind's declarations open that door), or a seat of the kind whose type is a MENU of capabilities
      (each declaration opens what that seat lists)
  D3  the meta-court refuses a kind that OPENS a capability the LANGUAGE does not NEED -- A6's gate: "a world in a language without network
      cannot parse a listener", for the language is refused and its grammar is never forged -- and refuses a NEEDS word no kind opens (least
      authority: Harobanda's "declared AND granted"); a word of an OPENS seat's MENU counts as opened
  D4  silence refuses: a kind that OPENS in a language that NEEDS nothing is refused; a language with neither is exactly what it was
  D5  the forged court refuses a sentence whose OPENS seat lists a capability the language does not NEED (CAPABILITY_NOT_NEEDED)
  D6  enforcement is the consumer's: the court publishes each declaration's opened capabilities with its world rows, for Harobanda's PID 1

Measured on haro 212a99e before this rung: NEEDS on a LANGUAGE and OPENS on a DECLARATION are each refused as an unknown clause.

The desk's readings, written here before the code: OPENS takes ONE word (a kind that opens two doors is two kinds, or a seat); a word that is
both a capability and a seat of the kind is read as the capability; an OPENS seat's MENU may list a capability the language does not NEED -- the
sentence that uses it is refused (D5), so a MENU can be shared by languages that need different doors; the meta verdict prints `needs` and
`opens` only for a language that NEEDS, so every other verdict keeps its bytes; a declaration of an OPENS seat kind that lists nothing opens
nothing, and its world row says so (opens []).

  python spike/v40/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
NINE = 'filesystem, process, network, environment, dynamic_load, gpio, threads, clock, inference'


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(s)


def lang(needs='NEEDS [network, process]', kinds=None):
    head = 'DEFINE LANGUAGE q AS (VERSION "0.40", GRAMMAR "0.40", COURT "x", EXTENSION ".q"' + (', ' + needs if needs else '') + ') RATIONALE "x"\n'
    menu = 'DEFINE MENU caps AS (WORDS [network, process, filesystem], MESSAGE "a capability") RATIONALE "x"\n'
    if kinds is None:
        kinds = ['DEFINE DECLARATION listener AS (VERB "LISTENER", SEATS [host: text?], OPENS network) RATIONALE "x"',
                 'DEFINE DECLARATION service AS (VERB "SERVICE", SEATS [host: text?, needs: [caps]?], OPENS needs) RATIONALE "x"']
    return head + menu + '\n'.join(kinds) + '\n'


L_OPENS_NET = 'DEFINE DECLARATION listener AS (VERB "LISTENER", SEATS [host: text?], OPENS network) RATIONALE "x"'
L_OPENS_SEAT = 'DEFINE DECLARATION service AS (VERB "SERVICE", SEATS [host: text?, needs: [caps]?], OPENS needs) RATIONALE "x"'
L_PLAIN = 'DEFINE DECLARATION note AS (VERB "NOTE", SEATS [text: text?]) RATIONALE "x"'

ACCEPTS = [
    ('A1', 'NEEDS two doors: a kind opens one by name, a kind opens what its seat lists', lang(),
     {'language': 'q', 'needs': 'network,process', 'opens': 'LISTENER:network,SERVICE:needs', 'counts': {'declarations': 2}}),
    ('A2', 'a language with neither NEEDS nor OPENS is what it was', lang(needs='', kinds=[L_PLAIN]),
     {'language': 'q', 'counts': {'declarations': 1}, 'verbs': ['NOTE']}),
    ('A3', 'an OPENS seat\'s MENU may list a door the language does not NEED (the sentence that uses it is refused)', lang(needs='NEEDS [network]', kinds=[L_OPENS_SEAT]),
     {'language': 'q', 'needs': 'network', 'opens': 'SERVICE:needs'}),
    ('A4', 'a kind beside them that opens nothing', lang(kinds=[L_OPENS_NET, L_OPENS_SEAT, L_PLAIN]),
     {'language': 'q', 'needs': 'network,process', 'opens': 'LISTENER:network,SERVICE:needs', 'counts': {'declarations': 3}}),
]

REJECTS = [
    ('R1', 'NEEDS a word outside the nine', lang(needs='NEEDS [network, internet]'),
     f"NEEDS: 'internet' is not a capability; the nine are {NINE}"),
    ('R2', 'NEEDS a word twice', lang(needs='NEEDS [network, process, network]'),
     "NEEDS: 'network' is named twice"),
    ('R3', 'A6\'s gate: a listener in a language without network', lang(needs='NEEDS [process]', kinds=[L_OPENS_NET, L_OPENS_SEAT]),
     'listener OPENS network, and the LANGUAGE q does not NEED it'),
    ('R4', 'silence refuses: a kind OPENS and the language NEEDS nothing', lang(needs='', kinds=[L_OPENS_NET]),
     'listener OPENS network, and the LANGUAGE q NEEDS nothing'),
    ('R5', 'least authority: a NEEDS word no kind opens', lang(needs='NEEDS [network, process, gpio]'),
     'NEEDS gpio, and no kind OPENS it'),
    ('R6', 'OPENS names neither a capability nor a seat of the kind', lang(kinds=[L_OPENS_NET, L_OPENS_SEAT.replace('OPENS needs', 'OPENS ghost')]),
     "OPENS: 'ghost' is neither a capability nor a seat of service"),
    ('R7', 'OPENS a seat that is not a MENU', lang(needs='NEEDS [network]', kinds=[L_OPENS_SEAT.replace('OPENS needs', 'OPENS host')]),
     "OPENS: the seat 'host' of service is not a MENU of capabilities"),
    ('R8', 'OPENS a seat whose MENU holds a word outside the nine', lang().replace('WORDS [network, process, filesystem]', 'WORDS [network, process, internet]'),
     "OPENS: the seat 'needs' of service is a MENU holding 'internet', which is not a capability"),
    ('R9', 'NEEDS on a kind is not a clause: a door is the language\'s to need', lang(kinds=[L_OPENS_NET.replace('OPENS network', 'NEEDS [network]'), L_OPENS_SEAT]),
     "Unknown clause 'NEEDS' in DECLARATION"),
]

doc = {'grammar': 'haro', 'version': '0.40',
       'comment': 'Written BEFORE any code reads NEEDS or OPENS (the W discipline). v0.40 is D51\'s declared half: NEEDS on a LANGUAGE, OPENS on a '
                  'DECLARATION, the closed catalog of nine, A6\'s gate at the meta-court.',
       'accepts': [{'id': i, 'name': n, 'source': s, 'expect': e} for i, n, s, e in ACCEPTS],
       'rejects': [{'id': i, 'name': n, 'source': s, 'refusal': r} for i, n, s, r in REJECTS]}
wr(os.path.join(HERE, 'fixtures.json'), json.dumps(doc, indent=1) + '\n')

# ---- the forged court's language and sentences
wr(os.path.join(SPIKE, 'door_v40.haro'), '''-- door_v40.haro -- a small language that declares the doors its worlds may open (Haro v0.40, D51's declared half). Its LANGUAGE NEEDS two of
-- the nine; a LISTENER opens network by name; a SERVICE opens what its NEEDS seat lists, from a MENU that also holds filesystem, which the
-- language does not NEED -- a sentence that lists it is refused by the court; a NOTE opens nothing.

DEFINE LANGUAGE door AS (
  VERSION "0.40", GRAMMAR "0.40",
  COURT "spike/v40/court_cases.json",
  EXTENSION ".door",
  NEEDS [network, process]
) RATIONALE "What a small service asks of the machine it runs on, declared before it runs"

DEFINE MENU caps AS (
  WORDS [network, process, filesystem],
  MESSAGE "A capability is network, process or filesystem",
  CODE "UNKNOWN_CAPABILITY"
) RATIONALE "The doors a service may list; filesystem is here so a sentence can ask for a door the language does not need"

DEFINE DECLARATION listener AS (
  VERB "LISTENER",
  SEATS [host: text?],
  OPENS network
) RATIONALE "A listener opens the network, whatever it is told"

DEFINE DECLARATION service AS (
  VERB "SERVICE",
  SEATS [host: text?, needs: [caps]?],
  OPENS needs
) RATIONALE "A service opens what it lists, and nothing it does not"

DEFINE DECLARATION note AS (
  VERB "NOTE",
  SEATS [text: text?]
) RATIONALE "A note opens nothing"
''')
SENT = {
    'clean': ['DEFINE LISTENER web AS (HOST "localhost") RATIONALE "x"', 'DEFINE SERVICE api AS (NEEDS [network, process]) RATIONALE "x"',
              'DEFINE NOTE n AS (TEXT "x") RATIONALE "x"'],
    'files': ['DEFINE LISTENER web AS (HOST "localhost") RATIONALE "x"', 'DEFINE SERVICE api AS (NEEDS [network, filesystem]) RATIONALE "x"'],
    'gpio': ['DEFINE SERVICE api AS (NEEDS [gpio]) RATIONALE "x"'],
    'quiet': ['DEFINE SERVICE quiet AS (NEEDS []) RATIONALE "x"', 'DEFINE SERVICE bare AS (HOST "x") RATIONALE "x"'],
}
for k, lines in SENT.items():
    wr(os.path.join(SPIKE, 'door', k + '.door'), '\n'.join(lines) + '\n')

NOT_NEEDED = "door (line 2): SERVICE api opens 'filesystem', and the language door does not NEED it"
cases = [
    {'id': 'D1', 'name': 'a sentence that opens only what the language needs', 'verb': 'check', 'args': ['door/clean.door'], 'first': 'ok'},
    {'id': 'D2', 'name': 'a SERVICE that lists a door the language does not NEED is refused', 'verb': 'check', 'args': ['door/files.door'],
     'first': NOT_NEEDED},
    # D3 CHANGED after the court spoke: the stage's diagnose check requires `cites` (it reads code, cites and severity, not the line, which D2's
    # first line pins); the refusal cites nothing, the door being the language's own NEEDS.
    {'id': 'D3', 'name': 'the refusal in the envelope: its code, no cites, an error', 'verb': 'diagnose', 'args': ['door/files.door'],
     'diagnose': {'code': 'CAPABILITY_NOT_NEEDED', 'cites': [], 'severity': 'error', 'line': 2}},
    {'id': 'D4', 'name': 'a word outside the MENU is the MENU\'s refusal, as it always was', 'verb': 'check', 'args': ['door/gpio.door'],
     'first': 'A capability is network, process or filesystem'},
    {'id': 'D5', 'name': 'the world publishes what each declaration opens: a LISTENER its door, a SERVICE what it lists; a NOTE nothing',
     'verb': 'world', 'args': ['door/clean.door'],
     'contains': ['"opens": [{"verb": "LISTENER", "name": "web", "opens": ["network"], "span": {"file": "clean.door", "line": 1}}',
                  '{"verb": "SERVICE", "name": "api", "opens": ["network", "process"], "span": {"file": "clean.door", "line": 2}}]'],
     'lacks': ['"name": "n"']},
    {'id': 'D6', 'name': 'a SERVICE that lists nothing, or has no NEEDS seat, opens nothing, and its row says so', 'verb': 'world', 'args': ['door/quiet.door'],
     'contains': ['{"verb": "SERVICE", "name": "quiet", "opens": [], "span"', '{"verb": "SERVICE", "name": "bare", "opens": [], "span"']},
    {'id': 'D7', 'name': 'a world of a language that NEEDS nothing has no opens: every other court keeps its bytes', 'verb': 'world',
     'court': 'panel_court.haro', 'args': ['panel/clean.panel'], 'lacks': ['"opens"']},
]
wr(os.path.join(HERE, 'court_cases.json'), json.dumps({'grammar': 'haro', 'version': '0.40',
                                                       'comment': 'Written BEFORE any code reads NEEDS or OPENS. Each case runs the court forged from door_v40.haro (or, D7, panel_court.haro) on a sentence of door/.',
                                                       'cases': cases}, indent=1) + '\n')
print(f'wrote {len(ACCEPTS)} accepts, {len(REJECTS)} rejects, {len(cases)} court cases, {len(SENT)} sentences')
