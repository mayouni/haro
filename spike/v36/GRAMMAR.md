# Haro v0.36 -- `finally` on every exit (D52 rung 1, A1 completed)

stzlib-security's A1 (SOFTANZA_ONE_HOUR.md section 3, stzlib origin/main 0a311d01b), adopted as D52 with its semantics lines whole. This rung builds them in the
surface `haro` compiles today. Fixtures first: `fixtures.json` and `cases/` (63b5c94), then the compiler (`vm/src/compile.zig`, `tryStmt` and the jumps).

## The semantics, as the VM now holds them

    try
        ...                  the body
    catch                    or catch(e); optional when finally is present
        ...                  the handler
    finally
        ...                  runs after the body or the handler, on EVERY exit
    done

| line | says | cases |
|---|---|---|
| S1 | the `finally` runs exactly once per entry of the `try` | F01, F12, F13, F24 |
| S2 | a `return` in the body or the handler is held: its value is taken, the `finally` runs, the value taken is returned | F04, F05, F10, F19, F20, F22, F23 |
| S3 | a raise in the body or the handler is held: the `finally` runs, the raise resumes outward | F02, F03, F06, F14 |
| S4 | a raise in the `finally` replaces the held exit; so does a `return` in it (the desk's reading, below) | F12, F13, F15, F16 |
| S5 | `exit` and `loop` crossing a `try` run its `finally` first, innermost first when they cross several | F07, F08, F09, F11, F17, F18, F21 |

**Before this rung**, measured on haro 52d53b9: the normal path, a caught raise, an uncaught raise and S4's raise already held (F01, F02, F03, F16). Missing:
S2 entirely, S5 entirely, S3 for a raise in the HANDLER (F06), and one defect no line names: a `try` inside a `finally` overwrote the error the `finally`
was holding, so the wrong error was raised again (F14 printed "outer caught: inner"). The last two were not in D52's probes; the fixtures found them.

## How it is compiled

- **A region** is a `try` body whose `try` has a `finally`, or the handler of such a `try`. The compiler keeps the open regions, innermost last, each
  with the state OUTSIDE it: the open `try` bodies and the open catches.
- **A jump** (`return`, `exit`, `loop`) leaving regions compiles, innermost first: leave the `try` bodies down to the region (`pend`), then that region's
  `finally`, again, at the jump; last, leave the bodies down to the target. The `finally` is compiled in its own `try`'s outside state, so a raise in it
  goes outward and never to its own handler (it runs once: F12, F13), and a jump in it does not cross it again (F15).
- **A `return`'s value** is taken first (an error in it is the `try`'s to catch, F-90) and held in a register the `finally` blocks compiled on the way out
  may not reuse (F04). An eval string's `return` halts its nested run; it compiles the way out only when a `finally` is open (F23), so every eval
  without one is the code it was.
- **A loop** records the regions open at its entry, so an `exit` inside a `try` body leaves only what it crosses (F24).
- **The handler of a `try` with a `finally`** is a protected region of its own: a raise in it is held in its own register while the `finally` runs, then
  raised again keeping its origin (F06); a jump out of it runs the `finally` (F05, F21).
- **Each handler's error register is named by the open `try` statements**, in any of their parts, not by the open catches: a `finally` is compiled
  outside its catch, so the old naming gave a `try` inside it the register of the error it was holding (F14).
- **The cost** is code, not time: each jump that crosses a `finally` carries a copy of it. stzlib writes no `finally` today, so its code is unchanged in
  size; a `try` nested in another's body or `finally` now takes an error register of its own, as one nested in a catch already did.

## The desk's reading, recorded under D52

A `return` inside `finally` replaces the held exit -- a held return (F15) or a held raise (F16), which is then lost. A1 names only a raise replacing a held
exit; a return doing the same is the consistent reading, and the one Java, C# and Python made. A held raise lost this way is a defect to warn about, not a
semantics to forbid: it belongs with the five checker rules (rung 4), not here.

## Not covered, named

- **The cause** of a replaced error (S4's second half): rung (2), which needs the error value.
- **`catch e` without parentheses**: rung (2). `catch(e)` binds the message today, and works with every case above (F22).
- **`bye` inside a `try`**: A1 does not list it; it ends the process and runs no `finally`.
- **A function whose locals share registers** (its locals overflow the window, `shareFunction`): no case is that large. Sharing is decided by source
  stretches, and a `finally` compiled at a jump runs its statements where the jump is; the reasoning that it holds is in the account, unmeasured.
- **A borrow left open in a handler** that raises, under a `finally`: the second landing ends it with the same helper the first landing uses
  (`forgetBorrows`); no case pins it on its own.
