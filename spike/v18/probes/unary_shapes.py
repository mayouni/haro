import subprocess, os, tempfile
RN = os.path.abspath('zig-out-j/bin/rnxc.exe')
d = tempfile.mkdtemp()
p = os.path.join(d, 't.ring')


def shape(text):
    open(p, 'w').write(text + '\n')
    out = subprocess.run([RN, 'dump', p], capture_output=True).stdout.decode('latin-1').split('\n')
    # compress: kind names with depth, no leaves except operators
    lines = []
    for ln in out[0:]:
        if not ln.strip():
            continue
        depth = (len(ln) - len(ln.lstrip(' '))) // 2
        k = ln.strip().split('  ')[0]
        lines.append((depth, ln.strip()))
    # print a bracketed form of the first expression
    def br(i, depth):
        d0, t = lines[i]
        kids = []
        j = i + 1
        while j < len(lines) and lines[j][0] > d0:
            if lines[j][0] == d0 + 1:
                kids.append(j)
            j += 1
        name = t.split('  ')[0]
        if t.find("'") >= 0 and not kids:
            return t.split("'")[1] if name in ('identifier', 'number') else name
        return name.replace('_expression', '')[:5] + '(' + ' '.join(br(k, d0 + 1) for k in kids) + ')'
    # root is lines[0]; statement is lines[1]
    return br(2, 2)


for t in ['-a + b', '-a - b', '-a - b - c', '-a * b - c', '-a - b * c', '-a * b', '-a < b', '-a = b', '-a and b', '-a ** b', '-a : b', '-a % b - c',
          '-a.b - c', '-f(x) - c', '- a - b', '-a-b', '-a -b', '+a + b', '!a - b', 'x = -a - b', '? -a - b', '-a - b + c', '-a + b - c', '1 -a - b']:
    print('%-14s' % t, shape(t))
