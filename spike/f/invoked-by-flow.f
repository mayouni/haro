-- EXPECT: parse-error claims the seam runs upward
-- The seam is closed DOWNWARD (placement contract C3 section 3): a workflow step
-- may invoke a FLOW; a FLOW may never contain a workflow. This file tries to
-- open it from the other end and is refused by name.
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A workflow does not say what starts it."
DEFINE INVOKED_BY encaisser AS () RATIONALE "Backwards."
