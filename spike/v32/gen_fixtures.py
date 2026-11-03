"""Haro v0.32 -- DEFINE PATTERN (BLOCKS.md 4.3), fixtures first.

Writes fixtures.json (the meta-court's: what a declaration with a PATTERN must be accepted for and refused for) and court_cases.json (the
forged court's: the grants world, grants_v32.haro, and its twelve sentences in spike/grants/ (ten at first; shape_broken and zone_primary were added after the code)) BEFORE any code reads a PATTERN. The world and
the sentences are committed with them: they are fixtures too.

The design this file pins (the desk's, within the author's word to start the rung; D46 records it for him to refuse):

  DEFINE PATTERN name AS (OVER kind.seat, MATCH [ rule ], SETS [kind.seat: set, ...], MESSAGE, CODE, CITES, SEVERITY) RATIONALE "..."

  OVER     the seat a pattern judges, named as declaration.seat. The value judged is the seat's value AS WRITTEN in the sentence, read by
           the one LOAD (v0.30): `[read, write]` is a list of two words, `read` one word. A seat a sentence does not write is not judged
           (REQUIRED speaks for a required one). A whole declaration as the judged value is not built: the court already judges a
           declaration's form, and no customer asks for more
  MATCH    the rule, a C6 list between brackets, written in the declaration itself and not in a string. The meta-court judges it by the
           pattern engine's declaration (v0.31): recursion, a nullable repetition, a group, WHILE and the editing words are refused, in
           the engine's words. A pattern may use another by RULE name; the patterns of a language form one set of named rules
  SETS     where a MEMBER set comes from, as the points REFINE already writes: `zone.rights: granted` says the set `granted` is the values of
           the seat zone.rights across every ZONE of the sentence. A set is DATA the court collects, never code. A MENU of the language is a
           set already, under its own name. One set, one declaration: a set named twice, or named like a MENU, is refused
  the rest MESSAGE, CODE, CITES (a list, or the word none), SEVERITY (error or warning) are a CONSTRAINT's, with the same meaning and the
           same words. Under Art. 1 explainability a pattern carries a CODE, as a REFUSAL and a CONSTRAINT do

Run once; the files it writes are committed as they stand."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = 'DEFINE LANGUAGE grants AS (VERSION "0.32", GRAMMAR "0.32", COURT "x", EXTENSION ".grant") RATIONALE "x"\n'
BASE = (LANG +
        'DEFINE FORM word AS (SEATS [value: name]) RATIONALE "x"\n'
        'DEFINE MENU channels AS (WORDS [mail, chat, call], CODE "UNKNOWN_CHANNEL") RATIONALE "x"\n'
        'DEFINE DECLARATION zone AS (VERB "ZONE", SEATS [rights: [word]]) RATIONALE "x"\n'
        'DEFINE DECLARATION use AS (VERB "USE", SEATS [wants: [word], primary: name?, via: [word]?]) RATIONALE "x"\n')
COUNTS = {'declarations': 2, 'forms': 1, 'menus': 1}


def pat(name, over='use.wants', match='[INTO [ANY WORD]]', extra='', msg='"m"'):
    return f'DEFINE PATTERN {name} AS (OVER {over}, MATCH {match}, MESSAGE {msg}{extra}) RATIONALE "x"\n'


def accept(id_, name, patterns, n):
    return {'id': id_, 'name': name, 'source': BASE + patterns, 'expect': {'language': 'grants', 'counts': dict(COUNTS, patterns=n)}}


def reject(id_, name, source, refusal):
    return {'id': id_, 'name': name, 'source': source, 'refusal': refusal}


accepts = [
    accept('A1', 'a pattern over a seat, its set the values of another declaration\'s seat: the value join (OVER, SETS, MATCH, MESSAGE, CODE, CITES)',
           pat('wants_granted', match='[INTO [ANY MEMBER granted]]', extra=', SETS [zone.rights: granted], CODE "RIGHT_NOT_GRANTED", CITES ["right:granted-by-a-zone"]'), 1),
    accept('A2', 'a MENU is a set under its own name, and CITES none is the same word as on a CONSTRAINT',
           pat('via_channel', over='use.via', match='[INTO [ANY MEMBER channels]]', extra=', CODE "NOT_A_CHANNEL", CITES none'), 1),
    accept('A3', 'a pattern uses another by RULE name: the patterns of a language are one set of named rules',
           pat('granted_right', over='use.primary', match='[MEMBER granted]', extra=', SETS [zone.rights: granted], CODE "PRIMARY_NOT_GRANTED"') +
           pat('wants_granted', match='[INTO [ANY RULE granted_right]]', extra=', CODE "RIGHT_NOT_GRANTED"'), 2),
    accept('A4', 'SEVERITY warning is a CONSTRAINT\'s word, and a rule may be written across lines with a comment in it',
           'DEFINE PATTERN few AS (\n  OVER use.wants,\n  MATCH [INTO [REPEAT 0 3 SKIP] -- at most three\n  ],\n  MESSAGE "m", CODE "MANY_RIGHTS", SEVERITY warning\n) RATIONALE "x"\n', 1),
    accept('A5', 'a rule that needs no set: types alone', pat('words_only', match='[INTO [ANY WORD]]'), 1),
    accept('A6', 'two patterns over one seat are two patterns',
           pat('a_words', match='[INTO [ANY WORD]]') + pat('b_few', match='[INTO [REPEAT 0 3 SKIP]]', extra=', SEVERITY warning'), 2),
]
rejects = [
    reject('R1', 'OVER names a declaration the language does not have', BASE + pat('p', over='ghost.wants'), "OVER: 'ghost' resolves to nothing in this declaration"),
    reject('R2', 'OVER names something that is no DECLARATION', BASE + pat('p', over='channels.wants'), "OVER must name a DECLARATION; 'channels' is a MENU"),
    reject('R3', 'OVER names a seat the declaration lacks', BASE + pat('p', over='use.ghost'), "OVER names a seat of use; 'ghost' is not one"),
    reject('R4', 'OVER names a seat as declaration.seat, not as a bare word', BASE + pat('p', over='wants'), 'OVER names a seat as declaration.seat'),
    reject('R5', 'MATCH is a rule between brackets, not a string', BASE + 'DEFINE PATTERN p AS (OVER use.wants, MATCH "x", MESSAGE "m") RATIONALE "x"\n', 'a rule is written [ ... ]'),
    reject('R6', 'a rule that is never closed', BASE + 'DEFINE PATTERN p AS (OVER use.wants, MATCH [INTO [ANY WORD], MESSAGE "m") RATIONALE "x"\n', 'a rule is not closed'),
    reject('R7', 'the bound: ANY over a rule that can match nothing would never move, and the engine\'s words are the meta-court\'s', BASE + pat('p', match='[INTO [ANY OPT WORD]]'),
           'ANY over a rule that can match nothing'),
    reject('R8', 'the bound: a group in a rule is the host escape', BASE + pat('p', match='[WORD (print "x")]'), 'would run the host'),
    reject('R9', 'the bound: WHILE is refused', BASE + pat('p', match='[WHILE WORD]'), 'WHILE is refused'),
    reject('R10', 'the bound: two patterns that refer to each other are recursive, and the cycle is named', BASE + pat('a', match='[RULE b]') + pat('b', match='[RULE a]'), 'is recursive (a -> b -> a)'),
    reject('R11', 'a MEMBER that names no set and no MENU', BASE + pat('p', match='[INTO [ANY MEMBER nope]]'), 'MEMBER nope names no set'),
    reject('R12', 'a RULE that names no pattern', BASE + pat('p', match='[INTO [ANY RULE nope]]'), 'RULE nope names no pattern'),
    reject('R13', 'SETS names a declaration the language does not have', BASE + pat('p', extra=', SETS [ghost.rights: granted]'), "SETS: 'ghost' resolves to nothing in this declaration"),
    reject('R14', 'SETS names a seat the declaration lacks', BASE + pat('p', extra=', SETS [zone.ghost: granted]'), "SETS names a seat of zone; 'ghost' is not one"),
    reject('R15', 'a set named like a MENU: one name, one meaning', BASE + pat('p', extra=', SETS [zone.rights: channels]'), "set 'channels' is already a MENU: one name, one meaning"),
    reject('R16', 'a set declared by two patterns', BASE + pat('p', extra=', SETS [zone.rights: granted]') + pat('q', extra=', SETS [zone.rights: granted]'), "set 'granted' is declared twice"),
    reject('R17', 'a PATTERN without OVER', BASE + 'DEFINE PATTERN p AS (MATCH [WORD], MESSAGE "m") RATIONALE "x"\n', 'PATTERN requires the OVER clause'),
    reject('R18', 'a PATTERN without MATCH', BASE + 'DEFINE PATTERN p AS (OVER use.wants, MESSAGE "m") RATIONALE "x"\n', 'PATTERN requires the MATCH clause'),
    reject('R19', 'a SEVERITY that is neither error nor warning', BASE + pat('p', extra=', SEVERITY fatal'), "'fatal' is not a SEVERITY of a PATTERN: error or warning"),
    reject('R20', 'a CODE outside the Diagnostic Contract\'s format', BASE + pat('p', extra=', CODE "bad code"'), "is not a code in the Diagnostic Contract's format"),
    reject('R21', 'a pattern named like a declaration: one namespace', BASE + pat('zone'), "'zone' is already declared -- one namespace, one name, one meaning"),
    reject('R22', 'a rule that holds a double quote and a single quote cannot ride into a court', BASE + pat('p', match='[INTO [ANY LIT "it\'s"]]'),
           'a rule that holds a double quote and a single quote'),
    reject('R23', 'an empty CITES says nothing, on a PATTERN as on every element that cites', BASE + pat('p', extra=', CITES []'), 'an empty CITES says nothing'),
    reject('R24', 'an unknown clause lists the allowed ones, sorted', BASE + pat('p', extra=', WHEN "x"'), "Unknown clause 'WHEN' in PATTERN -- allowed: CITES, CODE, MATCH, MESSAGE, OVER, SETS, SEVERITY"),
    reject('R26', 'a PATTERN without MESSAGE (added after the code, found by reading it: no fixture said MESSAGE is required)', BASE + 'DEFINE PATTERN p AS (OVER use.wants, MATCH [WORD]) RATIONALE "x"\n', 'PATTERN requires the MESSAGE clause'),
    reject('R27', "SETS draws from words, strings and numbers: a list of pairs is refused by name (added after the code: the court once gave a pair list's values, and no fixture pinned it)",
           BASE + 'DEFINE FORM limit AS (SEATS [right: name, max: number]) RATIONALE "x"\nDEFINE DECLARATION cap AS (VERB "CAP", SEATS [limits: [limit]]) RATIONALE "x"\n' + pat('p', extra=', SETS [cap.limits: caps]'),
           "SETS: 'cap.limits' is a list of pairs; a set draws from words, strings and numbers"),
    reject('R25', 'Art. 1 explainability: a refusal is traceable by a stable identifier, so a PATTERN carries a CODE',
           BASE + 'DEFINE NARRATE voice AS (SAYS [use: "{name} wants {wants}."], REFUSES "Stopped at line {line}: {message} ({cites})") RATIONALE "x"\n' +
           pat('p') + 'DEFINE CONSTITUTION charter AS (ARTICLES [explainability]) RATIONALE "x"\n',
           "Art. 1 explainability: PATTERN 'p' carries no CODE"),
]
doc = {
    'grammar': 'haro', 'version': '0.32',
    'comment': ('Written BEFORE any code reads a PATTERN (the W discipline). v0.32 is BLOCKS.md 4.3 and Central\'s item 3, the value join: a fact across '
                'declarations, said once as a pattern over a seat, judged by the pattern engine of v0.31. DEFINE PATTERN name AS (OVER kind.seat, MATCH [ rule ], '
                'SETS [kind.seat: set], MESSAGE, CODE, CITES, SEVERITY). The module docstring of gen_fixtures.py states the design each fixture pins. '
                'A1-A6 accept; R1-R27 refuse, each by the fragment of why. R7-R12 are the bound and the names, the pattern engine\'s own words in the meta-court\'s '
                'mouth; R25 is the pattern joining Art. 1.'),
    'accepts': accepts, 'rejects': rejects,
}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')

# ---- the court's cases: grants_v32.haro and spike/grants/*.grant ----------------------------------------------------------------
MSG_WANTS = 'USE report wants a right no ZONE grants'
cases = [
    {'id': 'G1', 'name': 'the clean sentence: one zone, one use, every right asked for is granted', 'verb': 'check', 'args': ['grants/clean.grant'], 'first': 'ok', 'counts': {'ZONE': 1, 'USE': 1}},
    {'id': 'G2', 'name': 'the meta-court reads the world: four patterns, a menu, a form, two declarations', 'verb': 'meta', 'args': ['grants_v32.haro'], 'first': 'ok',
     'contains': ['patterns 4', 'menus 1', 'forms 1', 'declarations 2']},
    {'id': 'G3', 'name': 'the value join on a list: a right no zone grants is refused at its WANTS clause, in the declared words', 'verb': 'check', 'args': ['grants/ungranted.grant'],
     'refused': True, 'contains': ['grants (line 8): ' + MSG_WANTS]},
    {'id': 'G4', 'name': 'the envelope: the pattern\'s code and the cite it declares', 'verb': 'diagnose', 'args': ['grants/ungranted.grant'],
     'diagnose': {'code': 'RIGHT_NOT_GRANTED', 'cites': ['right:granted-by-a-zone']}},
    {'id': 'G5', 'name': 'the value join on one value, a rule another pattern uses by name: the primary right is refused at its PRIMARY clause (line 9)', 'verb': 'check',
     'args': ['grants/primary_ungranted.grant'], 'refused': True, 'contains': ['grants (line 9): USE report needs a right most, and no ZONE grants it']},
    {'id': 'G6', 'name': 'a set with no member: no zone, so the right asked for is granted by no one', 'verb': 'check', 'args': ['grants/no_zone.grant'], 'refused': True,
     'contains': ['grants (line 4): ' + MSG_WANTS]},
    {'id': 'G7', 'name': 'a list judged against a MENU\'s words: a channel the menu lacks is refused at its VIA clause (line 9)', 'verb': 'check', 'args': ['grants/bad_channel.grant'],
     'refused': True, 'contains': ['grants (line 9): USE report goes through something that is no channel']},
    {'id': 'G8', 'name': 'CITES none: the envelope carries the code and no cite', 'verb': 'diagnose', 'args': ['grants/bad_channel.grant'], 'diagnose': {'code': 'NOT_A_CHANNEL', 'cites': []}},
    {'id': 'G9', 'name': 'SEVERITY warning: the sentence stands and the pattern speaks after the verdict, with its code and line', 'verb': 'check', 'args': ['grants/many.grant'],
     'first': 'ok', 'counts': {'ZONE': 1, 'USE': 1}, 'contains': ['warning MANY_RIGHTS: USE report asks for more than three rights (line 8)']},
    {'id': 'G10', 'name': 'a warning is a warning in the envelope too, and a pattern with no CITES keeps the default rule:<CODE> (written with cites [] and corrected after the court spoke: v0.28 keeps the default where no CITES is declared, as a CONSTRAINT does)',
     'verb': 'diagnose', 'args': ['grants/many.grant'], 'diagnose': {'code': 'MANY_RIGHTS', 'cites': ['rule:MANY_RIGHTS'], 'severity': 'warning'}},
    {'id': 'G11', 'name': 'a set is the UNION of every zone\'s rights: two zones grant one right each, and a use may ask for both', 'verb': 'check', 'args': ['grants/union.grant'],
     'first': 'ok', 'counts': {'ZONE': 2, 'USE': 1}},
    {'id': 'G12', 'name': 'a seat the sentence does not write is not judged', 'verb': 'check', 'args': ['grants/absent.grant'], 'first': 'ok', 'counts': {'ZONE': 1, 'USE': 1}},
    {'id': 'G13', 'name': 'an empty list asks for nothing, and every right it asks for is granted', 'verb': 'check', 'args': ['grants/empty.grant'], 'first': 'ok', 'counts': {'ZONE': 1, 'USE': 1}},
    {'id': 'G14', 'name': 'two patterns refuse at once: diagnose carries both findings, each at its own line',
     'verb': 'diagnose', 'args': ['grants/two.grant'], 'contains': ['RIGHT_NOT_GRANTED', 'NOT_A_CHANNEL', '"line": 8', '"line": 9']},
    {'id': 'G16', 'name': 'a pattern judges the seat of its own kind only: a ZONE writes a PRIMARY the pattern over USE.primary would refuse, and it is not judged (added after the code, found by planting the kind filter off)',
     'verb': 'check', 'args': ['grants/zone_primary.grant'], 'first': 'ok', 'counts': {'ZONE': 1, 'USE': 1}},
    {'id': 'G15', 'name': 'a declaration the structural court refused is not judged again by a pattern: one finding, the shape\'s (added after the code, found by reading it)',
     'verb': 'diagnose', 'args': ['grants/shape_broken.grant'], 'contains': ['Clause WANTS takes a list of words'], 'lacks': ['RIGHT_NOT_GRANTED']},
]
cdoc = {
    'name': 'the grants world -- sentence-level cases for Haro v0.32 (DEFINE PATTERN, BLOCKS.md 4.3; Central\'s item 3, the value join)',
    'comment': ('Written BEFORE any court code reads a PATTERN. Each case runs the court forged from grants_v32.haro on haro AND on its checked build; the two must '
                'print the same bytes. The sentences are in grants/: clean, ungranted, primary_ungranted, no_zone, bad_channel, many, union, absent, empty, two, shape_broken, zone_primary. '
                'A refusal is at the line of the clause it is about (WANTS line 8, PRIMARY line 9, VIA line 9, and line 4 in the zoneless sentence), not at the declaration\'s.'),
    'cases': cases,
}
with open(os.path.join(HERE, 'court_cases.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(cdoc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print(f'{len(accepts)} accepts, {len(rejects)} rejects; {len(cases)} court cases')
