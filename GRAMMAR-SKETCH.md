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
