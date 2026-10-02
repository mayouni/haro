-- EXPECT: parse-error declaration set is closed
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "GATEWAY is not a RingFlex declaration."
DEFINE GATEWAY split_here AS () RATIONALE "Not a kind."
