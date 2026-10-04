# The program graph of Ring, built -- the structure level of the computing altitude (Haro v0.18, the eighteenth rung)

**Rung 1 of the code-graph memo** (`haro/CODEGRAPH.md`, section 7), built on the author's "start rung 1 of the code graph
memo". **Written after** the fixtures in `fixtures.txt` (22 programs, composed by hand before `l1.py` existed -- the W
discipline: fixtures first, prose second) and after the measurements of `probes/` that overturned several of this rung's
own first assumptions (section 3). `l1.py` is the reference implementation of this file; `rnxc` is the second reader of Ring, and the
court below judges both.

**What this is, in one line.** A Ring program as a graph -- names, literals, operators, structure, comments as nodes, no
punctuation, no layout -- with a printer that writes the one canonical text of a graph, so that *text -> graph -> text ->
graph* is the same graph, the second text is the first, and the compiled code of the original and of the canonical text
is the same code. The Ring++ face of Haro is a parser, this graph and this printer; the rest of the altitude is built on
them (CODEGRAPH sections 3 to 6).

## 0. What exists, and what does not

| | status | where |
|---|---|---|
| the graph: 49 kinds, `(kind :field value ...)` s-expressions | **built** | `l1.py` (`FIELDS`), section 2 |
| the abstraction, text to graph, from `rnxc dump`'s tree repaired by Ring's own rules | **built** | `l1.py` (`Abstract`, `finish`), section 3 |
| the canonical printer, graph to text | **built** | `l1.py` (`Printer`), section 4 |
| the court: 22 fixtures, 2 controls that must fail, a corpus | **built**, `python haro/spike/v18/l1_check.py`, guard stage 22 | `l1_check.py` |
| **the whole of Softanza through the court** | **measured**: 6,068 Ring files, none failing (section 6) | `probes/stress.py` |
| names resolved, edges (L2); the bytecode as a level (L3) | **not built.** Rungs 2 and 3 of the memo | -- |
| the text-primary / graph-as-cache store and its identity matcher (CODEGRAPH 6) | **not built.** Rung 4 | -- |
| a printer that wraps long lines | **not built**; the canonical text never wraps (section 4) | -- |

## 1. What is kept and what is dropped

**Kept, exactly as written:** every identifier (`N` and `n` stay two spellings, F-18), every number and every string as its raw
text (Ring has no escapes, F-55), every comment, every parenthesis the author wrote (a `paren` node), the order of everything.

**Dropped, because nothing reads it:** layout (blank lines, indentation, the column of anything), the `;` and `,` between
statements, a call statement's trailing period, the alternative spellings of one construct *where rnxc was measured to read the
two alike* (`func`/`def`/`function`; `ok`/`end`/`endif`; `but`/`elseif`; `else`/`other`; `?`...; `give`/`get`; `exit`/`break`;
`loop`/`continue`; `for`/`foreach`; `next`/`endfor`/`end`; `on`/`case`; `done`/`endtry`/`end`; `not`/`!`; `This`/`self`/`this`;
keyword case), and the byte-order mark.

**Not dropped, because the compiler does not read them alike** (42 of 45 alternative spellings did; these are the other
cases, `probes/synonyms.py`): `&&` and `||` keep their spelling (rnxc traps on them; `and`/`or` compile), and `see`, `put` and
`?` are two kinds, not one (section 3, rule 7).

## 2. The schema

A node is a dict `{'k': kind, field: value, ...}`; a field at its default is absent (`norm`), so two graphs are equal when
their dicts are equal. A statement or a definition carries one more optional field, `trail`: the comment that ended its line.

| kind | fields | tree-sitter node(s) | canonical text |
|---|---|---|---|
| `file` | `items` | `source_file` | -- |
| `package` | `name items` | `package_definition` | `package A.B` then its items one level in |
| `class` | `name parent items` | `class_definition`, `class_parent` | `class A from B` then its items one level in |
| `private` | -- | `private_section` | `private`, a marker among a class's items |
| `func` | `name params items` | `function_definition`, `param_list`, `typed_parameter` | `func name(a, int b)` -- always with parentheses |
| `expr` | `e` | `expression_statement` | the expression |
| `return` | `e amp` | `return_statement` | `return e` (`return & e` when `amp`) |
| `say` | `e` | `see_statement` led by `?` | `? e` |
| `see` | `e` | `see_statement` led by `see` or `put` | `see e` |
| `give` | `target` | `give_statement` | `give x` |
| `if` | `cond then elifs else` | `if_statement`, `elseif_clause`, `else_clause` | `if` / `but` / `else` / `ok` |
| `while` | `cond items` | `while_statement` | `while c` ... `end` |
| `for` | `var kind a b step items` | `for_statement` | `for i = a to b step s` / `for x in e` ... `next` |
| `dowhile` | `items cond` | `do_again_statement` | `do` ... `again c` |
| `switch` `case` | `subject cases other` / `values items` | `switch_statement` | `switch` / `on v1, v2` / `other` / `off` |
| `try` `catch` | `items catch finally` / `binding items` | `try_statement` | `try` / `catch(e)` / `finally` / `done` |
| `load` `import` | `mode path` / `name` | `load_statement`, `import_statement` | `load [package\|again] "p"`, `import A.B` |
| `exit` `loop` `bye` | `e` / `e` / -- | `exit_statement`, `loop_statement`, `bye_statement` | `exit [n]`, `loop [n]`, `bye` |
| `scanner` | `text` | `scanner_command` | the line as written |
| `comment` | `text` | `comment` | the comment as written, an item where it stands |
| `assign` `bin` `un` `post` | `op l r` / `op l r` / `op e` / `op e` | `assignment_expression`, `binary_expression`, `unary_expression`, `postfix_expression` | operators with their spelling, parentheses by precedence |
| `call` `callkw` `member` `index` | `callee args` / `e items` / `obj prop` / `obj idx` | `call_expression`, `call_keyword_expression`, `member_expression`, `subscript_expression` | `f(a)`, `call f(a)`, `o.p`, `o[i]` |
| `brace` `new` `lambda` | `obj items` / `from name args items` / `params items` | `brace_expression`, `new_expression`, `anonymous_function` | `o { ... }`, `new A(x)`, `func(a) { ... }` |
| `paren` `list` `pair` | `e` / `items` / `key value` | `parenthesized_expression`, `list_literal`, `hash_pair` | as written |
| `id` `num` `str` `sym` `self` `super` `bool` `null` | `text` ... | `identifier`, `number`, `string`, `symbol`, `self`, `super`, `boolean`, `null` | `NULL`, `This`, `true`, `false` canonical |

Of the grammar's 59 node kinds, 53 occur in the 193,994 named nodes of the Softanza base (CODEGRAPH, `study/codegraph/kinds.py`);
the 49 graph kinds fold the rest (an `arguments` node is a `call`'s `args`; `qualified_identifier` is a name list).

## 3. Ring's flow, and the nine rules that make the tree say it

**The tree of `tree-sitter-ring` is not what Ring does, and this rung's court found it nine ways.** Each rule is a measurement
of the oracle (`runtime/win64/ring.exe`), then of rnxc, then a repair that the court confirmed on the files that needed it.

1. **`end`, `endfunc` and `}` close nothing.** After a function, a statement written on the next line runs *as part of the
   function's flow*, up to the next definition -- with or without `end`, with braces or without (probe `probes/closers.py`,
   `fall.py`: 9 closers, 5 shapes, oracle and rnxc agree). So the graph has no statement after a definition, and **the printer
   never writes an `end` for a definition.** (The first version of fixture 20 had the printer close a definition "exactly when
   something that is not its own follows"; Ring has no such thing.)
2. **A function or a statement after a class is the class's** -- every `func` after the first `class` is a method of the latest
   (F-21). The parser nests a class inside the one before it and hands the methods that follow *to the outer class*; the graph
   puts the classes side by side, in source order, and gives each the methods that follow it (`probes/nest.ring`).
3. **A `return` that ends its line is bare, and what stands on a later row is a statement of its own that never runs.** Ring's own
   parser looks at the very next token after `return` and, finding the end of the line, returns NULL (`vendor/ring-vm/src/stmt.c:931`);
   measured on the oracle and the official 1.27, `return` then `6` answers the empty string. This grammar reads a newline as an extra,
   so it hangs the next row's expression on the `return` -- and in a class it does the opposite, cutting `return 7` into a bare
   `return` and a `7` side by side on ONE row. The graph says what Ring says: an expression on the same row is the return's value
   (its `=` compares), one on a later row is a dead statement after a bare return. **The first version of this rung joined them from
   any row, because rnxc did, and judged the choice by `rnxc dis` alone -- which can only say that two texts compile alike to rnxc.
   rnxc was wrong (HF-74; fixed 2026-10-04) and the oracle was never asked.**
4. **A line is read greedily, and a line that begins with `+` or `-` after a finished term is a statement of its own.** The parser
   cuts `return a + f(x) + b` at a `+` on the same row (the cut lands at a different `+` from one line to the next), cuts a
   call chain at a dot, and joins nothing across a trailing dot. The statement and every tail it was cut from are read again
   alone, inside a `func`, where the grammar keeps it whole; a payload that is still cut is parenthesised and read once more.
   This is a port of `compile.zig`'s `rereadSpan`, which found the same defects first.
5. **`private` is a keyword.** After a comment that follows a top-level statement and precedes a class, the parser reads
   `private` as an identifier and hangs everything after it on the last method (`probes/priv7.ring`); a bare `private` is the
   marker, and what follows it is the class's.
6. **A bare `end` or `endfunc` the parser read as a name is the inert closer of rule 1**, and is dropped.
7. **`?` prints a line; `see` and `put` print without one, in any case of letters** (measured on the oracle: `SEE "a"`, `put "b"`,
   `Put "c"`, `? "d"` print `abc` and `d` and a newline; Ring's parser has one branch for `see` and `put`, `stmt.c:382`, and another
   for `?`, `:392`). rnxc read the keyword case-sensitively and treated `put` as `?` (`compile.zig:5899`), so Ring's own library,
   which writes `See vValue`, printed a newline under rnxc. **Fixed 2026-10-04** (HF-74); the graph followed Ring all along.
8. **A brace belongs to the value.** `o = F(x) { ... }` gives `o` the value and runs the brace on it; the parser sometimes hangs
   the brace on the whole assignment. An assignment's value is what it assigned, so the two do the same; the graph keeps the
   first, which also prints as a statement of its own, where `(o = F(x)) { }` would join the call on the line above.
9. **Comments are not part of the tree's shape.** A comment after the last statement of a function the parser leaves open is the
   parser's, and belongs to what holds the function; a comment inside an expression has nowhere to stay in a layout-free text,
   so it becomes an item after its statement; a comment on the line where an item ends trails it (`trail`), pushed down to the
   last statement of a definition, whichever node the parser hung it on; the comments between two classes the parser nested
   stay between them. **Nothing a comment says is lost** (the control that drops them fails the round trip).

## 4. The canonical text

One text per graph. Tab indentation. A blank line before each definition (a `func`, `class` or `package` and the comments
directly above it) and before the item after a definition. A block statement closes with its keyword (`ok`, `end`, `next`,
`off`, `done`, `again c`); a definition closes with nothing. A function is always `func name(params)`. A switch's clauses are
one level in and their bodies two. A brace body prints on its own lines. Parentheses are the author's (`paren`) or the
precedence's (a left-associative operator needs them on its right side; a lower-precedence operand on either).

**Spelling, chosen by the corpus** (`study/codegraph/spellings.py`, 309 files of Softanza): `func` 1,342 against `def` 74;
`ok` 2,166 for every `if`; `but` 245; `while ... end`; `for ... next`; `?` 980 against `see` 172; `NULL` 418 against `null` 2;
`and` 318 / `or` 305 against `&&` / `||` (kept as written, rule above); `This` 9 against `self` 5. 840 of 13,460 keyword
occurrences differ from the lower-case spelling; the graph drops the case.

**The hazards a printer must keep** (the collision table):

| hazard | what Ring does | what the printer does |
|---|---|---|
| a bare expression statement that begins with `-` or `+` | joins the line above as a subtraction (Ring reads across lines) | never prints one after another expression statement: refinements build assignments and calls; a bare `-x` statement is a statement of its own only after a finished term at a line end |
| a statement that begins with `(` after a call statement | the scanner joins it to the call above | the brace-on-assignment rule above avoids the one case the corpus has |
| a `return` followed by an expression on the next line | the expression is the value | the value is printed on the return's line |
| a comment inside an expression | scanner drops it wherever a newline may stand | hoisted after the statement |
| a definition followed by a statement | the statement runs in the definition's flow | never printed: the graph has none |
| the length of a line | no limit | the printer does not wrap (a wrapped literal is a refinement's, rung 5) |

## 5. The court

`python haro/spike/v18/l1_check.py [--plant] [--quick]` (exit 1 on any failure); guard stage 22; ten seconds.

**F -- 22 fixtures**, `fixtures.txt`, each: a Ring program, the graph it must abstract to, the canonical text. Five checks on each:
the abstraction equals the hand-written graph; the printer, given the *hand-written* graph, prints the fixture's text; the
printed text parses back to the same graph; printing again gives the same text; and original and canonical text **compile to
the same code** (`rnxc dis`) -- or, where rnxc does not read Ring (`see`, `put`, a method whose `return` the parser split),
print the same output on the oracle. Two are printer-only (`--- ring` absent): a graph a refinement would build.
**Seven fixtures were changed after the court ran, and each says so in its note** (02, 11, 12, 17, 19, 20, 22): the court taught the
fixture, not the other way round.

**C -- two controls that must fail.** An abstraction that drops a `for`'s `step`: it round-trips as a graph (both passes lose
it), and **only `rnxc dis` catches it**. A printer that drops comments: caught by the round trip. Either control not firing
fails the stage.

**K -- a corpus**, 78 files: the spike's own Ring (every third), Ring++'s probes (every ninth), Ring's standard library (every
seventh), a sample of Softanza (every 97th, up to 40 KB). Floors pinned: 20 fixtures, 24 files. For every file: graph exact,
second text equal to the first, and compiled code equal -- **with the `load` and `import` lines of both texts blanked**, because a
copy compiled elsewhere cannot resolve them. (Measured the hard way: the first stress run compared code for 268 of 2,847 files,
the 2,570 others being tests that load the library; it said "exact" for all.) A file whose original **rnxc refuses part of**
(`rnxc census`: a refused statement compiles to a trap) is compared as a graph only: the canonical text of such a file often
compiles where the original does not (a comment inside a lambda body is one). A file **Ring itself refuses** (`ring -norun`:
an unclosed comment, a literal not closed) is not a program and is skipped by name.

**`rnxc dis` is the judge, and it is normalized in three places, each measured** (`dis()` in `l1_check.py`): a lambda is named
after its source line (`@@lambda62`); the `ret=` of a method whose `return` the parser split is `str` beside `ref` for the
same program (the answers are the same, probed); and `vnew`'s capacity is counted off the tree's children (blank lines in a
literal change it) -- the elements are the `vpush` instructions after it, which stay compared. A fourth, the `say` flag (rnxc read
`put` and `See` as `?`), was normalized until 2026-10-04 and is gone: the compiler was fixed (HF-74), so the judge sees it again.

## 6. Measured

```
the guard sample      78 Ring files:   77 round-trip exactly, 1 as a graph only          (10 s)
all of Softanza       6,068 Ring files, 0 failing:
                      5,958 exact (graph, second text, and compiled code with the loads blanked)
                         52 as graphs only (rnxc refuses part of the original)
                         58 refused by Ring itself (an unclosed comment, a literal not closed: not programs)
   base       5,720   5,655 exact, 52 as graphs only, 13 refused           [5,699 up to 120 KB, in quarters; 21 above, to 3 MB]
   max          155   124 exact, 31 refused        core 36: 31 / 5       engine 103: 103 / 0
   future        53   44 exact, 9 refused          tools 1: 1
```

**Re-run in full on 2026-10-04, after rnxc's print flag, bare return and `&&`/`||` were fixed (HF-74) and rule 3 became Ring's: the same
counts, base in quarters, the files over 120 KB, max, core, engine, future and tools -- 6,068 files, none failing.** **The numbers are the stress's** (`probes/stress.py`, `probes/stress_big.py`), taken after the failures it found were
repaired; the last repair (a byte-order mark before a `load`, which only turns a failure into a pass) came between the quarters,
and its one file was re-run alone. Across the runs the stress found, in order -- the bare return split from its value inside a class; a `return` cut at a
`+`; a call chain cut at a dot; `end` read as a name; a brace on a whole assignment; `private` read as an identifier; the
comments between two nested classes reordered; a trailing comment hung on the wrong node; a list's capacity (the judge, not
the graph); a byte-order mark before a `load`; and a unit rnxc refuses. **Each was a place where the tree, or the judge,
differed from Ring, and the abstraction, which had trusted it, was wrong until the court said so.**

## 7. Left, named

* **Long lines.** The printer never wraps; a 19 KB list literal prints on one line. A wrapped literal is the refinement's
  business (rung 5), and the court shows the parse does not depend on it.
* **rnxc's print flag** (`See`, `SEE`, `put`) and **rnxc's `&&`/`||`** and **a bare `return`, then `end`, then a statement**
  (rnxc swallows the statement as the value; Ring does not) are ringpp's (HF-74), not this rung's.
* **`.rh` files and `load` resolution** are untouched: the graph is of one file.
* **Option A's 95 percent identity threshold** (CODEGRAPH 6) is rung 4's measurement, on this graph.
