# Haro v0.28 -- every element that carries a CODE may cite, and the word none (HARO-MENU-CITES-01)

**Written after `fixtures.json` and `court_cases.json` beside it, which are the judges** (the W
discipline: fixtures first, prose second; the fixtures are 2852d3b, before any court code). v0.28
answers the Principal's ruling of 2026-11-02 (LEDGER.md line 156, carried by Central to this desk at
01:08): *an envelope cites only what exists; a MENU may carry CITES as a CONSTRAINT does; where the
contract binds nothing, the cite is none, never `rule:<CODE>` for a rule that does not exist.* The form
and the version were left to this desk. It is the twenty-eighth rung (charter D38). v0.28 refuses
nothing v0.27 accepted except one spelling no estate file wrote -- an empty `CITES []` -- and that
reversal is named (R2, HF-132).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `CITES` on `MENU`, `RANGE`, `FORMAT` and `UNION` | the instruments the element's refusal enforces, `kind:value` as every cite since v0.11, replacing the default `rule:<CODE>` (or `rule:<name>` without a CODE) in the envelope (A1, A3; N4, N6, N7, N8) | the ruling names the MENU; the reason it gives -- an envelope cites only what exists -- holds for every element that carries a CODE, so the four take CITES together. A RANGE would have been stzzui's next question |
| `CITES none`, on all seven elements that cite | the refusal cites nothing: the envelope's `cites` is `[]`, which the Diagnostic Contract calls honest where no law applies (2.5) (A2; N3, N9, N10, N14) | the ruling's own word, "none", and the machine language's own idiom for EGRESS: "a list names where the machine may go, and the word none says it goes nowhere" |
| `CITES []` | **refused**: "an empty CITES says nothing: a list names what the refusal cites, and the word none says it cites nothing" (R1, R2, R3) | before v0.28 the empty list meant **two things**: the default `rule:<name>` on a CONSTRAINT and a SYMBOL (the court read an empty list as absent), and nothing at all on a REFUSAL (whose default is no cite). One spelling, two meanings, silently -- HF-132. v0.28 retires the spelling; no `.haro` file in this repository or in stzzui wrote it (searched) |
| no `CITES` clause | the default, unchanged: `rule:<CODE>`, or `rule:<name>` without a CODE, as every court has cited since v0.11 (A4; N5) | the forge emits a cites element in a court's row only when the element declares one, so **a language that declares no CITES forges the bytes it forged before**: the ten committed courts re-forged on v0.28 are byte-identical to HEAD |
| a word other than `none` | refused: "CITES is a list of cites or the word none, not 'nothing'" (R4) | one exact spelling |

What does not change: a DECLARATION still carries no CITES (R7) -- its seats are coded by CODES and their
refusals (REQUIRED, DANGLING) cite `rule:<kind.seat>`, the language's own rule; a cite per seat is not
built here. `check` speaks as it did (N12): cites live in the envelope and the voice, never on the refusal line.

## Grammar (EBNF), the v0.27 text with these additions

```
MENU:        WORDS name_list, MESSAGE string, CODE string, CITES cites
RANGE:       MIN number, MAX number, MESSAGE string, CODE string, CITES cites
FORMAT:      SHAPE ident, FOLD ident, MESSAGE string, CODE string, CITES cites
UNION:       OF type_list, MESSAGE string, CODE string, CITES cites
CONSTRAINT, REFUSAL, SYMBOL:  CITES cites                         -- was string_list
cites      = "none" | "[" cite { "," cite } "]" ;                 -- never "[]"
cite       = string ;                                             -- "kind:value", kind rule | article | right | pattern
```

The meta-court prints nothing new on acceptance; the record of a menu, a range, a format and a union keeps
its cites after its code, and a cites value is a list or the string `"none"`. The forged court's row
carries the element's cites after its code only when declared (`CitesTail` in forge.ring); a constraint,
a refusal and a symbol carry theirs always, `"none"` among them (`CitesSource`). The court reads them in one
place for the four (`CtElementCites`) and beside the code for the other three.

## The world judged: a public notice

`notice_v28.haro` declares a notice an office or a desk puts out, and a contract that binds four things
and not the rest: the media (rule 4), the issuer (rule 2), the length (a reader's right) and the archive's
path (a pattern) -- and nothing about the tone, a letter's urgency, an unknown verb or a regulation the
town's register lacks. So the tones menu, the urgency constraint, the unknown-verb refusal and the
regulations symbol cite none; the audiences menu declares no CITES and keeps the default; the rest cite
what binds them. `notice/` holds the sentences and the register. `court_cases.json` is judged by
`haro_forge.py --stage=34` on rnxc and on the oracle, byte-identical:

| case | what | holds |
|---|---|---|
| N1, N2 | the clean notice is a sentence; the meta-court reads the world | ok |
| N3 | a MENU that cites none: `INVALID_TONE`, `cites []` -- stzzui's first case | ok |
| N4 | a MENU that cites what binds it: `rule:4`, never `rule:UNKNOWN_MEDIUM` | ok |
| N5 | a MENU without CITES keeps `rule:UNKNOWN_AUDIENCE` | ok |
| N6, N7, N8 | a RANGE, a FORMAT and a UNION cite their right, pattern and rule | ok |
| N9 | a CONSTRAINT that cites none -- which v0.23 to v0.27 could not say | ok |
| N10 | a REFUSAL that cites none: the envelope a REFUSAL without CITES already gave | ok |
| N11 | the voice tells a refusal with its cite: `(UNKNOWN_MEDIUM; rule:4)` | ok |
| N12 | `check` speaks as it did | ok |
| N13, N14 | a regulation the register holds resolves; one it lacks is refused under the SYMBOL's code with no cite | ok |

**Results.** 12 of 12 meta fixtures and 14 of 14 cases, rnxc and the oracle byte-identical (stage 1's v0.28
row and stage 34).

## What building it found, recorded (HF-132)

1. **The empty list meant two things** (above). Found writing R2 and R3, by reading what each reader of
   cites does with `[]` before writing what v0.28 should do with it: three readers, two answers.
2. **A fixture sentence was spelt wrong once, the judgement right.** N10's sentence first read `DEFINE
   BULLETIN ...`, which the court refuses as an unknown DECLARATION (`unknown_declaration`), not an unknown
   verb: `unknown_verb` is a top-level word that is not `DEFINE`. The sentence now reads `BULLETIN ...`;
   the case's judgement (`UNKNOWN_VERB`, `cites []`) is the one written before the court. Said here so the
   correction is not mistaken for a fixture adapted to pass.
3. **N13 and N14 were added after the court.** Listing which reader of cites each case reaches showed
   that none reached `world_lib.ring`'s `CtSymbolCode`, so the SYMBOL's `none` was changed in code no case
   judged. The notice gained an optional `FOLLOWS` seat typed by a SYMBOL that cites none, and two cases
   against `notice/register.json`. A guard is judged by which code its cases reach, not by how many there are.
4. **Each protection is load-bearing**: eight switched off in turn, each failing the guard for its own
   reason -- the forge's `CitesTail` (N3, N4, N6, N7), the court's `CtElementCites` (the same), the
   constraint's `none` (N9), the refusal's (N10), the symbol's (N14), the forge's constraint row (N9),
   the empty list accepted (R1, R2, R3), any word for none (R4); every file restored and checked.
5. **The ten committed courts and their grammars re-forge to HEAD's content** on v0.28 (machine, fleet,
   w, z, f, a, stzv, n, ledger, bank, clinic): a language that declares no CITES forges what it forged.
   The full guard was not run: the CPU was held at 21% of its rated speed (`bench/heartbeat.py`), where
   stage 6's timing cannot be measured. The stages this change can reach were: 1 (every version's meta
   fixtures), 13, 14, 17, 29 to 34, on both runtimes.

## Refused here

- No cite per seat of a DECLARATION: a REQUIRED or DANGLING refusal still cites `rule:<kind.seat>`, the
  language's own rule. If a pinned instrument binds a seat, that is a clause of its own.
- No change to the default: an element without CITES cites its own code, so RingFlex's and every other
  court's envelopes are unchanged. Whether a language under a pinned instrument must declare CITES on every
  coded element -- as Art. 1 makes every refusal carry a CODE -- is a rule nobody has asked for; not built.
- No change to the voice: `{cites}` is the comma-joined list, so a refusal that cites none tells an empty
  `{cites}`; the template is the maker's.
