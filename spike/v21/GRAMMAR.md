# A second face of the program graph, in Python's shape, as a printer (Haro v0.21, the twenty-first rung)

**Rung 6 of the code-graph memo** (`haro/CODEGRAPH.md`, section 7), built on the author's "go ahead with rung 6" (2026-10-19). **Written after** the
fixtures in `fixtures.txt` (46: the first 28 composed before `face_py.py` existed, the rest written as building found what the first ones had not
asked -- section 5), after the court that judges them (`face_check.py`, guard stage 25), and after `face_py.py`.

**What this is, in one line.** Rung 18's graph of a Ring program, printed in Python's shape so a Python reader -- a human or a model -- can read it,
with **one meaning, Ring's** (CODEGRAPH 3.2). It is one-way: nothing reads the face back (that is rung 7, and K3 decides whether it is built).

## 0. What exists, and what does not

| | status | where |
|---|---|---|
| the printer: graph to Python-shaped text, or a refusal by name | **built** | `face_py.py` (`print_py`), sections 1-3 |
| the collision table, sixteen entries, and the banner that travels with every text | **built** | `COLLISIONS`, `BANNER` |
| the court: fixtures, Python's parser on every text, the table reached, five controls, Softanza's corpus | **built**, `python haro/spike/v21/face_check.py`, guard stage 25 | section 4 |
| K3 measured on the corpus | **built**, a line of the court | section 6 |
| a reader of the face (text back to the graph) | **not built**: rung 7, open | section 7 |
| K4 and the memo's 20-task protocol: a model writing in each face under its GBNF | **not built** | section 7 |
| a runtime for the face's words (`at`, `eq`, `say` ...) so the text runs under Python | **not built**, and not the point: the text is read, not run | section 7 |

## 1. Three treatments, one rule

A Python reader must never take the program for something else. So each construct is exactly one of:

- **spelt plainly**, where Python reads it as Ring means it: an assignment, a call, a body, arithmetic and comparison between two values both known
  to be numbers (or `+` between two strings), `if`/`elif`/`else`, `while`, a for-in that only reads its variable, a comment (every kind written `#`);
- **spelt with an explicit word**, where Ring means something a Python reader would not guess -- the word is the warning:

| Ring | the face | why |
|---|---|---|
| `aL[i]`, `aL[i] = v` | `at(aL, i)`, `setat(aL, i, v)` | 1-based (C-3, F-54) |
| `aL[i] += v`, `aL[i]++` | `setat(aL, i, plus(at(aL, i), v))` | the target read once -- refused when it holds a call (`index-twice`) |
| `x = y`, `!=`, `<` ... (kinds not both known) | `eq(x, y)`, `ne`, `lt`, `gt`, `le`, `ge` | a numeric string equals its number (C-8) |
| `+` (kinds not both known) | `cat(a, b)` when the left is a string, else `plus(a, b)` | one operator, two meanings; `add` is Ring's own list builtin |
| `%` | `mod(a, b)` | Ring's sign rule |
| `for i = a to b step s` | `for i in span(a, b, s):` | inclusive |
| `a:b` | `rng(a, b)` | inclusive, eager (F-65) |
| `and`, `or`, `not` as a value | `both(a, b)`, `either(a, b)`, `negate(x)` | Ring's 1 or 0; Python's in a condition |
| `?`, `see`, `give x` | `say(x)`, `see(x)`, `x = give()` | Ring's printing and input |
| `$x` | `G.x` | the global (Rule A) |
| `@x`, `This.x`, a class-region name in a method | `self.x` | the attribute |
| a function that runs off its end, a bare `return` | `return ""` | NULL is the empty string (F-66) |
| a class region | `def __region__(self):` (and `super().__region__()`) | it runs at `new`, before `init` (F-121) |
| `try ... catch ... done`, `cCatchError` inside the handler | `except RingError as e:`, `str(e)` | the handler's own message (C-15) |
| `switch x on 1 ...` | `_switch = x` then `if eq(_switch, 1):` ... | Ring's `=`, the subject read once |
| `do ... again c` | `while True:` ... `if not (c): break` | the body runs first |
| `:Name`, `NULL`, `true` | `"name"`, `""`, `1` | what they are on Ring |
| a number past 2^53 | `9007199254740993.0` | a double on Ring (F-75) |
| a block of comments only | the comments, then `pass` | Python needs a statement |
| `func Main` | the function, then `main()` | Ring calls it after the top level (F-60) |

- **refused by name**, where no spelling cannot be misread -- the collision table (`COLLISIONS`), sixteen entries, each a finding or a correction
  already paid for: `brace` (a brace block), `eval` (F-72), `operator` (F-69), `getter` and `setter` (F-73), `catch-error` (C-15), `for-after`
  (section 2), `for-in-write` (by reference), `exit-levels` (`exit 2`, `loop 2`), `increment-value` (`n++` as a value, F-64), `lambda` (C-14; not
  spelt in this rung), `call-name` (`call f()`), `package` and `scanner` (C-28), `index-twice`, `dollar-param` (F-91). A refusal names its
  collision and the construct: `refused -- for-after: the variable of a numeric loop read after its loop -- ... (i)`.

**Names.** One name, one spelling: Ring folds case (F-18), so every use is written as the name's first occurrence. A Ring name that is not a Python
name is spelt as one, by one rule (`ident`): a Python keyword or one of the face's own words takes a trailing `_` (`del` -> `del_`, a function `G`
-> `G_`, since `G` is the globals); the `@` that begins a Softanza function's name is `at_` (`@Twice` -> `at_Twice`); a leading digit takes `_`
(`1Card` -> `_1Card`); any other character Python does not allow becomes `_`.

**The banner.** Every text begins with one line that says what the words mean -- the collision table's spellings travel with the face, as the memo
asks ("the table is the face's banner").

## 2. A loop variable read after its loop

On Ring a numeric loop leaves its variable at the value that FAILED the test (`4` after `for i = 1 to 3`); Python's leaves the last value. So a read
of the variable after its loop is `for-after`, refused -- and the first rule ("the name appears anywhere after the loop in the same block") was
wrong both ways, which the corpus said before any fixture did (section 5):

- **too strict**: a later loop on the same variable, `i = 0`, or a function's parameter of that name WRITE it before anything reads it;
- **too loose**: the rest of the same block is not all that runs next.

The rule now: scan **what can run next, in order, to the end of the function** -- the rest of each enclosing block; for an enclosing loop body, the
body again from its start (its next turn, which reaches the loop itself again); for a try body, its catch and finally -- and refuse if the variable
is READ before it is WRITTEN FOR CERTAIN. The scan descends into statements: an `if` or a `switch` writes for certain only if every branch does and
there is an `else`; a `while` or a for whose body may not run writes nothing for certain; a numeric loop on the variable writes it at entry; a
`try` writes for certain only through its finally, or a body and a catch that both write. **Once an `exit` or a `loop` may have jumped past what
follows, no later write is certain** and the scan goes on for reads alone. A function or class is another scope (Rule A) and is skipped, unless the
variable is a `$` global. `next i` leaves `i` as a statement in the graph: a read whose value is dropped, which changes nothing and is not counted.

Fixtures 40 to 46 pin each half: two that print because the variable is written first, four refused (after an enclosing `if`, on an enclosing
loop's next turn, in the catch of the try that holds the loop, after an `exit` that may skip the write), and `next i`.

## 3. Kinds

A light inference decides where an operator may be Python's: a name assigned only numbers is a number, only strings a string, from literals,
arithmetic, `len` and its kin, a numeric loop's variable; the parameters of a function are unknown. It is per function and conservative -- a kind it
cannot prove is unknown, and an unknown kind takes the explicit word. Nothing else depends on it.

## 4. The court (`face_check.py`, guard stage 25, about a minute)

    F  46 fixtures: 26 print exactly their text, 20 are refused for exactly their collision and words
    P  every printed text starts with the banner and is Python syntax (ast.parse); printing twice gives the same bytes
    T  the collision table: 16 collisions, 16 reached by a fixture
    D  five controls that must FAIL the fixtures: Python's brackets for an index, `==` whatever the kinds, a backslash as an escape, comments
       dropped, a brace block printed
    K  300 files of Softanza's base through the face: every text that prints must be Python syntax; refusals ranked
    --plant fails it

## 5. What building found (HF-91 to HF-94)

- **The loop-variable rule needed the program's flow, not its next lines (HF-91).** The first rule refused 87 of 300 corpus files and missed four
  shapes that change an answer silently; the flow scan refuses 2, and fixtures 41 to 44 are the four.
- **Ring's names are not Python's, and neither is the face's own vocabulary (HF-92).** Nine corpus texts were not Python at the first run: `del`
  (a Ring builtin, a Python keyword), Softanza's `@`-prefixed function names, a name beginning with a digit -- and the face's word for `+` was `add`,
  which IS a Ring builtin (it appends), so `add(aL, x)` would have printed two different things the same way. The word is `plus`.
- **Two constructs had no spelling the first rule saw (HF-93):** a `$x` parameter is the function's own local on Ring (F-91), which `G.x` would
  misread; a compound write `aL[F()] += 1` evaluates its target once and `setat`-over-`at` would run `F()` twice. Both refused by name; a block of
  comments only takes `pass`.
- **K3, measured (HF-94):** section 6.

## 6. K3

Kill criterion K3 says: if the collision fixtures outnumber the spellings, a second face is a reading aid and is not built as a parser. Measured:

    fixtures            26 spell, 20 are refused
    Softanza's base     300 files: 227 print whole (76%), 72 are refused, 1 does not parse as Ring
    what refuses        eval 22, call-name 20, lambda 19, operator 6, for-after 2, dollar-param 2, index-twice 1

**K3 is not met; rung 7 stays open.** Read it with its limit: a file prints whole only when NOTHING in it collides, so 76% is a floor on how much
of a file a reader gets; and the refusals are Ring's dynamic features -- eval and `call` by name (42 of 72) put a string where the graph has a
hole (CODEGRAPH 3.5), which no face can spell. `lambda` (19) is the one a later rung could spell: a lambda's free names are globals read when it
runs (C-14), which `G.` already says.

## 7. Not built, named

- **K4 and the 20-task protocol.** Whether a model writes a program better in this face than in Ring's, each under its GBNF, is the memo's other
  kill criterion and the rung's named guard; it needs the reader (a face written by a model has to come back to the graph to be judged) and a model
  run, so it waits for rung 7's decision.
- **A reader** (rung 7): K3 allows it; not started.
- **Lambdas**, spelt (see section 6); **a runtime for the face's words** -- the text is for reading, and `say`, `at` and their kin are named by the
  banner, not shipped.
