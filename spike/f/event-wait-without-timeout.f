-- EXPECT: refuse C2
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A workflow may not wait on the world for ever."
DEFINE EVENT_WAIT wait_it AS (AWAITS something, CORRELATED_BY key, ON_RECEIVED fini) RATIONALE "No timeout on an event wait."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
