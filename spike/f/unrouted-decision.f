-- EXPECT: refuse C8
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A declared decision that goes nowhere is a hole in the workflow."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE TASK ask_it AS (ASKS a, SURFACE s, DECISIONS [ok, refuser], SLA "1 working day", TIMEOUT "5 working days", ON_TIMEOUT fini, ROUTES [ok: fini]) RATIONALE "The decision refuser is declared and never routed."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
