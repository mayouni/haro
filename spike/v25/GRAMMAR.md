# Haro v0.25 -- the first two weaves: sovereignty and privacy over the personal seats, the regime named

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.25 is the declaring altitude of Haro grown by the Haro slice of ZC4,
the constitution plane's cross-repository rung (on the author's "Start ZC4", 2026-11-02; charter
D35): the sovereignty (W3) and privacy (W4) weaves are judged over the `PERSONAL` seats a
constitution names, each at the severity its `WEAVES` clause declares, and every refusal names
the article it serves and the declared regime's own article -- never a default. A `CONSTRAINT`
gains `SEVERITY`. The stzlib and HaroBase slices of the same rung carry the model path (a field
tag that reaches a model) and the column flags; this file is Haro's. v0.25 refuses nothing v0.24
accepted (A3 is v0.24's A1, unchanged); v0.23's R13 and R16 were amended with this rung
(recorded in `v23/GRAMMAR.md`).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `PERSONAL [patient.full_name, ...]` on the `CONSTITUTION` | the seats whose values are personal data, as paths `decl.seat`, each a seat of a declared kind (R5); named without privacy or sovereignty among the weaves they are refused, not accepted by silence (R6) | Zin's `Zec.classification(pii)` on a field, read in Haro's shape: a seat is the field, and the constitution names which ones. The organizations that hold zones are a `MENU` of sectors; a personal seat is a text whose value no fixture carries as a real person's |
| `WEAVES [sovereignty: constitutional, privacy: governance]` judged | **W4.4** privacy: a personal seat told by the voice (`{seat}` in its kind's `SAYS` template) is a log that carries a personal datum; **W4.2** privacy: a kind holding a personal seat that the `ASK` asks is analytics over personal data without consent; **W3.1** sovereignty: a kind holding a personal seat that the `WORLD` publishes is a movement out of its zone. At `constitutional` the court refuses (R1, R2, R3); at `governance` it accepts and warns (A2); at `advisory` it accepts and notes (A4) | the three paths a language already declares (v0.13, v0.7, v0.10), and Zin's three severities (`ZIN_CONSTITUTIONAL_WEAVES.md` 3.3); the model path is not Haro's to judge here -- it is stzlib's field tags and HaroBase's column flags, the same rung |
| `REGIME gdpr` read | every weave refusal ends `[Art. 5 organizational_sovereignty; <regime>]`: `gdpr: Article 5(1)(e)` for W4.4, `gdpr: Article 7` for W4.2, `gdpr: Chapter V` for W3.1; `Niger Law 2017-28` for `niger_2017_28` (R8), the law Zin's African companion names; a regime Haro has no table for is named as declared (A5); `no regime declared` where there is none (R4); a regime without any weave is refused (R10) | "the regime named in the refusal is the declared one ... never a default" (the launch's ZC4); the article numbers are the ones Zin's own documents cite (`ZIN_PRIVACY_WEAVE_DESIGN.md`) |
| the five other weaves | still carried, their words closed, refused by name (R7) | nothing a court does not judge is accepted by silence |
| `SEVERITY error \| warning` on a `CONSTRAINT` | a warning does not refuse: `check` prints `ok` and then `warning <CODE>: <message> (line N)`, as `NO_WORLD` is printed today; `diagnose` carries it as a `"warning"` diagnostic with the constraint's code and cites; a clean sentence still diagnoses empty (A6, R9; X6, X7, X8) | stzzui's seam S1 and Central's ask to haro-charter of 2026-10-31 22:54, item 2, built for the maker's own rules. A `REFUSAL`'s severity is not built: a refusal of the grammar (an unknown verb, a dangling reference) stops the parse or the pass, and stzzui's five warnings are of that kind -- a per-seat severity on `MESSAGES` is the next step, named here |

**In the forged court.** A personal point refined is admitted with its values spoken as
`[personal] -> [personal]` and enters the audit chain redacted (`"from": "[personal]"`), while a
non-personal point keeps its values (X4, X5): W4.4 at the sentence, through the chain v0.24 built.
The `.refined` and `.revert.rfn` files beside the sentence carry the values, as the sentence does --
they are the gate's artefacts, not a log.

## Grammar (EBNF), the v0.24 text with these additions

```
CONSTITUTION: ARTICLES name_list, WEAVES pair_list, REGIME IDENT,
              ZONE IDENT, SOVEREIGN IDENT, MOVEMENT IDENT, PERSONAL path_list
CONSTRAINT:   ON IDENT, WHEN string, THEN string, MESSAGE string, CODE string,
              CITES string_list, SEVERITY IDENT
severity_c   = "error" | "warning" ;
```

The meta-court prints three lines more on acceptance -- `regime`, `weaves` (as `name:severity`,
comma-joined) and `personal` -- and, after the fields, a `warning ...` or `note ...` line per weave
verdict at governance or advisory severity. Every forged court is born with `$aCourtPersonal` and
`$aCourtWarnings`.

## The world judged: the clinic

`clinic_v25.haro` declares a clinic (a sector; the sentences carry placeholders and file numbers,
never a person's name): patients, flows, registries held by an organization and entered through a
declared flow, a constraint of `SEVERITY warning` (two patients on one file is a clerk's error the
desk corrects, not a sentence the clinic refuses), a voice that tells patients by file number, and
`CONSTITUTION clinic_charter` under all six articles with both weaves constitutional, `REGIME gdpr`
and `PERSONAL [patient.full_name]`. `clinic/` holds the clean sentence, one with a shared file, and
two proposals. `v25/court_cases.json` is judged by `haro_forge.py --stage=31` on rnxc and the oracle:

| case | what | holds |
|---|---|---|
| X1, X2 | the clinic is a sentence; the meta-court reads the zone, both weaves, the regime, the personal seat | ok |
| X3 | the voice tells by file number, never by name | ok |
| X4, X5 | the chain redacts a personal point and keeps a non-personal one, Art. 6 named on the refusal | ok |
| X6, X7, X8 | a warning constraint stands, is spoken after the verdict and placed in the envelope; a clean sentence diagnoses empty | ok |

**Results.** 16 of 16 meta fixtures (6 accepts, 10 rejects) and 8 of 8 cases, rnxc and the oracle
byte-identical; stages 1 to 5, 9 to 18, 21, 29 and 30 run unchanged; the ten committed courts
regenerated by the new forge (the rule of HF-127, kept).

## What building it found, recorded (HF-128)

1. **Two true refusals, one order.** A constitution with a regime and personal seats and no weaves is
   refused twice over; the first run spoke the regime's refusal and the fixture, written first, asks
   for the personal seats'. The order was set to the fixture's -- the personal seats are checked
   before the regime -- and the court, not the fixture, moved: the fixture was right about which
   refusal a reader needs first.
2. **A line miscounted, corrected by inspection before the court ran.** X6 was written with the
   warning at line 9; counting the file gave line 8, and the fixture was corrected before the first
   run, so the court never judged the wrong number. Recorded because the W discipline is also about
   what a fixture author does when he finds his own slip.
3. **The regime's article is a table in the meta-court**, three entries for gdpr and one law for
   Niger, drawn from Zin's documents; a regime outside it is named as declared. The table is the
   honest size of what the estate has read; it grows by reading, never by default.
4. **A REFUSAL's severity has no place to be a warning**: the parser stops at an unknown verb and
   the references pass raises at a dangling name. stzzui's five warnings are of the reference kind
   (`UNRESOLVED_*`, `ROLE_UNDECLARED`), so the next step is a severity per seat beside `MESSAGES`,
   named, not built.

## Refused here

- The model path: it is stzlib's and HaroBase's in this rung, not a Haro rule over `UNDERSTAND`.
- A default regime: a refusal under none says "no regime declared".
- Consent, anonymisation, retention and redaction as declared safeguards (Zin's W4.2 and W4.4 escapes):
  the three paths are refused or warned about whole; the safeguards are ZC5's question for the tontine.
