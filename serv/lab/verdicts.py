"""RING'S VERDICT ON EVERY LAB CHECK -- so a check that fails on HaroServer says whose failure it is.

    python haro/serv/lab/verdicts.py

A check of the lab is an author's assertion, and an assertion can fail for two different reasons: the suite's own
expectation is not met by Softanza (it fails on Ring too), or Ring++ answers differently from Ring. The lab shows
the two apart only if it knows Ring's answer, so this asks for it: every check becomes one function of ONE Ring
program (its `Run` and its helpers renamed apart, each call inside a `try`), and that program runs

    on the ORACLE      runtime/... ring.exe of the A/B layout (D:\\rpp-pkgtest\\sec\\ora: our build of Ring 1.27, with
                       main's engine built Ring-flavoured beside it), from the migrated main worktree's library
                       (D:\\GitHub\\_wtmig, stzlib 0950e246a -- the commit the installed library is)
    on rnxc, WHOLE     the same program compiled at once, from the installed library: the compiler and the VM
                       without the resident path, so a check that differs only on the server names the server

Writes haro/serv/lab/verdicts.json: {id: {"ring": pass|fail|err, "whole": pass|fail|err}} and how it was taken.
Read-only on both library trees.
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RING = os.environ.get('RING') or r'D:/rpp-pkgtest/sec/ora/win64/ring.exe'
RING_TREE = os.environ.get('RING_TREE') or r'D:/GitHub/_wtmig/libraries/stzlib'
RNXC = os.environ.get('RNXC') or os.path.join(ROOT, 'zig-out', 'bin', 'rnxc.exe')
STZ_TREE = os.environ.get('STZ_TREE') or r'D:/ringpp/ringpp-win64/libraries/stzlib'
OUT = os.path.join(ROOT, 'runtime', 'lab')
NAME = r'[A-Za-z_@$][A-Za-z0-9_@$]*'


def lab_kit():
    """LabThen and LabShow, as lab.ring defines them."""
    src = open(os.path.join(HERE, 'lab.ring'), encoding='utf-8').read()
    keep = []
    for name in ('LabThen', 'LabShow'):
        m = re.search(r'^func ' + name + r'\b.*?(?=^func |\Z)', src, re.M | re.S)
        keep.append(m.group(0).rstrip() + '\n')
    return '\n'.join(keep)


def program(checks):
    top, funcs = ['load "stzlib.ring"', ''], []
    for c in checks:
        code, i = c['code'], c['id']
        for nm in set(re.findall(r'^(?:func|def)\s+(' + NAME + ')', code, re.M)):
            code = re.sub(r'(?<![A-Za-z0-9_@$])' + re.escape(nm) + r'(?![A-Za-z0-9_@$])', '%s_%d' % (nm, i), code, flags=re.I)
        funcs.append(code.rstrip() + '\n')
        top += ['try', '\t? "#%d " + Run_%d("")' % (i, i), 'catch', '\t? "#%d E " + cCatchError' % i, 'done']
    return '\n'.join(top) + '\n? "#END"\n\n' + lab_kit() + '\n' + '\n'.join(funcs)


def parse(out):
    """id -> (pass|fail|err, what it said): a FAIL's expected and got lines, an error's message."""
    v, cur = {}, None
    for line in out.replace('\r\n', '\n').split('\n'):
        m = re.match(r'#(\d+) (.*)', line)
        if not m:
            if cur is not None and v[cur][0] != 'pass' and line.strip():
                v[cur] = (v[cur][0], (v[cur][1] + '\n' + line).strip()[:400])
            continue
        cur, rest = int(m.group(1)), m.group(2)
        kind = 'pass' if rest.startswith('PASS') else 'err' if rest.startswith('E ') else 'fail'
        v[cur] = (kind, rest[2:].strip() if kind == 'err' else '')
    return v


def run(cmd, cwd, what):
    t = time.perf_counter()
    env = dict(os.environ, STZ_NO_VIEW='1')
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=1800, env=env)
    out = r.stdout.decode('utf-8', 'replace')
    print('%s: exit %d, %.0f s, reached the end: %s' % (what, r.returncode, time.perf_counter() - t, '#END' in out))
    if '#END' not in out:
        print('   its last lines:', ' | '.join(out.strip().split('\n')[-3:])[:400], (r.stderr.decode('utf-8', 'replace')[-300:]))
    return parse(out)


def main():
    d = json.load(open(os.path.join(HERE, 'checks.json'), encoding='utf-8'))
    os.makedirs(OUT, exist_ok=True)
    prog = os.path.join(OUT, 'verdicts_all.ring')
    open(prog, 'w', encoding='utf-8', newline='\n').write(program(d['checks']))
    ring = run([RING, prog], RING_TREE, 'the oracle')
    whole = run([RNXC, prog], STZ_TREE, 'rnxc, compiled whole')
    ids = [c['id'] for c in d['checks']]
    res = {}
    for i in ids:
        rk, rt = ring.get(i, ('none', ''))
        wk, wt = whole.get(i, ('none', ''))
        res[str(i)] = {'ring': rk, 'whole': wk, 'ring_said': rt, 'whole_said': wt}
    meta = {'taken': time.strftime('%Y-%m-%d %H:%M'), 'ring': RING, 'ring_tree': RING_TREE, 'rnxc': RNXC, 'stz_tree': STZ_TREE}
    json.dump({'meta': meta, 'verdicts': res}, open(os.path.join(HERE, 'verdicts.json'), 'w', encoding='utf-8'), indent=0)
    from collections import Counter
    print('on Ring:        ', dict(Counter(v['ring'] for v in res.values())))
    print('on rnxc, whole: ', dict(Counter(v['whole'] for v in res.values())))
    print('differ:', sum(1 for v in res.values() if v['ring'] != v['whole']))


main()
