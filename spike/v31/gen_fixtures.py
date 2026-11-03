"""Haro v0.31 -- step 2 of COMPASS-REBOL-06/07: pattern rules over the blocks step 1 reads, fixtures first.

Writes fixtures.json BEFORE any Haro code exists for the pattern engine. The 53 fixtures of the study
(study/rebol/pattern_fixtures.json, 17d9b4e: P01-P37 and X01-X16) are carried verbatim and unchanged. What Haro adds, each because
reading the reference or composing step 1 with step 2 showed that no fixture pinned it:

  P38-P43   Haro's `?` is a C6 value (Q-B1, v0.30) and a pattern over Haro's own declarations must be able to SEE it: the type word
            OPTIONAL, and INTO descending into the value an optional mark makes optional. P43 is the real shape: a declaration's seat list
  P44-P60   what the 53 left to a reading: a TO and a THRU that find nothing, LIT on a number, REPEAT 0, INTO on what holds nothing, a
            nested COLLECT, a MEMBER that reads a text and not a list, PEG's greedy ANY that never gives back, the empty rule
  P62, X35-X37  added AFTER the engine, each found by a plant (v31/plants.py): REPEAT 2 needs its two, REPEAT 2 needs a rule after it, and RULE
            or MEMBER followed by a value that is no word. The engine's protection was switched off and every fixture still held
  P61       the packrat: six rules each evaluating the one below twice. Within its step bound only because a (rule, sequence, position)
            is computed once -- the memo is load-bearing, and until now no fixture said so
  X17-X34   the protections the 53 left to chance: four of the seven refused words (EVAL, IF, INSERT, REMOVE) had no fixture, nor RULE/
            MEMBER/LIT without their operand, a rule that is no list, OR with a side missing, nullable bodies reached through SOME and
            through a named rule, a whole-number REPEAT count (the reference crashed on 1.5), a three-rule cycle, recursion through INTO,
            and a missing name found inside an INTO

The whole-spike fixture: the declaration form, which the meta-court spends code on, written once as a pattern and judged over every
declaration and sentence of the spike. Of 91 texts, 85 match; the six that do not are written to lack something (measured with the
reference, 2026-11-03, and each read by eye).

Expectations of the new fixtures are written by hand here. The reference is extended AFTER this file is committed, so the new fixtures
fail it first (court.py prints which). Run once; the file it writes is committed as it stands."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'study', 'rebol', 'pattern_fixtures.json')
study = json.load(open(STUDY, encoding='utf-8'))


def m(id_, name, rules, inp, match, kept=None, sets=None, start='main'):
    d = {'id': id_, 'name': name, 'rules': rules, 'start': start, 'input': inp, 'expect': {'match': match}}
    if kept is not None:
        d['expect']['kept'] = kept
    if sets:
        d['sets'] = sets
    return d


def x(id_, name, rules, refusal, sets=None, start='main'):
    d = {'id': id_, 'name': name, 'rules': rules, 'start': start, 'refusal': refusal}
    if sets:
        d['sets'] = sets
    return d


# the packrat fixture: r1..r6 each = AHEAD (the rule below) STRING OR AHEAD (the rule below) SKIP -- the rule below evaluated twice
# at the same position, the first branch failing; r7 = WORD. Three seats of work double each level without a memo
chain = {'main': '[RULE r1 END]', 'r7': '[WORD]'}
for k in range(1, 7):
    chain[f'r{k}'] = f'[AHEAD RULE r{k + 1} STRING OR AHEAD RULE r{k + 1} SKIP]'

matches = list(study['matches']) + [
    m('P38', 'OPTIONAL: the mark `?` makes one value of its own kind (Q-B1)', {'main': '[WORD OPTIONAL END]'}, 'note text?', True),
    m('P39', 'a plain word is not an OPTIONAL', {'main': '[OPTIONAL END]'}, 'text', False),
    m('P40', 'an optional value is not a WORD: the mark is part of the value', {'main': '[WORD END]'}, 'text?', False),
    m('P41', 'INTO an optional descends into the value it makes optional', {'main': '[INTO [ANY INTO [WORD INTO [WORD]]]]'}, '[note: text?]', True),
    m('P42', 'INTO an optional list, one level further', {'main': '[INTO [ANY INTO [WORD INTO [INTO [ANY WORD]]]]]'}, '[tags: [a, b]?]', True),
    m('P43', "a declaration's seat list: a pair of a name and a type, a list of types, or either made optional",
      {'main': '[LIT SEATS INTO [ANY INTO [WORD [WORD OR OPTIONAL OR LIST]]]]'}, 'SEATS [amount: number, note: text?, tags: [tag]?, owner: name]', True),
    m('P44', 'TO finds nothing: no match', {'main': '[TO NUMBER]'}, 'a b', False),
    m('P45', 'THRU finds nothing: no match', {'main': '[THRU LIT RATIONALE]'}, 'a b', False),
    m('P46', 'LIT matches a number as itself', {'main': '[LIT 5 END]'}, '5', True),
    m('P47', 'LIT on a number: another number does not match', {'main': '[LIT 5 END]'}, '6', False),
    m('P48', 'REPEAT 0 1 over an empty input', {'main': '[REPEAT 0 1 WORD END]'}, '', True),
    m('P49', 'INTO a value that holds nothing (a word) does not match', {'main': '[INTO [END]]'}, 'a', False),
    m('P50', 'INTO reads a group and a list alike', {'main': '[INTO [WORD] INTO [WORD]]'}, '(a) [b]', True),
    m('P51', 'a COLLECT inside a COLLECT is one kept list', {'main': '[COLLECT [KEEP WORD COLLECT [ANY [KEEP NUMBER]]]]'}, 'a 1 2', True, kept=['a', '[1, 2]']),
    m('P52', 'MEMBER reads a number, a string and a word by their text', {'main': '[INTO [ANY MEMBER sizes]]'}, '[1, 2, "x"]', True, sets={'sizes': ['1', '2', 'x']}),
    m('P53', 'MEMBER does not read a list', {'main': '[MEMBER tones END]'}, '[plain]', False, sets={'tones': ['plain']}),
    m('P54', 'ANY is greedy and never gives back (PEG, not a regular expression)', {'main': '[ANY WORD WORD]'}, 'a b', False),
    m('P55', 'a rule matches only when it consumes its whole input', {'main': '[WORD]'}, 'a b', False),
    m('P56', 'the empty rule matches the empty input', {'main': '[]'}, '', True),
    m('P57', 'the empty rule does not match a value', {'main': '[]'}, 'a', False),
    m('P58', 'a named rule used twice in one rule', {'w': '[WORD]', 'main': '[RULE w RULE w END]'}, 'a b', True),
    m('P59', 'a sub-rule is a sequence in its place', {'main': '[WORD [NUMBER STRING] END]'}, 'a 1 "x"', True),
    m('P60', 'a pair is one value; its key is read as a word', {'main': '[PAIR END]'}, 'name: text', True),
    m('P61', 'the packrat: six rules each evaluating the one below twice stay within nodes x positions, because a (rule, sequence, position) is computed once',
      chain, 'a', True),
    m('P62', 'REPEAT 2 needs its two: one word is too few (added after the engine, found by a plant)', {'main': '[REPEAT 2 WORD END]'}, 'a', False),
]
refusals = list(study['refusals']) + [
    x('X17', 'MEMBER without a name', {'main': '[MEMBER]'}, 'MEMBER takes a name'),
    x('X18', 'RULE without a name', {'main': '[RULE]'}, 'RULE takes a name'),
    x('X19', 'LIT without a value', {'main': '[LIT]'}, 'LIT takes a value'),
    x('X20', 'EVAL is refused: a pattern rule runs nothing', {'main': '[EVAL WORD]'}, 'EVAL is refused'),
    x('X21', 'IF is refused: a condition is a rule, never host code', {'main': '[IF WORD]'}, 'IF is refused'),
    x('X22', 'INSERT is refused: a pattern judges and never edits', {'main': '[INSERT WORD "x"]'}, 'INSERT is refused'),
    x('X23', 'REMOVE is refused: a pattern judges and never edits', {'main': '[REMOVE WORD]'}, 'REMOVE is refused'),
    x('X24', 'a rule that is no list', {'main': 'WORD'}, 'is not a list'),
    x('X25', 'OR with nothing before it', {'main': '[OR WORD]'}, 'OR needs a rule on each side'),
    x('X26', 'OR with nothing after it', {'main': '[WORD OR]'}, 'OR needs a rule on each side'),
    x('X27', 'SOME over ANY: it can match nothing, so it would never move', {'main': '[SOME ANY WORD]'}, 'can match nothing'),
    x('X28', 'TO over a named rule that can match nothing', {'e': '[ANY WORD]', 'main': '[TO RULE e]'}, 'can match nothing'),
    x('X29', 'REPEAT takes a whole count: 1.5 is not one', {'main': '[REPEAT 1.5 WORD]'}, 'a whole count of zero or more'),
    x('X30', 'REPEAT takes a count of zero or more: -1 is not one', {'main': '[REPEAT -1 WORD]'}, 'a whole count of zero or more'),
    x('X31', 'a cycle of three rules, named in full', {'a': '[RULE b]', 'b': '[RULE c]', 'c': '[RULE a]', 'main': '[RULE a]'}, 'a -> b -> c -> a'),
    x('X32', 'recursion through INTO: a smaller value does not excuse a rule that refers to itself', {'main': '[INTO [RULE main]]'}, 'recursive'),
    x('X33', 'a set that names nothing, found inside an INTO', {'main': '[INTO [ANY MEMBER nope]]'}, 'MEMBER nope names no set'),
    x('X34', 'a rule that names no pattern, found inside an INTO', {'main': '[INTO [ANY RULE nope]]'}, 'RULE nope names no pattern'),
    x('X35', 'REPEAT with a count and no rule after it (added after the engine, found by a plant)', {'main': '[REPEAT 2]'}, 'REPEAT takes a count, then a rule'),
    x('X36', 'RULE followed by a number, which is no name (added after the engine, found by a plant)', {'main': '[RULE 5]'}, 'RULE takes a name'),
    x('X37', 'MEMBER followed by a string, which is no name (added after the engine, found by a plant)', {'main': '[MEMBER "x"]'}, 'MEMBER takes a name'),
]
family = {
    'id': 'FAM1',
    'name': "the declaration form, written once as a pattern, over every declaration and sentence of the spike: a keyword, a name, AS, a group, RATIONALE and its string",
    'rules': {'decl': '[LIT DEFINE KEYWORD WORD LIT AS GROUP LIT RATIONALE STRING]', 'main': '[SOME RULE decl END]'},
    'start': 'main',
    'texts': 91,
    'matching': 85,
    'unmatched': {
        'f/missing-rationale.f': 'a sentence written to lack its RATIONALE (its second declaration)',
        'f/operator-in-guard.f': 'unreadable: an operator is not C6 (a text written to be refused)',
        'ledger/bank_no_rationale.ledger': 'a LIMIT written to lack its RATIONALE (refused under Art. 1)',
        'notice/unknown_verb.notice': 'a declaration without DEFINE: a verb the language does not know',
        'tontine/drop.z': 'DROP TABLE: not a declaration at all',
        'v15/four.haro': 'a declaration written to lack its RATIONALE, among four other defects',
    },
}
doc = {
    'grammar': 'haro', 'version': '0.31',
    'name': 'pattern rules over blocks of typed values, in Haro (step 2 of COMPASS-REBOL-06/07), fixtures first',
    'comment': ('Written BEFORE pattern_lib.haro. P01-P37 and X01-X16 are the study\'s 53, verbatim (study/rebol/pattern_fixtures.json); P38-P62 and '
                'X17-X37 are Haro\'s, each because no fixture pinned what it pins (the module docstring of gen_fixtures.py says which and why). A rule is C6 '
                'text, a list, read by the one LOAD (block_lib.haro); a grammar is data. Pattern words are UPPER_SNAKE keywords: the types WORD STRING NUMBER '
                'KEYWORD PATH PAIR LIST GROUP ROW OPTIONAL and SKIP (any one value); END; OPT ANY SOME REPEAT; OR (ordered choice); NOT AHEAD; INTO (a list, a '
                'group, a row, a pair read as its key then its value, an optional read as the value it marks); TO THRU; COLLECT KEEP; RULE name; MEMBER name '
                '(a value drawn from a SET the court collects, never code); LIT v. A lower_snake word, a string or a number in a rule matches itself. A rule '
                'matches only when it consumes its whole input. THE BOUND, refused at declaration and never at match time: recursion, a repetition or TO over a '
                'rule that can match nothing, a group in a rule, WHILE DO EVAL IF, and the editing words CHANGE INSERT REMOVE. Matching is PEG with a packrat '
                'memo: at most (rule nodes x input positions) steps, held on every match fixture. "matches" are judged by the verdict and the values kept; '
                '"refusals" by the fragment of why the declaration is refused. "family" is judged over every declaration and sentence of the spike, by the '
                'number that match and the six that do not, by name. Every fixture is judged on haro and its checked build, byte-identical, and beside the '
                'Python reference (study/rebol/pattern.py), the two refusing a difference by name (D43).'),
    'matches': matches, 'refusals': refusals, 'family': family,
}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print(f'{len(matches)} matches ({len(matches) - len(study["matches"])} new), {len(refusals)} refusals ({len(refusals) - len(study["refusals"])} new), '
      f'the family fixture ({family["texts"]} texts, {family["matching"]} match)')
