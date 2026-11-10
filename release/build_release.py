"""Haro's release builds (HARO-RELEASE-ADOPT-01; D63): one target per run, never two at once (the machine's build caps), each archive
holding the binary, LICENSE and THIRD-PARTY-NOTICES.txt, its SHA-256 written beside it.

  python release/build_release.py windows     x86_64-windows-gnu
  python release/build_release.py linux       x86_64-linux-gnu.2.28 (glibc 2.28 and later)
  python release/build_release.py macos       aarch64-macos
  python release/build_release.py notices     write runtime/release/<version>/THIRD-PARTY-NOTICES-<platform>.txt only
  python release/build_release.py public windows linux
                                              the public page for the named (accepted) builds: runtime/release/<version>/public/
                                              README.md and SHA256SUMS, refused if its text breaks the public-text rules

LICENSE is MIT, "Copyright (c) 2020-<year> Mansour Ayouni", the year read from the clock (D63, PRINCIPAL-COPYRIGHTYEARS-01): the text is
stzlib's LICENSE (release/licenses/MIT-LICENSE, from stzlib origin/main), its copyright line rewritten. The notices are assembled from
the licence files themselves -- the vendored ones, Zig's own and its C runtime's from the Zig that builds, and tree-sitter's
(release/licenses/, fetched at v0.25.10, the version that regenerated the vendored parser) -- never typed. Output:
runtime/release/<version>/ (gitignored); <version> is the latest rung and the commit that built it.
"""
import datetime, glob, hashlib, io, os, re, shutil, subprocess, sys, tarfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VM = os.path.join(ROOT, 'vm')
VENDOR = os.path.join(VM, 'vendor')
TARGETS = {
    'windows': ('x86_64-windows-gnu', 'windows-x86_64', 'haro.exe', 'zip'),
    'linux': ('x86_64-linux-gnu.2.28', 'linux-x86_64', 'haro', 'tar.gz'),
    'macos': ('aarch64-macos', 'macos-aarch64', 'haro', 'tar.gz'),
}


def zig_lib():
    out = subprocess.run(['zig', 'env'], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if '.lib_dir' in line:
            return line.split('"')[1].replace('\\\\', '\\')
    sys.exit('zig env gives no lib_dir')


def read(p):
    return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip() + '\n'


def notices(platform):
    lib = zig_lib()
    zig_root = os.path.dirname(lib)
    parts = [
        ('mimalloc', 'the memory allocator', os.path.join(VENDOR, 'mimalloc', 'LICENSE')),
        ('tree-sitter', 'the parsing runtime', os.path.join(HERE, 'licenses', 'tree-sitter-LICENSE')),
        ('Unicode data', 'tables inside the tree-sitter runtime', os.path.join(VENDOR, 'tree-sitter', 'src', 'unicode', 'LICENSE')),
        ('A tree-sitter grammar by Youssef Saeed', 'the grammar of the surface Haro reads', os.path.join(VENDOR, 'tree-sitter-ring', 'LICENSE')),
        ('The Zig standard library and compiler-rt', 'compiled into the binary', os.path.join(zig_root, 'LICENSE')),
    ]
    if platform == 'windows':
        parts.append(('mingw-w64 runtime', 'the C start-up code of the Windows binary', os.path.join(lib, 'libc', 'mingw', 'COPYING')))
    out = ['THIRD-PARTY NOTICES', '', 'The haro binary contains the following software, each under its own licence, reproduced in full.', '']
    for name, role, path in parts:
        out += ['=' * 78, f'{name} -- {role}', '=' * 78, '', read(path)]
    return '\n'.join(out)


def rung():
    """the latest rung built: the highest spike/vNN that holds its fixtures"""
    nums = [int(os.path.basename(os.path.dirname(p))[1:]) for p in glob.glob(os.path.join(ROOT, 'spike', 'v[0-9][0-9]', 'fixtures.json'))]
    return f'v0.{max(nums)}'


def version():
    head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return f'{rung()}-{head}'  # the rung, and the commit that built it


def licence():
    """MIT, the estate's text, the copyright's end year read from the clock"""
    text = read(os.path.join(HERE, 'licenses', 'MIT-LICENSE'))
    line = f'Copyright (c) 2020-{datetime.date.today().year} Mansour Ayouni'
    out, n = re.subn(r'^Copyright \(c\) .*$', line, text, count=1, flags=re.M)
    if n != 1:
        sys.exit('release/licenses/MIT-LICENSE has no copyright line')
    return out


# PRINCIPAL-AFFIRM-01 (a public page says what the project IS and DOES; no line lists what has not been done) and
# PRINCIPAL-HAROINDEPENDENT-01 (the release's public text names no other language). Each phrase is refused anywhere in the page.
REFUSED = [r'\bnot yet\b', r'\bnobody has\b', r'\bnever been\b', r'\bLimit:', r'\buntested\b', r'\bunmeasured\b', r'\bnot tested\b',
           r'\bnot been\b', r'\bRing\b', r'\bRing\+\+', r'\.ring\b']
SITE = 'https://mayouni.github.io/stzsite/'
PLATFORM_WORDS = {'windows-x86_64': 'Windows, x86-64', 'linux-x86_64': 'Linux, x86-64 (glibc 2.28 and later)',
                  'macos-aarch64': 'macOS, Apple silicon'}


def public(ver, out_dir, which):
    rows, sums = [], []
    for w in which:
        _, platform, _, kind = TARGETS[w]
        name = f'haro-{ver}-{platform}.{kind}'
        path = os.path.join(out_dir, name)
        if not os.path.exists(path):
            sys.exit(f'no archive {name}: build it first')
        d = sha(path)
        rows.append(f'| {PLATFORM_WORDS[platform]} | `{name}` | `{d}` |')
        sums.append(f'{d}  {name}')
    page = '\n'.join([
        '# Haro',
        '',
        'Haro is the foundational language of the Softanza project: a language of languages, in which a world is declared, '
        'constrained, asked and spoken to, and every sentence is judged by a court built from its declaration.',
        '',
        f'## Downloads -- {ver}',
        '',
        '| platform | archive | SHA-256 |',
        '|---|---|---|',
        *rows,
        '',
        'Each archive holds the `haro` binary, its LICENSE and THIRD-PARTY-NOTICES.txt. SHA256SUMS lists every sum.',
        '',
        '## Use',
        '',
        '```',
        'haro prog.haro                    runs a program',
        'haro check prog.haro              checks it without running it',
        'haro check --facts prog.haro      prints what the checker establishes, per function, as JSON',
        '```',
        '',
        '## Licence',
        '',
        f'MIT. Copyright (c) 2020-{datetime.date.today().year} Mansour Ayouni. Haro is a Softanza project: {SITE}',
        '',
    ])
    bad = [(p, m.group(0)) for p in REFUSED for m in [re.search(p, page)] if m]
    if bad:
        sys.exit('the public page is refused: ' + '; '.join(f'{p} matched {t!r}' for p, t in bad))
    pub = os.path.join(out_dir, 'public')
    os.makedirs(pub, exist_ok=True)
    open(os.path.join(pub, 'README.md'), 'w', encoding='utf-8', newline='\n').write(page)
    open(os.path.join(pub, 'SHA256SUMS'), 'w', encoding='utf-8', newline='\n').write('\n'.join(sums) + '\n')
    open(os.path.join(pub, 'LICENSE'), 'w', encoding='utf-8', newline='\n').write(licence())
    print('public page written to', pub)
    return 0


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == 'public' and all(w in TARGETS for w in sys.argv[2:]):
        ver = version()
        return public(ver, os.path.join(ROOT, 'runtime', 'release', ver), sys.argv[2:])
    if len(sys.argv) != 2 or sys.argv[1] not in list(TARGETS) + ['notices']:
        sys.exit(__doc__)
    which = sys.argv[1]
    ver = version()
    out_dir = os.path.join(ROOT, 'runtime', 'release', ver)
    os.makedirs(out_dir, exist_ok=True)
    if which == 'notices':
        for p in TARGETS:
            open(os.path.join(out_dir, f'THIRD-PARTY-NOTICES-{p}.txt'), 'w', encoding='utf-8', newline='\n').write(notices(p))
        print('notices written to', out_dir)
        return 0
    triple, platform, exe, kind = TARGETS[which]
    prefix = os.path.join(ROOT, 'runtime', 'release', 'build-' + which)
    cmd = ['zig', 'build', '-Doptimize=ReleaseFast', '-Dstrip=true', '-j2', f'-Dtarget={triple}', '-p', prefix]
    print(' '.join(cmd), flush=True)
    subprocess.run(cmd, cwd=VM, check=True)
    binary = os.path.join(prefix, 'bin', exe)
    name = f'haro-{ver}-{platform}'
    texts = [('LICENSE', licence().encode('utf-8')), ('THIRD-PARTY-NOTICES.txt', notices(which).encode('utf-8'))]
    archive = os.path.join(out_dir, f'{name}.{kind}')
    if kind == 'zip':
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(binary, f'{name}/{exe}')
            for fname, text in texts:
                z.writestr(f'{name}/{fname}', text)
    else:
        with tarfile.open(archive, 'w:gz') as t:
            info = t.gettarinfo(binary, f'{name}/{exe}')
            info.mode = 0o755
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            with open(binary, 'rb') as fh:
                t.addfile(info, fh)
            for fname, text in texts:
                info = tarfile.TarInfo(f'{name}/{fname}')
                info.size = len(text)
                info.mode = 0o644
                t.addfile(info, io.BytesIO(text))
    digest = sha(archive)
    open(archive + '.sha256', 'w', newline='\n').write(f'{digest}  {os.path.basename(archive)}\n')
    print(f'{os.path.basename(archive)}  {os.path.getsize(archive):,} bytes  sha256 {digest}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
