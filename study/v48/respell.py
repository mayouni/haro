"""v0.48: Haro's own calls of built-ins re-spelled as the Principal ruled (2026-11-09, "ParentClassName"): a call `name(` whose name is a
built-in in any case (study/v48/builtin_names.py's table) is written in the table's spelling. Not touched: a member call (`o.len()`), a
name the file defines as its own function (Ring: the program's function replaces the built-in, v48's P07), strings and comments (an eval's
code is a string: it is found by the guard and named). A .ring file is never touched.

  python study/v48/respell.py --plan [files]
  python study/v48/respell.py --apply files
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "study", "v47"))
import builtin_names as B  # noqa: E402
import reletter as R  # noqa: E402

TABLE = B.table()
SQUASH = {k.replace("_", ""): v for k, v in TABLE.items()}


def rewrite(rel, src, strings_too=False):
    """(new text, {old: new}, [], conflicts) -- the shape study/v47/port_cases.py reads"""
    if not rel.endswith(".haro"):
        return src, {}, [], []
    toks = R.tokens(src)
    own = {m.group(1).lower() for m in re.finditer(r"(?mi)^\s*(?:func|def)\s+(\w+)", src)}
    out, done = [], {}
    for i, (k, v) in enumerate(toks):
        if k == "id" and v.lower() not in own:
            j = R.sig(toks, i, 1)
            want = SQUASH.get(v.lower().replace("_", "")) if j is not None and toks[j][1] == "(" and not R.is_member(toks, i) else None
            if want and want != v and not (v.startswith("$") or v.startswith("@")):
                done[v] = want
                v = want
        out.append(v)
    return "".join(out), done, [], []


if __name__ == "__main__":
    a = sys.argv[1:]
    apply = a and a[0] == "--apply"
    files = a[1:] or [f for f in R.code_files() if "/cases/" not in f]
    total = 0
    for rel in files:
        p = os.path.join(ROOT, rel)
        raw = open(p, "rb").read().decode("utf-8")
        src = raw.replace("\r\n", "\n")
        new, done, _, _ = rewrite(rel, src)
        n = sum(1 for x, y in zip(R.tokens(src), R.tokens(new)) if x[1] != y[1])
        total += n
        if n:
            print(f"{rel}: {n} call(s)" + ("" if apply else f"  e.g. {', '.join(f'{k}->{v}' for k, v in list(done.items())[:6])}"))
        if apply and new != src:
            open(p, "wb").write((new.replace("\n", "\r\n") if "\r\n" in raw else new).encode("utf-8"))
    print(f"{total} call(s)")
