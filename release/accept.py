"""Acceptance of one release archive (HARO-RELEASE-ADOPT-01 (e)): the archive unpacked into a fresh folder, a fresh clone of
mayouni/stzradar beside it, then from the clone's root `haro tools/guard.haro` must exit 0 and `haro tools/feed.haro check` must report
0 problems (its exit code is the problem count). The Linux archive is accepted under WSL; the macOS archive cannot be accepted on this
machine, and says so (NOT RUN, absent hardware).

  python release/accept.py runtime/release/<version>/haro-<version>-windows-x86_64.zip
  python release/accept.py runtime/release/<version>/haro-<version>-linux-x86_64.tar.gz
"""
import os, subprocess, sys, tarfile, tempfile, zipfile

RADAR = 'https://github.com/mayouni/stzradar.git'


def wsl_path(p):
    p = os.path.abspath(p)
    return '/mnt/' + p[0].lower() + p[2:].replace('\\', '/')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    archive = os.path.abspath(sys.argv[1])
    name = os.path.basename(archive)
    if 'macos' in name:
        print(f'NOT RUN {name}: no macOS machine here (absent hardware); acceptance owed on one')
        return 2
    linux = 'linux' in name
    with tempfile.TemporaryDirectory() as td:
        if name.endswith('.zip'):
            zipfile.ZipFile(archive).extractall(td)
        else:
            with tarfile.open(archive) as t:
                t.extractall(td, filter='tar')
        top = [d for d in os.listdir(td) if os.path.isdir(os.path.join(td, d))][0]
        exe = os.path.join(td, top, 'haro' if linux else 'haro.exe')
        clone = os.path.join(td, 'stzradar')
        if linux:
            script = (f'set -e; git clone -q --depth 1 {RADAR} "{wsl_path(clone)}"; cd "{wsl_path(clone)}"; '
                      f'git log -1 --format="radar %h %ci"; chmod +x "{wsl_path(exe)}"; '
                      f'"{wsl_path(exe)}" tools/guard.haro; echo "guard exit $?"; '
                      f'set +e; "{wsl_path(exe)}" tools/feed.haro check; echo "feed check exit $?"')
            r = subprocess.run(['wsl.exe', '-e', 'bash', '-c', script], capture_output=True)
            out = r.stdout.decode('utf-8', 'replace')
            print(out[-3000:])
            ok = 'guard exit 0' in out and 'feed check exit 0' in out
        else:
            subprocess.run(['git', 'clone', '-q', '--depth', '1', RADAR, clone], check=True)
            head = subprocess.run(['git', 'log', '-1', '--format=radar %h %ci'], cwd=clone, capture_output=True, text=True).stdout
            print(head.strip())
            g = subprocess.run([exe, 'tools/guard.haro'], cwd=clone, capture_output=True)
            f = subprocess.run([exe, 'tools/feed.haro', 'check'], cwd=clone, capture_output=True)
            print(g.stdout.decode('utf-8', 'replace')[-1500:], f'guard exit {g.returncode}')
            print(f.stdout.decode('utf-8', 'replace')[-1500:], f'feed check exit {f.returncode}')
            ok = g.returncode == 0 and f.returncode == 0
    print(f'{"ACCEPTED" if ok else "REFUSED"} {name}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
