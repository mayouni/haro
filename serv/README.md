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
- **apps/** -- the court's apps. One of each kind: a route, state in an object, a redeploy that keeps it, a redeploy
  that adds an attribute (refused), a raising handler, a class admitted while serving, a Rule A refusal.
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

## What it showed -- the questions rung 5 left, answered by running

- **Code admitted per request is never released.** Every admission stays: about 22 KB and its route, and the host routes
  by a list. A HaroServer that admits code with requests (RingServ's eval-per-request shape) grows without bound. The
  next rung of the resident VM is RELEASE: an admission's functions dropped when its request is done, or a request's code
  compiled without being admitted at all.
- **One namespace for every app.** Softanza's library defines `echo`, so an app defining `Echo` is refused (C22). Apps
  need names of their own: packages, which Ring has (C-28 keeps them refused in Ring++) and Haro must decide.
- **Adding an attribute to a live class is refused, and a real app wants it** (`tally_v3.ring`). Objects moved to a
  class's new layout are the other open rung.
- **A large deployment blocks the loop**: Softanza's library compiles for 13.8 s while no request is answered.
