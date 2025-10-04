# LogiSuiEl-V4 API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Default Accounts

- **Admin**: username: `admin`, password: `admin`
- **Teacher**: username: `test`, password: `test`

## API Endpoints

### Authentication

#### POST /api/auth/token
Login to get access and refresh tokens.

**Request Body (form-data):**
```
username: admin
password: admin
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### GET /api/auth/me
Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@logisuiel.local",
  "role": "ADMIN",
  "full_name": "Administrator",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### POST /api/auth/refresh
Refresh access token.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

### Students

#### GET /api/students/
List all students with pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "Jean",
    "last_name": "Dupont",
    "class_name": "6A",
    "email": "jean.dupont@ecole.fr",
    "parent_contact": "0601020304",
    "date_of_birth": "2012-05-15T00:00:00",
    "notes": null,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### POST /api/students/
Create a new student.

**Request Body:**
```json
{
  "first_name": "Jean",
  "last_name": "Dupont",
  "class_name": "6A",
  "email": "jean.dupont@ecole.fr",
  "parent_contact": "0601020304",
  "date_of_birth": "2012-05-15"
}
```

#### GET /api/students/{student_id}
Get a specific student by ID.

#### PUT /api/students/{student_id}
Update a student.

#### DELETE /api/students/{student_id}
Delete a student.

#### POST /api/students/import
Import students from CSV file.

**Request Body (multipart/form-data):**
```
file: <students.csv>
```

**Response:**
```json
{
  "success": true,
  "imported_count": 10,
  "errors": []
}
```

#### POST /api/students/{student_id}/incidents
Create an incident for a student.

**Request Body:**
```json
{
  "student_id": 1,
  "type": "retard",
  "is_positive": false,
  "description": "Arrivé 10 minutes en retard",
  "severity": 1
}
```

#### GET /api/students/{student_id}/incidents
Get all incidents for a specific student.

---

### Schedule

#### GET /api/schedule/
List schedule events with optional date filtering.

**Query Parameters:**
- `start_date` (optional): Filter events after this date (ISO format)
- `end_date` (optional): Filter events before this date (ISO format)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Cours de Mathématiques",
    "description": "Chapitre 3: Géométrie",
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T10:00:00",
    "location": "Salle 101",
    "class_name": "6A",
    "event_type": "course",
    "recurrence": null,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### POST /api/schedule/
Create a new schedule event.

#### DELETE /api/schedule/{event_id}
Delete a schedule event.

#### POST /api/schedule/import-ics
Import schedule from ICS file URL.

**Request Body:**
```json
{
  "url": "https://example.com/calendar.ics"
}
```

**Response:**
```json
{
  "success": true,
  "imported_count": 25,
  "errors": []
}
```

---

### Dashboard

#### GET /api/dashboard/
Get dashboard data with upcoming events, reminders, and recent incidents.

**Response:**
```json
{
  "timetable_events": [...],
  "reminders": [...],
  "recent_incidents": [...]
}
```

---

### Seating Plan

#### GET /api/seating/
List seat assignments with optional class filter.

**Query Parameters:**
- `class_name` (optional): Filter by class name

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "class_name": "6A",
    "row": 1,
    "column": 1,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### POST /api/seating/
Create or update a seat assignment.

**Request Body:**
```json
{
  "student_id": 1,
  "class_name": "6A",
  "row": 2,
  "column": 3
}
```

#### DELETE /api/seating/{seat_id}
Delete a seat assignment.

---

### Evaluations

#### GET /api/evaluations/competences
List all competences.

#### POST /api/evaluations/competences
Create a new competence.

**Request Body:**
```json
{
  "code": "F1.1",
  "name": "Comprendre un texte",
  "description": "Extraire des informations",
  "category": "Français"
}
```

#### POST /api/evaluations/competences/import
Import competences from CSV file.

#### GET /api/evaluations/
List evaluations with optional student filter.

**Query Parameters:**
- `student_id` (optional): Filter by student ID

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "competence_id": 1,
    "type": "competence",
    "value": 4.0,
    "grade": "A",
    "comment": "Très bon travail",
    "date": "2024-01-15T00:00:00",
    "period": "Trimestre 1"
  }
]
```

#### POST /api/evaluations/
Create a new evaluation.

---

### Protocols

#### GET /api/protocols/
List protocols with optional type filter.

**Query Parameters:**
- `protocol_type` (optional): Filter by protocol type (PAI, PAP, PPS)

#### POST /api/protocols/
Create a new protocol.

**Request Body:**
```json
{
  "student_id": 1,
  "type": "PAI",
  "title": "Protocole allergies",
  "description": "Allergies alimentaires",
  "actions": [
    "Éviter les fruits à coque",
    "Trousse d'urgence disponible"
  ],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

#### GET /api/protocols/{protocol_id}
Get a specific protocol.

#### DELETE /api/protocols/{protocol_id}
Delete a protocol.

---

### Configuration

#### GET /api/config/
List all configuration entries.

**Response:**
```json
[
  {
    "id": 1,
    "key": "school_name",
    "value": "École Exemple",
    "description": "Nom de l'établissement",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### GET /api/config/{key}
Get a specific configuration value.

#### POST /api/config/
Create a new configuration entry (Admin only).

#### PUT /api/config/{key}
Update a configuration entry (Admin only).

#### DELETE /api/config/{key}
Delete a configuration entry (Admin only).

---

### Reminders

#### GET /api/reminders/
List user's reminders.

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Réunion parents",
    "description": "Réunion de rentrée",
    "due_date": "2024-09-15T18:00:00",
    "priority": 2,
    "completed": false,
    "category": "reunion",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### POST /api/reminders/
Create a new reminder.

#### PUT /api/reminders/{reminder_id}
Update a reminder.

#### DELETE /api/reminders/{reminder_id}
Delete a reminder.

---

### Reports

#### GET /api/reports/students/csv
Export students to CSV file.

**Response:** CSV file download

#### GET /api/reports/evaluations/csv
Export evaluations to CSV file.

**Query Parameters:**
- `student_id` (optional): Filter by student ID

**Response:** CSV file download

#### GET /api/reports/incidents/csv
Export incidents to CSV file.

**Response:** CSV file download

---

### System

#### GET /
Root endpoint with API information.

**Response:**
```json
{
  "message": "Welcome to LogiSuiEl School Management API",
  "version": "4.0.0",
  "docs": "/docs"
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

#### GET /docs
Interactive API documentation (Swagger UI).

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

---

## CSV File Formats

### Students CSV

```csv
first_name,last_name,class_name,email,parent_contact,date_of_birth
Jean,Dupont,6A,jean.dupont@ecole.fr,0601020304,2012-05-15
```

### Competences CSV

```csv
code,name,description,category
F1.1,Comprendre un texte,Extraire des informations,Français
```

---

## Notes

- All dates should be in ISO 8601 format
- Authentication tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Admin users have full access to all endpoints
- Teacher users have restricted access to modification endpoints
