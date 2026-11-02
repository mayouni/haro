"""Where Haro finds what it runs on -- one place, so every script agrees.

Haro's courts are code written in .haro files and run on the Haro VM, `haro` (vm/, forked from Ring++'s VM and compiler on
2026-11-02 and Haro's own from then). Each court is judged twice: on the VM as it ships (ReleaseFast) and on its CHECKED build
(ReleaseSafe: every integer overflow, bound and refcount checked), and the two must print the same bytes. Since the cut no Ring
runs in a court.

    HARO          this repository's root
    HARO_VM       $HARO_VM, else vm\\zig-out\\bin\\haro.exe                       the VM a court is judged on
    TWIN          $HARO_TWIN, else vm\\zig-out-safe\\bin\\haro.exe                 its checked build: the second judge
    OUT           runtime\\ (gitignored): what a run writes; TWIN_OUT, the second judge's forge folder
    RINGPP        $RINGPP, else a Ring++ checkout beside this one (<parent>\\ringpp): Ring++ is the bridge that keeps Softanza's legacy
                  code running, so what drives Softanza (its library, its engine, the local models) runs on Ring++'s package from there
    RING_ORACLE   Ring 1.27's VM as Ring++ builds it: ONLY for the studies and probes OF Ring's behaviour, which name it as their
                  subject; never a judge of a Haro court

    python paths.py              what this checkout runs on

    zig build -Doptimize=ReleaseFast -j2                       in vm\\     -> HARO_VM
    zig build -Doptimize=ReleaseSafe -j2 -p zig-out-safe       in vm\\     -> TWIN
"""
import os, re, subprocess, sys, time

HARO = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.join(HARO, 'spike')
STUDY = os.path.join(HARO, 'study')
VM_DIR = os.path.join(HARO, 'vm')
HARO_VM = os.environ.get('HARO_VM') or os.path.join(VM_DIR, 'zig-out', 'bin', 'haro.exe')
TWIN = os.environ.get('HARO_TWIN') or os.path.join(VM_DIR, 'zig-out-safe', 'bin', 'haro.exe')
OUT = os.path.join(HARO, 'runtime')
TWIN_OUT = os.path.join(OUT, 'haro-forge-twin')
RINGPP = os.path.abspath(os.environ.get('RINGPP') or os.path.join(os.path.dirname(HARO), 'ringpp'))
RINGPP_RNXC = os.path.join(RINGPP, 'zig-out', 'bin', 'rnxc.exe')
RING_ORACLE = os.path.join(RINGPP, 'runtime', 'win64', 'ring.exe')


def rel(path, start):
    """`path` relative to `start`, with forward slashes: what a court is handed when it must write by a relative name (the guard's
    stage 2: a write to the temp folder's absolute path was refused on this machine)."""
    return os.path.relpath(path, start).replace(os.sep, '/')


def is_declaration(path):
    """A .haro file is a DECLARATION when its first word, past `--` comments and blank lines, is DEFINE; any other .haro file is code."""
    try:
        with open(path, encoding='utf-8', errors='replace') as fh:
            for line in fh:
                s = line.strip()
                if not s or s.startswith('--'):
                    continue
                return s.split()[0] == 'DEFINE'
    except OSError:
        return False
    return False


def code_files(folder):
    """The code in a folder: its .haro files that are not declarations, sorted."""
    import glob
    return sorted(p for p in glob.glob(os.path.join(folder, '*.haro')) if not is_declaration(p))


def need_ringpp():
    """Stop, naming the way out, when a script needs Ring++ (the bridge) and there is no checkout."""
    if not os.path.isdir(RINGPP):
        how = '$RINGPP' if os.environ.get('RINGPP') else 'a checkout beside this one'
        sys.exit('no Ring++ checkout at %s (%s) -- clone it there, or set RINGPP=<a Ring++ checkout>' % (RINGPP, how))
    return RINGPP


def need_bins():
    """Stop when the VM or its checked build is missing, naming which and how to build it."""
    for name, p, how in (('the Haro VM', HARO_VM, 'zig build -Doptimize=ReleaseFast -j2 in vm/, or HARO_VM=<path>'),
                         ('its checked build', TWIN, 'zig build -Doptimize=ReleaseSafe -j2 -p zig-out-safe in vm/, or HARO_TWIN=<path>')):
        if not os.path.isfile(p):
            sys.exit('no %s at %s -- %s' % (name, p, how))
    return HARO_VM, TWIN


def build_of(exe=None):
    """Which build an executable is: the Haro VM or its checked build (vm/'s last commit and when the binary was built), Ring++'s
    rnxc (its checkout's HEAD, or the package's PACKAGE.txt), or a path, a size and a date."""
    exe = os.path.abspath(exe or HARO_VM)
    if not os.path.isfile(exe):
        return 'nothing at ' + exe
    built = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(exe)))

    def head(repo, *pathspec):
        try:
            return subprocess.run(['git', '-C', repo, 'log', '-1', '--format=%h'] + (['--'] + list(pathspec) if pathspec else []),
                                  capture_output=True, text=True, timeout=30).stdout.strip() or 'uncommitted'
        except (OSError, subprocess.SubprocessError):
            return '?'
    for label, p in (('the Haro VM', HARO_VM), ('its checked build', TWIN)):
        if os.path.normcase(exe) == os.path.normcase(os.path.abspath(p)):
            return '%s %s (vm/ at %s), built %s' % (label, exe, head(HARO, 'vm'), built)
    pkg = os.path.join(os.path.dirname(os.path.dirname(exe)), 'PACKAGE.txt')
    if os.path.isfile(pkg):
        m = re.search(r'rnxc\s+ringpp\s+(\S+)\s+(\S+)', open(pkg, encoding='utf-8').read())
        if m:
            return 'Ring++ %s %s, installed' % (m.group(1), m.group(2))
    d = os.path.dirname(exe)
    while os.path.dirname(d) != d:
        if os.path.exists(os.path.join(d, '.git')) and os.path.isfile(os.path.join(d, 'src', 'rnxc.zig')):
            return 'Ring++ checkout %s (HEAD %s), built %s' % (d, head(d), built)
        d = os.path.dirname(d)
    return '%s, %d bytes, built %s' % (exe, os.path.getsize(exe), built)


if __name__ == '__main__':
    for name, p, isdir in (('HARO', HARO, True), ('HARO_VM', HARO_VM, False), ('TWIN', TWIN, False), ('OUT', OUT, None),
                           ('RINGPP', RINGPP, True), ('RING_ORACLE', RING_ORACLE, False)):
        ok = '' if isdir is None else ('' if (os.path.isdir(p) if isdir else os.path.isfile(p)) else '  -- MISSING')
        print('%-12s %s%s' % (name, p, ok))
    print('the VM       ', build_of(HARO_VM))
    print('the twin     ', build_of(TWIN))
