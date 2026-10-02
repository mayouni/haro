-- EXPECT: clean
-- WORKFLOW B: RingFlex studies/commande-fournisseur.wflow, re-expressed in the
-- Grammar Commons' shape as a sentence of F (f_v08.haro). Every declaration of the
-- original is here with its words and its rationale; what moved is notation.
-- Domain: RestoLean capsule 1, the supplier order cycle: commande -> confirmation
-- fournisseur -> attente livraison -> controle reception -> paiement du. Waits,
-- SLAs, one compensation, irreversible acts, three suspensions.

DEFINE WORKFLOW cycle_commande_fournisseur AS (
  DEFINITION_VERSION "0.1.0",
  ZQL "restolean/app.zql",
  SURFACES "restolean-fournisseur.face",
  CALENDAR lyon_ouvre, CALENDAR_VERSION "2026.1",
  LOCALE fr
) RATIONALE "Une commande fournisseur vit des jours : elle est confirmee, elle attend une livraison, elle est controlee a l'arrivee, et elle se paie a l'echeance. Le registre porte qui a commande, qui a confirme, ce qui est arrive, et ce qui a ete regle."

DEFINE ACTOR restaurateur AS (ROLE achat) RATIONALE "Commande et controle."
DEFINE ACTOR fournisseur AS (ROLE vente) RATIONALE "Confirme et livre."
DEFINE ACTOR equipier_fournisseur AS (ROLE preparation) RATIONALE "Prepare la commande chez le fournisseur."
DEFINE ACTOR comptable AS (ROLE reglement, SEGREGATED_FROM restaurateur) RATIONALE "Regle, et n'est jamais celui qui a commande."

DEFINE ESCALATION relance_fournisseur AS (
  ON_BREACH [notify: fournisseur, notify: restaurateur]
) RATIONALE "Le restaurateur doit savoir que son fournisseur n'a pas confirme : il a une cuisine a approvisionner et un plan B a declencher."

DEFINE ESCALATION relance_livraison AS (
  ON_BREACH [notify: fournisseur, notify: restaurateur]
) RATIONALE "Une livraison en retard est une information de gestion, pas une erreur technique."

DEFINE ESCALATION alerte_reception AS (
  ON_BREACH [notify: restaurateur]
) RATIONALE "La marchandise attend sur le quai : temperature et DLC courent. Le controle ne peut pas attendre un jour ouvre."

DEFINE RETRY registre AS (
  ATTEMPTS 3, INITIAL "30 seconds", BACKOFF 2, MAX "10 minutes", NOT_ON [rejected]
) RATIONALE "Meme discipline que l'autre workflow : un refus metier ne se rejoue pas."

DEFINE INVOCATION emission AS (
  INVOKES emettre_commande_fournisseur, RETRY registre, COMPENSATED_BY annuler_commande_fournisseur,
  ON_COMMITTED confirmation, ON_REJECTED refusee_a_l_emission, ON_HELD refusee_a_l_emission
) RATIONALE "La commande part. Elle est compensable tant qu'elle n'est pas livree : l'annulation est un acte declare et journalise."

DEFINE TASK confirmation AS (
  ASKS fournisseur, SURFACE confirmation_commande,
  DECISIONS [confirmer, signaler_probleme, refuser],
  SLA "1 working day", ESCALATION relance_fournisseur,
  TIMEOUT "3 working days", ON_TIMEOUT abandonnee,
  ROUTES [confirmer: attente_livraison, signaler_probleme: resolution_probleme, refuser: refusee_par_fournisseur]
) RATIONALE "Le fournisseur confirme, signale un probleme, ou refuse. Trois jours ouvres sans reponse : la commande est abandonnee, jamais confirmee par defaut -- le silence n'engage personne."

DEFINE TASK resolution_probleme AS (
  ASKS restaurateur, SURFACE resolution_ecart_commande,
  DECISIONS [accepter, annuler],
  SLA "1 working day",
  TIMEOUT "3 working days", ON_TIMEOUT annulation,
  ROUTES [accepter: attente_livraison, annuler: annulation]
) RATIONALE "Le probleme signale (rupture, prix, colisage) se resout par messagerie entre les deux ; le workflow n'enregistre que la decision, jamais la conversation."

DEFINE EVENT_WAIT attente_livraison AS (
  AWAITS livraison_arrivee, CORRELATED_BY commande_id,
  TIMEOUT "10 working days", ON_TIMEOUT retard_livraison,
  ON_RECEIVED controle_reception
) RATIONALE "L'attente de la livraison est le coeur de ce cycle : des jours, reveilles par un evenement du monde reel. Le butoir est une duree declaree, comptee depuis l'entree dans l'etape -- il ne lit aucune donnee de l'instance."

DEFINE TASK retard_livraison AS (
  ASKS restaurateur, SURFACE suivi_livraison,
  DECISIONS [patienter, annuler],
  SLA "1 working day", ESCALATION relance_livraison,
  TIMEOUT "5 working days", ON_TIMEOUT annulation,
  ROUTES [patienter: attente_livraison, annuler: annulation]
) RATIONALE "Le retard rend la main au restaurateur : il patiente ou il annule. Personne ne decide a sa place et rien ne s'annule tout seul."

DEFINE TASK controle_reception AS (
  ASKS restaurateur, SURFACE controle_reception,
  DECISIONS [conforme, incoherence],
  SLA "4 hours", ESCALATION alerte_reception,
  TIMEOUT "1 working day", ON_TIMEOUT litige,
  ROUTES [conforme: enregistrement, incoherence: reclamation]
) RATIONALE "Reception : scan des etiquettes et codes, temperature, integrite des emballages, DLC, tracabilite des lots. Le SLA est en heures et non en jours ouvres parce que la marchandise, elle, ne chome pas."

DEFINE INVOCATION enregistrement AS (
  INVOKES approvisionner, RETRY registre, IRREVERSIBLE yes,
  ON_COMMITTED attente_echeance, ON_REJECTED litige, ON_HELD litige
) RATIONALE "Le flux ZQL approvisionner controle la ligne (article, quantite, prix unitaire) et l'ecrit au stock. IRREVERSIBLE : la marchandise est physiquement entree ; un stock ne se decommande pas, il se corrige par un autre mouvement declare."

DEFINE INVOCATION reclamation AS (
  INVOKES emettre_reclamation, RETRY registre, IRREVERSIBLE yes,
  ON_COMMITTED attente_reponse_reclamation, ON_REJECTED litige, ON_HELD litige
) RATIONALE "L'ecart constate part en reclamation chez le fournisseur. IRREVERSIBLE : une reclamation envoyee ne se rappelle pas ; elle se clot, ce qui est un autre acte."

DEFINE EVENT_WAIT attente_reponse_reclamation AS (
  AWAITS reponse_reclamation, CORRELATED_BY reclamation_id,
  TIMEOUT "5 working days", ON_TIMEOUT litige,
  ON_RECEIVED cloture_reclamation
) RATIONALE "Cinq jours ouvres sans reponse : le dossier devient un litige, un etat declare ou un humain reprend la main."

DEFINE INVOCATION cloture_reclamation AS (
  INVOKES cloturer_reclamation, RETRY registre, IRREVERSIBLE yes,
  ON_COMMITTED enregistrement, ON_REJECTED litige, ON_HELD litige
) RATIONALE "La reclamation close (avoir, remplacement, geste commercial) ramene la ligne corrigee au meme enregistrement de stock."

DEFINE TIMER_WAIT attente_echeance AS (
  AWAITS "the 5th working day of next month", ON_DUE reglement
) RATIONALE "L'echeance de prelevement est un repere metier mensuel, pas une duree : Rule 91 portee de l'affichage au calcul. Elle se resout une fois, contre le calendrier epingle a l'ouverture de l'instance."

DEFINE INVOCATION reglement AS (
  INVOKES regler_facture, RETRY registre, IRREVERSIBLE yes,
  ON_COMMITTED reglee, ON_REJECTED impayee, ON_HELD impayee
) RATIONALE "Le reglement est irreversible par nature : l'argent est parti. Un remboursement serait un autre workflow, avec sa propre preuve -- jamais une compensation silencieuse de celui-ci."

DEFINE COMPENSATION annulation AS (
  ON_COMPENSATED annulee, ON_FAILED compensation_impossible
) RATIONALE "Le seul chemin compensatoire du cycle : il deroule les invocations compensables achevees, de la plus recente a la plus ancienne. Ici cela signifie annuler_commande_fournisseur, et rien d'autre -- aucun des actes IRREVERSIBLE n'a pu s'executer sur ce chemin."

DEFINE TERMINAL reglee AS (OUTCOME success) RATIONALE "Cycle complet : commandee, confirmee, livree, controlee, reglee."
DEFINE TERMINAL refusee_a_l_emission AS (OUTCOME refused) RATIONALE "Refusee par une norme ZQL avant tout envoi."
DEFINE TERMINAL refusee_par_fournisseur AS (OUTCOME refused) RATIONALE "Le fournisseur a refuse la commande, avec sa decision au registre."
DEFINE TERMINAL annulee AS (OUTCOME abandoned) RATIONALE "Annulee et compensee : la commande emise a ete annulee chez le fournisseur, et le registre porte les deux actes."
DEFINE TERMINAL abandonnee AS (OUTCOME abandoned) RATIONALE "Aucune confirmation dans les delais."

DEFINE SUSPENDED litige AS (RESUMED_BY restaurateur, RESUMES_AT controle_reception) RATIONALE "Dossier ouvert : ni succes ni echec, un humain doit trancher. La reprise repasse par le controle de reception."
DEFINE SUSPENDED impayee AS (RESUMED_BY comptable, RESUMES_AT reglement) RATIONALE "Le reglement a ete refuse. La dette reste, visible, et le comptable reprend au meme acte."
DEFINE SUSPENDED compensation_impossible AS (RESUMED_BY restaurateur, RESUMES_AT annulation) RATIONALE "La compensation elle-meme a echoue. Rien ne continue en silence : c'est exactement la situation qu'un auditeur doit pouvoir trouver, et la reprise rejoue le deroulement."
