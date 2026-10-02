-- EXPECT: refuse C10
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A suspension re-enters at a declared step."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED parked, ON_HELD parked) RATIONALE "One act."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
DEFINE SUSPENDED parked AS (RESUMED_BY a, RESUMES_AT no_such_step) RATIONALE "Re-entry points at nothing."
