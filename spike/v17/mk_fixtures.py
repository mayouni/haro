"""Writes v17/fixtures.json: the conformance floor of the N letter as DRAWN (n_v17.haro, n/tontine.n).

Composed from the letter's own declared MESSAGES and CODES and from the rules in GRAMMAR.md -- before the
checks that judge them were run on these cases (the W discipline: fixtures first). Two kinds:

  court   a defect the EXISTING meta-vocabulary makes the forged court refuse: its message must hold the
          text declared in n_v17.haro, and `diagnose` must carry the code declared there
  rule    a defect the existing court CANNOT see (it must still say `ok`) and the rule of the next rung must
          catch: n_model.rules() must answer the code. Each is what v0.17 would add as a check

Each case is one replacement in n/tontine.n, anchored: the old text must occur exactly once.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
court, rule = [], []


def C(cid, name, old, new, message, code=None):
    court.append({'id': cid, 'name': name, 'old': old, 'new': new, 'message': message, 'code': code})


def R(cid, name, old, new, code):
    rule.append({'id': cid, 'name': name, 'old': old, 'new': new, 'code': code})


# ---- the existing vocabulary: references, menus, required seats, one namespace, closure ----------------------------
C('C01', 'a column keyed by a tongue nobody declared', 'WORDS [english: "who", french: "qui"]', 'WORDS [english: "who", german: "wer"]',
  "which resolves to nothing", None)
C('C02', 'a frame whose shape names no meaning', 'SHAPE [show, deposit, over, num], TARGET ledger', 'SHAPE [show, deposit, ovr, num], TARGET ledger',
  "FRAME ledger_over has 'ovr' in its SHAPE, which is not a declared meaning", 'DANGLING_MEANING')
C('C03', 'a frame aimed at no surface', 'SHAPE [show, deposit], TARGET ledger,', 'SHAPE [show, deposit], TARGET ledgr,',
  "FRAME ledger_all is aimed at 'ledgr', which is not a declared surface", 'DANGLING_SURFACE')
C('C04', 'an example that means no frame', 'MEANS ledger_over,\n  ASKING [english: "show deposits over 5000"', 'MEANS ledger_ovr,\n  ASKING [english: "show deposits over 5000"',
  "EXAMPLE p01 means 'ledger_ovr', which is not a declared frame", 'DANGLING_FRAME')
C('C05', 'a step aimed at no surface', 'TARGET graph, QUERY "?x received_pot_in round{num}", BINDS member', 'TARGET grph, QUERY "?x received_pot_in round{num}", BINDS member',
  "STEP find_beneficiary is aimed at 'grph', which is not a declared surface", 'DANGLING_SURFACE')
C('C06', 'a surface that tells in no tongue', 'TELLS [english, french]', 'TELLS [english, german]',
  "SURFACE ledger tells in 'german', which is not a declared tongue", 'DANGLING_TONGUE')
C('C07', 'a meaning that draws from no surface', 'SLOT entity, OF member, FROM graph', 'SLOT entity, OF member, FROM grph',
  "MEANING member draws its entities from 'grph', which is not a declared surface", 'DANGLING_SURFACE')
C('C08', 'an alias of no meaning', 'MEANING role, ENTITY "treasurer"', 'MEANING rol, ENTITY "treasurer"',
  "ALIAS treasurer is of 'rol', which is not a declared meaning", 'DANGLING_MEANING')
C('C09', 'a declaration N does not have: N never declares', 'DEFINE STEP find_beneficiary AS (', 'DEFINE NORM positive_deposit AS (RULE "amount > 0") RATIONALE "x"\n\nDEFINE STEP find_beneficiary AS (',
  "N asks; it never declares the world, the facts or a rule", None)
C('C10', 'a free-text slot: the one thing a question may not carry', 'DEFINE MEANING num AS (\n  SLOT number', 'DEFINE MEANING num AS (\n  SLOT text',
  "SLOT is none, number or entity, not 'text'", 'PARSE')
C('C11', 'a digit set the court does not know', 'DIGITS ascii,\n  NAMES upper_first,\n  REFUSES [\n    character: "the question', 'DIGITS arabic_indic,\n  NAMES upper_first,\n  REFUSES [\n    character: "the question',
  "DIGITS is ascii", 'PARSE')
C('C12', 'a refusal kind that does not exist', 'ambiguous: "the question needs one answer', 'name: "the question needs one answer',
  "not 'name'", 'PARSE')
C('C13', 'a spelling that does not exist', 'SPELLS [member: upper_first],', 'SPELLS [member: shouting],',
  "a spelling is as_is or upper_first, not 'shouting'", 'PARSE')
C('C14', 'a meaning with no slot', 'DEFINE MEANING show AS (\n  SLOT none,', 'DEFINE MEANING show AS (',
  "MEANING show needs a SLOT", 'MEANING_INCOMPLETE')
C('C15', 'a surface with no court: a surface is a protocol', 'KIND query, GRAMMAR "ZQL ASK", COURT "z_court.ring ask",', 'KIND query, GRAMMAR "ZQL ASK",',
  "SURFACE ledger needs its COURT", 'SURFACE_INCOMPLETE')
C('C16', 'a declaration without its rationale', 'DEFINE ALIAS collector AS (\n  MEANING role, ENTITY "collector",\n  WORDS [english: "collector", french: "collecteur"]\n) RATIONALE "The member who takes the deposits"',
  'DEFINE ALIAS collector AS (\n  MEANING role, ENTITY "collector",\n  WORDS [english: "collector", french: "collecteur"]\n)',
  "RATIONALE is mandatory on every declaration", None)
C('C17', 'a name declared twice: one namespace', 'DEFINE MEANING under AS (', 'DEFINE MEANING over AS (',
  "'over' is already declared", None)

# ---- the rules the existing vocabulary cannot say: what v0.17 adds ------------------------------------------------------
R('R01', 'a placeholder in a QUERY that is not a slot of the shape', 'QUERY "SELECT * FROM collect WHERE amount > {num}"', 'QUERY "SELECT * FROM collect WHERE amount > {amnt}"', 'N_SLOT_UNKNOWN')
R('R02', 'a placeholder in an ANSWERS that is not a slot', '{answer} received the pot in round {num}.', '{winner} received the pot in round {num}.', 'N_SLOT_UNKNOWN')
R('R03', 'a plan step using a slot nothing bound', 'QUERY "SELECT * FROM collect WHERE member = \'{member}\'"\n) RATIONALE "That member', 'QUERY "SELECT * FROM collect WHERE member = \'{memberr}\'"\n) RATIONALE "That member', 'N_SLOT_UNKNOWN')
R('R04', 'a slot meaning twice in one shape', 'SHAPE [show, deposit, member, over, num], TARGET ledger,', 'SHAPE [show, deposit, member, member, num], TARGET ledger,', 'N_SLOT_REPEATED')
R('R05', 'a frame with neither a target and query nor steps', 'SHAPE [show, deposit], TARGET ledger, QUERY "SELECT * FROM collect"', 'SHAPE [show, deposit], QUERY "SELECT * FROM collect"', 'N_FRAME_TARGET')
R('R06', 'a frame with both a target and steps', 'SHAPE [show, deposit], TARGET ledger, QUERY "SELECT * FROM collect"', 'SHAPE [show, deposit], TARGET ledger, QUERY "SELECT * FROM collect", STEPS [find_beneficiary]', 'N_FRAME_TARGET')
R('R07', 'a surface that cannot tell in a tongue, with no frame template to cover it', 'TELLS [english, french]', 'TELLS [english]', 'N_TELL_UNCOVERED')
R('R08', 'an ANSWERS with no EMPTY: an answer may be nobody', 'EMPTY [english: "Nobody received the pot in round {num}.", french: "Personne n\'a reçu la cagnotte au tour {num}."]', 'EMPTY [english: "Nobody received the pot in round {num}."]', 'N_TELL_UNCOVERED')
R('R09', 'a tongue that cannot say one kind of refusal', ',\n    surface: "la source a refusé la question compilée : {what}"', '', 'N_REFUSAL_UNCOVERED')
R('R10', 'a tongue that widens the gate beyond the court\'s safe set', 'ALLOWS "-\'?,.",\n  DIGITS ascii,\n  NAMES upper_first,\n  REFUSES [\n    character: "la question', 'ALLOWS "-\'?,.;",\n  DIGITS ascii,\n  NAMES upper_first,\n  REFUSES [\n    character: "la question', 'N_GATE_WIDENED')
R('R11', 'a word that means two things in one tongue', 'WORDS [english: "who", french: "qui"]', 'WORDS [english: "who show", french: "qui"]', 'N_WORD_AMBIGUOUS')
R('R12', 'a word both ignored and meaningful', 'IGNORES "the a an of me please', 'IGNORES "deposits the a an of me please', 'N_WORD_IGNORED')
R('R13', 'a meaning with no words in a tongue', 'WORDS [english: "who", french: "qui"]', 'WORDS [english: "who"]', 'N_TONGUE_UNCOVERED')
R('R14', 'an entity meaning of a kind its surface does not enumerate', 'SLOT entity, OF member, FROM graph', 'SLOT entity, OF person, FROM graph', 'N_ENTITY_UNKNOWN')
R('R15', 'a surface that does not enumerate what a meaning draws from it', 'ENTITIES [member, round, role],', 'ENTITIES [round, role],', 'N_ENTITY_UNKNOWN')
R('R16', 'a ledger query the ledger\'s own court refuses', 'QUERY "SELECT * FROM collect WHERE amount < {num}"', 'QUERY "SELECT member FROM collect WHERE amount < {num}"', 'N_QUERY_REFUSED')
R('R17', 'a graph pattern that is not three terms', 'QUERY "?x received_pot_in round{num}",\n  ANSWERS', 'QUERY "?x received_pot_in",\n  ANSWERS', 'N_QUERY_REFUSED')
R('R18', 'an example its own text does not reach', 'ASKING [english: "show deposits over 5000", french: "montre les dépôts au dessus de 5000"]', 'ASKING [english: "show deposits over five thousand", french: "montre les dépôts au dessus de 5000"]', 'N_EXAMPLE_FAILED')
R('R19', 'an example whose tongues compile to different queries', 'ASKING [english: "show deposits over 5000", french: "montre les dépôts au dessus de 5000"]', 'ASKING [english: "show deposits over 5000", french: "montre les dépôts au dessus de 4000"]', 'N_EXAMPLE_DIVERGES')
R('R20', 'a counterexample that IS understood', 'ASKING [english: "what is the meaning of life"], REFUSED word', 'ASKING [english: "show deposits"], REFUSED word', 'N_COUNTEREXAMPLE_FAILED')

doc = {
    'grammar': 'haro-n', 'version': '0.17',
    'comment': __doc__.strip(),
    'sentence': 'n/tontine.n', 'letter': 'n_v17.haro',
    'court': court, 'rules': rule,
}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(f'wrote {len(court)} court cases and {len(rule)} rule cases')
