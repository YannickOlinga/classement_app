#!/bin/bash
# Interface web locale — ouvre automatiquement le navigateur.
cd "$(dirname "$0")"
exec python3 app.py "$@"
