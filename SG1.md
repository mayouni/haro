# SG1.md -- the system grain of Haro's computing altitude, a draft

**A draft of the desk, 2026-11-07 21:39. Nothing in it is ruled and nothing is built.** It answers COMPASS-SYSLANG-02 (the
Compass, 2026-11-06 08:41: "SG1, the system grain designed inside charter section 5 (memory regime, capability types from arXiv
2603.00991 as principle 12's spec, BUDGET/PERSONAL/NEEDS as types, totality, the C ABI door), fixtures first") on SG0's decision
memo (syslang-sg0, 2026-11-07 13:09). Its type seats are written as an amendment of D55 (section 9), which is
HARO-TYPES-SYSTEM-01, and its decisions are one row with parts for the author (section 10).

What binds it, and is not reopened here:

- **The author's ruling of 2026-11-06** (CHARTER section 5): (a) Softanza's system language IS the system grain of this altitude --
  never a sibling language, never a letter, no second language drafted beside it; (b) C is the first native target and
  WebAssembly the second, behind one owned compiler, LLVM and MLIR refused; (c) self-hosting is tripwire T4.
- **D55** (TYPES.md, ruled 2026-11-07): no coercion, a checked letter per exact type, a real boolean, decimals, no null in every
  type, judged types. The grain adds to it; it changes none of its eight decisions.
- **The Substrate ruling of 2026-10-30**: Zig at the pin for the engine. The grain's first compiler is the Haro VM's, in Zig
  (stage1).

---

## 1. What SG0 gave, and what it did not

- **D1, the surface stands, on a ceiling.** Sonnet and opus wrote 479 of 480 programs right in the estate's surface and in Zig:
  no penalty measurable at this difficulty, not parity at any. SG1 therefore keeps Haro's surface and adds seats; it does not
  move the spelling (SG0's D3 did not fire).
- **The typed hole is the mechanism that mattered.** Haiku wrote 0 of 60 programs right without it and 60 of 60 with it. Every
  failure was one trap: the data line was `nums` at the top level, and the function read `$nums` -- two names (Rule A). When
  the driver passed the data as a typed parameter, the trap was gone. D55's letters rest on the same claim: a type the grammar
  can see is a type the decoder cannot get wrong.
- **Eight seats the surface does not have** (syslang-sg0 `docs/EXPRESSIBILITY.md`, each probed on haro c90edaf):

  | | what code needs | today |
  |---|---|---|
  | X1 | a wrapping 32-bit multiply | by hand only; the naive `(h * 16777619) & 0xFFFFFFFF` is WRONG and reads right |
  | X2 | unsigned 64-bit integers | no: numbers past 2^53 are doubles, bit operators act on signed 64 |
  | X3 | a fixed-size buffer | no type: a list of doubles that grows, a string that cannot be written in place |
  | X4 | an explicit allocator | no: memory is the VM's |
  | X5 | a reference to a scalar slot | not directly: a one-item list as a box |
  | X6 | a struct's byte layout | by hand: `int2bytes` gives one shape, 4 bytes little-endian |
  | X7 | a fixed-width integer that traps or wraps | by comparing each partial sum with 2147483647 |
  | X8 | 32-bit NOT and shifts | yes, with a mask every time |

- **A grammar of the system grain** must carry the bit operators, hex, `finally` and `catch e`; the engine's decoder refuses a
  statement four levels deep and a subscript assigned below the first level although the grammar has productions for both.
- **What SG0 did not measure**: code that NEEDS a seat. Its eight GAP tasks worked around each gap by bounding the input, and
  every frontier model passed them; that says nothing about a hash, a codec or a driver that cannot be bounded.

## 2. What the VM is today, measured here

| | where | what |
|---|---|---|
| values | `vm/src/main.zig:587` | eight tags: `nil, int, num, str, vec, obj, dll, cptr`; a value is 16 bytes |
| integers | `main.zig:4164` | 64-bit, and past 2^53 a double, with no word said (kept to match Ring) |
| memory | `main.zig:24-32`, `build.zig:33` | reference counting with real frees, deferred counting (Deutsch-Bobrow) on registers, mimalloc as the heap; typed registers carry no count traffic |
| cycles | `main.zig:2720`, `3447` | none detected: Ring has no cycle collection and the fork kept that |
| the foreign door | `vm/src/native.zig` | ABI v1, the engine's: an integer, a double, a borrowed string, an opaque handle cross; nothing else; strings in are borrowed, strings out copied, handles never freed by the VM |
| types | `vm/src/types.zig` | level-1 checking of the annotations Ring accepts and drops; runtime unchanged |
| doors | CHARTER D51 | nine words, declared on a LANGUAGE (`NEEDS`): filesystem, process, network, environment, dynamic_load, gpio, threads, clock, inference; the program half waits on W7's map |

No C target exists. No WebAssembly target exists.

---

## 3. The one design choice: a grain is a profile, not a language

The seats below are **Haro's, in every `.haro` file**: a hash written in a court's helper wants a wrapping word as much as a
driver does, and two type systems in one language is what D55 section 5 ended. Ruling (a) says the same thing from the other side.

**The system grain is a profile a unit declares** -- `PROFILE system` on its first line, as the charter's profiles are declared
(P1: declared, never silent). It does not add a seat. It REFUSES what the C target cannot hold without a runtime:

1. a managed allocation (a text, a vector, a map, an object made) outside a region (section 6);
2. `eval`, `load` at run time, a text run as code;
3. a call through a name the compiler cannot resolve (dynamic dispatch on a class not known when compiling);
4. a door not declared by `uses` (section 7).

What is left -- integers and words of a declared width, booleans, floats, bytes of a fixed length, records with a layout,
references, regions, total functions, the C door -- compiles to C with no Haro runtime linked, which is SG2's first target
(COMPASS-SYSLANG-03, numtheory). A unit without the profile keeps every seat and its managed values; only the profile's unit is
promised to compile without a runtime.

---

## 4. Integers and words (X1, X2, X7, X8)

**Two families of whole number, because they are two algebras.**

| family | letter | what its arithmetic means | on overflow | bit operators |
|---|---|---|---|---|
| `integer` | `i` | a number: a count, an offset, a size | raises `INTEGER_OVERFLOW` (D55 T1) | refused, `todo` the word it meant |
| `word` | `w` | a bit pattern, arithmetic modulo 2^n: a hash, a checksum, a PRNG state, a register | wraps, by definition | `& \| ^ ~ << >>` at its width |

- **Widths are part of the full type**, written where D55 writes full types (a parameter, a return, an attribute) and in a
  conversion: `i8 i16 i32 i64 u8 u16 u32 u64` for integers, `w8 w16 w32 w64` for words. `integer` alone is `i64`, so D55 is
  unchanged for every program that names no width. A local takes its width from its first value, as D55 says of every full type.
- **A word has no sign.** Signed modular arithmetic is a pattern read two ways and is where C's undefined behaviour lives; a
  signed reading of a word is a conversion, written: `i32(wX)` refuses a pattern above 2^31-1, `i32wrap(wX)` reinterprets it.
- **X1 is then one line that reads as it runs**: `wHash = wHash * w32(16777619)`. The naive form cannot be wrong, because no
  mask is written and no double is involved.
- **X8**: `~wX` is a NOT at the word's width; `wX << 1` drops the bit that leaves it. No mask, ever.
- **X7**: `i32` traps where Rust's debug build and Zig's safe build trap; the checked build and the fast build trap alike
  (D41: both builds, the same bytes), so the release build does not become the wrapping one.
- **Literals**: hex `0xFF`, binary `0b1010`, digit groups `1_000_000`. A literal takes the width of where it lands, and a literal
  that does not fit is refused when compiling (`w8(256)`, `iCount = 0x1_0000_0000` into an `i32`).
- **Mixing** is refused: `iA + wB`, `w32 + w64`, `u32 + i32`. One widening is free, as D55 frees integer into decimal: a
  narrower integer into a wider integer of the same sign.
- **`n` (any number, parameters only, D55 (f))** admits integers of any width and not words: a word is not a quantity.

**Why a letter and not only a width.** The width is a fact about storage; the family is a fact about meaning, and the meaning
is what an agent gets wrong (X1: right in Zig, which spells `*%`, wrong in the surface, which spells `*`). Zig and Rust put the
wrap on the operator (`*%`, `wrapping_mul`); an agent must remember it at every site and a reader must see it at every site.
On the type, the site cannot be wrong, and the letter puts the type at the site.

## 5. Bytes and layouts (X3, X6)

- **`x` bytes has a length fixed when made, always.** It is written in place (`xBuf[i] = w8(0x41)`), read as a word
  (`xBuf[i]` is a `w8`), and never grows; an index past its end raises `INDEX_OUT_OF_RANGE` with the length. `bytes of 64`, as a
  full type, fixes the length when compiling, so the C target places it without a heap. A growing byte store is a `vector of
  w8`, and the two are converted, never confused.
- **A layout is a record whose shape is the bytes'**:

      DEFINE LAYOUT Header
        magic:    w32 big
        version:  w16 little
        pad 2
        size:     u64 little

  Every field has a width and an order; padding is written, never inferred; there is no "native" order (X6's `int2bytes` gave
  the machine's and called it a number). `Header.size` is 16, known when compiling. `xBuf.read(Header, 0)` gives an `r`
  record, `xBuf.write(Header, 0, rH)` writes one, both bounds-checked against the length.
- **Bytes from a door stay `unjudged`** (D55 T7, (h)). Reading a layout out of them is allowed -- every bit pattern is a valid
  word -- and the record's fields are words or integers, never a sentence. A field that must hold one of N values (an enum) is
  read as a word and judged by a comparison the program writes.

## 6. References and regions (X4, X5): one rule, second-class

Haro has no pointer arithmetic and no lifetime annotations. One rule covers every value that must not outlive its place:

**A second-class value is passed down, never stored, returned or captured.** The compiler checks it at the three sites by name;
no borrow checker, no lifetime variable, nothing an agent writes beyond the word.

- **`ref`, for X5.** A parameter declared `ref iN` reads and writes its caller's slot, and the call writes `ref` too:
  `Inc(ref iCount)`. Written at both ends because a reader of the call must see that the call writes (C#'s rule). A `ref` is
  second-class: `$g = iN` inside the function stores the value, never the slot. Several results are a record, not several refs;
  `ref` is for the C door's out-parameters and for in-place updates.
- **`region`, for X4.** The memory regime is the VM's reference counting by default, and in the system profile a managed
  value is made only inside a region:

      using hArena = region(64 kb)
          vRows = ...          # made in hArena
      done                     # hArena released: every value made in it freed at once

  v0.38's `using` already calls `Release` on every exit, `raise` and `return` included; the region is a value with a
  Release. A value made in a region is second-class to its block: assigned to a name declared outside it, returned past
  `done`, or stored in an attribute, it is refused when compiling. A region past its size raises `REGION_FULL` with the size.
  An arena is the only allocator the first rung offers; a pool or a free-list waits for a customer.
- **Scoped door handles** (section 7) are second-class under the same rule. The paper this design answers (section 7) uses the
  same device for the same reason: a capability that cannot escape its block is one the type system can count.

Not proposed: a manual `free`, a pointer, an address, a cast between a reference and an integer. The C door crosses them
(section 8); Haro code does not hold them.

## 7. Capabilities as types (principle 12.4): `uses`, `personal`, `total`, `budget`

**The paper.** Odersky, Zhao, Xu, Bracevac and Pham, *Tracking Capabilities for Safer Agents*, arXiv 2603.00991 (v1 2026-03-01,
v2 2026-05-07; ACM CAIS '26 as *Securing Agents With Tracked Capabilities*), EPFL; read at the abstract and its sections 1 to 3.5.
An agent writes code in a capability-safe language -- Scala 3 with capture checking -- instead of calling tools; a type carries
the set of capabilities its values can reach, a pure type reaches none, and code that uses a capability its type does not name
is refused before it runs. It claims capability safety (not forged, not forgotten), completeness (every effect goes through a
capability) and local purity (a classified value is mapped only by pure functions), against a model treated as byzantine; it
names timing channels and external commands as outside what it stops.

**What Haro takes, and in its own words:**

- **`uses [door, ...]` on a function**, from D51's nine. A function with no `uses` is pure: it reaches no door, directly or
  through what it calls, and the compiler checks the closure of its calls. A unit's `NEEDS` bounds every `uses` in it (D51's
  second altitude, the program half). A native is mapped to its door by W7's map; until the map lands, the profile refuses a
  native that is not in the map, rather than guessing.
- **A door's handle is `h`, `handle of network`**, obtained only inside `using` and second-class to its block (section 6): the
  paper's scoped capability, which D55 T7 already names.
- **`personal`, the dual of `unjudged`.** `unjudged` guards what comes IN (integrity: may not run, become a sentence, or direct a
  door); `personal` guards what goes OUT (confidentiality). A value read from a seat the CONSTITUTION marks `PERSONAL` (D35,
  D37) carries the mark; it flows through pure functions and keeps the mark, and it may be a door's argument only where the
  door's sentence declares `SAFEGUARDS` for it (D37). This is the paper's local purity, with the seat that marks a datum
  personal being the one Haro already has.
- **`total` on a function** (principle 11, brought to the computing altitude where declared): no `while`, a `for` only over a
  collection or a range whose end is known before the loop starts, no recursion, and calls only to total functions. A total
  function terminates; the court that calls it may say so in its narration.
- **`budget`**: a ceiling on steps and memory for a call, raised as `BUDGET_EXCEEDED` when crossed, checked by the VM at its
  back edges. Its FORM is the constitution desk's (W6, COMPASS-SYSLANG-06); the grain reads that form and does not spell its
  own. A total function whose loop ends are literals has a budget the compiler can bound; the bound is reported, never trusted
  in place of the check.

**What the type system does not stop, said as the paper says it:** timing, and what an external program does once the
`process` door runs it. Harobanda's PID 1 enforces the doors at the machine (D51); Haro proves what was declared.

## 8. The C door

**The one foreign door, under `uses [dynamic_load]`:**

    DEFINE FOREIGN zlib FROM "z"
      def crc32(wCrc: w32, xData: bytes, iLen: u32) -> w32
      def deflateInit(ref rStream: z_stream, iLevel: i32) -> i32

- **What crosses, and how**: integers and words of a width, floats, booleans (as C's `bool`) by value; `bytes` borrowed for the
  call, never kept by C past it; a layout record by value or by `ref` (an out-parameter is a `ref`); a handle opaque, as ABI v1's.
  A text crosses only as `bytes`, its encoding and terminator written by the program. Nothing managed crosses.
- **Declared, not discovered**: a foreign function is called only as declared; a signature that disagrees with the library is
  the C compiler's refusal at SG3, and the VM's ABI check at the register target.
- **The engine's ABI v1 is not touched.** Softanza's engine keeps its four-thing protocol; the C door is for the grain's code
  and the 21 C trees the engine vendors, which speak C (the Compass's reason for C first).

## 9. The amendment of D55 -- HARO-TYPES-SYSTEM-01

Proposed as additions to TYPES.md; D55's eight rulings stand as they are.

| | adds | to |
|---|---|---|
| T4a | `integer` takes a width (`i8` to `i64`, `u8` to `u64`); `integer` alone is `i64`; overflow raises at every width | T4 |
| T4b | `word`, letter `w`, `w8` to `w64`: unsigned, wraps by definition, the only type the bit operators take | T4, section 4's letters (sixteen) |
| T4c | hex, binary and grouped literals, taking the width of where they land, refused when they do not fit | T4 |
| T6a | `bytes` has a length fixed when made; `bytes of N` fixes it when compiling; an element is a `w8` | T6 (and `x`, section 4) |
| T6b | a layout is a record declared with widths, orders and padding, read from and written to bytes | T6 |
| T8 | second-class values -- `ref`, a region's values, a scoped handle -- pass down and are never stored, returned or captured | new |
| T9 | `uses [door]` on a function, pure without it, the closure checked; `personal` as the dual of `unjudged`; `total` | T7 |

The letters become sixteen: `b i d f n t x k v m r o e h s w`. `w` is free in D55, and a lowercase `w` before a capital is never
read as the alphabet's W, which is a capital and a declared language, not a name.

## 10. Decisions for the author -- one row, HARO-TYPES-SYSTEM-01

| | decision | the desk recommends |
|---|---|---|
| (a) | the seats are Haro's in every `.haro` file; the system grain is a declared profile that only refuses (section 3) | yes |
| (b) | two whole-number families, `i` (traps) and `w` (wraps, bit operators), widths in the full type | yes; the alternative is the wrap on the operator, as Zig and Rust do (section 4, why not) |
| (c) | `bytes` fixed in length, `bytes of N`; layouts declared with order and padding, no native order | yes |
| (d) | one second-class rule for `ref`, regions and scoped handles; `ref` written at the call too | yes |
| (e) | the memory regime: reference counting by default, regions in the system profile, no manual free | yes |
| (f) | `uses` on functions, pure by default, the closure checked; a native outside W7's map refused in the profile until it lands | yes |
| (g) | `personal` as `unjudged`'s dual, reaching a door only under `SAFEGUARDS` | yes, built with the constitution desk |
| (h) | `total` on functions; `budget` in W6's form, checked at run time | yes; the form is W6's |
| (i) | the C door as `DEFINE FOREIGN`, under `uses [dynamic_load]`; ABI v1 untouched | yes |

## 11. The rungs, after D55's

Each one fixtures first, both builds byte for byte, every protection planted. Versions are taken when built; the order puts
the seats SG0 named before the governance seats, because SG2 needs the first and the second need W6 and W7.

1. **words and widths** (T4a-c, X1 X2 X7 X8), after D55's number rung (T4): the first acceptance set is SG0's S03, S08, S22, S23,
   S24, S25 and S27 written WITHOUT their workarounds, judged on both builds against the references' outputs.
2. **bytes and layouts** (T6a-b, X3 X6).
3. **second-class values and regions** (T8, X4 X5), with S28 written with a `ref`.
4. **the profile** (section 3) and **SG0b**, the harder set the Compass deferred until the seats exist (SG0-HARD-SET-01), in the
   grain's spelling against Zig on tasks that need the seats.
5. **`uses` and `total`** (T9 without `personal`), the program half of D51 when W7's map lands.
6. **the C door** (section 8), and then SG2: numtheory on the register target, then as C through `zig cc` (COMPASS-SYSLANG-03).
7. **`personal` and `budget`**, with the constitution desk (W6).

Owed to other desks, named so nobody waits on this one: the decoder's depth limit (statements four deep, subscripts below the
first level) is the engine's, stzlib-intelligence's; Haro's GBNF carrying the bit operators, hex, `finally` and `catch e` is this
desk's, with rung 1; W7's map of natives to doors and W6's budget form are the constitution desk's.

## 12. Measurements owed before rung 1

1. **Haro's own code and stzlib** (one sweep each, alone): how many sites mask with `& 0xFF...`, compare against `2147483647`, or
   build bytes with `int2bytes` -- the workarounds the seats retire, counted, so the rung can say what it moved.
2. **The cost of a width check** on integer arithmetic in the courts' hot loops (an add with an overflow test against the
   VM's add today), minima over repetitions, on a quiet machine.
3. **The Rule A trap on today's VM -- MEASURED 2026-11-07** (`study/sg1/rulea.haro`, haro b8233de: the top level writes
   `nums = [3, 1, 2]`, a function reads `$nums`). The run raises `Error (R24) : Using uninitialized variable: $nums` at line 6;
   `haro check` warns `haro/uninitialized-variable`, says no main scope assigns it as a global, and gives as "the usual cause"
   a typo under case-insensitive identifiers (F-18) -- which v0.42 ended in a `.haro` file. **Neither names the `nums` of line 1.**
   So rung 1 owes a fixture: in a `.haro` file the refusal of `$nums` names `nums` at line 1 and its `todo` says to pass it as a
   parameter or declare it `$nums`; and the checker's F-18 sentence is not said of a `.haro` file.
