# Haro v0.24 -- visible state through the access paths and the audit chain, sovereignty through the zones

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.24 is the declaring altitude of Haro grown by the two articles v0.23
refused by name (ZC3 of the constitution plane, on the author's "Start ZC3", 2026-11-02; charter
D34): **visible state** (3) and **organizational sovereignty** (5) each get a mechanism, judged
THROUGH what a language already declares and never reimplemented, and every refusal under them
carries its number and its article, in the domain's words (COMPASS-KERN-06's first consumer).
v0.24 refuses nothing v0.23 accepted (A4 is v0.23's A1, unchanged; every earlier fixture file
still passes). v0.23's R11 and R12, which pinned "no mechanism judges it yet", were amended the
same night to pin each mechanism's first refusal, so a fixture file states what its court does;
the amendment is recorded here and in `v23/GRAMMAR.md`.

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| **Art. 3 visible_state, through the access paths** | every declaration kind of the language is reached by a declared path: told by the `NARRATE` (a `SAYS` template for the kind), asked by the `ASK` (`FROM` names it) or published by the `WORLD` (`PUBLISH` names it); a kind none reaches is refused as hidden state (A1, A2, A3; R1, R2) | Zin's "consequential state has declared access paths; no hidden databases, no shadow state" (`constitution_commands.zig:87`), read in Haro's terms: the paths a governor reads a world through are the voice, the question and the published world, and all three exist (v0.13, v0.7, v0.10). Nothing new judges the sentence: a kind told is told by the narration it had |
| **Art. 3, through the audit chain** | under the article, every refinement proposal the forged court judges -- admitted or refused -- is one JSON line appended beside the sentence, `<file>.audit`: `event` (numbered), `proposal`, `target`, `from`, `to`, `author`, `posture`, `verdict`, `stage`, `code`; `audit <file>` answers the chain as a query, in order, then its count (W8, W9); a language under no visible state keeps none and says so (W10) | the charter owes the governor "the audit chain as a query" (section 2), and refinement's record is "a by-product" of the gate (6.5). The chain carries **no clock**: an event is numbered, so rnxc and the oracle write one chain and a chain is comparable byte for byte; the time a governor wants is the file's, which the host dates |
| **Art. 5 organizational_sovereignty, through the zones**: `ZONE kind, SOVEREIGN seat, MOVEMENT seat` on the `CONSTITUTION` | the world's zone kind (a `DECLARATION`); who holds a zone -- a seat typed by a `MENU` of organizations or `text`, never optional; what a zone is entered through -- a seat typed by a declared kind (the flow a record walks), never optional (A1, A5; R3 to R11); the zone seats named without the article are refused, not accepted by silence (R12) | "no ungoverned data movement" (Zin's W3) and "organizations retain full sovereignty over their data" (Art. 5's user text), read on what Z already declares: a `LANDING_ZONE` is where exported records land and `INTO` the flow every one walks; what Z's zone lacks is who holds it. The organizations are a `MENU` of sectors and roles -- the bank, the clearing house, the regulator -- never a customer's name |
| **Art. 5, in the forged court** | a zone instance without its holder or its entry is refused by the kind's own `MESSAGES` and `CODES`, with `[Art. 5 organizational_sovereignty]` and the cite `article:5` beside `rule:<CODE>` (W3 to W6); the article's number and name reach `check`, `diagnose` and the voice | the Kern lesson adopted, not copied: a refusal that names its law, in the domain's words (`VAULT ghost_vault is entered through 'nowhere', and no FLOW of that name is declared`) |

**What it does not judge, named.** A movement between two zones of different sovereigns: no
declaration carries one yet (Z's records land; nothing declares that a record of one zone reaches
another). ZC4's field tags -- a field declared personal that reaches an analytics, a log or a model
path -- are the paths that will, and the regime named in their refusals is the declared one.

## Grammar (EBNF), the v0.23 text with these additions

```
CONSTITUTION: ARTICLES name_list, WEAVES pair_list, REGIME IDENT,
              ZONE IDENT, SOVEREIGN IDENT, MOVEMENT IDENT
```

The meta-court prints one line more on acceptance: `zone <kind>` (empty under none). Every forged
court gains one verb, `audit <file>`, and three globals born in its prologue (`$aCourtZone`,
`$cCourtAuditFile`, `$aCourtAuditProposal`).

## The world judged: the bank under all six

`bank_v24.haro` is `ledger_v23.haro` grown by what the two articles need: a `FLOW` kind, a `VAULT`
kind (`held_by: holders`, a `MENU` of three organizations; `entered_through: flow`) with its
`MESSAGES` and `CODES`, a `SAYS` template for every kind, a fifth point (`vault.held_by: policy`,
floored `trusted`), and `CONSTITUTION bank_charter` under all six articles with `ZONE vault,
SOVEREIGN held_by, MOVEMENT entered_through`. `bank/` holds the clean sentence (two vaults, each held
and entered), a vault held by nobody and a vault entered through nothing; the proposals are v0.23's.
`v24/court_cases.json` is judged by `haro_forge.py --stage=30` on rnxc and the oracle, byte-identical:

| case | what | holds |
|---|---|---|
| W1, W2 | the clean bank is a sentence; the meta-court reads all six articles and the zone | ok |
| W3, W4 | Art. 5 through the required seat: `HELD_BY is required on VAULT orphan_vault [Art. 5 organizational_sovereignty]`, code `NO_HOLDER`, cites `rule:NO_HOLDER`, `article:5` | ok |
| W5, W6 | Art. 5 through the reference: the kind's own words, code `NO_FLOW`, cites `rule:NO_FLOW`, `article:5` | ok |
| W7 | Art. 3 through the voice: both vaults told, holder and entry alike | ok |
| W8 | Art. 3 through the chain: an admitted and a refused proposal are events 1 and 2, kept and answered | ok |
| W9, W10 | the chain before any event says so by name; the v0.23 ledger, under no visible state, keeps none | ok |

**Results.** 18 of 18 meta fixtures (5 accepts, 13 rejects) and 10 of 10 cases, rnxc and the oracle
byte-identical; stages 1 to 5, 9 to 18, 21 and 29 run unchanged after the change; the nine committed
courts regenerated by the new forge.

## What building it found, recorded (HF-127)

1. **A global the forge adds is born in every generated court, or Ring 1.27 makes it a function's
   local.** The first run of stage 30 held 10 of 10 and differed between the runtimes on W10, a
   refinement on the v0.23 ledger court still on disk from before the forge grew: on rnxc `$` is
   the global wherever it is first assigned; on the oracle `$cCourtAuditFile = ""` inside `CtRefine`
   made a local that `CtRefuse` could not see (haro.ring's own comment names the rule). Regenerating
   the nine courts closed it; every rung that grows the forge regenerates them, and the guard's
   stages do, in order.
2. **v0.23's R11 and R12 amended**: a fixture that pinned "no mechanism yet" would have failed the
   court that built the mechanism; each now pins that mechanism's first refusal, under its v0.23
   source, and its name says so. A fixture file states what its court does.
3. **An `ASK` of a `FROM` alone is a declared access path** the meta-court accepts (A2): no `WHERE`,
   no `EXPRESSION`. What a question over the kind then needs to be answered is ZC5's, with Z.
4. **The chain is numbered, not dated.** A clock in the court would break byte-identity between
   runtimes and determinism between runs; the governor's "who decided this three years ago" is
   answered by the event's author and the file's date, which the host keeps.
5. **Z's zone has no holder.** `LANDING_ZONE` carries `FORMAT` and `INTO` and no organization, so the
   tontine stands under Art. 5 only once its zone declares who holds it: ZC5's second act, with the
   codes Art. 1 asks for.

## Refused here

- No letter; the two mechanisms are seats of the constitution and verbs of the court, nothing else.
- No clock, no digest in the chain: what the gate knows is recorded; what it does not is not invented.
- No movement between zones judged: it is named as not judged, and ZC4's paths are its first form.
