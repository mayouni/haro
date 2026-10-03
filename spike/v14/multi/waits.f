-- two untimed waits, both reachable: C1 and C2
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "Two waits that could last for ever."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED ask_it, ON_REJECTED wait_it, ON_HELD fini) RATIONALE "Routes to both waits."
DEFINE TASK ask_it AS (ASKS a, SURFACE s, DECISIONS [ok], SLA "1 working day", ROUTES [ok: fini]) RATIONALE "A human task with no timeout."
DEFINE EVENT_WAIT wait_it AS (AWAITS something, CORRELATED_BY key, ON_RECEIVED fini) RATIONALE "An event wait with no timeout."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
