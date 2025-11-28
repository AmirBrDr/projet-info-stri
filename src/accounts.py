"""
Module de gestion des comptes utilisateurs - User Account Management Module

Ce module implémente les fonctions de gestion des comptes utilisateurs,
incluant la création, la modification, la suppression et l'authentification.
"""

from typing import Dict, List, Optional, Tuple

from .storage import (
    get_all_users,
    get_user,
    save_user,
    update_user,
    delete_user,
    hash_password,
    create_annuaire
)
from .validation import (
    validate_username,
    validate_password,
    validate_email
)


def creation_compte(
    admin_username: str,
    username: str,
    password: str,
    email: str,
    is_admin: bool = False
) -> Tuple[bool, str]:
    """
    Crée un nouveau compte utilisateur (fonction administrateur).

    Cette fonction permet à un administrateur de créer un nouveau compte
    utilisateur. Un annuaire vide est automatiquement créé et associé
    au nouveau compte.

    Args:
        admin_username: Nom d'utilisateur de l'administrateur qui crée le compte
        username: Nom d'utilisateur du nouveau compte
        password: Mot de passe du nouveau compte
        email: Adresse email du nouveau compte
        is_admin: True si le nouveau compte doit être administrateur

    Returns:
        Tuple[bool, str]: (succès, message)

    Raises:
        PermissionError: Si l'utilisateur n'est pas administrateur

    Example:
        >>> success, msg = creation_compte('admin', 'new_user', 'pass123', 'user@mail.com')
        >>> print(success, msg)
        True Compte créé avec succès
    """
    # Vérifier que l'utilisateur est administrateur
    admin = get_user(admin_username)
    if not admin or admin.get('is_admin') != 'True':
        return False, "Permission refusée: seul un administrateur peut créer des comptes"

    # Valider le nom d'utilisateur
    valid, msg = validate_username(username)
    if not valid:
        return False, msg

    # Valider le mot de passe
    valid, msg = validate_password(password)
    if not valid:
        return False, msg

    # Valider l'email
    valid, msg = validate_email(email)
    if not valid:
        return False, msg

    # Vérifier si le nom d'utilisateur existe déjà
    if get_user(username):
        return False, "Ce nom d'utilisateur existe déjà"

    # Vérifier si l'email est déjà utilisé
    users = get_all_users()
    for user in users:
        if user.get('email') == email:
            return False, "Cette adresse email est déjà utilisée"

    # Créer le compte
    new_user = {
        'username': username,
        'password_hash': hash_password(password),
        'is_admin': str(is_admin),
        'email': email
    }
    save_user(new_user)

    # Créer l'annuaire associé
    create_annuaire(username)

    return True, "Compte créé avec succès"


def suppression_compte(
    admin_username: str,
    username: str
) -> Tuple[bool, str]:
    """
    Supprime un compte utilisateur (fonction administrateur).

    Cette fonction permet à un administrateur de supprimer un compte
    utilisateur ainsi que son annuaire et ses permissions associées.

    Args:
        admin_username: Nom d'utilisateur de l'administrateur
        username: Nom d'utilisateur du compte à supprimer

    Returns:
        Tuple[bool, str]: (succès, message)
    """
    # Vérifier que l'utilisateur est administrateur
    admin = get_user(admin_username)
    if not admin or admin.get('is_admin') != 'True':
        return False, "Permission refusée: seul un administrateur peut supprimer des comptes"

    # Vérifier que le compte existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    # Empêcher la suppression de son propre compte admin
    if admin_username == username:
        return False, "Impossible de supprimer votre propre compte administrateur"

    # Supprimer le compte
    if delete_user(username):
        return True, "Compte supprimé avec succès"
    else:
        return False, "Erreur lors de la suppression du compte"


def modification_compte(
    admin_username: str,
    username: str,
    new_password: Optional[str] = None,
    new_email: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Modifie un compte utilisateur (fonction administrateur).

    Args:
        admin_username: Nom d'utilisateur de l'administrateur
        username: Nom d'utilisateur du compte à modifier
        new_password: Nouveau mot de passe (optionnel)
        new_email: Nouvelle adresse email (optionnel)

    Returns:
        Tuple[bool, str]: (succès, message)
    """
    # Vérifier que l'utilisateur est administrateur
    admin = get_user(admin_username)
    if not admin or admin.get('is_admin') != 'True':
        return False, "Permission refusée: seul un administrateur peut modifier des comptes"

    # Vérifier que le compte existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    updated_data = {}

    # Valider et ajouter le nouveau mot de passe
    if new_password:
        valid, msg = validate_password(new_password)
        if not valid:
            return False, msg
        updated_data['password_hash'] = hash_password(new_password)

    # Valider et ajouter le nouvel email
    if new_email:
        valid, msg = validate_email(new_email)
        if not valid:
            return False, msg

        # Vérifier si l'email est déjà utilisé par un autre utilisateur
        users = get_all_users()
        for u in users:
            if u.get('email') == new_email and u.get('username') != username:
                return False, "Cette adresse email est déjà utilisée"

        updated_data['email'] = new_email

    if not updated_data:
        return False, "Aucune modification spécifiée"

    # Mettre à jour le compte
    if update_user(username, updated_data):
        return True, "Compte modifié avec succès"
    else:
        return False, "Erreur lors de la modification du compte"


def liste_comptes(admin_username: str) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Liste tous les comptes utilisateurs (fonction administrateur).

    Args:
        admin_username: Nom d'utilisateur de l'administrateur

    Returns:
        Tuple[bool, List[Dict[str, str]]]: (succès, liste des utilisateurs)
    """
    # Vérifier que l'utilisateur est administrateur
    admin = get_user(admin_username)
    if not admin or admin.get('is_admin') != 'True':
        return False, []

    users = get_all_users()
    # Retourner les utilisateurs sans les hash de mot de passe
    safe_users = []
    for user in users:
        safe_user = {
            'username': user['username'],
            'email': user['email'],
            'is_admin': user['is_admin']
        }
        safe_users.append(safe_user)

    return True, safe_users


def authentifier(username: str, password: str) -> Tuple[bool, str]:
    """
    Authentifie un utilisateur avec son nom d'utilisateur et mot de passe.

    Args:
        username: Nom d'utilisateur
        password: Mot de passe en clair

    Returns:
        Tuple[bool, str]: (succès, message ou rôle si succès)
    """
    user = get_user(username)

    if not user:
        return False, "Utilisateur non trouvé"

    if user['password_hash'] != hash_password(password):
        return False, "Mot de passe incorrect"

    role = "administrateur" if user['is_admin'] == 'True' else "utilisateur"
    return True, f"Authentification réussie - Rôle: {role}"


def est_administrateur(username: str) -> bool:
    """
    Vérifie si un utilisateur est administrateur.

    Args:
        username: Nom d'utilisateur

    Returns:
        bool: True si l'utilisateur est administrateur, False sinon
    """
    user = get_user(username)
    return user is not None and user.get('is_admin') == 'True'


def initialiser_admin(username: str, password: str, email: str) -> Tuple[bool, str]:
    """
    Initialise le premier compte administrateur.

    Cette fonction ne peut être appelée que s'il n'existe aucun
    utilisateur dans le système.

    Args:
        username: Nom d'utilisateur de l'administrateur
        password: Mot de passe de l'administrateur
        email: Adresse email de l'administrateur

    Returns:
        Tuple[bool, str]: (succès, message)
    """
    users = get_all_users()

    if users:
        return False, "Un administrateur existe déjà"

    # Valider les données
    valid, msg = validate_username(username)
    if not valid:
        return False, msg

    valid, msg = validate_password(password)
    if not valid:
        return False, msg

    valid, msg = validate_email(email)
    if not valid:
        return False, msg

    # Créer le compte administrateur
    admin_user = {
        'username': username,
        'password_hash': hash_password(password),
        'is_admin': 'True',
        'email': email
    }
    save_user(admin_user)
    create_annuaire(username)

    return True, "Administrateur initialisé avec succès"
