-- EXPECT: parse-error no operators
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "There is no production that can parse an operator."
DEFINE GUARD g AS (NORM score > 5) RATIONALE "An operator."
