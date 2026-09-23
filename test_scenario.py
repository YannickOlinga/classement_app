#!/usr/bin/env python3
"""Script de test pour vérifier que le dossier sélectionné est bien utilisé."""
import tempfile
import shutil
from pathlib import Path

def creer_dossier_test():
    """Crée un dossier de test avec différents types de fichiers."""
    temp_dir = Path(tempfile.mkdtemp(prefix="test_organiseur_"))
    print(f"📁 Dossier de test créé : {temp_dir}")
    
    # Créer des fichiers de différents types
    fichiers_test = {
        "photo_vacances.jpg": "Images",
        "screenshot.png": "Images",
        "document.pdf": "Documents",
        "presentation.pptx": "Documents",
        "video.mp4": "Vidéos",
        "film.mkv": "Vidéos",
        "musique.mp3": "Audio",
        "podcast.wav": "Audio",
        "archive.zip": "Archives",
        "projet.py": "Code",
        "script.js": "Code",
        "application.exe": "Programmes",
        "fichier_inconnu.xyz": "Autres",
    }
    
    for nom_fichier, categorie in fichiers_test.items():
        chemin = temp_dir / nom_fichier
        chemin.write_text(f"Fichier de test pour la catégorie {categorie}")
        print(f"  ✓ {nom_fichier} ({categorie})")
    
    return temp_dir

def main():
    print("🧪 Scénario de test - Organisation de fichiers")
    print("=" * 50)
    
    # Créer le dossier de test
    dossier_test = creer_dossier_test()
    
    print("\n" + "=" * 50)
    print("Instructions de test :")
    print("=" * 50)
    print(f"\n1. Dossier de test : {dossier_test}")
    print("\n2. Test avec l'interface React :")
    print("   - Lancez l'application : ./start.sh")
    print("   - Allez sur http://localhost:5173")
    print(f"   - Entrez le dossier : {dossier_test}")
    print("   - Cliquez sur 'Organiser les fichiers'")
    print("   - Vérifiez que les fichiers sont déplacés dans les sous-dossiers")
    
    print("\n3. Test avec l'API FastAPI directement :")
    print("   - Lancez le backend : python3 api.py")
    print("   - Dans un autre terminal, lancez :")
    print(f"     python3 -c \"from client_api import organize; print(organize('{dossier_test}'))\"")
    
    print("\n4. Vérification manuelle :")
    print(f"   - Ouvrez le dossier : {dossier_test}")
    print("   - Vous devriez voir les sous-dossiers : Images, Vidéos, Documents, etc.")
    print("   - Chaque fichier doit être dans son dossier correspondant")
    
    print("\n5. Nettoyage :")
    print(f"   - Pour supprimer le dossier de test : rm -rf {dossier_test}")
    
    print("\n" + "=" * 50)
    print("Résultat attendu :")
    print("=" * 50)
    print(f"{dossier_test}/")
    print("├── Images/")
    print("│   ├── photo_vacances.jpg")
    print("│   └── screenshot.png")
    print("├── Vidéos/")
    print("│   ├── video.mp4")
    print("│   └── film.mkv")
    print("├── Documents/")
    print("│   ├── document.pdf")
    print("│   └── presentation.pptx")
    print("├── Audio/")
    print("│   ├── musique.mp3")
    print("│   └── podcast.wav")
    print("├── Archives/")
    print("│   └── archive.zip")
    print("├── Code/")
    print("│   ├── projet.py")
    print("│   └── script.js")
    print("├── Programmes/")
    print("│   └── application.exe")
    print("└── Autres/")
    print("    └── fichier_inconnu.xyz")
    
    print("\n" + "=" * 50)
    print("✅ Scénario de test prêt")
    print("=" * 50)

if __name__ == "__main__":
    main()
