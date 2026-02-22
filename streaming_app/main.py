"""
main.py
Point d'entrée de l'application de streaming.
Initialise les données hardcodées (employés, clients, films, acteurs, catégories)
puis lance la fenêtre de connexion.
"""

import sys
import os

# Ajouter le dossier courant au path pour que les imports fonctionnent
# depuis n'importe quel répertoire de travail.
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from views.login_view import LoginView
from models.employe import Employe
from models.client import Client
from models.film import Film
from models.categorie import Categorie
from models.acteur import Acteur
from models.carte_credit import CarteCredit


def initialiser_donnees():
    """
    Charge les données de départ hardcodées dans l'application.
    Simule ce que ferait une base de données en production.
    """

    # --- Employés (utilisés pour l'authentification) ---
    Employe.employes_list = [
        Employe("Tremblay", "Jean", "M", "2020-01-15", "admin", "admin123", "total"),
        Employe("Gagnon", "Marie", "F", "2021-06-01", "lecture", "lecture123", "lecture"),
    ]

    # --- Catégories de films ---
    action   = Categorie("Action", "Films d'action à grand spectacle")
    comedie  = Categorie("Comédie", "Films comiques et humoristiques")
    drame    = Categorie("Drame", "Films dramatiques et émotionnels")
    sci_fi   = Categorie("Science-fiction", "Films de science-fiction et futurisme")

    # --- Acteurs ---
    acteur1 = Acteur("Pitt", "Brad", "M", "Tyler Durden", "1995-01-01", "2010-12-31", 10000000)
    acteur2 = Acteur("Johansson", "Scarlett", "F", "Black Widow", "2010-05-01", "", 15000000)
    acteur3 = Acteur("DiCaprio", "Leonardo", "M", "Cobb", "2009-01-01", "2022-06-30", 20000000)

    # --- Films ---
    film1 = Film("Fight Club", 139, "Un homme insomniaque rencontre un vendeur de savon charismatique.")
    film1.ajouter_categorie(action)
    film1.ajouter_categorie(drame)
    film1.ajouter_acteur(acteur1)

    film2 = Film("Avengers: Endgame", 181, "Les héros de Marvel s'unissent pour sauver l'univers.")
    film2.ajouter_categorie(action)
    film2.ajouter_categorie(sci_fi)
    film2.ajouter_acteur(acteur2)

    film3 = Film("Inception", 148, "Un voleur qui s'introduit dans les rêves des gens.")
    film3.ajouter_categorie(sci_fi)
    film3.ajouter_categorie(action)
    film3.ajouter_acteur(acteur3)

    film4 = Film("La La Land", 128, "Un musicien et une actrice tombent amoureux à Los Angeles.")
    film4.ajouter_categorie(drame)
    film4.ajouter_categorie(comedie)

    Film.films_list = [film1, film2, film3, film4]

    # --- Clients de démonstration ---
    carte1 = CarteCredit("4111111111111111", "12/26", "123")
    client1 = Client.ajouter_client(
        "Bouchard", "Alice", "F", "2023-03-10", "alice@example.com", "motdepasse1"
    )
    client1.ajouter_carte_credit(carte1)

    Client.ajouter_client(
        "Leblanc", "Marc", "M", "2023-07-22", "marc@example.com", "motdepasse2"
    )


def main():
    """Lance l'application de streaming."""
    if not hasattr(Film, "films_list"):
        Film.films_list = []

    initialiser_donnees()

    root = tk.Tk()
    LoginView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
