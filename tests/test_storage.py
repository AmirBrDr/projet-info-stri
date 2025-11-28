"""
Tests unitaires pour le module de stockage (storage.py)

Ce module contient les tests unitaires pour les fonctions de stockage
et de manipulation des fichiers CSV.
"""

import os
import shutil
import tempfile
import unittest

from src.storage import (
    ensure_data_dir,
    hash_password,
    read_csv_file,
    write_csv_file,
    append_to_csv_file,
    get_all_users,
    get_user,
    save_user,
    update_user,
    delete_user,
    get_contacts,
    save_contact,
    update_contact,
    delete_contact,
    create_annuaire,
    get_permissions,
    add_permission,
    remove_permission,
    has_permission,
    DATA_DIR,
    USERS_FILE,
    get_annuaire_path
)


class TestStorage(unittest.TestCase):
    """Tests pour les fonctions de stockage."""

    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour les tests."""
        # Sauvegarder le répertoire de données original
        cls.original_data_dir = DATA_DIR

    def setUp(self):
        """Préparation avant chaque test."""
        # Créer un répertoire temporaire pour les tests
        self.test_dir = tempfile.mkdtemp()

        # Créer le répertoire data dans le répertoire temporaire
        self.data_dir = os.path.join(self.test_dir, 'data')
        os.makedirs(self.data_dir)

        # Modifier les chemins globaux pour les tests
        import src.storage as storage
        storage.DATA_DIR = self.data_dir
        storage.USERS_FILE = os.path.join(self.data_dir, 'users.csv')
        storage.PERMISSIONS_FILE = os.path.join(self.data_dir, 'permissions.csv')

        # Initialiser les fichiers de données
        ensure_data_dir()

    def tearDown(self):
        """Nettoyage après chaque test."""
        # Supprimer le répertoire temporaire
        shutil.rmtree(self.test_dir)

    def test_hash_password(self):
        """Test du hachage de mot de passe."""
        password = "test_password"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Vérifier que le hash est consistant
        self.assertEqual(hash1, hash2)

        # Vérifier que le hash n'est pas le mot de passe en clair
        self.assertNotEqual(hash1, password)

        # Vérifier que le hash a la bonne longueur (SHA-256 = 64 caractères)
        self.assertEqual(len(hash1), 64)

        print(f"✓ Hash du mot de passe '{password}': {hash1[:16]}...")

    def test_save_and_get_user(self):
        """Test de la sauvegarde et récupération d'un utilisateur."""
        user = {
            'username': 'test_user',
            'password_hash': hash_password('password123'),
            'is_admin': 'False',
            'email': 'test@example.com'
        }

        save_user(user)

        # Récupérer l'utilisateur
        retrieved_user = get_user('test_user')

        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user['username'], 'test_user')
        self.assertEqual(retrieved_user['email'], 'test@example.com')

        print(f"✓ Utilisateur sauvegardé et récupéré: {retrieved_user['username']}")

    def test_get_nonexistent_user(self):
        """Test de récupération d'un utilisateur inexistant."""
        user = get_user('nonexistent_user')
        self.assertIsNone(user)

        print("✓ Utilisateur inexistant retourne None comme attendu")

    def test_update_user(self):
        """Test de la mise à jour d'un utilisateur."""
        # Créer un utilisateur
        user = {
            'username': 'update_test',
            'password_hash': hash_password('old_password'),
            'is_admin': 'False',
            'email': 'old@example.com'
        }
        save_user(user)

        # Mettre à jour l'email
        success = update_user('update_test', {'email': 'new@example.com'})
        self.assertTrue(success)

        # Vérifier la mise à jour
        updated_user = get_user('update_test')
        self.assertEqual(updated_user['email'], 'new@example.com')

        print(f"✓ Utilisateur mis à jour: {updated_user['email']}")

    def test_delete_user(self):
        """Test de la suppression d'un utilisateur."""
        # Créer un utilisateur
        user = {
            'username': 'delete_test',
            'password_hash': hash_password('password'),
            'is_admin': 'False',
            'email': 'delete@example.com'
        }
        save_user(user)
        create_annuaire('delete_test')

        # Vérifier que l'utilisateur et l'annuaire existent
        self.assertIsNotNone(get_user('delete_test'))
        self.assertTrue(os.path.exists(get_annuaire_path('delete_test')))

        # Supprimer l'utilisateur
        success = delete_user('delete_test')
        self.assertTrue(success)

        # Vérifier la suppression
        self.assertIsNone(get_user('delete_test'))
        self.assertFalse(os.path.exists(get_annuaire_path('delete_test')))

        print("✓ Utilisateur et annuaire supprimés avec succès")

    def test_contact_operations(self):
        """Test des opérations sur les contacts."""
        username = 'contact_test'
        create_annuaire(username)

        # Ajouter un contact
        contact = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.dupont@example.com',
            'telephone': '0612345678',
            'adresse': '123 Rue Test'
        }
        save_contact(username, contact)

        # Récupérer les contacts
        contacts = get_contacts(username)
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['nom'], 'Dupont')

        print(f"✓ Contact ajouté: {contacts[0]['nom']} {contacts[0]['prenom']}")

        # Mettre à jour le contact
        success = update_contact(
            username,
            'jean.dupont@example.com',
            {'telephone': '0698765432'}
        )
        self.assertTrue(success)

        contacts = get_contacts(username)
        self.assertEqual(contacts[0]['telephone'], '0698765432')

        print(f"✓ Contact mis à jour: téléphone = {contacts[0]['telephone']}")

        # Supprimer le contact
        success = delete_contact(username, 'jean.dupont@example.com')
        self.assertTrue(success)

        contacts = get_contacts(username)
        self.assertEqual(len(contacts), 0)

        print("✓ Contact supprimé avec succès")

    def test_permission_operations(self):
        """Test des opérations sur les permissions."""
        owner = 'owner_test'
        granted_to = 'granted_test'

        # Ajouter une permission
        success = add_permission(owner, granted_to, 'read')
        self.assertTrue(success)

        # Vérifier la permission
        self.assertTrue(has_permission(owner, granted_to, 'read'))

        print(f"✓ Permission accordée: {owner} -> {granted_to} (read)")

        # Le propriétaire a toujours accès à son annuaire
        self.assertTrue(has_permission(owner, owner, 'read'))
        self.assertTrue(has_permission(owner, owner, 'write'))

        print("✓ Le propriétaire a toujours accès à son annuaire")

        # Révoquer la permission
        success = remove_permission(owner, granted_to)
        self.assertTrue(success)

        self.assertFalse(has_permission(owner, granted_to, 'read'))

        print("✓ Permission révoquée avec succès")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TESTS UNITAIRES - Module de Stockage")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
