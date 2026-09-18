# 🚀 Guide de Déploiement

## Option 1 : Replit (Recommandé - Plus simple)

1. Allez sur **[replit.com](https://replit.com)** et créez un compte
2. Cliquez sur **"Create Repl"** → sélectionnez **"Python"**
3. **Import from GitHub** ou uploadez directement les fichiers du projet
4. **Replit lance automatiquement** le serveur
5. Cliquez sur **"Run"** et obtenez votre URL publique (ex: `https://classement.random-user.repl.co`)
6. Partagez cette URL - tout le monde peut y accéder !

**Avantages** :
- ✅ Gratuit et instant
- ✅ Pas de configuration
- ✅ URL permanente
- ✅ Accessible partout

---

## Option 2 : PythonAnywhere (Stable)

1. Allez sur **[pythonanywhere.com](https://www.pythonanywhere.com)**
2. Créez un compte gratuit
3. Uploadez les fichiers dans "Files"
4. Allez dans "Web Apps" → créez une nouvelle app Python
5. Configurez pour servir depuis le répertoire du projet
6. Accédez via `https://votreusername.pythonanywhere.com`

---

## Option 3 : Render (Alternative Heroku gratuit)

1. Créez un compte sur **[render.com](https://render.com)**
2. Créez un nouveau **"Web Service"** → Python
3. Uploadez les fichiers (via Git ou ZIP)
4. Build command: `python3 -m pip install -r requirements.txt`
5. Start command: `WEB_MODE=true PORT=$PORT python3 app.py`
6. Déployé automatiquement avec URL publique

---

## 🔒 Notes de sécurité

- **L'accès aux fichiers** dépend du répertoire configuré
- Sur Replit/PythonAnywhere, les utilisateurs ne voient que les fichiers du projet
- Pour plus de contrôle, limitez l'accès dans `config.json`

## Test local avec mode web

```bash
WEB_MODE=true python3 app.py
```

Puis ouvrez : `http://localhost:8000`
