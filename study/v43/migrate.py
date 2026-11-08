"""v0.43's migration of Haro's own code (D55 T1: no coercion). Rewrites ONLY the lines named on the command line (file:line), or the
census rows (study/v43/census_lines.txt) when none is named.

  "" + x            ->  string(x)          a number written as text
  0 + x             ->  number(x)          a text read as a number
  "text" + x + ...  ->  "text" + string(x) for each operand of a `+` chain holding a text literal that reads as a number: a name whose
                        letter is n, i, j or k, a global not lettered c or t, len(), clock(), random(), a subscript, a member call, or
                        arithmetic in brackets. string() of a text is that text, so a wrapped operand that was text changes nothing

Prints each change; --dry prints without writing.
  python study/v43/migrate.py [--dry] [file:line ...]
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEXT_CALLS = {"ringstr", "ctjson", "upper", "lower", "ctjoin", "stzujoin", "narfill", "patprintkept", "typekindof", "ctstripprefix",
              "string", "substr", "left", "right", "trim", "char", "lines", "copy", "code", "message"}


def tokens(s):
    """(kind, text) tokens of one line: str, num, name, op, open, close, ws, comment"""
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c in "\"'`":
            j = s.find(c, i + 1)
            j = n - 1 if j < 0 else j
            out.append(("str", s[i:j + 1])); i = j + 1
        elif c == "#" or s.startswith("//", i):
            out.append(("comment", s[i:])); break
        elif c.isspace():
            j = i
            while j < n and s[j].isspace(): j += 1
            out.append(("ws", s[i:j])); i = j
        elif c.isdigit():
            j = i
            while j < n and (s[j].isalnum() or s[j] in "._"): j += 1
            out.append(("num", s[i:j])); i = j
        elif c.isalpha() or c in "_$@":
            j = i + 1
            while j < n and (s[j].isalnum() or s[j] == "_"): j += 1
            out.append(("name", s[i:j])); i = j
        elif c in "([{":
            out.append(("open", c)); i += 1
        elif c in ")]}":
            out.append(("close", c)); i += 1
        else:
            j = i + 1
            if s[i:i + 2] in ("+=", "-=", "++", "--", "<=", ">=", "!=", "==", "&&", "||"): j = i + 2
            out.append(("op", s[i:j])); i = j
    return out


def unit_end(t, i):
    """index past the operand unit starting at token i: an atom with its postfixes (call, subscript, member)"""
    n = len(t)
    if i >= n: return i
    k = t[i][0]
    if k == "open":
        i = match(t, i) + 1
    elif k in ("name", "num", "str"):
        i += 1
    else:
        return i
    while i < n:
        if t[i][0] == "open" and t[i][1] in "([":
            i = match(t, i) + 1
        elif t[i][0] == "op" and t[i][1] == "." and i + 1 < n and t[i + 1][0] == "name":
            i += 2
        else:
            break
    return i


def match(t, i):
    d = 0
    for j in range(i, len(t)):
        if t[j][0] == "open": d += 1
        elif t[j][0] == "close":
            d -= 1
            if d == 0: return j
    return len(t) - 1


def unit_start(t, end):
    """index of the operand unit ending just before `end` (exclusive), walking back over postfixes"""
    i = end - 1
    while i >= 0 and t[i][0] == "ws": i -= 1
    if i < 0: return None
    while True:
        if t[i][0] == "close":
            d = 0
            for j in range(i, -1, -1):
                if t[j][0] == "close": d += 1
                elif t[j][0] == "open":
                    d -= 1
                    if d == 0: break
            i = j
            if i > 0 and t[i][1] in "([" and t[i - 1][0] in ("name", "close"):
                i -= 1
                continue
            return i
        if t[i][0] in ("name", "num", "str"):
            if i >= 2 and t[i - 1] == ("op", "."):
                i -= 2
                continue
            return i
        return None


def numeric(text):
    s = text.strip()
    if not s or s[0] in "\"'`": return False
    if s.startswith("("): return not any(q in s for q in "\"'`")
    if s[0].isdigit(): return True
    head = s.split("(")[0].split("[")[0].split(".")[0]
    low = head.lower()
    if "(" in s and not s.startswith("("):
        callee = s.split("(")[0].split(".")[-1].lower()
        if callee in TEXT_CALLS: return False
        if callee in ("len", "clock", "random", "span"): return True
        if "." in s.split("(")[0]: return True  # a member call: e.Span()[:line]
        return "[" in s.split(")", 1)[-1]
    if "[" in s: return True
    name = head.lstrip("$@")
    if not name: return False
    if len(name) == 1: return name in "nijk" or head.startswith("$")
    if name[0] in "nijk" and (name[1].isupper() or name[1].isdigit()): return True
    if head.startswith("$") and name[0] not in "ct": return True
    return False


def rewrite(line):
    t = tokens(line)
    changed = True
    while changed:
        changed = False
        for i, (k, v) in enumerate(t):
            if k != "op" or v != "+": continue
            ls = unit_start(t, i)
            rs = i + 1
            while rs < len(t) and t[rs][0] == "ws": rs += 1
            re_ = unit_end(t, rs)
            if ls is None or re_ == rs: continue
            left = "".join(x[1] for x in t[ls:i]).strip()
            right = "".join(x[1] for x in t[rs:re_])
            before = t[ls - 1] if ls > 0 else None
            prev_plus = False
            j = ls - 1
            while j >= 0 and t[j][0] == "ws": j -= 1
            if j >= 0 and t[j] == ("op", "+"): prev_plus = True
            if t[rs][0] == "open" and match(t, rs) == re_ - 1:
                right = right.strip()[1:-1].strip()
            if left in ('""', "''") and not prev_plus:
                t[ls:re_] = [("name", "string(" + right + ")")]
                changed = True; break
            if left == "0" and not prev_plus:
                t[ls:re_] = [("name", "number(" + right + ")")]
                changed = True; break
    # wrap the numeric operands of each + chain holding a text literal
    out = []
    i = 0
    text_chain = any(k == "str" for k, _ in t) and any(x == ("op", "+") for x in t)
    if not text_chain: return "".join(v for _, v in t)
    plus_adj = set()
    for i, x in enumerate(t):
        if x == ("op", "+"):
            ls = unit_start(t, i)
            rs = i + 1
            while rs < len(t) and t[rs][0] == "ws": rs += 1
            re_ = unit_end(t, rs)
            if ls is not None: plus_adj.add((ls, i))
            if re_ > rs: plus_adj.add((rs, re_))
    spans = sorted(s for s in plus_adj if numeric("".join(v for _, v in t[s[0]:s[1]])) and not "".join(v for _, v in t[s[0]:s[1]]).startswith(("string(", "number(")))
    res, pos = [], 0
    for a, b in spans:
        if a < pos: continue
        res.append("".join(v for _, v in t[pos:a]))
        body = "".join(v for _, v in t[a:b]).strip()
        if t[a][0] == "open" and match(t, a) == b - 1:
            body = body[1:-1].strip()
        res.append("string(" + body + ")")
        trail = "".join(v for _, v in t[a:b])
        res.append(trail[len(trail.rstrip()):])
        pos = b
    res.append("".join(v for _, v in t[pos:]))
    return "".join(res)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    targets = []
    if args:
        for a in args:
            f, l = a.rsplit(":", 1)
            targets.append((os.path.join(ROOT, f), int(l)))
    else:
        index = {}
        for f in glob.glob(os.path.join(ROOT, "spike", "**", "*.haro"), recursive=True):
            index.setdefault(os.path.basename(f), []).append(f)
        for row in open(os.path.join(ROOT, "study", "v43", "census_lines.txt"), encoding="utf-8"):
            name, l = row.rstrip("\n").split("\t")
            for f in index.get(name, []):
                if os.sep + "v43" + os.sep in f: continue
                targets.append((f, int(l)))
    byfile = {}
    for f, l in targets: byfile.setdefault(f, set()).add(l)
    n = 0
    for f, ls in sorted(byfile.items()):
        raw = open(f, "rb").read().decode("utf-8")
        lines = raw.split("\n")
        for l in sorted(ls):
            if l > len(lines) or "+" not in lines[l - 1]: continue
            new = rewrite(lines[l - 1])
            if new != lines[l - 1]:
                n += 1
                print(f"{os.path.relpath(f, ROOT)}:{l}\n  - {lines[l-1].strip()[:200]}\n  + {new.strip()[:200]}")
                lines[l - 1] = new
        if not dry:
            open(f, "wb").write("\n".join(lines).encode("utf-8"))
    print(f"{n} line(s) changed")


if __name__ == "__main__":
    main()
