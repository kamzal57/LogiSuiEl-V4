# LogiSuiEl-V4

School Management Application - A comprehensive solution for teachers and school administrators.

## Overview

LogiSuiEl is a modern school management application built with FastAPI (backend) and React + TypeScript (frontend). It provides tools for managing students, schedules, evaluations, school life events, and protocols.

## Features

### Authentication
- Secure JWT-based authentication
- Two user roles: Admin and Teacher
- Default accounts:
  - Admin: `admin` / `admin`
  - Teacher: `test` / `test`

### Dashboard
- Weekly schedule overview (40%)
- Personal reminders, notes, and agenda (30%)
- Incidents, detentions, and appointments tracking (30%)
- "Class Mode" toggle to hide sensitive information during projection

### Seating Plan
- Interactive classroom seating arrangement
- Click on students to record:
  - Tardiness, absences, talking, behavior issues
  - Forgetfulness, lack of work
  - Positive participation

### Evaluations
- **Skills (Compétences)**: Track student competencies
- **Grades (Notes)**: Manage student grades
- **Reports (Bilans)**: Generate evaluation reports

### School Life
- Absences tracking
- Tardiness management
- Punishments and disciplinary actions
- Exclusions management

### Protocols
- Special protocols (PAI, etc.)
- List of students requiring specific actions
- Protocol details and action items

### Settings
- Personal information
- School information
- CSV import (students, competencies)
- ICS import (schedule from URL)
- Period configuration (trimesters, dates)
- Academic year, holidays, school days
- Appearance customization
- Security settings

### Additional Features
- Multi-language support (French/English)
- Data import/export (CSV)
- ICS calendar import from URL
- Letter templates
- Notes and personal documentation

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Async ORM with SQLite
- **JWT**: Secure token-based authentication
- **Pydantic**: Data validation
- **httpx**: Async HTTP client for ICS import

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **Material-UI (MUI)**: Component library
- **React Query**: Data fetching and caching
- **React Router**: Navigation
- **i18next**: Internationalization
- **Axios**: HTTP client

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

The backend will start at `http://localhost:8000`

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev
```

The frontend will start at `http://localhost:5173`

### Build for Production

```bash
cd frontend
npm run build
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## API Endpoints

### Authentication
- `POST /auth/token` - Login with username/password
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user profile

### Students
- `GET /students` - List all students
- `POST /students` - Create new student
- `POST /students/import` - Import students from CSV
- `POST /students/{id}/notes` - Add notes for a student
- `POST /students/{id}/behaviours` - Record student behaviors

### Schedule
- `GET /schedule` - Get timetable events
- `POST /schedule/import-ics` - Import schedule from ICS URL

### Dashboard
- `GET /dashboard` - Get dashboard data (schedule, reminders, incidents)

### Seating Plan
- `GET /seating-plan` - Get current seating arrangement
- `POST /seating-plan` - Update seating positions

### Protocols
- `GET /protocols` - List all protocols
- `POST /protocols` - Create new protocol

### Configuration
- `GET /config` - Get application configuration
- `PUT /config` - Update configuration

### Reports
- `GET /reports/{type}` - Export data (CSV/PDF)

### Notifications
- `POST /notifications/test` - Test notification (stub)

## Project Structure

```
LogiSuiEl-V4/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Configuration and security
│   │   ├── services/      # Business logic (CSV/ICS import, bootstrap)
│   │   ├── database.py    # Database connection
│   │   ├── dependencies.py # Dependency injection
│   │   ├── main.py        # FastAPI app
│   │   ├── models.py      # SQLAlchemy models
│   │   └── schemas.py     # Pydantic schemas
│   ├── tests/             # Backend tests
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── api/          # API client and endpoints
│   │   ├── components/   # Reusable components
│   │   ├── context/      # React context (Auth)
│   │   ├── layout/       # Layout components
│   │   ├── locales/      # i18n translations
│   │   ├── theme/        # MUI theme configuration
│   │   ├── types/        # TypeScript types
│   │   ├── views/        # Page components
│   │   ├── App.tsx       # Main app component
│   │   └── main.tsx      # Entry point
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Environment Variables

### Backend
Set these in your environment or create a `.env` file:
- `LOGISUIEL_DATABASE_URL` - Database connection string (default: `sqlite+aiosqlite:///./logisuiel.db`)
- `LOGISUIEL_SECRET_KEY` - JWT secret key
- `LOGISUIEL_BACKEND_CORS_ORIGINS` - Allowed CORS origins (default: `http://localhost:5173`)

### Frontend
Create `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

## Development

### Running both services

Terminal 1 (Backend):
```bash
cd backend
uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.

## Future Enhancements

- [ ] Mobile responsive design improvements
- [ ] Real-time notifications (WebSocket)
- [ ] Advanced data visualization and charts
- [ ] Export to PDF for reports
- [ ] SMS/Email notifications
- [ ] WhatsApp integration for parent communication
- [ ] QR code generation for various use cases
- [ ] Collaborative features for multiple teachers
- [ ] PostgreSQL support for production
- [ ] Docker containerization
- [ ] Advanced search and filtering
- [ ] Audit logging
- [ ] Data backup and restore

## Acknowledgments

Built with modern web technologies and best practices for educational management.
