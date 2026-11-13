//! `haro check --facts <file>` (v0.51, HARO-FACTS-01, answering stzlib-testoor's HARO-PROOF-01 (a)): what the checker and the compiler
//! establish, per function, as ONE JSON document a recorder can keep beside the bytes it was taken from.
//!
//!   format       "haro-check-facts/1"
//!   checker      {"name": "haro", "commit"}: the last commit that touched vm/ when this binary was built, "+uncommitted" after it when
//!                vm/ held changes then (build.zig). Both builds of one commit print the same record (D41), so the build is no part of it
//!   files        [{"path", "sha256" of the bytes read, "surface": "haro" | "ring", "top_findings"}]
//!   not_checked  [{"rules", "why"}]: the rules that did not look, as the text report says in words
//!   impurity     what the impurity analysis is, in one sentence
//!   functions    [{"file", "name", "class", "line", "end_line", "findings", "impure"?, "calls_static", "calls_dynamic", "calls_late",
//!                  "compiled", "refused"?, "reaches_uncompiled"}]
//!
//! A FIELD FOR A FACT NOT ESTABLISHED IS ABSENT, NEVER FALSE: `impure` only where the analysis saw one, `refused` only where the compiler
//! stopped. `total`, `uses` and profiles (D55 T7, D56) join when their rungs are built. A function's lines run from its definition to
//! the next definition, as the checker reads a method (types.nextDefBoundary: the grammar does not nest a method's body), with blank
//! lines at its end left out and comments kept.
const std = @import("std");
const ts = @import("ts.zig");
const co = @import("compile.zig");
const check = @import("check.zig");
const types = @import("types.zig");
const lift = @import("lift.zig");
const config = @import("config");

const Alloc = std.mem.Allocator;

pub const NotChecked = struct { rules: []const []const u8, why: []const u8 };

pub const IMPURITY = "direct only: a function that writes a $global, prints with see, or calls random, clock, date, time, epochtime, " ++
    "read, write, fopen, fwrite, fread, remove, system, eval, loadlib, loadlibfile or input, in its own lines; calls are not followed";

fn str(w: *std.Io.Writer, s: []const u8) !void {
    try w.writeByte('"');
    for (s) |ch| switch (ch) {
        '"' => try w.writeAll("\\\""),
        '\\' => try w.writeAll("\\\\"),
        '\n' => try w.writeAll("\\n"),
        '\r' => try w.writeAll("\\r"),
        '\t' => try w.writeAll("\\t"),
        0...8, 11, 12, 14...31, 127 => try w.print("\\u{x:0>4}", .{ch}),
        else => try w.writeByte(ch),
    };
    try w.writeByte('"');
}

fn strList(w: *std.Io.Writer, xs: []const []const u8) !void {
    try w.writeByte('[');
    for (xs, 0..) |x, i| {
        if (i > 0) try w.writeAll(", ");
        try str(w, x);
    }
    try w.writeByte(']');
}

fn isSynthetic(name: []const u8) bool {
    return name.len >= 2 and name[0] == '@' and name[1] == '@';
}

/// Each line's first byte, once per file: a row is a bisection, never a count from the file's start (a 30,000-function library made
/// that quadratic -- HF-157)
const Lines = struct {
    starts: []const usize,

    fn of(a: Alloc, src: []const u8) !Lines {
        var s = std.ArrayListUnmanaged(usize){};
        try s.append(a, 0);
        for (src, 0..) |ch, i| if (ch == '\n') try s.append(a, i + 1);
        return .{ .starts = s.items };
    }

    /// the 1-based row holding `byte`
    fn row(self: Lines, byte: usize) u32 {
        var lo: usize = 0;
        var hi: usize = self.starts.len;
        while (hi - lo > 1) {
            const mid = (lo + hi) / 2;
            if (self.starts[mid] <= byte) lo = mid else hi = mid;
        }
        return @intCast(lo + 1);
    }
};

/// Each function's first direct impurity, from ONE walk of the file: a tree cursor visits every node once in order, and an impure node
/// is its function's -- the one whose bytes hold its start -- if that function has none yet. The order is types.impurityInRange's:
/// the first impure node, in order, that starts in the function's bytes. A walk per function made it cubic: tree-sitter reaches a
/// child, or a next sibling, by stepping from the first (HF-157).
fn impurities(a: Alloc, root: ts.Node, fns: []const Fn, out: []?types.Impurity) void {
    if (fns.len == 0) return;
    var cur = ts.c.ts_tree_cursor_new(root.raw);
    defer ts.c.ts_tree_cursor_delete(&cur);
    while (true) {
        const n = ts.Node{ .raw = ts.c.ts_tree_cursor_current_node(&cur), .src = root.src };
        if (types.impurityDirect(a, n)) |imp| {
            if (fnAtByte(fns, n.startByte())) |j| {
                if (out[j] == null) out[j] = imp;
            }
        }
        if (ts.c.ts_tree_cursor_goto_first_child(&cur)) continue;
        while (!ts.c.ts_tree_cursor_goto_next_sibling(&cur)) {
            if (!ts.c.ts_tree_cursor_goto_parent(&cur)) return;
        }
    }
}

/// The function of `fns` (one file's, in order, disjoint) whose bytes [start, end) hold `byte`, or null
fn fnAtByte(fns: []const Fn, byte: usize) ?usize {
    var lo: usize = 0;
    var hi: usize = fns.len;
    while (lo < hi) {
        const mid = (lo + hi) / 2;
        if (fns[mid].end <= byte) lo = mid + 1 else hi = mid;
    }
    if (lo < fns.len and fns[lo].start <= byte and byte < fns[lo].end) return lo;
    return null;
}

fn lessStr(_: void, a: []const u8, b: []const u8) bool {
    return std.mem.lessThan(u8, a, b);
}

/// sorted, each once
fn uniq(a: Alloc, xs: *std.ArrayListUnmanaged([]const u8)) ![]const []const u8 {
    std.mem.sort([]const u8, xs.items, {}, lessStr);
    var out = std.ArrayListUnmanaged([]const u8){};
    for (xs.items) |x| {
        if (out.items.len > 0 and std.mem.eql(u8, out.items[out.items.len - 1], x)) continue;
        try out.append(a, x);
    }
    return out.items;
}

fn findingJson(w: *std.Io.Writer, f: check.Finding) !void {
    try w.writeAll("{\"rule\": ");
    try str(w, f.rule);
    try w.writeAll(", \"severity\": ");
    try str(w, f.severity.label());
    try w.print(", \"line\": {d}, \"col\": {d}, \"message\": ", .{ f.row, f.col });
    try str(w, f.message);
    try w.writeByte('}');
}

const Fn = struct { idx: usize, file: usize, start: usize, end: usize, line: u32 = 0, end_line: u32 = 0 };

fn lessFn(_: void, a: Fn, b: Fn) bool {
    if (a.file != b.file) return a.file < b.file;
    return a.start < b.start;
}

fn lessUsize(_: void, a: usize, b: usize) bool {
    return a < b;
}

/// The function of `fns` (one file's, in order, disjoint) whose rows hold `row`, or null
fn fnAtRow(fns: []const Fn, row: u32) ?usize {
    var lo: usize = 0;
    var hi: usize = fns.len;
    while (lo < hi) {
        const mid = (lo + hi) / 2;
        if (fns[mid].end_line < row) lo = mid + 1 else hi = mid;
    }
    if (lo < fns.len and fns[lo].line <= row and row <= fns[lo].end_line) return lo;
    return null;
}

pub fn print(
    a: Alloc,
    w: *std.Io.Writer,
    roots: []const ts.Node,
    paths: []const []const u8,
    origs: []const []const u8,
    findings: []const check.Finding,
    not_checked: []const NotChecked,
    fd: co.FactsData,
) !void {
    const d = fd.graph;
    var by_src = std.AutoHashMapUnmanaged(usize, usize){};
    for (roots, 0..) |r, i| try by_src.put(a, @intFromPtr(r.src.ptr), i);

    const lines = try a.alloc(Lines, roots.len);
    for (roots, 0..) |r, i| lines[i] = try Lines.of(a, r.src);
    var by_path = std.StringHashMapUnmanaged(usize){};
    for (paths, 0..) |p, i| try by_path.put(a, p, i);

    // every definition's first byte, per file -- functions and classes, as types.nextDefBoundary reads a method's extent -- from the
    // compiler's own lists, so no tree is walked once per function
    const defs = try a.alloc(std.ArrayListUnmanaged(usize), roots.len);
    for (defs) |*x| x.* = .{};
    for (d.funcs) |f| {
        if (isSynthetic(f.name) or f.lambda_at != null) continue;
        const fi = by_src.get(@intFromPtr(f.node.src.ptr)) orelse continue;
        try defs[fi].append(a, f.node.startByte());
    }
    for (d.classes) |c| {
        const fi = by_src.get(@intFromPtr(c.node.src.ptr)) orelse continue;
        try defs[fi].append(a, c.node.startByte());
    }
    for (defs) |x| std.mem.sort(usize, x.items, {}, lessUsize);

    // each function's own extent; a lambda is its enclosing function's, never a record of its own
    var fns = std.ArrayListUnmanaged(Fn){};
    for (d.funcs, 0..) |f, i| {
        if (isSynthetic(f.name) or f.lambda_at != null) continue;
        const fi = by_src.get(@intFromPtr(f.node.src.ptr)) orelse continue;
        const root = roots[fi];
        const start: usize = f.node.startByte();
        var end: usize = root.endByte();
        for (defs[fi].items) |s| if (s > start) {
            end = s;
            break;
        };
        // v0.69: a function written with its `end` stops there; what follows it is the file's, or the next definition's
        if (f.node.closedByEnd()) end = f.node.endByte();
        while (end > start and std.ascii.isWhitespace(root.src[end - 1])) end -= 1;
        try fns.append(a, .{ .idx = i, .file = fi, .start = start, .end = end, .line = lines[fi].row(start), .end_line = lines[fi].row(end -| 1) });
    }
    std.mem.sort(Fn, fns.items, {}, lessFn);

    // each file's functions, and each finding placed once: in the function whose rows hold it, or at the file's top
    const file_fns = try a.alloc([]const Fn, roots.len);
    {
        var k: usize = 0;
        for (0..roots.len) |fi| {
            const s = k;
            while (k < fns.items.len and fns.items[k].file == fi) k += 1;
            file_fns[fi] = fns.items[s..k];
        }
    }
    const fn_findings = try a.alloc(std.ArrayListUnmanaged(check.Finding), fns.items.len);
    for (fn_findings) |*x| x.* = .{};
    const top_findings = try a.alloc(std.ArrayListUnmanaged(check.Finding), roots.len);
    for (top_findings) |*x| x.* = .{};
    const base = try a.alloc(usize, roots.len);
    {
        var k: usize = 0;
        for (0..roots.len) |fi| {
            base[fi] = k;
            k += file_fns[fi].len;
        }
    }
    for (findings) |f| {
        const fi = by_path.get(f.file) orelse continue;
        if (fnAtRow(file_fns[fi], f.row)) |j| try fn_findings[base[fi] + j].append(a, f) else try top_findings[fi].append(a, f);
    }
    const impure = try a.alloc(?types.Impurity, fns.items.len);
    @memset(impure, null);
    for (roots, 0..) |r, fi| impurities(a, r, file_fns[fi], impure[base[fi] .. base[fi] + file_fns[fi].len]);

    const real = struct {
        fn f(fs: []const co.Func, start: usize) usize {
            var i = start;
            var guard: u32 = 0;
            while (fs[i].lambda_at != null and guard < 64) : (guard += 1) i = fs[i].encl orelse break;
            return i;
        }
    }.f;
    const display = struct {
        fn f(al: Alloc, dd: co.GraphData, i: usize) !?[]const u8 {
            if (i >= dd.funcs.len) return null;
            const t = dd.funcs[i];
            if (isSynthetic(t.name) or t.lambda_at != null) return null;
            if (t.owner) |o| if (o < dd.classes.len) return try std.fmt.allocPrint(al, "{s}.{s}", .{ dd.classes[o].name, t.name });
            return t.name;
        }
    }.f;

    // every call, gathered to the function (not lambda) that makes it
    const statics = try a.alloc(std.ArrayListUnmanaged([]const u8), d.funcs.len);
    const dynamics = try a.alloc(std.ArrayListUnmanaged([]const u8), d.funcs.len);
    const lates = try a.alloc(std.ArrayListUnmanaged([]const u8), d.funcs.len);
    for (statics, dynamics, lates) |*x, *y, *z| {
        x.* = .{};
        y.* = .{};
        z.* = .{};
    }
    for (d.funcs, 0..) |f, raw| {
        const from = real(d.funcs, raw);
        for (f.calls_static.items) |t| if (try display(a, d, t)) |n| try statics[from].append(a, n);
        for (f.calls_named.items) |ni| if (ni < d.names.len) try dynamics[from].append(a, d.names[ni]);
        for (f.calls_late.items) |ni| if (ni < d.names.len) try lates[from].append(a, d.names[ni]);
    }
    for (d.fixups) |fx| {
        if (fx.from >= d.funcs.len) continue;
        if (try display(a, d, fx.fidx)) |n| try statics[real(d.funcs, fx.from)].append(a, n);
    }

    try w.writeAll("{\n\"format\": \"haro-check-facts/1\",\n\"checker\": {\"name\": \"haro\", \"commit\": ");
    try str(w, config.commit);
    try w.writeAll("},\n\"files\": [");
    for (roots, 0..) |root, fi| {
        _ = root;
        var digest: [32]u8 = undefined;
        std.crypto.hash.sha2.Sha256.hash(origs[fi], &digest, .{});
        try w.writeAll(if (fi == 0) "\n  {\"path\": " else ",\n  {\"path\": ");
        try str(w, paths[fi]);
        try w.print(", \"sha256\": \"{s}\", \"surface\": ", .{std.fmt.bytesToHex(digest, .lower)});
        try str(w, if (lift.isHaro(paths[fi])) "haro" else "ring");
        try w.writeAll(", \"top_findings\": [");
        for (top_findings[fi].items, 0..) |f, n| {
            if (n > 0) try w.writeAll(", ");
            try findingJson(w, f);
        }
        try w.writeAll("]}");
    }
    try w.writeAll("\n],\n\"not_checked\": [");
    for (not_checked, 0..) |nc, i| {
        try w.writeAll(if (i == 0) "\n  {\"rules\": " else ",\n  {\"rules\": ");
        try strList(w, nc.rules);
        try w.writeAll(", \"why\": ");
        try str(w, nc.why);
        try w.writeByte('}');
    }
    try w.writeAll("\n],\n\"impurity\": ");
    try str(w, IMPURITY);
    try w.writeAll(",\n\"functions\": [");
    for (fns.items, 0..) |x, k| {
        const f = d.funcs[x.idx];
        const root = roots[x.file];
        try w.print("{s}\n  {{\"file\": {d}, \"name\": ", .{ if (k == 0) "" else ",", x.file });
        try str(w, f.name);
        try w.writeAll(", \"class\": ");
        if (f.owner) |o| (if (o < d.classes.len) try str(w, d.classes[o].name) else try w.writeAll("null")) else try w.writeAll("null");
        try w.print(", \"line\": {d}, \"end_line\": {d}, \"findings\": [", .{ x.line, x.end_line });
        for (fn_findings[k].items, 0..) |fd_, n| {
            if (n > 0) try w.writeAll(", ");
            try findingJson(w, fd_);
        }
        try w.writeByte(']');
        if (impure[k]) |imp| {
            try w.writeAll(", \"impure\": {\"why\": ");
            try str(w, imp.why);
            try w.print(", \"line\": {d}}}", .{imp.at.start().row + 1});
        }
        try w.writeAll(", \"calls_static\": ");
        try strList(w, try uniq(a, &statics[x.idx]));
        try w.writeAll(", \"calls_dynamic\": ");
        try strList(w, try uniq(a, &dynamics[x.idx]));
        try w.writeAll(", \"calls_late\": ");
        try strList(w, try uniq(a, &lates[x.idx]));
        try w.print(", \"compiled\": {s}", .{if (f.poisoned_own) "false" else "true"});
        if (f.poisoned_own) {
            for (fd.refusals) |r| {
                if (@intFromPtr(r.src.ptr) != @intFromPtr(root.src.ptr) or r.byte < x.start or r.byte >= x.end) continue;
                try w.writeAll(", \"refused\": {\"why\": ");
                try str(w, r.kind);
                try w.print(", \"line\": {d}}}", .{lines[x.file].row(r.byte)});
                break;
            }
        }
        try w.print(", \"reaches_uncompiled\": {s}}}", .{if (f.poisoned and !f.poisoned_own) "true" else "false"});
    }
    try w.writeAll("\n]\n}\n");
}
