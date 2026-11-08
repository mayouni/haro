"""v0.43's second migration of Haro's own code (D55 T3: only a boolean decides). Lexical, by rule, over spike/*.haro (code files only, never a
declaration, never a case program of a rung). Prints every change; --dry writes nothing.

  R1  a b-lettered name ASSIGNED 1 or 0 is assigned true or false             bAll = 0            ->  bAll = false
  R2  a b-lettered name COMPARED with 1 or 0 is the name, or its `not`         if bAll = 1         ->  if bAll
                                                                               if bAll = 0         ->  if not bAll
  R3  a function whose every return is 1, 0, true, false, a comparison or a   return 1            ->  return true
      logic expression returns true and false (a predicate)                   return 0            ->  return false

A name is compared when the token before it opens a condition or an operand (if, elseif, but, while, and, or, not, return, `(`, `,`, `[`, `=`
of another comparison); otherwise it is assigned (the start of a statement).

  python study/v43/migrate_bool.py [--dry] [files...]
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BNAME = r"[$@]?b[A-Z0-9]\w*"
COND_BEFORE = {"if", "elseif", "but", "while", "and", "or", "not", "return", "(", ",", "[", "=", "!", "&&", "||"}


def strip_strings(line):
    """the line with every string literal's inside blanked, same length, so a regex never matches inside one"""
    out, i, q = [], 0, None
    for ch in line:
        if q:
            out.append(ch if ch == q else " ")
            if ch == q: q = None
        elif ch in "\"'`":
            q = ch; out.append(ch)
        elif ch == "#":
            out.append(ch); out.extend(" " * (len(line) - len(out))); break
        else:
            out.append(ch)
    return "".join(out)[:len(line)]


def prev_token(s, at):
    j = at - 1
    while j >= 0 and s[j] in " \t": j -= 1
    if j < 0: return ""
    if s[j].isalnum() or s[j] == "_":
        k = j
        while k >= 0 and (s[k].isalnum() or s[k] == "_"): k -= 1
        return s[k + 1:j + 1].lower()
    return s[j]


def r1_r2(line):
    bare = strip_strings(line)
    edits = []
    for m in re.finditer(r"(?<![\w$@])(" + BNAME + r")(\s*)(!=|=)(\s*)([01])(?![\w.])", bare):
        name, op, val = m.group(1), m.group(3), m.group(5)
        before = prev_token(bare, m.start())
        compared = before in COND_BEFORE or op == "!="
        if compared:
            truthy = (op == "=" and val == "1") or (op == "!=" and val == "0")
            new = name if truthy else "not " + name
        else:
            if op != "=": continue
            new = f"{name}{m.group(2)}={m.group(4)}{'true' if val == '1' else 'false'}"
        edits.append((m.start(), m.end(), new))
    for a, b, new in reversed(edits):
        line = line[:a] + new + line[b:]
    return line


FUNC = re.compile(r"^\s*(func|def)\s+(\w+)", re.I)
CLASS = re.compile(r"^\s*class\s+\w+", re.I)
RET = re.compile(r"(?<![\w$@])return\b(.*?)(?=\bok\b|$)", re.I)


def is_boolish(expr):
    e = expr.strip()
    if e in ("0", "1", "true", "false"): return True
    bare = strip_strings(e)
    if re.search(r"(?<![<>!=])(=|!=|<=|>=|<|>)(?!=)", bare): return True
    if re.match(r"^not\b", bare) or re.search(r"\b(and|or)\b", bare): return True
    if re.match(r"^(isnull|isstring|isnumber|islist|isobject|ispointer|isdigit|isalpha|isspace|isupper|islower|fexists|direxists)\(", bare): return True
    if re.match(r"^" + BNAME + r"$", bare): return True
    return False


PREDICATES = set()   # lowercased names of functions found to be predicates, across every file (R3's fixed point)
BPARAMS = {}         # lowercased function name -> the positions of its b-lettered parameters (R4)


def spans_of(lines):
    spans, cur = [], None
    for i, l in enumerate(lines):
        if FUNC.match(l) or CLASS.match(l):
            if cur: spans.append(cur)
            cur = [i, i, FUNC.match(l).group(2).lower()] if FUNC.match(l) else None
        elif cur:
            cur[1] = i
    if cur: spans.append(cur)
    return spans


def returns_of(lines, a, b):
    rets = []
    for i in range(a + 1, b + 1):
        bare = strip_strings(lines[i])
        for m in RET.finditer(bare):
            rets.append((i, m.start(1), m.end(1), lines[i][m.start(1):m.end(1)]))
    return rets


def boolish2(expr):
    if is_boolish(expr): return True
    bare = strip_strings(expr.strip())
    m = re.match(r"^(not\s+)?(\w+)\s*\(", bare)
    if m and m.group(2).lower() in PREDICATES:
        depth = 0
        for k, ch in enumerate(bare):
            if ch == "(": depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0: return bare[k + 1:].strip() == ""
    return False


def learn(all_lines):
    """R3's fixed point over every file, and R4's parameter positions"""
    for lines in all_lines:
        for l in lines:
            m = re.match(r"^\s*(func|def)\s+(\w+)\s*(.*)$", l, re.I)
            if m:
                params = [p.strip() for p in strip_strings(m.group(3)).split(",") if p.strip()]
                pos = [k for k, p in enumerate(params) if re.match(r"^b[A-Z0-9]", p)]
                if pos: BPARAMS[m.group(2).lower()] = pos
    # the greatest fixed point: every function with a literal 1 or 0 return is a candidate, and one is dropped while any of its returns is
    # neither boolean-shaped nor a call of a candidate -- so a predicate that calls itself (PatNullable) stays one
    funcs = []
    for lines in all_lines:
        for a, b, name in spans_of(lines):
            rets = returns_of(lines, a, b)
            if rets:
                funcs.append((name, rets))
                PREDICATES.add(name)
    shrank = True
    while shrank:
        shrank = False
        for name, rets in funcs:
            if name in PREDICATES and not all(boolish2(r[3]) for r in rets):
                PREDICATES.discard(name); shrank = True


def r4(line):
    """a literal 1 or 0 passed where the callee's parameter is b-lettered"""
    bare = strip_strings(line)
    edits = []
    for m in re.finditer(r"(?<![\w$@.])(\w+)\s*\(", bare):
        pos = BPARAMS.get(m.group(1).lower())
        if not pos: continue
        k, depth, arg, starts = m.end(), 1, 0, [m.end()]
        ends = []
        while k < len(bare) and depth > 0:
            ch = bare[k]
            if ch in "([": depth += 1
            elif ch in ")]":
                depth -= 1
                if depth == 0: ends.append(k)
            elif ch == "," and depth == 1:
                ends.append(k); starts.append(k + 1)
            k += 1
        for p in pos:
            if p < len(ends):
                s, e = starts[p], ends[p]
                v = line[s:e].strip()
                if v in ("0", "1"):
                    lead = len(line[s:e]) - len(line[s:e].lstrip())
                    trail = len(line[s:e]) - len(line[s:e].rstrip())
                    edits.append((s + lead, e - trail, "true" if v == "1" else "false"))
    for a, b, new in sorted(edits, reverse=True):
        line = line[:a] + new + line[b:]
    return line


def r5(lines):
    """R5: a function whose every returned list starts with a literal 1 or 0 (a success flag, `[1, value]` / `[0, 0]`) returns
    true or false in that first place. A function that returns any other list ([node, pos] with 0 for no node) is left alone."""
    out = {}
    for a, b, name in spans_of(lines):
        rets = returns_of(lines, a, b)
        lists = [r for r in rets if r[3].strip().startswith("[")]
        if len(lists) < 2: continue
        heads = [re.match(r"^\[\s*([^,\]]*)\s*,", r[3].strip()) for r in lists]
        if not all(h and h.group(1).strip() in ("0", "1", "true", "false") for h in heads): continue
        if not any(h.group(1).strip() in ("0", "1") for h in heads): continue
        # a return that is no list literal passes another result through (`return aR`): it does not decide the shape
        for r, h in zip(lists, heads):
            i, s, e, expr = r
            line = out.get(i, lines[i])
            seg = line[s:e]
            v = h.group(1).strip()
            if v in ("0", "1"):
                seg2 = re.sub(r"^(\s*\[\s*)" + v, lambda m: m.group(1) + ("true" if v == "1" else "false"), seg, count=1)
                out[i] = line[:s] + seg2 + line[e:]
    return out


def r3(lines):
    """indices of `return 1` / `return 0` lines inside predicates, with the new text"""
    out = {}
    for a, b, name in spans_of(lines):
        if name not in PREDICATES: continue
        rets = returns_of(lines, a, b)
        for i, s, e, expr in rets:
            v = expr.strip()
            if v in ("0", "1"):
                line = out.get(i, lines[i])
                seg = line[s:e]
                new = seg.replace(v, "true" if v == "1" else "false", 1)
                out[i] = line[:s] + new + line[e:]
    return out


def main():
    dry = "--dry" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("--")] or sorted(glob.glob(os.path.join(ROOT, "spike", "*.haro")))
    total = 0
    code = []
    for f in files:
        raw = open(f, "rb").read().decode("utf-8")
        if not raw.lstrip().upper().startswith("DEFINE"): code.append((f, raw.split("\n")))
    learn([ls for _, ls in code])
    for f, lines in code:
        changed = 0
        for i, l in enumerate(lines):
            n = r4(r1_r2(l))
            if n != l:
                print(f"{os.path.relpath(f, ROOT)}:{i+1}\n  - {l.strip()[:160]}\n  + {n.strip()[:160]}")
                lines[i] = n; changed += 1
        for i, n in r5(lines).items():
            if n != lines[i]:
                print(f"{os.path.relpath(f, ROOT)}:{i+1}\n  - {lines[i].strip()[:160]}\n  + {n.strip()[:160]}")
                lines[i] = n; changed += 1
        for i, n in r3(lines).items():
            if n != lines[i]:
                print(f"{os.path.relpath(f, ROOT)}:{i+1}\n  - {lines[i].strip()[:160]}\n  + {n.strip()[:160]}")
                lines[i] = n; changed += 1
        total += changed
        if changed and not dry:
            open(f, "wb").write("\n".join(lines).encode("utf-8"))
    print(f"{total} line(s) changed")


if __name__ == "__main__":
    main()
