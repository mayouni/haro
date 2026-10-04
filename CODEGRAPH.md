# Haro -- the code graph beneath the faces

**Status: v0.1 DESIGN MEMO, 2026-10-04** (COMPASS-HARO-05). Written by the `haro-charter` desk on the author's "do the design
memo for the code graph", answering the Softanza Compass's tensions T1 and T5. **It proposes and rules nothing**: its
recommendations are R1 to R12, and the four decisions that are the author's are Q1 to Q4 (section 8). It changes no compiler:
the only code it adds is the study under `haro/study/codegraph/`, which is the first measurement of the court it recommends.

**How to read it.** Every claim is **[M] measured** (a number, with the file that produced it), **[R] recorded** (a source in the
estate, read at the file) or **[D] designed** (this memo's proposal, reversible by name). A number without a source is a defect.
Where the Compass page described an estate asset and I could read the asset, I read it, and say so; where a claim could not be
checked, it is marked.

---

## 1. The question, and the position

The author's bar asks that the computing altitude not be *a text the compiler reads* but *a graph the compiler compiles*, with
every syntax a *face* over it, so that an agent fluent in Ring, Python or JavaScript writes Haro, and a refinement is a graph
transformation rather than a text patch. The Compass named the design and recommended: one semantics, many spellings; a round trip
judged at every face; **one court first, on the one face that exists, then faces** (T1, T5).

**The position of this memo, in one sentence.** Haro's computing altitude should compile a *program graph*; the Ring++ text is its
first face, a parser into the graph and a printer out of it, judged by a round trip; other faces arrive as printers before they
arrive as parsers, and never as semantics; and the graph is a **derived, content-addressed artifact of the face text** until a
measurement says the text should become the derived thing (section 3.7).

**What this memo adds to the Compass's design**, in order of how much it changes it:

1. **The round trip is measurable today, and it holds.** 429 of 429 Ring files in four corpora go text, tree, canonical text, tree
   and come back the same tree, with a printer that has no access to the author's layout (section 4.1). The risky half of T5 -- can
   a face's printer be a right inverse of its parser -- is not risky on the Ring++ face at the token level.
2. **The loss to name is not comments.** Layout is 5 to 10 percent of a file's bytes and a pure loss. Comments are 26.8 percent of
   the Softanza library's bytes and carry 8,306 `#-->` promises: a graph that drops them as trivia drops the estate's guards.
   Comments are nodes (section 3.3).
3. **Identity is the hard requirement and it is nearly free.** A name-and-hash matcher keeps 98.1 percent of statements across 56
   real edits. The graph model Refine already specified requires stable ids; the matcher is how a text-edited face gets them
   (section 4.4).
4. **The stzCodeGraph the Compass cites is an index, not the graph.** Its shared line protocol (`CLASS|METHOD|FUNC|IMPORT|CALL`)
   cannot print a program, and its Ring peer reads Ring with a name-based text parser. It is a *projection* of the graph this memo
   designs, not a candidate for it (section 2).
5. **A second face is a collision list before it is a syntax.** Ring's own findings make a Python-shaped face dangerous in
   fourteen specific ways (section 5). "A Python-shaped face of Haro is not Python" is a rule the court must be able to enforce.

---

## 2. What the estate already has, read at the files

| asset | what it is | what it lacks for this purpose | source |
|---|---|---|---|
| **`rnxc` and the Ring grammar** | text, then a tree-sitter parse, then `compile.zig`, then bytecode; compiled images and the library prefix are keyed by source hashes. The grammar names **59 kinds of node** (of 177 including tokens); newlines and `;` are *extras* (whitespace), and an external scanner decides what a space means before `(` and `[` | the compiler reads the tree directly; there is no stored graph and no printer | [R] ringpp `CLAUDE.md`; [M] `vendor/tree-sitter-ring/src/node-types.json`, `grammar.js` |
| **`rnxc dump`** | prints the parse, one node a line | **lossy in four ways** (this study): a leaf's text stops at 40 bytes, a newline in a leaf shows as a backslash, interior nodes carry no position, and three kinds of token are not nodes at all -- the `(` that opens a parameter list, the `[` that opens a subscript, and the content of a string the grammar splits | [M] `haro/study/codegraph/cst.py` |
| **`stzCodeGraph`** (stzlib) | "the code graph, polyglot by essence": a model, an ingestion of a **line protocol** (`CLASS`, `METHOD`, `FUNC`, `IMPORT`, `CALL`) and every query -- ancestry, descendants, impact, cascade, callers, callees, `DeadCode`, `CyclicCalls`. Python and JavaScript peers parse with the engine's vendored tree-sitter grammars; **the Ring peer parses with a text parser and builds a name-based call graph, strings and comments stripped first** | it is an **index of declarations and calls**: it holds no statement, no expression, no comment and no order, so nothing can be printed from it. Its Ring peer is not the real parse | [R] `base/meta/stzCodeGraph.ring`, `stzRingCodeGraph.ring`, read |
| **Refine's RCP system graph** | a typed, attributed property graph spanning "projects, modules, files, functions, and the syntactic structure inside functions"; node types include `Statement`, `Expression`, `Type`, `Binding`, `Library`, `Comment` (a textual annotation attached to another node); **stable node identifiers that survive transformation**; content-addressable states; **twelve primitive operations**; canonical serialization = a snapshot plus an append-only log of transformation events | its structural node types have **no Class, Method or Attribute** (a class could only be a `Type` or a `Module`: a gap to settle with Refine, section 7); it specifies the graph, not the parser or printer that feed it | [R] `refine/specs/RCP_GRAPH_MODEL_SPECIFICATION_v2_0.md` 1.1-1.5, 6.1, 9.1, read |
| **The levels document** (`stz/declarative/IR.md`) | the intermediate levels of a *declared* language, each with what it may lose, the court that judges it and **the correctness class of the step into it**; five classes: exact; exact except a named loss; near, tolerance written; over-approximation, extra named; equivalent in effect, comparison named | it covers the declared altitude. The *structure* level there may lose comments and layout; **it has no row for the computing altitude** | [R] `stz/declarative/IR.md`, read |
| **The charter and principle 10** | every named thing is a refinement point; a declaration is its own point; the `<R:KIND ...>` comment tag is "the lift for foreign code"; the agent proposes a refinement and never edits text | at the computing altitude a point needs an identity that survives an edit: nothing gives it one | [R] CHARTER section 6; PRINCIPLES 10 |

So the estate has the *theory* of the graph (RCP), the *index* of it (stzCodeGraph), the *parser* of Ring (tree-sitter-ring in
`rnxc`) and the *vocabulary of losses* (IR.md). It does not have the **program graph** itself, the **printer**, or an **identity**
mechanism. Those are what this memo designs.

---

## 3. The design

### 3.1 Levels

The Compass's phrase "the graph is what gets compiled" is one level among four. They are the levels document's idea, extended to the
computing altitude:

| # | level | what it is | may lose | judged by | class of the step into it |
|---|---|---|---|---|---|
| **L0** | **concrete tree** | the tree-sitter parse with every token, every comment, every hidden token and every gap of layout, in order | nothing | `print(L0)` equals the file, byte for byte | **exact** |
| **L1** | **program graph** | names, literals, operators and structure; statements, expressions, types, parameters; **comments as typed trivia attached to a node**; a stable id per node; no punctuation and no layout | layout; the choice among equivalent spellings; punctuation that structure determines | the **round-trip court** (section 3.6) | **exact except a named loss** (layout) |
| **L2** | **resolved graph** | L1 plus edges: calls, references, inherits, scope, `depends_on` -- RCP's structural edge types | nothing L1 had | agreement with what the compiler resolves (Rule A, `rnxc check`) | **exact**, and **over-approximation, extra named** where a call cannot be resolved |
| **L3** | **bytecode image** | what `rnxc` already compiles and caches | everything but behaviour | the A/B against the oracle (the existing clock and gate) | **equivalent in effect, comparison named** |

Two things follow. **L0 is lossless and is what a same-face edit round-trips through**; **L1 is what faces share**, so L0 is
per-face and L1 is not. And the *stzCodeGraph line protocol is a projection of L2* (`CLASS`, `METHOD`, `FUNC`, `IMPORT`, `CALL` are
the declaration and call nodes and edges, flattened): the index stays, and is fed by the real parse rather than a name-based one.

### 3.2 What a face is

A **face** is a *parser* (text to L1), a *printer* (L1 to text), a *spelling table* (one obvious spelling per construct: principle
2) and a *collision list* (what the face may not spell because its reading would change the meaning: section 5), judged by the
round-trip court. Three rules:

1. **One semantics.** A face spells the graph; it never gives it Python's or JavaScript's meaning. Ring++'s meaning is the graph's.
2. **A printer refuses before it approximates.** A construct a face cannot spell without a reader taking it for something else is
   refused by name at print time, never printed near.
3. **The printer is the formatter.** The canonical text of a face is the one spelling; `fmt` is the printer. Principle 2 gets a
   mechanism instead of a convention.

### 3.3 Comments are nodes

The Compass's rule -- name the loss, and the loss is layout and comments -- is **half wrong for the computing altitude**. In the
declared altitude's structure level (IR.md) comments are lost harmlessly, because a declaration's meaning is its clauses. In Ring a
comment is where the estate keeps meaning:

| tree | files | lines | comment lines | comment bytes | `#-->` promises | `<R:` tags |
|---|---|---|---|---|---|---|
| Softanza `base` | 5,728 | 917,948 | 158,628 (17.3%) | **26.8% of bytes** | **8,306 lines in 2,969 files** | 7 |
| Softanza `core` | 36 | 9,903 | 1,472 (14.9%) | 24.1% | 427 in 11 files | 0 |
| ringpp `bench`+`tests` | 155 | 6,146 | 1,048 (17.1%) | 36.5% | 0 | 0 |

[M, `census_comments.py`, 2026-10-04.] A narrated guard's `#-->` is a *promise the run checks*; a `<R:` tag is a refinement point the
gate reads; the intent clause of a method is the principle-5 channel. **A graph that dropped comments would drop the estate's
claims.** So: a comment is a node of a **kind** (`promise`, `tag`, `intent`, `note`), attached to the node it describes by a fixed
rule (a comment on its own lines attaches to the next statement or definition; a trailing comment to the statement on its line),
printed by every face, and refinable like anything else (Refine's own graph model already makes `Comment` a structural node type
[R, RCP 1.2]). The only loss a face may name is **layout**, which the measurement prices
at 5 to 10 percent of the bytes (section 4.3).

### 3.4 Identity

The RCP model requires that a node keep its identifier when a transformation changes its properties. A face is edited as text, so
identity must be *recovered when the edited text is parsed again*. The matcher recommended is the cheapest there is: a function
by its qualified name, a statement by the hash of its tokens, statements within a matched function aligned by longest common
subsequence, comments by their attachment. Measured over real history it keeps 98.1 percent of statements (section 4.4); the
remainder -- edited statements, renamed functions -- is where a tree matcher (a GumTree-class algorithm) or an identifier written
into the text would carry the load. **The agent never edits text** (charter 6.6): its refinement is a graph transformation
against ids taken from the *current* parse, applied to L1 and printed as a text diff, which is the derived view the charter already
wants. Identity matters most for the human's edit, and that is the case the measurement covers.

### 3.5 Dynamic code is a hole the graph names

The estate's Ring has code in strings: `eval` (136 sites in 44 files [R, ringpp `CLAUDE.md`]), `addmethod`, `addattribute`,
`call "name"()`. A graph of the text cannot see inside them. **A node whose behaviour is determined by a string is marked
`dynamic`; a refinement cannot target inside it; the court says so.** The declared altitude has no such holes (it is total, principle
11), which is exactly why the two altitudes keep different graphs' promises.

### 3.6 The court

The **round-trip court** of a face has three parts, each with a class:

1. **Same face, text to L0 to text: exact**, byte for byte (trivial by construction; kept as a guard against a lossy parser).
2. **Same face, text to L1 to canonical text to L1: exact except layout** -- the measurement of section 4.1, at the token level.
3. **Across faces, L1 to face A to L1, and L1 to face B to L1: exact**, and the *meaning-collision fixtures* of section 5: for each
   collision, a program whose two spellings must be refused or must keep one meaning.

Fixtures first, as every rung: a corpus with pinned floors, the two controls that must fail (a printer that spaces every `(` and `[`,
a printer that drops comments), and a hand-composed set -- one program per Ring trap in section 5 -- written *before* the L1 printer.

### 3.7 Where the text lives: the fork

| | **A. text is primary** | **B. the graph is primary** | **C. text primary, ids in a sidecar** |
|---|---|---|---|
| what is stored | the face text in git; the graph derived and cached by content hash, like the compiled image | the graph and an event log (RCP 9.1); the text derived | the text, plus a committed id map |
| identity | recovered by the matcher on every parse (98.1% free) | exact, always | exact where the sidecar is current |
| cost | none: git, editors and the existing estate keep working | a new store, no text diff or merge, every tool rewritten | two files to keep in step; a stale sidecar is a silent defect |
| fits | the oracle, the clock, 5,728 files of Softanza as they are | refinement as the only way to change code | a middle that tends to become B |

**Recommended: A**, with a stated threshold for leaving it: if, on Haro's own programs, **fewer than 95 percent of refinement
targets still resolve after a human edit**, move to C. The measurement that would decide is a stage-4 court over the real history of
Haro's files (the baseline is section 4.4). B is the end state only if refinement becomes the *only* write path, which the charter
asks of the agent and not of the human.

**Measured by rung 2 (2026-10-04, `haro/spike/v19/IDENTITY.md`): 98.3 percent of the statements a refinement could have targeted still
resolve after the next human edit on Haro's own history (38 pairs, 28,996 statements) and 99.1 percent on the memo's seven files. The
95 percent threshold holds, K2 does not fire, and A stands.** Most of it is a name, a hash and the same text anywhere in the same
function: name and text alone keep 86.0 percent, the function pool takes it to 95.6, similarity to 98.3. Per edit, not per lineage.

---

## 4. What was measured

All of it from `haro/study/codegraph/`, on this machine, 2026-10-04, reproducible with the scripts named. Nothing here touches the
estate's trees except to read them.

### 4.1 The round trip, text to tree to canonical text to tree (`corpus.py`)

`cst.py` recovers a lossless concrete tree from `rnxc dump` and the source; `printer.py` prints it with **no knowledge of the
original layout** -- one space between tokens, a call's `(` and a subscript's `[` glued, brackets and commas and the member dot
glued, each statement on its own line, comments kept; `round.py` parses the printed text again and compares the two trees node for
node and token for token.

| corpus | files | same | differ | not measured |
|---|---|---|---|---|
| Haro spike (`haro/spike/*.ring`) | 26 | 26 | 0 | 0 |
| Ring's standard library (`vendor/ring-stdlib`) | 99 | 99 | 0 | 0 |
| Ring++ probes and benchmarks (`bench`, `tests`) | 155 | 154 | 0 | 1 |
| Softanza `base`, every 38th file up to 400 KB | 150 | 150 | 0 | 0 |
| **all** | **430** | **429 of 429 measured (100%)** | **0** | **1** |

The one file not measured is `bench/reports_2021_comments.ring`, a probe of Ring's *non-nesting block comments* that the parser is
right to refuse. 1,269 KB were measured, 656 s. **The controls can fail**: a printer that puts a space before every `(` and `[`
changes 8 of 8 files; a printer that drops comments changes 8 of 8. The round trip is therefore not an artefact of a lenient
comparison.

**What it shows:** a layout-free printer is a right inverse of the Ring++ parser at the token level, on 429 files from four
different authors. **What it does not show:** the *abstraction* step. L1 drops the punctuation that structure determines and prints
it back from a template per kind of node; that is 59 templates, not measured here. 4.5 says what is owed.

### 4.2 What the dump hides (`cst.py`)

Every gap between two recovered tokens is layout, a `;`, or one of exactly **three** hidden things: the `(` that opens a parameter
list (64 in `n_lib.ring`), the `[` that opens a subscript (605, equal to its 605 `subscript_expression` nodes), and the content of
a string the grammar parses into parts. Nothing else is hidden. That is the whole list of what `rnxc dump` would have to add -- node
positions, full leaf text, and those three -- to be a lossless export, which is the ringpp request in section 7.

### 4.3 What layout costs, and what the graph weighs (`layout.py`)

| sample | files | bytes | canonical | layout | tokens/KB | nodes/KB | comments, share of the canonical text |
|---|---|---|---|---|---|---|---|
| Haro spike | 20 | 401 KB | 380 KB | **5.3%** | 204 | 304 | 19.3% |
| Ring stdlib shims | 20 | 5 KB | 4 KB | 9.6% | 134 | 220 | 15.9% |
| Softanza `base` | 31 | 105 KB | 98 KB | **6.6%** | 134 | 204 | 38.8% |

Layout, the one thing a face may lose, is 5 to 10 percent of the bytes. The graph is **about 200 to 300 nodes per KB of source**.
At that ratio Softanza's 26.8 MB `base` tree would be about 5 million nodes [D: an estimate from the sample's ratio, not a count].
That is why the graph is per-file and cached like the compiled image, not resident (section 6).

### 4.4 Identity across real edits (`identity.py`)

Seven files, up to twelve consecutive revisions each (four of them this repository's own Ring, three of stzlib's, read with `git show`,
read-only), 56 old-against-new pairs, **49,933 old statements** counted at every depth. A function is matched by qualified name, a
statement by the hash of its tokens, statements in a matched function by longest common subsequence.

| | share |
|---|---|
| **kept** (an identical statement in the matched function) | **98.1%** |
| changed in place (edited or deleted) | 1.8% |
| lost with their function (renamed, moved or deleted) | 0.1% |

51 of the 56 edits keep 95 percent or more; the weakest file is `stzCodeGraph.ring` (86.3% kept) because one revision rewrote a
large part of it. **Caveats:** the edits are commits, not keystrokes; a statement's hash covers its whole subtree, so an edit inside an
`if` counts the `if` as changed and keeps the statements around it; a rename of a function is a loss by construction. The number is
the *floor of what a name-and-hash matcher gives for free*.

### 4.5 What is not measured, and is owed

1. **The abstraction step** (L0 to L1 to text): 59 printing templates and the comment-attachment rule. The recommended first rung
   measures it on the same corpus, with floors. **Measured by rung 1 (2026-10-04, `haro/spike/v18/GRAMMAR.md`):** 49 graph kinds
   fold the grammar's node kinds; the abstraction is not a function of the tree alone, because the tree is wrong about structure
   in nine ways Ring's own flow corrects (HF-73); the printer writes no `end`; the round trip holds on all of Softanza's 6,068
   Ring files (5,958 exact in graph and compiled code, 52 as graphs only, 58 refused by Ring itself), judged by `rnxc dis`.
2. **Resolution** (L2): how many call edges `rnxc` resolves that stzRingCodeGraph's name-based parse does not, and the reverse.
3. **Graph build cost** against the 3.38 seconds `rnxc` spends in tree-sitter on the 613-file load unit [R, ringpp `CLAUDE.md`].
4. **Whether a second face helps a model.** The hypothesis -- "an agent skilled in any of these languages writes Haro" -- has no
   measurement. It needs a protocol of the kind that decided the `stz` verbs (twenty tasks, per the Compass page: [R via the Compass], not
   re-read here): a model writes the same tasks in a Ring-shaped and a Python-shaped face under the face's GBNF, and the court judges
   (K4 in section 6).

---

## 5. The faces: what a second spelling must refuse

The grammar has 59 kinds of node. Spelling them in another syntax is mostly notation. It is dangerous in exactly the places where
Ring's meaning differs from what a reader of Python or JavaScript expects from the same shape. Ranked by how much code uses them:

Counted over the 429 files of 4.1 that parse (`kinds.py`): **193,994 named nodes of 53 of the grammar's 59 kinds**. Six kinds never
occur in these files -- `brace_block`, `give_statement`, `import_statement`, `interpolation`, `new_with_parens`, `package_definition`.

| kind | nodes | share | what a second face does with it |
|---|---|---|---|
| `identifier` | 51,910 | 26.8% | case-folded: `N` and `n` are one variable (F-18) |
| `expression_statement`, `assignment_expression` | 16,417 | 8.5% | spelling |
| `call_expression` | 16,415 | 8.5% | spelling |
| `number` | 15,705 | 8.1% | doubles past 2^53 (F-75) |
| `binary_expression` | 15,036 | 7.8% | `=` compares, and a numeric string equals its number (C-8) |
| `string` | 13,441 | 6.9% | no escapes (F-55): every literal printed raw |
| `arguments` | 12,391 | 6.4% | spelling |
| `member_expression` | 6,191 | 3.2% | a getter runs on every dot but `This`'s (F-73) |
| `comment` | 5,235 | 2.7% | typed nodes (3.3) |
| `subscript_expression` | 5,218 | 2.7% | **1-based**; a one-character string on a string (C-3) |
| `self` | 4,918 | 2.5% | spelling (`This`) |
| `if_statement` | 3,989 | 2.1% | spelling; the `:` is a range (F-65) |
| `function_definition` | 3,894 | 2.0% | **order is semantic** (F-21) |
| `for_statement` | 935 | 0.5% | 889 `for i = a to b`, 46 `for x in list` (by reference), 10 with `step` |
| `new_expression` | 357 | 0.2% | spelling |
| `try_statement` | 136 | 0.1% | the caught message is process-wide (C-15) |
| `class_definition` | 82 | 0.0% | a `private` section runs to the end of the file |
| `brace_expression` | 38 | 0.0% | no spelling: hooks and method-first calls |
| `anonymous_function` | 18 | 0.0% | spelling |
| `eval(...)` calls | 11 | -- | a graph hole (3.5) |

The constructs that need the most care are the **common** ones: strings, numbers, identifiers and subscripts are 44 percent of the
nodes. The exotic ones (brace blocks, `eval`, getters) are rare and are also the ones with no spelling at all.

Each collision below is a Ring finding already paid for (`docs/FINDINGS.md`, `docs/CORRECTIONS.md`); a Python-shaped face that prints
the shape without the warning would be read wrongly by every Python reader and by every model.

| construct | Ring++ means | a Python reader expects | verdict |
|---|---|---|---|
| `a[i]` | **1-based**; on a string, a one-character *string* (C-3, F-54) | 0-based | **collision**: no spelling until one exists that cannot be misread |
| `"\n"` | a backslash and an `n`: **Ring has no string escapes** (F-55) | a newline | **collision**: the face prints every literal raw |
| `N` and `n` | **one variable** (F-18) | two | **collision**: the face is case-folding too |
| `1 = "1"` | true: a numeric string equals its number (C-8) | false | **collision** |
| numbers past 2^53 | doubles (F-75) | exact big integers | **collision** (value) |
| `for i = a to b step s` | inclusive bound; after the loop `i` is the value that failed the test | `range(a, b, s)` exclusive; last value | header: spelling; **post-loop value: collision** |
| `for x in list` | binds by reference | by value | **collision** |
| `o.x` with `getx()` defined | **calls `getx()`** on every dot but `This`'s (F-73) | an attribute read | **collision** |
| `obj { ... }` | a brace block with `braceStart`/`braceEnd` hooks; a bare call is the object's method first | nothing | **no spelling** |
| `operator(cOp, x)` | one method for every operator, the right side with an "r" (F-69) | `__add__` and friends | **collision** of shape |
| `try ... catch ... done`, `cCatchError` | the caught message is **process-wide** outside the handler (C-15) | an exception object | **collision** |
| `eval(s)` | runs in the **caller's scope** and creates its variables there (F-72) | its own scope | **collision**; and a graph hole (3.5) |
| function and class order | every `func` after the first `class` **becomes a method** (F-21) | order is free | **layout is semantic**: the printer must order free functions first |
| `if c: s ok` | the `:` is a **range** (F-65) | a block opener | the face never prints `:` as one |

**What it costs the claim.** "Any model writes Haro in the shape it knows" is true only of the *spellings in the left-hand
column's right-hand cell*, which are the minority: the table is the face's banner, and it must travel with the face. The honest
promise of a second face is *readability for a human who knows the other language*, not behavioural transfer.

---

## 6. Costs, risks, and what would make this wrong

**Costs** [M or D as marked]: a printer (the token-level one is 76 lines; the 59-template L1 one is the work); a matcher (the
measured one is a name table and a longest-common-subsequence); a court in the guard (the full corpus is 656 s, so the guard gets a
sample of about forty files at about twenty seconds, and the full run is a monthly measurement); memory, at about 200 to 300 nodes
a KB [D], so the graph is **per file and cached by hash**, never the whole library resident.

**Risks.**

1. *The abstraction step is unmeasured* (4.5.1). Mitigation: it is the first rung, and the token-level printer is the fallback.
2. *Comment attachment is ambiguous* where a comment sits between two statements, or inside an expression. A fixed rule plus
   fixtures; the round trip is judged on where the comment prints.
3. *Identity under refactor*: a moved or renamed function loses its statements' ids (0.1% here). A rename is a graph operation
   and carries the id; a rename done by hand in text does not.
4. *Two sources of truth.* Avoided by A: the text is the source, the graph is a cache with a hash.
5. *The compiler reads the tree directly* (4,800 lines of `compile.zig`). **Do not route the compiler through L1** until L1 round
   trips: L1 is first a *sidecar* emitted from the same parse, and the compiler is untouched.
6. *The graph is blind to dynamic code* (3.5). Named, not solved.

**What would make this wrong.** Four kill criteria, each measurable:

- **K1** the L1 printer cannot reach 99 percent of the corpus (then faces are token-level only and the graph is an index);
- **K2** fewer than 90 percent of statements keep identity on *Haro's* history (then ids must live in the text: option C);
- **K3** the collision fixtures outnumber the spellings (then a second face is a reading aid and is not built as a parser);
- **K4** a model does no better writing a Python-shaped face than a Ring-shaped one under its GBNF (then faces are not worth their
  court, and the graph is justified only by refinement and the formatter).

---

## 7. The plan: rungs, owners, guards

Each rung is fixtures first, prose second, and has a guard before it is called built.

| rung | what | owner | guard |
|---|---|---|---|
| **0, done here** | the round trip at the token level, the comment census, the layout and identity measurements, the kinds table | haro-charter | `haro/study/codegraph/*.py`; `results.json`, `identity.json`, `layout.json`, `census_comments.json` |
| **1 -- the structure level of the computing altitude (Haro v0.18) -- BUILT 2026-10-04** | the L1 schema (RCP's node types, with Class, Method and Attribute settled with Refine); the 59 printing templates; comment attachment; hand-composed fixtures, one per trap in section 5, written first; the court in the guard (a sample of ~40 files, floors pinned, the two controls failing) | haro-charter, with stz for the IR.md row | guard stage 22 |
| **2 -- identity -- BUILT 2026-10-04 (Haro v0.19)** | node ids; the name-and-hash matcher; a stage that replays real history and pins the retention (baseline 98.1%) and the K2 threshold | haro-charter | guard stage 23 |
| **3 -- `rnxc fmt` and the lossless export** | `rnxc dump --json` (every node with its byte span; the three hidden tokens; full leaf text), then the printer as `fmt` | **ringpp** (outside `haro/`, as D14 for the forge) | the court's corpus run on the real binary |
| **4 -- L2 and the projection** | the resolved graph from `rnxc`; the line protocol as its projection; stzRingCodeGraph answers compared and every difference named | ringpp, stzlib | agreement table, differences listed |
| **5 -- refinement over L1** | a refinement as a sequence of RCP's twelve operations; the gate runs on L1; the diff is the printer's | haro-charter, Refine | the principle-10 fixture, at the computing altitude |
| **6 -- a second face, as a printer** | Python-shaped, one-way, with every collision refused by name; read by a human and a model (K4) | haro-charter | the 20-task protocol |
| **7 -- a second face as a parser** | only if rung 6 and K3 allow | -- | the round trip across faces |

**Asks of other desks:** *ringpp* -- the lossless export (rung 3); *Refine* -- RCP's structural node types name no Class, Method or
Attribute; *stz* -- a row for the computing altitude in `IR.md`, with L1's loss named; *stzlib* -- stzRingCodeGraph's Ring peer
becomes a projection of rung 4. **Interplay with T2** (COMPASS-HARO-01): if every verb moves to one `stz` executable, `fmt` and the
graph export are `stz` subcommands, and the faces are named by file extension.

---

## 8. Decisions that are the author's

- **Q1 -- where the text lives.** *Recommendation: A* (text primary, graph a cache by hash), with the K2 threshold written down.
- **Q2 -- how many faces before the announcement.** *Recommendation: one* (Ring++) *plus printers* for Python and JavaScript, read
  by humans, until a customer needs a parser. Faces are a readability feature before they are a compatibility one.
- **Q3 -- who builds what.** *Recommendation:* the haro-charter desk writes the L1 schema, the court and the matcher in the spike
  (rungs 1, 2, 5); ringpp builds the export and `fmt` (rung 3); stz and Refine carry their rows; the Compass keeps the page.
- **Q4 -- whether `fmt` ships before Haro.** The canonical printer is a Ring++ feature as much as a Haro one: one obvious spelling
  for the 5,728 files of Softanza, with a court that proves the formatter changes no meaning. *Recommendation:* ringpp's call; it is
  the cheapest visible product of this memo.

---

## 9. What is not claimed

- That L1 round-trips: only L0 and the token-level printer are measured.
- That the graph can replace the text, or should: R1 keeps the text.
- That a second face is feasible or valuable: section 5 lists what it must refuse, and K4 has no measurement.
- That 98.1 percent identity holds on Haro programs: it is the measured baseline on seven files, four of them this repository's own.
- The graph's build cost and memory: estimated, not measured.
- That `eval` and the reflection family can be graphed: they are marked as holes.

---

## Recommendations

**R1** the graph is derived from the face text and cached by content hash; the text is primary until K2 fires. **R2** four levels, L0
to L3; the compiler is untouched until L1 round-trips. **R3** comments are typed nodes; the only named loss is layout. **R4** a face is a
parser, a printer, a spelling table and a collision list under a round-trip court. **R5** a printer refuses before it approximates.
**R6** the printer is the formatter. **R7** identity is a qualified name plus a token hash, matched by longest common subsequence, with
a floor pinned at the measured baseline. **R8** dynamic code is marked, and cannot be targeted. **R9** stzCodeGraph's line protocol is a
projection of L2, fed by the real parse. **R10** `rnxc dump --json` is the first ringpp item. **R11** the first Haro rung is the structure
level of the computing altitude, in the guard. **R12** no second face as a parser before the printer, the collision fixtures and K4.

## Files

    haro/CODEGRAPH.md                            this memo
    haro/study/codegraph/cst.py                  a lossless concrete tree recovered from `rnxc dump` and the source
    haro/study/codegraph/printer.py              the canonical printer for the Ring face (no layout in, none out)
    haro/study/codegraph/round.py                one file: text, tree, canonical text, tree, compared
    haro/study/codegraph/corpus.py               four corpora, two controls that must fail; results.json
    haro/study/codegraph/census_comments.py      what lives in comments; census_comments.json
    haro/study/codegraph/layout.py               bytes, tokens, nodes per KB; layout.json
    haro/study/codegraph/identity.py             identity across real edits; identity.json
    haro/study/codegraph/kinds.py                the 59 kinds ranked by use; kinds.json
    haro/spike/v18/GRAMMAR.md                    rung 1: the schema, Ring's flow, the canonical text, the court, the numbers
    haro/spike/v18/l1.py, l1_check.py            rung 1: the graph, the abstraction, the printer; the court (guard stage 22)
    haro/spike/v18/fixtures.txt                  rung 1: 22 hand-composed programs, graph and canonical text
    haro/spike/v19/IDENTITY.md                   rung 2: what has an id, the matcher, the court, the numbers
    haro/spike/v19/ids.py, ids_check.py          rung 2: ids and the matcher; the court (guard stage 23)
    haro/spike/v19/fixtures.txt                  rung 2: 23 hand-composed edits and the ids each must leave
