-- EXPECT: refuse C1
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "Every wait carries a TIMEOUT."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE TASK ask_it AS (ASKS a, SURFACE s, DECISIONS [ok], SLA "1 working day", ROUTES [ok: fini]) RATIONALE "A human task that could sleep for ever."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
