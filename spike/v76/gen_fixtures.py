"""Haro v0.76, the peer and the endpoint (doc/DOORS.md rung 3, D88 (e)): the cases of v76/fixtures.json and their files, written
BEFORE the code, and before any build: the code is built when v0.75 stands in the shared runtime. Every expectation is typed here.

The spellings are this desk's, under D84, chosen after reading what they serve on stzlib 2a5b3ca7f: its network doors are its
engine's (`StzEngineHttpGet(tUrl)`, `StzEngineTcpConnect(tHost, nPort)`, the credential broker's `StzBrokerRequest(grant, method,
tUrl, ...)`), which take an address as one text or as a host and a port; its broker binds a credential to one host, https only,
and follows no redirect; its target admission asks, while an agent acts, whether a host came from code, a declaration or a typed
read. So: the kind PEER (HOST a name, or NET an address and its prefix; SCHEMES; PORT), the judge `Endpoint(peer, text)`, a value
that answers its parts -- `Url()`, `Scheme()`, `Host()`, `Port()`, `Path()` -- for the engine's own wrappers to read. No door of
the VM changes: the network's door is the engine's (D88 (e)).

  python spike/v76/gen_fixtures.py     writes cases/ and fixtures.json

The lines:
  L1  a sentence of doors declares peers; `sDoors.Endpoint(peer, text)` answers an endpoint: its peer, its scheme, its host, its
      port, its path; it prints as its address made plain; the letter h holds it; a sentence of another language judges none
  L2  the address made plain: the scheme and the host in small letters, the scheme's own port left out, the path as it was given
  L3  an address that is no address is ENDPOINT_FORM: no scheme, a name and a secret before the host, a blank, a control byte, a
      backslash, a bracket, a byte past ASCII, a port that is no port
  L4  a scheme the peer is not reached by is ENDPOINT_SCHEME; a host that is not the peer's is ENDPOINT_HOST, whatever it holds or
      ends with; a port that is not the peer's is ENDPOINT_PORT
  L5  a peer the sentence does not declare is PEER_UNKNOWN, and the refusal names the ones it does
  L6  a peer that is a network takes an address inside its prefix, written as four numbers and no other way
  L7  the declaration's court: a peer with no host and no network (PEER_NOWHERE), one with both (PEER_TWICE), a host that is no
      name, a network that is no prefix, a scheme outside the five -- each refused when the program is compiled, its verdict the
      standalone court's
  L8  an endpoint is made by its judge alone, and is not written into
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
cases = []
RULE = 'haro/refused-form'
CASES = os.path.join(HERE, 'cases')
os.makedirs(CASES, exist_ok=True)

GITHUB = 'DEFINE PEER github AS (HOST "api.github.com", SCHEMES [https]) RATIONALE "where releases are read from"'
DB = 'DEFINE PEER db AS (HOST "db.internal", SCHEMES [tcp], PORT 5432) RATIONALE "the database of this program"'
LAN = 'DEFINE PEER lan AS (NET "10.9.0.0/16", SCHEMES [http], PORT 8080) RATIONALE "the machines of the house"'
BOTH = 'DEFINE PEER site AS (HOST "example.org", SCHEMES [https, http]) RATIONALE "a site reached either way"'


def said(code, message):
    return 'Error (' + code + ') : ' + message


def case(cid, line, what, src, run, judged=None, check=None):
    """run: {'stdout': text} exact with exit 0; {'refuses': [row, reason, written]} with 'never'. judged: [[language, text, code or
    None, message]] for the law. check: {'errors': n, 'found': [[row, rule]]}."""
    name = cid.lower() + '.haro'
    with open(os.path.join(CASES, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    c = {'id': cid, 'line': line, 'what': what, 'file': 'cases/' + name, 'run': run}
    if judged is not None:
        c['judged'] = judged
    if check is not None:
        c['check'] = check
    cases.append(c)


def tries(decls, peer, texts, what='e.Code()'):
    """a program that asks for an endpoint of each text and prints the refusal's code, or `judged`"""
    lines = ['load "doors.haro"', "sDoors = doors'" + decls + "'", 'vTexts = [' + ', '.join(texts) + ']', 'for i = 1 to Len(vTexts)', '    try',
             '        hAny = sDoors.Endpoint("' + peer + '", vTexts[i])', '        print "judged"', '    catch e', '        print ' + what, '    end', 'end']
    return '\n'.join(lines) + '\n'


case('E01', 'L1', 'a peer declared, an endpoint judged and held by an h name', f'''load "doors.haro"
sDoors = doors'{GITHUB}'
hApi = sDoors.Endpoint("github", "https://api.github.com/user?per_page=5")
print hApi
print hApi.Peer()
print hApi.Scheme()
print hApi.Host()
print hApi.Port()
print hApi.Path()
print hApi.Url()
''', {'stdout': 'https://api.github.com/user?per_page=5\ngithub\nhttps\napi.github.com\n443\n/user?per_page=5\nhttps://api.github.com/user?per_page=5\n'},
     judged=[['doors', GITHUB, None, '']], check={'errors': 0, 'found': []})

case('E02', 'L2', 'the address made plain: small letters for the scheme and the host, the scheme\'s own port left out, the path as given', f'''load "doors.haro"
sDoors = doors'{GITHUB}
{DB}
{BOTH}'
print sDoors.Endpoint("github", "HTTPS://API.GitHub.com/Repos/Haro")
print sDoors.Endpoint("github", "https://api.github.com:443/user")
print sDoors.Endpoint("github", "https://api.github.com")
print sDoors.Endpoint("db", "tcp://db.internal:5432")
print sDoors.Endpoint("db", "tcp://db.internal")
print sDoors.Endpoint("db", "tcp://db.internal").Port()
print sDoors.Endpoint("site", "http://example.org/a#b")
print sDoors.Endpoint("site", "http://example.org/a#b").Port()
''', {'stdout': 'https://api.github.com/Repos/Haro\nhttps://api.github.com/user\nhttps://api.github.com\ntcp://db.internal:5432\ntcp://db.internal:5432\n5432\nhttp://example.org/a#b\n80\n'})

BS = 'Char(92)'
case('E03', 'L3', 'an address that is no address is ENDPOINT_FORM', tries(GITHUB, 'github', [
    '""', '"api.github.com/user"', '"https:/api.github.com"', '"https://"', '"https://token:x@api.github.com/"', '"https://api.github.com@evil.org/"',
    '"https://api.github.com /user"', '"https://api.github.com/a" + Char(10) + "b"', '"https://api.github.com" + ' + BS + ' + "@evil.org/"',
    '"https://[::1]/"', '"https://api.github.com:port/"', '"https://api.github.com:0/"', '"https://api.github.com:70000/"',
    '"https://api.github.com/caf" + Char(233)', '"1https://api.github.com/"']) + '''try
    hAny = sDoors.Endpoint("github", "api.github.com/user")
catch e
    print e.Message()
end
''', {'stdout': 'ENDPOINT_FORM\n' * 15 + said('ENDPOINT_FORM', '`api.github.com/user` is no address a peer is reached at') + '\n'})

case('E04', 'L4', 'a host that is not the peer\'s is ENDPOINT_HOST, whatever it holds or ends with', tries(GITHUB, 'github', [
    '"https://evil.org/"', '"https://api.github.com.evil.org/"', '"https://evilapi.github.com/"', '"https://uploads.api.github.com/"',
    '"https://github.com/"', '"https://api.github.com./"', '"https://140.82.112.5/"']) + '''try
    hAny = sDoors.Endpoint("github", "https://api.github.com.evil.org/")
catch e
    print e.Message()
end
''', {'stdout': 'ENDPOINT_HOST\n' * 7 + said('ENDPOINT_HOST', '`api.github.com.evil.org` is not the host of the peer `github`') + '\n'})

case('E05', 'L4', 'a scheme the peer is not reached by is ENDPOINT_SCHEME; a port that is not the peer\'s is ENDPOINT_PORT', f'''load "doors.haro"
sDoors = doors'{GITHUB}
{DB}'
vTries = [["github", "http://api.github.com/"], ["github", "ftp://api.github.com/"], ["github", "https://api.github.com:8443/"], ["db", "tcp://db.internal:22"], ["db", "https://db.internal:5432"]]
for i = 1 to Len(vTries)
    try
        hAny = sDoors.Endpoint(vTries[i][1], vTries[i][2])
        print "judged"
    catch e
        print e.Message()
    end
end
''', {'stdout': said('ENDPOINT_SCHEME', 'the peer `github` is not reached by http') + '\n'
      + said('ENDPOINT_SCHEME', 'the peer `github` is not reached by ftp') + '\n'
      + said('ENDPOINT_PORT', 'the peer `github` is not reached at port 8443') + '\n'
      + said('ENDPOINT_PORT', 'the peer `db` is not reached at port 22') + '\n'
      + said('ENDPOINT_SCHEME', 'the peer `db` is not reached by https') + '\n'})

case('E06', 'L5', 'a peer the sentence does not declare is PEER_UNKNOWN, and names the ones it does', f'''load "doors.haro"
sDoors = doors'{GITHUB}
{DB}'
try
    hAny = sDoors.Endpoint("gitlab", "https://gitlab.com/")
    print "judged"
catch e
    print e.Code()
    print e.Message()
end
''', {'stdout': 'PEER_UNKNOWN\n' + said('PEER_UNKNOWN', 'no peer called `gitlab` is declared here; the peers are github, db') + '\n'},
     judged=[['doors', GITHUB + '\n' + DB, None, '']])

case('E07', 'L6', 'a peer that is a network takes an address inside its prefix, written as four numbers and no other way', f'''load "doors.haro"
sDoors = doors'{LAN}'
print sDoors.Endpoint("lan", "http://10.9.3.7:8080/status")
print sDoors.Endpoint("lan", "http://10.9.255.255/")
vTexts = ["http://10.10.0.1/", "http://10.8.255.255/", "http://printer.local/", "http://010.9.3.7/", "http://10.9.3/", "http://168363783/", "http://0x0a.9.3.7/", "http://10.9.3.256/", "http://10.9.3.7.1/"]
for i = 1 to Len(vTexts)
    try
        hAny = sDoors.Endpoint("lan", vTexts[i])
        print "judged"
    catch e
        print e.Code()
    end
end
try
    hAny = sDoors.Endpoint("lan", "http://10.10.0.1/")
catch e
    print e.Message()
end
''', {'stdout': 'http://10.9.3.7:8080/status\nhttp://10.9.255.255:8080/\n' + 'ENDPOINT_HOST\n' * 9
      + said('ENDPOINT_HOST', '`10.10.0.1` is not in the network of the peer `lan`') + '\n'}, judged=[['doors', LAN, None, '']])

NOWHERE = 'DEFINE PEER a AS (SCHEMES [https]) RATIONALE "x"'
M_NOWHERE = 'PEER a names no host: give it HOST, or NET for a network by its prefix'
case('E08', 'L7', 'a peer with no host and no network is refused when the program is compiled', f'''load "doors.haro"
print "before"
sDoors = doors'{NOWHERE}'
''', {'refuses': [3, 'the court of doors refuses this literal -- PEER_NOWHERE: ' + M_NOWHERE + '; written', "'" + NOWHERE + "'"], 'never': 'before'},
     judged=[['doors', NOWHERE, 'PEER_NOWHERE', M_NOWHERE],
             ['doors', 'DEFINE PEER b AS (HOST "x.org", NET "10.0.0.0/8") RATIONALE "x"', 'PEER_TWICE', 'PEER b says HOST and NET: it is one or the other'],
             ['doors', 'DEFINE PEER c AS (HOST "Bad_Host!", SCHEMES [https]) RATIONALE "x"', 'FORMAT',
              "'Bad_Host!' cannot be a host: a name on the wire is lowercase letters, digits and the hyphen, in labels separated by dots"],
             ['doors', 'DEFINE PEER d AS (HOST "x.org", SCHEMES [gopher]) RATIONALE "x"', 'UNKNOWN_SCHEME',
              "A peer is reached by https, http, wss, ws or tcp, not 'gopher'"],
             ['doors', 'DEFINE PEER e AS (NET "10.0.0.0", SCHEMES [http]) RATIONALE "x"', 'FORMAT', "'10.0.0.0' is not an address/prefix (a.b.c.d/n)"]],
     check={'errors': 1, 'found': [[3, RULE]]})

FAKE = 'new HaroEndpoint("github", "https", "https://evil.org/", "evil.org", 443, "/")'
case('E09', 'L8', 'an endpoint is made by its judge alone: `new` of one is refused when compiling', f'''load "doors.haro"
xFake = {FAKE}
print "made"
''', {'refuses': [2, 'an endpoint is made by its judge -- <doors>.Endpoint(peer, text); written', FAKE], 'never': 'made'},
     check={'errors': 1, 'found': [[2, RULE]]})

case('E10', 'L8', 'a write into an endpoint is refused, and it is what it was', f'''load "doors.haro"
sDoors = doors'{GITHUB}'
hApi = sDoors.Endpoint("github", "https://api.github.com/user")
try
    hApi.tHost = "evil.org"
    print "written"
catch e
    print e.Code()
end
print hApi.Host()
print hApi
''', {'stdout': 'ENDPOINT_FIXED\napi.github.com\nhttps://api.github.com/user\n'})

RAW = 'DEFINE PEER raw AS (HOST "queue.internal", SCHEMES [tcp]) RATIONALE "a peer reached by tcp that names no port"'
case('E12', 'L4', 'a peer that names no port, reached by a scheme that has none of its own, is ENDPOINT_PORT', f'''load "doors.haro"
sDoors = doors'{RAW}'
try
    hAny = sDoors.Endpoint("raw", "tcp://queue.internal:9000")
    print "judged"
catch e
    print e.Message()
end
''', {'stdout': said('ENDPOINT_PORT', 'the peer `raw` names no port, and tcp has none of its own') + '\n'})

LAMP = 'DEFINE LAMP north AS (SHOWS green) RATIONALE "x"'
case('E11', 'L1', 'an endpoint is judged by a sentence of doors: a sentence of another language answers ENDPOINT_NO_DOORS', f'''load "doors.haro"
load "../../v70/cases/signal.haro"
sLamp = signal'{LAMP}'
try
    hAny = sLamp.Endpoint("github", "https://api.github.com/")
    print "judged"
catch e
    print e.Message()
end
''', {'stdout': said('ENDPOINT_NO_DOORS', 'an endpoint is judged by a sentence of doors, and this is a sentence of signal') + '\n'})

doc = {'version': '0.76', 'task': 'doc/DOORS.md rung 3: the peer and the endpoint', 'languages': ['doors'],
       'law': 'the verdict on a sentence of doors is the one its own forged court answers, standing alone, on the same text', 'cases': cases}
with open(os.path.join(HERE, 'fixtures.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')
print(len(cases), 'cases written')
