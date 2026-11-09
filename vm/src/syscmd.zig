//! `systemcmd(cCommand)` -- run a command through the shell and answer what it wrote to its standard output (HARO-SYSTEMCMD-01, v0.46's
//! sixth round, 2026-11-09).
//!
//! On Ring this is LIBRARY code, stdlibcore.ring's SystemCmd: `System(cmd + "> " + tempname())`, the file read back, a last "\n"
//! dropped. Haro carries no part of Ring's library (D50), so a program that called it met R3, and a guard could not read a child's
//! output. It is Haro's own native here, published at start-up as httpd's are -- no library, no DLL.
//!
//! The shell is the one Ring's system() runs: C's popen (`_popen` on Windows, through cmd.exe), read in binary, so the bytes are what
//! Ring's read() of the redirect file would hold. THE DESK'S NAMED DIVERGENCE: the whole last line end goes -- "\r\n" or "\n" -- where
//! Ring's drops only the "\n" and leaves a "\r" on Windows. The command's standard error is not captured, as Ring's redirect does not
//! capture it. What this program printed before the call is flushed first, as `system` does.
const std = @import("std");
const builtin = @import("builtin");
const native = @import("native.zig");
const vm = @import("main.zig");

const RppVal = native.RppVal;
const Tag = native.Tag;

var alloc: std.mem.Allocator = undefined;
var out_buf: std.ArrayListUnmanaged(u8) = .{};

const FILE = opaque {};
const is_win = builtin.os.tag == .windows;
extern "c" fn _popen(cmd: [*:0]const u8, mode: [*:0]const u8) ?*FILE;
extern "c" fn _pclose(f: *FILE) c_int;
extern "c" fn popen(cmd: [*:0]const u8, mode: [*:0]const u8) ?*FILE;
extern "c" fn pclose(f: *FILE) c_int;
extern "c" fn fread(buf: [*]u8, size: usize, n: usize, f: *FILE) usize;

fn retStr(out: *RppVal, s: []const u8) void {
    out_buf.clearRetainingCapacity();
    out_buf.appendSlice(alloc, s) catch {};
    out.* = RppVal.str(out_buf.items);
}

fn systemCmd(args: [*]const RppVal, argc: u32, out: *RppVal) callconv(.c) c_int {
    if (argc != 1 or args[0].tag != @intFromEnum(Tag.str)) {
        retStr(out, "Bad parameter type!");
        return 1;
    }
    const cmd = args[0].asStr();
    const z = alloc.allocSentinel(u8, cmd.len, 0) catch {
        retStr(out, "");
        return 0;
    };
    defer alloc.free(z);
    @memcpy(z[0..cmd.len], cmd);
    vm.outFlush();
    const f = (if (is_win) _popen(z.ptr, "rb") else popen(z.ptr, "r")) orelse {
        retStr(out, "");
        return 0;
    };
    var got: std.ArrayListUnmanaged(u8) = .{};
    defer got.deinit(alloc);
    var buf: [4096]u8 = undefined;
    while (true) {
        const n = fread(&buf, 1, buf.len, f);
        if (n == 0) break;
        got.appendSlice(alloc, buf[0..n]) catch break;
    }
    _ = if (is_win) _pclose(f) else pclose(f);
    var s = got.items;
    if (std.mem.endsWith(u8, s, "\r\n")) s = s[0 .. s.len - 2] else if (std.mem.endsWith(u8, s, "\n")) s = s[0 .. s.len - 1];
    retStr(out, s);
    return 0;
}

/// Publish it through the same table `rpp_init` fills, at start-up.
pub fn registerAll(a: std.mem.Allocator) void {
    alloc = a;
    native.reg_alloc = a;
    native.register("systemcmd", &systemCmd);
}
