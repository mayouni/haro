"""Haro v0.70, sentences made when a program runs (TYPES.md T7, D83, D84): the cases of v70/fixtures.json and their files, written BEFORE
the code. Every expectation is typed here; the courts' words were read off the forged courts of the two languages below, standing alone.

  python spike/v70/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  `load` of a declaration makes its language's name a type's name: `signal.Judge(tText)` answers a sentence, and it prints as its text
  L2  a sentence answers Language(), Version(), Text() and Warnings()
  L3  a text the court refuses raises the court's refusal: its code and its message; uncaught, it stops the run
  L4  the letter `s` holds a sentence and nothing else
  L5  a sentence is not edited: its text is taken, changed and judged again, and the first sentence stands
  L6  a sentence's parts are not written (SENTENCE_FIXED)
  L7  two languages in one program, each judged by its own court
  L8  THE LAW: what `Judge` answers is what the language's own forged court answers, standing alone, on the same text
  L9  a name that is no loaded language judges nothing
  L10 `haro check` of a program that judges reads no error
  L11 the declaration is judged when the program is compiled: one the meta-court refuses stops the program at its `load`

CHANGED AFTER THE CODE, each said: J03, J05, J10 -- Message() answers the whole line the VM prints for a coded error, `Error (CODE) :
message`, as it does for every error of the VM (v0.37, E3), where the first text here gave the court's message alone. J04 -- the
refusal is raised in judge_lib.haro, so the run's first line is that file's and the program's line stands in the call chain; the first
text gave the program's line first. J11 -- `lamp` is read as a variable nobody assigned (R24 when it runs); the first text expected the
compiler to refuse the statement. J13 -- the refusal stands in the declaration, at the meta-court's own line (dim.haro, line 7); the
first text put it at the program's `load`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []
RULE = 'haro/refused-form'

SIGNAL = '''-- signal.haro -- a small language for v0.70's cases: a lamp shows one of three colours

DEFINE LANGUAGE signal AS (
  VERSION "1.2", GRAMMAR "1.0",
  COURT "spike/v70/fixtures.json",
  EXTENSION ".signal"
) RATIONALE "What a lamp may show, declared before it shows it"

DEFINE MENU colours AS (
  WORDS [red, amber, green],
  MESSAGE "A lamp shows red, amber or green",
  CODE "UNKNOWN_COLOUR"
) RATIONALE "The three colours a lamp may show"

DEFINE DECLARATION lamp AS (
  VERB "LAMP",
  SEATS [shows: colours, label: text?]
) RATIONALE "A lamp and the colour it shows"
'''

GATE = '''-- gate.haro -- a second small language: a gate stands open or shut

DEFINE LANGUAGE gate AS (
  VERSION "0.3", GRAMMAR "0.3",
  COURT "spike/v70/fixtures.json",
  EXTENSION ".gate"
) RATIONALE "Whether a gate stands open or shut"

DEFINE MENU states AS (
  WORDS [open, shut],
  MESSAGE "A gate is open or shut",
  CODE "UNKNOWN_STATE"
) RATIONALE "The two states of a gate"

DEFINE DECLARATION barrier AS (
  VERB "GATE",
  SEATS [state: states]
) RATIONALE "A gate and the state it stands in"
'''

# a declaration the meta-court refuses: its LANGUAGE carries no RATIONALE
DIM = '''DEFINE LANGUAGE dim AS (
  VERSION "1.0", GRAMMAR "1.0",
  COURT "spike/v70/fixtures.json",
  EXTENSION ".dim"
)

DEFINE DECLARATION bulb AS (
  VERB "BULB",
  SEATS [label: text?]
) RATIONALE "A bulb"
'''

for name, text in (('signal.haro', SIGNAL), ('gate.haro', GATE), ('dim.haro', DIM)):
    with open(os.path.join(HERE, 'cases', name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

GREEN = 'DEFINE LAMP north AS (SHOWS green) RATIONALE "open in the morning"'
AMBER = 'DEFINE LAMP north AS (SHOWS amber) RATIONALE "x"'
BLUE = 'DEFINE LAMP north AS (SHOWS blue) RATIONALE "x"'
CUT = 'DEFINE LAMP north AS (SHOWS green RATIONALE "x"'
SHUT = 'DEFINE GATE east AS (STATE shut) RATIONALE "x"'
M_BLUE = "A lamp shows red, amber or green, not 'blue'"


def said(code, message):
    """what Message() answers for a court's refusal: the line the VM prints for any coded error, `Error (CODE) : message`"""
    return 'Error (' + code + ') : ' + message


M_CUT = "Expected ',' or ')' after a clause, found 'RATIONALE'"
M_KIND = "Unknown kind 'LAMP': the kinds are closed (GATE)"


def case(cid, line, what, src, run, judged=None, check=None, ext='.haro'):
    """run: {'stdout': text} exact with exit 0; {'raises': text} a line the run prints, with {'never': text} it must not print;
    {'refuses': [row, reason, written]} the compiler's refusal; 'also' a second line the run prints. judged: [[language, text, code or
    None, message]] for L8. check: {'errors': n, 'found': [[row, rule]]} for the case's file, or [file, row, rule] for another."""
    name = cid.lower() + ext
    with open(os.path.join(HERE, 'cases', name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if judged is not None:
        c['judged'] = judged
    if check is not None:
        c['check'] = check
    cases.append(c)


case('J01', 'L1', 'a declaration loaded, a text judged, the sentence printed as its text', f'''load "signal.haro"
tText = '{GREEN}'
sLamp = signal.Judge(tText)
print sLamp
''', {'stdout': GREEN + '\n'}, judged=[['signal', GREEN, None, '']])

case('J02', 'L2', 'what a sentence answers', f'''load "signal.haro"
sLamp = signal.Judge('{AMBER}')
print sLamp.Language()
print sLamp.Version()
print sLamp.Text()
print Len(sLamp.Warnings())
''', {'stdout': 'signal\n1.2\n' + AMBER + '\n0\n'}, judged=[['signal', AMBER, None, '']])

case('J03', 'L3', 'a refused text raises the court\'s refusal, caught: its code and its message', f'''load "signal.haro"
try
    sLamp = signal.Judge('{BLUE}')
    print "judged"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'UNKNOWN_COLOUR\n' + said('UNKNOWN_COLOUR', M_BLUE) + '\n'}, judged=[['signal', BLUE, 'UNKNOWN_COLOUR', M_BLUE]])

case('J04', 'L3', 'uncaught, the refusal stops the run, and the program\'s line is in its call chain', f'''load "signal.haro"
sLamp = signal.Judge('{BLUE}')
print "judged"
''', {'raises': said('UNKNOWN_COLOUR', M_BLUE), 'also': 'Called from line 2 in file j04.haro', 'never': 'judged'}, judged=[['signal', BLUE, 'UNKNOWN_COLOUR', M_BLUE]])

case('J05', 'L3', 'a text that does not parse is refused with the court\'s PARSE', f'''load "signal.haro"
try
    sLamp = signal.Judge('{CUT}')
    print "judged"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'PARSE\n' + said('PARSE', M_CUT) + '\n'}, judged=[['signal', CUT, 'PARSE', M_CUT]])

case('J06', 'L4', 'a text literal given to an s name is refused when compiling', f'''load "signal.haro"
sLamp = '{GREEN}'
print sLamp
''', {'refuses': [2, 's is the letter of a sentence, and this literal is a text; written', 'sLamp']},
     check={'errors': 1, 'found': [[2, RULE]]})

case('J07', 'L4', 'a text given to an s name when the program runs is TYPE_LETTER', f'''load "signal.haro"
tText = '{GREEN}'
sLamp = tText
print "held"
''', {'raises': 'Line 3 Error (TYPE_LETTER) : `sLamp` is lettered s, a sentence, and is given a text', 'never': 'held'})

case('J08', 'L5', 'the text taken, changed and judged again; the first sentence stands', f'''load "signal.haro"
sFirst = signal.Judge('{AMBER}')
tNext = SubStr(sFirst.Text(), "amber", "red")
sNext = signal.Judge(tNext)
print sNext
print sFirst
''', {'stdout': AMBER.replace('amber', 'red') + '\n' + AMBER + '\n'},
     judged=[['signal', AMBER, None, ''], ['signal', AMBER.replace('amber', 'red'), None, '']])

case('J09', 'L6', 'a write into a sentence is refused, and the sentence is what it was', f'''load "signal.haro"
sLamp = signal.Judge('{AMBER}')
try
    sLamp.tText = '{BLUE}'
    print "written"
catch e
    print e.Code()
end
print sLamp
''', {'stdout': 'SENTENCE_FIXED\n' + AMBER + '\n'})

case('J10', 'L7', 'two languages, each judged by its own court; a lamp is no sentence of gate', f'''load "signal.haro"
load "gate.haro"
sLamp = signal.Judge('{AMBER}')
sGate = gate.Judge('{SHUT}')
print sLamp.Language()
print sGate.Language()
print sGate.Version()
try
    sWrong = gate.Judge(sLamp.Text())
    print "judged"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'signal\ngate\n0.3\nUNKNOWN_KIND\n' + said('UNKNOWN_KIND', M_KIND) + '\n'},
     judged=[['signal', AMBER, None, ''], ['gate', SHUT, None, ''], ['gate', AMBER, 'UNKNOWN_KIND', M_KIND]])

case('J11', 'L9', 'a name that is no loaded language judges nothing: it is a variable nobody assigned', f'''load "signal.haro"
sLamp = lamp.Judge('{GREEN}')
print "judged"
''', {'raises': 'Line 2 Error (R24) : Using uninitialized variable: lamp', 'never': 'judged'})

case('J12', 'L10', 'the checker reads a program that judges: no error', f'''load "signal.haro"
func Show(ptText)
    sLamp = signal.Judge(ptText)
    print sLamp.Language()
end
Show('{GREEN}')
''', {'stdout': 'signal\n'}, judged=[['signal', GREEN, None, '']], check={'errors': 0, 'found': []})

case('J13', 'L11', 'a declaration the meta-court refuses stops the program at its load, in the meta-court\'s words', '''load "dim.haro"
print "ran"
''', {'raises': 'every stzu declaration carries its RATIONALE (the commons, 3.8)', 'never': 'ran'}, check={'errors': 1, 'found': [['dim.haro', 7, RULE]]})

doc = {'version': '0.70', 'task': 'TYPES.md T7, rung 1: sentences made when a program runs', 'languages': ['signal', 'gate'],
       'law': 'what Judge answers is what the language\'s own forged court answers, standing alone, on the same text', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
