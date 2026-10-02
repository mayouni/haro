# Haro v0.13 -- NARRATE: the court's voice

**Written after `fixtures.json` and `narration_cases.json` beside it, which are the judge**
(the W discipline: fixtures first, prose second). v0.13 is the declaring altitude of Haro
grown by the last row of the charter's section 3 that no rung had built: "`NARRATE` -- how a
run of the language is narrated back (stzn); the court's voice". stzn is the seventh name of
the family sentence: "stzu is you speaking to the machine, stzn is the machine speaking
back" (stz `CLAUDE.md`); its v0 renders `narrations/index.html` from every run and stores
nothing. Principle 8 of `haro/PRINCIPLES.md` rules the relation: "the narration (stzn) is a
projection from programs and runs, never parsed back". v0.13 refuses nothing v0.12
accepted (fixture A2 is v0.12's A1).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `NARRATE`, at most one per language | the language's voice | a language has one voice (R3) |
| `SAYS [kind: "template", ...]` | a template per declaration kind, kind by name | required: a voice that says nothing narrates nothing (R7). The kind must be declared (R1) and voiced once (R6). A template fills `{name}`, `{verb}`, `{rationale}`, `{line}` and any seat of its kind (R2) -- never a seat the kind lacks, because a narration that names a seat the sentence cannot hold would lie about its own source; every brace closes (R4) |
| `OPENS "..."` | the line before the declarations | fills `{language}`, `{file}` (the file's name, no directory) and `{count}` (R5: `{name}` is refused here, nothing has been named yet) |
| `ENDS "..."` | the line after | the same placeholders as OPENS |
| `REFUSES "..."` | the one line when the court stops | fills `{language}`, `{file}`, `{line}`, `{code}`, `{message}` and `{cites}` -- the line, message, code and cites the envelope of v0.11 gives the same verdict |

## Grammar (EBNF), the v0.12 text with this addition

```
NARRATE:     OPENS string, SAYS message_list, ENDS string, REFUSES string
message_list = "[" IDENT ":" STRING { "," IDENT ":" STRING } [ "," ] "]" ;
```

## What the forge makes of it

A court whose language declares a NARRATE loads `narrate_lib.ring` (and nothing else new)
and gains one verb:

```
<lang>_court.ring narrate <file>      the sentence, narrated back in the language's own voice
```

The opening, then one sentence per declaration in file order, then the ending. A kind the
voice does not speak is narrated plainly -- its verb, its name and the author's own reason
(`task a_cote: ...`) -- because the rationale is mandatory on every declaration (C6 3.8), so
a narration never drops it. A sentence the court refuses is narrated as the refusal alone.
An opening, ending or refusal the voice leaves out takes the court's plain words.

**Two laws of the estate keep it honest, and the court is built to them.** The StzNarration
law: a narration is a rendering of a real run, never stored, the plain-text sentence being
the document -- the court prints to stdout, writes no file, and has no verb that reads a
narration back, so a narration handed to `check` is simply refused as the nonsense it is.
And stzn's honesty guard, which `narrate.luau` states in its own header ("a narration that
uppercases `Lowercased('RING') is ring` would lie about its own output"): a placeholder is
filled with the sentence's own text, verbatim, never uppercased, trimmed or rephrased. A seat
a sentence left out fills as nothing; a list seat fills as its items joined by `, `, a pair
list as `key -> value`.

## Measured

`f_v13.haro` is `f_v11.haro` with a voice: the workflow, the actor, the invocation and the
terminal are spoken -- "go invokes the flow do_it; committed it goes to fini, rejected to
refuse, held to refuse. One act, three endings routed." -- and the ten other kinds take the
plain default. The 27 F fixtures, the 16 + 25 Z cases, the 35 A cases, the world's nine
checks and the envelope's 28 codes are unchanged on it. The guard's stage 16 judges the
voice by laws read from the estate, by a checker that reads the source files in Python and
never asks the court what it said:

    hand-written    the smallest lawful workflow, narrated by hand BEFORE the court
                    (v13/narration_cases.json, 7 lines), is what the court prints
    honesty         5 lawful sentences narrated whole: every declaration named, every
                    rationale verbatim, 92 seat values verbatim, in order, the count right
    consistency     22 refused sentences narrated as the one line the envelope gives the
                    same verdict -- its line, its message, its code
    never parsed back   the narration is refused by `check`
    never stored        narrating changes no file in the folder
    one voice       a language that declares no NARRATE (z) refuses `narrate`
    the same bytes on rnxc and the oracle on every run

**The guard found a real weakness before the number was trusted.** The first version
narrated an unvoiced kind as its verb and name alone, and the honesty check -- every
rationale verbatim -- failed on three of the five sentences: the author's reason was being
dropped for every kind the voice did not speak. The default carries the rationale now. The
first version of the checker was also wrong, on its own: it read one DEFINE per line and the
fixtures wrap across lines; the court was right and the reader was fixed.

## What it does not do, named

- **No skin.** stzn v0's HTML, its RETRO and MODERN wardrobes, its tally and its law box
  are a rendering of the narration, not the declaration's job; they stay stzn's. The court
  gives the words, in order, as plain lines.
- **One language's voice.** A `SENTENCE` seat's language is judged in its own language but
  not narrated in its own voice; `narrate` speaks the first language's.
- **Sentences, not runs.** `narrate` narrates a sentence as the court judged it. Narrating
  a run of the algorithm letter (`run`) or an answer to a question (`ask`) is a later rung;
  the voice declared here is the part both would reuse.
- **No world warning.** `NO_WORLD` is the envelope's, and is not narrated.
