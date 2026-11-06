# Haro v0.40 -- the doors a language's worlds may open (D51's declared half)

stzlib-security's A6, as D51 decided it: what nothing declared in is out by construction, one floor above Harobanda. Fixtures first
(`fixtures.json`, `court_cases.json`, `door_v40.haro`, `door/`: 661f41b), then the meta-court (`haro_lib.haro`), the forge (`forge.haro`), the
court (`court_lib.haro`) and its new library (`needs_lib.haro`).

## What a declaration says

    DEFINE LANGUAGE door AS (VERSION "0.40", GRAMMAR "0.40", COURT "...", EXTENSION ".door", NEEDS [network, process]) RATIONALE "..."
    DEFINE MENU caps AS (WORDS [network, process, filesystem], MESSAGE "...") RATIONALE "..."
    DEFINE DECLARATION listener AS (VERB "LISTENER", SEATS [host: text?], OPENS network) RATIONALE "..."
    DEFINE DECLARATION service AS (VERB "SERVICE", SEATS [needs: [caps]?], OPENS needs) RATIONALE "..."

The words are the closed catalog of nine: filesystem, process, network, environment, dynamic_load, gpio, threads, clock, inference.

| line | says | fixtures |
|---|---|---|
| D1 | `NEEDS [..]` on the LANGUAGE: words of the nine, each once | A1, R1, R2 |
| D2 | `OPENS word` on a DECLARATION: a capability, or a seat of the kind typed by a MENU of capabilities | A1, A3, R6, R7, R8, R9 |
| D3 | a kind opening a door the LANGUAGE does not NEED is refused -- A6's gate: the language is refused, so no grammar is forged and a listener cannot be parsed; a NEEDS word no kind can open is refused (a word of an OPENS seat's MENU counts) | R3, R5, A1 |
| D4 | a kind that OPENS in a language that NEEDS nothing is refused; a language with neither is exactly what it was | R4, A2, stage 45's byte check |
| D5 | the forged court refuses a sentence whose OPENS seat lists a door the language does not NEED (`CAPABILITY_NOT_NEEDED`) | D2, D3, D4 |
| D6 | the court's `world` publishes what each declaration opens, for the consumer that enforces it | D5, D6, D7 |

## How it is built

- **The meta-court** reads NEEDS (a namelist) and OPENS (one word) and judges them after the whole file is read. Its verdict prints `needs` and
  `opens VERB:word,...` only for a language that NEEDS, so every other verdict keeps its bytes.
- **The forge** writes the doors as a 25th element of the language entry, `[[needs...], [[verb, word, by seat], ...]]`, only where the language
  NEEDS (the 24th, the patterns, is then written empty when there are none, and the court calls the pattern judge only for a non-empty one). A
  court whose language NEEDS loads `needs_lib.haro`, and the world library even without a WORLD, so it can publish; no other court changes --
  stage 45 forges panel_v35.haro and compares its court and grammar with the committed ones, byte for byte.
- **The court** judges an OPENS seat's values after every value has its shape (a word outside the MENU is the MENU's refusal, D4) and publishes
  `"opens": [{"verb", "name", "opens", "span"}]` after the symbols and the refs; a kind that opens a seat and lists nothing publishes `"opens": []`.

## The desk's readings, recorded as its own

- OPENS takes one word: a kind that opens two doors is two kinds, or a seat.
- A word that is both a capability and a seat of the kind is read as the capability.
- An OPENS seat's MENU may list a door the language does not NEED; the sentence that uses it is refused (D5), so one MENU can serve languages
  that need different doors.
- Enforcement is the consumer's: Haro proves the declaration and publishes the doors; it claims nothing about a door it does not run.

## Found on the way

- `aNd` is the keyword `and` -- the keywords are case-insensitive -- so a variable of that name made the statement around it an ERROR node, which
  the compiler refused and the forge met as an uninitialized name. Renamed; nothing in the language changed.
- A language with no WORLD carried the world stub, which refuses `world` outright; a language that NEEDS has something to publish, so its court
  carries the world library.

## Not covered, named

- The second altitude -- `NEEDS` on a program unit, refused at compile against the natives it calls -- waits on the map from native families to the
  nine, which waits on W7's measurement (D51, ruling 3).
- The court publishes the doors; Harobanda's PID 1 (COMPASS-KERN-02's generated filter) is the consumer that enforces them, and is not built here.
