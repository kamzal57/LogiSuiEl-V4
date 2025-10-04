# LogiSuiEl-V4

## School Management Application

LogiSuiEl is a comprehensive school management system designed for teachers and administrators to manage students, schedules, evaluations, and more.

## Features

### Core Features
- **Dashboard**: Weekly schedule, reminders, and incident tracking
- **Student Management**: Import/export students, track personal information
- **Competencies Management**: Define and track student competencies
- **Evaluations**: Grade students on competencies and subjects
- **Schedule Management**: Import schedules from ICS files
- **Seating Plan**: Interactive classroom seating arrangement
- **Protocols**: Manage PAI, PAP, PPS and other student protocols
- **Incidents Tracking**: Record behavior, absences, participation
- **Reminders**: Personal notes, meetings, parent appointments

### Security
- Role-based access control (Admin/Teacher)
- JWT authentication
- Secure password hashing

### Internationalization
- Multi-language support (French/English)
- Configurable interface

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI
- **Database**: SQLite (upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with OAuth2

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **State Management**: React Query
- **Routing**: React Router

## Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database with seed data:
```bash
python -m app.seed
```

5. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Default Credentials

After running the seed script, you can login with:

- **Admin Account**:
  - Username: `admin`
  - Password: `admin`

- **Teacher Account**:
  - Username: `test`
  - Password: `test`

## Usage

### Importing Students

1. Prepare a CSV file with the following columns:
   - first_name, last_name, date_of_birth, class_name, student_id, email, phone, address, parent_name, parent_email, parent_phone, medical_info

2. See `examples/students.csv` for a sample file

3. Use the API endpoint: `POST /api/students/import`

### Importing Competencies

1. Prepare a CSV file with the following columns:
   - code, name, description, category, level

2. See `examples/competences.csv` for a sample file

3. Use the API endpoint: `POST /api/competences/import`

### Importing Schedule from ICS

1. Get the URL of an ICS calendar file

2. Use the API endpoint: `POST /api/schedule/import-ics?url=<your-ics-url>`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

#### Authentication
- `POST /api/auth/token` - Login
- `GET /api/auth/me` - Get current user
- `GET /api/auth/preferences` - Get user preferences
- `PUT /api/auth/preferences` - Update user preferences

#### Students
- `GET /api/students/` - List students
- `POST /api/students/` - Create student
- `POST /api/students/import` - Import from CSV
- `POST /api/students/{id}/incidents` - Add incident
- `POST /api/students/{id}/evaluations` - Add evaluation

#### Schedule
- `GET /api/schedule/` - Get schedule events
- `POST /api/schedule/` - Create event
- `POST /api/schedule/import-ics` - Import from ICS

#### Dashboard
- `GET /api/dashboard/` - Get dashboard data
- `GET /api/dashboard/reminders` - Get reminders
- `POST /api/dashboard/reminders` - Create reminder

#### Seating Plan
- `GET /api/seating/` - Get seating arrangement
- `POST /api/seating/` - Create/update seat

#### Competencies
- `GET /api/competences/` - List competencies
- `POST /api/competences/` - Create competency
- `POST /api/competences/import` - Import from CSV

#### Protocols
- `GET /api/protocols/` - List protocols
- `POST /api/protocols/` - Create protocol

## Development

### Backend Development

Run with auto-reload:
```bash
uvicorn app.main:app --reload
```

### Frontend Development

Run with hot module replacement:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

## Project Structure

```
LogiSuiEl-V4/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Core configuration
│   │   ├── services/      # Business logic
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── main.py        # FastAPI app
│   │   └── seed.py        # Database seeding
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── context/       # React context
│   │   ├── layout/        # Layout components
│   │   ├── views/         # Page views
│   │   ├── App.tsx        # Main app
│   │   └── main.tsx       # Entry point
│   ├── package.json       # Node dependencies
│   └── vite.config.ts     # Vite configuration
└── examples/              # Sample CSV files
```

## Contributing

This project is under active development. Contributions are welcome!

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.