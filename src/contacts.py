"""
Module de gestion des contacts - Contact Management Module

Ce module implémente les fonctions de gestion des contacts dans
les annuaires des utilisateurs.
"""

import csv
import os
from typing import Dict, List, Optional, Tuple

from .storage import (
    get_contacts,
    save_contact,
    update_contact,
    delete_contact,
    get_annuaire_path,
    has_permission,
    get_user,
    CONTACT_FIELDNAMES,
    ensure_data_dir
)
from .validation import validate_contact, validate_email


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
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    # Créer le dictionnaire du contact
    contact = {
        'nom': nom,
        'prenom': prenom,
        'email': email,
        'telephone': telephone,
        'adresse': adresse
    }

    # Valider les données du contact
    valid, msg = validate_contact(contact)
    if not valid:
        return False, msg

    # Vérifier si l'email existe déjà dans l'annuaire
    contacts = get_contacts(username)
    for c in contacts:
        if c['email'] == email:
            return False, "Un contact avec cette adresse email existe déjà"

    # Ajouter le contact
    save_contact(username, contact)

    return True, "Contact ajouté avec succès"


def recherche_contact(
    username: str,
    target_username: str,
    critere: str,
    valeur: str
) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Recherche des contacts dans l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur qui effectue la recherche
        target_username: Nom d'utilisateur propriétaire de l'annuaire à consulter
        critere: Critère de recherche ('nom', 'prenom', 'email', 'telephone')
        valeur: Valeur à rechercher

    Returns:
        Tuple[bool, List[Dict[str, str]]]: (succès, liste des contacts trouvés)

    Example:
        >>> success, contacts = recherche_contact('user1', 'user1', 'nom', 'Dupont')
        >>> print(success, len(contacts))
        True 1
    """
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, []

    # Vérifier les permissions d'accès
    if not has_permission(target_username, username, 'read'):
        return False, []

    # Valider le critère de recherche
    valid_criteres = ['nom', 'prenom', 'email', 'telephone', 'adresse']
    if critere not in valid_criteres:
        return False, []

    # Récupérer les contacts
    contacts = get_contacts(target_username)

    # Filtrer les contacts selon le critère
    valeur_lower = valeur.lower()
    results = [
        c for c in contacts
        if valeur_lower in c.get(critere, '').lower()
    ]

    return True, results


def liste_contacts(
    username: str,
    target_username: Optional[str] = None
) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Liste tous les contacts d'un annuaire.

    Args:
        username: Nom d'utilisateur qui effectue la consultation
        target_username: Nom d'utilisateur propriétaire de l'annuaire
                         (si None, consulte son propre annuaire)

    Returns:
        Tuple[bool, List[Dict[str, str]]]: (succès, liste des contacts)

    Example:
        >>> success, contacts = liste_contacts('user1')
        >>> print(success, type(contacts))
        True <class 'list'>
    """
    # Si target_username non spécifié, utiliser l'annuaire de l'utilisateur
    if target_username is None:
        target_username = username

    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, []

    # Vérifier les permissions d'accès
    if not has_permission(target_username, username, 'read'):
        return False, []

    # Récupérer et retourner les contacts
    contacts = get_contacts(target_username)
    return True, contacts


def suppression_contact(username: str, email: str) -> Tuple[bool, str]:
    """
    Supprime un contact de l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur propriétaire de l'annuaire
        email: Adresse email du contact à supprimer

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = suppression_contact('user1', 'jean@mail.com')
        >>> print(success, msg)
        True Contact supprimé avec succès
    """
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    # Vérifier que le contact existe
    contacts = get_contacts(username)
    contact_exists = any(c['email'] == email for c in contacts)
    if not contact_exists:
        return False, "Contact non trouvé"

    # Supprimer le contact
    if delete_contact(username, email):
        return True, "Contact supprimé avec succès"
    else:
        return False, "Erreur lors de la suppression du contact"


def modification_contact(
    username: str,
    email: str,
    nouveau_nom: Optional[str] = None,
    nouveau_prenom: Optional[str] = None,
    nouvel_email: Optional[str] = None,
    nouveau_telephone: Optional[str] = None,
    nouvelle_adresse: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Modifie un contact dans l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur propriétaire de l'annuaire
        email: Adresse email actuelle du contact (identifiant)
        nouveau_nom: Nouveau nom (optionnel)
        nouveau_prenom: Nouveau prénom (optionnel)
        nouvel_email: Nouvelle adresse email (optionnel)
        nouveau_telephone: Nouveau numéro de téléphone (optionnel)
        nouvelle_adresse: Nouvelle adresse postale (optionnel)

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = modification_contact('user1', 'jean@mail.com', nouveau_telephone='0612345678')
        >>> print(success, msg)
        True Contact modifié avec succès
    """
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    # Vérifier que le contact existe
    contacts = get_contacts(username)
    current_contact = None
    for c in contacts:
        if c['email'] == email:
            current_contact = c
            break

    if not current_contact:
        return False, "Contact non trouvé"

    # Construire les données mises à jour
    updated_data = {}

    if nouveau_nom:
        updated_data['nom'] = nouveau_nom

    if nouveau_prenom:
        updated_data['prenom'] = nouveau_prenom

    if nouvel_email:
        # Vérifier que le nouvel email n'existe pas déjà
        for c in contacts:
            if c['email'] == nouvel_email and c['email'] != email:
                return False, "Un contact avec cette adresse email existe déjà"
        valid, msg = validate_email(nouvel_email)
        if not valid:
            return False, msg
        updated_data['email'] = nouvel_email

    if nouveau_telephone is not None:
        updated_data['telephone'] = nouveau_telephone

    if nouvelle_adresse is not None:
        updated_data['adresse'] = nouvelle_adresse

    if not updated_data:
        return False, "Aucune modification spécifiée"

    # Valider les nouvelles données
    new_contact = current_contact.copy()
    new_contact.update(updated_data)
    valid, msg = validate_contact(new_contact)
    if not valid:
        return False, msg

    # Mettre à jour le contact
    if update_contact(username, email, updated_data):
        return True, "Contact modifié avec succès"
    else:
        return False, "Erreur lors de la modification du contact"


def export_csv(username: str, filepath: str) -> Tuple[bool, str]:
    """
    Exporte l'annuaire d'un utilisateur vers un fichier CSV.

    Args:
        username: Nom d'utilisateur propriétaire de l'annuaire
        filepath: Chemin du fichier CSV de destination

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = export_csv('user1', '/tmp/export.csv')
        >>> print(success, msg)
        True Annuaire exporté avec succès
    """
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    try:
        contacts = get_contacts(username)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CONTACT_FIELDNAMES)
            writer.writeheader()
            writer.writerows(contacts)

        return True, f"Annuaire exporté avec succès vers {filepath}"

    except IOError as e:
        return False, f"Erreur lors de l'export: {str(e)}"


def import_csv(username: str, filepath: str) -> Tuple[bool, str]:
    """
    Importe des contacts depuis un fichier CSV vers l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur propriétaire de l'annuaire
        filepath: Chemin du fichier CSV source

    Returns:
        Tuple[bool, str]: (succès, message)

    Example:
        >>> success, msg = import_csv('user1', '/tmp/import.csv')
        >>> print(success, msg)
        True 5 contacts importés avec succès
    """
    # Vérifier que l'utilisateur existe
    user = get_user(username)
    if not user:
        return False, "Utilisateur non trouvé"

    if not os.path.exists(filepath):
        return False, "Fichier non trouvé"

    try:
        imported_count = 0
        errors = []

        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Récupérer les données du contact
                contact = {
                    'nom': row.get('nom', ''),
                    'prenom': row.get('prenom', ''),
                    'email': row.get('email', ''),
                    'telephone': row.get('telephone', ''),
                    'adresse': row.get('adresse', '')
                }

                # Valider le contact
                valid, msg = validate_contact(contact)
                if not valid:
                    errors.append(f"Contact invalide ({contact.get('email', 'N/A')}): {msg}")
                    continue

                # Vérifier si l'email existe déjà
                contacts = get_contacts(username)
                email_exists = any(c['email'] == contact['email'] for c in contacts)
                if email_exists:
                    errors.append(f"Contact ignoré (email déjà existant): {contact['email']}")
                    continue

                # Ajouter le contact
                save_contact(username, contact)
                imported_count += 1

        if errors:
            error_msg = "; ".join(errors[:5])  # Limiter à 5 erreurs
            if len(errors) > 5:
                error_msg += f" ... et {len(errors) - 5} autres erreurs"
            return True, f"{imported_count} contacts importés. Erreurs: {error_msg}"
        else:
            return True, f"{imported_count} contacts importés avec succès"

    except IOError as e:
        return False, f"Erreur lors de l'import: {str(e)}"
    except Exception as e:
        return False, f"Erreur inattendue: {str(e)}"
