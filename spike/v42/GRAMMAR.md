# Haro v0.42 -- one spelling per name (D55, case-exact names)

The author's rulings of 2026-11-07, given in the session (all quoted whole in `TYPES.md` and `CHARTER.md` D55):

> on the desk's advice that names be case-exact and a collision by case refused: "I agree with you!"

> on TYPES.md's decision (e), a keyword in another case refused as PRINCIPLES 2.2 reads it, not a name as v0.41 read it: "Yes as recommended"

> on the natives' spelling, asked with the measurement below: "Lowercase (Recommended)"

Fixtures first (`fixtures.json`, `cases/`, `name_court.py`: 4facb1c, 14 cases, 2 holding before the code), then the compiler.

| line | in a `.haro` file | cases |
|---|---|---|
| N1 | a local, a parameter, a global, a function, a class, an attribute (`@nX` or bare) and a method are spelled where used as where declared; any other spelling is refused, naming the declared spelling and its line (or its file) | N01, N02, N04, N05, N08-N11, N14, N15, N17 |
| N2 | a second spelling in one scope is the same refusal: `oclient = 2` after `oClient = 1` is no second variable, `$ntotal = 2` no second global | N03, N19 |
| N3 | two functions whose names differ only by case are refused at a call of either, naming both | N06 |
| N4 | a native is spelled in lowercase, as the VM registers it: `isnull`, not `isNull` | N07 |
| N5 | a keyword of the grammar in another case is no name -- `aNd`, `If`, a member `o.See()` -- refused, also in an eval | N12, N16, N18 |
| N6 | a `.ring` file folds case as Ring does; a `.haro` file calls a `.ring` function by its definition's spelling | N13, N14 |

The refusal's words:

    one spelling per name -- declared `oClient` at line 4; written `oclient`
    one spelling per name -- declared `StzThing` in N14_lib.ring; written `stzthing`
    two functions differ only by case -- `Foo` at line 5 and `foo` at line 7; written `Foo`
    a native is spelled in lowercase -- `isnull`; written `isNull`
    a keyword in another case is no name -- `and` is a keyword; written `aNd`

## How it is built

- **Resolution stays Ring's.** The compiler folds case in 157 comparisons, and a `.ring` file must keep reading that way; none of them was
  changed. Instead every lookup that resolves a name -- `lookup` (locals, parameters), `findFunc`, `findClass`, the two global tables, `attrSlot`
  and `declaredAttr`, a method on a receiver (`memberCall`, against every class's methods and attributes), and the native a call falls to --
  compares, when a `.haro` statement is being compiled, the spelling written with the spelling it resolved to. The first difference is
  recorded, and the statement is refused when it has compiled (`stmtSpelled`). A second spelling of a name therefore never becomes a second
  name: it resolves to the first, and is refused.
- **Every statement goes through it**: the body loop, a rejoined `return`, each piece of a re-read span (a class method's `return @nX` is one),
  and an eval's statements. A keyword in another case is found by walking the statement before it compiles, member names included.
- **The trap stands at the fault's line.** A fault is raised after the statement compiled, when the compiler's row may have moved to a
  callee's (plant P14 found that it matters: a call); the trap takes the fault's own row.
- **Haro's block words stay contextual.** `within` and `using` are names where they open no block (v0.38's B03), so they are no keywords in
  principle 2.2's sense; v41's S14 (`Using = 5` is a name), changed in the fixtures commit, was restored before the code landed.
- **Haro's own code**: 433 native calls lowered in 16 files (`isNull` 377, `isString` 31, `isList` 16, `isNumber` 8, `isWindows` 1), strings
  included, because the forge writes court code in strings. The census of every code file then found ONE real fault: `haro_lib.haro`'s
  StzuDeclare writes `aPtS` and `aFlS` at line 2717 for the `aPts` and `aFls` it declared at line 2529 -- the same variables under Ring,
  reassigned; renamed. The other double spellings a lexical scan saw (`cT`/`ct`, `aFS`/`aFs` ...) are separate locals of separate
  functions, which the compiler accepts. v37's G06 spells `isstring` (changed after its court spoke, said so).

## Measured

- Before the rung (`runtime/v42/spell_scan.py`, Haro's 34 code files): 2,000 native calls, 433 not in lowercase; 8 words in two spellings in
  one file; no keyword in another case.
- `haro census max/stzMax.ring` (765 files) on v0.41 and on v0.42: the same lines, timings and memory aside, and the same lift counts.

## The protections, each switched off (`plants.py`)

16 plants in `compile.zig`, each built and judged alone: **16 of 16 caught**. Repaired on the way, not removed: P7 (a global written)
missed because every case read its global, and N19 writes one; P14's fixture was N02 and is N05, where the row has moved. **Removed**: P16
switched off the check that a looked-up name stands in the statement's own text, and no case moved; two probes -- a misspelling two
statements after its declaration, and a `.haro` call of a `.ring` function whose body writes `NN` for its own `nN` -- read the same. No
lookup in the compiler takes a name it builds itself. The check is gone, as v0.40 removed its two missed conditions.

## The desk's readings, recorded as its own

- A `.ring` declaration is spelled as Ring reads it: a keyword-shaped name in a `.ring` file is lowered by v0.41 (a method `See` is
  declared `see`), so a `.haro` caller writes `o.see()`, and `o.See()` is refused as a keyword in another case.
- A method on a receiver whose class is not known when compiling is accepted when some class of the program declares that spelling --
  the strongest check the compiler can make without the receiver's class.
- An eval's refusal is the eval's own error (`E1`), as every eval failure is, and names the declared spelling without its line when the
  declaration stands outside the eval's text.

## Not covered, named

- An attribute read on a receiver from outside its class (`o.nX`) is not checked; a method called on it is.
- A duplicate definition spelled the same (`func Foo` twice) is principle 2.5's, not this rung's.
- A function header's own name and parameters are not walked for keywords: a parameter named `If` is refused where it is used.
