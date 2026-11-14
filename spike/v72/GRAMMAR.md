# Haro v0.72 -- the language of doors and the place

`doc/DOORS.md`, its first rung (D87, D88, D89): a program declares the folders it opens, once, as a sentence of Haro's standard
language of doors; an outside text is judged against one of them into a place; and a door of the filesystem takes a place.

    load "doors.haro"                                                   # Haro's standard language of doors
    sDoors = doors'DEFINE ROOT data AS (AT "data", ALLOWS [read, list]) RATIONALE "the notes this program reads"'
    hNote = sDoors.Place("data", tGiven)                                # judged: a place beneath the root, or a refusal
    print Read(hNote)                                                   # the door takes the place

Fixtures first (8e0a6df: 14 cases, 1 of 14 before the code). The judge in Haro 0404225; the loader, the compiler and the VM ffc90ae;
four cases the plants called for, the plants and stage 77 in 8220562 and 7893527.

| line | what | cases |
|---|---|---|
| L1 | `load "doors.haro"` is Haro's standard language of doors, found wherever the program stands, by where it stands; a sentence of it declares roots; a declaration a program loads is no code | D01, D17, D18 |
| L2 | `sDoors.Place(root, text)` answers a place: its root, its path beneath the root made plain, what the root allows; it prints as its path; the letter `h` holds it; a sentence of another language judges none (PLACE_NO_DOORS) | D01, D02, D15 |
| L3 | a text that leaves its root is PLACE_ESCAPES; a name a place cannot hold is PLACE_NAME | D03, D04 |
| L4 | a root the sentence does not declare is ROOT_UNKNOWN, and the refusal names the roots it does declare | D05 |
| L5 | a root ANYWHERE takes the file a person names, wherever it is, and reads only | D06 |
| L6 | the declaration's court: a root with no folder that does not say ANYWHERE (ROOT_NOWHERE), one that says both (ROOT_TWICE), one ANYWHERE that lists what it allows (ROOT_ANYWHERE_READS), a permission outside the four (UNKNOWN_PERMISSION) -- each refused when the program is compiled, its verdict the standalone court's | D07 |
| L7 | a door takes a place: `Read`, `FExists`, `DirExists`, `Dir`, `Write` and `Remove`, each asking its own permission of the root, or PLACE_NOT_ALLOWED | D08, D09, D10, D16 |
| L8 | the door checks again where it opens: a link beneath the root that leads out of it is PLACE_ESCAPES at the door | D11 |
| L9 | a place is made by its judge alone, and is not written into (PLACE_FIXED) | D12, D13 |
| L10 | a door still takes text as it did: the rung refuses nothing that ran | D14 |

## The spellings (this desk's, under D84)

- **The language `doors`**, in `spike/doors.haro`, loaded by its file's name from any folder. Its one kind in this rung is **ROOT**:
  `AT "folder"` names where it stands; `ANYWHERE yes` says it has no folder; `ALLOWS [read, write, list, remove]` says what may be
  done beneath it. A root that lists nothing reads.
- **The judge `Place(root, text)`**, a method of a sentence of doors. Its answer is a place: `Root()`, `Path()`, `Allows()`; printed,
  it is its path.
- **The letter `h`** holds a place: it is T7's handle of the filesystem, held before the door is opened.
- **What each door asks**: `Read`, `FExists` and `DirExists` ask read; `Dir` asks list; `Write` asks write; `Remove` asks remove.

## What the judge reads in a text

- Either slash is one separator; `.` is dropped; `..` is taken where it stays inside the root, and refused where it steps out.
- **PLACE_ESCAPES**: a step back out of the root, a rooted path, a drive, a share, a scheme.
- **PLACE_NAME**: nothing, a control byte, a device's name (`con`, `nul`, `com1` ... with any extension), a name that ends with a dot
  or a blank, a colon or a wildcard in a name.
- **A root ANYWHERE** has no folder to leave: it takes a rooted path and a drive, keeps the rules of names, and allows read alone.
- The rules are the same on every platform, so a program judged on one is judged alike on another.

## How it is built

- **The standard language is found last.** The loader and the compiler look for a loaded file beside the program, in the working
  folder, beside haro and in its `load` folder, as they did, and then in the forge's folder. A file named `doors.haro` beside the
  program is the program's, and one loaded from a folder of the program is another file (D17).
- **A forged court's libraries are found there too.** The court of doors loads `expr_lib.haro`, `world_lib.haro` and
  `needs_lib.haro` besides its court library, each from the forge's folder. The forwarding files v0.70 wrote beside a forged court
  are taken out: one mechanism finds a court's libraries.
- **The judge is Haro code** (`judge_lib.haro`, `HaroPlaceOf`): it reads the roots the sentence declares through the sentence's own
  court, judges the text, and makes a `HaroPlace` -- the root's name, its folder, the path made plain, what it allows.
- **The VM knows a place by its class**, as it knows a sentence: it prints as its path, the letter `h` holds it, a write into it is
  PLACE_FIXED, and `new` of one is refused by the compiler outside the judging library.
- **At the door** the VM asks, in order: does the root allow what this door does (PLACE_NOT_ALLOWED); does what the path leads to,
  asked of the platform, stand beneath the root's folder (PLACE_ESCAPES) -- the path itself where it exists, else the nearest folder
  above it that does; then the door takes the path as it takes any text. A root ANYWHERE has no folder to compare with.

## What the rung found

- **The plants called for four cases**, each added after the code and said so in the generator. The judge's first refusal, a place
  asked of a sentence of another language, stood in no case (D15). No root of the cases withheld read or list, so a door that asked
  the wrong permission failed nothing, and `DirExists` stood in no case (D16). The compiler's look in the forge's folder failed
  nothing, because a load is also matched by the end of its name: two loaded files that end alike say which is which (D17). The
  report of a load that cannot be opened read the loaded declaration as code (D18).
- **Two mechanisms did one job.** With the forwarding files switched off the court's libraries were found in the forge's folder,
  and with that look switched off for them the forwarding files answered: neither plant could be caught. The forwarding files are
  taken out, and the plant of the one mechanism left fails every case.
- **Two lines of the judge no case could fail were taken out.** A root ANYWHERE that lists what it allows is no sentence of doors,
  so the judge never meets one; under ANYWHERE a scheme is refused by the colon rule. Each rule stands in one place.
- **A plant that broke the whole declaration proved nothing.** It failed fifteen cases for not forging; sharpened to a fifth
  permission, it fails the one case that types the four.

## Measured

- The court: 18 of 18 on both builds. 30 plants, each caught by its fixture: K1-K13 in `vm/src`, each built; J1-J13 in the judge
  and M1-M4 in the declaration of doors, where nothing is built (`plants.py`).
- The courts of v0.70 and v0.71 hold on v0.72's builds: 15 of 15, 14 of 14.
- stzlib origin/main 2a5b3ca7f, its 204 landed `.haro` files, `haro check` of each alone, v0.71 against v0.72: 1,498 errors before and after, no file changes; no file there loads a declaration or names the class of a place
- The 77-stage guard on builds made from the commit: 77 stages green, 0 failures, 3,264 s on a machine running on battery; stage 6, the cold-load timing, read 143.8 ms, under the 150 ms ceiling. A first run stopped in stage 1 when the machine went into standby; nothing of it is counted

## What stands at its present size

- `Place` reads the sentence's roots through its court at each call.
- Six doors take a place: `Read`, `FExists`, `DirExists`, `Dir`, `Write`, `Remove`. `FOpen`, `Rename` and the other built-ins of
  files take text, as every door still does until `unjudged` is built (DOORS.md rung 4).
- The second check asks the platform where the path leads at the moment the door opens.
- A haro that stands outside the repository's `vm/` finds the standard language by `HARO_HOME`.
- COMMAND and the invocation are DOORS.md's next rung; PEER and the endpoint the one after.
