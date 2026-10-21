"""C-33: `new K()` on a class with no `init` -- keep. Also marks F-131 decided."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CR, LF = chr(13), chr(10)


def edit(path, fn):
    raw = io.open(path, encoding='utf-8', newline='').read()
    nl = CR + LF if CR + LF in raw else LF
    s = fn(raw.replace(CR + LF, LF))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
    print('edited', os.path.relpath(path, ROOT))


ENTRY = '''## C-33 - `new K()` on a class with no `init` makes the object

**Verdict: keep. Decided 2026-10-21 by the session, on the author's delegation ("decide on my behalf").**
F-131: with an empty parenthesis the constructor is asked for; Ring 1.27 has none to call and raises `Error (R3) : Calling Function without
definition: init`, Ring++ makes the object and goes on (`new K` without parentheses makes it on both, and neither calls `init`; where `init` exists
`new K()` and `new K(1)` call it on both). **Why keep:** the difference is on the permissive side -- a program that runs on Ring never meets it, because
Ring stops there -- so it cannot fail one that passes on Ring, and the estate's wide suite passes every assertion Ring passes. Raising R3 here would
make Ring++ refuse something its own `new K` form allows, for no program's benefit. **What it costs:** a Ring++ program written to rely on it does not run on
Ring (Ring is retired for the author's projects, so that is a portability note, not a loss), and a model that writes `new K()` for a class with no
constructor is not told it was wrong -- the K4 cloud rows rose from 19 to 20 of 20 on this alone. **The other half is Haro's and is decided there:** Haro's
`new(Name)` is the constructor call, and for a class with no constructor it refuses loudly (D24: one exact spelling, refuse loudly), as the face's reader
already does when it reads `new(Name)` as `new K()` and the target has none; `new_without_init(Name)` stays the spelling of "make it, call nothing".
**The pattern it hurts:** none measured. **The guard:** `haro/spike/v22/scratch/probe_new.py` runs the five shapes on both runtimes and prints the one difference.

---

'''


def corrections(s):
    marker = '\n---\n\n## C-10 '
    assert s.count(marker) == 1
    return s.replace(marker, '\n---\n\n' + ENTRY + '## C-10 ')


def findings(s):
    a = '**Not decided here**: keep (the permissive side cannot fail a program that passes on Ring), or raise R3 as Ring does -- a Haro question as much as\na Ring++ one, because Haro\'s `new(Name)` must say what it means for a class with no constructor. Proposed: keep on Ring++, and let Haro refuse it loudly (D24: one exact spelling, refuse loudly).'
    assert s.count(a) == 1, s.count(a)
    return s.replace(a, '**Decided 2026-10-21 as C-33: keep** (the permissive side cannot fail a program that passes on Ring), and let Haro refuse it loudly -- its `new(Name)` is the constructor call (D24: one exact spelling, refuse loudly).')


edit(os.path.join(ROOT, 'docs', 'CORRECTIONS.md'), corrections)
edit(os.path.join(ROOT, 'docs', 'FINDINGS.md'), findings)
