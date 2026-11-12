"""Haro v0.62 -- a boolean reaches a native as 1 or 0 (HARO-NATIVE-BOOL-01). Written FIRST, before the VM is touched.

THE FINDING. stzlib-haroport, 2026-11-12, from base/common on haro.exe 69d7e21 with Haro's engine build:
    StzEngineStringReplaceCS(xS, "mm", "30", 1)     -> "MM 30"
    StzEngineStringReplaceCS(xS, "mm", "30", true)  -> "30 30"
A .haro `true` given to an engine native arrived as nothing, and the native read its flag as 0: a case-sensitive replace ran
case-insensitive, and stzDateTime printed 10:03 for 10:30 -- 34 date assertions, no error. The natives read their flags as numbers.

THE READING (the desk's, D74, principle 4 and v0.53's mirror): where a value crosses to a native, a boolean is the number 1 or 0 -- as an
argument and as an item of a list the native reads. v0.53 made a native's 1 or 0 a boolean where a .haro file wants one; this is the way
out. A .ring file has no booleans and is untouched.

THE LINES:
  N1  a boolean argument reaches a native as 1 or 0: Shutdown(true) ends the program with code 1, Shutdown(false) with 0
  N2  the finding itself, on the engine: ReplaceCS with true is case-sensitive, with false is not
  N3  a boolean inside a list reaches a native as 1 or 0
  N4  a .ring file untouched

The engine cases (kind `engine`) load Softanza's engine from STZ_ENGINE_DIR; the court names them NOT RUN when it is unset.

  python spike/v62/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'


def engine(dll):
    return [f'LoadLib(SysGet("STZ_ENGINE_DIR") + "/zig-out/bin/{dll}")']


CASES = [
    ('B01', 'N1', 'Shutdown(true) ends the program with code 1', 'run', ['print "before"', 'Shutdown(true)', 'print "after"'],
     'before\n', 1),
    ('B02', 'N1', 'Shutdown(false) ends the program with code 0', 'run', ['print "before"', 'Shutdown(false)', 'print "after"'],
     'before\n', 0),
    ('B03', 'N1', 'a b name given to a native is its 1 or 0', 'run', ['bFail = true', 'print "before"', 'Shutdown(bFail)'],
     'before\n', 1),
    ('B04', 'N2', 'the finding: ReplaceCS with true is case-sensitive, with false is not', 'engine', engine('stz_string.dll') + [
        'xS = StzEngineString("MM mm")', 'StzEngineStringReplaceCS(xS, "mm", "30", true)', 'print StzEngineStringData(xS)',
        'xT = StzEngineString("MM mm")', 'StzEngineStringReplaceCS(xT, "mm", "30", false)', 'print StzEngineStringData(xT)'],
     'MM 30\n30 30\n', 0),
    ('B05', 'N3', 'a boolean inside a list reaches a native as 1 or 0', 'engine', engine('stz_geo.dll') + [
        'print StzEngineGeoRingContains([0, 0, true, 0, true, true, 0, true], 0.5f, 0.5f)',
        'print StzEngineGeoRingContains([0, 0, false, 0, false, false, 0, false], 0.5f, 0.5f)'],
     '1\n0\n', 0),
    ('B06', 'N4', 'a .ring file passes its numbers as it did', 'run', ['? "before"', 'shutdown(1)'],
     'before\n', 1),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for cid, line, why, kind, src, stdout, code in CASES:
        ext = '.ring' if cid == 'B06' else '.haro'
        name = f'cases/{cid}{ext}'
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(src) + '\n')
        row = {'id': cid, 'kind': kind, 'line': line, 'why': why, 'file': name, 'stdout': stdout}
        if code:
            row['exit'] = code
        out.append(row)
    doc = {
        'rung': 'v0.62',
        'decision': 'HARO-NATIVE-BOOL-01 (stzlib-haroport, 2026-11-12); the desk\'s readings are D74',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build; an engine case '
                 'only where STZ_ENGINE_DIR names Softanza\'s engine built for Haro',
        'lines': {'N1': 'a boolean argument is 1 or 0', 'N2': 'the finding on the engine', 'N3': 'a boolean list item is 1 or 0',
                  'N4': 'a .ring file untouched'},
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
