"""
Module client_form.py
Formulaire de création et de modification d'un client.
Valide toutes les entrées avant d'appeler le modèle Client.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import date
from models.client import Client


class ClientForm:
    """Formulaire modal pour créer ou modifier un client."""

    def __init__(self, root, refresh_callback, client=None):
        """
        Initialise le formulaire.

        Args:
            root (tk.Widget): La fenêtre parente.
            refresh_callback (callable): Fonction à appeler après sauvegarde
                                         pour rafraîchir la liste principale.
            client (Client|None): Client à modifier, ou None pour une création.
        """
        self.top = tk.Toplevel(root)
        self.top.title("Modifier un client" if client else "Créer un client")
        self.top.geometry("360x380")
        self.top.resizable(False, False)
        self.top.grab_set()  # Bloquer la fenêtre parente pendant le formulaire

        self.refresh_callback = refresh_callback
        self.client = client

        # --- Champ Nom ---
        tk.Label(self.top, text="Nom *").pack(pady=(10, 0))
        self.entry_nom = tk.Entry(self.top, width=35)
        self.entry_nom.pack()

        # --- Champ Prénom ---
        tk.Label(self.top, text="Prénom *").pack(pady=(8, 0))
        self.entry_prenom = tk.Entry(self.top, width=35)
        self.entry_prenom.pack()

        # --- Champ Sexe ---
        tk.Label(self.top, text="Sexe *").pack(pady=(8, 0))
        self.sexe_var = tk.StringVar(value="M")
        frame_sexe = tk.Frame(self.top)
        frame_sexe.pack()
        for valeur, libelle in [("M", "Masculin"), ("F", "Féminin"), ("Autre", "Autre")]:
            tk.Radiobutton(frame_sexe, text=libelle, variable=self.sexe_var,
                           value=valeur).pack(side="left", padx=5)

        # --- Champ Date d'inscription ---
        tk.Label(self.top, text="Date d'inscription (YYYY-MM-DD) *").pack(pady=(8, 0))
        self.entry_date = tk.Entry(self.top, width=35)
        self.entry_date.pack()
        # Valeur par défaut : aujourd'hui
        self.entry_date.insert(0, str(date.today()))

        # --- Champ Courriel ---
        tk.Label(self.top, text="Courriel *").pack(pady=(8, 0))
        self.entry_courriel = tk.Entry(self.top, width=35)
        self.entry_courriel.pack()

        # --- Champ Mot de passe ---
        tk.Label(self.top, text="Mot de passe * (8 caractères min.)").pack(pady=(8, 0))
        self.entry_password = tk.Entry(self.top, show="*", width=35)
        self.entry_password.pack()

        # --- Bouton Enregistrer ---
        tk.Button(self.top, text="Enregistrer", command=self.save,
                  width=15, bg="#4CAF50", fg="white").pack(pady=15)

        # --- Pré-remplir si modification ---
        if client:
            self.entry_nom.insert(0, client.nom)
            self.entry_prenom.insert(0, client.prenom)
            self.sexe_var.set(client.sexe)
            self.entry_date.delete(0, tk.END)
            self.entry_date.insert(0, client.date_inscription)
            self.entry_courriel.insert(0, client.courriel)

    # ------------------------------------------------------------------ #
    # Validation et sauvegarde                                            #
    # ------------------------------------------------------------------ #

    def _valider_courriel(self, courriel):
        """Vérifie que le courriel contient au minimum un '@' et un '.'."""
        return "@" in courriel and "." in courriel.split("@")[-1]

    def _valider_date(self, date_str):
        """Vérifie que la date est au format YYYY-MM-DD."""
        try:
            date.fromisoformat(date_str)
            return True
        except ValueError:
            return False

    def save(self):
        """
        Valide les champs puis crée ou modifie le client.
        Affiche un message de confirmation ou d'erreur selon le résultat.
        """
        nom = self.entry_nom.get().strip()
        prenom = self.entry_prenom.get().strip()
        sexe = self.sexe_var.get()
        date_inscription = self.entry_date.get().strip()
        courriel = self.entry_courriel.get().strip()
        password = self.entry_password.get()

        # --- Validation des champs obligatoires ---
        if not nom:
            messagebox.showwarning("Champ manquant", "Le nom est obligatoire.")
            self.entry_nom.focus()
            return

        if not prenom:
            messagebox.showwarning("Champ manquant", "Le prénom est obligatoire.")
            self.entry_prenom.focus()
            return

        if not courriel:
            messagebox.showwarning("Champ manquant", "Le courriel est obligatoire.")
            self.entry_courriel.focus()
            return

        if not self._valider_courriel(courriel):
            messagebox.showwarning("Courriel invalide", "Le courriel doit contenir '@' et un domaine valide.")
            self.entry_courriel.focus()
            return

        if not date_inscription:
            messagebox.showwarning("Champ manquant", "La date d'inscription est obligatoire.")
            self.entry_date.focus()
            return

        if not self._valider_date(date_inscription):
            messagebox.showwarning("Date invalide", "La date doit être au format YYYY-MM-DD (ex: 2024-01-15).")
            self.entry_date.focus()
            return

        if not password:
            messagebox.showwarning("Champ manquant", "Le mot de passe est obligatoire.")
            self.entry_password.focus()
            return

        # --- Appel au modèle Client (peut lever ValueError) ---
        try:
            if self.client:
                # Modification d'un client existant
                Client.modifier_client(
                    self.client.courriel,
                    nom, prenom, sexe,
                    courriel, password
                )
                messagebox.showinfo("Succès", "Client modifié avec succès.")
            else:
                # Création d'un nouveau client
                Client.ajouter_client(nom, prenom, sexe, date_inscription, courriel, password)
                messagebox.showinfo("Succès", "Client créé avec succès.")

            self.refresh_callback()
            self.top.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur de validation", str(e))
