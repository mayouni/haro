# Haro v0.71 -- the literal and `of`

TYPES.md T7, the second step of its first rung (D83 (4) and (5), D84, D86): a sentence written in a program is judged when the program
is compiled, and a definition says which language's sentence it takes and which it answers.

    load "signal.haro"
    sLamp = signal'DEFINE LAMP north AS (SHOWS green) RATIONALE "x"'    # a literal: judged when compiling
    func Show(psLamp of signal)                                        # takes a sentence of signal
    func Lamp(ptColour) of signal                                      # answers one

Fixtures first (28b54bc: 13 cases over v0.70's two languages; 0 of 13 before the code). The code 3a624a5; the last case, the plants and
stage 76 dde15f7.

| line | what | cases |
|---|---|---|
| L1 | a language's name with a text right after it is a literal: a sentence, judged when the program is compiled | Q01, Q02 |
| L2 | a literal its court refuses is refused when compiling, at its line, in the court's words; nothing of the program runs | Q03 |
| L3 | THE LAW: a literal's verdict is the one the language's own forged court answers, standing alone, on the same text | every case that judges |
| L4 | `of` on a parameter: a sentence of that language passes; a sentence of another is SENTENCE_OF_ANOTHER; a text is TYPE_LETTER, as for any `s` name | Q04, Q05, Q06 |
| L5 | `of` on a return: the definition answers a sentence of that language; a sentence of another is SENTENCE_OF_ANOTHER, anything else SENTENCE_EXPECTED | Q07, Q08, Q09 |
| L6 | `of` names a language the file loads, and has one place, a definition's header | Q10, Q14 |
| L7 | no word is reserved: a method named `Of` is a name, and `of` in a text or a comment is what it was | Q11 |
| L8 | `haro check` lists a refused literal and reads no error where the literals and declarations hold | Q01, Q03, Q04, Q11 |
| L9 | a finding on a line that holds a literal or `<language>.Judge(` stands at the file's own column | Q12, Q13 |

The text of a literal is in any of Haro's three quotes, right after the language's name, with no space.

## The desk's readings (D86, under D84)

- **A literal is judged twice by the same court**: when the program is compiled, so a refused one stops the program before a line
  of it runs, and again where it stands when the program runs, since a sentence is made by its court alone (v0.70, J15). It reads
  `<language>.Judge(<text>)`.
- **This step builds `of` on a parameter and on an answer.** An attribute's `of`, D83's third place, comes with a later step; away
  from a header `of` is refused by name.
- **SENTENCE_EXPECTED is an answer's.** A text given to a parameter lettered `s` is TYPE_LETTER, as it is for every `s` name; an
  answer has no letter, so a definition `of` a language that answers a text is SENTENCE_EXPECTED. The empty text is no answer and
  passes, as it passes every letter.

## How it is built

- **The loader's pass** (`haro.zig`, `languageSugar`) reads a file that loads a declaration, outside every text and comment. A
  language's name followed by `.Judge(` or by a quote is given `HaroLang("...")` around it, and a literal `.Judge(` and `)` around
  its text. Each literal is judged there: the language's forged court is run as a child on the text, standing alone, and its first
  refusal becomes the file's fault -- the program's first statement is refused with it, at the literal's line.
- **`of`**: on a line that opens a definition, `of <language>` is blanked, so the parser reads the header without it, and kept as a
  mark -- the header's row, the parameter it follows or none for the answer, the language. `of` before a word that is no language of
  the file, and `of <language>` anywhere else, are the file's fault.
- **The lift** (`lift.zig`, `findOf`) writes the checks from the marks, in the tree: `HaroOfGiven(name, "language", "name")` after
  the brace it gave the header, and `HaroOfAnswer(..., "language", "Name")` around what each `return` of the definition gives -- a
  nested definition's returns left alone. A check that could not be written refuses the program by name.
- **Columns.** What the loader's pass puts in is kept as inserts in the file's coordinates and merged with the lift's, so the checker
  names the file's own column on such a line. v0.70 left it shifted by the text put in.
- **`judge_lib.haro`**: `HaroOfGiven` and `HaroOfAnswer` raise SENTENCE_OF_ANOTHER and SENTENCE_EXPECTED as the VM raises a coded
  error.

## What the rung found

- **A plant that caught nothing, again.** Reading `of` away from a header failed no case when switched on, because no case said what
  `of` is there. It is refused by name (Q14).
- **A refusal of a malformed header drew a second one.** `(psLamp of lamp)` was read by the parser as three parameters, and the
  compiler refused `of` for having no letter beside the fault that named the real cause. `of` and the word after it are blanked
  there too, and the fault is the one finding of its line.
- **One expectation changed after the code**, said in the generator: the refusal of a literal quotes its text in its quotes, as it
  stands in the file (Q03).

## Measured

- The court: 14 of 14 on both builds. Eleven plants, P1-P11, each caught by its fixture: eight in `vm/src`, three in the judging
  library, where nothing is built (`plants.py`).
- v0.70's court holds on v0.71's builds: 15 of 15.
- stzlib origin/main 8221cdcfd, its 195 landed `.haro` files, `haro check` of each alone, v0.70 against v0.71: 1,120 errors before
  and after, no file changes. No file there loads a declaration, and such a file is read as it was.
- The 76-stage guard on builds made from the commit: 75 stages green in the full run, 2,285 s. Stage 6, the cold-load timing, read
  187.5 ms there on a machine running on battery -- the native court beside it read 11.9 ms where it reads 9.7 -- and, run again
  alone and alternated three times, 139.5, 136.6 and 134.8 ms on v0.71 against 133.3, 138.2 and 143.0 on v0.70, under the 150 ms
  ceiling.

## What stands at its present size

- A literal's court is run once for each different literal of a file when it is compiled, as a child process.
- A refusal raised by a check of `of` names the judging library's line first, and the program's line in its call chain.
- A definition `of` a language that ends without a `return` answers nothing, and nothing is checked.
- `of` on an attribute, and `unjudged`, are the next steps.
