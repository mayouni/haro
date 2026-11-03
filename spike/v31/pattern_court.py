"""The pattern court of Haro v0.31 (step 2 of COMPASS-REBOL-06/07), standalone: born here, relayed into haro_forge.py as stage 36.

Judges pattern_lib.haro (the pattern engine, run by pattern.haro) on the Haro VM AND on its checked build, the two printing the same
bytes (D41), and beside the Python reference (study/rebol/pattern.py), the two refusing a difference by name (D43):

  1. the reference holds: its own 53 fixtures, and the 95 of v31/fixtures.json;
  2. v31/fixtures.json (written first), every match fixture by its verdict, its values kept, and its step bound; every refusal fixture by
     the fragment of why; each on haro and on the checked build, and each line identical to the reference's -- verdict, kept values, steps,
     bound, and the words of a refusal. The steps are the reference's to the step: a packrat counted the same way;
  3. the whole spike, FAM1: the declaration form written once as a pattern, over every declaration and sentence, by the number that
     match and the six that do not, named; the verdict and the steps of each text identical to the reference's.

  python spike/v31/pattern_court.py [--plant]      --plant flips one verdict, to prove the court can fail
"""
import json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'study', 'rebol'))
import paths
import pattern as reference                       # the Python model; imports block.py beside it
sys.path.insert(0, os.path.join(ROOT, 'spike', 'v30'))
import block_court                                # the one family of texts, and the one list of the sentence extensions
from block import Refused

HARO_VM, TWIN = paths.need_bins()
FIXTURES = os.path.join(HERE, 'fixtures.json')
CWD = SPIKE                                       # where pattern.haro and pattern_lib.haro are run from; plants.py points it at a planted copy
PLANT = '--plant' in sys.argv


def run(exe, args, cwd=None):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=900, cwd=cwd or CWD)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def case_text(cid, rules, sets, start, inp=None, file=None):
    """One case of the line protocol pattern.haro reads."""
    lines = [f'case {cid}']
    for name, text in rules.items():
        assert '\n' not in text and ' ' not in name
        lines.append(f'rule {name} {text}')
    for name, members in (sets or {}).items():
        assert all(m and ' ' not in m for m in members)
        lines.append(('set ' + name + ' ' + ' '.join(members)).rstrip())
    lines.append(f'start {start}')
    if file is not None:
        lines.append(f'file {file}')
    elif inp is not None:
        assert '\n' not in inp
        lines.append(f'input {inp}')
    return '\n'.join(lines) + '\n'


def reference_line(cid, rules, sets, start, inp=None, text=None):
    """The line the reference prints for a case, in pattern.haro's format."""
    try:
        if inp is None and text is None:
            reference.declare(rules, sets or {})
            return f'{cid} declared'
        whole, kept, steps, bound = reference.run(rules, sets or {}, start, text if text is not None else inp)
        return f'{cid} match {1 if whole else 0} steps {steps} bound {bound} kept ' + '\t'.join(kept)
    except Refused as e:
        return f'{cid} refused {e}'


def haro_lines(cases_file, builds):
    outs = {}
    for label, exe in builds:
        outs[label] = run(exe, ['pattern.haro', 'cases', cases_file])
    return outs


def judge_reference():
    failures = 0
    for label, path in (('its own 53 (study/rebol/pattern_fixtures.json)', os.path.join(ROOT, 'study', 'rebol', 'pattern_fixtures.json')),
                        ('the fixtures of v31/fixtures.json', None)):
        if path is None:
            doc = json.load(open(FIXTURES, encoding='utf-8'))
            tmp = os.path.join(tempfile.gettempdir(), 'haro_v31_ref.json')
            json.dump({'matches': doc['matches'], 'refusals': doc['refusals']}, open(tmp, 'w', encoding='utf-8'))
            path = tmp
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            bad = reference.court(path)
        last = buf.getvalue().strip().splitlines()[-1]
        ok = not bad
        print(('  ok   ' if ok else '  FAIL ') + f'the reference holds {label}: ' + last)
        failures += 0 if ok else 1
    return failures


def judge_fixtures(builds=(('haro', None), ('checked', None)), quiet=False):
    """Returns (failures, the ids that failed). builds: the (label, exe) pairs; None takes the VM and its checked build."""
    builds = [(l, e or (HARO_VM if l == 'haro' else TWIN)) for l, e in builds]
    say = (lambda *a: None) if quiet else print
    doc = json.load(open(FIXTURES, encoding='utf-8'))
    cases, expect = [], []
    for f in doc['matches']:
        cases.append(case_text(f['id'], f['rules'], f.get('sets'), f['start'], inp=f['input']))
        expect.append(('match', f, reference_line(f['id'], f['rules'], f.get('sets'), f['start'], inp=f['input'])))
    for f in doc['refusals']:
        cases.append(case_text(f['id'], f['rules'], f.get('sets'), f['start']))
        expect.append(('refusal', f, reference_line(f['id'], f['rules'], f.get('sets'), f['start'])))
    failures, failed_ids = 0, []
    with tempfile.TemporaryDirectory() as td:
        cf = os.path.join(td, 'cases.txt')
        with open(cf, 'w', encoding='utf-8', newline='') as fh:
            fh.write(''.join(cases))
        t0 = time.perf_counter()
        outs = haro_lines(cf, builds)
        dt = time.perf_counter() - t0
    lines = {label: o.split('\n') for label, o in outs.items()}
    first = builds[0][0]
    ok_n = 0
    diff = []
    worst = 0.0
    for n, (kind, f, ref) in enumerate(expect):
        got = lines[first][n] if n < len(lines[first]) else 'NO OUTPUT'
        if any((lines[l][n] if n < len(lines[l]) else None) != got for l, _ in builds):
            diff.append(f['id'])
        ok, why = True, ''
        if got != ref:                                   # D43: a difference from the reference is refused by name
            ok, why = False, f'differs from the reference: haro `{got[:150]}` reference `{ref[:150]}`'
        elif kind == 'match':
            parts = got.split(' ')
            e = f['expect']
            whole = got.startswith(f['id'] + ' match 1')
            kept = got.split(' kept ', 1)[1].split('\t') if ' kept ' in got and got.split(' kept ', 1)[1] else []
            steps, bound = int(parts[4]), int(parts[6]) if parts[2] in ('0', '1') else (0, 0)
            if not got.startswith(f['id'] + ' match'):
                ok, why = False, got[:160]
            elif whole != e['match']:
                ok, why = False, f'match {whole}, expected {e["match"]}'
            elif 'kept' in e and kept != e['kept']:
                ok, why = False, f'kept {kept}, expected {e["kept"]}'
            elif steps > bound:
                ok, why = False, f'{steps} steps over the bound {bound}'
            else:
                worst = max(worst, steps / bound)
        else:
            if not (got.startswith(f['id'] + ' refused ') and f['refusal'] in got):
                ok, why = False, ('declared, must be refused' if got.endswith('declared') else f'refused for another reason: {got[:160]}')
        if PLANT and f['id'] == 'P01':
            ok, why = False, 'PLANTED'
        if ok:
            ok_n += 1
            say(f'  ok   {f["id"]}: {f["name"][:105]}')
        else:
            failures += 1
            failed_ids.append(f['id'])
            say(f'  FAIL {f["id"]}: {f["name"][:80]} -- {why}')
    say(f'PATTERN COURT (haro): {ok_n} of {len(expect)} fixtures hold, each the reference\'s own line to the step; the most a match spent was {worst:.0%} of its step bound; {dt:.2f} s per build for all')
    if len(builds) > 1:
        if diff:
            failures += 1
            say(f'  FAIL haro and its checked build differ on {diff}')
        else:
            say(f'  ok   haro and its checked build print the same bytes on all {len(expect)} cases')
    return failures, failed_ids


def family_files():
    """Every declaration and every sentence of the spike: v30/block_court.py's family, the one copy."""
    return block_court.family()


def same_reader_refusal(got, ref):
    """A text neither reader can read is refused by the READER, whose wording is step 1's to judge (v30/block_court.py): Haro's reads
    `block (line 3): ...`, the reference's `line 3: ...`. Two refusals at the same line of the same text agree here; any other difference does not."""
    import re
    a = re.match(r'(\S+) refused block \(line (\d+)\): ', got)
    b = re.match(r'(\S+) refused line (\d+): ', ref)
    return bool(a and b and a.groups() == b.groups())


def judge_family():
    doc = json.load(open(FIXTURES, encoding='utf-8'))['family']
    files = family_files()
    failures = 0
    cases = ''.join(case_text(p, doc['rules'], None, doc['start'], file=p) for p in files)
    # the case id is the path: no spaces in the spike's paths
    assert all(' ' not in p for p in files)
    with tempfile.TemporaryDirectory() as td:
        cf = os.path.join(td, 'family.txt')
        with open(cf, 'w', encoding='utf-8', newline='') as fh:
            fh.write(cases)
        t0 = time.perf_counter()
        outs = haro_lines(cf, (('haro', HARO_VM), ('checked', TWIN)))
        dt = time.perf_counter() - t0
    if outs['haro'] != outs['checked']:
        failures += 1
        print('  FAIL haro and its checked build differ on the family')
    else:
        print('  ok   haro and its checked build print the same bytes on the family')
    lines = outs['haro'].split('\n')
    matched, unmatched, steps_total, diffs = 0, {}, 0, []
    for p, got in zip(files, [l for l in lines if l]):
        text = open(os.path.join(SPIKE, p), encoding='utf-8').read()
        ref = reference_line(p, doc['rules'], None, doc['start'], text=text)
        if got != ref and not same_reader_refusal(got, ref):
            diffs.append((p, got[:100], ref[:100]))
        if ' match 1 ' in got:
            matched += 1
        else:
            unmatched[p] = got.split(' ', 1)[1][:60]
        if ' steps ' in got:
            steps_total += int(got.split(' steps ')[1].split(' ')[0])
    for p, g, r in diffs[:5]:
        failures += 1
        print(f'  FAIL {p} differs from the reference: haro `{g}` reference `{r}`')
    if len([l for l in lines if l]) != len(files):
        failures += 1
        print(f'  FAIL {len([l for l in lines if l])} verdicts for {len(files)} texts')
    want = set(doc['unmatched'])
    if set(unmatched) != want:
        failures += 1
        print(f'  FAIL the texts that do not match are {sorted(unmatched)}, expected {sorted(want)}')
    if matched != doc['matching'] or len(files) != doc['texts']:
        failures += 1
        print(f'  FAIL {matched} of {len(files)} match, expected {doc["matching"]} of {doc["texts"]}')
    if PLANT:
        failures += 1
        print('  FAIL the family -- PLANTED')
    print(f'FAMILY {doc["id"]}: {matched} of {len(files)} texts match the declaration form, {steps_total:,} steps, {dt:.2f} s per build; '
          f'the {len(unmatched)} that do not are the ones written to lack something: ' + ', '.join(sorted(unmatched)))
    return failures


def court():
    print('pattern court -- Haro v0.31: pattern_lib.haro judged by v31/fixtures.json and the whole spike, on haro and its checked build, beside the reference')
    failures = judge_reference()
    failures += judge_fixtures()[0]
    failures += judge_family()
    return failures


if __name__ == '__main__':
    t0 = time.perf_counter()
    n = court()
    print(f'pattern_court: {"FAIL" if n else "PASS"} ({n} failure(s), {time.perf_counter() - t0:.1f} s)')
    sys.exit(1 if n else 0)
