"""
Application principale - Service d'annuaires partagés

Ce module fournit une interface en ligne de commande interactive
pour gérer les annuaires de contacts partagés.
"""

import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.accounts import (  # noqa: E402
    creation_compte,
    suppression_compte,
    modification_compte,
    liste_comptes,
    authentifier,
    est_administrateur,
    initialiser_admin
)
from src.contacts import (  # noqa: E402
    ajout_contact,
    recherche_contact,
    liste_contacts,
    suppression_contact,
    modification_contact,
    export_csv,
    import_csv
)
from src.permissions import (  # noqa: E402
    accorder_permission,
    revoquer_permission,
    liste_permissions,
    liste_acces_accordes
)
from src.storage import get_all_users, ensure_data_dir  # noqa: E402


def afficher_menu_principal():
    """Affiche le menu principal."""
    print("\n" + "=" * 50)
    print("       SERVICE D'ANNUAIRES PARTAGÉS")
    print("=" * 50)
    print("\n1. Se connecter")
    print("2. Quitter")
    print()


def afficher_menu_admin():
    """Affiche le menu administrateur."""
    print("\n" + "-" * 40)
    print("        MENU ADMINISTRATEUR")
    print("-" * 40)
    print("\n--- Gestion des comptes ---")
    print("1. Créer un compte utilisateur")
    print("2. Supprimer un compte utilisateur")
    print("3. Modifier un compte utilisateur")
    print("4. Lister tous les comptes")
    print("\n--- Mon annuaire ---")
    print("5. Ajouter un contact")
    print("6. Rechercher un contact")
    print("7. Lister mes contacts")
    print("8. Supprimer un contact")
    print("9. Modifier un contact")
    print("10. Exporter mon annuaire (CSV)")
    print("11. Importer des contacts (CSV)")
    print("\n--- Permissions ---")
    print("12. Accorder une permission")
    print("13. Révoquer une permission")
    print("14. Lister mes permissions accordées")
    print("15. Consulter un autre annuaire")
    print("\n0. Se déconnecter")
    print()


def afficher_menu_utilisateur():
    """Affiche le menu utilisateur."""
    print("\n" + "-" * 40)
    print("        MENU UTILISATEUR")
    print("-" * 40)
    print("\n--- Mon annuaire ---")
    print("1. Ajouter un contact")
    print("2. Rechercher un contact")
    print("3. Lister mes contacts")
    print("4. Supprimer un contact")
    print("5. Modifier un contact")
    print("6. Exporter mon annuaire (CSV)")
    print("7. Importer des contacts (CSV)")
    print("\n--- Permissions ---")
    print("8. Accorder une permission")
    print("9. Révoquer une permission")
    print("10. Lister mes permissions accordées")
    print("11. Lister mes accès à d'autres annuaires")
    print("12. Consulter un autre annuaire")
    print("\n0. Se déconnecter")
    print()


def saisir_contact():
    """Saisit les informations d'un contact."""
    print("\n--- Informations du contact ---")
    nom = input("Nom (obligatoire): ").strip()
    prenom = input("Prénom (obligatoire): ").strip()
    email = input("Email (obligatoire): ").strip()
    telephone = input("Téléphone (optionnel): ").strip()
    adresse = input("Adresse (optionnel): ").strip()
    return nom, prenom, email, telephone, adresse


def afficher_contacts(contacts):
    """Affiche une liste de contacts."""
    if not contacts:
        print("\nAucun contact trouvé.")
        return

    print(f"\n{len(contacts)} contact(s) trouvé(s):")
    print("-" * 60)
    for i, contact in enumerate(contacts, 1):
        print(f"\n[{i}] {contact['nom']} {contact['prenom']}")
        print(f"    Email: {contact['email']}")
        if contact.get('telephone'):
            print(f"    Téléphone: {contact['telephone']}")
        if contact.get('adresse'):
            print(f"    Adresse: {contact['adresse']}")
    print("-" * 60)


def gerer_session_admin(username):
    """Gère la session d'un administrateur."""
    while True:
        afficher_menu_admin()
        choix = input("Votre choix: ").strip()

        if choix == '0':
            print("Déconnexion...")
            break

        elif choix == '1':  # Créer un compte
            print("\n--- Création de compte ---")
            new_username = input("Nom d'utilisateur: ").strip()
            new_password = input("Mot de passe: ").strip()
            new_email = input("Email: ").strip()
            is_admin_str = input("Administrateur ? (o/n): ").strip().lower()
            is_admin = is_admin_str == 'o'

            success, msg = creation_compte(
                username, new_username, new_password, new_email, is_admin
            )
            print(f"\n{'✓' if success else '✗'} {msg}")

        elif choix == '2':  # Supprimer un compte
            print("\n--- Suppression de compte ---")
            target = input("Nom d'utilisateur à supprimer: ").strip()
            confirm = input(f"Confirmer la suppression de '{target}' ? (o/n): ")
            if confirm.lower() == 'o':
                success, msg = suppression_compte(username, target)
                print(f"\n{'✓' if success else '✗'} {msg}")
            else:
                print("Suppression annulée.")

        elif choix == '3':  # Modifier un compte
            print("\n--- Modification de compte ---")
            target = input("Nom d'utilisateur à modifier: ").strip()
            new_password = input("Nouveau mot de passe (laisser vide pour ne pas changer): ").strip() or None
            new_email = input("Nouvel email (laisser vide pour ne pas changer): ").strip() or None

            success, msg = modification_compte(username, target, new_password, new_email)
            print(f"\n{'✓' if success else '✗'} {msg}")

        elif choix == '4':  # Lister les comptes
            success, users = liste_comptes(username)
            if success:
                print(f"\n{len(users)} compte(s):")
                for user in users:
                    role = "Admin" if user['is_admin'] == 'True' else "User"
                    print(f"  - {user['username']} ({user['email']}) [{role}]")
            else:
                print("Erreur lors de la récupération des comptes.")

        elif choix in ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
            # Rediriger vers les fonctions utilisateur
            gerer_action_utilisateur(username, str(int(choix) - 4))

        else:
            print("Choix invalide.")


def gerer_session_utilisateur(username):
    """Gère la session d'un utilisateur standard."""
    while True:
        afficher_menu_utilisateur()
        choix = input("Votre choix: ").strip()

        if choix == '0':
            print("Déconnexion...")
            break

        gerer_action_utilisateur(username, choix)


def gerer_action_utilisateur(username, choix):
    """Gère une action utilisateur."""
    if choix == '1':  # Ajouter un contact
        nom, prenom, email, telephone, adresse = saisir_contact()
        success, msg = ajout_contact(username, nom, prenom, email, telephone, adresse)
        print(f"\n{'✓' if success else '✗'} {msg}")

    elif choix == '2':  # Rechercher un contact
        print("\n--- Recherche de contact ---")
        print("Critères: nom, prenom, email, telephone, adresse")
        critere = input("Critère de recherche: ").strip().lower()
        valeur = input("Valeur recherchée: ").strip()

        success, results = recherche_contact(username, username, critere, valeur)
        if success:
            afficher_contacts(results)
        else:
            print("Erreur lors de la recherche.")

    elif choix == '3':  # Lister les contacts
        success, contacts = liste_contacts(username)
        if success:
            afficher_contacts(contacts)
        else:
            print("Erreur lors de la récupération des contacts.")

    elif choix == '4':  # Supprimer un contact
        email = input("Email du contact à supprimer: ").strip()
        confirm = input(f"Confirmer la suppression ? (o/n): ")
        if confirm.lower() == 'o':
            success, msg = suppression_contact(username, email)
            print(f"\n{'✓' if success else '✗'} {msg}")
        else:
            print("Suppression annulée.")

    elif choix == '5':  # Modifier un contact
        print("\n--- Modification de contact ---")
        email = input("Email du contact à modifier: ").strip()
        print("(Laisser vide pour ne pas modifier)")
        nouveau_nom = input("Nouveau nom: ").strip() or None
        nouveau_prenom = input("Nouveau prénom: ").strip() or None
        nouvel_email = input("Nouvel email: ").strip() or None
        nouveau_telephone = input("Nouveau téléphone: ").strip()
        nouvelle_adresse = input("Nouvelle adresse: ").strip()

        # Convertir les chaînes vides en None pour les champs optionnels
        nouveau_telephone = nouveau_telephone if nouveau_telephone else None
        nouvelle_adresse = nouvelle_adresse if nouvelle_adresse else None

        success, msg = modification_contact(
            username, email, nouveau_nom, nouveau_prenom,
            nouvel_email, nouveau_telephone, nouvelle_adresse
        )
        print(f"\n{'✓' if success else '✗'} {msg}")

    elif choix == '6':  # Exporter CSV
        filepath = input("Chemin du fichier d'export: ").strip()
        success, msg = export_csv(username, filepath)
        print(f"\n{'✓' if success else '✗'} {msg}")

    elif choix == '7':  # Importer CSV
        filepath = input("Chemin du fichier à importer: ").strip()
        success, msg = import_csv(username, filepath)
        print(f"\n{'✓' if success else '✗'} {msg}")

    elif choix == '8':  # Accorder permission
        print("\n--- Accorder une permission ---")
        granted_to = input("Nom d'utilisateur bénéficiaire: ").strip()
        print("Types: read, write, all")
        permission_type = input("Type de permission: ").strip()

        success, msg = accorder_permission(username, granted_to, permission_type)
        print(f"\n{'✓' if success else '✗'} {msg}")

    elif choix == '9':  # Révoquer permission
        granted_to = input("Nom d'utilisateur à révoquer: ").strip()
        success, msg = revoquer_permission(username, granted_to)
        print(f"\n{'✓' if success else '✗'} {msg}")

    elif choix == '10':  # Lister permissions accordées
        success, permissions = liste_permissions(username)
        if success and permissions:
            print(f"\n{len(permissions)} permission(s) accordée(s):")
            for perm in permissions:
                print(f"  - {perm['granted_to']} ({perm['permission_type']})")
        elif success:
            print("Aucune permission accordée.")
        else:
            print("Erreur lors de la récupération des permissions.")

    elif choix == '11':  # Lister accès accordés
        success, access_list = liste_acces_accordes(username)
        if success and access_list:
            print(f"\n{len(access_list)} accès accordé(s):")
            for access in access_list:
                print(f"  - Annuaire de {access['owner']} ({access['permission_type']})")
        elif success:
            print("Aucun accès à d'autres annuaires.")
        else:
            print("Erreur lors de la récupération des accès.")

    elif choix == '12':  # Consulter autre annuaire
        target = input("Nom d'utilisateur de l'annuaire à consulter: ").strip()
        success, contacts = liste_contacts(username, target)
        if success:
            print(f"\nAnnuaire de {target}:")
            afficher_contacts(contacts)
        else:
            print("Accès refusé ou annuaire non trouvé.")

    else:
        print("Choix invalide.")


def main():
    """Point d'entrée principal de l'application."""
    # Initialiser le répertoire de données
    ensure_data_dir()

    # Vérifier s'il faut initialiser le premier administrateur
    users = get_all_users()
    if not users:
        print("\n" + "=" * 50)
        print("   INITIALISATION DU SYSTÈME")
        print("=" * 50)
        print("\nAucun utilisateur n'existe. Création de l'administrateur initial.")
        print()

        admin_username = input("Nom d'utilisateur administrateur: ").strip()
        admin_password = input("Mot de passe: ").strip()
        admin_email = input("Email: ").strip()

        success, msg = initialiser_admin(admin_username, admin_password, admin_email)
        if success:
            print(f"\n✓ {msg}")
        else:
            print(f"\n✗ {msg}")
            return

    # Boucle principale
    while True:
        afficher_menu_principal()
        choix = input("Votre choix: ").strip()

        if choix == '1':  # Se connecter
            print("\n--- Connexion ---")
            username = input("Nom d'utilisateur: ").strip()
            password = input("Mot de passe: ").strip()

            success, msg = authentifier(username, password)
            if success:
                print(f"\n✓ {msg}")

                if est_administrateur(username):
                    gerer_session_admin(username)
                else:
                    gerer_session_utilisateur(username)
            else:
                print(f"\n✗ {msg}")

        elif choix == '2':  # Quitter
            print("\nAu revoir!")
            break

        else:
            print("Choix invalide.")


if __name__ == '__main__':
    main()
