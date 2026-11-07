"""Scratch: wrap the VM's slow paths, equality jumps and truth ops with the V43 census. Never committed."""
import re, sys
p = r"D:\GitHub\haro\vm\src\main.zig"
s = open(p, encoding="utf-8", newline="").read()
n0 = len(s)

# arithmetic and + slow paths: self.arithSlow(base + in.a, OP, X, Y) / self.addSlow(base + in.a, base + in.b, X, Y, F)
def wrap_arith(m):
    op, x, y = m.group(1), m.group(2), m.group(3)
    return f'self.cenThen(pc, "arith{op}", {x}, {y}, self.arithSlow(base + in.a, {op}, {x}, {y}))'
s, k1 = re.subn(r'self\.arithSlow\(base \+ in\.a, (\.\w+|aop), (\w+|Value\.int\(in\.d\)), (\w+|Value\.int\(in\.d\))\)', wrap_arith, s)

def wrap_add(m):
    x, y, f = m.group(1), m.group(2), m.group(3)
    return f'self.cenThen(pc, "add", {x}, {y}, self.addSlow(base + in.a, base + in.b, {x}, {y}, {f}))'
s, k2 = re.subn(r'self\.addSlow\(base \+ in\.a, base \+ in\.b, (\w+|Value\.int\(in\.d\)), (\w+|Value\.int\(in\.d\)), ([^)]*\)?)\)', wrap_add, s)

# equality jumps
s, k3 = re.subn(r'if \(valEq\(regs\[base \+ in\.a\], regs\[base \+ in\.b\]\)\) \{',
                'self.cenEq(pc, regs[base + in.a], regs[base + in.b]);\n                if (valEq(regs[base + in.a], regs[base + in.b])) {', s)
s, k4 = re.subn(r'if \(!valEq\(regs\[base \+ in\.a\], regs\[base \+ in\.b\]\)\) \{',
                'self.cenEq(pc, regs[base + in.a], regs[base + in.b]);\n                if (!valEq(regs[base + in.a], regs[base + in.b])) {', s)
# ordering with a text and a number
s, k5 = re.subn(r'(\n\s*)if \(valCmp\(regs\[base \+ in\.a\], regs\[base \+ in\.b\]\) ',
                r'\1self.cenEq(pc, regs[base + in.a], regs[base + in.b]);\1if (valCmp(regs[base + in.a], regs[base + in.b]) ', s)
# truth
s, k6 = re.subn(r'if \(!truthy\(regs\[base \+ in\.a\]\)\) \{', 'self.cenTruth(pc, regs[base + in.a]);\n                if (!truthy(regs[base + in.a])) {', s)
s, k7 = re.subn(r'if \(truthy\(regs\[base \+ in\.a\]\)\) \{', 'self.cenTruth(pc, regs[base + in.a]);\n                if (truthy(regs[base + in.a])) {', s)
s, k8 = re.subn(r'Value\.int\(if \(truthy\(regs\[base \+ in\.b\]\)\) (\d) else (\d)\)',
                r'Value.int(if (self.cenTruthB(pc, regs[base + in.b])) \1 else \2)', s)

helpers = '''
    fn cenThen(self: *VM, pc: u32, what: []const u8, x: Value, y: Value, r: ?[]const u8) ?[]const u8 {
        if ((x.tag == .str) != (y.tag == .str) and x.tag != .vec and y.tag != .vec) self.censusPair(pc, what, x, y);
        return r;
    }
    fn cenEq(self: *VM, pc: u32, x: Value, y: Value) void {
        if (x.tag == y.tag) return;
        if (isNum(x) and isNum(y)) return;
        self.censusPair(pc, "cmp", x, y);
    }
    fn cenTruth(self: *VM, pc: u32, v: Value) void {
        if (v.tag == .int and (v.p.i == 0 or v.p.i == 1)) return;
        var b: [64]u8 = undefined;
        const k = if (v.tag == .int) "cond:int-not-0-or-1" else (std.fmt.bufPrint(&b, "cond:{s}", .{@tagName(v.tag)}) catch return);
        self.census(pc, k);
    }
    fn cenTruthB(self: *VM, pc: u32, v: Value) bool {
        self.cenTruth(pc, v);
        return truthy(v);
    }
'''
s = s.replace("    fn valEq(a: Value, b: Value) bool {", helpers + "\n    fn valEq(a: Value, b: Value) bool {", 1)
open(p, "w", encoding="utf-8", newline="").write(s)
print("arith", k1, "add", k2, "eq", k3, "ne", k4, "order", k5, "jfalsy", k6, "jtruthy", k7, "truth/lnot", k8, "bytes", n0, "->", len(s))
