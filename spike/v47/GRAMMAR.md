# Haro v0.47 -- a name's first letter is its type (D55 T2)

D55 (a), the author 2026-11-07: "letters on every name ... yes". On this rung's scope, asked with the measurement below, the author
2026-11-08: "Yes, as recommended" -- check the letters whose types exist, re-letter Haro's code by rule, the `a` names wait for v0.50 (map
and record) so each is renamed once, a single lowercase letter only as a loop counter. Fixtures first (`fixtures.json`, `cases/`: 36b0aca,
14 cases, 5 holding before the code; amended at 1813273 before the parameter code -- Y15 added, Y13 corrected (its own `o = new P` broke the rule it tests, and its trace is the VM's existing class-region report); Y16 written after the plants, 0340c54 -- that commit also carried v38's `B03.haro` out of the index, a removal staged earlier, said so here).

| line | what | cases |
|---|---|---|
| Y1 | a value's name -- local, parameter, global, attribute -- begins with a type's letter then a capital: one of D55's sixteen (b i d f n t x k v m r o e h s w) or `a`, Softanza's list, until v0.50. A name with no letter is refused when compiling; Softanza's `c` is refused with `t` as its todo; a `.ring` file is untouched | Y02, Y03, Y11, Y13, Y15, Y16 |
| Y2 | a single lowercase letter is a name only as a `for` counter or a `catch` name | Y07, Y08 |
| Y3 | the letters whose types exist are checked: b boolean, i integer, n any number, f a number (until v0.48 splits float from decimal), t text, v vector, o object, h handle. A literal of another type is refused when compiling; any other value is checked where it is given -- a statement, a parameter on entry, a `for` counter -- and raises TYPE_LETTER | Y01, Y04, Y05, Y06, Y12, Y14 |
| Y4 | the letters whose types are not built yet (a d k x m r e s w) are accepted and not checked, each until its rung | Y09 |
| Y5 | the empty text NULL is absence until v0.49 builds `none`, and passes any letter | Y10 |

The desk's readings, recorded as its own: `n` on a local stays accepted until v0.48 (a local lettered `i` now would be relettered `d`
when a pointed literal becomes a decimal -- renamed once, as the ruling keeps the `a` names); functions, methods and classes are not
lettered (a letter names the type of a VALUE); `cCatchError`, Ring's name for the caught error, is read and never declared, and a
declaration is what is lettered.

## How it is built

- **The shape and the literal, when compiling** (`compile.zig`, `assign`, which now wraps the old body as `assignBody`): in a `.haro`
  statement a name given a value -- an identifier, `$g`, `This.x` -- is read for its letter (`letterFault`). No letter, a letter that is
  no type's, or a lone letter is the statement's fault, the same refusal a misspelling is (v42): the statement is compiled to a trap and
  the program stops there when it reaches it. Softanza's `c` names its todo, `t` and the rest of the name. A checked letter given a
  literal of another type (`literalLetter`: an integer, a pointed number, a text, a boolean, a list, a `new`) is the statement's fault
  too. A name spelled other than its declaration is that fault first, since it names the declaration the writer meant (v42's N03, N19).
- **The value, where it is given** (`main.zig`, the op `lchk`): after the assignment the target is read back -- a local's own register,
  else the target compiled as an expression into a temporary -- and checked against its letter. A compound with a literal of the
  letter's own kind (`iN += 1`, `tS += "x"`) keeps the type and emits nothing; so does `=` of a literal, settled when compiling. The
  check reports the statement's own line: Ring's F-114 row (after a statement's last call, the next token's line) is not a `.haro`
  statement's.
- **A parameter** (`emitOne`): a `.haro` function's lettered parameters are checked on entry, at the function's line; a parameter's
  shape refused is carried to the function's first statement (`entry_fault`), which is refused naming it.
- **A counter**: a `for` counter's name is lettered or a single letter; a `for x in` counter with a checked letter is checked on every
  element, after `iget`.

## Haro's own code, re-lettered by rule

`study/v47/reletter.py` holds the rules and was run once over the code as it stood at 1813273; `study/v47/port_cases.py` carried each
rung case's renames back into that rung's `gen_fixtures.py`, its program's source.

- R1 Softanza's `c` is text: `cName` -> `tName`, `$cX` -> `$tX`, file-wide and repository-wide (a global keeps one name across files);
  `cCatchError` kept.
- R2 a `t` name that held a token (a list) is `a` until v0.50 letters it, in the five library files whose t-names were tokens, read one
  by one (`study/v47/names.py`).
- R3 a single letter or a word declared in a function is lettered by what it holds, the original kept after the letter: a number `n`, a
  text `t`, a token or list `a`, anything else `x` -- `x` and `a` are not checked until their rungs, so a doubtful reading costs nothing
  at run time. A single letter that is only ever a `for` counter stays. A `$` global is renamed file-wide.
- R4 the forge writes code in strings: a `$c` global inside a string of `forge.haro` follows R1, since the court it forges declares it.
- R5 a `v` name held any value (Softanza's "value": `vInit`, `vKey`, `vVal`, `vC`), and D55's `v` is the vector: it is `x`.

## The cases of earlier rungs, changed after their courts spoke

v36, v37, v38, v41 and v42 run `.haro` programs whose names had no letter; each was re-lettered by the rules above and each says so in
its `gen_fixtures.py`. By hand: v38's `Res` takes a text (`tN`), U12's eval strings, K01's fmt text, W08's R24 naming `$nnever` (R24
folds a name -- see "Named"), and B03 moved to the Ring surface (`cases/B03.ring`, its program as it was): a `.haro` name always carries a
letter, so it is never `within` or `using`. v41's S14 now expects `Using` refused as a name with no letter -- which is how it shows
`Using` is read as a name. v42's `oClient` held a number and is `nClient`, its misspellings (`nclient`, `$ntotal`) kept as the subject.
v39's cases are read by `haro check`, which does not judge letters: they are unchanged.

## Measured

- **The court**: 16 of 16 cases on haro and its checked build, byte for byte.
- **Plants, 15 of 15** (`plants.py`): L1 no letter passes, L2 `c` loses its todo, L3 a literal of another type accepted, L4 an integer takes a pointed number, L5 null a text like any other, L6 `lchk` lets anything through, L7 Ring's F-114 row, L8 no entry check, L9 no parameter shape, L10 no for-in check, L11 a single-letter counter refused, L12 and L15 the checks reach a `.ring` file (MISSED first: Y11 held only literals; Y16 written after), L13 attributes not lettered, L14 the letter fault before the spelling fault (v42's N03, N19).
- **The census** (`study/v47/census.py`, 252 `.haro` code files): before the code was re-lettered the compiler refused 5,361 statements for `c` and 2,380 for no letter (counted with every loader, one fault a statement); after, none in Haro's code -- what remains is v39's checker-only cases and the SG1 probe, both named below.
- **Stage 6** (`study/v47/stage6_ab.py`), the court compiled from scratch, alternating the VM before the rung (9b82974) and the rung's, four rounds of 15 on the same court sources: 143.5 ms and 144.4 ms (+0.9 ms) -- no measurable cost. The guard's stage 6 read 179.6 ms while other sessions held the machine, and 139.6 ms alone (edit 19.0 ms).
- **The earlier rungs' courts**: v36 24 of 24, v37 31 of 31, v38 33 of 33, v41 17 of 17, v42 19 of 19, on both builds.

## Named

- `haro check` does not judge letters yet (types.zig): v39's case programs, read only by it, keep names with no letter.
- R24 in a `.haro` file names a variable folded to lowercase, as Ring does (`$nnever`), though a `.haro` name is spelled as declared.
- F-114 in a `.haro` file: an error after a statement's last call reports the next token's line for every check but the letter's (a
  NO_COERCION after `nX = 1 + Word()` as a function's last statement reports the line of `func Word`).
- `study/sg1/rulea.haro` is a probe pinned to haro b8233de, with its measurement in SG1.md; it is left as measured.
- A `catch` name with no letter is not judged (the binding is not an assignment); a single letter there is allowed, as Y2 says.
