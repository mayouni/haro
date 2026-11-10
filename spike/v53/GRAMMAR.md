# Haro v0.53 -- the classic Ring surface's 1 and 0 cross as false and true

HARO-RINGBOUNDARY-BOOL-01, from stzlib-haroport (2026-11-10 04:12): in a `.haro` file, `bFlag = OldFlag()` where a `.ring` function returns
1 was TYPE_LETTER, and `if OldFlag()` was BOOLEAN_EXPECTED -- so no `.haro` code could call Softanza's `.ring` predicates while the library
moves to `.haro`, bottom up. TYPES.md section 6 (D55, ruled 2026-11-07) had ruled the binding: "an integer 0 or 1 entering a b name becomes
false or true, and any other integer is refused". This rung builds it, and reads a condition as the same crossing.

Fixtures first (ffbc76e: 14 cases, 5 failing before the code; 9 held and guard). Code f2b5861. **Two fixtures changed after the code,
said so**: V05's object was named `oK`, the keyword `ok` in another case, and is `oThing`; V12 asked `Len("ab")`, whose 2 is never
converted, so it could not tell a built-in proven Haro's from one that is not -- `Len("a")` answers 1, and the case then found that `Len`,
compiled to an opcode of its own, was not in the built-in table the first test asked: the test now asks Ring's 258 names and Haro's.

| line | what | cases |
|---|---|---|
| R1 | a `.ring` answer 1 or 0 given to a `b` name with `=` is `true` or `false` | V01 |
| R2 | ... in a condition (`if`, `elseif`, `while`) and as an operand of `not`, `and`, `or` | V02, V03, V04 |
| R3 | ... from a method dispatched by name | V05 |
| R4 | any other answer is refused by the check that stood: TYPE_LETTER at a `b` name, BOOLEAN_EXPECTED in a condition | V06, V07, V08 |
| R5 | a call the compiler proves is Haro's stays strict -- a function of a `.haro` file, a built-in, a method through `this`; a value no longer a call's answer is not converted; arithmetic sees the integer | V09, V10, V11, V12, V13 |
| R6 | a `.ring` file reads as it did | V14 |

## The desk's reading (D65)

- **Where**: the compiler converts where a boolean is wanted -- a `b` name given the value with `=`, a condition, an operand of `not`,
  `and`, `or` -- and only the answer of a call: a value already bound, `iX = OldFlag()` then `if iX`, is an integer and stays one.
- **Whose call**: one the compiler cannot prove is Haro's -- a function declared in a `.ring` file, a native it does not know (Softanza's
  engine answers 1 and 0 too), a method dispatched by name. A function of a `.haro` file, a built-in, and a method reached through `this`
  in a `.haro` file are Haro's, and a `.haro` function still answers a boolean when a boolean is meant.
- **What**: 1 becomes `true` and 0 `false`; anything else is left as it is, so the check that stood refuses it in its own words.
- **Cost**: nothing on the call path. A `.ring` function returns as it always did; the conversion is one instruction after the call, in
  a `.haro` file's boolean place.

## How it is built

- `compile.zig`: `unprovenCall` decides whose a call is; `boolExpr` compiles an operand where a boolean is wanted and adds the conversion
  after an unproven call; `assign` marks the call a `b` name is given, and the call is converted where it is compiled, so a local, a
  global and an attribute alike receive the boolean.
- `main.zig`: `truth` with `c = 4` -- a 1 or 0 becomes a boolean, anything else stays.

## Measured

- **The court**: 14 of 14 on haro and its checked build (stage 57).
- **Plants**: Q1 to Q11, each one protection switched off: 11 of 11 caught. **The guard**: 58 stages, 1,519 s, every stage passing but stage 48, whose B22 asserted the old crossing (a .ring 1 an integer to a .haro condition); B22 changed by the ruling, said so, and stage 48 then passes on the committed tree.

## haroport, beside the rung (HARO-PORTTOOL-01)

`port/haroport.py`, stzlib-haroport's second ask: one command over a tree root -- `plan ROOT [--json]` writes nothing, `apply ROOT --out
DIR` writes the ported tree beside the original, each `.ring` file as `.haro` and each load rewritten to it. It lowers keywords
(`lift.zig`'s list and the scanner's `to`, `in`, `step`), respells built-ins unless the tree defines the name, makes Softanza's `c` and `v`
into `t` and `x` across the whole tree, letters a function's bare locals by what they hold, and unwraps Softanza's `_name_`; a rename
landing on a keyword, a name already there or a class's attribute is refused and listed. Fixtures first (8ff5486: 11 cases); the tool
40d76b9; H12 added after the tool, said so; 12 of 12, plants T1 to T11 caught (stage 58). On stzlib cb6f5de65: 6,936 files, 501,043
rewrites, 4,475 refused (4,272 a class's attribute written bare in a method, 109 a keyword, 94 a name already there); the ported tree
compiles 95,388 of 140,737 statements (67%), where the rename alone compiled 24%. The 21 families left lead with a name that has no type
letter (26,581: globals and names at the top level or in a class body, which the tool leaves) and a `b` name given 1 or 0 (5,051).

## Named

- A `b` parameter given an unproven call's answer as an argument is not converted: the binding is the callee's, and no case asks it yet.
- `boolExpr`'s gate on a `.haro` file is not planted: in a `.ring` file a converted 1 and an unconverted one test alike, so the gate
  saves work and changes no answer a case could see.
