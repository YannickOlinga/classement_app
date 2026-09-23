#!/usr/bin/env python3
"""Client Python pour tester l'API FastAPI."""
import json
import requests
from pathlib import Path

API_BASE = "http://localhost:8000"


def get_config():
    """Récupère la configuration actuelle."""
    resp = requests.get(f"{API_BASE}/api/config")
    resp.raise_for_status()
    return resp.json()


def update_config(categories: dict, dossier_autres: str):
    """Met à jour la configuration."""
    payload = {
        "categories": categories,
        "dossier_autres": dossier_autres,
    }
    resp = requests.post(f"{API_BASE}/api/config", json=payload)
    resp.raise_for_status()
    return resp.json()


def organize(dossier: str | None = None):
    """Lance l'organisation des fichiers.
    
    Args:
        dossier: Chemin du dossier à organiser (requis)
    """
    if not dossier:
        raise ValueError("Le paramètre 'dossier' est requis")
    
    payload = {
        "dossier": dossier
    }
    resp = requests.post(f"{API_BASE}/api/organiser", json=payload)
    resp.raise_for_status()
    return resp.json()


def health_check():
    """Vérifie la santé de l'API."""
    try:
        resp = requests.get(f"{API_BASE}/api/health", timeout=2)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


if __name__ == "__main__":
    import sys

    if not health_check():
        print("❌ API non disponible. Assurez-vous que le serveur est en cours d'exécution.")
        print(f"   Lancer: python3 api.py")
        sys.exit(1)

    print("✅ API disponible\n")

    # Exemple 1: Récupérer la config
    print("📥 Récupération de la configuration...")
    config = get_config()
    print(f"   ✓ {len(config['categories'])} catégories chargées")
    print(f"   ✓ Dossier 'Autres': {config['dossier_autres']}\n")

    # Exemple 2: Afficher les catégories
    print("📂 Catégories actuelles:")
    for ext, cat in list(config["categories"].items())[:5]:
        print(f"   {ext:8} → {cat}")
    if len(config["categories"]) > 5:
        print(f"   ... et {len(config['categories']) - 5} autres")

    print("\n✅ Client prêt!")
    print("\nExemples d'utilisation:")
    print("  config = get_config()")
    print("  result = organize('~/Downloads')")
    print("  result = organize('/Users/username/Documents/Projet')")
    print("  update_config({''.pdf': 'Docs'}, 'Autres')")
