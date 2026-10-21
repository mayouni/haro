"""The pool margin: a quarter more is not enough for a short prompt (a 368-token prompt on the 1.5B was 1.1 MB short even with it); the engine copy now carries a constant gigabyte too.
Corrects ENGINE_NOTES.md, K4.md, HF-113 and the stzlib session prompt (55)."""
import io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CR, LF = chr(13), chr(10)


def edit(path, fn):
    raw = io.open(path, encoding='utf-8', newline='').read()
    nl = CR + LF if CR + LF in raw else LF
    s = fn(raw.replace(CR + LF, LF))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(LF, nl))
    print('edited', path)


def rep(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:80])
    return s.replace(a, b)


def notes(s):
    s = rep(s, '    const mem_size_est: usize = 128 * 1024 * 1024 + kv_len * n_new * n_head * n_layer * 24 + n_new * n_embd * n_layer * 64;\n    const mem_size: usize = mem_size_est + mem_size_est / 4;',
            '    const mem_size_est: usize = 128 * 1024 * 1024 + kv_len * n_new * n_head * n_layer * 24 + n_new * n_embd * n_layer * 64;\n    const mem_size: usize = mem_size_est + mem_size_est / 4 + 1024 * 1024 * 1024;')
    return s.replace('A quarter more of a pool that is not touched is address space', '**A quarter more was not enough, and the first version of this fix was wrong for short prompts:** a 368-token prompt on the 1.5B (the rung 5 agent tasks) failed with a quarter more by 1.1 MB (`needed 2800125616, available 2799001600`), because the estimate under-counts something that does not grow with the prompt, so a percentage margin only works for long ones; the copy carries a constant gigabyte as well. A pool that is not touched is address space', 1)


def k4(s):
    return rep(s, 'the Ring++ copy of the engine carries a 25 percent margin', 'the Ring++ copy of the engine carries a margin (a quarter more, then a constant gigabyte as well: the quarter alone failed a 368-token prompt)')


def hf(s):
    return rep(s, 'A quarter more in the engine COPY (stz_neural rebuilt in 29 s, the original DLL kept beside it) runs the 1.5B;', 'A quarter more in the engine COPY runs it for prompts of about 400 tokens and over and fails a 368-token one by 1.1 MB (found by the rung 5 agent tasks): the copy carries a quarter and a constant gigabyte (stz_neural rebuilt in 29 s, the original DLL kept beside it);')


def prompt55(s):
    return rep(s, 'or at least the interim `+ est/4` the ringpp copy carries.', 'or at least the interim the ringpp copy carries, `est + est/4 + 1 GiB` (`est/4` alone failed a 368-token prompt on the 1.5B by 1.1 MB: the estimate under-counts something that does not grow with the prompt).')


edit(os.path.join(ROOT, 'haro', 'spike', 'v22', 'k4', 'ENGINE_NOTES.md'), notes)
edit(os.path.join(ROOT, 'haro', 'spike', 'v22', 'k4', 'K4.md'), k4)
edit(os.path.join(ROOT, 'haro', 'FINDINGS.md'), hf)
edit(r'D:\GitHub\softanza\prompts\55-stzlib-small-model-plane.md', prompt55)
