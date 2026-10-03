"""mk_meta_fixtures.py -- the fixtures of the meta-clause UNDERSTAND (rung 17), in the format of v16/fixtures.json.

The letter they stand on is n_v17.haro, the real one: an accept is the letter itself (and the letter with its
UNDERSTAND taken away, which must be exactly as before), a reject is the letter with one defect made by one
anchored replacement. Each reject's `refusal` fragment is composed here, by hand, from what the rule must say --
the meta-court's own answer is read AFTER, and a fragment that is not in it is a defect of the rule or of the
fragment, never adjusted to fit.

    python haro/spike/v17/mk_meta_fixtures.py          writes v17/meta_fixtures.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LETTER = open(os.path.join(os.path.dirname(HERE), 'n_v17.haro'), encoding='utf-8', newline='').read()
assert '\r\n' not in LETTER

UND = LETTER[LETTER.index('DEFINE UNDERSTAND n AS ('):]
assert UND.count('DEFINE UNDERSTAND') == 1


def mutate(old, new, src=LETTER):
    assert src.count(old) == 1, (old[:60], src.count(old))
    return src.replace(old, new)


accepts = [
    {'id': 'A1', 'name': 'the N letter itself: UNDERSTAND names the eight declarations that play the eight roles',
     'source': LETTER, 'expect': {'language': 'n', 'understands': 1, 'declarations': 8}},
    {'id': 'A2', 'name': 'the letter without its UNDERSTAND is exactly what it was at v0.16: a letter that checks and cannot understand',
     'source': LETTER.replace(UND, ''), 'expect': {'language': 'n', 'understands': 0, 'declarations': 8}},
    {'id': 'A3', 'name': 'the roles in another order and on other lines are the same UNDERSTAND (a role is named by its clause, never by its place)',
     'source': mutate('''  TONGUE [tongue], MEANING [meaning], ALIAS [alias], SURFACE [surface],
  STEP [step], FRAME [frame], EXAMPLE [example], COUNTEREXAMPLE [counterexample]''',
                      '''  COUNTEREXAMPLE [counterexample], EXAMPLE [example],
  FRAME [frame], STEP [step],
  SURFACE [surface], ALIAS [alias], MEANING [meaning], TONGUE [tongue]'''),
     'expect': {'language': 'n', 'understands': 1}},
]

rejects = [
    {'id': 'R1', 'name': 'a role is left out: an emitted court that does not know what an example is cannot judge one',
     'source': mutate(''',
  STEP [step], FRAME [frame], EXAMPLE [example], COUNTEREXAMPLE [counterexample]''', ''',
  STEP [step], FRAME [frame], EXAMPLE [example]'''),
     'refusal': 'UNDERSTAND requires the COUNTEREXAMPLE clause'},
    {'id': 'R2', 'name': 'a role names two declarations: a role is played by one',
     'source': mutate('TONGUE [tongue],', 'TONGUE [tongue, meaning],'),
     'refusal': 'TONGUE names the one DECLARATION that plays it -- 2 name(s) given'},
    {'id': 'R3', 'name': 'a role names a kind this language never declares',
     'source': mutate('STEP [step]', 'STEP [stepp]'),
     'refusal': "STEP: 'stepp' resolves to nothing in this declaration"},
    {'id': 'R4', 'name': 'a role names a MENU: a menu is words, not a kind a sentence declares',
     'source': mutate('SURFACE [surface]', 'SURFACE [slots]'),
     'refusal': "SURFACE must name a DECLARATION; 'slots' is a MENU"},
    {'id': 'R5', 'name': 'two roles name one declaration: a declaration plays one role',
     'source': mutate('ALIAS [alias]', 'ALIAS [meaning]'),
     'refusal': "ALIAS and MEANING name the same declaration 'meaning'"},
    {'id': 'R6', 'name': 'the kind that plays TONGUE has no JOINS seat: the emitted court reads it to join several names in an answer',
     'source': mutate('names: spellings?, joins: text?, refuses', 'names: spellings?, refuses'),
     'refusal': "TONGUE: no seat 'joins' on tongue"},
    {'id': 'R7', 'name': 'the kind that plays FRAME has no EMPTY seat: a plan that binds nothing could not say so',
     'source': mutate('answers: [in_tongue]?, empty: [in_tongue]?]', 'answers: [in_tongue]?]'),
     'refusal': "FRAME: no seat 'empty' on frame"},
    {'id': 'R8', 'name': 'a language is understood one way: a second UNDERSTAND is refused',
     'source': LETTER + '\n' + UND.replace('DEFINE UNDERSTAND n AS', 'DEFINE UNDERSTAND m AS'),
     'refusal': 'a .haro file declares at most one UNDERSTAND'},
    {'id': 'R9', 'name': 'a clause of UNDERSTAND that is not a role: nothing is understood beyond the eight roles',
     'source': mutate('COUNTEREXAMPLE [counterexample]\n)', 'COUNTEREXAMPLE [counterexample],\n  PLAN [frame]\n)'),
     'refusal': "Unknown clause 'PLAN' in UNDERSTAND"},
]

doc = {'grammar': 'haro', 'version': '0.17',
       'comment': 'v0.17: UNDERSTAND -- the one meta-clause the dynamic half of N needs (v17/GRAMMAR.md section 8). '
                  'Built by mk_meta_fixtures.py on the real letter, n_v17.haro; every reject is one anchored defect.',
       'accepts': accepts, 'rejects': rejects}
open(os.path.join(HERE, 'meta_fixtures.json'), 'w', encoding='utf-8', newline='').write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
print('meta_fixtures.json:', len(accepts), 'accepts,', len(rejects), 'rejects')
