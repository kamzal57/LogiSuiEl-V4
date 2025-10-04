# LogiSuiEl-V4

Application de gestion scolaire complète pour enseignants et établissements scolaires.

## 📋 Description

LogiSuiEl est une application web moderne de gestion scolaire qui permet aux enseignants et administrateurs de gérer efficacement:

- **Élèves**: Gestion complète avec import CSV
- **Compétences**: Référentiel de compétences avec import CSV
- **Évaluations**: Notes et compétences par période
- **Emploi du temps**: Gestion avec import ICS
- **Vie scolaire**: Absences, retards, incidents, punitions
- **Plan de classe**: Placement interactif des élèves
- **Protocoles**: PAI, PAP et autres protocoles spéciaux
- **Dashboard**: Vue d'ensemble avec rappels et événements

## 🏗️ Architecture

Le projet est organisé en deux parties principales:

### Backend (FastAPI)
- API REST avec FastAPI
- Base de données SQLite (migration PostgreSQL possible)
- Authentification JWT avec rôles (Admin, Professeur)
- Import CSV et ICS
- Documentation API automatique

### Frontend (React + TypeScript)
- Interface moderne avec Material-UI
- React Router pour la navigation
- React Query pour la gestion d'état
- Support multilingue (i18next)
- Mode "Classe" pour masquer informations sensibles

## 🚀 Installation

### Prérequis
- Python 3.8+
- Node.js 18+
- npm ou yarn

### Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python -m app.seed

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible à http://localhost:8000
- Documentation API: http://localhost:8000/api/v1/docs

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer l'application en mode développement
npm run dev
```

L'application sera accessible à http://localhost:3000

## 👤 Comptes par défaut

Après l'initialisation de la base de données:

- **Administrateur**: `admin` / `admin`
- **Professeur**: `test` / `test`

⚠️ **Important**: Changez ces mots de passe en production!

## 📚 Fonctionnalités principales

### Tableau de bord
- Emploi du temps de la semaine (40%)
- Pense-bête et agenda personnel (30%)
- Rappels: retenues, appels, rendez-vous (30%)
- Bouton "Mode Classe" pour projection

### Gestion des élèves
- Liste complète avec recherche et filtres
- Fiche individuelle avec toutes les informations
- Import CSV massif
- Export des données

### Plan de classe interactif
- Placement visuel des élèves
- Clic sur un élève pour saisir:
  - Retards, absences, bavardages
  - Comportements négatifs ou positifs
  - Oublis, manque de travail
  - Participation positive

### Évaluations
- **Compétences**: Évaluation par compétences
- **Notes**: Gestion des notes classiques
- **Bilans**: Bilans périodiques (trimestres)

### Vie scolaire
- **Absences**: Suivi et justification
- **Retards**: Enregistrement avec durée
- **Incidents**: Typologie et résolution
- **Punitions**: Gestion et suivi
- **Exclusions**: Historique

### Protocoles
- Liste des élèves avec PAI, PAP, etc.
- Actions à entreprendre pour chaque protocole
- Suivi de l'application

### Configuration
- Informations personnelles
- Paramètres de l'établissement
- Import CSV (élèves et compétences)
- Import ICS (emploi du temps via URL)
- Périodes (trimestres, dates)
- Année scolaire, vacances, jours fériés
- Style et apparence
- Modes "Classe" et "Hors classe"
- Sécurité (identifiants)

## 📁 Format des fichiers d'import

### CSV Élèves
```csv
first_name,last_name,class_name,student_id,email,date_of_birth,parent_name,parent_email,parent_phone
Jean,Dupont,6ème A,STU001,jean@example.com,2010-05-15,M. Dupont,parent@example.com,0612345678
```

### CSV Compétences
```csv
code,name,description,category,level
MATH-01,Résoudre des problèmes,Résoudre des problèmes simples,Mathématiques,1
FR-01,Lire et comprendre,Lire et comprendre un texte,Français,1
```

### Import ICS
Fournir l'URL directe vers un fichier .ics (iCalendar):
```
https://example.com/calendrier/emploi_du_temps.ics
```

## 🔒 Sécurité

- Authentification JWT avec refresh tokens
- Rôles et permissions (Admin / Professeur)
- CORS configuré
- Protection des routes sensibles
- Hachage des mots de passe avec bcrypt

**Pour la production**:
- Changez `SECRET_KEY` dans `backend/app/core/config.py`
- Utilisez HTTPS
- Configurez correctement CORS
- Utilisez PostgreSQL au lieu de SQLite
- Activez les logs et monitoring

## 🛠️ Technologies utilisées

### Backend
- FastAPI - Framework web moderne
- SQLAlchemy - ORM pour base de données
- Pydantic - Validation de données
- JWT - Authentification
- Python-Jose - Tokens JWT
- Passlib - Hachage de mots de passe
- ICS - Parsing de fichiers iCalendar

### Frontend
- React 18 - Framework UI
- TypeScript - Typage statique
- Material-UI - Composants UI
- React Router - Navigation
- React Query - Gestion d'état serveur
- Axios - Client HTTP
- i18next - Internationalisation
- Vite - Build tool

## 📖 Documentation API

Une fois le backend lancé, consultez la documentation interactive:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 🧪 Développement

### Structure du projet
```
LogiSuiEl-V4/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints API
│   │   ├── core/         # Configuration et sécurité
│   │   ├── models/       # Modèles SQLAlchemy
│   │   ├── schemas/      # Schémas Pydantic
│   │   ├── services/     # Services métier
│   │   ├── main.py       # Point d'entrée FastAPI
│   │   └── seed.py       # Initialisation BDD
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # Client API
│   │   ├── components/   # Composants réutilisables
│   │   ├── context/      # Contexts React
│   │   ├── layout/       # Composants de layout
│   │   ├── views/        # Pages/vues
│   │   ├── theme/        # Thème Material-UI
│   │   └── App.tsx       # Composant principal
│   └── package.json
└── README.md
```

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

kamzal57

## 🙏 Remerciements

Merci aux enseignants et administrateurs qui ont contribué aux spécifications fonctionnelles de cette application.
