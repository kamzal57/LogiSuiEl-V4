# LogiSuiEl-V4

Application de gestion scolaire complète pour enseignants et administration.

## Description

LogiSuiEl-V4 est une application de gestion scolaire moderne conçue pour faciliter le suivi des élèves, des évaluations, des emplois du temps et des incidents. Elle offre une interface intuitive et des fonctionnalités complètes pour la gestion quotidienne d'une classe ou d'un établissement.

## Fonctionnalités

### Authentification et Sécurité
- Authentification sécurisée avec tokens JWT
- Deux types de comptes : Administrateur et Professeur
- Comptes par défaut : `admin/admin` et `test/test`

### Gestion des Élèves
- CRUD complet pour les élèves
- Import CSV des données élèves
- Informations personnelles et contacts parents
- Historique des incidents et évaluations

### Évaluations
- Gestion des compétences
- Notes et bilans
- Import CSV des compétences
- Suivi par période (trimestres)

### Emploi du Temps
- Import depuis fichiers ICS (calendrier)
- Visualisation hebdomadaire
- Gestion des événements (cours, réunions, retenues)

### Plan de Classe Interactif
- Disposition des élèves dans la classe
- Saisie rapide d'incidents (retards, absences, comportements, participations)

### Tableau de Bord
- Vue d'ensemble de l'emploi du temps
- Pense-bêtes et agenda personnel
- Rappels et événements à venir
- Incidents récents

### Protocoles
- Gestion des PAI, PAP, PPS
- Actions à entreprendre par élève
- Suivi des protocoles actifs

### Exports et Rapports
- Export CSV des élèves, évaluations et incidents
- Génération de rapports personnalisés

### Configuration
- Paramètres de l'établissement
- Configuration de l'année scolaire
- Gestion des périodes (trimestres)
- Personnalisation de l'interface

## Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation du Backend

```bash
# Aller dans le dossier backend
cd backend

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
uvicorn app.main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

La documentation interactive Swagger sera disponible sur `http://localhost:8000/docs`

## Utilisation

### API Endpoints

#### Authentification
- `POST /api/auth/token` - Obtenir un token d'accès
- `GET /api/auth/me` - Obtenir les informations de l'utilisateur courant
- `POST /api/auth/refresh` - Rafraîchir le token

#### Élèves
- `GET /api/students/` - Lister les élèves
- `POST /api/students/` - Créer un élève
- `GET /api/students/{id}` - Obtenir un élève
- `PUT /api/students/{id}` - Modifier un élève
- `DELETE /api/students/{id}` - Supprimer un élève
- `POST /api/students/import` - Importer des élèves depuis CSV

#### Emploi du Temps
- `GET /api/schedule/` - Lister les événements
- `POST /api/schedule/` - Créer un événement
- `POST /api/schedule/import-ics` - Importer depuis ICS

#### Évaluations
- `GET /api/evaluations/competences` - Lister les compétences
- `POST /api/evaluations/competences` - Créer une compétence
- `POST /api/evaluations/competences/import` - Importer des compétences CSV
- `GET /api/evaluations/` - Lister les évaluations
- `POST /api/evaluations/` - Créer une évaluation

#### Tableau de Bord
- `GET /api/dashboard/` - Obtenir les données du tableau de bord

#### Plan de Classe
- `GET /api/seating/` - Lister les positions des élèves
- `POST /api/seating/` - Assigner une position

#### Protocoles
- `GET /api/protocols/` - Lister les protocoles
- `POST /api/protocols/` - Créer un protocole

#### Configuration
- `GET /api/config/` - Lister les configurations
- `GET /api/config/{key}` - Obtenir une configuration
- `POST /api/config/` - Créer une configuration (Admin)
- `PUT /api/config/{key}` - Modifier une configuration (Admin)

#### Rappels
- `GET /api/reminders/` - Lister les rappels
- `POST /api/reminders/` - Créer un rappel
- `PUT /api/reminders/{id}` - Modifier un rappel

#### Rapports
- `GET /api/reports/students/csv` - Export CSV des élèves
- `GET /api/reports/evaluations/csv` - Export CSV des évaluations
- `GET /api/reports/incidents/csv` - Export CSV des incidents

## Structure du Projet

```
backend/
├── app/
│   ├── api/                 # Routes API
│   │   ├── auth.py
│   │   ├── students.py
│   │   ├── schedule.py
│   │   ├── dashboard.py
│   │   ├── seating.py
│   │   ├── protocols.py
│   │   ├── config.py
│   │   ├── evaluations.py
│   │   ├── reminders.py
│   │   └── reports.py
│   ├── core/                # Configuration et sécurité
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── services/            # Services métier
│   │   ├── bootstrap.py
│   │   ├── csv_import.py
│   │   └── ics_import.py
│   ├── models.py            # Modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   └── main.py              # Application FastAPI
├── tests/
│   └── test_auth.py         # Tests d'authentification
├── requirements.txt
└── pytest.ini
```

## Format des Fichiers CSV

### Élèves (students.csv)
```csv
first_name,last_name,class_name,email,parent_contact,date_of_birth
Jean,Dupont,6A,jean.dupont@ecole.fr,0601020304,2012-05-15
Marie,Martin,6A,marie.martin@ecole.fr,0605060708,2012-08-22
```

### Compétences (competences.csv)
```csv
code,name,description,category
C1.1,Comprendre un texte,Extraire des informations d'un texte,Français
C1.2,Produire un écrit,Rédiger un texte cohérent,Français
M1.1,Calcul mental,Effectuer des calculs rapides,Mathématiques
```

## Tests

Lancer les tests avec pytest :

```bash
cd backend
pytest
```

Les tests incluent :
- Authentification (login, token, utilisateur courant)
- Health check
- Endpoints principaux

## Technologies Utilisées

- **FastAPI** : Framework web moderne pour Python
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **Pydantic** : Validation des données
- **SQLite** : Base de données (peut être remplacée par PostgreSQL)
- **JWT** : Authentification par tokens
- **bcrypt** : Hachage sécurisé des mots de passe
- **pytest** : Framework de tests

## Sécurité

- Les mots de passe sont hachés avec bcrypt
- Authentification par tokens JWT
- Expiration automatique des tokens
- Contrôle d'accès basé sur les rôles (RBAC)
- CORS configuré pour le frontend

## Prochaines Étapes

- [ ] Développement du frontend React/TypeScript
- [ ] Interface utilisateur intuitive avec Material-UI
- [ ] Mode "Classe" pour masquer les informations sensibles
- [ ] Internationalisation (français/anglais)
- [ ] Widgets optionnels (jeux, annuaire, dictionnaire)
- [ ] Notifications et rappels avancés
- [ ] Génération de lettres types
- [ ] Support QR codes

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

MIT License - voir le fichier LICENSE pour plus de détails.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.