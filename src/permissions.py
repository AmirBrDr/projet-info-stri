"""
Module de gestion des permissions - Permission Management Module

Ce module implémente les fonctions de gestion des permissions d'accès
aux annuaires entre utilisateurs.
"""

from typing import Dict, List, Tuple

from .storage import (
    get_user,
    add_permission,
    remove_permission,
    get_permissions,
    get_user_permissions,
    has_permission
)


def accorder_permission(
    owner: str,
    granted_to: str,
    permission_type: str = 'read'
) -> Tuple[bool, str]:
    """
    Accorde une permission d'accès à un utilisateur pour consulter un annuaire.

    Args:
        owner: Nom d'utilisateur propriétaire de l'annuaire
        granted_to: Nom d'utilisateur à qui accorder la permission
        permission_type: Type de permission ('read', 'write', 'all')

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = accorder_permission('user1', 'user2', 'read')
        >>> print(success, msg)
        True Permission accordée avec succès
    """
    # Vérifier que le propriétaire existe
    owner_user = get_user(owner)
    if not owner_user:
        return False, "Propriétaire non trouvé"

    # Vérifier que l'utilisateur bénéficiaire existe
    target_user = get_user(granted_to)
    if not target_user:
        return False, "Utilisateur bénéficiaire non trouvé"

    # Vérifier que le type de permission est valide
    valid_types = ['read', 'write', 'all']
    if permission_type not in valid_types:
        return False, f"Type de permission invalide. Valeurs possibles: {valid_types}"

    # Vérifier qu'on n'accorde pas la permission à soi-même
    if owner == granted_to:
        return False, "Impossible d'accorder une permission à soi-même"

    # Ajouter la permission
    if add_permission(owner, granted_to, permission_type):
        return True, "Permission accordée avec succès"
    else:
        return False, "Cette permission existe déjà"


def revoquer_permission(owner: str, granted_to: str) -> Tuple[bool, str]:
    """
    Révoque une permission d'accès d'un utilisateur à un annuaire.

    Args:
        owner: Nom d'utilisateur propriétaire de l'annuaire
        granted_to: Nom d'utilisateur dont la permission est révoquée

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = revoquer_permission('user1', 'user2')
        >>> print(success, msg)
        True Permission révoquée avec succès
    """
    # Vérifier que le propriétaire existe
    owner_user = get_user(owner)
    if not owner_user:
        return False, "Propriétaire non trouvé"

    # Révoquer la permission
    if remove_permission(owner, granted_to):
        return True, "Permission révoquée avec succès"
    else:
        return False, "Aucune permission à révoquer"


def liste_permissions(owner: str) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Liste toutes les permissions accordées par un propriétaire d'annuaire.

    Args:
        owner: Nom d'utilisateur propriétaire de l'annuaire

    Returns:
        Tuple[bool, List[Dict[str, str]]]: (succès, liste des permissions)

    Example:
        >>> success, permissions = liste_permissions('user1')
        >>> print(success, len(permissions))
        True 2
    """
    # Vérifier que le propriétaire existe
    owner_user = get_user(owner)
    if not owner_user:
        return False, []

    permissions = get_permissions(owner)
    return True, permissions


def liste_acces_accordes(username: str) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Liste tous les annuaires auxquels un utilisateur a accès.

    Args:
        username: Nom d'utilisateur

    Returns:
        Tuple[bool, List[Dict[str, str]]]: (succès, liste des accès)

    Example:
        >>> success, access_list = liste_acces_accordes('user2')
        >>> print(success, len(access_list))
        True 3
    """
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, []

    permissions = get_user_permissions(username)
    return True, permissions


def verifier_permission(
    owner: str,
    username: str,
    permission_type: str = 'read'
) -> bool:
    """
    Vérifie si un utilisateur a une permission spécifique sur un annuaire.

    Args:
        owner: Nom d'utilisateur propriétaire de l'annuaire
        username: Nom d'utilisateur qui veut accéder
        permission_type: Type de permission requis ('read', 'write', 'all')

    Returns:
        bool: True si l'utilisateur a la permission, False sinon

    Example:
        >>> has_access = verifier_permission('user1', 'user2', 'read')
        >>> print(has_access)
        True
    """
    return has_permission(owner, username, permission_type)
