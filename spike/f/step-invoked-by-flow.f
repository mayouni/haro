-- EXPECT: parse-error claims the seam runs upward
-- The same law in body position: a step that writes CALLED_BY is claiming that
-- a ZQL flow calls it, which is the reverse seam again.
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A step is invoked by nothing; it is reached."
DEFINE INVOCATION go AS (CALLED_BY encaisser) RATIONALE "Backwards."
