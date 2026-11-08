"""v0.47's measurement: the names Haro's own code declares (locals and globals by assignment, parameters, attributes), by their shape.
Lexical, over spike/*.haro code files (never a declaration, never a rung's case); strings and comments excluded.

  lettered   a lowercase letter then a capital (cName, aList, nCount, $bFlag, @nX): counted by its letter
  single     one lowercase letter (i, j, k, n, x)
  word       a lowercase word with no capital (out, within, result)
  other      anything else (CamelCase, a digit after the letter)
"""
import glob, os, re, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def bare(text):
    out, i, n, q = [], 0, len(text), None
    while i < n:
        c = text[i]
        if q:
            if c == q: q = None
            out.append(" " if c != "\n" else "\n"); i += 1; continue
        if c in "\"'`": q = c; out.append(" "); i += 1; continue
        if c == "#" or text.startswith("//", i):
            j = text.find("\n", i); j = n if j < 0 else j
            out.append(" " * (j - i)); i = j; continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2); j = n if j < 0 else j + 2
            out.append("".join("\n" if ch == "\n" else " " for ch in text[i:j])); i = j; continue
        out.append(c); i += 1
    return "".join(out)


def shape(name):
    core = name.lstrip("$@")
    if len(core) == 1 and core.islower(): return "single"
    if len(core) >= 2 and core[0].islower() and core[1].isupper(): return "lettered:" + core[0]
    if core.islower() or (core.replace("_", "").isalnum() and core == core.lower()): return "word"
    return "other"


decl = collections.Counter()
names_by = collections.defaultdict(set)
files = 0
for f in sorted(glob.glob(os.path.join(ROOT, "spike", "*.haro"))):
    raw = open(f, encoding="utf-8", errors="replace").read()
    if raw.lstrip().upper().startswith("DEFINE"):
        continue
    files += 1
    t = bare(raw)
    seen = set()
    for m in re.finditer(r"(?m)^\s*([$@]?[A-Za-z_]\w*)\s*(=|\+=|-=|\*=|/=)(?!=)", t):
        seen.add(m.group(1))
    for m in re.finditer(r"(?mi)^\s*(?:func|def)\s+\w+\s*\(?([^)\n]*)\)?", t):
        for p in m.group(1).split(","):
            p = p.strip()
            if re.match(r"^[A-Za-z_]\w*$", p): seen.add(p)
    for m in re.finditer(r"(?mi)^\s*for\s+([A-Za-z_]\w*)\s*(=|in\b)", t):
        seen.add(m.group(1))
    for n in seen:
        s = shape(n)
        decl[s] += 1
        names_by[s].add(n.lstrip("$@"))
print(f"{files} code files; {sum(decl.values())} declared names (a name counted once per file)")
for s, c in sorted(decl.items(), key=lambda kv: -kv[1]):
    ex = sorted(names_by[s])[:8]
    print(f"  {c:5d}  {s:12s}  e.g. {', '.join(ex)}")
