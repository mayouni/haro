"""Haro v0.72, the language of doors and the place (doc/DOORS.md rung 1, D88): every case of v72/fixtures.json on haro and on its checked build.
A case passes when, on both builds:

  the run     prints the fixture's bytes and exits 0; or prints the line the fixture names and never the one it forbids; or is refused
              by the compiler at the fixture's line, for its reason
  the check   (where the case has one) counts the fixture's errors and lists its error findings, line and rule, for the case's file
  THE LAW     for each text the case judges, the language's own court -- forged from the same declaration by the build under test and
              run standing alone, as `haro <language>_court.haro diagnose <file>` -- answers the fixture's verdict: no finding, or the
              fixture's code and message first. So what a program's `Judge` is held to is what the standalone court says
  the image   (J14) with the compiled image kept, a second run answers the same; a declaration edited between runs is forged again
  D41         the two builds print the same bytes, run and check

  python spike/v72/place_court.py                 haro and the checked build, as paths.py finds them
  python spike/v72/place_court.py    --vm X.exe   one build only (the plants)
  python spike/v72/place_court.py    --plant      the guard's own plant: one fixture's expected bytes doctored, so the court must fail
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(SPIKE)
sys.path.insert(0, ROOT)
PLANT = '--plant' in sys.argv
VM = os.path.abspath(sys.argv[sys.argv.index('--vm') + 1]) if '--vm' in sys.argv else None
sys.argv = [sys.argv[0]]
import paths

FINDING = re.compile(r'^  (\d+):(\d+)  (\w+)\s+(haro/\S+)$')
COUNTS = re.compile(r'^  (\d+) error, ')
LAW_DIR = os.path.join(ROOT, 'runtime', 'v72', 'law')


def sh(exe, args, cwd):
    env = dict(os.environ)
    env['HARO_NOCACHE'] = '1'
    env['HARO_HOME'] = SPIKE     # the forge's folder, for a build that does not stand in the repository's vm/
    try:
        r = subprocess.run([exe] + args, capture_output=True, env=env, timeout=120, cwd=cwd)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', -1
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n'), r.returncode


def read_check(out, name):
    """the error findings in order -- [row, rule] in the case's own file, [file, row, rule] in another -- and the error count"""
    found, file, errors = [], '', None
    for ln in out.split('\n'):
        m = FINDING.match(ln)
        if m:
            if m.group(3) == 'error':
                own = os.path.basename(file) == name
                found.append([int(m.group(1)), m.group(4)] if own else [os.path.basename(file), int(m.group(1)), m.group(4)])
            continue
        m = COUNTS.match(ln)
        if m:
            errors = int(m.group(1))
            continue
        if ln and not ln.startswith(' '):
            file = ln.strip()
    return found, errors


_forged = {}


def standalone(exe, label, lang, text):
    """the language's own court, forged by this build and run alone on the text: (code, message) of its first error, or (None, '')"""
    out_dir = os.path.join(LAW_DIR, label)
    os.makedirs(out_dir, exist_ok=True)
    rel = os.path.relpath(out_dir, SPIKE).replace('\\', '/')
    if (label, lang) not in _forged:
        said, _ = sh(exe, ['forge.haro', os.path.join(SPIKE, lang + '.haro'), rel], SPIKE)
        _forged[(label, lang)] = said.strip().startswith('forged ' + lang)
    if not _forged[(label, lang)]:
        return 'NOT FORGED', ''
    path = os.path.join(out_dir, 'text.' + lang)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text + '\n')
    raw, _ = sh(exe, [rel + '/' + lang + '_court.haro', 'diagnose', rel + '/text.' + lang], SPIKE)
    try:
        ds = [d for d in json.loads(raw)['diagnostics'] if d['severity'] == 'error']
    except (ValueError, KeyError):
        return 'NO JSON', raw.strip()[:120]
    return (ds[0]['code'], ds[0]['message']) if ds else (None, '')


def kept(c, exe):
    """L12: the case and its declaration in a folder of their own, the image cache on and in that folder: two runs print the first
    answer and write an image; the declaration edited, two more print the second"""
    import shutil, tempfile
    k, bad, said = c['kept'], [], ''
    name = os.path.basename(c['file'])
    with tempfile.TemporaryDirectory() as td:
        for f in [name] + k['beside']:
            shutil.copyfile(os.path.join(HERE, 'cases', f), os.path.join(td, f))
        env = dict(os.environ)
        env.pop('HARO_NOCACHE', None)
        env['HARO_HOME'] = SPIKE
        env['HARO_CACHE'] = os.path.join(td, 'cache', 'images')

        def go():
            r = subprocess.run([exe, name], capture_output=True, env=env, timeout=120, cwd=td)
            return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
        for n, want in ((1, k['first']), (2, k['first'])):
            out = go()
            said += out
            if out != want:
                bad.append(f'run {n} prints {out[:200]!r}, not {want!r}')
        images = sum(len(fs) for d, _, fs in os.walk(os.path.join(td, 'cache', 'images')))
        if not images:
            bad.append('no image was kept')
        f, old, new = k['edit']
        text = open(os.path.join(td, f), encoding='utf-8').read()
        if text.count(old) != 1:
            bad.append(f'the edit finds {text.count(old)} of {old!r}')
        with open(os.path.join(td, f), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text.replace(old, new))
        for n, want in ((3, k['then']), (4, k['then'])):
            out = go()
            said += out
            if out != want:
                bad.append(f'run {n}, after the edit, prints {out[:200]!r}, not {want!r}')
    return bad, said


def with_link(c, label, exe):
    """L8: `way_out`, beneath cases/data, leads to cases/ itself -- a junction on Windows, a symbolic link elsewhere -- for the one
    case that asks, and is taken away after"""
    link = os.path.join(HERE, 'cases', 'data', 'way_out')
    target = os.path.join(HERE, 'cases')
    if os.path.lexists(link):
        os.rmdir(link) if os.name == 'nt' else os.remove(link)
    if os.name == 'nt':
        import _winapi
        _winapi.CreateJunction(target, link)
    else:
        os.symlink(target, link)
    try:
        return judge(dict((k, v) for k, v in c.items() if k != 'setup'), label, exe)
    finally:
        os.rmdir(link) if os.name == 'nt' else os.remove(link)


def judge(c, label, exe):
    if c.get('setup') == 'link':
        return with_link(c, label, exe)
    if 'kept' in c:
        return kept(c, exe)
    bad = []
    cwd = os.path.join(HERE, os.path.dirname(c['file']))
    name = os.path.basename(c['file'])
    out, rc = sh(exe, [name], cwd)
    r = c['run']
    if 'stdout' in r:
        if out != r['stdout'] or rc != 0:
            bad.append(f'the run prints {out[:300]!r} (exit {rc}), not {r["stdout"]!r}')
    elif 'refuses' in r:
        row, reason, written = r['refuses']
        text = f'({reason} `{written}`, line {row} of {name})'
        if text not in out:
            bad.append(f'the run does not refuse with {text!r}: {out.strip()[:240]!r}')
    else:
        if r['raises'] not in out:
            bad.append(f'the run does not print {r["raises"]!r}: {out.strip()[:240]!r}')
    if 'also' in r and r['also'] not in out:
        bad.append(f'the run does not print {r["also"]!r}: {out.strip()[:300]!r}')
    if 'never' in r and r['never'] + '\n' in out:
        bad.append(f'the run prints {r["never"]!r}')
    chk = ''
    if 'check' in c:
        chk, _ = sh(exe, ['check', name], cwd)
        found, errors = read_check(chk, name)
        if errors != c['check']['errors']:
            bad.append(f'check counts {errors} error(s), not {c["check"]["errors"]}')
        if found != c['check']['found']:
            bad.append(f'check finds {found}, not {c["check"]["found"]}')
    for lang, text, code, message in c.get('judged', []):
        got = standalone(exe, label, lang, text)
        if got != (code, message):
            bad.append(f'THE LAW: the court of {lang}, alone, answers {got} on {text!r}; the fixture says {(code, message)}')
    return bad, out + '\x00' + chk


def main():
    doc = json.load(open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8'))
    if VM:
        builds = [('vm', VM)]
    else:
        vm, twin = paths.need_bins()
        builds = [('haro', vm), ('checked', twin)]
    failed = []
    for c in doc['cases']:
        if PLANT and c['id'] == 'D01':
            c = json.loads(json.dumps(c))
            c['run']['stdout'] += 'doctored\n'
        res = [judge(c, label, exe) for label, exe in builds]
        bad = [f'{label}: {b}' for (label, _), (bs, _) in zip(builds, res) for b in bs]
        if len({o for _, o in res}) > 1:
            bad.append('the builds differ')
        if bad:
            failed.append(c['id'])
        print(f'  {"FAIL" if bad else "ok  "} {c["id"]} [{c["line"]}] {c["what"]}')
        for b in bad:
            print(f'       {b}')
    n = len(doc['cases'])
    print(f'PLACE COURT {n - len(failed)} of {n} cases on ' + ' and '.join(label for label, _ in builds)
          + (f'; FAILED: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
