"""Haro v0.34 -- COMPASS-KERN-03's field check: a question is judged against the declared schema before it runs. Fixtures first.

Writes, BEFORE any code reads a FIELDS clause: fixtures.json (the meta-court's: what an ASK with FIELDS is accepted and refused for), q_cases.json (the forged court's `ask`
verb: questions on a sentence that declares its records' fields), z_v34.haro (the Q world with the link) and tontine/records.z (the tontine with it). The files it writes are
committed as they stand.

THE FINDING THIS RUNG STARTED FROM. The row (COMPASS-KERN-03, 2026-11-01) asks for "a court that judges a Q or zql query against the declared schema before it runs". This desk
answered on 2026-11-02 that the court's `ask` verb already refused an unknown FROM, a clause the ASK does not admit and a WHERE that computes, and that the missing half was "one
rung: resolve WHERE's names and ORDER BY's field against the FROM declaration's fields". Reading the Q world for the rung found there are NO fields to resolve against: FROM names a
FLOW, a flow has no seats, the fields live on an ENTITY, and nothing says which flow's records are which entity's. (The other flow, indice, has records no entity describes at all.)
The schema was never declared. So the rung is the link, then the check:

  records: entity?        a new optional seat on Z's flow: the ENTITY whose records walk it. Z's, not the language's: zing is schema-less at the query and its sentences never
                          wrote this; a flow that does not write it is not field-checked, and zing's reading stands (a missing field is missing)
  FIELDS seat.seat        a new clause of ASK, generic to any language that declares one: a seat of the kind asked (one reference to a DECLARATION), then a list of
                          name: type pairs of the declaration it refers to. `FIELDS records.fields`. The meta-court judges that both seats exist and have those shapes
  the names a question may use for a FROM declaration whose link is written: the keys of that list of pairs, and the names the flow's own steps COMPUTE (zing overlays a
                          computed value on the record by name, so a record of the flow has it). A name is the head of a dotted path: `member.first` names `member`
  a refusal               WHERE or ORDER BY names a field the declaration does not declare: refused before the question runs, naming the field, the declaration and the fields it has,
                          in the declaring language's own words (its unknown_seat refusal's message, when it declares one)

THE DIVERGENCE FROM ZING, NAMED. For a flow whose records are declared, zing answers a question that names an undeclared field with no rows (it reads a missing field as missing)
and Haro refuses. None of zing's 25 pinned questions names an undeclared field, so all 25 still hold; the new refusals are marked haro_only, as q20's is (HF-51). This is the point
of the Compass row (an error in the domain's words, where silence is a typo's best friend), and a decision for the author to refuse (D48 records it as the desk's, within the rung).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
rw = lambda p: open(p, encoding='utf-8', newline=None).read()


def wr(p, s):
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(s)


def sub(s, old, new):
    assert s.count(old) == 1, (old[:70], s.count(old))
    return s.replace(old, new)


# ---- z_v34.haro: Z with the link and the clause ----------------------------------------------------------------------------------------------
z = rw(os.path.join(SPIKE, 'z_v27.haro'))
z = sub(z, '-- z_v27.haro -- Z with the field tag (Haro v0.27, ZTAG): z_v26.haro plus a mark on the field form.',
        '-- z_v34.haro -- Z with the schema a question is checked against (Haro v0.34, COMPASS-KERN-03\'s field check): z_v27.haro plus `records: entity?` on the FLOW, which says\n'
        '-- whose records walk it, and `FIELDS records.fields` on the ASK, which makes a question that names a field the entity does not declare (or a step does not compute) a\n'
        '-- refusal, before it runs, in this language\'s words. A flow that writes no RECORDS is not checked, and zing\'s reading stands: a missing field is missing. zing\'s 16 cases\n'
        '-- and 25 questions are judged unchanged. v34/gen_fixtures.py states the finding and the divergence.\n--\n'
        '-- z_v27.haro -- Z with the field tag (Haro v0.27, ZTAG): z_v26.haro plus a mark on the field form.')
z = sub(z, '  VERSION "0.27",\n  GRAMMAR "0.27",', '  VERSION "0.34",\n  GRAMMAR "0.34",')
z = sub(z, '  VERB "FLOW",\n  SEATS []\n) RATIONALE "A named walk a record takes; its steps declare themselves THROUGH it, and its committed records are what a question asks"',
        '  VERB "FLOW",\n  SEATS [records: entity?]\n) RATIONALE "A named walk a record takes; its steps declare themselves THROUGH it, and its committed records are what a question asks. RECORDS says which ENTITY those records are, and so which fields a question may name; a flow that does not say is not field-checked"')
z = sub(z, '  FROM [flow], WHERE zexpr, CLAUSES [where, order, limit]\n)', '  FROM [flow], WHERE zexpr, CLAUSES [where, order, limit], FIELDS records.fields\n)')
z = sub(z, 'DEFINE REFUSAL dangling_reference AS (', '''DEFINE REFUSAL unknown_seat AS (
  MESSAGE "A question names only the fields its flow's records declare, or its steps compute.",
  CODE "UNKNOWN_FIELD"
) RATIONALE "WHERE or ORDER BY names a field the flow's ENTITY does not declare: a typo, refused before the question runs, where zing reads it as missing and answers no rows"

DEFINE REFUSAL dangling_reference AS (''')
wr(os.path.join(SPIKE, 'z_v34.haro'), z)

# ---- tontine/records.z: the tontine with the link, and an entity for the survey ----------------------------------------------------------------
t = rw(os.path.join(SPIKE, 'tontine.z'))
t = sub(t, '-- tontine.z -- zing\'s "tontine conformance fixtures v1" source', '-- records.z -- tontine.z with the schema declared (z_v34.haro, COMPASS-KERN-03\'s field check): `collect` says RECORDS deposit, `indice` says RECORDS survey, and a new\n-- ENTITY survey declares the one field its records carry besides the score the flow computes. Everything else is tontine.z as it stands.\n-- tontine.z -- zing\'s "tontine conformance fixtures v1" source')
t = sub(t, 'DEFINE FLOW collect AS () RATIONALE', 'DEFINE FLOW collect AS (RECORDS deposit) RATIONALE')
t = sub(t, 'DEFINE FLOW indice AS () RATIONALE', 'DEFINE FLOW indice AS (RECORDS survey) RATIONALE')
t = sub(t, 'DEFINE NORM positive_deposit AS (', 'DEFINE ENTITY survey AS (\n  FIELDS [reponses: text]\n) RATIONALE "One answered satisfaction survey; the score is computed in-flow and is not a declared field"\n\nDEFINE NORM positive_deposit AS (')
wr(os.path.join(SPIKE, 'tontine', 'records.z'), t)
wr(os.path.join(SPIKE, 'tontine', 'records_dangling.z'), sub(t, 'DEFINE FLOW collect AS (RECORDS deposit) RATIONALE', 'DEFINE FLOW collect AS (RECORDS ghost) RATIONALE'))

# ---- the cases: zing's rows, zing's answers where a question is zing's, and the new refusals -------------------------------------------------------
q = json.load(open(os.path.join(SPIKE, 'v07', 'q_cases.json'), encoding='utf-8'))
by = {c['id']: c for c in q['cases']}
FIELDS = 'id, member, amount, round, status'
cases = [
    {'id': 'f01', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE round = 1', 'expect': by['q02']['expect'],
     'name': 'zing\'s q02 on a flow whose records are declared: the same four rows, the check changes no answer'},
    {'id': 'f02', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE amount >= 7500 AND round = 2', 'expect': by['q08']['expect'], 'name': 'zing\'s q08, declared'},
    {'id': 'f03', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect ORDER BY amount DESC LIMIT 1', 'expect': by['q03']['expect'], 'name': 'zing\'s q03, declared: ORDER BY a declared field'},
    {'id': 'f04', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE round = 1 ORDER BY member DESC', 'expect': by['q10']['expect'], 'name': 'zing\'s q10, declared: WHERE and ORDER BY together'},
    {'id': 'f05', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE status = "active"', 'expect': [],
     'name': 'a field the entity declares and the rows lack is lawful, and matches nothing: a declared field is not a field every row has'},
    {'id': 'f06', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect ORDER BY member.first', 'expect': by['q01']['expect'],
     'name': 'a dotted name is judged by its head: member is declared, so member.first is lawful, and orders by what the rows hold (nothing: their own order)'},
    {'id': 'f07', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE ammount > 1', 'haro_only': True,
     'refusal': f"WHERE names 'ammount', which collect does not declare (its fields: {FIELDS})", 'name': 'a typo in WHERE: refused before the question runs, naming the field, the flow and what it has'},
    {'id': 'f08', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE round = 1 AND nope CONTAINS "x"', 'haro_only': True,
     'refusal': "WHERE names 'nope', which collect does not declare", 'name': 'an undeclared field deep in a WHERE, beside a declared one'},
    {'id': 'f09', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect ORDER BY nope', 'haro_only': True,
     'refusal': "ORDER BY names 'nope', which collect does not declare (its fields: " + FIELDS + ")", 'name': 'ORDER BY an undeclared field'},
    {'id': 'f10', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE SUM(nope) > 1', 'haro_only': True,
     'refusal': "WHERE names 'nope', which collect does not declare", 'name': 'an aggregate names a field too'},
    {'id': 'f11', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect ORDER BY nope.sub', 'haro_only': True,
     'refusal': "ORDER BY names 'nope', which collect does not declare", 'name': 'a dotted name whose head is not declared is refused by its head'},
    {'id': 'f12', 'sentence': 'tontine/records.z', 'rows': [{'reponses': '5,5,5', 'score': 100}, {'reponses': '1', 'score': 20}], 'query': 'SELECT * FROM indice WHERE score > 50',
     'expect': [{'reponses': '5,5,5', 'score': 100}], 'name': 'a name a step of the flow COMPUTEs is a field of its records, though no entity declares it'},
    {'id': 'f13', 'sentence': 'tontine/records.z', 'rows': [{'reponses': '5,5,5', 'score': 100}], 'query': 'SELECT * FROM indice WHERE total > 1', 'haro_only': True,
     'refusal': "WHERE names 'total', which indice does not declare (its fields: reponses, score)", 'name': 'the fields of a flow are its entity\'s and what its steps compute, and no others'},
    {'id': 'f14', 'sentence': 'tontine.z', 'query': 'SELECT * FROM collect WHERE nope = 1', 'expect': [],
     'name': 'a flow that writes no RECORDS is not field-checked: zing\'s reading stands, a missing field is missing, and no rows match'},
    {'id': 'f15', 'sentence': 'tontine/records.z', 'query': 'SELECT * FROM collect WHERE round = 1 ORDER BY amount LIMIT 0', 'expect': [], 'name': 'LIMIT 0 on declared fields: unchanged'},
]
wr(os.path.join(HERE, 'q_cases.json'), json.dumps({
    'grammar': 'Q', 'version': '0.34', 'ask': 'questions', 'rows': q['rows'],
    'comment': ('Written BEFORE the check (the W discipline). The rows are zing\'s ledger (v07/q_cases.json); a case may carry its own. f01-f04 are zing\'s own questions (q02, q08, q03, q10) with their answers, '
                'asked of a sentence that declares its records: the check must change no answer. f05, f06, f12 and f14 are lawful and say what the check does NOT refuse; f07-f11 and f13 are '
                'the new refusals, marked haro_only: zing reads a missing field as missing and answers no rows. All 25 of zing\'s pinned questions are asked again, unchanged, on tontine.z by stage 10.'),
    'cases': cases}, indent=1, ensure_ascii=False) + '\n')

# ---- the meta-court's fixtures --------------------------------------------------------------------------------------------------------------
LANG = 'DEFINE LANGUAGE q AS (VERSION "0.34", GRAMMAR "0.34", COURT "x", EXTENSION ".q") RATIONALE "x"\n'
EXPR = ('DEFINE EXPRESSION zexpr AS (OPERATORS [or, and, not, cmp, contains, add, sub, mul, div, round, neg], OPERANDS [number, text, flag, ref, agg], AGGREGATES [sum, count], '
        'ABSENT missing, DIVISION calm, EQUALITY value) RATIONALE "x"\n')
FIELD = 'DEFINE FORM field AS (SEATS [name: name, type: name]) RATIONALE "x"\n'
ENTITY = 'DEFINE DECLARATION entity AS (VERB "ENTITY", SEATS [fields: [field]]) RATIONALE "x"\n'


def decl(name, verb, seats):
    return f'DEFINE DECLARATION {name} AS (VERB "{verb}", SEATS {seats}) RATIONALE "x"\n'


def ask(frm='[flow]', extra=''):
    return f'DEFINE ASK questions AS (FROM {frm}, WHERE zexpr, CLAUSES [where, order, limit]{extra}) RATIONALE "x"\n'


BASE = LANG + EXPR + FIELD + ENTITY + decl('flow', 'FLOW', '[records: entity?]')


def accept(id_, name, src, **counts):
    return {'id': id_, 'name': name, 'source': src, 'expect': {'language': 'q', 'counts': counts}}


def reject(id_, name, src, refusal):
    return {'id': id_, 'name': name, 'source': src, 'refusal': refusal}


accepts = [
    accept('A1', 'FIELDS records.fields: a seat of the kind asked that refers to a declaration, and a list of name: type pairs of that declaration', BASE + ask(extra=', FIELDS records.fields'), asks=1),
    accept('A2', 'an ASK without FIELDS is the ASK it was: nothing existing changes', BASE + ask(), asks=1),
    accept('A3', 'two kinds may be asked, each with the seat', BASE + decl('stream', 'STREAM', '[records: entity?]') + ask(frm='[flow, stream]', extra=', FIELDS records.fields'), asks=1),
]
rejects = [
    reject('R1', 'FIELDS names a seat the kind asked lacks', BASE + ask(extra=', FIELDS ghost.fields'), "FIELDS: 'ghost' is not a seat of flow"),
    reject('R2', 'the first seat is a list: a question\'s FROM declaration has one entity', LANG + EXPR + FIELD + ENTITY + decl('flow', 'FLOW', '[records: [entity]?]') + ask(extra=', FIELDS records.fields'),
           "FIELDS: 'records' of flow must be one reference to a declaration"),
    reject('R3', 'the first seat is no reference to a declaration', LANG + EXPR + FIELD + ENTITY + decl('flow', 'FLOW', '[records: name?]') + ask(extra=', FIELDS records.fields'),
           "FIELDS: 'records' of flow must refer to a declaration, not to 'name'"),
    reject('R4', 'the second seat is not a seat of the declaration the first refers to', BASE + ask(extra=', FIELDS records.ghost'), "FIELDS: 'ghost' is not a seat of entity"),
    reject('R5', 'the second seat is no list of name: type pairs', LANG + EXPR + FIELD + decl('entity', 'ENTITY', '[fields: name]') + decl('flow', 'FLOW', '[records: entity?]') + ask(extra=', FIELDS records.fields'),
           "FIELDS: 'fields' of entity is not a list of name: type pairs"),
    reject('R6', 'FIELDS is written seat.seat', BASE + ask(extra=', FIELDS records'), 'FIELDS is written seat.seat'),
    reject('R7', 'every kind asked has the seat: the second lacks it', BASE + decl('stream', 'STREAM', '[tag: name?]') + ask(frm='[flow, stream]', extra=', FIELDS records.fields'),
           "FIELDS: 'records' is not a seat of stream"),
]
wr(os.path.join(HERE, 'fixtures.json'), json.dumps({
    'grammar': 'haro', 'version': '0.34',
    'comment': ('Written BEFORE any code reads FIELDS (the W discipline). v0.34 is COMPASS-KERN-03\'s field check: an ASK may name where the schema of the kind asked lives, FIELDS seat.seat, '
                'and the forged court\'s ask verb then refuses a WHERE or ORDER BY that names a field the declaration does not declare. The module docstring of gen_fixtures.py states the finding '
                'the rung started from (the world declared no schema) and the divergence from zing. A1-A3 accept; R1-R7 refuse, each by the fragment of why. A2 pins that nothing existing changes.'),
    'accepts': accepts, 'rejects': rejects}, indent=1, ensure_ascii=False) + '\n')
print(f'{len(accepts)} accepts, {len(rejects)} rejects; {len(cases)} question cases; z_v34.haro, tontine/records.z, tontine/records_dangling.z')
