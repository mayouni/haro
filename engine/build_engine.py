r"""Build Softanza's engine for Haro's native ABI -- from a COPY of stzlib's engine sources at a stated ref, never stzlib's tree.

UNDER THE AUTHOR'S HARO-FIRST RULING, 2026-11-08: "Ring++ will be retired as Ring and all it's libraries, only Haro will remain." The only
build Haro could load was Ring++'s engine copy (ringpp runtime/engine-copy), older than stzlib's main; this brings the build here. Forked
from ringpp 98642d9 bench/engine_copy.py, carrying what Haro needs and nothing of Ring:

  1. `git archive <ref> libraries/stzlib/engine` of D:\GitHub\stzlib -> runtime/engine (gitignored), keeping its zig-out and .zig-cache
     across refreshes, so a refresh rebuilds only what changed. The ref is read, never checked out (stzlib's checkout stands on a branch)
  2. src/ring_api.zig := engine/ring_api_haro.zig, the backend over Haro's ABI; it exports the 37 names the bridges import, so no bridge
     file changes
  3. every domain's entry file gains rpp_init / rpp_abi_version (the names the VM looks for), handing the bridge's table to its registerAll
  4. build.zig: only the domains named in ONLY are built (batches share one cache); addRing does nothing; the three installs outside the
     domain loops are off; and NO Ring installation is searched -- the build is pointed at a folder that does not exist, so readRingMinor
     answers its default, 27, which only Ring's own backend reads. No Ring header is carried (D50)
  5. the ggml pool estimate for Qwen2.5-Coder 1.5B, a quarter more and a gigabyte (ringpp's K4 fix, 2026-10-20), re-applied after a copy

NOT CARRIED, named: ringpp's Linux patches (libcurl's config, ggml's and tree-sitter's feature macros, setenv) -- this machine builds for
Windows; a Linux Haro brings them when it is built. The --oracle and --official flavours, which served Ring and the oracle.

  python engine/build_engine.py                  copy and patch from stzlib origin/main
  python engine/build_engine.py --ref=<commit>   from another ref
  python engine/build_engine.py --build          copy, patch and build every domain, in batches, ReleaseSafe (the engine's own default)
  python engine/build_engine.py --build stz_string stz_list   these only
  python engine/build_engine.py --dst=C:\haro-engine --build  the copy and its build in another folder (STZ_ENGINE_DIR names it)

Each batch checks the free space on the drive first and stops below 11 GB (this machine freezes under pressure; a hook refuses builds
under 10). What built and what did not is written to runtime/engine/BUILT.txt, one line a domain.
"""
import io, os, shutil, subprocess, sys, tarfile, time

STZLIB = r'D:\GitHub\stzlib'
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DST = os.path.join(ROOT, 'runtime', 'engine')
BACKEND = os.path.join(HERE, 'ring_api_haro.zig')
KEEP = ('.zig-cache', 'zig-out', 'BUILT.txt', 'REF.txt')
BATCH = 12
FLOOR_GB = 11.0

RPP_A = """

// Haro (engine/build_engine.py): the same table, through the same ringlib_init, over Haro's backend of ring_api.zig. Two exports, named as
// the VM looks for them.
const RPP = @import("ring_api.zig");
export fn rpp_init(h: *const RPP.HostApi) callconv(.c) c_int {
    RPP.setHost(h);
    var dummy: u8 = 0;
    ring_bridge.ringlib_init(@ptrCast(&dummy));
    return 0;
}
export fn rpp_abi_version() callconv(.c) u32 {
    return 3;
}
"""
RPP_B = RPP_A.replace('ring_bridge.ringlib_init(@ptrCast(&dummy));', 'ringlib_init(@ptrCast(&dummy));')

NEURAL_OLD = "    const mem_size: usize = 128 * 1024 * 1024 + kv_len * n_new * n_head * n_layer * 24 + n_new * n_embd * n_layer * 64;"
NEURAL_NEW = (
    "    const mem_size_est: usize = 128 * 1024 * 1024 + kv_len * n_new * n_head * n_layer * 24 + n_new * n_embd * n_layer * 64;\n"
    "    // Haro's copy (ringpp's K4 fix, 2026-10-20): the estimate above is short for Qwen2.5-1.5B, so the model cannot run at all. A quarter more,\n"
    "    // and a constant gigabyte: the estimate under-counts something that does not grow with the prompt.\n"
    "    const mem_size: usize = mem_size_est + mem_size_est / 4 + 1024 * 1024 * 1024;")


def rw(path):
    s = io.open(path, encoding='utf-8', newline='').read()
    return s, ('\r\n' if '\r\n' in s else '\n')


def save(path, s):
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


def free_gb(path):
    return shutil.disk_usage(path).free / 1e9


def copy_sources(ref):
    """the engine at `ref`, from git archive, into DST; the build's cache and output kept"""
    sha = subprocess.run(['git', 'rev-parse', '--short', ref], cwd=STZLIB, capture_output=True, text=True).stdout.strip()
    if not sha:
        sys.exit(f'no ref {ref!r} in {STZLIB}')
    os.makedirs(DST, exist_ok=True)
    for name in os.listdir(DST):
        if name in KEEP:
            continue
        p = os.path.join(DST, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    t0 = time.time()
    arc = subprocess.run(['git', 'archive', '--format=tar', sha, 'libraries/stzlib/engine'], cwd=STZLIB, capture_output=True)
    if arc.returncode != 0:
        sys.exit(arc.stderr.decode('utf-8', 'replace'))
    n = 0
    prefix = 'libraries/stzlib/engine/'
    with tarfile.open(fileobj=io.BytesIO(arc.stdout)) as tf:
        for m in tf.getmembers():
            if not m.name.startswith(prefix):
                continue
            rel = m.name[len(prefix):]
            if not rel or rel.split('/')[0] in ('zig-out', '.zig-cache'):
                continue
            out = os.path.join(DST, *rel.split('/'))
            if m.isdir():
                os.makedirs(out, exist_ok=True)
            elif m.isfile():
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with open(out, 'wb') as fh:
                    fh.write(tf.extractfile(m).read())
                n += 1
    open(os.path.join(DST, 'REF.txt'), 'w').write(f'stzlib {ref} = {sha}\n')
    print(f'copied {n} files of stzlib {ref} ({sha}) in {time.time() - t0:.0f} s')
    return sha


def patch_copy():
    shutil.copyfile(BACKEND, os.path.join(DST, 'src', 'ring_api.zig'))
    p = os.path.join(DST, 'src', 'neural_gen.zig')
    if os.path.exists(p):
        s, nl = rw(p)
        if s.count(NEURAL_OLD) == 1:
            save(p, s.replace(NEURAL_OLD, NEURAL_NEW.replace('\n', nl)))
            print('neural_gen.zig: the pool-size fix applied')
        elif 'mem_size_est' in s:
            print('neural_gen.zig: already carries the pool-size fix')
        else:
            print('neural_gen.zig: the line changed upstream -- the pool-size fix was NOT applied; check the 1.5B model runs')
    domains, skipped = [], []
    src = os.path.join(DST, 'src')
    for f in sorted(os.listdir(src)):
        if not f.endswith('_entry.zig'):
            continue
        dom = f[:-len('_entry.zig')]
        s, nl = rw(os.path.join(src, f))
        if '@export(&ring_bridge.ringlib_init, .{ .name = "ringlib_init" });' in s:
            s = s.rstrip('\r\n') + RPP_A.replace('\n', nl) + nl
        elif 'fn ringlib_init(' in s:
            s = s.rstrip('\r\n') + RPP_B.replace('\n', nl) + nl
        else:
            skipped.append((dom, 'no ringlib_init in the entry'))
            continue
        save(os.path.join(src, f), s)
        domains.append(dom)
    print(f'entries patched: {len(domains)}')
    for d, why in skipped:
        print(f'  skipped {d:18s} {why}')

    bz = os.path.join(DST, 'build.zig')
    s, nl = rw(bz)

    def patch(old, new):
        nonlocal s
        old, new = old.replace('\n', nl), new.replace('\n', nl)
        if s.count(old) != 1:
            sys.exit(f'build.zig: {s.count(old)} of {old[:70]!r} -- the engine\'s build.zig changed; read it before patching')
        s = s.replace(old, new)

    patch('pub fn build(b: *std.Build) void {',
          '/// Haro: only the domains named in the ONLY environment variable (comma-separated) are built, so batches share one cache.\n'
          'fn wanted(b: *std.Build, name: []const u8) bool {\n'
          '    const only = std.process.getEnvVarOwned(b.allocator, "ONLY") catch return false;\n'
          '    var it = std.mem.splitScalar(u8, only, \',\');\n'
          '    while (it.next()) |o| if (std.mem.eql(u8, std.mem.trim(u8, o, " "), name)) return true;\n'
          '    return false;\n'
          '}\n\n'
          'pub fn build(b: *std.Build) void {')
    patch('    for (core_domains) |dom| {\n', '    for (core_domains) |dom| {\n        if (!wanted(b, dom.name)) continue;\n')
    patch('    for (base_domains) |dom| {\n', '    for (base_domains) |dom| {\n        if (!wanted(b, dom.name)) continue;\n')
    for old in ('        b.installArtifact(studio);', '    b.installArtifact(static_lib);', '    b.installArtifact(gen_refdata);'):
        patch(old, old.replace('b.installArtifact', 'if (false) b.installArtifact'))
    patch('fn addRing(b: *std.Build, mod: *std.Build.Module, lib: *std.Build.Step.Compile, ring_dir: []const u8) void {\n'
          '    mod.addIncludePath(.{ .cwd_relative = b.fmt("{s}/language/include", .{ring_dir}) });\n'
          '    lib.addLibraryPath(.{ .cwd_relative = b.fmt("{s}/lib", .{ring_dir}) });\n'
          '    lib.linkSystemLibrary("ring");\n'
          '}',
          'fn addRing(b: *std.Build, mod: *std.Build.Module, lib: *std.Build.Step.Compile, ring_dir: []const u8) void {\n'
          '    // Haro: nothing references Ring\'s C API, and no part of Ring is carried (D50).\n'
          '    _ = b;\n    _ = mod;\n    _ = lib;\n    _ = ring_dir;\n'
          '}')
    patch('orelse (discoverRingDir(b) orelse {', 'orelse (@as(?[]const u8, "_no_ring_haro_D50") orelse {')
    save(bz, s)
    print('build.zig: ONLY from the environment; addRing a no-op; extra installs off; no Ring installation searched')
    return domains


def build(domains):
    zig_env = dict(os.environ)
    zig_env['ZIG_GLOBAL_CACHE_DIR'] = os.path.join(ROOT, 'runtime', 'zig-global')
    results = {}
    t_all = time.time()
    for k in range(0, len(domains), BATCH):
        batch = domains[k:k + BATCH]
        gb = free_gb(DST)
        if gb < FLOOR_GB:
            print(f'STOPPED before batch {k // BATCH + 1}: {gb:.1f} GB free, under the {FLOOR_GB:.0f} GB floor', flush=True)
            for d in domains[k:]:
                results[d] = 'not built (disk)'
            break
        env = dict(zig_env)
        env['ONLY'] = ','.join(batch)
        t0 = time.time()
        r = subprocess.run(['zig', 'build', '-j2'], cwd=DST, env=env, capture_output=True, timeout=3600)
        dt = time.time() - t0
        bindir = os.path.join(DST, 'zig-out', 'bin')
        for d in batch:
            ok = os.path.exists(os.path.join(bindir, d + '.dll'))
            results[d] = 'built' if ok else 'FAILED'
        tail = r.stderr.decode('utf-8', 'replace')[-600:] if r.returncode != 0 else ''
        print(f'batch {k // BATCH + 1}: {",".join(batch)} -- exit {r.returncode}, {dt:.0f} s, {free_gb(DST):.1f} GB free'
              + (f'\n{tail}' if tail else ''), flush=True)
    with open(os.path.join(DST, 'BUILT.txt'), 'w') as fh:
        for d in domains:
            fh.write(f'{d}\t{results.get(d, "not built")}\n')
    nb = sum(1 for v in results.values() if v == 'built')
    print(f'ENGINE {nb} of {len(domains)} domains built in {time.time() - t_all:.0f} s; ' + os.path.join(DST, 'BUILT.txt'))
    return 0 if nb == len(domains) else 1


def main():
    global DST
    ref = 'origin/main'
    for a in sys.argv[1:]:
        if a.startswith('--ref='):
            ref = a[6:]
        elif a.startswith('--dst='):
            # another folder for the copy and its build (2026-11-08: D: was at its floor, C:\haro-engine on the author's word);
            # stzlib finds it through STZ_ENGINE_DIR
            DST = os.path.abspath(a[6:])
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not os.path.isdir(STZLIB):
        print('SKIP: no stzlib at ' + STZLIB)
        return 0
    copy_sources(ref)
    domains = patch_copy()
    if names:
        domains = [d for d in domains if d in names]
    if '--build' in sys.argv:
        return build(domains)
    print('copy at: ' + DST)
    return 0


if __name__ == '__main__':
    sys.exit(main())
