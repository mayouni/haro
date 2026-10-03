-- three different laws broken in one file: C5, C1, C6, C15
DEFINE WORKFLOW bad AS (DEFINITION_VERSION "0.1.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "Three different laws broken in one file."
DEFINE ACTOR a AS (ROLE r) RATIONALE "One actor."
DEFINE GUARD unread AS (NORM some_norm) RATIONALE "Never read."
DEFINE INVOCATION go AS (INVOKES do_it, IRREVERSIBLE yes, ON_COMMITTED nowhere_at_all, ON_REJECTED fini, ON_HELD fini) RATIONALE "One arrow points at nothing."
DEFINE TASK ask_it AS (ASKS a, SURFACE s, DECISIONS [ok], SLA "1 working day", ROUTES [ok: fini]) RATIONALE "A human task that could sleep for ever, and nothing reaches it."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Done."
