-- EXPECT: parse-error no HELD outcome
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A held dossier is a SUSPENDED state, not a terminal."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED parked, ON_REJECTED parked, ON_HELD parked) RATIONALE "One act."
DEFINE TERMINAL parked AS (OUTCOME held) RATIONALE "Not an ending."
