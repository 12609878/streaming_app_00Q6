"""
Module film.py
Classe représentant un film disponible sur la plateforme de streaming.
Un film peut appartenir à plusieurs catégories et avoir plusieurs acteurs.
"""


class Film:
    """Représente un film avec ses catégories et ses acteurs."""

    def __init__(self, nom, duree, description):
        """
        Initialise un film.

        Args:
            nom (str): Titre du film.
            duree (int): Durée en minutes.
            description (str): Résumé du film.
        """
        self.nom = nom
        self.duree = duree
        self.description = description
        self.categories = []   # Liste d'objets Categorie
        self.acteurs = []      # Liste d'objets Acteur

    def ajouter_categorie(self, categorie):
        """Associe une catégorie au film."""
        self.categories.append(categorie)

    def ajouter_acteur(self, acteur):
        """Associe un acteur au film."""
        self.acteurs.append(acteur)

    def get_categories_str(self):
        """Retourne les catégories sous forme de chaîne (ex : 'Action, Comédie')."""
        if self.categories:
            return ", ".join(str(c) for c in self.categories)
        return "Aucune catégorie"

    def get_acteurs_str(self):
        """Retourne les acteurs sous forme de chaîne pour l'infobulle."""
        if self.acteurs:
            return "\n".join(str(a) for a in self.acteurs)
        return "Aucun acteur"

    def __str__(self):
        return f"{self.nom} ({self.duree} min) - {self.get_categories_str()}"
