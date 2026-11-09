"""v0.47: a rung's case programs re-lettered by study/v47/reletter.py's rules, and each changed line carried back into that case's
region of the rung's gen_fixtures.py (the program's source), so regenerating writes the re-lettered case. A line whose old text is not
found exactly once in its case's region is printed and nothing of that case is changed: it is done by hand.

  python study/v47/port_cases.py v38 [W01 W02 ...]     the cases named, or every case of the rung
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import reletter as R  # noqa: E402
# v0.48: `--respell` ports with study/v48/respell.py (the built-ins' spelling) instead of the letters' rules
if '--respell' in sys.argv:
    sys.argv.remove('--respell')
    sys.path.insert(0, os.path.join(ROOT, 'study', 'v48'))
    import respell as TOOL  # noqa: E402
else:
    TOOL = R


def literals(s):
    """the Python literals a program line may be written as"""
    out = ["'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"]
    if "'" in s:
        out.append('"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"')
    return out


def requote(lit, new):
    if lit.startswith("'"):
        return "'" + new.replace("\\", "\\\\").replace("'", "\\'") + "'"
    return '"' + new.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    rung, want = sys.argv[1], set(sys.argv[2:])
    gp = os.path.join(ROOT, "spike", rung, "gen_fixtures.py")
    g = open(gp, encoding="utf-8").read()
    starts = [(m.start(), m.group(1)) for m in re.finditer(r"\n    \('([A-Z]\d+)',", g)]
    ends = {cid: (starts[i + 1][0] if i + 1 < len(starts) else g.index("\n]", s)) for i, (s, cid) in enumerate(starts)}
    edits = []
    for s, cid in starts:
        if want and cid not in want:
            continue
        cf = os.path.join(ROOT, "spike", rung, "cases", cid + ".haro")
        if not os.path.exists(cf):
            continue
        rel = f"spike/{rung}/cases/{cid}.haro"
        old = open(cf, encoding="utf-8").read()
        new, _, _, conflicts = TOOL.rewrite(rel, old)
        if conflicts:
            print(f"{cid}: CONFLICT {conflicts}")
            continue
        if new == old:
            continue
        region = g[s:ends[cid]]
        ok, local = True, []
        for a, b in zip(old.split("\n"), new.split("\n")):
            if a == b:
                continue
            a0, b0 = a.lstrip("\t"), b.lstrip("\t")
            hits = [(lit, region.count(lit)) for lit in literals(a0)]
            hit = [lit for lit, n in hits if n >= 1]
            if not hit:
                print(f"{cid}: NOT FOUND {a0!r} -> {b0!r}")
                ok = False
                break
            local.append((hit[0], requote(hit[0], b0)))
        if not ok:
            continue
        for lit, rep in local:
            region = region.replace(lit, rep)
        edits.append((s, ends[cid], region, cid))
    for s, e, region, cid in sorted(edits, reverse=True):
        g = g[:s] + region + g[e:]
        print(f"{cid}: ported")
    open(gp, "w", encoding="utf-8", newline="\n").write(g)


if __name__ == "__main__":
    main()
