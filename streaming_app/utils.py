"""
Module utils.py
Fonctions utilitaires partagées dans toute l'application.
"""

import hashlib


def hasher_mot_de_passe(mot_de_passe):
    """
    Convertit un mot de passe en clair en une empreinte SHA-256.
    Le mot de passe original ne peut pas être retrouvé à partir du hash.

    Args:
        mot_de_passe (str): Le mot de passe en clair saisi par l'utilisateur.

    Returns:
        str: Le hash SHA-256 du mot de passe (64 caractères hexadécimaux).

    Exemple:
        hasher_mot_de_passe("admin123")
        → "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
    """
    return hashlib.sha256(mot_de_passe.encode("utf-8")).hexdigest()
