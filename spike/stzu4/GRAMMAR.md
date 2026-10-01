# stzu v0.4 -- a language over a language: the SENTENCE, the VIEW and the paths

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.4 is the declaring altitude of Haro grown by what a language
declared OVER another language needs. The corpus is harobanda's fleet file: every
`MEMBER` names a machine FILE that the fleet court reads, judges with the machine court,
and reads through for the rules no single machine can fail -- one link, one server; one
address, one machine; a promise held against the device that claims it. The charter's
section 3 says composition is the normal way to declare a language; this is that claim
with a number on it (`haro/SPIKE.md`, the fourth rung). v0.4 refuses nothing v0.3
accepted (fixture A7 is v0.3's A5, unchanged).

## What is new, and where it comes from

| kind or clause | declares | the lesson it carries |
|---|---|---|
| `SENTENCE` | `OF "other.stzu"`, optional `MESSAGE` and `REFUSED` | a seat type: the value names a FILE of another declared language, read beside the file being judged and judged by that language's own court; the file that cannot be read speaks `MESSAGE` (FR13), the file its court refuses speaks `REFUSED` with `{why}` and `{line}` (FR12: "MEMBER cassee is refused: ... (line 1 of cassee.machine)"). The named declaration is read beside the `.stzu` that names it and judged by the meta-court first (R2, R3); a sentence is a scalar seat's type, never a list's (R4) |
| a PATH | `seg.seg.seg` in a condition | a place is read along a path: a seat, a reference's declaration, a SENTENCE's one declaration of a ONE kind (`declaration.box`, its name as a value), a seat of it (`declaration.thing.kind`), or the SET of a kind inside it (`declaration.part`, `server.declaration.peer`). The head is `self`, `this`, a VIEW, a seat, a ONE kind or a kind; a step is a seat, a VIEW on that declaration's kind, or a kind inside a sentence (R5, R13) |
| `VIEW` | `ON decl`, `ONE "path"`, optional `NAMED "value or path"`, `WHERE "cond"` | a derived place by a closed rule: the one declaration of a set along a path, narrowed by a name and a condition. `ON member, ONE "declaration.network", NAMED "fleet.link"` is the member's network on the fleet's link; with no `ON`, `ONE "member", WHERE "..."` is a place of the whole sentence, the first member that serves. A view reads like a reference seat (`link_network.address`), as a step (`this.link_network.address`), and `self is VIEW` asks whether this declaration is it (R6, R7, R8, R10) |
| `some`/`all` over a path, `earlier` | `some server.declaration.peer where ...`, `earlier member where ...` | a quantifier runs over any path that ends at a set; `earlier` runs over the declarations of a kind before this one, so the LATER of two is refused and `{other}` names the earlier (FR9, FR25). `named` takes a value or a place. Inside a quantifier over ANOTHER language's declarations, a kind or a whole-sentence view of the ON declaration's language is still in reach (`fleet.link` from a peer); a seat of the ON declaration is `this.SEAT` (R9, R16) |
| a place on the right of `=` | `key = this.key`, `declaration.box = this.declaration.box` | a comparison takes a place on either side; a bare word on the right is still a value, a dotted name or `this`/`self` a place -- `member.key = self.key`, never `= key` (R14, and the fleet's first FR23) |
| `FOLD case` on a FORMAT | `SHAPE hex64, FOLD case` | a format whose values compare case-blind, read folded at the court's parse: one key is one key however it is spelled (FR26, FR5 corrected) |
| `MESSAGES` for a required seat | `through: "RETIREMENT {name} names no THROUGH: ..."` | a declaration's own words for a required seat that is absent, as for a reference that resolves to nothing (FR22; R12) |
| `hex64`, `hex64_lower` | shapes | an ed25519 public key as a device publishes it; a journal head exactly as the journal wrote it (FR6, FR20, FR21) |

## Grammar (EBNF), the v0.3 text with these additions

```
kind        = ... v0.3's twelve ... | "SENTENCE" | "VIEW" ;
                SENTENCE: OF STRING, MESSAGE STRING, REFUSED STRING
                VIEW:     ON IDENT, ONE STRING, NAMED STRING, WHERE STRING
                FORMAT:   SHAPE IDENT, FOLD IDENT, MESSAGE STRING
```

The court of a language that declares a SENTENCE carries the named language's whole
record beside its own -- kinds, menus, formats, unions, constraints, world, views,
sentences, recursively -- and judges a sentence seat's file by switching to that record
and back. The forge emits one court for the composition; nothing is generated twice.

## The condition language, grown

```
cond   = term { ("and" | "or") term } ;
term   = [ "not" ] atom ;
atom   = "(" cond ")" | "exists" decl
       | ("some" | "all" | "earlier") path [ "named" (value | path) ] [ "where" cond ]
       | path "=" (value | path) | path "!=" (value | path) | path ">" number | path "<" number
       | path "present" | path "absent" | path "contains" value
       | path "empty" | path "nonempty" | path "unique" | path "distinct"
       | path ("within" | "host_of" | "under" | "covers") (path | value)
       | path "cyclic" | path "matches" format
       | "self" "is" view ;
path   = seg { "." seg } ;   seg = IDENT | "self" | "this" ;
```

**Two names, one meaning each.** A VIEW's name is not a seat of its ON declaration (R8).
Where a seat and a kind share a name (a RETIREMENT's `member` and the kind `member`), a
quantifier reads the kind, since it wants a set, and a path reads the seat. `present` and
`absent` on a seat of this declaration ask whether the clause is WRITTEN -- a list of
references is present when written, empty or unresolved -- and on a view or a kind whether
it resolves. `unique`, `empty`, `nonempty`, `distinct` and `contains` read the list as
written, so a list of references reads its names whether or not they resolve.

**Each path is total.** A path walks seats and kinds of finite sentences; a view walks one
set once; `earlier` walks a prefix of the pool; `is` compares two declarations. A reference
that resolves to nothing still raises the "says nothing" rule of v0.3 and the reference's
own refusal speaks; a view or a kind that resolves to nothing is simply absent.

## The refusal channel

Unchanged: `<language> (line N): message`. A SENTENCE seat's file that its court refuses is
refused WITH the declaration that names it, in the sentence's `REFUSED` words -- "line 3"
in a file the reader did not open is not an answer (harb's own rule, FR12).

## What v0.4 still cannot say, named

The acts of a language that are not its grammar: the fleet's roll, its `verify` of a signed
record under a member's key, and the fingerprint beside each member. A VIEW's `WHERE` reads
the views declared before it, never after. The meta-court judges the named language in
full on every read of the declaration that names it; a court for ten nested languages would
pay ten times, and nothing caches it.
