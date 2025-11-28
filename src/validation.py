"""
Module de validation des données - Data Validation Module

Ce module fournit des fonctions de validation pour les données
utilisateur et contact (email, téléphone, etc.).
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Valide le format d'une adresse email.

    Args:
        email: Adresse email à valider

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    if not email:
        return False, "L'adresse email est obligatoire"

    # Expression régulière pour valider un email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True, ""
    else:
        return False, "Format d'adresse email invalide"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Valide le format d'un numéro de téléphone.

    Args:
        phone: Numéro de téléphone à valider

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    if not phone:
        # Le téléphone n'est pas obligatoire
        return True, ""

    # Supprimer les espaces et tirets pour la validation
    cleaned_phone = re.sub(r'[\s\-\.]', '', phone)

    # Accepter les formats avec ou sans indicatif pays
    # Ex: 0612345678, +33612345678, 0033612345678
    pattern = r'^(\+?\d{1,3})?[0-9]{9,10}$'

    if re.match(pattern, cleaned_phone):
        return True, ""
    else:
        return False, "Format de numéro de téléphone invalide"


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Valide le format d'un nom d'utilisateur.

    Args:
        username: Nom d'utilisateur à valider

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    if not username:
        return False, "Le nom d'utilisateur est obligatoire"

    if len(username) < 3:
        return False, "Le nom d'utilisateur doit contenir au moins 3 caractères"

    if len(username) > 50:
        return False, "Le nom d'utilisateur ne peut pas dépasser 50 caractères"

    # Seuls les caractères alphanumériques et underscores sont autorisés
    pattern = r'^[a-zA-Z0-9_]+$'

    if re.match(pattern, username):
        return True, ""
    else:
        return False, (
            "Le nom d'utilisateur ne peut contenir que des lettres, "
            "chiffres et underscores"
        )


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Valide le format d'un mot de passe.

    Args:
        password: Mot de passe à valider

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    if not password:
        return False, "Le mot de passe est obligatoire"

    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères"

    return True, ""


def validate_nom(nom: str) -> Tuple[bool, str]:
    """
    Valide le format d'un nom.

    Args:
        nom: Nom à valider

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    if not nom:
        return False, "Le nom est obligatoire"

    if len(nom) > 100:
        return False, "Le nom ne peut pas dépasser 100 caractères"

    return True, ""


def validate_prenom(prenom: str) -> Tuple[bool, str]:
    """
    Valide le format d'un prénom.

    Args:
        prenom: Prénom à valider

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    if not prenom:
        return False, "Le prénom est obligatoire"

    if len(prenom) > 100:
        return False, "Le prénom ne peut pas dépasser 100 caractères"

    return True, ""


def validate_contact(contact: dict) -> Tuple[bool, str]:
    """
    Valide les données d'un contact.

    Args:
        contact: Dictionnaire contenant les données du contact

    Returns:
        Tuple[bool, str]: (validité, message d'erreur si invalide)
    """
    # Valider le nom (obligatoire)
    valid, msg = validate_nom(contact.get('nom', ''))
    if not valid:
        return False, msg

    # Valider le prénom (obligatoire)
    valid, msg = validate_prenom(contact.get('prenom', ''))
    if not valid:
        return False, msg

    # Valider l'email (obligatoire)
    valid, msg = validate_email(contact.get('email', ''))
    if not valid:
        return False, msg

    # Valider le téléphone (optionnel)
    valid, msg = validate_phone(contact.get('telephone', ''))
    if not valid:
        return False, msg

    return True, ""
