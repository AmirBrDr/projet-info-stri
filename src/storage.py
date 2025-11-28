"""
Module de stockage des données - Data Storage Module

Ce module gère la persistance des données dans des fichiers CSV.
Il fournit des fonctions pour lire, écrire et manipuler les données
des utilisateurs, contacts et permissions.
"""

import csv
import os
import hashlib
from typing import Dict, List, Optional, Any


# Chemins par défaut pour les fichiers de données
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
PERMISSIONS_FILE = os.path.join(DATA_DIR, 'permissions.csv')


def get_annuaire_path(username: str) -> str:
    """
    Retourne le chemin du fichier annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur

    Returns:
        str: Chemin du fichier CSV de l'annuaire
    """
    return os.path.join(DATA_DIR, f'annuaire_{username}.csv')


def ensure_data_dir() -> None:
    """
    S'assure que le répertoire de données existe.
    Crée le répertoire et les fichiers nécessaires s'ils n'existent pas.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Créer le fichier users.csv avec en-têtes s'il n'existe pas
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password_hash', 'is_admin', 'email'])

    # Créer le fichier permissions.csv avec en-têtes s'il n'existe pas
    if not os.path.exists(PERMISSIONS_FILE):
        with open(PERMISSIONS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['owner', 'granted_to', 'permission_type'])


def hash_password(password: str) -> str:
    """
    Hache un mot de passe en utilisant SHA-256.

    Args:
        password: Mot de passe en clair

    Returns:
        str: Hash SHA-256 du mot de passe
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def read_csv_file(filepath: str) -> List[Dict[str, str]]:
    """
    Lit un fichier CSV et retourne une liste de dictionnaires.

    Args:
        filepath: Chemin du fichier CSV

    Returns:
        List[Dict[str, str]]: Liste de dictionnaires représentant les lignes

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_file(
    filepath: str,
    data: List[Dict[str, str]],
    fieldnames: List[str]
) -> None:
    """
    Écrit des données dans un fichier CSV.

    Args:
        filepath: Chemin du fichier CSV
        data: Liste de dictionnaires à écrire
        fieldnames: Liste des noms de colonnes
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def append_to_csv_file(
    filepath: str,
    row: Dict[str, str],
    fieldnames: List[str]
) -> None:
    """
    Ajoute une ligne à un fichier CSV existant.

    Args:
        filepath: Chemin du fichier CSV
        row: Dictionnaire représentant la ligne à ajouter
        fieldnames: Liste des noms de colonnes

    Note:
        Crée le fichier avec les en-têtes s'il n'existe pas.
    """
    file_exists = os.path.exists(filepath)

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# Fonctions spécifiques pour les utilisateurs
def get_all_users() -> List[Dict[str, str]]:
    """
    Récupère tous les utilisateurs.

    Returns:
        List[Dict[str, str]]: Liste des utilisateurs
    """
    ensure_data_dir()
    return read_csv_file(USERS_FILE)


def get_user(username: str) -> Optional[Dict[str, str]]:
    """
    Récupère un utilisateur par son nom d'utilisateur.

    Args:
        username: Nom d'utilisateur

    Returns:
        Optional[Dict[str, str]]: Données de l'utilisateur ou None
    """
    users = get_all_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


def save_user(user: Dict[str, str]) -> None:
    """
    Sauvegarde un nouvel utilisateur.

    Args:
        user: Dictionnaire contenant les données de l'utilisateur
    """
    ensure_data_dir()
    fieldnames = ['username', 'password_hash', 'is_admin', 'email']
    append_to_csv_file(USERS_FILE, user, fieldnames)


def update_user(username: str, updated_data: Dict[str, str]) -> bool:
    """
    Met à jour les données d'un utilisateur.

    Args:
        username: Nom d'utilisateur à mettre à jour
        updated_data: Dictionnaire avec les nouvelles valeurs

    Returns:
        bool: True si la mise à jour a réussi, False sinon
    """
    users = get_all_users()
    user_found = False

    for user in users:
        if user['username'] == username:
            user.update(updated_data)
            user_found = True
            break

    if user_found:
        fieldnames = ['username', 'password_hash', 'is_admin', 'email']
        write_csv_file(USERS_FILE, users, fieldnames)

    return user_found


def delete_user(username: str) -> bool:
    """
    Supprime un utilisateur et son annuaire.

    Args:
        username: Nom d'utilisateur à supprimer

    Returns:
        bool: True si la suppression a réussi, False sinon
    """
    users = get_all_users()
    initial_count = len(users)
    users = [u for u in users if u['username'] != username]

    if len(users) < initial_count:
        fieldnames = ['username', 'password_hash', 'is_admin', 'email']
        write_csv_file(USERS_FILE, users, fieldnames)

        # Supprimer l'annuaire de l'utilisateur
        annuaire_path = get_annuaire_path(username)
        if os.path.exists(annuaire_path):
            os.remove(annuaire_path)

        # Supprimer les permissions associées
        delete_user_permissions(username)

        return True

    return False


# Fonctions spécifiques pour les contacts
CONTACT_FIELDNAMES = ['nom', 'prenom', 'telephone', 'adresse', 'email']


def get_contacts(username: str) -> List[Dict[str, str]]:
    """
    Récupère tous les contacts d'un utilisateur.

    Args:
        username: Nom d'utilisateur

    Returns:
        List[Dict[str, str]]: Liste des contacts
    """
    ensure_data_dir()
    annuaire_path = get_annuaire_path(username)
    return read_csv_file(annuaire_path)


def save_contact(username: str, contact: Dict[str, str]) -> None:
    """
    Sauvegarde un nouveau contact dans l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur
        contact: Dictionnaire contenant les données du contact
    """
    ensure_data_dir()
    annuaire_path = get_annuaire_path(username)
    append_to_csv_file(annuaire_path, contact, CONTACT_FIELDNAMES)


def update_contact(
    username: str,
    email: str,
    updated_data: Dict[str, str]
) -> bool:
    """
    Met à jour un contact dans l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur
        email: Email du contact à mettre à jour (identifiant unique)
        updated_data: Dictionnaire avec les nouvelles valeurs

    Returns:
        bool: True si la mise à jour a réussi, False sinon
    """
    contacts = get_contacts(username)
    contact_found = False

    for contact in contacts:
        if contact['email'] == email:
            contact.update(updated_data)
            contact_found = True
            break

    if contact_found:
        annuaire_path = get_annuaire_path(username)
        write_csv_file(annuaire_path, contacts, CONTACT_FIELDNAMES)

    return contact_found


def delete_contact(username: str, email: str) -> bool:
    """
    Supprime un contact de l'annuaire d'un utilisateur.

    Args:
        username: Nom d'utilisateur
        email: Email du contact à supprimer

    Returns:
        bool: True si la suppression a réussi, False sinon
    """
    contacts = get_contacts(username)
    initial_count = len(contacts)
    contacts = [c for c in contacts if c['email'] != email]

    if len(contacts) < initial_count:
        annuaire_path = get_annuaire_path(username)
        write_csv_file(annuaire_path, contacts, CONTACT_FIELDNAMES)
        return True

    return False


def create_annuaire(username: str) -> None:
    """
    Crée un fichier annuaire vide pour un utilisateur.

    Args:
        username: Nom d'utilisateur
    """
    ensure_data_dir()
    annuaire_path = get_annuaire_path(username)
    if not os.path.exists(annuaire_path):
        with open(annuaire_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CONTACT_FIELDNAMES)


# Fonctions spécifiques pour les permissions
PERMISSION_FIELDNAMES = ['owner', 'granted_to', 'permission_type']


def get_permissions(owner: str) -> List[Dict[str, str]]:
    """
    Récupère les permissions accordées par un propriétaire.

    Args:
        owner: Nom d'utilisateur du propriétaire de l'annuaire

    Returns:
        List[Dict[str, str]]: Liste des permissions
    """
    ensure_data_dir()
    all_permissions = read_csv_file(PERMISSIONS_FILE)
    return [p for p in all_permissions if p['owner'] == owner]


def get_user_permissions(username: str) -> List[Dict[str, str]]:
    """
    Récupère les permissions accordées à un utilisateur.

    Args:
        username: Nom d'utilisateur

    Returns:
        List[Dict[str, str]]: Liste des permissions
    """
    ensure_data_dir()
    all_permissions = read_csv_file(PERMISSIONS_FILE)
    return [p for p in all_permissions if p['granted_to'] == username]


def add_permission(
    owner: str,
    granted_to: str,
    permission_type: str
) -> bool:
    """
    Ajoute une permission d'accès à un annuaire.

    Args:
        owner: Propriétaire de l'annuaire
        granted_to: Utilisateur à qui la permission est accordée
        permission_type: Type de permission ('read', 'write', 'all')

    Returns:
        bool: True si la permission a été ajoutée, False si elle existe déjà
    """
    ensure_data_dir()
    permissions = get_permissions(owner)

    # Vérifier si la permission existe déjà
    for p in permissions:
        if p['granted_to'] == granted_to:
            return False

    permission = {
        'owner': owner,
        'granted_to': granted_to,
        'permission_type': permission_type
    }
    append_to_csv_file(PERMISSIONS_FILE, permission, PERMISSION_FIELDNAMES)
    return True


def remove_permission(owner: str, granted_to: str) -> bool:
    """
    Supprime une permission d'accès à un annuaire.

    Args:
        owner: Propriétaire de l'annuaire
        granted_to: Utilisateur dont la permission est révoquée

    Returns:
        bool: True si la permission a été supprimée, False sinon
    """
    all_permissions = read_csv_file(PERMISSIONS_FILE)
    initial_count = len(all_permissions)
    all_permissions = [
        p for p in all_permissions
        if not (p['owner'] == owner and p['granted_to'] == granted_to)
    ]

    if len(all_permissions) < initial_count:
        write_csv_file(PERMISSIONS_FILE, all_permissions, PERMISSION_FIELDNAMES)
        return True

    return False


def has_permission(owner: str, username: str, required_type: str = 'read') -> bool:
    """
    Vérifie si un utilisateur a la permission d'accéder à un annuaire.

    Args:
        owner: Propriétaire de l'annuaire
        username: Utilisateur qui veut accéder
        required_type: Type de permission requis ('read', 'write', 'all')

    Returns:
        bool: True si l'utilisateur a la permission, False sinon
    """
    # Le propriétaire a toujours accès à son propre annuaire
    if owner == username:
        return True

    permissions = get_permissions(owner)
    for p in permissions:
        if p['granted_to'] == username:
            if p['permission_type'] == 'all':
                return True
            if p['permission_type'] == required_type:
                return True
            if required_type == 'read' and p['permission_type'] in ['read', 'write']:
                return True

    return False


def delete_user_permissions(username: str) -> None:
    """
    Supprime toutes les permissions associées à un utilisateur.

    Args:
        username: Nom d'utilisateur
    """
    all_permissions = read_csv_file(PERMISSIONS_FILE)
    # Supprimer les permissions où l'utilisateur est propriétaire ou bénéficiaire
    all_permissions = [
        p for p in all_permissions
        if p['owner'] != username and p['granted_to'] != username
    ]
    write_csv_file(PERMISSIONS_FILE, all_permissions, PERMISSION_FIELDNAMES)
