-- EXPECT: parse-error instance data
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A deadline may not read what the instance carries."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE TASK wait_it AS (ASKS a, SURFACE s, DECISIONS [ok], SLA "1 working day", TIMEOUT "2 working days after date_convenue", ON_TIMEOUT fini, ROUTES [ok: fini]) RATIONALE "The refused construct."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
