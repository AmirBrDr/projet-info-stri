"""
Tests unitaires pour le module de validation (validation.py)

Ce module contient les tests unitaires pour les fonctions de validation
des données utilisateur et contact.
"""

import unittest

from src.validation import (
    validate_email,
    validate_phone,
    validate_username,
    validate_password,
    validate_nom,
    validate_prenom,
    validate_contact
)


class TestValidation(unittest.TestCase):
    """Tests pour les fonctions de validation."""

    def test_validate_email_valid(self):
        """Test de validation d'emails valides."""
        valid_emails = [
            'test@example.com',
            'user.name@domain.org',
            'user+tag@company.fr',
            'firstname.lastname@university.edu',
        ]

        for email in valid_emails:
            valid, msg = validate_email(email)
            self.assertTrue(valid, f"Email '{email}' devrait être valide")
            print(f"✓ Email valide: {email}")

    def test_validate_email_invalid(self):
        """Test de validation d'emails invalides."""
        invalid_emails = [
            '',
            'invalid',
            'invalid@',
            '@domain.com',
            'user@domain',
            'user@.com',
        ]

        for email in invalid_emails:
            valid, msg = validate_email(email)
            self.assertFalse(valid, f"Email '{email}' devrait être invalide")
            print(f"✓ Email invalide détecté: '{email}' - {msg}")

    def test_validate_phone_valid(self):
        """Test de validation de numéros de téléphone valides."""
        valid_phones = [
            '0612345678',
            '06 12 34 56 78',
            '06-12-34-56-78',
            '+33612345678',
            '0033612345678',
            '',  # Optionnel, donc valide
        ]

        for phone in valid_phones:
            valid, msg = validate_phone(phone)
            self.assertTrue(valid, f"Téléphone '{phone}' devrait être valide")
            if phone:
                print(f"✓ Téléphone valide: {phone}")

    def test_validate_phone_invalid(self):
        """Test de validation de numéros de téléphone invalides."""
        invalid_phones = [
            'abc',
            '123',
            'phone number',
        ]

        for phone in invalid_phones:
            valid, msg = validate_phone(phone)
            self.assertFalse(valid, f"Téléphone '{phone}' devrait être invalide")
            print(f"✓ Téléphone invalide détecté: '{phone}' - {msg}")

    def test_validate_username_valid(self):
        """Test de validation de noms d'utilisateur valides."""
        valid_usernames = [
            'user123',
            'test_user',
            'Admin',
            'user_name_123',
        ]

        for username in valid_usernames:
            valid, msg = validate_username(username)
            self.assertTrue(valid, f"Username '{username}' devrait être valide")
            print(f"✓ Username valide: {username}")

    def test_validate_username_invalid(self):
        """Test de validation de noms d'utilisateur invalides."""
        invalid_usernames = [
            '',
            'ab',  # Trop court
            'user@name',  # Caractère non autorisé
            'user name',  # Espace non autorisé
            'a' * 51,  # Trop long
        ]

        for username in invalid_usernames:
            valid, msg = validate_username(username)
            self.assertFalse(valid, f"Username '{username}' devrait être invalide")
            display = username[:20] + '...' if len(username) > 20 else username
            print(f"✓ Username invalide détecté: '{display}' - {msg}")

    def test_validate_password_valid(self):
        """Test de validation de mots de passe valides."""
        valid_passwords = [
            'password',
            '123456',
            'Pass123!',
            'very_long_password_123',
        ]

        for password in valid_passwords:
            valid, msg = validate_password(password)
            self.assertTrue(valid, f"Password devrait être valide")
            print(f"✓ Password valide: {'*' * len(password)}")

    def test_validate_password_invalid(self):
        """Test de validation de mots de passe invalides."""
        invalid_passwords = [
            '',
            '12345',  # Trop court
        ]

        for password in invalid_passwords:
            valid, msg = validate_password(password)
            self.assertFalse(valid, f"Password devrait être invalide")
            print(f"✓ Password invalide détecté: '{'*' * len(password)}' - {msg}")

    def test_validate_contact_valid(self):
        """Test de validation d'un contact valide."""
        contact = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.dupont@example.com',
            'telephone': '0612345678',
            'adresse': '123 Rue de la Paix'
        }

        valid, msg = validate_contact(contact)
        self.assertTrue(valid)
        print(f"✓ Contact valide: {contact['nom']} {contact['prenom']}")

    def test_validate_contact_missing_required(self):
        """Test de validation d'un contact avec champs obligatoires manquants."""
        # Contact sans nom
        contact_no_nom = {
            'nom': '',
            'prenom': 'Jean',
            'email': 'jean@example.com'
        }
        valid, msg = validate_contact(contact_no_nom)
        self.assertFalse(valid)
        print(f"✓ Contact sans nom rejeté: {msg}")

        # Contact sans prénom
        contact_no_prenom = {
            'nom': 'Dupont',
            'prenom': '',
            'email': 'jean@example.com'
        }
        valid, msg = validate_contact(contact_no_prenom)
        self.assertFalse(valid)
        print(f"✓ Contact sans prénom rejeté: {msg}")

        # Contact sans email
        contact_no_email = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': ''
        }
        valid, msg = validate_contact(contact_no_email)
        self.assertFalse(valid)
        print(f"✓ Contact sans email rejeté: {msg}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TESTS UNITAIRES - Module de Validation")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
