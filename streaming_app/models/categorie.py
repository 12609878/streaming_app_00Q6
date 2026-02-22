"""
Module categorie.py
Classe représentant une catégorie de film (ex : Comédie, Action).
"""


class Categorie:
    """Représente une catégorie de film."""

    def __init__(self, nom, description=""):
        """
        Initialise une catégorie.

        Args:
            nom (str): Nom de la catégorie.
            description (str): Description optionnelle.
        """
        self.nom = nom
        self.description = description

    def __str__(self):
        return self.nom
