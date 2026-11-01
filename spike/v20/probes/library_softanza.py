"""The library derivation on Softanza itself (D32, HF-123): a METHOD point in base/common/stzCancelToken.ring -- a class file that runs nothing --
refined through the program that loads it (stzLib.ring) with the engine's own native list. The file on disk is never written: the tags and the
refinements live in the model, and the derivation checks the unit with the file's text replaced (`rnxc check --closed --subst`).

    python haro/spike/v20/probes/library_softanza.py [<stzlib folder>]      RNXC=<rnxc> picks the compiler

The library is the INSTALLED one (D:/ringpp/ringpp-win64/libraries/stzlib, Softanza main) unless a folder is given: read, never written. The
native list is taken from a run of the install's own rnxc that loads the library and prints cfunctions() (0.4 s on its prefix), into scratch/.
A named SKIP when the install is not on this machine. ~1.5 minutes: each derivation checks the whole unit (697 files), ~16 s."""
import os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
V20 = os.path.dirname(HERE)
sys.path.insert(0, V20)
import refine

INSTALL = r'D:/ringpp/ringpp-win64'
LIB = sys.argv[1] if len(sys.argv) > 1 else INSTALL + '/libraries/stzlib'
F = LIB + '/base/common/stzCancelToken.ring'
if not os.path.isfile(F) or not os.path.isfile(INSTALL + '/bin/rnxc.exe'):
    print('library_softanza: SKIP -- no Softanza install at %s' % INSTALL)
    sys.exit(0)
scratch = os.path.join(V20, 'scratch', 'libsoftanza')
os.makedirs(scratch, exist_ok=True)
nat = os.path.join(scratch, 'natives.txt')
probe = os.path.join(scratch, 'natives_probe.ring')
open(probe, 'wb').write(b'load "stzlib.ring"\naC = cfunctions()\nfor c in aC\n\t? c\nnext\n')
env = dict(os.environ, PATH=os.path.join(os.environ.get('SystemRoot', r'C:\Windows'), 'System32'))
r = subprocess.run([INSTALL + '/bin/rnxc.exe', probe], cwd=scratch, capture_output=True, env=env, timeout=900)
open(nat, 'wb').write(r.stdout)
nnat = len(r.stdout.split())
unit = {'root': LIB + '/stzLib.ring', 'file': F, 'natives': nat}

canon = refine.Model(open(F, 'rb').read().decode('latin-1')).text()
lines = canon.split('\n')
lines.insert(next(i for i, l in enumerate(lines) if re.match(r'^\tfunc init\(\)$', l)), '\t# <R:METHOD name="ZzBudget" params="n" calls="StzRetryBudget">')
lines.insert(next(i for i, l in enumerate(lines) if re.match(r'^\tfunc _Ensure\(\)$', l)), '\t# <R:METHOD name="ZzSignal" params="n" calls="stzenginecancelsignal">')
text = '\n'.join(lines)
on_disk = open(F, 'rb').read()
m = refine.Model(text, {}, unit)
bad = []
if m.text() != text:
    bad.append('the tagged text is not its own canonical text')
print('the engine registers %d native name(s)' % nnat)


def sentence(k, target, to, why):
    return ('DEFINE REFINE r%d AS ( TARGET "%s", KIND method, FROM "absent", TO "%s", AUTHOR "mansour", POSTURE trusted, REASON "%s" )'
            % (k, target, to, why))


WANT = [('ZzBudget', 'oB = StzRetryBudget(n) return oB', 'a budget, one argument short', 'rejected', 'derivation', 'StzRetryBudget() takes 2'),
        ('ZzBudget', 'oB = StzRetryBudget(n, 60) return oB', 'a budget over a minute', 'admitted', None, ''),
        ('ZzSignal', 'stzenginecancelsignal(n)', 'the engine raises the flag', 'admitted', None, '')]
for k, (target, to, why, status, stage, words) in enumerate(WANT, 1):
    t = time.time()
    o = m.refine(sentence(k, target, to, why))
    print('%d. %-8s %-38s -> %s%s  (%.1f s)' % (k, target, to, o.status, '' if o.admitted else ' at %s: %s' % (o.stage, o.why[:110]), time.time() - t))
    if o.status != status or (stage and (o.stage != stage or words not in o.why)):
        bad.append('step %d: %s at %s, want %s %s' % (k, o.status, o.stage, status, stage or ''))

m2 = refine.Model(text.replace('calls="stzenginecancelsignal"', 'calls="StzEngineCancelSignal"'), {}, unit)
errs = [e['msg'] for e in m2.lift()['errors'] if not e['own']]
print("the native spelt as Softanza spells it: %s" % (errs[0] if errs else 'lifts'))
if not (errs and "is declared 'stzenginecancelsignal'" in errs[0]):
    bad.append('a native spelt by case folding was not refused by name (D24)')
m3 = refine.Model(text, {})
o = m3.refine(sentence(9, 'ZzBudget', 'oB = StzRetryBudget(n, 60) return oB', 'alone'))
print('the same refinement, the file asked about alone: %s at %s' % (o.status, o.stage))
if o.admitted:
    bad.append('alone, a call into another file was admitted')
if open(F, 'rb').read() != on_disk:
    bad.append('the file on disk changed')
for b in bad:
    print('  FAIL ' + b)
print('library_softanza: %s' % ('PASS' if not bad else 'FAILED'))
sys.exit(1 if bad else 0)
