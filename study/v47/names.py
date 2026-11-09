"""v0.47: every declared name of the repository's .haro code that the letter rule refuses or that needs a reading (the t-names), with
its files. Lexical (study/v47/letters.py's reading): assigned names, parameters, for counters; strings and comments blanked.

  python study/v47/names.py [shape]      shape: c, t, single, word, other, badletter (default: all but c)
"""
import glob, os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LETTERS = set("bidfntxkvmroehswa")


def code_files():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "*.haro"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        if rel.startswith(("runtime/", "vm/")) or "/scratch/" in rel:
            continue
        head = open(f, encoding="utf-8", errors="replace").read(4000).lstrip()
        if head.upper().startswith("DEFINE"):
            continue
        out.append(rel)
    return out


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


def shape(name, counter=False):
    core = name.lstrip("$@")
    if len(core) == 1 and core.islower(): return "ok" if counter else "single"
    if len(core) >= 2 and core[0].islower() and core[1].isupper():
        if core[0] == "c": return "c"
        if core[0] == "t": return "t"
        return "ok" if core[0] in LETTERS else "badletter"
    if core == core.lower() and core.replace("_", "").isalnum(): return "word"
    return "other"


def declared(t):
    """(name, is_counter) for each declaration in bare text t"""
    for m in re.finditer(r"(?m)^\s*([$@]?[A-Za-z_]\w*)\s*(=|\+=|-=|\*=|/=)(?!=)", t):
        yield m.group(1), False
    for m in re.finditer(r"(?m)^\s*(?:This|this|self)\.([A-Za-z_]\w*)\s*(=|\+=|-=|\*=|/=)(?!=)", t):
        yield m.group(1), False
    for m in re.finditer(r"(?mi)^\s*(?:func|def)\s+\w+\s*\(?([^)\n]*)\)?", t):
        for p in m.group(1).split(","):
            p = p.strip()
            if re.match(r"^[A-Za-z_]\w*$", p): yield p, False
    for m in re.finditer(r"(?mi)^\s*for\s+([A-Za-z_]\w*)\s*(=|in\b)", t):
        yield m.group(1), True


if __name__ == "__main__":
    want = sys.argv[1] if len(sys.argv) > 1 else None
    where = collections.defaultdict(set)
    for rel in code_files():
        t = bare(open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read())
        for name, ctr in declared(t):
            s = shape(name, ctr)
            if s == "ok" or (want is None and s == "c") or (want and s != want):
                continue
            where[(s, name)].add(rel)
    for (s, name), fs in sorted(where.items()):
        fl = sorted(fs)
        print(f"{s:9s} {name:22s} {len(fl):3d}  {', '.join(fl[:4])}{' ...' if len(fl) > 4 else ''}")
