# LogiSuiEl Backend

FastAPI backend for the LogiSuiEl School Management Application.

## Features

- User authentication with JWT tokens
- Role-based access control (Admin, Teacher)
- Student management
- Competence management
- Evaluations and grades
- Incident tracking
- Attendance management
- Timetable/schedule management
- Seating plan
- Protocols (PAI, PAP, etc.)
- CSV import for students and competences
- ICS import for timetables
- Dashboard with overview

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python -m app.seed
```

This will create:
- Admin user: username `admin`, password `admin`
- Teacher user: username `test`, password `test`
- Sample students and competences

## Running the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/api/v1/docs
- Alternative docs: http://localhost:8000/api/v1/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Login
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/auth/preferences` - Get user preferences
- `PUT /api/v1/auth/preferences` - Update user preferences

### Students
- `GET /api/v1/students` - List students
- `POST /api/v1/students` - Create student (Admin only)
- `GET /api/v1/students/{id}` - Get student
- `PUT /api/v1/students/{id}` - Update student (Admin only)
- `DELETE /api/v1/students/{id}` - Delete student (Admin only)
- `POST /api/v1/students/import` - Import from CSV (Admin only)

### Competences
- `GET /api/v1/competences` - List competences
- `POST /api/v1/competences` - Create competence (Admin only)
- `POST /api/v1/competences/import` - Import from CSV (Admin only)

### Schedule
- `GET /api/v1/schedule` - List timetable events
- `POST /api/v1/schedule` - Create event (Admin only)
- `POST /api/v1/schedule/import-ics` - Import from ICS URL (Admin only)

### School Life
- `GET /api/v1/school-life/evaluations` - List evaluations
- `POST /api/v1/school-life/evaluations` - Create evaluation
- `GET /api/v1/school-life/incidents` - List incidents
- `POST /api/v1/school-life/incidents` - Create incident
- `GET /api/v1/school-life/attendance` - List attendance
- `POST /api/v1/school-life/attendance` - Create attendance

### Protocols
- `GET /api/v1/protocols` - List protocols
- `POST /api/v1/protocols` - Create protocol

### Seating
- `GET /api/v1/seating` - Get seating plan
- `POST /api/v1/seating` - Create/update seat

### Dashboard
- `GET /api/v1/dashboard` - Get dashboard data

## CSV Format Examples

### Students CSV
```csv
first_name,last_name,class_name,student_id,email,date_of_birth
Jean,Dupont,6ème A,STU001,jean@example.com,2010-05-15
Marie,Martin,6ème A,STU002,marie@example.com,2010-08-22
```

### Competences CSV
```csv
code,name,description,category,level
MATH-01,Résoudre des problèmes,Résoudre des problèmes simples,Mathématiques,1
FR-01,Lire et comprendre,Lire et comprendre un texte,Français,1
```

## Database

The application uses SQLite by default (file: `logisuiel.db`). To use PostgreSQL or another database, update the `DATABASE_URL` in `app/core/config.py`.

## Security

- Change the `SECRET_KEY` in `app/core/config.py` for production
- Use strong passwords
- Configure CORS origins appropriately
- Use HTTPS in production

## Development

The application uses:
- FastAPI for the web framework
- SQLAlchemy for ORM
- Pydantic for validation
- JWT for authentication
- Passlib for password hashing
