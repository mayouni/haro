-- EXPECT: parse-error deleted from the language
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A step routes its own decisions inline."
DEFINE GUARD g AS (DECISION ask_it, IS approuver) RATIONALE "The deleted form."
