# Haro v0.16 -- NARRATE tells a run and a question

**Written after `fixtures.json`, and `run_cases.json` beside it, which are the judge of what it
must say** (the W discipline: fixtures first, prose second). v0.13 gave a language a voice that
could say what a SENTENCE is. It could not say what a RUN did, and a run is the thing stzn
exists for: "the machine speaking back" is a narration of an execution, not of its source.
Two verbs of the A letter and the Q letter answer in the language's own voice at last -- `run`
becomes `narrate-run`, `ask` becomes `narrate-ask` -- and the rule of principle 8 is kept to
the letter: the narration is a projection of the run, never stored, never parsed back.
v0.16 refuses nothing v0.15 accepted (fixture A3 is a v0.15 voice, unchanged).

## What is new

| clause | declares | the lesson it carries |
|---|---|---|
| `TELLS [event: "template", ...]` inside a `NARRATE` | a template per EVENT of a run or of a question | a key is an event of a RUN or an ASK the language declares (R3, R6), or a declaration kind that plays a construct of that RUN (R1, R4); told once (R5); every `{word}` a placeholder the event has (R2, R9); every brace closes (R7) |
| `SAYS` and `TELLS` | a voice that says a sentence, tells a run, or both | **either is enough** (A1: TELLS alone is a voice) and a voice with neither narrates nothing (R8, which is v0.13's R7, still said in its words) |

The events, and what each one can fill:

| event | for a language that declares | when it happens | placeholders |
|---|---|---|---|
| `run` | a RUN | first, before any step | `{algorithm}` `{record}` (the input, as JSON) `{language}` `{file}` |
| a step kind (`compute`, `collect`, `group`, `branch`, `iterate`: whatever plays a construct of the RUN) | a RUN | as the step does its work | `{name}` `{verb}` `{rationale}` `{line}`, the step's own seats (`{into}` `{when}` `{over}` `{as}` ...), and what it DID: `{value}` `{key}` `{taken}` `{count}` |
| `result` | a RUN | last | `{algorithm}` `{result}` `{language}` `{file}` |
| `ask` | an ASK | first | `{question}` `{from}` `{language}` `{file}` |
| `matched` | an ASK | after the condition | `{count}` `{total}` `{from}` |
| `ordered` | an ASK | after the sort, **only if the question orders** | `{field}` `{direction}` |
| `cut` | an ASK | **only if the limit dropped rows** | `{limit}` `{dropped}` `{count}` |
| `answer` | an ASK | last | `{count}` `{rows}` |

## Grammar (EBNF), the v0.15 text with this addition

```
NARRATE:  [OPENS string,] [SAYS message_list,] [TELLS message_list,] [ENDS string,] [REFUSES string]
```

(at least one of SAYS and TELLS; the list shape is v0.13's.)

## What the forge makes of it

A court whose language declares a NARRATE with a TELLS, and a RUN or an ASK, gains:

```
<lang>_court.ring narrate-run <file> <algorithm> <record json>
<lang>_court.ring narrate-ask <file> <question> <rows json>
```

A court with no voice refuses either, and says so (`this language declares no NARRATE`); one
with a voice and no RUN refuses `narrate-run` (`declares no RUN`), and one with no ASK refuses
`narrate-ask` (`declares no ASK`).

## A projection of THE run, not a second one

`narrate-run` calls the same `RunAlgorithm` that `run` calls, once, with a flag raised
(`$bRunTrace`). Each step then records what it did as it does it (`RunNote`: its depth, its
name, the value it made, the key it filed under, the arm it took, the items it will walk) and
`narrate-run` tells that record afterwards. Nothing is re-evaluated, so what is told cannot
differ from what was done; the questions go the same way (`$bAskTrace`, `AskNote`). A step
under another is indented two spaces a level: a branch's arm one deeper than the branch, a
loop's body one deeper than the loop. The flag is off in every other verb, and every earlier
stage passes byte for byte to prove it.

## Three rules that were decided, and why

**What a step DID is told before what was written.** A COMPUTE has a seat named `value` (the
expression) and an event that made one (the number). A template's `{value}` is the number:
the event's placeholders shadow a seat of the same name. The first cut filled both and
printed `11` and `3 + 4 * 2` run together as `113 + 4 * 2` -- the hand-written narration
failed on it before anything else did. The expression's text is therefore not reachable from a
voice; that is named below.

**An event the voice does not tell is told plainly, from the event's own fields.** A step
without a template reads `<verb> <name>` and then what it did: a branch the arm it took
(`branch filter_gt_test: then`), a loop how many items (`iterate map_scale_over: 3 item(s)`),
a group the key it filed under (`group g: 1 under 1`), any other its value. The question's
events have plain forms too. The first default read only the event's value, so a branch and a
loop -- whose events carry an arm and a count, and no value -- said nothing of what happened.

**A `cut` is told only when the limit dropped rows.** "Only the first 5 are kept" over three
matches is not true. The Q fixtures never put a limit above the match count, so none of them
could have caught it; the guard asks three more questions whose limit is above it, with the
answer zing already gave the same question without the limit.

## What judges it

Python reads the declarations itself -- never asking the court what it meant -- and parses
each narration into the tree the sentence and the record say it must be:

- the answer told is the answer the stz and zing fixtures give;
- the depth-0 steps are the algorithm's declared STEPS, in order;
- an ITERATE walks as many items as the list it names holds, and its body runs once per item;
- a BRANCH's steps are those of the arm it announced, and its condition is the one declared;
- every collected, computed or filed value, rebuilt from the told lines alone, is the value
  the answer holds (31 answers rebuilt over 30 runs);
- a question's `matched`, `ordered`, `cut` and `answer` agree with its own clauses and zing's
  rows (the cut only when it dropped);
- a refused run is told as far as it got and then as the one refusal, never as answering;

plus three runs and a question composed by hand before the court ran, the same court under a
voice that tells almost nothing (three runs and a question, also by hand), one execution (the
telling calls `RunAlgorithm` and `AskRun` once each, and the check fails on a copy that calls
it twice), nothing written to the folder, a told run refused as a sentence, and the two
runtimes printing the same bytes on every one.

## What it does not do

- A voice cannot reach the TEXT of a step's expression (`{value}` is the number). Telling "why"
  a branch went the way it did would need the evaluated operands, not the source.
- The voice is one template per event: no choice of wording by value, no plural.
- A refused run is told up to the step that was running; what it was in the middle of is the
  refusal's message, not a further line.
- The laws judge shape and values, not prose: that a template reads well is not measured.
- N, the language of the natural, still waits on its study; this is the telling of A and Q only.
