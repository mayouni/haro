# Haro v0.35 -- the per-seat severity: a reference that resolves to nothing, and a kind a REFUSAL names, may be a warning

**Written after `fixtures.json`, `court_cases.json`, the world `panel_v35.haro`, its twin `panel_errors.haro` and the sentences under `panel/`, which are the judges**
(the W discipline: fixtures first, prose second; they are fe49473, before any code read a `SEVERITIES`). Added after the code, and said so in the case file: the cites of
P7 (the guard's reader of a `diagnose` case requires them), and P24, the explicit `error` on `NEXT` and `GADGET`, and the words of P15 and P16, found by designing the plants.
v0.35 is the ask the constitution desk routed on 2026-11-02, "the per-seat severity design, with Zin's per-rule granularity beside it", taken on the author's word as the
last owed item of Central's batch of 2026-11-03. It is the thirty-fifth rung (charter D49).

## The customer, read first: StzZui's five warnings are three mechanisms

zane.js reports five diagnostics as warnings, and a court can only refuse, so `zane.stzu` leaves them undeclared rather than over-refuse (its seam S1, and D2 for WIDGET and
USER). Read against `violations.json` (stzzui origin/main ff5d1c5, read-only), they are three mechanisms, and only one of them is a seat:

| diagnostic | what it says | what carries it |
|---|---|---|
| `INTENT_FLOW_NO_SATISFIES` | an INTENT_FLOW declares no intents | **already**: a CONSTRAINT `satisfies absent or satisfies empty`, `SEVERITY warning` (v0.25) |
| `ROLE_UNDECLARED` | a surface declares interactions and gives none a role | **already**: `ON interaction`, `not (earlier interaction) and (all interaction where role absent)`, `SEVERITY warning` -- said once, on the first interaction |
| `UNRESOLVED_INTENT_FLOW` | a reference names no declared flow | **new**: `SEVERITIES [intent_flow: warning]` on the kind |
| `UNRESOLVED_ENTITY` | a name resolves to no entity in the world | **new**: the same, on a SYMBOL seat the world resolves |
| `UNSPECIFIED_DECLARATION` | WIDGET and USER, kinds the language lacks | **new**: `SEVERITIES [widget: warning]` on `unknown_declaration` -- the NAMED kind is read past, and said |

The two **already** were proved on a scratch language before any fixture was written, and are judged here by P19 to P21.

## Zin's granularity, beside it

Zin sets a severity per **rule** (its WEAVE_POLICY), and Haro already does: a CONSTRAINT is a rule and its `SEVERITY` is v0.25's. The constitution sets one per **weave**
(constitutional, governance, advisory). What neither carried is the rule the **grammar** makes -- a reference must resolve, a kind must be declared. Those have no CONSTRAINT to
carry a `SEVERITY`, so the severity goes where that rule is written: on the **seat**, beside its `MESSAGES` and `CODES`, and on the **NAMED word**, beside its message and code.
The same two words, `error` and `warning`, at every grain. Zin's `SUPPRESS ... BECAUSE` (a rule switched off, with a reason) is not this: a warning is still said.

## The forms

    DEFINE DECLARATION form AS (
      VERB "FORM",
      SEATS [intent_flow: intent_flow?, next: intent_flow?, also: [intent_flow]?],
      MESSAGES [intent_flow: "FORM {name} walks the INTENT_FLOW '{value}', and no flow of that name is declared", ...],
      CODES [intent_flow: "UNRESOLVED_INTENT_FLOW", ...],
      SEVERITIES [intent_flow: warning, next: error, also: warning]
    ) RATIONALE "..."

    DEFINE REFUSAL unknown_declaration AS (
      MESSAGE "...",
      NAMED [widget: "WIDGET names a rendering, ...", user: "USER is not a kind this language defines", gadget: "GADGET was retired: ..."],
      CODES [widget: "UNSPECIFIED_DECLARATION", user: "UNSPECIFIED_DECLARATION", gadget: "RETIRED_KIND"],
      SEVERITIES [widget: warning, user: warning, gadget: error]
    ) RATIONALE "..."

**On a DECLARATION**, `SEVERITIES` names seats of the kind, each once, each `error` or `warning`, and each a **reference**: a DECLARATION, a UNION that holds one, a SYMBOL, or a
list of pairs whose keys or values are references (R1 to R5). `error` is the default and may be written, as `SEVERITY error` may on a CONSTRAINT.
**On a REFUSAL**, only on `unknown_declaration`, it names NAMED words (R6 to R11). An unknown verb stops the parse, an unknown clause has no declaration to belong to, and a
dangling reference is its seat's: none of them can be read past.

## What a warning is: a refusal demoted, and nothing else

The same code, the same cites, the same line, the same words its refusal would have carried. The verdict stays `ok`, and the warning is spoken after it, as a CONSTRAINT's of
`SEVERITY warning` is; in the envelope it is `"severity": "warning"`. **The twin pins it**: `panel_errors.haro` is the same language with every `SEVERITIES` line removed, and on
each sentence a case marks it must REFUSE with exactly the warning's words and line, and its envelope must match the warning's in code, cites, span and message: only the
severity differs (stage 40, on both builds).

- **Only a reference.** A value of the wrong shape is refused before the references pass and never reaches the severity (P23; R3 and R4 refuse the declaration that tries).
- **One warning per element.** A list held at warning speaks each element that resolves to nothing, in the order written (P24); a refusal stops at the first, a warning has no reason to.
- **A refused sentence speaks no warning** (P4): `check` stops at the first refusal, as it always did.
- **A kind read past must still be a declaration**: a name, `AS`, a body whose parentheses balance, `RATIONALE` and its string (P15, P16). It is not declared: it counts
  nowhere (P11) and a reference to it resolves to nothing (P14). A sentence of nothing but such kinds declares nothing (P17).
- **Without a world**, a SYMBOL held at warning is `NO_WORLD` as before: unresolved, so not a warning of its own (P9).
- **Order**: warnings are spoken in the order the passes meet them -- the kinds read past, then the constraints, then the references, then the world -- and within a pass in
  the order of the sentence. Not sorted by line: sorting would change the order v0.25's warnings are spoken in.

## How it is judged

| judge | what | holds |
|---|---|---|
| the meta fixtures | `fixtures.json`: 8 accepts and 11 rejects, each by the fragment of why | 19 of 19, stage 1 |
| the cases | `court_cases.json`: 24 cases over 20 sentences of `panel/`, with `panel/world.json`, on `haro` and its checked build, the same bytes | 24 of 24, stage 40 |
| **the twin** | `panel_errors.haro`, the same language without `SEVERITIES`, refuses each marked sentence with the warning's words, line, code, cites and span | 6 of 6 on each build, stage 40 |
| the protections | `plants.py`: each switched off in turn in a copy of `haro_lib.haro`, `forge.haro`, `court_lib.haro`, `world_lib.haro` or `severity_lib.haro` | see SPIKE.md, the thirty-fifth rung |

## What it costs

`severity_lib.haro` is loaded only by a court whose language holds a seat or a NAMED word at a severity, and the forge writes a kind's or a refusal's severities only where
they are declared: every other committed court is byte-identical. `court_lib.haro` gains three hooks (a kind read past, a seat held at warning, a parse that may return
nothing) and `world_lib.haro` one: the cold compile of every court pays for those lines, measured in SPIKE.md.

## Not decided here

- **A list of SYMBOLs** is not a seat the meta-court accepts (a list's element is a FORM, a DECLARATION, a MENU or a UNION of declarations). StzZui's `VISIBLE_ENTITIES` is a list,
  so `UNRESOLVED_ENTITY` on it needs either that, or its entities declared in the sentence. Another rung, on a customer's word.
- **`unknown_seat` at warning** (an unknown clause read past) would answer StzZui's S13 in part; zane.js READS those fields where the court refuses them, which is not a warning.
  Not built.
- **Zin's `SUPPRESS ... BECAUSE`** -- a rule switched off for a declared reason -- is not a severity, and is the constitution desk's to bring.
- StzZui adopting it: `zane.stzu` types `INTENT_FLOW` as a `name` today so the court does not over-refuse; with this rung it can type it `intent_flow` and hold it at warning.
  That, and its 57 fixtures, are StzZui's.
