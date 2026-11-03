# One format, and pattern rules over it -- COMPASS-REBOL-06 and 07, a design memo

**What this is.** The design memo the author's two rulings of 2026-10-30 asked haro-charter for, routed by the Compass (`softanza/
mailbox/compass.md`, 2026-10-30 23:54) and carried by Central (2026-10-31 00:12):

> **COMPASS-REBOL-06, RULED YES.** The canonical printed text of Haro's graph is the family's one format, in which a declaration, a memo
> and a program are all written, so one LOAD serves every letter (the REBOL block, with a court).
>
> **COMPASS-REBOL-07, RULED YES.** The courts and Q need pattern rules over blocks of typed values, as data, total and judged: Red's
> Parse without the escape into the host and without the documented infinite loop.

It **proposes and rules nothing** beyond those two rulings. Section 6 lists what is the author's to decide. Everything it claims was
measured first, in `haro/study/rebol/`, and the fixtures were written before any reader, printer or engine (17d9b4e): **21 printing
fixtures and 53 pattern fixtures, all holding, and 9 of 9 protections load-bearing** (each switched off in turn fails the fixture it
exists for). Two fixtures were added after the reader, each because a plant showed that no fixture pinned the protection it tested;
both say so in their names.

---

## 1. The questions, as routed

**06**: what the ruling costs and the order; which of the three textual shapes today -- C6 declarations, the memo shape of C9 and
`.pia`, each face's spelling -- becomes a printing of the canonical text first; what court proves two printings equal; whether C6 and
the memo shape stay as spellings or are retired.

**07**: the home of the pattern rules (inside Q, inside the court programs the forge emits, or a Commons facility); the bound that
keeps them total (W's: no loops, no recursion, no user functions; Parse's `into` and `collect`/`keep` as the model; `paren!` and
`while` refused); the fixtures that judge them, before prose.

## 2. What the family writes today, measured

`haro/study/rebol/census.py` (21 s, read-only, every tree at its working state of 2026-11-02) reads every text of each shape with one
reference reader (`block.py`) and asks whether it reads, and whether text -> block -> canonical text -> block gives the same block back.

| shape | texts | read by the one LOAD | round trip | notes |
|---|---|---|---|---|
| Haro's meta-language (`.haro`, the spike) | 29 | **29** | **29** | canonical printing 238,565 bytes against 237,620 written (+0.4%) |
| the letters' sentences (the spike's worlds) | 62 | **61** | **61** | the one refused is `f/operator-in-guard.f`, a fixture written to be refused; +2.9% bytes |
| the machine language (`.stzu`) | 2 | 2 | 2 | +0.1% bytes |
| `.zql` (zing), an elder | 19 | 0 | -- | single quotes: D-ZQL-1, recorded in C6 section 6 |
| `.zui` (StzZui), an elder | 72 | 0 | -- | `//` comments: D-ZUI-1, recorded |
| `.wflow` (RingFlex), an elder | 29 | 5 | 5 | `->` in 19 files and `=` in 5: **not recorded** in C6 section 6 (HF-133) |
| memos, as C9's `_StzOutputParseMemo` reads them: the journal's yaml fences | 1,241 | 109 (9%) | 109 | |
| the same, the mailboxes' | 790 | 11 (1%) | 11 | |
| the same, `.pia` agents (roster, stzlib, harobanda) | 18 | **18** | 18 | |
| memos, the **house reading** (C9's rules and three more, section 3.4): the journal | 1,241 | **1,007 (81%)** | 1,007 | |
| the same, the mailboxes | 790 | **572 (72%)** | 572 | |
| a program: the Ring++ face, 300 Softanza base files | 300 | 0 | -- | Ring's lexis (`=`, `'`, `#`, operators) is not C6 |

Five things follow, and each shapes the design.

1. **C6 is already one format for everything Haro forges.** Every `.haro` file and every sentence of every letter reads through one
   LOAD and survives the canonical printing, within half a percent to three percent of the bytes written: the declaration shape is
   *nearly canonical already*. What is missing is not a format but its two instruments -- one reader (the spike has two C6 lexers,
   `StzuTokenize` in the meta-court and `CtTokenize` in every forged court) and a printer (none exists: `haro.ring` prints its verdict,
   never a declaration).
2. **Haro itself diverges from C6, unrecorded.** C6 3.7 writes `DEFINE <KIND> <name> ( ... )`; every Haro declaration and sentence writes
   `DEFINE KIND name AS ( ... )`. Haro also writes `?` after a seat type -- after a list type too (`[in_tongue]?`) -- which C6's lexis
   does not have. Haro was born after the Commons, so by C6's own section 6 ("no divergence licence") each is a finding against C6.
3. **"The memo shape" is two shapes.** C9's reader reads every `.pia` and 9% of the journal. The house memo -- what every desk writes --
   wraps prose onto deeper continuation lines, writes keys with spaces (`the page:`), and writes a paragraph under a key; with those
   three rules 81% of the journal and 72% of the mailboxes read, and every text read survives its own round trip. What is left (234 and
   218 texts) is prose written at a field's own level, which no indentation rule reads without guessing.
4. **A memo does not cross into C6 for one reason: the quote.** Of the 1,007 journal memos the house reading reads, 400 survive
   memo -> block -> C6 text -> block; the other 607 hold a `"` in their prose, and a C6 string has no way to carry one. With **one
   amendment -- a doubled quote `""` inside a string is one quote** (SQL's and CSV's convention, no backslash) -- **1,007 of 1,007 and
   572 of 572 cross and come back, and the 97 C6 files read alike with and without it.** Memo keys are the second gap: 24% of the
   journal's keys and 33% of the mailboxes' are not C6 identifiers (`COMPASS-REBOL-06`, `the page`), so a pair's key must be allowed to be
   a string.
5. **A program is not C6 text, and nothing measured here makes it one.** The program graph already has a canonical printing and a
   court -- `rnxc fmt`, rung 3 of `CODEGRAPH.md`, 6,003 of Softanza's 6,061 files printed byte for byte as the reference -- but in Ring++'s
   lexis. Whether a Haro program is *written* as a block is a question of Haro's own program syntax (section 6, Q-B3).

## 3. COMPASS-REBOL-06: the design

### 3.1 The block, and the one LOAD

The canonical text is C6, read by one LOAD into a **block**: a sequence of typed values.

| value | written | example |
|---|---|---|
| word | `lower_snake` | `tones` |
| keyword | `UPPER_SNAKE` | `DEFINE` |
| string | `"..."`, folding a continuation's indent (C6 3.2); `""` inside is one quote (proposed) | `"the tones"` |
| number | C6 3.3 | `-1.5` |
| path | words joined by dots | `deposit.amount` |
| pair | `key: value`, the key a word, keyword, path or (proposed) string | `name: text` |
| list, group | `[ ... ]`, `( ... )`, items separated by commas, a trailing comma allowed | `[plain, formal]` |
| row | an item of several values | `CODE "X"` inside a group |
| optional | Haro's `?` after any value (to be recorded or refused in C6, Q-B1) | `[intents]?` |
| comment | `--` to the line's end: a value of the block, in its place | `-- why` |

A comment is never lost; its position *inside a row* is the one named loss besides layout (it moves after the row). The reader is
`block.py`; its rules are the fixtures' (L01-L07 read alike, D01-D05 read differently, F01-F06 refused).

### 3.2 The canonical printing

One spelling per block: a declaration a paragraph and a blank line between them; a group's items one a line, two spaces deeper, a
comma after each but the last; a list inline unless it holds a comment or a group; a string on one line; a comment on its own line.
Fixtures K01 and K02. The printer is the formatter, as `CODEGRAPH.md` R6 says of programs.

### 3.3 A spelling, and the court that proves two printings equal

A **spelling** is a reader and a printer to and from the block. C6 is the canonical spelling; the memo is a spelling; each program
face is a spelling. The court has `CODEGRAPH.md`'s rung-3 shape, three questions from the cheapest to the one that matters:

| | asks | measured here |
|---|---|---|
| R | text -> block -> its own printing -> block: the same block | C6: 97 of the 97 it reads (Haro's 92, the five `.wflow`); memos: 1,597 of the 1,597 the house reading reads |
| X | two spellings of one thing load to the same block (and two different things do not) | fixtures L05, L06 and D04; all 1,597 memos into C6 and back once a string can hold a quote (400 + 159 + 18 without it) |
| F | fixtures written first: same, differ, canonical, refused | 21 of 21 |

The court never compares bytes of a human's writing: it compares blocks, and the canonical printing is the only text it ever writes.

### 3.4 The memo spelling, made exact

The house reading is C9's reader and three rules, each measured: **(a)** a line deeper than a line that holds a scalar, and not a list
item, continues that scalar (under a list element's first field, a deeper `key: value` is its next field instead); **(b)** a map
field's key may hold spaces; **(c)** a deeper paragraph under `key:` that opens with neither a field nor a list item is the key's text.
Every scalar is a string. Proposed as the declared memo spelling; `_StzOutputParseMemo` (stzlib, `stzOutputSchema.ring:622`) grows
the three rules and keeps every text it reads today: on all 138 (109 + 11 + 18) the house reading gives the block C9's reader gives.

### 3.5 Order and cost

| step | what | cost | why in this order |
|---|---|---|---|
| **1** | **C6 declarations become the canonical text**: one reader in Ring (`block_lib.ring`, replacing `StzuTokenize` and `CtTokenize` -- one LOAD for the meta-court and every forged court), a canonical printer (`haro.ring fmt <file>`), and the printing court as a guard stage over every `.haro` and sentence | one rung of the spike; nothing visible changes (every court prints the same verdicts) | it is 99% true already; the rest is two instruments | **BUILT 2026-11-03 as Haro v0.30** (`spike/v30/GRAMMAR.md`, guard stage 35, D44): `block_lib.haro` is the one lexer, loader and printer; `haro.haro <file> fmt` the printer at the command line; every court prints the bytes it printed. Written before the cut, this row says `.ring` and `haro.ring`: read `.haro` and `haro.haro` (CLAUDE.md, "The cut").
| 2 | **pattern rules** (07, section 4) over the blocks step 1 reads | one rung | 07's rules are data only when they are read by the one LOAD | **BUILT 2026-11-03 as Haro v0.31** (`spike/v31/GRAMMAR.md`, guard stage 36, D45): the engine in Haro, `spike/pattern_lib.haro`, judged beside the Python reference down to the step; what remains of 4.3 -- the declaration `DEFINE PATTERN` in the meta-language and the court collecting its sets -- is the next rung. Written before the cut, this row says `.ring`: read `.haro`.
| 3 | **the memo spelling**: the house rules in C9's reader, a memo printer, and two C6 amendments -- the doubled quote and a string as a pair's key -- at Ringua, C6's owner | an amendment of C6 and a change to stzlib's reader; every desk's memos then read by one reader | the amendments are another desk's to make; nothing in steps 1 and 2 waits on them |
| 4 | **programs**: a block printing of the L1 graph (an export, so tools read programs with the one LOAD), the Ring++ face staying the human spelling under its rung-3 court | small for the export; the rest is Q-B3 | a program is not C6 text, and whether it becomes one is the author's |
| -- | **the elders** (`.zql`, `.zui`, `.wflow`) read by the one LOAD | their owners' changes | each diverges lexically; until one converges it is a spelling, read by its own reader |

### 3.6 Stay or retire

**Nothing is retired.** C6's declaration shape is *promoted*: it is the canonical text. The memo shape stays a spelling, because it is
how every desk and every model writes (1,579 memos read), and its strict C9 subset stays what an agent's output is validated against.
`.pia` stays (18 of 18 read as written). Retiring the memo shape would cost every desk its habit and every model its most natural
output, and buys nothing the court does not already give: a memo and its C6 printing are one block.

## 4. COMPASS-REBOL-07: the design

### 4.1 The rule language

A rule is a C6 list, read by the one LOAD: a grammar is data. Pattern words are keywords; a lower_snake word, a string or a number in a
rule matches itself; `LIT v` matches any value as itself (a keyword included); a nested list is a sub-rule.

| words | meaning |
|---|---|
| `WORD STRING NUMBER KEYWORD PATH PAIR LIST GROUP ROW SKIP`, `END` | one value of a type, any one value, the end |
| `OPT ANY SOME`, `REPEAT n [m]` | repetition, greedy, as PEG |
| `OR` | ordered choice that commits (Parse's `\|`, PEG's `/`): P37 |
| `NOT AHEAD` | look without consuming |
| `INTO` | descend into a list, a group, a row, or a pair (read as its key, then its value) |
| `TO THRU` | skip up to, or past, what matches |
| `COLLECT KEEP` | Parse's `collect`/`keep`; a top-level `COLLECT` is the result, as Parse returns it |
| `RULE name`, `MEMBER name` | a named rule; a value drawn from a declared SET |

A rule matches only when it consumes its whole input. Fixtures P01-P37.

### 4.2 The bound that keeps them total

Each is a refusal **at declaration**, never a check at match time:

- **no recursion**: named rules form a DAG (X01, X02);
- **every repetition moves**: `ANY`, `SOME` and `TO` over a rule that can match nothing are refused by a nullable analysis (X03-X05, X16),
  so each turn consumes a value of a finite input -- **Parse's documented infinite loop cannot be written**;
- **no host**: a group in a rule (Parse's `paren!`) and `WHILE`, `DO`, `EVAL`, `IF` are refused (X06, X07, X15);
- **no editing**: `CHANGE`, `INSERT`, `REMOVE` are refused -- a pattern judges and never edits (X08);
- **data, not code**: `MEMBER` reads a SET the court collects (a menu's words, a kind's seats, the values of other declarations'
  list seats, a world's symbols); a rule never computes one.

`INTO` descends into a strictly smaller value, so depth is the input's. Matching is PEG with a packrat memo: **at most rule nodes x
input positions steps**, held on every fixture (reached exactly only on the empty input, P06), and every protection is load-bearing:
switched off, recursion fails X01 and X02, the nullable check X03, X04, X05 and X16. `TO` and `THRU` scan forward, which can add a
factor of the input's length; that is a polynomial, named, not a loop.

### 4.3 The home

**Declared in Haro's meta-language, judged by the meta-court, run by one library.** A pattern is a declaration of the language it
judges -- `DEFINE PATTERN name AS (MATCH [...], OVER <seat or kind>)`, its sets named from the language's own records -- so the bound in
4.2 is the meta-court's refusal, in the declaring language's words; and every forged court, and Q's `ask` verb, load one
`pattern_lib.ring`. Not inside Q alone (the courts need it first: stzzui's value join is a court's constraint). Not per court (one
engine, judged once). Not a Commons facility yet: the Commons fixes form, never meaning (C6 section 1), and a second engine in another
runtime is exactly what COMPASS-REBOL-03's twin court would then have to judge. It becomes Commons when an elder or a second runtime
asks for it.

### 4.4 What it answers, and what it does not

- **stzzui's value join (Central's item 3 of 2026-10-31):** every value of one list seat is drawn from the union of other declarations'
  list seats -- `[INTO [ANY MEMBER rights]]`, the set collected by the court (P18-P20). Answered.
- **A form stated once and judged everywhere:** Haro's declaration form as one rule, `[LIT DEFINE KEYWORD WORD LIT AS GROUP LIT RATIONALE
  STRING]`, over every C6 file the LOAD reads: 87 of 97 match, in 13,008 steps and 0.9 s (the largest input 1,113 values); the 10 that
  do not are five fixtures written to be refused and the five `.wflow` files that omit `DEFINE` (D-WFLOW-1).
- **NOT COMPASS-KERN-03's field check, and this corrects what this desk said on 2026-11-02:** a Q question (`SELECT * FROM deposits WHERE
  amount > 10`) is not C6 text -- `*` and `>` are not in its lexis -- so a pattern cannot read it until Q's question is a block. Resolving
  WHERE's names against the FROM kind's fields directly in `ask_lib.ring` is the cheaper rung, and stays the proposal.
  *Built 2026-11-03 as v0.34 (D48), with one more correction: the FROM kind had no fields to resolve against -- a flow has none, the entity holds them, and nothing linked the two -- so the rung began with the link (`FIELDS` on an ASK, `RECORDS` on Z's flow).*
- **NOT Central's item 4** (a seat shared by ten kinds): that is composition of declarations, not a pattern over a block.
- **NOT the conditions and expressions** inside `WHEN "..."` strings: they have their own lexers (`CondTokenize`, `ExTokenize`) and stay
  strings. Making them blocks would put operators into C6's lexis; not proposed.

## 5. Costs, risks, and what would make this wrong

- **The house memo is a convention, not a grammar.** 19% of the journal and 28% of the mailboxes write prose a reader cannot place. The
  canonical memo printing ends that for every memo printed by a tool; memos typed by hand keep the risk until a desk's own check reads them.
- **A doubled quote is a C6 amendment**, and C6 is a contract several languages pin. Measured harmless on every C6 file (97 alike, 0
  differ); the elders that pin C6 v1.0 would see a new string form.
- **`AS` and `?`**: recording them in C6 or removing them from Haro is the author's (Q-B1); either way, one of the two documents changes.
- **The pattern engine is a model.** `pattern.py` is the reference, as `l1.py` was for `rnxc fmt`; the Ring library in step 2 is judged by
  the same fixtures, on rnxc and the oracle.
- **What would make this wrong:** a family text that the block cannot hold without a new value kind every time (each would be a finding,
  as `?` was); or patterns that need recursion to say what a court needs (none of the 53 fixtures, nor the value join, does).

## 6. Decisions that are the author's

- **Q-B1** Haro's `AS` in the declaration header and its `?` mark: recorded in C6 as amendments (recommended: both are in every Haro file),
  or removed from Haro.
- **Q-B2** the two C6 amendments the memo spelling needs: a doubled quote inside a string, and a string as a pair's key (recommended: both;
  measured harmless). They are Ringua's to write, on the author's word.
- **Q-B3** a Haro program: written as a block (one LOAD for programs too, a new program syntax), or the Ring++ face as the program's spelling
  with a block export (recommended: the export now, the syntax when the computing altitude is designed).
- **Q-B4** the elders: converge on C6's lexis, or stay spellings with their own readers -- their owners', on the author's word.

## Files

- **4.3, built** (Haro v0.32, 2026-11-03): `DEFINE PATTERN` in the meta-language -- `spike/grants_v32.haro` the world, `spike/pattern_judge.haro` the court's half, `spike/v32/` (fixtures first, the court cases, the plants, GRAMMAR.md).

- **Step 2, built** (Haro v0.31, 2026-11-03): `spike/pattern_lib.haro`, `spike/pattern.haro`, `spike/v31/` (fixtures first, the court, the plants, GRAMMAR.md); the reference `pattern.py` fixed and extended.

- **Step 1, built** (Haro v0.30, 2026-11-03): `spike/block_lib.haro`, `spike/block.haro`, `spike/v30/` (fixtures first, the court, the plants, GRAMMAR.md).

- `haro/study/rebol/gen_fixtures.py`, `pattern_fixtures.json` (53), `printing_fixtures.json` (21) -- written first (17d9b4e); D05 and F06
  added after the reader, each found by a plant.
- `block.py` -- the one LOAD, the C6 and memo readers (C9's and the house reading), the canonical printers, the printing court.
- `pattern.py` -- the pattern engine and its court; `plants.py` -- the 9 protections, each switched off in turn.
- `census.py`, `results.json` -- the measurements of section 2.
