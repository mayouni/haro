"""Phase 1.5 -- the exemplar extension study: run every experiment and check every fact STUDY.md cites.

  python haro/study/phase15/study_run.py

  E3  NaturalLib 1.27 as shipped      (e3_run.py: official Ring 1.27; Ring++ for the refusal)
  E1  the tontine knowledge graph     (e12_run.py: stzKnowledgeGraph on the Ring++ package)
  E2  stzNatural as shipped, retargeted by data   (e12_run.py)
  E4  the composed exemplar, two languages, judged  (e4_run.py: G1-G7)

Needs the Ring++ package (python bench/package.py), the author's tree at D:\\GitHub\\stzlib (read-only), zing's
build for the live witness, and the official Ring 1.27 install: each experiment SKIPs or says so when its
subject is not there. About twenty seconds warm; a cold first run compiles Softanza for each program (~30 s more).
Writes nothing outside this folder.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
steps = [('E3 NaturalLib as shipped', 'e3_run.py'), ('E1+E2 the graph and stzNatural', 'e12_run.py'), ('E4 the composed exemplar', 'e4_run.py')]
failed = []
t0 = time.perf_counter()
for label, script in steps:
    print(f'\n=== {label} ({script})')
    sys.stdout.flush()
    p = subprocess.run([sys.executable, os.path.join(HERE, script)] + [a for a in sys.argv[1:] if a == '--plant'], cwd=HERE)
    if p.returncode != 0:
        failed.append(script)
print(f'\nphase15: {"FAIL" if failed else "PASS"} -- {len(steps) - len(failed)} of {len(steps)} experiment groups hold ({time.perf_counter() - t0:.0f} s){" -- failed: " + ", ".join(failed) if failed else ""}')
sys.exit(1 if failed else 0)
