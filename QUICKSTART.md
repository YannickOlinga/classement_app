# 🚀 Démarrage Rapide - Organiseur Files (React + FastAPI)

## ⚡ En 3 commands

```bash
# 1. Installer les dépendances
pip3 install -r requirements.txt
cd frontend && npm install && cd ..

# 2. Lancer l'app automatiquement
./start.sh

# 3. Ouvrir le navigateur
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

## 📋 Checklist Rapide

- [ ] Python 3.8+ installé? `python3 --version`
- [ ] Node.js 16+? `node --version`
- [ ] Dans le dossier `/classement`? `pwd`
- [ ] `start.sh` rendu exécutable? `ls -la start.sh`

## 🔥 Raccourcis Utiles

| Commande | Action |
|----------|--------|
| `./start.sh` | Lancer tout (backend + frontend) |
| `python3 api.py` | Lancer le backend seul |
| `cd frontend && npm run dev` | Lancer le frontend seul |
| `python3 client_api.py` | Tester l'API |

## 🌐 URLs de développement

```
🎨 Frontend:      http://localhost:5173
🔌 API Backend:   http://localhost:8000
📚 API Docs:      http://localhost:8000/docs
🔄 ReDoc:         http://localhost:8000/redoc
```

## 📦 Architecture

```
React Frontend (Vite) ←→ FastAPI Backend (Uvicorn)
      5173                     8000
```

**Flux de données:**
1. React affiche l'interface
2. Appels API `/api/*` au backend
3. Backend organise les fichiers avec `organiser.py`
4. React affiche le résultat

## 🎯 Prochaines Étapes

- [ ] Lire [SETUP.md](SETUP.md) pour plus de détails
- [ ] Essayer le bouton "Organiser les fichiers" 
- [ ] Personnaliser `config.json` avec vos catégories
- [ ] Consulter `/docs` pour voir tous les endpoints API

## 💡 Astuces

- **Hot Reload?** Modifiez `frontend/src/App.jsx` → Auto refresh
- **API Down?** Vérifiez que `python3 api.py` s'exécute
- **Port occupé?** Voir la section "Dépannage" dans SETUP.md

---

👉 **Commencez:** `./start.sh` (puis ouvrez http://localhost:5173)
