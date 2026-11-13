"""Haro v0.69, `haro check` names what the run refuses (HARO-CHECKRUN-01): every case of v69/fixtures.json on haro and on its checked
build. For each case the court runs the file, checks it, and where the case says so reads `check --facts`. A case passes when, on both
builds:

  the run     refuses at the fixture's file, line and words; or prints the fixture's bytes; or raises what the fixture names
  the check   counts the fixture's errors, lists its error findings in order (file, line, rule), gives each refused form the run's
              own words, and reads the unit as a library only where the fixture says so
  THE LAW     where the run refuses, check holds a haro/refused-form finding at the line and in the words the run itself PRINTED --
              read off the run's output, not off the fixture
  the facts   hold the fixture's findings at the file's top and in each function, with its lines
  D41         the two builds print the same bytes, run and check

  python spike/v69/checkrun_court.py              haro and the checked build, as paths.py finds them
  python spike/v69/checkrun_court.py --vm X.exe   one build only (the plants)
  python spike/v69/checkrun_court.py --plant      the guard's own plant: one fixture's line doctored, so the court must fail
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths

REFUSED = re.compile(r'Haro refused this statement \((.*), line (\d+) of ([^)\s]+)\)')
FINDING = re.compile(r'^  (\d+):(\d+)  (\w+)\s+(haro/\S+)$')
COUNTS = re.compile(r'^  (\d+) error, (\d+) warn, (\d+) perf, (\d+) note')


def sh(exe, args, cwd):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    try:
        r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=60, cwd=cwd)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', -1
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def read_check(out):
    """the check's own account: its findings in order [file, row, severity, rule, message], its error count, and whether it read the
    unit as a library"""
    found, file, errors, lines = [], '', None, out.split('\n')
    for i, ln in enumerate(lines):
        m = FINDING.match(ln)
        if m:
            found.append([os.path.basename(file), int(m.group(1)), m.group(3), m.group(4), lines[i + 1].strip() if i + 1 < len(lines) else ''])
            continue
        m = COUNTS.match(ln)
        if m:
            errors = int(m.group(1))
            continue
        if ln and not ln.startswith(' '):
            file = ln.strip()
    return found, errors, 'nothing in this unit runs' in out


def judge(c, exe):
    """one case on one build: the list of what is wrong (empty when it passes), and the bytes the builds must share"""
    bad = []
    cwd = os.path.join(HERE, os.path.dirname(c['file']))
    name = os.path.basename(c['file'])
    run_out, run_rc = sh(exe, [name], cwd)
    chk_out, _ = sh(exe, ['check', name], cwd)
    found, errors, library = read_check(chk_out)
    want = c['check']
    errs = [f for f in found if f[2] == 'error']

    # the run
    r = c['run']
    said = REFUSED.search(run_out)
    if 'refuses' in r:
        f, row, reason, written = r['refuses']
        text = f'({reason} `{written}`, line {row} of {f})'
        if text not in run_out:
            bad.append(f'the run does not refuse with {text!r}: {run_out.strip()[:200]!r}')
    elif 'stdout' in r:
        if run_out != r['stdout'] or run_rc != 0:
            bad.append(f'the run prints {run_out!r} (exit {run_rc}), not {r["stdout"]!r}')
    else:
        if r['raises'] not in run_out:
            bad.append(f'the run does not raise {r["raises"]!r}: {run_out.strip()[:200]!r}')

    # the check
    if errors != want['errors']:
        bad.append(f'check counts {errors} error(s), not {want["errors"]}')
    got = [[f[0], f[1], f[3]] for f in errs]
    if got != want['found']:
        bad.append(f'check finds {got}, not {want["found"]}')
    for f, row, reason, written in want['refused']:
        msg = f'{reason} `{written}`'
        if not any(e[0] == f and e[1] == row and e[3] == 'haro/refused-form' and e[4] == msg for e in errs):
            bad.append(f'check has no refused form {msg!r} at {f}:{row}')
    if library != want['library']:
        bad.append('check reads the unit as a library' if library else 'check does not read the unit as a library')

    # THE LAW: what the run printed, check holds
    if said:
        words, row, f = said.group(1), int(said.group(2)), said.group(3)
        if not any(e[0] == f and e[1] == row and e[3] == 'haro/refused-form' and e[4] == words for e in errs):
            bad.append(f'THE LAW: the run refuses {words!r} at {f}:{row} and check does not say so')

    # the facts
    if 'facts' in c:
        raw, _ = sh(exe, ['check', name, '--facts'], cwd)
        try:
            doc = json.loads(raw)
        except ValueError:
            doc = None
            bad.append('the facts are no JSON')
        if doc:
            top = [[x['rule'], x['line']] for x in doc['files'][0]['top_findings']]
            if top != c['facts']['top']:
                bad.append(f'the facts hold {top} at the top, not {c["facts"]["top"]}')
            for fn, w in c['facts']['functions'].items():
                g = next((x for x in doc['functions'] if x['name'] == fn), None)
                if g is None:
                    bad.append(f'the facts have no function {fn}')
                    continue
                have = {'line': g['line'], 'end_line': g['end_line'], 'compiled': g['compiled'],
                        'findings': [[x['rule'], x['line']] for x in g['findings']]}
                if 'impure' in w:
                    have['impure'] = g.get('impure')
                if have != w:
                    bad.append(f'the facts say {have} of {fn}, not {w}')
    return bad, run_out + '\x00' + chk_out


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        if PLANT and c['id'] == 'S01':
            c = json.loads(json.dumps(c))
            c['check']['found'][0][1] += 1
        res = [judge(c, exe) for _, exe in builds]
        bad = [f'{label}: {b}' for (label, _), (bs, _) in zip(builds, res) for b in bs]
        if len({o for _, o in res}) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
        print(f'  {"FAIL" if bad else "ok  "} {c["id"]} [{c["line"]}] {c["what"]}')
        for b in bad:
            print(f'       {b}')
    n = len(doc['cases'])
    print(f'CHECKRUN COURT {n - len(failed)} of {n} cases on ' + ' and '.join(label for label, _ in builds)
          + (f'; FAILED: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
