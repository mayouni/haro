"""Haro v0.71, the literal and `of` (TYPES.md T7, D83 (4) and (5), D84): the cases of v71/fixtures.json and their files, written BEFORE
the code. Every expectation is typed here; the courts' words are those of v0.70's two languages, `signal` and `gate`.

  python spike/v71/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  a language's name with a text right after it is a literal: a sentence, judged when the program is compiled
  L2  a literal its court refuses is refused when compiling, at its line, in the court's words; nothing of the program runs
  L3  THE LAW: a literal's verdict is the one the language's own forged court answers, standing alone, on the same text
  L4  `of` on a parameter: a sentence of that language passes; a sentence of another is SENTENCE_OF_ANOTHER; a text is TYPE_LETTER,
      as for any s name
  L5  `of` on a return: the function answers a sentence of that language; a sentence of another is SENTENCE_OF_ANOTHER, anything
      else SENTENCE_EXPECTED
  L6  `of` names a language the file loads: any other word there is refused when compiling
  L7  no word is reserved: a method named Of is a name, and `of` in a text or a comment is what it was
  L8  `haro check` lists a refused literal and reads no error in a program whose literals and declarations hold
  L9  a finding on a line that holds a literal or `<language>.Judge(` stands at the file's own column

CHANGED AFTER THE CODE, said: Q03 -- what the refusal quotes is the literal's text in its quotes, as it stands in the file; the
first text here quoted the language's name with it.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
V70 = os.path.join(os.path.dirname(HERE), 'v70', 'cases')
cases = []
RULE = 'haro/refused-form'

# the two languages of v0.70's cases, the same bytes
for name in ('signal.haro', 'gate.haro'):
    with open(os.path.join(V70, name), encoding='utf-8', newline='') as f:
        text = f.read()
    with open(os.path.join(HERE, 'cases', name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

GREEN = 'DEFINE LAMP north AS (SHOWS green) RATIONALE "open in the morning"'
AMBER = 'DEFINE LAMP north AS (SHOWS amber) RATIONALE "x"'
BLUE = 'DEFINE LAMP north AS (SHOWS blue) RATIONALE "x"'
SHUT = 'DEFINE GATE east AS (STATE shut) RATIONALE "x"'
M_BLUE = "A lamp shows red, amber or green, not 'blue'"


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, judged=None, check=None):
    """run: {'stdout': text} exact with exit 0; {'raises': text} a line the run prints, with 'never' a line it must not print;
    {'refuses': [row, reason, written]} the compiler's refusal. judged: [[language, text, code or None, message]] for L3. check:
    {'errors': n, 'found': [[row, rule]]} for the case's file, with 'cols': {row: column} where a column is pinned."""
    name = cid.lower() + '.haro'
    with open(os.path.join(HERE, 'cases', name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if judged is not None:
        c['judged'] = judged
    if check is not None:
        c['check'] = check
    cases.append(c)


case('Q01', 'L1', 'a literal is a sentence', f'''load "signal.haro"
sLamp = signal'{GREEN}'
print sLamp
print sLamp.Language()
''', {'stdout': GREEN + '\nsignal\n'}, judged=[['signal', GREEN, None, '']], check={'errors': 0, 'found': []})

case('Q02', 'L1', 'a literal where a value stands: an argument, and each of the three quotes', f'''load "signal.haro"
load "gate.haro"
func Show(psAny)
    print psAny.Language() + ": " + psAny.Text()
end
Show(signal'{AMBER}')
Show(gate`{SHUT}`)
''', {'stdout': 'signal: ' + AMBER + '\ngate: ' + SHUT + '\n'}, judged=[['signal', AMBER, None, ''], ['gate', SHUT, None, '']])

LIT_BLUE = "signal'" + BLUE + "'"
case('Q03', 'L2', 'a literal the court refuses is refused when compiling, and nothing runs', f'''load "signal.haro"
print "before"
sLamp = {LIT_BLUE}
print "after"
''', {'refuses': [3, 'the court of signal refuses this literal -- UNKNOWN_COLOUR: ' + M_BLUE + '; written', "'" + BLUE + "'"],
      'never': 'before'},
     judged=[['signal', BLUE, 'UNKNOWN_COLOUR', M_BLUE]], check={'errors': 1, 'found': [[3, RULE]]})

case('Q04', 'L4', 'a parameter of a language takes a sentence of it', f'''load "signal.haro"
func Show(psLamp of signal)
    print psLamp.Text()
end
Show(signal'{AMBER}')
Show(signal.Judge('{GREEN}'))
''', {'stdout': AMBER + '\n' + GREEN + '\n'}, check={'errors': 0, 'found': []})

case('Q05', 'L4', 'a sentence of another language given to it is SENTENCE_OF_ANOTHER', f'''load "signal.haro"
load "gate.haro"
func Show(psLamp of signal)
    print "shown"
end
try
    Show(gate'{SHUT}')
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'SENTENCE_OF_ANOTHER\n' + said('SENTENCE_OF_ANOTHER', '`psLamp` is a sentence of signal, and is given a sentence of gate') + '\n'})

case('Q06', 'L4', 'a text given to it is TYPE_LETTER, as for any s name', f'''load "signal.haro"
func Show(psLamp of signal)
    print "shown"
end
Show('{AMBER}')
''', {'raises': 'Error (TYPE_LETTER) : `psLamp` is lettered s, a sentence, and is given a text', 'never': 'shown'})

case('Q07', 'L5', 'a function of a language answers a sentence of it', f'''load "signal.haro"
func Lamp(ptColour) of signal
    return signal.Judge('DEFINE LAMP north AS (SHOWS ' + ptColour + ') RATIONALE "x"')
end
sLamp = Lamp("amber")
print sLamp
''', {'stdout': AMBER + '\n'})

case('Q08', 'L5', 'answering a sentence of another language is SENTENCE_OF_ANOTHER', f'''load "signal.haro"
load "gate.haro"
func Lamp of signal
    return gate'{SHUT}'
end
try
    sLamp = Lamp()
    print "answered"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'SENTENCE_OF_ANOTHER\n' + said('SENTENCE_OF_ANOTHER', '`Lamp` answers a sentence of signal, and answers a sentence of gate') + '\n'})

case('Q09', 'L5', 'answering anything else is SENTENCE_EXPECTED', f'''load "signal.haro"
func Lamp of signal
    return '{AMBER}'
end
try
    xLamp = Lamp()
    print "answered"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'SENTENCE_EXPECTED\n' + said('SENTENCE_EXPECTED', '`Lamp` answers a sentence of signal, and answers a text') + '\n'})

case('Q10', 'L6', '`of` names a language the file loads: another word there is refused when compiling', '''load "signal.haro"
func Show(psLamp of lamp)
    print "shown"
end
print "ran"
''', {'refuses': [2, '`of` names a language this file loads; written', 'lamp'], 'never': 'ran'}, check={'errors': 1, 'found': [[2, RULE]]})

case('Q11', 'L7', 'a method named Of is a name, and `of` in a text or a comment is what it was', f'''load "signal.haro"
class Box
    def Of(piN)
        return piN * 2
    end
end
oBox = new Box
# the double of four
print oBox.Of(4)
print "a lamp of signal"
sLamp = signal'{AMBER}'
print sLamp.Language()
''', {'stdout': '8\na lamp of signal\nsignal\n'}, check={'errors': 0, 'found': []})

case('Q12', 'L9', 'a finding on a line that holds a literal stands at the file\'s own column', f'''load "signal.haro"
sLamp = signal'{AMBER}' cName = "x"
print sLamp
''', {'refuses': [2, "`c` is Softanza's letter and no type's -- text is t: tName; written", 'cName']},
     check={'errors': 1, 'found': [[2, RULE]], 'cols': {'2': len("sLamp = signal'" + AMBER + "' ") + 1}})

case('Q13', 'L9', 'and so does one on a line that holds <language>.Judge(', f'''load "signal.haro"
sLamp = signal.Judge('{AMBER}') cName = "x"
print sLamp
''', {'refuses': [2, "`c` is Softanza's letter and no type's -- text is t: tName; written", 'cName']},
     check={'errors': 1, 'found': [[2, RULE]], 'cols': {'2': len("sLamp = signal.Judge('" + AMBER + "') ") + 1}})

doc = {'version': '0.71', 'task': 'TYPES.md T7: the literal and `of`', 'languages': ['signal', 'gate'],
       'law': 'a literal\'s verdict is the one the language\'s own forged court answers, standing alone, on the same text', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
