"""The printing court of Haro v0.30 (step 1 of COMPASS-REBOL-06), standalone: born here, relayed into haro_forge.py as stage 35.

Judges block.haro (the one reader of C6 and its canonical printer, block_lib.haro) on the Haro VM AND on its checked build,
the two printing the same bytes (D41):

  1. the reference still holds: study/rebol/block.py on its own 21 fixtures (the Python model BLOCKS.md was measured with);
  2. v30/fixtures.json (written first): each "same" pair reads to one block, each "differ" pair to two, each "canonical" text
     prints as given, each "refused" text is refused with the fragment named -- and the five memo-spelling fixtures it leaves
     to step 3 are printed by name, so what was skipped is said;
  3. the round trip over the family: every Haro declaration (paths.is_declaration over spike/**/*.haro) and every sentence of
     every letter (the census's extensions) reads, prints canonically and reads back to the same block -- one process per
     build for the whole family -- except the texts written to be refused, named below;
  4. the meta-court's `fmt` verb (haro.haro <file> fmt) prints what block.haro prints: one printer.

  python spike/v30/block_court.py [--plant]      --plant flips one verdict, to prove the court can fail
"""
import json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
import paths

HARO_VM, TWIN = paths.need_bins()
FIXTURES = os.path.join(HERE, 'fixtures.json')
REFERENCE = os.path.join(ROOT, 'study', 'rebol', 'block.py')
SENTENCE_EXT = ('.z', '.f', '.a', '.n', '.stzv', '.machine', '.fleet', '.ledger', '.bank', '.clinic', '.notice', '.grant', '.w')
# the texts of the family written to be refused: a reader that reads them is wrong
REFUSED_BY_DESIGN = {'f/operator-in-guard.f'}
PLANT = '--plant' in sys.argv


CWD = SPIKE                                    # where block.haro and block_lib.haro are run from; plants.py points it at a planted copy


def run(exe, args, cwd=None):
    cwd = cwd or CWD
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=600, cwd=cwd)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def write(folder, name, text):
    p = os.path.join(folder, name)
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)
    return p


def reference():
    p = subprocess.run([sys.executable, '-I', REFERENCE], capture_output=True, timeout=600)
    out = p.stdout.decode('utf-8', 'replace')
    last = out.strip().splitlines()[-1] if out.strip() else 'NO OUTPUT'
    ok = p.returncode == 0 and last.startswith('PRINTING COURT: 21 of 21')
    print(('  ok   ' if ok else '  FAIL ') + 'the reference, study/rebol/block.py: ' + last)
    return 0 if ok else 1


def fixtures(builds=(('haro', None), ('checked', None)), quiet=False):
    """Returns (failures, the ids that failed). builds: the (label, exe) pairs to judge on; None takes the VM and its checked build."""
    builds = [(l, e or (HARO_VM if l == 'haro' else TWIN)) for l, e in builds]
    doc = json.load(open(FIXTURES, encoding='utf-8'))
    assert doc['grammar'] == 'haro' and doc['version'] == '0.30'
    failures = 0
    passed = total = 0
    diff = []
    failed_ids = []
    say = (lambda *a: None) if quiet else print
    with tempfile.TemporaryDirectory() as td:
        for section in ('same', 'differ', 'canonical', 'refused'):
            for f in doc[section]:
                total += 1
                if section in ('same', 'differ'):
                    a = write(td, f['id'] + '.a', f['a'])
                    b = write(td, f['id'] + '.b', f['b'])
                    args = ['block.haro', 'same', a, b]
                else:
                    t = write(td, f['id'] + '.txt', f['text'])
                    args = ['block.haro', 'fmt' if section == 'canonical' else 'load', t]
                outs = {label: run(exe, args) for label, exe in builds}
                if len(set(outs.values())) > 1:
                    diff.append(f['id'])
                out = outs[builds[0][0]]
                if section == 'same':
                    ok, why = out == 'same\n', out.strip()[:200]
                elif section == 'differ':
                    ok, why = out == 'differ\n', out.strip()[:200]
                elif section == 'canonical':
                    ok, why = out == f['canonical'], repr(out)[:300]
                else:
                    first = out.split('\n')[0]
                    ok = first.startswith('block (line') and f['why'] in first
                    why = ('accepted, must refuse: ' if not first.startswith('block (line') else 'refused for another reason: ') + first[:200]
                if PLANT and f['id'] == 'K04':
                    ok, why = False, 'PLANTED'
                if ok:
                    passed += 1
                    say(f'  ok   {f["id"]}: {f["name"][:110]}')
                else:
                    failures += 1
                    failed_ids.append(f['id'])
                    say(f'  FAIL {f["id"]}: {f["name"][:90]} -- {why}')
    say(f'PRINTING COURT (haro): {passed} of {total} fixtures hold')
    if len(builds) > 1:
        if diff:
            failures += 1
            say(f'  FAIL haro and its checked build differ on {diff}')
        else:
            say(f'  ok   haro and its checked build print the same bytes on all {total} fixtures')
    for f in doc.get('left_to_step_3', []):
        say(f'  SKIPPED {f["id"]} ({f["section"]}): {f["why"]}')
    return failures, failed_ids


def family():
    """Every declaration and every sentence of the spike, relative to spike/ with forward slashes."""
    out = []
    for dirpath, dirs, files in os.walk(SPIKE):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', 'scratch')]
        for fn in files:
            p = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1]
            if fn.startswith('zz_'):
                continue                       # stage 18's mutation scratch (zz_mut.haro): written and removed by the guard, never a text of the family
            if (ext == '.haro' and paths.is_declaration(p)) or ext in SENTENCE_EXT:
                out.append(os.path.relpath(p, SPIKE).replace(os.sep, '/'))
    return sorted(out)


def roundtrip():
    files = family()
    decls = [f for f in files if f.endswith('.haro')]
    outs = {}
    for label, exe in (('haro', HARO_VM), ('checked', TWIN)):
        t0 = time.perf_counter()
        outs[label] = run(exe, ['block.haro', 'roundtrip'] + files)
        outs[label + '_t'] = time.perf_counter() - t0
    failures = 0
    lines = [l for l in outs['haro'].split('\n') if l]
    ok_n = bytes_in = bytes_out = 0
    for l in lines:
        kind, _, rest = l.partition(' ')
        name = rest.split(':')[0].split(' ')[0]
        if kind == 'ok':
            ok_n += 1
            parts = rest.split(' ')
            bytes_in += int(parts[2]); bytes_out += int(parts[3])
            if name in REFUSED_BY_DESIGN:
                failures += 1
                print(f'  FAIL {name} was written to be refused and the reader read it')
        elif kind == 'refused' and name in REFUSED_BY_DESIGN:
            print(f'  ok   refused by design: {l[:160]}')
        else:
            failures += 1
            print(f'  FAIL {l[:200]}')
    if len(lines) != len(files):
        failures += 1
        print(f'  FAIL {len(lines)} verdicts for {len(files)} files')
    if PLANT:
        failures += 1
        print('  FAIL the round trip -- PLANTED')
    print(f'ROUND TRIP: {ok_n} of {len(files)} texts read, print canonically and read back to the same block '
          f'({len(decls)} declarations, {len(files) - len(decls)} sentences; {bytes_in:,} bytes written, {bytes_out:,} printed, '
          f'{(bytes_out - bytes_in) * 100.0 / max(bytes_in, 1):+.1f}%); haro {outs["haro_t"]:.2f} s, checked {outs["checked_t"]:.2f} s')
    if outs['haro'] != outs['checked']:
        failures += 1
        print('  FAIL haro and its checked build differ on the round trip')
    else:
        print('  ok   haro and its checked build print the same bytes on the round trip')
    return failures


def meta_fmt(decl='machine_v03.haro'):
    """One printer: the meta-court's fmt verb and block.haro print the same canonical text."""
    a = run(HARO_VM, ['haro.haro', decl, 'fmt'])
    b = run(HARO_VM, ['block.haro', 'fmt', decl])
    c = run(TWIN, ['haro.haro', decl, 'fmt'])
    ok = a == b == c and 'DEFINE LANGUAGE' in a and not a.startswith('block (line')
    print(('  ok   ' if ok else '  FAIL ') + f'haro.haro {decl} fmt prints what block.haro fmt prints, on both builds ({len(a)} bytes)'
          + ('' if ok else f' -- meta: {a[:120]!r} block: {b[:120]!r}'))
    return 0 if ok else 1


def court():
    print('printing court -- Haro v0.30: block_lib.haro judged by v30/fixtures.json and the family round trip, on haro and its checked build')
    failures = reference()
    failures += fixtures()[0]
    failures += roundtrip()
    failures += meta_fmt()
    return failures


if __name__ == '__main__':
    t0 = time.perf_counter()
    n = court()
    print(f'block_court: {"FAIL" if n else "PASS"} ({n} failure(s), {time.perf_counter() - t0:.1f} s)')
    sys.exit(1 if n else 0)
