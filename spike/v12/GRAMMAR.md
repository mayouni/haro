# Haro v0.12 -- FORMS: the function-name grammar as data

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures
first, prose second). v0.12 is the declaring altitude of Haro grown by the charter's
section 3 row "`FORMS` inside a vocabulary: the function-name grammar of principle 7
declared as data for the computing altitude's families" -- and by nothing else. Principle 7
is ruled (H-7, `haro/PRINCIPLES.md` 7, seven points): the active and passive forms, `VerbQ`
returning the receiver and requiring `Verb`, suffixes naming parameters in order, `W` and
`X`, the plural and exceptional forms, a definition declaring the forms it offers with the
family generated from them, and the misspelled form, free-order parameters and the `FF`
clash refused as grammar. Its guard is spelled out there too: "a form fixture per rule; the
family generator's output pinned; the checker run over the Softanza base unit printing
members that disagree". v0.12 refuses nothing v0.11 accepted (fixture A2 is v0.11's A1).

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `FORMS`, at most one per language | the vocabulary's own spelling rule, once | a vocabulary spells its families one way; the forms document is one document (R4) |
| `FLUENT "Q"` | the suffix of the form that returns the receiver, last of the suffixes | `Q("rixxnxg").RemoveQ("x").ReplaceQ(...).UppercaseQ()` -- the chain of actions; `VerbQ` requires `Verb` (H-7 point 2) |
| `PASSIVE "ed"` | the inflection of the form that may not mutate | `Replaced`, `Removed`, `Spacified`; applied when a family is GENERATED (`e` takes `d`, consonant-`y` takes `ied`), never read off a name -- no dictionary inverts `Removed` |
| `STATEMENT "X"` | the assertion suffix, outermost | `AllNumbersInQX`: the statement wraps the fluent form (H-7 point 4) |
| `PARAMS [cs: "CS", st: "ST", ...]` | the parameter suffixes, a key per suffix | "`Many` > `CS` implies the list then the flag": suffix order is parameter order (point 3), so no order is fixed and `FindCSZZ` and `FindZZCS` both agree. One meaning per suffix (R1, R2): the document's `FF` -- the future form AND the free form -- cannot be declared twice, which is point 7's clash made a refusal of the meta-court; a suffix is letters (R5); `fluent` and `passive` are the roles' own words, not keys (R7) |
| `FAMILY [kind, base, forms]` | the declaration kind that spells a family, its base-verb seat and its offered-forms seat | "a definition declares the forms it offers (`forms [Many, CS, Q]`); the compiler generates the family" (point 6). The kind is declared, the base seat is one verb, the forms seat is a list (R3, R6) -- typed by a MENU of the FORMS' own words, because a list seat is typed by a declared menu, form or kind and never by a bare `[name]` |

## Grammar (EBNF), the v0.11 text with this addition

```
FORMS:       FLUENT string, PASSIVE string, STATEMENT string,
             PARAMS message_list, FAMILY name_list
message_list = "[" IDENT ":" STRING { "," IDENT ":" STRING } [ "," ] "]" ;
```

## What the forge makes of it

A court whose language declares a FORMS loads `forms_lib.ring` (and nothing else new) and
gains two verbs:

```
<lang>_court.ring family <file>               every FAMILY's members, generated
<lang>_court.ring spellings <file> <names>    one verdict per name, then a summary
```

**`family`** generates each declared family: every subset of the offered parameter forms,
in the order offered, as the plain name, then the fluent name, then the passive name.
`FindNext` offering `[st, cs]` is `FindNext`, `FindNextST`, `FindNextCS`, `FindNextSTCS`;
`ReplaceAll` offering `[cs, fluent]` is `ReplaceAll`, `ReplaceAllQ`, `ReplaceAllCS`,
`ReplaceAllCSQ`.

**`spellings`** reads a list of names (one a line, `#` a comment) and splits each from the
end: the statement form, the fluent form, then declared suffixes longest first, each spelt
once. A name agrees when it parses; it disagrees when a suffix appears twice, when the
fluent form is not last or the statement form not outermost, when a trailing run of two or
more capitals is spelt by no suffix (`ToJSON`), when a fluent name has no plain twin in the
list (`ReplaceNthCharQ` with no `ReplaceNthChar`), or when its base is a declared family's
and it is not a member that family generates (`FindFirstXT` against `FindFirst` offering
`[st, d, zz, cs]`). Members a family generates that the list lacks print as `missing`. The
last line counts: `spellings: N agree, M disagree of T; K declared members missing`.

**At `check`**, a family offering a form the FORMS does not declare is refused -- by the
menu that types the seat first (code `FORMS`, the menu's own), and by the FORMS pass second
if a menu and the FORMS ever disagree. The refusal carries the envelope of v0.11.

## Measured

`stzv_v12.haro` declares the Softanza vocabulary's FORMS as the forms document spells them
(`FLUENT "Q"`, `PASSIVE "ed"`, `STATEMENT "X"`, twelve parameter suffixes); `stz/string.stzv`
five families of stzString by base verb and offered forms. The guard's stage 15 judges the
court two ways, neither mine. The forms document's own examples, re-expressed as names in
`v12/doc_names.txt` with the verdict principle 7 gives each in `v12/forms_cases.json`: the
three families it spells, member for member (24 names); 30 names judged -- `RemoveFFQ` the
FF clash, `UppercasingFQ` a fluent form with no plain twin, `FindFirstXT` outside its
family, `FindQCS` the fluent form not last, `ToJSON` a run no suffix spells; and
`FindLasteAsSection`, `WithoutSapces` and `NearstTo` AGREE, because the court judges the
forms grammar and not the dictionary. Then stzString.ring's own definitions, read live from
the author's tree by the guard on every run and never written to: every `Find*`, `Replace*`
and `Remove*` method, 595 names.

    595 definitions    584 agree with the FORMS
                        11 disagree:  2 the grammar's own refusal (FindSSZ, FindSSZZ: S twice)
                                      1 a fluent form with no plain twin (ReplaceNthCharQ)
                                      8 shipped members outside the forms their family
                                        offers (FindFirstXT, FindFirstZ, FindFirstSZZ,
                                        ReplaceAllExcept and ReplaceAllExceptQ, ReplaceMany,
                                        ReplaceManyCS, ReplaceManyCSQ)
                        41 generated members the tree does not ship (FindNextST,
                           FindFirstSTCS, RemoveCS, ReplaceCSQ, ReplacedXT ...)

The floor is pinned at 584. The same bytes on `rnxc` and the oracle on every `family` and
`spellings` run, first run of the cases. The eight are point 6 of H-7 working on families
declared from the document's examples, not a verdict on the tree: a family declared wider
would take them in, and that is the vocabulary's decision. The 41 are what the compiler of
principle 7 would add, named one by one -- the first measured slice of the "10,600
hand-typed spelling variants it retires".

## What it does not do, named

- **No dictionary.** A misspelled WORD (`FindLasteAsSection`, `WithoutSapces`) agrees with
  the forms grammar; its refusal is the computing altitude's, an unknown name.
- **The passive is generated, never read.** `Replaced` agrees as a plain name whose base is
  `Replaced`; it is a member of the `replace` family only because that family offers
  `passive` and generates it.
- **Points 1, 4 and 5 of H-7** -- a passive body that writes an attribute, `W` parsed at
  compile time, `Many`/`Except`/`IsNot` verified against the base's signature -- need bodies
  and signatures, which this altitude does not hold.
- **Prefixes** (`viz`, `rnd`, `@`) are read as part of the base; the document's prefix forms
  are not declared.
- **One trailing capital** is never a disagreement (`ToA` could be a word); two or more are.
- Suffix order is not judged: H-7 point 3 makes the order the parameter order, which is
  free, and a fixed order is a decision the vocabulary has not taken.
