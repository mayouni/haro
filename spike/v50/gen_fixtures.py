"""Haro v0.50 -- a program that serves another: output reaches its reader before the program waits, a line is read whole, the end of
input is said, and Ring's three streams are there. Written FIRST, before the VM is touched.

THE FINDING. HARO-STDIOFLUSH-01, from the Radar desk (2026-11-09 14:10, through central 16:15), building Radar's MCP server on Haro
(stzradar tools/mcp.haro): Haro held a program's output to a pipe until the program ended, `give` waited for input without sending it,
there was no way to flush, and a read at the end of input answered "" for ever -- so the server counted four empty reads to guess its
client had gone, and sent each reply by running an empty shell command (system() flushes). Asked: (a) flush before waiting for input,
as C's stdio does for a terminal, (b) or a flush, (c) a way to know the input has ended. This desk found a fourth reading `give`: a line
past 4,096 bytes was cut, the rest coming back as the next line -- an MCP message is one line, and can be longer.

THE LINES:
  S1  `give` sends the program's output before it waits for input, as Ring's `see` and C's stdio for a terminal do
  S2  `stdin`, `stdout` and `stderr` are the program's three streams, file handles as Ring has them (type "file"); `fflush(stdout)`
      (`FFlush(stdout)` in a .haro file) sends the output now; a write through `stdout` keeps its place among `see`'s; a program's
      own variable of that name is its own
  S3  `give` reads a line whole, whatever its length (a named divergence: Ring's give cuts a line at 255 bytes)
  S4  `feof(stdin)` answers whether a read has met the end of input -- C's and Ring's answer: 1 once a read found no more, so an
      empty line is not the end and a last line without its line end is; in a .haro file `FEOF` answers a boolean, as `FExists` does

THE DIALOG CASES. A `dialog` case runs the program with its input and output on pipes and follows its steps: `expect` waits (10 s at
most) until the program's whole output so far ends with the text, `send` writes a line, `touch` makes a file in its folder, `close`
ends its input. A program that holds its output never meets an `expect`: that is the defect, read the way Radar's client reads it.

  python spike/v50/gen_fixtures.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = '\t'
LONG = 100000

CASES = [
    # ---- S1: output sent before give waits
    dict(id='D01', line='S1', why='a .ring program\'s prompt reaches its reader before give waits', ext='.ring', kind='dialog',
         src=['see "name?" + nl', 'give cName', 'see "hello " + cName + nl'],
         steps=[['expect', 'name?\n'], ['send', 'Ann\n'], ['close']],
         stdout='name?\nhello Ann\n'),
    dict(id='D02', line='S1', why='a .haro program\'s prompt reaches its reader before give waits', ext='.haro', kind='dialog',
         src=['see "name?" + nl', 'give tName', 'see "hello " + tName + nl'],
         steps=[['expect', 'name?\n'], ['send', 'Ann\n'], ['close']],
         stdout='name?\nhello Ann\n'),
    # ---- S2: the streams, and a flush asked for
    dict(id='D03', line='S2', why='fflush(stdout) sends the output while the program still runs (it waits for a file the reader makes on seeing it)',
         ext='.ring', kind='dialog',
         src=['see "ready" + nl', 'fflush(stdout)', 'while not fexists("go.txt")', 'end', 'see "went" + nl'],
         steps=[['expect', 'ready\n'], ['touch', 'go.txt'], ['close']],
         stdout='ready\nwent\n'),
    dict(id='D04', line='S2', why='FFlush(stdout) in a .haro file, the same', ext='.haro', kind='dialog',
         src=['see "ready" + nl', 'FFlush(stdout)', 'while not FExists("go.txt")', 'end', 'see "went" + nl'],
         steps=[['expect', 'ready\n'], ['touch', 'go.txt'], ['close']],
         stdout='ready\nwent\n'),
    dict(id='D05', line='S2', why='the three streams are file handles; a write through stdout keeps its place among see\'s, stderr is not stdout',
         ext='.ring', kind='run', input='',
         src=['see "one" + nl', 'fputs(stdout, "two" + nl)', 'see "three" + nl', 'fputs(stderr, "err" + nl)',
              '? type(stdin) + " " + type(stdout) + " " + type(stderr)'],
         stdout='one\ntwo\nthree\nfile file file\n'),
    dict(id='D06', line='S2', why='FPuts(stdout, ..) in a .haro file keeps its place too', ext='.haro', kind='run', input='',
         src=['see "one" + nl', 'FPuts(stdout, "two" + nl)', 'see "three" + nl'],
         stdout='one\ntwo\nthree\n'),
    dict(id='D07', line='S2', why='a .ring program\'s own variable named stdout is its own, in any case', ext='.ring', kind='run', input='',
         # D07 CHANGED AFTER THE CODE, said so: plant F9 missed -- a top-level read finds the global as the main chunk's own name, so
         # only a FUNCTION reading the program's global asks whether it replaces the stream; g() asks it
         src=['StdOut = 5', '? stdout + 1', '? f()', '? g()', 'func f', T + 'stdin = "mine"', T + 'return stdin', 'func g',
              T + 'return stdout + 2'],
         stdout='6\nmine\n7\n'),
    # D14 was ADDED AFTER THE CODE, said so: the plants found the .haro file's exact spelling of the three names judged by no case. Its
    # message names `stdout` folded -- R24 folds a name in a .haro file, a gap named since v0.42, not this rung's.
    dict(id='D14', line='S2', why='in a .haro file the streams are spelled exactly: `StdOut` is no stream', ext='.haro', kind='run', input='',
         src=['FPuts(StdOut, "x" + nl)'],
         stdout='\nLine 1 Error (R24) : Using uninitialized variable: stdout \nin file D14.haro ', exit=1),
    # ---- S3: a line read whole
    dict(id='D08', line='S3', why=f'a .ring give reads a {LONG:,}-byte line whole, and the next give the next line', ext='.ring', kind='run',
         input='a' * LONG + '\nb\n',
         src=['give a', '? len(a)', 'give b', '? b'],
         stdout=f'{LONG}\nb\n'),
    dict(id='D09', line='S3', why='a .haro give, the same', ext='.haro', kind='run',
         input='a' * LONG + '\r\nb\r\n',
         src=['give tA', '? Len(tA)', 'give tB', '? tB'],
         stdout=f'{LONG}\nb\n'),
    # ---- S4: the end of input
    dict(id='D10', line='S4', why='feof(stdin): 0 before reading, 0 after a line and after an empty line, 1 once a read found no more',
         ext='.ring', kind='run', input='a\n\n',
         src=['? feof(stdin)', 'give a', '? "[" + a + "] " + feof(stdin)', 'give b', '? "[" + b + "] " + feof(stdin)',
              'give c', '? "[" + c + "] " + feof(stdin)', 'give d', '? "[" + d + "] " + feof(stdin)'],
         stdout='0\n[a] 0\n[] 0\n[] 1\n[] 1\n'),
    dict(id='D11', line='S4', why='a last line without its line end is read, and the end is met with it, as C\'s fgets meets it',
         ext='.ring', kind='run', input='abc',
         src=['give a', '? a', '? feof(stdin)'],
         stdout='abc\n1\n'),
    dict(id='D12', line='S4', why='in a .haro file FEOF answers a boolean: `if FEOF(stdin)` is a condition', ext='.haro', kind='run',
         input='a\n\n',
         src=['give tA', 'while not FEOF(stdin)', T + 'see "[" + tA + "]" + nl', T + 'give tA', 'end', 'see "end" + nl'],
         stdout='[a]\n[]\nend\n'),
    # ---- the whole: a server answering each line, leaving at the end of its input
    dict(id='D13', line='S1, S4', why='a .haro server answers each line before the next is sent, an empty line included, and leaves when its input ends',
         ext='.haro', kind='dialog',
         src=['func main', T + 'while true', T + T + 'give tLine', T + T + 'if tLine = "" and FEOF(stdin)', T + T + T + 'exit',
              T + T + 'ok', T + T + 'see "got [" + tLine + "]" + nl', T + 'end', T + 'see "bye" + nl'],
         steps=[['send', 'a\n'], ['expect', 'got [a]\n'], ['send', '\n'], ['expect', 'got []\n'], ['send', 'b\n'],
                ['expect', 'got [b]\n'], ['close']],
         stdout='got [a]\ngot []\ngot [b]\nbye\n'),
]


def main():
    os.makedirs(os.path.join(HERE, 'cases'), exist_ok=True)
    out = []
    for c in CASES:
        name = 'cases/' + c['id'] + c['ext']
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(c['src']) + '\n')
        row = {'id': c['id'], 'kind': c['kind'], 'line': c['line'], 'why': c['why'], 'file': name}
        if c['kind'] == 'dialog':
            row['steps'] = c['steps']
        else:
            row['input'] = c['input']
        row['stdout'] = c['stdout']
        if c.get('exit'):
            row['exit'] = c['exit']
        out.append(row)
    doc = {
        'rung': 'v0.50',
        'decision': 'HARO-STDIOFLUSH-01 (the Radar desk, through central 2026-11-09 16:15): a program that serves another',
        'class': 'exact: the program\'s whole stdout and its exit code, byte for byte, on haro and on its checked build; a dialog\'s every '
                 'expect met within 10 s',
        'lines': {
            'S1': 'give sends the program\'s output before it waits',
            'S2': 'stdin, stdout, stderr are file handles; fflush(stdout) sends the output; a stdout write keeps its place',
            'S3': 'give reads a line whole (Ring cuts at 255 bytes: a named divergence)',
            'S4': 'feof(stdin) answers whether a read met the end of input; a boolean in a .haro file',
        },
        'cases': out,
    }
    with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1)
    print(f'{len(out)} cases written')


if __name__ == '__main__':
    main()
