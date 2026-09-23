#!/bin/bash
# Interface graphique locale — ouvre l'interface tkinter.
cd "$(dirname "$0")"
exec /usr/bin/python3 gui.py "$@"


