#!/usr/bin/env python3
"""
Organiseur de fichiers — classe automatiquement les fichiers d'un dossier
dans des sous-dossiers par type (Images, Vidéos, Documents, etc.).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

DEFAULT_CATEGORIES: dict[str, str] = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".ico": "Images",
    ".heic": "Images",
    ".tiff": "Images",
    ".tif": "Images",
    ".mp4": "Vidéos",
    ".avi": "Vidéos",
    ".mkv": "Vidéos",
    ".mov": "Vidéos",
    ".wmv": "Vidéos",
    ".flv": "Vidéos",
    ".webm": "Vidéos",
    ".m4v": "Vidéos",
    ".mpeg": "Vidéos",
    ".mpg": "Vidéos",
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".csv": "Documents",
    ".md": "Documents",
    ".pages": "Documents",
    ".numbers": "Documents",
    ".key": "Documents",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",
    ".wma": "Audio",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",
    ".dmg": "Archives",
    ".iso": "Archives",
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".c": "Code",
    ".cpp": "Code",
    ".h": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".sql": "Code",
    ".rb": "Code",
    ".go": "Code",
    ".rs": "Code",
    ".php": "Code",
    ".swift": "Code",
    ".sh": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".exe": "Programmes",
    ".msi": "Programmes",
    ".app": "Programmes",
    ".deb": "Programmes",
    ".rpm": "Programmes",
    ".pkg": "Programmes",
}

DEFAULT_AUTRES = "Autres"


def normaliser_extension(ext: str) -> str:
    ext = ext.strip().lower()
    if not ext:
        return ""
    return ext if ext.startswith(".") else f".{ext}"


def charger_config() -> tuple[dict[str, str], str]:
    """Charge (extensions → dossier, nom du dossier « Autres »)."""
    if CONFIG_PATH.is_file():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            categories = {k: v for k, v in data.get("categories", {}).items()}
            autres = data.get("dossier_autres", DEFAULT_AUTRES)
            if categories:
                return categories, autres
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULT_CATEGORIES), DEFAULT_AUTRES


def sauvegarder_config(categories: dict[str, str], dossier_autres: str) -> None:
    payload = {
        "categories": dict(sorted(categories.items())),
        "dossier_autres": dossier_autres,
    }
    CONFIG_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def categories_par_dossier(categories: dict[str, str]) -> dict[str, list[str]]:
    par_dossier: dict[str, list[str]] = defaultdict(list)
    for ext, dossier in categories.items():
        par_dossier[dossier].append(ext)
    return {d: sorted(exts) for d, exts in sorted(par_dossier.items())}


def dossiers_geres(categories: dict[str, str], dossier_autres: str) -> frozenset[str]:
    return frozenset(categories.values()) | {dossier_autres}


def categorie_fichier(chemin: Path, categories: dict[str, str], dossier_autres: str) -> str:
    return categories.get(chemin.suffix.lower(), dossier_autres)


def destination_unique(dossier: Path, nom: str) -> Path:
    cible = dossier / nom
    if not cible.exists():
        return cible
    stem = Path(nom).stem
    suffix = Path(nom).suffix
    n = 1
    while True:
        cible = dossier / f"{stem} ({n}){suffix}"
        if not cible.exists():
            return cible
        n += 1


def organiser(
    dossier: Path,
    categories: dict[str, str],
    dossier_autres: str = DEFAULT_AUTRES,
    *,
    simulation: bool = False,
    inclure_caches: bool = False,
    journal: Callable[[str], None] | None = None,
) -> tuple[int, int]:
    if not dossier.is_dir():
        raise NotADirectoryError(f"Dossier introuvable : {dossier}")

    def log(msg: str) -> None:
        if journal:
            journal(msg)
        else:
            print(msg)

    geres = dossiers_geres(categories, dossier_autres)
    deplaces = 0
    ignores = 0

    for entree in sorted(dossier.iterdir()):
        if entree.is_dir():
            if entree.name in geres:
                continue
            ignores += 1
            log(f"  ⊘ Dossier ignoré : {entree.name}/")
            continue

        if not entree.is_file():
            ignores += 1
            continue

        if not inclure_caches and entree.name.startswith("."):
            ignores += 1
            continue

        if entree.resolve() == Path(__file__).resolve():
            ignores += 1
            continue

        cat = categorie_fichier(entree, categories, dossier_autres)
        sous_dossier = dossier / cat
        destination = destination_unique(sous_dossier, entree.name)

        if simulation:
            log(f"  → {entree.name}  →  {cat}/{destination.name}")
            deplaces += 1
            continue

        sous_dossier.mkdir(exist_ok=True)
        shutil.move(str(entree), str(destination))
        log(f"  ✓ {entree.name}  →  {cat}/")
        deplaces += 1

    return deplaces, ignores


def dossier_telechargements() -> Path:
    home = Path.home()
    for candidat in (
        home / "Downloads",
        home / "Téléchargements",
        home / "Download",
    ):
        if candidat.is_dir():
            return candidat
    return home / "Downloads"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classe les fichiers d'un dossier dans des sous-dossiers par type.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python3 organiser.py --gui              # Interface graphique
  python3 organiser.py                    # Téléchargements (simulation)
  python3 organiser.py --appliquer        # Téléchargements (réel)
  python3 organiser.py ~/Desktop --appliquer
        """,
    )
    parser.add_argument("dossier", nargs="?", default=None, help="Dossier à organiser")
    parser.add_argument("--gui", action="store_true", help="Lancer l'interface graphique")
    parser.add_argument("--appliquer", action="store_true", help="Déplacer réellement les fichiers")
    parser.add_argument("--fichiers-caches", action="store_true", help="Inclure les fichiers cachés")
    args = parser.parse_args()

    if args.gui:
        from gui import lancer_interface

        lancer_interface()
        return 0

    categories, dossier_autres = charger_config()
    cible = Path(args.dossier).expanduser().resolve() if args.dossier else dossier_telechargements()
    simulation = not args.appliquer

    print()
    print("  Organiseur de fichiers")
    print("  " + "─" * 40)
    print(f"  Dossier : {cible}")
    print(f"  Mode    : {'simulation' if simulation else 'application'}")
    print()

    try:
        deplaces, ignores = organiser(
            cible,
            categories,
            dossier_autres,
            simulation=simulation,
            inclure_caches=args.fichiers_caches,
        )
    except NotADirectoryError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1

    print()
    print("  " + "─" * 40)
    if deplaces == 0:
        print("  Aucun fichier à classer.")
    else:
        action = "seraient classés" if simulation else "classés"
        print(f"  {deplaces} fichier(s) {action}.")
        if ignores:
            print(f"  {ignores} élément(s) ignoré(s).")
        if simulation:
            print()
            print("  Relancez avec --appliquer pour déplacer les fichiers.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
