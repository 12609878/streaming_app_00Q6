"""
Module client.py
Classe représentant un client abonné au service de streaming.
Hérite de Personne et peut posséder plusieurs cartes de crédit.
"""

from models.personne import Personne


class Client(Personne):
    """Client héritant de Personne. Gère la liste statique de tous les clients."""

    # Liste statique partagée entre toutes les instances (remplace la base de données)
    clients_list = []

    def __init__(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        """
        Initialise un client.

        Args:
            nom (str): Nom de famille.
            prenom (str): Prénom.
            sexe (str): Sexe ('M', 'F' ou 'Autre').
            date_inscription (str): Date d'inscription (YYYY-MM-DD).
            courriel (str): Adresse courriel unique.
            mot_de_passe (str): Mot de passe (minimum 8 caractères).
        """
        super().__init__(nom, prenom, sexe)
        self.date_inscription = date_inscription
        self.courriel = courriel
        self.mot_de_passe = mot_de_passe
        self.cartes_credit = []   # Un client peut avoir plusieurs cartes de crédit

    def ajouter_carte_credit(self, carte):
        """Ajoute une carte de crédit à ce client."""
        self.cartes_credit.append(carte)

    @classmethod
    def ajouter_client(cls, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        """
        Crée et ajoute un nouveau client à la liste.

        Raises:
            ValueError: Si le courriel existe déjà ou le mot de passe est trop court.
        """
        # Validation : courriel unique (insensible à la casse)
        for client in cls.clients_list:
            if client.courriel.lower() == courriel.lower():
                raise ValueError("Ce courriel est déjà utilisé par un autre client.")

        # Validation : longueur mot de passe
        if len(mot_de_passe) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

        nouveau_client = Client(nom, prenom, sexe, date_inscription, courriel, mot_de_passe)
        cls.clients_list.append(nouveau_client)
        return nouveau_client

    @classmethod
    def supprimer_client(cls, courriel):
        """Supprime le client dont le courriel correspond."""
        cls.clients_list = [c for c in cls.clients_list if c.courriel != courriel]

    @classmethod
    def modifier_client(cls, ancien_courriel, nom, prenom, sexe, nouveau_courriel, mot_de_passe):
        """
        Modifie les informations d'un client existant.

        Raises:
            ValueError: Si le nouveau courriel est pris, le mot de passe trop court,
                        ou le client est introuvable.
        """
        for client in cls.clients_list:
            if client.courriel == ancien_courriel:
                # Vérifier que le nouveau courriel n'appartient pas à un autre client
                for c in cls.clients_list:
                    if c.courriel.lower() == nouveau_courriel.lower() and c is not client:
                        raise ValueError("Ce courriel est déjà utilisé par un autre client.")

                if len(mot_de_passe) < 8:
                    raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

                client.nom = nom
                client.prenom = prenom
                client.sexe = sexe
                client.courriel = nouveau_courriel
                client.mot_de_passe = mot_de_passe
                return

        raise ValueError("Client introuvable.")

    def __str__(self):
        return f"{self.prenom} {self.nom} <{self.courriel}>"
