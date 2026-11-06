# Haro v0.37 -- the error value, `catch e`, and the cause (D52 rung 2)

stzlib-security's A4, as D52 amended it, and the half of A1 the last rung left open. Fixtures first: `fixtures.json` and `cases/` (4f32d59), then the VM
(`vm/src/main.zig`), the compiler (`compile.zig`), the lift (`lift.zig`) and the printer (`fmt.zig`).

## What a program sees

    try
        ...
    catch e                   e is bound -- as catch(e) is -- when it stands on catch's own line
        ? "caught: " + e      the message, byte for byte: every text use of e is what it was
        ? e.Message()         the message, a plain string
        ? e.Code()            Ring's code of an error the VM raised (R2, R14 ...); "" for raise()
        ? e.Span()[:line]     where it was raised: a list with :file and :line
        ? e.Cause()           the error a raise in a finally replaced; "" when nothing was held
    done

| line | says | cases |
|---|---|---|
| E1 | `catch e` binds e, only when e is on catch's line; a name on the next line is the statement it always was | G01-G05 |
| E2 | in a text context the error is its message, byte for byte; assigned, passed and returned as itself | G06, G25, G26 |
| E3 | `Message()` the plain message; `Code()` Ring's code or ""; the names in any case; no argument | G07-G10, G29 |
| E4 | `Span()` the file and line where it was raised; a rethrow, `raise(e)` included, keeps its origin | G11-G14, G30 |
| E5 | `Cause()` the held error a raise in `finally` replaced -- of the body or the handler -- chained, never a loop | G15-G22, G28 |
| E6 | the methods belong to the error: a plain string, one made from an error, or the variable whose string was raised, refuses them | G23, G24, G27 |
| E7 | `haro fmt` prints `catch e` as `catch(e)` | K01 |

## How it is held

- **An error is a string.** A handler receives the message as a Ring string, so nothing that reads it changes: stzlib's 517 reads of `cCatchError`
  migrate to `e` by a rename. Its header's four spare bytes (a `Str` is 24 bytes before and after) hold 1 + the index of an ERROR RECORD: the file
  and line where it was raised, its cause, and whether `raise()` made it. Every other string holds 0.
- **Made at the landing.** Every handler landing (ten places in the VM) turns the error into an error value before the unwind moves the frame, so
  the place is the raise's. A string already an error keeps its record -- a rethrow, and `raise(e)` (the desk's reading: it is a rethrow). A fresh
  string nobody holds is marked in place; one held elsewhere (a variable's, a constant's) is copied, so the mark never reaches another holder (G27).
- **The record lives as long as its string**: freeing the string frees the record and releases its cause.
- **The methods** are answered where a method call on a non-object already fails (`callm`), so no path that worked before does one more thing.
  A string made FROM an error (`e + ""`) is a new string, a plain one.
- **The cause.** A `finally` on an error path -- the body raised and there is no catch, or the handler raised -- runs under a handler of its own;
  if it raises, that landing attaches the held error as the new one's cause and raises on (`trap` with d = 1 + the held register). A cause is set
  once and never forms a loop (G28). An error a handler HANDLED is not held (G19); a held RETURN is not an error (G20).
- **`catch e`** is lifted before the parse, as `not` already is: `catch e` with e alone on catch's line becomes `catch(e)`, the form the grammar
  reads as a binding. The census counts the sites (`lift.catch_sites`). `haro fmt` reads the same shape and prints `catch(e)`: printed as a
  statement on the next line, as it was, it would now change what the program means.
- **Found in passing, fixed:** a VM error a `finally` raised again and nothing caught was reported as `In raise()` (since v0.36 and before it, on
  the no-catch path). The record remembers what made the error, and the report says so (G30).

## Not covered, named

- **An error crossing an eval string** arrives as its message: the eval's run returns text, and the outer landing makes a new error at the eval's
  line. `catch e` INSIDE an eval string is not lifted (the eval compiles its own parse, as it does for `not`).
- **The uncaught report's line** for a rethrow is where it was raised again, not where it began (G30 pins it as it is); `Span()` has the origin.
- **The record's release** is a memory protection, not an answer: switched off, every case still prints the same bytes (a record would leak). No
  case can see it.
- `cCatchError` outside a handler stays readable (ruling 2): refusing it waits on stzlib's sweep reading 0, and is rung (4)'s `haro/last-error-read`.
