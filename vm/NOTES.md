# The Haro VM and compiler

`haro` is Haro's own VM and compiler: one binary, built from this folder.

    zig build -Doptimize=ReleaseFast -j2        -> vm/zig-out/bin/haro.exe     (one heavy job: the grammar's parser is 21 MB of C)

## Where it came from

Forked on 2026-11-02, at the author's word, from **Ring++'s VM and compiler** (github.com/mayouni/rnx-spike, private, branch `next`,
commit 2ea38fd: `src/*.zig` and three vendored C trees). Ring++ was built as a new technology: a register VM and a compiler that
fix Ring's weaknesses while keeping a surface on which Softanza's legacy Ring code runs. Ring++ stays exactly that, the bridge
for Softanza. Haro takes the technology and owns it from here: a fix made in one is carried to the other by hand, when it matters to
both.

## What was renamed (step 2 of the cut)

Everything a user sees:
- the binary and its usage text (`rnxc` -> `haro`);
- the environment variables (`RNXC_*` -> `HARO_*`);
- the image cache (`%LOCALAPPDATA%\haro\images`; `.haroi` images and `.harop` prefixes);
- the runtime's name in its own messages;
- the checker's rule ids (`haro/...`) and its source anchor (`#haro:`);
- `haro <file.haro>` runs a file, as `haro exec` does. A `.ring` file runs the same way. Haro's own code is `.haro` (D40), but the
  code-graph and refinement rungs write Softanza-shaped programs of the legacy surface and run them.

`src/rnxc.zig` is `src/haro.zig`.

## What was kept, and why

- **The comments.** They are the code's history: measurements, findings (F-n) and decisions (C-n) of Ring++'s record, which is
  where they are explained.
- **The language surface of Haro's code today.** Its error codes (R24, C22...), Rule A, and the refusals of Ring's implicit files
  and packages are what that surface means now. They change only when Haro designs its own computing syntax: the block syntax of
  BLOCKS.md (Q-B3: "later, when the computing altitude is designed").
- **The grammar `vendor/tree-sitter-ring`.** It is Youssef's tree-sitter grammar of that surface, MIT, vendored byte for byte with
  its licence and hashes. A third party's work keeps its own name. It goes when Haro's own syntax has its own grammar.
- **The native interface names.** `rpp_init` and `rpp_abi_version` are a contract with Softanza's engine libraries, which export
  them. `rpp_http_*` are HaroServer's eight natives, and HaroServer runs on Ring++ today. Renaming either breaks a caller that was
  not part of this step.
- **Not carried:** Ring's standard library and its zip extension, which Ring++ installs beside rnxc for Softanza's legacy code,
  and Ring 1.27's own VM (Ring++'s oracle). Haro's code loads none of them, and from step 4 of the cut no Haro court is judged
  against Ring 1.27.

## Vendored

    vendor/tree-sitter        the tree-sitter runtime            SHA256SUMS, NOTES.md
    vendor/tree-sitter-ring   the grammar of the surface         SHA256SUMS, NOTES.md, LICENSE
    vendor/mimalloc           the VM heap's allocator            SHA256SUMS, NOTES.md

Each was checked against its SHA256SUMS when copied (2026-11-02).
