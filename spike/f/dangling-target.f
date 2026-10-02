-- EXPECT: refuse C5
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "Every arrow lands somewhere declared."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED nowhere_at_all, ON_REJECTED fini, ON_HELD fini) RATIONALE "One arrow points at nothing."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
