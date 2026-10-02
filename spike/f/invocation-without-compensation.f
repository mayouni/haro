-- EXPECT: refuse C3
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "An act that changes the world must say whether it can be taken back."
DEFINE INVOCATION go AS (INVOKES do_it, ON_COMMITTED fini, ON_REJECTED fini, ON_HELD fini) RATIONALE "Neither COMPENSATED_BY nor IRREVERSIBLE."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
