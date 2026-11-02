# Haro v0.27 -- the field tag: a pair form's mark, PERSONAL reaching it, SAFEGUARDS on the ask and the voice (ZTAG)

**Written after `fixtures.json` and `court_cases.json` beside it, which are the judges** (the W
discipline: fixtures first, prose second). v0.27 answers the author's yes of 2026-11-02 to
CONSTITUTION-ZTAG-01 -- "should Z's field form carry a tag, so that `member: text` is personal at the
sentence and the weaves judge it there?" -- the question ZC5 left open (HF-130). It is the first rung
after the constitution plane's charge, built by the same desk on the same discipline, and recorded as
the twenty-seventh rung (charter D37). v0.27 refuses nothing v0.26 accepted: A4 is v0.26's A1 unchanged,
and the tontine's sixteen cases, twenty-five questions and twenty-two told questions are judged as before.

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| a pair form's third seat: `DEFINE FORM field AS (SEATS [name: name, type: name, tag: tags?])` | a pair form (a name and a scalar, written as `a: b`) may carry a third, optional seat typed by a MENU -- the mark -- and a sentence writes it after the value: `member: text personal`. A mark the MENU does not know is refused in the MENU's words with its CODE (Y6, Y7); a mark on a form that takes none is refused by name | the author's words: a tag on the field form, where zing's grammar will read it. The MENU is the world's: `tags` (plain, personal, confidential) is stzFieldTags' pair of tags plus the plain word, Zin's classifications |
| `PERSONAL [entity.fields.tag]`, a three-part path | `decl.seat.mark`: the seat is a list of a pair form, the mark its MENU seat, and that MENU can say `personal` (R3, R4, R9). Every field a sentence marks personal or confidential is a personal datum at the record level; `check` names them -- `personal member` -- in the order the sentence writes them (Y1, Y8) | v0.25's two-part path names a seat whose VALUE is personal (a patient's name); the three-part path names the seat that MARKS which fields are. HF-130 found Z had no seat of the first kind; this is the second kind |
| `SAFEGUARDS [ask: consent, voice: redaction]` | what each path out of the world declares, in stzFieldTags' five words (R5): the ask takes `consent` or `anonymisation` (R6), the voice takes `redaction`; the paths Haro governs here are those two, the model path staying stzlib's and HaroBase's (R8); SAFEGUARDS without privacy among WEAVES is refused (R7) | v25/GRAMMAR.md's "Refused here" named the safeguards as "ZC5's question for the tontine"; here they are, as the escapes Zin's W4.2 and W4.4 give |
| the weaves over the marks | **W4.2**: a language with an ASK and a mark path declares a safeguard for the ask path, or is refused at constitutional (R1), warned at governance (A3), noted at advisory; **W4.4**: a voice that TELLS `{rows}` declares redaction for the voice path, or the same (R2, A3). **W3.1 stays silent on a mark**: the WORLD publishes the entity's SHAPE, marks included -- a schema moves no datum | the three paths of v0.25, judged where the datum is: a question's answer and a told answer carry rows; a published symbol carries a span and a rationale |
| the forged court applies what it can | under `ask: anonymisation` the `ask` verb answers with the marked fields `[personal]`; under `ask: consent` it answers whole, as zing answers (Y4); under `voice: redaction` `narrate-ask` tells the answer's rows with the marked fields `[personal]` (Y5, Y9). The voice's SAYS line for the entity still says `member -> text`: the shape, not the datum (Y3) | redaction and anonymisation are the two safeguards a court can APPLY; consent is a claim the world makes and the court records (`meta` prints `safeguards ask:consent,voice:redaction`) |

## Grammar (EBNF), the v0.26 text with these additions

```
FORM:          SEATS [name: type, name: type, name: MENU?]      -- a pair form's optional mark seat
pair          = ident ":" (ident | string | number) [ident] ;    -- the mark after the value (z.gbnf, only
                                                                   where a pair form has a mark seat)
CONSTITUTION:  PERSONAL path_list                                -- a path decl.seat or decl.seat.mark
               SAFEGUARDS pair_list                              -- ask: consent | anonymisation, voice: redaction
```

The meta-court prints one line more on acceptance, `safeguards` (as `path:word`, comma-joined). Every
forged court is born with `$aCourtMarks` and `$aCourtSafeguards`, so the ten committed courts were
regenerated (HF-127's rule, kept); only `z.gbnf`'s `pair` rule changed among the grammars.

## The world judged: the tontine, tagged

`z_v27.haro` is `z_v26.haro` plus the MENU `tags`, the mark seat on `field`, `PERSONAL [entity.fields.tag]`
and `SAFEGUARDS [ask: consent, voice: redaction]`: the members consented to the circle's ledger, so the
treasurer's question is answered whole, as zing answers it; what the voice tells leaves the circle, so it
leaves redacted. `tontine.z` gained one word, `personal`, on its member field. `v27/court_cases.json` is
judged by `haro_forge.py --stage=33` on rnxc and the oracle:

| case | what | holds |
|---|---|---|
| Y1, Y2 | the tagged tontine is a sentence, zing's counts unchanged, `personal member` named; the meta-court reads the mark path and the safeguards | ok |
| Y3 | the voice's shape line unchanged: `member -> text` | ok |
| Y4 | the ask under consent: `SELECT * FROM collect WHERE round = 1` answers Aminata and Moussa whole, Fatima filtered | ok |
| Y5, Y9 | the voice under redaction: the same answer told with `"member": "[personal]"`, no name in the output; two marks, both redacted | ok |
| Y6, Y7 | `member: text secret`: refused in the MENU's words, code TAG | ok |
| Y8 | `member` personal and `amount` confidential: `personal member, amount` | ok |
| Y10, Y11 | the runtime unchanged; v0.26's declaration still accepted | ok |

**Results.** 14 of 14 meta fixtures (5 accepts, 9 rejects) and 11 of 11 cases, rnxc and the oracle
byte-identical; stages 9, 10, 13, 14, 19 and 32 pass on the regenerated Z (zing's 16 cases and 25
questions unchanged; the 22 told questions now told with the member redacted, which the law of stage 19
reads off the sentence's marks and the declaration's safeguards); stages 1 to 5, 11, 12, 15 to 18, 21 and
29 to 31 pass.

## What building it found, recorded (HF-131)

1. **The fixture was wrong once, the court right.** R1 was written under `ARTICLES [explainability]`
   with no NARRATE, so Art. 1 refused it before the weave could -- the fixture's own declaration broke
   another article. It stands under `trust_hierarchy`, the one article a bare world satisfies, and the
   refusal it asks for is unchanged. Said in the fixture file's comment.
2. **A law that reads the sentence.** Stage 19's told answers had been checked against zing's rows to the
   byte; with the voice under redaction the told rows carry `[personal]` where the sentence marks a
   field. The law now reads the marks off the sentence and the safeguard off the declaration, and
   redacts zing's rows before comparing -- the fixture (zing's answers) unchanged, the law stated.
3. **Consent is why zing's pin holds.** Had the tontine declared `ask: anonymisation`, the court's `ask`
   would answer redacted and stage 10's comparison with zing's own answers would have to learn the same
   law. The tontine declares consent, which is also the true thing about a circle whose treasurer keeps
   its ledger; a world that wants anonymisation says so and its questions answer redacted (A2).
4. **A schema is not a datum.** The WORLD publishes `entity` with its fields and their marks; W3.1 does
   not fire on a mark, and the voice's `member -> text` line is kept, because a shape leaves no person's
   datum. What leaves are rows, and rows are what the two safeguards govern.

## Refused here

- A fourth seat, or a mark on a form that is not a pair form: the mark is written after a pair's value and
  nowhere else, so zing's grammar learns one shape.
- Retention and on_premise as Haro safeguards: the log's retention is stzlib's `:log` path, the model's
  on_premise is HaroBase's grant and stzlib's `:model` path (D35). Named in R5's list so the word is
  known, refused on Haro's two paths so nothing is accepted by silence.
- A default safeguard: a world under privacy that marks a field and declares nothing is refused, warned
  or noted at its own severity, never answered whole in silence.
