# Guide d'Installation Rapide - Backend Formulaire RGPD

## Installation en 5 minutes

### 1. Prérequis
- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installation

```bash
# Aller dans le dossier du projet
cd formulaire-backend

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances (déjà fait)
pip install -r requirements.txt

# Lancer l'application
python src/main.py
```

### 3. Accès
- **Application web** : http://localhost:5000
- **API** : http://localhost:5000/api/prospects

### 4. Test rapide

Ouvrez http://localhost:5000 dans votre navigateur et remplissez le formulaire pour tester l'intégration complète.

## Structure des fichiers

```
formulaire-backend/
├── src/
│   ├── main.py              # Point d'entrée
│   ├── models/
│   │   └── prospect.py      # Modèle de données RGPD
│   ├── routes/
│   │   └── prospect.py      # API endpoints
│   └── static/              # Frontend intégré
│       ├── index.html       # Formulaire
│       ├── style.css        # Styles
│       └── script.js        # JavaScript
└── requirements.txt         # Dépendances
```

## API Endpoints principaux

- `POST /api/prospects` - Créer un prospect
- `GET /api/prospects` - Lister les prospects
- `GET /api/prospects/{id}` - Détails d'un prospect
- `DELETE /api/prospects/{id}` - Supprimer (RGPD)

## Configuration de production

Pour déployer en production, modifiez dans `src/main.py` :

```python
# Remplacer
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Par une clé sécurisée
app.config['SECRET_KEY'] = 'votre-cle-secrete-unique'

# Et pour la production
app.run(host='0.0.0.0', port=5000, debug=False)
```

## Support

Pour toute question technique, consultez la documentation complète dans `documentation_backend.md`.

