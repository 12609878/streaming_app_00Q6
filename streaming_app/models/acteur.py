"""
Module acteur.py
Classe représentant un acteur, héritant de Personne.
Un acteur peut avoir joué dans plusieurs films.
"""

from models.personne import Personne


class Acteur(Personne):
    """Acteur héritant de Personne. Peut jouer dans plusieurs films."""

    def __init__(self, nom, prenom, sexe, nom_personnage, debut_emploi, fin_emploi, cachet):
        """
        Initialise un acteur.

        Args:
            nom (str): Nom de famille.
            prenom (str): Prénom.
            sexe (str): Sexe ('M', 'F' ou 'Autre').
            nom_personnage (str): Nom du personnage joué.
            debut_emploi (str): Date de début d'emploi (YYYY-MM-DD).
            fin_emploi (str): Date de fin d'emploi (YYYY-MM-DD ou vide si en cours).
            cachet (float): Cachet en dollars.
        """
        super().__init__(nom, prenom, sexe)
        self.nom_personnage = nom_personnage
        self.debut_emploi = debut_emploi
        self.fin_emploi = fin_emploi
        self.cachet = cachet

    def __str__(self):
        return f"{self.prenom} {self.nom} (rôle : {self.nom_personnage})"
