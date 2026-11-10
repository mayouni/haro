//! Haro's decimal (v0.52, D55 T4): an exact base-10 number, a 64-bit coefficient and a scale -- the digits after its point, 0 to 18.
//! `12.50` is 1250 at scale 2. Pure arithmetic, no VM: main.zig calls it from the paths only code of a .haro file reaches.
//!
//!   + -     exact at the larger scale            * exact, the scales added
//!   /       the exact quotient in the fewest digits, or `inexact` when it has no end (1 / 3)
//!   divRound  the quotient rounded half to even, to the places asked (Haro's `Divide`)
//!   past 64 bits of coefficient or 18 digits of scale: `overflow`
const std = @import("std");

pub const MAX_SCALE: u32 = 18;

pub const Dec = struct { c: i64, s: u32 };

pub const Fail = error{ overflow, inexact, zero };

const POW10 = blk: {
    var p: [39]i128 = undefined;
    p[0] = 1;
    var i: usize = 1;
    while (i < 39) : (i += 1) p[i] = p[i - 1] * 10;
    break :blk p;
};

fn fit(v: i128) Fail!i64 {
    if (v > std.math.maxInt(i64) or v < std.math.minInt(i64)) return error.overflow;
    return @intCast(v);
}

/// `x` brought to scale `s` (s >= x.s), as an i128
fn up(x: Dec, s: u32) i128 {
    return @as(i128, x.c) * POW10[s - x.s];
}

pub fn add(a: Dec, b: Dec) Fail!Dec {
    const s = @max(a.s, b.s);
    return .{ .c = try fit(up(a, s) + up(b, s)), .s = s };
}

pub fn sub(a: Dec, b: Dec) Fail!Dec {
    const s = @max(a.s, b.s);
    return .{ .c = try fit(up(a, s) - up(b, s)), .s = s };
}

pub fn mul(a: Dec, b: Dec) Fail!Dec {
    const s = a.s + b.s;
    if (s > MAX_SCALE) return error.overflow;
    return .{ .c = try fit(@as(i128, a.c) * @as(i128, b.c)), .s = s };
}

/// -1, 0 or 1, by value: 0.10 and 0.1 are equal
/// the remainder with the dividend's sign, at the larger scale (C's fmod, exact)
pub fn rem(a: Dec, b: Dec) Fail!Dec {
    if (b.c == 0) return error.zero;
    const s = @max(a.s, b.s);
    return .{ .c = try fit(@rem(up(a, s), up(b, s))), .s = s };
}

pub fn cmp(a: Dec, b: Dec) i32 {
    const s = @max(a.s, b.s);
    const x = up(a, s);
    const y = up(b, s);
    return if (x < y) -1 else if (x > y) 1 else 0;
}

fn gcd(a0: u128, b0: u128) u128 {
    var a = a0;
    var b = b0;
    while (b != 0) {
        const t = a % b;
        a = b;
        b = t;
    }
    return a;
}

/// The exact quotient, in the fewest digits after its point: it exists when the reduced divisor is 2^p 5^q, and its scale is then
/// max(p, q) less the scales' difference; trailing zeros after the point are dropped.
pub fn div(a: Dec, b: Dec) Fail!Dec {
    if (b.c == 0) return error.zero;
    if (a.c == 0) return .{ .c = 0, .s = 0 };
    const neg = (a.c < 0) != (b.c < 0);
    var n: u128 = @abs(@as(i128, a.c));
    var d: u128 = @abs(@as(i128, b.c));
    const g = gcd(n, d);
    n /= g;
    d /= g;
    var p: u32 = 0;
    var q: u32 = 0;
    while (d % 2 == 0) : (p += 1) d /= 2;
    while (d % 5 == 0) : (q += 1) d /= 5;
    if (d != 1) return error.inexact;
    const m = @max(p, q);
    // n / (2^p 5^q) = n 2^(m-p) 5^(m-q) / 10^m
    var coeff: u128 = n;
    var k: u32 = 0;
    while (k < m - p) : (k += 1) coeff = std.math.mul(u128, coeff, 2) catch return error.overflow;
    k = 0;
    while (k < m - q) : (k += 1) coeff = std.math.mul(u128, coeff, 5) catch return error.overflow;
    // the value is coeff * 10^-(m) * 10^(b.s - a.s)
    var scale: i64 = @as(i64, m) + @as(i64, a.s) - @as(i64, b.s);
    if (scale < 0) {
        coeff = std.math.mul(u128, coeff, @intCast(POW10[@intCast(-scale)])) catch return error.overflow;
        scale = 0;
    }
    while (scale > 0 and coeff % 10 == 0) : (scale -= 1) coeff /= 10;
    if (scale > MAX_SCALE) return error.inexact;
    if (coeff > std.math.maxInt(i64)) return error.overflow;
    const c: i64 = @intCast(coeff);
    return .{ .c = if (neg) -c else c, .s = @intCast(scale) };
}

/// n / d rounded half to even, both non-negative-signed by `neg`
fn roundHalfEven(n: u128, d: u128) u128 {
    const q = n / d;
    const r = n % d;
    const twice = r * 2;
    if (twice > d or (twice == d and q % 2 == 1)) return q + 1;
    return q;
}

/// a / b rounded half to even to `places` digits after the point (Haro's `Divide(a, b, iPlaces)`)
pub fn divRound(a: Dec, b: Dec, places: u32) Fail!Dec {
    if (b.c == 0) return error.zero;
    if (places > MAX_SCALE) return error.overflow;
    const neg = (a.c < 0) != (b.c < 0);
    // value * 10^places = a.c * 10^(places + b.s - a.s) / b.c
    const e: i64 = @as(i64, places) + @as(i64, b.s) - @as(i64, a.s);
    var n: u128 = @abs(@as(i128, a.c));
    var d: u128 = @abs(@as(i128, b.c));
    if (e >= 0) {
        n = std.math.mul(u128, n, @intCast(POW10[@intCast(e)])) catch return error.overflow;
    } else {
        d = std.math.mul(u128, d, @intCast(POW10[@intCast(-e)])) catch return error.overflow;
    }
    const q = roundHalfEven(n, d);
    if (q > std.math.maxInt(i64)) return error.overflow;
    const c: i64 = @intCast(q);
    return .{ .c = if (neg) -c else c, .s = places };
}

/// `x` rounded half to even to `places` (or widened with zeros when it has fewer)
pub fn round(x: Dec, places: u32) Fail!Dec {
    if (places > MAX_SCALE) return error.overflow;
    if (places >= x.s) return .{ .c = try fit(up(x, places)), .s = places };
    return divRound(x, .{ .c = 1, .s = 0 }, places);
}

pub fn toF64(x: Dec) f64 {
    return @as(f64, @floatFromInt(x.c)) / @as(f64, @floatFromInt(POW10[x.s]));
}

/// whole: its integer, or null
pub fn whole(x: Dec) ?i64 {
    const p: i64 = @intCast(POW10[x.s]);
    if (@rem(x.c, p) != 0) return null;
    return @divTrunc(x.c, p);
}

/// The value's digits: `-1.50`, `0.005`, `12`
pub fn text(x: Dec, buf: []u8) []const u8 {
    const neg = x.c < 0;
    const mag: u64 = @abs(x.c);
    var digits: [24]u8 = undefined;
    const ds = std.fmt.bufPrint(&digits, "{d}", .{mag}) catch return "0";
    var w: usize = 0;
    if (neg) {
        buf[0] = '-';
        w = 1;
    }
    if (x.s == 0) {
        @memcpy(buf[w .. w + ds.len], ds);
        return buf[0 .. w + ds.len];
    }
    if (ds.len <= x.s) {
        buf[w] = '0';
        buf[w + 1] = '.';
        w += 2;
        var z: usize = 0;
        while (z < x.s - ds.len) : (z += 1) {
            buf[w] = '0';
            w += 1;
        }
        @memcpy(buf[w .. w + ds.len], ds);
        return buf[0 .. w + ds.len];
    }
    const ip = ds.len - x.s;
    @memcpy(buf[w .. w + ip], ds[0..ip]);
    w += ip;
    buf[w] = '.';
    w += 1;
    @memcpy(buf[w .. w + x.s], ds[ip..]);
    return buf[0 .. w + x.s];
}

/// A literal or a text: `[-]digits[.digits]`, its scale the digits written after the point. Null when it is no decimal; `overflow`
/// when it holds more than the coefficient or the scale can.
pub fn parse(s0: []const u8) Fail!?Dec {
    var s = s0;
    var neg = false;
    if (s.len > 0 and (s[0] == '-' or s[0] == '+')) {
        neg = s[0] == '-';
        s = s[1..];
    }
    if (s.len == 0) return null;
    var c: i128 = 0;
    var scale: u32 = 0;
    var seen_point = false;
    var digits: u32 = 0;
    for (s) |ch| {
        if (ch == '.') {
            if (seen_point) return null;
            seen_point = true;
            continue;
        }
        if (ch < '0' or ch > '9') return null;
        c = c * 10 + (ch - '0');
        digits += 1;
        if (c > std.math.maxInt(i64)) return error.overflow;
        if (seen_point) scale += 1;
    }
    if (digits == 0) return null;
    if (scale > MAX_SCALE) return error.overflow;
    const v: i64 = @intCast(c);
    return .{ .c = if (neg) -v else v, .s = scale };
}

/// A float rounded half to even to `places`, read off its shortest exact rendering at that precision
pub fn fromF64(f: f64, places: u32) Fail!Dec {
    if (places > MAX_SCALE or !std.math.isFinite(f)) return error.overflow;
    var buf: [400]u8 = undefined;
    const t = std.fmt.bufPrint(&buf, "{d:.[1]}", .{ f, places }) catch return error.overflow;
    return (try parse(t)) orelse error.overflow;
}

/// fromF64, for a caller that answers none as well
pub fn fromF64Opt(f: f64, places: u32) Fail!?Dec {
    return try fromF64(f, places);
}

test "decimal" {
    var b: [64]u8 = undefined;
    try std.testing.expectEqualStrings("0.3", text(try add(.{ .c = 1, .s = 1 }, .{ .c = 2, .s = 1 }), &b));
    try std.testing.expectEqualStrings("3.5", text(try div(.{ .c = 7, .s = 0 }, .{ .c = 2, .s = 0 }), &b));
    try std.testing.expectEqualStrings("0.125", text(try div(.{ .c = 1, .s = 0 }, .{ .c = 8, .s = 0 }), &b));
    try std.testing.expectEqualStrings("3", text(try div(.{ .c = 15, .s = 1 }, .{ .c = 5, .s = 1 }), &b));
    try std.testing.expectError(error.inexact, div(.{ .c = 1, .s = 0 }, .{ .c = 3, .s = 0 }));
    try std.testing.expectEqualStrings("0.12", text(try divRound(.{ .c = 1, .s = 0 }, .{ .c = 8, .s = 0 }, 2), &b));
    try std.testing.expectEqualStrings("-0.33", text(try divRound(.{ .c = -1, .s = 0 }, .{ .c = 3, .s = 0 }, 2), &b));
    try std.testing.expectEqualStrings("-1.50", text(.{ .c = -150, .s = 2 }, &b));
    try std.testing.expectEqualStrings("0.005", text(.{ .c = 5, .s = 3 }, &b));
}
