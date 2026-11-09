"""v0.47: what the letter rule refuses in the repository's .haro code, file by file -- `haro census` on each, one process at a time.

A declaration (first word DEFINE) is no code and is skipped; a file another loads is counted where it is loaded and again alone (the
census of a file counts the statements of every file it loads), so the per-reason total is read from the distinct (file, line, name).

  python study/v47/census.py [--vm PATH] [--list]
"""
import glob, os, re, subprocess, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VM = os.path.join(ROOT, "vm", "zig-out", "bin", "haro.exe")
args = sys.argv[1:]
if "--vm" in args:
    VM = os.path.abspath(args[args.index("--vm") + 1])
LISTING = "--list" in args

LETTER = re.compile(r"^\s+(\d+)x (a name begins with its type's letter|`c` is Softanza's letter|[a-z] is the letter of)")


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


files = code_files()
total = collections.Counter()
per_file = []
for rel in files:
    r = subprocess.run([VM, "census", os.path.join(ROOT, rel)], capture_output=True, timeout=300, cwd=os.path.dirname(os.path.join(ROOT, rel)))
    text = r.stdout.decode("utf-8", "replace")
    n = 0
    for line in text.splitlines():
        m = LETTER.match(line)
        if m:
            n += int(m.group(1))
            total[m.group(2)] += int(m.group(1))
    per_file.append((n, rel))
print(f"{len(files)} .haro code files")
for n, rel in sorted(per_file, reverse=True):
    if n and (LISTING or n >= 1):
        print(f"  {n:5d}  {rel}")
print("by reason (summed over censuses, a loaded file counted with each loader):")
for k, v in total.most_common():
    print(f"  {v:6d}  {k}")
