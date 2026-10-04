import glob, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import l1_check as ck
STZ = r'D:\GitHub\stzlib\libraries\stzlib'
files = []
for sub in sys.argv[1:]:
    files += glob.glob(os.path.join(STZ, sub, '**', '*.ring'), recursive=True)
files = sorted(files, key=os.path.getsize)
def main():
    for p in files:
        if os.path.getsize(p) <= 120000: continue
        t0 = time.time()
        try:
            st, why = ck.round_trip(ck.read_text(p), 'big', path=p)
        except Exception as e:
            st, why = 'tool', repr(e)[:200]
        print(f'{os.path.getsize(p)//1000:6d} KB {time.time()-t0:5.0f} s {st} {str(why)[:160]} {os.path.relpath(p, STZ)}', flush=True)
sys.setrecursionlimit(200_000); threading.stack_size(128*1024*1024)
t = threading.Thread(target=main); t.start(); t.join()
