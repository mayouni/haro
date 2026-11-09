const std = @import("std");

// The Haro VM and compiler: ONE binary, `haro`.
//
// Forked on 2026-11-02 from Ring++'s VM and compiler (github.com/mayouni/rnx-spike, branch `next`, 2ea38fd), at the author's word:
// Haro owns its toolchain from here and evolves it; Ring++ stays the bridge that keeps Softanza's legacy code running. NOTES.md
// says what was carried over and what was renamed.
//
//   zig build -Doptimize=ReleaseFast -j2       -> zig-out/bin/haro.exe
//
// The VM's memory model is the one Ring++'s gate always built (mimalloc, reference counting, typed registers, eager copy at
// assignment), so it is the default here and the A/B variants Ring++ priced it with are not carried. The options stay, defaulted,
// because the VM's source reads them.
//
// Three vendored C trees, each with SHA256SUMS: the tree-sitter runtime, the grammar of the surface Haro's code is written in
// today (Youssef's tree-sitter grammar, MIT, credited as it is), and mimalloc. The generated parser table is 21 MB of switch
// statements, so it is compiled -O1; UBSan trips harmlessly on it; fdopen needs a POSIX level declared for non-Windows targets, and
// on glibc that level hides le16toh/be16toh unless _DEFAULT_SOURCE is declared beside it.
const ts_c_flags = [_][]const u8{
    "-std=c11",
    "-w",
    "-fno-sanitize=undefined",
    "-D_POSIX_C_SOURCE=200809L",
    "-D_DEFAULT_SOURCE",
    "-D_DARWIN_C_SOURCE",
};

fn vmCommit(b: *std.Build) []const u8 {
    const root = b.pathFromRoot(".");
    var code: u8 = 0;
    const h = b.runAllowFail(&.{ "git", "-C", root, "log", "-1", "--format=%H", "--", "." }, &code, .Ignore) catch return "unknown";
    const hash = std.mem.trim(u8, h, " \r\n");
    if (hash.len == 0) return "unknown";
    const st = b.runAllowFail(&.{ "git", "-C", root, "status", "--porcelain", "--untracked-files=no", "--", "." }, &code, .Ignore) catch return "unknown";
    if (std.mem.trim(u8, st, " \r\n").len > 0) return b.fmt("{s}+uncommitted", .{hash});
    return hash;
}

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const opts = b.addOptions();
    opts.addOption(bool, "rc", b.option(bool, "rc", "reference counting and real frees") orelse true);
    opts.addOption(bool, "mi", b.option(bool, "mi", "allocate through mimalloc") orelse true);
    opts.addOption(bool, "typed", b.option(bool, "typed", "typed registers") orelse true);
    opts.addOption(bool, "deferred", b.option(bool, "deferred", "deferred counting") orelse false);
    opts.addOption(bool, "cow", b.option(bool, "cow", "eager copy at assignment") orelse true);
    // v0.51 (HARO-FACTS-01): the checker's version in `haro check --facts` -- the last commit that touched vm/, and "+uncommitted"
    // when vm/ holds changes as it is built; "unknown" without git (a build from an archive). A commit of records alone changes nothing.
    opts.addOption([]const u8, "commit", vmCommit(b));

    const vendor = b.pathFromRoot("vendor");
    const mod = b.createModule(.{
        .root_source_file = b.path("src/haro.zig"),
        .target = target,
        .optimize = optimize,
        .link_libc = true,
        // the release builds strip (release/build_release.py): a Linux binary carried 12 MB of debug information in itself
        .strip = b.option(bool, "strip", "leave the debug information out of the binary"),
    });
    mod.addOptions("config", opts);
    mod.addIncludePath(.{ .cwd_relative = b.fmt("{s}/tree-sitter/include", .{vendor}) });
    mod.addIncludePath(.{ .cwd_relative = b.fmt("{s}/tree-sitter/src", .{vendor}) });
    mod.addIncludePath(.{ .cwd_relative = b.fmt("{s}/tree-sitter-ring/src", .{vendor}) });
    mod.addCSourceFile(.{
        .file = .{ .cwd_relative = b.fmt("{s}/tree-sitter/src/lib.c", .{vendor}) },
        .flags = &ts_c_flags,
    });
    mod.addCSourceFiles(.{
        .root = .{ .cwd_relative = b.fmt("{s}/tree-sitter-ring/src", .{vendor}) },
        .files = &.{ "parser.c", "scanner.c" },
        .flags = &(ts_c_flags ++ [_][]const u8{"-O1"}),
    });
    mod.addIncludePath(.{ .cwd_relative = b.fmt("{s}/mimalloc/include", .{vendor}) });
    // a macOS build cross-compiled without Apple's SDK: mimalloc's random source includes CommonCrypto, which Zig's macOS headers
    // lack; compat/macos declares the one call (HARO-RELEASE-ADOPT-01 (c), 2026-11-09)
    if (target.result.os.tag == .macos) mod.addIncludePath(b.path("compat/macos"));
    mod.addCSourceFile(.{
        .file = .{ .cwd_relative = b.fmt("{s}/mimalloc/src/static.c", .{vendor}) },
        .flags = &.{ "-O2", "-DNDEBUG" },
    });
    b.installArtifact(b.addExecutable(.{ .name = "haro", .root_module = mod }));
}
