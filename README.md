# LogiSuiEl-V4

A comprehensive school management application for teachers with a FastAPI backend and React frontend.

## Screenshots

### Login Page
![Login](https://github.com/user-attachments/assets/28ea999f-16f0-4b8a-954d-dea617f8169b)

### Dashboard
![Dashboard](https://github.com/user-attachments/assets/4a25cc05-e54a-4514-a718-227ba3c0c738)

### Seating Plan
![Seating Plan](https://github.com/user-attachments/assets/a56bb5e4-4883-479a-b6f9-528f3580fd25)

### Settings
![Settings](https://github.com/user-attachments/assets/420aa7fb-f7b0-4d80-9386-65b6e7e97173)

## Features

- **Dashboard**: Three-column layout with timetable, reminders, and incidents
- **Seating Plan**: Interactive seating arrangement with student behavior tracking
- **Evaluations**: Competence-based and traditional grade management
- **School Life**: Absence, late, punishment, and exclusion tracking
- **Protocols**: PAI and other special protocols for students
- **Settings**: School configuration, data import (CSV/ICS), and appearance customization
- **Authentication**: Secure login with admin and teacher roles
- **Internationalization**: French and English language support
- **Class Mode**: Toggle to hide sensitive information during projection

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM with async support)
- SQLite (database, easily upgradeable to PostgreSQL)
- JWT authentication
- CSV and ICS file import support

### Frontend
- React 19 with TypeScript
- Vite (build tool)
- Material-UI (component library)
- React Router (routing)
- React Query (data fetching)
- i18next (internationalization)
- Axios (HTTP client)

## Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env to configure CORS origins for your frontend
# For development with frontend on localhost:5173, no changes needed

# Run the server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# The default API URL is http://localhost:8000
# Edit .env if your backend is running on a different URL

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Default Credentials

Two default accounts are created automatically on first startup:

- **Admin Account**: 
  - Username: `admin` 
  - Password: `admin`
  - Full access to all features
  
- **Teacher Account**: 
  - Username: `test` 
  - Password: `test`
  - Standard teacher permissions

⚠️ **Security Note**: Change these default passwords in production!

## Quick Start

1. **Start the backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn app.main:app --reload
   ```

2. **Start the frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```

3. **Open your browser** to `http://localhost:5173`

4. **Login** with `admin/admin` or `test/test`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
LogiSuiEl-V4/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration and security
│   │   ├── services/     # Business logic
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI application
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── context/      # React contexts
│   │   ├── layout/       # Layout components
│   │   ├── views/        # Page components
│   │   ├── locales/      # Translations
│   │   └── App.tsx       # Main application
│   ├── package.json      # Node dependencies
│   └── vite.config.ts    # Vite configuration
└── README.md
```

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm run test
```

### Building for Production

Backend:
```bash
cd backend
# The backend doesn't require a build step
# Deploy using gunicorn or uvicorn
```

Frontend:
```bash
cd frontend
npm run build
# Output will be in the dist/ directory
```

## Data Import

### Students CSV Format
```csv
first_name,last_name,class_name,student_id,birth_date,email,phone
John,Doe,6A,ST001,2010-05-15,john.doe@example.com,1234567890
```

### Competences CSV Format
```csv
code,name,description,subject
C1,Reading Comprehension,Understand written texts,French
C2,Problem Solving,Solve mathematical problems,Math
```

### Timetable ICS
Provide a URL to an ICS file (calendar format) to import your timetable.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

This is an educational project. Feel free to fork and modify for your own needs.

## Support

For issues and questions, please open an issue on the GitHub repository.
