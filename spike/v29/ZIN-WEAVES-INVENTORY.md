# ZIN-WEAVES-INVENTORY -- the six carried weaves read against Haro's mechanisms (WC0)

```yaml
by:        constitution · claude-sonnet-5-5 · 2026-11-02 14:29
rung:      WC0 of the second charge (softanza/memos/2026-11-02-weaves-charge.md, section 2), read-only: no guard run and none needed;
           nothing in zin/, harobase or stzlib was edited; this file is the rung's one artefact
version:   Haro v0.29 is this desk's number (CLAUDE.md: "take the next free version number and say so"); v0.28 is the latest on main
read:      zin cc98126: doc/design/ZIN_CONSTITUTIONAL_WEAVES.md (887 lines), and src/ for any weave code;
           haro main fe773fd (D:/GitHub/haro, read through the desk's worktree D:/GitHub/_hwc): CHARTER.md D33-D38, spike/haro_lib.ring,
           court_lib.ring, narrate_lib.ring, ask_lib.ring, v10, v23-v28, clinic_v25.haro, bank_v24.haro, ledger_v23.haro, z_v27.haro,
           machine_v03.haro; harobase main 01401ea (CHARTER.md, src/log.zig); stzlib main 616c43b6c (base/security/stzSecurityEvent.ring,
           base/governance/stzGovernance.ring, engine/src/resilience.zig)
measured:  [R] a read, [M] a count by grep; no court was forged and no guard was run (haro-charter has not reported the guard green)
```

A file:line is of the commit named above. Zin lines are of `ZIN_CONSTITUTIONAL_WEAVES.md`; Haro lines are of `spike/` unless a path says otherwise.

## 0. The three counts

| count | value | what it is |
|---|---|---|
| rules with a mechanism | **28 of 42** | **8 judged THROUGH what exists** (no new seat), **20 that need a declared seat** |
| rules absent at this altitude | **14 of 42** | each with the pillar of Zin's that owns what it quantifies over |
| fixture candidates | **28** at rule level: 8 writable now, 20 after their seat | at least 56 fixtures (an accept and a refusal each); v25's ratio (16 meta fixtures and 8 cases for three rules and three clauses) says the real figure is nearer 100 |

| weave | rules | THROUGH | SEAT | ABSENT |
|---|---|---|---|---|
| W1 resilience | 7 | 2 (1.2, 1.5) | 4 (1.1, 1.3, 1.4, 1.7) | 1 (1.6) |
| W2 observability | 6 | 2 (2.2, 2.3) | 3 (2.1, 2.5, 2.6) | 1 (2.4) |
| W5 temporal integrity | 5 | 1 (5.2) | 2 (5.1, 5.3) | 2 (5.4, 5.5) |
| W6 cost awareness | 13 | 0 | 7 (6.1, 6.2, 6.3, 6.4, 6.7, 6.9, 6.10) | 6 (6.5, 6.6, 6.8, 6.11, 6.12, 6.13) |
| W7 learnability | 6 | 2 (7.1, 7.4) | 2 (7.2, 7.5) | 2 (7.3, 7.6) |
| W8 structural integrity | 5 | 1 (8.5) | 2 (8.1, 8.2) | 2 (8.3, 8.4) |
| **total** | **42** | **8** | **20** | **14** |

**The rule used to sort.** THROUGH: every REQUIRE of the rule reads from something Haro declares today -- an article's mechanism, a
constraint's SEVERITY and CITES, the audit chain -- so a refusal needs no new clause. SEAT: a mechanism family exists (named in the row)
but the rule reads something no declaration carries today, so it is judged only once a CONSTITUTION clause or a seat names it. ABSENT:
what the rule quantifies over belongs to one of Zin's product pillars (Zpm pricing, Zai agents and retrieval, Zca calendars, Zsm
system dynamics, Zui forms) and is not a thing a Haro language declares or could by the charter's means. A rule with two halves takes the
verdict of the half that needs more.

## 1. What this inventory found that the charge did not say

1. **The six are refused by name today, not accepted by silence.** `WEAVES [resilience: ...]` is refused with "no weave but sovereignty
   (W3) and privacy (W4) is judged in Haro v0.25 -- the five others are Zin's design, carried, not built" (`haro_lib.ring:2137-2142`,
   pinned by `v25/fixtures.json` R7 at `:131-133`). The charter's remedy for silence is already in force; WC1 and WC2 lift it weave by weave.
2. **The correction to carry, and where it lives.** "The five others" is wrong (eight minus two is six) in eight places: `haro_lib.ring:2137`
   (comment) and `:2140` (the message), `v25/fixtures.json:131` (name) and `:133` (the pinned refusal), `v23/fixtures.json:156` (name),
   `v23/GRAMMAR.md:113`, `v25/GRAMMAR.md:21`, `CHARTER.md:1145`. The pinned refusal is a fixture, so the change is one made after the court
   spoke and is said so in v29's account. It is moot as a number the moment WC1 lands: the message must be built from the judged set, never
   written as a count, so it cannot miscount again.
3. **Zin's document counts its rules four ways.** 42 across the six is right [M]: W1.1-1.7, W2.1-2.6, W5.1-5.5, W6.1-6.13, W7.1-7.6,
   W8.1-8.5. But the text says "seven" weaves (`:27`, `:71`, `:883`) and "35 weave rules" (`:875`), lists rules out of order (W1.7 before W1.6
   at `:119`, W2.6 before W2.5 at `:184`, W6.10 before W6.9 at `:461`), and places W6.11-6.13, W8.5 and W3.8 after W8's list (`:594-678`).
   The eight weaves hold 42 + the judged two's 13 = 55 rules in this document alone (W3.1-3.8, W4.1-4.5).
4. **The two weaves called judged are judged on three rules of thirteen**: W3.1 and W4.2, W4.4 (`haro_lib.ring:2347-2398`). Out of this
   charge; named so the figure is not read as more than it is.
5. **No weave is code in Zin** [M]: a grep of `W[1-8].N` across `src/` finds `compiler/roadmap_data.zig` only, as in ZC0. The rules are
   the fixture source and the only source.
6. **Severity has three granularities, and only one is Haro's.** Zin's is per RULE: `WEAVE_POLICY (W7.1 SEVERITY constitutional ...)` at
   `:738-745`, with W1.1 constitutional, W7.1 governance and W6.5 advisory as its examples (`:728-730`). Haro's is per WEAVE
   (`WEAVES [name: severity]`, `haro_lib.ring:2128-2135`). The compass's per-seat one is haro-charter's to design (HF-128; Central 01:08).
   Asked in the mailbox, never built here.
7. **W7.1 cannot be softened in Haro.** Zin's own governance-severity example is "an undocumented declaration" (`:729`); Haro refuses a
   declaration without a RATIONALE unconditionally (`haro_lib.ring:1037-1038`, principle 5), so a world cannot declare learnability
   below constitutional for that rule. A difference to record in v29's account, not a defect.
8. **Zin's weaves are universal and always enforced** (`:17`, `:37`, `:774`: "Opt-in ... No (always enforced)"); Haro's are chosen per world, as D33 chose the
   articles. The consequence is silent suppression by omission: a world that leaves `resilience` out of WEAVES is not judged by W1 and
   nothing says so, where Zin's `SUPPRESS Wx.y BECAUSE "..."` (`:749-760`) is auditable. Whether a Haro world must say what it leaves
   out is the author's to rule (a question for WC2's first rung, not decided here).
9. **The hypothesis about WC1 holds in part.** The compass named W2, W7 and W5's monotonic half. Found: W2 through what exists for 2 of its 6
   rules, W7 for 2 of 6, **W5's monotonic rule (5.3) only as an accept** (the chain is numbered, so it cannot violate it, and a refusal
   needs the declared clock), and three rules nobody named: W1.2, W1.5 and W8.5.
10. **No constitution world has a subject for four of the five seats.** The five worlds under a CONSTITUTION (ledger_v23, bank_v24,
    clinic_v25, z_v26, z_v27) declare no dependency, no cost budget, no clock and no event kind [M, grep of budget, dependency, adapter, retry, timeout, fallback, clock, date, time; `account.ceiling` is a money limit, not a cost budget]. The exceptions: floored-llm points
    in four files (ledger_v23.haro:69, bank_v24.haro:87, z_v26.haro:160, z_v27.haro:165), all on a `message` point; and the `machine` language
    (machine_v03.haro, Harobanda's, carrying no CONSTITUTION), whose SERVICE has a restart policy, memory, cpu and task ceilings and a
    `clock` capability. WC4's proof world must give the seats a subject; WC2's fixtures declare small ones.

## 2. The rules, one by one

Haro's mechanisms, once: **RATIONALE mandatory** `haro_lib.ring:1037-1038`; **the articles** 1 `:2237-2250`, 2 `:2251-2254`, 3 `:2255-2278`,
4 `:2279-2292`, 5 `:2293-2330`, 6 `:2331-2345`; **the weave verdict** `StzuWeave` `:2413`; **the closed words** `StzuArticles`
`:86`, `StzuWeaves` `:89`, `StzuSeverities` `:92`, `StzuPostures` `:80`; **the C2 gate record** `CtRecord` (code, severity, message, span,
cites, language, why, todo) `court_lib.ring:1871-1879`, **the diagnostic** six fields without why or todo `:489-516`; **the gate** derivation
`:2069`, governance `:2078`, trust `:2085-2108`, revert `:2113-2119`; **the audit chain** `CtAuditWrite` `:230-255`; **the voice**
`narrate_lib.ring:93, :168, :216, :273`; **a degradation** `NO_WORLD` `court_lib.ring:565, :2289`; **SEVERITY on a CONSTRAINT**
`haro_lib.ring:119, :1506-1510`; **references resolved at check time** `StzuResolveSeats` `:2589`.

### W1 resilience (Zin :73-142)

| rule | Zin | Haro / estate mechanism | verdict |
|---|---|---|---|
| W1.1 dependency has a defensive posture | :85 | no constitution world declares a dependency; nearest: machine_v03.haro:173 SERVICE `restart` (menu :40), `health`, `ready`; the court's own dependency, the world, degrades as a declared warning (court_lib.ring:565). Record plane: stzlib engine/src/resilience.zig (retry_delay_ms, RateLimiter, CircuitBreaker) | SEAT: a dependency kind and its posture (S1) |
| W1.2 mutation has a recovery path | :91 | Art. 2: a REFINE is declared (haro_lib.ring:2251-2254), the inverse is computed first and written beside (court_lib.ring:2113-2119), charter 6.5; Zin's own ZC0 reading is that W1.2 is Art. 2's design | THROUGH Art. 2 (a world's own flows' compensation is not judged: named) |
| W1.3 resource has a budget | :98 | machine_v03.haro:173 SERVICE `needs [capability]` with `memory`, `cpu`, `tasks` ceilings; capability :157, menu :60, constraints :373 ff | SEAT: a budget (S3), the one with a real subject |
| W1.4 external dependency has a fallback | :104 | NO_WORLD (court_lib.ring:565); record plane: CircuitBreaker, resilience.zig | SEAT (S1) |
| W1.5 degradation preserves invariants | :111 | Haro's two degradations are warnings: NO_WORLD and a CONSTRAINT of SEVERITY warning (haro_lib.ring:1506-1510); an article's refusal is StzuFail, never a warning (:2237-2345), so no degradation passes an article; the refusable shape is a warning CONSTRAINT whose CITES names an article the world stands under (CITES on every coded element, v0.28, D38) | THROUGH the cited article; shape to confirm in WC1 |
| W1.6 archetype detection on resilience | :127 | Zsm archetypes read a series over time; a court judges one sentence, and the chain is numbered, not dated (court_lib.ring:226-228) | ABSENT (Zsm) |
| W1.7 connection has a retry policy or safe_to_fail | :119 | resilience.zig retry_delay_ms at the record plane; no connection kind in any world | SEAT (S1) |

### W2 observability (Zin :144-200)

| rule | Zin | Haro / estate mechanism | verdict |
|---|---|---|---|
| W2.1 flow has completion metrics | :157 | flow kinds exist (clinic_v25.haro `flow`; Z `step`, z_v27.haro:93-97); the run is told, not measured (narrate_lib.ring:216); a metric needs a clock (W5.1) and a metric kind; record plane: stzMetric | SEAT: a flow's metric (S5) |
| W2.2 AI decision has a trace | :164 | a model's decision is a proposal of posture llm; the chain keeps author, posture, rule, verdict, stage and code for admitted and refused alike (court_lib.ring:230-255, written at :1903; v26 T14's audit step); no confidence field | THROUGH Art. 3 and Art. 4: a point floored llm (z_v27.haro:165) in a world without visible_state is the refusable shape |
| W2.3 denial has an audit trail | :171 | every gate refusal enters the chain (CtRefuse, court_lib.ring:1900-1903) under visible_state; under none nothing is written (CtUnderArticle :199, :1935-1940) | THROUGH Art. 3 |
| W2.4 stock has monitoring | :177 | Zsm stock; no Haro world declares one; a warning CONSTRAINT at a threshold is a world's own rule, not a weave | ABSENT (Zsm) |
| W2.5 dependency has latency tracking | :191 | no dependency kind; record plane: stzMetric `http.request.ms` | SEAT (S1 with S5) |
| W2.6 performance-critical endpoint has a budget | :184 | no endpoint kind in any world (HaroServer's routes are app code) | SEAT (S3) |

### W5 temporal integrity (Zin :335-385)

| rule | Zin | Haro / estate mechanism | verdict |
|---|---|---|---|
| W5.1 event has a governed timestamp from a declared clock | :348 | the chain is numbered, not dated, so both runtimes write the same bytes (HF-127; court_lib.ring:226-228); machine has a `clock` capability (machine_v03.haro:60); record plane: `recorded_at` is read from the clock inside HaroBase, never handed in (harobase CHARTER.md:88, :280) | SEAT: a declared clock that governs the sentence's events and never enters the chain's bytes (S2) |
| W5.2 historical entity is versioned | :355 | the WORLD is versioned data (v10/GRAMMAR.md:1-8); a revert is its own event, nothing erased (court_lib.ring:2113-2119); chain events numbered (:230); record plane: hb_event insert-only (harobase CHARTER.md:92-93), bitemporal fact versions (:270-285) | THROUGH Art. 2 and Art. 3 |
| W5.3 snapshots use monotonic time | :363 | the chain's order is a counter, monotonic by construction; record plane: transaction time never runs backwards (harobase src/log.zig:282-283). A refusal needs a declared clock of kind wall used for a span | SEAT (S2); holds as an accept on the chain |
| W5.4 bitemporal query is unambiguous | :370 | no Haro language asks over time (ask_lib.ring:96 has no temporal clause); at HaroBase the verb takes both axes, `hb_facts_as_of(valid_at, known_at)` (harobase CHARTER.md:277-279, :487) | ABSENT here; held at HaroBase by the signature (WC3) |
| W5.5 calendar rule is timezone-aware | :377 | Zca calendars; no calendar in any world | ABSENT (Zca) |

### W6 cost awareness (Zin :387-478, :594-678)

| rule | Zin | Haro / estate mechanism | verdict |
|---|---|---|---|
| W6.1 LLM agent has a budget and a monitor | :399 | the agent a Haro world has is a point floored llm (ledger_v23.haro:69, bank_v24.haro:87, z_v26.haro:160, z_v27.haro:165); the monitor exists at the record plane, `model.call` recorded by the model door (stzSecurityEvent.ring:107); no budget exists | SEAT: a budget on the point (S3) |
| W6.2 metered API has a ceiling | :407 | the one metered external dependency a Haro world has is the model, W6.1's | SEAT (S1 with S3) |
| W6.3 compute operation has a budget | :414 | machine_v03.haro:173 `memory`, `cpu`, `tasks`; a service declaring none is the refusable shape | SEAT (S3) |
| W6.4 total cost is a monitored stock | :420 | declaration half: a ceiling the declared budgets sum under; monitor half is the record plane's (Central's .central/cost.jsonl, stzlib's model.call) | SEAT (S3), declaration half only |
| W6.5 pricing tier is viable | :428 | Zpm pricing: Zin's product | ABSENT (Zpm) |
| W6.6 context budget sums to 100% | :435 | Zai context windows; Haro declares no agent context | ABSENT (Zai) |
| W6.7 tool policy, MAX_COST under the budget | :445 | an actor's tools are the capabilities it needs (machine_v03.haro:157, `needs_are_granted`); the inequality needs W6.1's budget first | SEAT (S3) |
| W6.8 success metrics at autonomy L3 | :453 | Zai autonomy levels; Haro's postures rank an origin, not an autonomy (haro_lib.ring:80) | ABSENT (Zai) |
| W6.9 high-impact agent has a risk gate | :467 | the gate exists (governance stage court_lib.ring:2078, floors :2085-2108, widening a rule is tier 4, charter 6.4; Art. 4 and 6); a documented worst case and a review cadence have no seat | SEAT: two of its three REQUIREs |
| W6.10 service has a timeout budget | :461 | machine's `health` window is the nearest (constraint health_under_an_hour); no timeout seat | SEAT (S3) |
| W6.11 retrieval allocation has context quality | :594 | Zai retrieval | ABSENT (Zai) |
| W6.12 autonomous agent declares LOOP.MAX_TURNS | :649 | the agent loop is stzlib's (stzGovernance.ring:934-956 registers an actor in a loop: coverage and a reversibility class); no Haro kind loops | ABSENT here; record plane's |
| W6.13 long-term memory declares MEMORY_POLICY | :666 | the memory is HaroBase (insert-only events, erasable content, harobase CHARTER.md:92-100); retention and redaction are stzFieldTags' safeguards (v0.27, D37) | ABSENT here; WC3 |

### W7 learnability (Zin :480-535)

| rule | Zin | Haro / estate mechanism | verdict |
|---|---|---|---|
| W7.1 declaration has a description | :492 | RATIONALE mandatory on every declaration, a refusal and not a severity (haro_lib.ring:1037-1038; Art. 1 :2237; principle 5) | THROUGH Art. 1 |
| W7.2 error has a human message and a suggestion | :498 | message: MESSAGE is required on a REFUSAL (haro_lib.ring:154) and a CONSTRAINT; suggestion: the gate's record carries `why` and `todo` (court_lib.ring:1871-1879) but the diagnostic has six fields without them (:489-516) and no declared REFUSAL or CONSTRAINT has a suggestion seat | SEAT: a suggestion (S5) |
| W7.3 form field has help text | :505 | Zui forms (stzzui); Haro's FORM is a seat structure, not a screen: a name collision | ABSENT (Zui) |
| W7.4 denial has an explanation | :511 | every gate refusal carries `why` and `todo` (court_lib.ring:1900-1903, :2081), every constraint a MESSAGE, Art. 1's CODE and CITES | THROUGH Art. 1 |
| W7.5 keyword has an example | :518 | Haro's analogue of a composed pillar's keyword is a language's VERB; N's UNDERSTAND requires EXAMPLE and COUNTEREXAMPLE (haro_lib.ring:188) but a DECLARATION's verb needs none; the court's cases (the COURT clause) are per language | SEAT: a verb's example (S5) |
| W7.6 agent has an identity | :525 | Zai agent; a refinement's author is a name and a rank (court_lib.ring:230-255); record plane: stzGovernance registration requires coverage | ABSENT here; record plane's |

### W8 structural integrity (Zin :537-628)

| rule | Zin | Haro / estate mechanism | verdict |
|---|---|---|---|
| W8.1 high-impact entity has cascade awareness | :555 | references are resolved at check time (haro_lib.ring:2589, :1528, :1546), so a declaration's dependents are countable; the review gate is the REFINE gate (Art. 2, 6); no declared threshold | SEAT: a threshold and a review path (S4) |
| W8.2 entity change reports its cascade | :562 | the admitted line reports its passes, not dependents (court_lib.ring:2123); the graph exists (CODEGRAPH.md rung 4, HF-82 to HF-84); HF-127 is a cascade made visible by hand | SEAT (S4) |
| W8.3 API version change has a migration path | :569 | Zxt versions; the language-version analogue (LANGUAGE VERSION and GRAMMAR, haro_lib.ring:97-100) is held by the guard, stage 1 re-running every earlier rung's fixtures: a process, not a seat | ABSENT as a court rule |
| W8.4 RETRIEVAL_PIPELINE has evaluation | :576 | Zai retrieval: Zin's product | ABSENT (Zai) |
| W8.5 synthesis never overrides proofs | :612 | the model proposes, the court disposes: every proposal is re-judged at the derivation and constraint stages (court_lib.ring:2069), and Art. 4 refuses a model on a policy point (haro_lib.ring:2279-2292) | THROUGH Art. 4 |

## 3. The seat each weave judges over

W3 and W4 judge over `PERSONAL` (a path naming the seat or the mark), and a verdict is judged on the paths a language declares: voice, ask,
world. The six judge over, in the order of the charge's own questions:

| weave | judges over | exists today | to be declared |
|---|---|---|---|
| W1 | a declared **dependency** and the posture it takes; Art. 2 for mutations | NO_WORLD; machine's SERVICE restart | S1: a CONSTITUTION clause naming the kinds that are dependencies, a posture seat on them |
| W2 | the **audit chain** for decisions and denials; a flow's metric | the chain, under Art. 3 | S5: a metric seat on a flow kind (W2.1, 2.5) |
| W5 | the **chain** (numbered) for versioning; a declared **clock** for stamps and spans | the chain; HaroBase's `recorded_at` | S2: a CLOCK, typed, with a sync policy and a kind (wall or monotonic), governing the sentence's events and never the chain's bytes |
| W6 | the **floored-llm points**; machine's service ceilings; a world ceiling | the four floors; model.call at stzlib | S3: a budget (tokens, cost, latency) on the point, the unit named by the world, never a default |
| W7 | **RATIONALE, CODE, CITES and the gate's why and todo** (Art. 1) | all of it | S5: a suggestion seat on REFUSAL and CONSTRAINT; a verb's example |
| W8 | the **resolved reference graph** of a language's kinds; the REFINE gate as the review path | StzuResolveSeats; CODEGRAPH rung 4 | S4: a threshold and the kinds it covers |

**Sorted.** *Judged THROUGH what exists* (WC1): W1.2, W1.5, W2.2, W2.3, W5.2, W7.1, W7.4, W8.5 -- **each is an article's rule seen from the
weave**, so the weave judges that the article it rests on is declared and holds, and builds no second mechanism: W1.2 on Art. 2; W1.5 on the
article a degrading element cites; W2.2 on Art. 3 and 4; W2.3 on Art. 3; W5.2 on Art. 2 and 3; W7.1 and W7.4 on Art. 1; W8.5 on Art. 4.
*Needs a declared seat* (WC2): the other twenty, by five seats: S1 dependency posture (1.1, 1.4, 1.7, 2.5, 6.2), S2 clock (5.1, 5.3), S3 budget
(1.3, 2.6, 6.1, 6.3, 6.4, 6.7, 6.9, 6.10), S4 cascade (8.1, 8.2), S5 metric, suggestion and example (2.1, 7.2, 7.5). The five are candidates,
each a D-entry when designed; the laws that stand: a clock never enters the chain's bytes (HF-127), and a budget is declared on the point
floored llm and named in the world's units.

## 4. Where the record plane holds a rule (WC3's anchors)

| rule | repository | anchor |
|---|---|---|
| W5.1 | HaroBase | `recorded_at` read inside, never handed in (CHARTER.md:88, :280); replay reads no clock (:251) |
| W5.2, W5.4 | HaroBase | hb_event insert-only (:92-93); `AS OF` and `AS KNOWN AT` as one verb with both axes (:277-279, :487) |
| W5.3 | HaroBase | transaction time never runs backwards (src/log.zig:282-283) |
| W6.1, W6.4 | stzlib | `model.call` in the catalog (base/security/stzSecurityEvent.ring:107): the monitor, without a budget |
| W6.12, W7.6 | stzlib | stzGovernance.ring:934-956: an actor in a loop states its coverage and a reversibility class |
| W6.13 | HaroBase, stzlib | erasable content (CHARTER.md:95-100); stzFieldTags' retention and redaction safeguards |
| W1.1, W1.4, W1.7 | stzlib | engine/src/resilience.zig: retry_delay_ms, RateLimiter, CircuitBreaker |

## 5. What is asked, of whom, and what waits

- **haro-charter** (mailbox): the per-seat severity design, and Zin's per-rule granularity beside it (finding 6); the guard green from
  `D:/GitHub/haro`. **WC1 waits for that report**; no court is forged before it.
- **the author**, at WC2's first rung and not now: whether a world must say what it leaves out of WEAVES (finding 8).
- **nobody else.** No stzlib or HaroBase edit is made at WC0, and no catalog kind is proposed.

## 6. Refused here, by the charge's order

- No fixture is written: the three counts go to the mailbox first. No court is forged and no guard is run.
- Nothing in zin/ is edited; ` M src/auto_tests.zig` in zin predates this desk and stays uncommitted.
- Zin's product rules are counted ABSENT, never built; no letter, no second compiler, no clock in the chain, no customer name.
- Nothing is done in `D:/GitHub/haro`'s main checkout or in the ringpp worktree's stale `haro/` (the worktree was fast-forwarded to
  private/next 2ea38fd and its leftover cache removed; no Haro work was done in it).
