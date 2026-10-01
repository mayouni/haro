"""haro_forge.py -- the guard of the Haro spike (charter section 10).

Born standalone; folded into bench/gate.py only when green. Every claim it
prints is a comparison against a pinned judge or an oracle:

  stage 1  the stzu meta-court, ported to pure Ring (haro/spike/stzu.ring),
           judged by stz/declarative/stzu/fixtures.json exactly as the Luau
           runner judges it, on rnxc AND on the oracle ring.exe -- and the two
           runtimes must print the same bytes for every fixture.

Later stages (the forge, the machine court against harb, the GBNF, the
refinement, the timing) are added below as they are built.

Usage: python haro/spike/haro_forge.py [--stage N] [--plant]
  --plant   plants a known-wrong verdict to prove the guard can fail.
"""
import json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RNXC = os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
ORACLE = os.path.join(ROOT, 'runtime', 'win64', 'ring.exe')
STZU_FIXTURES = r'D:\GitHub\stz\declarative\stzu\fixtures.json'
STZU_RING = os.path.join(HERE, 'stzu.ring')

PLANT = '--plant' in sys.argv


def run(exe, script, path):
    # cwd beside the script: Ring resolves a ROOT file's `load` from the
    # current directory (C-4), Ring++ beside the root; running both from
    # HERE asks the same question of each.
    env = dict(os.environ)
    env['RNXC_NOCACHE'] = '1'
    r = subprocess.run([exe, os.path.basename(script), path], capture_output=True,
                       env=env, timeout=120, cwd=os.path.dirname(script))
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def parse_verdict(out):
    """'ok' + fields, or a refusal line. Returns (accepted, fields|refusal)."""
    lines = [l for l in out.split('\n') if l != '']
    if not lines:
        return False, 'NO OUTPUT'
    if lines[0] != 'ok':
        return False, lines[0]
    fields = {}
    for l in lines[1:]:
        k, _, v = l.partition(' ')
        fields[k] = v
    return True, fields


def judge_stzu(exe, label):
    """Mirror experiment/run_stzu.luau: accepts carry structural
    expectations, rejects carry the fragment the refusal must contain."""
    doc = json.load(open(STZU_FIXTURES, encoding='utf-8'))
    assert doc['grammar'] == 'stzu' and doc['version'] == '0.1'
    passed = failed = 0
    outputs = {}
    with tempfile.TemporaryDirectory() as td:
        for case in doc['accepts'] + doc['rejects']:
            p = os.path.join(td, case['id'] + '.stzu')
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(case['source'])
            out = run(exe, STZU_RING, p)
            outputs[case['id']] = out
            ok, got = parse_verdict(out)
            why = ''
            if 'expect' in case:
                verdict = ok
                if not ok:
                    why = ' -- refused: ' + got
                else:
                    e = case['expect']
                    for k, want in e.items():
                        if k == 'counts':
                            for ck, cv in want.items():
                                if int(got.get(ck, '-1')) != cv:
                                    verdict = False
                                    why = f' -- {ck}: expected {cv} got {got.get(ck)}'
                        elif k == 'verbs':
                            g = [v for v in got.get('verbs', '').split(',') if v]
                            if g != sorted(want):
                                verdict = False
                                why = f' -- verbs: expected {sorted(want)} got {g}'
                        elif got.get(k) != want:
                            verdict = False
                            why = f" -- {k}: expected '{want}' got '{got.get(k)}'"
                if PLANT and case['id'] == 'A1':
                    verdict = False
                    why = ' -- PLANTED'
                kind = 'accept'
            else:
                frag = case['refusal']
                if ok:
                    verdict, why = False, ' -- ACCEPTED, must refuse'
                elif frag not in got:
                    verdict, why = False, f" -- refused for the wrong reason: '{frag}' not in '{got}'"
                else:
                    verdict = True
                kind = 'reject'
            if verdict:
                passed += 1
            else:
                failed += 1
                print(f'  FAIL {case["id"]} ({kind}): {case["name"]}{why}')
    print(f'STZU-CONFORMANCE ({label}): {passed} passed, {failed} failed')
    return failed, outputs


def stage1():
    print('stage 1 -- the stzu meta-court in pure Ring, judged by its pinned fixtures')
    f1, o1 = judge_stzu(RNXC, 'rnxc')
    f2, o2 = judge_stzu(ORACLE, 'oracle ring.exe')
    diff = [k for k in o1 if o1[k] != o2.get(k)]
    if diff:
        print(f'  FAIL the two runtimes differ on {len(diff)} fixture(s): {diff}')
        for k in diff[:3]:
            print('    rnxc  :', o1[k].strip()[:200])
            print('    oracle:', o2[k].strip()[:200])
    else:
        print(f'  ok   rnxc and the oracle print the same bytes on all {len(o1)} fixtures')
    return f1 + f2 + len(diff)


if __name__ == '__main__':
    t0 = time.perf_counter()
    failures = stage1()
    print(f'haro_forge: {"FAIL" if failures else "PASS"} ({failures} failure(s), {time.perf_counter()-t0:.1f} s)')
    sys.exit(1 if failures else 0)
