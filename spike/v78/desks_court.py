"""Haro v0.78, three findings of the desks (HARO-COMPILE-EXIT-01, HARO-LIBIMAGE-01, HARO-INVOCATION-STDIN-01): every case of
v78/fixtures.json on haro and on its checked build. A case passes when, on both builds:

  library   a copy of cases/lib and a cache folder of the case's own; each step is done in order and judged:
              fresh    the root is run in an empty cache -- its bytes, its exit code, its path line -- and its image is taken away
              prefix   `haro prefix lib.haro` ends with 0 and keeps one library file
              run      the root is run: the fixture's bytes and exit code, the SAME bytes and exit code as every run before it
                       in the case (the whole compile among them, where the case has one), and the fixture's path line
              append   a line is added to the library's file
              images   the cache folder holds that many images of a root
            the path line: with HARO_PATH=1 the run writes exactly one line that starts with `path: ` to its standard error,
            the fixture's; a case marked silent runs without HARO_PATH and writes none
  prefix    `haro prefix` prints the fixture's words and ends with its code
  usage     `haro` with no argument prints the fixture's words
  limit     the court writes a program of the fixture's size and runs the fixture's command under each memory limit of the
            ladder (0: no limit). Where a run says the fixture's words, its exit code is the fixture's; and at least one rung
            says them -- a ladder that never does asked nothing, and fails. A case without words is judged on its bytes
  run       the file is run in a copy of its folder: the fixture's bytes and exit code
  D41       the two builds answer the same: the same bytes, codes and path lines (a limit case: the same verdict)

  python spike/v78/desks_court.py                haro and the checked build, as paths.py finds them
  python spike/v78/desks_court.py --vm X.exe      one build only (the plants)
  python spike/v78/desks_court.py --only L06      one case alone
  python spike/v78/desks_court.py --plant         the guard's own plant: one fixture's bytes doctored, so the court must fail
"""
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths

WORK = os.path.join(ROOT, 'runtime', 'v78', 'court')
LIMIT = os.path.join(HERE, 'under_limit.py')


def sh(exe, args, cwd, extra=None, mb=0, cache=None):
    """one run: its standard output, its standard error, its exit code"""
    env = dict(os.environ)
    for k in ('HARO_NOCACHE', 'HARO_NOIMAGE', 'HARO_PATH', 'HARO_IMAGE', 'HARO_CACHE'):
        env.pop(k, None)
    env['HARO_HOME'] = SPIKE
    env['PATH'] = os.path.dirname(exe) + os.pathsep + env.get('PATH', '')
    if cache:
        env['HARO_CACHE'] = cache
    else:
        env['HARO_NOCACHE'] = '1'
    env.update(extra or {})
    cmd = [exe] + args
    if mb:
        cmd = [sys.executable, LIMIT, str(mb)] + cmd
    try:
        r = subprocess.run(cmd, capture_output=True, env=env, timeout=300, cwd=cwd)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', '', -1
    out = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    err = r.stderr.decode('utf-8', 'replace').replace('\r\n', '\n')
    return out, err, r.returncode


def copy_of(sub, label, cid):
    dst = os.path.join(WORK, label, cid)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(os.path.join(HERE, 'cases', sub), dst)
    return dst


def bytes_bad(c, out, rc):
    bad = []
    if 'stdout' in c and out != c['stdout']:
        bad.append(f'prints {out[:300]!r}, not {c["stdout"]!r}')
    for h in c.get('has', []):
        if h not in out:
            bad.append(f'does not print {h!r}: {out.strip()[:240]!r}')
    if 'never' in c and c['never'] in out:
        bad.append(f'prints {c["never"]!r}')
    if rc != c['exit']:
        bad.append(f'ends with {rc}, not {c["exit"]}')
    return bad


def library(c, label, exe):
    d = copy_of('lib', label, c['id'])
    cache = os.path.join(d, '_cache')
    os.makedirs(cache)
    extra = dict(c.get('env', {}))
    if not c.get('silent'):
        extra['HARO_PATH'] = '1'
    bad, seen, said = [], [], []
    for n, (step, arg) in enumerate(c['steps'], 1):
        if step == 'prefix':
            out, err, rc = sh(exe, ['prefix', 'lib.haro'], d, cache=cache)
            kept = glob.glob(os.path.join(cache, '*.harop'))
            if rc != 0 or len(kept) != 1:
                bad.append(f'step {n}: `haro prefix` ends with {rc} and keeps {len(kept)} library file(s): {(out + err).strip()[:200]!r}')
        elif step == 'append':
            with open(os.path.join(d, 'lib.haro'), 'a', encoding='utf-8', newline='\n') as f:
                f.write(arg)
        elif step == 'images':
            have = len(glob.glob(os.path.join(cache, '*.haroi')))
            if have != arg:
                bad.append(f'step {n}: the cache holds {have} image(s) of a root, not {arg}')
            said.append(f'images {have}')
        else:
            out, err, rc = sh(exe, [c['root']], d, extra=extra, cache=cache)
            for b in bytes_bad(c, out, rc):
                bad.append(f'step {n} ({step}): the run {b}')
            if seen and (out, rc) != seen[0]:
                bad.append(f'step {n} ({step}): the run prints {out[:200]!r} (exit {rc}), not what step 1 of the case printed')
            seen.append((out, rc))
            lines = [ln for ln in err.split('\n') if ln.startswith('path:')]
            if c.get('silent'):
                if lines:
                    bad.append(f'step {n} ({step}): without HARO_PATH the run writes {lines!r}')
            elif lines != [arg]:
                bad.append(f'step {n} ({step}): the path line is {lines!r}, not {[arg]!r}')
            said.append(repr((out, rc, lines)))
            if step == 'fresh':
                for p in glob.glob(os.path.join(cache, '*.haroi')):
                    os.remove(p)
    return bad, '\x00'.join(said)


def prefix(c, label, exe):
    d = copy_of('lib', label, c['id'])
    cache = os.path.join(d, '_cache')
    os.makedirs(cache)
    out, err, rc = sh(exe, ['prefix', c['library']], d, cache=cache)
    first = out.split('\n')[0]
    return [f'`haro prefix` {b}' for b in bytes_bad(c, first, rc)], first.split(',')[0] + f'|{rc}'


def usage(c, label, exe):
    out, err, rc = sh(exe, [], HERE)
    text = out + err
    return [f'the usage text does not hold {h!r}' for h in c['has'] if h not in text], text


def big_program(label, functions):
    d = os.path.join(WORK, label, 'big')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'big.haro')
    lines = []
    for i in range(functions):
        lines += [f'func F{i}(iA, iB)', f'\tiC = iA * {i} + iB', f'\tif iC > {i}', f'\t\treturn iC - {i}', '\tend', '\treturn iC', 'end', '']
    lines.append('print F1(2, 3)')
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    return d


def limit(c, label, exe, big):
    d = big_program(label, big['functions'])
    args = ['big.haro' if a == '{big}' else a for a in c['args']]
    bad, said, rows = [], 0, []
    for mb in c['ladder']:
        out, err, rc = sh(exe, args, d, mb=mb)
        if 'says' in c:
            if c['says'] in out + err:
                said += 1
                rows.append(f'{mb} MB: says it, exit {rc}')
                if rc != c['exit']:
                    bad.append(f'under {mb} MB the run says {c["says"]!r} and ends with {rc}, not {c["exit"]}')
        else:
            for b in bytes_bad(c, out, rc):
                bad.append(f'the run {b}')
    if 'says' in c and not said:
        bad.append(f'no rung of {c["ladder"]} MB says {c["says"]!r}: the case asked nothing on this build')
    return bad, 'verdict:' + ('bad' if bad else 'good')


def run(c, label, exe):
    d = copy_of(c['dir'], label, c['id'])
    out, err, rc = sh(exe, [c['file']], d)
    return [f'the run {b}' for b in bytes_bad(c, out, rc)], out + f'|{rc}'


def judge(c, label, exe, doc):
    kind = c['kind']
    if kind == 'library':
        return library(c, label, exe)
    if kind == 'prefix':
        return prefix(c, label, exe)
    if kind == 'usage':
        return usage(c, label, exe)
    if kind == 'limit':
        return limit(c, label, exe, doc['big'])
    return run(c, label, exe)


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    if ONLY:
        doc['cases'] = [c for c in doc['cases'] if c['id'] == ONLY]
    for c in doc['cases']:
        if PLANT and c['id'] == 'L01':
            c = json.loads(json.dumps(c))
            c['stdout'] += 'doctored\n'
        res = [judge(c, label, exe, doc) for label, exe in builds]
        bad = [f'{label}: {b}' for (label, _), (bs, _) in zip(builds, res) for b in bs]
        if len({o for _, o in res}) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
        print(f'  {"FAIL" if bad else "ok  "} {c["id"]} [{c["line"]}] {c["what"]}', flush=True)
        for b in bad:
            print(f'       {b}', flush=True)
    n = len(doc['cases'])
    print(f'DESKS COURT {n - len(failed)} of {n} cases on ' + ' and '.join(label for label, _ in builds)
          + (f'; FAILED: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
