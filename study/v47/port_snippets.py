"""v0.47: the .haro code the guard's Python checks carry -- a mutation's `old` text, a probe's expected line -- re-lettered as the files they
name were. A string literal of a .py file that stands verbatim in a renamed .haro file as it was at HEAD is replaced by the same span of
the renamed file: study/v47/reletter.py renames token for token, so the two files' tokens align one to one. A literal that stands in no
file (a mutation's `new` side) but holds a Softanza name gets the uniform rules alone (R1 c -> t, R5 v -> x) and is printed, to be read.

  python study/v47/port_snippets.py            report
  python study/v47/port_snippets.py --apply    rewrite the .py files
"""
import ast, glob, io, os, re, subprocess, sys, tokenize as pytok
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import reletter as R  # noqa: E402

APPLY = "--apply" in sys.argv


def head_text(rel):
    r = subprocess.run(["git", "show", "HEAD:" + rel], cwd=ROOT, capture_output=True)
    return r.stdout.decode("utf-8").replace("\r\n", "\n") if r.returncode == 0 else None


# the renamed code files: HEAD text, current text, and the aligned token offsets
FILES = []
for rel in R.code_files():
    if "/cases/" in rel:
        continue
    old = head_text(rel)
    if old is None:
        continue
    new = open(os.path.join(ROOT, rel), encoding="utf-8").read().replace("\r\n", "\n")
    if old == new:
        continue
    to, tn = R.tokens(old), R.tokens(new)
    if len(to) != len(tn):
        print(f"SKIP {rel}: token counts differ ({len(to)} vs {len(tn)})")
        continue
    so, sn, po, pn = [], [], 0, 0
    for (ka, va), (kb, vb) in zip(to, tn):
        so.append(po); sn.append(pn); po += len(va); pn += len(vb)
    so.append(po); sn.append(pn)
    FILES.append((rel, old, new, so, sn))


def renamed(snippet):
    """the snippet's span in the renamed file, when it stands once in one HEAD file on token boundaries"""
    hits = []
    for rel, old, new, so, sn in FILES:
        at = old.find(snippet)
        if at < 0:
            continue
        end = at + len(snippet)
        if at in so and end in so:
            i, j = so.index(at), so.index(end)
            hits.append(new[sn[i]:sn[j]])
        else:
            hits.append(None)
    hits = [h for h in hits if h is not None]
    if hits and all(h == hits[0] for h in hits):
        return hits[0]
    return None


SOFT = re.compile(r"(?<![A-Za-z0-9_])(\$?)([cv])([A-Z]\w*)")


def uniform(s):
    return SOFT.sub(lambda m: m.group(1) + ("x" if m.group(2) == "v" else "t") + m.group(3) if m.group(0) not in ("cCatchError",) else m.group(0), s)


def literals(src):
    """(start, end, value, raw) of every plain string literal of a Python file"""
    out = []
    lines = src.splitlines(keepends=True)
    offs = [0]
    for ln in lines:
        offs.append(offs[-1] + len(ln))
    for tok in pytok.generate_tokens(io.StringIO(src).readline):
        if tok.type != pytok.STRING:
            continue
        raw = tok.string
        if re.match(r"^[rRbBuU]*[fF]", raw):
            continue  # an f-string is left to be read
        try:
            val = ast.literal_eval(raw)
        except Exception:
            continue
        if not isinstance(val, str):
            continue
        s = offs[tok.start[0] - 1] + tok.start[1]
        e = offs[tok.end[0] - 1] + tok.end[1]
        out.append((s, e, val, raw))
    return out


def requote(raw, val):
    m = re.match(r"^([rRuU]*)('''|\"\"\"|'|\")", raw)
    pre, q = m.group(1), m.group(2)
    if "r" in pre.lower():
        return pre + q + val + q
    body = val.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n" if len(q) == 1 else "\n")
    body = body.replace(q, "\\" + q) if len(q) == 1 else body
    return pre + q + body + q


total = 0
for py in sorted(glob.glob(os.path.join(ROOT, "spike", "**", "*.py"), recursive=True)):
    rel = os.path.relpath(py, ROOT).replace("\\", "/")
    if "/scratch/" in rel or rel.startswith("spike/v3") or rel.startswith("spike/v4"):
        continue
    src = open(py, encoding="utf-8").read()
    edits = []
    for s, e, val, raw in literals(src):
        if len(val) < 6 or not re.search(r"[A-Za-z]", val):
            continue
        new = renamed(val)
        how = "file"
        if new is None:
            if not SOFT.search(val) or val.strip() == "cCatchError":
                continue
            new = uniform(val)
            how = "uniform"
        if new == val:
            continue
        edits.append((s, e, requote(raw, new), how, val, new))
    # the uniform rule only where the script mutates Haro's own code: it holds a span of a renamed file
    if not any(how == "file" for *_, how, _v, _n in [(0, 0, 0, h, v, n) for s, e, r, h, v, n in edits]):
        edits = []
    if not edits:
        continue
    total += len(edits)
    print(f"== {rel}: {len(edits)} literal(s)")
    for s, e, rep, how, val, new in edits:
        if how == "uniform":
            print(f"   uniform: {val[:90]!r} -> {new[:90]!r}")
    if APPLY:
        for s, e, rep, how, val, new in sorted(edits, reverse=True):
            src = src[:s] + rep + src[e:]
        open(py, "w", encoding="utf-8", newline="").write(src)
print(f"{total} literal(s)")
