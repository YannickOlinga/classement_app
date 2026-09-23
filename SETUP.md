# 🚀 Organiseur de Fichiers - Setup React + FastAPI

## Architecture

```
┌─────────────────────────────────────────────┐
│         React Frontend (Vite)                │
│      (Port 5173 - localhost:5173)           │
│  ✨ Interface interactive avec material UI   │
└──────────────┬──────────────────────────────┘
               │ HTTP/REST API
               ↓
┌─────────────────────────────────────────────┐
│        FastAPI Backend (Uvicorn)             │
│      (Port 8000 - localhost:8000)           │
│  ⚡ Gestion des fichiers & configurations   │
│  📚 OpenAPI Docs: /docs                     │
└─────────────────────────────────────────────┘
```

## 🛠️ Installation Rapide

### Prérequis
- Python 3.8+
- Node.js 16+ et npm
- macOS (le projet est configuré pour macOS)

### Installation

```bash
# 1. Installation des dépendances Python
pip3 install fastapi uvicorn python-multipart

# 2. Installation des dépendances Node
cd frontend
npm install
cd ..
```

## ▶️ Démarrage

### Option 1: Script automatique (recommandé)
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manuel

**Terminal 1 - Backend:**
```bash
python3 api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 📡 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/config` | Récupère la configuration actuelle |
| POST | `/api/config` | Met à jour la configuration |
| POST | `/api/organiser` | Applique l'organisation des fichiers |
| GET | `/api/health` | Vérification de santé |
| GET | `/docs` | Documentation interactive (Swagger) |

## 🎨 Frontend

- **Framework**: React 19 avec Vite
- **Styling**: CSS moderne avec animations
- **Features**:
  - Affichage des catégories de fichiers
  - Visualisation de l'organisation par dossier
  - Bouton pour lancer l'organisation
  - Gestion des erreurs
  - Interface responsive (mobile-friendly)

## 🔧 Backend

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Features**:
  - API RESTful complète
  - CORS activé pour React
  - Documentation automatique (Swagger/OpenAPI)
  - Intégration avec `organiser.py` existant
  - Thread-safe state management

## 🌐 URLs locales

| Application | URL |
|-------------|-----|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

## 📝 Développement

### Hot Reload activé
- Frontend: Automatique avec Vite
- Backend: Relancez `python3 api.py` après modifications

### Structure du projet

```
classement/
├── api.py                  # Backend FastAPI
├── organiser.py           # Logique d'organisation (existant)
├── config.json            # Configuration des catégories
├── start.sh               # Script de démarrage
└── frontend/
    ├── package.json       # Dépendances Node
    ├── vite.config.js     # Configuration Vite (avec proxy API)
    ├── src/
    │   ├── App.jsx        # Composant principal React
    │   ├── App.css        # Styles de l'app
    │   ├── main.jsx       # Point d'entrée
    │   └── index.css      # Styles globaux
    └── public/            # Assets statiques
```

## 🚀 Déploiement

### Production avec Procfile
Le `Procfile` est déjà configuré pour Heroku/Fly.io:

```bash
# Procfile
web: python3 api.py
```

Pour déployer:
```bash
git push heroku main
```

## ⚙️ Configuration

Modifiez `config.json` pour ajouter/modifier les catégories de fichiers:

```json
{
  "categories": {
    ".pdf": "Documents",
    ".jpg": "Images",
    ".mp4": "Vidéos"
  },
  "dossier_autres": "Autres"
}
```

## 🐛 Dépannage

### Port déjà utilisé
```bash
# Backend (8000)
lsof -ti:8000 | xargs kill

# Frontend (5173)
lsof -ti:5173 | xargs kill
```

### Erreur CORS
Vérifiez que Vite proxy les requêtes API. Voir `frontend/vite.config.js`

### Modules Python manquants
```bash
pip3 install --upgrade fastapi uvicorn python-multipart
```

### Modules Node manquants
```bash
cd frontend
npm install
```

## 📚 Documentation Officielle

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- Uvicorn: https://www.uvicorn.org/

---

**Dernière mise à jour**: 18 septembre 2026
