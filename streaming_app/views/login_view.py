"""
Module login_view.py
Fenêtre de connexion pour les employés.
Gère l'authentification et redirige vers la fenêtre principale
selon le niveau d'accès (total ou lecture).
"""

import tkinter as tk
from tkinter import messagebox
from models.employe import Employe


class LoginView:
    """Fenêtre de connexion. Demande le code utilisateur et le mot de passe."""

    def __init__(self, root):
        """
        Initialise la fenêtre de connexion.

        Args:
            root (tk.Tk): La fenêtre racine Tkinter.
        """
        self.root = root
        self.root.title("Connexion Employé")
        self.root.geometry("350x220")
        self.root.resizable(False, False)

        tk.Label(root, text="Streaming App", font=("Arial", 14, "bold")).pack(pady=10)

        # Champ : Code utilisateur
        tk.Label(root, text="Code utilisateur").pack(pady=3)
        self.entry_code = tk.Entry(root)
        self.entry_code.pack()
        self.entry_code.focus()

        # Champ : Mot de passe (masqué)
        tk.Label(root, text="Mot de passe").pack(pady=3)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        # Touche Entrée déclenche la connexion
        self.root.bind("<Return>", lambda event: self.login())

        # Bouton connexion
        tk.Button(root, text="Connexion", command=self.login, width=15).pack(pady=15)

    def login(self):
        """
        Vérifie les identifiants via la classe Employe.
        Ouvre la fenêtre principale avec le bon niveau d'accès, ou affiche une erreur.
        """
        code = self.entry_code.get().strip()
        password = self.entry_password.get()

        # Validation : champs non vides
        if not code or not password:
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.")
            return

        try:
            employe = Employe.authentifier(code, password)

            if employe is None:
                messagebox.showerror("Erreur", "Code utilisateur ou mot de passe incorrect.")
                self.entry_password.delete(0, tk.END)
                return

            # Connexion réussie : ouvrir la fenêtre principale
            self.root.destroy()
            from views.main_view import MainView
            root = tk.Tk()
            MainView(root, employe)
            root.mainloop()

        except Exception as e:
            messagebox.showerror("Erreur inattendue", str(e))
