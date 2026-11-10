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
    ('T3', 'H02', 'a function the tree defines is respelled as the built-in', [("        if v.lower() in tree_funcs:",
                                                                                "        if False:")]),
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
    ('T10', 'H10', 'a load keeps .ring', [("    return re.sub(r'(?m)^(", "    return text or re.sub(r'(?m)^(")]),
    ('T11', 'H07', '_name_ is not unwrapped', [("    return v[1:-1] if len(v) > 2", "    return None if len(v) > 2")]),
    # the second round
    ('T12', 'H13', 'an @-attribute in a method is refused as bare', [
        ("if line_start and k == 'id' and not v.startswith('@') and v in attrs", "if line_start and k == 'id' and v in attrs")]),
    ('T13', 'H14', 'a load after a byte order mark keeps .ring', [
        ("    return re.sub(r'(?m)^(\\ufeff?\\s*load", "    return re.sub(r'(?m)^(\\s*load")]),
    ('T14', 'H15', '$_name is left', [("            g = '$' + name[2:]", "            g = name")]),
    ('T15', 'H16', '$_name lands on a $name already in the tree', [("            if g in tree_names:", "            if False:")]),
    ('T16', 'H17', 'a call keeps its spelling against the declaration', [
        ("                if want != v:\n                    toks[i][1] = want\n                    renames.append(('D', v, want))",
         "                if False:\n                    toks[i][1] = want\n                    renames.append(('D', v, want))")]),
    ('T17', 'H18', 'a name declared in two spellings takes one of them', [("            if len(spellings) > 1:", "            if False:")]),
    ('T18', 'H19', ':key = value is left', [("    toks, pairs = pair_lists(toks)", "    pairs = []")]),
    ('T19', 'H19', 'a pair\'s value ends at any comma', [("                    elif ke == 'op' and ve == ',' and depth == 0:",
                                                         "                    elif ke == 'op' and ve == ',':")]),
    ('T20', 'H20', 'the unit is the whole tree', [("    reach = loaded(root, rels, srcs, unit) if unit else set(rels)", "    reach = set(rels)")]),
    ('T21', 'H17', 'a call through a receiver is respelled', [
        ("        if k != 'id' or v.startswith(('$', '@')) or is_member(toks, i) or is_symbol(toks, i):",
         "        if k != 'id' or v.startswith(('$', '@')) or is_symbol(toks, i):")]),
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
