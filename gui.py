#!/usr/bin/env python3
"""Interface graphique pour l'organiseur de fichiers."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog, ttk
except ModuleNotFoundError as e:
    print(
        "Erreur : tkinter n'est pas disponible avec ce Python.\n\n"
        "Sur macOS, lancez plutôt :\n"
        "  /usr/bin/python3 gui.py\n"
        "  ./lancer_gui.sh\n\n"
        "Ou installez tk pour Homebrew : brew install python-tk@3.14",
        file=__import__("sys").stderr,
    )
    raise SystemExit(1) from e

from organiser import (
    CONFIG_PATH,
    categories_par_dossier,
    charger_config,
    dossier_telechargements,
    normaliser_extension,
    organiser,
    sauvegarder_config,
)


class OrganiseurApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Organiseur de fichiers")
        self.minsize(720, 520)
        self.geometry("900x620")

        self.categories, self.dossier_autres = charger_config()
        self.dossier_cible = tk.StringVar(value=str(dossier_telechargements()))
        self.inclure_caches = tk.BooleanVar(value=False)

        self._construire_ui()
        self._rafraichir_liste()

    def _construire_ui(self) -> None:
        style = ttk.Style()
        if "aqua" in style.theme_names():
            style.theme_use("aqua")

        pad = {"padx": 10, "pady": 6}

        # --- Dossier cible ---
        frame_dossier = ttk.LabelFrame(self, text="Dossier à organiser")
        frame_dossier.pack(fill="x", **pad)

        ttk.Entry(frame_dossier, textvariable=self.dossier_cible).pack(
            side="left", fill="x", expand=True, padx=(10, 6), pady=10
        )
        ttk.Button(frame_dossier, text="Parcourir…", command=self._choisir_dossier).pack(
            side="right", padx=(0, 10), pady=10
        )

        # --- Catégories ---
        frame_cat = ttk.LabelFrame(self, text="Dossiers de destination (catégories)")
        frame_cat.pack(fill="both", expand=True, **pad)

        colonnes = ("dossier", "extensions")
        self.arbre = ttk.Treeview(
            frame_cat,
            columns=colonnes,
            show="headings",
            selectmode="browse",
            height=12,
        )
        self.arbre.heading("dossier", text="Nom du dossier")
        self.arbre.heading("extensions", text="Extensions")
        self.arbre.column("dossier", width=180, minwidth=120)
        self.arbre.column("extensions", width=520, minwidth=200)
        self.arbre.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        scroll = ttk.Scrollbar(frame_cat, orient="vertical", command=self.arbre.yview)
        scroll.pack(side="right", fill="y", padx=(4, 10), pady=10)
        self.arbre.configure(yscrollcommand=scroll.set)

        frame_btns = ttk.Frame(self)
        frame_btns.pack(fill="x", padx=10, pady=(0, 4))

        ttk.Button(frame_btns, text="+ Nouveau dossier", command=self._nouveau_dossier).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(frame_btns, text="Renommer dossier", command=self._renommer_dossier).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(frame_btns, text="Supprimer dossier", command=self._supprimer_dossier).pack(
            side="left", padx=(0, 6)
        )
        ttk.Separator(frame_btns, orient="vertical").pack(side="left", fill="y", padx=12)
        ttk.Button(frame_btns, text="+ Extension", command=self._ajouter_extension).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(frame_btns, text="− Extension", command=self._retirer_extension).pack(side="left")

        ttk.Label(
            frame_btns,
            text="  (Le dossier sans extension = fichiers non reconnus)",
            foreground="#555",
        ).pack(side="left", padx=8)

        # --- Actions ---
        frame_action = ttk.Frame(self)
        frame_action.pack(fill="x", padx=10, pady=6)

        ttk.Button(frame_action, text="Aperçu", command=lambda: self._executer(True)).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(frame_action, text="Organiser maintenant", command=lambda: self._executer(False)).pack(
            side="left", padx=(0, 16)
        )
        ttk.Button(frame_action, text="Enregistrer la config", command=self._enregistrer).pack(side="left")
        ttk.Checkbutton(
            frame_action,
            text="Inclure fichiers cachés",
            variable=self.inclure_caches,
        ).pack(side="right")

        # --- Journal ---
        frame_log = ttk.LabelFrame(self, text="Journal")
        frame_log.pack(fill="both", expand=True, **pad)

        self.journal = tk.Text(frame_log, height=10, wrap="word", state="disabled", font=("Menlo", 11))
        self.journal.pack(fill="both", expand=True, padx=10, pady=10)

    def _log(self, texte: str) -> None:
        self.journal.configure(state="normal")
        self.journal.insert("end", texte + "\n")
        self.journal.see("end")
        self.journal.configure(state="disabled")

    def _vider_journal(self) -> None:
        self.journal.configure(state="normal")
        self.journal.delete("1.0", "end")
        self.journal.configure(state="disabled")

    def _choisir_dossier(self) -> None:
        chemin = filedialog.askdirectory(
            title="Choisir le dossier à organiser",
            initialdir=self.dossier_cible.get() or str(dossier_telechargements()),
        )
        if chemin:
            self.dossier_cible.set(chemin)

    def _selection(self) -> str | None:
        sel = self.arbre.selection()
        if not sel:
            messagebox.showinfo("Sélection", "Sélectionnez un dossier dans la liste.")
            return None
        return self.arbre.item(sel[0], "values")[0]

    def _est_dossier_autres(self, nom: str) -> bool:
        return nom == self.dossier_autres

    def _rafraichir_liste(self) -> None:
        for item in self.arbre.get_children():
            self.arbre.delete(item)

        par_dossier = categories_par_dossier(self.categories)
        if self.dossier_autres not in par_dossier:
            par_dossier[self.dossier_autres] = []

        for nom, exts in par_dossier.items():
            label_ext = ", ".join(exts) if exts else "(toutes extensions non listées ailleurs)"
            self.arbre.insert("", "end", values=(nom, label_ext))

    def _persister(self) -> None:
        sauvegarder_config(self.categories, self.dossier_autres)

    def _enregistrer(self) -> None:
        self._persister()
        messagebox.showinfo("Enregistré", f"Configuration sauvegardée :\n{CONFIG_PATH}")

    def _nouveau_dossier(self) -> None:
        nom = simpledialog.askstring(
            "Nouveau dossier",
            "Nom du dossier à créer (ex. Factures, Projets) :",
            parent=self,
        )
        if not nom:
            return
        nom = nom.strip()
        if not nom:
            return
        if nom == self.dossier_autres or nom in categories_par_dossier(self.categories):
            messagebox.showwarning("Existant", f"Le dossier « {nom} » existe déjà.")
            return

        ext = simpledialog.askstring(
            "Extension (optionnel)",
            f"Extension pour « {nom} » (ex. pdf, .facture)\nLaissez vide pour ajouter plus tard :",
            parent=self,
        )
        if ext:
            ext_n = normaliser_extension(ext)
            if not ext_n:
                return
            if ext_n in self.categories:
                ancien = self.categories[ext_n]
                if not messagebox.askyesno(
                    "Extension déjà utilisée",
                    f"{ext_n} est déjà associée à « {ancien} ».\nLa déplacer vers « {nom} » ?",
                ):
                    return
            self.categories[ext_n] = nom

        self._rafraichir_liste()
        self._persister()

    def _renommer_dossier(self) -> None:
        ancien = self._selection()
        if not ancien:
            return

        nouveau = simpledialog.askstring(
            "Renommer",
            f"Nouveau nom pour « {ancien} » :",
            initialvalue=ancien,
            parent=self,
        )
        if not nouveau:
            return
        nouveau = nouveau.strip()
        if not nouveau or nouveau == ancien:
            return

        par_dossier = categories_par_dossier(self.categories)
        if nouveau in par_dossier and nouveau != ancien:
            messagebox.showwarning("Existant", f"Le dossier « {nouveau} » existe déjà.")
            return

        if self._est_dossier_autres(ancien):
            self.dossier_autres = nouveau
        else:
            for ext, dossier in list(self.categories.items()):
                if dossier == ancien:
                    self.categories[ext] = nouveau

        self._rafraichir_liste()
        self._persister()

    def _supprimer_dossier(self) -> None:
        nom = self._selection()
        if not nom:
            return

        if self._est_dossier_autres(nom):
            messagebox.showwarning(
                "Impossible",
                f"« {nom} » est le dossier par défaut (fichiers non reconnus).\n"
                "Vous pouvez le renommer, mais pas le supprimer.",
            )
            return

        if not messagebox.askyesno(
            "Confirmer",
            f"Supprimer la catégorie « {nom} » ?\n"
            f"Les extensions associées iront dans « {self.dossier_autres} ».",
        ):
            return

        self.categories = {
            ext: (self.dossier_autres if dossier == nom else dossier)
            for ext, dossier in self.categories.items()
            if dossier != nom
        }
        self._rafraichir_liste()
        self._persister()

    def _ajouter_extension(self) -> None:
        dossier = self._selection()
        if not dossier:
            return

        if self._est_dossier_autres(dossier):
            messagebox.showinfo(
                "Dossier par défaut",
                f"« {dossier} » reçoit automatiquement toute extension non listée.\n"
                "Sélectionnez un autre dossier pour ajouter des extensions.",
            )
            return

        ext = simpledialog.askstring(
            "Extension",
            f"Extension pour « {dossier} » (ex. pdf ou .pdf) :",
            parent=self,
        )
        if not ext:
            return
        ext_n = normaliser_extension(ext)
        if not ext_n:
            return

        if ext_n in self.categories and self.categories[ext_n] != dossier:
            if not messagebox.askyesno(
                "Remplacer",
                f"{ext_n} est déjà dans « {self.categories[ext_n]} ».\nDéplacer vers « {dossier} » ?",
            ):
                return

        self.categories[ext_n] = dossier
        self._rafraichir_liste()
        self._persister()

    def _retirer_extension(self) -> None:
        dossier = self._selection()
        if not dossier:
            return

        if self._est_dossier_autres(dossier):
            messagebox.showinfo("Info", "Ce dossier n'a pas d'extensions à retirer.")
            return

        exts = [e for e, d in self.categories.items() if d == dossier]
        if not exts:
            messagebox.showinfo("Info", f"Aucune extension dans « {dossier} ».")
            return

        ext = simpledialog.askstring(
            "Retirer",
            f"Extension à retirer de « {dossier} » :\nDisponibles : {', '.join(exts)}",
            parent=self,
        )
        if not ext:
            return
        ext_n = normaliser_extension(ext)
        if ext_n in self.categories and self.categories[ext_n] == dossier:
            del self.categories[ext_n]
            self._rafraichir_liste()
            self._persister()
        else:
            messagebox.showwarning("Introuvable", f"{ext_n} n'est pas dans « {dossier} ».")

    def _executer(self, simulation: bool) -> None:
        from pathlib import Path

        cible = Path(self.dossier_cible.get().strip()).expanduser()
        if not cible.is_dir():
            messagebox.showerror("Erreur", f"Dossier introuvable :\n{cible}")
            return

        if not simulation:
            if not messagebox.askyesno(
                "Confirmer",
                f"Déplacer les fichiers dans :\n{cible}\n\nContinuer ?",
            ):
                return

        self._vider_journal()
        mode = "APERÇU (simulation)" if simulation else "ORGANISATION"
        self._log(f"── {mode} ──")
        self._log(f"Dossier : {cible}")
        self._log("")

        try:
            deplaces, ignores = organiser(
                cible,
                self.categories,
                self.dossier_autres,
                simulation=simulation,
                inclure_caches=self.inclure_caches.get(),
                journal=self._log,
            )
        except NotADirectoryError as e:
            messagebox.showerror("Erreur", str(e))
            return

        self._log("")
        self._log("── Fin ──")
        if deplaces == 0:
            self._log("Aucun fichier à classer.")
        else:
            verbe = "seraient classés" if simulation else "classés"
            self._log(f"{deplaces} fichier(s) {verbe}.")
            if ignores:
                self._log(f"{ignores} élément(s) ignoré(s).")

        if not simulation and deplaces:
            messagebox.showinfo("Terminé", f"{deplaces} fichier(s) organisé(s).")


def lancer_interface() -> None:
    app = OrganiseurApp()
    app.mainloop()


if __name__ == "__main__":
    lancer_interface()
