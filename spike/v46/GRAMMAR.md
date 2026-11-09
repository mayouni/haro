# Haro v0.46 -- stzlib's findings on haro.exe

Under the author's Haro-first ruling (PRINCIPAL-HAROFIRST-01, 2026-11-08: "the fixes and enhancements should go into Haro and not Ring++";
"Ring++ will be retired as Ring and all it's libraries, only Haro will remain."), the findings stzlib's port to Haro sends are Haro's. Three
came in on 2026-11-08 from the session "StzLib towards Haro" (stzlib-haroport), each with a probe in stzlib's
`base/doc/design/haroport_probes/`; each reproduced here before anything was changed. Fixtures first (`fixtures.json`, `cases/`: 4a6d724,
7 cases, 1 holding before the code -- K04, a true arity error that must stay reported; K03 rewritten to stzlib's probe whole before any code,
K08 written after the plants, both said so). Every run case was read off Ring 1.27.

| line | what | cases |
|---|---|---|
| K1 | a read by a key not proven a whole number answers the element or the empty text of a missing key, so it is never held as an uncounted integer, nor read by an uncounted `vget` (HARO-KEYEDRELEASE-01: a segfault, two shapes) | K01, K02, K09 |
| K2 | `haro check`: a call whose statement follows a lone `.` is a call on a receiver, and the class's own method's arity is not its (HARO-ARITY-RECEIVER-01) | K03, K04 |
| K4 | an error unwound out of a call leaves no uncounted borrow behind: the unwind clears from the first unwound frame's base, its call window (HARO-CLONEDEEP-01) | K13 |
| K5 | `parentclassname(o)` answers the parent's name as Ring stores it, folded, `""` with none, Bad parameter type for anything else (Ring 1.27, meta_e.c; HARO-PARENTCLASSNAME-01) | K16, K17 |
| K6 | `systemcmd(cCommand)` answers what the command writes to its standard output, its last line end dropped; a .haro file calls it `SystemCmd`; no text is Bad parameter type (HARO-SYSTEMCMD-01 (a)) | K18, K19, K22 |
| K7 | a statement holding a node the parser's recovery put where nothing was written is refused; `a == b` names `==` (HARO-SYSTEMCMD-01 (b)) | K20, K21 |
| K8 | a program's output past its 64 KB buffer reaches a pipe whole and once: stdout is written streaming (HARO-PIPEWRITE-01) | K23 |
| K3 | `object2pointer(o)` is an OBJECTPOINTER, `pointer2object(p)` that same object, shared; two pointers to one object are equal; `ptrcmp` and `pointercompare` answer it, `obj2ptr` and `ptr2obj` are the short forms; anything else Bad parameter type!, as Ring's (HARO-OBJECT2POINTER-01, HARO-PTRCMP-01) | K05-K08, K10-K12 |

## How it is built

- **K1, the class of a subscript** (`compile.zig`, `exprClass`): an element class is a fact about positions. `aSeen[cKey]` with a text
  key answers an element or `""`, so unless the index is proven an integer the answer is the element class joined with text, and the
  name it lands in is a counted register. Before, a list whose every write was an integer made the read an uncounted integer register; the
  missing key's answer, the VM's static `empty_str`, was released from it once per missing key, its count reached zero, and `release`
  freed static memory -- the segfault stzlib met at 0x7ff75a000100, which came with the fork from Ring++.
- **K2, the checker** (`types.zig`, `checkCall`): the grammar cuts `return This.ScoreOf(pcNotes).ToSound()` into a bare `return`, a
  statement `This.ScoreOf(pcNotes)` whose LAST token is a lone `.`, and a statement `ToSound()`. The compiler re-reads the span and rejoins
  them (as HF-149 met for `return @nX`); the checker walks the raw tree, saw `ToSound()` unqualified and resolved it to the class's own.
  A call whose statement follows a lone `.` -- the last token of the statement before -- is left alone. `ts.zig` gains `prevSibling`,
  anonymous tokens included.
- **K3, two natives** (`main.zig`, beside `reference`): a C pointer of kind OBJECTPOINTER to the object, retained so the pointer never
  outlives it; back, the object as a shared reference (`rref = 1`, Ring's lNewRef, as `reference()` makes one). `valEq` compares two
  C pointers by what they point at.

## Measured

- **Before**, on haro 1dc5795: stzlib's `haro_keyed_release.ring` segfaulted in `release()`; `haro check` reported `haro/type-arity` at
  `haro_arity_receiver.ring` 4:32; `object2pointer` was R3 -- its name in `builtins.zig`'s list of Ring names, implemented nowhere.
- **Read off Ring 1.27**: the keyed loop prints `2`, `2`, an empty line and `done`; `type(object2pointer(o))` is OBJECTPOINTER,
  isPointer 1, a write through `pointer2object` reaches the original, two pointers to one object compare 1, `isNull` 0.
- **stzlib's own guard** `base/test/stats/stzDataSet_defects_narrated.ring`, which crashed after 41 assertions (its `_CategoryIds` is the
  K1 pattern). **CORRECTED 2026-11-08, second round**: the 185 of 185 first written here was measured on stzlib c4f6f85ea, a ref OLDER than the guard that reaches the MutualInformation loop, and named no ref -- stzlib's port caught it. At stzlib origin/main 4fdffce2c, after the second round, the guard passes 185 of 185 with its three MutualInformation scenarios run.

## The protections, each switched off (`plants.py`)

**The sixth round** (haro e56949e, ddcb88d, e63a4b5 fixtures; f29db68 code): HARO-SYSTEMCMD-01 from lookout, through central. (a) `systemcmd` is Ring's LIBRARY code (stdlibcore.ring: `System(cmd + "> " + tempname())`, the file read back, a last `\n` dropped), and Haro carries no part of Ring's library (D50), so it was R3: it is Haro's own native now (`syscmd.zig`), C's popen as Ring's `system()` runs the shell, read in binary; the desk's named divergence -- the whole last line end goes, where Ring's leaves a `\r` on Windows. (b) `a == b`: the parser's recovery put a MISSING identifier between the two `=`, and the compiler read it as a variable named "" (R24 naming nothing); a missing node now refuses its statement, naming `==`. **HARO-PIPEWRITE-01**, found reproducing HARO-CHECKPIPE-01 (stzlib-haroport: `haro check` through a pipe ended "error: WriteFailed"): not a reader closing early -- through `cat` the checker failed after 932 lines, and a PROGRAM's output through a pipe Git Bash makes, past the 64 KB buffer, was repeated and lost lines (20,000 printed, 557,632 carried, 12,925 distinct); a pipe Python or cmd.exe makes carried it whole, which is why no court saw it. Zig's file writer starts positional; every stdout writer is streaming now. K23 runs through Git Bash's pipe (NOT RUN where that bash is absent). Plants N18 to N23 caught; 23 of 23 cases.

**The fifth round** (haro b6aea26 fixtures, 66354e5 code): HARO-PARENTCLASSNAME-01, from stzlib's sound_mu3 guard (stzlib 44103f717): `parentclassname` raised R3. Built beside `classname`, on its op with c = 1, reading the class's parent; a report names it. Plants N15, N16, N17 caught.

**The fourth round** (haro 64a96b1 fixtures, 664fee2 code): HARO-ARITY-RECEIVER-02, stzlib's last arity error (stzResponsePlan.ring 445). When the method before ends `return ... > 0`, the grammar cuts a chained call that is a method's LAST statement: the lone `.` ends that statement inside the definition and the cut call is the definition's next sibling. K14 is a ten-line class that parses whole, K15 stzlib's probe as sent (its unclosed `if` kept). The check now descends to the statement before's last leaf; N3 re-pointed and N14 caught. 17 of 17 cases on both builds.

**The third round** (haro f1554fb fixture, 9b82974 code): HARO-CLONEDEEP-01. stzlib's stzObject guard crashed in `Summary()` -- the crash first looked like its IfQ scenario, whose line was still in the output buffer -- or hung. ddmin over its 17 scenarios found one, "AddTimeValue ... keep the elapsed time", and reading it gave K13, 31 lines and no library: an error raised inside `$aTV + This.T()` and caught outside. The append borrows `$aTV`'s list into a register uncounted and ends the borrow with a raw store the raise skipped; `forgetUnwound` cleared registers from the end of the handler's frame, but a callee's frame starts inside it, at the call window, so the borrow stayed and the next store there released it and freed the global's list. Clearing now starts at the first unwound frame's base. N13 caught; **12 of 12 plants**. stzlib's stzObject_defects_narrated.ring (4fdffce2c) passes 186 of 186, its DataSet guard 185 of 185; the 50-stage guard green (1,632 s).

**The second round** (haro 4b85327 fixtures, 47fced6 code, on stzlib's second report): a key the compiler cannot prove a text -- `"" + (anA[i] * 3 + anB[i])` is a ref, its operands may be objects -- reached the keyed read through an uncounted `vget`, and the static empty text was freed again (K09, stzlib's haro_keyed_release_arith.ring). The count that closes it was N2's, removed in the first round as idle because no case reached it: **a plant that moves no case says the cases are thin, not that the protection is idle** -- N2 is restored and caught by K09. `ptrcmp`, `pointercompare`, `obj2ptr`, `ptr2obj` added (K10-K12; N10-N12 caught). **11 of 11 plants** in all.

**7 of 7 caught** (first round): the keyed read's class (N1), the receiver call's lone `.` (N3), object2pointer's object check (N5), pointer2object's
kind check (N6), its shared reference (N7), pointer equality (N8), the OBJECTPOINTER kind (N9).

- **N2 removed, named**: a `vget` counted whenever the index was not proven an integer. The class of the read (N1) is what stops the
  crash -- the move into the now-counted register retains -- and switched off, nothing moved; the change is taken out.
- **N4 removed, named**: a lone `.` as the sibling of the receiver call's statement. The grammar puts it at the end of the statement before
  (N3), never there; taken out.
- **N6 missed first**: K07 passes a number, refused before the kind is asked; K08, a file's pointer (Ring's answer read off Ring 1.27),
  was written after the plants and catches it.

## The desk's readings, recorded as its own

- `valEq` compares any two C pointers by what they point at, not only object pointers: two values pointing at one thing are equal, as
  Ring's `=` on pointers is. Only object pointers are in a case.
- The object behind a pointer is retained and never released by the pointer: a pointer is kept by nothing Haro can see, so the object it
  names lives with the program, as on Ring.

## Not covered, named


- `strictEq`, the comparison `find()` and its kin use, is unchanged for C pointers.
- A checker that knows the receiver's class could judge `This.F().M()`'s arity; this one says nothing of it.
