import csv
from io import StringIO
from typing import List, Dict
from datetime import datetime


def parse_students_csv(content: str) -> List[Dict]:
    """Parse students CSV content."""
    students = []
    errors = []
    
    csv_file = StringIO(content)
    reader = csv.DictReader(csv_file)
    
    for row_num, row in enumerate(reader, start=2):
        try:
            student = {
                "first_name": row.get("first_name", row.get("prenom", "")),
                "last_name": row.get("last_name", row.get("nom", "")),
                "class_name": row.get("class_name", row.get("classe", "")),
                "email": row.get("email", ""),
                "parent_contact": row.get("parent_contact", row.get("contact_parent", "")),
                "notes": row.get("notes", "")
            }
            
            # Parse date of birth if present
            dob = row.get("date_of_birth", row.get("date_naissance", ""))
            if dob:
                try:
                    student["date_of_birth"] = datetime.strptime(dob, "%Y-%m-%d")
                except ValueError:
                    pass
            
            students.append(student)
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return students, errors


def parse_competences_csv(content: str) -> List[Dict]:
    """Parse competences CSV content."""
    competences = []
    errors = []
    
    csv_file = StringIO(content)
    reader = csv.DictReader(csv_file)
    
    for row_num, row in enumerate(reader, start=2):
        try:
            competence = {
                "code": row.get("code", ""),
                "name": row.get("name", row.get("nom", "")),
                "description": row.get("description", ""),
                "category": row.get("category", row.get("categorie", ""))
            }
            competences.append(competence)
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return competences, errors
