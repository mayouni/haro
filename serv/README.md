# HaroServer -- the host loop, first build (2026-10-31)

HaroServer is Haro's server: the counterpart of RingServ, which Ring++ measured and learned from (CLAUDE.md, "RINGSERV
ON RING++"). RingServ is one resident Ring state fed its library file by file, apps arriving as code that DEFINES
functions and classes, every request a call into the same state. Its host is C and Zig around Ring's VM.

This first build is that design on the resident VM, with the host loop in the program itself:

    rnxc resident host.ring          HAROSERV_PORT, default 8642

- **host.ring** -- the loop. It waits for a request (`rpp_http_next`), routes it to the function an app registered,
  and answers (`rpp_http_reply`). A deployment is a request too:
  - `POST /admit/<app>` admits the body's code into the running program (`admitcode`);
  - `POST /replace/<app>` replaces what the app defined (`replacecode`). The app's objects are kept, and every request
    after it runs the new code. A refusal is 422 with the reason, and the program stays as it was.
  - `POST /run?<input>` (2026-10-31, the resident VM's sixth rung): the body is code that defines `func Run cInput`. It
    is admitted, called with what followed `?`, and RELEASED (`releasecode`) before the reply -- the program after the
    request is the program before it. 200 and what Run returned, 500 and its error, 422 when it could not be admitted,
    or released: code that defines a class or a lambda stays in the program, says so, and `/run` is then refused
    (Run is defined) until a `/replace/run`.
- **apps/** -- the court's apps. One of each kind: a route, state in an object, a redeploy that keeps it, a redeploy
  that adds an attribute (admitted: the running object takes it, rung 7) and one that drops one (refused), a raising
  handler, a class admitted while serving, a Rule A refusal.
- **court.py** -- boots the host on a free port and drives it over HTTP. Every answer is checked and the costs are
  measured.
  - `--softanza` adds an app that loads Softanza's library into the running server, run from the install's tree.
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
- **One namespace for every app.** Softanza's library defines `echo`, so an app defining `Echo` is refused (C22). Apps
  need names of their own: packages, which Ring has (C-28 keeps them refused in Ring++) and Haro must decide.
- **Adding an attribute to a live class was refused, and a real app wants it -- answered by rung 7.** `tally_v3.ring`
  adds `nAdds`; the running tally keeps its 13 and counts from 0. Each object made before takes an added attribute at
  its first access past its own slots, starting as declared (a constant; a list a list of its own); about 55 ns an
  object, once, and nothing for the rest. Refused, with the reason: a dropped or reordered attribute, a starting value
  that runs code, region code that uses it, and a class another class the program holds inherits from.
- **A large deployment blocks the loop**: Softanza's library compiles for 13.8 s while no request is answered.
