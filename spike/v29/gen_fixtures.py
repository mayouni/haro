"""Haro v0.29 -- the weave fixtures, WRITTEN BEFORE THE COURT THAT PASSES THEM (WC1 of the weaves charge).

Run: python gen_fixtures.py   (writes fixtures.json beside it)

The rules judged are the ones ZIN-WEAVES-INVENTORY.md sorted 'THROUGH what exists' and that have a refusable shape without a
new seat -- W1.5, W2.2, W2.3, W5.2, W7.4, W8.5. W1.2 and W7.1 hold by construction (the gate writes the inverse before a change
lands; a declaration without a RATIONALE is refused whatever the weaves say) and are named as held, not judged. Each judged
rule is the condition of an article read at the WEAVE's severity: where the world stands under the article, the article's own
refusal comes first and is constitutional.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

LANG = 'DEFINE LANGUAGE clinic AS (VERSION "0.29", GRAMMAR "0.29", COURT "x", EXTENSION ".clinic") RATIONALE "x"\n'
KIND = 'DEFINE DECLARATION patient AS (VERB "PATIENT", SEATS [file_no: text, ward: text]) RATIONALE "x"\n'
VOICE = 'DEFINE NARRATE voice AS (SAYS [patient: "{name}, file {file_no}."]) RATIONALE "x"\n'
REFUSAL = 'DEFINE REFUSAL unknown_verb AS (MESSAGE "The verb set is closed", CODE "UNKNOWN_VERB") RATIONALE "x"\n'
REFUSAL_NOCODE = 'DEFINE REFUSAL unknown_verb AS (MESSAGE "The verb set is closed") RATIONALE "x"\n'
RULE = ('DEFINE CONSTRAINT one_file AS (ON patient, WHEN "earlier patient where file_no = this.file_no", MESSAGE "two patients share a file", '
        'CODE "ONE_FILE") RATIONALE "x"\n')
RULE_NOCODE = ('DEFINE CONSTRAINT one_file AS (ON patient, WHEN "earlier patient where file_no = this.file_no", '
               'MESSAGE "two patients share a file") RATIONALE "x"\n')


def rule_warning(cite):
    return ('DEFINE CONSTRAINT one_file AS (ON patient, WHEN "earlier patient where file_no = this.file_no", MESSAGE "two patients share a file", '
            'CODE "ONE_FILE", CITES ["%s"], SEVERITY warning) RATIONALE "x"\n' % cite)


def refine(ward='trusted', fileno='trusted', fileno_kind='policy'):
    return ('DEFINE REFINE clinic AS (POINTS [patient.ward: knob, patient.file_no: %s], FLOOR [patient.ward: %s, patient.file_no: %s]) '
            'RATIONALE "x"\n' % (fileno_kind, ward, fileno))


def charter(arts, weaves):
    return ('DEFINE CONSTITUTION charter AS (ARTICLES [%s], WEAVES [%s]) RATIONALE "x"\n' % (', '.join(arts), ', '.join(weaves)))


FIVE = ['resilience: constitutional', 'observability: constitutional', 'temporal_integrity: constitutional',
        'learnability: constitutional', 'structural_integrity: constitutional']

CARRIED_ALL_FIVE = ('W1.1,W1.3,W1.4,W1.6,W1.7,W2.1,W2.4,W2.5,W2.6,W5.1,W5.3,W5.4,W5.5,W7.2,W7.3,W7.5,W7.6,W8.1,W8.2,W8.3,W8.4')

v25 = json.load(open(os.path.join(HERE, '..', 'v25', 'fixtures.json'), encoding='utf-8'))
v25_a1 = [c for c in v25['accepts'] if c['id'] == 'A1'][0]

accepts = [
    {
        'id': 'A1',
        'name': 'the five weaves the court now judges, all constitutional, in a world that satisfies each: a chain, a voice with codes, a gate whose policy points are no model\'s',
        'source': (LANG + KIND + VOICE + REFUSAL + RULE + refine(ward='llm') + charter(
            ['explainability', 'visible_state', 'predictable_authority'], FIVE)),
        'expect': {'language': 'clinic', 'weaves': ','.join(w.replace(': ', ':') for w in FIVE),
                   'judged': 'W1.5,W2.2,W2.3,W5.2,W7.4,W8.5', 'held': 'W1.2,W7.1', 'carried': CARRIED_ALL_FIVE},
    },
    {
        'id': 'A2',
        'name': 'nothing to trace: a world with no REFINE names observability and temporal_integrity at constitutional and is accepted -- a rule judged finds nothing without a gate',
        'source': (LANG + KIND + VOICE + charter(['explainability'], ['observability: constitutional', 'temporal_integrity: constitutional'])),
        'expect': {'language': 'clinic', 'weaves': 'observability:constitutional,temporal_integrity:constitutional',
                   'judged': 'W2.2,W2.3,W5.2', 'held': '',
                   'carried': 'W2.1,W2.4,W2.5,W2.6,W5.1,W5.3,W5.4,W5.5'},
    },
    {
        'id': 'A3',
        'name': 'structural_integrity at governance: a policy point floored llm and no predictable_authority is accepted with a warning that names the rule, the point and the article',
        'source': (LANG + KIND + VOICE + refine(fileno='llm') + charter(['trust_hierarchy'], ['structural_integrity: governance'])),
        'expect': {'language': 'clinic', 'weaves': 'structural_integrity:governance', 'judged': 'W8.5', 'held': '',
                   'carried': 'W8.1,W8.2,W8.3,W8.4',
                   'warning': "W8.5 structural_integrity: policy point 'patient.file_no' has FLOOR llm -- a model-composed proposal could replace a rule the court proved [Art. 4 predictable_authority]"},
    },
    {
        'id': 'A4',
        'name': 'learnability at advisory: a CONSTRAINT with no CODE is accepted with a note that names the rule, the constraint and Art. 1',
        'source': (LANG + KIND + VOICE + RULE_NOCODE + charter(['visible_state'], ['learnability: advisory'])),
        'expect': {'language': 'clinic', 'weaves': 'learnability:advisory', 'judged': 'W7.4', 'held': 'W7.1',
                   'carried': 'W7.2,W7.3,W7.5,W7.6',
                   'note': "W7.4 learnability: CONSTRAINT 'one_file' carries no CODE -- a denial is explained to its reader by a stable identifier (C2 2.1) [Art. 1 explainability]"},
    },
    {
        'id': 'A5',
        'name': 'a degradation that cites a law the world does not stand under is no breach: a warning CONSTRAINT citing article:visible_state, in a world under trust_hierarchy alone, is accepted at constitutional',
        'source': (LANG + KIND + VOICE + rule_warning('article:visible_state') + refine() + charter(['trust_hierarchy'], ['resilience: constitutional'])),
        'expect': {'language': 'clinic', 'weaves': 'resilience:constitutional', 'judged': 'W1.5', 'held': 'W1.2',
                   'carried': 'W1.1,W1.3,W1.4,W1.6,W1.7'},
    },
    {
        'id': 'A6',
        'name': 'v0.25\'s A1 unchanged: the clinic under all six articles and both original weaves is accepted as before, and prints none of the new lines',
        'source': v25_a1['source'],
        'expect': v25_a1['expect'],
    },
    {
        'id': 'A7',
        'name': 'W1.2 held by construction: a world that refines and stands under no article but the trust floor is accepted under resilience -- the gate writes the inverse before a change lands',
        'source': (LANG + KIND + refine() + charter(['trust_hierarchy'], ['resilience: constitutional'])),
        'expect': {'language': 'clinic', 'weaves': 'resilience:constitutional', 'judged': 'W1.5', 'held': 'W1.2',
                   'carried': 'W1.1,W1.3,W1.4,W1.6,W1.7'},
    },
]

rejects = [
    {
        'id': 'R1',
        'name': 'W1.5 resilience, constitutional: a CONSTRAINT held at warning that cites an article the world stands under is a degradation past a law -- refused with the rule, the constraint, the cite and the article',
        'source': (LANG + KIND + VOICE + rule_warning('article:3') + charter(['visible_state'], ['resilience: constitutional'])),
        'refusal': "W1.5 resilience: CONSTRAINT 'one_file' is SEVERITY warning and cites article:3, and the world stands under visible_state -- a degradation must not pass a law the world declares [Art. 3 visible_state]",
    },
    {
        'id': 'R2',
        'name': 'W2.2 observability, constitutional: a point a model may propose (FLOOR llm) and no visible_state -- no chain keeps the proposal or its refusal',
        'source': (LANG + KIND + refine(ward='llm') + charter(['trust_hierarchy'], ['observability: constitutional'])),
        'refusal': "W2.2 observability: point 'patient.ward' has FLOOR llm -- a model may propose it -- and visible_state is not among ARTICLES: no chain keeps the model's proposal or its refusal [Art. 3 visible_state]",
    },
    {
        'id': 'R3',
        'name': 'W2.3 observability, constitutional: a REFINE whose gate denies and no visible_state -- a denial enters no audit chain',
        'source': (LANG + KIND + refine() + charter(['trust_hierarchy'], ['observability: constitutional'])),
        'refusal': "W2.3 observability: 'clinic' declares a REFINE, whose gate denies, and visible_state is not among ARTICLES: a denial enters no audit chain [Art. 3 visible_state]",
    },
    {
        'id': 'R4',
        'name': 'W5.2 temporal_integrity, constitutional: a REFINE changes points that have a history and no visible_state numbers the changes',
        'source': (LANG + KIND + refine() + charter(['trust_hierarchy'], ['temporal_integrity: constitutional'])),
        'refusal': "W5.2 temporal_integrity: 'clinic' declares a REFINE, which changes points that have a history, and visible_state is not among ARTICLES: no numbered chain versions the changes [Art. 3 visible_state]",
    },
    {
        'id': 'R5',
        'name': 'W7.4 learnability, constitutional: a world that denies (a CONSTRAINT) and declares no NARRATE -- a denial no voice tells is not explained',
        'source': (LANG + KIND + RULE + charter(['trust_hierarchy'], ['learnability: constitutional'])),
        'refusal': "W7.4 learnability: 'clinic' declares 1 denial(s) (CONSTRAINT or REFUSAL) and no NARRATE -- a denial no voice tells is not explained [Art. 1 explainability]",
    },
    {
        'id': 'R6',
        'name': 'W7.4 learnability, constitutional: a REFUSAL with no CODE -- the stable identifier is how a reader meets a denial',
        'source': (LANG + KIND + VOICE + REFUSAL_NOCODE + charter(['visible_state'], ['learnability: constitutional'])),
        'refusal': "W7.4 learnability: REFUSAL 'unknown_verb' carries no CODE -- a denial is explained to its reader by a stable identifier (C2 2.1) [Art. 1 explainability]",
    },
    {
        'id': 'R7',
        'name': 'W8.5 structural_integrity, constitutional: a policy point a model may propose and no predictable_authority -- a synthesis could replace a rule the court proved',
        'source': (LANG + KIND + refine(fileno='llm') + charter(['trust_hierarchy'], ['structural_integrity: constitutional'])),
        'refusal': "W8.5 structural_integrity: policy point 'patient.file_no' has FLOOR llm -- a model-composed proposal could replace a rule the court proved [Art. 4 predictable_authority]",
    },
    {
        'id': 'R8',
        'name': 'where the article is declared its own refusal comes first, constitutional, and the weave does not say it twice: predictable_authority refuses the llm policy point before W8.5 can',
        'source': (LANG + KIND + refine(fileno='llm') + charter(['predictable_authority'], ['structural_integrity: governance'])),
        'refusal': "Art. 4 predictable_authority: policy point 'patient.file_no' has FLOOR llm",
    },
    {
        'id': 'R9',
        'name': 'cost_awareness is still refused by name: none of its 13 rules is judged, a budget needing a seat the world does not declare yet',
        'source': (LANG + KIND + VOICE + charter(['visible_state'], ['cost_awareness: constitutional'])),
        'refusal': "WEAVES names 'cost_awareness', and none of its 13 rules is judged in Haro v0.29 -- they are Zin's design, carried, not built",
    },
    {
        'id': 'R10',
        'name': 'W7.1 held by construction: a declaration with no RATIONALE is refused whatever the weaves say',
        'source': (LANG + 'DEFINE DECLARATION patient AS (VERB "PATIENT", SEATS [file_no: text])\n' + charter(['trust_hierarchy'], ['learnability: advisory'])),
        'refusal': 'carries its RATIONALE',
    },
]

doc = {
    'grammar': 'haro',
    'version': '0.29',
    'comment': ('The Haro v0.29 conformance floor, written BEFORE the court that passes it (the W discipline: fixtures first, prose second). '
                'v0.29 is WC1 of the second charge of the constitution desk (the six carried weaves, 2026-11-02): five of the six -- resilience '
                '(W1.5), observability (W2.2, W2.3), temporal_integrity (W5.2), learnability (W7.4) and structural_integrity (W8.5) -- are '
                'judged at the declaring altitude with no new seat, each rule an article\'s condition read at the weave\'s severity; W1.2 and '
                'W7.1 hold by construction; cost_awareness stays refused by name. The rules, their sort and the readings are in '
                'ZIN-WEAVES-INVENTORY.md; the account is GRAMMAR.md. A6 is v0.25\'s A1 unchanged: nothing v0.28 accepted is refused here but a '
                'weave name this rung now judges.'),
    'accepts': accepts,
    'rejects': rejects,
}

with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='') as fh:
    json.dump(doc, fh, indent=2, ensure_ascii=False)
    fh.write('\n')
print('fixtures.json:', len(accepts), 'accepts,', len(rejects), 'rejects')
