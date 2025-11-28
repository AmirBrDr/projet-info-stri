"""
Tests unitaires pour le module de gestion des comptes (accounts.py)

Ce module contient les tests unitaires pour les fonctions de gestion
des comptes utilisateurs.
"""

import os
import shutil
import tempfile
import unittest

from src.accounts import (
    creation_compte,
    suppression_compte,
    modification_compte,
    liste_comptes,
    authentifier,
    est_administrateur,
    initialiser_admin
)
from src.storage import (
    ensure_data_dir,
    get_user,
    get_annuaire_path
)


class TestAccounts(unittest.TestCase):
    """Tests pour les fonctions de gestion des comptes."""

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

        # Créer un administrateur pour les tests
        success, msg = initialiser_admin(
            'admin',
            'admin123',
            'admin@example.com'
        )
        self.assertTrue(success, f"Erreur lors de l'initialisation admin: {msg}")

    def tearDown(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.test_dir)

    def test_initialiser_admin(self):
        """Test de l'initialisation d'un administrateur."""
        # Déjà initialisé dans setUp, vérifier qu'on ne peut pas en créer un autre
        success, msg = initialiser_admin(
            'admin2',
            'admin456',
            'admin2@example.com'
        )
        self.assertFalse(success)
        self.assertIn("existe déjà", msg)

        print("✓ Impossible de créer un deuxième administrateur initial")

    def test_creation_compte_success(self):
        """Test de la création réussie d'un compte utilisateur."""
        success, msg = creation_compte(
            admin_username='admin',
            username='new_user',
            password='password123',
            email='newuser@example.com',
            is_admin=False
        )

        self.assertTrue(success)
        self.assertIn("succès", msg)

        # Vérifier que le compte existe
        user = get_user('new_user')
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], 'newuser@example.com')

        # Vérifier que l'annuaire a été créé
        import src.storage as storage
        annuaire_path = os.path.join(storage.DATA_DIR, 'annuaire_new_user.csv')
        self.assertTrue(os.path.exists(annuaire_path))

        print(f"✓ Compte créé avec succès: {user['username']}")
        print(f"✓ Annuaire créé: {annuaire_path}")

    def test_creation_compte_not_admin(self):
        """Test de création de compte par un non-administrateur."""
        # Créer un utilisateur normal
        creation_compte(
            'admin', 'normal_user', 'password', 'normal@example.com', False
        )

        # Tenter de créer un compte avec l'utilisateur normal
        success, msg = creation_compte(
            admin_username='normal_user',
            username='another_user',
            password='password',
            email='another@example.com'
        )

        self.assertFalse(success)
        self.assertIn("Permission refusée", msg)

        print("✓ Création de compte refusée pour non-administrateur")

    def test_creation_compte_duplicate_username(self):
        """Test de création de compte avec un nom d'utilisateur existant."""
        creation_compte(
            'admin', 'existing_user', 'password', 'existing@example.com', False
        )

        success, msg = creation_compte(
            admin_username='admin',
            username='existing_user',
            password='password',
            email='different@example.com'
        )

        self.assertFalse(success)
        self.assertIn("existe déjà", msg)

        print("✓ Création de compte refusée pour nom d'utilisateur existant")

    def test_creation_compte_duplicate_email(self):
        """Test de création de compte avec un email existant."""
        creation_compte(
            'admin', 'user1', 'password', 'same@example.com', False
        )

        success, msg = creation_compte(
            admin_username='admin',
            username='user2',
            password='password',
            email='same@example.com'
        )

        self.assertFalse(success)
        self.assertIn("email est déjà utilisée", msg)

        print("✓ Création de compte refusée pour email existant")

    def test_creation_compte_invalid_username(self):
        """Test de création de compte avec un nom d'utilisateur invalide."""
        success, msg = creation_compte(
            admin_username='admin',
            username='ab',  # Trop court
            password='password123',
            email='valid@example.com'
        )

        self.assertFalse(success)
        self.assertIn("3 caractères", msg)

        print("✓ Création de compte refusée pour username invalide")

    def test_creation_compte_invalid_password(self):
        """Test de création de compte avec un mot de passe invalide."""
        success, msg = creation_compte(
            admin_username='admin',
            username='validuser',
            password='123',  # Trop court
            email='valid@example.com'
        )

        self.assertFalse(success)
        self.assertIn("6 caractères", msg)

        print("✓ Création de compte refusée pour mot de passe invalide")

    def test_suppression_compte(self):
        """Test de la suppression d'un compte utilisateur."""
        # Créer un compte
        creation_compte(
            'admin', 'to_delete', 'password', 'todelete@example.com', False
        )

        # Supprimer le compte
        success, msg = suppression_compte('admin', 'to_delete')
        self.assertTrue(success)

        # Vérifier que le compte n'existe plus
        self.assertIsNone(get_user('to_delete'))

        print("✓ Compte supprimé avec succès")

    def test_suppression_compte_not_admin(self):
        """Test de suppression de compte par un non-administrateur."""
        creation_compte(
            'admin', 'user1', 'password', 'user1@example.com', False
        )
        creation_compte(
            'admin', 'user2', 'password', 'user2@example.com', False
        )

        success, msg = suppression_compte('user1', 'user2')
        self.assertFalse(success)
        self.assertIn("Permission refusée", msg)

        print("✓ Suppression refusée pour non-administrateur")

    def test_suppression_propre_compte_admin(self):
        """Test qu'un admin ne peut pas supprimer son propre compte."""
        success, msg = suppression_compte('admin', 'admin')
        self.assertFalse(success)
        self.assertIn("votre propre compte", msg)

        print("✓ Auto-suppression du compte admin refusée")

    def test_modification_compte(self):
        """Test de la modification d'un compte utilisateur."""
        creation_compte(
            'admin', 'to_modify', 'oldpass', 'oldmail@example.com', False
        )

        success, msg = modification_compte(
            admin_username='admin',
            username='to_modify',
            new_email='newmail@example.com'
        )
        self.assertTrue(success)

        user = get_user('to_modify')
        self.assertEqual(user['email'], 'newmail@example.com')

        print("✓ Email du compte modifié avec succès")

    def test_liste_comptes(self):
        """Test de la liste des comptes utilisateurs."""
        creation_compte(
            'admin', 'user1', 'password', 'user1@example.com', False
        )
        creation_compte(
            'admin', 'user2', 'password', 'user2@example.com', False
        )

        success, users = liste_comptes('admin')
        self.assertTrue(success)
        self.assertEqual(len(users), 3)  # admin + 2 users

        # Vérifier que les hashes de mot de passe ne sont pas exposés
        for user in users:
            self.assertNotIn('password_hash', user)

        print(f"✓ Liste des comptes: {len(users)} utilisateurs")
        for user in users:
            print(f"  - {user['username']} ({user['email']})")

    def test_authentifier_success(self):
        """Test d'authentification réussie."""
        creation_compte(
            'admin', 'auth_user', 'mypassword', 'auth@example.com', False
        )

        success, msg = authentifier('auth_user', 'mypassword')
        self.assertTrue(success)
        self.assertIn("réussie", msg)

        print(f"✓ Authentification réussie: {msg}")

    def test_authentifier_wrong_password(self):
        """Test d'authentification avec mauvais mot de passe."""
        creation_compte(
            'admin', 'auth_user2', 'correctpass', 'auth2@example.com', False
        )

        success, msg = authentifier('auth_user2', 'wrongpass')
        self.assertFalse(success)
        self.assertIn("incorrect", msg)

        print("✓ Authentification échouée pour mauvais mot de passe")

    def test_authentifier_unknown_user(self):
        """Test d'authentification avec utilisateur inconnu."""
        success, msg = authentifier('unknown_user', 'password')
        self.assertFalse(success)
        self.assertIn("non trouvé", msg)

        print("✓ Authentification échouée pour utilisateur inconnu")

    def test_est_administrateur(self):
        """Test de vérification du statut administrateur."""
        creation_compte(
            'admin', 'normal_user', 'password', 'normal@example.com', False
        )

        self.assertTrue(est_administrateur('admin'))
        self.assertFalse(est_administrateur('normal_user'))
        self.assertFalse(est_administrateur('nonexistent'))

        print("✓ Vérification du statut administrateur correcte")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TESTS UNITAIRES - Module de Gestion des Comptes")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
