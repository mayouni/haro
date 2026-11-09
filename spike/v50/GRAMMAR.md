# Haro v0.50 -- a program that serves another

HARO-STDIOFLUSH-01, from the Radar desk (2026-11-09 14:10, through central 16:15), found building Radar's MCP server on Haro
(stzradar `tools/mcp.haro`). Haro held a program's output to a pipe until the program ended, `give` waited for input without sending
it, nothing flushed it, and a read at the end of input answered "" for ever. So the server counted four empty reads to guess that its
client had gone, and sent each reply by running an empty shell command, since `system()` flushes. Asked: (a) flush before waiting for
input, as C's stdio does for a terminal; (b) or a flush; (c) a way to know the input has ended. This desk found a fourth reading `give`:
a line past 4,096 bytes was cut, the rest coming back as the next line -- an MCP message is one line, and can be longer.

Fixtures first (58f71dc: 13 cases, 12 failing before the code; D07 held and guards a program's own `stdout`). Code 8e631e3. **Two
fixtures changed after the code**, said so: D14 was added, since the .haro file's exact spelling of the three names was judged by no
case; and D07 now reads the program's `stdout` from a function as well, since plant F9 MISSED -- at the top level the main chunk finds
its own name before the stream is asked, so only a function asks whether a program's global replaces the stream.

| line | what | cases |
|---|---|---|
| S1 | `give` sends the program's output before it waits for input, as Ring's `see` and C's stdio for a terminal do | D01, D02, D13 |
| S2 | `stdin`, `stdout`, `stderr` are the program's three streams, file handles as Ring has them (type "file"); `fflush(stdout)` (`FFlush(stdout)` in a .haro file) sends the output now; a write through `stdout` keeps its place among `see`'s; a program's own global of that name is its own; in a .haro file they are spelled exactly | D03-D07, D14 |
| S3 | `give` reads a line whole, whatever its length | D08, D09 |
| S4 | `feof(stdin)` answers whether a read met the end of input -- C's answer and Ring's: 1 once a read found no more, so an empty line is not the end, and a last line without its line end is; in a .haro file `FEOF` answers a boolean, as `FExists` does | D10, D11, D12, D13 |

## How a server reads its input

```
func main
    while true
        give tLine
        if tLine = "" and FEOF(stdin)
            exit
        ok
        Handle(tLine)
    end
```

`give` sends every reply written so far before it waits, so a reply needs no flush of its own; `FFlush(stdout)` is there for a program
that sends while it works and reads nothing.

## How it is built

- `give` (main.zig, `.giveline`) calls `outFlush()` before it reads; it reads byte by byte as before (nothing past the line end is
  taken from a pipe), into a growing buffer; a read that finds no more input sets `stdin_ended`.
- `stdin`, `stdout`, `stderr` compile to three builtins next to `sysargv` (compile.zig, `streamOf`), each answering one table entry
  for C's stream, made at its first read. C's streams are named per C library: UCRT's `__acrt_iob_func`, macOS's `__stdinp`, glibc's
  and musl's variables. `gorc` reads a program's own global of that name once it is set, as for `nl`.
- `fflush` on `stdout` flushes Haro's buffer, then C's. `fwrite`, `fputc`, `fputs` on `stdout` flush Haro's buffer first and C's after,
  so neither passes the other. `feof` on `stdin` answers 1 when `give` found the end, or when C's own reads did.
- `feof` joins the yes-or-no built-ins, so in a .haro file it answers a boolean.

## Measured

- **The court**: 14 of 14 on haro and its checked build (stage 54); the dialog cases wait at most 10 s for each reply, and before the
  code every one of them waited out its 10 s.
- **Plants**: F1 to F10, each one protection switched off: 10 of 10 caught (F9 after D07's change, above).
- **A long line**: `give` of a 100,000-byte line, the program's whole run 0.033 s against 0.013 s for a one-byte line (best of 5,
  heartbeat fit to measure) -- byte-at-a-time reading costs about 0.2 us a byte, kept so nothing past the line end is taken.

- **The guard**: 54 stages on the committed tree (8e631e3), 1,667 s: every stage passes but stage 6, whose cold compile read 154.3 ms
  against its 150 ms ceiling, and 166.5 ms run alone. Not this rung's: `study/v50/stage6_ab.py`, the VM before the rung (1f1ad87)
  against the rung's, alternating, minima of 4 rounds of 15, heartbeat fit to measure -- A 164.0 ms, B 161.9 ms, B-A -2.1 ms. The
  machine reads over the ceiling today, as it has before (v0.36's account: 180-186 ms before the change as after).

## Named

- **A divergence**: Ring's `give` cuts a line at 255 bytes (`RING_LARGEBUF`, genlib_e.c `ring_vm_generallib_give`), keeping the rest
  for the next read. Haro reads the line whole in a .ring file too: the cut is a buffer's size, not a meaning, and no program relies on
  a line arriving in pieces.
- **Not changed**: `see` still buffers, where Ring flushes after every `see`. Output is sent when the program waits for input, flushes,
  runs a command, ends, or fills 64 KB. A program's output therefore reaches a pipe at its next `give`, not at its `see`.
- **Two readers of one input**: `give` reads the input itself; `fgets(stdin, ..)` and `fgetc(stdin)` read through C's buffer. A
  program that mixes them can see lines out of order, as a C program mixing `read()` and `fgets()` can. Use one.
- `tui_key` without a console (one byte of stdin) neither flushes nor sets the end: no case asks it yet.
