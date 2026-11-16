# Haro v0.76 -- the peer and the endpoint

`doc/DOORS.md`, its third rung (D88 (e), D93): a program declares the hosts it reaches, once, in the same sentence of doors that
declares its folders and its commands; an outside text is judged against one of them into an endpoint; and the engine's own
wrappers read the endpoint's parts. No door of the VM changes: the network's door is the engine's.

    load "doors.haro"
    sDoors = doors'DEFINE PEER github AS (HOST "api.github.com", SCHEMES [https]) RATIONALE "where releases are read from"
                   DEFINE PEER lan AS (NET "10.9.0.0/16", SCHEMES [http], PORT 8080) RATIONALE "the machines of the house"'
    hApi = sDoors.Endpoint("github", tGiven)       # judged: an endpoint of the peer, or a refusal by name
    print hApi.Url()                               # what a wrapper of the engine hands on

Fixtures first (ff71467: 11 cases, none holding before the code; d064d7a: a twelfth, still before the code). The judge in Haro
b1962e1; the VM's half ab32ec2; three cases made to ask what none asked, three checks that repeated another taken out, the plants
and stage 81, ee5b871.

| line | what | cases |
|---|---|---|
| L1 | a sentence of doors declares peers; `sDoors.Endpoint(peer, text)` answers an endpoint: its peer, its scheme, its host, its port, its path; it prints as its address made plain; the letter `h` holds it; a sentence of another language judges none (ENDPOINT_NO_DOORS) | E01, E11 |
| L2 | the address made plain: the scheme and the host in small letters, the scheme's own port left out, the path as it was given; a peer that lists no scheme is reached by https | E02 |
| L3 | an address that is no address is ENDPOINT_FORM: no scheme, a name and a secret before the host, a blank, a control byte, a backslash, a bracket, a byte past ASCII, a port that is no port | E03 |
| L4 | a scheme the peer is not reached by is ENDPOINT_SCHEME; a host that is not the peer's is ENDPOINT_HOST, whatever it holds or ends with; a port that is not the peer's is ENDPOINT_PORT | E04, E05, E12 |
| L5 | a peer the sentence does not declare is PEER_UNKNOWN, and the refusal names the ones it does | E06 |
| L6 | a peer that is a network takes an address inside its prefix, written as four numbers and no other way | E07 |
| L7 | the declaration's court: a peer with no host and no network (PEER_NOWHERE), one with both (PEER_TWICE), a host that is no name, a network that is no prefix (FORMAT), a scheme outside the five (UNKNOWN_SCHEME) -- each refused when the program is compiled, its verdict the standalone court's | E08 |
| L8 | an endpoint is made by its judge alone, and is not written into (ENDPOINT_FIXED) | E09, E10 |

## The spellings (this desk's, under D84), chosen after reading what they serve

Read on stzlib origin/main 2a5b3ca7f before a word was chosen: the network's doors are its engine's -- `StzEngineHttpGet(tUrl)`,
`StzEngineTcpConnect(tHost, nPort)`, the credential broker's `StzBrokerRequest(grant, method, tUrl, ...)` -- and they take an
address as one text or as a host and a port. Its broker binds a credential to one host, https only, and follows no redirect. Its
target admission asks, while an agent acts, whether a host came from code, a declaration or a typed read.

- **The kind PEER**: `HOST "name"` is a host by its exact name, as the wire carries it; `NET "a.b.c.d/n"` is a network by its
  prefix; `SCHEMES [...]` lists how it is reached -- https, http, wss, ws, tcp -- and a peer that lists none is reached by https;
  `PORT n` names its port, where it is not the scheme's own.
- **The judge `Endpoint(peer, text)`**, a method of a sentence of doors. Its answer is an endpoint: `Peer()`, `Scheme()`,
  `Host()`, `Port()`, `Path()`, `Url()`; printed, it is its address made plain.
- **The letter `h`** holds an endpoint: T7's handle of the network door, held before the door is opened.

## What the judge reads in an address

- **Its form**: every byte printable ASCII and no backslash; a scheme of letters before `://`; then the host, with no name and
  secret before it and no bracket; then, after a colon, a port of digits from 1 to 65535; then the path, as it is given.
- **The host is compared whole**, in small letters. `api.github.com.evil.org`, `evilapi.github.com`, a host under the peer's, the
  peer's own with a dot after it, and an address in numbers are each another host.
- **For a network**, the host is four plain numbers, each 0 to 255 with no zero before it, inside the prefix. A name, three numbers,
  one number, a number in another base, a part past 255: each is refused, since a client may read each as an address the text
  does not show.
- **The port**: the one the peer names, else the scheme's own -- 443 for https and wss, 80 for http and ws; tcp has none, so a peer
  reached by tcp names its port. An address that writes no port is reached at the peer's.

## How it is built

- **The declaration** (`spike/doors.haro`): the kind PEER, two formats (a host's name, a network's prefix), the menu of schemes,
  two constraints; the language NEEDS network beside filesystem and process, and a PEER OPENS network.
- **The judge is Haro code** (`judge_lib.haro`, `HaroEndpointOf`): it reads the peers the sentence declares -- once, as every
  judge of doors does since v0.75 -- judges the text, and makes a `HaroEndpoint`.
- **The VM knows an endpoint by its class**, as it knows a place and an invocation: it prints as its address, the letter `h`
  holds it, a write into it is ENDPOINT_FIXED, and `new` of one is refused by the compiler outside the judging library.
- **No door of the VM takes it.** A wrapper of the engine reads its parts and passes them on. A native given the endpoint itself
  receives nothing: the wrapper asks for `Url()`, or for `Host()` and `Port()`.

## The seam with the engine (D88 (e))

Haro judges the text of an address against a declared peer. What happens after a name is resolved, and at a redirect, happens
where the socket is. The endpoint hands the engine what that check starts from: the peer's name, the host as it was judged, the
scheme and the port. The engine's desk decides how its doors use them.

## What the rung found

- **The judge ran before the VM knew its value.** Written in Haro, it passed every case that only judges on the installed
  v0.74 -- 7 of 12 -- with no build; the five left waited for the VM to know the class.
- **The plants took three checks out and asked for three cases**, each said in the generator. An empty address, a port that is
  no digits, and the count of an address's parts were each asked twice. A backslash beside an `@`, a peer with no scheme, and a
  bracket with a colon in it were each answered by another rule, so each has a case of its own now.

## Measured

- The court: 12 of 12 on both builds. 32 plants, each caught by its fixture: K1-K4 in `vm/src`, each built; J1-J23 in the judge
  and M1-M5 in the declaration of doors, where nothing is built (`plants.py`).
- The courts of v0.72 to v0.75 hold on the same builds: 18 of 18, 21 of 21, 14 of 14, 10 of 10.
- The 82-stage guard on builds made from the commit: PASS, 0 failures, 1994.5 s on the builds of 83d2d99; its stage 6 read 139.1 ms cold and 15.6 ms for an edit with another desk's run beside it, 122.4 ms and 15.1 ms alone, under ceilings of 150 and 50

## What stands at its present size

- The engine's doors take an address as text: a wrapper that takes an endpoint is the engine's desk's to write.
- The check after a name is resolved, and at a redirect, is the engine's (D88 (e)).
- A peer names one host or one network; an address of six parts in brackets is refused as no address.
- `unjudged` whole is DOORS.md's rung 4: until it is built an address as plain text reaches the engine's doors as it did.
