# Haro v0.55 -- one form for each construct

HARO-ONEFORM-01. The Principal, 2026-11-11, in this desk's chat: "Ring uses different keywords to end a block (ok, end, }, off, done...).
I want Hero to end this chao and do not enherit it. Opt for a strict one form. Try to identify any simular issue and solve it." The choice
of each form is delegated; the desk's choices are D67: the word that says what the construct does, and among equals the one Haro's own
code already writes. A `.ring` file reads every spelling as it always has.

Fixtures first (845d588: 29 cases, 27 failing before the code; O28, the one forms together, and O29, a `.ring` file, hold and guard; O30
added before the code, 48bd6e4). Code d59e84d; haroport's rule O be72c33; Haro's code rewritten 16e50a0 (a tool commit).

## The table

| line | the one form | refused in a `.haro` file | cases |
|---|---|---|---|
| F1 | every block ends with `end`: if, while, for, switch, try, within, using | ok, next, off, done, endif, endwhile, endfor, endswitch, endtry; a block's braces | O01-O08, O30 |
| F2 | a definition -- func, class, package -- has no end word: it ends where the next begins | end, endfunc, endfunction, endclass, endpackage; a definition's braces | O09-O11 |
| F3 | func, elseif, else, case, for, see, give, exit, loop, and, or, not, from, `#`, this | def, function, but, other, on, foreach, put, get, break, continue, &&, \|\|, !, `:` and `<` before a parent, //, self outside a brace object | O12-O24 |
| F4 | a definition's parameters in parentheses, `func Add(iA, iB)`; none without, `func Main` | `func f a, b`; `func f()` | O25, O26 |
| F5 | a statement has no trailing period | `g().` | O27 |
| F6 | kept, each a different construct: `?` (a line) beside `see`; the three quote marks; /* */; self inside a brace object; `do ... again` | -- | O28, O29 |

Found by counting each spelling in Haro's own code and in stzlib 4e354d7cc's library (`runtime/v55/count_forms.py`, `count_more.py`):
stzlib writes `ok` 55,278 times, `next` 19,108, `but` 6,057, `def` 71,281 against `func` 18,163, braces around blocks 2,050, `//` 1,425;
Haro's code wrote `ok` 2,594, `next` 720, `but` 267, `done` 237.

## How it is built

- `compile.zig`: `oneForm` walks each statement of a `.haro` file with the keyword walk (v0.41): a block statement's last token is `end`,
  its braces refused; `oneWord` names the one spelling of a word that has others; `self` is refused outside a brace object; a statement's
  trailing period is refused. `defForm` reads a definition's own words -- for the function and every class and package around it -- when
  the function is entered; its fault is the function's first statement's, as a parameter's shape is (v0.47).
- `lift.zig`: `within` and `using` close with `end`. The grammar reads that `end` as the end of the definition around them; the lift's
  token walk counts every block statement's first and last token, and an end word a definition took, so each `end` closes its own block.

## Measured

- The court: 30 of 30 on haro and its checked build; plants N1-N16 caught, each failing its own case.
- Stage 6, the cold compile, alternating A (v0.54, built from cb61195) and B (v0.55), minima of 15 runs over 4 rounds
  (`study/v55/stage6_ab.py`): with a second walk per statement B-A was +3.0 ms (154.8 against 157.8); with the keyword walk (v0.41) folded
  into the one-form walk, -0.6 ms (155.2 against 154.6), inside the rounds' spread. The machine reads v0.54 above stage 6's 150 ms
  ceiling today, as at v0.50.
- A count by the lowercase word overstates a `.haro` file: `on` 136 and `other` 18 in Haro's code were names (`oN`, `Other`); in a `.haro`
  file a keyword is lowercase exactly (v0.41), so rule O matches the word exactly, and a `.ring` file's keywords are lowered first (K).

- stzlib 4e354d7cc ported by haroport (rounds 1-3 and rule O, `--unit base/stzBase.ring`, 2 min 37 s; 189,633 rewrites of rule O) compiles 126,749 of 140,799 statements on v0.55 (90%), where round 2 alone compiled 107,027 of 140,743 (76%). Rule O leaves 77 sites: 34 one-line definitions `def Width()   return x`, whose body stands on the definition's line, so taking `()` away leaves the body read as parameters; 32 bare parameter lists of the same shape; and 11 statements the grammar reads as a call ending in a period followed by another statement (`oCanvas.AddPolylineQ([ ... ,` across lines `]).StrokeQ(...)`, base/graphics/stzTreeCanvas.ring 183) -- a misreading v0.54 compiled silently and v0.55 refuses.

## Haro's code, and haroport's rule O

`study/v55/oneform.py` rewrote Haro's own code by haroport's rule O (a tool commit, listed in `spike/v20/tool_commits.txt`): every block's
end word, a definition's parameters, `def`. A definition's end word goes and leaves its line, so every line keeps its number. Earlier
rungs' cases that wrote the other forms were rewritten with it, their expected bytes unchanged. Two cases hold code inside a string, which
the tool leaves as text, and an eval in a `.haro` program reads by Haro's rules: v36's F23 and v38's U12 had their `done` written `end` by
hand, by the ruling, after their courts refused it.

`port/haroport.py`'s rule O writes a ported tree in the one forms: blocks matched lexically, in document order, each block word opening
and each end word or block brace closing; an end word with no block open is a definition's and goes. H28-H30, written after the rule's
code (said so), 30 of 30, plants T33-T43 caught; H01, H03 and H23 expect the one forms now, by the ruling.

## Named

- A definition's words are read when the function is entered and reported at its first statement: a function with no statement reports none.
- A comment between two top-level statements of the program's main body is read where it stands beside a definition only.
- `;` between two statements on one line, and `new P()` beside `new P`, are not refused: each is one construct written two ways, named here
  for a later rung.
