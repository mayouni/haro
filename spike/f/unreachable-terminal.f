-- EXPECT: refuse C7
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "An ending nothing can reach is an ending that never happens."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED fini, ON_HELD fini) RATIONALE "One act."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
DEFINE TERMINAL orphan AS (OUTCOME refused) RATIONALE "Nothing points here."
