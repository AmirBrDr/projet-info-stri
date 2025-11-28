# Guide d'utilisation - Service d'annuaires partagés

## 🚀 Comment lancer l'application

### Prérequis
- Python 3.6 ou supérieur
- Aucune dépendance externe requise (utilisation uniquement de la bibliothèque standard Python)

### Installation
Clonez le dépôt et naviguez vers le répertoire du projet:

```bash
git clone <url-du-depot>
cd projet-info-stri
```

### Lancer l'application
Exécutez l'application en ligne de commande:

```bash
python src/main.py
```

Ou depuis n'importe quel répertoire:

```bash
python /chemin/vers/projet-info-stri/src/main.py
```

### Exécuter les tests unitaires
Pour exécuter tous les tests:

```bash
python run_tests.py
```

Ou pour exécuter un module de test spécifique:

```bash
python -m unittest tests.test_accounts -v
```

---

## 📁 Structure du projet

```
projet-info-stri/
├── README.md                 # Spécifications du projet
├── USAGE.md                  # Ce fichier (guide d'utilisation)
├── run_tests.py             # Script d'exécution des tests
├── src/                      # Code source
│   ├── __init__.py          # Initialisation du package
│   ├── main.py              # Point d'entrée de l'application
│   ├── accounts.py          # Gestion des comptes utilisateurs
│   ├── contacts.py          # Gestion des contacts
│   ├── permissions.py       # Gestion des permissions
│   ├── storage.py           # Stockage des données (CSV)
│   └── validation.py        # Validation des données
├── tests/                    # Tests unitaires
│   ├── __init__.py
│   ├── test_accounts.py     # Tests de gestion des comptes
│   ├── test_contacts.py     # Tests de gestion des contacts
│   ├── test_permissions.py  # Tests de gestion des permissions
│   ├── test_storage.py      # Tests de stockage
│   └── test_validation.py   # Tests de validation
└── data/                     # Données (fichiers CSV)
    ├── users.csv            # Comptes utilisateurs
    ├── permissions.csv      # Permissions d'accès
    └── annuaire_<user>.csv  # Annuaire de chaque utilisateur
```

---

## 🔧 Fonctionnalités implémentées

### Fonctions principales (Étape 3)
1. **Creation_Compte** - Création d'un compte utilisateur par l'administrateur
2. **Ajout_Contact** - Ajout d'un contact dans l'annuaire d'un utilisateur
3. **Recherche_Contact** - Recherche d'un contact dans un annuaire
4. **Liste_Contacts** - Lister les contacts d'un annuaire

### Fonctions supplémentaires
5. **Suppression_Contact** - Suppression d'un contact
6. **Modification_Contact** - Modification des informations d'un contact
7. **Export_CSV** - Exportation de l'annuaire vers un fichier CSV
8. **Import_CSV** - Importation de contacts depuis un fichier CSV
9. **Accorder_Permission** - Accorder l'accès à son annuaire à un autre utilisateur
10. **Révoquer_Permission** - Révoquer l'accès à son annuaire
11. **Liste_Permissions** - Lister les permissions accordées

### Fonctionnalités de sécurité
- Mots de passe hachés avec SHA-256
- Validation des formats (email, téléphone)
- Gestion des permissions d'accès aux annuaires
- Séparation des rôles administrateur/utilisateur

---

## 📖 Guide d'utilisation

### Premier lancement
Au premier lancement, l'application vous demandera de créer un compte administrateur:

```
INITIALISATION DU SYSTÈME
Aucun utilisateur n'existe. Création de l'administrateur initial.

Nom d'utilisateur administrateur: admin
Mot de passe: admin123
Email: admin@example.com

✓ Administrateur initialisé avec succès
```

### Menu principal
```
==================================================
       SERVICE D'ANNUAIRES PARTAGÉS
==================================================

1. Se connecter
2. Quitter
```

### Actions administrateur
- Créer/supprimer/modifier des comptes utilisateurs
- Lister tous les comptes
- Gérer son propre annuaire
- Accorder/révoquer des permissions

### Actions utilisateur
- Gérer son annuaire (ajouter, modifier, supprimer, rechercher des contacts)
- Exporter/importer son annuaire en CSV
- Gérer les permissions d'accès à son annuaire
- Consulter les annuaires auxquels il a accès

---

## 📝 Format des données

### Structure d'un contact
| Champ | Type | Obligatoire |
|-------|------|-------------|
| nom | string | ✓ |
| prenom | string | ✓ |
| email | string | ✓ |
| telephone | string | |
| adresse | string | |

### Exemple de fichier CSV annuaire
```csv
nom,prenom,telephone,adresse,email
Dupont,Jean,0612345678,123 Rue de Paris,jean.dupont@email.com
Martin,Marie,0698765432,456 Avenue des Champs,marie.martin@email.com
```

---

## 🔒 Sécurité

### Hachage des mots de passe
Les mots de passe sont hachés avec l'algorithme SHA-256 avant d'être stockés dans le fichier `users.csv`. Ils ne sont jamais stockés en clair.

### Permissions d'accès
Chaque utilisateur peut accorder ou révoquer l'accès à son annuaire. Types de permissions:
- **read** : Lecture seule de l'annuaire
- **write** : Modification de l'annuaire
- **all** : Tous les droits

---

## 🧪 Tests unitaires

Les tests unitaires couvrent les modules suivants:
- **test_storage.py** : Tests du module de stockage CSV
- **test_validation.py** : Tests de validation des données
- **test_accounts.py** : Tests de gestion des comptes
- **test_contacts.py** : Tests de gestion des contacts
- **test_permissions.py** : Tests de gestion des permissions

Pour exécuter les tests:
```bash
python run_tests.py
```

---

## 📚 Documentation des fonctions

Toutes les fonctions sont documentées avec des docstrings conformes aux conventions Python. Les docstrings incluent:
- Description de la fonction
- Arguments et leurs types
- Valeurs de retour
- Exemples d'utilisation

Exemple:
```python
def ajout_contact(
    username: str,
    nom: str,
    prenom: str,
    email: str,
    telephone: str = '',
    adresse: str = ''
) -> Tuple[bool, str]:
    """
    Ajoute un nouveau contact dans l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur propriétaire de l'annuaire
        nom: Nom du contact (obligatoire)
        prenom: Prénom du contact (obligatoire)
        email: Adresse email du contact (obligatoire)
        telephone: Numéro de téléphone du contact (optionnel)
        adresse: Adresse postale du contact (optionnel)

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = ajout_contact('user1', 'Dupont', 'Jean', 'jean@mail.com')
        >>> print(success, msg)
        True Contact ajouté avec succès
    """
```

---

## ⚠️ Notes importantes

1. **Pas de base de données** : Conformément aux spécifications, l'application utilise uniquement des fichiers CSV pour le stockage.

2. **Communication réseau** : Les fonctions de communication réseau (`creer_serveur()`, `connecter_serveur()`, etc.) ne sont pas implémentées car elles seront fournies séparément.

3. **Format des PDU** : L'architecture est conçue pour être compatible avec un protocole de communication JSON.
