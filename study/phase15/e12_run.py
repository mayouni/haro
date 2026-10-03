"""Phase 1.5, E1 (the knowledge graph) and E2 (stzNatural as shipped, then retargeted by data): run on the
Ring++ package and check each fact the study cites. Exit 1 on any failure.

Usage: python haro/study/phase15/e12_run.py
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PACKAGE_RNXC = os.path.join(ROOT, 'runtime', 'package', 'ringpp-win64', 'bin', 'rnxc.exe')
fails = []


def check(ok, text):
    print(('  ok   ' if ok else '  FAIL ') + text)
    if not ok:
        fails.append(text)


def run(script):
    env = dict(os.environ)
    env.pop('RNXC_NOCACHE', None)
    p = subprocess.run([PACKAGE_RNXC, script], capture_output=True, cwd=HERE, env=env, timeout=900)
    return p.returncode, p.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')


def line(out, prefix):
    for l in out.split('\n'):
        if l.startswith(prefix):
            return l[len(prefix):].strip()
    return None


# ---- E1 ---------------------------------------------------------------------------------------------------
art = os.path.join(HERE, 'data', 'tontine.zknw')
before = open(art, 'rb').read() if os.path.exists(art) else b''
rc, out = run('e1_graph.ring')
out_e1 = out
after = open(art, 'rb').read()
print('E1 -- the tontine knowledge graph, stzKnowledgeGraph')
check(rc == 0, f'the experiment runs on Ring++ (exit {rc})')
check(line(out, 'E1a facts=') == '19', 'E1a the ontology and facts: 19 facts (11 is-a, 3 received_pot_in, 3 guarantees, 2 holds_role)')
check('moussa' in (line(out, 'E1c who received the pot in round2') or '') and 'boubacar' in (line(out, 'E1c who guarantees sanda') or '')
      and 'zeinab' in (line(out, 'E1c who is the treasurer') or ''),
      'E1c a triple pattern is a closed query: the round-2 beneficiary is moussa, sanda\'s guarantor boubacar, the treasurer zeinab')
check((line(out, 'E1c does boubacar guarantee sanda') == '1'), 'E1c a fully bound pattern answers 1 (true)')
check(line(out, 'E1d reloaded facts=').startswith('19 (original 19)') and 'moussa' in (line(out, 'E1d same answer after reload:') or ''),
      'E1d the artifact reloads to the same 19 facts and answers the same')
check(line(out, 'E1e law survives the artifact? unique=') == '1' and b'received_pot_in | unique' in after,
      'E1e the :Unique law travels in the artifact (an `ontology` section of the .zknw)')
check(re.search(r'E1e property survives the artifact\? <>', out) is not None and line(out, 'E1e property on the live graph') == 'Moussa',
      'E1e a node property (the ledger\'s spelling "Moussa") exists on the live graph and does NOT survive the artifact')
check(line(out, 'E1b a second pot for fatima:').startswith('admitted=0') and 'already bears' in out,
      'E1b the law judges a fact: a second pot for fatima is refused, with the reason')
check('admitted=1' in (line(out, 'E1b round3 already has aminata; a second beneficiary for it:') or ''),
      'E1b but :Unique is the subject\'s side only: a second beneficiary for round 3 is ADMITTED (one-per-round is not expressible)')
qp = next((l for l in out.splitlines() if 'QueryPath answers' in l), '')
jw = next((l for l in out.splitlines() if 'a join would add' in l), '')
check('[ "fatima" ]' in qp and '"zeinab"' not in qp and 'zeinab' in jw,
      'E1f QueryPath answers the first pattern only (fatima): the join to zeinab does not happen')
check('raised=<>' in out_e1 and 'facts loaded=2' in out_e1 and 'law present=1' in out_e1,
      'E1g a world is not judged when it is LOADED: an artifact that breaks its own :Unique law loads, both facts, no refusal')
check(before == after or before == b'', 'E1d the artifact data/tontine.zknw regenerates byte-identically (' + str(len(after)) + ' bytes, ' + str(after.count(b'\n')) + ' lines)')

# ---- E2 ---------------------------------------------------------------------------------------------------
print('E2 -- stzNatural as shipped, and with the tontine vocabulary as data')
rc, out = run('e2_stznatural.ring')
check(rc == 0, f'the experiment runs on Ring++ (exit {rc})')
a = [l for l in out.split('\n') if l.startswith('E2a ')]
check(len(a) == 2 and all('RAISED Unsupported object type!' in l for l in a),
      'E2a a tontine question executed as shipped is refused (English and French): "Unsupported object type!"')
check("not understood: 'deposits' 'over'" in (line(out, 'E2b ') or '') and 'did you mean' in (line(out, 'E2b ') or ''),
      'E2b strict mode names the words it did not understand (and guesses "power" for "over", from a lexicon of string verbs)')
check(line(out, 'E2c pairs with one semantic form in both languages:') == '3 of 3', 'E2c the tontine vocabulary as two packs, data only: 3 of 3 questions give ONE semantic form in English and French')
d = {k: line(out, f'E2d {k}:') or '' for k in ('plain', 'quoted', 'bracketed')}
check(d['plain'].endswith('marker=0') and d['quoted'].endswith('marker=0') and d['bracketed'].endswith('marker=1') and 'literal:[ 5000 ]' in d['bracketed'],
      'E2d the shipped tokenizer is NOT closed: a bracketed section of the question ran code in a dry run (Marker() called once) and its return value became the literal')
print(f'e12: {"FAIL" if fails else "PASS"} ({len(fails)} failure(s))')
sys.exit(1 if fails else 0)
