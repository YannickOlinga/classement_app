#!/usr/bin/env python3
"""Organiseur de fichiers — interface web locale (stdlib uniquement)."""
from __future__ import annotations

import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))
from organiser import (
    categories_par_dossier,
    charger_config,
    dossier_telechargements,
    normaliser_extension,
    organiser,
    sauvegarder_config,
)

_cats, _dossier_autres = charger_config()
_lock = threading.Lock()


def get_state() -> tuple[dict, str]:
    with _lock:
        return dict(_cats), _dossier_autres


def set_state(cats: dict, autres: str) -> None:
    global _cats, _dossier_autres
    with _lock:
        _cats, _dossier_autres = cats, autres
    sauvegarder_config(cats, autres)


def build_config_payload(cats: dict, autres: str) -> dict:
    pd = categories_par_dossier(cats)
    if autres not in pd:
        pd[autres] = []
    return {"categories": cats, "dossier_autres": autres, "par_dossier": pd}


HTML_APP = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Organiseur de fichiers</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f2f2f7;--surface:#fff;--border:#d1d1d6;
  --primary:#007AFF;--primary-h:#0068d9;
  --danger:#FF3B30;--success:#34C759;
  --text:#1c1c1e;--text2:#636366;--text3:#8e8e93;
  --chip-bg:#ddeeff;--chip-fg:#0056CC;
  --log-bg:#1c1c1e;
}
html,body{height:100%}
body{
  font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif;
  font-size:13px;background:var(--bg);color:var(--text);
  display:flex;flex-direction:column;height:100vh;overflow:hidden;
}

/* Header */
.hdr{background:var(--surface);border-bottom:1px solid var(--border);padding:10px 18px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.hdr h1{font-size:15px;font-weight:600;white-space:nowrap}
.folder-row{display:flex;align-items:center;gap:8px;flex:1;max-width:640px}
.folder-inp{
  flex:1;min-width:0;background:var(--bg);border:1px solid var(--border);border-radius:8px;
  padding:6px 10px;font-size:13px;font-family:inherit;color:var(--text);outline:none;
}
.folder-inp:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,122,255,.15)}

/* Buttons */
.btn{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:6px 14px;font-size:13px;font-family:inherit;cursor:pointer;color:var(--text);white-space:nowrap;transition:background .1s}
.btn:hover{background:var(--bg)}
.btn:active{opacity:.85}
.btn-primary{background:var(--primary);border-color:var(--primary);color:#fff}
.btn-primary:hover{background:var(--primary-h);border-color:var(--primary-h)}
.btn-danger{color:var(--danger);border-color:var(--danger)}
.btn-danger:hover{background:#fff0ef}
.btn-sm{padding:4px 10px;font-size:12px;border-radius:6px}

/* Main */
.main{display:flex;flex:1;gap:1px;background:var(--border);overflow:hidden;min-height:0}
.panel-l{width:200px;flex-shrink:0;background:var(--surface);display:flex;flex-direction:column;overflow:hidden}
.panel-l-hdr{padding:9px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.panel-l-hdr span{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:var(--text2)}
.cat-list{flex:1;overflow-y:auto;padding:4px 0}
.cat-item{padding:7px 14px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:6px;transition:background .1s}
.cat-item:hover{background:var(--bg)}
.cat-item.sel{background:var(--primary);color:#fff}
.cat-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cat-badge{font-size:11px;background:rgba(0,0,0,.08);border-radius:10px;padding:1px 6px;opacity:.65;flex-shrink:0}
.cat-item.sel .cat-badge{background:rgba(255,255,255,.25);opacity:1}

.panel-r{flex:1;background:var(--surface);display:flex;flex-direction:column;overflow:hidden}
.panel-r-hdr{padding:13px 20px 11px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-shrink:0}
.panel-r-hdr h2{font-size:15px;font-weight:600;flex:1}
.panel-r-body{flex:1;overflow-y:auto;padding:16px 20px}

/* Extension chips */
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}
.chip{display:inline-flex;align-items:center;gap:3px;background:var(--chip-bg);color:var(--chip-fg);border-radius:6px;padding:4px 8px 4px 10px;font-size:12px;font-family:"SF Mono",Menlo,Monaco,monospace}
.chip-x{background:none;border:none;cursor:pointer;color:var(--chip-fg);opacity:.5;font-size:14px;line-height:1;padding:0;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.chip-x:hover{opacity:1;background:rgba(0,86,204,.15)}
.add-row{display:flex;gap:8px;align-items:center;margin-top:4px}
.inp-sm{border:1px solid var(--border);border-radius:6px;padding:5px 8px;font-size:12px;font-family:"SF Mono",Menlo,Monaco,monospace;width:150px;outline:none;color:var(--text);background:var(--bg)}
.inp-sm:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,122,255,.15)}
.note-box{background:#fff8e6;border:1px solid #ffe59e;border-radius:8px;padding:12px 16px;color:#9a6800;font-size:12px;line-height:1.6}
.empty-hint{color:var(--text3);margin-top:16px}
.placeholder{color:var(--text3);text-align:center;margin-top:50px;font-size:14px}

/* Bottom bar */
.bot{background:var(--surface);border-top:1px solid var(--border);padding:9px 18px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.bot label{display:flex;align-items:center;gap:5px;color:var(--text2);cursor:pointer;user-select:none}

/* Log */
.log-wrap{background:var(--log-bg);flex-shrink:0;height:185px;display:flex;flex-direction:column;min-height:0}
.log-hdr{padding:5px 16px;border-bottom:1px solid #3a3a3c;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.log-hdr span{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:#8e8e93}
.log-hdr button{background:none;border:none;color:#8e8e93;font-size:11px;cursor:pointer;padding:2px 7px;border-radius:4px}
.log-hdr button:hover{background:#3a3a3c;color:#e5e5ea}
.log-body{flex:1;overflow-y:auto;padding:8px 16px;font-family:"SF Mono",Menlo,Monaco,"Courier New",monospace;font-size:12px;line-height:1.65;color:#e5e5ea;white-space:pre-wrap}
.lk{color:#34C759}.la{color:#64D2FF}.li{color:#636366}.lh{color:#ffd60a;font-weight:700}.lc{color:#bf5af2}.le{color:#FF453A}

/* Overlay / modal base */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;z-index:999}
.overlay.hidden{display:none}
.modal{background:var(--surface);border-radius:14px;padding:24px;box-shadow:0 20px 60px rgba(0,0,0,.25)}

/* Text input modal */
.modal-sm{width:320px}
.modal h3{font-size:15px;margin-bottom:14px}
.modal-inp{width:100%;border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:13px;font-family:inherit;color:var(--text);outline:none;margin-bottom:16px}
.modal-inp:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,122,255,.15)}
.modal-btns{display:flex;justify-content:flex-end;gap:8px}

/* Folder picker modal */
.fp-modal{width:480px;max-height:75vh;display:flex;flex-direction:column;padding:20px}
.fp-title{font-size:15px;font-weight:600;margin-bottom:10px}
.fp-crumb{display:flex;align-items:center;flex-wrap:wrap;gap:2px;padding:6px 0;border-bottom:1px solid var(--border);margin-bottom:6px;min-height:32px}
.fp-bc{cursor:pointer;color:var(--primary);font-size:12px;padding:2px 4px;border-radius:4px}
.fp-bc:hover{background:var(--chip-bg)}
.fp-sep{color:var(--text3);font-size:12px;padding:0 1px}
.fp-list{flex:1;overflow-y:auto;margin:4px 0 12px;border:1px solid var(--border);border-radius:8px;min-height:120px}
.fp-item{padding:8px 14px;cursor:pointer;display:flex;align-items:center;gap:8px;transition:background .1s;font-size:13px}
.fp-item:hover{background:var(--bg)}
.fp-item:not(:last-child){border-bottom:1px solid #f0f0f2}
.fp-cur{padding:6px 12px;background:var(--bg);border-radius:6px;font-size:12px;color:var(--text2);margin-bottom:8px;word-break:break-all;font-family:"SF Mono",Menlo,Monaco,monospace}
.fp-empty{padding:20px;text-align:center;color:var(--text3);font-size:12px}

/* Scrollbar */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(0,0,0,.18);border-radius:3px}
</style>
</head>
<body>

<div class="hdr">
  <h1>📁 Organiseur de fichiers</h1>
  <div class="folder-row">
    <input id="folder" class="folder-inp" placeholder="Cliquez sur Choisir… ou tapez un chemin" spellcheck="false">
    <button class="btn" onclick="browse()">Choisir…</button>
  </div>
</div>

<div class="main">
  <div class="panel-l">
    <div class="panel-l-hdr">
      <span>Catégories</span>
      <button class="btn btn-sm" onclick="newCat()">+ Nouveau</button>
    </div>
    <div class="cat-list" id="cat-list"></div>
  </div>
  <div class="panel-r">
    <div class="panel-r-hdr" id="r-hdr">
      <h2 style="color:var(--text3);font-weight:400">Sélectionnez une catégorie</h2>
    </div>
    <div class="panel-r-body" id="r-body">
      <p class="placeholder">← Choisissez une catégorie dans la liste</p>
    </div>
  </div>
</div>

<div class="bot">
  <label><input type="checkbox" id="hidden-cb"> Fichiers cachés</label>
  <div style="flex:1"></div>
  <button class="btn" onclick="runOrg(true)">Aperçu</button>
  <button class="btn btn-primary" onclick="runOrg(false)">Organiser maintenant</button>
</div>

<div class="log-wrap">
  <div class="log-hdr">
    <span>Journal</span>
    <button onclick="clearLog()">Effacer</button>
  </div>
  <div class="log-body" id="log"></div>
</div>

<!-- Text input modal -->
<div class="overlay hidden" id="overlay-text">
  <div class="modal modal-sm">
    <h3 id="m-title"></h3>
    <input id="m-inp" class="modal-inp" autocomplete="off">
    <div class="modal-btns">
      <button class="btn" onclick="mCancel()">Annuler</button>
      <button class="btn btn-primary" onclick="mOk()">OK</button>
    </div>
  </div>
</div>

<!-- Folder picker modal -->
<div class="overlay hidden" id="overlay-fp">
  <div class="modal fp-modal">
    <div class="fp-title">📂 Choisir un dossier</div>
    <div class="fp-crumb" id="fp-crumb"></div>
    <div class="fp-cur" id="fp-cur"></div>
    <div class="fp-list" id="fp-list"><div class="fp-empty">Chargement…</div></div>
    <div class="modal-btns">
      <button class="btn" onclick="fpCancel()">Annuler</button>
      <button class="btn btn-primary" onclick="fpSelect()">✓ Sélectionner ce dossier</button>
    </div>
  </div>
</div>

<script>
const S = {cats:{}, autres:'Autres', pd:{}, sel:null};

// ── API helpers ──────────────────────────────────────────────
async function apiGet(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return r.json();
}
async function apiPost(url, data) {
  const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return r.json();
}

// ── Init ─────────────────────────────────────────────────────
async function init() {
  try {
    const d = await apiGet('/api/config');
    applyConfig(d);
    document.getElementById('folder').value = d.dossier_cible || '';
  } catch(e) {
    logLine('Erreur chargement config : ' + e.message, 'le');
  }
}

function applyConfig(d) {
  if (d.error) { alert(d.error); return; }
  S.cats = d.categories;
  S.autres = d.dossier_autres;
  S.pd = d.par_dossier;
  renderList();
  if (S.sel) renderDetail(S.sel);
}

// ── Category list ─────────────────────────────────────────────
function renderList() {
  const el = document.getElementById('cat-list');
  el.innerHTML = '';
  Object.keys(S.pd).forEach(name => {
    const exts = S.pd[name] || [];
    const div = document.createElement('div');
    div.className = 'cat-item' + (name === S.sel ? ' sel' : '');
    const badge = name === S.autres ? '∞' : exts.length;
    div.innerHTML = '<span class="cat-name">' + esc(name) + '</span><span class="cat-badge">' + badge + '</span>';
    div.onclick = () => { S.sel = name; renderList(); renderDetail(name); };
    el.appendChild(div);
  });
}

// ── Category detail ───────────────────────────────────────────
function renderDetail(name) {
  const exts = S.pd[name] || [];
  const isDef = name === S.autres;

  // Header
  const hdr = document.getElementById('r-hdr');
  hdr.innerHTML = '';
  const h2 = document.createElement('h2');
  h2.textContent = name;
  if (isDef) {
    const badge = document.createElement('span');
    badge.textContent = 'par défaut';
    badge.style.cssText = 'font-size:11px;font-weight:400;color:var(--text3);background:var(--bg);border-radius:4px;padding:2px 7px;margin-left:8px';
    h2.appendChild(badge);
  }
  hdr.appendChild(h2);
  const btnRen = document.createElement('button');
  btnRen.className = 'btn btn-sm';
  btnRen.textContent = 'Renommer';
  btnRen.onclick = () => renameCat(name);
  hdr.appendChild(btnRen);
  if (!isDef) {
    const btnDel = document.createElement('button');
    btnDel.className = 'btn btn-sm btn-danger';
    btnDel.textContent = 'Supprimer';
    btnDel.onclick = () => deleteCat(name);
    hdr.appendChild(btnDel);
  }

  // Body
  const body = document.getElementById('r-body');
  body.innerHTML = '';
  if (isDef) {
    body.innerHTML = '<div class="note-box"><strong>Dossier par défaut</strong><br>Reçoit automatiquement tout fichier dont l\'extension n\'est listée nulle part ailleurs. Vous pouvez le renommer, mais pas le supprimer.</div>';
    return;
  }

  // Chips
  const chips = document.createElement('div');
  chips.className = 'chips';
  exts.forEach(e => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.appendChild(document.createTextNode(e));
    const x = document.createElement('button');
    x.className = 'chip-x';
    x.textContent = '×';
    x.onclick = () => removeExt(e, name);
    chip.appendChild(x);
    chips.appendChild(chip);
  });
  body.appendChild(chips);

  // Add-row
  const row = document.createElement('div');
  row.className = 'add-row';
  const inp = document.createElement('input');
  inp.id = 'new-ext';
  inp.className = 'inp-sm';
  inp.placeholder = '.pdf ou pdf';
  inp.autocomplete = 'off';
  inp.addEventListener('keydown', ev => { if (ev.key === 'Enter') addExt(name); });
  const btnAdd = document.createElement('button');
  btnAdd.className = 'btn btn-sm btn-primary';
  btnAdd.textContent = '+ Ajouter';
  btnAdd.onclick = () => addExt(name);
  row.appendChild(inp);
  row.appendChild(btnAdd);
  body.appendChild(row);

  if (!exts.length) {
    const p = document.createElement('p');
    p.className = 'empty-hint';
    p.textContent = 'Aucune extension associée.';
    body.appendChild(p);
  }
}

// ── Category ops ──────────────────────────────────────────────
async function newCat() {
  const nom = await modal('Nom du nouveau dossier', '', 'ex. Factures, Projets…');
  if (!nom) return;
  try {
    const d = await apiPost('/api/dossier/ajouter', {nom});
    if (d.error) { alert(d.error); return; }
    S.sel = nom; applyConfig(d);
  } catch(e) { alert('Erreur : ' + e.message); }
}

async function renameCat(ancien) {
  const nouveau = await modal('Renommer « ' + ancien + ' »', ancien, '');
  if (!nouveau || nouveau === ancien) return;
  try {
    const d = await apiPost('/api/dossier/renommer', {ancien, nouveau});
    if (d.error) { alert(d.error); return; }
    S.sel = nouveau; applyConfig(d);
  } catch(e) { alert('Erreur : ' + e.message); }
}

async function deleteCat(nom) {
  if (!confirm('Supprimer « ' + nom + ' » ?\nSes extensions seront réassignées à « ' + S.autres + ' ».')) return;
  try {
    const d = await apiPost('/api/dossier/supprimer', {nom});
    if (d.error) { alert(d.error); return; }
    S.sel = null;
    document.getElementById('r-hdr').innerHTML = '<h2 style="color:var(--text3);font-weight:400">Sélectionnez une catégorie</h2>';
    document.getElementById('r-body').innerHTML = '<p class="placeholder">← Choisissez une catégorie dans la liste</p>';
    applyConfig(d);
  } catch(e) { alert('Erreur : ' + e.message); }
}

// ── Extension ops ─────────────────────────────────────────────
async function addExt(dossier) {
  const inp = document.getElementById('new-ext');
  const ext = (inp ? inp.value : '').trim();
  if (!ext) return;
  try {
    const d = await apiPost('/api/extension/ajouter', {ext, dossier});
    if (d.error) { alert(d.error); return; }
    applyConfig(d);
  } catch(e) { alert('Erreur : ' + e.message); }
}

async function removeExt(ext, dossier) {
  try {
    const d = await apiPost('/api/extension/retirer', {ext, dossier});
    if (d.error) { alert(d.error); return; }
    applyConfig(d);
  } catch(e) { alert('Erreur : ' + e.message); }
}

// ── Organise ──────────────────────────────────────────────────
async function runOrg(sim) {
  const dossier = document.getElementById('folder').value.trim();
  if (!dossier) { alert('Veuillez d\'abord choisir un dossier avec le bouton « Choisir… ».'); return; }
  if (!sim && !confirm('Déplacer les fichiers dans :\n' + dossier + '\n\nContinuer ?')) return;

  const logEl = document.getElementById('log');
  logEl.innerHTML = '';
  logLine('── ' + (sim ? 'APERÇU (simulation)' : 'ORGANISATION') + ' ──', 'lh');
  logLine('Dossier : ' + dossier, 'lh');
  logLine('', '');

  try {
    const d = await apiPost('/api/executer', {
      dossier,
      simulation: sim,
      inclure_caches: document.getElementById('hidden-cb').checked,
    });
    if (d.error) { logLine('Erreur : ' + d.error, 'le'); return; }
    d.lignes.forEach(line => {
      const cls = line.includes('✓') ? 'lk' : line.includes('→') ? 'la' : line.includes('⊘') ? 'li' : '';
      logLine(line, cls);
    });
    logLine('', '');
    if (d.deplaces === 0) {
      logLine('── Aucun fichier à classer. ──', 'lc');
    } else {
      const v = sim ? 'seraient classés' : 'classés';
      logLine('── ' + d.deplaces + ' fichier(s) ' + v + (d.ignores ? ', ' + d.ignores + ' ignoré(s)' : '') + ' ──', 'lc');
      if (!sim) alert(d.deplaces + ' fichier(s) organisé(s).');
    }
  } catch(e) {
    logLine('Erreur réseau : ' + e.message, 'le');
  }
  document.getElementById('log').scrollTop = 999999;
}

function logLine(text, cls) {
  const el = document.getElementById('log');
  const sp = document.createElement('span');
  if (cls) sp.className = cls;
  sp.textContent = text + '\n';
  el.appendChild(sp);
}

function clearLog() { document.getElementById('log').innerHTML = ''; }

// ── Folder picker ─────────────────────────────────────────────
let fpResolve = null;
let fpCurrent = '';

async function browse() {
  const cur = document.getElementById('folder').value.trim();
  const result = await openFolderPicker(cur);
  if (result) document.getElementById('folder').value = result;
}

function openFolderPicker(startPath) {
  return new Promise(async resolve => {
    fpResolve = resolve;
    document.getElementById('overlay-fp').classList.remove('hidden');
    await fpLoad(startPath || '/Users');
  });
}

async function fpLoad(path) {
  const listEl = document.getElementById('fp-list');
  listEl.innerHTML = '<div class="fp-empty">Chargement…</div>';
  try {
    const d = await apiGet('/api/ls?path=' + encodeURIComponent(path));
    if (d.error) {
      listEl.innerHTML = '<div class="fp-empty" style="color:var(--danger)">' + esc(d.error) + '</div>';
      return;
    }
    fpCurrent = d.path;
    document.getElementById('fp-cur').textContent = d.path;

    // Breadcrumb — DOM pur, pas de onclick dans innerHTML
    const crumb = document.getElementById('fp-crumb');
    crumb.innerHTML = '';
    const rootBtn = document.createElement('span');
    rootBtn.className = 'fp-bc';
    rootBtn.textContent = '🖥 /';
    rootBtn.onclick = () => fpLoad('/');
    crumb.appendChild(rootBtn);
    let acc = '';
    d.path.split('/').filter(Boolean).forEach(part => {
      acc += '/' + part;
      const sep = document.createElement('span');
      sep.className = 'fp-sep';
      sep.textContent = '›';
      crumb.appendChild(sep);
      const btn = document.createElement('span');
      btn.className = 'fp-bc';
      btn.textContent = part;
      const p = acc;
      btn.onclick = () => fpLoad(p);
      crumb.appendChild(btn);
    });

    // Liste — DOM pur
    listEl.innerHTML = '';
    if (!d.is_root) {
      const up = document.createElement('div');
      up.className = 'fp-item';
      up.innerHTML = '<span>⬆</span><span style="color:var(--text2)">Dossier parent</span>';
      up.onclick = () => fpLoad(d.parent);
      listEl.appendChild(up);
    }
    if (!d.dirs.length) {
      const empty = document.createElement('div');
      empty.className = 'fp-empty';
      empty.textContent = 'Aucun sous-dossier';
      listEl.appendChild(empty);
    } else {
      d.dirs.forEach(name => {
        const full = d.path.replace(/\/$/, '') + '/' + name;
        const item = document.createElement('div');
        item.className = 'fp-item';
        item.innerHTML = '<span>📁</span><span>' + esc(name) + '</span>';
        item.onclick = () => fpLoad(full);
        listEl.appendChild(item);
      });
    }
  } catch(e) {
    listEl.innerHTML = '<div class="fp-empty" style="color:var(--danger)">Erreur : ' + esc(e.message) + '</div>';
  }
}

function fpSelect() {
  document.getElementById('overlay-fp').classList.add('hidden');
  if (fpResolve) { fpResolve(fpCurrent); fpResolve = null; }
}

function fpCancel() {
  document.getElementById('overlay-fp').classList.add('hidden');
  if (fpResolve) { fpResolve(null); fpResolve = null; }
}

document.getElementById('overlay-fp').addEventListener('click', e => { if (e.target === e.currentTarget) fpCancel(); });

// ── Text input modal ──────────────────────────────────────────
let mResolve = null;

function modal(title, def, ph) {
  return new Promise(resolve => {
    document.getElementById('m-title').textContent = title;
    const inp = document.getElementById('m-inp');
    inp.value = def || ''; inp.placeholder = ph || '';
    document.getElementById('overlay-text').classList.remove('hidden');
    inp.focus(); inp.select();
    mResolve = resolve;
    inp.onkeydown = e => { if (e.key === 'Enter') mOk(); if (e.key === 'Escape') mCancel(); };
  });
}
function mOk() {
  const v = document.getElementById('m-inp').value.trim();
  document.getElementById('overlay-text').classList.add('hidden');
  if (mResolve) { mResolve(v || null); mResolve = null; }
}
function mCancel() {
  document.getElementById('overlay-text').classList.add('hidden');
  if (mResolve) { mResolve(null); mResolve = null; }
}
document.getElementById('overlay-text').addEventListener('click', e => { if (e.target === e.currentTarget) mCancel(); });

// ── Util ──────────────────────────────────────────────────────
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function jq(s) { return JSON.stringify(String(s)); }
// jqattr : JSON pour usage dans un attribut HTML (guillemets échappés en &quot;)
function jqattr(s) { return JSON.stringify(String(s)).replace(/"/g, '&quot;'); }

init();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html: str):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def config_response(self):
        cats, autres = get_state()
        self.send_json(build_config_payload(cats, autres))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self.send_html(HTML_APP)
            return

        if path == "/api/config":
            cats, autres = get_state()
            payload = build_config_payload(cats, autres)
            payload["dossier_cible"] = str(dossier_telechargements())
            self.send_json(payload)
            return

        if path == "/api/ls":
            raw = parse_qs(parsed.query).get("path", [""])[0].strip()
            try:
                target = Path(raw).expanduser().resolve() if raw else Path.home()
                dirs: list[str] = []
                for e in target.iterdir():
                    try:
                        if e.is_dir() and not e.name.startswith("."):
                            dirs.append(e.name)
                    except OSError:
                        pass
                dirs.sort(key=str.lower)
                self.send_json({
                    "path": str(target),
                    "parent": str(target.parent),
                    "is_root": target == target.parent,
                    "dirs": dirs,
                })
            except PermissionError:
                self.send_json({"error": "Accès refusé : " + raw}, 403)
            except Exception as e:
                self.send_json({"error": str(e)}, 400)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = self.read_json()
        except Exception:
            self.send_json({"error": "Corps JSON invalide"}, 400)
            return

        cats, autres = get_state()

        try:
            if path == "/api/executer":
                dossier_str = data.get("dossier", "").strip()
                if not dossier_str:
                    self.send_json({"error": "Dossier requis"}, 400)
                    return
                dossier = Path(dossier_str).expanduser().resolve()
                simulation = bool(data.get("simulation", True))
                inclure_caches = bool(data.get("inclure_caches", False))
                lignes: list[str] = []
                deplaces, ignores = organiser(
                    dossier, cats, autres,
                    simulation=simulation,
                    inclure_caches=inclure_caches,
                    journal=lignes.append,
                )
                self.send_json({"lignes": lignes, "deplaces": deplaces, "ignores": ignores})
                return

            if path == "/api/dossier/ajouter":
                nom = (data.get("nom") or "").strip()
                if not nom:
                    self.send_json({"error": "Nom requis"}, 400)
                    return
                pd = categories_par_dossier(cats)
                if nom in pd or nom == autres:
                    self.send_json({"error": f"La catégorie « {nom} » existe déjà."}, 400)
                    return
                ext_raw = (data.get("ext") or "").strip()
                if ext_raw:
                    ext_n = normaliser_extension(ext_raw)
                    if ext_n:
                        cats[ext_n] = nom
                set_state(cats, autres)
                self.config_response()
                return

            if path == "/api/dossier/renommer":
                ancien = (data.get("ancien") or "").strip()
                nouveau = (data.get("nouveau") or "").strip()
                if not nouveau:
                    self.send_json({"error": "Nouveau nom requis"}, 400)
                    return
                pd = categories_par_dossier(cats)
                if nouveau in pd and nouveau != ancien:
                    self.send_json({"error": f"La catégorie « {nouveau} » existe déjà."}, 400)
                    return
                if ancien == autres:
                    autres = nouveau
                else:
                    cats = {e: (nouveau if d == ancien else d) for e, d in cats.items()}
                set_state(cats, autres)
                self.config_response()
                return

            if path == "/api/dossier/supprimer":
                nom = (data.get("nom") or "").strip()
                if nom == autres:
                    self.send_json({"error": "Le dossier par défaut ne peut pas être supprimé."}, 400)
                    return
                cats = {e: (autres if d == nom else d) for e, d in cats.items()}
                set_state(cats, autres)
                self.config_response()
                return

            if path == "/api/extension/ajouter":
                ext_n = normaliser_extension(data.get("ext", ""))
                dossier = (data.get("dossier") or "").strip()
                if not ext_n or not dossier:
                    self.send_json({"error": "Extension et dossier requis"}, 400)
                    return
                cats[ext_n] = dossier
                set_state(cats, autres)
                self.config_response()
                return

            if path == "/api/extension/retirer":
                ext_n = normaliser_extension(data.get("ext", ""))
                dossier_cible = (data.get("dossier") or "").strip()
                if ext_n in cats and cats.get(ext_n) == dossier_cible:
                    del cats[ext_n]
                    set_state(cats, autres)
                self.config_response()
                return

        except NotADirectoryError as e:
            self.send_json({"error": str(e)})
            return
        except PermissionError as e:
            self.send_json({"error": "Permission refusée : " + str(e)})
            return
        except Exception as e:
            self.send_json({"error": "Erreur serveur : " + str(e)})
            return

        self.send_response(404)
        self.end_headers()


def find_free_port(start: int = 8765) -> int:
    import socket
    for port in range(start, start + 40):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start


def main() -> None:
    port = find_free_port()
    server = HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"   # IPv4 explicite — localhost peut résoudre en ::1
    print(f"\n  Organiseur de fichiers  —  {url}")
    print("  Appuyez sur Ctrl+C pour quitter.\n")
    threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Arrêt.")


if __name__ == "__main__":
    main()
