"""v0.47: Haro's own code re-lettered by rule (D55 T2, the author's scope of 2026-11-08: "Yes, as recommended").

THE RULES, in order of precedence, applied to the tokens of a .haro code file (strings and comments untouched, save the one case below):
  R1  Softanza's c is text: cName -> tName, $cX -> $tX, everywhere a token is so spelled -- file-wide and repository-wide, so a global
      or an attribute keeps one name across files
  R2  a t-name that held a TOKEN (a list) before the rule is `a`, Softanza's list, until v0.50 letters it: tName -> aName, in the
      library files named in T_TOKENS, read one by one (study/v47/names.py lists every t-name and its assignment)
  R3  a single letter or a word that is declared in a function (assigned, a parameter, a counter of a while loop) is lettered by what
      it holds, the original kept after the letter: a number n (nI, nJ, nN), a text t (tC, tS), a token or a list a (aT, aV),
      anything else x (xV, xA) -- the letter a value is read by, never guessed into a checked one: x and a are not checked until their
      rungs, so a doubtful reading costs nothing at run time. A single letter that is only ever a `for` counter in its function stays
  R1 keeps `cCatchError`, Ring's name for the caught error: the system gives it and the program only reads it, which no letter rule
      judges (a declaration is what is lettered)
  R5  a v-name held any value (Softanza's "value": vInit, vKey, vVal, vC), and D55's v is the vector: it is x
  R4  the forge writes code in strings: a `$c` global spelled inside a string of forge.haro follows R1, since the court it forges
      declares that global

A rename whose new name already stands in the same function is a CONFLICT, printed and not applied: the file is left as it was.

  python study/v47/reletter.py --plan            the renames, file by file, with conflicts
  python study/v47/reletter.py --apply FILE...   rewrite the files (LF kept as each has it)
"""
import os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

T_TOKENS = {"spike/court_lib.haro", "spike/haro_lib.haro", "spike/severity_lib.haro", "spike/block_lib.haro", "spike/expr_lib.haro"}
# a name the system gives and the program only reads: Ring's caught error, which D52 kept (v0.37's `catch e` binds beside it)
SYSTEM = {"cCatchError"}
# a reading R3 cannot make, or a name it would land on twice: (file, function, name) -> the name given
OVERRIDES = {
    ("spike/haro_lib.haro", "StzuParseMessageList", "t"): "aNext",
    # found by the guard's stage 1 (TYPE_LETTER): PatNew's third part is any value, not a character
    ("spike/pattern_lib.haro", "PatNew", "c"): "xC",
}
KEYWORDS = set("""again and but bye call case catch class continue def do done else elseif end exit for from func get give if import in
load loop new next not off ok on or other package private put return see step switch to try while within using finally null true
false this self""".split())

TOK = re.compile(r'''(?P<cm>\#[^\n]*|//[^\n]*|/\*.*?\*/)|(?P<st>"[^"]*"|'[^']*'|`[^`]*`)|(?P<id>[$@]?[A-Za-z_][A-Za-z0-9_]*)|(?P<num>\d+(?:\.\d+)?)|(?P<nl>\n)|(?P<ws>[ \t\r]+)|(?P<op>.)''', re.S)


def tokens(src):
    out = []
    for m in TOK.finditer(src):
        out.append([m.lastgroup, m.group()])
    return out


def scopes(toks):
    """[(start, end, name)] over token indexes: the top level, then each func/def/class to the next"""
    marks = [(0, "@main")]
    line_start = True
    for i, (k, v) in enumerate(toks):
        if k == "nl":
            line_start = True
            continue
        if k in ("ws", "cm"):
            continue
        if line_start and k == "id" and v in ("func", "def", "class"):
            nm = next((toks[j][1] for j in range(i + 1, min(i + 6, len(toks))) if toks[j][0] == "id"), "?")
            marks.append((i, ("class " if v == "class" else "") + nm))
        line_start = False
    out = []
    for n, (s, nm) in enumerate(marks):
        e = marks[n + 1][0] if n + 1 < len(marks) else len(toks)
        out.append((s, e, nm))
    return out


def sig(toks, i, step):
    """the next significant token from i in direction step"""
    j = i + step
    while 0 <= j < len(toks) and toks[j][0] in ("ws", "cm"):
        j += step
    return j if 0 <= j < len(toks) else None


def is_member(toks, i):
    j = sig(toks, i, -1)
    return j is not None and toks[j][1] == "."


def shape(name):
    core = name.lstrip("$@")
    if len(core) == 1 and core.islower(): return "single"
    if len(core) >= 2 and core[0].islower() and core[1].isupper(): return "lettered"
    if core == core.lower() and re.match(r"^[a-z_][a-z0-9_]*$", core): return "word"
    return "other"


def rhs_text(toks, i):
    """the code after `=` on the line of the token at i"""
    j = sig(toks, i, 1)
    if j is None or toks[j][1] not in ("=", "+", "-", "*", "/"):
        return None
    if toks[j][1] != "=":
        k = sig(toks, j, 1)
        if k is None or toks[k][1] != "=":
            return None
        j = k
    else:
        k = sig(toks, j, 1)
        if k is not None and toks[k][1] == "=":
            return None
    parts = []
    j += 1
    while j < len(toks) and toks[j][0] != "nl":
        parts.append(toks[j][1])
        j += 1
    return "".join(parts).strip()


NUM_CALLS = ("len(", "ascii(", "number(", "floor(", "ceil(", "round(", "abs(", "fabs(", "sqrt(", "pow(", "ExNumText(")
TEXT_CALLS = ("char(", "substr(", "upper(", "lower(", "trim(", "string(", "left(", "right(", "copy(", "hex(", "RingStr(", "StzuJoin(",
              "CondPrintP(", "CondRightText(")
TOKEN_CALLS = ("CtNext(", "CtPeek(", "CtExpect(", "StzuPeek(", "StzuExpect(", "StzuNext(", "ExPeek(", "ExNext(", "CondNext(", "CondPeek(",
               "BlkPeek(", "BlkNext(", "BlkLexError(")


def kind_of(rhs, known):
    """the letter a value assigned as `rhs` is read by: n, t, a or x"""
    r = rhs.strip()
    if not r:
        return None
    if r == "null":
        return None
    if re.fullmatch(r"-?\d+", r) or r.startswith(NUM_CALLS):
        return "n"
    if r.startswith("substr("):
        # Ring's substr: two arguments find (a position), three take a piece (a text)
        depth, commas = 0, 0
        for ch in r[len("substr("):]:
            if ch in "([": depth += 1
            elif ch in ")]":
                if depth == 0: break
                depth -= 1
            elif ch == "," and depth == 0: commas += 1
        return "n" if commas == 1 else "t"
    if r.startswith('"') or r.startswith("'") or r.startswith("`") or r.startswith(TEXT_CALLS) or r.startswith("+"):
        return "t"
    if r.startswith(TOKEN_CALLS) or r.startswith("["):
        return "a"
    if r.startswith("new "):
        return "o"
    m = re.fullmatch(r"([$@]?[A-Za-z_]\w*)(\[[^\]]*\])?", r)
    if m:
        base = m.group(1)
        core = base.lstrip("$@")
        idx = m.group(2)
        if shape(base) == "lettered":
            l = core[0]
            if idx:
                return "t" if l in "ct" else ("a" if re.search(r"Toks", base) else None)
            return {"c": "t", "t": "t", "n": "n", "i": "n", "a": "a", "b": None}.get(l)
        if core in known:
            return None if idx else known[core]
    if re.fullmatch(r"[\w$@]+\s*[-+*/%]\s*[\w$@]+(\s*[-+*/%]\s*[\w$@]+)*", r):
        ops = re.findall(r"[$@]?[A-Za-z_]\w*", r)
        if all((shape(o) == "lettered" and o.lstrip("$@")[0] in "ni") or known.get(o) == "n" for o in ops):
            return "n"
    return None


PARAM_KIND = {"c": "t", "n": "n", "i": "n", "j": "n", "k": "n", "m": "n"}


def scope_plan(toks, s, e, fname, rel):
    """{old: new} for the singles and words declared in this scope"""
    decl = collections.defaultdict(list)   # name -> [(how, rhs)]
    idents = set()
    line_start = True
    func_line = s if fname != "@main" else None
    for i in range(s, e):
        k, v = toks[i]
        if k == "nl":
            line_start = True
            continue
        if k in ("ws", "cm"):
            continue
        if k == "id":
            idents.add(v)
            if line_start and v in ("within", "using"):
                # a block's name: `within $g = v`, `using o = v` (D52)
                j = sig(toks, i, 1)
                if j is not None and toks[j][0] == "id":
                    r = rhs_text(toks, j)
                    if r is not None:
                        decl[toks[j][1]].append(("assign", r))
            elif line_start:
                r = rhs_text(toks, i)
                if r is not None:
                    decl[v].append(("assign", r))
        line_start = False
    # parameters: the identifiers on the func line after the function's name
    if not fname.startswith("class ") and fname != "@main":
        i = s
        seen_name = False
        while i < e and toks[i][0] != "nl":
            if toks[i][0] == "id":
                if toks[i][1] in ("func", "def"):
                    pass
                elif not seen_name:
                    seen_name = True
                else:
                    decl[toks[i][1]].append(("param", None))
            i += 1
    # for counters
    for i in range(s, e):
        if toks[i][0] == "id" and toks[i][1] == "for":
            j = sig(toks, i, 1)
            if j is not None and toks[j][0] == "id":
                decl[toks[j][1]].append(("for", None))
    plan = {}
    known = {}
    for _round in range(3):
        for name, hows in decl.items():
            if name in KEYWORDS or shape(name) not in ("single", "word"):
                continue
            if all(h == "for" for h, _ in hows) and shape(name) == "single":
                continue
            kinds = set()
            for h, r in hows:
                if h == "param":
                    kinds.add(PARAM_KIND.get(name.lstrip("$@"), "x"))
                elif h == "assign":
                    kd = kind_of(r, known)
                    if kd: kinds.add(kd)
            kinds.discard(None)
            letter = kinds.pop() if len(kinds) == 1 else ("x" if kinds or True else "x")
            if len(kinds) > 0:
                letter = "x"
            known[name.lstrip("$@")] = letter
            core = name.lstrip("$@")
            prefix = name[: len(name) - len(core)]
            plan[name] = OVERRIDES.get((rel, fname, name)) or (prefix + letter + core[0].upper() + core[1:])
    return plan, idents


def file_plan(rel, src):
    toks = tokens(src)
    file_map = {}
    conflicts = []
    t_tok = rel in T_TOKENS
    for k, v in toks:
        if k != "id":
            continue
        core = v.lstrip("$@")
        pre = v[: len(v) - len(core)]
        if len(core) >= 2 and core[1].isupper():
            if v in SYSTEM:
                continue
            if core[0] == "c":
                file_map[v] = pre + "t" + core[1:]
            elif core[0] == "v":
                file_map[v] = pre + "x" + core[1:]
            elif core[0] == "t" and t_tok and not pre:
                file_map[v] = "a" + core[1:]
    scope_maps = []
    for s, e, nm in scopes(toks):
        sp, idents = scope_plan(toks, s, e, nm, rel)
        # every name the scope will hold after the file map, to find a rename that lands on a name already there
        after = {file_map.get(x, x) for x in idents}
        for old, new in list(sp.items()):
            if new in after or new in file_map.values() and new in {file_map.get(x) for x in idents}:
                conflicts.append(f"{rel} {nm}: {old} -> {new} (already there)")
                del sp[old]
        for old, new in file_map.items():
            if old in idents and new in idents and file_map.get(new, new) == new:
                conflicts.append(f"{rel} {nm}: {old} -> {new} (already there)")
        scope_maps.append((s, e, nm, sp))
    # a $ global is one name in every function: renamed file-wide, by what every scope that declares it reads it as
    globs = collections.defaultdict(set)
    for s, e, nm, sp in scope_maps:
        for old in [o for o in sp if o.startswith("$")]:
            globs[old].add(sp.pop(old))
    for old, news in globs.items():
        file_map[old] = news.pop() if len(news) == 1 else "$x" + old[1].upper() + old[2:]
    return toks, file_map, scope_maps, conflicts


def rewrite(rel, src, strings_too=False):
    toks, file_map, scope_maps, conflicts = file_plan(rel, src)
    out = []
    for s, e, nm, sp in scope_maps:
        for i in range(s, e):
            k, v = toks[i]
            if k == "id":
                if v in sp and not is_member(toks, i):
                    v = sp[v]
                elif v in file_map:
                    v = file_map[v]
            elif k == "st" and strings_too:
                v = re.sub(r"\$c([A-Z]\w*)", r"$t\1", v)
            out.append(v)
    return "".join(out), file_map, scope_maps, conflicts


def code_files():
    import glob
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "*.haro"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace("\\", "/")
        if rel.startswith(("runtime/", "vm/")) or "/scratch/" in rel:
            continue
        lines = [ln for ln in open(f, encoding="utf-8", errors="replace").read(20000).splitlines()
                 if ln.strip() and not ln.lstrip().startswith(("--", "#"))]
        if lines and lines[0].lstrip().upper().startswith("DEFINE"):
            continue
        out.append(rel)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--plan":
        files = a[1:] or [f for f in code_files() if "/cases/" not in f]
        for rel in files:
            src = open(os.path.join(ROOT, rel), encoding="utf-8", newline="").read()
            _, file_map, scope_maps, conflicts = rewrite(rel, src)
            used = sum(1 for k in file_map)
            print(f"== {rel}: {used} lettered renames (c->t{', t->a' if rel in T_TOKENS else ''})")
            for s, e, nm, sp in scope_maps:
                if sp:
                    print(f"   {nm}: " + ", ".join(f"{o}->{n}" for o, n in sp.items()))
            for c in conflicts:
                print("   CONFLICT", c)
    elif a and a[0] == "--apply":
        bad = 0
        for rel in a[1:]:
            p = os.path.join(ROOT, rel)
            raw = open(p, "rb").read().decode("utf-8")
            src = raw.replace("\r\n", "\n")
            new, _, _, conflicts = rewrite(rel, src, strings_too=rel.endswith("forge.haro"))
            if conflicts:
                bad += 1
                print(f"{rel}: NOT APPLIED, {len(conflicts)} conflicts")
                for c in conflicts: print("   ", c)
                continue
            if "\r\n" in raw:
                new = new.replace("\n", "\r\n")
            if new != raw:
                open(p, "wb").write(new.encode("utf-8"))
                print(f"{rel}: rewritten")
        sys.exit(1 if bad else 0)
    else:
        print(__doc__)
