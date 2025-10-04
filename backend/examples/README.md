# Example CSV Files

This directory contains example CSV files for testing the import functionality of LogiSuiEl-V4.

## Students CSV (students.csv)

Import students with the following command:

```bash
curl -X POST "http://localhost:8000/api/students/import" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@examples/students.csv"
```

### Format

- `first_name`: Student's first name
- `last_name`: Student's last name
- `class_name`: Class identifier (e.g., 6A, 5B)
- `email`: Student's email address (optional)
- `parent_contact`: Parent phone number (optional)
- `date_of_birth`: Birth date in YYYY-MM-DD format (optional)

## Competences CSV (competences.csv)

Import competences/skills with the following command:

```bash
curl -X POST "http://localhost:8000/api/evaluations/competences/import" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@examples/competences.csv"
```

### Format

- `code`: Unique competence code (e.g., F1.1, M2.1)
- `name`: Competence name
- `description`: Detailed description
- `category`: Subject or category (e.g., Français, Mathématiques)

## Getting an Access Token

First, authenticate to get a token:

```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -d "username=admin&password=admin"
```

The response will include an `access_token` that you can use in subsequent requests.
