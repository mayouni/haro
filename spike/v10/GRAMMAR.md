# Haro v0.10 -- the WORLD as versioned data: SYMBOL and PUBLISH

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.10 is the declaring altitude of Haro grown by what the charter's
section 3 `WORLD` row asks beyond cardinality (v0.2) and entry (v0.8): "the ontology
declared beside the grammar: entities, relations, constraints, as versioned data (C1,
`world.json`); never a mutable runtime store" (`haro/SPIKE.md`, the tenth rung). v0.10
refuses nothing v0.9 accepted (fixture A3 is v0.9's A2, unchanged).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `SYMBOL` | `KIND "flow"` the symbol kind a seat's value resolves to; `REF "calls"` the kind of ref the sentence contributes for it; `MESSAGE` the refusal when the world declares no such symbol | RingFlex's placement contract (C3 section 3.2): "a step's `INVOKES <name>` must resolve to a C1 symbol -- `flow:<name>` in the project's `world.json`"; `COMPENSATED_BY` beside it since the 2026-08-21 ruling. A seat typed by a SYMBOL holds a name the court cannot resolve from the file alone, so it is resolved in the court's LAST pass, only when a world is handed in (A1); a SYMBOL types a scalar seat (R3); one KIND, one SYMBOL (R4); KIND is required (R1) |
| `PUBLISH` on the `WORLD` | `[kind: symbolkind, ...]` the DECLARATION kinds a sentence contributes as symbols, and as which symbol kind | C1 says emitting is each court's job, and a court emits only what it can prove from its own artifact: Z publishes its flows, entities, norms and zones; F publishes one `process` per workflow and no `flow` -- "if this court declared the symbols it points at, resolution would be a check against itself" (A2, R2) |

## Grammar (EBNF), the v0.9 text with these additions

```
SYMBOL:      KIND string, REF string, MESSAGE string
WORLD:       ONE name_list, FIRST IDENT, ENTRY name_list, PUBLISH pair_list
pair_list    = "[" IDENT ":" IDENT { "," IDENT ":" IDENT } [ "," ] "]" ;
```

## What the forge makes of it

A court whose language declares a SYMBOL or a PUBLISH reads and writes JSON with
`expr_lib.ring`'s reader, and gains:

```
<lang>_court.ring check <file> [<world.json>]    with a world, every SYMBOL seat resolves
<lang>_court.ring world <file>                   the sentence's own C1 rows, as JSON
```

**Resolution is the court's last pass, after the references**, so a file is judged alone
exactly as before and a world adds one question. A name the world lacks is refused in
the SYMBOL's own words, prefixed `UNRESOLVED`, on the declaration's line. **No world at
all is a warning, not a refusal**: the verdict prints as before and a last line says
`warning NO_WORLD: no world to resolve against; N symbol reference(s) unresolved, which
is what C3 section 3.2 asks a project to close` -- C2's second rung, "undecidable without
more input", in RingFlex's reading. Names match case-blind, as C1 3.1 has it (stzGraph
lowers node ids). The rows a sentence contributes: one symbol per declaration of a
PUBLISH kind -- `{kind, name, span{file, line}, rationale}` -- and one ref per SYMBOL seat
written -- `{from, to, kind, span}`, from the sentence's first published declaration (the
process) to `<KIND>:<value>`, of the SYMBOL's REF kind -- under `{"world": <file stem>,
"contract": "1.0"}`.

## Measured

`f_v10.haro` is `f_v08.haro` with a `flow` SYMBOL typing INVOKES and COMPENSATED_BY and
`PUBLISH [workflow: process]`; `z_v10.haro` is `z_v07.haro` with `PUBLISH [flow: flow,
entity: entity, norm: norm, landing_zone: zone]`. The eight earlier fixture suites and
RingFlex's 26 are unchanged on them (the 26 now end `check` with the NO_WORLD line, which
the stage-11 judge reads past). The guard's stage 13 judges the world against RingFlex's
placement gate on RingFlex's own world fixtures, read-only: the lawful workflow resolves
against `world.json`; a world missing one flow refuses the step that names it, by the
step's and the flow's names; a world missing the compensating flow refuses the
compensating step by that flow's name; no world is a warning; and the rows the workflow
contributes are one `process` symbol and three `calls` refs with no `flow` symbol -- the
five gates of `tests/boundary-run.ring` sections C and D. Then the seam between two
forged letters: the world Z's court emits from `tontine.z` (flows `collect` and `indice`,
plus entity, norm and zone symbols) resolves `f/tontine_cycle.f`, an F workflow invoking
both; against RingFlex's world, which declares no `collect`, its first step is refused by
name; and the merged rows satisfy C1 3.2, every ref's ends being symbols. Nine checks,
the same bytes on `rnxc` and the oracle, first run; RingFlex's own gate 44 of 44 under
official Ring beside it.

## What it does not do, named

- The world is emitted and resolved, never STORED: no court writes a `world.json`
  anywhere; a project (zing's build, a harness) merges the rows its courts answer. The row
  of section 3 says "never a mutable runtime store", and this keeps it.
- `ON SURFACE` is not a SYMBOL: C3 does not ask for it and nothing emits a `screen`
  symbol yet (RingFlex's own boundary, kept).
- The C2 diagnostic envelope -- six fields, JSON -- is not emitted; Haro's refusal is one
  line, `<lang> (line N): message`, as every rung before. The envelope is a decision for
  the family's courts together, not this one's alone.
