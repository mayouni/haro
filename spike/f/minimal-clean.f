-- EXPECT: clean
-- The smallest lawful workflow. Most other fixtures are this file with exactly
-- one thing wrong, so each isolates the rule it tests.
DEFINE WORKFLOW minimal AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "The smallest workflow that says something true."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED refuse, ON_HELD refuse) RATIONALE "One act, three endings routed."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
DEFINE TERMINAL refuse AS (OUTCOME refused) RATIONALE "Refused."
