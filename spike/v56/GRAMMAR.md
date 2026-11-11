# Haro v0.56 -- every definition ends with `end`, in any order; `func` a function, `def` a method

HARO-DEFINITIONS-01. The Principal, 2026-11-11, in this desk's chat, after v0.55: "the ring's style of positioning classes at the end
etc, shloud not be adopted by haro. it was one of the things that let agents suffer most (including you) and waste token to remind them tat
each time! aloso, i would like to keep func for functions and def for methods so they are clearley separate", and for the rest "i let you
decide". His own: no position rule; `func` for functions and `def` for methods. The desk's readings (D68), on his delegation: a definition
is a block like every other and ends with `end`; a chain across lines continues with its dot at the start of the next line
(HARO-PORTTOOL-CHAINDOT-01, from stzlib-haroport). This replaces v0.55's F2 ("a definition has no end word") and its `func` for methods.

Fixtures first (1cf9fb0: 12 cases, 11 failing before the code; e9d668f: E13, E14 before their code). Code 4577bb0; haroport f3040fb; Haro's code rewritten a05259f (a tool commit).

| line | what | cases |
|---|---|---|
| G1 | every definition -- func, def, class, package -- ends with `end`. A definition without it, an `end` that closes nothing, a body on its header's line, or `endfunc`/`endclass` refuses the program at its first statement, so nothing runs | E06-E09, E15-E19 |
| G2 | `func` defines a function and `def` a method; `func` inside a class and `def` outside one are refused, each naming the other | E10, E11 |
| G3 | any order: a class, a function and the program's statements stand where the writer puts them; a statement at the top level is the program's, run in the order written; a function after a class is a function | E01-E05 |
| G4 | a `.ring` file reads as Ring reads it: a func after a class is its method, a statement after a func belongs to it | E12 |
| G5 | a chain across lines continues with its dot at the start of the next line; a dot that ends a line is refused | E13, E14 |

## How it is built

- **The structure is read from the tokens, not from the grammar.** In a `.haro` file every block and every definition ends with `end`, so
  each opener -- if, while, for, switch, try, do, `within`/`using` before a header, func, def, class, package -- is closed by the next `end`
  no inner opener took. `lift.zig`'s `defBraces` matches them and gives the parser each definition in braces (` {` after its header, `}` in
  place of its `end`), which the grammar reads one way only. No line moves, and the grammar is unchanged, so a `.ring` file parses exactly
  as before.
- `compile.zig`: in a `.haro` file each piece belongs where the tree puts it (`haroOwner`); every statement at a file's top level is the
  program's (`spliceOne`); the lift's fault refuses the program's first statement (`collectAll`, `file_fault`); `defForm` refuses `func` in a
  class and `def` outside one; the statement walk refuses a dot that ends a line inside a chain.

## Measured

- The court: 20 of 20 on haro and its checked build; plants D1-D10 and L1-L9 caught, each failing its own case.
- stzlib 4e354d7cc's `.ring` library, censused on v0.55 and on v0.56: the same code, 1,374,140 instructions; three statements fewer
  counted, each a bare `end` the grammar read as a name after a definition, which Ring holds inert (v18/probes/closers.py) and v0.56
  compiles as nothing.
- Stage 6, the cold compile, A (v0.55 on b2f10a7's sources) against B (v0.56 on its own), minima of 15 runs over 3 rounds
  (`study/v56/stage6_ab.py`): with each `.haro` file parsed twice (as written, then in braces) B-A was +25.2 ms (142.4 against
  167.6); parsed once, in braces, -23.5 ms (142.2 against 118.7) -- the braces spare the parser the readings it kept of each definition.

## The grammar, tried first and left as it was

The first build gave a definition's `end` a dynamic precedence in the grammar. It read every v0.56 case, and all 7,152 stzlib files parsed
the same but one (whose `haro check` was the same). Then a method whose last line held a `+` lost its `end` to its class: the parser
pruned the right reading before the `end` was reached, at any weight. Penalising a definition without a body fixed that and moved 556
stzlib trees, three statements of which compiled differently: `return pc = "=" or ...` became a bare return and an assignment. A grammar
shared with Ring's surface cannot be bent for one surface without moving the other, so the grammar is back as it was and the structure is
the tokens'.

## Haro's code, and haroport

`study/v56/defends.py` closed every definition of Haro's own code with `end` and wrote a method `def` (a tool commit): 189 files, 859
definitions, 34 methods; each `end` takes the blank line after its definition when there is one. haroport's rule O does the same for a
ported tree, takes a one-line definition's body to its own line, moves a dot that ends a line to the start of the next
(HARO-PORTTOOL-CHAINDOT-01: 342 chains in stzlib were being cut into a call and a global call) and reads a name that starts with a digit
(HARO-PORTTOOL-DIGITNAME-01).

## Named

- The shared haro.exe was replaced by a build of this uncommitted work on 2026-11-11 for some hours; Radar found its tools stopped
  (HARO-BREAKING-NOTICE-01). It was restored to b2f10a7, and work in progress builds only into `runtime/v56/` since.
- A plant left in `compile.zig` by an interrupted plants run (D5's `false and`) was found by a court and removed by hand.
