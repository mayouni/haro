# Haro v0.23 -- the constitution: a world under Zin's articles, judged through what exists

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.23 is the declaring altitude of Haro grown by the ruling of
2026-11-01 on Zin (COMPASS-KERN-09; charter section 2, ratified by the author the same night,
"Ratified, start ZC2"; D33): Zin's six immutable articles enter Haro as a **declared
governance sentence** -- a `CONSTITUTION` declaration that a world declares itself under --
and the four articles Haro already holds are judged THROUGH the mechanisms the charter names
and never reimplemented. The inventory behind it is `ZIN-INVENTORY.md` beside this file
(ZC0, HF-124); this is ZC2 of the constitution plane
(`softanza/memos/2026-11-01-constitution-launch.md`). v0.23 refuses nothing v0.22 accepted
(fixture A3 is v0.13's A1, unchanged, and every earlier fixture file still passes).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `CONSTITUTION`, at most one | `ARTICLES [explainability, reversibility, predictable_authority, trust_hierarchy]` -- the articles the world is under, each a word of Zin's six in Zin's order and numbering (`zin/src/compiler/constitution.zig:35-40`), each at most once (A1, A2, R1, R2, R3, R4) | the articles are a **menu of the meta-language**, not a text a maker writes: Zin's six are immutable (every Zin compilation must satisfy them), and what a world chooses is which it stands under. A seventh word is refused with the six named and numbered (R1), so the refusal is a lesson, not a wall |
| judged once the whole file is read, in `ARTICLES`' order | **1 explainability**: a `NARRATE` is declared, and every `REFUSAL` and every `CONSTRAINT` carries a `CODE` (R5, R6, R7); **2 reversibility**: a `REFINE` is declared (R8, R17); **4 predictable_authority**: no `policy` point is floored `llm` (R10, A4); **6 trust_hierarchy**: every point of the `REFINE` has a `FLOOR` (R9) | each article is judged **through** what the charter names (section 2): RATIONALE, the C2 envelope and the narration for 1; refinement for 2; the gate's governance stage for 4 ("a rule cannot be changed by a model-composed proposal", charter 6.4); the trust posture and a point's floor for 6 ("a trust requirement is declared, never implied: silence refuses", Harobanda's own rule). Nothing is reimplemented: the checks ask whether the mechanism is there, and the mechanism judges the sentence |
| **3 visible_state** and **5 organizational_sovereignty** | refused by name as what Haro v0.23 does not judge yet, with where it will (R11, R12) | a state, not a fault (the launch's own words): ZC3 builds 3 on the narration and the audit chain and 5 on the zones Z declares, fixtures first; these two rejects become accepts then |
| `WEAVES [privacy: governance, ...]`, `REGIME gdpr` | carried, their words closed -- a weave is one of Zin's eight by name and number (R14), a severity one of Zin's three (R15) -- and refused by name until ZC4 (R13, R16) | the whole sentence's shape is declared now, and nothing it names is accepted by silence; the regime is the declared one, "never a default" (the launch's ZC4) |
| `CITES` on a `CONSTRAINT` | `CITES ["right:one-limit-per-account"]`, the pinned instruments the maker's own rule cites, as a `REFUSAL` and a `SYMBOL` already could (v0.11) | stzzui's seam S2 and Central's ask to haro-charter of 2026-10-31 22:54, item 1, answered once here: a constraint's declared cites replace the default `rule:<CODE>` in the envelope (L6) |

**What the forged court does with it.** The court carries the articles (`$aCourtConstitution`,
empty under no constitution), and a refusal that enforces an article names it and cites it:
a declaration without RATIONALE is refused `... [Art. 1 explainability]` with the code
`RATIONALE` and the cite `article:1` (L3, L4), told in the voice with its cite (L5); a
proposal below a point's floor is refused `... [Art. 6 trust_hierarchy]` with `article:6`
beside `rule:trust-floor` (L7, L8). That is the number-and-article shape of COMPASS-KERN-06,
consumed here. A language under no constitution prints what it printed before, to the byte
(stages 1 to 18 and 21 unchanged). Reversibility is judged by the gate itself: the admitted
proposal's inverse, written before it landed, restores the sentence byte for byte (L9, L10).

## Grammar (EBNF), the v0.22 text with these additions

```
CONSTITUTION: ARTICLES name_list, WEAVES pair_list, REGIME IDENT
CONSTRAINT:   ON IDENT, WHEN string, THEN string, MESSAGE string, CODE string,
              CITES string_list
article      = "explainability" | "reversibility" | "visible_state"
             | "predictable_authority" | "organizational_sovereignty" | "trust_hierarchy" ;
weave        = "resilience" | "observability" | "sovereignty" | "privacy"
             | "temporal_integrity" | "cost_awareness" | "learnability" | "structural_integrity" ;
severity     = "constitutional" | "governance" | "advisory" ;
```

The meta-court prints two lines more on acceptance: `constitution 0|1` and `articles` as the
comma-joined list in the declared order (empty under none).

## The world judged: a bank's ledger

`ledger_v23.haro` declares a bank's ledger (a sector, never a customer) under the four articles:
two kinds (`ACCOUNT`, `LIMIT`), a menu, a constraint that CITES, three coded refusals, a `REFINE`
of four points with a floor each (a ceiling an external actor may turn, a daily amount and a
rule the bank's, the words of a refusal a model may propose), a `NARRATE` whose `REFUSES`
carries `{cites}`, and `CONSTITUTION bank_charter`. `ledger/` holds the clean sentence, one
without a RATIONALE, one with two limits on an account, and four proposals. `court_cases.json`
is judged by `haro_forge.py --stage=29` on rnxc and on the oracle, byte-identical:

| case | what | holds |
|---|---|---|
| L1 | the clean ledger is a sentence: 2 ACCOUNT, 1 LIMIT | ok |
| L2 | the meta-court reads the constitution: `constitution 1`, the four articles, 4 points, a voice | ok |
| L3, L4, L5 | Art. 1 through RATIONALE, the envelope and the voice | ok |
| L6 | the maker's constraint cites what it CITES | ok |
| L7, L8 | Art. 6 through the floor: a model below a knob's floor, an external actor below a policy's | ok |
| L9, L10 | Art. 2 through refinement: admitted at the floor, reverted byte for byte; the floor per point | ok |

**Results.** 22 of 22 meta fixtures and 10 of 10 cases, rnxc and the oracle byte-identical;
guard stages 1 to 5, 9 to 18 and 21 run unchanged after the change (stage 20 fails in this
fresh worktree on a CRLF checkout of `n/tontine.n` and passes in the main checkout: HF-126,
N's owner's). Edit to verdict of a sentence of the ledger is the court's usual (stage 6's
regime); the constitution adds one list to the court and two comparisons to a refusal.

## What building it found, recorded (HF-125, HF-126)

1. **Three fixtures were written against v0.13's rule, not v0.23's.** A5, R6 and R7 declared a
   NARRATE of a `REFUSES` alone, which v0.13 refuses: "a voice that says and tells nothing
   narrates nothing". They were corrected to carry a `SAYS` and the court was not touched; the
   first run read 19 of 22, the second 22 of 22. Recorded so the correction is not mistaken
   for a fixture adapted to pass.
2. **HF-36 again.** `aCC = [aCC[1], aCn[7]]` answers on rnxc and is `Error (R2)` on the oracle
   (stage 29's L6: the oracle's diagnosis came back `PARSE` at line 0 with Ring's own error as
   the message); written as `aCC[2] = aCn[7]`. A probe of three lines reproduces it.
3. **Zin's Art. 4 and Art. 6 are one stage of Haro's gate**, split by what each forbids: a
   model-composed proposal into a `policy` point (4, judged at the declaring altitude) and an
   origin below a floor (6, judged at the sentence, the `TRUST_FLOOR` refusal citing it).
4. **Explainability has a cost Z does not pay yet.** Z's constraints and refusals carry no CODE
   (z_v06 to z_v16), so the tontine stands under Art. 1 only once they are coded: ZC5's first act,
   and the right one -- C2 asked for codes before the constitution did.
5. **`CITES` on `CONSTRAINT`** is a dozen lines in three files (the clause, the record, the row,
   the pass); **`SEVERITY`** is designed and not built: `error` or `warning` on `CONSTRAINT` and
   `REFUSAL`, a warning leaving the verdict `ok` and spoken after it as `NO_WORLD` is today,
   `"warning"` in the envelope -- it is what the weaves need (Zin's three severities), so it
   comes with ZC4 (stzzui's S1, Central's item 2).

## Refused here

- No letter; the alphabet is closed, and the constitution is a declaration like `WORLD` and `REFINE`.
- Nothing of Zin's compiler ported; its articles were read (`constitutional.zig`, the CSP stage 4) and its
  numbering kept, so a refusal here and a diagnostic there name the same article.
- The weaves judged by nothing are accepted by nothing: every weave named is refused until ZC4.
