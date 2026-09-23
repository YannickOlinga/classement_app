#!/usr/bin/env python3
"""API FastAPI pour l'organiseur de fichiers."""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, Optional, Union

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError:
    print("❌ FastAPI not installed. Run: pip install fastapi uvicorn")
    exit(1)

from organiser import (
    categories_par_dossier,
    charger_config,
    dossier_telechargements,
    normaliser_extension,
    organiser,
    sauvegarder_config,
)

app = FastAPI(title="Organiseur API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
_cats, _dossier_autres = charger_config()
_lock = threading.Lock()


def get_state() -> tuple[dict, str]:
    """Récupère l'état actuel."""
    with _lock:
        return dict(_cats), _dossier_autres


def set_state(cats: dict, autres: str) -> None:
    """Définit l'état actuel."""
    global _cats, _dossier_autres
    with _lock:
        _cats, _dossier_autres = cats, autres
    sauvegarder_config(cats, autres)


def build_config_payload(cats: dict, autres: str) -> dict:
    """Construit la réponse de configuration."""
    pd = categories_par_dossier(cats)
    if autres not in pd:
        pd[autres] = []
    return {"categories": cats, "dossier_autres": autres, "par_dossier": pd}


# Routes
@app.get("/api/config")
async def get_config() -> dict[str, Any]:
    """Récupère la configuration actuelle."""
    cats, autres = get_state()
    return build_config_payload(cats, autres)


@app.post("/api/config")
async def update_config(payload: dict[str, Any]) -> dict[str, Any]:
    """Met à jour la configuration."""
    try:
        cats = payload.get("categories", {})
        autres = payload.get("dossier_autres", "Autres")
        set_state(cats, autres)
        return build_config_payload(cats, autres)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/organiser")
async def apply_organiser(body: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Applique l'organiseur."""
    try:
        cats, autres = get_state()
        
        # Récupérer le dossier depuis la requête - requis
        if not body or "dossier" not in body or not body["dossier"]:
            raise ValueError("Dossier requis dans la requête")
        
        dossier_str = body["dossier"].strip()
        dossier = Path(dossier_str).expanduser().resolve()
        
        if not dossier.is_dir():
            raise ValueError(f"Le dossier n'existe pas: {dossier}")
        
        deplaces, ignores = organiser(dossier, cats, autres)
        return {
            "success": True,
            "message": f"Fichiers organisés avec succès ({deplaces} déplacés, {ignores} ignorés)",
            "deplaces": deplaces,
            "ignores": ignores,
            "dossier": str(dossier),
            "config": build_config_payload(cats, autres),
        }
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Vérification de santé."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
