# Haro v0.44 -- the ported defects (HARO-PORTED-FINDINGS-01)

The author's ruling of 2026-11-08 (PRINCIPAL-HAROFIRST-01, LEDGER line 207, carried by Central at 08:18), quoted whole:

> "I want all our projects to work against Haro and not Ring++, excpet when this is required for intermediate port reasons. And even for
> that, the fixes and enhancements should go into Haro and not Ring++. When Haro is abale to run all Softanza code (through it's Ring syntax
> surface, or in poure Haro after updating the Softanza code itself, then Ring++ will be retired like Ring has been retired)."

And on this desk's order of work, asked "Start with the four ported defects, then C27?": "Yes, that order".

stzlib's sweep of 1,746 guards found four runtime defects on Ring++ and reproduced each on `haro.exe`. Under the ruling they are fixed
here. **Ring 1.27 is the specification of a `.ring` file's surface**, so every expected answer of a `.ring` case was read off Ring 1.27
(`ported_court.py --ring`), which is this rung's subject and never its judge. Fixtures first (`fixtures.json`, `cases/`: 07912da, 12 cases,
1 holding before the code -- Q12, an append that keeps an archive, which must not move).

| line | what | cases |
|---|---|---|
| P1 | a math native outside its domain raises R51 "Value Error", as Ring's library does: `sqrt` of a negative, `log` and `log10` at or below zero, `asin` and `acos` beyond 1, `pow` of a negative to a non-whole power or of 0 to a negative one; an overflow to `inf` is no error | Q01, Q02 |
| P2 | a NaN is unordered: every ordering false, `=` false, `!=` true, in a condition as in a value, in a `.ring` and a `.haro` file | Q03, Q04, Q13 |
| P3 | `s[i] = c` writes a letter of a local text in a `.ring` file as Ring does: one character, or a number taken as its byte; more or fewer is R7, past the end R2; another name holding the text does not change | Q05-Q08 |
| P4 | a `.haro` file refuses it: `TEXT_IN_PLACE` | Q09 |
| P5 | `zip_openfile(f, "a")` on a file that is no archive answers Ring's NULL, every call on it does nothing, the file is left | Q10, Q12 |
| P6 | `zip_extract_allfiles` writes every entry, the last of a name winning, and answers nothing; a name that leaves its folder is not written | Q11, Q14 |

## How it is built

- **R51** is checked in the math natives' argument check, before the computation, per function -- the rule C's library reports as a
  domain or pole error and Ring raises on; `pow(2, 2000)` is `inf` on both.
- **A NaN** (`inf - inf` still makes one) is `unordered` in `jlt`, `jle`, `jgt`, `jge` and `cmpv`. A jump that fires when its comparison
  holds (`c = 0`) does not; an inverted one (`c = 1`, which the compiler emits for every condition, firing when it fails) does.
- **A letter of a text** (`textLetter`, from `vset`): a new text, Ring's rule, put in the local's register. The compiler marks in `vset`'s
  `d` (bit 2) that the container is a local's own register; a global's, an attribute's or a list item's text reaches `vset` through a
  register its holder does not read back, so it is refused by name rather than written into nothing.
- **zip**: append opens the file and asks whether it is an archive before reading it as one; extraction reads its entries by position
  (`readEntryAt`), since by name the first of two `a.txt` was read twice, and its error was swallowed by `std.zip.extract`'s caller so
  every entry after a duplicate was lost.

## Measured

- **Before**, on haro 5ef8a04: `sqrt(-2)` printed `-nan`, and `x <= 0` and `x >= 0` were both true -- a `.ring` file's `if y >= 0` took
  the branch Ring does not; `s[2] = "x"` was `Bad parameter type!` in both files; appending to a 28-byte text wrote 113 bytes over it;
  three entries (`a.txt`, `a.txt`, `b.txt`) extracted to one file, the first `a.txt`, answering 0.
- **Read off Ring 1.27** (`D:\Ring127`): R51 on `sqrt(-2)`, `log(-1)`, `log(0)`, `log10(0)`, `acos(2)`, `asin(2)`, `pow(-8, 0.5)`,
  `pow(0, -1)`; `sqrt(-0.0)` is 0, `pow(-8, 3)` is -512, `pow(2, 2000)` is `inf`; a NaN's orderings 0, `!=` 1; `s[2] = 66` is `aBc`;
  `zip_openfile` on no archive `isnull`, the file 28 bytes after; extraction `second` for the duplicate, and an empty answer.

## The protections, each switched off (`plants.py`)

**20 of 20 caught**, each one text substitution in `main.zig`, `compile.zig` or `zip.zig`, built into its own folder and judged by the
court alone: the four domain checks (Z1-Z4), the NaN in `jlt`, `jgt` and `cmpv` (Z5, Z7, Z9), the letter of a text -- `.haro`'s refusal,
the global's refusal, R7, R2, the copy, the compiler's mark of a local, the byte (Z10-Z16) -- and zip: append's archive check, the null
archive's calls, its NULL, extraction by position, its empty answer, and the name that leaves the folder (Z17-Z22).

- **Z6 and Z8 removed, named**: the NaN check of `jle` and `jge`. The compiler emits an ordering jump only inverted (`c = 1`, from
  `cond()`), and for these two a NaN's `valCmp` of 0 already makes `<=` and `>=` hold, so the jump fires and the comparison reads false;
  switched off, no case moved and none can. The checks are removed from the VM.
- **Four zip plants first stood 0 times**: `zip.zig` carries CRLF line ends in this working copy (HF-135) and the plant script matched raw
  bytes. It matches on LF-normalised text now, and they were caught on the rerun.
- **One plant's build ran past 15 minutes** with 11 GB free on D:; the build cache (2.4 GB, regenerated by any build) was cleared and the
  rest built in about 70 s each.

## The desk's readings, recorded as its own

- **A letter of a global's, an attribute's or a list item's text is refused in a `.ring` file**, where Ring writes it: allowing it would be
  a wrong answer with no error until the compiler writes the new text back to its holder. A named divergence, until that is built.
- **A name that leaves the extraction folder is not written** (absolute, a drive, a `..` part). Ring 1.27 writes `../evil.txt` beside the
  folder (zip slip, read off Ring): least authority over parity, a named divergence.
- A null archive is Ring's NULL, an empty text, so `isnull()` sees it; the VM's native bridge turns a null *handle* into the integer 0,
  which it does not, and changing the bridge would reach every engine handle -- so the answer is zip's own.
- `TEXT_IN_PLACE`'s `todo` builds the new text: `left(t, i - 1) + c + substr(t, i + 1)`. Bytes written in place are D56 (c)'s, not built.

## Not covered, named

- The three defects that wait for stzlib to load on Haro (RNXC-PREFIX-01, RNXC-EVALAPPEND-01, a process alive after R3): v0.45's C27 first.
- The other math natives (`sin`, `tan`, `exp`, `cosh` ...) have no domain error in C's sense and are as before.
