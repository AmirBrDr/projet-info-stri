# STRI1A / L3 IRT – 2025/2026 — Projet Informatique
## Service d’annuaires partagés

### Présentation Générale du Projet

#### 1. Objectif Principal
Concevoir et développer une application distribuée client/serveur permettant de gérer des annuaires de contacts partagés entre utilisateurs. Le projet mettra en pratique les connaissances en programmation réseau, architecture logicielle et gestion de données.

#### 2. Organisation des Équipes
- Étudiants non-alternants : groupes de 3 personnes  
- Étudiants alternants : groupes de 4 personnes

⚠ Important : chaque membre de l'équipe doit contribuer activement. Vous devrez fournir un document détaillant :
- la répartition des tâches (en pourcentage),
- qui a réalisé quelle partie,
- le planning de réalisation des tâches.

---

## 3. Description Fonctionnelle de l'Application

L'application permettra à plusieurs utilisateurs de gérer leurs propres annuaires de contacts tout en pouvant consulter les annuaires d'autres utilisateurs (selon permissions).

### Côté Serveur
Le serveur constitue le cœur de l'application et doit :
- Stocker les données dans des fichiers texte/CSV (⚠ INTERDICTION d'utiliser une base de données).
- Gérer plusieurs annuaires simultanément.
- Associer un annuaire unique à chaque compte utilisateur.
- Assurer la persistance des données entre les sessions.
- Gérer les permissions d'accès aux annuaires.

### Côté Client
L'interface client propose :
- Un menu textuel interactif (ligne de commande).
- Un système d'authentification sécurisée.
- Des actions différenciées selon le profil utilisateur (administrateur ou utilisateur).

Au lancement du client, un menu texte sera affiché pour choisir l’action à réaliser. Il faut d'abord se connecter (paramètres d’authentification). Après connexion, les actions disponibles dépendront du profil : administrateur du serveur ou utilisateur.

### Structure des Données
Pour chaque contact dans l’annuaire, stocker :
- nom (obligatoire)
- prénom (obligatoire)
- numéro de téléphone portable
- adresse postale
- adresse mail (obligatoire)

Conseil : prévoir une validation des formats (email, téléphone) pour assurer la qualité des données.

---

## 4. Profils Utilisateurs et Fonctionnalités

### Administrateur du serveur
- Gère les comptes utilisateurs (création, suppression, modification, liste…).
- À chaque compte créé, un annuaire est créé et associé à ce compte.

### Utilisateur (ayant un compte)
Après connexion, l'utilisateur peut :
- Gérer son annuaire : ajout, suppression, modification d’un contact, export/import CSV, etc.
- Gérer les permissions relatives à son annuaire (autorisation, révocation…).
- Consulter un autre annuaire si le propriétaire a donné les permissions nécessaires.

---

## 5. Communication Réseau Client/Serveur

Vous n’aurez pas à implémenter les fonctions de communication réseau. Considérer les éléments suivants :
- Le serveur est créé par la fonction `creer_serveur()`.
- Le client se connecte via `connecter_serveur()` et se déconnecte via `deconnecter_serveur()`.
- Les échanges de PDU se font par `envoyer_PDU()` et `recevoir_PDU()`.
- Vous pouvez structurer la PDU en JSON ou utiliser un format textuel similaire à HTTP.

---

# Planning et Livrables

Le projet comprend 3 étapes.

Dates limites de dépôt :
- Non Alternants : Dimanche 4 janvier à 22h (pour les étapes 1 et 2)
- Alternants : Dimanche 11 janvier à 22h (pour les étapes 1 et 2)
- Date limite étape 3 :
  - Non Alternants : Dimanche 18 janvier à 22h
  - Alternants : Dimanche 25 janvier à 22h

---

## Étape 1 : Spécification Protocolaire (RFC)
But : rédiger une RFC contenant la spécification protocolaire de l’application.

La RFC doit contenir au minimum :
- Une introduction présentant l’objectif de l’application.
- Le format des unités de données du protocole (PDU).
- Les types de requête/réponse et leurs descriptions.
- Les codes de succès et d’erreurs utilisés et leurs descriptions.
- Des exemples d’échanges requête/réponse : scénarios nominaux et scénarios d'erreur, avec diagrammes de séquence.

Ressources :
- Site officiel des RFC : http://www.rfc-editor.org/
- Traductions françaises : http://abcdrfc.free.fr/
- Exemples : RFC 2616 (HTTP), RFC 5321 (SMTP)

Livrable : Dossier de spécification protocolaire — PDF nommé `RFC_Annuaires_GroupeX.pdf`

---

## Étape 2 : Conception de l'Architecture Logicielle
But : écrire les algorithmes généraux du client et du serveur en démarche top-down.

Exigences :
- Au moins deux niveaux de raffinage (niveau 1 : algorithme succinct tenant sur une page A4 ; niveau 2 : algorithmes des fonctions appelées).
- Présenter algorithmes haut-niveau du client et du serveur.

Livrable : Dossier de conception (Algorithmes – Structures des données – Gestion des cas limites) — PDF nommé `Conception_Annuaires_GroupeX.pdf`

---

## Étape 3 : Codage fonctionnel et tests unitaires
Réalisation en Python des fonctions suivantes (minimum) :
- Creation_Compte : création d’un compte utilisateur par l’administrateur.
- Ajout_Contact : ajout d’un contact dans l’annuaire par l’utilisateur.
- Recherche_Contact : recherche d’un contact dans l’annuaire d’un utilisateur.
- Liste_Contacts : lister les contacts de l’annuaire d’un utilisateur.

- Les non-alternants doivent réaliser 3 fonctions supplémentaires au choix.

Test unitaire :
- Saisir les données nécessaires, les passer en paramètres, et afficher le résultat renvoyé par l’exécution.
- Montrer les modifications effectuées dans les fichiers stockés.

### Exigences de codage
- Code Python 3 propre et commenté.
- Respect des conventions PEP 8.
- Gestion des exceptions.
- Documentation des fonctions (docstrings).
- Tests unitaires exhaustifs avec assertions.
- Utilisation de fichiers CSV pour le stockage.

Livrables :
- Document de code (PDF) : `Code_Annuaires_GroupeX.pdf`.
- Code source complet des fonctions (.py).
- Code des tests unitaires.
- Explications des choix techniques.
- Capsule vidéo de démonstration (8–10 minutes) hébergée sur YouTube, Vimeo, ou autre (ne pas héberger sur le LMS). Le lien de la vidéo doit figurer dans la page de garde du document de code.

Contenu attendu dans la vidéo :
- Présentation rapide de l'architecture logicielle (fonctions + fichiers).
- Exécution des tests pour chaque fonction.
- Commentaires en direct expliquant les résultats.
- Démonstration des modifications dans les fichiers CSV.

---

## Modalités de dépôt
- Format : Un fichier ZIP contenant tous les livrables.
- Nom du ZIP : `Projet_Annuaires_GroupeX_EtapeY.zip`
- Plateforme : déposer sur le site stri.fr (sauf la vidéo qui doit être hébergée ailleurs).

Contenu du ZIP :
- Documents PDF (RFC, Conception, Code).
- Fichiers Python (.py) dans un répertoire spécifique.
- Document de code avec le lien de la vidéo.
- Document des prompts et outils IA utilisés (si vous avez eu recours à l’IA générative).
- Document contenant le planning des tâches et la répartition entre les membres du groupe.

---

## Recommandations

Organisation du travail :
- Utiliser un outil de gestion de projet (Trello, Notion, ...).
- Utiliser un gestionnaire de versions (Git recommandé).
- Organiser des réunions d'équipe régulières.
- Tenir un journal de bord du projet.

Qualité du code :
- Commenter le code de manière pertinente.
- Tester régulièrement chaque fonction.
- Créer un fichier `README.md` expliquant comment lancer l'application.

Documentation :
- Rédiger clairement et structurer les documents.
- Utiliser des diagrammes lorsque c’est possible.
- Relire et corriger les fautes d'orthographe.
- Soigner la présentation (mise en page, hiérarchie des titres).

---

## FAQ

Q1 : Peut-on utiliser SQLite ou une autre base de données ?  
A1 : ❌ Non — l'utilisation de bases de données est strictement interdite. Utiliser des fichiers texte/CSV.

Q2 : Quel langage pour les étapes 1 et 2 ?  
A2 : Les étapes 1 et 2 sont indépendantes du langage. Seule l'étape 3 impose Python.

Q3 : Comment gérer plusieurs clients simultanés ?  
A3 : Aborder la problématique dans l'étape 2 (conception). Une approche simple : traiter les requêtes séquentiellement.

Q4 : Le serveur doit-il avoir une interface graphique ?  
A4 : Non — une interface en ligne de commande suffit.

Q5 : L’application doit-elle s’exécuter en réseau ?  
A5 : Non — vous n’avez pas à implémenter le réseau dans l’étape 3. Prévoir l’utilisation des fonctions réseau indiquées dans la présentation.

Q6 : Comment stocker les mots de passe de manière sécurisée ?  
A6 : Utiliser un hachage (par ex. `hashlib` en Python). Ne pas stocker les mots de passe en clair.

Q7 : Combien de temps doit durer la vidéo de démonstration ?  
A7 : Entre 8 et 10 minutes maximum.

---

Fin du document.
