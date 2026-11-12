# Haro v0.64 -- records

HARO-RECORD-01. TYPES.md T6 (D55): a record is `r`, "named fields fixed when it is made", its fields "checked when compiling: rUser.nmae
is refused with did you mean name"; v0.41's refusal of `:key = value` points at the record once records land. Asked how a record is
written, the Principal chose **"Declared, built in order"** (2026-11-12):

    record User
        tName
        iAge
    end

    rAda = User("ada", 36)
    print rAda.tName          # ada
    rAda.iAge = 37

The desk's readings are D76. Fixtures first (507d745: 13 cases, 12 failing before the code; R12, a `.ring` file, holds). R06 was changed
and R14 added after the court spoke, said so: R06 gave `rX` the literal `new P`, which v0.47's rule refuses when compiling, not when
running; R14 is that case now, and R06 gives the object through a function.

| line | what | cases |
|---|---|---|
| K1 | a record is a block of lettered fields ended by `end`, standing where a definition stands; built by its name, one value per field in order; its fields read and written by name | R01 |
| K2 | the number of values is checked when compiling, naming the fields in order | R02 |
| K3 | a field the record lacks is refused when compiling where the record is proven (a name given `User(...)`), naming the nearest field within two edits | R03, R04 |
| K4 | each value is checked against its field's letter where it is given | R05 |
| K5 | an `r` name holds a record and nothing else; an `o` name holds no record | R06, R07, R14 |
| K6 | a record is a value: assigning it copies it | R08 |
| K7 | `new User` is refused: a record is built by its name | R09 |
| K8 | a record holds no method | R10 |
| K9 | where the record is not proven, a missing field is NO_FIELD when running, naming the nearest | R11 |
| K10 | a `.ring` file is untouched: `record` is a name there | R12 |
| K11 | the refusal of `:key = value` names the record | R13 |

## How it is built

- `lift.zig`: `record Name` at a line's start is a definition: given to the parser as `class ` (six bytes for six), its row kept in the
  file's marks; a `def` or `func` inside it is the file's fault (R_RECDEF).
- `compile.zig`: a class on a record row is a record. `User(a, b)` in a `.haro` file builds it: `newobj` with the record's name index in
  b and c, each value checked against its field's letter and stored in its slot. `recvClass` proves the record a `User(...)` call makes,
  so a missing field is refused where the record is proven; `new User` and a method are refused; `r` is a checked letter.
- `main.zig`: an object carries its record's name (`Obj.rec`, 0 for no record), and a copy keeps it; `r` holds a record, `o` no record;
  a by-name read or write of a field a record lacks is NO_FIELD, naming the nearest field (`nameDistance`, within two edits).

## Changed by the ruling, said so

- v0.41's S06 and S13: the refusal of `:key = value` now ends "or declare a record for named fields".
- v0.47's Y09: `rUser`, written to show a letter not yet built, is `sUser` -- `r` is checked since v0.64.
