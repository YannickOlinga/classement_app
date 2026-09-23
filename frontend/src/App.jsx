import { useState, useEffect } from 'react'
import './App.css'

function LandingPage({ onNavigate }) {
  return (
    <div className="landing-page">
      {/* HEADER */}
      <header className="header">
        <div className="header-container">
          <div className="logo">
            <span className="logo-icon">⧉</span>
            <span className="logo-text">Organiseur</span>
          </div>
          <nav className="nav">
            <a href="#features" className="nav-link">Fonctionnalités</a>
            <a href="#why" className="nav-link">Pourquoi</a>
          </nav>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-container">
          <h1 className="hero-title">
            Organisez vos fichiers<br />en quelques secondes
          </h1>
          <p className="hero-subtitle">
            Automatisez le tri de vos dossiers. Classifiez par catégorie, gagnez du temps, retrouvez ce que vous cherchez.
          </p>
          <div className="hero-cta">
            <button className="btn btn-primary" onClick={() => onNavigate('organizer')}>
              Commencer maintenant
            </button>
            <button className="btn btn-secondary" onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}>
              Voir comment ça marche
            </button>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="features">
        <div className="features-container">
          <h2 className="section-title">Fonctionnalités</h2>
          <p className="section-subtitle">Tout ce dont vous avez besoin pour organiser vos fichiers</p>
          
          <div className="features-grid">
            <div className="feature">
              <div className="feature-number">01</div>
              <h3 className="feature-title">Sélection simple</h3>
              <p className="feature-text">Choisissez le dossier à organiser en un clic. Aucune configuration complexe.</p>
            </div>
            <div className="feature">
              <div className="feature-number">02</div>
              <h3 className="feature-title">Classification intelligente</h3>
              <p className="feature-text">Les fichiers sont triés automatiquement par type et catégorie.</p>
            </div>
            <div className="feature">
              <div className="feature-number">03</div>
              <h3 className="feature-title">Ultra-rapide</h3>
              <p className="feature-text">Organiser des centaines de fichiers en quelques secondes.</p>
            </div>
            <div className="feature">
              <div className="feature-number">04</div>
              <h3 className="feature-title">Entièrement gratuit</h3>
              <p className="feature-text">Aucune limite, aucun compte requis, zéro frais.</p>
            </div>
            <div className="feature">
              <div className="feature-number">05</div>
              <h3 className="feature-title">Local et sécurisé</h3>
              <p className="feature-text">Vos fichiers ne quittent jamais votre ordinateur.</p>
            </div>
            <div className="feature">
              <div className="feature-number">06</div>
              <h3 className="feature-title">Personnalisable</h3>
              <p className="feature-text">Créez vos propres catégories et règles de classification.</p>
            </div>
          </div>
        </div>
      </section>

      {/* WHY SECTION */}
      <section id="why" className="why">
        <div className="why-container">
          <h2 className="section-title">Pourquoi utiliser Organiseur ?</h2>
          <div className="benefits">
            <div className="benefit">
              <div className="benefit-icon">✓</div>
              <h3>Gain de temps</h3>
              <p>Arrêtez le tri manuel. Automatisez en quelques clics.</p>
            </div>
            <div className="benefit">
              <div className="benefit-icon">✓</div>
              <h3>Productivité accrue</h3>
              <p>Retrouvez vos fichiers instantanément, sans fouiller.</p>
            </div>
            <div className="benefit">
              <div className="benefit-icon">✓</div>
              <h3>Espace disque optimisé</h3>
              <p>Mieux organisé = plus facile de nettoyer les doublons.</p>
            </div>
          </div>
        </div>
      </section>

      {/* SOCIAL PROOF SECTION */}
      <section className="social-proof">
        <div className="social-proof-container">
          <p className="social-proof-title">Utilisé par des milliers d'utilisateurs</p>
          <div className="stats">
            <div className="stat">
              <span className="stat-number">50K+</span>
              <span className="stat-label">Fichiers organisés</span>
            </div>
            <div className="stat">
              <span className="stat-number">1K+</span>
              <span className="stat-label">Utilisateurs actifs</span>
            </div>
            <div className="stat">
              <span className="stat-number">100%</span>
              <span className="stat-label">Gratuit</span>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-content">
            <div className="footer-section">
              <h4>Organiseur</h4>
              <p>Organisez vos fichiers automatiquement.</p>
            </div>
            <div className="footer-section">
              <h4>Liens</h4>
              <ul className="footer-links">
                <li><a href="#features">Fonctionnalités</a></li>
                <li><a href="#why">À propos</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Légal</h4>
              <ul className="footer-links">
                <li><a href="#">Conditions d'utilisation</a></li>
                <li><a href="#">Politique de confidentialité</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2026 Organiseur. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function OrganizerPage({ onNavigate }) {
  const [config, setConfig] = useState(null)
  const [loading, setLoading] = useState(true)
  const [organizing, setOrganizing] = useState(false)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('categories')
  const [selectedFolder, setSelectedFolder] = useState('~/Downloads')
  const [suggestions] = useState([
    { label: 'Téléchargements', path: '~/Downloads' },
    { label: 'Bureau', path: '~/Desktop' },
    { label: 'Documents', path: '~/Documents' },
    { label: 'Images', path: '~/Pictures' },
    { label: 'Musique', path: '~/Music' },
  ])

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/config')
      if (!response.ok) throw new Error('Erreur lors du chargement')
      const data = await response.json()
      setConfig(data)
      setError(null)
    } catch (err) {
      setError(err.message)
      console.error('Error fetching config:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFolderChange = (e) => {
    setSelectedFolder(e.target.value)
  }

  const selectFolder = (path) => {
    setSelectedFolder(path)
  }

  const handleOrganize = async () => {
    if (!selectedFolder) {
      setError('Veuillez sélectionner un dossier')
      return
    }

    try {
      setOrganizing(true)
      const payload = {
        dossier: selectedFolder
      }
      const response = await fetch('/api/organiser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Erreur lors de l\'organisation')
      }
      const data = await response.json()
      setConfig(data.config)
      alert(`✅ ${data.message}`)
      setError(null)
    } catch (err) {
      setError(err.message)
      console.error('Error organizing:', err)
    } finally {
      setOrganizing(false)
    }
  }

  return (
    <div className="app-layout">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <button className="btn-back" onClick={() => onNavigate('landing')}>
            ← Retour
          </button>
          <h1>Organiseur</h1>
          <p>Classifiez vos fichiers</p>
        </div>

        {loading ? (
          <div className="sidebar-content">
            <div className="loading-spinner">Chargement...</div>
          </div>
        ) : error && !config ? (
          <div className="sidebar-content">
            <div className="error-message">
              <strong>Erreur</strong>
              <p>{error}</p>
              <button onClick={() => setError(null)}>Fermer</button>
            </div>
          </div>
        ) : config ? (
          <div className="sidebar-content">
            <div className="stats">
              <div className="stat-item">
                <span className="stat-label">Catégories</span>
                <span className="stat-value">{Object.keys(config.categories).length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Dossiers</span>
                <span className="stat-value">{Object.keys(config.par_dossier).length}</span>
              </div>
            </div>

            {/* FOLDER PICKER */}
            <div className="folder-section">
              <label className="folder-label">
                Choisir un dossier:
              </label>
              
              <div className="folder-suggestions">
                {suggestions.map((suggestion) => (
                  <button
                    key={suggestion.path}
                    className={`suggestion-btn ${selectedFolder === suggestion.path ? 'active' : ''}`}
                    onClick={() => selectFolder(suggestion.path)}
                  >
                    {suggestion.label}
                  </button>
                ))}
              </div>

              <div className="folder-input-container">
                <label htmlFor="folder-input" className="folder-input-label">Ou entrez un chemin personnalisé:</label>
                <input
                  id="folder-input"
                  type="text"
                  placeholder="~/Downloads, ~/Desktop, /Users/username/Folder..."
                  value={selectedFolder}
                  onChange={handleFolderChange}
                  className="folder-input"
                />
              </div>

              {selectedFolder && (
                <div className="folder-selected">
                  ✓ {selectedFolder}
                </div>
              )}
            </div>

            <div className="tabs">
              <button 
                className={`tab ${activeTab === 'categories' ? 'active' : ''}`}
                onClick={() => setActiveTab('categories')}
              >
                Catégories
              </button>
              <button 
                className={`tab ${activeTab === 'folders' ? 'active' : ''}`}
                onClick={() => setActiveTab('folders')}
              >
                Dossiers
              </button>
            </div>

            {error && (
              <div className="error-message-compact">
                <strong>⚠️ Erreur</strong>
                <p>{error}</p>
              </div>
            )}

            <button
              className="btn-organize"
              onClick={handleOrganize}
              disabled={organizing || !selectedFolder}
            >
              {organizing ? 'En cours...' : 'Organiser'}
            </button>
          </div>
        ) : null}
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        {config && !loading && !error ? (
          <>
            {activeTab === 'categories' && (
              <section>
                <h2>Catégories de fichiers</h2>
                <div className="items-grid">
                  {Object.entries(config.categories).map(([ext, cat]) => (
                    <div key={ext} className="item-card">
                      <div className="item-ext">{ext}</div>
                      <div className="item-cat">{cat}</div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {activeTab === 'folders' && (
              <section>
                <h2>Dossiers d'organisation</h2>
                <div className="items-grid">
                  {Object.entries(config.par_dossier).map(([folder, files]) => (
                    <div key={folder} className="item-card">
                      <div className="item-title">{folder}</div>
                      <div className="item-count">{files.length} type{files.length > 1 ? 's' : ''}</div>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        ) : null}
      </main>
    </div>
  )
}

export default function App() {
  const [currentPage, setCurrentPage] = useState('landing')

  return currentPage === 'landing' ? (
    <LandingPage onNavigate={setCurrentPage} />
  ) : (
    <OrganizerPage onNavigate={setCurrentPage} />
  )
}
