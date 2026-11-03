# Haro v0.34 -- a question is judged against the schema the language declares, before it runs (COMPASS-KERN-03's field check)

**Written after `fixtures.json`, `q_cases.json`, the world `z_v34.haro` and the sentences `tontine/records.z` and `records_dangling.z`, which are the judges** (the W discipline:
fixtures first, prose second; they are 3d97769, before any code read a `FIELDS`; the cases added after the code, f16 to f19 and the `speaks` fragments, say so in the case file
and are named below). v0.34 answers the row COMPASS-KERN-03 of 2026-11-01, "a court that judges a Q or zql query against the declared schema before it runs, errors in the
domain's words", taken on the author's word ("KERN-03 field check"). It is the thirty-fourth rung (charter D48).

## The finding the rung started from: the schema was never declared

This desk answered on 2026-11-02 that the forged court's `ask` verb already refused an unknown `FROM`, a clause the ASK does not admit and a `WHERE` that computes, and that the
missing half was "one rung: resolve WHERE's names and ORDER BY's field against the FROM declaration's fields". Reading the Q world to build it found **no fields to resolve
against**. `FROM` names a **flow**; a flow in Z has `SEATS []`; the fields live on an **entity**; and nothing says which flow's records are which entity's. The other flow in the
tontine, `indice`, has records no entity describes at all (it computes a score into a record whose one input is a survey). So the question the row asks of a court cannot be
answered by a court alone: it needs the schema to be said first. The rung is the link, and then the check.

## What is new

| form | declares | where it comes from |
|---|---|---|
| `FIELDS seat.seat` on an `ASK` | where the schema of a kind asked lives: a **seat of every kind in FROM** that refers to one declaration, then a **list of `name: type` pairs** of that declaration | generic to any language that has an ASK; the meta-court judges that both seats exist and have those shapes (R1 to R7). A language with no `FIELDS` forges the court it forged before, byte for byte |
| `records: entity?` on Z's `flow` | **whose records walk the flow**: the entity a question's fields are read from | **Z's, not the language's.** zing is schema-less at the query and its sentences never wrote it. Optional on purpose: a flow that writes no `RECORDS` is not field-checked, and zing's reading stands (a missing field is missing) |
| the refusal `unknown_seat` of Z, `CODE "UNKNOWN_FIELD"` | the words a refusal of this kind is spoken in | the court already read the category for an unknown clause; the field check reuses the language's own sentence, appended after the specific one |

## What a question may name

For a `FROM` declaration whose `RECORDS` is written, the names a question may use are:

1. the keys of the entity's `FIELDS` pair list (`id, member, amount, round, status` for `collect`), then
2. the names the **flow's own steps `COMPUTE`** (a step of `indice` computes `score`, so a record of `indice` has `score`: zing overlays a computed value on the record by name),

and **no others**. A name is the **head** of a dotted path: `member.first` names `member`. Another flow's computed names and another entity's fields are not this flow's (f16, f17).
The check covers `WHERE` (every reference and the field inside an aggregate) and `ORDER BY`, is made **before the question runs** (f18: with no row to run it on, a typo is still
refused), and a refusal says **which clause, which name, which declaration, and what the declaration does have**:

    WHERE names 'ammount', which collect does not declare (its fields: id, member, amount, round, status) -- A question names only the fields its flow's records declare, or its steps compute.

## The divergence from zing, named

For a flow whose records are declared, **zing answers a question that names an undeclared field with no rows** (it reads a missing field as missing) and **Haro refuses**. This is
the point of the row, "an error in the domain's words, where silence is a typo's best friend", and it is a decision the author may reverse: the cost of reversing is the
`FIELDS` line of the ASK. None of zing's 25 pinned questions names an undeclared field, so **all 25 still hold on the unchanged `tontine.z`** (a flow without `RECORDS` is not
checked) and the new refusals are marked `haro_only`, as q20's is (HF-51). A name that a flow's entity declares and the rows happen to lack is lawful and matches nothing (f05):
a declared field is not a field every row has.

## How it is judged

| judge | what | holds |
|---|---|---|
| the meta fixtures | `fixtures.json`: three accepts (the clause, no clause, two kinds asked) and seven rejects, each by the fragment of why | 10 of 10, stage 1 |
| the cases | `q_cases.json`: 19 questions on `tontine/records.z` and `tontine.z`, the answer or the refusal each must have, on `haro` and its checked build, the two printing the same bytes | 19 of 19, stage 39 |
| **the twin** | `ask_court.py` reads the sentence with regular expressions, nothing of the court's code, and decides by itself 84 more questions (2 flows x 13 candidate names x WHERE, ORDER BY and an aggregate, and three that are lawful) | the court agrees on 84 of 84, stage 39 |
| the link | `records_dangling.z`: a `RECORDS` that names no entity is refused by the references pass, before any question | stage 39 |
| zing's questions | stage 10: the 25 questions of `v07/q_cases.json`, asked of `tontine.z` with Z forged from `z_v34.haro` | unchanged |
| the protections | `plants.py`: 21, each switched off in turn in a copy of `haro_lib.haro`, `forge.haro` or `ask_lib.haro`, judged by the fixtures and the cases | 21 of 21 load-bearing, the fixtures each fails printed beside it; `--plant` fails the stage |

## What it costs

The court library is **unchanged**: the field check is in `ask_lib.haro`, loaded only by a court forged from a language with an ASK, and the forge writes the fifth element of
`$aCourtAsk` only where `FIELDS` is declared, so every committed court of a language without it is byte-identical. Z's court gains the check and nothing else; no cold compile of
any other language moves (stage 6 states the figure).

## Not decided here

- **Which of zql's sentences declare `RECORDS`** is the stzzql desk's, and the sentences of the estate are read-only to this one. Until they do, a zql question is exactly the
  question it was. The court is Haro's; the schema seat is the sentence's.
- **A computed field's type** is not read: the pair list gives a field's `type` and the check does not use it (a type-aware comparison, `amount > "x"`, is another rung).
- **`SELECT` columns** do not exist in the grammar (`SELECT *` only), so nothing there to check.
