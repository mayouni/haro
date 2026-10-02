-- EXPECT: clean
-- THE POSITIVE HALF OF THE SEAM (placement contract C3 section 3): a step
-- invokes a ZQL flow and routes all three of its endings -- COMMITTED,
-- REJECTED, HELD -- which mirror ZQL's own three.
DEFINE WORKFLOW paiement AS (DEFINITION_VERSION "1.0.0", ZQL "x/app.zql", SURFACES "x.face", CALENDAR c, CALENDAR_VERSION "1", LOCALE fr) RATIONALE "A durable act that spends transactional ones, and says which."
DEFINE ACTOR tresorier AS (ROLE finance) RATIONALE "The treasurer."
DEFINE INVOCATION encaisser AS (INVOKES encaisser_paiement, COMPENSATED_BY rembourser_paiement, ON_COMMITTED notifier, ON_REJECTED annulation, ON_HELD annulation) RATIONALE "The money moves inside one ZQL transaction; the dossier does not."
DEFINE INVOCATION notifier AS (INVOKES notifier_client, IRREVERSIBLE yes, ON_COMMITTED fini, ON_REJECTED annulation, ON_HELD annulation) RATIONALE "Telling someone cannot be taken back, and the file says so."
DEFINE COMPENSATION annulation AS (ON_COMPENSATED refuse, ON_FAILED refuse) RATIONALE "Unwinding is itself flow work: the engine replays the compensating invocations in reverse order of completion."
DEFINE TERMINAL fini AS (OUTCOME success) RATIONALE "Paid, and told."
DEFINE TERMINAL refuse AS (OUTCOME refused) RATIONALE "Not paid, and unwound."
