# Haro v0.2 -- the WORLD and REFINE seats, and the types a court needs

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.2 is the declaring altitude of Haro grown by what the spike
measured on a real language (`haro/SPIKE.md`): of the machine language's 120 fixtures, 70
were rules its v0.1 declaration could not carry, and almost all of them are data -- a menu
of words, a range of numbers, a format of text, a reference that must resolve, a count, a
condition between two seats of one declaration. v0.2 declares those. It refuses nothing
v0.1 accepted (fixture A10 is the pinned machine declaration, unchanged).

## What is new, and where it comes from

| kind | declares | the lesson it carries |
|---|---|---|
| `MENU` | `WORDS [a, b, c]`, optional `MESSAGE` | `RESTART is never, always or on_failure` (R25); a closed word set is the most common rule a court has |
| `RANGE` | `MIN n`, `MAX n`, optional `MESSAGE` | `HEALTH 0 is not a window`, `CPU 2000 is more than sixteen cores' worth` (R54, R58); MIN above MAX is refused |
| `FORMAT` | `SHAPE` from the closed menu `absolute_path ipv4 cidr mac label domain`, optional `MESSAGE` | `AT is an absolute path, not 'data'` (R24); `HARDWARE is six pairs of hex` (R74) |
| a seat typed by a DECLARATION | a reference: `after: [service]`, `user: user?` | `kds comes AFTER 'network_up', which resolves to nothing` (R8); the declared `dangling_reference` REFUSAL speaks |
| `NAMES` on a DECLARATION | the declaration's names are drawn from a MENU | `'bluetooth' is not a capability: the menu is ...` (R16) |
| `CONSTRAINT` | `ON decl`, `WHEN "cond"`, optional `THEN "cond"`, `MESSAGE` | `PROFILE edge contradicts KERNEL linux` (R15); `uid 0 is the machine itself` (R47); refusal phrasing as declared data (G3) |
| `WORLD` | at most one; `ONE [decls]`, `FIRST decl` | `A machine file declares exactly one MACHINE`, `comes first` (R9, R10) |
| `REFINE` | at most one; `POINTS [decl.seat: kind, ...]`, `FLOOR [decl.seat: posture, ...]` | the charter's section 6: every refinable point declared with its kind (RFN's six, D6) and its trust floor; a target outside POINTS is not a point |

## Grammar (EBNF), the v0.1 text with these additions

```
kind        = "LANGUAGE" | "DECLARATION" | "FORM" | "EXPRESSION" | "REFUSAL"
            | "MENU" | "RANGE" | "FORMAT" | "CONSTRAINT" | "WORLD" | "REFINE" ;
value       = STRING | IDENT | NUMBER | name_list | seat_list | point_list ;
name_list   = "[" [ IDENT { "," IDENT } [ "," ] ] "]" ;
point_list  = "[" [ point { "," point } [ "," ] ] "]" ;
point       = IDENT "." IDENT ":" IDENT ;                 (declaration.seat: word)
seat_type   = IDENT | "[" IDENT "]" ;                     (unchanged; what IDENT may name has grown)
```

A seat's type resolves to a primitive (`name text number flag ref`), a FORM, an EXPRESSION,
a MENU (a word from its WORDS), a RANGE (a number within it), a FORMAT (a text of its shape)
or a DECLARATION (a reference to a declaration of that kind in the same sentence). A list
seat's element is a FORM (written in place, as v0.1), a DECLARATION (a list of references) or
a MENU (a list of words from the menu). A FORM cannot be referred to: it is written in place.

## The condition language (closed, total)

```
cond   = term { ("and" | "or") term } ;
term   = [ "not" ] atom ;
atom   = "(" cond ")"
       | seat "=" value | seat "!=" value
       | seat "present" | seat "absent"
       | seat "contains" value
       | seat "empty" | seat "nonempty"
       | seat "unique"                   (no other declaration of this kind carries the value)
       | seat "distinct"                 (a list seat holds no item twice)
       | "exists" decl                   (the sentence declares at least one of this kind)
       | decl "." seat "=" value         (the ONE declaration of that kind; decl must be in WORLD's ONE)
       | decl "." seat "!=" value ;
seat   = IDENT ;  decl = IDENT ;  value = IDENT | NUMBER | "'" text "'" ;
```

No arithmetic, no call, no loop: a condition is read, never run. `and` binds tighter than
`or`. A quoted value uses single quotes, because the condition sits inside a double-quoted
clause and the Commons has no escapes. The meta-court checks every seat and declaration a
condition names at declaration time (R10, R18, R19); the forged court evaluates it on every
declaration of the `ON` kind: when `WHEN` holds and `THEN` is absent, or `WHEN` holds and
`THEN` does not, the declaration is refused with `MESSAGE`.

## The refusal channel

Unchanged: `stzu (line N): message`. The forged court speaks the MENU's, RANGE's, FORMAT's
and CONSTRAINT's own MESSAGE, with the value that failed, so a court's phrasing is declared
beside its grammar and never authored per runtime.

## What v0.2 still cannot say, named

A computation: a cycle through AFTER, an address inside a subnet, a path inside a declared
mount, destinations covering every address. A default (libc by profile, board by
architecture): derivation, not judgement. A table (the consoles of each board) is sayable
as one CONSTRAINT per row, and the machine declaration below says it that way.
