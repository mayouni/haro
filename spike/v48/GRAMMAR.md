# Haro v0.48 -- a built-in is spelled as Softanza writes a name (D58)

The Principal, 2026-11-09, reading `parentclassname` in this desk's exchange with stzlib's port: "It can been easily manged by AI but for a
human reader it's better to be ParentClassName or at least parent_class_name". Asked with the history -- their own ruling of 2026-11-07
for v0.42 was "Lowercase (Recommended)", after a count of 433 calls -- and three options (ParentClassName, keep lowercase,
parent_class_name), they chose **"ParentClassName"**. It revises v0.42's line N4. The table of spellings and the order of the work are the
desk's, under the Principal's "I let you decide" (2026-11-09). Fixtures first (542edea: 8 cases, 2 holding; P08 corrected before its
code passed -- its own `eval()` was the lowercase the rule refuses first; P09 written after the code and before the plants, 02d4996).

| line | what | cases |
|---|---|---|
| P1 | in a `.haro` file a built-in -- one of Ring's 258 or one of the VM's own 19 -- is called by one spelling, Softanza's casing (`Len`, `IsNull`, `SubStr`, `ParentClassName`); any other spelling, lowercase included, is refused when compiling, naming the one to write | P01, P02, P03 |
| P2 | a built-in registered with an underscore is reached by its spelling without one (`tui_size` is `TUISize`), and a spelling of it in another case is refused naming it | P04, P05, P09 |
| P3 | a program's own function of a built-in's name is the program's, as Ring has it; a `.ring` file reads every spelling as Ring does | P06, P07 |
| P4 | an eval in a `.haro` program spells a built-in as the root does | P08 |

## The table

`study/v48/builtin_names.py` holds every split, written by hand once: the name is cut into the English words it is made of and each
word is capitalised -- `parentclassname` ParentClassName, `isnull` IsNull, `substr` SubStr (Ring's own word, sub-string), `addattribute`
AddAttribute; a digit stays where it stands and starts no word (`list2str` List2Str, `atan2` ATan2, `log10` Log10); a C library name keeps
C's reading with each part a word (`fopen` FOpen, `fgetc` FGetC, `ungetc` UnGetC, `clearerr` ClearErr, `perror` PError, `fabs` FAbs);
Ring's internal prefixes are words (`ring_state_new` RingStateNew, `ringvm_callfunc` RingVMCallFunc) and the underscore goes, as no other
Softanza name carries one; the VM's own natives follow the same rule (`AdmitApp`, `TUIInit`, `WebServe`). `--zig` writes the array
`builtins.pascal` (277 entries); the file says it is generated.

## How it is built

- **The check** (`compile.zig`, `spellNative`): in a `.haro` statement a call that resolves to a native -- after the program's own
  functions, which come first as Ring has it -- is looked up by the native it RESOLVED to, and refused unless written as the table says:
  "a built-in is spelled `IsNull`; written `isNull`". The statement is compiled to a trap, as every spelling fault since v0.42.
- **An underscore native** (`builtins.underscoreOf`): a `.haro` call whose name matches, in any case, a native registered with an
  underscore reaches that native; the check then names its one spelling.
- **The yes-or-no natives** (`yesNoNative`): their boolean answer in a `.haro` file was keyed to the lowercase spelling; it folds case now,
  so `IsNull(null)` is `true`.
- A report still names a built-in as the VM registers it (`In len() in file ...`): the desk's reading, recorded.

## Haro's own code, re-spelled

`study/v48/respell.py` (a tool's commit, 20fc236, listed apart for stage 24): every call of a built-in in Haro's libraries and tools,
2,172 calls, not a member call, not a name the file defines as its own function, never inside a string. The `.haro` cases of v36, v37,
v38, v41, v42, v43, v44 and v47 were re-spelled after their courts spoke (`study/v47/port_cases.py --respell`), each generator saying so.
By hand: v42's N07 keeps `isNull`, its subject, and now names `IsNull`; v44's Q02 evaluates its expressions in a `.haro` program, so they
are `Log(-1)`, `ACos(2)`; v29's two plant texts quote the library. The forge writes no native call into a court.

## Measured

- **The court**: 9 of 9 on haro and its checked build. The ten courts of v36 to v48 green on both builds.
- **Plants, 5 of 5** (`plants.py`): B1 any spelling passes, B2 no underscore resolution, B3 the spelling looked up by the name written,
  B4 a yes-or-no answer only in lowercase, B5 the check reaches a `.ring` file (MISSED first: the guard inside the check and the one at
  its call site each keep a `.ring` file out alone; B5 switches both). v42's P4 re-pointed at the new call, caught.
- **The census** (`study/v47/census.py`): before the re-spelling the compiler refused 118 statements of Haro's code for a built-in's
  spelling; after, none outside the cases that test it.

## Named

- `haro check` does not judge the spelling yet (types.zig lowers every name); nor the letters (v0.47).
- An engine native (Softanza's, loaded from its DLLs) is not in the table: it is called from Softanza's `.ring` code.
- A report names the built-in as the VM registers it, in lowercase.
