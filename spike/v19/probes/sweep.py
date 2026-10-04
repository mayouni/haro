"""What the two thresholds cost and buy: Haro's history replayed with SIM_MIN and RENAME_MIN moved.
   python haro/spike/v19/probes/sweep.py        graphs come from the scratch cache, so this is seconds once ids_check has run"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import ids_check as ck, ids
sys.setrecursionlimit(100000)
srcs = ck.hand_written()
print('SIM_MIN  RENAME_MIN   statements kept   by similarity   definitions kept')
for sim in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.01):
    ids.SIM_MIN = sim
    ids.RENAME_MIN = 0.6
    t = ck.replay(srcs, 7)
    r, same = ck.share(t)
    print(f"  {sim:4.2f}      0.60        {r*100:6.2f}%  (same text {same*100:5.2f}%)   {t['how'].get('similar', 0):5d}       {ck.share(t, 'definition')[0]*100:6.2f}%")
ids.SIM_MIN = 0.6
for ren in (0.3, 0.5, 0.6, 0.8, 1.01):
    ids.RENAME_MIN = ren
    t = ck.replay(srcs, 7)
    r, same = ck.share(t)
    print(f"  0.60      {ren:4.2f}        {r*100:6.2f}%  (same text {same*100:5.2f}%)   {t['how'].get('similar', 0):5d}       {ck.share(t, 'definition')[0]*100:6.2f}%   renames {t['how'].get('rename', 0)}")
ids.RENAME_MIN = 0.6
print('\nwhat each pass buys (every other pass on):')
for label, kw in (('everything', {}), ('no move pass (C)', {'USE_MOVE': False}), ('no function pool (D)', {'USE_POOL': False}),
                  ('neither C nor D', {'USE_MOVE': False, 'USE_POOL': False}), ('no similarity (B2)', {'SIM_MIN': 1.01}),
                  ('name and text only', {'USE_MOVE': False, 'USE_POOL': False, 'SIM_MIN': 1.01, 'RENAME_MIN': 1.01})):
    saved = {k: getattr(ids, k) for k in kw}
    for k, v in kw.items():
        setattr(ids, k, v)
    t = ck.replay(srcs, 7)
    r, same = ck.share(t)
    print(f'  {label:24s} statements {r*100:6.2f}%   definitions {ck.share(t, "definition")[0]*100:6.2f}%   comments {ck.share(t, "comment")[0]*100:6.2f}%')
    for k, v in saved.items():
        setattr(ids, k, v)
