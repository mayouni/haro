"""Haro v0.30 -- step 1 of COMPASS-REBOL-06: the one reader of C6 and its canonical printer, fixtures first.

Writes fixtures.json BEFORE any Haro code exists for the reader or the printer. The sixteen C6 fixtures of the study
(study/rebol/printing_fixtures.json, 17d9b4e, then D05 and F06) are carried verbatim; what Haro adds is named H/D/K/F
with a number past the study's. The expected canonical texts are computed by the study's reference reader (block.py)
and were read by eye before this file was committed: the reference is the judge of the printer, the fixtures the judge
of both.

Five of the study's twenty-one are the MEMO spelling (L05, L06, D04, K03, F05): step 3 of the memo, not this rung.
They are listed under left_to_step_3 so the guard prints what it skipped, by name.

Q-B1 (ruled 2026-11-02): Haro's `AS` and `?` are C6, recorded as amendments Ringua writes -- the reader accepts them.
Q-B2 (ruled 2026-11-02): a doubled quote inside a string, and a string as a pair's key, are C6 amendments Ringua
writes; until its text lands the reader REFUSES both, by name (F07, F08).

Run once; the file it writes is committed as it stands."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'study', 'rebol')
sys.path.insert(0, STUDY)
import block                                           # the reference reader and printer

study = json.load(open(os.path.join(STUDY, 'printing_fixtures.json'), encoding='utf-8'))
MEMO = {'L05', 'L06', 'D04', 'K03', 'F05'}


def carried(section):
    return [f for f in study[section] if f['id'] not in MEMO]


def canon(text):
    return block.print_c6(block.load(text))


same = carried('same') + [
    {'id': 'H01', 'name': "Haro's `?` is C6 (Q-B1): an optional seat, on one line and on many",
     'a': 'DEFINE DECLARATION deposit AS (SEATS [amount: number, note: text?, tags: [tag]?]) RATIONALE "a deposit"',
     'b': 'DEFINE DECLARATION deposit AS (\n  SEATS [\n    amount: number,\n    note: text?,\n    tags: [tag]?,\n  ],\n) RATIONALE "a deposit"\n'},
    {'id': 'H02', 'name': 'a path is one value, however the layout around it',
     'a': '(POINTS [deposit.amount: trusted])',
     'b': '(\n  POINTS [\n    deposit.amount:   trusted\n  ]\n)'},
    {'id': 'H03', 'name': 'a negative and a decimal number, spaced or not',
     'a': '[-1, 2.5]', 'b': '[ -1 ,2.5 ]'},
    {'id': 'H04', 'name': 'a comment at the end of a line and on its own line are one block: a comment is a value, layout is not',
     'a': 'DEFINE X y AS () RATIONALE "r" -- why', 'b': 'DEFINE X y AS () RATIONALE "r"\n-- why\n'},
]
differ = carried('differ') + [
    {'id': 'D06', 'name': 'a path is not two words', 'a': '[deposit.amount]', 'b': '[deposit, amount]'},
    {'id': 'D07', 'name': 'an optional value is not the value (Q-B1)', 'a': '[tags: [tag]?]', 'b': '[tags: [tag]]'},
    {'id': 'D08', 'name': 'a group is not a list', 'a': '(a, b)', 'b': '[a, b]'},
]
K04 = 'DEFINE DECLARATION deposit AS (SEATS [amount: number, note: text?], POINTS [deposit.amount: trusted]) RATIONALE "a deposit"'
K05 = '(A 1, -- why\n B [x, -- here\n y], C (D 2))'
K06 = 'DEFINE MENU tones AS (WORDS [plain, formal], CODE "X") RATIONALE "the tones" -- after\n-- alone\nDEFINE MENU moods AS (WORDS [calm]) RATIONALE "the moods"'
K07 = '[-1,   2.50]'
canonical = carried('canonical') + [
    {'id': 'K04', 'name': "an optional seat keeps its `?`, a path its dots; a list of pairs prints inline", 'text': K04, 'canonical': canon(K04)},
    {'id': 'K05', 'name': 'a comment stands on its own line; a list holding a comment, and a list holding a group, print one item a line',
     'text': K05, 'canonical': canon(K05)},
    {'id': 'K06', 'name': 'a comment ends its line; two declarations keep a blank line between them', 'text': K06, 'canonical': canon(K06)},
    {'id': 'K07', 'name': 'a number prints as written', 'text': K07, 'canonical': canon(K07)},
]
refused = carried('refused') + [
    {'id': 'F07', 'name': "a string as a pair's key waits for C6's amendment (Q-B2, Ringua writes it): refused by name until its text lands",
     'text': '("the page": 1)', 'why': "pair's key waits for C6's amendment (Q-B2)"},
    {'id': 'F08', 'name': "a doubled quote inside a string waits for C6's amendment (Q-B2): a C6 string has no escape today",
     'text': 'x "a ""b"" c"', 'why': "doubled quote inside a string waits for C6's amendment (Q-B2)"},
    {'id': 'F09', 'name': 'a path is written without spaces', 'text': '[a . b]', 'why': "'.'"},
    {'id': 'F10', 'name': 'a `?` marks the value before it; here nothing stands before it', 'text': '[?]', 'why': "'?'"},
    {'id': 'F11', 'name': 'mixed case is neither a word nor a keyword (C6 3.4, 3.5; the study reader read it as a word -- Haro refuses it, as both its lexers did)',
     'text': 'Foo', 'why': 'neither a lower_snake identifier nor an UPPER_SNAKE keyword'},
    {'id': 'F12', 'name': 'a pair with no value', 'text': '(a:)', 'why': 'no value'},
]
left = [{'id': f['id'], 'section': s, 'why': 'the memo spelling: step 3 of BLOCKS.md 3.5, not this rung'}
        for s in ('same', 'differ', 'canonical', 'refused') for f in study[s] if f['id'] in MEMO]

doc = {
    'grammar': 'haro', 'version': '0.30',
    'name': 'the one reader of C6 and its canonical printer (step 1 of COMPASS-REBOL-06), fixtures first',
    'comment': ('Written BEFORE block_lib.haro and block.haro. Carried verbatim from study/rebol/printing_fixtures.json: the sixteen C6 '
                'fixtures (L01-L04, L07; D01-D03, D05; K01, K02; F01-F04, F06). Added for Haro: H01-H04 and D06-D08 (Haro\'s `?` is C6 by Q-B1, '
                'paths, numbers, comments), K04-K07 (the printer on those), F07-F12 (Q-B2\'s two amendments refused by name until Ringua\'s text '
                'lands; a path with spaces; a `?` on nothing; mixed case; a pair with no value). "same" pairs must read to equal blocks, '
                '"differ" pairs must not; "canonical" gives the one printing; "refused" a text the reader refuses, with a fragment of why. '
                'Every fixture is judged on haro and on its checked build, byte-identical. left_to_step_3 names the five memo-spelling fixtures '
                'the guard skips, so a scoped run prints what it skipped.'),
    'same': same, 'differ': differ, 'canonical': canonical, 'refused': refused, 'left_to_step_3': left,
}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
n = sum(len(doc[s]) for s in ('same', 'differ', 'canonical', 'refused'))
print(f'{n} fixtures written ({len(same)} same, {len(differ)} differ, {len(canonical)} canonical, {len(refused)} refused); {len(left)} left to step 3')
for f in canonical:
    if f['id'] >= 'K04':
        print('----', f['id']); print(f['canonical'], end='')
