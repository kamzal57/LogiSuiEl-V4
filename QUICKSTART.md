# Quick Start Guide - LogiSuiEl V4

This guide will help you get the application up and running in minutes.

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

## Step 1: Clone the Repository

```bash
git clone https://github.com/kamzal57/LogiSuiEl-V4.git
cd LogiSuiEl-V4
```

## Step 2: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database with sample data:
```bash
python -m app.seed
```

This will create:
- Admin user: `admin` / `admin`
- Teacher user: `test` / `test`
- Sample students and competencies
- Sample schedule events and reminders

5. Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API Documentation (Swagger): http://localhost:8000/docs

## Step 3: Frontend Setup

Open a new terminal window:

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at: http://localhost:5173

## Step 4: Access the Application

1. Open your browser and go to http://localhost:5173
2. Login with one of the default accounts:
   - **Admin**: username `admin`, password `admin`
   - **Teacher**: username `test`, password `test`

## Features to Explore

### Dashboard
- View weekly schedule
- Check reminders and notes
- See upcoming appointments
- Review recent incidents

### Students
- List all students
- Import students from CSV (see `examples/students.csv`)
- Add incidents and evaluations for students

### Schedule
- View schedule events
- Import schedule from ICS URL
- Create new events

### Evaluations
- Track student grades
- Manage competencies
- Generate reports

### Protocols
- Manage PAI, PAP, PPS protocols
- Track student-specific accommodations

## API Testing

You can test the API using the interactive documentation:
1. Go to http://localhost:8000/docs
2. Click "Authorize" and login with admin/admin
3. Try the various endpoints

Example API calls:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"

# Get students (use the token from login)
curl http://localhost:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Importing Data

### Students CSV
1. Prepare a CSV file with columns: `first_name, last_name, date_of_birth, class_name, student_id, email, phone, address, parent_name, parent_email, parent_phone, medical_info`
2. See `examples/students.csv` for a template
3. Use the API endpoint `POST /api/students/import` to upload

### Competencies CSV
1. Prepare a CSV file with columns: `code, name, description, category, level`
2. See `examples/competences.csv` for a template
3. Use the API endpoint `POST /api/competences/import` to upload

### Schedule ICS
1. Get the URL of an ICS calendar file
2. Use the API endpoint `POST /api/schedule/import-ics?url=YOUR_ICS_URL`

## Troubleshooting

### Backend won't start
- Make sure Python 3.9+ is installed: `python --version`
- Check if port 8000 is already in use
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Check if port 5173 is already in use
- Try deleting `node_modules` and running `npm install` again

### Database issues
- Delete `logisuiel.db` and run `python -m app.seed` again
- Make sure the backend directory has write permissions

## Next Steps

- Customize the application settings
- Import your own student data
- Configure your school information
- Set up your schedule
- Explore the API documentation

## Support

For issues and questions, please open an issue on GitHub:
https://github.com/kamzal57/LogiSuiEl-V4/issues
