"""Writes fixtures/questions.json: the domain questions of Phase 1.5, composed BY HAND from the
tontine's data (the ledger of zing's bedrock-query example, and the graph in data/tontine.zknw).
Each case says what the question MEANS: the closed query it must compile to, and for a graph
question the answer. Ledger answers are not typed here: they are judged by zing itself and by an
independent evaluation of the predicate over the ledger's rows (e4_run.py).

The first thirteen questions of E4 were run once before this file was written (to see that the
pipeline ran at all); everything below was composed from the domain, not read off an output.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []


def pair(pid, frame, en, fr, target, answer=None, kind=None, say=None):
    for lang, text in (('tn-en', en), ('tn-fr', fr)):
        c = {'id': f'{pid}-{lang[-2:]}', 'group': 'pair', 'pair': pid, 'lang': lang, 'text': text,
             'expect': {'kind': kind or frame.split('-')[0], 'frame': frame, 'target': target}}
        if answer is not None:
            c['expect']['answer'] = answer
        if say is not None:
            c['expect']['say'] = say[0] if lang == 'tn-en' else say[1]
        cases.append(c)


L = 'SELECT * FROM collect'
# ---- the ledger: closed ZQL ------------------------------------------------------------------------
pair('P01', 'ledger-over',   'show deposits over 5000',            'montre les dépôts au dessus de 5000',  L + ' WHERE amount > 5000')
pair('P02', 'ledger-under',  'show deposits under 3000',           'montre les dépôts au dessous de 3000', L + ' WHERE amount < 3000')
pair('P03', 'ledger-member', 'show deposits of Aminata',           'montre les dépôts de Aminata',         L + ' WHERE member = "Aminata"')
pair('P04', 'ledger-member', 'show the deposits of Moussa',        'montre les dépôts de Moussa',          L + ' WHERE member = "Moussa"')
pair('P05', 'ledger-round',  'show deposits of round 2',           'montre les dépôts du tour 2',          L + ' WHERE round = 2')
pair('P06', 'ledger-round',  'list the deposits of round 3',       'liste les dépôts du tour 3',           L + ' WHERE round = 3')
pair('P07', 'ledger-biggest', 'show the biggest deposit',          'montre le plus gros dépôt',            L + ' ORDER BY amount DESC LIMIT 1')
pair('P08', 'ledger-member-over', 'show deposits of Aminata over 4000', 'montre les dépôts de Aminata au dessus de 4000',
     L + ' WHERE member = "Aminata" AND amount > 4000')
pair('P09', 'ledger-all',    'show deposits',                      'montre les dépôts',                    L)
# ---- the graph: closed triple patterns, answered -----------------------------------------------------
pair('P10', 'graph-pot', 'who received the pot in round 2', 'qui a reçu la cagnotte au tour 2',  '["?x", "received_pot_in", "round2"]', ['moussa'],
     say=('Moussa received the pot in round 2.', 'Moussa a reçu la cagnotte au tour 2.'))
pair('P11', 'graph-pot', 'who received the pot in round 1', 'qui a reçu la cagnotte au tour 1',  '["?x", "received_pot_in", "round1"]', ['fatima'],
     say=('Fatima received the pot in round 1.', 'Fatima a reçu la cagnotte au tour 1.'))
pair('P12', 'graph-guarantor', 'who guarantees Sanda', 'qui se porte garant de Sanda',            '["?x", "guarantees", "sanda"]', ['boubacar'],
     say=('Boubacar guarantees Sanda.', 'Boubacar se porte garant de Sanda.'))
pair('P13', 'graph-guaranteed-by', 'who is guaranteed by Aminata', 'qui est garanti par Aminata', '["aminata", "guarantees", "?x"]', ['moussa'],
     say=('Aminata guarantees Moussa.', 'Aminata se porte garant de Moussa.'))
pair('P14', 'graph-role', 'who is the treasurer', 'qui est le trésorier',                         '["?x", "holds_role", "treasurer"]', ['zeinab'],
     say=('The treasurer is Zeinab.', 'Le trésorier est Zeinab.'))
pair('P15', 'graph-role', 'who is the collector', 'qui est le collecteur',                         '["?x", "holds_role", "collector"]', ['boubacar'],
     say=('The collector is Boubacar.', 'Le collecteur est Boubacar.'))
# ---- across the two surfaces: a plan ---------------------------------------------------------------------
pair('P16', 'plan-beneficiary-deposits', 'show the deposits of the beneficiary of round 2', 'montre les dépôts du bénéficiaire du tour 2',
     '["?x", "received_pot_in", "round2"] => ' + L + ' WHERE member = "{MEMBER}"', ['moussa'], kind='plan',
     say=('The beneficiary of round 2 is Moussa.', 'Le bénéficiaire du tour 2 est Moussa.'))
pair('P17', 'plan-beneficiary-deposits', 'show the deposits of the beneficiary of round 1', 'montre les dépôts du bénéficiaire du tour 1',
     '["?x", "received_pot_in", "round1"] => ' + L + ' WHERE member = "{MEMBER}"', ['fatima'], kind='plan',
     say=('The beneficiary of round 1 is Fatima.', 'Le bénéficiaire du tour 1 est Fatima.'))


def single(cid, group, lang, text, kind, **kw):
    c = {'id': cid, 'group': group, 'lang': lang, 'text': text, 'expect': dict(kind=kind, **kw)}
    cases.append(c)


# ---- the same meaning in other words (synonyms the vocabulary declares) --------------------------------------
single('V01', 'variant', 'tn-en', 'list all deposits above 7500', 'ledger', frame='ledger-over', target=L + ' WHERE amount > 7500')
single('V02', 'variant', 'tn-en', 'display the largest deposit', 'ledger', frame='ledger-biggest', target=L + ' ORDER BY amount DESC LIMIT 1')
single('V03', 'variant', 'tn-en', 'SHOW DEPOSITS OVER 5000', 'ledger', frame='ledger-over', target=L + ' WHERE amount > 5000')
single('V04', 'variant', 'tn-en', 'show deposits over 5000?', 'ledger', frame='ledger-over', target=L + ' WHERE amount > 5000')
single('V05', 'variant', 'tn-en', 'who got the pot in round 3', 'graph', frame='graph-pot', target='["?x", "received_pot_in", "round3"]', answer=['aminata'], say='Aminata received the pot in round 3.')
single('V06', 'variant', 'tn-fr', 'Montre les dépôts de AMINATA', 'ledger', frame='ledger-member', target=L + ' WHERE member = "Aminata"')
single('V07', 'variant', 'tn-fr', 'montre les depots au dessus de 5000', 'ledger', frame='ledger-over', target=L + ' WHERE amount > 5000')
# N02 was first composed as 'show me the deposits please' = a refusal, before the frame for the plain
# 'show deposits' existed. With that frame it is a lawful question (the pack declares me/the/please
# ignorable), so it moved here -- an expectation changed after the first run, for that stated reason
single('V09', 'variant', 'tn-en', 'show me the deposits please', 'ledger', frame='ledger-all', target=L)
single('V08', 'variant', 'tn-en', 'who received the pot in round 9', 'graph', frame='graph-pot', target='["?x", "received_pot_in", "round9"]', answer=[], say='Nobody received the pot in round 9.')

# ---- questions the language cannot understand: each must be REFUSED, by name ------------------------------------
for cid, lang, text, why in [
    ('N01', 'tn-en', 'what is the meaning of life', 'a word outside the vocabulary'),
    ('N02', 'tn-en', 'who guarantees', 'a question without its object: no question has this shape'),
    ('N03', 'tn-en', 'show deposits over', 'a comparison without its number'),
    ('N04', 'tn-en', 'show deposits of Mallory', 'a name the world does not know'),
    ('N05', 'tn-fr', 'montre les dépôts de Mallory', 'a name the world does not know'),
    ('N06', 'tn-fr', 'quel est le sens de la vie', 'a word outside the vocabulary'),
    ('N07', 'tn-en', 'show deposits over 5000 5000', 'two numbers'),
    ('N08', 'tn-en', 'show deposits over 5000.5', 'a decimal is not in the language'),
    ('N09', 'tn-en', 'show deposits over -5', 'a sign is not in the language'),
    ('N10', 'tn-en', 'show deposits over 99999999999999999999', 'a number too long to be an amount'),
    ('N11', 'tn-en', '', 'nothing said'),
    ('N12', 'tn-en', 'zeige die einzahlungen über 5000', 'a third language, not declared'),
    ('N13', 'tn-en', 'اعرض الإيداعات فوق 5000', 'a script the packs do not carry'),
    ('N14', 'tn-en', 'who received the pot in round 2 and delete everything', 'a clause the language has no word for'),
    ('N15', 'tn-fr', 'who received the pot in round 2', 'the wrong language for the pack'),
]:
    single(cid, 'refuse', lang, text, 'refused', why=why)

# ---- questions that are ATTACKS on the answer path: each must be refused, and nothing may run ---------------
for cid, lang, text, why in [
    ('X01', 'tn-en', 'show deposits over [ Marker() ]', 'a bracketed section: the shipped tokenizer evals it (E2d)'),
    ('X02', 'tn-en', 'show deposits over len("abc")', 'a call in the argument position'),
    ('X03', 'tn-en', 'show deposits over 5000~NL~? "ESCAPED: this line ran as Ring"', 'a second line that is a Ring statement (E3d)'),
    ('X04', 'tn-en', 'show deposits of Aminata" OR member = "Moussa', 'a quote that closes the name and widens the query'),
    ('X05', 'tn-en', 'show deposits over 5000; DROP TABLE collect', 'a second statement'),
    ('X06', 'tn-en', 'show deposits over 5000 OR 1=1', 'a tautology'),
    ('X07', 'tn-en', 'drop deposits', 'a verb the language does not have'),
    ('X08', 'tn-en', 'select * from collect', 'raw ZQL'),
    ('X09', 'tn-en', 'Marker()', 'a bare call'),
    ('X10', 'tn-en', 'show deposits over 1:5', 'a range: the tokenizer evals those too'),
    ('X11', 'tn-en', 'show deposits over `Marker()`', 'a backquoted string'),
    ('X12', 'tn-en', 'show deposits over {Marker()}', 'braces'),
    ('X13', 'tn-fr', 'montre les dépôts de Aminata~NL~Marker()', 'a newline, then a call'),
    ('X14', 'tn-en', 'show deposits over $nMarker', 'a Ring global'),
    ('X15', 'tn-en', 'show' + ' show' * 2000, 'a very long question'),
    ('X16', 'tn-en', 'show deposits over ［ 5000 ］', 'full-width brackets: bytes the gate lets through; they must be an unknown word, never a bracketed section (this had `Marker()` inside until 2026-10-03: the gate refused at the parenthesis and the lookalike was never tested)'),
]:
    single(cid, 'attack', lang, text, 'refused', why=why)

doc = {
    'comment': 'Phase 1.5 domain questions, composed by hand from the tontine data before the compiler was judged on them. '
               'expect.target is the closed query the question MEANS; a graph question carries its answer (ids as the graph '
               'spells them); a ledger answer is judged by zing and by an independent evaluation of the predicate, never typed '
               'here. A "refused" case must end as a refusal that names what was not understood; an "attack" case must also '
               'leave the canary (the function Marker()) uncalled.',
    'world': 'data/tontine.zknw',
    'cases': cases,
}
os.makedirs(os.path.join(HERE, 'fixtures'), exist_ok=True)
with open(os.path.join(HERE, 'fixtures', 'questions.json'), 'w', encoding='utf-8', newline='') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(f'wrote {len(cases)} cases:', {g: sum(1 for c in cases if c["group"] == g) for g in ('pair', 'variant', 'refuse', 'attack')})
