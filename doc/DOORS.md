# What a door takes -- places, endpoints and invocations

**Status: a proposal (HARO-DOORS-01), written 2026-11-14 on the Principal's word. Asked how `unjudged` should be brought in -- staged,
enforced at once, or after the languages its refusals need -- he answered "Option 3": design the languages for paths, hosts and
commands first, then build `unjudged` whole (CHARTER D87). RULED the same day: "Yes, as recommended" -- the five parts of section 7,
each as this document recommends (CHARTER D88). Rung 1 is built, 2026-11-14, as v0.72 (CHARTER D89, `spike/v72/GRAMMAR.md`): the language `doors`, ROOT, the judge `Place`, and six doors of the filesystem taking a place. Rung 2 is built the same day, as v0.73 (CHARTER D90, `spike/v73/GRAMMAR.md`): COMMAND (RUNS or ITSELF, TAKES, IN, QUIET), the judge `Invocation`, and `System` and `SystemCmd` taking an invocation with no shell; the refusal of a command line built as text is its next step. Rungs 3 to 5 are designed here.**

## 0. The question

TYPES.md T7, ruled in D55 (h): text that came through a door is `unjudged`, and may not be run as code, become a sentence without its
court, or **be given to a door as its argument -- a path, a host, a command**. The last part cannot be built alone. A program's command
line is outside text, and this line stands in every court Haro forges:

    tSrc = Read(sysargv[4])

Refusing it is right only if the program has a way to make a door's argument out of what a person typed. This document designs that
way: what a program declares, what judges the text, what the door then takes.

## 1. What exists, measured

Read on haro b058cc4 and stzlib origin/main 8221cdcfd (its 195 landed `.haro` files), 2026-11-14, by search over the source.

| | Haro's own code (`spike`, `port`) | stzlib's landed `.haro` files |
|---|---|---|
| files read and written | `Read` 33, `Write` 8, `FWrite` 5, `FOpen` 1, `Remove` 1 | `Write` 81, `Read` 68, `Remove` 24, `FWrite` 9, `Dir` 2 |
| asked whether they exist | `FExists` 9 | `FExists` 138, `DirExists` 2 |
| libraries loaded | `LoadLib` 2 | `LoadLib` 103 |
| the environment read | `SysGet` 3 | `SysGet` 32 |
| programs run | `SystemCmd` 2, `System` 1 | `System` 12, `SystemCmd` 1 |
| the command line | 15 `Read(sysargv[...])` in 5 files, 8 of them in `court_lib.haro` | 19 uses of `sysargv` |
| text run as code | none | 1 `Eval` (`common/stzFuncs.haro`) |

What Haro already judges:

- **The nine doors** (D51, v0.40): filesystem, process, network, environment, dynamic_load, gpio, threads, clock, inference. A
  language says which it NEEDS, a kind which it OPENS, and the forged court publishes what each declaration opens.
- **Shapes of values**, in the court library, used by the machine language: `absolute_path`, `ipv4`, `cidr`, `domain`, `label`, `mac`.
- **A program holds a court** (v0.70) and **a literal is judged when the program is compiled** (v0.71).

What stzlib's engine already holds: a credential broker that attaches a secret to a request bound for the one host its grant names
and follows no redirect, and a list of shut doors any engine library asks before it acts. A door that checks before it opens is not
new to the estate.

## 2. Six lessons this design takes

From this desk's knowledge of the systems named, not read again for this memo.

| lesson | where it was learned | what Haro takes |
|---|---|---|
| a program is given folders, and every path is resolved beneath one of them | capability file systems: WASI's preopened directories, `openat2` with `RESOLVE_BENEATH`, OpenBSD's `unveil` | a ROOT, and a place beneath it |
| the check and the use are one act, or a link moved between them wins | time-of-check to time-of-use races on paths | the door opens beneath the root and compares what it opened |
| a list of what may be reached is a line an operator can read | Deno's `--allow-read`, `--allow-net`, `--allow-run` | one declaration of a program's doors |
| a command is a program and its arguments, never a line given to a shell | shell injection | an invocation is a vector |
| a host is checked after its name is resolved, and a redirect is a new host | server-side request forgery | the endpoint's second check is the door's |
| text from outside never chooses a door's argument | CaMeL (2025), cited in PROOF.md | T7's rule itself |

## 3. The design

### 3.1 One declaration: the doors a program opens

A program declares its doors as a sentence of one standard language, forged like any language and loaded like any declaration. Three
kinds, written here with working words -- the spellings are chosen when the rung starts (D84):

    DEFINE ROOT cases AS (AT "spike/v70/cases", ALLOWS [read]) RATIONALE "the sentences this court judges"
    DEFINE PEER registry AS (HOST "registry.example.org", PORTS [443], SCHEMES [https]) RATIONALE "where releases are read from"
    DEFINE COMMAND forge AS (RUNS "haro", TAKES [word, place]) RATIONALE "the forge, run as a child"

- **ROOT**: a folder and what may be done beneath it -- `read`, `write`, `list`, `remove`; optionally the kinds of file by extension.
- **PEER**: a host by its exact name, or a network by its prefix; the ports and the schemes it may be reached on.
- **COMMAND**: a program and the shapes of the arguments it may be given.

The language NEEDS filesystem, network and process, and each kind OPENS its door (D51). So the sentence's `world` rows already say
what the program opens, and whoever holds the machine -- Harobanda -- reads the same list.

### 3.2 Three judges

Each takes outside text and answers a judged value, or a refusal with its name.

- **A place**: a ROOT and a text. The text is read as a path beneath the root and normalised. Refused: a path that leaves the root
  (`..`, an absolute path elsewhere, a drive, a scheme); a name the platform reads otherwise (a NUL or control byte, a device name, a
  trailing dot or space, a stream after a colon); a kind the root does not list.
- **An endpoint**: a PEER and a text. Refused: a host that is not the peer's, a port or a scheme it does not list.
- **An invocation**: a COMMAND and its arguments. Each argument is judged by its declared shape -- a word, a number, a place of a
  named root, one word of a MENU. The result is a vector: the program, then its arguments.

### 3.3 What a door takes

- text the program itself wrote: a literal, or text made only of literals -- as today;
- a place, an endpoint, an invocation;
- **never unjudged text**: UNJUDGED_DOOR.

A place carries what its root allows, so `Write` given a place of a read-only root is refused at the door, by name.

The strict form -- every argument of a door is a place, an endpoint or an invocation, the program's own literals included -- is the
proof profile's (D56, D81): there, what a program can reach is read off one declaration.

### 3.4 The value is a handle

T7's third part says "a handle names its door": `handle of file`, `handle of network`, letter `h`. A place, an endpoint and an
invocation are that: handles of filesystem, network and process, held before the door is opened. So this design is also how D83 (8)
is built, and the rule that a program whose language does not NEED a door cannot hold a handle of it is the declaration's own gate.

### 3.5 The door's half

A judged place is checked again where it is used. The VM opens the file, asks the platform what it opened, and compares that with the
root: a link or a junction that leads out is refused at the open, with the same name as a `..` would be. For an endpoint the second
check -- the address a name resolved to, a redirect -- is made where the socket is, in the engine, as the broker already does.

### 3.6 The usual case, made short

A tool that reads the file a person names:

    load "doors.haro"
    sDoors = doors'
      DEFINE ROOT given AS (AT anywhere, ALLOWS [read]) RATIONALE "the file a person names on the command line"
    '
    tSrc = Read(sDoors.Place("given", sysargv[4]))

`AT anywhere` gives no containment and says so: the program reads any file a person names, and never writes or removes one. Haro's
fifteen lines become this one declaration in the court library and one judged read each.

### 3.7 `unjudged`, whole, built on it

- A door's answer is unjudged: a file's text, the command line, the environment, a socket's bytes, a model's text, a child's output.
- The mark is on the value when the program runs and goes where the value goes -- through a call, a list, an attribute, joined text.
- It ends at a court (`Judge`), at one of the three judges above, and at a conversion that refuses what it cannot read.
- It is refused at `Eval` and its kin (UNJUDGED_RUN), at a door (UNJUDGED_DOOR), and at a parameter not declared `unjudged`
  (UNJUDGED_ARGUMENT).

## 4. The order of rungs proposed

| rung | what | converts |
|---|---|---|
| 1 | the standard language of doors; ROOT and the place; the filesystem doors take a place -- **built, v0.72** | nothing yet refused |
| 2 | COMMAND and the invocation; a child is run from a vector -- **built, v0.73**; the refusal of a command line built as text is a step of its own, next | Haro's run of a program and stzlib's 10 lines, with that step |
| 3 | PEER and the endpoint, judged by Haro and held by the engine | with stzlib's engine desk |
| 4 | `unjudged`, whole: the mark, where it ends, its three refusals | Haro's 15 reads; stzlib's 19 uses of the command line, counted and sent first |
| 5 | `of` on an attribute, and handles written with `of` | -- |

Each takes the next free number when it starts.

## 5. What it costs, and the risks

- **stzlib's conversions.** 12 `System` calls build a command line as text (`System(tRun + "faces,ocr" + tOut)`); each becomes a
  declared COMMAND. 103 `LoadLib` calls load the engine's libraries from a folder the environment names (`STZ_ENGINE_DIR`): the folder
  is outside text, so it is a ROOT declared once.
- **Windows.** A path has more spellings than one: drives, `\\?\`, short names, device names, streams. The place's judge refuses what
  it does not read, and the door's second check is the one that holds.
- **The check and the use.** Between a judge and an open a link can move. Section 3.5 is the answer; it is the VM's work on each
  platform and is measured when it is built.
- **A declaration nobody reads.** `AT anywhere` can be written everywhere. It is still one line that says what a program does, and
  the proof profile refuses it.
- **NOT MEASURED**: what a judged read costs beside a plain one; how many of stzlib's 81 writes and 68 reads take outside text.

## 6. What this document does not decide

The names: the standard language's, its three kinds' words, the three judges', the refusals'. They are spellings, this desk's under
D84, chosen when each rung starts and counted on stzlib first.

## 7. The questions

**HARO-DOORS-01: (a) to (e) RULED 2026-11-14, the Principal: "Yes, as recommended".** As it was put, class: judgement, with what
was recommended and is now ruled after each --

- **(a) The frame.** A door takes what the program itself wrote, or a value judged against the program's one declaration of its
  doors: roots, peers, commands. Outside text reaches a door no other way. **Ruled: yes.**
- **(b) The program's own literals.** They stay allowed at a door in an ordinary program -- only outside text is refused -- and
  the strict form, where a literal too goes through the declaration, is the proof profile's. Or strict for every program.
  **Ruled: literals stay allowed in an ordinary program; the strict form is the proof profile's.**
- **(c) `AT anywhere`.** A program may declare a root with no folder, read only, so a tool that reads any file a person names says
  so in one line. Or every root is a folder. **Ruled: it may.**
- **(d) No shell.** A command is a declared program with judged arguments; in `.haro` code a command line built as text is refused
  once invocations are built. **Ruled: yes.**
- **(e) The network's door is the engine's.** Haro judges an endpoint and names its refusal; the check after a name is resolved, and
  at a redirect, is made where the socket is -- stzlib's engine, as its broker does today. **Ruled: yes.**
