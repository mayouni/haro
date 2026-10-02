-- EXPECT: clean
-- WORKFLOW A: RingFlex studies/homologuer-audit.wflow, re-expressed in the Grammar
-- Commons' shape as a sentence of F (f_v08.haro). Every declaration of the original
-- is here with its words and its rationale; what moved is notation: a step is a
-- declaration of its kind, an arrow is a seat, a deadline is a string, an
-- escalation's actions are a sequence of verb: target, a routing's branches are
-- guard: target. Domain: Organizium, the audit homologation cycle.

DEFINE WORKFLOW homologuer_audit AS (
  DEFINITION_VERSION "0.1.0",
  ZQL "organizium/app.zql",
  SURFACES "organizium-homologation.face",
  CALENDAR niamey_ouvre, CALENDAR_VERSION "2026.1",
  LOCALE fr
) RATIONALE "Un resultat d'audit n'est homologue qu'apres controle humain par un auditeur independant, et validation de la direction au-dessus du seuil declare. Le registre porte la preuve de qui a signe, quand, et sous quelle version de la definition."

DEFINE ACTOR agent_saisie AS (ROLE saisie) RATIONALE "L'agent qui saisit le resultat."
DEFINE ACTOR auditeur AS (ROLE controle, SEGREGATED_FROM agent_saisie) RATIONALE "L'auditeur est independant de la saisie (BCEAO-002)."
DEFINE ACTOR responsable_audit AS (ROLE controle) RATIONALE "Reprend le dossier au-dela du SLA."
DEFINE ACTOR direction AS (ROLE approbation, SEGREGATED_FROM agent_saisie) RATIONALE "Signe au-dessus du seuil."

DEFINE GUARD direction_requise AS (NORM seuil_direction) RATIONALE "Le seuil est une regle metier : elle est declaree en NORM ZQL et seulement CITEE ici. Aucun nombre n'apparait dans ce fichier."

DEFINE ESCALATION relance_auditeur AS (
  ON_BREACH [notify: auditeur, reassign: responsable_audit]
) RATIONALE "Le controle ne peut pas dormir : au-dela du SLA, le responsable d'audit reprend le dossier, et le registre nomme qui a repris."

DEFINE ESCALATION relance_direction AS (
  ON_BREACH [notify: direction]
) RATIONALE "La direction est notifiee mais jamais dessaisie : personne d'autre ne peut approuver a sa place (SOD)."

DEFINE RETRY registre AS (
  ATTEMPTS 3, INITIAL "30 seconds", BACKOFF 2, MAX "10 minutes", NOT_ON [rejected]
) RATIONALE "Un REJECTED est un refus metier : le rejouer ne fait que repeter le refus. Seuls HELD et les echecs de transport se rejouent."

DEFINE INVOCATION saisie AS (
  INVOKES enregistrer_audit, RETRY registre, COMPENSATED_BY retirer_audit,
  ON_COMMITTED controle_auditeur, ON_REJECTED refuse_a_la_saisie, ON_HELD attente_correction
) RATIONALE "L'agent saisit le resultat ; le flux ZQL applique score_plafond. Le 999 du legacy n'est pas une erreur a rattraper ici : c'est un commit qui ne peut pas avoir lieu."

DEFINE TASK controle_auditeur AS (
  ASKS auditeur, SURFACE controle_audit,
  DECISIONS [homologuer, retourner, refuser],
  SLA "2 working days", ESCALATION relance_auditeur,
  TIMEOUT "10 working days", ON_TIMEOUT abandonne,
  ROUTES [homologuer: aiguillage_direction, retourner: attente_correction, refuser: refuse_au_controle]
) RATIONALE "L'auditeur est independant de la saisie (BCEAO-002 : l'audit ne releve pas de la ligne qu'il controle). Dix jours ouvres sans decision : le dossier est abandonne, pas homologue par defaut."

DEFINE ROUTING aiguillage_direction AS (
  WHEN [direction_requise: validation_direction], OTHERWISE publication
) RATIONALE "Le seuil est une regle metier : elle est declaree en NORM ZQL et seulement CITEE ici. Aucun nombre n'apparait dans ce fichier."

DEFINE TASK validation_direction AS (
  ASKS direction, SURFACE validation_homologation,
  DECISIONS [approuver, refuser],
  SLA "3 working days", ESCALATION relance_direction,
  TIMEOUT "the 5th working day of next month", ON_TIMEOUT abandonne,
  ROUTES [approuver: publication, refuser: refuse_par_direction]
) RATIONALE "Au-dessus du seuil, la direction signe. Le delai butoir est un repere metier (la cloture mensuelle), pas une duree machine -- Rule 91, portee du calendrier a l'echeance."

DEFINE TASK attente_correction AS (
  ASKS agent_saisie, SURFACE correction_audit,
  DECISIONS [corriger, renoncer],
  SLA "5 working days",
  TIMEOUT "20 working days", ON_TIMEOUT abandonne,
  ROUTES [corriger: saisie, renoncer: abandonne]
) RATIONALE "Le retour a la saisie est une correction declaree, pas une boucle : elle repasse par le meme flux ZQL et le meme controle."

DEFINE INVOCATION publication AS (
  INVOKES publier_homologation, RETRY registre, COMPENSATED_BY retirer_homologation,
  ON_COMMITTED homologue, ON_REJECTED refuse_a_la_publication, ON_HELD attente_correction
) RATIONALE "La publication inscrit l'homologation au registre. Elle est compensable : une homologation publiee par erreur se retire par un acte declare et journalise, jamais par une edition du registre."

DEFINE TERMINAL homologue AS (OUTCOME success) RATIONALE "Homologue : controle par un auditeur independant, approuve si le seuil l'exigeait, publie au registre."
DEFINE TERMINAL refuse_a_la_saisie AS (OUTCOME refused) RATIONALE "Refuse par une norme ZQL avant toute ecriture : score hors bornes ou libelle vide."
DEFINE TERMINAL refuse_au_controle AS (OUTCOME refused) RATIONALE "Refuse par l'auditeur, avec sa decision au registre."
DEFINE TERMINAL refuse_par_direction AS (OUTCOME refused) RATIONALE "Refuse par la direction au-dessus du seuil."
DEFINE TERMINAL refuse_a_la_publication AS (OUTCOME refused) RATIONALE "Le registre a refuse la publication ; l'audit reste non homologue."
DEFINE TERMINAL abandonne AS (OUTCOME abandoned) RATIONALE "Aucune decision dans les delais. L'abandon est un etat declare et visible, jamais un dossier qui dort sans fin."
