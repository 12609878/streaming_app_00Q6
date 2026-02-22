"""
Module main_view.py
Fenêtre principale de l'application de streaming.
Affiche la liste des clients et des films.
Gère les accès selon le niveau de l'employé connecté :
- 'total'   : peut créer, modifier et supprimer des clients
- 'lecture' : consultation seulement, boutons désactivés
"""

import tkinter as tk
from tkinter import messagebox, ttk
from models.client import Client
from models.film import Film


class MainView:
    """Fenêtre principale après connexion."""

    def __init__(self, root, employe):
        """
        Initialise la fenêtre principale.

        Args:
            root (tk.Tk): La fenêtre racine Tkinter.
            employe (Employe): L'employé connecté (détermine le niveau d'accès).
        """
        self.root = root
        self.employe = employe
        self.root.title(f"Streaming App - Connecté : {employe.prenom} {employe.nom} [{employe.type_acces}]")
        self.root.geometry("800x550")

        # --- Menu ---
        menubar = tk.Menu(self.root)
        menu_fichier = tk.Menu(menubar, tearoff=0)
        menu_fichier.add_command(label="Se déconnecter", command=self.deconnecter)
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=menu_fichier)
        self.root.config(menu=menubar)

        # --- Section Clients ---
        frame_clients = tk.LabelFrame(self.root, text="Clients", padx=5, pady=5)
        frame_clients.pack(fill="both", expand=True, padx=10, pady=5)

        colonnes_clients = ("Nom", "Prénom", "Courriel")
        self.tree_clients = ttk.Treeview(frame_clients, columns=colonnes_clients, show="headings", height=7)
        for col in colonnes_clients:
            self.tree_clients.heading(col, text=col)
            self.tree_clients.column(col, width=200)
        self.tree_clients.pack(fill="both", expand=True)

        # Boutons clients (désactivés en mode lecture)
        frame_btn_clients = tk.Frame(frame_clients)
        frame_btn_clients.pack(pady=5)

        state = "normal" if employe.type_acces == "total" else "disabled"

        self.btn_creer = tk.Button(frame_btn_clients, text="Créer client",
                                   command=self.creer_client, state=state)
        self.btn_creer.pack(side="left", padx=5)

        self.btn_modifier = tk.Button(frame_btn_clients, text="Modifier client",
                                      command=self.modifier_client, state=state)
        self.btn_modifier.pack(side="left", padx=5)

        self.btn_supprimer = tk.Button(frame_btn_clients, text="Supprimer client",
                                       command=self.supprimer_client, state=state)
        self.btn_supprimer.pack(side="left", padx=5)

        if employe.type_acces == "lecture":
            tk.Label(frame_clients, text="Mode lecture seule — modifications non autorisées",
                     fg="red").pack()

        # --- Section Films ---
        frame_films = tk.LabelFrame(self.root, text="Films disponibles", padx=5, pady=5)
        frame_films.pack(fill="both", expand=True, padx=10, pady=5)

        colonnes_films = ("Titre", "Durée (min)", "Catégories")
        self.tree_films = ttk.Treeview(frame_films, columns=colonnes_films, show="headings", height=6)
        self.tree_films.heading("Titre", text="Titre")
        self.tree_films.heading("Durée (min)", text="Durée (min)")
        self.tree_films.heading("Catégories", text="Catégories")
        self.tree_films.column("Titre", width=250)
        self.tree_films.column("Durée (min)", width=100, anchor="center")
        self.tree_films.column("Catégories", width=300)
        self.tree_films.pack(fill="both", expand=True)

        # Infobulle acteurs au survol d'un film
        self.tree_films.bind("<Motion>", self._afficher_infobulle_acteurs)
        self._tooltip = None

        self.refresh_list()

    # ------------------------------------------------------------------ #
    # Méthodes de rafraîchissement                                        #
    # ------------------------------------------------------------------ #

    def refresh_list(self):
        """Met à jour les deux listes (clients et films) depuis les données en mémoire."""
        self._refresh_clients()
        self._refresh_films()

    def _refresh_clients(self):
        """Recharge la liste des clients dans le tableau."""
        for row in self.tree_clients.get_children():
            self.tree_clients.delete(row)
        for client in Client.clients_list:
            self.tree_clients.insert("", tk.END, values=(client.nom, client.prenom, client.courriel))

    def _refresh_films(self):
        """Recharge la liste des films dans le tableau."""
        for row in self.tree_films.get_children():
            self.tree_films.delete(row)
        for film in Film.films_list:
            self.tree_films.insert(
                "", tk.END,
                values=(film.nom, film.duree, film.get_categories_str()),
                tags=(film.get_acteurs_str(),)
            )

    # ------------------------------------------------------------------ #
    # Infobulle acteurs                                                   #
    # ------------------------------------------------------------------ #

    def _afficher_infobulle_acteurs(self, event):
        """Affiche une infobulle avec les acteurs du film survolé."""
        item = self.tree_films.identify_row(event.y)
        if item:
            tags = self.tree_films.item(item, "tags")
            texte = tags[0] if tags else ""
            if texte:
                if self._tooltip:
                    self._tooltip.destroy()
                x = self.root.winfo_pointerx() + 15
                y = self.root.winfo_pointery() + 10
                self._tooltip = tk.Toplevel(self.root)
                self._tooltip.wm_overrideredirect(True)
                self._tooltip.wm_geometry(f"+{x}+{y}")
                tk.Label(self._tooltip, text=f"Acteurs :\n{texte}",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         justify="left", padx=5, pady=3).pack()
                return
        if self._tooltip:
            self._tooltip.destroy()
            self._tooltip = None

    # ------------------------------------------------------------------ #
    # Actions clients                                                     #
    # ------------------------------------------------------------------ #

    def creer_client(self):
        """Ouvre le formulaire de création d'un nouveau client."""
        from views.client_form import ClientForm
        ClientForm(self.root, self.refresh_list)

    def modifier_client(self):
        """Ouvre le formulaire de modification pour le client sélectionné."""
        selection = self.tree_clients.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client à modifier.")
            return

        index = self.tree_clients.index(selection[0])
        client = Client.clients_list[index]

        from views.client_form import ClientForm
        ClientForm(self.root, self.refresh_list, client)

    def supprimer_client(self):
        """Demande confirmation puis supprime le client sélectionné."""
        selection = self.tree_clients.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client à supprimer.")
            return

        index = self.tree_clients.index(selection[0])
        client = Client.clients_list[index]

        # Dialogue de confirmation obligatoire
        confirmer = messagebox.askyesno(
            "Confirmation de suppression",
            f"Voulez-vous vraiment supprimer le client :\n{client.prenom} {client.nom} ({client.courriel}) ?"
        )
        if confirmer:
            try:
                Client.supprimer_client(client.courriel)
                messagebox.showinfo("Succès", "Client supprimé avec succès.")
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    # ------------------------------------------------------------------ #
    # Déconnexion                                                         #
    # ------------------------------------------------------------------ #

    def deconnecter(self):
        """Ferme la fenêtre principale et réaffiche la fenêtre de connexion."""
        self.root.destroy()
        import tkinter as tk2
        from views.login_view import LoginView
        root = tk2.Tk()
        LoginView(root)
        root.mainloop()
