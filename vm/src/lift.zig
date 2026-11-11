//! RING'S `not`, AS RING READS IT (C-32, F-130).
//!
//! Ring binds `not` and `!` LOOSER than every comparison and arithmetic operator and TIGHTER than `and` and `or`: `not a = b` is
//! `not (a = b)`, `not a + b` is `not (a + b)`, `not a < b and c` is `(not (a < b)) and c` (measured on the oracle and the official 1.27,
//! bench/exec/not_precedence.ring). tree-sitter-ring binds them like a unary minus, tighter than every binary operator -- its table names
//! PREC.NOT = 4 and never uses it -- so `not a = b` arrives as `(not a) = b` and compiled to another program: a silent wrong answer.
//!
//! The tree cannot be edited, and the compiler reads the shape of a chain in some thirty places (the classes, the element classes, the
//! append idiom, the condition jumps), so the fix is made where the tree is made: a `not` that is the leftmost operand of a chain of
//! tighter binary operators gets parentheses round the chain, in the text the compiler is handed, and the text is parsed again. What the
//! compiler reads is then what Ring reads, in every place at once, and a file with no such `not` is untouched -- the same tree, the same
//! bytes. A `not` under parentheses is its own operand and is left alone; `and`/`or` end the chain; a `not` that is the RIGHT operand
//! of a tighter operator (`a = not b`) is Ring's error C28 and is not touched.
//!
//! The text the compiler holds is therefore not always the file's. Whoever needs the file's bytes -- the image stamps, a byte offset
//! printed for an applier -- takes them from the original (rnxc.zig, `Unit.origs`).

const std = @import("std");
const ts = @import("ts.zig");
const c = ts.c;

/// What the estate costs, for the census: the `not`s lifted, the files that held one, the nanoseconds spent looking.
pub var sites: u32 = 0;
pub var files: u32 = 0;
pub var ns: u64 = 0;
/// the part of `ns` spent parsing the rewritten text
pub var ns_reparse: u64 = 0;
/// the `catch e` lifted to `catch(e)` (D52 rung 2)
pub var catch_sites: u32 = 0;
/// the `within` and `using` blocks rewritten onto `try ... finally` (D52 rung 3)
pub var block_sites: u32 = 0;
/// RNXC_LIFT_TRACE=1: every site, as file:line and the chain it covers, on stderr (set by rnxc.zig)
pub var trace: bool = false;
var file_name: []const u8 = "";

/// What the lift made of a file: the tree, the text it indexes, and what was put in to make that text from the file's.
// ---- HARO-SURFACE-01: the extension says how a file is read (the author's rulings of 2026-11-06; v41/GRAMMAR.md)

/// The Ring keywords: vendor/tree-sitter-ring/grammar.js's keyword() words, exactly (v41/surface_court.py checks the two lists agree).
pub const ring_keywords = [_][]const u8{
    "again", "and", "break", "but", "bye", "call", "case", "catch", "changeringkeyword", "changeringoperator", "class", "continue", "def",
    "disablehashcomments", "do", "done", "else", "elseif", "enablehashcomments", "end", "endclass", "endfor", "endfunc", "endfunction",
    "endif", "endpackage", "endswitch", "endtry", "endwhile", "exit", "false", "finally", "for", "foreach", "from", "func", "function",
    "get", "give", "if", "import", "load", "loadsyntax", "loop", "new", "next", "not", "null", "off", "ok", "on", "or", "other", "package",
    "private", "put", "return", "see", "self", "super", "switch", "this", "true", "try", "while",
};

/// A file is read by Haro's rules when its name ends .haro -- a keyword in lowercase only, a symbol as written, no `:key = value` -- and by
/// Ring's otherwise, so Softanza's code reads exactly as it did.
pub fn isHaro(path: []const u8) bool {
    return std.mem.endsWith(u8, path, ".haro");
}

/// Whether the program's root file is a .haro file: an eval reads its text by the root's rules (S5). Set by the loader.
pub var haro_root: bool = false;

fn ringKeyword(w: []const u8) bool {
    for (ring_keywords) |k| {
        if (std.ascii.eqlIgnoreCase(k, w)) return true;
    }
    return false;
}

/// A byte of a name, as grammar.js's IDENT_CLASS has it: anything but blank and the operator, quote and comment characters.
fn nameByte(b: u8) bool {
    if (b == ' ' or b == '\t' or b == '\n' or b == '\r') return false;
    return std.mem.indexOfScalar(u8, ";\"'`#+*/%.,()=<>![]{}:&|~^?-", b) == null;
}

/// Every word outside the strings and comments that is a Ring keyword written in a case other than lowercase. Found lexically: Ring's text has
/// no escapes, so a string runs from a quote to the same quote, and a comment from # or // to the end of the line or from /* to */. Not from
/// the parse: a .ring file read by the lowercase-only grammar is a cascade of error recovery, in which a string can be misjudged and swallow
/// code, and the leaves fold skipped text (v41's stzlib A/B: three `NOT (` in stzListFunc.ring stayed a name).
fn ringSpans(alloc: std.mem.Allocator, src: []const u8, out: *std.ArrayListUnmanaged([2]u32)) !void {
    var i: usize = 0;
    const n = src.len;
    while (i < n) {
        const ch = src[i];
        if (ch == '"' or ch == '\'' or ch == '`') {
            // an unclosed quote is no string to the grammar: only the quote is passed, and what follows is read as code, as the grammar reads it
            const j = std.mem.indexOfScalarPos(u8, src, i + 1, ch) orelse n;
            i = if (j >= n) i + 1 else j + 1;
            continue;
        }
        if (ch == '#' or (ch == '/' and i + 1 < n and src[i + 1] == '/')) {
            i = std.mem.indexOfScalarPos(u8, src, i, '\n') orelse n;
            continue;
        }
        if (ch == '/' and i + 1 < n and src[i + 1] == '*') {
            // an unclosed `/*` is no comment to the grammar (stzlib's datetime/48_custom_format_strings.ring): what follows is read as code
            const j = std.mem.indexOfPos(u8, src, i + 2, "*/") orelse n;
            i = if (j >= n) i + 2 else j + 2;
            continue;
        }
        if (!nameByte(ch)) {
            i += 1;
            continue;
        }
        var j = i;
        while (j < n and nameByte(src[j])) j += 1;
        const w = src[i..j];
        if (w.len <= 24 and ringKeyword(w)) {
            for (w) |c2| {
                if (std.ascii.isUpper(c2)) {
                    try out.append(alloc, .{ @intCast(i), @intCast(j) });
                    break;
                }
            }
        }
        i = j;
    }
}

/// Parse `src` by the rules of its file. A .haro file is parsed as written: the grammar's keywords are lowercase, and any other spelling is a
/// name (S1). Any other file is read as Ring reads it, a keyword in any case (S2): its keyword-shaped words written in another case are lowered
/// and the text parsed again -- the same length, so every byte offset and column is the file's, and the tree is the one the case-insensitive
/// grammar made of the same text. A reader that prints the file's bytes takes them by span from the original (fmt, dumpjson, dump).
pub fn parse(alloc: std.mem.Allocator, parser: ts.Parser, src: []const u8, haro: bool) ?Lifted {
    if (haro) return .{ .tree = parser.parse(src) orelse return null, .src = src };
    // the words are found lexically, so the file is lowered BEFORE its one parse (a parse then a reparse cost a .ring file twice)
    var spans = std.ArrayListUnmanaged([2]u32){};
    defer spans.deinit(alloc);
    ringSpans(alloc, src, &spans) catch return .{ .tree = parser.parse(src) orelse return null, .src = src };
    if (spans.items.len == 0) return .{ .tree = parser.parse(src) orelse return null, .src = src };
    const text = alloc.dupe(u8, src) catch return null;
    for (spans.items) |sp| {
        for (text[sp[0]..sp[1]]) |*ch| ch.* = std.ascii.toLower(ch.*);
    }
    const tree = parser.parse(text) orelse return null;
    ring_case_files += 1;
    return .{ .tree = tree, .src = text };
}

/// the .ring files whose keywords were lowered to be read as Ring reads them, for the census
pub var ring_case_files: u32 = 0;

pub const Lifted = struct { tree: ts.Tree, src: []const u8, inserts: []const Insert = &.{} };

/// `len` bytes the lift put in before byte `pos` of the FILE's text; a list of them is in text order.
pub const Insert = struct { pos: u32, len: u32 };

/// The byte of the file's text that byte `at` of the lifted text came from; a byte the lift put in is the place it was put (v0.39: the
/// checker reads the lifted tree and names the file's own columns).
pub fn fileByte(inserts: []const Insert, at: u32) u32 {
    var shift: u32 = 0;
    for (inserts) |x| {
        const start = x.pos + shift;
        if (at < start) break;
        if (at < start + x.len) return x.pos;
        shift += x.len;
    }
    return at - shift;
}

/// `prior` in the file's coordinates, `edits` (sorted) in those of the text `prior` made: the two in the file's, in text order. An edit at the
/// place an earlier insert begins goes before it, as splice puts it.
fn compose(alloc: std.mem.Allocator, prior: []const Insert, edits: []const Edit) ?[]const Insert {
    const out = alloc.alloc(Insert, prior.len + edits.len) catch return null;
    var i: usize = 0;
    var j: usize = 0;
    var k: usize = 0;
    var shift: u32 = 0;
    while (j < edits.len) {
        if (i < prior.len and prior[i].pos + shift < edits[j].pos) {
            out[k] = prior[i];
            shift += prior[i].len;
            i += 1;
        } else {
            out[k] = .{ .pos = edits[j].pos - shift, .len = @intCast(piece(edits[j]).len) };
            j += 1;
        }
        k += 1;
    }
    while (i < prior.len) : (i += 1) {
        out[k] = prior[i];
        k += 1;
    }
    return out;
}

/// A parenthesis to put in at `pos`, or, when `text` is given, that text.
const Edit = struct { pos: u32, close: bool, text: []const u8 = "" };

fn piece(e: Edit) []const u8 {
    return if (e.text.len > 0) e.text else if (e.close) ")" else "(";
}

fn eq(a: []const u8, b: []const u8) bool {
    return std.mem.eql(u8, a, b);
}

fn sameNode(a: ts.Node, b: ts.Node) bool {
    return c.ts_node_eq(a.raw, b.raw);
}

/// `not x` and `!x`, by the operator token the compiler tests (compile.zig, `opText`).
fn isNot(n: ts.Node) bool {
    if (!eq(n.kind(), "unary_expression")) return false;
    var i: u32 = 0;
    while (i < n.childCount()) : (i += 1) {
        const ch = n.child(i);
        if (ch.isNamed()) continue;
        const k = ch.kind();
        return eq(k, "not") or eq(k, "!");
    }
    return false;
}

/// A node whose operator binds tighter than `not`: every binary operator but `and`/`or`, and the `=` the grammar calls an assignment
/// where a value is wanted (an equality, there). The compound assignments are statements and are not a chain.
fn isChain(n: ts.Node) bool {
    const k = n.kind();
    const binary = eq(k, "binary_expression");
    if (!binary and !eq(k, "assignment_expression")) return false;
    if (n.namedChildCount() < 2) return false;
    var i: u32 = 0;
    while (i < n.childCount()) : (i += 1) {
        const ch = n.child(i);
        if (ch.isNamed()) continue;
        const op = ch.kind();
        if (binary) return !(eq(op, "and") or eq(op, "or") or eq(op, "&&") or eq(op, "||"));
        return eq(op, "=");
    }
    return false;
}

/// `and`, `or`, `&&`, `||`: the operators that end a chain
fn isLogic(n: ts.Node) bool {
    if (!eq(n.kind(), "binary_expression")) return false;
    var i: u32 = 0;
    while (i < n.childCount()) : (i += 1) {
        const ch = n.child(i);
        if (ch.isNamed()) continue;
        const op = ch.kind();
        return eq(op, "and") or eq(op, "or") or eq(op, "&&") or eq(op, "||");
    }
    return false;
}

/// The first named child that is not a comment (a comment can stand among an expression's operands).
fn firstOperand(n: ts.Node) ?ts.Node {
    var i: u32 = 0;
    const cnt = n.namedChildCount();
    while (i < cnt and i < 8) : (i += 1) {
        const ch = n.namedChild(i);
        if (!eq(ch.kind(), "comment")) return ch;
    }
    return null;
}

/// The last byte of what a chain's last operand really ends in: a trailing comment may be a child of the expression and must stay outside
/// the parenthesis it would swallow.
fn lastByte(n_in: ts.Node) u32 {
    var n = n_in;
    while (eq(n.kind(), "binary_expression") or eq(n.kind(), "assignment_expression") or eq(n.kind(), "unary_expression")) {
        var i = n.namedChildCount();
        var last: ?ts.Node = null;
        while (i > 0) {
            i -= 1;
            const ch = n.namedChild(i);
            if (!eq(ch.kind(), "comment")) {
                last = ch;
                break;
            }
        }
        n = last orelse break;
    }
    return n.endByte();
}

/// Is there an `=` in the chain that Ring's parser may read as an ASSIGNMENT?
fn hasEquals(n: ts.Node, depth: u32) bool {
    if (depth > 64) return true;
    const k = n.kind();
    if (eq(k, "assignment_expression")) return true;
    if (!eq(k, "binary_expression")) return false;
    var i: u32 = 0;
    while (i < n.childCount()) : (i += 1) {
        const ch = n.child(i);
        if (!ch.isNamed()) {
            if (eq(ch.kind(), "=")) return true;
        } else if (hasEquals(ch, depth + 1)) return true;
    }
    return false;
}

/// Does only blank stand before `n` on its line?
fn startsLine(n: ts.Node) bool {
    var i = n.startByte();
    while (i > 0) {
        i -= 1;
        const ch = n.src[i];
        if (ch == '\n') return true;
        if (ch != ' ' and ch != '\t' and ch != '\r') return false;
    }
    return true;
}

/// Where the chain `t` ends. The grammar reads a statement-initial `x = y or z` as the ASSIGNMENT x = (y or z), its right side taking the `or`
/// and everything after; Ring reads `(x = y) or z`. So when the chain is such an assignment, it ends where the first `and`/`or` on the left
/// spine of its right side begins -- what stands tighter than the `or` is the `=`'s right operand, `= c` and `+ d` included.
fn chainEnd(t: ts.Node) u32 {
    if (!eq(t.kind(), "assignment_expression")) return lastByte(t);
    var i = t.namedChildCount();
    var r: ?ts.Node = null;
    while (i > 0) {
        i -= 1;
        const ch = t.namedChild(i);
        if (!eq(ch.kind(), "comment")) {
            r = ch;
            break;
        }
    }
    var n = r orelse return lastByte(t);
    while (isLogic(n)) n = firstOperand(n) orelse return lastByte(t);
    return lastByte(n);
}

/// Every `not` that leads a chain: the parentheses go round the operand of the `not` and the chain it leads.
fn findSites(alloc: std.mem.Allocator, root: ts.Node, out: *std.ArrayListUnmanaged(Edit)) !void {
    var cur = c.ts_tree_cursor_new(root.raw);
    defer c.ts_tree_cursor_delete(&cur);
    // the ancestors of the node under the cursor, the root first
    var path = std.ArrayListUnmanaged(ts.Node){};
    defer path.deinit(alloc);
    while (true) {
        const raw = c.ts_tree_cursor_current_node(&cur);
        const node = ts.Node{ .raw = raw, .src = root.src };
        if (node.isNamed() and path.items.len > 0 and isNot(node) and !node.hasError()) try site(alloc, node, path.items, out);
        if (c.ts_tree_cursor_goto_first_child(&cur)) {
            try path.append(alloc, node);
            continue;
        }
        while (!c.ts_tree_cursor_goto_next_sibling(&cur)) {
            if (!c.ts_tree_cursor_goto_parent(&cur)) return;
            _ = path.pop();
        }
    }
}

fn site(alloc: std.mem.Allocator, u: ts.Node, path: []const ts.Node, out: *std.ArrayListUnmanaged(Edit)) !void {
    // the chain starts where this `not` is its parent's FIRST operand...
    var top = path.len - 1;
    if (!isChain(path[top])) return;
    const first = firstOperand(path[top]) orelse return;
    if (!sameNode(first, u)) return;
    // ...and goes up as long as each node is the first operand of a chain node: that is where Ring's `not` ends
    while (top > 0) {
        const g = path[top - 1];
        if (!isChain(g)) break;
        const f = firstOperand(g) orelse break;
        if (!sameNode(f, path[top])) break;
        top -= 1;
    }
    const t = path[top];
    if (t.hasError()) return;
    // A STATEMENT that begins its line is the one place Ring's parser still has its assignment flag up (lAssignmentFlag, expr.c): there an
    // identifier followed by `=` is an ASSIGNMENT, whatever stands before it -- `not a = b` sets a to b, `not a = b and c` sets it to
    // `b and c`, `not Id(a) = b` is R34 (measured on the oracle and the official 1.27). Every other place that holds an expression (the
    // arguments, the conditions, `return`, `?`, the right of an assignment) clears it, and `=` is the comparison. rnxc refuses the
    // statement, loudly, and a lift would turn that refusal into a quiet comparison: so it is left as it is. A `return` the grammar cut
    // from its value does not begin its line.
    if (top > 0 and eq(path[top - 1].kind(), "expression_statement") and startsLine(t) and hasEquals(t, 0)) return;
    const x = firstOperand(u) orelse return;
    const open = x.startByte();
    const close = chainEnd(t);
    if (close <= open) return;
    if (trace) {
        const text = t.src[t.startByte()..close];
        std.debug.print("lift: {s}:{d}: {s}\n", .{ file_name, t.start().row + 1, if (text.len > 100) text[0..100] else text });
    }
    try out.append(alloc, .{ .pos = open, .close = false });
    try out.append(alloc, .{ .pos = close, .close = true });
}

fn order(_: void, a: Edit, b: Edit) bool {
    if (a.pos != b.pos) return a.pos < b.pos;
    return a.close and !b.close; // a parenthesis closes before the next one opens
}

/// `tree` is the parse of `src`. Returns the tree the compiler should read and the text its offsets index: the same two when no `not`
/// leads a chain, and the parse of the rewritten text when one does. The old tree is freed when it is replaced.
/// `catch e`, e on catch's own line (D52, A4): the grammar reads the name as a STATEMENT of the handler, which reads e; Haro's spelling
/// makes it the binding, so it gets the parentheses of `catch(e)`, the form the grammar reads as one. A name on the NEXT line is the
/// statement it always was, and is left alone (v37 G03). A comment after the name stays outside the parentheses.
fn findCatch(alloc: std.mem.Allocator, n: ts.Node, out: *std.ArrayListUnmanaged(Edit)) !void {
    if (eq(n.kind(), "catch_clause") and n.childCount() > 0) {
        const kw = n.child(0);
        if (firstOperand(n)) |st| {
            if (eq(st.kind(), "expression_statement") and st.start().row == kw.start().row) {
                var named: u32 = 0;
                var id: ?ts.Node = null;
                var i: u32 = 0;
                while (i < st.namedChildCount()) : (i += 1) {
                    const ch = st.namedChild(i);
                    if (eq(ch.kind(), "comment")) continue;
                    named += 1;
                    id = ch;
                }
                if (named == 1 and eq(id.?.kind(), "identifier") and id.?.startByte() == st.startByte()) {
                    try out.append(alloc, .{ .pos = id.?.startByte(), .close = false });
                    try out.append(alloc, .{ .pos = id.?.endByte(), .close = true });
                }
            }
        }
    }
    var i: u32 = 0;
    while (i < n.namedChildCount()) : (i += 1) try findCatch(alloc, n.namedChild(i), out);
}

/// `within` and `using` (D52 rung 3, A2 and A3). `within $g = v ... end` (v0.55, D67: every block ends with `end`; `done` before it) is
/// rewritten, on the same lines, to `try within $g = v ... finally end`, and `using` alike: a try whose body opens with the word and its header, and whose empty `finally` the compiler fills -- the restore,
/// the release (compile.zig, `blockSite`). The grammar reads both words as bare names, and reads a `done` as a bare name too, except inside a
/// try's catch or finally, where it ends that try (v38 B01). The grammar reads an `end` after them as the end of the
/// definition around them. So the tree cannot say which end closes which block; the tokens can. In document order every block statement's
/// first token and every `within` or `using` opens; every block statement's last token, every `done` -- keyword or bare name -- and every
/// end word a definition took closes, innermost first. A word with no header on its line, or with no `done`, is left as it was, and the compiler refuses it by name (B04, B05).
pub fn soleChild(n: ts.Node) ?ts.Node {
    var one: ?ts.Node = null;
    var i: u32 = 0;
    while (i < n.namedChildCount()) : (i += 1) {
        const ch = n.namedChild(i);
        if (eq(ch.kind(), "comment")) continue;
        if (one != null) return null;
        one = ch;
    }
    return one;
}

/// The word of a statement that is a bare `within` or `using`, wherever it stands.
pub fn blockWord(n: ts.Node) ?ts.Node {
    if (!eq(n.kind(), "expression_statement")) return null;
    const id = soleChild(n) orelse return null;
    if (!eq(id.kind(), "identifier")) return null;
    // Haro's words, lowercase in every file (HARO-SURFACE-01): `Within` is a name
    return if (std.mem.eql(u8, id.text(), "within") or std.mem.eql(u8, id.text(), "using")) id else null;
}

/// A statement that is a bare `within` or `using`: the head of a block -- or, left bare, a block the compiler refuses.
pub fn isMarker(n: ts.Node) bool {
    return blockWord(n) != null;
}

/// `name = value` on the marker's line: one `=`, a name on its left -- the header a block needs.
pub fn isHeader(marker: ts.Node, n: ts.Node) bool {
    if (!eq(n.kind(), "expression_statement") or n.start().row != marker.start().row) return false;
    const a = soleChild(n) orelse return false;
    if (!eq(a.kind(), "assignment_expression") or a.namedChildCount() < 2 or !eq(a.namedChild(0).kind(), "identifier")) return false;
    var i: u32 = 0;
    while (i < a.childCount()) : (i += 1) {
        if (eq(a.child(i).kind(), "=")) return true;
    }
    return false;
}

/// The statement after `n` in document order: its next sibling, or its parent's, and so on up -- the grammar can end a function's body right
/// after a bare word, and the header then stands one level up (v38 U01).
fn nextStatement(n: ts.Node) ?ts.Node {
    var cur = n;
    while (true) {
        var s = cur.nextNamedSibling();
        while (!s.isNull() and eq(s.kind(), "comment")) s = s.nextNamedSibling();
        if (!s.isNull()) return s;
        const p = cur.parent();
        if (p.isNull()) return null;
        cur = p;
    }
}

fn isBareDone(n: ts.Node) bool {
    if (!eq(n.kind(), "expression_statement")) return false;
    const id = soleChild(n) orelse return false;
    // where the grammar finds no block or definition for it, an `end` is a bare name, as `done` is (v0.55)
    return eq(id.kind(), "identifier") and (std.mem.eql(u8, id.text(), "done") or std.mem.eql(u8, id.text(), "end"));
}

const Tok = struct { pos: u32, what: enum { block, open, close } };

/// v0.55 (D67): a statement that opens a block closed by its last token
fn opensBlock(k: []const u8) bool {
    for ([_][]const u8{ "if_statement", "while_statement", "for_statement", "switch_statement", "try_statement", "do_again_statement" }) |b|
        if (eq(k, b)) return true;
    return false;
}


fn blockTokens(alloc: std.mem.Allocator, n: ts.Node, out: *std.ArrayListUnmanaged(Tok)) !void {
    const cnt = n.childCount();
    var i: u32 = 0;
    while (i < cnt) : (i += 1) {
        const ch = n.child(i);
        const k = ch.kind();
        if (ch.isNamed()) {
            if (isMarker(ch)) {
                if (nextStatement(ch)) |h| if (isHeader(ch, h)) {
                    try out.append(alloc, .{ .pos = ch.startByte(), .what = .block });
                    continue;
                };
            }
            if (isBareDone(ch)) {
                try out.append(alloc, .{ .pos = ch.startByte(), .what = .close });
                continue;
            }
            try blockTokens(alloc, ch, out);
        } else if (i == 0 and opensBlock(n.kind())) {
            try out.append(alloc, .{ .pos = ch.startByte(), .what = .open });
        } else if (eq(k, "done") or (i + 1 == cnt and opensBlock(n.kind())) or defEnd(n.kind(), k)) {
            try out.append(alloc, .{ .pos = ch.startByte(), .what = .close });
        }
    }
}

/// The last token of a definition or of a broken span, when it is an end word: a block's `end` the grammar gave to what holds it -- in an
/// eval's text, or a .ring file -- closes that block (a .haro file's definitions reach the parser in braces, so theirs never does)
fn defEnd(parent: []const u8, k: []const u8) bool {
    if (!eq(parent, "function_definition") and !eq(parent, "class_definition") and !eq(parent, "package_definition") and !eq(parent, "ERROR"))
        return false;
    return eq(k, "end") or eq(k, "endfunc") or eq(k, "endfunction") or eq(k, "endclass") or eq(k, "endpackage");
}

fn findBlocks(alloc: std.mem.Allocator, root: ts.Node, out: *std.ArrayListUnmanaged(Edit)) !void {
    var toks = std.ArrayListUnmanaged(Tok){};
    defer toks.deinit(alloc);
    try blockTokens(alloc, root, &toks);
    var open = std.ArrayListUnmanaged(Tok){};
    defer open.deinit(alloc);
    for (toks.items) |t| switch (t.what) {
        .block, .open => try open.append(alloc, t),
        .close => if (open.pop()) |o| if (o.what == .block) {
            try out.append(alloc, .{ .pos = o.pos, .close = false, .text = "try " });
            try out.append(alloc, .{ .pos = t.pos, .close = true, .text = "finally " });
        },
    };
}

/// v0.56 (D68, the Principal 2026-11-11: no position rule; `func` a function, `def` a method). In a .haro file every block and every
/// definition ends with `end`, so the file's structure is in its tokens: each opener -- if, while, for, switch, try, do, `within`/`using`
/// before a header, func, def, class, package -- is closed by the next `end` (`again` for a do) that no inner opener took. The grammar,
/// which also reads Ring's surface, cannot tell a definition's `end` from its class's in every shape (a method whose last line holds a `+`
/// lost its `end` to the class); so each definition is given to the parser in braces, which it reads one way only: ` {` after its header,
/// `}` in place of its `end`. Nothing else moves, and no line changes its number.
///
/// A file whose structure the tokens do not close is not rewritten, and the first fault is kept for the compiler, which refuses the
/// program's first statement with it: a definition without its `end`, an `end` that closes nothing, a definition's body on its header's
/// line, or an end word in another spelling.
pub const Fault = struct { why: []const u8, word: []const u8, row: u32 };

/// the fault of each .haro file read, by its name
pub var faults: std.StringHashMapUnmanaged(Fault) = .{};

pub const R_NOEND = "a definition ends with `end`, and this one has none; written";
pub const R_STRAY = "an `end` closes nothing here; written";
pub const R_ONELINE = "a definition's body starts on the line after its header; written";
pub const R_ENDWORD = "one spelling: `end`; written";

const Open = struct { def: bool, row: u32, head_end: u32, name: []const u8, braced: bool = false };

fn wordByte(b: u8) bool {
    return std.ascii.isAlphanumeric(b) or b == '_';
}

const Braced = struct { text: []const u8, inserts: []const Insert };

/// A .haro file read once, its definitions already in braces (v0.56): the load path's parse, so a file is never parsed twice
pub fn parseHaro(alloc: std.mem.Allocator, parser: ts.Parser, src: []const u8, name: []const u8) ?Lifted {
    if (bracesText(alloc, src, name)) |b| {
        const tree = parser.parse(b.text) orelse return null;
        def_files += 1;
        return .{ .tree = tree, .src = b.text, .inserts = b.inserts };
    }
    return .{ .tree = parser.parse(src) orelse return null, .src = src };
}

fn defBraces(alloc: std.mem.Allocator, parser: ts.Parser, src: []const u8, name: []const u8) ?Lifted {
    const b = bracesText(alloc, src, name) orelse return null;
    const tree = parser.parse(b.text) orelse return null;
    def_files += 1;
    return .{ .tree = tree, .src = b.text, .inserts = b.inserts };
}

fn bracesText(alloc: std.mem.Allocator, src: []const u8, name: []const u8) ?Braced {
    var stack = std.ArrayListUnmanaged(Open){};
    defer stack.deinit(alloc);
    var ends = std.ArrayListUnmanaged(u32){};
    defer ends.deinit(alloc);
    var heads = std.ArrayListUnmanaged(u32){};
    defer heads.deinit(alloc);
    var fault: ?Fault = null;
    const n = src.len;
    var i: usize = 0;
    var row: u32 = 0;
    var prev: u8 = '\n'; // the last byte of code before this one, blanks left out
    scan: while (i < n) {
        const ch = src[i];
        if (ch == '\n') {
            row += 1;
            prev = '\n';
            i += 1;
            continue;
        }
        if (ch == ' ' or ch == '\t' or ch == '\r') {
            i += 1;
            continue;
        }
        if (ch == '"' or ch == '\'' or ch == '`') {
            const close = std.mem.indexOfScalarPos(u8, src, i + 1, ch) orelse break :scan;
            for (src[i..close]) |b| {
                if (b == '\n') row += 1;
            }
            i = close + 1;
            prev = ch;
            continue;
        }
        if (ch == '#' or (ch == '/' and i + 1 < n and src[i + 1] == '/')) {
            while (i < n and src[i] != '\n') i += 1;
            continue;
        }
        if (ch == '/' and i + 1 < n and src[i + 1] == '*') {
            const close = std.mem.indexOfPos(u8, src, i + 2, "*/") orelse break :scan;
            for (src[i .. close + 2]) |b| {
                if (b == '\n') row += 1;
            }
            i = close + 2;
            continue;
        }
        if (!wordByte(ch) and ch != '$' and ch != '@') {
            // a block opened with a brace on its own line is closed by a brace (the compiler refuses both, naming `end`)
            if (ch == '{') {
                if (stack.items.len > 0 and !stack.items[stack.items.len - 1].def and stack.items[stack.items.len - 1].row == row)
                    stack.items[stack.items.len - 1].braced = true;
            } else if (ch == '}') {
                if (stack.items.len > 0 and stack.items[stack.items.len - 1].braced) _ = stack.pop();
            }
            prev = ch;
            i += 1;
            continue;
        }
        const s = i;
        if (ch == '$' or ch == '@') i += 1;
        while (i < n and wordByte(src[i])) i += 1;
        const w = src[s..i];
        const named = !(prev == '.' or prev == ':' or ch == '$' or ch == '@' or std.ascii.isDigit(ch));
        prev = 'a';
        if (!named) continue;
        const def = eq(w, "func") or eq(w, "def") or eq(w, "class") or eq(w, "package");
        if (def) {
            // the header's code ends before the line's comment or its end
            var j = i;
            var last: usize = i;
            while (j < n and src[j] != '\n') : (j += 1) {
                const b = src[j];
                if (b == '#' or (b == '/' and j + 1 < n and src[j + 1] == '/')) break;
                if (b == '"' or b == '\'' or b == '`') {
                    const close = std.mem.indexOfScalarPos(u8, src, j + 1, b) orelse break;
                    j = close;
                    last = close + 1;
                    continue;
                }
                if (b != ' ' and b != '\t' and b != '\r') last = j + 1;
            }
            // its name: the word after it
            var k = i;
            while (k < n and (src[k] == ' ' or src[k] == '\t')) k += 1;
            var e = k;
            while (e < n and wordByte(src[e])) e += 1;
            try_push(alloc, &stack, .{ .def = true, .row = row, .head_end = @intCast(last), .name = if (e > k) src[k..e] else w }) orelse return null;
            continue;
        }
        if (eq(w, "if") or eq(w, "while") or eq(w, "for") or eq(w, "foreach") or eq(w, "switch") or eq(w, "try") or eq(w, "do")) {
            try_push(alloc, &stack, .{ .def = false, .row = row, .head_end = 0, .name = w }) orelse return null;
            continue;
        }
        if (eq(w, "within") or eq(w, "using")) {
            // a block when a header follows on its line: a name, then `=`
            var k = i;
            while (k < n and (src[k] == ' ' or src[k] == '\t')) k += 1;
            var e = k;
            if (e < n and (src[e] == '$' or src[e] == '@')) e += 1;
            while (e < n and wordByte(src[e])) e += 1;
            var q = e;
            while (q < n and (src[q] == ' ' or src[q] == '\t')) q += 1;
            if (e > k and q < n and src[q] == '=' and !(q + 1 < n and src[q + 1] == '='))
                try_push(alloc, &stack, .{ .def = false, .row = row, .head_end = 0, .name = w }) orelse return null;
            continue;
        }
        if (eq(w, "endfunc") or eq(w, "endfunction") or eq(w, "endclass") or eq(w, "endpackage")) {
            if (fault == null) fault = .{ .why = R_ENDWORD, .word = w, .row = row };
            break :scan;
        }
        if (eq(w, "again")) {
            _ = stack.pop();
            continue;
        }
        // a block's end word in another spelling closes the block (the compiler refuses it, naming `end`, v0.55)
        if (eq(w, "ok") or eq(w, "next") or eq(w, "off") or eq(w, "done") or eq(w, "endif") or eq(w, "endwhile") or eq(w, "endfor") or
            eq(w, "endswitch") or eq(w, "endtry"))
        {
            if (stack.items.len > 0 and !stack.items[stack.items.len - 1].def) _ = stack.pop();
            continue;
        }
        if (eq(w, "end")) {
            const o = stack.pop() orelse {
                if (fault == null) fault = .{ .why = R_STRAY, .word = w, .row = row };
                break :scan;
            };
            if (o.def) {
                if (o.row == row) {
                    if (fault == null) fault = .{ .why = R_ONELINE, .word = o.name, .row = row };
                    break :scan;
                }
                ends.append(alloc, @intCast(s)) catch return null;
                heads.append(alloc, o.head_end) catch return null;
            }
            continue;
        }
    }
    if (fault == null) {
        for (stack.items) |o| {
            if (!o.def) continue;
            fault = .{ .why = R_NOEND, .word = o.name, .row = o.row };
            break;
        }
    }
    // the table lives as long as the program, never in an eval's scratch (which is reset between evals), and an eval keeps none:
    // the compiler reads it for a file only
    const keep = !eq(name, "eval");
    if (fault) |f| {
        if (keep) faults.put(std.heap.page_allocator, name, f) catch {};
        return null;
    }
    if (keep) _ = faults.remove(name);
    if (heads.items.len == 0) return null;
    // the text: ` {` after each header, `}` for each definition's `end` -- the inserts in file order
    std.mem.sort(u32, heads.items, {}, std.sort.asc(u32));
    const text = alloc.alloc(u8, n + 2 * heads.items.len) catch return null;
    const ins = alloc.alloc(Insert, heads.items.len) catch return null;
    var at: usize = 0;
    var from: usize = 0;
    for (heads.items, 0..) |h, hi| {
        @memcpy(text[at .. at + (h - from)], src[from..h]);
        at += h - from;
        text[at] = ' ';
        text[at + 1] = '{';
        at += 2;
        from = h;
        ins[hi] = .{ .pos = h, .len = 2 };
    }
    @memcpy(text[at..], src[from..]);
    for (ends.items) |e| {
        var shift: usize = 0;
        for (heads.items) |h| {
            if (h <= e) shift += 2;
        }
        const p = e + shift;
        text[p] = '}';
        text[p + 1] = ' ';
        text[p + 2] = ' ';
    }
    return .{ .text = text, .inserts = ins };
}

fn try_push(alloc: std.mem.Allocator, stack: *std.ArrayListUnmanaged(Open), o: Open) ?void {
    stack.append(alloc, o) catch return null;
}

/// the .haro files whose definitions were given to the parser in braces, for the census
pub var def_files: u32 = 0;

/// The blocks pass alone, for `haro fmt`, which prints the blocks back as they were written (fmt.zig, `sTry`).
pub fn blocks(alloc: std.mem.Allocator, parser: ts.Parser, tree: ts.Tree, src: []const u8, prior: []const Insert) Lifted {
    if (std.ascii.indexOfIgnoreCase(src, "within") == null and std.ascii.indexOfIgnoreCase(src, "using") == null)
        return .{ .tree = tree, .src = src, .inserts = prior };
    var edits = std.ArrayListUnmanaged(Edit){};
    defer edits.deinit(alloc);
    findBlocks(alloc, tree.root(), &edits) catch return .{ .tree = tree, .src = src, .inserts = prior };
    if (edits.items.len == 0) return .{ .tree = tree, .src = src, .inserts = prior };
    const r = splice(alloc, parser, tree, src, edits.items, prior) orelse return .{ .tree = tree, .src = src, .inserts = prior };
    tree.deinit();
    block_sites += @intCast(edits.items.len / 2);
    return r;
}

/// The text with each edit's parenthesis put in, parsed again. Null when it does not parse, or when a file that parsed no longer does:
/// a rewrite that breaks a file is no fix, so the grammar's reading is kept and nothing worse than before is said.
fn splice(alloc: std.mem.Allocator, parser: ts.Parser, tree: ts.Tree, src: []const u8, edits: []Edit, prior: []const Insert) ?Lifted {
    std.mem.sort(Edit, edits, {}, order);
    var extra: usize = 0;
    for (edits) |e| extra += piece(e).len;
    const text = alloc.alloc(u8, src.len + extra) catch return null;
    var w: usize = 0;
    var r: usize = 0;
    for (edits) |e| {
        const n = e.pos - r;
        @memcpy(text[w .. w + n], src[r .. r + n]);
        w += n;
        r += n;
        const pc = piece(e);
        @memcpy(text[w .. w + pc.len], pc);
        w += pc.len;
    }
    @memcpy(text[w .. w + (src.len - r)], src[r..]);
    var tr = std.time.Timer.start() catch return null;
    const again = parser.parse(text) orelse return null;
    ns_reparse += tr.read();
    if (again.root().hasError() and !tree.root().hasError()) {
        again.deinit();
        return null;
    }
    const ins = compose(alloc, prior, edits) orelse {
        again.deinit();
        return null;
    };
    return .{ .tree = again, .src = text, .inserts = ins };
}

pub fn apply(alloc: std.mem.Allocator, parser: ts.Parser, tree_in: ts.Tree, src_in: []const u8, name: []const u8, prior: []const Insert, braced: bool) Lifted {
    file_name = name;
    var t0 = std.time.Timer.start() catch return .{ .tree = tree_in, .src = src_in };
    defer ns += t0.read();
    // v0.56 (D68): a .haro file's definitions, matched to their `end` by the tokens, are given to the parser in braces
    var tree0 = tree_in;
    var src0 = src_in;
    var pre: []const Insert = prior;
    if (!braced and (isHaro(name) or (std.mem.eql(u8, name, "eval") and haro_root))) {
        if (defBraces(alloc, parser, src_in, name)) |r| {
            tree0.deinit();
            tree0 = r.tree;
            src0 = r.src;
            pre = r.inserts;
        }
    }
    const bl = blocks(alloc, parser, tree0, src0, pre);
    var tree = bl.tree;
    var src = bl.src;
    var ins = bl.inserts;
    if (std.ascii.indexOfIgnoreCase(src, "catch") != null) {
        var edits = std.ArrayListUnmanaged(Edit){};
        defer edits.deinit(alloc);
        findCatch(alloc, tree.root(), &edits) catch {};
        if (edits.items.len > 0) {
            if (splice(alloc, parser, tree, src, edits.items, ins)) |r| {
                tree.deinit();
                tree = r.tree;
                src = r.src;
                ins = r.inserts;
                catch_sites += @intCast(edits.items.len / 2);
            }
        }
    }
    // `not` and `!` are the only words that matter, and most files hold neither
    if (std.ascii.indexOfIgnoreCase(src, "not") == null and std.mem.indexOfScalar(u8, src, '!') == null)
        return .{ .tree = tree, .src = src, .inserts = ins };

    var lifted_here: u32 = 0;
    // a `not not` chain gains one level of parentheses a pass; Ring refuses that shape (C28), so the bound only has to be finite
    var pass: u32 = 0;
    while (pass < 4) : (pass += 1) {
        var edits = std.ArrayListUnmanaged(Edit){};
        defer edits.deinit(alloc);
        findSites(alloc, tree.root(), &edits) catch break;
        if (edits.items.len == 0) break;
        const r = splice(alloc, parser, tree, src, edits.items, ins) orelse break;
        tree.deinit();
        tree = r.tree;
        src = r.src;
        ins = r.inserts;
        lifted_here += @intCast(edits.items.len / 2);
    }
    if (lifted_here > 0) {
        sites += lifted_here;
        files += 1;
    }
    return .{ .tree = tree, .src = src, .inserts = ins };
}
