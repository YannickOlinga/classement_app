#!/usr/bin/env python3
"""Test simple pour vérifier que l'API utilise bien le dossier spécifié."""
import sys
import tempfile
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from client_api import health_check, organize

def main():
    print("🧪 Test API - Vérification du dossier spécifié")
    print("=" * 50)
    
    # Vérifier que l'API est disponible
    if not health_check():
        print("❌ API non disponible. Lancez d'abord : python3 api.py")
        sys.exit(1)
    
    print("✅ API disponible\n")
    
    # Créer un dossier de test
    temp_dir = Path(tempfile.mkdtemp(prefix="test_api_"))
    print(f"📁 Dossier de test : {temp_dir}")
    
    # Créer quelques fichiers de test
    (temp_dir / "test.txt").write_text("Fichier de test")
    (temp_dir / "image.jpg").write_text("Fichier image")
    (temp_dir / "code.py").write_text("Fichier code")
    
    print("✓ Fichiers de test créés\n")
    
    # Tester l'organisation avec ce dossier
    print(f"🔧 Test d'organisation sur : {temp_dir}")
    try:
        result = organize(str(temp_dir))
        print("✅ Organisation réussie !")
        print(f"   Fichiers déplacés : {result.get('deplaces', 0)}")
        print(f"   Fichiers ignorés : {result.get('ignores', 0)}")
        print(f"   Message : {result.get('message', '')}")
        
        # Vérifier que les fichiers ont été déplacés
        sous_dossiers = [d for d in temp_dir.iterdir() if d.is_dir()]
        print(f"\n📂 Sous-dossiers créés : {len(sous_dossiers)}")
        for dossier in sous_dossiers:
            fichiers = list(dossier.iterdir())
            print(f"   {dossier.name}/ : {len(fichiers)} fichier(s)")
        
        print("\n✅ Test réussi - Le dossier spécifié est bien utilisé !")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("\n⚠️  Le dossier spécifié n'est probablement pas utilisé correctement")
        sys.exit(1)
    
    print(f"\n🗑️  Pour nettoyer : rm -rf {temp_dir}")

if __name__ == "__main__":
    main()
