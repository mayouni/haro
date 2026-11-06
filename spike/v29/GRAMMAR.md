# Haro v0.29 -- five of the six carried weaves judge what they can with no new seat (WC1)

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures first, prose second; the fixtures were committed
before any court code, 15 of 17 failing on the court of the day and 2 holding). v0.29 is WC1 of the second charge of the constitution desk,
the six carried weaves (W1 resilience, W2 observability, W5 temporal integrity, W6 cost awareness, W7 learnability, W8 structural
integrity), filed by the compass on the author's word of 2026-11-02. Its first rung, WC0, read the 42 rules against Haro's mechanisms and
sorted them (`ZIN-WEAVES-INVENTORY.md`: 28 with a mechanism, 8 of them judged through what exists and 20 needing a declared seat; 14 absent at
this altitude). WC1 builds the eight that need no seat -- and finds that six of them can be refused and two cannot. The version number is the
one Haro's `CLAUDE.md` holds for this desk. v0.29 refuses nothing v0.28 accepted but a weave name this rung now judges.

## What is new, and where it comes from

| weave | rule | the court refuses (at the weave's severity) | the article it serves |
|---|---|---|---|
| `resilience` | **W1.5** a degradation preserves the invariants | a `CONSTRAINT` of `SEVERITY warning` whose `CITES` names `article:N` (or `article:<name>`) of an article the world stands under | the cited one |
| `observability` | **W2.2** an AI decision has a trace | a point `FLOOR llm` (a model may propose it) in a world with a `REFINE` and no `visible_state` | 3 |
| `observability` | **W2.3** a denial has an audit trail | a `REFINE` (whose gate denies) and no `visible_state` | 3 |
| `temporal_integrity` | **W5.2** a historical entity is versioned | a `REFINE` (it changes points that have a history) and no `visible_state`: no numbered chain versions the changes | 3 |
| `learnability` | **W7.4** a denial has an explanation | a world that declares a `CONSTRAINT` or a `REFUSAL` and no `NARRATE`; a `REFUSAL` or a `CONSTRAINT` with no `CODE` | 1 |
| `structural_integrity` | **W8.5** synthesis never overrides what is proved | a `policy` point `FLOOR llm` in a world not under `predictable_authority` | 4 |
| `resilience` | **W1.2** a mutation has a recovery path | nothing: the gate writes a change's inverse before the change lands -- **held by construction** | 2 |
| `learnability` | **W7.1** a declaration has a description | nothing: a declaration without a `RATIONALE` is refused whatever the weaves say -- **held by construction** | 1 |
| `cost_awareness` | W6.1 to W6.13 | **still refused by name**: none of its 13 rules is judged -- a budget needs a seat the world does not declare yet (WC2) | -- |

**One reading serves all six: a weave rule is an article's condition, read at the weave's severity.** Where the world stands under the
article, the article's own refusal comes first, constitutional, and the weave does not say it twice (R8: `predictable_authority` refuses the
model on a policy point before W8.5 can). Where it does not, the weave says it at the severity the world chose: `constitutional` refuses,
`governance` warns, `advisory` notes -- the machinery of v0.25, unchanged. Every refusal names the rule (`W2.2`), the weave, the declared thing
in the world's words (the point, the constraint, the language) and, last, the article it serves (`[Art. 3 visible_state]`). No regime is
named: a regime's articles are v0.25's table for W3 and W4, and the six have none.

**Judged is not the same as fired.** A2 is a world with no `REFINE` that names `observability` and `temporal_integrity` at constitutional
and is accepted: the rules are judged and find nothing, because there is no gate whose denial or proposal wants a trace.

## What the court prints, so that a partial weave is never a silent one

WC0 found that a world which leaves a weave out of `WEAVES` is silently not judged by it, and that a weave judged on some of its rules looks,
once named, like a weave judged on all of them. On acceptance the meta-court now prints three lines more, **only when one of these six is
named**: `judged` (the rules it refuses on), `held` (the rules that cannot fail) and `carried` (Zin's rules it does not judge), each the rule ids
in the order of `WEAVES`. Worlds that name only sovereignty and privacy print what they printed, to the byte (A6 is v0.25's A1 unchanged);
those two weaves are judged on three of their thirteen rules, which WC0 named and these lines do not yet say.

```
judged W1.5,W2.2,W2.3,W5.2,W7.4,W8.5
held W1.2,W7.1
carried W1.1,W1.3,W1.4,W1.6,W1.7,W2.1,W2.4,W2.5,W2.6,W5.1,W5.3,W5.4,W5.5,W7.2,W7.3,W7.5,W7.6,W8.1,W8.2,W8.3,W8.4
```

## Grammar

No clause is added. `WEAVES [name: severity]` takes the eight words it took; what changes is how many of them the court judges. The
`WEAVES names '<weave>', and none of its N rules is judged` refusal replaces v0.25's "no weave but sovereignty (W3) and privacy (W4) is judged
... the five others", which counted wrongly (eight minus two is six) and counted weaves where it should have counted rules; the new text is built
from the table of rules (`StzuWeaveRules`), so it cannot miscount again.

## Amended with this rung (said so, not silent)

Two pinned refusals named `resilience`, which is judged now, so they were amended after the court spoke, the weave they name changed to the one
none of whose rules is judged: **v23 R13** and **v25 R7**. Their names carry the date and this file's address. No other fixture of any rung
changed; stages 1 of v23 to v28 and v32 to v35 pass as they did (the guard's stage 1: 0 failures, haro and its checked build byte-identical).

## What building it found, recorded (HF-144)

1. **Eight were in the sort, six can be refused.** WC0 sorted W1.2 and W7.1 "through" Art. 2 and Art. 1. Built, neither has a shape the court can
   refuse: the gate writes the inverse unconditionally, and a missing `RATIONALE` is a grammar error before any weave looks. They are *held*,
   printed as such, and pinned by naming (P12) rather than by a refusal. The judged count is six, not eight.
2. **W5.2 rests on Art. 3 alone.** WC0 said "Art. 2 and 3". The revert is written under any articles; what versions an update is the numbered
   chain, which `visible_state` alone writes. W5.2 and W2.3 therefore share one condition (a `REFINE` and no chain) and are kept apart because
   they are different weaves making different claims; a world naming both at constitutional is refused once, by whichever comes first.
3. **A plant showed a protection no fixture pinned.** P14 (a cite is read without its kind) was missed by all seventeen fixtures: a cite of
   another kind that spells the article after the same eight characters (`pattern:visible_state`, `pattern:` being as long as `article:`) was
   read as an article's. **A8 was added after the court spoke**, and P14 is caught by it. Fifteen plants, every one caught, the file restored
   byte for byte each time (`plants.py`).
4. **A guard that could never matter was removed.** The first W8.5 skipped itself when `predictable_authority` is declared; with the article
   declared Art. 4 raises first and the weave is never reached, so the condition was dead and the plant that would have exercised it could not
   exist. Removed rather than kept "for safety".
5. **W1.5 is a reading, and it is stated as one.** Zin's rule asks that a degraded state keep the audit trail, not bypass the policy and not
   violate compliance. Haro's degradations are warnings, and an article's refusal is never a warning, so no degradation can pass an article by
   construction -- except the maker's own, a constraint held at warning that cites the law it degrades. That is the shape refused. A broader
   reading (any warning in a world under any article) would refuse worlds that Zin's rule does not.

## Refused here, by the charge's order

- The twenty rules that need a declared seat (a dependency's posture, a clock, a budget, a cascade threshold, a metric, a suggestion, a verb's
  example): WC2, one decision entry each. The first of them is the question the author parked, whether a world must say what it leaves out of
  `WEAVES`.
- `cost_awareness`: it has no rule that can be judged without a budget.
- Any change to the forged court: the weaves are judged where a language is declared, so `forge.haro` and the ten committed courts are untouched.
- A clock in the chain; a letter; an edit in zin; a customer's name.
