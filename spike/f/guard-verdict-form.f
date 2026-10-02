-- EXPECT: parse-error deleted from the language
-- The form the Phase 1 drafts used and never read. Refused BY NAME, so an
-- author following those drafts is told what replaced it.
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A step routes its own verdicts inline."
DEFINE GUARD g AS (VERDICT go, IS committed) RATIONALE "The deleted form."
