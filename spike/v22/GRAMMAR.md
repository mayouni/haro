# The reader of the Python-shaped face (Haro v0.22, the twenty-second rung)

**Rung 7 of the code-graph memo** (`haro/CODEGRAPH.md`, section 7), built on the author's "continue" (2026-10-20), after K3 had been measured and not met (rung 6, HF-94).
**Written after** the fixtures in `fixtures.txt` (67: composed by hand before `face_read.py` existed, the same discipline as every rung, and amended in the open as the oracle
showed where they were wrong -- section 7), after the court that judges them (`face_read_check.py`, guard stage 26) and after `face_read.py`.

**What this is, in one line.** A text in the face rung 6 prints, read back to rung 18's graph -- and from the graph to Ring -- with **one meaning, Ring's**. It accepts exactly
the printer's image: the text is parsed with Python's own parser, a graph is built from the tree, the graph is printed back by v21's printer, and the two must be the same
Python up to layout, comments, quotes, parentheses and the few things the face writes out. A text that is not the face's own spelling of one Ring meaning is refused
with the line the face writes instead. That is the memo's rule 4 (a face is a parser, a printer, a spelling table and a collision list under a round-trip court), and the
reason the printer had to change first (section 7): a reader needs a face that is injective, and rung 6's was not.

## 0. What exists, and what does not

| | status | where |
|---|---|---|
| the reader: face text to the graph, or a refusal by name | **built** | `face_read.py` (`read_py`, `read_ring`), sections 1-4 |
| the printer made invertible, and a formatter (print of a read text is that text) | **built**, v21 amended | `v21/face_py.py`, `v21/GRAMMAR.md` section 8 |
| the declared losses: what the face does not keep, as one function | **built** | `losses.py`, section 6 |
| the court: fixtures, the printer's text read back, controls, the corpus to the same graph, the oracle | **built**, `python haro/spike/v22/face_read_check.py`, guard stage 26 | section 5 |
| the lenient reading (a model's text that is not the face's spelling, read anyway, for K4 to count) | **built** | `read_py(text, strict=False)` |
| a GBNF for the face (the write surface of a model that writes it) | **drafted, owed**: `face_gbnf.py`, held by the decoder, 27 of 43 printed texts accepted | section 8 |
| K4: a model writing in each face | **measured 2026-10-20 and 2026-10-21: met for capable models and for small local ones** (`k4/K4.md`, HF-110 to HF-115) | section 8 |
| lambdas, brace blocks, `eval`, `call f()`, operator methods, getters, setters | **not spelt**: refused by the printer (v21), so never read | `v21/GRAMMAR.md` section 1 |

## 1. The rule: read, print, compare

    text --ast.parse--> Python's tree --build--> a graph (rung 18) --print_py--> the face's text for it
                                                        \                              |
                                                         `---- print_ring ----> Ring    `-- the two must be one Python, or `not-canonical`

`read_py(text, strict=True)` builds the graph and prints it with `face_py.print_py`; if that raises (a collision: `for-after`, `name-clash`, ...) the text is refused for the
printer's collision. Otherwise the two texts are compared as syntax trees after the invisible differences are taken out of both -- layout, comments, quotes, parentheses,
a function's trailing `return ""`, the closing `main()` call, `pass`, nested `and`/`or` -- and a difference is refused as `not-canonical`, **quoting the first line that differs
and the line the face writes** (`line 2: the text has `return a == b`, the face writes `return eq(a, b)``). `strict=False` skips that comparison and keeps the printer's collisions:
the text is read with the meaning it has, which is how K4 will count how often a model needs the correction.

Why exactly the printer's image, and not "any Python that has a Ring meaning": the face's rule is that a Python reader must never take the program for something else
(CODEGRAPH 3.2), and the dangerous cases are the ones where Python's text is valid and means something else -- `a == b` on a string and a number, `+` on a string and a
number, `a[0]`, `not` over a comparison. The kind inference that decides where an operator may be Python's lives in the printer; the comparison reuses it, so a model that
writes `x == y` where the kinds are unknown is told to write `eq(x, y)`, and is never silently given Python's `==`.

## 2. What a text spells, read back

The inverse of `v21/GRAMMAR.md` section 1, one row per spelling:

| the face | Ring | |
|---|---|---|
| `at(a, i)`, `setat(a, i, v)` | `a[i]`, `a[i] = v` | 1-based |
| `eq(a, b)` `ne` `lt` `gt` `le` `ge`, or `==` `!=` `<` ... where both kinds are known | `=` `!=` `<` ... | Ring's comparison (C-8) |
| `cat(a, b)`, `plus(a, b)`, or `+` where both are known | `+` | |
| `mod(a, b)`, `rng(a, b)` | `%`, `a:b` | |
| `both(a, b)`, `either(a, b)`, `negate(x)`, and `and` `or` `not` in a condition | `and` `or` `not` | 1 or 0 as a value |
| `say(x)`, `see(x)`, `x = give()`, `load("f")`, `bye()` | `? x`, `see x`, `give x`, `load "f"`, `bye` | |
| `for i in span(a, b, s):`, `for x in list:` | `for i = a to b step s`, `for x in list` | inclusive |
| `try: ... except RingError as e: ... finally: ...`, `str(e)` | `try ... catch ... finally ... done`, `cCatchError` | |
| `_switch = x` then `if eq(_switch, v) or ...: ... elif ...: ... else: ...` | `switch x on v, ... other ... off` | found again |
| `while True:` ending `if not (c): break` | `do ... again c` | found again |
| `G.x` | `$x` | the global |
| `self.x` in a method, `self.at_x` | `This.x`, `@x` | |
| `at_Foo`, `Foo__at__Bar`, `at_` | `@Foo`, `Foo@Bar`, `@` | one escape for the sigil, anywhere |
| `del_`, `G_`, `_1Card` | `del`, `G`, `1Card` | a keyword or face word takes `_`, a leading digit `_` |
| `new(K, a, b)`, `new_without_init(K)` | `new K(a, b)`, `new K` | only the first calls `init` |
| `[a, b]`, `["name", v]` | a list; a pair is a list of two | F-59 |
| `def __region__(self):`, `# private: ...` | the class region; `private` | |
| `main()` last, `return ""` last | dropped: Ring calls `Main`, a function returns NULL | F-60, F-66 |

## 3. What the reader decides once

The printer maps several graphs to one text; a reader must pick one, and says so. Each is a **named loss** (section 6), pinned by a fixture or by the corpus:

- `x += 1` is `x++`; `x = plus(x, y)` stays `x = x + y` (it is not rewritten to `x += y`: `+=` and `x = x + y` differ only on `nl`, HF-108).
- `self.x` in a method is `This.x`; in `__region__` it is the bare name, when the region assigns it (the printer decides the same way, so the two agree).
- A catch has a binding only if the handler uses the name other than as `str(e)`.
- `return ""` is a bare return, dropped when it is the function's last statement and carries no comment (a comment would go with it).
- A `not` that is the operand of a comparison, of arithmetic or of a unary sign is written with its parenthesis in the Ring (`(not a) = b`): Ring binds `not` looser than they are (HF-105) and the graph reads it so (F-130), so a graph read from Ring text keeps the parenthesis the text had and the reader writes it, which keeps the round trip exact; the operand OF a `not` needs none (`not (a == b)` is `not a = b`).
- The three kinds of comment are `#`, one comment a line; `# private: the methods below are private to the class` is the `private` marker.
- A comment after code on its line follows the deepest statement that ends there; on a header line it opens the block.

## 4. What the reader refuses

| id | for |
|---|---|
| `syntax` | the text is not Python (Python's own message follows) |
| `construct` | Python the face has no word for: lambda, comprehension, tuple, dict, set, `True`/`False`/`None` (the face writes `1`, `0`, `""`), a subscript (`at(a, i)`), an f-string, `import`, `raise`, `with`, `assert`, `del`, a keyword or default argument, `*args`, a chained comparison, `is`, `in`, `//`, a conditional expression, `else` on a loop, `while True:` that is not a do-again, a class body that is not methods, a method without `self`, a definition inside a block, `a = b = 1` |
| `word` | a face word used as the face does not use it: `at(a)`, `span` outside a loop, `say` as a value, `str(x)` outside a handler, `G` alone |
| `order` | a statement after a definition belongs to the last function on Ring (HF-73); a function after a class is a method of it (F-21): the top level first, then functions, then classes |
| `not-canonical` | a spelling the face does not print for that graph, with the line it writes |
| (the printer's 23) | every collision of v21: a text the printer would refuse to print is refused to read |

## 5. The court (`face_read_check.py`, guard stage 26)

    F  67 fixtures: 33 read to exactly their Ring, 34 refused for exactly their id and words
    H  the fixtures are honest: every text is Python, every Ring is canonical Ring, 29 of the 33 read texts are v21's own image of their Ring
    R  the 42 fixtures v21 prints are read back from the printer's own text and printing the reading gives the same text
    D  five controls on the reader that must fail the fixtures: Python's meaning for eq(), an index read 0-based, a binding kept that the handler does not use, a reader that
       does not insist on the face's spelling, a reader that forgets the sigil of at_
    K  300 files of Softanza's base: 221 print whole, and each is read back from its own text to the same text (78 are refused by the printer, 1 does not parse as Ring)
    L  and read back to the SAME GRAPH, up to the 12 declared losses (+ 2 synthetic cases for the two the sample does not show), and each loss is needed: taken out in turn, it
       fails on 24 files (case), 91 (parentheses), 162 (strings), 52 (pairs), 58 (assignment), 60 (returns), 77 (comments), 6 (trails), 12 (else-if), 144 (classes), 1 (catch), 1 (numbers)
    S  THE ORACLE: each of the 159 probes of bench/exec that the face can spell (95; the rest hold eval, lambdas, braces, loads, a loop variable read after its loop ...), printed,
       read back to Ring and run on the oracle from one path and one folder, prints what the original prints, 95 of 95, line numbers aside (the program is printed again)
    --plant fails it

**Which judge decides what.** The oracle decides meaning (S); the graph comparison decides that nothing was lost that is not named (L); the fixtures decide the spelling. Compiled code
(`rnxc dis`) was tried and is the wrong judge: it is exact up to the compiler's own choices, and 7 of 21 files compiled alike where the named losses (an `x++` read as `x += 1`) alone
change an instruction.

## 6. The declared losses (`losses.py`)

Across faces, L1 to face to L1 is exact (CODEGRAPH 3.6) **up to these twelve**, and only these. Each is a spelling, never a meaning, and each can be switched off so that the court
shows it is needed:

    case      names: Ring folds case (F-18); the face writes every use as the first spelling
    parens    the face prints Python's precedence, not the author's parentheses
    strings   a string is its value (quotes are the face's choice); `:Name` is "name", NULL is "", true is 1
    pairs     `:name = value` is the list ["name", value] (F-59); a string key before `=` in a list is a comparison (F-93)
    assign    `x += v`, `x -= v`, `x++` and `x = x + v` are one statement; `&&` is `and`; `exit 1` is `exit`
    returns   running off the end, a bare `return` and `return ""` are one NULL (F-66)
    comments  one line a comment, all written `#`
    trails    a comment after a statement follows the deepest statement that ends its line
    elif      an else holding only an if is an elif
    classes   the region first then the methods; a region's bare name, `This.x` and `x` are one attribute; `This.@x` is `@x`
    catch     a binding is kept only if the handler uses it
    numbers   a number past 2^53 is written as the double it is (F-75)

## 7. What building found (HF-104 to HF-109)

- **The printer was not injective (HF-104).** Four things that a Python reader cannot tell apart: `new K(x)` and a call of a function `K(x)`; `@x`, `This.x` and a region's bare `x` (all `self.x`); `o.@x` (printed `o._x`, which is also a name Ring allows); and two Ring names that print as one (`del` is `del_`, and `del_` is a name). Fixed by changing the face, not the reader: `new(K, ...)`, `at_` for the sigil everywhere, `__at__` inside a name, a generic clash check over every name printed, and four more collisions -- fixtures 47-50, 67-71 of v21 first.
- **`new K` does not call `init` and `new K()` does (HF-106),** which the printer had written as one call. Found by the oracle step: 41 of 98 runnable probes behaved differently after a round trip, and 37 of them were this one line (`Calling Function without definition: init`). The face has two words now, `new` and `new_without_init`.
- **Ring binds `not` looser than a comparison, and rnxc does not (HF-105).** Measured on the oracle: `not a = b` is `not (a = b)`; rnxc compiles `(not a) = b`, and the graph and the formatter read the same tree. A silent wrong answer in the shipped compiler, found by a reader that had to write Ring: the face refuses a graph of that shape (`not-precedence`), the reader parenthesizes the `not` it means. Reported and spawned as its own task; not fixed in rung 7. **Fixed 2026-10-20** (ringpp C-32, F-130): the compiler lifts a `not` over its chain where the text is loaded (src/lift.zig), the graph (l1.py `lift_not`) and the formatter read it as Ring does, `not` has its own precedence in the printer (between `and` and the comparisons), and the face's collision is retired with its fixture; the reader keeps the parenthesis round a `not` operand, and R29's Ring is `if not a = b`.
- **`:name = value` outside a list literal is a comparison to the graph and a pair to Ring++ (HF-107),** and a string key inside a list literal is a pair node in the graph and a comparison on Ring (F-59, F-93): the printer wrote `F(:from = 3)` as `eq("from", 3)` and `[ "name" = v ]` as a string with its quotes inside. Both printed right now.
- **`x += nl` is not `x = x + nl` (HF-108)** (vmexpr.c:27: a number plus the newline alone is text; `+=` has no such case), so the face refuses a `+=` of `nl` unless the left side is known to be a string -- which is nearly always.
- **The printer is the formatter (HF-109).** Parenthesizing by the author's nodes made `print(read(print(g)))` differ from `print(g)`; the printer now prints Python's precedence and no parenthesis node, and the fixed point holds on 221 of 221 files. Two more facts the corpus supplied: a block comment's blank line printed `# ` with a space, and an `else:` holding only an `if` is, in Python's tree, an `elif`.
- **What it cost.** The stricter printer refuses more: files that print whole were 227 of 300 (76%, rung 6) and are 221 (74%). K3 stays not met.

## 8. Not built, named

- **K4 is measured, and met (2026-10-20).** Twenty tasks, shown and hidden data, Claude haiku and sonnet: Ring 19-20 of 20 with or without a primer, the face at best ties (20 of 20 read for its meaning, 20 of 20 again respelled by the printer, 2-5 of 20 under its strict spelling). `k4/K4.md` has the design, the table and the limits; HF-110 and HF-111 the findings. For them the face is a reading aid, a lint and a respeller, not a write surface. **The regime Softanza names, a small local model under the decoder, was measured on 2026-10-21** (SmolLM2-135M, Qwen2.5-Coder-0.5B and 1.5B; the face does not beat Ring++ at any size, and the decoder buys shape and not meaning; HF-114) -- so the consequence holds there too.
- **A GBNF for the face: built 2026-10-21.** `face_gbnf.py` (about 93 of the decoder's 128 rules) accepts the twenty K4 programs and 39 of the 43 texts the printer prints for the v21 fixtures, rejects what the shape excludes, and is judged with its Ring++ counterpart (`ringpp_gbnf.py`) by `grammar_court.py`, guard stage 27, with no model loaded; the four it does not accept are trailing comments, `next i` and `new @`.
- **The collisions' own spellings** (lambda is the one K3 named as spellable), and a face for the declared altitude.
- **A reader for the corpus's tests**, which hold `load`, `eval` and braces the face does not spell: 95 of the 159 runnable probes, 221 of 300 library files.
