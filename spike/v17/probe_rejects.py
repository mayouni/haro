"""Exploration (not the judge): one defect at a time put into n/tontine.n, and what the forged N court says.
Run from anywhere: python haro/spike/v17/probe_rejects.py"""
import os, subprocess, sys, tempfile

SP = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(SP))
import paths
RNXC = paths.RNXC
SENT = open(os.path.join(SP, 'n', 'tontine.n'), encoding='utf-8', newline='').read()

DEFECTS = [
    ('dangling tongue in a column', 'WORDS [english: "who", french: "qui"]', 'WORDS [english: "who", german: "wer"]'),
    ('frame shape names no meaning', 'SHAPE [show, deposit, over, num], TARGET ledger', 'SHAPE [show, deposit, ovr, num], TARGET ledger'),
    ('frame aimed at no surface', 'SHAPE [show, deposit], TARGET ledger,', 'SHAPE [show, deposit], TARGET ledgr,'),
    ('example means no frame', 'MEANS ledger_over,\n  ASKING [english: "show deposits over 5000"', 'MEANS ledger_ovr,\n  ASKING [english: "show deposits over 5000"'),
    ('step aimed at no surface', 'TARGET graph, QUERY "?x received_pot_in round{num}", BINDS member', 'TARGET grph, QUERY "?x received_pot_in round{num}", BINDS member'),
    ('surface tells in no tongue', 'TELLS [english, french]', 'TELLS [english, german]'),
    ('meaning draws from no surface', 'SLOT entity, OF member, FROM graph', 'SLOT entity, OF member, FROM grph'),
    ('alias of no meaning', 'MEANING role, ENTITY "treasurer"', 'MEANING rol, ENTITY "treasurer"'),
    ('a declaration N does not have (N never declares)', 'DEFINE STEP find_beneficiary AS (', 'DEFINE NORM positive_deposit AS (RULE "amount > 0") RATIONALE "x"\n\nDEFINE STEP find_beneficiary AS ('),
    ('a text slot (a free string)', 'DEFINE MEANING num AS (\n  SLOT number', 'DEFINE MEANING num AS (\n  SLOT text'),
    ('a digit set the court does not know', 'DIGITS ascii,\n  NAMES upper_first,\n  REFUSES [\n    character: "the question', 'DIGITS arabic_indic,\n  NAMES upper_first,\n  REFUSES [\n    character: "the question'),
    ('a refusal kind that does not exist', 'ambiguous: "the question needs one answer', 'name: "the question needs one answer'),
    ('a spelling that does not exist', 'SPELLS [member: upper_first],', 'SPELLS [member: shouting],'),
    ('a meaning with no slot', 'DEFINE MEANING show AS (\n  SLOT none,', 'DEFINE MEANING show AS ('),
    ('a surface with no court', 'KIND query, GRAMMAR "ZQL ASK", COURT "z_court.ring ask",', 'KIND query, GRAMMAR "ZQL ASK",'),
    ('a declaration without a rationale', 'DEFINE ALIAS collector AS (\n  MEANING role, ENTITY "collector",\n  WORDS [english: "collector", french: "collecteur"]\n) RATIONALE "The member who takes the deposits"', 'DEFINE ALIAS collector AS (\n  MEANING role, ENTITY "collector",\n  WORDS [english: "collector", french: "collecteur"]\n)'),
    ('a name declared twice', 'DEFINE MEANING under AS (', 'DEFINE MEANING over AS ('),
]
only = sys.argv[1:]
with tempfile.TemporaryDirectory() as td:
    for label, old, new in DEFECTS:
        if SENT.count(old) != 1:
            print(f'!! anchor for {label!r} found {SENT.count(old)} times')
            continue
        p = os.path.join(td, 'x.n')
        open(p, 'w', encoding='utf-8', newline='').write(SENT.replace(old, new))
        r = subprocess.run([RNXC, 'n_court.ring', 'check', p], capture_output=True, cwd=SP, env=dict(os.environ, RNXC_NOCACHE='1', HARO_NOCACHE='1'), timeout=120)
        o = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip().splitlines()
        first = o[0] if o else ''
        print(f'{label:52s} -> {first[:170]}')
