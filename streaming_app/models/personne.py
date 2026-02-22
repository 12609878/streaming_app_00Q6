"""
Module personne.py
Classe de base représentant une personne.
Héritée par Client, Acteur et Employe.
"""


class Personne:
    """Classe de base contenant les informations communes à toute personne."""

    def __init__(self, nom, prenom, sexe):
        """
        Initialise une personne.

        Args:
            nom (str): Nom de famille.
            prenom (str): Prénom.
            sexe (str): Sexe ('M', 'F' ou 'Autre').
        """
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe

    def __str__(self):
        return f"{self.prenom} {self.nom}"
