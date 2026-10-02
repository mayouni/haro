-- EXPECT: refuse C4
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "An invocation declares all three of a ZQL flow endings."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED fini) RATIONALE "ON HELD is missing."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
