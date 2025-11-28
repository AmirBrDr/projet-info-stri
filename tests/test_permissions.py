"""
Tests unitaires pour le module de gestion des permissions (permissions.py)

Ce module contient les tests unitaires pour les fonctions de gestion
des permissions d'accès aux annuaires.
"""

import os
import shutil
import tempfile
import unittest

from src.permissions import (
    accorder_permission,
    revoquer_permission,
    liste_permissions,
    liste_acces_accordes,
    verifier_permission
)
from src.accounts import (
    initialiser_admin,
    creation_compte
)
from src.contacts import (
    ajout_contact,
    liste_contacts,
    recherche_contact
)
from src.storage import ensure_data_dir


class TestPermissions(unittest.TestCase):
    """Tests pour les fonctions de gestion des permissions."""

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

        # Créer des utilisateurs pour les tests
        initialiser_admin('admin', 'admin123', 'admin@example.com')
        creation_compte('admin', 'user1', 'password', 'user1@example.com', False)
        creation_compte('admin', 'user2', 'password', 'user2@example.com', False)
        creation_compte('admin', 'user3', 'password', 'user3@example.com', False)

    def tearDown(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.test_dir)

    def test_accorder_permission_success(self):
        """Test d'accord de permission réussi."""
        success, msg = accorder_permission('user1', 'user2', 'read')

        self.assertTrue(success)
        self.assertIn("succès", msg)

        print(f"✓ Permission accordée: user1 -> user2 (read)")

    def test_accorder_permission_owner_not_found(self):
        """Test d'accord de permission avec propriétaire inexistant."""
        success, msg = accorder_permission('nonexistent', 'user2', 'read')

        self.assertFalse(success)
        self.assertIn("non trouvé", msg)

        print("✓ Permission refusée pour propriétaire inexistant")

    def test_accorder_permission_target_not_found(self):
        """Test d'accord de permission avec bénéficiaire inexistant."""
        success, msg = accorder_permission('user1', 'nonexistent', 'read')

        self.assertFalse(success)
        self.assertIn("non trouvé", msg)

        print("✓ Permission refusée pour bénéficiaire inexistant")

    def test_accorder_permission_invalid_type(self):
        """Test d'accord de permission avec type invalide."""
        success, msg = accorder_permission('user1', 'user2', 'invalid')

        self.assertFalse(success)
        self.assertIn("invalide", msg)

        print("✓ Permission refusée pour type invalide")

    def test_accorder_permission_self(self):
        """Test d'accord de permission à soi-même."""
        success, msg = accorder_permission('user1', 'user1', 'read')

        self.assertFalse(success)
        self.assertIn("soi-même", msg)

        print("✓ Permission refusée pour soi-même")

    def test_accorder_permission_duplicate(self):
        """Test d'accord de permission déjà existante."""
        accorder_permission('user1', 'user2', 'read')
        success, msg = accorder_permission('user1', 'user2', 'write')

        self.assertFalse(success)
        self.assertIn("existe déjà", msg)

        print("✓ Permission en double détectée")

    def test_revoquer_permission_success(self):
        """Test de révocation de permission réussie."""
        accorder_permission('user1', 'user2', 'read')

        success, msg = revoquer_permission('user1', 'user2')

        self.assertTrue(success)
        self.assertIn("succès", msg)

        print("✓ Permission révoquée avec succès")

    def test_revoquer_permission_not_found(self):
        """Test de révocation de permission inexistante."""
        success, msg = revoquer_permission('user1', 'user2')

        self.assertFalse(success)
        self.assertIn("Aucune permission", msg)

        print("✓ Révocation refusée pour permission inexistante")

    def test_liste_permissions_success(self):
        """Test de listage des permissions accordées."""
        accorder_permission('user1', 'user2', 'read')
        accorder_permission('user1', 'user3', 'write')

        success, permissions = liste_permissions('user1')

        self.assertTrue(success)
        self.assertEqual(len(permissions), 2)

        print(f"✓ Permissions accordées par user1: {len(permissions)}")
        for perm in permissions:
            print(f"  - {perm['owner']} -> {perm['granted_to']} ({perm['permission_type']})")

    def test_liste_acces_accordes_success(self):
        """Test de listage des accès accordés à un utilisateur."""
        accorder_permission('user1', 'user3', 'read')
        accorder_permission('user2', 'user3', 'write')

        success, access_list = liste_acces_accordes('user3')

        self.assertTrue(success)
        self.assertEqual(len(access_list), 2)

        print(f"✓ Accès accordés à user3: {len(access_list)}")
        for access in access_list:
            print(f"  - Annuaire de {access['owner']} ({access['permission_type']})")

    def test_verifier_permission_owner_always_access(self):
        """Test que le propriétaire a toujours accès à son annuaire."""
        self.assertTrue(verifier_permission('user1', 'user1', 'read'))
        self.assertTrue(verifier_permission('user1', 'user1', 'write'))
        self.assertTrue(verifier_permission('user1', 'user1', 'all'))

        print("✓ Le propriétaire a toujours accès à son annuaire")

    def test_verifier_permission_granted(self):
        """Test de vérification d'une permission accordée."""
        accorder_permission('user1', 'user2', 'read')

        self.assertTrue(verifier_permission('user1', 'user2', 'read'))

        print("✓ Permission accordée vérifiée correctement")

    def test_verifier_permission_not_granted(self):
        """Test de vérification d'une permission non accordée."""
        self.assertFalse(verifier_permission('user1', 'user2', 'read'))

        print("✓ Absence de permission détectée correctement")

    def test_permission_all_grants_all_access(self):
        """Test que la permission 'all' donne tous les accès."""
        accorder_permission('user1', 'user2', 'all')

        self.assertTrue(verifier_permission('user1', 'user2', 'read'))
        self.assertTrue(verifier_permission('user1', 'user2', 'write'))
        self.assertTrue(verifier_permission('user1', 'user2', 'all'))

        print("✓ Permission 'all' donne tous les accès")

    def test_consulter_annuaire_avec_permission(self):
        """Test de consultation d'annuaire avec permission."""
        # user1 ajoute des contacts
        ajout_contact('user1', 'Dupont', 'Jean', 'jean@example.com')
        ajout_contact('user1', 'Martin', 'Marie', 'marie@example.com')

        # user2 n'a pas accès initialement
        success, contacts = liste_contacts('user2', 'user1')
        self.assertFalse(success)
        self.assertEqual(len(contacts), 0)

        print("✓ Accès refusé sans permission")

        # Accorder la permission
        accorder_permission('user1', 'user2', 'read')

        # user2 peut maintenant voir l'annuaire de user1
        success, contacts = liste_contacts('user2', 'user1')
        self.assertTrue(success)
        self.assertEqual(len(contacts), 2)

        print(f"✓ Accès autorisé avec permission: {len(contacts)} contacts visibles")

    def test_rechercher_dans_annuaire_avec_permission(self):
        """Test de recherche dans un annuaire avec permission."""
        # user1 ajoute des contacts
        ajout_contact('user1', 'Dupont', 'Jean', 'jean@example.com')

        # Accorder la permission
        accorder_permission('user1', 'user2', 'read')

        # user2 peut rechercher dans l'annuaire de user1
        success, results = recherche_contact('user2', 'user1', 'nom', 'Dupont')
        self.assertTrue(success)
        self.assertEqual(len(results), 1)

        print(f"✓ Recherche avec permission: {len(results)} résultat")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TESTS UNITAIRES - Module de Gestion des Permissions")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
