"""Haro v0.51 -- `haro check --facts`: what the checker and the compiler establish, per function, as one JSON record a recorder can keep.
Written FIRST, before the VM is touched.

THE ASK. HARO-PROOF-01 (a), from stzlib-testoor (2026-11-08 18:51), on the Principal's word: "can Haro's graph or `haro check` export,
per function, what the checker already establishes ... with the checker's version and the source hash? Testoor needs nothing else to
begin recording grade 5". This desk answered (2026-11-09 10:56) with the record's shape and placed it as HARO-FACTS-01: a field for a
fact not built is ABSENT, never false (`total`, `uses`, profiles are D55 T7 and D56, not built).

THE RECORD (format "haro-check-facts/1"), one JSON document on stdout, the same bytes on haro and its checked build:
  checker      {"name": "haro", "commit": the last commit that touched vm/, "+uncommitted" after it when vm/ held changes at the build}
  files        [{"path", "sha256" of the bytes read, "surface": "haro" | "ring", "top_findings": the findings outside every function}]
  not_checked  [{"rules": [...], "why": ...}]: the rules that did not look, as `haro check` says in words
  impurity     the analysis in one sentence: direct only, calls not followed
  functions    [{"file": index into files, "name", "class": name or null, "line", "end_line",
                 "findings": [{"rule", "severity", "line", "col", "message"}],
                 "impure": {"why", "line"} -- ABSENT when the analysis saw nothing,
                 "calls_static", "calls_dynamic", "calls_late" (resolved by name when the program runs: a native, or nothing),
                 "compiled": the compiler finished this function's own body,
                 "refused": {"why", "line"} -- present only when it did not,
                 "reaches_uncompiled": a function it calls was not finished}]

THE LINES:
  P1  the record exists, is JSON, names its format, its checker's commit and every file's sha256 and surface; the flag goes before or
      after the file
  P2  every function and method of the unit, its lines, the checker's findings inside it, and those outside every function per file
  P3  its calls: bound by the compiler (a lambda's are its function's), dispatched by name, resolved when the program runs
  P4  its direct impurity, the first one met, with its line; absent when none is seen
  P5  whether the compiler finished it, why not and where; whether it reaches a function that was not finished
  P6  the rules that did not look, and why

  python spike/v51/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'

A_RING = ['f()', '', 'func f', T + 'x = g(1)', T + 'k = new K', T + 'k.m()', T + 'return x', '', 'func g n', T + 'see n', T + 'return n', '',
          'func h', T + '$count = 1', T + 'return clock()', '', 'class K', T + 'func m', T + T + 'return nowhere(2)']

CASES = [
    dict(id='X01', line='P1', why='the record names its format, its checker and the file it read, by sha256 and surface',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("d['format']", 'haro-check-facts/1'),
             ("d['checker']['name']", 'haro'),
             ("d['checker']['commit']", '@COMMIT'),
             ("len(d['files'])", 1),
             ("d['files'][0]['path'].endswith('a.ring')", True),
             ("d['files'][0]['sha256']", '@SHA:a.ring'),
             ("d['files'][0]['surface']", 'ring'),
         ]),
    dict(id='X02', line='P1', why='`haro check --facts <file>` is the same record, byte for byte, as `haro check <file> --facts`',
         files={'a.ring': A_RING}, run='a.ring', flag_first=True, same_as_flag_last=True, asserts=[("d['format']", 'haro-check-facts/1')]),
    dict(id='X03', line='P2', why='every function and method, in file order, with its lines and its class',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("[(x['class'], x['name'], x['line'], x['end_line'], x['file']) for x in d['functions']]",
              [[None, 'f', 3, 7, 0], [None, 'g', 9, 11, 0], [None, 'h', 13, 15, 0], ['K', 'm', 18, 19, 0]]),
         ]),
    dict(id='X04', line='P2', why='a finding is its function\'s, at its line and column; a function without one has none',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("[(x['rule'], x['severity'], x['line'], x['col']) for x in fn(d, 'K.m')['findings']]", [['haro/undefined-function', 'error', 19, 10]]),
             ("'nowhere()' in fn(d, 'K.m')['findings'][0]['message']", True),
             ("fn(d, 'f')['findings']", []),
             ("d['files'][0]['top_findings']", []),
         ]),
    dict(id='X05', line='P2', why='a finding outside every function is its file\'s',
         files={'t.ring': ['? nowhere(1)', 'func f', T + 'return 1']}, run='t.ring', asserts=[
             ("[(x['rule'], x['line']) for x in d['files'][0]['top_findings']]", [['haro/undefined-function', 1]]),
             ("fn(d, 'f')['findings']", []),
         ]),
    dict(id='X06', line='P3', why='calls the compiler bound, and a call resolved only when the program runs',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("fn(d, 'f')['calls_static']", ['K.m', 'g']),
             ("fn(d, 'f')['calls_dynamic']", []),
             ("fn(d, 'f')['calls_late']", []),
             ("fn(d, 'K.m')['calls_late']", ['nowhere']),
             ("fn(d, 'h')['calls_static'] + fn(d, 'h')['calls_late']", []),
         ]),
    dict(id='X07', line='P3', why='a method called on a receiver the compiler cannot prove is dispatched by name; a lambda\'s calls are its function\'s',
         files={'l.ring': ['func f o', T + 'o.run()', T + 'q = func x { return g(x) }', T + 'return call q(1)', 'func g n', T + 'return n',
                           'class A', T + 'func run', T + T + 'return 1', 'class B', T + 'func run', T + T + 'return 2']},
         run='l.ring', asserts=[
             ("fn(d, 'f')['calls_dynamic']", ['run']),
             ("fn(d, 'f')['calls_static']", ['g']),
             ("[x['name'] for x in d['functions']]", ['f', 'g', 'run', 'run']),
         ]),
    dict(id='X08', line='P4', why='the first direct impurity met, with its line; none seen, no field',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("fn(d, 'g')['impure']", {'why': 'prints', 'line': 10}),
             ("fn(d, 'h')['impure']", {'why': 'writes a global', 'line': 14}),
             ("'impure' in fn(d, 'f')", False),
             ("'impure' in fn(d, 'K.m')", False),
             ("'calls are not followed' in d['impurity']", True),
         ]),
    dict(id='X09', line='P4', why='a call whose value moves on its own is an impurity, named',
         files={'c.ring': ['func f', T + 'return clock()']}, run='c.ring', asserts=[
             ("fn(d, 'f')['impure']", {'why': 'calls clock()', 'line': 2}),
         ]),
    dict(id='X10', line='P5', why='a .haro function the compiler refused: not compiled, why and where; its caller compiled and reaches it',
         files={'b.haro': ['f()', 'func f', T + 'return len("abc")', 'func g', T + 'return f()']}, run='b.haro', asserts=[
             ("d['files'][0]['surface']", 'haro'),
             ("fn(d, 'f')['compiled']", False),
             ("'a built-in is spelled `Len`' in fn(d, 'f')['refused']['why']", True),
             ("fn(d, 'f')['refused']['line']", 3),
             ("fn(d, 'g')['compiled']", True),
             ("'refused' in fn(d, 'g')", False),
             ("fn(d, 'g')['reaches_uncompiled']", True),
             ("fn(d, 'f')['reaches_uncompiled']", False),
         ]),
    dict(id='X11', line='P5', why='every function of a clean unit compiled, none reaching an unfinished one',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("[(x['compiled'], x['reaches_uncompiled']) for x in d['functions']]", [[True, False]] * 4),
         ]),
    dict(id='X12', line='P2', why='a unit of two files: each function names its own file',
         files={'main.ring': ['load "lib.ring"', '? twice(2)', 'func local', T + 'return twice(1)'], 'lib.ring': ['func twice n', T + 'return n * 2']},
         run='main.ring', asserts=[
             ("sorted(x['path'].replace(chr(92), '/').split('/')[-1] for x in d['files'])", ['lib.ring', 'main.ring']),
             ("d['files'][fn(d, 'twice')['file']]['path'].endswith('lib.ring')", True),
             ("d['files'][fn(d, 'local')['file']]['path'].endswith('main.ring')", True),
             ("d['files'][fn(d, 'twice')['file']]['sha256']", '@SHA:lib.ring'),
             ("fn(d, 'local')['calls_static']", ['twice']),
         ]),
    dict(id='X13', line='P6', why='the rules that did not look, and why: eval in the unit, no listener named',
         files={'e.ring': ['eval("x = 1")', 'func f', T + 'return 1']}, run='e.ring', asserts=[
             ("[r for x in d['not_checked'] for r in x['rules']]",
              ['haro/undefined-function', 'haro/unknown-class', 'haro/unknown-package', 'haro/uninitialized-variable', 'haro/listener-binds-all']),
             ("all(len(x['why']) > 0 for x in d['not_checked'])", True),
         ]),
    dict(id='X14', line='P6', why='a unit without eval: only the listener rule did not look',
         files={'a.ring': A_RING}, run='a.ring', asserts=[
             ("[r for x in d['not_checked'] for r in x['rules']]", ['haro/listener-binds-all']),
         ]),
]


def main():
    out = []
    for c in CASES:
        folder = os.path.join(HERE, 'cases', c['id'])
        os.makedirs(folder, exist_ok=True)
        for name, lines in c['files'].items():
            with open(os.path.join(folder, name), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('\n'.join(lines) + '\n')
        row = {'id': c['id'], 'line': c['line'], 'why': c['why'], 'folder': 'cases/' + c['id'], 'run': c['run'],
               'flag_first': c.get('flag_first', False), 'same_as_flag_last': c.get('same_as_flag_last', False),
               'asserts': [[e, v] for e, v in c['asserts']]}
        out.append(row)
    doc = {
        'rung': 'v0.51',
        'decision': 'HARO-FACTS-01, answering HARO-PROOF-01 (a): `haro check --facts`, per function, what the checker and the compiler establish',
        'class': 'every assert holds on the JSON each build prints; both builds print the same bytes (D41); exit 0. @COMMIT is the last '
                 'commit that touched vm/ (+uncommitted when vm/ holds changes); @SHA:<file> is the sha256 of that case file\'s bytes',
        'lines': {
            'P1': 'the record: format, checker commit, each file\'s sha256 and surface; the flag before or after the file',
            'P2': 'every function and method, its lines, the findings inside it; those outside every function per file',
            'P3': 'its calls: static, dynamic, late',
            'P4': 'its first direct impurity and its line; absent when none is seen',
            'P5': 'compiled or not, why and where; whether it reaches an unfinished function',
            'P6': 'the rules that did not look, and why',
        },
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
