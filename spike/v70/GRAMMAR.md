# Haro v0.70 -- a program judges

TYPES.md T7, the first step of its first rung (D83, D84, D85): **a sentence of a declared language is a value of that language's type,
and only its court makes one.** A program loads a language's declaration, asks the language to judge a text, and holds what the court
made.

    load "signal.haro"                       # the declaration: its first word is DEFINE
    sLamp = signal.Judge(tText)              # a sentence, or the court's refusal raised
    print sLamp                              # its text
    print sLamp.Language()                   # with Version(), Text() and Warnings()

Fixtures first (0c3e86a: 13 cases over two small languages written for them, `signal` and `gate`; 0 of 13 before the code). The Haro
side d1457a9, the code df2f25e, the court's last cases and the plants 98ec805.

| line | what | cases |
|---|---|---|
| L1 | `load` of a declaration makes its language's name a type's name: `signal.Judge(tText)` answers a sentence, which prints as its text | J01 |
| L2 | a sentence answers `Language()`, `Version()`, `Text()` and `Warnings()` | J02 |
| L3 | a text the court refuses raises the court's refusal: its code and its message; uncaught, it stops the run | J03, J04, J05 |
| L4 | the letter `s` holds a sentence and nothing else | J06, J07 |
| L5 | a sentence is not edited: its text is taken, changed and judged again, and the first sentence stands | J08 |
| L6 | a write into a sentence is refused (SENTENCE_FIXED) | J09 |
| L7 | two languages in one program, each judged by its own court | J10 |
| L8 | THE LAW: what `Judge` answers is what the language's own forged court answers, standing alone, on the same text | every case that judges |
| L9 | a name that is no loaded language judges nothing | J11 |
| L10 | `haro check` of a program that judges reads no error | J12 |
| L11 | the declaration is judged when the program is compiled: one the meta-court refuses stops the program, in the meta-court's words | J13 |
| L12 | the compiled image is kept as any program's is, and an edited declaration is forged again | J14 |
| L13 | a sentence is made by its court alone: `new` of one is refused when compiling | J15 |

## The court

`sentence_court.py` runs each case on both builds. For L8 it forges each language's court with the build under test and runs it
standing alone, as `haro <language>_court.haro diagnose <file>`, on every text a case judges: the fixture's verdict must be that
court's. So a program's `Judge` is held to what the standalone court says, and L8 held on v0.69 before a line of the code.

## How it is built

- **The court a program holds is the forge's own output.** The loader (`haro.zig`) reads a loaded `.haro` file whose first word is
  DEFINE as a declaration: it runs this same haro as a child on `forge.haro` in the forge's folder, and the file's place in the unit is
  taken by three lines -- load `judge_lib.haro`, load the forged court, say the language is loaded with its version. The forged court
  is kept in the cache folder under a name made of the declaration's bytes, this haro and the forge's three files, so an edit to any
  of them forges again. The forge's folder is `HARO_HOME`, or `spike` three folders above the executable.
- **A refused declaration.** When the forge answers the meta-court's refusal, the file's place is taken by nothing that runs and the
  refusal stands at the meta-court's own line of the declaration, in its words; `haro check` lists it there.
- **The language's name.** In a file that loads a declaration, `<language>.Judge(` reads `HaroLang("<language>").Judge(`: two
  insertions around the name, outside every text and comment. No word is reserved, and a name that is no loaded language is what it
  always was.
- **`judge_lib.haro`** stands between the program and the court: it keeps each loaded language's tables under its name, puts them
  back before a text is judged, and answers a `HaroSentence` or raises the court's first refusal as the VM raises a coded error,
  `Error (CODE) : message`, so `Code()` answers the court's code. `court_lib.haro` judges a text as it judges a file
  (`CtDiagnoseText`), and a court loaded by a program that judges has no main.
- **The VM** (`main.zig`) knows a sentence by its class: the letter `s` is checked and holds one alone, it prints as its text, and a
  write into one by an attribute's name is SENTENCE_FIXED once its court has made it. The compiler checks `s` as it checks every
  letter, and refuses `new` of a sentence outside the judging library.

## What the rung found

- **A plant that caught nothing found a way round the court.** A write into a sentence by its slot was refused as well as a write by
  its attribute's name; switched off, it failed no case. Looking for what else reaches a sentence found `new HaroSentence(...)`: held
  by an `x` name and then given to an `s` name, it passed the letter's check unjudged. `new` of a sentence is refused when compiling
  (J15), and the slot check, which no program reaches, was taken out.
- **Four expectations were typed before the code and changed after it**, each said in the generator. `Message()` answers the whole
  line the VM prints for a coded error, its code included, as for every error of the VM (J03, J05, J10). An uncaught refusal's first
  line is the judging library's, and the program's line stands in its call chain (J04). A name that is no language is a variable
  nobody assigned, R24 when it runs (J11). A refused declaration is named at its own line (J13).

## Measured

- The court: 15 of 15 on both builds. Fifteen plants, K1-K15, each caught by its fixture: eleven in `vm/src`, four in the two
  libraries, where nothing is built (`plants.py`).
- A program that judges, its image cache empty: 0.53 s for the first run, the forge and the compile in it; 0.02 s for the next, from
  the kept image; 0.2 s for the run after its declaration was edited.
- stzlib origin/main 8221cdcfd, its 195 landed `.haro` files: no name lettered `s` (1,683 lettered `t` by the same search), so the
  check of `s` refuses nothing there. `haro check` of each file alone, v0.69 against v0.70: 1,120 errors before and after, and no
  file changes.
- The 75-stage guard on builds made from the commit: 74 stages green in the full run, 1,927 s, stage 6 at 139.5 ms cold. Stage 36
  failed there on its pinned count of the spike's declarations -- 147, and 150 with this rung's three -- and passes with the count
  moved: 141 of 150 match, `dim.haro` being written to lack its RATIONALE.
- v0.47's Y09 named `s` as a letter not built yet; it names `w` now.

## What stands at its present size

- An uncaught refusal names the judging library's line first; the program's line is in the call chain under it.
- A finding's column on a line that holds `<language>.Judge(` counts the text the loader put in.
- `haro check` of a program that judges counts the court library's own warnings and notes with the program's; its errors are the
  program's.
- A haro outside the repository's `vm/` is told the forge's folder by `HARO_HOME`.
- The literal `panel"..."` and `of` are the next step; `unjudged` the rung after.
