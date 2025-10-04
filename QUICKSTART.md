# Quick Start Guide - LogiSuiEl

## Getting Started in 5 Minutes

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Step 1: Clone the Repository
```bash
git clone https://github.com/kamzal57/LogiSuiEl-V4.git
cd LogiSuiEl-V4
```

### Step 2: Start the Backend
Open a terminal:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

✅ Backend is running at `http://localhost:8000`
📚 API docs at `http://localhost:8000/docs`

### Step 3: Start the Frontend
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend is running at `http://localhost:5173`

### Step 4: Login
Open your browser to `http://localhost:5173` and login with:
- **Admin**: username `admin`, password `admin`
- **Teacher**: username `test`, password `test`

## What You'll See

### Dashboard
Three-column layout showing:
- Schedule (40%)
- Personal notes and reminders (30%)
- Incidents and appointments (30%)

### Features
- 📋 **Seating Plan**: Interactive classroom layout
- 📊 **Evaluations**: Skills, grades, and reports
- 🏫 **School Life**: Absences, tardiness, punishments
- 📝 **Protocols**: Special protocols (PAI, etc.)
- ⚙️ **Settings**: Configuration and data import

### Navigation
Use the tabs at the top to navigate between sections:
- Tableau de bord (Dashboard)
- Plan de classe (Seating Plan)
- Évaluations (Evaluations)
- Vie scolaire (School Life)
- Protocoles (Protocols)
- Paramètres (Settings)

### Language
Click the globe icon (🌐) in the top right to toggle between French and English.

## Next Steps

1. **Import Data**: Go to Settings → Import/Export to upload CSV files for students and competencies
2. **Import Schedule**: Go to Settings → Schedule Config to import ICS calendar
3. **Configure**: Customize the application in Settings
4. **Explore**: Try clicking on seats in the Seating Plan to record student behaviors

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- API documentation at `http://localhost:8000/docs`
- Open an issue on GitHub for questions

## Production Build

### Frontend
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

### Backend
For production, use a production ASGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Tips

- The application auto-saves your work
- Use "Mode Classe" in the dashboard to hide sensitive info during projection
- Default database is SQLite (file: `logisuiel.db` in backend directory)
- All data is stored locally

Enjoy using LogiSuiEl! 🎓
