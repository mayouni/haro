-- EXPECT: refuse C6
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A step nothing can reach is a dead step."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED fini, ON_HELD fini) RATIONALE "The only reachable step."
DEFINE INVOCATION orphan AS (INVOKES never_run, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED fini, ON_HELD fini) RATIONALE "Nothing points here."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
