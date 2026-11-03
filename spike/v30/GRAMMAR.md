# Haro v0.30 -- the one reader of C6 and its canonical printer (step 1 of COMPASS-REBOL-06)

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures first, prose second; the
fixtures are ee9071c, before any reader or printer code). v0.30 is step 1 of BLOCKS.md section 3.5, as Central read the
Principal's word of 2026-11-02 (LEDGER.md lines 157 to 160; mailbox 14:08) and prompt 56 carried it: *one reader of C6
-- the spike had two C6 lexers -- and a canonical printer, under the printing court, as a guard stage.* It is the
thirtieth rung (charter D44). v0.29 is the constitution desk's. **Nothing visible changes**: every court prints the bytes
it printed, which is what step 1 promised ("it is 99% true already; the rest is two instruments").

## What is new, and where it comes from

| instrument | what it is | the lesson it carries |
|---|---|---|
| `block_lib.haro`, the one lexer (`BlkTokenize`) | C6's lexis in one place: `--` comments (kept as tokens), double-quoted strings folding a continuation's indent, numbers with a sign and a fraction, lower_snake words, UPPER_SNAKE keywords, the punctuation of lists, groups and pairs, Haro's `?` and the `.` of a path; a token carries its byte span | the meta-court's `StzuTokenize` and every court's `CtTokenize` were two hand-written character walks of one lexis, and they had **drifted**: one read `-5` and `1.5`, the other refused `-` and `.`; one dropped the whitespace before a folded line break, the other kept it (HF-135). Two lexers of one format is two formats |
| the error token | the lexer refuses nothing: when a text cannot be read its last token is `[error, category, line, text]` and each reader composes the refusal in its own words | the meta-court says *character '>' is not part of the stzu grammar*, a court says *The character '>' is not part of the notice grammar -- <the language's own message>*, the block loader says *the character '>' is not part of C6*. One lexer, three voices, every court byte-identical to before |
| `BlkLoad`, the block loader | C6 text -> a **block**: a sequence of typed values (word, keyword, string, number, path, pair, list, group, row, comment, optional) -- the model of BLOCKS.md 3.1, `block.py` ported | the courts' parsers stay what they are (a declaration's parser and a sentence's parser both read these tokens); the block is the generic reading, the one the printer and the round-trip court use, and the one step 2's pattern rules will match over |
| `BlkPrintC6`, the canonical printer | one spelling per block (BLOCKS.md 3.2): a declaration a paragraph, a blank line between; a group's items one a line, two spaces deeper, a comma after each but the last; a list inline unless it holds a comment or a group; a comment on its own line | the formatter is the printer, as `CODEGRAPH.md` R6 says of programs; K01 to K07 pin it, and the family round trip proves it loses nothing a second reading can see |
| `block.haro` | the one LOAD at the command line: `load`, `fmt`, `same <a> <b>`, `roundtrip <file> ...` (one process for the whole family, 92 texts in under a second) | the fast path named: process cold start is the tax nobody budgets (CLAUDE.md, PX) |
| `haro.haro <file> fmt` | the meta-court prints the canonical spelling of a declaration before judging it | BLOCKS.md 3.5 step 1 asked for `haro fmt <file>` of the declaration; one printer, proved by the court to print what `block.haro fmt` prints |
| `?` is C6 | the loader reads Haro's `?` as an optional value after any value, and the printer keeps it (H01, D07, K04) | **Q-B1, ruled** (LEDGER.md line 157): `AS` and `?` are recorded in C6 as amendments Ringua writes, not removed from Haro |
| two refusals by name | `"the page": 1` -- *a string as a pair's key waits for C6's amendment (Q-B2)*; `"a ""b"" c"` -- *a doubled quote inside a string waits for C6's amendment (Q-B2)* (F07, F08) | **Q-B2, ruled** (line 158): both amendments are yes and Ringua writes them. Until its text lands the reader REFUSES them, so neither the old reading (two adjacent strings) nor an early adoption stands in for the amendment. When Ringua's text lands, two refusals become two readings and two fixtures move from `refused` to `same` |

## The lexis, exactly, and where the one reader diverges from the two it replaces and from the study's model

The judge of the reader is the fixture file; this table is what the fixtures leave implicit, so a divergence is a
decision read here and not rediscovered.

| text | the meta-court's old lexer | a court's old lexer | `block.py` (the study) | **the one reader** |
|---|---|---|---|---|
| `-5`, `1.5` | a number | `-` and `.` refused as characters | a number | a number (C6 3.3). In a sentence a court's parser now meets a number where it met a refused character |
| `1.` | the number `1.` | `1` then `.` refused | `1` then `.` refused | `1` then `.`: a fraction is digits after the dot |
| `1a` | `1` then `a` | refused: *neither a number nor a word* | `1` then `a` | refused, by name (a court's reading: the typo is named) |
| `Foo` | refused | refused | a **word** | refused: case is meaning (C6 3.4, 3.5; F11). The study model was lenient here and the census's 29 of 29 did not depend on it |
| a string's trailing whitespace before a folded line break | dropped | kept | kept | **kept** (C6 3.2 folds the continuation's indent, not what stands before the break). The meta-court's rationale of such a string gains a space; no fixture of stages 1 and 18 wrote one (the guard says so) |
| `"a ""b"" c"` | three strings | three strings | `DOUBLED_QUOTE` off: three strings | refused by name (Q-B2) |
| `"the page": 1` | not reached (the meta-court's parser) | not reached | a pair with a string key | refused by name (Q-B2) |
| `?`, `.` | tokens | refused as characters | `?` a token, `.` inside a path only | tokens; a court refuses both as it did, in its own words; the loader reads `?` as optional and `.` inside a path |
| a BOM at the text's start | refused | refused | whitespace anywhere | layout at the start only |
| `--` comment | dropped | dropped | a value | a token: a value to the block, layout to a court |

## Grammar: the block (BLOCKS.md 3.1), as the loader reads it

```
block      = { value | comment } ;
value      = scalar [ "?" ]* ;                                   -- Haro's optional mark, after any value (Q-B1)
scalar     = name [ ":" value ] | string | number | list | group ;  -- name ":" value is a pair; a string before ":" is refused (Q-B2)
name       = word | keyword | path ;   path = word { "." word } with no space on either side of a dot
list       = "[" items "]" ;   group = "(" items ")" ;
items      = [ item { "," item } [ "," ] ] ;                     -- a trailing comma is layout; an empty item is refused
item       = { comment } value { value } { comment } ;          -- one value is that value, several are a ROW; a comment inside a row moves after it
```

## The court: `v30/block_court.py`, guard stage 35

| what | judged | holds |
|---|---|---|
| the reference | `study/rebol/block.py` on its own 21 fixtures | 21 of 21 |
| the fixtures | `v30/fixtures.json` on `haro` and on its checked build, byte-identical: 9 same, 7 differ, 6 canonical, 11 refused | 33 of 33, the same bytes on both builds |
| left to step 3, printed by name | L05, L06, D04, K03, F05: the memo spelling (BLOCKS.md 3.5 step 3, with Q-B2's amendments) | 5 skipped, named |
| the round trip | every declaration (29 `.haro` files whose first word is DEFINE, `paths.is_declaration`) and every sentence of every letter (62 files of the census's twelve extensions): text -> block -> canonical printing -> block, one process per build | 90 of 91 read, print and read back to the same block; `f/operator-in-guard.f` refused by design (a fixture written to be refused: `>` is not C6); 328,088 bytes written, 330,329 printed (+0.7%); the same bytes on both builds, in a quarter of a second each |
| one printer | `haro.haro machine_v03.haro fmt` prints what `block.haro fmt machine_v03.haro` prints, on both builds | holds |
| the protections | `v30/plants.py`: sixteen, each switched off in turn in a copy of `block_lib.haro` | 16 of 16 load-bearing; the fixture each fails is printed beside it |
| every court unchanged | the whole guard, stages 1 to 34, with the meta-court and every forged court tokenising through the one lexer | every stage passes (the whole guard passes, 34 stages printing the bytes the baseline run printed (stage 21 reads four more refusal texts, 1,189 to 1,193, none naming a person) and stage 35 new); the ten committed courts are not regenerated (the forge's prologue is unchanged) |

The stage runs in 2.5 s; `--plant` fails it (K04 and the round trip).

## What building it found (HF-135)

1. **The two lexers had drifted in four places** (the table above), each place a reading one court had and the other
   had not. None was a fixture's business until a third reader asked what the format IS. The one lexer takes C6's
   reading at each place and the guard proves no committed text or fixture stood on a drifted one.
2. **A plant found the guard's scratch in the family.** The round trip read `zz_mut.haro` (stage 18's mutation file)
   while the baseline guard was writing it, and the two builds "differed" on its byte count. A text the guard writes and
   removes is not a text of the family: the court skips `zz_*` and says why.
3. **The fixture is the judge of the message.** F07 and F08 were written with the fragment `(Q-B2)`; the first code
   wrote `(Q-B2, Ringua writes it)` and failed its own fixtures. The messages followed the fixtures, not the other way.
4. **The cold compile** (D42's ceiling, stage 6) costs 7 ms: 122.1 ms before the wiring, 129.1 after (129.1 to 132.5 over three quiet runs), minima of 15 on a quiet
   machine (the court library loads `block_lib.haro`, about 470 lines, and loses the 130 of `CtTokenize`); the sentence-edited
   path is unchanged at 14.1 ms; 18 ms of the ceiling remain. Compiling the block library alone is 16 ms per process, lexing
   the stage 6 sentence 2 ms. **A reading taken beside a running probe is not a measurement**: the same stage read 150.5 ms on
   the unwired tree while the printing court ran beside it, and 240 ms once after the wiring; quiet, 122 and 129 (HF-53 again).
5. **The working copy is not the repository.** 107 tracked text files, the guard among them, carry CRLF in this checkout
   while the repository holds LF (`* text=auto eol=lf`, HF-126): an exact-text edit script that matched nothing found it.
   A fresh clone is clean; this working copy predates the attribute and was never re-checked out. Each file edited here
   was normalised first; the rest are left as they are, named.

## What v0.30 does not do, named

- **The two parsers stay two.** The meta-court parses declarations into language records and a court parses sentences
  into declaration records, each from the one lexer's tokens. Reading both through `BlkLoad` and walking the block would
  make every refusal's position and wording a new decision; it is a rung of its own if the pattern rules (step 2) want it.
- **The memo spelling** (five fixtures, named) is step 3, with Q-B2's amendments at Ringua.
- **The elders** stay spellings with their own readers (Q-B4, ruled NOT NOW): the round-trip court exists now, which is
  what Q-B4 waited for; asking their owners is Central's, on the author's word.
- **`haro fmt`** -- the VM's verb -- formats a PROGRAM of the computing surface (Ring++'s formatter, carried in the fork);
  the canonical printing of a DECLARATION is `haro haro.haro <file> fmt`. Two formatters for two altitudes until Q-B3's
  block syntax is designed.
