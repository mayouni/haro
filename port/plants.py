"""Every protection of haroport (HARO-PORTTOOL-01) switched off in turn: the court must fail, for the case that protection exists for. Each
plant is text substitutions in port/haroport.py, the court run, the file restored byte for byte -- verified by its digest, and restored even
when the script is stopped. No build: the tool is Python.

  python port/plants.py            all plants
  python port/plants.py T1 T3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, 'haroport.py')
COURT = os.path.join(HERE, 'port_court.py')

PLANTS = [
    ('T1', 'H01', 'a keyword in another case is left', [("        if k == 'id' and v.lower() in KW and v != v.lower() and not is_symbol(toks, i):",
                                                          "        if False and k == 'id' and v.lower() in KW and v != v.lower() and not is_symbol(toks, i):")]),
    ('T2', 'H01', 'a symbol\'s name is lowered too', [("        if k == 'id' and v.lower() in KW and v != v.lower() and not is_symbol(toks, i):",
                                                       "        if k == 'id' and v.lower() in KW and v != v.lower():")]),
    ('T3', 'H02', 'a function the tree defines is respelled as the built-in', [("        if j is None or toks[j][1] != '(' or v.lower() in tree_funcs:",
                                                                                "        if j is None or toks[j][1] != '(':")]),
    ('T4', 'H03', 'Softanza\'s c and v are left', [("                c_map[name] = new", "                pass")]),
    ('T5', 'H04', 'the top level and a class body are lettered too', [("        if kind in ('func', 'method'):", "        if True:")]),
    ('T6', 'H05', 'a method\'s attribute is made a local', [
        ("            if (v in decl or base in decl) and letter_word(base) and v not in attrs and base not in attrs:",
         "            if (v in decl or base in decl) and letter_word(base):"),
        ("            elif kind == 'method' and (new in attrs or v in attrs):", "            elif False:")]),
    ('T7', 'H12', 'a local lands on a name already in its function', [("            elif new in idents:", "            elif False:")]),
    ('T8', 'H08', 'an unwrapped name lands on a keyword', [("            if new.lower() in KW:\n                why = 'keyword:",
                                                           "            if False:\n                why = 'keyword:")]),
    ('T9', 'H06', 'a c name lands on a name already in the tree', [("            elif new in tree_names:", "            elif False:")]),
    ('T10', 'H10', 'a load keeps .ring', [("    return re.sub(r'(?m)^(\\s*load\\s+[\"\\'][^\"\\'\\n]*?)\\.ring([\"\\'])', r'\\1.haro\\2', text)", "    return text")]),
    ('T11', 'H07', '_name_ is not unwrapped', [("    return v[1:-1] if len(v) > 2", "    return None if len(v) > 2")]),
]


def main():
    want = set(sys.argv[1:])
    original = open(TOOL, 'rb').read()

    def restore():
        open(TOOL, 'wb').write(original)
        assert hashlib.sha256(open(TOOL, 'rb').read()).hexdigest() == hashlib.sha256(original).hexdigest()

    results = []
    try:
        for pid, case, why, subs in PLANTS:
            if want and pid not in want:
                continue
            text = original.decode('utf-8')
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r} ({text.count(stale[0])} found)', flush=True)
                results.append((pid, 'STALE'))
                continue
            for o, n in subs:
                text = text.replace(o, n)
            open(TOOL, 'wb').write(text.encode('utf-8'))
            r = subprocess.run([sys.executable, COURT], capture_output=True, timeout=900)
            restore()
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', r.stdout.decode('utf-8', 'replace'), re.M)
            verdict = 'CAUGHT' if case in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its case {case}; failed {", ".join(failed) or "none"}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
