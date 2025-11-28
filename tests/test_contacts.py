"""
Tests unitaires pour le module de gestion des contacts (contacts.py)

Ce module contient les tests unitaires pour les fonctions de gestion
des contacts dans les annuaires.
"""

import csv
import os
import shutil
import tempfile
import unittest

from src.contacts import (
    ajout_contact,
    recherche_contact,
    liste_contacts,
    suppression_contact,
    modification_contact,
    export_csv,
    import_csv
)
from src.accounts import (
    initialiser_admin,
    creation_compte
)
from src.storage import (
    ensure_data_dir,
    get_contacts
)


class TestContacts(unittest.TestCase):
    """Tests pour les fonctions de gestion des contacts."""

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

        # Créer un administrateur et un utilisateur pour les tests
        initialiser_admin('admin', 'admin123', 'admin@example.com')
        creation_compte('admin', 'test_user', 'password', 'user@example.com', False)

    def tearDown(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.test_dir)

    def test_ajout_contact_success(self):
        """Test d'ajout de contact réussi."""
        success, msg = ajout_contact(
            username='test_user',
            nom='Dupont',
            prenom='Jean',
            email='jean.dupont@example.com',
            telephone='0612345678',
            adresse='123 Rue de la Paix, 75001 Paris'
        )

        self.assertTrue(success)
        self.assertIn("succès", msg)

        # Vérifier que le contact existe dans l'annuaire
        contacts = get_contacts('test_user')
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]['nom'], 'Dupont')
        self.assertEqual(contacts[0]['prenom'], 'Jean')

        print(f"✓ Contact ajouté: {contacts[0]['nom']} {contacts[0]['prenom']}")
        print(f"  Email: {contacts[0]['email']}")
        print(f"  Téléphone: {contacts[0]['telephone']}")
        print(f"  Adresse: {contacts[0]['adresse']}")

    def test_ajout_contact_user_not_found(self):
        """Test d'ajout de contact pour utilisateur inexistant."""
        success, msg = ajout_contact(
            username='nonexistent',
            nom='Test',
            prenom='User',
            email='test@example.com'
        )

        self.assertFalse(success)
        self.assertIn("non trouvé", msg)

        print("✓ Ajout refusé pour utilisateur inexistant")

    def test_ajout_contact_duplicate_email(self):
        """Test d'ajout de contact avec email existant."""
        ajout_contact(
            'test_user', 'Dupont', 'Jean', 'same@example.com'
        )

        success, msg = ajout_contact(
            username='test_user',
            nom='Martin',
            prenom='Pierre',
            email='same@example.com'
        )

        self.assertFalse(success)
        self.assertIn("existe déjà", msg)

        print("✓ Ajout refusé pour email existant")

    def test_ajout_contact_invalid_email(self):
        """Test d'ajout de contact avec email invalide."""
        success, msg = ajout_contact(
            username='test_user',
            nom='Test',
            prenom='User',
            email='invalid_email'
        )

        self.assertFalse(success)
        self.assertIn("email", msg.lower())

        print("✓ Ajout refusé pour email invalide")

    def test_ajout_contact_missing_required(self):
        """Test d'ajout de contact avec champs obligatoires manquants."""
        success, msg = ajout_contact(
            username='test_user',
            nom='',
            prenom='User',
            email='test@example.com'
        )

        self.assertFalse(success)
        self.assertIn("obligatoire", msg)

        print("✓ Ajout refusé pour nom manquant")

    def test_recherche_contact_success(self):
        """Test de recherche de contact réussie."""
        # Ajouter plusieurs contacts
        ajout_contact('test_user', 'Dupont', 'Jean', 'jean@example.com')
        ajout_contact('test_user', 'Dupont', 'Marie', 'marie@example.com')
        ajout_contact('test_user', 'Martin', 'Pierre', 'pierre@example.com')

        # Rechercher par nom
        success, results = recherche_contact(
            'test_user', 'test_user', 'nom', 'Dupont'
        )

        self.assertTrue(success)
        self.assertEqual(len(results), 2)

        print(f"✓ Recherche 'Dupont': {len(results)} résultats")
        for contact in results:
            print(f"  - {contact['nom']} {contact['prenom']}")

    def test_recherche_contact_partial_match(self):
        """Test de recherche de contact avec correspondance partielle."""
        ajout_contact('test_user', 'Dupontel', 'Jean', 'jean@example.com')
        ajout_contact('test_user', 'Dupont', 'Marie', 'marie@example.com')

        success, results = recherche_contact(
            'test_user', 'test_user', 'nom', 'Dupon'
        )

        self.assertTrue(success)
        self.assertEqual(len(results), 2)

        print(f"✓ Recherche partielle 'Dupon': {len(results)} résultats")

    def test_recherche_contact_case_insensitive(self):
        """Test de recherche de contact insensible à la casse."""
        ajout_contact('test_user', 'Dupont', 'Jean', 'jean@example.com')

        success, results = recherche_contact(
            'test_user', 'test_user', 'nom', 'dupont'
        )

        self.assertTrue(success)
        self.assertEqual(len(results), 1)

        print("✓ Recherche insensible à la casse fonctionne")

    def test_liste_contacts_success(self):
        """Test de listage des contacts réussi."""
        ajout_contact('test_user', 'Dupont', 'Jean', 'jean@example.com')
        ajout_contact('test_user', 'Martin', 'Marie', 'marie@example.com')
        ajout_contact('test_user', 'Bernard', 'Pierre', 'pierre@example.com')

        success, contacts = liste_contacts('test_user')

        self.assertTrue(success)
        self.assertEqual(len(contacts), 3)

        print(f"✓ Liste des contacts: {len(contacts)} contacts")
        for contact in contacts:
            print(f"  - {contact['nom']} {contact['prenom']} ({contact['email']})")

    def test_liste_contacts_empty(self):
        """Test de listage d'un annuaire vide."""
        success, contacts = liste_contacts('test_user')

        self.assertTrue(success)
        self.assertEqual(len(contacts), 0)

        print("✓ Liste vide retournée pour annuaire vide")

    def test_suppression_contact_success(self):
        """Test de suppression de contact réussie."""
        ajout_contact('test_user', 'Dupont', 'Jean', 'jean@example.com')

        success, msg = suppression_contact('test_user', 'jean@example.com')

        self.assertTrue(success)
        self.assertIn("succès", msg)

        contacts = get_contacts('test_user')
        self.assertEqual(len(contacts), 0)

        print("✓ Contact supprimé avec succès")

    def test_suppression_contact_not_found(self):
        """Test de suppression de contact inexistant."""
        success, msg = suppression_contact('test_user', 'nonexistent@example.com')

        self.assertFalse(success)
        self.assertIn("non trouvé", msg)

        print("✓ Suppression refusée pour contact inexistant")

    def test_modification_contact_success(self):
        """Test de modification de contact réussie."""
        ajout_contact(
            'test_user', 'Dupont', 'Jean', 'jean@example.com',
            telephone='0612345678'
        )

        success, msg = modification_contact(
            username='test_user',
            email='jean@example.com',
            nouveau_telephone='0698765432',
            nouvelle_adresse='456 Avenue Nouvelle'
        )

        self.assertTrue(success)

        contacts = get_contacts('test_user')
        self.assertEqual(contacts[0]['telephone'], '0698765432')
        self.assertEqual(contacts[0]['adresse'], '456 Avenue Nouvelle')

        print("✓ Contact modifié avec succès")
        print(f"  Nouveau téléphone: {contacts[0]['telephone']}")
        print(f"  Nouvelle adresse: {contacts[0]['adresse']}")

    def test_modification_contact_change_email(self):
        """Test de modification de l'email d'un contact."""
        ajout_contact('test_user', 'Dupont', 'Jean', 'old@example.com')

        success, msg = modification_contact(
            username='test_user',
            email='old@example.com',
            nouvel_email='new@example.com'
        )

        self.assertTrue(success)

        contacts = get_contacts('test_user')
        self.assertEqual(contacts[0]['email'], 'new@example.com')

        print("✓ Email du contact modifié avec succès")

    def test_export_csv_success(self):
        """Test d'export CSV réussi."""
        ajout_contact('test_user', 'Dupont', 'Jean', 'jean@example.com', '0612345678')
        ajout_contact('test_user', 'Martin', 'Marie', 'marie@example.com', '0698765432')

        export_path = os.path.join(self.test_dir, 'export.csv')
        success, msg = export_csv('test_user', export_path)

        self.assertTrue(success)
        self.assertTrue(os.path.exists(export_path))

        # Vérifier le contenu du fichier
        with open(export_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)

        print(f"✓ Annuaire exporté: {export_path}")
        print(f"  {len(rows)} contacts exportés")

    def test_import_csv_success(self):
        """Test d'import CSV réussi."""
        # Créer un fichier CSV à importer
        import_path = os.path.join(self.test_dir, 'import.csv')
        with open(import_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['nom', 'prenom', 'email', 'telephone', 'adresse']
            )
            writer.writeheader()
            writer.writerow({
                'nom': 'Importé',
                'prenom': 'Contact1',
                'email': 'import1@example.com',
                'telephone': '0611111111',
                'adresse': 'Adresse 1'
            })
            writer.writerow({
                'nom': 'Importé',
                'prenom': 'Contact2',
                'email': 'import2@example.com',
                'telephone': '0622222222',
                'adresse': 'Adresse 2'
            })

        success, msg = import_csv('test_user', import_path)

        self.assertTrue(success)
        self.assertIn("2 contacts importés", msg)

        contacts = get_contacts('test_user')
        self.assertEqual(len(contacts), 2)

        print(f"✓ Import réussi: {msg}")

    def test_import_csv_with_duplicates(self):
        """Test d'import CSV avec doublons d'email."""
        # Ajouter un contact existant
        ajout_contact('test_user', 'Existant', 'Contact', 'existing@example.com')

        # Créer un fichier avec un email dupliqué
        import_path = os.path.join(self.test_dir, 'import_dup.csv')
        with open(import_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['nom', 'prenom', 'email', 'telephone', 'adresse']
            )
            writer.writeheader()
            writer.writerow({
                'nom': 'Nouveau',
                'prenom': 'Contact',
                'email': 'new@example.com',
                'telephone': '',
                'adresse': ''
            })
            writer.writerow({
                'nom': 'Doublon',
                'prenom': 'Contact',
                'email': 'existing@example.com',  # Déjà existant
                'telephone': '',
                'adresse': ''
            })

        success, msg = import_csv('test_user', import_path)

        self.assertTrue(success)
        self.assertIn("1 contacts importés", msg)
        self.assertIn("ignoré", msg)

        print(f"✓ Import avec doublons géré: {msg}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TESTS UNITAIRES - Module de Gestion des Contacts")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
