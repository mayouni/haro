"""COMPASS-REBOL-06 and 07 (ruled yes by the author, 2026-10-30), fixtures first.

Writes the two fixture files the design memo is judged by, BEFORE any reader, printer or pattern engine exists:

  pattern_fixtures.json   07: pattern rules over blocks of typed values -- what matches, what is kept, what the declaration
                          of a rule is refused for (the bound that keeps them total)
  printing_fixtures.json  06: the one LOAD -- texts in two spellings that must read to the same block, texts that must not,
                          and the canonical printing of a block

The notation of a rule is itself C6 (the Grammar Commons): a rule is a list of values, so a grammar is data, read by the
same LOAD as the sentences it judges. Run once; the files it writes are committed as they stand."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))


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


MATCHES = [
    m('P01', 'a sequence of types', {'main': '[WORD NUMBER STRING]'}, 'tone 3 "x"', True),
    m('P02', 'the same sequence, out of order, does not match', {'main': '[WORD NUMBER STRING]'}, 'tone "x" 3', False),
    m('P03', 'OPT: a value that may be absent', {'main': '[WORD OPT NUMBER STRING]'}, 'tone "x"', True),
    m('P04', 'ANY then END: every value is a word', {'main': '[ANY WORD END]'}, 'a b c', True),
    m('P05', 'ANY then END: a number stops it short of the end', {'main': '[ANY WORD END]'}, 'a 1', False),
    m('P06', 'SOME needs at least one', {'main': '[SOME NUMBER]'}, '', False),
    m('P07', 'OR: ordered choice, the second alternative taken', {'main': '[WORD OR NUMBER]'}, '5', True),
    m('P08', 'literal words as a closed menu: a word outside it does not match', {'main': '[plain OR formal OR urgent]'}, 'shouty', False),
    m('P09', 'literal words as a closed menu: a word inside it matches', {'main': '[plain OR formal OR urgent]'}, 'formal', True),
    m('P10', 'LIT matches a keyword as itself (a bare keyword in a rule is a pattern word)', {'main': '[LIT DEFINE KEYWORD WORD]'},
      'DEFINE MENU tones', True),
    m('P11', 'INTO descends into a list: every item a word', {'main': '[WORD INTO [ANY WORD]]'}, 'tags [a, b, c]', True),
    m('P12', 'INTO: a number among the items does not match', {'main': '[WORD INTO [ANY WORD]]'}, 'tags [a, 2, c]', False),
    m('P13', "a declaration's shape: DEFINE, its kind, its name, AS, a group of rows, RATIONALE and a string",
      {'main': '[LIT DEFINE KEYWORD WORD LIT AS INTO [ANY ROW] LIT RATIONALE STRING]'},
      'DEFINE MENU tones AS (WORDS [plain, formal], CODE "X") RATIONALE "r"', True),
    m('P14', 'a clause is a row of a keyword and one value', {'clause': '[INTO [KEYWORD SKIP]]', 'main': '[INTO [ANY RULE clause]]'},
      '(WORDS [plain], CODE "X")', True),
    m('P15', 'a bare string where a clause belongs is not a row', {'clause': '[INTO [KEYWORD SKIP]]', 'main': '[INTO [ANY RULE clause]]'},
      '(WORDS [plain], "X")', False),
    m('P16', 'PAIR: a seat list is pairs', {'main': '[INTO [ANY PAIR]]'}, '[name: text, ceiling: number]', True),
    m('P17', 'INTO a pair reads it as its key and its value', {'main': '[INTO [ANY INTO [WORD WORD]]]'}, '[name: text, ceiling: number]', True),
    m('P18', 'MEMBER: a value drawn from a declared set', {'main': '[INTO [ANY MEMBER tones]]'}, '[plain, urgent]', True,
      sets={'tones': ['plain', 'formal', 'urgent']}),
    m('P19', 'MEMBER: a value outside the set does not match', {'main': '[INTO [ANY MEMBER tones]]'}, '[plain, loud]', False,
      sets={'tones': ['plain', 'formal', 'urgent']}),
    m('P20', "the value join (stzzui's VIBE_STRIPS_RIGHT): every strip is a value some other declaration's list seat holds -- the set is "
             "the union of those seats, which the court collects as data and the rule only reads",
      {'main': '[INTO [ANY MEMBER rights]]'}, '[left, right]', True, sets={'rights': ['left', 'centre', 'right']}),
    m('P21', 'COLLECT and KEEP: the words kept, the numbers passed over', {'main': '[COLLECT [ANY [KEEP WORD OR NUMBER]]]'}, 'a 1 b 2', True,
      kept=['a', 'b']),
    m('P22', 'KEEP outside a COLLECT keeps into the result', {'main': '[ANY [KEEP NUMBER OR SKIP]]'}, 'a 1 b 2', True, kept=['1', '2']),
    m('P23', 'TO skips up to what matches, consuming none of it', {'main': '[TO NUMBER NUMBER END]'}, 'a b 3', True),
    m('P24', 'THRU skips past what matches', {'main': '[THRU LIT RATIONALE STRING END]'}, 'DEFINE X y AS () RATIONALE "r"', True),
    m('P25', 'NOT: a value that is not a number, every time', {'main': '[ANY [NOT NUMBER SKIP] END]'}, 'a b c', True),
    m('P26', 'NOT: a number stops it', {'main': '[ANY [NOT NUMBER SKIP] END]'}, 'a 2', False),
    m('P27', 'AHEAD looks without consuming', {'main': '[AHEAD WORD SKIP END]'}, 'a', True),
    m('P28', 'REPEAT n: exactly two words', {'main': '[REPEAT 2 WORD END]'}, 'a b', True),
    m('P29', 'REPEAT n: three words are one too many', {'main': '[REPEAT 2 WORD END]'}, 'a b c', False),
    m('P30', 'REPEAT n m: between one and two', {'main': '[REPEAT 1 2 WORD END]'}, 'a b', True),
    m('P31', 'named rules, referred to and never recursive', {'seat': '[INTO [WORD WORD]]', 'seats': '[INTO [ANY RULE seat]]',
                                                               'main': '[LIT SEATS RULE seats]'}, 'SEATS [name: text]', True),
    m('P32', 'a comment is not a value', {'main': '[WORD END]'}, 'a -- a note', True),
    m('P33', 'INTO, three deep', {'main': '[INTO [INTO [INTO [NUMBER]]]]'}, '[[[7]]]', True),
    m('P34', 'an empty list', {'main': '[INTO [END]]'}, '[]', True),
    m('P35', 'a path is one value', {'main': '[PATH END]'}, 'deposit.amount', True),
    m('P36', 'items are values, a row is one item: [a b, c] is two items, the first a row', {'main': '[INTO [ROW WORD END]]'}, '[a b, c]', True),
    m('P37', 'ordered choice commits: the first alternative that matches is taken, and the rest is not tried again',
      {'main': '[[WORD OR WORD NUMBER] END]'}, 'a 1', False),
]

REFUSALS = [
    x('X01', 'a rule that refers to itself is recursive: refused', {'main': '[WORD RULE main]'}, 'recursive'),
    x('X02', 'recursion through another rule: refused', {'a': '[RULE b]', 'b': '[RULE a]', 'main': '[RULE a]'}, 'recursive'),
    x('X03', 'ANY over a rule that can match nothing would never end: refused', {'main': '[ANY OPT WORD]'}, 'can match nothing'),
    x('X04', 'SOME over a look-ahead consumes nothing: refused', {'main': '[SOME AHEAD WORD]'}, 'can match nothing'),
    x('X05', 'ANY over a named rule that can match nothing: refused', {'e': '[OPT NUMBER]', 'main': '[ANY RULE e]'}, 'can match nothing'),
    x('X06', 'WHILE is refused: a pattern rule is total', {'main': '[WHILE WORD]'}, 'WHILE is refused'),
    x('X07', 'a group in a rule is the host escape (Parse paren!): refused', {'main': '[WORD (print "x")]'}, 'would run the host'),
    x('X08', 'CHANGE is refused: a pattern judges and never edits', {'main': '[CHANGE WORD "x"]'}, 'CHANGE is refused'),
    x('X09', 'a rule that names no pattern', {'main': '[RULE nope]'}, 'names no pattern'),
    x('X10', 'a set that names nothing', {'main': '[MEMBER nope]'}, 'names no set'),
    x('X11', 'REPEAT with its minimum above its maximum', {'main': '[REPEAT 3 2 WORD]'}, 'REPEAT 3 2'),
    x('X12', 'REPEAT without its count', {'main': '[REPEAT WORD]'}, 'REPEAT takes'),
    x('X13', 'a pattern word with nothing to apply to', {'main': '[OPT]'}, 'OPT takes a rule'),
    x('X14', 'a keyword that is no pattern word', {'main': '[FOO WORD]'}, 'FOO is not a pattern word'),
    x('X15', 'DO is refused: a pattern rule runs nothing', {'main': '[DO WORD]'}, 'DO is refused'),
    x('X16', 'TO over a rule that can match nothing: it would stop at once and mean nothing', {'main': '[TO OPT WORD]'}, 'can match nothing'),
]

pattern = {
    'name': 'pattern rules over blocks of typed values (COMPASS-REBOL-07, ruled yes 2026-10-30), fixtures first',
    'comment': (
        'Written BEFORE any engine. A rule is a C6 list read by the one LOAD, so a grammar is data. Pattern words are UPPER_SNAKE '
        'keywords: the types WORD STRING NUMBER KEYWORD PATH PAIR LIST GROUP ROW and SKIP (any one value); END; OPT ANY SOME '
        'REPEAT n [m]; OR (ordered choice, as Parse | and PEG /); NOT and AHEAD (look, consume nothing); INTO (descend into a list, '
        'a group, a row or a pair -- a pair reads as its key then its value); TO and THRU; COLLECT and KEEP (Parse collect/keep); '
        'RULE name (a named rule); MEMBER name (a value drawn from a declared set -- a set is DATA the court collects from the '
        'sentence or the world, never code); LIT v (a keyword or any value matched as itself). A lower_snake word, a string or a '
        'number in a rule matches itself. A nested list in a rule is a sub-rule. A rule matches only when it consumes its whole '
        'input. THE BOUND, refused at declaration: recursion (the named rules form a DAG), a repetition or TO over a rule that can '
        'match nothing (so every ANY/SOME turn consumes a value of a finite input: Parse\'s documented infinite loop cannot be '
        'written), a group in a rule (Parse paren!, the host escape), WHILE, DO, and the editing words (CHANGE, INSERT, REMOVE): a '
        'pattern judges and never edits. Comments are not values. In the input, list and group items are separated by commas; an '
        'item of several values is a ROW (a clause such as CODE "X" is one).'),
    'matches': MATCHES,
    'refusals': REFUSALS,
}

DECL_ONE = 'DEFINE MENU tones AS (WORDS [plain, formal], CODE "X") RATIONALE "the tones"'
DECL_MANY = 'DEFINE MENU tones AS (\n  WORDS [\n    plain,\n    formal,\n  ],\n  CODE "X",\n) RATIONALE "the tones"\n'
DECL_CANON = 'DEFINE MENU tones AS (\n  WORDS [plain, formal],\n  CODE "X"\n) RATIONALE "the tones"\n'
MEMO = 'by: ringpp\nsubject: a memo\ndid:\n  - one thing\n  - another\nstate:\n  ringpp: next 9a92a6f\n'
MEMO_C6 = '(by: "ringpp", subject: "a memo", did: ["one thing", "another"], state: (ringpp: "next 9a92a6f"))'
PIA = ('pia: 1\nname: stock-watcher\nskills:\n  - name: check-stock\n    when: always\n')
PIA_C6 = '(pia: "1", name: "stock-watcher", skills: [(name: "check-stock", when: "always")])'

printing = {
    'name': 'the one LOAD and its printings (COMPASS-REBOL-06, ruled yes 2026-10-30), fixtures first',
    'comment': (
        'Written BEFORE any reader or printer. LOAD reads C6 text (strings in double quotes, numbers, lower_snake words, '
        'UPPER_SNAKE keywords, paths a.b, pairs key: value, lists [ ], groups ( ), comments --) into a block of typed values; the '
        'memo spelling (the indentation subset of C9 and .pia, read as _StzOutputParseMemo reads it) loads to the same values: a '
        'map is a group of pairs, a list a list, every scalar a string. "same" pairs must LOAD to equal blocks, "differ" pairs must '
        'not; "canonical" gives the one printing of a block; "refused" a text the LOAD refuses, with a fragment of why.'),
    'same': [
        {'id': 'L01', 'name': 'one declaration, one line and many lines', 'a': DECL_ONE, 'b': DECL_MANY},
        {'id': 'L02', 'name': 'a trailing comma is layout', 'a': '[a, b]', 'b': '[a, b,]'},
        {'id': 'L03', 'name': 'a string across lines folds its continuation indent to one space (C6 3.2)',
         'a': 'DEFINE X y AS () RATIONALE "a long\n    rationale"', 'b': 'DEFINE X y AS () RATIONALE "a long rationale"'},
        {'id': 'L04', 'name': 'CRLF and LF are the same text (C6 3.10)', 'a': DECL_ONE.replace(' (', ' (\n').replace('\n', '\r\n'),
         'b': DECL_ONE.replace(' (', ' (\n')},
        {'id': 'L05', 'name': 'a memo in its own spelling and in C6 are one block', 'a': MEMO, 'a_spelling': 'memo', 'b': MEMO_C6},
        {'id': 'L06', 'name': 'a .pia agent (a list of maps) in both spellings', 'a': PIA, 'a_spelling': 'memo', 'b': PIA_C6},
        {'id': 'L07', 'name': 'a comment survives as a value of the block, in its place', 'a': '(A 1, -- why\n B 2)', 'b': '(\n  A 1,\n  -- why\n  B 2\n)'},
    ],
    'differ': [
        {'id': 'D01', 'name': 'two items are not one row of two values', 'a': '[a, b]', 'b': '[a b]'},
        {'id': 'D02', 'name': 'a string is not a word', 'a': '"a"', 'b': 'a'},
        {'id': 'D03', 'name': 'a keyword is not a word: case is meaning (C6 3.4, 3.5)', 'a': 'CODE', 'b': 'code'},
        {'id': 'D04', 'name': 'in the memo spelling every scalar is a string, so the C6 word is another value', 'a': 'by: ringpp\n',
         'a_spelling': 'memo', 'b': '(by: ringpp)'},
    ],
    'canonical': [
        {'id': 'K01', 'name': "a declaration: its clauses one a line, a list inline, no trailing comma", 'text': DECL_MANY, 'canonical': DECL_CANON},
        {'id': 'K02', 'name': 'two declarations: a blank line between them', 'text': DECL_ONE + ' ' + DECL_ONE.replace('tones', 'moods'),
         'canonical': DECL_CANON + '\n' + DECL_CANON.replace('tones AS', 'moods AS').replace('the tones', 'the moods')},
        {'id': 'K03', 'name': 'a memo printed in its own spelling', 'text': MEMO_C6, 'spelling': 'memo',
         'canonical': MEMO},
    ],
    'refused': [
        {'id': 'F01', 'name': 'single quotes are .zql\'s divergence (D-ZQL-1), not C6', 'text': "x 'a'", 'why': 'single quote'},
        {'id': 'F02', 'name': 'a string never closed', 'text': 'x "a', 'why': 'not closed'},
        {'id': 'F03', 'name': 'a list never closed', 'text': '[a, b', 'why': 'not closed'},
        {'id': 'F04', 'name': 'a comma outside a list or a group', 'text': 'a, b', 'why': 'comma'},
        {'id': 'F05', 'name': 'a memo that opens with a bare list (as _StzOutputParseMemo refuses it)', 'text': '- a\n- b\n',
         'spelling': 'memo', 'why': 'bare list'},
    ],
}

for name, doc in (('pattern_fixtures.json', pattern), ('printing_fixtures.json', printing)):
    with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    n = sum(len(v) for k, v in doc.items() if isinstance(v, list))
    print('wrote', name, n, 'fixtures')
