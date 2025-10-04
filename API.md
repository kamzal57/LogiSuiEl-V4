# API Documentation - LogiSuiEl V4

Base URL: `http://localhost:8000/api/v1`

## 🔐 Authentication

All endpoints (except `/auth/token`) require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### POST /auth/token
Login to get access and refresh tokens.

**Request Body (form-data):**
```
username: string
password: string
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### GET /auth/me
Get current user information.

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "ADMIN",
  "is_active": true
}
```

### GET /auth/preferences
Get current user preferences.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "class_mode": false,
  "language": "fr",
  "theme": "light",
  "widgets_enabled": null,
  "settings": null
}
```

### PUT /auth/preferences
Update user preferences.

**Query Parameters:**
- `class_mode`: boolean (optional)
- `language`: string (optional)
- `theme`: string (optional)
- `widgets_enabled`: string (optional)
- `settings`: string (optional)

## 👥 Students

### GET /students
Get list of students.

**Query Parameters:**
- `class_name`: string (optional) - Filter by class

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "Jean",
    "last_name": "Dupont",
    "date_of_birth": "2010-05-15",
    "class_name": "6ème A",
    "student_id": "STU001",
    "email": "jean@example.com",
    "phone": null,
    "address": null,
    "parent_name": "M. Dupont",
    "parent_email": "parent@example.com",
    "parent_phone": "0612345678",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

### GET /students/{student_id}
Get a specific student.

### POST /students
Create a new student (Admin only).

**Request Body:**
```json
{
  "first_name": "Marie",
  "last_name": "Martin",
  "date_of_birth": "2010-08-22",
  "class_name": "6ème A",
  "student_id": "STU002",
  "email": "marie@example.com",
  "parent_name": "Mme Martin",
  "parent_email": "parent.martin@example.com",
  "parent_phone": "0623456789"
}
```

### PUT /students/{student_id}
Update a student (Admin only).

### DELETE /students/{student_id}
Delete a student (Admin only).

### POST /students/import
Import students from CSV file (Admin only).

**Request (multipart/form-data):**
```
file: students.csv
```

**CSV Format:**
```csv
first_name,last_name,class_name,student_id,email,date_of_birth,parent_name,parent_email,parent_phone
```

## 📚 Competences

### GET /competences
Get list of competences.

**Query Parameters:**
- `category`: string (optional) - Filter by category

### POST /competences
Create a new competence (Admin only).

**Request Body:**
```json
{
  "code": "MATH-01",
  "name": "Résoudre des problèmes",
  "description": "Résoudre des problèmes simples",
  "category": "Mathématiques",
  "level": 1
}
```

### POST /competences/import
Import competences from CSV file (Admin only).

**CSV Format:**
```csv
code,name,description,category,level
```

## 📅 Schedule

### GET /schedule
Get timetable events.

**Query Parameters:**
- `week_type`: string (optional) - A, B, or null

### POST /schedule
Create a timetable event (Admin only).

**Request Body:**
```json
{
  "title": "Mathématiques",
  "class_name": "6ème A",
  "location": "Salle 101",
  "start_time": "2024-01-15T08:00:00",
  "end_time": "2024-01-15T09:00:00",
  "day_of_week": 0,
  "week_type": "A",
  "is_recurring": true,
  "color": "#1976d2"
}
```

### POST /schedule/import-ics
Import schedule from ICS URL (Admin only).

**Request Body:**
```json
{
  "url": "https://example.com/calendar.ics"
}
```

## 📊 Dashboard

### GET /dashboard
Get dashboard overview data.

**Response:**
```json
{
  "timetable": [...],
  "reminders": [...],
  "recent_incidents": [...]
}
```

## 🏫 School Life

### GET /school-life/evaluations
Get evaluations.

**Query Parameters:**
- `student_id`: number (optional)
- `period`: string (optional)

### POST /school-life/evaluations
Create an evaluation.

**Request Body:**
```json
{
  "student_id": 1,
  "competence_id": 1,
  "score": 15.5,
  "note": "A",
  "period": "Trimestre 1",
  "comment": "Très bon travail"
}
```

### GET /school-life/incidents
Get incidents.

**Query Parameters:**
- `student_id`: number (optional)
- `type`: string (optional)
- `resolved`: boolean (optional)

### POST /school-life/incidents
Create an incident.

**Request Body:**
```json
{
  "student_id": 1,
  "type": "chatting",
  "description": "Bavardage répété en classe",
  "severity": 2
}
```

### GET /school-life/attendance
Get attendance records.

**Query Parameters:**
- `student_id`: number (optional)

### POST /school-life/attendance
Create an attendance record.

**Request Body:**
```json
{
  "student_id": 1,
  "date": "2024-01-15",
  "status": "absent",
  "note": "Absence justifiée"
}
```

## 🪑 Seating Plan

### GET /seating
Get seating plan.

**Query Parameters:**
- `class_name`: string (optional)

### POST /seating
Create or update seat assignment.

**Request Body:**
```json
{
  "student_id": 1,
  "class_name": "6ème A",
  "row": 1,
  "column": 2
}
```

## 📋 Protocols

### GET /protocols
Get protocols (PAI, PAP, etc.).

**Query Parameters:**
- `student_id`: number (optional)
- `is_active`: boolean (optional)

### POST /protocols
Create a protocol.

**Request Body:**
```json
{
  "student_id": 1,
  "type": "PAI",
  "title": "Allergie aux arachides",
  "description": "Allergie sévère",
  "actions": "{\"emergency\": \"Appeler SAMU\"}",
  "start_date": "2024-01-01",
  "is_active": true
}
```

## 🔑 Roles and Permissions

### ADMIN Role
- Full access to all endpoints
- Can create, update, delete all resources
- Can import CSV and ICS files
- Can manage users

### TEACHER Role
- Read access to all resources
- Can create and update evaluations
- Can create incidents and attendance
- Can view dashboard and reports
- Cannot delete resources
- Cannot import files

## 📝 Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 🧪 Testing with cURL

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

### Get Students
```bash
curl -X GET "http://localhost:8000/api/v1/students" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Student
```bash
curl -X POST "http://localhost:8000/api/v1/students" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Student",
    "class_name": "6ème A",
    "student_id": "TEST001"
  }'
```

## 📖 Interactive Documentation

Once the backend is running, access interactive documentation at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc
