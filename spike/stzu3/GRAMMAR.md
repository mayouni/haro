# stzu v0.3 -- a seat of two shapes, a reference's own words, and a condition that reads across

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.3 is the declaring altitude of Haro grown by what the machine
language's 25 remaining fixtures could not say under v0.2 (`haro/SPIKE.md`, the second
rung): a seat whose value has one of two shapes, a reference seat's own refusal, and a
condition that reads THROUGH a reference, quantifies over a kind, and tests a relation
between two values. v0.3 refuses nothing v0.2 accepted (fixture A7 is v0.2's A7, unchanged).

## What is new, and where it comes from

| kind or clause | declares | the lesson it carries |
|---|---|---|
| `UNION` | `OF [a, b, [c]]`, optional `MESSAGE` | `ADDRESS dhcp` or `ADDRESS "10.0.0.2/8"`; `EGRESS none` or `EGRESS ["10.9.0.0/16"]` (HF-32, six fixtures). The alternatives are value types -- a MENU, a RANGE, a FORMAT, a primitive, or a list of a FORM -- told apart by the value's SHAPE: a word, a text, a number, a list. The court checks the value as the alternative its shape names and speaks that alternative's words (`'192.168.10.1' is not an address/prefix`, R38); a value of no alternative's shape is refused in the union's own MESSAGE. Two alternatives of one shape are refused at declaration time |
| `MESSAGES` on a DECLARATION | `[seat: "text", ...]` | what the court says when a reference seat's name resolves to nothing: `{name} needs {value}, which no declaration grants` (R17). It speaks for a reference seat only; a menu, a range or a format speaks for itself (HF-37) |
| `x.seat` in a condition | reads through a scalar reference seat of the declaration | `network.domain absent`, `network.address = dhcp` on a PEER (R71, the peer on a dhcp link); v0.2 read `x.seat` from a ONE kind only |
| `some` / `all` | `some KIND [named VALUE] [where COND]`, `all LISTSEAT [where COND]` | `not some capability named gpio` (R20); `not all needs where grant = yes` (R18, `{other}` names the one refused); `not some mount where (fs = ext4 or fs = vfat) and this.identity under at` (R65, R68). Inside the condition a bare seat is the quantified declaration's and `this.SEAT` is the ON declaration's; `self` is the quantified declaration's name |
| `within`, `host_of`, `under`, `covers`, `cyclic`, `matches` | the closed relations | an address within a prefix (R70); the prefix's own host address (R73); a path under a directory (R65); a list of prefixes covering one (R88-R90); a list of references returning to its declaration (R21); a text of a FORMAT's shape (R76, on `self`) |

## Grammar (EBNF), the v0.2 text with these additions

```
kind        = ... v0.2's eleven ... | "UNION" ;
value       = STRING | IDENT | NUMBER | name_list | seat_list | point_list
            | type_list | message_list ;
type_list   = "[" alt { "," alt } [ "," ] "]" ;          (OF; at least two)
alt         = IDENT | "[" IDENT "]" ;                     (a value type, or a list of a FORM)
message_list = "[" IDENT ":" STRING { "," IDENT ":" STRING } [ "," ] "]" ;
```

A UNION is a scalar seat's type, never a list seat's element. Its value shape is the shape
of the alternative the written value fits: a word for a MENU, `name`, `flag` or `ref`; a text
for a FORMAT or `text`; a number for a RANGE or `number`; a list of words or of texts for a
list of a FORM (by the FORM's first seat). The grammar the forge emits for a union seat is
the alternatives' shapes joined by `|`.

## The condition language (closed, total), grown

```
cond   = term { ("and" | "or") term } ;
term   = [ "not" ] atom ;
atom   = "(" cond ")"
       | "exists" decl
       | ("some" | "all") target [ "named" value ] [ "where" cond ]    (where runs to ")" or the end)
       | place "=" value | place "!=" value | place ">" number | place "<" number
       | place "present" | place "absent" | place "contains" value
       | place "empty" | place "nonempty" | place "unique" | place "distinct"
       | place ("within" | "host_of" | "under" | "covers") (place | value)
       | place "cyclic" | place "matches" format ;
place  = "self" | "this" "." seat | seat | x "." seat ;
target = decl | listseat ;
```

`x.seat` reads through `x` when `x` is a scalar reference seat of the current declaration
(the referenced declaration's `seat`), and from the one declaration of `x` when `x` is a ONE
kind; anything else is refused at declaration time (R9, R10). `some` and `all` quantify over
the declarations of a kind (`named` narrows them to one name) or over the declarations a
list seat of references names; a list is already named, so `named` goes with a kind (R13).
Inside the quantifier's `where`, a bare seat is the quantified declaration's (R16),
`this.seat` is the ON declaration's (R14, R15), and `self` is the quantified declaration's
name. `cyclic` follows a list seat of references to the declaration's own kind (R18);
`covers` takes a list seat, or a union seat one of whose shapes is a list (R19); `matches`
names a FORMAT (R11). The relations are a closed menu (R17).

**Each relation is total.** `within` and `host_of` parse two addresses; `under` compares a
path with a directory at a slash boundary (`/` keeps every absolute path); `covers` sweeps
the prefixes' ranges in order of their first address; `cyclic` follows references through
declarations of one kind with a visited list bounded by their number; `matches` is a
FORMAT's shape. None loops over anything but the sentence. **This is not the governed door
to the computing altitude**: it is the closed menu of FORMAT shapes grown by five relations,
each a fixed line of the court, named by the declaration and never written by it. The
computations v0.3 still cannot say are the ones no fixture asks for.

**A condition that reads through a reference that resolves to nothing says nothing**: the
constraint is skipped, and the reference's own refusal speaks (its MESSAGES, or the
language's `dangling_reference`).

## The court's order, changed

v0.2's court checked a declaration's typed values -- menus, ranges, formats AND references
-- before any CONSTRAINT. v0.3 checks the LOCAL types first (a menu, a range, a format, a
union), then the CONSTRAINTs in their declared order, then the references. A reference is
a fact about the whole sentence, as a constraint is, and the constraints are the maker's own
words about the whole sentence, so they speak first: `ledger SEES a mount and this machine
declares no MOUNT` (R82) is the constraint `sees_needs_a_mount`, and it now speaks before
the reference `data` is found to resolve to nothing. Two refusals that both hold compete
for the first word, and the declared order decides (HF-37): `hosted_boards` is declared
before `rpi4_is_aarch64`, so a hosted machine on a pico2 hears about the profile, as harb's
R35 expects, not about the architecture.

## The refusal channel

Unchanged: `stzu (line N): message`, and the forged court speaks the UNION's, the
MESSAGES', the MENU's, RANGE's, FORMAT's and CONSTRAINT's own text, with `{name}`, `{VERB}`,
`{value}`, `{other}`, `{seat}` and `{x.seat}` filled in -- `{x.seat}` now through a
reference seat too (`'{name}' cannot be a name on {network.domain}`).

## What v0.3 still cannot say, named

The fleet file's kinds (`FLEET`, `MEMBER`, `RETIREMENT`): they are another language's
declarations, refused by the machine court by name, and a court for the fleet language is
that language's own declaration. A reference seat's words for two causes (none declared,
no such one) are one MESSAGE; v0.3 closes the second cause by order, not by a second
message. A computation outside the five relations is unsayable, by design.
