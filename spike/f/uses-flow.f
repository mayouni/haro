-- EXPECT: parse-error belongs to ZQL
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "The word FLOW belongs to ZQL."
DEFINE FLOW encaisser AS () RATIONALE "Not here."
