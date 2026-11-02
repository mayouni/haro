"""COMPASS-REBOL-06, measured before it is designed: the three textual shapes of the family as they stand, read-only.

  C6     the declaration shape: Haro's meta-language (.haro), every letter's sentences, the machine language (.stzu), and the
         three elders the Commons was extracted from (.zql, .wflow, .zui)
  memo   the indentation shape C9's output schemas and .pia agents share, read as _StzOutputParseMemo reads it: the yaml
         fences of the journal and the mailboxes, and every .pia file
  face   a program's spelling (Ring++ today): asked only whether the one LOAD reads it

For each: how many texts the one LOAD reads, why it refuses the rest, and whether a text survives the trip text -> block ->
canonical text -> block (its own spelling, and for memos the crossing into C6). Writes results.json.

  python census.py
"""
import collections, glob, json, os, re, time
from block import load, load_memo, print_c6, print_memo, Refused

HERE = os.path.dirname(os.path.abspath(__file__))
GH = 'D:/GitHub'
SPIKE = os.path.join(GH, 'ringpp', 'haro', 'spike')
SENTENCE_EXT = ('.z', '.f', '.a', '.n', '.stzv', '.machine', '.fleet', '.ledger', '.bank', '.clinic', '.notice', '.w')


def files(pattern):
    return sorted(set(glob.glob(pattern, recursive=True)))


def read(p):
    return open(p, encoding='utf-8', errors='replace').read()


def reason(e):
    s = re.sub(r'^line \d+: ', '', str(e))
    s = re.sub(r"'[^']*'", "'_'", s)
    return s[:90]


def c6_family(name, paths):
    acc = trip = 0
    why = collections.Counter()
    bytes_in = bytes_canon = 0
    trips_failed = []
    for p in paths:
        t = read(p)
        try:
            vals = load(t)
        except Refused as e:
            why[reason(e)] += 1
            continue
        acc += 1
        try:
            canon = print_c6(vals)
            if load(canon) == vals:
                trip += 1
                bytes_in += len(t.encode('utf-8')); bytes_canon += len(canon.encode('utf-8'))
            else:
                trips_failed.append(os.path.basename(p))
        except Refused as e:
            trips_failed.append(os.path.basename(p) + ': ' + str(e))
    return {'family': name, 'files': len(paths), 'loaded': acc, 'round_trip': trip, 'refused_why': dict(why.most_common(8)),
            'round_trip_failed': trips_failed[:8], 'bytes': bytes_in, 'canonical_bytes': bytes_canon}


def yaml_fences(paths):
    out = []
    for p in paths:
        t = read(p).replace('\r\n', '\n')
        for m in re.finditer(r'```yaml\n(.*?)```', t, re.S):
            out.append((p, m.group(1)))
    return out


def memo_family(name, texts, house=False):
    acc = own = cross = 0
    why, cross_why = collections.Counter(), collections.Counter()
    keys = nonident = 0
    for p, t in texts:
        try:
            vals = load_memo(t, house)
        except Refused as e:
            why[reason(e)] += 1
            continue
        acc += 1

        def walk(v):
            nonlocal keys, nonident
            if v[0] == 'pair':
                keys += 1
                nonident += v[1][0] == 'str'
                walk(v[2])
            elif v[0] in ('group', 'list'):
                for x in v[1]:
                    walk(x)
        walk(vals[0])
        try:
            if load_memo(print_memo(vals), house) == vals:
                own += 1
        except Refused as e:
            why['own printing: ' + reason(e)] += 1
        try:
            if load(print_c6(vals)) == vals:
                cross += 1
        except Refused as e:
            cross_why[reason(e)] += 1
    return {'family': name + (', the house reading' if house else ', as C9 reads it'), 'texts': len(texts), 'loaded': acc, 'own_round_trip': own, 'into_c6_and_back': cross,
            'refused_why': dict(why.most_common(8)), 'c6_crossing_refused_why': dict(cross_why.most_common(6)),
            'keys': keys, 'keys_not_c6_identifiers': nonident}


def face_sample(paths, n=300):
    paths = paths[::max(1, len(paths) // n)][:n]
    acc = 0
    why = collections.Counter()
    for p in paths:
        try:
            load(read(p)); acc += 1
        except Refused as e:
            why[reason(e)] += 1
    return {'family': 'Ring++ face (Softanza base, a sample)', 'files': len(paths), 'loaded': acc,
            'refused_why': dict(why.most_common(6))}


def main():
    t0 = time.time()
    res = {'when': time.strftime('%Y-%m-%d %H:%M'), 'c6': [], 'memo': [], 'face': None}
    haro = files(SPIKE + '/**/*.haro') + files(SPIKE + '/*.haro')
    sentences = [p for p in files(SPIKE + '/**/*') if os.path.splitext(p)[1] in SENTENCE_EXT]
    res['c6'].append(c6_family("Haro's meta-language (.haro, the spike)", sorted(set(haro))))
    res['c6'].append(c6_family("the letters' sentences (the spike's worlds)", sentences))
    res['c6'].append(c6_family('the machine language (.stzu, harobanda and stzzui)', files(GH + '/harobanda/**/*.stzu') + files(GH + '/stzzui/**/*.stzu')))
    res['c6'].append(c6_family('.zql (zing), an elder', files(GH + '/zing/**/*.zql')))
    res['c6'].append(c6_family('.wflow (RingFlex), an elder', files(GH + '/ringflex/**/*.wflow')))
    res['c6'].append(c6_family('.zui (StzZui), an elder', files(GH + '/stzzui/**/*.zui')))
    journal = yaml_fences(files(GH + '/softanza/memos/*.md'))
    mailbox = yaml_fences(files(GH + '/softanza/mailbox/*.md'))
    pia = [(p, read(p)) for p in files(GH + '/softanza/**/*.pia') + files(GH + '/_wtmig/libraries/stzlib/**/*.pia') + files(GH + '/harobanda/**/*.pia')]
    for house in (False, True):
        res['memo'].append(memo_family('the journal (softanza/memos, yaml fences)', journal, house))
        res['memo'].append(memo_family('the mailboxes (softanza/mailbox, yaml fences)', mailbox, house))
        res['memo'].append(memo_family('.pia agents (roster, stzlib, harobanda)', pia, house))
    res['face'] = face_sample(files(GH + '/_wtmig/libraries/stzlib/base/**/*.ring'))
    # the house reading keeps every text C9's reader reads: the same block, text for text
    agree = differ = 0
    for _, t in journal + mailbox + pia:
        try:
            x = load_memo(t, False)
        except Refused:
            continue
        if load_memo(t, True) == x:
            agree += 1
        else:
            differ += 1
    res['house_reading_agrees_with_c9'] = {'same_block': agree, 'another_block': differ}
    # the proposed C6 amendment, measured: a doubled quote inside a string is one quote
    import block
    block.DOUBLED_QUOTE = True
    res['doubled_quote'] = {'journal': memo_family('the journal', journal, True)['into_c6_and_back'],
                            'mailboxes': memo_family('the mailboxes', mailbox, True)['into_c6_and_back']}
    c6 = sorted(set(haro)) + sentences + files(GH + '/harobanda/**/*.stzu') + files(GH + '/stzzui/**/*.stzu') + files(GH + '/ringflex/**/*.wflow')
    alike = differ = 0
    for p in c6:
        t = read(p)
        try:
            block.DOUBLED_QUOTE = False; a1 = load(t)
        except Refused:
            continue
        block.DOUBLED_QUOTE = True
        if load(t) == a1:
            alike += 1
        else:
            differ += 1
    block.DOUBLED_QUOTE = False
    res['doubled_quote'].update({'c6_files_read_alike': alike, 'c6_files_that_differ': differ})
    # 07 judging 06's corpus: Haro's declaration form, stated once as a pattern rule, over every C6 file the LOAD reads
    import pattern
    rules = {'decl': '[LIT DEFINE KEYWORD WORD LIT AS GROUP LIT RATIONALE STRING]', 'main': '[ANY RULE decl END]'}
    compiled = pattern.declare(rules, {})
    hit = miss = steps = 0
    t1 = time.time()
    biggest = (0, '')
    for p in c6:
        try:
            vals = tuple(v for v in load(read(p)) if v[0] != 'comment')
        except Refused:
            continue
        mt = pattern.Matcher(compiled, {})
        ok, j, _ = mt.m(compiled['main'], vals, 0)
        good = ok and j == len(vals)
        hit += good; miss += not good; steps += mt.steps
        biggest = max(biggest, (len(vals), os.path.basename(p)))
    res['pattern_over_corpus'] = {'rule': rules, 'files_matching': hit, 'files_not': miss, 'steps': steps,
                                  'seconds': round(time.time() - t1, 2), 'largest_input_values': biggest}
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(HERE, 'results.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    for fam in res['c6']:
        print(f"C6    {fam['family']:58} files {fam['files']:4}  loaded {fam['loaded']:4}  round trip {fam['round_trip']:4}  canonical {fam['canonical_bytes']}/{fam['bytes']} bytes")
        if fam['refused_why']:
            print('        refused:', fam['refused_why'])
        if fam['round_trip_failed']:
            print('        trip failed:', fam['round_trip_failed'])
    for fam in res['memo']:
        print(f"memo  {fam['family']:75} texts {fam['texts']:4}  loaded {fam['loaded']:4}  own trip {fam['own_round_trip']:4}  into C6 and back {fam['into_c6_and_back']:4}  keys {fam['keys']} ({fam['keys_not_c6_identifiers']} not C6 identifiers)")
        if fam['refused_why']:
            print('        refused:', fam['refused_why'])
        if fam['c6_crossing_refused_why']:
            print('        C6 crossing refused:', fam['c6_crossing_refused_why'])
    f = res['face']
    print(f"face  {f['family']:58} files {f['files']:4}  loaded {f['loaded']:4}  refused: {f['refused_why']}")
    print('house reading against C9:', res['house_reading_agrees_with_c9'])
    print('doubled quote:', res['doubled_quote'])
    print('pattern over the corpus:', res['pattern_over_corpus'])
    print(f"census: {res['seconds']} s")


if __name__ == '__main__':
    main()
