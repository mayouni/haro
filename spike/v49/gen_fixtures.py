"""Haro v0.49 -- zip.zig retired: Softanza's engine carries ZIP. Written FIRST, before the VM is touched.

THE RULING. The author, 2026-11-08, of Haro carrying ziplib's natives: "why using "ziplib.ring" altogetjer! we have zip covered by the
engine!!" -- and on Ring++'s retirement, "only Haro will remain". stzlib's port moved stzZipFile onto the engine's stz_compress (stzlib
cb6f5de65, 2026-11-09: no zip_* call outside its guard's own assertions, verified by this desk with git grep); the twelve natives zip.zig
published into every Haro program have no caller left.

THE LINES:
  Z1  the twelve names are no longer the VM's: a call of one is what Ring answers with its zip extension not loaded -- R3, Calling
      Function without definition, naming it, catchable
  Z2  ZIP belongs to Softanza's engine (stz_compress: StzEngineZipNames, Read, Crc, Write, ExtractAll, LastError), judged by stzlib's own
      guard (stzZipFile_defects_narrated.ring) -- a gate this desk does not own, named here and not run by this court

v0.44's zip cases (Q10, Q11, Q12, Q14) and their six plants (Z17-Z22) retire with the code they judged; v44/gen_fixtures.py says so.

  python spike/v49/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
NAMES = ['zip_openfile', 'zip_entry_open', 'zip_entry_write', 'zip_entry_fwrite', 'zip_entry_read', 'zip_entry_fread', 'zip_entry_close',
         'zip_extract_allfiles', 'zip_close', 'zip_filescount', 'zip_getfilenamebyindex', 'zip_extract_file']

CASES = [
    ('R01', 'Z1', 'a zip_ call is Ring\'s R3 for a function nothing defines, uncaught at its line', '.ring', [
        '? "before"', 'oZip = zip_openfile("a.zip", "w")', '? "after"'],
     ['before', '', 'Line 2 Error (R3) : Calling Function without definition: zip_openfile ', 'in file R01.ring '], 1),
    # R02 called each name through eval() first, and held before the code: an eval does not reach a native published at start-up, so it
    # asked nothing. Each name is called directly.
    ('R02', 'Z1', 'each of the twelve names raises R3, caught', '.ring',
     [x for n in NAMES for x in ('try', T + n + '()', 'catch', T + '? cCatchError', 'done')],
     ['Error (R3) : Calling Function without definition: ' + n for n in NAMES]),
    ('R03', 'Z1', 'no archive is written: the R3 comes before the call runs', '.ring', [
        'try', T + 'zip_openfile("never.zip", "w")', 'catch', T + '? "refused"', 'done', '? fexists("never.zip")'],
     ['refused', '0']),
]

os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
out = []
for row in CASES:
    cid, line, why, ext, prog, want = row[:6]
    name = f'cases/{cid}{ext}'
    with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(prog) + '\n')
    case = {'id': cid, 'kind': 'run', 'line': line, 'why': why, 'file': name, 'stdout': '\n'.join(want) + '\n'}
    if len(row) > 6 and row[6]:
        case['stdout'] = '\n'.join(want)
        case['exit'] = row[6]
    out.append(case)
doc = {'rung': 'v0.49', 'decision': 'zip.zig retired; Softanza\'s engine carries ZIP (the author 2026-11-08; stzlib cb6f5de65)',
       'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build',
       'lines': {'Z1': 'a zip_ call is R3, as Ring without its extension', 'Z2': 'ZIP is the engine\'s, judged by stzlib\'s guard (not run here)'},
       'cases': out}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print(f'wrote {len(out)} cases')
