"""v0.43 measurement: what Haro's own code puts where T3 will want a boolean.

For every tracked .haro file that parses as code, every condition (if, elseif/but, while, do-again) and every operand of
and / or / not is classified by its shape. Static: a call's return is unknown unless it is a native whose name says it answers
0 or 1. Prints totals and per-file counts; writes rows to runtime/v43/cond_rows.tsv.
"""
import json, subprocess, sys, collections, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HARO = os.path.join(ROOT, "vm", "zig-out", "bin", "haro.exe")
COMPARE = {"=", "!=", "<", ">", "<=", ">=", "<>"}
LOGIC = {"and", "or", "&&", "||"}
NOT = {"not", "!"}
COND_KEYWORDS = {"if", "elseif", "but", "while", "again"}


def files():
    out = subprocess.run(["git", "ls-files", "*.haro"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return [f for f in out if f.startswith("spike/")]


def kids(nodes, i, ch):
    return ch.get(i, [])


def classify(nodes, ch, i, src):
    n = nodes[i]
    k = n["k"]
    if k == "parenthesized_expression":
        inner = [c for c in ch.get(i, []) if nodes[c].get("n")]
        return classify(nodes, ch, inner[0], src) if inner else "other"
    if k == "binary_expression":
        ops = [nodes[c]["t"] for c in ch.get(i, []) if not nodes[c].get("n") and "t" in nodes[c]]
        op = ops[0].lower() if ops else ""
        if op in COMPARE:
            return "comparison"
        if op in LOGIC:
            return "logic"
        return "arith:" + op
    if k in ("unary_expression", "not_expression"):
        ops = [nodes[c].get("t", "").lower() for c in ch.get(i, []) if not nodes[c].get("n")]
        if ops and ops[0] in NOT:
            return "logic"
        return "unary"
    if k in ("true", "false") or (k == "identifier" and n.get("t", "").lower() in ("true", "false")):
        return "true/false"
    if k == "number":
        return "number literal"
    if k == "string":
        return "string literal"
    if k == "identifier":
        t = n.get("t", "")
        name = t.lstrip("$@")
        if len(name) > 1 and name[0] == "b" and name[1].isupper():
            return "name b-lettered"
        return "name other"
    if k in ("member_expression", "attribute_expression") or k.startswith("member"):
        return "attribute"
    if k == "call_expression" or k.endswith("call_expression") or k == "method_call":
        f = [c for c in ch.get(i, []) if nodes[c].get("n")]
        name = ""
        if f:
            fn = nodes[f[0]]
            name = fn.get("t", "")
            if not name:
                # a method call: take its last identifier
                ids = [nodes[c].get("t", "") for c in ch.get(f[0], []) if nodes[c]["k"] == "identifier"]
                name = ids[-1] if ids else ""
        low = name.lower()
        if re.match(r"^(is|has|contains|exists|find|starts|ends)", low) or low in ("eof", "fexists", "direxists"):
            return "call predicate-named"
        if low in ("len", "substr", "find", "ring_find", "count"):
            return "call len/find/count"
        return "call other"
    if k == "index_expression" or k.startswith("index") or k.startswith("subscript"):
        return "subscript"
    return "other:" + k


def main():
    tot = collections.Counter()
    per = collections.defaultdict(collections.Counter)
    rows = []
    skipped = []
    for f in files():
        p = subprocess.run([HARO, "dump", "--json", f], cwd=ROOT, capture_output=True, text=True)
        try:
            d = json.loads(p.stdout)
        except Exception:
            skipped.append((f, "no json"))
            continue
        if d.get("error"):
            skipped.append((f, "parse error"))
            continue
        nodes = d["nodes"]
        ch = collections.defaultdict(list)
        for i, n in enumerate(nodes):
            if "p" in n:
                ch[n["p"]].append(i)
        data = open(os.path.join(ROOT, f), "rb").read().decode("utf-8", "replace")
        if data.lstrip().upper().startswith("DEFINE"):
            skipped.append((f, "a declaration"))
            continue
        sites = []
        for i, n in enumerate(nodes):
            t = n.get("t", "").lower() if not n.get("n") else None
            if t in COND_KEYWORDS:
                par = n.get("p")
                sib = ch.get(par, [])
                after = [c for c in sib if c > i and nodes[c].get("n")]
                if after:
                    sites.append(("cond:" + t, after[0]))
            elif t in LOGIC:
                par = n["p"]
                for c in ch.get(par, []):
                    if nodes[c].get("n"):
                        sites.append(("operand:" + t, c))
            elif t in NOT:
                par = n["p"]
                for c in ch.get(par, []):
                    if c > i and nodes[c].get("n"):
                        sites.append(("operand:not", c))
                        break
        for where, c in sites:
            cl = classify(nodes, ch, c, data)
            tot[(where.split(":")[0], cl)] += 1
            per[f][cl] += 1
            s, e = nodes[c]["s"], nodes[c]["e"]
            line = data.count("\n", 0, s) + 1
            rows.append((f, line, where, cl, data[s:e].replace("\n", " ")[:120]))
    with open(os.path.join(ROOT, "runtime", "v43", "cond_rows.tsv"), "w", encoding="utf-8") as o:
        for r in rows:
            o.write("\t".join(map(str, r)) + "\n")
    print("files read:", len(per), " skipped:", len(skipped))
    for f, why in skipped:
        print("  skipped", why, f)
    byw = collections.defaultdict(collections.Counter)
    for (w, cl), n in tot.items():
        byw[w][cl] += n
    for w in sorted(byw):
        print(f"\n{w}: {sum(byw[w].values())}")
        for cl, n in byw[w].most_common():
            print(f"  {n:6d}  {cl}")


if __name__ == "__main__":
    main()
