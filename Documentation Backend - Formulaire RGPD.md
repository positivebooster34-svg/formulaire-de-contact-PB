# Documentation Backend - Formulaire RGPD

## Vue d'ensemble

Cette application Flask fournit une API backend complète pour traiter les soumissions du formulaire de recueil de coordonnées conforme au RGPD. Elle inclut la validation des données, le stockage sécurisé et la traçabilité des actions pour la conformité RGPD.

## Architecture

### Structure du projet

```
formulaire-backend/
├── venv/                    # Environnement virtuel Python
├── src/
│   ├── models/
│   │   ├── user.py         # Modèle utilisateur (template)
│   │   └── prospect.py     # Modèle prospect avec logs RGPD
│   ├── routes/
│   │   ├── user.py         # Routes utilisateur (template)
│   │   └── prospect.py     # Routes API pour les prospects
│   ├── static/             # Fichiers frontend (HTML, CSS, JS)
│   │   ├── index.html      # Formulaire principal
│   │   ├── style.css       # Styles responsive
│   │   └── script.js       # Logique JavaScript
│   ├── database/
│   │   └── app.db          # Base de données SQLite
│   └── main.py             # Point d'entrée de l'application
└── requirements.txt        # Dépendances Python
```

### Technologies utilisées

- **Flask** : Framework web Python léger et flexible
- **SQLAlchemy** : ORM pour la gestion de base de données
- **Flask-CORS** : Support des requêtes cross-origin
- **SQLite** : Base de données embarquée pour le développement
- **JavaScript** : Validation côté client et communication AJAX

## Modèles de données

### Modèle Prospect

Le modèle `Prospect` stocke toutes les informations des prospects avec une conformité RGPD complète :

**Champs de données :**
- `nom`, `prenom` : Coordonnées de base (String, 50 caractères max)
- `telephone` : Numéro de téléphone (String, 20 caractères max)
- `email` : Adresse email (String, 100 caractères max)
- `preference_contact` : Mode de contact préféré ('mail' ou 'tel')
- `jours_preference` : Jours de préférence pour contact téléphonique (JSON)
- `tranche_horaire` : Créneau horaire préféré ('matin', 'apresmidi', 'soiree')

**Consentements RGPD :**
- `consentement_rgpd` : Consentement obligatoire au traitement (Boolean)
- `consentement_marketing` : Consentement optionnel marketing (Boolean)

**Métadonnées :**
- `date_creation`, `date_modification` : Horodatage automatique
- `ip_address` : Adresse IP de soumission
- `user_agent` : Navigateur utilisé
- `statut` : État du prospect ('nouveau', 'contacte', 'converti', 'supprime')

### Modèle ProspectLog

Le modèle `ProspectLog` assure la traçabilité complète des actions pour la conformité RGPD :

**Champs de traçabilité :**
- `prospect_id` : Référence au prospect concerné
- `action` : Type d'action ('creation', 'modification', 'consultation', 'suppression')
- `details` : Détails de l'action en format JSON
- `date_action` : Horodatage de l'action
- `ip_address`, `user_agent` : Informations de connexion
- `utilisateur` : Identifiant de l'utilisateur ayant effectué l'action

## API Endpoints

### POST /api/prospects
**Créer un nouveau prospect**

Endpoint principal pour traiter les soumissions du formulaire.

**Données attendues :**
```json
{
  "nom": "Martin",
  "prenom": "Pierre", 
  "tel": "06 12 34 56 78",
  "email": "pierre.martin@email.com",
  "preferenceContact": "mail",
  "joursPreference": ["Lundi", "Mardi"],
  "trancheHoraire": "matin",
  "consentementRGPD": true,
  "consentementMarketing": false
}
```

**Validation effectuée :**
- Nom et prénom : 2-50 caractères, lettres uniquement
- Téléphone : Format français valide
- Email : Format valide, maximum 100 caractères
- Consentement RGPD : Obligatoire
- Unicité de l'email

**Réponse de succès (201) :**
```json
{
  "success": true,
  "message": "Prospect créé avec succès",
  "prospect_id": 1
}
```

**Réponse d'erreur (400/409/500) :**
```json
{
  "success": false,
  "message": "Description de l'erreur",
  "errors": ["Liste des erreurs de validation"]
}
```

### GET /api/prospects
**Récupérer la liste des prospects**

Endpoint pour consulter les prospects avec pagination.

**Paramètres optionnels :**
- `page` : Numéro de page (défaut: 1)
- `per_page` : Éléments par page (défaut: 10, max: 100)
- `statut` : Filtrer par statut

**Réponse :**
```json
{
  "success": true,
  "prospects": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### GET /api/prospects/{id}
**Récupérer un prospect spécifique**

Endpoint pour consulter les détails d'un prospect. Enregistre automatiquement l'action de consultation dans les logs.

### PUT /api/prospects/{id}
**Mettre à jour un prospect**

Endpoint pour modifier certains champs d'un prospect (statut, tranche_horaire). Enregistre automatiquement les modifications dans les logs.

### DELETE /api/prospects/{id}
**Supprimer un prospect (RGPD)**

Endpoint pour supprimer définitivement un prospect conformément aux droits RGPD. Enregistre l'action avant suppression.

### GET /api/prospects/{id}/logs
**Consulter l'historique d'un prospect**

Endpoint pour récupérer tous les logs d'actions effectuées sur un prospect spécifique.

## Sécurité et validation

### Validation côté serveur

Toutes les données sont validées côté serveur avec des règles strictes :

**Validation des noms :**
- Longueur : 2 à 50 caractères
- Caractères autorisés : lettres, espaces, tirets, apostrophes
- Expression régulière : `^[a-zA-ZÀ-ÿ\s\-\']+$`

**Validation du téléphone :**
- Format français avec ou sans espaces/tirets
- Expression régulière : `^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$`

**Validation de l'email :**
- Format standard d'adresse email
- Longueur maximum : 100 caractères
- Expression régulière : `^[^\s@]+@[^\s@]+\.[^\s@]+$`

### Gestion des erreurs

L'API gère plusieurs types d'erreurs :

- **400 Bad Request** : Données manquantes ou invalides
- **409 Conflict** : Email déjà existant
- **404 Not Found** : Prospect non trouvé
- **500 Internal Server Error** : Erreur serveur

### Protection des données

**Stockage sécurisé :**
- Emails stockés en minuscules
- Adresses IP et User-Agent enregistrés pour la traçabilité
- Horodatage automatique de toutes les actions

**Méthodes d'anonymisation :**
- Méthode `to_dict_anonymized()` pour les exports
- Masquage partiel des données sensibles

## Conformité RGPD

### Traçabilité complète

Chaque action sur un prospect est automatiquement enregistrée :

- **Création** : Enregistrement des préférences et consentements
- **Consultation** : Traçage des accès aux données
- **Modification** : Historique des changements avec anciennes valeurs
- **Suppression** : Enregistrement avant suppression définitive

### Gestion des consentements

- **Consentement obligatoire** : Traitement des données personnelles
- **Consentement optionnel** : Communications marketing
- **Granularité** : Consentements séparés et spécifiques
- **Révocabilité** : Possibilité de modifier les consentements

### Droits des personnes

L'API facilite l'exercice des droits RGPD :

- **Droit d'accès** : Consultation des données via GET /api/prospects/{id}
- **Droit de rectification** : Modification via PUT /api/prospects/{id}
- **Droit à l'effacement** : Suppression via DELETE /api/prospects/{id}
- **Droit à la portabilité** : Export des données en JSON
- **Historique** : Consultation des logs via GET /api/prospects/{id}/logs

## Installation et déploiement

### Prérequis

- Python 3.11+
- pip (gestionnaire de paquets Python)
- Environnement virtuel recommandé

### Installation locale

1. **Cloner et configurer l'environnement :**
```bash
cd formulaire-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
```

2. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application :**
```bash
python src/main.py
```

L'application sera accessible sur `http://localhost:5000`

### Configuration

**Variables d'environnement recommandées :**
- `SECRET_KEY` : Clé secrète Flask (modifier en production)
- `DATABASE_URL` : URL de base de données (SQLite par défaut)
- `CORS_ORIGINS` : Origines autorisées pour CORS

**Configuration de production :**
- Utiliser PostgreSQL ou MySQL au lieu de SQLite
- Configurer un serveur WSGI (Gunicorn, uWSGI)
- Activer HTTPS pour la sécurité
- Configurer la sauvegarde automatique de la base de données

### Déploiement

**Options de déploiement :**
1. **Serveur traditionnel** : Nginx + Gunicorn
2. **Cloud** : Heroku, AWS, Google Cloud
3. **Conteneurs** : Docker + Kubernetes
4. **Serverless** : AWS Lambda, Vercel

**Checklist de déploiement :**
- [ ] Modifier la `SECRET_KEY` en production
- [ ] Configurer une base de données persistante
- [ ] Activer HTTPS
- [ ] Configurer les sauvegardes
- [ ] Mettre en place la surveillance
- [ ] Tester tous les endpoints
- [ ] Vérifier la conformité RGPD

## Maintenance et monitoring

### Logs et surveillance

**Logs applicatifs :**
- Toutes les actions sont enregistrées dans `ProspectLog`
- Logs Flask pour les requêtes HTTP
- Gestion des erreurs avec stack traces

**Métriques recommandées :**
- Nombre de soumissions par jour
- Taux d'erreur des validations
- Temps de réponse des endpoints
- Utilisation de la base de données

### Sauvegarde et récupération

**Stratégie de sauvegarde :**
- Sauvegarde quotidienne de la base de données
- Rétention des sauvegardes selon la politique RGPD
- Test régulier de la procédure de récupération

**Procédures RGPD :**
- Suppression automatique des données après 3 ans
- Procédure d'export pour la portabilité
- Anonymisation pour les statistiques

### Évolutions futures

**Améliorations possibles :**
- Interface d'administration web
- API de statistiques et reporting
- Intégration avec des CRM
- Notifications par email
- Authentification et autorisation
- Chiffrement des données sensibles
- Audit trail plus détaillé

Cette documentation fournit toutes les informations nécessaires pour comprendre, installer, utiliser et maintenir le backend du formulaire RGPD.

