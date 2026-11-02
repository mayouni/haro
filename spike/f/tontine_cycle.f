-- EXPECT: clean
-- THE SEAM BETWEEN TWO FORGED LETTERS: a workflow of F that INVOKES two flows of Z
-- (tontine.z: collect, indice) by name and never restates them. Judged clean alone
-- (the court reads the file and nothing else); resolved against the C1 world that
-- Z's own court emits from tontine.z (`z_court.haro world tontine.z`), every
-- invocation lands on a flow: symbol; against a world that declares no `indice`,
-- the second step is refused by name. The placement contract C3 section 3.2,
-- between two languages the forge made.

DEFINE WORKFLOW cycle_tontine AS (
  DEFINITION_VERSION "0.1.0",
  ZQL "tontine.z",
  SURFACES "tontine.face",
  CALENDAR niamey_ouvre, CALENDAR_VERSION "2026.1",
  LOCALE fr
) RATIONALE "A round of the circle: the collector records the deposit through the collect flow, then the satisfaction index is computed through the indice flow."

DEFINE ACTOR collector AS (ROLE collecte) RATIONALE "Records the deposits in the field."
DEFINE ACTOR treasurer AS (ROLE tresorerie, SEGREGATED_FROM collector) RATIONALE "Audits, and is never the collector."

DEFINE INVOCATION deposit AS (
  INVOKES collect, IRREVERSIBLE yes,
  ON_COMMITTED survey, ON_REJECTED refused, ON_HELD refused
) RATIONALE "The deposit is a ZQL transaction; the dossier that holds the round is this workflow."

DEFINE INVOCATION survey AS (
  INVOKES indice, IRREVERSIBLE yes,
  ON_COMMITTED done, ON_REJECTED refused, ON_HELD refused
) RATIONALE "The index is computed in-flow by ZQL; the workflow only waits for its ending."

DEFINE TERMINAL done AS (OUTCOME success) RATIONALE "Deposited and surveyed."
DEFINE TERMINAL refused AS (OUTCOME refused) RATIONALE "Refused by a norm of the world."
