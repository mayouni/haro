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
    ('T22', 'H21', 'a pair\'s value ends at a line that ends in an operator', [
        ("                    if ke == 'nl' and depth == 0 and not (last is not None and (",
         "                    if ke == 'nl' and depth == 0 and not (False and last is not None and (")]),
    ('T23', 'H22', 'an unwrapped c name keeps its c', [("                if len(core) >= 2 and core[1].isupper() and core[0] in 'cv':",
                                                        "                if False:")]),
    # the third round (SPELLINGS-02)
    ('T24', 'H23', 'pc keeps its c', [("    if re.fullmatch(r'pc[A-Z]\\w*', core):", "    if False:")]),
    ('T25', 'H23', 'pa with an element letter is left', [("    if re.fullmatch(r'pa[ncoa][A-Z]\\w*', core):", "    if False:")]),
    ('T26', 'H25', 'Softanza\'s list letters are left', [("    if re.fullmatch(r'a[ncoa][A-Z]\\w*', core):", "    if False:")]),
    ('T27', 'H26', 'an ALL_CAPS name is left', [("    if re.fullmatch(r'[A-Z][A-Z0-9_]+', core) and (pre + core) in letters:",
                                                 "    if False and re.fullmatch(r'[A-Z][A-Z0-9_]+', core) and (pre + core) in letters:")]),
    ('T28', 'H27', 'a capitalised attribute is left', [("    if pre == '@' and re.fullmatch(r'[A-Z][a-z]\\w*', core) and (pre + core) in letters:",
                                                        "    if False and pre == '@' and re.fullmatch(r'[A-Z][a-z]\\w*', core) and (pre + core) in letters:")]),
    ('T29', 'H27', 'a counted name is a boolean when it starts at 0', [("        if name in counted:\n            out[name] = 'n'",
                                                                        "        if False:\n            out[name] = 'n'")]),
    ('T30', 'H24', 'a b name keeps its 1 and 0', [("    bool_literals(toks, renames)\n", "")]),
    ('T31', 'H24', 'a condition keeps its 1 and 0', [("        if toks[before][0] == 'id' and toks[before][1].lower() in ('if', 'elseif', 'while'):",
                                                      "        if False:")]),
    ('T32', 'H17', 'a call in capitals is lettered as a constant', [
        ("    if re.fullmatch(r'[A-Z][A-Z0-9_]+', core) and (pre + core) in letters:\n        return pre + letters[pre + core] + core",
         "    if re.fullmatch(r'[A-Z][A-Z0-9_]+', core):\n        return pre + letters.get(pre + core, 'x') + core")]),
    # rule O (D67, HARO-ONEFORM-01)
    ('T33', 'H28', 'a block\'s end word is left', [("            if stack and stack[-1] == 'blk':\n                stack.pop()\n                put(i, 'end')",
                                                   "            if stack and stack[-1] == 'blk':\n                stack.pop()\n                pass")]),
    ('T34', 'H28', 'a definition\'s end word is left', [("            elif not stack and low in DEF_ENDS:\n                put(i, '')",
                                                        "            elif not stack and low in DEF_ENDS:\n                pass")]),
    ('T35', 'H28', 'a word with a one spelling is left', [("            put(i, ONE_WORD[low])", "            pass")]),
    ('T36', 'H28', 'a block\'s braces are left', [("            if header:\n                stack[-1] = 'brace'", "            if False:\n                stack[-1] = 'brace'")]),
    ('T37', 'H29', 'self in a brace object is made this too', [("        elif word and low == 'self' and obj == 0:", "        elif word and low == 'self':")]),
    ('T38', 'H29', 'a class\'s parent after : is left', [("                            put(jj, 'from')", "                            pass")]),
    ('T39', 'H29', 'a definition\'s parameters are left', [("                        params(out, j, renames)", "                        pass")]),
    ('T40', 'H29', 'a trailing period is left', [("            if (j is None or out[j][0] == 'nl') and b is not None and out[b][1] == ')':",
                                                  "            if False:")]),
    ('T41', 'H29', 'a // comment is left', [("            if v.startswith('//'):", "            if False:")]),
    ('T42', 'H29', '&& and || are left', [("            put(i, 'and' if v == '&' else 'or')\n            out[i + 1][1] = ''",
                                           "            continue_ = None\n            i += 1\n            continue")]),
    ('T43', 'H30', 'rule O is never applied', [("    toks = one_form(toks, renames)\n", "")]),
    # v0.56 (D68): every definition ends with end, func a function and def a method
    ('T44', 'H31', 'no definition is ended', [("    toks = def_ends(toks, renames)\n", "")]),
    ('T45', 'H31', 'a method before private is not ended there', [("            if open_def and open_class:\n                close(open_def[0], ln, open_def[1])\n                open_def = None\n        elif w == 'class':",
                                                                  "            pass\n        elif w == 'class':")]),
    ('T46', 'H31', 'a one-line body stays on its definition\'s line', [("            body_on_own_line(out, j, b, renames)\n", "")]),
    ('T47', 'H31', 'a one-line body is read as parameters', [("                if first and k == 'op' and v == ')':\n                    closed = True",
                                                             "                if False:\n                    closed = True")]),
    ('T48', 'H29', 'a definition after a class stays func', [("            want = 'def' if open_class else 'func'", "            want = w")]),
    ('T49', 'H31', 'an end never takes the blank line after', [("        if nxt < upto and not code(nxt)", "        if False and nxt < upto and not code(nxt)")]),
    ('T50', 'H32', 'a line-end chain dot is dropped, as before', [("                if n is not None and n < len(out) and out[n][0] == 'id' and out[n][1].lower() not in KW:",
                                                                   "                if False:")]),
    ('T51', 'H33', 'a digit-led name is not read', [("                if j is not None and out[j][0] == 'num' and j + 1 < len(out) and out[j + 1][0] == 'id':",
                                                     "                if False:")]),
    # v0.57 (D69): see and put written as print, or through the stream
    ('T52', 'H34', 'see and put are left', [("    toks = printing(toks, renames)\n", "")]),
    ('T53', 'H34', 'a line ending in + nl is not print\'s', [("        if out[a][0] == 'id' and out[a][1].lower() == 'nl' and b is not None and out[b][1] == '+':",
                                                              "        if False:")]),
    ('T54', 'H01', 'a statement word ends no see\'s expression', [("            elif kj in ('id', 'op') and depth == 0 and vj.lower() in STMT_WORDS and last is not None:",
                                                                   "            elif False:")]),
    ('T55', 'H29', 'a bracket around the statement ends no see\'s expression', [("                if depth == 0:\n                    break   # it closes what holds the statement (a brace object's `}`)",
                                                                                 "                if False:\n                    break   # it closes what holds the statement (a brace object's `}`)")]),
    # v0.59 (D71)
    ('T56', 'H35', 'null and isnull are left', [("    toks = null_free(toks, renames)\n", "")]),
    ('T57', 'H36', 'a call is renamed as the local of its name', [("            called = j is not None and toks[j][1] == '('", "            called = False")]),
    ('T58', 'H37', 'a global named in text keeps its old name', [("            if k == 'st' and len(v) > 3 and v[1] == '$' and v[1:-1] in c_map:",
                                                                  "            if False:")]),
    ('T59', 'H37', 'a global named as a symbol keeps its old name', [("            if k == 'id' and is_symbol(toks, i) and v.startswith('$') and v in c_map:",
                                                                      "            if False:")]),
    # v0.61 (D73): rule A
    ('T60', 'H38', 'a name lettered a is left as written', [("    if m and (pre + core).lower() not in KW and core.lower() not in KW:",
                                                             "    if False:")]),
    ('T61', 'H38', 'a name lettered a is v whatever it holds', [("('v' if letters.get(pre + core) == 'v' else 'x')", "'v'")]),
    ('T62', 'H39', 'two names given one new name are both renamed', [("        if len(olds) > 1:", "        if False:")]),
    ('T63', 'H04', 'a list declared in a function is lettered a', [("        return 'v'\n    if low.startswith('new '):",
                                                                    "        return 'a'\n    if low.startswith('new '):")]),
    ('T64', 'H40', 'a definition\'s own name is respelled as a built-in', [
        ("        if v.startswith('_') or (h is not None and toks[h][0] == 'id' and toks[h][1].lower() in ('def', 'func', 'function')):",
         "        if v.startswith('_'):")]),
    ('T65', 'H40', 'a name with a leading underscore is respelled as a built-in', [
        ("        if v.startswith('_') or (h is not None", "        if (h is not None")]),
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
