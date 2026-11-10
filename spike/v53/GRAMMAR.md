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

## Named

- A `b` parameter given an unproven call's answer as an argument is not converted: the binding is the callee's, and no case asks it yet.
- `boolExpr`'s gate on a `.haro` file is not planted: in a `.ring` file a converted 1 and an unconverted one test alike, so the gate
  saves work and changes no answer a case could see.
