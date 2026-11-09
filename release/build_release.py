"""Haro's release builds (HARO-RELEASE-ADOPT-01 (b) (c)): one target per run, never two at once (the machine's build caps), each
archive holding the binary and THIRD-PARTY-NOTICES.txt, its SHA-256 written beside it.

  python release/build_release.py windows     x86_64-windows-gnu
  python release/build_release.py linux       x86_64-linux-gnu.2.28 (glibc 2.28 and later)
  python release/build_release.py macos       aarch64-macos
  python release/build_release.py notices     write runtime/release/THIRD-PARTY-NOTICES.txt only

The notices are assembled from the licence files themselves -- the vendored ones, Zig's own and its C runtime's from the Zig that
builds, and tree-sitter's (release/licenses/, fetched at v0.25.10, the version that regenerated the vendored parser) -- never typed.
Output: runtime/release/<version>/ (gitignored). The release's licence and its public place are the Principal's (a) (d).
"""
import hashlib, io, os, shutil, subprocess, sys, tarfile, zipfile

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


def version():
    head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return f'v0.50-{head}'  # the rung, and the commit that built it


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
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
    text = notices(which).encode('utf-8')
    archive = os.path.join(out_dir, f'{name}.{kind}')
    if kind == 'zip':
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(binary, f'{name}/{exe}')
            z.writestr(f'{name}/THIRD-PARTY-NOTICES.txt', text)
    else:
        with tarfile.open(archive, 'w:gz') as t:
            info = t.gettarinfo(binary, f'{name}/{exe}')
            info.mode = 0o755
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            with open(binary, 'rb') as fh:
                t.addfile(info, fh)
            info = tarfile.TarInfo(f'{name}/THIRD-PARTY-NOTICES.txt')
            info.size = len(text)
            info.mode = 0o644
            t.addfile(info, io.BytesIO(text))
    digest = sha(archive)
    open(archive + '.sha256', 'w', newline='\n').write(f'{digest}  {os.path.basename(archive)}\n')
    print(f'{os.path.basename(archive)}  {os.path.getsize(archive):,} bytes  sha256 {digest}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
