import glob, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import l1_check as ck
step, start = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 0
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 60_000
root = sys.argv[4] if len(sys.argv) > 4 else ck.STZ
files = sorted(glob.glob(os.path.join(root, '**', '*.ring'), recursive=True))
files = [p for p in files[start::step] if os.path.getsize(p) <= limit]
print(len(files), 'files')
def main():
    t0 = time.time(); bad = []; cat = {}
    for p in files:
        dis_on = True
        try:
            st, why = ck.round_trip(ck.read_text(p), 'stress', path=p)
        except Exception as e:
            st, why = 'tool', repr(e)[:200]
        if st is None:
            k = 'exact, code compared (loads blanked)' if ck.has_loads(p) else 'exact, code compared'
        elif st == 'skipped':
            k = ('refused by Ring itself' if 'Ring itself' in str(why) else
                 'rnxc refuses part of it (graph exact, code not compared)' if 'rnxc refuses' in str(why) else
                 'does not compile alone (graph exact, code not compared)')
        else:
            k = 'FAIL'; bad.append((p, st, why)); print('FAIL', p, st, str(why)[:260], flush=True)
        cat[k] = cat.get(k, 0) + 1
    print(cat)
    print(f'{len(files)} files, failed {len(bad)} in {time.time()-t0:.0f} s')
import sys as _s
_s.setrecursionlimit(200_000); threading.stack_size(128*1024*1024)
t = threading.Thread(target=main); t.start(); t.join()
