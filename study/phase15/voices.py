"""Phase 1.5, voices: the answer OUT, in the language of the question.

Haro v0.16's NARRATE tells how a question was answered, in the voice a language declares -- and a
language has ONE voice (v0.13, R3). So a second human language is a second declaration: this derives a
French twin of z_v16.haro (same world, same ASK, a French voice), forges it into a scratch folder with
copies of the court's libraries -- nothing is written to haro/spike -- and offers both voices.
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))   # this repository's root, for paths.py
import paths                                   # where Ring++ is (Haro is its own repository since 2026-11-02)
ROOT = paths.RINGPP
SPIKE = paths.SPIKE
RNXC = paths.HARO_VM
ORACLE = paths.RING_ORACLE
OUT = os.path.join(HERE, 'scratch', 'voices')
LIBS = ('court_lib.haro', 'cond_lib.haro', 'expr_lib.haro', 'world_lib.haro', 'ask_lib.haro', 'narrate_lib.haro')

FRENCH_VOICE = '''DEFINE NARRATE telling AS (
  TELLS [
    ask: "Question posée à {from} : {question}",
    matched: "{count} lignes sur {total} correspondent.",
    ordered: "Triées par {field}, ordre {direction}.",
    cut: "Seules les {limit} premières sont gardées ({dropped} écartées).",
    answer: "La réponse tient en {count} ligne(s) : {rows}"
  ],
  REFUSES "Je m'arrête : {message} ({code})"
) RATIONALE "Une question racontée comme la raconterait une personne : combien de lignes correspondent sur combien, comment elles sont triées, combien sont gardées, et la réponse -- la même réponse que `ask`, enregistrée pendant que la question s'exécute"
'''


def build():
    """Forge the French twin into scratch/voices; returns the folder."""
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    src = open(os.path.join(SPIKE, 'z_v16.haro'), encoding='utf-8').read()
    twin, n = re.subn(r'DEFINE LANGUAGE z AS \(', 'DEFINE LANGUAGE zfr AS (', src, count=1)
    assert n == 1
    i = twin.index('DEFINE NARRATE telling AS (')
    twin = twin[:i] + FRENCH_VOICE
    twin = '-- zfr: z_v16.haro with a French voice (Phase 1.5). Derived by voices.py; not a declaration of the spike.\n' + twin
    haro = os.path.join(OUT, 'zfr.haro')
    open(haro, 'w', encoding='utf-8', newline='').write(twin)
    r = subprocess.run([RNXC, 'forge.haro', haro, OUT], capture_output=True, cwd=SPIKE, env=dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1'), timeout=300)
    o = r.stdout.decode('utf-8', 'replace')
    assert o.startswith('forged zfr'), o[:200]
    for lib in LIBS:
        shutil.copy(os.path.join(SPIKE, lib), OUT)
    shutil.copy(os.path.join(SPIKE, 'tontine.z'), OUT)
    return OUT


def tell(exe, lang, question, rows_json):
    """narrate-ask in the voice of the question's language; 'en' is the spike's z court, 'fr' the twin."""
    if lang == 'tn-fr':
        court, cwd = 'zfr_court.haro', OUT
    else:
        court, cwd = 'z_court.haro', SPIKE
    r = subprocess.run([exe, court, 'narrate-ask', 'tontine.z', question, rows_json], capture_output=True, cwd=cwd, env=dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1'), timeout=120)
    return r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip()


if __name__ == '__main__':
    import json, sys
    build()
    rows = json.load(open(os.path.join(SPIKE, 'v07', 'q_cases.json'), encoding='utf-8'))['rows']
    q = 'SELECT * FROM collect WHERE amount > 5000'
    for lang in ('tn-en', 'tn-fr'):
        for exe in (RNXC, ORACLE):
            print('==', lang, os.path.basename(exe))
            print(tell(exe, lang, q, json.dumps(rows))[:600])
