"""Where Haro finds what it runs on -- one place, so every script agrees.

Haro's courts are Ring code. Each runs on `rnxc` (Ring++) AND on the oracle (Ring++'s own build of Ring 1.27's VM), and the two must
print the same bytes. Both binaries come from a Ring++ checkout. Haro grew inside Ring++ (under haro/ on branch `next`) and its
scripts reached Ring++ by climbing directories; since 2026-11-02 it is its own repository, so they ask here instead.

    HARO       this repository's root
    RINGPP     $RINGPP, else a Ring++ checkout beside this one (<parent>\\ringpp); a script that needs it and finds none stops,
               naming what it looked for -- there is no silent fallback to an installed Ring++, because a court must say which
               compiler it ran on
    VM         $HARO_VM, else HARO\\vm\\zig-out\\bin\\haro.exe: Haro's own VM and compiler (vm/, forked from Ring++ on
               2026-11-02)
    RNXC       $RNXC, else VM: the runtime a script judges
    RING       $RING, else RINGPP\\runtime\\win64\\ring.exe          (the oracle)
    OUT        HARO\\runtime\\ (gitignored): what a run writes. The guard's oracle work folder, which was
               RINGPP\\runtime\\haro-forge-oracle, is ORACLE_OUT here

    python paths.py              what this checkout runs on
"""
import os, re, subprocess, sys, time

HARO = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.join(HARO, 'spike')
STUDY = os.path.join(HARO, 'study')
_BESIDE = os.path.join(os.path.dirname(HARO), 'ringpp')
RINGPP = os.path.abspath(os.environ.get('RINGPP') or _BESIDE)
VM = os.environ.get('HARO_VM') or os.path.join(HARO, 'vm', 'zig-out', 'bin', 'haro.exe')   # the Haro VM, built from vm/
RNXC = os.environ.get('RNXC') or VM            # the runtime a script judges: the Haro VM, unless RNXC names another (Ring++'s fmt court does)
RINGPP_RNXC = os.path.join(RINGPP, 'zig-out', 'bin', 'rnxc.exe')   # Ring++'s own, for what still runs Softanza's legacy code
RING = os.environ.get('RING') or os.path.join(RINGPP, 'runtime', 'win64', 'ring.exe')
OUT = os.path.join(HARO, 'runtime')
ORACLE_OUT = os.path.join(OUT, 'haro-forge-oracle')


def rel(path, start):
    """`path` relative to `start`, with forward slashes: what a Ring program is handed when it must write by a relative name
    (Ring's write() refused the temp folder's absolute path on this machine: the note at the guard's stage 2)."""
    return os.path.relpath(path, start).replace(os.sep, '/')


def need_ringpp():
    """Stop, naming the way out, when there is no Ring++ checkout to run on."""
    if not os.path.isdir(RINGPP):
        how = '$RINGPP' if os.environ.get('RINGPP') else 'a checkout beside this one'
        sys.exit('no Ring++ checkout at %s (%s) -- clone it there, or set RINGPP=<a Ring++ checkout>' % (RINGPP, how))
    return RINGPP


def need_bins():
    """Stop when rnxc or the oracle is missing, naming which and how to get it."""
    for name, p, how in (('the runtime', RNXC, 'zig build -Doptimize=ReleaseFast -j2 in vm/, or RNXC=<path>'),
                         ('the oracle', RING, "tests/b2_runtimes.ps1 in Ring++, or RING=<path>")):
        if not os.path.isfile(p):
            sys.exit('no %s at %s -- %s' % (name, p, how))
    return RNXC, RING


def rnxc_build(rnxc=None):
    """Which Ring++ an rnxc is: an installed package names its ringpp commit in PACKAGE.txt; a build inside a Ring++ checkout says
    that checkout's last commit and when the binary was built (a build may be older than its checkout's HEAD, so both are given);
    anything else, its size and date."""
    rnxc = os.path.abspath(rnxc or RNXC)
    if not os.path.isfile(rnxc):
        return 'no rnxc at ' + rnxc
    if os.path.normcase(rnxc) == os.path.normcase(os.path.abspath(VM)):
        built = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(rnxc)))
        try:
            head = subprocess.run(['git', '-C', HARO, 'log', '-1', '--format=%h', '--', 'vm'], capture_output=True, text=True, timeout=30).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            head = '?'
        return 'the Haro VM %s (vm/ at %s), built %s' % (rnxc, head or 'uncommitted', built)
    built = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(rnxc)))
    pkg = os.path.join(os.path.dirname(os.path.dirname(rnxc)), 'PACKAGE.txt')
    if os.path.isfile(pkg):
        m = re.search(r'rnxc\s+ringpp\s+(\S+)\s+(\S+)', open(pkg, encoding='utf-8').read())
        if m:
            return 'ringpp %s %s, installed' % (m.group(1), m.group(2))
    d = os.path.dirname(rnxc)
    while os.path.dirname(d) != d:
        if os.path.exists(os.path.join(d, '.git')) and os.path.isfile(os.path.join(d, 'src', 'rnxc.zig')):
            try:
                head = subprocess.run(['git', '-C', d, 'log', '-1', '--format=%h %ad', '--date=format:%Y-%m-%d %H:%M'],
                                      capture_output=True, text=True, timeout=30).stdout.strip()
            except (OSError, subprocess.SubprocessError):
                head = '?'
            return 'ringpp checkout %s (HEAD %s), rnxc built %s' % (d, head, built)
        d = os.path.dirname(d)
    return '%s, %d bytes, built %s' % (rnxc, os.path.getsize(rnxc), built)


if __name__ == '__main__':
    print('HARO       ', HARO)
    print('RINGPP     ', RINGPP, '' if os.path.isdir(RINGPP) else '  -- MISSING')
    print('VM         ', VM, '' if os.path.isfile(VM) else '  -- MISSING (zig build in vm/)')
    print('RNXC       ', RNXC, '' if os.path.isfile(RNXC) else '  -- MISSING')
    print('RING       ', RING, '' if os.path.isfile(RING) else '  -- MISSING')
    print('OUT        ', OUT)
    print('rnxc build ', rnxc_build())
