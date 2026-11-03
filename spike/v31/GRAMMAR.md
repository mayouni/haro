# Haro v0.31 -- pattern rules over blocks, in Haro (step 2 of COMPASS-REBOL-06 and 07)

**Written after `fixtures.json` beside it, which is the judge** (the W discipline: fixtures first, prose second; the first 95
fixtures are b4c40d9, before any engine code, and four more were added after the engine, each found by a plant, and said so in
their names). v0.31 is step 2 of BLOCKS.md section 3.5, on the author's word to start it (2026-11-03, this session): *pattern
rules over the blocks step 1 reads* -- Red's Parse without the escape into the host and without the documented infinite loop. It is
the thirty-first rung (charter D45). v0.29 is the constitution desk's. **Nothing visible changes**: no court loads the engine yet,
so stages 1 to 35 run unchanged and stage 6's cold compile is untouched.

## What is new, and where it comes from

| instrument | what it is | the lesson it carries |
|---|---|---|
| `pattern_lib.haro`, the engine | a rule is C6 text -- a list -- read by the one LOAD of v0.30; `PatDeclare` compiles a set of named rules and either refuses it, naming why, or yields rules that are total by construction; `PatRun` matches by PEG with a packrat memo | the reference (`study/rebol/pattern.py`) was a Python model; this is the same engine in the language the courts are written in, so a court can load it. Nodes and sequences are integer ids in global lists, because **a list assigned is a list copied** (probed on the VM): a memo keyed by a list would copy the input at every step |
| `pattern.haro` | the engine at the command line: `haro pattern.haro cases <file>` judges a whole case file, one process for the lot, one line a case | the fast path named (CLAUDE.md, PX): the 99 fixtures and 91 texts of the spike run in 0.4 s per build, process start included |
| the type word `OPTIONAL` | one value that carries Haro's `?` mark; `INTO` an optional descends into the value it marks (a sequence of one) | **Q-B1 meeting step 2.** v0.30 made `?` a C6 value; a pattern over Haro's own declarations (`SEATS [amount: number, note: text?]`) could not see one. Without the word, the rule language could not describe the text its own language is written in (P38-P43) |
| a whole REPEAT count | `REPEAT n m`: n and m digits; `1.5` and `-1` are refused by name | the reference crashed with an uncaught `ValueError` on `REPEAT 1.5` and accepted `REPEAT -1` as a count that always matches. A crash is not a refusal (X29, X30). The reference is fixed in the same rung |
| `v31/pattern_court.py`, `v31/plants.py` | the court (guard stage 36) and the 45 protections switched off in turn | below |

## The rule language, as v0.31 reads it

A rule is a list. A lower_snake word, a string, a number, a path, a pair or an optional in a rule matches itself; a nested list is a
sub-rule; a keyword is a pattern word.

| words | meaning |
|---|---|
| `WORD STRING NUMBER KEYWORD PATH PAIR LIST GROUP ROW OPTIONAL`, `SKIP`, `END` | one value of a kind, any one value, the end |
| `OPT ANY SOME`, `REPEAT n [m]` | repetition, greedy, as PEG |
| `OR` | ordered choice that commits (P37) |
| `NOT AHEAD` | look without consuming |
| `INTO` | descend into a list, a group, a row, a pair (read as its key then its value) or an optional (read as the value it marks) |
| `TO THRU` | skip up to, or past, what matches |
| `COLLECT KEEP` | Parse's `collect`/`keep`; a top-level `COLLECT` is the result |
| `RULE name`, `MEMBER name`, `LIT v` | a named rule; a value drawn from a SET the court collects (a number, a string, a word and a keyword by their text); a value matched as itself |

A rule matches only when it consumes its whole input. Comments are not values. Matching is PEG with a packrat memo: **a (node,
sequence, position) is computed once**, so a match costs at most rule nodes x input positions steps. The court holds that on every
fixture, and the worst match spent exactly 100% of it, reached only on the empty input (P06, P48, P56).

## The bound, refused at declaration and never at match time

| refused | by | fixtures |
|---|---|---|
| recursion, in full (`a -> b -> c -> a`), through RULE or through INTO | a depth-first walk of the named rules | X01 X02 X31 X32 |
| ANY, SOME or TO over a rule that can match nothing: Parse's documented infinite loop cannot be written | a nullable analysis | X03 X04 X05 X16 X27 X28 |
| a group in a rule (Parse's `paren!`, the escape into the host); WHILE DO EVAL IF | the word table | X06 X07 X15 X20 X21 |
| CHANGE INSERT REMOVE: a pattern judges and never edits | the word table | X08 X22 X23 |
| a rule that is no list; OR with a side missing; a word that is no pattern word; a unary word with nothing to apply to | the compiler | X24 X25 X26 X13 X14 |
| REPEAT without a count, with a count and no rule, with a count that is no whole number, with its minimum above its maximum | the compiler | X11 X12 X29 X30 X35 |
| RULE or MEMBER without a name, or followed by a value that is no word; LIT without a value; a RULE or a MEMBER that names nothing | the compiler and the checks | X09 X10 X17 X18 X19 X33 X34 X36 X37 |

## The court: `v31/pattern_court.py`, guard stage 36

| what | judged | holds |
|---|---|---|
| the reference | `study/rebol/pattern.py` on the study's own 53, and on the 99 of `v31/fixtures.json` | 53 of 53, 99 of 99 |
| the fixtures | every match fixture by its verdict, its values kept and its step bound, every refusal by the fragment of why; on `haro` and on its checked build | 99 of 99, byte-identical |
| **the twin** (D43) | each case's line from the engine against the reference's line for the same case: verdict, values kept, **steps**, bound, and the words of a refusal | identical on all 99, down to the step. A difference is refused by name, by case |
| FAM1, the whole spike | the declaration form written once as `[SOME RULE decl END]` with `decl = [LIT DEFINE KEYWORD WORD LIT AS GROUP LIT RATIONALE STRING]`, over every declaration and sentence | 85 of 91 match, 11,390 steps, the reference's own total; the six that do not are named, and each was written to lack something (a rationale, a DEFINE, a declaration at all) |
| the protections | `v31/plants.py`: 45, each switched off in turn in a copy of `pattern_lib.haro` | 45 of 45 load-bearing, the fixtures each fails printed beside it; `--plant` fails the stage |
| every other stage | the whole guard, stages 1 to 35, with the engine loaded by no court | the whole guard passes, 36 stages in 1,189 s on haro and its checked build |

The stage runs in half a second. **FAM1 is the memo's claim made small**: the meta-court spends code on "every declaration carries its
RATIONALE" (a sentence refused at `haro (line N): every stzu declaration carries its RATIONALE`), and a pattern says the shape of a
declaration in one line, judged over the family the one LOAD reads. It does not replace the meta-court; it shows the home BLOCKS.md
4.3 argued for would hold such a rule.

## What building found (HF-136)

1. **The reference crashed where it should have refused**: `REPEAT 1.5` raised an uncaught `ValueError` (X29), and `REPEAT -1` was a count that matched anything (X30). Found by reading `int(...)` while writing the port; fixed in the reference, the fixtures first.
2. **Step 1's `?` and step 2's rules had not met.** The rule language had no word for the one value kind Q-B1 added; composing the two rungs on Haro's own seat list found it (P43).
3. **The plants found four missing fixtures** after the engine passed: REPEAT's minimum (P62), REPEAT with a count and no rule (X35), RULE and MEMBER followed by a value that is no word (X36, X37). The engine's protection was switched off and every fixture still held, which is the sentence that defines a missing fixture.
4. **Some fixtures are carried by the twin and not by themselves.** X12's fragment (`REPEAT takes`) also appears in the message of the neighbouring refusal, so switching REPEAT's count check off leaves X12's fragment satisfied; the plant is caught because the engine's line then differs from the reference's. The study's fixtures stay verbatim; the twin is why a weak fragment costs nothing here.
5. **P17 does not pin a pair's order**: its key and value are both words, so reading a pair as value-then-key passes it. P41 to P43 pin it (the plant is caught by them).
6. **Two reader refusals worded differently.** A text neither reader can read is refused by the reader, in Haro's words (`block (line 3): ...`) and in the reference's (`line 3: ...`); that wording is step 1's to judge (v30), and the family court takes two refusals at the same line of the same text as agreeing.
7. **Three quirks of the VM met on the way**, each probed and avoided: a parameter named `cAll` makes `str2list(cAll)` a refused statement (`cText` does not); `list(0)` is an error, not an empty list; a top-level statement written after a `func` belongs to that function.

## What v0.31 does not do, named

- **The declaration `DEFINE PATTERN name AS (MATCH [...], OVER <seat or kind>)`** of BLOCKS.md 4.3, judged by the meta-court, is the next rung. It changes the meta-language and the forge's prologue (every forged court regenerates, the cold compile grows by what the court loads), and it needs decisions the fixtures must pin first: where a set comes from (a menu's words, a kind's seats, the values of another declaration's list seat, a world's symbols), what a refused pattern's code and cites are in the diagnostic envelope, and what `OVER` hands the engine (a seat's value read as a block, as the court holds it).
- **Sets are data the court supplies.** The engine takes them as arguments; collecting them from a sentence's records is the court's half, with the declaration.
- **Q's `ask` verb** (COMPASS-KERN-03's field check) does not use patterns: a question is not C6 text (BLOCKS.md 4.4).
- **The conditions and expressions** inside `WHEN "..."` strings keep their own lexers.
