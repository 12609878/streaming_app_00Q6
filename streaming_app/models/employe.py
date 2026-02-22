"""
Module employe.py
Classe représentant un employé de l'entreprise, héritant de Personne.
Les employés se connectent au système avec un code utilisateur et un mot de passe.
Deux niveaux d'accès : 'total' (lecture + écriture) et 'lecture' (consultation seulement).
"""

from models.personne import Personne


class Employe(Personne):
    """Employé héritant de Personne. Utilisé pour l'authentification."""

    # Liste statique des employés (données hardcodées, pas de base de données)
    employes_list = []

    def __init__(self, nom, prenom, sexe, date_embauche, code_utilisateur, password, type_acces):
        """
        Initialise un employé.

        Args:
            nom (str): Nom de famille.
            prenom (str): Prénom.
            sexe (str): Sexe ('M', 'F' ou 'Autre').
            date_embauche (str): Date d'embauche (YYYY-MM-DD).
            code_utilisateur (str): Identifiant de connexion.
            password (str): Mot de passe (en clair ici, hashé dans une version production).
            type_acces (str): 'total' ou 'lecture'.
        """
        super().__init__(nom, prenom, sexe)
        self.date_embauche = date_embauche
        self.code_utilisateur = code_utilisateur
        self.password = password
        self.type_acces = type_acces

    @classmethod
    def authentifier(cls, code_utilisateur, password):
        """
        Vérifie les identifiants d'un employé.

        Args:
            code_utilisateur (str): Code utilisateur saisi.
            password (str): Mot de passe saisi.

        Returns:
            Employe: L'objet employé si authentification réussie, None sinon.
        """
        for employe in cls.employes_list:
            if employe.code_utilisateur == code_utilisateur and employe.password == password:
                return employe
        return None

    def __str__(self):
        return f"{self.prenom} {self.nom} [{self.type_acces}]"
