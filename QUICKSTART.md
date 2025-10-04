# Guide de démarrage rapide - LogiSuiEl V4

## 🚀 Installation rapide

### Prérequis
- Python 3.8 ou supérieur
- Node.js 18 ou supérieur
- npm ou yarn

### Étape 1: Cloner le projet

```bash
git clone https://github.com/kamzal57/LogiSuiEl-V4.git
cd LogiSuiEl-V4
```

### Étape 2: Configuration du Backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données avec les comptes de test
python -m app.seed
```

**Comptes créés automatiquement:**
- Administrateur: `admin` / `admin`
- Professeur: `test` / `test`

### Étape 3: Démarrer le Backend

```bash
# Toujours dans le dossier backend avec venv activé
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le backend est maintenant accessible:
- API: http://localhost:8000
- Documentation: http://localhost:8000/api/v1/docs

### Étape 4: Configuration du Frontend

```bash
# Dans un nouveau terminal, depuis la racine du projet
cd frontend

# Installer les dépendances
npm install

# Démarrer l'application
npm run dev
```

L'application est maintenant accessible à: http://localhost:3000

### Étape 5: Se connecter

1. Ouvrir http://localhost:3000 dans votre navigateur
2. Utiliser les identifiants de test:
   - Admin: `admin` / `admin`
   - Prof: `test` / `test`

## 📊 Importer des données

### Import CSV - Élèves

1. Aller dans **Configuration** > **Import de données**
2. Utiliser le fichier exemple `examples/students_example.csv`
3. Format requis:
   ```csv
   first_name,last_name,class_name,student_id,email,date_of_birth,parent_name,parent_email,parent_phone
   ```

### Import CSV - Compétences

1. Aller dans **Configuration** > **Import de données**
2. Utiliser le fichier exemple `examples/competences_example.csv`
3. Format requis:
   ```csv
   code,name,description,category,level
   ```

### Import ICS - Emploi du temps

1. Aller dans **Configuration** > **Emploi du temps**
2. Entrer l'URL de votre fichier .ics
3. Exemple: `https://example.com/calendrier.ics`

## 🎯 Premières étapes

1. **Créer des élèves** ou importer depuis CSV
2. **Définir des compétences** ou importer depuis CSV
3. **Configurer l'emploi du temps** via import ICS
4. **Créer un plan de classe** dans Plan de classe
5. **Commencer à évaluer** dans Évaluations

## 🔧 Problèmes courants

### Le backend ne démarre pas
- Vérifier que Python 3.8+ est installé: `python --version`
- Vérifier que l'environnement virtuel est activé
- Vérifier que toutes les dépendances sont installées

### Le frontend ne démarre pas
- Vérifier que Node.js 18+ est installé: `node --version`
- Supprimer `node_modules` et refaire `npm install`
- Vérifier que le port 3000 est disponible

### Erreur de connexion API
- Vérifier que le backend tourne sur le port 8000
- Vérifier le fichier `frontend/vite.config.ts` (proxy configuré)

## 📚 Documentation complète

Voir [README.md](../README.md) pour la documentation complète.

## 🆘 Support

En cas de problème, ouvrir une issue sur GitHub.
