-- EXPECT: refuse C15
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A guard nothing reads is a leftover or a forgotten arrow."
DEFINE GUARD unread AS (NORM some_norm) RATIONALE "Never read."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED fini, ON_HELD fini) RATIONALE "One act."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
