# Haro v0.32 -- DEFINE PATTERN: the value join, said once as a rule over a seat (BLOCKS.md 4.3)

**Written after `fixtures.json` and `court_cases.json` beside it, which are the judges** (the W discipline: fixtures first, prose second;
the fixtures, the world `grants_v32.haro` and its sentences are c1f6d95, before any code read a PATTERN; the fixtures added after the code
say so in their names). v0.32 is the next rung BLOCKS.md 4.3 and v0.31 named, taken on the author's word (2026-11-03: "DEFINE PATTERN"), and
the answer to **Central's item 3** of 2026-10-31, stzzui's S7: a fact *across declarations* that no clause of the court's own grammar could
say -- "every right a use asks for is a right some zone grants". It is the thirty-second rung (charter D46). v0.31's engine finally has a
customer: a language declares a rule, the court collects the sets it draws from, and the sentence is judged.

## What is new, and where it comes from

| clause | declares | the lesson it carries |
|---|---|---|
| `DEFINE PATTERN name AS (...) RATIONALE "..."` | a rule over a seat, judged on every declaration of the seat's kind | a kind of the meta-language, the first since v0.28. It is a `CONSTRAINT` whose condition is a pattern: the same `MESSAGE`, `CODE`, `CITES` (a list, or the word `none`) and `SEVERITY` (`error` or `warning`), with the same meaning |
| `OVER kind.seat` (required) | the seat judged, named as `declaration.seat` | **the value judged is the seat's value as written**, read by the one LOAD (v0.30): `RIGHTS [read, write]` is a list of two words, `PRIMARY read` one word. Nothing is re-derived from a record the court holds; the court slices the sentence's own text by the span the parser already kept for the refinement gate |
| `MATCH [ rule ]` (required) | the rule, a C6 list written in the declaration, not in a string | a new clause shape, `rule`: the tokens between the matching brackets rejoined into one line. Comments inside it are layout. The rule is judged **by the pattern engine's own declaration** (v0.31), in its own words, so the meta-court refuses recursion, a repetition that cannot move, a group, `WHILE` and the editing words without a line of its own |
| `SETS [kind.seat: set, ...]` | where a `MEMBER` set comes from | the points `REFINE` already writes, reused: `zone.rights: granted` says the set `granted` is the values of the seat `zone.rights` across **every** `ZONE` of the sentence. A set is data the court collects, never code (BLOCKS.md 4.2). A `MENU` of the language is a set already, under its own name. One set, one declaration: a set named twice, or named like a `MENU` or a kind, is refused |
| a pattern uses another by `RULE name` | the patterns of a language are **one set of named rules** | the engine's named-rule graph, now across declarations: `wants_are_granted` reuses `granted_right`, and a cycle between two patterns is refused with the cycle named (`a -> b -> a`) |
| Art. 1 explainability | a pattern carries a `CODE` | a refusal under explainability is traceable by a stable identifier (C2 2.1); a pattern refuses as a constraint does, so it joins the article's check |
| the record | the language entry's **24th element**, present only where a language declares a pattern | `[name, over kind, over seat, rule, sets, message, line, code, cites, severity]`. A language without a pattern forges **the bytes it forged before**: the ten committed courts are byte-identical |
| `pattern_lib.haro`, `pattern_judge.haro` | the engine and the court's half | **loaded only by a court whose language declares a pattern**, as `expr_lib.haro` is for an `EXPRESSION`. The court library every court loads grew by 7 lines (the guard on the 24th element) and not by the 98 of the judge: the first version put them in `court_lib.haro` and cost the cold compile 6.6 ms (alternating A/B, minima of 25); moved, +1.3 ms |

## Grammar (EBNF), the v0.28 text with this addition

```
PATTERN:  OVER path, MATCH rule, SETS point_list, MESSAGE string, CODE string, CITES cites, SEVERITY IDENT   -- OVER, MATCH, MESSAGE required
path       = IDENT "." IDENT ;                                -- declaration.seat
rule       = "[" { token } "]" ;                              -- brackets balanced; a C6 list of pattern words (v0.31)
point_list = "[" point { "," point } "]" ;  point = IDENT "." IDENT ":" IDENT ;     -- kind.seat: set
```

The meta-court prints one line more on acceptance, `patterns N`, **only where N is above zero**, so no language without a pattern prints a
different byte.

## How a pattern is judged

1. The meta-court resolves `OVER` and each `SETS` point to a seat that exists, refuses a set that is named twice or named like a `MENU`
   or a kind, and hands every rule of the language, with the set names and the `MENU` names, to `PatDeclare` (v0.31): the bound and the names.
2. The forge ships the patterns as the language entry's 24th element, and loads the engine and the judge for a court that carries one.
3. The court, after the `CONSTRAINT`s and before the references, collects the sets from the sentence's own declarations and the language's
   menus (a word, a string or a number is one member; a list is its items), declares the rules, and for every declaration of the `OVER`
   kind that writes the seat reads the value as written and matches it.
4. A value the rule does not match is a finding at the line of **that seat's clause**: a refusal in the declared words with the declared
   code and cites, or, under `SEVERITY warning`, a warning spoken after the verdict. A seat the sentence does not write is not judged
   (`REQUIRED` speaks for a required one); a declaration the structural court already refused is not judged again.

## The world judged: grants

`grants_v32.haro` declares zones that grant rights and uses that ask for them, and four patterns: `granted_right` (one value), `wants_are_granted`
(a list, reusing the first by name), `via_is_a_channel` (a list against a `MENU`'s words, `CITES none`) and `wants_are_few` (`SEVERITY warning`).
`grants/` holds the twelve sentences; `court_cases.json` holds the 16 cases, judged by `haro_forge.py --stage=37`:

| case | what | holds |
|---|---|---|
| G1, G2 | the clean sentence; the meta-court reads the world, `patterns 4` | ok |
| G3, G4 | the value join on a list: a right no zone grants is refused at its `WANTS` clause (line 8), in the declared words; the envelope carries the code and the cite | ok |
| G5 | the value join on one value, through a rule another pattern uses by name: refused at `PRIMARY` (line 9) | ok |
| G6 | a set with no member: no zone, so no right is granted | ok |
| G7, G8 | a list judged against a `MENU`'s words: refused at `VIA` (line 9); `CITES none` gives an envelope with the code and no cite | ok |
| G9, G10 | `SEVERITY warning`: the sentence stands, the pattern speaks after the verdict with its code and line; the envelope carries `"warning"` and the default cite `rule:<CODE>` | ok |
| G11 | a set is the **union** of every zone's rights | ok |
| G12, G13 | a seat the sentence does not write is not judged; an empty list asks for nothing | ok |
| G14 | two patterns refuse at once, each at its own line | ok |
| G15 | a declaration the structural court refused is not judged again by a pattern (added after the code) | ok |
| G16 | a pattern judges the seat of its own kind only: a `ZONE` writes a `PRIMARY` that the pattern over `USE.primary` would refuse, and it is not judged (added after the code, found by planting the kind filter off) | ok |

## The court: the numbers

| what | judged | holds |
|---|---|---|
| the meta fixtures | `v32/fixtures.json`: 6 accepts by their counts (`patterns N` among them), 27 rejects by the fragment of why; on `haro` and on its checked build | 33 of 33, stage 1 |
| the court cases | `v32/court_cases.json` over `grants/`, the court forged from `grants_v32.haro` on both runtimes, the two printing the same bytes | 16 of 16, stage 37 |
| the committed courts | every pattern-less language re-forged | byte-identical to HEAD: a language without a pattern forges the bytes it forged |
| the protections | `v32/plants.py`: 40, each switched off in turn in a copy of `haro_lib.haro`, `forge.haro` or `pattern_judge.haro`, judged by the same fixtures and cases | 40 of 40 load-bearing, the fixtures each fails printed beside it |
| the cold compile | stage 6, the machine court, minima of 15 | 136.5, 143.1, 146.5, 146.2 and 147.8 ms in five standalone runs against the 150 ceiling, 142.0 in the first full guard, and **169.7 once in the last full guard (median 324), under the load of other sessions**; 14.4 to 18.7 ms for the edit; the court library grew by +1.3 ms (alternating A/B). The margin is thin on a shared machine that read HEAD itself at 135 to 153 ms today; stage 6 is a wall-clock gate and flakes under external load (PX: flaky is a latency defect) |
| the meta-court's cold start | `haro.haro machine_v03.haro`, alternating A/B, minima of 25 | 116.2 ms before, 131.3 after (+15.1 ms): it loads the engine to judge the bound |

## What building found (HF-137)

1. **Where the court's code lives is a cost.** The first version put the pattern judge in the court library every court loads, 98 lines, and the cold compile of a court that declares no pattern grew 6.6 ms; moved to `pattern_judge.haro`, loaded only for a language that declares a pattern, it costs 1.3 ms (the 7 lines of the guard). Both figures are minima of 25 runs timed **alternately** on two copies, because a straight before-and-after read 153 ms for HEAD itself on a machine 20% slower than the day's first reading: a timing on a loaded machine proves nothing, and two builds timed alternately cancel the drift.
2. **A global first assigned in a function is global on this VM**, on `haro` and on its checked build. The engine births its own through `PatReset`, and no root file carries boilerplate: the births every earlier rung wrote in its root file are a Ring 1.27 habit, not a need.
3. **An undefined function compiles and fails only when called**, so a court may carry the call and load the library only where a language declares it.
4. **The plants found what the tests did not, again.** R26 (`MESSAGE` is required), G15 (a declaration the structural court refused was judged again by a pattern: a spurious second finding), G16 (the kind filter: nothing changed when it was switched off, because no two kinds shared a seat name, so a `ZONE` now writes a `PRIMARY` too), and an unpinned branch that gave a pair list's values to a set.
5. **That branch was a design question written as code.** The values of a pair list are rarely what a join wants (the keys are the identifiers), and a wrong set is a silent failure. The branch went; R27 refuses a `SETS` over a pair list by name, fixture first.
6. **A fixture was wrong and the court right (G10).** A pattern with no `CITES` keeps the default `rule:<CODE>` since v0.28, as a constraint does. Changed after the court spoke, and said so in its name.
7. **A rule inside a declaration is a clause shape, not a string.** `MATCH [ ... ]` is the tokens between the matching brackets rejoined to one line, so the engine judges it where it is written. The price: a rule holding both a double and a single quote cannot ride in the source of a court, and is refused (R22).
8. **The engine's words come through the meta-court's mouth**, at the line of the pattern the engine names: a cycle between two patterns is refused as `a -> b -> a`.
9. **The meta-court pays for the engine.** It loads `pattern_lib.haro` to judge the bound, and its cold start on `machine_v03.haro` rose from 116.2 to 131.3 ms (alternating A/B, minima of 25). Nothing gates the meta-court's time; the remedy, if it ever matters, is to split the engine into its declaration half and its match half and load only the first there.
10. **The family follows the spike, and its list of extensions is kept by hand.** The full guard's one failure was v0.31's FAM1 pinning 85 of 91 texts: the grants world made the spike 104 (13 new, all matching the declaration form) once `.grant` joined the sentence extensions of the v0.30 round trip and of FAM1, two copies of one list. Changed after the court spoke, and said so in the fixture; a new letter's extension is added to both until the list is read from the declarations.

## What v0.32 does not do, named

- **A whole declaration as the judged value** (`OVER kind`, BLOCKS.md 4.3 wrote "seat or kind"): the court already judges a declaration's form
  structurally, and no customer asks for more. The span of a declaration is not kept; keeping it is a small rung if one does.
- **A set drawn from anything but a seat's values and a `MENU`'s words**: a world's symbols, a kind's seat names. Named by BLOCKS.md 4.2;
  each is one more form of `SETS` and one more fixture.
- **stzzui's declaration** is stzzui's to rewrite: its VIBE_STRIPS_RIGHT constraint becomes a `PATTERN` over the vibe's strips with the `rights`
  of the zones as its set, and the twin-court ratchet then shrinks by the difference this rung closes.
- **The meta-court loads the engine** (`pattern_lib.haro`), so every `haro.haro` and `forge.haro` run compiles about 520 lines more; a court's
  cold compile (stage 6) does not.
