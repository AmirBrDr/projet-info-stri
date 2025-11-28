#!/usr/bin/env python3
"""
Script pour exécuter tous les tests unitaires.

Ce script exécute les tests de tous les modules de l'application
et affiche un rapport détaillé des résultats.
"""

import os
import sys
import unittest

# Ajouter le répertoire racine au PYTHONPATH
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)


def run_all_tests():
    """Exécute tous les tests unitaires."""
    print("\n" + "=" * 70)
    print("            EXÉCUTION DES TESTS UNITAIRES")
    print("         Service d'annuaires partagés - STRI 2025/2026")
    print("=" * 70 + "\n")

    # Découvrir tous les tests dans le répertoire tests/
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')

    # Exécuter les tests avec un rapport détaillé
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Afficher le résumé
    print("\n" + "=" * 70)
    print("                    RÉSUMÉ DES TESTS")
    print("=" * 70)
    print(f"\nTests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")

    if result.failures:
        print("\n--- Échecs ---")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)

    if result.errors:
        print("\n--- Erreurs ---")
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)

    print("\n" + "=" * 70)

    # Retourner le code de sortie approprié
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
