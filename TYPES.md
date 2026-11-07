# TYPES.md -- Haro's types, redesigned

**A proposal of the desk, 2026-11-07 12:54, for the author's ruling. Nothing in it is built, and nothing in it is ruled until he rules it.**

The author's words in the session, 2026-11-07, quoted whole:

> "About the question of casesensitity in Haro, what do you advise? Keep in mind that we are making a language that is mainly executed by agents
> (so the ease of LLMs to work with it is esstiel) and humans only reading the surface they need to understand the goals and to mange the
> refinements"

> (on the desk's advice: case-exact names, a collision by case refused) "I agree with you! And willing to push it firther to requestion any ring
> dogmas, like the use of a for list (while it's actually inhertied from an C array type that does not exist in ring), c for string while it's c
> char, etc. I want Haro to be cprecise in using an expressive letter for each of it's exact types"

> "Ok but I noticed Haro holds no bolean type which was one of my strong critics to ring! Think of this widely and redeesign a good correct
> typesystem for Haro that is relevant to it's nature and core mission as a language of languages, and a governed languge of the agentic age"

The first two are rulings: **names in a `.haro` file are case-exact** (v0.42) and **each exact type has its own expressive letter**. The third is
the charge this memo answers.

---

## 1. What exists today, measured

**The VM has eight kinds of value and no boolean** (`vm/src/main.zig:587`): `nil, int, num, str, vec, obj, dll, cptr`. `true` is the integer 1,
`false` is 0, and an `if` takes any value: Ring's truthiness, carried through the fork.

**It coerces where Ring coerces.** An integer past 2^53 becomes a float with no word said (`main.zig:4164`, kept to match Ring's doubles); `"1" + 1`
is 2; `1 = "1"` is answered, not refused; `""` is Ring's NULL.

**The declared altitude has its own small type set**, separate from the VM's: the meta-court types a seat as `string`, `ident`, `number`, `flag`,
`namelist`, `pairlist`, `citelist`, `messagelist`, `pathlist`, `seatlist`, `pointlist`, `contextlist`, `rule`, `path` (`spike/haro_lib.haro:102-146`).
Two type systems, one language, no mapping between them.

**PRINCIPLES.md ruled much of this in v0.1 and none of it was built**: identifiers case-sensitive and a collision by case refused (2.1); keywords
reserved in every casing (2.2); `true`, `false` and `nil` literals of their own types, no predefined variable (1.1); a symbol its own type (2.4);
an error a value of type `error` (4.1); an `if` whose condition is not a boolean refused (4.3); typed parameters in the sketch,
`def Twice(n: integer) -> integer` (GRAMMAR-SKETCH 2), and "declared languages as typed literals" (GRAMMAR-SKETCH 6). The cut gave Haro its own VM
on 2026-11-02 (D39); the VM it took was Ring's semantics, and these rules have waited since.

**Haro's own code** (34 code files of `spike/`, strings and comments excluded): 971 prefixed names, 15,706 uses -- `a` 437 names (9,227 uses), `c`
330 (4,880), `n` 106 (1,047), `b` 75 (403; booleans that are integers), `t` 16 (122; tokens, not text), `v` 4, `x` 3.

**v0.41 diverges from principle 2.2, said here so it is not lost.** v0.41 reads `aNd` and `If` in a `.haro` file as names; 2.2 says a keyword is
reserved in every casing, which makes them refusals. Both close the misreading the author ruled against; 2.2's is the safer reading for an
agent, because no reader ever sees `If = 5` and has to know it is not the keyword. This memo proposes 2.2 (decision (e)), in v0.42 with the
collision rule it belongs to.

---

## 2. What a type system is for, in Haro

Haro is not a general-purpose language that happens to be governed. It is the language in which languages are declared and judged, written
mostly by agents and read by people who manage what the agents propose. Four jobs follow, and every rule below answers one of them.

1. **An agent writes it.** A type must be visible in the text where the name is used, not only where it was declared, and a grammar must be able
   to see it -- Haro decodes against its grammar (principle 3), and a constraint the grammar cannot see is one the decoder cannot enforce.
2. **A person reads it.** No hidden rule: what is written is what runs. No value means two things, no two names look alike.
3. **Languages are its values.** A declared language is a type; its court is that type's checker; a sentence the court accepted is a value of it.
4. **It is governed.** Nothing becomes a value by accident: no coercion, no truthiness, no outside text treated as judged, no effect without a door
   (principle 12), and every number says whether it is exact (principle 13).

---

## 3. The rules

### T1 -- Every value has exactly one type, and no value changes type unasked

No coercion, anywhere: `"1" + 1` is refused, `1 = "1"` is refused (comparing two types is a mistake, not `false`), an integer that overflows
raises `INTEGER_OVERFLOW` and never becomes a float. A change of type is a conversion, written, and a conversion is a judgement: `integer("12a")`
is refused by name with its `todo`, never 0.

### T2 -- A name's first letter is its type, and the compiler holds it to it

In a `.haro` file a name is a lowercase type letter followed by a capital: `tTitle`, `lNames`, `bReady`. The letter is checked wherever the
value's type is known when compiling, and at the assignment where it is known only when running (one tag comparison; its cost measured before
it is promised). `tTitle = 3` is `TYPE_LETTER` refused, naming the letter, the type and the value's type.

The letter carries the OUTER type. The full type -- what a list holds, what a map maps, which language a sentence is in -- is written once, at
the boundaries where a reader needs it: a parameter, a return, an attribute.

    def Total(lAmounts: list of decimal) -> decimal  is "the sum of the amounts"

A local takes its full type from its first value; the letter is its declaration.

**Why letters and not only annotations.** An annotation is seen where the name is declared; a letter is seen at every use, by the agent reading
the line it is about to extend and by the grammar. A context-free grammar cannot do type inference, but it can read a letter: `if` can be made to
accept only a `b` name, a comparison or a boolean literal, and an agent decoding against that grammar cannot write `if nCount` at all. Letters
turn part of type checking into grammar, which is where Haro wants its checks (principle 3).

### T3 -- Boolean is its own type, and only a boolean decides

`true` and `false` are the two values of `boolean`, literals, not variables (principle 1.1). A comparison answers a boolean. `if`, `while`, a
W condition, and `and`, `or`, `not` take booleans only: `if nCount`, `if tName`, `if lItems` are refused, with the comparison they meant as the
`todo` (`if nCount > 0`, `if tName != ""`, `if len(lItems) > 0`). A boolean is printed `true` or `false`. It is not a number: `true + 1` is refused.

### T4 -- Three kinds of number, each saying whether it is exact

| type | letter | what it is | exact |
|---|---|---|---|
| `integer` | `i` | a whole number, 64 bits, overflow raised | exact |
| `decimal` | `d` | a base-10 number, as money and measured quantities are written | exact, to its digits |
| `float` | `f` | binary floating point, for science, graphics, models | near, never exact |

Haro already has ledgers, banks and tontines among its worlds; in a governed language money is never a binary float. So **a literal with a point
is a `decimal`** (`0.1 + 0.2 = 0.3` is `true`), and a float is asked for (`0.1f`, or `float(x)`). Mixing is refused but for one widening:
an integer may join a decimal. `float` keeps its honest name: "real" is a promise binary floating point does not keep. Comparing two floats with
`=` is refused (principle 13: a claim of sameness names its class); `near(fA, fB, fTolerance)` says it.

### T5 -- Absence is not a value of every type

`none` belongs to no type. A function that may find nothing returns `maybe T`, and its caller resolves it where it lands:

    tTitle = oDoc.Title() else "untitled"
    oUser  = oTeam.Find(kId) else raise(...)

A `maybe` never travels in a local, so it needs no letter: a name's letter always names what it holds. Only a return and an attribute may be
declared `maybe`. Ring's NULL, which was the empty string, is gone with the global it lived in: `""` is a text of length 0 and nothing else.

### T6 -- Structure: list, map, record, object, error

| type | letter | what it is |
|---|---|---|
| `list of T` | `l` | ordered, of one element type |
| `map of K to V` | `m` | a key to a value, keys unique; what Softanza's pair lists were used for when the keys vary |
| `record` | `r` | named fields fixed when it is made; what pair lists were used for when the keys are known (`[:name = "x", :age = 3]`) |
| object | `o` | an instance of a class, its attributes declared with their types |
| `error` | `e` | the caught value of v0.37 made a type of its own: Message, Code, Span, Cause, and the C2 envelope (principle 4.1) |

A record's fields are checked when compiling: `rUser.nmae` is refused with `did you mean name`. The declared altitude already asks for this:
COMPASS-KERN-03's `FIELDS` and `RECORDS` (v0.34) are records a sentence names. When records land, v0.41's refusal of `:key = value`, whose
`todo` today says `[:key, value]`, says the record instead.

### T7 -- Judged types: what Haro is for

**A sentence of a declared language is a value of that language's type, and only its court makes one.**

    sRule = panel.judge(tText)            # a sentence of panel, or the court's refusal as an error
    sRule = panel"..."                    # a literal: judged when compiling (GRAMMAR-SKETCH 6)
    def Apply(sRule: sentence of panel)   # no unjudged text reaches Apply

A sentence carries its language, the language's version and the court's verdict with its cites. The letter is `s`. The meta-altitude's own
values -- a declaration, a kind, a seat -- are sentences of `haro` itself, the language of languages, judged by the meta-court.

**Text that came through a door is `unjudged` until a judge says otherwise.** What a model generated, a socket received, a file held or a person
typed may be stored, printed and passed to a judge, but it may not be run as code (v0.39's text-run-as-code, made a type rule), become a sentence
without its court, or be given to a door as its argument (a path, a host, a command). `unjudged` is a mark the checker follows through
assignments, not a letter: the text is still a `t`.

**A handle names its door.** `handle of file`, `handle of network`, letter `h`: a program whose language does not NEED a door (D51) cannot hold
a handle of it. This is D51's computing altitude, the half that waits for W7's map, expressed as a type.

---

## 4. The letters, whole

| letter | type | Softanza's letter, and why it changes |
|---|---|---|
| `b` | `boolean` | `b`, but it held an integer |
| `i` | `integer` | `n` |
| `d` | `decimal` | `n`, a double |
| `f` | `float` | `n` |
| `n` | any number: `integer`, `decimal` or `float` (decision (f)) | `n` |
| `t` | `text`: valid UTF-8 | `c`, C's char; Haro has no char type |
| `x` | `bytes`: raw, from a file or a socket | `c`, the same string type as text |
| `k` | `symbol`: an interned name, `:Name`, kept as written (v0.41) | none; symbols were strings |
| `l` | `list of T` | `a`, C's array; a Haro list grows and is not an array |
| `m` | `map of K to V` | `a`, a list of pairs |
| `r` | `record` | `a`, a list of pairs |
| `o` | an object | `o` |
| `e` | `error` | `c`, the message text |
| `h` | `handle of door` | `p`, a pointer |
| `s` | `sentence of L` | none |

Fifteen letters, one per type, none shared. A `$` or `@` stands before the letter as today (`$lCourtAsk`, `@tTitle`); the letter rule does not
change what a name is (principle 1.2).

---

## 5. The two altitudes, one type system

The meta-court's seat types become Haro types, so a declared language and a program speak of the same values:

| seat type today | Haro type |
|---|---|
| `string` | `text` |
| `ident`, `name` | `symbol` |
| `number` | `integer` or `decimal`, by the seat (decision (g)) |
| `flag` | `boolean` |
| `namelist` | `list of symbol` |
| `pairlist` | `map of symbol to symbol` |
| `citelist`, `messagelist`, `pathlist`, `pointlist`, `contextlist`, `seatlist` | `list of` the record each one is |
| `ref` (a seat typed by a declaration) | `sentence of` that kind |

The forge then emits, for every declared language, its type -- the court as the type's checker, the GBNF as the type's grammar -- and a program
that holds one of its sentences holds a typed value.

---

## 6. The `.ring` boundary

`.ring` files keep Ring's reading (D54): their values carry no letter and no checked type. A value crossing from `.ring` code into a `.haro`
name is checked at that binding: an integer 0 or 1 entering a `b` name becomes `false` or `true`, and
any other integer is refused; a Ring string entering a `t` name must be valid UTF-8; a list of pairs entering an `m` or `r` name is converted,
and refused if a key repeats or a field is missing. Softanza is not touched; how often its results cross each rule is measured before the rule
is built (section 8).

---

## 7. What it costs, and the risks

- **The VM.** New tags for `boolean`, `decimal`, `bytes`, `symbol`, `map`, `record`, `error`, and the `unjudged` mark. The engine boundary
  (`vm/src/native.zig`, the ABI to Softanza's engine) carries values both ways: a new tag there must be converted at the boundary, never passed
  through, or the engine sees what it cannot read.
- **Decimal arithmetic** is slower than a double. A literal with a point being decimal moves that cost onto every such literal; measured on the
  courts and on stzMax before (c) is ruled.
- **Haro's own code**: 971 names to re-letter, by a rename that asks the compiler what each name holds, not by text (437 `a`, 330 `c`, 106 `n`,
  75 `b` whose values become booleans, 16 `t` that are tokens and become records). Mechanical, verified like v0.41's migration: the same courts,
  the same bytes.
- **Agents trained on Softanza** write `cName` and `aList`. The refusal teaches them in one turn (`TYPE_LETTER: c is no letter in a .haro file;
  text is t: tName`), and the grammar can make the old letters unemittable.
- **What it does not decide**: whether text is indexed by byte, code point or grapheme; lists counted from 1 or 0; function values. Those are in
  the survey of Ring's habits, ruled with their costs beside them.

---

## 8. Measurements owed before the first rung of it

1. stzlib, one sweep: how often a Softanza result that a `.haro` program would bind is a 0/1 integer used as a boolean, a pair list with
   repeated keys, a string that is not UTF-8.
2. The courts and stzMax with every pointed literal a decimal: the cost, two figures, minima over repetitions.
3. Haro's own code: how many of its 437 `a` names are lists, maps and records, read from what the compiler binds to them.
4. The cost of the runtime letter check per assignment, on the courts' hot loops.

---

## 9. Decisions for the author

| | decision | the desk's recommendation | class |
|---|---|---|---|
| (a) | letters on every name, the full type written at parameters, returns and attributes | yes | judgement |
| (b) | the fifteen letters of section 4 | as written | naming |
| (c) | a literal with a point is a `decimal`; a float is asked for | yes, after measurement 2 | judgement |
| (d) | `none` belongs to no type; `maybe T` only on returns and attributes, resolved where it lands | yes | judgement |
| (e) | a keyword in another case is refused (principle 2.2), not a name as v0.41 reads it | yes, in v0.42 | judgement |
| (f) | `n` as "any number", or no letter that stands for more than one type | keep `n`, for parameters only | judgement |
| (g) | a seat typed `number` becomes `integer` or `decimal` by what it counts | by the seat, the meta-court refusing `number` | judgement |
| (h) | `unjudged` text: the three uses it may not have (run, sentence, door argument) | yes | judgement |

---

## 10. The rungs, in order

Each one fixtures first, both builds byte for byte, every protection planted, as every rung.

1. **v0.42 -- case-exact names** (ruled): a name spelled only as declared; two names differing only by case refused (`CASE_COLLISION`); a keyword
   in another case refused (e).
2. **v0.43 -- boolean, and no coercion** (T1, T3): `true`/`false` a type, conditions boolean only, comparisons across types refused, integer
   overflow raised.
3. **v0.44 -- the letters, checked** (T2), and Haro's own code re-lettered.
4. **v0.45 -- numbers** (T4): decimal and float apart, `near`.
5. **v0.46 -- absence** (T5): `maybe`, `else`.
6. **v0.47 -- map and record** (T6), and v0.41's `todo` pointing at them.
7. **v0.48 -- judged types** (T7): sentences as values, `unjudged`, handles by door, and the seat types of section 5.
