"""
Module carte_credit.py
Classe représentant une carte de crédit associée à un client.
"""


class CarteCredit:
    """Représente une carte de crédit (numéro, expiration, code secret)."""

    def __init__(self, numero, date_expiration, code_secret):
        """
        Initialise une carte de crédit.

        Args:
            numero (str): Numéro de carte (16 chiffres).
            date_expiration (str): Date d'expiration au format MM/AA.
            code_secret (str): Code CVV (3 chiffres).
        """
        self.numero = numero
        self.date_expiration = date_expiration
        self.code_secret = code_secret

    def __str__(self):
        # Masquer le numéro pour la sécurité
        return f"**** **** **** {self.numero[-4:]}"
