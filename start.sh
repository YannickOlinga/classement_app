#!/bin/bash

# Script de démarrage du projet Organiseur avec React + FastAPI

echo "🚀 Démarrage du projet Organiseur (React + FastAPI)..."

# Vérifier les dépendances Python
echo "📦 Vérification des dépendances Python..."
/usr/bin/python3 -m pip install -q fastapi uvicorn python-multipart 2>/dev/null || {
    echo "⚠️  Impossible d'installer fastapi. Assurez-vous que Python 3 est installé."
    exit 1
}

# Vérifier les dépendances Node
echo "📦 Vérification des dépendances Node..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install -q
fi
cd ..

# Démarrer le backend FastAPI
echo "🔧 Démarrage du backend FastAPI (port 8000)..."
/usr/bin/python3 api.py &
BACKEND_PID=$!

# Petit délai pour que le backend démarre
sleep 2

# Démarrer le frontend Vite
echo "🎨 Démarrage du frontend Vite (port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Message de succès
echo ""
echo "✅ Application lancée!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Frontend:  http://localhost:5173"
echo "🔌 API:       http://localhost:8000"
echo "📚 Docs:      http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Pour arrêter l'application, appuyez sur Ctrl+C"
echo ""

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt de l'application..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Application arrêtée"
    exit 0
}

# Gérer l'interruption
trap cleanup SIGINT SIGTERM

# Attendre que les processus se terminent
wait
