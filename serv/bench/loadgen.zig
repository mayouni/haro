//! loadgen -- the web comparison's client (webbench.py): an HTTP/1.1 load generator in one file.
//!
//!     loadgen <port> <path> <connections> <seconds> <warmup-seconds>
//!
//! Each of <connections> threads loops until the deadline: connect to 127.0.0.1:<port>, send one GET
//! asking the server to close (`Connection: close` -- the one way HaroServer serves, so every server is
//! measured the same way), read the answer to its Content-Length, close abortively (SO_LINGER 0, so a
//! run of hundreds of thousands of connections leaves no client port in TIME_WAIT), and record how long
//! the whole took. Requests begun in the warm-up are not counted. One JSON line on stdout:
//!     {"n":..., "rps":..., "p50_us":..., "p90_us":..., "p99_us":..., "max_us":..., "errors":..., "non200":...}
//! Written in Zig, not Python, so the client is not the thing measured: a Python client takes about as long
//! per request as the fastest servers here answer one.
const std = @import("std");
const builtin = @import("builtin");

const Ctx = struct {
    addr: std.net.Address,
    request: []const u8,
    start: std.time.Instant,
    warm_ns: u64,
    end_ns: u64,
};

const Result = struct {
    lat: std.ArrayListUnmanaged(u32) = .{},
    errors: u64 = 0,
    non200: u64 = 0,
};

fn lingerZero(fd: std.posix.socket_t) void {
    if (builtin.os.tag == .windows) {
        const L = extern struct { onoff: u16, linger: u16 };
        const l = L{ .onoff = 1, .linger = 0 };
        std.posix.setsockopt(fd, std.posix.SOL.SOCKET, std.posix.SO.LINGER, std.mem.asBytes(&l)) catch {};
    } else {
        const L = extern struct { onoff: c_int, linger: c_int };
        const l = L{ .onoff = 1, .linger = 0 };
        std.posix.setsockopt(fd, std.posix.SOL.SOCKET, std.posix.SO.LINGER, std.mem.asBytes(&l)) catch {};
    }
}

fn contentLength(head: []const u8) ?usize {
    var it = std.mem.splitSequence(u8, head, "\r\n");
    while (it.next()) |line| {
        const colon = std.mem.indexOfScalar(u8, line, ':') orelse continue;
        if (!std.ascii.eqlIgnoreCase(std.mem.trim(u8, line[0..colon], " "), "content-length")) continue;
        return std.fmt.parseInt(usize, std.mem.trim(u8, line[colon + 1 ..], " \t"), 10) catch null;
    }
    return null;
}

/// One request on a connection of its own: true for a 200, false for another status.
fn one(ctx: *const Ctx, buf: []u8) !bool {
    const s = try std.net.tcpConnectToAddress(ctx.addr);
    defer {
        lingerZero(s.handle);
        s.close();
    }
    var off: usize = 0;
    while (off < ctx.request.len) {
        const n = try std.posix.send(s.handle, ctx.request[off..], 0);
        if (n == 0) return error.Closed;
        off += n;
    }
    var got: usize = 0;
    var body_from: ?usize = null;
    var want: ?usize = null;
    while (true) {
        if (got == buf.len) return error.TooLarge;
        const n = try std.posix.recv(s.handle, buf[got..], 0);
        if (n == 0) break;
        got += n;
        if (body_from == null) {
            if (std.mem.indexOf(u8, buf[0..got], "\r\n\r\n")) |he| {
                body_from = he + 4;
                want = contentLength(buf[0..he]);
            }
        }
        if (body_from) |b| {
            if (want) |w| {
                if (got >= b + w) break;
            }
        }
    }
    if (body_from == null) return error.NoHead;
    return std.mem.startsWith(u8, buf[0..got], "HTTP/1.1 200") or std.mem.startsWith(u8, buf[0..got], "HTTP/1.0 200");
}

fn worker(ctx: *const Ctx, res: *Result) void {
    const a = std.heap.page_allocator;
    var buf: [1 << 16]u8 = undefined;
    while (true) {
        const t0 = std.time.Instant.now() catch return;
        const since = t0.since(ctx.start);
        if (since >= ctx.end_ns) break;
        const ok = one(ctx, &buf) catch {
            if (since >= ctx.warm_ns) res.errors += 1;
            continue;
        };
        const t1 = std.time.Instant.now() catch return;
        if (since < ctx.warm_ns) continue;
        if (!ok) {
            res.non200 += 1;
            continue;
        }
        const us = t1.since(t0) / 1000;
        res.lat.append(a, @intCast(@min(us, std.math.maxInt(u32)))) catch {};
    }
}

pub fn main() !void {
    const a = std.heap.page_allocator;
    const args = try std.process.argsAlloc(a);
    if (args.len != 6) {
        std.debug.print("usage: loadgen <port> <path> <connections> <seconds> <warmup-seconds>\n", .{});
        std.process.exit(2);
    }
    const port = try std.fmt.parseInt(u16, args[1], 10);
    const path = args[2];
    const conns = try std.fmt.parseInt(usize, args[3], 10);
    const secs = try std.fmt.parseFloat(f64, args[4]);
    const warm = try std.fmt.parseFloat(f64, args[5]);
    const request = try std.fmt.allocPrint(a, "GET {s} HTTP/1.1\r\nHost: 127.0.0.1:{d}\r\nConnection: close\r\n\r\n", .{ path, port });
    const ctx = Ctx{
        .addr = try std.net.Address.parseIp4("127.0.0.1", port),
        .request = request,
        .start = try std.time.Instant.now(),
        .warm_ns = @intFromFloat(warm * 1e9),
        .end_ns = @intFromFloat((warm + secs) * 1e9),
    };
    const results = try a.alloc(Result, conns);
    for (results) |*r| r.* = .{};
    const threads = try a.alloc(std.Thread, conns);
    for (threads, 0..) |*t, i| t.* = try std.Thread.spawn(.{}, worker, .{ &ctx, &results[i] });
    for (threads) |t| t.join();

    var all = std.ArrayListUnmanaged(u32){};
    var errors: u64 = 0;
    var non200: u64 = 0;
    for (results) |r| {
        try all.appendSlice(a, r.lat.items);
        errors += r.errors;
        non200 += r.non200;
    }
    std.mem.sort(u32, all.items, {}, std.sort.asc(u32));
    const n = all.items.len;
    const pct = struct {
        fn f(xs: []const u32, p: f64) u32 {
            if (xs.len == 0) return 0;
            const i: usize = @intFromFloat(@floor(p * @as(f64, @floatFromInt(xs.len))));
            return xs[@min(i, xs.len - 1)];
        }
    }.f;
    var out: [512]u8 = undefined;
    const line = try std.fmt.bufPrint(&out, "{{\"n\":{d},\"rps\":{d:.1},\"p50_us\":{d},\"p90_us\":{d},\"p99_us\":{d},\"max_us\":{d},\"errors\":{d},\"non200\":{d}}}\n", .{
        n,
        @as(f64, @floatFromInt(n)) / secs,
        pct(all.items, 0.5),
        pct(all.items, 0.9),
        pct(all.items, 0.99),
        if (n > 0) all.items[n - 1] else 0,
        errors,
        non200,
    });
    try std.fs.File.stdout().writeAll(line);
}
