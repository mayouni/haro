# Haro -- a grammar sketch

**Illustrative, not normative.** 2026-09-26, with `haro/CHARTER.md`. Every program below
is what the charter's rules would make an agent write; none of it parses anywhere today.
The normative grammar is the single source file the charter's section 4 describes, and
it does not exist until the author ratifies the charter. Spellings marked *(author)* are
choices for ratification; the rules behind them are the charter's.

---

## 1. The one-spelling table (Rule C, applied)

| construct | Haro spelling *(author)* | Ring spellings retired |
|---|---|---|
| definition | `def` | `func` |
| block close | `end` | `ok`, `next`, `off`, `done` |
| else-if | `but` | `elseif` |
| logic | `and`, `or`, `not` | `&&`, `\|\|`, `!` |
| print | `?` | `see`, `put` |
| comment | `#` to end of line | `//`, `/* */` |
| string | `"..."` with escapes `\n \t \r \" \\` | `'...'`, no escapes |
| symbol | `:Name` keeps its text | lowercased atom |
| pair | `:Name = value` is a named argument in a call, a pair in a list literal | a two-element list in both |
| range | `a .. b` | `a : b` |
| equality | `=` compares; `is` is identity | `=` converting |
| append | `add(aL, x)` or `aL.Add(x)` | `aL + x` in place |

Keywords, closed and reserved in every casing: `def end class from new if but else for
in to step while switch on other try catch return break continue and or not true false
nil is const global use forms profile import`. *(author: the exact set.)*

## 2. The smallest program (the spike's target)

```
# twice.haro -- one definition with its intent, one typed parameter, one call

def Twice(n: integer) -> integer  is "doubles a number"
    return n * 2
end

? Twice(21)
```

Its refused twin, `twice_refused.haro`:

```
def Twice(n: integer) -> integer  is "doubles a number"
    return n * 2
end

true = 0            # CONST_ASSIGN, exit 1, the record in CHARTER.md section 5
? Twice(21)
```

The intent clause is trailing prose, never compared (Commons 3.8). A definition without
it:

```
def Twice(n: integer) -> integer
    return n * 2
end
```

```
haro twice.haro:1:1 MISSING_INTENT: Twice has no intent clause.
  why:  a definition that cannot say what it is for cannot be asked about it, and the
        library's Ask/HowTo read this clause, not a comment (charter 2.5).
  todo: edit: append ` is "<one sentence: what Twice does>"` to line 1
```

## 3. Names: three sigils, no upward resolution

```
$nCalls = 0                          # a global: declared at the top level, spelled $ everywhere
const $NL = "\n"                     # a constant: CONST_ASSIGN if written again

class Counter
    @n = 0                           # an attribute, always @
    def Bump()  is "adds one to the count, in place"
        @n++                         # ++ is a statement, never a value (F-64)
        $nCalls++
    end
    def Bumped() -> Counter  is "a copy with one more"
        o = This.Copy()              # o is a local; nothing above can see it
        o.Bump()
        return o
    end
end
```

What is refused, and how:

```
def Reset()  is "starts the count again"
    n = 0                            # UNKNOWN_NAME if meant @n; a local otherwise -- but:
    $nCalls = 0                      # fine, the global
    nCalls = 0                       # SHADOWS_GLOBAL: nCalls hides $nCalls; todo: write $nCalls
end
```

A lambda captures explicitly, so the C-14 question never arises:

```
nBase = 10
f = def (x: integer) use nBase  is "adds the base"
    return x + nBase
end
? f(32)                              # 42; and nBase = 100 afterwards does not change f
```

## 4. Forms as grammar

```
class stzString
    @cContent: string

    def Remove(pcSub: string) forms [Many, CS, Q]  is "deletes every occurrence of the substring, in place"
        @cContent = StzReplace(@cContent, pcSub, "")
    end
end
```

From that one definition the compiler derives and checks:

| generated | rule it is checked against |
|---|---|
| `RemoveMany(pacSubs: list)` | plural: the list form of the same verb |
| `RemoveCS(pcSub, pCaseSensitive: boolean)` | suffix declares the trailing parameter |
| `RemoveManyCS(pacSubs, pCaseSensitive)` | suffix order is parameter order |
| `RemoveQ`, `RemoveManyQ`, `RemoveCSQ`, `RemoveManyCSQ` | returns `This`; a `Q` body returning anything else is refused |
| `Removed(pcSub) -> string` | passive: returns a value, may not write `@cContent` |

A hand-written member that disagrees:

```
    def RemoveQ(pcSub: string)  is "..."
        return @cContent                 # Q_RETURNS_VALUE: a Q form returns the receiver
    end
```

```
haro stzString.haro:14:9 Q_RETURNS_VALUE: RemoveQ returns a string; a Q form returns
  its receiver.
  why:  Q means "returns the object so calls can chain" (the forms document, line 80);
        the house rule q-returns-object is a compile rule in Haro (charter 2.7).
  todo: edit: replace `return @cContent` with `return This`; or rename to Removed()
        if a value was meant
```

## 5. Named arguments (decision D4, as recommended)

```
def FindNext(pcSub: string, :StartingAt = 1, :CaseSensitive = true) -> integer  is "the position of the next occurrence"
    ...
end

n = o.FindNext("x", :StartingAt = 5)       # bound by name at compile time
n = o.FindNext("x", :StartingAt = 5, :Foo = 1)
```

```
haro find.haro:9:33 UNKNOWN_NAMED_ARGUMENT: FindNext has no parameter Foo.
  why:  named arguments are part of the call and resolved at compile time; on Ring
        `:Foo = 1` was a two-element list the callee had to inspect at run time
        (F-59; Ring, Judged by the Record, 5.2).
  todo: the parameters are pcSub, StartingAt, CaseSensitive; remove :Foo or pick one
```

Under grain 3 of the GBNF, `:Foo` is not emittable at that position at all.

## 6. Declared languages as typed literals

```
aBig = aNums.FindAllW( w"{ @item > 5 and @i < 10 }" )     # a W literal: parsed at compile time
oLx  = listex"[@N1-3, @S]"                                # a listex literal: its grammar, its court
```

A malformed W is a compile refusal, not an empty answer at the call:

```
haro filter.haro:3:22 W_SYNTAX: `@item >` is not a W expression; an operand is missing.
  why:  W is a closed expression language compiled by the engine; on Ring++ it refused
        at the call ("refused, not answered empty"), and in Haro it refuses at compile
        time because the literal is typed (charter 6.1).
  todo: edit: replace `@item >` with `@item > <number>`
```

## 7. The error, as a value

```
try
    o = new stzTable(paTable)
catch e
    ? e.Code()                         # "BAD_PARAMETER"
    ? e.Todo()                         # the instruction, as text
    ? e.Span().Line()
end
```

No `cCatchError`; no process-wide last error; `e` is the handler's own.

## 8. A GBNF fragment for the spike subset

Illustrative of the dialect `gbnf_machine.zig` accepts (the generated file, not
hand-written):

```
root      ::= (defn | stmt | ws)*
defn      ::= "def" ws ident "(" params? ")" (ws "->" ws type)? ws "is" ws string nl
              stmt* "end" nl
params    ::= param ("," ws param)*
param     ::= ident ":" ws type
type      ::= "integer" | "float" | "string" | "boolean" | "list" | ident
stmt      ::= ws* ("return" ws expr | "?" ws expr | ident ws "=" ws expr) nl
expr      ::= term ((ws ("*" | "+" | "-" | "/") ws) term)*
term      ::= integer | string | "true" | "false" | "nil" | call | ident
call      ::= ident "(" (expr ("," ws expr)*)? ")"
ident     ::= [A-Za-z_] [A-Za-z0-9_]*
integer   ::= [0-9]+
string    ::= "\"" ( [^"\\] | "\\" ["\\ntr] )* "\""
ws        ::= [ \t]*
nl        ::= "\n" | "\r\n"
```

Grain 3 for a hole inside `Twice`'s body rewrites `ident` as:

```
ident     ::= "n" | "Twice"
call      ::= "Twice" "(" expr ")"
```

so that a reference to a name not in scope, or a call with two arguments, is not a
sentence the decoder can produce.

## 9. Two things the sketch does not show, on purpose

- **The class-body rules** (`from`, `super`, operators, `obj { }`) -- carried from Ring
  as the charter says, and unchanged enough not to need a sketch.
- **The profile clause** (`profile softanza`) and the migration profile's `inferred`
  intents -- decision D3 and H-6; their spelling waits on the ruling.

---

## v0.2 -- the declaring and declared altitudes, sketched

**2026-10-01.** Everything above is the computing altitude (v0.1). What follows sketches the
two altitudes the author's ruling added. The declaring altitude's form is stzu v0.1's,
verbatim, so the first block below is real and judged today; the seats marked *(v0.2)* are
this charter's proposals and parse nowhere yet.

### 10. A language declared, in a dozen lines (the real form, stzu v0.1)

```
-- tontine.stzu -- a savings circle, declared as a language

DEFINE LANGUAGE tontine AS (
  VERSION "0.1", GRAMMAR "0.1",
  COURT "tontine/fixtures.json",
  EXTENSION ".tontine"
) RATIONALE "A circle of members who deposit each round and take turns receiving the pot"

DEFINE DECLARATION member AS (
  VERB "MEMBER", SEATS [name: text, joined: text]
) RATIONALE "One person in the circle"

DEFINE EXPRESSION amount_rule AS (
  OPERATORS [cmp, and], OPERANDS [number, var], VARIABLES [amount]
) RATIONALE "A bounded condition on a deposit; no call, no loop, no host"

DEFINE DECLARATION norm AS (
  VERB "NORM", SEATS [rule: amount_rule, message: text]
) RATIONALE "A rule the court enforces, with the sentence it speaks when it refuses"

DEFINE REFUSAL unknown_verb AS (
  MESSAGE "The tontine speaks MEMBER, DEPOSIT, NORM and ROUND; nothing else."
) RATIONALE "Destruction is not forbidden; it is unparseable"
```

The meta-court checks closure at every layer, one `LANGUAGE` first, one namespace, seat
types resolving, required clauses and menu coherence [R, stzu GRAMMAR.md, "The checks"].

### 11. The seats v0.2 adds *(proposed; parse nowhere today)*

```
DEFINE WORLD tontine AS (
  ENTITIES [member, deposit, round],
  RELATIONS [deposit belongs_to member, deposit in round],
  CONSTRAINTS [round has_at_least 2 member]
) RATIONALE "The ontology, versioned beside the grammar, shipped in the binary; never a store"

DEFINE ASK tontine AS (
  QUERY "q",                            -- the Q letter, the closed query grammar
  LANGUAGES [fr, ar, ha, en]            -- the human languages the natural door speaks
) RATIONALE "NL asks, never declares; the engine compiles to q, never to host code"

DEFINE NARRATE tontine AS (
  VOICE "stzn", SCENES [round_opened, deposit_taken, payout_made]
) RATIONALE "Every run narrates itself; the narration is the court's voice"

DEFINE REFINE tontine AS (
  POINTS [norm.rule: policy, deposit.amount: parameter],
  FLOOR  [norm.rule: trusted]
) RATIONALE "Which declared things may be refined, by whom; a policy point refuses model-composed proposals by construction"
```

### 12. A sentence of the declared language, and its refusal

```
-- circle.tontine -- the maker's own world, in its own words

MEMBER amina AS (name: "Amina", joined: "2026-10")
MEMBER moussa AS (name: "Moussa", joined: "2026-10")
NORM positive_deposit AS (
  rule: amount > 0,
  message: "A deposit must bring something to the circle"
)
DEPOSIT d1 AS (member: amina, round: 1, amount: 0)
```

```
tontine (line 8): A deposit must bring something to the circle
  code     NORM_VIOLATED            severity error        language tontine
  cites    norm:positive_deposit
  why      the norm's rule is `amount > 0` and the deposit brings 0
  todo     set amount to a value above 0, or withdraw the deposit
```

The refusal is the maker's own sentence, declared in the `NORM`; the envelope is C2's; the
`language` is `tontine`, not `haro`.

### 13. A refinement, as a sentence *(proposed)*

```
REFINE deposit.d1.amount AS (
  from: 0, to: 5000,
  author: "aicha", posture: llm,
  reason: "Amina's first deposit, recorded from the ledger photo"
) RATIONALE "A parameter point; bounded by the norm; reversible"
```

```
admitted: deposit.d1.amount 0 -> 5000 [llm] (structural + constraint + derivation +
          governance + trust passed); inverse recorded; revert with REVERT r-0001
```

And the same sentence against a policy point:

```
REFINE norm.positive_deposit.rule AS (from: "amount > 0", to: "amount >= 0",
  author: "aicha", posture: llm, reason: "allow a zero placeholder")
```

```
tontine (line 1): trust: posture :llm below the required floor for 'norm.positive_deposit'
  code     TRUST_FLOOR               severity error
  why      a policy point refuses model-composed proposals by construction (REFINE ... FLOOR)
  todo     a trusted actor may propose it; or propose a parameter change instead
```

### 14. The machine, the real customer

`harobanda/declarative/machine/machine.stzu` declares the machine language in 79 lines; a
machine is then one sentence of it:

```
DEFINE SERVICE kds AS (
  RUN ["/stzr", "/app/kds.luau"],
  RESTART always,
  READY "/run/kds.ready"
) RATIONALE "The kitchen display world; it says when it is serving"
```

Under Haro the `RUN` seat names `/rnx` and a Haro world; a change to `RESTART` is a
refinement judged by the gate and tried in the second slot before it is committed -- which is
what the two boot slots already do [R, 07-SYSTEM]. The spike of the charter's section 10 is
exactly this file, forged on `rnx`.
