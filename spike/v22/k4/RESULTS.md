# K4 -- results

Twenty tasks, two inputs each (the shown data and hidden data), one attempt per task; the models are Claude haiku and Claude sonnet, run as sub-agents that read one prompt file and wrote one answer file (two tool calls each). Ring++ is judged on rnxc; the face is read by the reader (strict: the face's own spelling; lenient: its meaning) and the Ring++ that comes out is run on rnxc. (Rounds 1-3 were written as Ring 1.27 and first judged on the oracle; see K4.md.)

| condition | model | runs | strict | lenient | respelled by the printer then strict |
|---|---|---|---|---|---|
| Ring, a primer of Ring's facts | haiku | 2 | 20/20, 20/20 | 20/20, 20/20 | 20/20, 20/20 |
| Ring, a primer of Ring's facts | sonnet | 2 | 20/20, 20/20 | 20/20, 20/20 | 20/20, 20/20 |
| Ring, no primer | haiku | 1 | 19/20 | 19/20 | 19/20 |
| Ring, no primer | sonnet | 1 | 20/20 | 20/20 | 20/20 |
| the face, round-1 primer | haiku | 2 | 1/20, 1/20 | 3/20, 3/20 | 3/20, 3/20 |
| the face, round-1 primer | sonnet | 2 | 3/20, 3/20 | 19/20, 19/20 | 19/20, 19/20 |
| the face, primer amended (order, no str(), explicit words are always right) | haiku | 2 | 6/20, 2/20 | 20/20, 20/20 | 20/20, 20/20 |
| the face, primer amended (order, no str(), explicit words are always right) | sonnet | 2 | 4/20, 5/20 | 20/20, 20/20 | 20/20, 20/20 |
| the face, F2 plus new vs new_without_init | haiku | 1 | 5/20 | 20/20 | 20/20 |
| the face, F2 plus new vs new_without_init | sonnet | 1 | 5/20 | 20/20 | 20/20 |

## What failed (lenient)

- F / haiku: T01 refused x2, T02 refused x2, T03 refused x2, T04 refused x2, T05 refused x2, T06 refused x2, T07 refused x2, T08 refused x2, T09 refused x2, T10 refused x2, T12 refused x2, T13 refused x2, T14 refused x2, T15 refused x2, T16 refused x2, T19 refused x2, T20 refused x2
- F / sonnet: T10 refused x2
- F2 / haiku: nothing
- F2 / sonnet: nothing
- F3 / haiku: nothing
- F3 / sonnet: nothing
- R / haiku: nothing
- R / sonnet: nothing
- R0 / haiku: T10 wrong x1
- R0 / sonnet: nothing
