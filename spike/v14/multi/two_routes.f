-- one step, two missing verdicts: C4 twice
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "One step missing two of its three endings."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini) RATIONALE "ON REJECTED and ON HELD are missing."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
