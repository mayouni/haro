# HaroServer -- the host loop, first build (2026-10-31)

HaroServer is Haro's server: the counterpart of RingServ, which Ring++ measured and learned from (CLAUDE.md, "RINGSERV
ON RING++"). RingServ is one resident Ring state fed its library file by file, apps arriving as code that DEFINES
functions and classes, every request a call into the same state. Its host is C and Zig around Ring's VM.

This first build is that design on the resident VM, with the host loop in the program itself:

    rnxc resident host.ring          HAROSERV_PORT, default 8642

- **host.ring** -- the loop. It waits for a request (`rpp_http_next`), routes it to the function an app registered,
  and answers (`rpp_http_reply`). A deployment is a request too:
  - `POST /admit/<app>?<exports>` admits the body's code into the running program as a NAMESPACE of its own
    (`admitapp`, D31): its functions, classes and globals are `app::Name`, it reads the base's names after its own,
    and another app reaches it only through what it exports -- the query, comma-separated (`?Entry,Sum`), spelt
    `app.Name` by the other app;
  - `POST /replace/<app>` replaces what the app defined, within its namespace (`replaceapp`). The app's objects are
    kept, and every request after it runs the new code. A refusal is 422 with the reason, and the program stays as it was;
  - `POST /base/<name>` admits the body into the BASE (`admitcode`) -- shared code every app reads after its own
    names, Softanza's library for one.
  - **Every deployment compiles in the background** (rung 9, 2026-11-01): `admitstart` starts its compile on a thread of
    its own, the loop serves on, and installs it between two requests (`admitstate`, `admitfinish`). A deployment whose
    compile is over within 50 ms -- a small app's -- is answered with its outcome as before: 201, or 422 and the reason.
    A larger one is answered 202 (`compiling <app>`), and `GET /deploy/<app>` says where it stands: 202 while it
    compiles or waits, 200 `admitted ...`, or 422 and the reason. One compiles at a time: a deployment that arrives
    meanwhile is queued behind it (202, `queued <app>`), and `/run` answers 503 until it is installed. While one is
    under way the loop waits for a request at most 10 ms (`rpp_http_next(nWaitMs)`), so a compile that ends while
    nobody asks is installed all the same.
  - An app registers its routes by its handler's name in the app; the host keeps them as `app::Handler`, a name only
    the host may call by string (an app reaching another's internal name by string is R3).
  - `POST /run?<input>` (2026-10-31, the resident VM's sixth rung): the body is code that defines `func Run cInput`. It
    is admitted, called with what followed `?`, and RELEASED (`releasecode`) before the reply -- the program after the
    request is the program before it. 200 and what Run returned, 500 and its error, 422 when it could not be admitted,
    or released: code that defines a class or a lambda stays in the program, says so, and `/run` is then refused
    (Run is defined) until a `/replace/run`.
- **apps/** -- the court's apps. One of each kind: a route, state in an object, a redeploy that keeps it, a redeploy
  that adds an attribute (admitted: the running object takes it, rung 7) and one that drops one (refused), a raising
  handler, a class admitted while serving, a handler that makes objects of a class an app deployed after it brings
  (`ledger.ring`, then `entry.ring`: rung 8, `new entry.Entry` through `entry`'s export), a Rule A refusal; and two
  apps defining the same names (`twin_a.ring`, `twin_b.ring`), one exporting a function (`sum.ring`) and one reaching
  it and failing on what it keeps (`calc.ring`).
- **court.py** -- boots the host on a free port and drives it over HTTP. Every answer is checked and the costs are
  measured.
  - `--softanza` admits Softanza's library into the base of the running server (`/base/stz`) and an app reading it,
    run from the install's tree.
  - `--platform=linux` runs the Linux rnxc under WSL; run the court itself under WSL to time Linux without the relay.
  - The gate runs it with a small load (step `HaroServer`).

The socket under the loop is rnxc's: `src/httpd.zig`, eight natives (`rpp_http_*`) published at start-up as
`src/zip.zig`'s are. There is no DLL; it is one binary. One request at a time and one connection per request, because
the VM runs one program on one thread and the loop is the program. A client that connects and sends nothing holds the
loop for at most 10 s.

## Measured, 2026-10-31 (4d533d7's VM, `src/httpd.zig`)

| | Windows | Linux |
|---|---|---|
| GET to an app's route, sequential, a new connection each | ~5,000-6,300 req/s, p50 0.14-0.18 ms | 7,800 req/s, p50 0.12 ms |
| code admitted with a request (a function and its route), small program | 0.33 ms | 1.3 ms (tree read through /mnt/d) |
| ... while the program holds Softanza's library (49,700 functions) | 0.94 ms | -- |
| the program per admitted function | +22 KB of private memory | -- |
| Softanza's library itself, admitted over HTTP | 13.8 s, cold; the loop answers nothing meanwhile | -- |

## A large deployment, in the background -- measured, 2026-11-01 (rung 9)

| | Windows | Linux |
|---|---|---|
| Softanza's library deployed into the base while the court sends requests | 15.5-17.1 s; 67,760-74,110 requests answered meanwhile, p50 0.19 ms; the longest wait 114-143 ms | -- |
| ... that longest wait, by phase (`RNXC_ADMIT_PHASES=1`) | the install 70-82 ms, the new functions reshaped 22 ms, the library's top level 20-30 ms -- on the program's thread; the parse trees' release (146 ms) and the compaction (~90 ms) after it run on the compiling thread | -- |
| 8,000 functions deployed while the court sends requests | ~0.5 s; ~1,500 requests answered meanwhile, the longest wait 17-20 ms | ~0.5 s; 331 requests (WSL's relay) |
| a small deployment, over HTTP | p50 0.39-0.40 ms (0.33 synchronous): the hand-off to the compiling thread | -- |

Before rung 9 the whole compile was a pause: 13.8 s at Softanza's size. The program's thread now pays the install and
the top level alone. Every check of the court passed through the background path, every small deployment answered 201
or 422 at once as before.

A Windows client through WSL's localhost relay reads ~2 ms a request against the Linux server; that is the relay.

## Release -- measured, 2026-10-31 (the resident VM's sixth rung)

| | Windows | Linux |
|---|---|---|
| a run over HTTP: admit, call, release, reply | p50 0.61-0.69 ms | 2.8 ms (a Windows client through WSL's relay) |
| 3,000 runs, each answering with a 16 KB literal of its own released code | private memory 36-53 MB, bounded | not measured |
| a release itself, in a program holding Softanza's library | at most 0.01 ms; a round is its admission, 0.4-0.9 ms | -- |

Bounded, not flat: a released run's source and compile stay in the program's arena until it is compacted, which now
happens once it has grown past twice its size plus 16 MB (it was 64 MB, and a small server climbed 64 MB first), in
under a millisecond at this size. The court holds the second half's high-water mark to the first half's.

## What it showed -- the questions rung 5 left, answered by running

- **Code admitted per request was never released -- answered by rung 6.** `/run` admits, calls and releases; the
  program keeps its size and the process its memory, bounded. What cannot be released: code that defines a class or a
  lambda (an object or a closure could outlive it), a replacement, and code a class reaches through `addmethod`; and
  only the LAST admission (a stack).
- **One namespace for every app -- answered by D31 (2026-11-01, haro/CHARTER.md).** Softanza's library defines `echo`,
  so an app defining `Echo` was refused (C22). Each app is a namespace of its own now: two apps define `Greet` and
  `Name` and each answers its own; `calc` reaches `sum.Sum` through `sum`'s export and gets R3 for `sum.Secret`, which
  `sum` keeps; an export naming nothing the app defines is refused. What the build decided beyond the decision: the
  host reaches an app's names by their internal spelling `app::Name` (the host owns its apps; only apps are held to
  exports); an app's top level and its lambdas resolve a name given by string as the base does, and an `eval` in its
  code resolves every name as the base does (none of them carries the app in its name); and an app's admission is not released, since another app may hold its exports.
  The resident VM's guard, section 11 (bench/resident/ns_host.ring), holds the rest.
- **Adding an attribute to a live class was refused, and a real app wants it -- answered by rung 7.** `tally_v3.ring`
  adds `nAdds`; the running tally keeps its 13 and counts from 0. Each object made before takes an added attribute at
  its first access past its own slots, starting as declared (a constant; a list a list of its own); about 55 ns an
  object, once, and nothing for the rest. Refused, with the reason: a dropped or reordered attribute, a starting value
  that runs code, region code that uses it, and a class another class the program holds inherits from.
- **An app could make another app's objects only through a factory the other app defined -- answered by rung 8.** A
  `new K` compiled before any app brought K finds K by name once one does, as Ring does: `apps/ledger.ring`'s handler
  makes `new Entry(...)`, answers 500 and R11 until `apps/entry.ring` is deployed after it, and 200 from then on. In
  `new K { ... }` of a class not yet held, a bare name the class lacks is R12, where Ring makes a variable.
- **A large deployment blocked the loop -- answered by rung 9 (2026-11-01).** Softanza's library compiled for 13.8 s while
  no request was answered. Every deployment compiles on a thread of its own now while the loop serves: 67,760 requests
  answered during the library's compile, the longest waiting 114 ms -- the install and the library's top level, which
  run on the program's thread. A deployment that arrives meanwhile is queued, and `/run` answers 503 until it is in.
