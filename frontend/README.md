# LogiSuiEl Frontend

Interface utilisateur moderne pour l'application de gestion scolaire LogiSuiEl.

## Fonctionnalités

- Interface responsive Material-UI
- Authentification JWT
- Navigation par onglets
- Mode "Classe" pour masquer informations sensibles
- Support multilingue (FR/EN)
- Gestion en temps réel avec React Query

## Installation

```bash
npm install
```

## Développement

```bash
npm run dev
```

L'application sera accessible à http://localhost:3000

## Build de production

```bash
npm run build
```

Les fichiers optimisés seront dans le dossier `dist/`

## Variables d'environnement

Créer un fichier `.env` à la racine:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Structure

- `src/api/` - Client API et types
- `src/components/` - Composants réutilisables
- `src/context/` - Contexts React (Auth, etc.)
- `src/layout/` - Composants de layout (TopBar, TabStrip, etc.)
- `src/views/` - Pages de l'application
- `src/theme/` - Configuration Material-UI

## Pages principales

- `/login` - Page de connexion
- `/dashboard` - Tableau de bord
- `/students` - Gestion des élèves
- `/seating` - Plan de classe
- `/evaluations` - Évaluations (Compétences, Notes, Bilans)
- `/school-life` - Vie scolaire (Absences, Retards, Incidents)
- `/protocols` - Protocoles (PAI, PAP, etc.)
- `/settings` - Configuration

## Technologies

- React 18
- TypeScript
- Material-UI v5
- React Router v6
- React Query (TanStack Query)
- Axios
- i18next
- Vite
