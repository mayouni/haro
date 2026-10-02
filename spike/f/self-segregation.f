-- EXPECT: refuse C9
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "Segregation separates two people, not one from a reflection."
DEFINE ACTOR a AS (ROLE r, SEGREGATED_FROM a) RATIONALE "Segregated from itself."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED fini, ON_HELD fini) RATIONALE "One act."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
