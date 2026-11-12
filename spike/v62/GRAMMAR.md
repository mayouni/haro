# Haro v0.62 -- two silent defects: a boolean to a native, an object through a pointer

Two findings of 2026-11-12, each a wrong answer with no error, ruled on by the desk (D74).

**HARO-NATIVE-BOOL-01** (stzlib-haroport). A `.haro` `true` given to an engine native crossed as nothing, and the native read its flag as
0: `StzEngineStringReplaceCS(xS, "mm", "30", true)` ran case-insensitive, and stzDateTime printed 10:03 for 10:30 (34 assertions). Where a
value crosses to a native, a boolean is now the number 1 or 0 -- an argument, and an item of a list the native reads. v0.53 made a native's 1
or 0 a boolean where a `.haro` file wants one; this is the way out.

**HARO-THISCHAIN-01** (stzlib-security). Inside a method, `This.Route().Revoke()` -- `Route` answering `Pointer2Object` of a stored
pointer -- did not reach the object: a capability revocation was lost. Reduced by this desk to a function and a global, and measured on a
build that printed the count: a callee's frame begins inside its caller's (the caller's argument registers are the callee's first), and
the count of Ring's named holders walked each live frame to its full size, so a temporary in the overlap was taken off twice. The object's
one named holder read as none, and Ring's rule (a reference with one holder is copied when assigned) copied it. Each frame is now walked
only up to where the next begins. A VM defect: `.ring` and `.haro` alike.

Fixtures first: 41c9ffb (B01-B06, 5 failing before the code), 02ed068 (C01-C04, written after B's code and before C's, 3 failing).

| line | what | cases |
|---|---|---|
| N1 | a boolean argument reaches a native as 1 or 0 | B01-B03 |
| N2 | the finding on the engine: ReplaceCS with `true` is case-sensitive, with `false` is not | B04 |
| N3 | a boolean inside a list reaches a native as 1 or 0 | B05 |
| N4 | a `.ring` file passes its numbers as it did | B06 |
| N5 | an object reached by `Pointer2Object` in a function, a method, or a chain through `this` is that object | C01, C02, C04 |
| N6 | an object assigned with no reference is still copied | C03 |

B04 and B05 load Softanza's engine from `STZ_ENGINE_DIR`; the court names them NOT RUN where it names no engine.

## How it is built

- `main.zig`: a native call's arguments, and the host's list readers (`hostListTag`, `hostListNum`), read a boolean as the integer it holds.
- `main.zig`, `ringHolders`: frame k is walked up to the base of frame k+1's own registers.
