# ZIN-INVENTORY -- Zin's constitution read against Haro's mechanisms (ZC0)

```yaml
by:        constitution · claude-fable-5-1 · 2026-11-01 23:25
rung:      ZC0 of the constitution plane (softanza/memos/2026-11-01-constitution-launch.md, section 3), read-only:
           nothing in zin/ was edited; this file is the rung's one artefact
read:      zin cc98126 (2026-05-13, 1,248 commits): doc/design/ZIN_CONSTITUTIONAL_WEAVES.md (887 lines),
           ZIN_ZLM_CONSTITUTIONAL_LAYER.md (695), ZIN_PRIVACY_WEAVE_DESIGN.md (521), src/compiler/constitution.zig (78),
           constitutional.zig (576), constitution_commands.zig, src/csp/validators_stage4.zig, readme.md, build.zig, test.sh;
           ringpp next b43166c: haro/CHARTER.md (v0.2 + v0.3 amendments), haro/FINDINGS.md (to HF-123), haro/spike/v20/GRAMMAR.md,
           v20/refine.py, v06/GRAMMAR.md, v10/GRAMMAR.md, narrate_lib.ring, court_lib.ring, haro_lib.ring, z_v06.haro;
           stzlib base/refine/stzRefinableCode.ring (_wtc, 6389ddbee); harobanda declarative/machine/machine.stzu, README.md
measured:  zig build test --summary all -j2 in zin, 2026-11-01 23:18, foreground, nothing else running
```

Every line below says what was read [R] and what was measured [M]. A file:line is of the commit named above.

## 0. The three counts

| count | value | source |
|---|---|---|
| articles mapped onto a Haro mechanism that exists | **4 of 6**: 1 explainability, 2 reversibility, 4 predictable authority, 6 trust hierarchy | section 2, file:line on both sides |
| articles absent | **2 of 6**: 3 visible state, 5 organizational sovereignty -- each with a qualification its row states | section 2 |
| fixture candidates | **63 strict** (74 broad); **0** for the weaves | section 3, the census [M] |

The compass's hypothesis (reversibility = refinement, explainability = narrate, predictable authority = capabilities and
Harobanda, trust hierarchy = trust posture; visible state and organizational sovereignty absent) **holds**, with two
qualifications on Haro's side (3's typed-seat half is structural; 5's compiler description maps while its name does not)
and one correction on Zin's side: three of the six articles (2, 4, 6) have no enforcing rule in Zin's constitutional
pass, and a second engine re-reads 1, 4 and 6 as rules of its own (section 1).

## 1. Zin's side: what the record holds

1. **The articles** are six, hard-coded, "Pre-Phase 0" (`constitution.zig:35-40`); `parseConstitution` returns the
   default (`:57-59`); `zin constitution check` prints every article as "(Stage 6 STUB)" and exits 0
   (`constitution_commands.zig:126-147`). The text a user reads for each article is `articleContext`
   (`constitution_commands.zig:83-93`) [R].
2. **The enforcing pass** is `enforce` in `constitutional.zig:28-183`, run after semantic checks. It holds four rules:
   Art. 1 `ZIN-C001` a declaration has a non-empty name (`:31-54`); Art. 3 `ZIN-C003` no `any` type in a governed entity
   (`:56-80`); Art. 1 `ZIN-C001-ZPT` a design override names its `INTENT` (`:86-150`, doubled by `ZPT-E021` in
   `semantic.zig:1966-1976`); Art. 5 `ZIN-C005-ZPT` a design override cannot remove the focus ring (`:152-178`, the
   comment calls it "Keyboard Sovereignty"). `articles_checked` is 2, or 4 when a design override is present
   (`:180-183`) [R]. Its tests assert exactly that (`constitutional.zig:451`, "articles_checked is always 2") [R].
3. **A second reading** runs in the CSP engine's stage 4 (`csp/validators_stage4.zig:1-40`): Art. 1 = a rule of
   critical or blocking severity has a cause; Art. 4, renamed "Trust Boundary" = an actor of elevated trust declares at
   least one permission; Art. 6, renamed "Severity Alignment" = a rule named alert, warning or critical is above `.info`.
   Its own header says the AST articles "don't translate cleanly to the chunk model" [R].
4. **A diagnostic carries its article**: `article: ?u8` on the node (`diagnostics/types.zig:437-448`, a test), rendered
   by the formatter (`formatter.zig:756-961`, five tests), with message templates `ART1_UNTRACEABLE`, `ART3_HIDDEN_STATE`
   (`templates.zig:100-262`) [R]. This is the number-and-article shape of COMPASS-KERN-06, already Zin's.
5. **Named and parsed, never judged**: `IRREVERSIBLE` is a keyword (`lexer.zig:42`); `COMPENSATION` is a seat of
   `RETRY_POLICY` lowered to IR (`ir_emitter.zig:2322-2342`); `CAN escalate` is an actor's declared permission
   (`ir_emitter.zig:10737`); `TrustLevel` is five levels 0-4 on an actor chunk, untrusted to privileged
   (`csp/chunk_types.zig:343-349`); a deployment has a `constitutional_gate` seat (`targets/docker_plugin.zig:344`).
   No rule reads any of them against an article [R, grep of every `.article =` and `ZIN-C00` site].
   `src/compiler/trust/` is pack signing (`roots.zig:1-12`), another meaning of the word.
6. **The weaves** are design: `ZIN_CONSTITUTIONAL_WEAVES.md` declares **eight**, not seven (W8 Structural Integrity,
   with W8.1-W8.5), `ZIN_PRIVACY_WEAVE_DESIGN.md` grows W4 from 5 rules to 16, and `ZIN_ZLM_CONSTITUTIONAL_LAYER.md` is a
   constitution for the model (four `Zsp` constructs; declared source, versioned, an amendment process, a transparent
   refusal that does not moralise). In `src/` only `roadmap_data.zig:1621-1640` names them, as a roadmap entry.
   **No pass, no test** [R, grep of `W[1-8].N` and `weave` across `src/`].
7. **The customer's constitution text** exists as a ZML dialect block (`dialects/zml/parser.zig:137-228`: "minimum viable
   constitution", "full banking-style constitution with principles array") and ZinForj records a `constitution_hash` per
   build and a `constitutional_violations` table on agent outputs (`zinforj/store.zig:46, :172-214`;
   `zai_engine.zig:3565, :3574`). Product, by the ruling; read for shape only.

## 2. The mapping, article by article

| article (Zin's words, `constitution.zig:35-40`) | Zin's enforcing rule | Haro's mechanism | verdict |
|---|---|---|---|
| **1 Explainability** -- "every declaration traces to a declared artifact" | `ZIN-C001` (`constitutional.zig:31-54`), `ZIN-C001-ZPT` (`:86-150`), `ZPT-E021` (`semantic.zig:1966-1976`); CSP Art. 1 (`validators_stage4.zig:304-351`) | `RATIONALE` mandatory on every declaration, judged: `haro_lib.ring:1000-1001`; charter `:181`, `:441`, principle 5 (`:739`). The refusal explains: the C2 envelope's `why` and `todo`, `court_lib.ring:1678`; principle 4 (`:738`). The run explains: `NARRATE`, `narrate_lib.ring:93` (NarrateRun), `:168` (NarRefuse), `:216` (NarTellRun); charter `:184`, D12 (`:866`) | **MAPPED.** Zin asks that a declaration say why it exists; Haro's `RATIONALE` is that, refused when absent, and the narration says why a run did what it did |
| **2 Reversibility** -- "every state mutation has compensation or IRREVERSIBLE marker" | **none**: declared (`:36`); `IRREVERSIBLE` a keyword (`lexer.zig:42`), `COMPENSATION` lowered (`ir_emitter.zig:2322-2342`), neither judged; W1.2 is its design | refinement: "the inverse is computed before the refinement lands; a revert is its own event; nothing is erased", charter 6.5 (`:426-428`); a revert is a sentence `REVERTS n`, gated like any other, `v20/GRAMMAR.md:142-145`; `refine.py:1956` (Model), `:2010` (revert), `:2077` (audit); `stzRefinableCode.ring:5-6, :15, :29`; measured: refused as `:llm`, admitted as `:trusted`, "reverted byte for byte", charter `:522-523` | **MAPPED**, and stronger here: Zin marks what cannot be undone; Haro computes the inverse first and refuses a change whose inverse it cannot write |
| **3 Visible State** -- "consequential state has declared access paths" | `ZIN-C003` no `any` type (`constitutional.zig:56-80`); CSP has no Art. 3 | the `any` half is structural: a seat is typed by its declaration and the court parses a seat's text with the expression's own menus (charter `:441` "seats are typed"; `v06/GRAMMAR.md`, fixture A3). The access-path half: the `WORLD` is versioned data, "never a mutable runtime store" (`v10/GRAMMAR.md:1-8`), and the audit chain as a query is **owed** to the governor (charter `:150-151`) -- stated, not built, judged by no court | **ABSENT** as a judged article: nothing in Haro refuses a state that has no declared access path. The typed-seat half is noted so ZC3 does not rebuild it |
| **4 Predictable Authority** -- "no implicit permission escalation" | **none** in the pass: declared (`:38`); `CAN escalate` is an actor's own seat (`ir_emitter.zig:10737`), judged by nothing; CSP "Trust Boundary" (`validators_stage4.zig:360-403`) is the one running rule; W3.7 (asymmetric validation of a grant) is its design | the gate's governance stage: a declared risk tier -- undeclared never proceeds -- the actor's permission, an authority that covers the tier (`v20/GRAMMAR.md:99`; charter 6.4, `:419-423`; `stzRefinableCode.ring:128-132, :261-268`); **widening a rule is a tier-4 act whatever the point's tier, tightening the point's own** (`v20/GRAMMAR.md:107-110`; HF-102, `FINDINGS.md:98`); least authority: reads closed by default (D30, `:1050`), exports nothing by default (D31, `:1055`), the write surface is what a task names (D26, `:1033`); the door: principle 12 "no effect without a door" (`:746`, `:954`; HF-70, `FINDINGS.md:130`), Harobanda's `CAPABILITY` "the declaration only grants or refuses it -- silence refuses" (`machine.stzu:40-43`; `README.md:204`; charter `:452`) | **MAPPED.** Zin's article is a sentence; Haro's is a stage that runs on every change, and it is asymmetric already -- W3.7's shape, built before W3.7 was read |
| **5 Organizational Sovereignty** -- "LLM agents sandboxed; no live writes" (`:39`); the user text adds "Organizations retain full sovereignty over their data" (`constitution_commands.zig:89`) | `ZIN-C005-ZPT` (`constitutional.zig:152-178`): a design override cannot remove the focus ring -- an accessibility rule of the Zpt pillar, "Keyboard Sovereignty" by its own comment; nothing else | the **description's** half maps: "the agent proposes; it never commits" (charter `:144-146`; Aicha "bound by the rule that a model proposes and never commits", `:458`); a model-composed proposal is refused at `policy/*` "not by convention, by construction" (6.4, `:422-424`; `v20/GRAMMAR.md:108`); principle 12 (`:746`). The **name's** half -- an organization's data under its own authority, W3's "no ungoverned data movement" -- has no mechanism: Z declares `LANDING_ZONE`s as the places records land (`z_v06.haro:77-78`, `:16`; `tontine.z:61`), not as jurisdictions, and no court judges a movement between them | **ABSENT as named** (the compass's reading, the one the ruling imports); **present as Zin's compiler describes it**. ZC3 builds the name's half on the zones Z declares, and does not rebuild the description's half |
| **6 Trust Hierarchy** -- "Level 0-4 constraints respected" | **none** in the pass: declared (`:40`); `TrustLevel` 0-4 is a field on an actor chunk (`csp/chunk_types.zig:343-349`); CSP "Severity Alignment" (`validators_stage4.zig:413-505`) is a naming rule, not a trust rule | trust posture: four postures ranked, `trusted` 3, `external` 2, `sandboxed` 1, `llm` 0, and a point's `floor` the origin must clear -- "origin is not identity: the same actor, the same value" (`v20/GRAMMAR.md:100`; `stzRefinableCode.ring:152-166, :187-193, :273`); `REFINE`'s `FLOOR` seat and its closed menu, `haro_lib.ring:1993-2010` ("is not a posture: trusted, external, sandboxed or llm"); charter 6.4 (`:422-424`), `:499-500`, `:522-523` [M] | **MAPPED.** Zin's five levels on an actor against Haro's four postures on an origin with a floor per point. The count differs (5 against 4) and the subject differs (actor against origin): a fixture question for ZC2, not a mechanism gap |

## 3. The fixture candidates -- the constitutional subset of Zin's tests

**3.1 The figure, reproduced and corrected.** `readme.md:3` and `:202` say 4,396 tests; `:154` says 1,979 (written at
49b40b5, 2026-03-28). At 1724807 (2026-05-06, the commit that wrote 4,396) `src/` held **4,397** `test` blocks in 241
files [M, `git grep`]; `build.zig:131-139` generates `src/auto_tests.zig` from every `.zig` under `src/` except
`main.zig`, `tests.zig` and itself, and `main.zig` holds one test block: 4,397 - 1 = **4,396**. At HEAD cc98126, 150
commits later: **4,825** test blocks in 269 of 283 files, `main.zig`'s one skipped, and
`zig build test --summary all -j2` answers **"4824/4824 tests passed"** -- 5 of 5 steps, 21 s to run, 24 s to compile
[M, 2026-11-01 23:18-23:19]. The compass's "164 `test` blocks across 269 files" is two counts: 164 is the top-level
`src/*.zig` only; 269 is the files with tests at every depth. Zin's tree carried ` M src/auto_tests.zig` before this run
and the same after it -- the generator's write, not this desk's; nothing was committed.

**3.2 The census.** Every test block (a `test "..." {` line at column 0 to the `}` at column 0) was read for an article
(`Art N`, `ZIN-C00N`, `.article = N`, `ARTN_`, the article's name), for "constitution" and for a weave (`WN.M`,
"weave"): 133 blocks matched; each was then read by hand into mechanism or product, and the mechanism files were read
whole (every test in `constitutional.zig` exercises `enforce` whether or not its name says Art). The script and its
table are in the desk's scratchpad (`zin_census.py`, `zin_census.tsv`), reproducible from the commit.

**3.3 Strict: 63**, in three kinds.

| kind | count | where (file:line of the `test` line) |
|---|---|---|
| **A** -- a rule exercised: a declaration accepted or refused under an article | **40** | `constitutional.zig` 18 (`:187-575`: Art. 1 twice, Art. 3, Art. 5-Zpt); `csp/validators_stage4.zig` 17 (`:283-505`: Art. 1, 4, 6 in the chunk reading; the four `recheckConnected` tests excluded); `simulation/k2_zml_session1.zig:243, :259`; `simulation/s9_integration.zig:577` (S9f.2); `simulation/t_validation_quality.zig:623` (W-diag); `simulation/p_integration.zig:102` |
| **B** -- the constitution's shape: six articles, numbered 1 to 6, named, parsed idempotently | **13** | `constitution.zig:62, :67`; `constitution_commands.zig:151, :158, :163`; `simulation/core_types_through_cli.zig:124-170` (C1.1 to C1.8) |
| **C** -- a refusal carries its article (KERN-06's shape) | **10** | `diagnostics/formatter.zig:756, :848, :886, :920, :961`; `diagnostics/types.zig:437`; `diagnostics/templates.zig:100, :143, :262`; `simulation/core_types_through_cli.zig:252` (D1.8) |

**3.4 Broad adds 11, to 74**: `s9_integration.zig` S9f.1, S9f.5, S9f.6, S9f.15, S9f.16 and S9h.4 (the constitutional
stage among the pipeline's others, 6); `zlm/tests/smoke.zig:200` and `csp/evaluation.zig:1818` (Art. 6's severity rule
reached end to end, 2); `lexer.zig:472` (`IRREVERSIBLE` is a keyword, 1); `test.sh` T204 (`:1145`) and T249 (`:1356`)
(the CLI prints "Constitutional Validation", 2).

**3.5 Weaves: 0.** No weave is code, so no test exercises one.

**3.6 Not candidates**, the rest of the 133: ZinForj's `constitution_hash` and `constitutional_violations` (32 tests),
the providers' `constitutional_annotation` metadata (`provider.zig:376-379`; 7), the ZML dialect's declared constitution
block (7 -- a customer's text, the product's), target plugins' `constitutional_gate` seat (11), pipeline and IR plumbing
(7), and 33 blocks that merely hold the word "article" or "regulator".

**3.7 How a candidate becomes a fixture** is ZC2's work, not this rung's, and one shape is already visible: a Zig test
asserts `violations == N` on a source string; the Haro fixture is a sentence of a declared language with an accept, or a
refusal fragment naming the number and the article (the v06 shape: `id`, `name`, `source`, `expect` or the fragment).
Kind A re-expresses one to one where Haro holds the mechanism; kind A's Art. 3 rows re-express against ZC3's mechanism,
because a seat without a type is already unparseable here (structural) and the article's refusal must be about an access
path; kind B is a handful of fixtures of the governance sentence itself; kind C is one rule of the court (every refusal
under an article names it), held by every refusal fixture at once.

## 4. What this inventory found that the launch prompt did not say (carried by HF-124)

1. Zin's constitutional pass enforces two articles (1, 3), a third (5) only as a UI rule; articles 2, 4 and 6 are named
   and never judged there; the CSP engine re-reads 1, 4 and 6 as rules of its own and says so; `check` is a stub.
2. The weaves are eight, not seven; none is code; W4 alone is 16 rules in its own document.
3. Article 5 has three readings in Zin's own record: its name, its compiler description, its one enforced rule.
4. The readme's 4,396 is 1724807's count; today 4,824 pass [M]. The compass's 164 and 269 are two different counts.
5. Trust: Zin's five levels on an actor; Haro's four postures on an origin, with a floor per point.
6. W3.7's asymmetry (a grant is held to a higher authority than a restriction) is already Haro's gate (widening = tier 4).
7. A diagnostic that carries its article number is already Zin's shape (section 1.4) -- KERN-06 asks Haro for what Zin had.

## 5. Refused here, by the launch's order

- No fixture is written: the three counts go to the first memo first.
- Nothing is ported: the Zig was read, never run except as Zin's own test suite.
- `zin/` is untouched; ` M src/auto_tests.zig` predates this desk and stays uncommitted.
- No letter is proposed; no product part (pillars, foundry, IDE, ZinScript, ZLM's constitution) is carried.
