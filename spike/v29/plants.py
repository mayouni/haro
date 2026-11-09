"""Every protection of the v0.29 weave judgements switched off in turn: the meta fixtures must fail, for the fixture that protection exists for
(the W discipline: a protection no fixture pins is not a protection).

Each plant is one text substitution in spike/haro_lib.haro, applied to the file in place, the v29 fixtures judged on haro, and the file
restored byte for byte before the next plant (verified by its digest, and restored even if the script is stopped). A plant that makes a
refusal a note keeps the message and the line and changes only the severity handed to StzuWeave: the rule still SEES the defect.

Printed is CAUGHT with the fixtures that failed, or MISSED: a protection no fixture pins, and the answer to it is a fixture.

  python spike/v29/plants.py            all plants
  python spike/v29/plants.py P3 P7      some
"""
import contextlib, hashlib, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
sys.path.insert(0, SPIKE)
os.chdir(SPIKE)
import haro_forge as hf                                    # noqa: E402

LIB = os.path.join(SPIKE, 'haro_lib.haro')

# (id, the fixture(s) it must fail, what the plant takes away, old text, new text) -- every old text appears exactly once
PLANTS = [
    ('P1', ['R1'], 'W1.5 never looks at a warning CONSTRAINT',
     'if aConstraints[j][9] = "warning" and isList(aConstraints[j][8])', 'if 0'),
    ('P2', ['A5'], 'W1.5 refuses a cite of an article the world does not stand under',
     'if InStrList(aAn[nCA], aArts)', 'if 1'),
    ('P3', ['R2'], 'W2.2 never looks at a floor llm',
     'if aFlO[j][3] = "llm"', 'if 0'),
    ('P4', ['R3'], 'W2.3 is demoted to a note whatever the weave\'s severity',
     'StzuWeave(tWS, aRefine[3], "W2.3 observability', 'StzuWeave("advisory", aRefine[3], "W2.3 observability'),
    ('P5', ['R4'], 'W5.2 is demoted to a note whatever the weave\'s severity',
     'StzuWeave(tWS, aRefine[3], "W5.2 temporal_integrity', 'StzuWeave("advisory", aRefine[3], "W5.2 temporal_integrity'),
    ('P6', ['R5'], 'W7.4 never asks whether a world that denies has a voice',
     'if nDen > 0 and isNull(aNarrate)', 'if 0'),
    ('P7', ['R6'], 'W7.4 never asks a REFUSAL for its CODE',
     'if aRefusals[j][6] = ""\n\t\t\t\t\t\t\tStzuWeave(tWS', 'if 0\n\t\t\t\t\t\t\tStzuWeave(tWS'),
    ('P8', ['A4'], 'W7.4 never asks a CONSTRAINT for its CODE',
     'if aConstraints[j][7] = ""\n\t\t\t\t\t\t\tStzuWeave(tWS', 'if 0\n\t\t\t\t\t\t\tStzuWeave(tWS'),
    ('P9', ['R7', 'A3'], 'W8.5 never looks at a policy point floored llm',
     'if aFlS[k][1] = aPtS[j][1] and aFlS[k][2] = aPtS[j][2] and aFlS[k][3] = "llm"', 'if 0'),
    ('P10', ['R9'], 'a weave none of whose rules is judged is no longer refused by name',
     'if len(aWR[1]) + len(aWR[2]) = 0', 'if len(aWR[1]) + len(aWR[2]) = 99'),
    ('P11', ['A1', 'A2', 'A3', 'A4', 'A5', 'A7'], 'the court prints no line of the rules it judges',
     '? "judged " + tJudged', '? "judgedx " + tJudged'),
    ('P12', ['A1', 'A4', 'A5', 'A7'], 'W1.2 and W7.1 are no longer named as held by construction',
     'return [["W1.5"], ["W1.2"], [', 'return [["W1.5"], [], ['),
    ('P13', ['A1'], 'W2.2 and W2.3 are not both named',
     'return [["W2.2", "W2.3"], [], [', 'return [["W2.2"], [], ['),
    ('P14', ['A8'], 'a cite is read without its kind: any cite names an article',
     'if left(tCite, 8) != "article:" return 0 ok', ''),
    ('P15', ['R8'], 'Art. 4 is demoted to a note: the article no longer refuses the model on a policy point',
     'StzuFail(aFls[k][4], "Art. 4 predictable_authority', 'StzuWeave("advisory", aFls[k][4], "Art. 4 predictable_authority'),
]


def judge():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        hf.judge_stzu(hf.HARO_VM, 'haro', hf.STZU29_FIXTURES)
    return sorted(set(re.findall(r'^  FAIL (\w+) ', buf.getvalue(), re.M)), key=lambda s: (s[0], int(s[1:]))), buf.getvalue()


def main():
    want = [a for a in sys.argv[1:] if not a.startswith('-')]
    original = open(LIB, 'rb').read()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode('utf-8')
    nl = '\r\n' if '\r\n' in text else '\n'
    base, _ = judge()
    print(f'unplanted: {len(base)} fixture(s) fail', base if base else '')
    if base:
        print('the court must pass its fixtures before it is planted')
        return 1
    missed = 0
    try:
        for pid, fixtures, what, old, new in PLANTS:
            if want and pid not in want:
                continue
            old_n, new_n = old.replace('\n', nl), new.replace('\n', nl)
            if text.count(old_n) != 1:
                print(f'{pid}: ANCHOR NOT UNIQUE ({text.count(old_n)}): {old[:60]!r}')
                missed += 1
                continue
            open(LIB, 'wb').write(text.replace(old_n, new_n).encode('utf-8'))
            failed, _ = judge()
            open(LIB, 'wb').write(original)
            hit = [f for f in fixtures if f in failed]
            if hit:
                print(f'{pid} CAUGHT by {",".join(hit)} ({len(failed)} fail): {what}')
            else:
                print(f'{pid} MISSED (failed: {failed}): {what}')
                missed += 1
    finally:
        open(LIB, 'wb').write(original)
        assert hashlib.sha256(open(LIB, 'rb').read()).hexdigest() == digest, 'haro_lib.haro was not restored'
    print('restored byte for byte;', 'every plant caught' if not missed else f'{missed} MISSED')
    return 1 if missed else 0


if __name__ == '__main__':
    sys.exit(main())
